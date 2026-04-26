#!/usr/bin/env python3
"""
PE-7 v2.0 — 실행 전 사전 점검 스크립트
워크플로우 실행 전 모든 요구사항 스캔
E-10 (환경변수 미설정) 사전 방지
Gilbert Kwak | 2026-04-26
"""
import os, sys, subprocess, json
from pathlib import Path

PASS, WARN, FAIL = "✅", "⚠️ ", "❌"

results = []

def check(name: str, ok: bool, detail: str, critical: bool = True):
    status = PASS if ok else (FAIL if critical else WARN)
    level  = "PASS" if ok else ("FAIL" if critical else "WARN")
    results.append({"name": name, "status": level, "detail": detail})
    print(f"  {status} {name}: {detail}")
    return ok

print("\n" + "="*55)
print(" PE-7 v2.0 — 실행 전 사전 점검")
print("="*55 + "\n")

# 1. Python 버전
v = sys.version_info
check("Python 3.11+", v.major == 3 and v.minor >= 11,
      f"Python {v.major}.{v.minor}.{v.micro}")

# 2. 필수 패키지 (PE-7 스크립트 의존성)
required_pkgs = [
    "requests", "pandas", "numpy", "scipy",
    "gspread", "pptx", "feedparser", "praw", "openai",
]
for pkg in required_pkgs:
    try:
        __import__(pkg)
        check(f"pkg:{pkg}", True, "설치됨", critical=False)
    except ImportError:
        check(f"pkg:{pkg}", False, "맵 설치: pip install " + pkg, critical=False)

# 3. 환경변수 (E-10 사전 방지)
required_env = [
    "NOTION_TOKEN",
    "NOTION_KPI_DB_ID",
    "GOOGLE_SHEETS_ID",
    "GOOGLE_SERVICE_ACCOUNT_JSON",
    "OPENAI_API_KEY",
    "REDDIT_CLIENT_ID",
    "REDDIT_SECRET",
    "SLACK_WEBHOOK_URL",
]
env_ok = 0
for env in required_env:
    val = os.environ.get(env, "")
    ok  = bool(val) and val != "placeholder"
    check(f"env:{env}", ok, "설정됨" if ok else "❌ 미설정 (E-10)")
    if ok: env_ok += 1

# 4. 스크립트 파일 존재
scripts = [
    "scripts/pe7/sheets_exporter.py",
    "scripts/pe7/supply_chain_collector.py",
    "scripts/pe7/sentiment_analyzer.py",
    "scripts/pe7/markowitz.py",
    "scripts/pe7/black_litterman.py",
    "scripts/pe7/monthly_ppt_gen.py",
]
for s in scripts:
    check(f"script:{Path(s).name}", Path(s).exists(), "있음" if Path(s).exists() else "없음", critical=False)

# 5. 워크플로우 파일
workflows = [
    ".github/workflows/pe7_daily_pipeline.yml",
    ".github/workflows/pe7_monthly_report.yml",
    ".github/workflows/pe7_e0n_validate.yml",
]
for w in workflows:
    check(f"workflow:{Path(w).name}", Path(w).exists(), "있음" if Path(w).exists() else "없음")

# 6. Notion 연결 테스트
try:
    import requests
    token = os.environ.get("NOTION_TOKEN", "")
    if token:
        res = requests.get(
            "https://api.notion.com/v1/users/me",
            headers={"Authorization": f"Bearer {token}", "Notion-Version": "2022-06-28"},
            timeout=8
        )
        check("Notion API", res.status_code == 200,
              f"HTTP {res.status_code}" + (" — 연결 성공" if res.status_code == 200 else " — 토큰 유효성 확인 필요"))
    else:
        check("Notion API", False, "NOTION_TOKEN 미설정")
except Exception as e:
    check("Notion API", False, f"E-05 연결 실패: {e}")

# ── 종합 판정 ─────────────────────────────────────────
print("\n" + "="*55)
total_fail = sum(1 for r in results if r["status"] == "FAIL")
total_warn = sum(1 for r in results if r["status"] == "WARN")

if total_fail == 0 and total_warn == 0:
    print(" 🟢 전체 PASS — PE-7 v2.0 실행 준비 완료")
elif total_fail == 0:
    print(f" 🟡 WARN {total_warn}개 — 필수 항목은 이상 없음")
else:
    print(f" 🔴 FAIL {total_fail}개 — 어보 준비 확인 후 다시 시도")
    print(" 특히 Secrets 8개 등록: bash scripts/pe7/setup/register_secrets.sh")

print(f" PASS: {sum(1 for r in results if r['status'] == 'PASS')} | "
      f"WARN: {total_warn} | FAIL: {total_fail}")
print("="*55)

# CI: FAIL 시 exit(1)
if total_fail > 0:
    sys.exit(1)
