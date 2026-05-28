#!/usr/bin/env python3
"""
sync_engines_to_notion.py
────────────────────────
3-Engine 구조(PE-CON / PE-FIN / PE-IP) 메타데이터를
Notion PE 허브 데이터베이스에 upsert(생성 또는 업데이트).

동작 원리:
  1. engines/ 디렉토리를 스캔하여 각 엔진의 메타데이터 수집
  2. 각 엔진 내 YAML front-matter 또는 README.md 파싱
  3. Notion PE 허브 DB에 engine_id 기준으로 upsert
  4. status / last_commit / file_count / description 업데이트

필수 환경변수:
  NOTION_TOKEN          — Notion Integration Secret
  NOTION_PE_HUB_DB_ID   — PE 허브 데이터베이스 ID

선택 환경변수:
  DRY_RUN               — 'true'이면 Notion API 호출 없이 검증만
  TARGET_ENGINE         — 'all' | 'PE-CON' | 'PE-FIN' | 'PE-IP'
"""

import os
import sys
import json
import argparse
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    from notion_client import Client
    from notion_client.errors import APIResponseError
except ImportError:
    print("ERROR: notion-client not installed. Run: pip install notion-client==2.3.0")
    sys.exit(1)

# ──────────────────────────────────────────────
# 로거 설정
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# 상수
# ──────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent.parent
ENGINES_DIR = REPO_ROOT / "engines"

# 3-Engine 정의: GitHub 디렉토리명 → Notion 표시명 + 도메인
ENGINE_MAP = {
    "PE-CON": {
        "display_name": "PE-CON (Context Engine)",
        "domain": "Context & Knowledge",
        "color": "blue",
    },
    "PE-FIN": {
        "display_name": "PE-FIN (Financial Engine)",
        "domain": "Finance & Valuation",
        "color": "green",
    },
    "PE-IP": {
        "display_name": "PE-IP (IP/Legal Engine)",
        "domain": "IP & Legal",
        "color": "purple",
    },
}


# ──────────────────────────────────────────────
# 유틸리티
# ──────────────────────────────────────────────
def get_engine_metadata(engine_dir: Path, engine_key: str) -> dict:
    """engines/<KEY>/ 디렉토리를 스캔하여 메타데이터 반환."""
    meta = {
        "engine_id": engine_key,
        "display_name": ENGINE_MAP.get(engine_key, {}).get("display_name", engine_key),
        "domain": ENGINE_MAP.get(engine_key, {}).get("domain", "Unknown"),
        "file_count": 0,
        "prompt_count": 0,
        "script_count": 0,
        "description": "",
        "last_modified": datetime.now(timezone.utc).isoformat(),
        "status": "Active",
    }

    if not engine_dir.exists():
        meta["status"] = "Missing"
        log.warning(f"Engine directory not found: {engine_dir}")
        return meta

    # 파일 카운트
    all_files = list(engine_dir.rglob("*"))
    meta["file_count"] = sum(1 for f in all_files if f.is_file())
    meta["prompt_count"] = sum(1 for f in all_files if f.suffix in (".md", ".txt") and f.is_file())
    meta["script_count"] = sum(1 for f in all_files if f.suffix == ".py" and f.is_file())

    # README.md에서 description 추출
    readme = engine_dir / "README.md"
    if readme.exists():
        content = readme.read_text(encoding="utf-8", errors="ignore")
        lines = [l.strip() for l in content.split("\n") if l.strip() and not l.startswith("#")]
        meta["description"] = lines[0][:200] if lines else ""

    # 최신 수정 시간
    mtimes = [f.stat().st_mtime for f in all_files if f.is_file()]
    if mtimes:
        latest = datetime.fromtimestamp(max(mtimes), tz=timezone.utc)
        meta["last_modified"] = latest.isoformat()

    return meta


def build_notion_properties(meta: dict) -> dict:
    """엔진 메타데이터 → Notion page properties 딕셔너리."""
    engine_info = ENGINE_MAP.get(meta["engine_id"], {})
    color = engine_info.get("color", "default")

    return {
        # Title (필수)
        "Name": {
            "title": [{"text": {"content": meta["display_name"]}}]
        },
        # Engine ID
        "Engine ID": {
            "rich_text": [{"text": {"content": meta["engine_id"]}}]
        },
        # Domain
        "Domain": {
            "select": {"name": meta["domain"]}
        },
        # Status
        "Status": {
            "select": {"name": meta["status"], "color": "green" if meta["status"] == "Active" else "red"}
        },
        # File count
        "File Count": {
            "number": meta["file_count"]
        },
        # Prompt count
        "Prompt Count": {
            "number": meta["prompt_count"]
        },
        # Script count
        "Script Count": {
            "number": meta["script_count"]
        },
        # Description
        "Description": {
            "rich_text": [{"text": {"content": meta["description"][:2000]}}]
        },
        # Last Modified
        "Last Modified": {
            "date": {"start": meta["last_modified"]}
        },
        # GitHub URL
        "GitHub URL": {
            "url": f"https://github.com/GilbertKwak/prompt-engineering-system/tree/main/engines/{meta['engine_id']}"
        },
    }


def find_existing_page(notion: Client, db_id: str, engine_id: str) -> Optional[str]:
    """Notion DB에서 engine_id 기준으로 기존 페이지 ID 반환."""
    try:
        results = notion.databases.query(
            database_id=db_id,
            filter={
                "property": "Engine ID",
                "rich_text": {"equals": engine_id},
            },
        )
        pages = results.get("results", [])
        if pages:
            return pages[0]["id"]
    except APIResponseError as e:
        log.warning(f"Query failed for engine {engine_id}: {e}")
    return None


def upsert_engine_to_notion(
    notion: Client,
    db_id: str,
    meta: dict,
    dry_run: bool = False,
) -> dict:
    """Notion DB에 엔진 메타데이터 upsert."""
    props = build_notion_properties(meta)
    engine_id = meta["engine_id"]

    existing_page_id = find_existing_page(notion, db_id, engine_id)

    if dry_run:
        action = "UPDATE" if existing_page_id else "CREATE"
        log.info(f"[DRY RUN] Would {action} page for {engine_id}")
        log.debug(f"Properties: {json.dumps(props, indent=2, ensure_ascii=False)}")
        return {"action": action, "engine_id": engine_id, "dry_run": True}

    try:
        if existing_page_id:
            # 업데이트
            notion.pages.update(page_id=existing_page_id, properties=props)
            log.info(f"✅ UPDATED: {engine_id} (page_id={existing_page_id[:8]}...)")
            return {"action": "updated", "engine_id": engine_id, "page_id": existing_page_id}
        else:
            # 신규 생성
            page = notion.pages.create(
                parent={"database_id": db_id},
                properties=props,
            )
            page_id = page["id"]
            log.info(f"✅ CREATED: {engine_id} (page_id={page_id[:8]}...)")
            return {"action": "created", "engine_id": engine_id, "page_id": page_id}

    except APIResponseError as e:
        log.error(f"❌ FAILED: {engine_id} — {e}")
        return {"action": "error", "engine_id": engine_id, "error": str(e)}


# ──────────────────────────────────────────────
# 메인
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Sync 3-Engine structure to Notion PE Hub DB")
    parser.add_argument("--engine", default="all", help="Engine to sync: all | PE-CON | PE-FIN | PE-IP")
    parser.add_argument("--dry-run", default="false", help="Dry-run mode")
    args = parser.parse_args()

    dry_run = args.dry_run.lower() == "true"
    target = args.engine.upper() if args.engine else "all"

    # 환경변수 검증
    token = os.environ.get("NOTION_TOKEN")
    db_id = os.environ.get("NOTION_PE_HUB_DB_ID")

    if not token or not db_id:
        if dry_run:
            log.warning("DRY RUN: NOTION_TOKEN or NOTION_PE_HUB_DB_ID not set — skipping API calls")
            token = token or "dry-run-token"
            db_id = db_id or "dry-run-db-id"
        else:
            log.error("NOTION_TOKEN and NOTION_PE_HUB_DB_ID must be set as GitHub Secrets")
            log.error("Setup guide: https://github.com/GilbertKwak/prompt-engineering-system/blob/main/docs/notion-sync-setup.md")
            sys.exit(1)

    notion = Client(auth=token) if not dry_run else None

    # 동기화 대상 결정
    engines_to_sync = list(ENGINE_MAP.keys()) if target == "ALL" else [target] if target in ENGINE_MAP else list(ENGINE_MAP.keys())

    log.info(f"{'[DRY RUN] ' if dry_run else ''}Syncing engines: {engines_to_sync}")

    results = []
    for engine_key in engines_to_sync:
        # engines/ 디렉토리 우선, 없으면 루트의 PE-* 디렉토리 확인
        engine_dir = ENGINES_DIR / engine_key
        if not engine_dir.exists():
            engine_dir = REPO_ROOT / engine_key

        meta = get_engine_metadata(engine_dir, engine_key)
        log.info(f"Engine {engine_key}: {meta['file_count']} files, {meta['prompt_count']} prompts, {meta['script_count']} scripts")

        if not dry_run and notion:
            result = upsert_engine_to_notion(notion, db_id, meta, dry_run=False)
        else:
            result = upsert_engine_to_notion(None, db_id, meta, dry_run=True)

        results.append(result)

    # 결과 요약
    print("\n" + "=" * 50)
    print(f"{'[DRY RUN] ' if dry_run else ''}Engine Sync Summary")
    print("=" * 50)
    for r in results:
        status = r.get("action", "unknown").upper()
        eid = r.get("engine_id", "?")
        err = r.get("error", "")
        print(f"  {status:10s} {eid}" + (f" → {err}" if err else ""))

    errors = [r for r in results if r.get("action") == "error"]
    if errors:
        log.error(f"{len(errors)} engine(s) failed to sync")
        sys.exit(1)

    log.info(f"Done. {len(results)} engine(s) processed.")


if __name__ == "__main__":
    main()
