#!/usr/bin/env python3
"""
notion_pe_hub_push.py
=====================
GitHub Actions에서 호출되는 Notion PE 허브 Push 스크립트.

기능:
  - output/*.json 결과물을 Notion 데이터베이스 페이지로 upsert
  - 3-Engine (FIN / CON / IP) 각각 별도 DB 레코드 생성
  - 중복 방지: Commit SHA + Engine 조합으로 기존 레코드 검색 후 Update
  - 실패 시 상세 오류 로그 출력 (CI 로그에서 즉시 파악 가능)

필수 환경변수:
  NOTION_TOKEN          - Notion Integration Token (secrets.NOTION_TOKEN)
  NOTION_PE_HUB_DB_ID   - PE Hub 데이터베이스 ID (secrets.NOTION_PE_HUB_DB_ID)

선택 환경변수:
  NOTION_FIN_DB_ID      - PE-FIN 전용 DB (없으면 PE Hub DB 사용)
  NOTION_CON_DB_ID      - PE-CON 전용 DB
  NOTION_IP_DB_ID       - PE-IP 전용 DB

실행 예시:
  python scripts/notion_pe_hub_push.py \\
      --engine ALL \\
      --commit abc1234 \\
      --branch main
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from notion_client import Client
except ImportError:
    print("[ERROR] notion-client not installed. Run: pip install notion-client")
    sys.exit(1)

# ─── 상수 ──────────────────────────────────────────────────────
OUTPUT_DIR = Path(__file__).parent.parent / "output"

ENGINE_MAP = {
    "FIN": {"file": "fin_result.json", "label": "PE-FIN", "env": "NOTION_FIN_DB_ID"},
    "CON": {"file": "con_result.json", "label": "PE-CON", "env": "NOTION_CON_DB_ID"},
    "IP":  {"file": "ip_result.json",  "label": "PE-IP",  "env": "NOTION_IP_DB_ID"},
}


# ─── Notion 클라이언트 초기화 ──────────────────────────────────
def get_notion_client() -> Client:
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        print("[ERROR] NOTION_TOKEN 환경변수가 설정되지 않았습니다.")
        print("       GitHub Repository → Settings → Secrets → Actions에서 추가하세요.")
        sys.exit(1)
    return Client(auth=token)


def get_db_id(engine: str) -> str:
    """엔진별 DB ID 반환. 전용 DB가 없으면 PE Hub DB 사용."""
    hub_db = os.environ.get("NOTION_PE_HUB_DB_ID")
    if not hub_db:
        print("[ERROR] NOTION_PE_HUB_DB_ID 환경변수가 설정되지 않았습니다.")
        sys.exit(1)
    engine_db = os.environ.get(ENGINE_MAP[engine]["env"])
    return engine_db if engine_db else hub_db


# ─── JSON 결과 로드 ────────────────────────────────────────────
def load_result(engine: str) -> dict | None:
    file_path = OUTPUT_DIR / ENGINE_MAP[engine]["file"]
    if not file_path.exists():
        print(f"[SKIP] {file_path} 없음 — {engine} Engine 건너뜀")
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"[OK] {engine} 결과 로드: {file_path}")
        return data
    except json.JSONDecodeError as e:
        print(f"[ERROR] {file_path} JSON 파싱 실패: {e}")
        return None


# ─── Notion 페이지 Upsert ──────────────────────────────────────
def find_existing_page(notion: Client, db_id: str, commit: str, engine: str) -> str | None:
    """Commit SHA + Engine 기준으로 기존 페이지 검색."""
    try:
        results = notion.databases.query(
            database_id=db_id,
            filter={
                "and": [
                    {"property": "Commit SHA", "rich_text": {"equals": commit[:8]}},
                    {"property": "Engine",     "select":    {"equals": engine}},
                ]
            },
        )
        pages = results.get("results", [])
        if pages:
            return pages[0]["id"]
    except Exception as e:
        print(f"[WARN] 기존 페이지 검색 실패 (신규 생성으로 대체): {e}")
    return None


def build_properties(engine: str, data: dict, commit: str, branch: str) -> dict:
    """Notion 페이지 properties 딕셔너리 생성."""
    now_iso = datetime.now(timezone.utc).isoformat()
    engine_label = ENGINE_MAP[engine]["label"]

    # 공통 properties (모든 Engine 공유)
    props = {
        "Name": {
            "title": [{"text": {"content": f"[{engine_label}] {commit[:8]} — {branch}"}}]
        },
        "Engine": {
            "select": {"name": engine_label}
        },
        "Commit SHA": {
            "rich_text": [{"text": {"content": commit[:8]}}]
        },
        "Branch": {
            "rich_text": [{"text": {"content": branch}}]
        },
        "Run At": {
            "date": {"start": now_iso}
        },
        "Status": {
            "select": {"name": "✅ Completed"}
        },
    }

    # PE-FIN 전용 properties
    if engine == "FIN" and data:
        _add_number(props, "IRR (%)",    data.get("irr"))
        _add_number(props, "NPV ($M)",   data.get("npv"))
        _add_number(props, "CAPEX ($M)", data.get("capex"))
        _add_number(props, "OPEX ($M)",  data.get("opex"))
        _add_number(props, "Yield",      data.get("target_yield"))
        scenario = data.get("scenario", "Base")
        props["Scenario"] = {"select": {"name": scenario}}

    return props


def _add_number(props: dict, key: str, value):
    """None이 아닌 경우에만 number property 추가."""
    if value is not None:
        try:
            props[key] = {"number": float(value)}
        except (TypeError, ValueError):
            pass


def build_page_content(engine: str, data: dict, commit: str, branch: str) -> str:
    """Notion 페이지 본문 (Markdown 형식)."""
    engine_label = ENGINE_MAP[engine]["label"]
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        f"## {engine_label} 실행 결과",
        f"",
        f"- **실행 시각**: {now_str}",
        f"- **Commit**: `{commit[:8]}`",
        f"- **Branch**: `{branch}`",
        f"",
        "### Raw Output",
        "```json",
        json.dumps(data, indent=2, ensure_ascii=False) if data else "{}",
        "```",
    ]
    return "\n".join(lines)


def upsert_page(
    notion: Client,
    db_id: str,
    engine: str,
    data: dict,
    commit: str,
    branch: str,
    dry_run: bool = False,
):
    properties = build_properties(engine, data, commit, branch)
    engine_label = ENGINE_MAP[engine]["label"]

    if dry_run:
        print(f"[DRY-RUN] {engine_label} — properties: {list(properties.keys())}")
        return

    existing_id = find_existing_page(notion, db_id, commit, engine_label)

    try:
        if existing_id:
            notion.pages.update(page_id=existing_id, properties=properties)
            print(f"[UPDATE] {engine_label} 페이지 업데이트 완료: {existing_id}")
        else:
            page = notion.pages.create(
                parent={"database_id": db_id},
                properties=properties,
            )
            print(f"[CREATE] {engine_label} 새 페이지 생성: {page['id']}")
            # 페이지 본문 추가 (별도 블록 append)
            content = build_page_content(engine, data, commit, branch)
            notion.blocks.children.append(
                block_id=page["id"],
                children=[
                    {
                        "object": "block",
                        "type": "code",
                        "code": {
                            "rich_text": [{"type": "text", "text": {"content": content[:2000]}}],
                            "language": "markdown",
                        },
                    }
                ],
            )
    except Exception as e:
        print(f"[ERROR] Notion API 오류 ({engine_label}): {e}")
        raise


# ─── 메인 ──────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Notion PE Hub Push Script")
    parser.add_argument("--engine",  default="ALL", choices=["ALL", "FIN", "CON", "IP"])
    parser.add_argument("--commit",  default="unknown")
    parser.add_argument("--branch",  default="main")
    parser.add_argument("--dry_run", action="store_true")
    args = parser.parse_args()

    notion = get_notion_client()
    engines = ["FIN", "CON", "IP"] if args.engine == "ALL" else [args.engine]

    success, skipped, failed = 0, 0, 0

    for eng in engines:
        db_id = get_db_id(eng)
        data  = load_result(eng)
        if data is None:
            skipped += 1
            continue
        try:
            upsert_page(notion, db_id, eng, data, args.commit, args.branch, args.dry_run)
            success += 1
        except Exception:
            failed += 1

    print(f"\n[SUMMARY] 성공: {success} / 건너뜀: {skipped} / 실패: {failed}")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
