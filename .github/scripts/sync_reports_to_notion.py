#!/usr/bin/env python3
"""
sync_reports_to_notion.py
──────────────────────────
reports/ 및 PE-CON/PE-FIN/PE-IP 내 Markdown 보고서를
Notion Reports DB에 upsert.

수집 항목:
  - 보고서 제목 (파일명 또는 # 첫 헤딩)
  - 엔진 분류 (경로 기반)
  - 요약 (첫 단락 200자)
  - 작성일 / 수정일
  - GitHub 원본 URL

필수 환경변수:
  NOTION_TOKEN           — Notion Integration Secret
  NOTION_REPORTS_DB_ID   — Reports 데이터베이스 ID
"""

import os
import sys
import re
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

# 스캔 대상 디렉토리
SCAN_DIRS = [
    REPO_ROOT / "reports",
    REPO_ROOT / "PE-CON",
    REPO_ROOT / "PE-FIN",
    REPO_ROOT / "PE-IP",
]

# 제외 패턴
EXCLUDE_PATTERNS = [
    "README.md",
    "CHANGELOG.md",
    "TODO.md",
    "MASTER_COMMANDS.md",
    "USAGE_COMMANDS.md",
]


def detect_engine_from_path(path: Path) -> str:
    """경로에서 엔진 태그 감지."""
    parts = [p.upper() for p in path.parts]
    for engine in ["PE-CON", "PE-FIN", "PE-IP"]:
        if engine in parts or engine.replace("-", "_") in parts:
            return engine
    # 파일명 키워드 매핑
    stem = path.stem.lower()
    if any(kw in stem for kw in ["financial", "fin", "irr", "npv", "capex", "jv", "hbm"]):
        return "PE-FIN"
    if any(kw in stem for kw in ["context", "knowledge", "session"]):
        return "PE-CON"
    if any(kw in stem for kw in ["ip", "patent", "legal", "contract"]):
        return "PE-IP"
    return "General"


def extract_report_metadata(md_path: Path) -> dict:
    """Markdown 파일에서 보고서 메타데이터 추출."""
    meta = {
        "filename": md_path.name,
        "relative_path": str(md_path.relative_to(REPO_ROOT)),
        "title": md_path.stem.replace("-", " ").replace("_", " ").title(),
        "summary": "",
        "engine_tag": detect_engine_from_path(md_path),
        "last_modified": datetime.fromtimestamp(
            md_path.stat().st_mtime, tz=timezone.utc
        ).isoformat(),
        "word_count": 0,
    }

    try:
        content = md_path.read_text(encoding="utf-8", errors="ignore")

        # 제목: 첫 번째 # 헤딩 추출
        title_match = re.search(r"^#{1,2}\s+(.+)$", content, re.MULTILINE)
        if title_match:
            meta["title"] = title_match.group(1).strip()[:200]

        # 요약: 헤딩·코드블록·빈줄 제외한 첫 단락
        clean_lines = []
        in_code_block = False
        for line in content.split("\n"):
            if line.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("|"):
                if clean_lines:
                    break  # 첫 단락 완성
                continue
            # 마크다운 제거
            line = re.sub(r"[*_`\[\]]", "", line)
            clean_lines.append(line)

        meta["summary"] = " ".join(clean_lines)[:300]

        # 단어 수
        meta["word_count"] = len(content.split())

    except Exception as e:
        log.warning(f"Could not parse {md_path.name}: {e}")

    return meta


def build_report_properties(meta: dict) -> dict:
    """보고서 메타데이터 → Notion properties."""
    return {
        "Name": {
            "title": [{"text": {"content": meta["title"][:200]}}]
        },
        "File Path": {
            "rich_text": [{"text": {"content": meta["relative_path"]}}]
        },
        "Summary": {
            "rich_text": [{"text": {"content": meta["summary"][:2000]}}]
        },
        "Engine Tag": {
            "select": {"name": meta["engine_tag"]}
        },
        "Last Modified": {
            "date": {"start": meta["last_modified"]}
        },
        "Word Count": {
            "number": meta["word_count"]
        },
        "GitHub URL": {
            "url": f"https://github.com/GilbertKwak/prompt-engineering-system/blob/main/{meta['relative_path']}"
        },
    }


def find_existing_report_page(notion: Client, db_id: str, file_path: str) -> Optional[str]:
    """파일 경로 기준으로 기존 페이지 검색."""
    try:
        results = notion.databases.query(
            database_id=db_id,
            filter={"property": "File Path", "rich_text": {"equals": file_path}},
        )
        pages = results.get("results", [])
        return pages[0]["id"] if pages else None
    except APIResponseError:
        return None


def main():
    parser = argparse.ArgumentParser(description="Sync Markdown reports to Notion Reports DB")
    parser.add_argument("--dry-run", default="false")
    args = parser.parse_args()
    dry_run = args.dry_run.lower() == "true"

    token = os.environ.get("NOTION_TOKEN")
    db_id = os.environ.get("NOTION_REPORTS_DB_ID")

    if not token or not db_id:
        if dry_run:
            log.warning("DRY RUN: Secrets not set — skipping API calls")
        else:
            log.error("NOTION_TOKEN and NOTION_REPORTS_DB_ID must be set")
            sys.exit(1)

    notion = Client(auth=token) if (token and not dry_run) else None

    # 모든 대상 디렉토리 스캔
    md_files = []
    for scan_dir in SCAN_DIRS:
        if scan_dir.exists():
            found = list(scan_dir.rglob("*.md"))
            md_files.extend(found)
            log.info(f"Found {len(found)} .md files in {scan_dir.name}/")

    # 제외 필터
    md_files = [
        f for f in md_files
        if f.name not in EXCLUDE_PATTERNS
    ]
    log.info(f"Total reports to sync: {len(md_files)}")

    results = []
    for md_path in sorted(md_files):
        meta = extract_report_metadata(md_path)
        props = build_report_properties(meta)

        if dry_run:
            log.info(f"[DRY RUN] {meta['engine_tag']:10s} | {meta['title'][:60]}")
            results.append({"action": "dry_run", "file": meta["filename"]})
            continue

        existing_id = find_existing_report_page(notion, db_id, meta["relative_path"])
        try:
            if existing_id:
                notion.pages.update(page_id=existing_id, properties=props)
                log.info(f"✅ UPDATED: {meta['title'][:50]}")
                results.append({"action": "updated", "file": meta["filename"]})
            else:
                notion.pages.create(parent={"database_id": db_id}, properties=props)
                log.info(f"✅ CREATED: {meta['title'][:50]}")
                results.append({"action": "created", "file": meta["filename"]})
        except APIResponseError as e:
            log.error(f"❌ FAILED: {meta['filename']} — {e}")
            results.append({"action": "error", "file": meta["filename"], "error": str(e)})

    created = sum(1 for r in results if r["action"] == "created")
    updated = sum(1 for r in results if r["action"] == "updated")
    errors = sum(1 for r in results if r["action"] == "error")
    log.info(f"Reports sync done: {created} created, {updated} updated, {errors} errors")

    if errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
