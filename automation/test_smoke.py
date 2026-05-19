#!/usr/bin/env python3
"""
Smoke Test — AI Intel Pipeline 연결 검증

실행:
  export PERPLEXITY_API_KEY="pplx-xxxx"
  export NOTION_API_KEY="secret_xxxx"
  python automation/test_smoke.py

검사 항목:
  [1] 환경변수 (Secrets) 설정 여부
  [2] Perplexity API 키 유효성 (minimal 1-call)
  [3] Notion API 키 + C-31 page 접근 가능 여부
  [4] 4개 스크립트 import 에러 없는지 확인
  [5] output 디렉토리 쓰기 권한
"""

import os
import sys
import json
import importlib.util
from pathlib import Path

# ── ANSI 색상
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

NOTION_C31_PAGE_ID = "34a55ed436f0814d9cffe6a2f0816e29"

results = []

def ok(label, detail=""):
    msg = f"  {GREEN}✅ PASS{RESET}  {label}"
    if detail:
        msg += f"  {BLUE}({detail}){RESET}"
    print(msg)
    results.append(("PASS", label))

def fail(label, detail=""):
    msg = f"  {RED}❌ FAIL{RESET}  {label}"
    if detail:
        msg += f"  {RED}→ {detail}{RESET}"
    print(msg)
    results.append(("FAIL", label))

def warn(label, detail=""):
    msg = f"  {YELLOW}⚠️  WARN{RESET}  {label}"
    if detail:
        msg += f"  {YELLOW}({detail}){RESET}"
    print(msg)
    results.append(("WARN", label))

def section(title):
    print(f"\n{BOLD}{BLUE}{'─'*55}{RESET}")
    print(f"{BOLD}  {title}{RESET}")
    print(f"{BOLD}{BLUE}{'─'*55}{RESET}")


# ════════════════════════════════════════════════════
# [1] 환경변수 확인
# ════════════════════════════════════════════════════
section("[1] 환경변수 (Secrets) 설정 확인")

PERPLEXITY_API_KEY = os.environ.get("PERPLEXITY_API_KEY", "")
NOTION_API_KEY     = os.environ.get("NOTION_API_KEY", "")

if PERPLEXITY_API_KEY and PERPLEXITY_API_KEY.startswith("pplx-"):
    ok("PERPLEXITY_API_KEY", f"pplx-****{PERPLEXITY_API_KEY[-4:]}")
elif PERPLEXITY_API_KEY:
    warn("PERPLEXITY_API_KEY", "설정됨 (pplx- prefix 없음 — 확인 필요)")
else:
    fail("PERPLEXITY_API_KEY", "미설정 — export PERPLEXITY_API_KEY=pplx-xxx")

if NOTION_API_KEY and NOTION_API_KEY.startswith("secret_"):
    ok("NOTION_API_KEY", f"secret_****{NOTION_API_KEY[-4:]}")
elif NOTION_API_KEY:
    warn("NOTION_API_KEY", "설정됨 (secret_ prefix 없음 — 확인 필요)")
else:
    fail("NOTION_API_KEY", "미설정 — export NOTION_API_KEY=secret_xxx")


# ════════════════════════════════════════════════════
# [2] Perplexity API 유효성 (sonar, 1회 최소 호출)
# ════════════════════════════════════════════════════
section("[2] Perplexity API 연결 테스트")

if not PERPLEXITY_API_KEY:
    warn("SKIP", "API 키 없음")
else:
    try:
        import requests
        resp = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "sonar",
                "messages": [{"role": "user", "content": "ping"}],
                "max_tokens": 5,
            },
            timeout=15,
        )
        if resp.status_code == 200:
            model = resp.json().get("model", "unknown")
            ok("Perplexity API", f"HTTP 200 · model={model}")
        elif resp.status_code == 401:
            fail("Perplexity API", "HTTP 401 — API 키 오류 또는 만료")
        elif resp.status_code == 429:
            warn("Perplexity API", "HTTP 429 — Rate limit (키는 유효)")
        else:
            warn("Perplexity API", f"HTTP {resp.status_code} — {resp.text[:80]}")
    except requests.exceptions.Timeout:
        fail("Perplexity API", "Timeout (네트워크 확인)")
    except Exception as e:
        fail("Perplexity API", str(e)[:80])


# ════════════════════════════════════════════════════
# [3] Notion API 키 + C-31 page 접근
# ════════════════════════════════════════════════════
section("[3] Notion API 연결 + C-31 페이지 접근 테스트")

if not NOTION_API_KEY:
    warn("SKIP", "API 키 없음")
else:
    try:
        import requests
        # 3-a. API 키 자체 유효성
        resp = requests.get(
            "https://api.notion.com/v1/users/me",
            headers={
                "Authorization": f"Bearer {NOTION_API_KEY}",
                "Notion-Version": "2022-06-28",
            },
            timeout=10,
        )
        if resp.status_code == 200:
            bot_name = resp.json().get("name", "unknown")
            ok("Notion API 키", f"bot={bot_name}")
        elif resp.status_code == 401:
            fail("Notion API 키", "HTTP 401 — Integration Token 오류")
        else:
            warn("Notion API 키", f"HTTP {resp.status_code}")

        # 3-b. C-31 페이지 접근
        resp2 = requests.get(
            f"https://api.notion.com/v1/pages/{NOTION_C31_PAGE_ID}",
            headers={
                "Authorization": f"Bearer {NOTION_API_KEY}",
                "Notion-Version": "2022-06-28",
            },
            timeout=10,
        )
        if resp2.status_code == 200:
            title_block = resp2.json().get("properties", {}).get("title", {})
            ok("Notion C-31 페이지", f"page_id={NOTION_C31_PAGE_ID[:8]}… 접근 성공")
        elif resp2.status_code == 404:
            fail("Notion C-31 페이지", "HTTP 404 — page_id 오류 또는 Integration 미연결")
        elif resp2.status_code == 403:
            fail("Notion C-31 페이지", "HTTP 403 — C-31 페이지에 Integration 연결 필요")
        else:
            warn("Notion C-31 페이지", f"HTTP {resp2.status_code}")
    except Exception as e:
        fail("Notion API", str(e)[:80])


# ════════════════════════════════════════════════════
# [4] 4개 스크립트 import 에러 확인
# ════════════════════════════════════════════════════
section("[4] automation/ 스크립트 import 검증")

SCRIPTS = [
    "automation/ai_intel_collector.py",
    "automation/ai_ew_detector.py",
    "automation/kg_delta_generator.py",
    "automation/notion_c31_updater.py",
]

for script_path in SCRIPTS:
    path = Path(script_path)
    if not path.exists():
        fail(path.name, f"파일 없음 — {script_path}")
        continue
    try:
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod  = importlib.util.module_from_spec(spec)
        # argparse가 sys.argv를 파싱하지 않도록 격리
        _argv = sys.argv
        sys.argv = [path.name]
        try:
            spec.loader.exec_module(mod)
        except SystemExit:
            pass  # argparse --help 등 정상 종료는 무시
        finally:
            sys.argv = _argv
        ok(path.name)
    except ImportError as e:
        fail(path.name, f"ImportError: {e}")
    except Exception as e:
        warn(path.name, f"{type(e).__name__}: {str(e)[:60]}")


# ════════════════════════════════════════════════════
# [5] output 디렉토리 쓰기 권한
# ════════════════════════════════════════════════════
section("[5] output/ai_intel 디렉토리 쓰기 권한")

OUT_DIR = Path("output/ai_intel")
try:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    test_file = OUT_DIR / ".smoke_write_test"
    test_file.write_text("ok")
    test_file.unlink()
    ok("output/ai_intel", "디렉토리 생성 및 쓰기 성공")
except Exception as e:
    fail("output/ai_intel", str(e))


# ════════════════════════════════════════════════════
# 최종 결과 요약
# ════════════════════════════════════════════════════
print(f"\n{BOLD}{'═'*55}{RESET}")
print(f"{BOLD}  🔬 Smoke Test 결과 요약{RESET}")
print(f"{BOLD}{'═'*55}{RESET}")

passed = sum(1 for r in results if r[0] == "PASS")
warned = sum(1 for r in results if r[0] == "WARN")
failed = sum(1 for r in results if r[0] == "FAIL")
total  = len(results)

print(f"  총 {total}건  →  {GREEN}PASS {passed}{RESET}  /  {YELLOW}WARN {warned}{RESET}  /  {RED}FAIL {failed}{RESET}")

if failed == 0 and warned == 0:
    print(f"\n  {GREEN}{BOLD}🎉 모든 검사 통과 — 파이프라인 실행 준비 완료!{RESET}")
    print(f"  다음 단계: GitHub Actions → PE · AI Intel Weekly Digest → Run workflow")
elif failed == 0:
    print(f"\n  {YELLOW}{BOLD}⚠️  경고 있음 — 확인 후 실행 권장{RESET}")
else:
    print(f"\n  {RED}{BOLD}❌ 실패 항목 수정 후 재실행{RESET}")
    for r in results:
        if r[0] == "FAIL":
            print(f"     → {r[1]}")

print()
sys.exit(1 if failed > 0 else 0)
