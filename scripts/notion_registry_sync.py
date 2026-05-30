#!/usr/bin/env python3
"""
scripts/notion_registry_sync.py
================================
GitHub Actions에서 preflight 결과를 Notion 레지스트리 페이지에 동기화합니다.

환경변수 (GitHub Secrets):
  NOTION_TOKEN              - Notion Integration 토큰
  NOTION_REGISTRY_PAGE_ID   - 대상 Notion 페이지 ID
  VALIDATION_STATUS         - PASS / FAIL
  TOTAL_TOOLS               - 전체 도구 수
  VALID_TOOLS               - 유효 도구 수
  ERROR_COUNT               - 오류 수
  LAST_VALIDATED            - ISO 타임스탬프
  RUN_URL                   - GitHub Actions 실행 URL
  COMMIT_SHA                - 커밋 SHA (short)
  COMMIT_MSG                - 커밋 메시지
"""

import os
import sys
import json
import requests
from datetime import datetime, timezone

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


def get_env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def notion_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def build_status_block(status: str, total: str, valid: str, errors: str,
                       run_url: str, commit_sha: str, commit_msg: str,
                       timestamp: str) -> list:
    """Notion block 배열 생성 (기존 페이지 내용 앞에 삽입)."""
    icon = "✅" if status == "PASS" else "❌"
    short_sha = commit_sha[:7] if len(commit_sha) >= 7 else commit_sha
    date_str  = timestamp[:10] if timestamp else datetime.now(timezone.utc).strftime("%Y-%m-%d")
    time_str  = timestamp[11:19] if len(timestamp) >= 19 else ""

    def text(content: str, bold=False, code=False, color="default") -> dict:
        ann = {"bold": bold, "code": code, "color": color,
               "italic": False, "strikethrough": False, "underline": False}
        return {"type": "text", "text": {"content": content}, "annotations": ann}

    def paragraph(*parts) -> dict:
        return {"object": "block", "type": "paragraph",
                "paragraph": {"rich_text": list(parts)}}

    def heading2(content: str) -> dict:
        return {"object": "block", "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": content}}]}}

    def divider() -> dict:
        return {"object": "block", "type": "divider", "divider": {}}

    def callout(content: str, emoji: str, color: str) -> dict:
        return {
            "object": "block", "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": content}}],
                "icon": {"type": "emoji", "emoji": emoji},
                "color": color,
            }
        }

    status_color = "green_background" if status == "PASS" else "red_background"
    status_label = f"{icon} {status}"

    blocks = [
        divider(),
        heading2(f"Preflight 실행 — {date_str} {time_str} UTC"),
        callout(
            f"{status_label}  |  총 도구: {total}  |  유효: {valid}  |  오류: {errors}",
            emoji=icon,
            color=status_color,
        ),
        paragraph(
            text("커밋: ", bold=True),
            text(short_sha, code=True),
            text(f"  {commit_msg[:80]}" if commit_msg else ""),
        ),
        paragraph(
            text("Actions 실행: ", bold=True),
            {"type": "text",
             "text": {"content": "GitHub Actions 로그 보기", "link": {"url": run_url}},
             "annotations": {"bold": False, "italic": False, "strikethrough": False,
                              "underline": True, "code": False, "color": "blue"}}
            if run_url else text("(URL unavailable)"),
        ),
        divider(),
    ]
    return blocks


def append_blocks(token: str, page_id: str, blocks: list) -> bool:
    """Notion 페이지 맨 위에 블록 삽입 (prepend 시뮬: append 후 위로 이동 불가 → append 사용)."""
    url = f"{NOTION_API}/blocks/{page_id}/children"
    payload = {"children": blocks}
    resp = requests.patch(url, headers=notion_headers(token), json=payload, timeout=30)
    if resp.status_code not in (200, 201):
        print(f"❌ Notion API error {resp.status_code}: {resp.text[:300]}")
        return False
    print(f"✅ Notion 동기화 완료 (page_id={page_id[:8]}...)")
    return True


def main():
    token   = get_env("NOTION_TOKEN")
    page_id = get_env("NOTION_REGISTRY_PAGE_ID")

    if not token:
        print("⚠️  NOTION_TOKEN not set — skipping Notion sync")
        sys.exit(0)
    if not page_id:
        print("⚠️  NOTION_REGISTRY_PAGE_ID not set — skipping Notion sync")
        sys.exit(0)

    blocks = build_status_block(
        status      = get_env("VALIDATION_STATUS", "UNKNOWN"),
        total       = get_env("TOTAL_TOOLS", "?"),
        valid       = get_env("VALID_TOOLS",  "?"),
        errors      = get_env("ERROR_COUNT",  "?"),
        run_url     = get_env("RUN_URL"),
        commit_sha  = get_env("COMMIT_SHA"),
        commit_msg  = get_env("COMMIT_MSG"),
        timestamp   = get_env("LAST_VALIDATED"),
    )

    success = append_blocks(token, page_id, blocks)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
