#!/bin/bash
# =============================================================================
# register_secrets.sh — PE-7 자동화 GitHub Secrets 5종 일괄 등록
# =============================================================================
# 사용법:
#   chmod +x register_secrets.sh
#   ./register_secrets.sh
#
# 사전 조건:
#   - gh CLI 설치 및 로그인 (gh auth login)
#   - pe7-automation-xxxx.json 다운로드 완료
# =============================================================================

set -euo pipefail

REPO="GilbertKwak/prompt-engineering-system"
GCP_JSON_PATH="${GCP_JSON_PATH:-~/Downloads/pe7-automation-xxxx.json}"

echo "🔐 PE-7 GitHub Secrets 등록 시작"
echo "Repository: $REPO"
echo "==========================================="

# -------------------------------------------------------
# Secret 1: NOTION_TOKEN
# -------------------------------------------------------
if [ -z "${NOTION_TOKEN:-}" ]; then
  echo ""
  read -rsp "🔑 NOTION_TOKEN를 입력하세요 (secret_xxx...): " NOTION_TOKEN
  echo ""
fi
echo "$NOTION_TOKEN" | gh secret set NOTION_TOKEN -R "$REPO" --body-stdin
echo "✅ NOTION_TOKEN 등록 완료"

# -------------------------------------------------------
# Secret 2: NOTION_KPI_DB_ID
# -------------------------------------------------------
if [ -z "${NOTION_KPI_DB_ID:-}" ]; then
  echo ""
  read -rsp "🔑 NOTION_KPI_DB_ID를 입력하세요 (32자리, 하이픈 없음): " NOTION_KPI_DB_ID
  echo ""
fi
echo "$NOTION_KPI_DB_ID" | gh secret set NOTION_KPI_DB_ID -R "$REPO" --body-stdin
echo "✅ NOTION_KPI_DB_ID 등록 완료"

# -------------------------------------------------------
# Secret 3: GOOGLE_SHEETS_ID
# -------------------------------------------------------
if [ -z "${GOOGLE_SHEETS_ID:-}" ]; then
  echo ""
  read -rsp "🔑 GOOGLE_SHEETS_ID를 입력하세요 (/spreadsheets/d/{ID}/의 ID): " GOOGLE_SHEETS_ID
  echo ""
fi
echo "$GOOGLE_SHEETS_ID" | gh secret set GOOGLE_SHEETS_ID -R "$REPO" --body-stdin
echo "✅ GOOGLE_SHEETS_ID 등록 완료"

# -------------------------------------------------------
# Secret 4: GOOGLE_SERVICE_ACCOUNT_JSON
# -------------------------------------------------------
GCP_JSON_PATH=$(eval echo "$GCP_JSON_PATH")
if [ ! -f "$GCP_JSON_PATH" ]; then
  echo ""
  read -rp "📂 GCP JSON 키 파일 경로를 입력하세요: " GCP_JSON_PATH
fi
gh secret set GOOGLE_SERVICE_ACCOUNT_JSON -R "$REPO" < "$GCP_JSON_PATH"
echo "✅ GOOGLE_SERVICE_ACCOUNT_JSON 등록 완료"

# -------------------------------------------------------
# Secret 5: SLACK_WEBHOOK_URL
# -------------------------------------------------------
if [ -z "${SLACK_WEBHOOK_URL:-}" ]; then
  echo ""
  read -rsp "🔑 SLACK_WEBHOOK_URL를 입력하세요 (https://hooks.slack.com/...): " SLACK_WEBHOOK_URL
  echo ""
fi
echo "$SLACK_WEBHOOK_URL" | gh secret set SLACK_WEBHOOK_URL -R "$REPO" --body-stdin
echo "✅ SLACK_WEBHOOK_URL 등록 완료"

# -------------------------------------------------------
# 등록 결과 확인
# -------------------------------------------------------
echo ""
echo "=========================================="
echo "🎉 5종 Secrets 등록 완료!"
echo ""
echo "📋 등록된 Secrets 목록:"
gh secret list -R "$REPO"

echo ""
echo "🚀 다음 단계:"
echo "   gh workflow run pe7_e0n_validate.yml -R $REPO --ref main"
