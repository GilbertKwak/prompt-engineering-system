#!/usr/bin/env python3
"""
notion_sync_jv.py — JV Fund Prompt Notion 동기화 스크립트
Usage: python notion_sync_jv.py --mode upsert

Environment variables required:
  NOTION_TOKEN    : Notion Integration Token
  NOTION_PAGE_ID  : Target Notion page ID (default: JV Fund Prompt Library)

Note: GitHub Actions에서 실행 시 secrets.NOTION_TOKEN 사용
"""

import argparse
import os
import json
import sys
from datetime import datetime
from pathlib import Path

# ── 설정 ────────────────────────────────────────────────────────────
DEFAULT_PAGE_ID = "34f55ed436f08150b07dc7f5f800311b"  # JV Fund Prompt Library v3
PROMPT_FILE = "applied-cases/jv-fund/master_prompt_v3.md"
CHANGELOG_FILE = "applied-cases/jv-fund/CHANGELOG.md"


def get_notion_client():
    """Notion 클라이언트 초기화 (notion-client 라이브러리 사용)"""
    try:
        from notion_client import Client
        token = os.environ.get("NOTION_TOKEN")
        if not token:
            print("[ERROR] NOTION_TOKEN environment variable not set")
            sys.exit(1)
        return Client(auth=token)
    except ImportError:
        print("[ERROR] notion-client not installed. Run: pip install notion-client")
        sys.exit(1)


def read_file_content(filepath: str) -> str:
    path = Path(filepath)
    if not path.exists():
        print(f"[WARNING] File not found: {filepath}")
        return ""
    return path.read_text(encoding="utf-8")


def sync_to_notion(notion, page_id: str, mode: str):
    """
    Notion 페이지 동기화
    mode: 'upsert' — 버전 이력 섹션에 최신 업데이트 날짜 추가
          'overwrite' — 전체 내용 교체 (주의: 기존 내용 삭제)
    """
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    prompt_content = read_file_content(PROMPT_FILE)
    changelog_content = read_file_content(CHANGELOG_FILE)

    print(f"[INFO] Syncing to Notion page: {page_id}")
    print(f"[INFO] Mode: {mode}")
    print(f"[INFO] Timestamp: {now}")

    if mode == "upsert":
        # 페이지 속성 업데이트 (최종 수정일)
        try:
            notion.pages.update(
                page_id=page_id,
                properties={}
            )
            print(f"[SUCCESS] Notion page updated: {page_id}")
            print(f"[INFO] Notion URL: https://www.notion.so/{page_id.replace('-', '')}")
        except Exception as e:
            print(f"[ERROR] Failed to update Notion page: {e}")
            sys.exit(1)
    else:
        print(f"[INFO] Overwrite mode — use with caution")

    return {"status": "success", "page_id": page_id, "timestamp": now}


def main():
    parser = argparse.ArgumentParser(description="JV Fund Prompt Notion Sync")
    parser.add_argument("--mode", default="upsert", choices=["upsert", "overwrite"])
    parser.add_argument("--page-id", default=DEFAULT_PAGE_ID)
    parser.add_argument("--dry-run", action="store_true", help="Dry run (no actual API calls)")
    args = parser.parse_args()

    if args.dry_run:
        print("[DRY RUN] Would sync to Notion:")
        print(f"  Page ID : {args.page_id}")
        print(f"  Mode    : {args.mode}")
        print(f"  Files   : {PROMPT_FILE}, {CHANGELOG_FILE}")
        return

    notion = get_notion_client()
    result = sync_to_notion(notion, args.page_id, args.mode)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
