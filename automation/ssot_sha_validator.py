#!/usr/bin/env python3
"""
Section B — ssot_sha_validator.py
Notion Hub ↔ GitHub SHA 비교 및 자동 동기화
실행: python automation/ssot_sha_validator.py --page-id <NOTION_PAGE_ID> [--auto-sync] [--output sha_report.json]
"""
import os
import sys
import json
import subprocess
import argparse
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("[ERROR] requests 패키지 필요: pip install requests")
    sys.exit(1)

NOTION_VERSION = "2022-06-28"


def get_git_sha(cwd: str = ".") -> str:
    """현재 git HEAD SHA 취득"""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=cwd, text=True
        ).strip()
    except Exception:
        return ""


def get_git_short_sha(cwd: str = ".") -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=cwd, text=True
        ).strip()
    except Exception:
        return ""


def fetch_notion_page(page_id: str, token: str) -> dict:
    """Notion 페이지 properties 취득"""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    resp = requests.get(url, headers=headers, timeout=15)
    if resp.status_code == 200:
        return resp.json()
    raise RuntimeError(f"Notion API 오류 {resp.status_code}: {resp.text[:200]}")


def extract_sha_from_properties(page_data: dict) -> str:
    """Notion page properties에서 SHA 값 추출 (rich_text 또는 title)"""
    props = page_data.get("properties", {})
    for key in ["SHA", "sha", "last_sha", "commit_sha", "GitHub SHA", "github_sha"]:
        if key in props:
            prop = props[key]
            ptype = prop.get("type", "")
            if ptype == "rich_text":
                items = prop.get("rich_text", [])
                if items:
                    return items[0].get("plain_text", "")
            elif ptype == "title":
                items = prop.get("title", [])
                if items:
                    return items[0].get("plain_text", "")
    return ""


def update_notion_sha(page_id: str, token: str, sha: str, short_sha: str) -> bool:
    """Notion 페이지 SHA 속성 업데이트"""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    # SHA 속성이 없을 수 있으므로 여러 키 시도
    for sha_key in ["SHA", "sha", "GitHub SHA"]:
        payload = {
            "properties": {
                sha_key: {
                    "rich_text": [
                        {"type": "text", "text": {"content": f"{short_sha} ({sha[:16]}...)"}}
                    ]
                }
            }
        }
        resp = requests.patch(url, headers=headers, json=payload, timeout=15)
        if resp.status_code == 200:
            return True
    return False


def append_ssot_block(page_id: str, token: str, git_sha: str, notion_sha: str, status: str) -> bool:
    """Notion 페이지에 SSOT 동기화 로그 블록 추가"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    icon = "✅" if status == "MATCH" else "⚠️"
    text = f"{icon} SSOT SHA 검증 [{now}] | GitHub: {git_sha[:8]} | Notion: {notion_sha[:8] if notion_sha else 'N/A'} | Status: {status}"
    payload = {
        "children": [
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"type": "text", "text": {"content": text}}],
                    "icon": {"emoji": icon},
                    "color": "green_background" if status == "MATCH" else "yellow_background",
                },
            }
        ]
    }
    resp = requests.patch(url, headers=headers, json=payload, timeout=15)
    return resp.status_code == 200


def run_ssot_validation(
    page_id: str,
    notion_token: str,
    auto_sync: bool = False,
    cwd: str = ".",
) -> dict:
    report = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "git_sha": "",
        "notion_sha": "",
        "status": "UNKNOWN",
        "synced": False,
        "error": "",
    }

    # 1. GitHub SHA 취득
    git_sha = get_git_sha(cwd)
    short_sha = get_git_short_sha(cwd)
    report["git_sha"] = git_sha

    if not git_sha:
        report["status"] = "WARN"
        report["error"] = "git 명령 실패 (non-git 환경) — GitHub Actions 환경에서 실행하세요"
        print(f"[WARN] {report['error']}")
        return report

    # 2. Notion Hub SHA 취득
    try:
        page_data = fetch_notion_page(page_id, notion_token)
        notion_sha = extract_sha_from_properties(page_data)
        report["notion_sha"] = notion_sha
    except Exception as e:
        report["status"] = "ERROR"
        report["error"] = f"Notion 조회 실패: {e}\n⚠️ MANUAL_REVIEW_REQUIRED: E-03 — Notion Integration 연결 여부 확인"
        print(f"[ERROR] {report['error']}")
        return report

    # 3. SHA 비교
    if notion_sha and notion_sha.startswith(git_sha[:8]):
        report["status"] = "MATCH"
        print(f"[✅ E-01 PASS] SHA 일치: GitHub={git_sha[:8]} | Notion={notion_sha[:8]}")
    else:
        report["status"] = "MISMATCH"
        print(f"[⚠️  E-01 FAIL] SHA 불일치 감지 → E-01 태깅")
        print(f"    GitHub  SHA: {git_sha[:8]}")
        print(f"    Notion  SHA: {notion_sha[:8] if notion_sha else '없음'}")

        # 4. auto-sync
        if auto_sync:
            print("[AUTO-SYNC] Notion SHA 업데이트 시도...")
            ok = update_notion_sha(page_id, notion_token, git_sha, short_sha)
            if ok:
                append_ssot_block(page_id, notion_token, git_sha, notion_sha, "SYNCED")
                report["synced"] = True
                report["status"] = "SYNCED"
                print(f"[✅] Notion SHA 업데이트 완료: {short_sha}")
            else:
                print("[❌] Notion SHA 업데이트 실패 — 수동 확인 필요")
        else:
            append_ssot_block(page_id, notion_token, git_sha, notion_sha, "MISMATCH")

    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SSOT SHA Validator (Section B)")
    parser.add_argument("--page-id", required=True, help="Notion Hub 페이지 ID")
    parser.add_argument("--auto-sync", action="store_true", help="불일치 시 Notion 자동 업데이트")
    parser.add_argument("--output", default="", help="JSON 리포트 출력 경로")
    parser.add_argument("--root", default=".", help="git 루트 경로")
    args = parser.parse_args()

    notion_token = os.environ.get("NOTION_API_KEY", "")
    if not notion_token:
        print("[ERROR] NOTION_API_KEY 환경변수 미설정 — E-08 태깅")
        sys.exit(1)

    report = run_ssot_validation(
        page_id=args.page_id,
        notion_token=notion_token,
        auto_sync=args.auto_sync,
        cwd=args.root,
    )

    print(f"\nSSoT 검증 결과: {report['status']}")

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2))
        print(f"리포트 저장: {out}")
