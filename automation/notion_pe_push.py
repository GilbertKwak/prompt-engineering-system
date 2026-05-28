#!/usr/bin/env python3
"""
notion_pe_push.py
================================================
GitHub Actions scripts/ 실행 결과를 Notion PE Hub 데이터베이스에
자동 Push하는 단방향 파이프라인.

설계 원칙:
  - GitHub = SSOT (단방향 Push, Notion은 조회·협업 UI)
  - 3-Engine (PE-FIN / PE-CON / PE-IP) 결과를 각각 별도 레코드로 적재
  - 멱등성: 동일 run_id 재실행 시 Upsert (중복 방지)

사용법 (로컬 테스트):
  export NOTION_TOKEN=secret_xxx
  export NOTION_PE_HUB_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  python automation/notion_pe_push.py \
    --results_dir output/notion-sync/ \
    --run_id run-20260528-120000 \
    --engine_scope all

GitHub Secrets 필요:
  NOTION_TOKEN         → Notion Integration Token (secret_...)
  NOTION_PE_HUB_DB_ID  → Notion DB ID (하이픈 없는 32자리)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import requests

# ──────────────────────────────────────────────
# 상수
# ──────────────────────────────────────────────
NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

# 결과 파일 → Notion 엔진 레이블 매핑
ENGINE_MAP = {
    "pe_fin_result.json": {"engine": "PE-FIN", "label": "💰 Financial Engine"},
    "pe_con_result.json": {"engine": "PE-CON", "label": "🧠 Context Engine"},
    "pe_ip_result.json":  {"engine": "PE-IP",  "label": "⚙️ IP Engine"},
}


# ──────────────────────────────────────────────
# Notion API 클라이언트
# ──────────────────────────────────────────────
class NotionClient:
    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION,
        }

    def _req(self, method: str, path: str, **kwargs) -> dict:
        url = f"{NOTION_API_BASE}{path}"
        resp = requests.request(method, url, headers=self.headers, timeout=30, **kwargs)
        if not resp.ok:
            print(f"[ERROR] Notion API {method} {path} → {resp.status_code}: {resp.text[:300]}")
            resp.raise_for_status()
        return resp.json()

    def query_db(self, db_id: str, filter_body: dict) -> list[dict]:
        """데이터베이스 쿼리 (멱등성 체크용)"""
        data = self._req("POST", f"/databases/{db_id}/query", json={"filter": filter_body})
        return data.get("results", [])

    def create_page(self, db_id: str, properties: dict, content_blocks: list) -> dict:
        """새 페이지(레코드) 생성"""
        payload = {
            "parent": {"database_id": db_id},
            "properties": properties,
            "children": content_blocks,
        }
        return self._req("POST", "/pages", json=payload)

    def update_page(self, page_id: str, properties: dict) -> dict:
        """기존 페이지 업데이트 (Upsert)"""
        return self._req("PATCH", f"/pages/{page_id}", json={"properties": properties})

    def append_blocks(self, page_id: str, blocks: list) -> dict:
        """페이지에 블록 추가"""
        return self._req("PATCH", f"/blocks/{page_id}/children", json={"children": blocks})


# ──────────────────────────────────────────────
# 속성 빌더 헬퍼
# ──────────────────────────────────────────────
def prop_title(text: str) -> dict:
    return {"title": [{"text": {"content": text[:2000]}}]}

def prop_rich_text(text: str) -> dict:
    return {"rich_text": [{"text": {"content": str(text)[:2000]}}]}

def prop_select(name: str) -> dict:
    return {"select": {"name": name}}

def prop_date(iso: str) -> dict:
    return {"date": {"start": iso}}

def prop_number(val: float) -> dict:
    return {"number": round(float(val), 4)}

def prop_url(url: str) -> dict:
    return {"url": url[:2000]}

def code_block(text: str, language: str = "json") -> dict:
    """Notion code block"""
    return {
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [{"type": "text", "text": {"content": text[:2000]}}],
            "language": language,
        },
    }

def heading_block(text: str, level: int = 2) -> dict:
    h_type = f"heading_{level}"
    return {
        "object": "block",
        "type": h_type,
        h_type: {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }

def paragraph_block(text: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": text[:2000]}}]},
    }


# ──────────────────────────────────────────────
# 결과 파일 → Notion 속성 변환
# ──────────────────────────────────────────────
def build_properties(result: dict, engine_label: str, run_id: str, timestamp: str) -> dict:
    """
    Notion DB 속성 구성.
    DB에 없는 속성은 API가 무시하므로, 가능한 많은 필드를 포함해 범용성 확보.
    실제 DB 스키마에 맞게 키명 조정 필요.
    """
    status = result.get("status", "unknown")
    irr    = result.get("irr") or result.get("IRR")
    npv    = result.get("npv") or result.get("NPV")
    capex  = result.get("capex") or result.get("CAPEX")

    props = {
        # 필수: Title (DB의 title 컬럼명이 다를 경우 변경)
        "Name": prop_title(f"[{engine_label}] {run_id}"),

        # 공통 메타
        "Engine":    prop_select(engine_label),
        "Status":    prop_select(status.upper()),
        "Run ID":    prop_rich_text(run_id),
        "Synced At": prop_date(timestamp),

        # PE-FIN 전용 재무 지표
        **({
            "IRR (%)": prop_number(float(irr) * 100 if irr and float(irr) < 2 else float(irr)),
        } if irr is not None else {}),
        **({
            "NPV ($M)": prop_number(float(npv)),
        } if npv is not None else {}),
        **({
            "CAPEX ($M)": prop_number(float(capex)),
        } if capex is not None else {}),
    }
    return props


def build_content_blocks(result: dict, engine: str, run_id: str) -> list:
    """Notion 페이지 본문 블록 구성"""
    blocks = [
        heading_block(f"{engine} 실행 결과", level=2),
        paragraph_block(f"Run ID: {run_id}  |  Status: {result.get('status','unknown')}"),
        heading_block("Raw JSON Output", level=3),
        code_block(json.dumps(result, ensure_ascii=False, indent=2), language="json"),
    ]

    # 시나리오 분석이 있는 경우 추가
    if "scenarios" in result:
        blocks.append(heading_block("시나리오 분석", level=3))
        for k, v in result["scenarios"].items():
            blocks.append(paragraph_block(f"• {k}: {v}"))

    return blocks


# ──────────────────────────────────────────────
# 멱등성: run_id + engine 기준 기존 페이지 조회
# ──────────────────────────────────────────────
def find_existing_page(client: NotionClient, db_id: str, run_id: str, engine_label: str) -> Optional[str]:
    """동일 Run ID + Engine 조합이 이미 있으면 page_id 반환"""
    try:
        results = client.query_db(db_id, {
            "and": [
                {"property": "Run ID", "rich_text": {"equals": run_id}},
                {"property": "Engine", "select": {"equals": engine_label}},
            ]
        })
        if results:
            return results[0]["id"]
    except Exception as e:
        print(f"[WARN] 기존 페이지 조회 실패 (무시하고 신규 생성): {e}")
    return None


# ──────────────────────────────────────────────
# 메인 Push 로직
# ──────────────────────────────────────────────
def push_result(client: NotionClient, db_id: str, result_file: Path,
                run_id: str, timestamp: str) -> bool:
    """단일 결과 파일을 Notion에 Push. 성공 시 True 반환."""

    filename = result_file.name
    engine_info = ENGINE_MAP.get(filename)
    if not engine_info:
        print(f"[SKIP] 알 수 없는 결과 파일: {filename}")
        return False

    engine     = engine_info["engine"]
    eng_label  = engine_info["label"]

    # 결과 파일 로드
    try:
        result = json.loads(result_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERROR] 결과 파일 읽기 실패 {filename}: {e}")
        return False

    print(f"\n[PUSH] {eng_label} → Notion DB")
    print(f"       status: {result.get('status','unknown')}")

    properties = build_properties(result, eng_label, run_id, timestamp)
    blocks     = build_content_blocks(result, engine, run_id)

    # Upsert: 기존 페이지 있으면 Update, 없으면 Create
    existing_id = find_existing_page(client, db_id, run_id, eng_label)

    try:
        if existing_id:
            client.update_page(existing_id, properties)
            # 본문 갱신: 기존 블록은 보존하고 최신 결과 블록 추가
            client.append_blocks(existing_id, [
                paragraph_block(f"--- 재실행 {timestamp} ---"),
                *blocks,
            ])
            print(f"       ✅ Updated (page_id: {existing_id})")
        else:
            page = client.create_page(db_id, properties, blocks)
            print(f"       ✅ Created (page_id: {page['id']})")
        return True
    except Exception as e:
        print(f"       ❌ Push 실패: {e}")
        return False


# ──────────────────────────────────────────────
# 엔트리포인트
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="PE Hub → Notion Push")
    parser.add_argument("--results_dir",  default="output/notion-sync/")
    parser.add_argument("--run_id",       default=None)
    parser.add_argument("--engine_scope", default="all")
    args = parser.parse_args()

    # 환경변수 확인
    token = os.environ.get("NOTION_TOKEN")
    db_id = os.environ.get("NOTION_PE_HUB_DB_ID")

    if not token or not db_id:
        print("[ERROR] 환경변수 NOTION_TOKEN / NOTION_PE_HUB_DB_ID 가 설정되지 않았습니다.")
        print("        로컬 테스트: export NOTION_TOKEN=secret_xxx")
        print("        GitHub:     Settings > Secrets > Actions에 추가")
        sys.exit(1)

    run_id    = args.run_id or f"run-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    timestamp = datetime.now(timezone.utc).isoformat()
    results_dir = Path(args.results_dir)

    if not results_dir.exists():
        print(f"[ERROR] results_dir 없음: {results_dir}")
        sys.exit(1)

    client = NotionClient(token)

    # 처리할 파일 결정
    scope = args.engine_scope.lower()
    all_files = list(ENGINE_MAP.keys())
    if scope == "fin":
        target_files = ["pe_fin_result.json"]
    elif scope == "con":
        target_files = ["pe_con_result.json"]
    elif scope == "ip":
        target_files = ["pe_ip_result.json"]
    else:
        target_files = all_files

    print(f"\n{'='*50}")
    print(f"  Notion PE Hub Sync")
    print(f"  Run ID      : {run_id}")
    print(f"  Engine Scope: {scope}")
    print(f"  DB ID       : {db_id[:8]}...")
    print(f"{'='*50}")

    success_count = 0
    for fname in target_files:
        fpath = results_dir / fname
        if not fpath.exists():
            print(f"[SKIP] 파일 없음: {fpath}")
            continue
        if push_result(client, db_id, fpath, run_id, timestamp):
            success_count += 1

    total = len([f for f in target_files if (results_dir / f).exists()])
    print(f"\n{'='*50}")
    print(f"  완료: {success_count}/{total} 성공")
    print(f"{'='*50}\n")

    if success_count == 0 and total > 0:
        sys.exit(1)  # 전체 실패 시 Actions job 실패 처리


if __name__ == "__main__":
    main()
