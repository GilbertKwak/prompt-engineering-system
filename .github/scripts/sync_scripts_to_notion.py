#!/usr/bin/env python3
"""
sync_scripts_to_notion.py
─────────────────────────
scripts/ 디렉토리의 Python 스크립트 메타데이터를
Notion Scripts DB에 upsert.

수집 항목:
  - 파일명, 경로, 크기
  - docstring (첫 줄 설명)
  - argparse 인자 목록 (정적 파싱)
  - 마지막 수정 시간
  - 실행 횟수 (GitHub Actions 실행 시 +1)

필수 환경변수:
  NOTION_TOKEN           — Notion Integration Secret
  NOTION_SCRIPTS_DB_ID   — Scripts 데이터베이스 ID
"""

import os
import sys
import re
import ast
import argparse
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    from notion_client import Client
    from notion_client.errors import APIResponseError
except ImportError:
    print("ERROR: notion-client not installed")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).parent.parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"


def extract_script_metadata(script_path: Path) -> dict:
    """Python 스크립트에서 메타데이터 추출."""
    meta = {
        "filename": script_path.name,
        "relative_path": str(script_path.relative_to(REPO_ROOT)),
        "size_bytes": script_path.stat().st_size,
        "description": "",
        "args": [],
        "last_modified": datetime.fromtimestamp(
            script_path.stat().st_mtime, tz=timezone.utc
        ).isoformat(),
        "engine_tag": "",
    }

    try:
        source = script_path.read_text(encoding="utf-8", errors="ignore")

        # docstring 추출
        try:
            tree = ast.parse(source)
            docstring = ast.get_docstring(tree)
            if docstring:
                first_line = docstring.strip().split("\n")[0]
                meta["description"] = first_line[:300]
        except SyntaxError:
            # 파싱 실패시 주석에서 추출
            for line in source.split("\n")[:10]:
                line = line.strip()
                if line.startswith("#") and len(line) > 2:
                    meta["description"] = line[1:].strip()[:300]
                    break

        # argparse --argument 목록 추출 (정적)
        args_found = re.findall(r"add_argument\(['\"](-{1,2}[\w-]+)['\"]\s*[,)]", source)
        meta["args"] = list(dict.fromkeys(args_found))[:20]  # 중복 제거, 최대 20개

        # 엔진 태그 추출 (파일명 또는 경로에서)
        for engine in ["PE-CON", "PE-FIN", "PE-IP"]:
            if engine.lower().replace("-", "_") in script_path.stem.lower() or engine in str(script_path):
                meta["engine_tag"] = engine
                break
        # financial_bridge → PE-FIN 자동 태깅
        if not meta["engine_tag"]:
            stem = script_path.stem.lower()
            if any(kw in stem for kw in ["financial", "fin", "irr", "npv", "capex"]):
                meta["engine_tag"] = "PE-FIN"
            elif any(kw in stem for kw in ["context", "con", "knowledge"]):
                meta["engine_tag"] = "PE-CON"
            elif any(kw in stem for kw in ["ip", "legal", "patent"]):
                meta["engine_tag"] = "PE-IP"

    except Exception as e:
        log.warning(f"Could not parse {script_path.name}: {e}")

    return meta


def build_script_properties(meta: dict) -> dict:
    """스크립트 메타데이터 → Notion properties."""
    args_str = ", ".join(meta["args"]) if meta["args"] else ""

    props = {
        "Name": {
            "title": [{"text": {"content": meta["filename"]}}]
        },
        "File Path": {
            "rich_text": [{"text": {"content": meta["relative_path"]}}]
        },
        "Description": {
            "rich_text": [{"text": {"content": meta["description"][:2000]}}]
        },
        "Arguments": {
            "rich_text": [{"text": {"content": args_str[:2000]}}]
        },
        "File Size (KB)": {
            "number": round(meta["size_bytes"] / 1024, 2)
        },
        "Last Modified": {
            "date": {"start": meta["last_modified"]}
        },
        "GitHub URL": {
            "url": f"https://github.com/GilbertKwak/prompt-engineering-system/blob/main/{meta['relative_path']}"
        },
    }

    if meta.get("engine_tag"):
        props["Engine Tag"] = {"select": {"name": meta["engine_tag"]}}

    return props


def find_existing_script_page(notion: Client, db_id: str, filename: str) -> Optional[str]:
    """파일명 기준으로 기존 페이지 검색."""
    try:
        results = notion.databases.query(
            database_id=db_id,
            filter={"property": "Name", "title": {"equals": filename}},
        )
        pages = results.get("results", [])
        return pages[0]["id"] if pages else None
    except APIResponseError:
        return None


def main():
    parser = argparse.ArgumentParser(description="Sync scripts/ metadata to Notion Scripts DB")
    parser.add_argument("--dry-run", default="false")
    args = parser.parse_args()
    dry_run = args.dry_run.lower() == "true"

    token = os.environ.get("NOTION_TOKEN")
    db_id = os.environ.get("NOTION_SCRIPTS_DB_ID")

    if not token or not db_id:
        if dry_run:
            log.warning("DRY RUN: Secrets not set — skipping API calls")
        else:
            log.error("NOTION_TOKEN and NOTION_SCRIPTS_DB_ID must be set")
            sys.exit(1)

    notion = Client(auth=token) if (token and not dry_run) else None

    # scripts/ 디렉토리 스캔
    if not SCRIPTS_DIR.exists():
        log.warning(f"scripts/ directory not found at {SCRIPTS_DIR}")
        return

    py_files = list(SCRIPTS_DIR.rglob("*.py"))
    log.info(f"Found {len(py_files)} Python scripts in scripts/")

    results = []
    for script_path in sorted(py_files):
        meta = extract_script_metadata(script_path)
        props = build_script_properties(meta)

        if dry_run:
            log.info(f"[DRY RUN] Would upsert: {meta['filename']} ({meta['size_bytes']} bytes)")
            results.append({"action": "dry_run", "file": meta["filename"]})
            continue

        existing_id = find_existing_script_page(notion, db_id, meta["filename"])
        try:
            if existing_id:
                notion.pages.update(page_id=existing_id, properties=props)
                log.info(f"✅ UPDATED: {meta['filename']}")
                results.append({"action": "updated", "file": meta["filename"]})
            else:
                notion.pages.create(parent={"database_id": db_id}, properties=props)
                log.info(f"✅ CREATED: {meta['filename']}")
                results.append({"action": "created", "file": meta["filename"]})
        except APIResponseError as e:
            log.error(f"❌ FAILED: {meta['filename']} — {e}")
            results.append({"action": "error", "file": meta["filename"], "error": str(e)})

    # 요약
    created = sum(1 for r in results if r["action"] == "created")
    updated = sum(1 for r in results if r["action"] == "updated")
    errors = sum(1 for r in results if r["action"] == "error")
    log.info(f"Scripts sync done: {created} created, {updated} updated, {errors} errors")

    if errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
