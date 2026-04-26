#!/bin/bash
# PE-7 v2.0 — GitHub Secrets 일괄 등록
# 사용법: bash scripts/pe7/setup/register_secrets.sh
# 사전 조건: gh auth login 완료
# Gilbert Kwak | 2026-04-26

set -e

REPO="GilbertKwak/prompt-engineering-system"
ECHO_OK="✅"
ECHO_WARN="⚠️ "
ECHO_FAIL="❌"

echo "====================================================="
echo " PE-7 v2.0 — GitHub Secrets 일괄 등록"
echo "====================================================="
echo ""

# gh CLI 로그인 확인
if ! gh auth status &>/dev/null; then
    echo "$ECHO_FAIL gh CLI 로그인이 필요합니다: gh auth login"
    exit 1
fi
echo "$ECHO_OK gh CLI 로그인 확인"
echo ""

# ── 1. NOTION_TOKEN ────────────────────────────────────
echo "[1/8] NOTION_TOKEN"
read -sp "  입력 (Notion Integration Token): " NOTION_TOKEN_VAL
echo ""
echo "$NOTION_TOKEN_VAL" | gh secret set NOTION_TOKEN -R "$REPO"
echo "$ECHO_OK NOTION_TOKEN 등록 완료"
echo ""

# ── 2. NOTION_KPI_DB_ID ───────────────────────────────
echo "[2/8] NOTION_KPI_DB_ID"
echo "  힉트: Notion KPI 데이터베이스 URL에서 32자리 ID 복사"
read -sp "  입력: " NOTION_KPI_VAL
echo ""
echo "$NOTION_KPI_VAL" | gh secret set NOTION_KPI_DB_ID -R "$REPO"
echo "$ECHO_OK NOTION_KPI_DB_ID 등록 완료"
echo ""

# ── 3. GOOGLE_SHEETS_ID ──────────────────────────────
echo "[3/8] GOOGLE_SHEETS_ID"
echo "  힉트: Google Sheets URL 중 /spreadsheets/d/{ID}/ 부분"
read -sp "  입력: " GSHEETS_VAL
echo ""
echo "$GSHEETS_VAL" | gh secret set GOOGLE_SHEETS_ID -R "$REPO"
echo "$ECHO_OK GOOGLE_SHEETS_ID 등록 완료"
echo ""

# ── 4. GOOGLE_SERVICE_ACCOUNT_JSON ─────────────────────
echo "[4/8] GOOGLE_SERVICE_ACCOUNT_JSON"
echo "  힉트: GCP 서비스 계정 JSON 파일을 gcp_sa_key.json으로 저장 후 실행"
if [ -f "gcp_sa_key.json" ]; then
    cat gcp_sa_key.json | gh secret set GOOGLE_SERVICE_ACCOUNT_JSON -R "$REPO"
    echo "$ECHO_OK GOOGLE_SERVICE_ACCOUNT_JSON 등록 완료 (gcp_sa_key.json 사용)"
else
    echo "$ECHO_WARN gcp_sa_key.json 없음 → 수동 입력:"
    read -sp "  JSON 전체 문자열 표룰여넣기: " GSA_VAL
    echo ""
    echo "$GSA_VAL" | gh secret set GOOGLE_SERVICE_ACCOUNT_JSON -R "$REPO"
    echo "$ECHO_OK GOOGLE_SERVICE_ACCOUNT_JSON 등록 완료"
fi
echo ""

# ── 5. OPENAI_API_KEY ─────────────────────────────────
echo "[5/8] OPENAI_API_KEY"
read -sp "  입력 (sk-...): " OPENAI_VAL
echo ""
echo "$OPENAI_VAL" | gh secret set OPENAI_API_KEY -R "$REPO"
echo "$ECHO_OK OPENAI_API_KEY 등록 완료"
echo ""

# ── 6. REDDIT_CLIENT_ID ──────────────────────────────
echo "[6/8] REDDIT_CLIENT_ID"
echo "  힉트: reddit.com/prefs/apps → 앱 이름 아래 14자리 코드"
read -sp "  입력: " REDDIT_ID_VAL
echo ""
echo "$REDDIT_ID_VAL" | gh secret set REDDIT_CLIENT_ID -R "$REPO"
echo "$ECHO_OK REDDIT_CLIENT_ID 등록 완료"
echo ""

# ── 7. REDDIT_SECRET ────────────────────────────────
echo "[7/8] REDDIT_SECRET"
read -sp "  입력: " REDDIT_SEC_VAL
echo ""
echo "$REDDIT_SEC_VAL" | gh secret set REDDIT_SECRET -R "$REPO"
echo "$ECHO_OK REDDIT_SECRET 등록 완료"
echo ""

# ── 8. SLACK_WEBHOOK_URL ────────────────────────────
echo "[8/8] SLACK_WEBHOOK_URL"
echo "  힉트: Slack App Directory → Incoming Webhooks → Webhook URL"
read -sp "  입력 (https://hooks.slack.com/...): " SLACK_VAL
echo ""
echo "$SLACK_VAL" | gh secret set SLACK_WEBHOOK_URL -R "$REPO"
echo "$ECHO_OK SLACK_WEBHOOK_URL 등록 완료"
echo ""

# ── 최종 확인 ────────────────────────────────────────
echo "====================================================="
echo " 구동 확인"
echo "====================================================="
gh secret list -R "$REPO"
echo ""

# 등록된 Secrets 개수 확인
COUNT=$(gh secret list -R "$REPO" | wc -l)
if [ "$COUNT" -ge 8 ]; then
    echo "$ECHO_OK $COUNT개 Secrets 등록 완료 — PE-7 v2.0 실행 준비 완료!"
    echo ""
    echo "다음 단계:"
    echo "  gh workflow run pe7_e0n_validate.yml -R $REPO"
else
    echo "$ECHO_WARN Secrets 등록 불완전 ($COUNT/8) — 누락된 Secret 재등록 필요"
fi

echo ""
echo "[E-10 사전 방지] python scripts/pe7/setup/verify_setup.py 뗄 실행 권장"
