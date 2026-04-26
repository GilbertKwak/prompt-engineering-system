#!/bin/bash
# =============================================================================
# register_secrets.sh — PE-7 자동화 파이프라인 GitHub Secrets 일괄 등록
# 작성일: 2026-04-26
# 관리자: Gilbert Kwak
# 레포:   GilbertKwak/prompt-engineering-system
# 참조:   Notion → 🔐 완전 자동화 Integration 설정 가이드 (v1.0)
# =============================================================================
# 사용법:
#   chmod +x setup/register_secrets.sh
#   ./setup/register_secrets.sh
#
# 필요 준비물:
#   1. gh CLI 설치 및 로그인 (gh auth login)
#   2. GCP 서비스 계정 JSON 키 파일 (~/.config/pe7/service-account.json)
#   3. 아래 변수값 직접 채워서 실행
# =============================================================================

set -euo pipefail

REPO="GilbertKwak/prompt-engineering-system"
SA_JSON_PATH="${HOME}/.config/pe7/service-account.json"  # JSON 키 경로 (수정 가능)

# --------------------------------------------------------------------------
# 색상 출력 헬퍼
# --------------------------------------------------------------------------
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# --------------------------------------------------------------------------
# 사전 확인
# --------------------------------------------------------------------------
command -v gh >/dev/null 2>&1 || error "gh CLI가 설치되지 않았습니다. https://cli.github.com 참조"
gh auth status >/dev/null 2>&1 || error "gh 로그인 필요: gh auth login"

info "대상 레포: ${REPO}"
info "======================================"

# --------------------------------------------------------------------------
# Secret 1: NOTION_TOKEN
# 출처: https://notion.so/my-integrations → Internal Integration Secret
# --------------------------------------------------------------------------
read -rsp "[1/5] NOTION_TOKEN (secret_xxx...): " NOTION_TOKEN_VAL
echo
[[ -z "${NOTION_TOKEN_VAL}" ]] && error "NOTION_TOKEN이 비어있습니다."
echo "${NOTION_TOKEN_VAL}" | gh secret set NOTION_TOKEN -R "${REPO}" --body ""
printf '%s' "${NOTION_TOKEN_VAL}" | gh secret set NOTION_TOKEN -R "${REPO}"
info "NOTION_TOKEN 등록 완료"

# --------------------------------------------------------------------------
# Secret 2: NOTION_KPI_DB_ID
# 출처: Notion KPI DB URL → /d/{32자리}/ 또는 UUID 하이픈 제거
# --------------------------------------------------------------------------
read -rp "[2/5] NOTION_KPI_DB_ID (32자리 hex, 하이픈 없음): " NOTION_KPI_DB_ID_VAL
[[ ${#NOTION_KPI_DB_ID_VAL} -ne 32 ]] && warn "32자리가 아닙니다 (입력값: ${#NOTION_KPI_DB_ID_VAL}자리) — 계속 진행합니다."
printf '%s' "${NOTION_KPI_DB_ID_VAL}" | gh secret set NOTION_KPI_DB_ID -R "${REPO}"
info "NOTION_KPI_DB_ID 등록 완료"

# --------------------------------------------------------------------------
# Secret 3: GOOGLE_SHEETS_ID
# 출처: Sheets URL → /spreadsheets/d/{ID}/edit 중 {ID} 부분
# --------------------------------------------------------------------------
read -rp "[3/5] GOOGLE_SHEETS_ID (Sheets URL의 /d/{ID}/ 부분): " GOOGLE_SHEETS_ID_VAL
[[ -z "${GOOGLE_SHEETS_ID_VAL}" ]] && error "GOOGLE_SHEETS_ID가 비어있습니다."
printf '%s' "${GOOGLE_SHEETS_ID_VAL}" | gh secret set GOOGLE_SHEETS_ID -R "${REPO}"
info "GOOGLE_SHEETS_ID 등록 완료"

# --------------------------------------------------------------------------
# Secret 4: GOOGLE_SERVICE_ACCOUNT_JSON
# 출처: GCP Console → IAM → 서비스 계정 → KEYS → JSON 다운로드
# --------------------------------------------------------------------------
if [[ ! -f "${SA_JSON_PATH}" ]]; then
  read -rp "[4/5] Service Account JSON 파일 경로: " SA_JSON_PATH
fi
[[ ! -f "${SA_JSON_PATH}" ]] && error "JSON 파일을 찾을 수 없습니다: ${SA_JSON_PATH}"
gh secret set GOOGLE_SERVICE_ACCOUNT_JSON -R "${REPO}" < "${SA_JSON_PATH}"
info "GOOGLE_SERVICE_ACCOUNT_JSON 등록 완료"

# --------------------------------------------------------------------------
# Secret 5: SLACK_WEBHOOK_URL
# 출처: api.slack.com → App → Incoming Webhooks → Webhook URL
# --------------------------------------------------------------------------
read -rp "[5/5] SLACK_WEBHOOK_URL (https://hooks.slack.com/services/...): " SLACK_WEBHOOK_URL_VAL
[[ ! "${SLACK_WEBHOOK_URL_VAL}" =~ ^https://hooks.slack.com ]] && warn "Slack Webhook URL 형식이 예상과 다릅니다. 확인 후 진행하세요."
printf '%s' "${SLACK_WEBHOOK_URL_VAL}" | gh secret set SLACK_WEBHOOK_URL -R "${REPO}"
info "SLACK_WEBHOOK_URL 등록 완료"

# --------------------------------------------------------------------------
# 최종 확인
# --------------------------------------------------------------------------
echo
info "======================================"
info "✅ 5종 Secrets 등록 완료!"
info "--------------------------------------"
gh secret list -R "${REPO}"
echo
info "다음 단계:"
info "  gh workflow run pe7_e0n_validate.yml -R ${REPO} --ref main"
info "  gh run watch -R ${REPO}"
