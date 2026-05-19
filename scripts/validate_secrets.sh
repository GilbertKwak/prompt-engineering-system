#!/usr/bin/env bash
# ============================================================
# Secrets & API 연결 검증 스크립트
# 사용법: bash scripts/validate_secrets.sh
# ============================================================
set -euo pipefail

PASS=0
FAIL=0

check() {
  local label="$1"
  local result="$2"
  if [ "$result" = "ok" ]; then
    echo "  [PASS] $label"
    PASS=$((PASS+1))
  else
    echo "  [FAIL] $label — $result"
    FAIL=$((FAIL+1))
  fi
}

echo ""
echo "=================================================="
echo " Secrets & API Validation"
echo "=================================================="
echo ""

# ── 1. 환경변수 존재 확인 ────────────────────────────────────
echo "[1] 환경변수 체크"
[ -n "${PERPLEXITY_API_KEY:-}" ] && check "PERPLEXITY_API_KEY 설정" "ok" || check "PERPLEXITY_API_KEY 설정" "미설정"
[ -n "${NOTION_API_KEY:-}" ] && check "NOTION_API_KEY 설정" "ok" || check "NOTION_API_KEY 설정" "미설정"
echo ""

# ── 2. Perplexity API 연결 테스트 ────────────────────────────
echo "[2] Perplexity API 연결 테스트"
if [ -n "${PERPLEXITY_API_KEY:-}" ]; then
  PPLX_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST "https://api.perplexity.ai/chat/completions" \
    -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"sonar","messages":[{"role":"user","content":"ping"}],"max_tokens":5}' \
    --max-time 15 2>/dev/null || echo "000")

  if [ "$PPLX_STATUS" = "200" ]; then
    check "Perplexity API (sonar) 응답" "ok"
  elif [ "$PPLX_STATUS" = "401" ]; then
    check "Perplexity API 인증" "401 Unauthorized — API Key 재확인 필요"
  elif [ "$PPLX_STATUS" = "429" ]; then
    check "Perplexity API" "429 Rate Limit — 잠시 후 재시도"
  else
    check "Perplexity API" "HTTP $PPLX_STATUS"
  fi
else
  check "Perplexity API" "SKIP (API key 미설정)"
fi
echo ""

# ── 3. Notion API 연결 테스트 ────────────────────────────────
echo "[3] Notion API 연결 테스트"
NOTION_PAGE_ID="34a55ed436f0814d9cffe6a2f0816e29"
if [ -n "${NOTION_API_KEY:-}" ]; then
  NOTION_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -X GET "https://api.notion.com/v1/pages/${NOTION_PAGE_ID}" \
    -H "Authorization: Bearer $NOTION_API_KEY" \
    -H "Notion-Version: 2022-06-28" \
    --max-time 15 2>/dev/null || echo "000")

  if [ "$NOTION_STATUS" = "200" ]; then
    check "Notion API + C-31 페이지 접근" "ok"
  elif [ "$NOTION_STATUS" = "401" ]; then
    check "Notion API 인증" "401 Unauthorized — Integration Token 재확인"
  elif [ "$NOTION_STATUS" = "404" ]; then
    check "Notion C-31 페이지" "404 Not Found — 페이지 ID 또는 Integration 연결 확인"
  else
    check "Notion API" "HTTP $NOTION_STATUS"
  fi
else
  check "Notion API" "SKIP (API key 미설정)"
fi
echo ""

# ── 4. Python 환경 확인 ──────────────────────────────────────
echo "[4] Python 환경"
PY_VER=$(python --version 2>&1 || python3 --version 2>&1 || echo "미설치")
check "Python 버전: $PY_VER" "ok"

for pkg in requests httpx notion-client tenacity rich; do
  pip show "$pkg" > /dev/null 2>&1 && check "pip: $pkg" "ok" || check "pip: $pkg" "미설치 (pip install $pkg)"
done
echo ""

# ── 5. 스크립트 파일 존재 확인 ──────────────────────────────
echo "[5] 스크립트 파일 확인"
for f in \
  automation/ai_intel_collector.py \
  automation/ai_ew_detector.py \
  automation/kg_delta_generator.py \
  automation/notion_c31_updater.py \
  automation/requirements.txt; do
  [ -f "$f" ] && check "$f" "ok" || check "$f" "파일 없음"
done
echo ""

# ── 결과 요약 ────────────────────────────────────────────────
echo "=================================================="
echo " 결과: PASS $PASS / FAIL $FAIL"
echo "=================================================="

if [ $FAIL -gt 0 ]; then
  echo " ⚠ 위 FAIL 항목을 해결 후 다시 실행하세요."
  exit 1
else
  echo " ✓ 모든 검증 통과! 파이프라인 실행 준비 완료."
fi
echo ""
