#!/usr/bin/env python3
"""
Notion 검증 체계 — notion_validator.py v1.1

변경 이력:
  v1.1 (2026-05-20)
    - _is_iso8601(): 정규식 끝 $ 추가 → 부분 매칭 방지
    - verify_post(): float 캐스팅 TypeError 방어 처리
    - validate_and_create(): raise 후 불필요한 return None 제거
    - RICH_TEXT_LIMIT 상수화 (1990자, Notion 블록당 2000자 제한 안전 여유)
    - SCHEMA에 'c-31-weekly' 모드 추가 (EW 탐지 파이프라인 연동)

3단계 검증:
  Stage 1 (Pre-Write)  : Notion API 호출 전 페이로드 유효성 검사
  Stage 2 (Post-Write) : 쓰기 완료 후 GET으로 실제 저장값 비교
  Stage 3 (Report)     : 검증 결과를 해당 페이지에 기록

Usage (단독 실행):
    python scripts/notion_validator.py --mode pre  --payload data/ew3_result.json
    python scripts/notion_validator.py --mode post --page-id <NOTION_PAGE_ID> --payload data/ew3_result.json

Import:
    from notion_validator import validate_pre, verify_post, write_validation_report
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

try:
    from notion_client import Client as NotionClient
except ImportError:
    print("ERROR: notion-client not installed. Run: pip install notion-client")
    sys.exit(1)


# ─────────────────────────────────────────────
# 상수
# ─────────────────────────────────────────────
RICH_TEXT_LIMIT = 1990  # Notion rich_text 블록당 2000자 제한 — 안전 여유 10자


# ─────────────────────────────────────────────
# Result 구조체
# ─────────────────────────────────────────────
@dataclass
class ValidationResult:
    passed: bool
    stage: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def summary(self) -> str:
        status = "✅ PASS" if self.passed else "❌ FAIL"
        lines = [f"[{self.stage}] {status}"]
        lines += [f"  ERROR: {e}" for e in self.errors]
        lines += [f"  WARN:  {w}" for w in self.warnings]
        return "\n".join(lines)

    def raise_if_failed(self) -> None:
        if not self.passed:
            raise ValueError(f"Validation failed at {self.stage}:\n" + self.summary())


# ─────────────────────────────────────────────
# 공통 헬퍼
# ─────────────────────────────────────────────
def _is_iso8601(value: str) -> bool:
    """YYYY-MM-DD 또는 YYYY-MM-DDTHH:MM:SS 형식 확인 ($ 앵커로 부분 매칭 방지)"""
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2})?$", value or ""))


def _is_url(value: str) -> bool:
    return bool(re.match(r"^https?://", value or ""))


def _is_recent(iso_str: str, seconds: int = 60) -> bool:
    """iso_str이 현재 시각으로부터 seconds 이내인지 확인"""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return datetime.now(timezone.utc) - dt < timedelta(seconds=seconds)
    except Exception:
        return False


def _extract_title(props: dict) -> str:
    for val in props.values():
        if val.get("type") == "title":
            items = val.get("title", [])
            return items[0]["text"]["content"] if items else ""
    return ""


def _extract_number(props: dict, prop_name: str) -> Optional[float]:
    p = props.get(prop_name, {})
    return p.get("number")


def _extract_select(props: dict, prop_name: str) -> Optional[str]:
    p = props.get(prop_name, {})
    sel = p.get("select")
    return sel.get("name") if sel else None


def _extract_rich_text(props: dict, prop_name: str) -> str:
    items = props.get(prop_name, {}).get("rich_text", [])
    return items[0]["text"]["content"] if items else ""


def _extract_checkbox(props: dict, prop_name: str) -> Optional[bool]:
    return props.get(prop_name, {}).get("checkbox")


# ─────────────────────────────────────────────
# Stage 1: Pre-Write 검증
# ─────────────────────────────────────────────
# 모드별 스키마 정의
SCHEMA: Dict[str, Dict[str, Any]] = {
    "ew3-weekly": {
        "required_fields": ["gallium_qoq_delta", "germanium_qoq_delta", "lithium_qoq_delta", "pe3_score"],
        "number_ranges": {
            "gallium_qoq_delta": (-100.0, 500.0),
            "germanium_qoq_delta": (-100.0, 500.0),
            "lithium_qoq_delta": (-100.0, 500.0),
            "pe3_score": (0.0, 100.0),
        },
        "bool_fields": [],
    },
    "ga-s4-monthly": {
        "required_fields": ["total_non_cn_tons", "threshold_achieved", "s4_status", "report_month"],
        "number_ranges": {
            "total_non_cn_tons": (0.0, 10000.0),
        },
        "bool_fields": ["threshold_achieved"],
        "date_fields": ["report_month"],   # YYYY-MM 형식
        "select_fields": {"s4_status": ["ACTIVE", "INACTIVE", "MONITOR"]},
    },
    "pejv-partner-update": {
        "required_fields": ["total_non_cn_tons", "s4_status", "report_month"],
        "number_ranges": {
            "total_non_cn_tons": (0.0, 10000.0),
        },
        "bool_fields": [],
        "select_fields": {"s4_status": ["ACTIVE", "INACTIVE", "MONITOR"]},
    },
    # ── EW 탐지 파이프라인 연동 (C-31 Weekly) ──────────────────────────
    "c-31-weekly": {
        "required_fields": ["ew_signal", "ew_score", "detected_at", "domain"],
        "number_ranges": {
            "ew_score": (0.0, 100.0),
        },
        "bool_fields": ["ew_signal"],
        "date_fields": ["detected_at"],
        "select_fields": {
            "domain": [
                "semiconductor", "ai-infra", "supply-chain",
                "geopolitics", "macro", "energy",
            ],
        },
    },
}


def validate_pre(data: Dict[str, Any], mode: str) -> ValidationResult:
    """
    Stage 1: Notion에 쓰기 전 페이로드 검증
    """
    errors: List[str] = []
    warnings: List[str] = []

    schema = SCHEMA.get(mode)
    if schema is None:
        warnings.append(f"[SCHEMA] 알 수 없는 mode '{mode}' — 기본 검증만 수행")
    else:
        # 1) 필수 필드 존재 여부
        for f in schema.get("required_fields", []):
            if f not in data or data[f] is None or data[f] == "":
                errors.append(f"[MISSING] 필수 필드 누락: '{f}'")

        # 2) 숫자 범위
        for f, (lo, hi) in schema.get("number_ranges", {}).items():
            val = data.get(f)
            if val is not None:
                if not isinstance(val, (int, float)):
                    errors.append(f"[TYPE] '{f}' 숫자 타입 필요, 실제: {type(val).__name__}")
                elif not (lo <= val <= hi):
                    errors.append(f"[RANGE] '{f}' 범위 초과: {val} (허용: {lo}~{hi})")

        # 3) bool 필드
        for f in schema.get("bool_fields", []):
            val = data.get(f)
            if val is not None and not isinstance(val, bool):
                errors.append(f"[TYPE] '{f}' bool 타입 필요, 실제: {type(val).__name__}")

        # 4) select 허용값
        for f, allowed in schema.get("select_fields", {}).items():
            val = data.get(f)
            if val is not None and val not in allowed:
                errors.append(f"[SELECT] '{f}' 허용값 외 값: '{val}' (허용: {allowed})")

        # 5) 날짜 형식 (YYYY-MM 또는 ISO8601)
        for f in schema.get("date_fields", []):
            val = data.get(f, "")
            if not re.match(r"^\d{4}-\d{2}", val or ""):
                errors.append(f"[FORMAT] '{f}' 날짜 형식 불일치: '{val}'")

    # 6) URL 필드 공통 검증 (있으면)
    for key in ["source_url", "source_urls"]:
        urls = data.get(key, [])
        if isinstance(urls, str):
            urls = [urls]
        for url in urls:
            if not _is_url(url):
                warnings.append(f"[FORMAT] URL 형식 불량: '{url}'")

    # 7) 빈 데이터 경고
    if not data:
        errors.append("[EMPTY] 페이로드가 비어 있음")

    return ValidationResult(
        passed=len(errors) == 0,
        stage="PRE-WRITE",
        errors=errors,
        warnings=warnings,
    )


# ─────────────────────────────────────────────
# Stage 2: Post-Write 검증 (round-trip)
# ─────────────────────────────────────────────
def verify_post(
    notion: NotionClient,
    page_id: str,
    expected: Dict[str, Any],
    mode: str,
    staleness_seconds: int = 60,
) -> ValidationResult:
    """
    Stage 2: Notion 페이지를 GET하여 기대값과 실제 저장값 비교
    """
    errors: List[str] = []
    warnings: List[str] = []

    try:
        page = notion.pages.retrieve(page_id=page_id)
    except Exception as e:
        return ValidationResult(
            passed=False,
            stage="POST-WRITE",
            errors=[f"[API] Notion 페이지 조회 실패: {e}"],
        )

    props = page.get("properties", {})

    # staleness 확인
    edited_time = page.get("last_edited_time", "")
    if edited_time and not _is_recent(edited_time, seconds=staleness_seconds):
        warnings.append(f"[STALE] last_edited_time이 {staleness_seconds}초 초과: {edited_time}")

    # 모드별 핵심 필드 round-trip 비교
    if mode == "ew3-weekly":
        checks = {
            "Ga_Delta": (_extract_number(props, "Ga_Delta"), expected.get("gallium_qoq_delta")),
            "Ge_Delta": (_extract_number(props, "Ge_Delta"), expected.get("germanium_qoq_delta")),
            "Li_Delta": (_extract_number(props, "Li_Delta"), expected.get("lithium_qoq_delta")),
            "PE3_Score": (_extract_number(props, "PE3_Score"), expected.get("pe3_score")),
            "EW3": (_extract_checkbox(props, "EW3"), expected.get("ew3_triggered")),
        }
    elif mode in ("ga-s4-monthly", "pejv-partner-update"):
        checks = {
            "Total_Non_CN": (_extract_number(props, "Total_Non_CN"), expected.get("total_non_cn_tons")),
            "S4_Status": (_extract_select(props, "S4_Status"), expected.get("s4_status")),
        }
    elif mode == "c-31-weekly":
        checks = {
            "EW_Score": (_extract_number(props, "EW_Score"), expected.get("ew_score")),
            "EW_Signal": (_extract_checkbox(props, "EW_Signal"), expected.get("ew_signal")),
            "Domain": (_extract_select(props, "Domain"), expected.get("domain")),
        }
    else:
        checks = {}
        warnings.append(f"[SCHEMA] mode '{mode}' 에 대한 Post-Write 비교 스키마 없음 — 기본 검사만 수행")

    for field_name, (actual, exp_val) in checks.items():
        if exp_val is None:
            continue  # expected에 없으면 skip
        if actual is None:
            errors.append(f"[MISSING] Notion에서 '{field_name}' 값 없음")
        elif isinstance(exp_val, float):
            # float 비교: 0.001 허용 오차 (캐스팅 실패 방어)
            try:
                if abs(float(actual) - exp_val) > 0.001:
                    errors.append(f"[MISMATCH] '{field_name}': 기대={exp_val}, 실제={actual}")
            except (TypeError, ValueError):
                errors.append(f"[TYPE] '{field_name}' float 변환 불가: 실제={actual!r}")
        else:
            if str(actual) != str(exp_val):
                errors.append(f"[MISMATCH] '{field_name}': 기대='{exp_val}', 실제='{actual}'")

    return ValidationResult(
        passed=len(errors) == 0,
        stage="POST-WRITE",
        errors=errors,
        warnings=warnings,
    )


# ─────────────────────────────────────────────
# Stage 3: 검증 결과 Notion 페이지에 기록
# ─────────────────────────────────────────────
def write_validation_report(
    notion: NotionClient,
    page_id: str,
    results: List[ValidationResult],
) -> None:
    """
    Stage 3: 검증 통합 결과를 Notion 페이지 프로퍼티에 기록
    Notion DB에 아래 3개 필드가 있어야 함:
      - Validation Status (Select): PASS / FAIL / WARN
      - Validation Log (Rich Text)  ← 블록당 최대 2000자, RICH_TEXT_LIMIT 상수 사용
      - Validated At (Date)
    """
    all_passed = all(r.passed for r in results)
    has_warnings = any(r.warnings for r in results)

    if all_passed and not has_warnings:
        status = "PASS"
    elif all_passed and has_warnings:
        status = "WARN"
    else:
        status = "FAIL"

    log_lines: List[str] = []
    for r in results:
        log_lines.append(r.summary())
    log_text = "\n".join(log_lines)[:RICH_TEXT_LIMIT]

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")

    try:
        notion.pages.update(
            page_id=page_id,
            properties={
                "Validation Status": {"select": {"name": status}},
                "Validation Log": {
                    "rich_text": [{"type": "text", "text": {"content": log_text}}]
                },
                "Validated At": {"date": {"start": now_iso}},
            },
        )
        print(f"  📋 Validation Report 기록 완료: {status} | page_id={page_id}")
    except Exception as e:
        # 검증 필드가 없을 경우 경고만 출력 (치명적 오류 아님)
        print(f"  ⚠️  Validation Report 기록 실패 (필드 미존재 가능): {e}")


# ─────────────────────────────────────────────
# 편의 함수: validate_and_create
# ─────────────────────────────────────────────
def validate_and_create(
    notion: NotionClient,
    db_id: str,
    properties: Dict[str, Any],
    raw_payload: Dict[str, Any],
    mode: str,
    fail_on_error: bool = True,
) -> Optional[str]:
    """
    Pre-Write 검증 → DB 엔트리 생성 → Post-Write 검증 → Report 기록
    page_id 반환 (실패 시 None)
    """
    results: List[ValidationResult] = []

    # Stage 1: Pre-Write
    pre = validate_pre(raw_payload, mode)
    results.append(pre)
    print(pre.summary())
    if not pre.passed and fail_on_error:
        pre.raise_if_failed()  # raise 후 함수 종료 (return None 불필요)

    # DB 엔트리 생성
    try:
        response = notion.pages.create(
            parent={"database_id": db_id},
            properties=properties,
        )
        page_id = response["id"]
        print(f"  📝 Notion 페이지 생성: {page_id}")
    except Exception as e:
        results.append(ValidationResult(
            passed=False, stage="DB-CREATE",
            errors=[f"[API] 페이지 생성 실패: {e}"],
        ))
        if fail_on_error:
            raise
        return None

    # Stage 2: Post-Write
    post = verify_post(notion, page_id, raw_payload, mode)
    results.append(post)
    print(post.summary())

    # Stage 3: Report
    write_validation_report(notion, page_id, results)

    if not post.passed and fail_on_error:
        post.raise_if_failed()

    return page_id


# ─────────────────────────────────────────────
# CLI (단독 실행)
# ─────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description="Notion 검증 체계 v1.1")
    parser.add_argument("--mode", required=True,
                        choices=["pre", "post"],
                        help="검증 단계: pre=Pre-Write, post=Post-Write")
    parser.add_argument("--payload", required=True, help="JSON 페이로드 파일 경로")
    parser.add_argument("--schema-mode", default="ew3-weekly",
                        choices=list(SCHEMA.keys()),
                        help=f"스키마 모드 ({' / '.join(SCHEMA.keys())})")
    parser.add_argument("--page-id", default="",
                        help="Post-Write 검증 대상 Notion 페이지 ID")
    parser.add_argument("--fail-on-error", action="store_true",
                        help="에러 시 exit code 1 반환")
    args = parser.parse_args()

    with open(args.payload) as f:
        payload = json.load(f)

    if args.mode == "pre":
        result = validate_pre(payload, args.schema_mode)
        print(result.summary())
        if not result.passed and args.fail_on_error:
            sys.exit(1)

    elif args.mode == "post":
        if not args.page_id:
            print("ERROR: --page-id 필요 (Post-Write 모드)")
            sys.exit(1)
        api_key = os.environ.get("NOTION_API_KEY", "")
        if not api_key:
            print("ERROR: NOTION_API_KEY 환경변수 없음")
            sys.exit(1)
        notion = NotionClient(auth=api_key)
        result = verify_post(notion, args.page_id, payload, args.schema_mode)
        print(result.summary())
        if not result.passed and args.fail_on_error:
            sys.exit(1)


if __name__ == "__main__":
    main()
