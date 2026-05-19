#!/usr/bin/env python3
"""
Smoke Test — AI Intel Weekly Pipeline
Perplexity API / Notion API / 4개 스크립트 import 검증
Usage: python automation/test_smoke.py
"""

import os
import sys
import json
import importlib.util
from pathlib import Path

# .env 지원 (python-dotenv 있을 경우)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

PASS = "\033[92m[PASS]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"
INFO = "\033[94m[INFO]\033[0m"

results = []

def check(label: str, ok: bool, detail: str = ""):
    tag = PASS if ok else FAIL
    msg = f"{tag} {label}"
    if detail:
        msg += f"  →  {detail}"
    print(msg)
    results.append((label, ok))


# ──────────────────────────────────────────
# 1. 환경변수 존재 확인
# ──────────────────────────────────────────
print("\n=== [1/4] 환경변수 확인 ===")
PPLX_KEY = os.getenv("PERPLEXITY_API_KEY", "")
NOTION_KEY = os.getenv("NOTION_API_KEY", "")
NOTION_PAGE = os.getenv("NOTION_C31_PAGE_ID", "34a55ed436f0814d9cffe6a2f0816e29")

check("PERPLEXITY_API_KEY 존재", bool(PPLX_KEY), f"{'설정됨 (길이 ' + str(len(PPLX_KEY)) + ')' if PPLX_KEY else '미설정 — export PERPLEXITY_API_KEY=pplx-xxxx'}")
check("NOTION_API_KEY 존재", bool(NOTION_KEY), f"{'설정됨 (길이 ' + str(len(NOTION_KEY)) + ')' if NOTION_KEY else '미설정 — export NOTION_API_KEY=secret_xxxx'}")
check("NOTION_C31_PAGE_ID", bool(NOTION_PAGE), NOTION_PAGE or "미설정")


# ──────────────────────────────────────────
# 2. Perplexity API Minimal Call
# ──────────────────────────────────────────
print("\n=== [2/4] Perplexity API 연결 테스트 ===")
import requests

if PPLX_KEY:
    try:
        resp = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {PPLX_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "sonar",
                "messages": [{"role": "user", "content": "Reply with just: OK"}],
                "max_tokens": 5,
            },
            timeout=15,
        )
        if resp.status_code == 200:
            content = resp.json()["choices"][0]["message"]["content"].strip()
            check("Perplexity sonar API 호출", True, f"응답: '{content}'")
        elif resp.status_code == 401:
            check("Perplexity sonar API 호출", False, "401 Unauthorized — API 키 확인 필요")
        elif resp.status_code == 429:
            check("Perplexity sonar API 호출", True, "429 Rate limit (키 유효, 할당량 초과)")
        else:
            check("Perplexity sonar API 호출", False, f"HTTP {resp.status_code}: {resp.text[:120]}")
    except requests.exceptions.Timeout:
        check("Perplexity sonar API 호출", False, "Timeout (15s) — 네트워크 확인")
    except Exception as e:
        check("Perplexity sonar API 호출", False, str(e))
else:
    check("Perplexity sonar API 호출", False, "API 키 없음 — 건너뜀")


# ──────────────────────────────────────────
# 3. Notion API + C-31 페이지 접근 확인
# ──────────────────────────────────────────
print("\n=== [3/4] Notion API 연결 테스트 ===")

if NOTION_KEY:
    # 3-a. 사용자 인증 확인
    try:
        r = requests.get(
            "https://api.notion.com/v1/users/me",
            headers={
                "Authorization": f"Bearer {NOTION_KEY}",
                "Notion-Version": "2022-06-28",
            },
            timeout=10,
        )
        if r.status_code == 200:
            bot_name = r.json().get("name", "unknown")
            check("Notion API 인증", True, f"Bot: {bot_name}")
        else:
            check("Notion API 인증", False, f"HTTP {r.status_code}")
    except Exception as e:
        check("Notion API 인증", False, str(e))

    # 3-b. C-31 페이지 접근
    page_id = NOTION_PAGE.replace("-", "")
    try:
        r2 = requests.get(
            f"https://api.notion.com/v1/pages/{page_id}",
            headers={
                "Authorization": f"Bearer {NOTION_KEY}",
                "Notion-Version": "2022-06-28",
            },
            timeout=10,
        )
        if r2.status_code == 200:
            title_parts = r2.json().get("properties", {}).get("title", {}).get("title", [])
            title = title_parts[0]["plain_text"] if title_parts else "(제목 없음)"
            check("C-31 페이지 접근", True, f"페이지명: '{title}'")
        elif r2.status_code == 404:
            check("C-31 페이지 접근", False, "404 — Page ID 확인 또는 Integration 연결 필요")
        elif r2.status_code == 403:
            check("C-31 페이지 접근", False, "403 — Notion 페이지에 Integration 연결 안 됨")
        else:
            check("C-31 페이지 접근", False, f"HTTP {r2.status_code}")
    except Exception as e:
        check("C-31 페이지 접근", False, str(e))
else:
    check("Notion API 인증", False, "API 키 없음 — 건너뜀")
    check("C-31 페이지 접근", False, "API 키 없음 — 건너뜀")


# ──────────────────────────────────────────
# 4. 4개 스크립트 Import 에러 확인
# ──────────────────────────────────────────
print("\n=== [4/4] 스크립트 Import 검증 ===")

SCRIPT_DIR = Path(__file__).parent
SCRIPTS = [
    "ai_intel_collector",
    "ai_ew_detector",
    "kg_delta_generator",
    "notion_c31_updater",
]

for name in SCRIPTS:
    path = SCRIPT_DIR / f"{name}.py"
    if not path.exists():
        check(f"{name}.py import", False, "파일 없음")
        continue
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        # __name__ guard로 main() 실행 방지
        mod.__name__ = f"_smoke_{name}"
        spec.loader.exec_module(mod)
        check(f"{name}.py import", True)
    except SyntaxError as e:
        check(f"{name}.py import", False, f"SyntaxError: {e}")
    except ImportError as e:
        check(f"{name}.py import", False, f"ImportError: {e} — pip install -r requirements.txt 실행")
    except SystemExit:
        check(f"{name}.py import", True, "(SystemExit — argparse, 정상)")
    except Exception as e:
        check(f"{name}.py import", False, f"{type(e).__name__}: {e}")


# ──────────────────────────────────────────
# 최종 결과 요약
# ──────────────────────────────────────────
print("\n" + "=" * 50)
total = len(results)
passed = sum(1 for _, ok in results if ok)
failed = total - passed

if failed == 0:
    print(f"\033[92m✅ 전체 {total}개 PASS — 파이프라인 준비 완료\033[0m")
else:
    print(f"\033[93m⚠️  {passed}/{total} PASS  |  {failed}개 FAIL — 위 항목 확인 필요\033[0m")

print("=" * 50)
sys.exit(0 if failed == 0 else 1)
