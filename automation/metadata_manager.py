#!/usr/bin/env python3
"""
metadata_manager.py — PE-7 v2.9 PHASE 1 핵심 모듈

C-01 해결: update_content(old_str exact match) → replace_content(section-level) 전면 전환
PE-7 v2.9 표준 S1~S4 완전 적용
SSO 동기화 성공률: 30% → 95% 목표

Author: GilbertKwak PE System
Version: 1.0.0 (PE-7 v2.9)
Created: 2026-05-06
"""

import os
import json
import hashlib
import time
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, List, Tuple, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict, field

import requests

# ─────────────────────────────────────────────
# 설정
# ─────────────────────────────────────────────
NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION  = "2022-06-28"
METADATA_STORE  = os.path.join(os.path.dirname(__file__), "..", "logs", "section_metadata")
MAX_WORKERS     = 5      # 병렬 처리 최대 스레드
RETRY_LIMIT     = 3      # API 호출 재시도 횟수
POST_UPDATE_WAIT = 3.0   # PE-7 v2.9 S4: 업데이트 후 검증 대기(초)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("metadata_manager")

os.makedirs(METADATA_STORE, exist_ok=True)


# ─────────────────────────────────────────────
# 데이터 구조
# ─────────────────────────────────────────────
@dataclass
class SectionMeta:
    section_id:       str
    heading:          str
    heading_level:    int           # 1=H1, 2=H2, 3=H3
    heading_block_id: str
    content_hash:     str
    last_synced:      str
    sync_status:      str           # synced | stale | error | unknown
    block_count:      int = 0
    char_count:       int = 0
    error_log:        List[str] = field(default_factory=list)


@dataclass
class PageMetadata:
    page_id:     str
    page_title:  str
    schema_ver:  str = "PE-7-v2.9"
    created_at:  str = ""
    updated_at:  str = ""
    sections:    List[SectionMeta] = field(default_factory=list)

    def section_by_id(self, section_id: str) -> Optional[SectionMeta]:
        for s in self.sections:
            if s.section_id == section_id:
                return s
        return None

    def section_by_heading(self, heading: str) -> Optional[SectionMeta]:
        for s in self.sections:
            if s.heading.strip() == heading.strip():
                return s
        return None


# ─────────────────────────────────────────────
# Notion API 헬퍼
# ─────────────────────────────────────────────
def _notion_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }


def _api_call(
    method: str,
    url: str,
    token: str,
    payload: Optional[Dict] = None,
    retry: int = RETRY_LIMIT,
) -> Dict:
    """재시도 로직 포함 Notion API 호출 래퍼."""
    headers = _notion_headers(token)
    for attempt in range(1, retry + 1):
        try:
            resp = requests.request(
                method,
                url,
                headers=headers,
                json=payload,
                timeout=30,
            )
            if resp.status_code == 429:  # Rate limit
                wait = int(resp.headers.get("Retry-After", 5))
                logger.warning(f"Rate limit — {wait}초 대기 (시도 {attempt}/{retry})")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            logger.error(f"API 호출 실패 (시도 {attempt}/{retry}): {e}")
            if attempt == retry:
                raise
            time.sleep(2 ** attempt)  # exponential backoff
    return {}


def _fetch_all_blocks(page_id: str, token: str) -> List[Dict]:
    """페이지의 모든 블록을 페이지네이션으로 가져온다."""
    blocks: List[Dict] = []
    url = f"{NOTION_API_BASE}/blocks/{page_id}/children"
    cursor = None
    while True:
        params = {"page_size": 100}
        if cursor:
            params["start_cursor"] = cursor
        data = _api_call("GET", url + "?" + "&".join(f"{k}={v}" for k, v in params.items()), token)
        blocks.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
    return blocks


# ─────────────────────────────────────────────
# [S4] 무결성 해시
# ─────────────────────────────────────────────
def calculate_section_hash(content_blocks: List[Dict]) -> str:
    """
    PE-7 v2.9 S4: 섹션 블록 리스트를 SHA-256으로 해싱.
    텍스트 내용만 추출하여 포맷 노이즈 제거.
    """
    text_parts: List[str] = []
    for block in content_blocks:
        btype = block.get("type", "")
        bdata = block.get(btype, {})
        rich_texts = bdata.get("rich_text", [])
        for rt in rich_texts:
            text_parts.append(rt.get("plain_text", ""))
    raw = "\n".join(text_parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# ─────────────────────────────────────────────
# [PHASE 1-A] initialize_section_metadata
# ─────────────────────────────────────────────
def initialize_section_metadata(
    page_id: str,
    token: str,
    page_title: str = "",
    force_refresh: bool = False,
) -> PageMetadata:
    """
    PE-7 v2.9 PHASE 1: 페이지의 모든 섹션 자동 스캔 및 메타데이터 초기화.

    - 각 heading 블록을 섹션 경계로 인식
    - heading_block_id 수집 (section-level replace_content 타겟팅용)
    - content_hash 계산 (변경 감지용)
    - 로컬 JSON 캐시에 저장

    Args:
        page_id:       Notion 페이지 UUID
        token:         Notion API 토큰
        page_title:    페이지 제목 (로깅용)
        force_refresh: 캐시 무시하고 강제 재스캔

    Returns:
        PageMetadata 객체
    """
    cache_path = os.path.join(METADATA_STORE, f"{page_id}.json")

    # 캐시 로드 (force_refresh=False 일 때)
    if not force_refresh and os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            meta = _deserialize_metadata(raw)
            logger.info(f"[INIT] 캐시 로드: {page_id} ({len(meta.sections)}섹션)")
            return meta
        except Exception as e:
            logger.warning(f"[INIT] 캐시 파손 — 재스캔: {e}")

    logger.info(f"[INIT] 섹션 스캔 시작: page={page_id}")
    blocks = _fetch_all_blocks(page_id, token)

    # 섹션 파싱
    sections: List[SectionMeta] = []
    current_heading_block: Optional[Dict] = None
    current_content_blocks: List[Dict] = []
    section_counter = 0

    HEADING_TYPES = {"heading_1": 1, "heading_2": 2, "heading_3": 3}

    def _flush_section():
        nonlocal section_counter
        if current_heading_block is None:
            return
        btype = current_heading_block["type"]
        heading_text = "".join(
            rt.get("plain_text", "")
            for rt in current_heading_block[btype].get("rich_text", [])
        )
        section_counter += 1
        sec_id = f"SEC-{page_id[:8].upper()}-{section_counter:03d}"
        h = calculate_section_hash(current_content_blocks)
        total_chars = sum(
            len(rt.get("plain_text", ""))
            for b in current_content_blocks
            for rt in b.get(b["type"], {}).get("rich_text", [])
        )
        sections.append(SectionMeta(
            section_id=sec_id,
            heading=heading_text,
            heading_level=HEADING_TYPES.get(btype, 2),
            heading_block_id=current_heading_block["id"],
            content_hash=h,
            last_synced=_now_iso(),
            sync_status="synced",
            block_count=len(current_content_blocks),
            char_count=total_chars,
        ))

    for block in blocks:
        btype = block.get("type", "")
        if btype in HEADING_TYPES:
            _flush_section()
            current_heading_block = block
            current_content_blocks = []
        else:
            current_content_blocks.append(block)

    _flush_section()  # 마지막 섹션

    # 제목 미발견 시 전체를 단일 섹션으로
    if not sections and blocks:
        logger.warning("[INIT] 헤딩 없음 — 전체를 단일 섹션으로 처리")
        h = calculate_section_hash(blocks)
        sections.append(SectionMeta(
            section_id=f"SEC-{page_id[:8].upper()}-000",
            heading="(전체 페이지)",
            heading_level=0,
            heading_block_id=page_id,
            content_hash=h,
            last_synced=_now_iso(),
            sync_status="synced",
            block_count=len(blocks),
            char_count=0,
        ))

    meta = PageMetadata(
        page_id=page_id,
        page_title=page_title or page_id,
        created_at=_now_iso(),
        updated_at=_now_iso(),
        sections=sections,
    )

    _save_metadata(meta)
    logger.info(f"[INIT] 완료: {len(sections)}섹션 스캔 — page={page_id}")
    return meta


# ─────────────────────────────────────────────
# [PHASE 1-B] update_section_by_metadata
# ─────────────────────────────────────────────
def update_section_by_metadata(
    page_id: str,
    section_id_or_heading: str,
    new_content_blocks: List[Dict],
    token: str,
) -> Dict[str, Any]:
    """
    PE-7 v2.9 S1: heading_block_id로 직접 타겟팅하여 섹션 교체.
    update_content(old_str) 방식 완전 대체.

    전략:
    1. 메타데이터에서 heading_block_id 조회
    2. 해당 heading 다음 ~ 다음 heading 사이의 모든 블록 삭제
    3. new_content_blocks 순차 추가
    4. S4: 3초 대기 후 content_hash 검증

    Args:
        page_id:               Notion 페이지 UUID
        section_id_or_heading: SectionMeta.section_id 또는 heading 텍스트
        new_content_blocks:    교체할 새 블록 리스트 (Notion block format)
        token:                 Notion API 토큰

    Returns:
        결과 dict: {success, section_id, blocks_written, hash_verified, error}
    """
    result: Dict[str, Any] = {
        "success": False,
        "section_id": section_id_or_heading,
        "blocks_written": 0,
        "hash_verified": False,
        "error": None,
    }

    # 1. 메타데이터 로드
    meta = _load_metadata(page_id)
    if meta is None:
        result["error"] = f"메타데이터 없음 — initialize_section_metadata() 먼저 실행"
        logger.error(result["error"])
        return result

    # 2. 섹션 탐색
    section = meta.section_by_id(section_id_or_heading) or meta.section_by_heading(section_id_or_heading)
    if section is None:
        # Fallback: fuzzy match
        section = _fuzzy_find_section(meta, section_id_or_heading)
        if section:
            logger.warning(f"[UPDATE] Fuzzy match 사용: '{section_id_or_heading}' → '{section.heading}'")
        else:
            result["error"] = f"섹션 미발견: '{section_id_or_heading}' — 수동 확인 필요"
            logger.error(result["error"])
            return result

    heading_block_id = section.heading_block_id
    logger.info(f"[UPDATE] 섹션 교체 시작: '{section.heading}' (block={heading_block_id})")

    try:
        # 3. 현재 블록 조회 (heading 이후 섹션 범위)
        all_blocks = _fetch_all_blocks(page_id, token)
        blocks_to_delete = _get_section_content_blocks(all_blocks, heading_block_id)

        # 4. 기존 콘텐츠 블록 삭제
        for blk in blocks_to_delete:
            _api_call("DELETE", f"{NOTION_API_BASE}/blocks/{blk['id']}", token)

        # 5. 새 블록 추가 (heading 뒤에 삽입) — 500자 단위 자동 분할
        chunks = _split_blocks(new_content_blocks, chunk_size=90)  # API 100-block limit 대비
        blocks_written = 0
        for chunk in chunks:
            payload = {"children": chunk, "after": heading_block_id}
            _api_call(
                "PATCH",
                f"{NOTION_API_BASE}/blocks/{page_id}/children",
                token,
                payload,
            )
            blocks_written += len(chunk)
            time.sleep(0.3)  # rate limit 예방

        result["blocks_written"] = blocks_written

        # 6. S4: 검증 (3초 대기 후 hash 비교)
        time.sleep(POST_UPDATE_WAIT)
        refreshed_blocks = _fetch_all_blocks(page_id, token)
        refreshed_section_blocks = _get_section_content_blocks(refreshed_blocks, heading_block_id)
        new_hash = calculate_section_hash(new_content_blocks)
        refreshed_hash = calculate_section_hash(refreshed_section_blocks)
        result["hash_verified"] = (new_hash == refreshed_hash)

        if result["hash_verified"]:
            logger.info(f"[UPDATE] ✅ 검증 통과: '{section.heading}'")
            section.content_hash = new_hash
            section.last_synced = _now_iso()
            section.sync_status = "synced"
            section.block_count = blocks_written
        else:
            logger.warning(f"[UPDATE] ⚠️ Hash 불일치: '{section.heading}' — 재검토 필요")
            section.sync_status = "stale"

        meta.updated_at = _now_iso()
        _save_metadata(meta)
        result["success"] = True

    except Exception as e:
        result["error"] = str(e)
        section.sync_status = "error"
        section.error_log.append(f"{_now_iso()}: {e}")
        _save_metadata(meta)
        logger.error(f"[UPDATE] 실패: {e}")

    return result


# ─────────────────────────────────────────────
# [PHASE 1-C] validate_metadata_integrity
# ─────────────────────────────────────────────
def validate_metadata_integrity(
    page_id: str,
    token: str,
) -> Dict[str, Any]:
    """
    PE-7 v2.9 S2: 동기화 전 메타데이터 정합성 검증.

    검증 항목:
    - 모든 heading_block_id가 실제 Notion 블록에 존재하는지
    - content_hash 일치 여부 (변경 감지)
    - 섹션 누락/추가 감지

    Returns:
        {valid, stale_sections, missing_sections, new_sections, detail}
    """
    report: Dict[str, Any] = {
        "valid": True,
        "stale_sections": [],
        "missing_sections": [],
        "new_sections": [],
        "detail": [],
    }

    meta = _load_metadata(page_id)
    if meta is None:
        report["valid"] = False
        report["detail"].append("메타데이터 파일 없음 — initialize_section_metadata() 실행 필요")
        return report

    # 현재 Notion 블록 스캔
    live_blocks = _fetch_all_blocks(page_id, token)
    live_heading_ids = {
        b["id"]: b for b in live_blocks
        if b.get("type", "") in {"heading_1", "heading_2", "heading_3"}
    }

    # 메타데이터 섹션 검증
    known_ids = {s.heading_block_id for s in meta.sections}
    for section in meta.sections:
        hid = section.heading_block_id
        if hid not in live_heading_ids:
            report["missing_sections"].append(section.section_id)
            report["valid"] = False
            report["detail"].append(f"[MISSING] '{section.heading}' (block={hid}) — Notion에서 삭제됨")
            continue

        # Hash 비교
        live_content = _get_section_content_blocks(live_blocks, hid)
        live_hash = calculate_section_hash(live_content)
        if live_hash != section.content_hash:
            report["stale_sections"].append(section.section_id)
            report["detail"].append(
                f"[STALE] '{section.heading}' — hash 불일치 (cached vs live)"
            )

    # 신규 섹션 감지 (메타데이터에 없는 heading)
    for hid, blk in live_heading_ids.items():
        if hid not in known_ids:
            btype = blk["type"]
            heading_text = "".join(
                rt.get("plain_text", "")
                for rt in blk[btype].get("rich_text", [])
            )
            report["new_sections"].append(heading_text)
            report["detail"].append(f"[NEW] 미등록 섹션 발견: '{heading_text}' (block={hid})")

    if report["stale_sections"] or report["new_sections"]:
        report["valid"] = False

    logger.info(
        f"[VALIDATE] page={page_id} | valid={report['valid']} | "
        f"stale={len(report['stale_sections'])} | missing={len(report['missing_sections'])} | "
        f"new={len(report['new_sections'])}"
    )
    return report


# ─────────────────────────────────────────────
# [PHASE 1-D] 병렬 섹션 업데이트
# ─────────────────────────────────────────────
def parallel_section_update(
    page_id: str,
    updates: List[Dict[str, Any]],  # [{section_id_or_heading, new_content_blocks}, ...]
    token: str,
    max_workers: int = MAX_WORKERS,
) -> List[Dict[str, Any]]:
    """
    대용량 페이지 섹션 병렬 업데이트.
    각 update: {section_id_or_heading: str, new_content_blocks: List[Dict]}
    """
    logger.info(f"[PARALLEL] {len(updates)}개 섹션 병렬 처리 시작 (workers={max_workers})")
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                update_section_by_metadata,
                page_id,
                u["section_id_or_heading"],
                u["new_content_blocks"],
                token,
            ): u["section_id_or_heading"]
            for u in updates
        }
        for future in as_completed(futures):
            sid = futures[future]
            try:
                res = future.result()
                results.append(res)
                status = "✅" if res["success"] else "❌"
                logger.info(f"[PARALLEL] {status} '{sid}'")
            except Exception as e:
                results.append({"success": False, "section_id": sid, "error": str(e)})
                logger.error(f"[PARALLEL] 실패 '{sid}': {e}")

    success_count = sum(1 for r in results if r["success"])
    logger.info(f"[PARALLEL] 완료: {success_count}/{len(updates)} 성공")
    return results


# ─────────────────────────────────────────────
# [PHASE 1-E] 오류 사전 예측기
# ─────────────────────────────────────────────
def error_predictor(
    page_id: str,
    proposed_updates: List[Dict[str, Any]],
    token: str,
) -> Dict[str, Any]:
    """
    PE-7 v2.9 S3: 실행 전 오류 예측 및 대안 제시.

    예측 항목:
    - 섹션 미발견 위험
    - 블록 수 초과 위험 (100-block limit)
    - 중복 heading 위험
    - API rate limit 위험
    - 메타데이터 stale 위험

    Returns:
        {safe_to_proceed, risks, alternatives, pre_fix_actions}
    """
    report = {
        "safe_to_proceed": True,
        "risks": [],
        "alternatives": [],
        "pre_fix_actions": [],
    }

    meta = _load_metadata(page_id)
    if meta is None:
        report["safe_to_proceed"] = False
        report["risks"].append("[R-01] 메타데이터 없음")
        report["alternatives"].append("initialize_section_metadata() 먼저 실행")
        return report

    # 섹션 식별 위험
    for upd in proposed_updates:
        sid = upd.get("section_id_or_heading", "")
        found = meta.section_by_id(sid) or meta.section_by_heading(sid)
        if not found:
            fuzzy = _fuzzy_find_section(meta, sid)
            if fuzzy:
                report["risks"].append(f"[R-02] 정확 매칭 실패: '{sid}' — fuzzy: '{fuzzy.heading}'")
                report["alternatives"].append(f"'{sid}' → '{fuzzy.heading}' 사용 권장")
            else:
                report["safe_to_proceed"] = False
                report["risks"].append(f"[R-03] 섹션 미발견: '{sid}'")
                report["alternatives"].append("initialize_section_metadata(force_refresh=True) 재실행")

        # 블록 수 초과
        blocks = upd.get("new_content_blocks", [])
        if len(blocks) > 90:
            report["risks"].append(f"[R-04] '{sid}': {len(blocks)}블록 → 100-block limit 위험")
            report["alternatives"].append("parallel_section_update() 또는 _split_blocks() 사용")

    # Rate limit 위험 (한 번에 10+ 섹션)
    if len(proposed_updates) >= 10:
        report["risks"].append(f"[R-05] {len(proposed_updates)}개 동시 업데이트 → rate limit 위험")
        report["alternatives"].append("max_workers=3으로 조정 또는 배치 분할 실행")

    # Metadata stale 검증
    integrity = validate_metadata_integrity(page_id, token)
    if not integrity["valid"]:
        report["risks"].append("[R-06] 메타데이터 stale — 불일치 위험")
        report["pre_fix_actions"].append("initialize_section_metadata(force_refresh=True) 실행 후 재시도")
        if integrity["missing_sections"]:
            report["safe_to_proceed"] = False

    if report["risks"]:
        logger.warning(f"[PREDICT] {len(report['risks'])}개 위험 감지 — safe={report['safe_to_proceed']}")
    else:
        logger.info("[PREDICT] ✅ 위험 없음 — 안전 실행 가능")

    return report


# ─────────────────────────────────────────────
# 내부 유틸리티
# ─────────────────────────────────────────────
def _get_section_content_blocks(
    all_blocks: List[Dict],
    heading_block_id: str,
) -> List[Dict]:
    """heading_block_id 이후 ~ 다음 heading 전까지의 블록 리스트 반환."""
    HEADING_TYPES = {"heading_1", "heading_2", "heading_3"}
    found = False
    result = []
    for block in all_blocks:
        if block["id"] == heading_block_id:
            found = True
            continue
        if found:
            if block.get("type", "") in HEADING_TYPES:
                break
            result.append(block)
    return result


def _split_blocks(blocks: List[Dict], chunk_size: int = 90) -> List[List[Dict]]:
    """블록 리스트를 chunk_size 단위로 분할."""
    return [blocks[i:i + chunk_size] for i in range(0, len(blocks), chunk_size)]


def _fuzzy_find_section(
    meta: PageMetadata,
    query: str,
) -> Optional[SectionMeta]:
    """heading 텍스트 부분 매칭으로 섹션 탐색."""
    query_lower = query.lower()
    for s in meta.sections:
        if query_lower in s.heading.lower() or s.heading.lower() in query_lower:
            return s
    return None


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _save_metadata(meta: PageMetadata) -> None:
    cache_path = os.path.join(METADATA_STORE, f"{meta.page_id}.json")
    data = asdict(meta)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _load_metadata(page_id: str) -> Optional[PageMetadata]:
    cache_path = os.path.join(METADATA_STORE, f"{page_id}.json")
    if not os.path.exists(cache_path):
        return None
    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return _deserialize_metadata(raw)
    except Exception as e:
        logger.error(f"메타데이터 로드 실패: {e}")
        return None


def _deserialize_metadata(raw: Dict) -> PageMetadata:
    sections = [
        SectionMeta(
            section_id=s["section_id"],
            heading=s["heading"],
            heading_level=s.get("heading_level", 2),
            heading_block_id=s["heading_block_id"],
            content_hash=s["content_hash"],
            last_synced=s["last_synced"],
            sync_status=s.get("sync_status", "unknown"),
            block_count=s.get("block_count", 0),
            char_count=s.get("char_count", 0),
            error_log=s.get("error_log", []),
        )
        for s in raw.get("sections", [])
    ]
    return PageMetadata(
        page_id=raw["page_id"],
        page_title=raw.get("page_title", ""),
        schema_ver=raw.get("schema_ver", "PE-7-v2.9"),
        created_at=raw.get("created_at", ""),
        updated_at=raw.get("updated_at", ""),
        sections=sections,
    )


# ─────────────────────────────────────────────
# CLI 진입점 (테스트용)
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    token = os.environ.get("NOTION_TOKEN", "")
    if not token:
        print("❌ NOTION_TOKEN 환경변수 필요")
        sys.exit(1)

    if len(sys.argv) < 3:
        print("Usage: python metadata_manager.py <command> <page_id>")
        print("  init     <page_id>          — 섹션 메타데이터 초기화")
        print("  validate <page_id>          — 정합성 검증")
        print("  predict  <page_id>          — 오류 사전 예측")
        sys.exit(0)

    cmd = sys.argv[1]
    pid = sys.argv[2]

    if cmd == "init":
        meta = initialize_section_metadata(pid, token, force_refresh=True)
        print(json.dumps(asdict(meta), ensure_ascii=False, indent=2))
    elif cmd == "validate":
        report = validate_metadata_integrity(pid, token)
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif cmd == "predict":
        report = error_predictor(pid, [], token)
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"알 수 없는 명령: {cmd}")
        sys.exit(1)
