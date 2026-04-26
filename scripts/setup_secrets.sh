#!/usr/bin/env bash
# =============================================================
# PE-7 GitHub Secrets 등록 헬퍼 스크립트
# PE-1/PE-2/PE-3 파이프라인 연계에 필요한 모든 Secrets 설정
# =============================================================
# 사전 요구사항:
#   brew install gh   →  gh auth login
# 실행:
#   chmod +x scripts/setup_secrets.sh
#   ./scripts/setup_secrets.sh
# =============================================================

set -euo pipefail

REPO="GilbertKwak/prompt-engineering-system"
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_RED='\033[0;31m'
COLOR_RESET='\033[0m'

log_info()    { echo -e "${COLOR_GREEN}[INFO]${COLOR_RESET}  $*"; }
log_warn()    { echo -e "${COLOR_YELLOW}[WARN]${COLOR_RESET}  $*"; }
log_error()   { echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} $*"; }
log_section() { echo -e "\n${COLOR_YELLOW}━━━ $* ━━━${COLOR_RESET}"; }

# GitHub CLI 로그인 확인
check_gh_auth() {
  if ! gh auth status &>/dev/null; then
    log_error "GitHub CLI 미로그인. 'gh auth login' 먼저 실행하세요."
    exit 1
  fi
  log_info "GitHub CLI 인증 확인 완료"
}

# Secret 설정 함수 (값 입력 대화형)
set_secret() {
  local secret_name="$1"
  local description="$2"
  local example="${3:-}"

  echo
  log_warn "Secret: ${secret_name}"
  echo "  📋 설명: ${description}"
  [ -n "$example" ] && echo "  💡 예시: ${example}"

  # 이미 설정된 경우 스킵 옵션
  echo -n "  값 입력 (Enter=스킵, 이미 설정됨): "
  IFS= read -r -s secret_value
  echo

  if [ -z "$secret_value" ]; then
    log_warn "${secret_name} 스킵됨 (기존 값 유지)"
    return 0
  fi

  echo "$secret_value" | gh secret set "$secret_name" --repo "$REPO"
  log_info "${secret_name} 등록 완료 ✓"
}

# JSON 파일로 Secret 설정
set_secret_from_file() {
  local secret_name="$1"
  local description="$2"

  echo
  log_warn "Secret: ${secret_name}"
  echo "  📋 설명: ${description}"
  echo -n "  JSON 파일 경로 입력 (예: ~/Downloads/service-account.json): "
  read -r file_path

  file_path="${file_path/#\~/$HOME}"

  if [ -z "$file_path" ]; then
    log_warn "${secret_name} 스킵됨"
    return 0
  fi

  if [ ! -f "$file_path" ]; then
    log_error "파일 없음: $file_path"
    return 1
  fi

  gh secret set "$secret_name" --repo "$REPO" < "$file_path"
  log_info "${secret_name} 등록 완료 ✓"
}

main() {
  echo
  echo "╔═══════════════════════════════════════════════════════╗"
  echo "║   PE-7 Secrets Setup — PE-1/PE-2/PE-3 Integration   ║"
  echo "╚═══════════════════════════════════════════════════════╝"
  echo "  Repository: ${REPO}"

  check_gh_auth

  # ─── 1. Notion ───────────────────────────────────────────
  log_section "1/4  Notion"

  set_secret \
    "NOTION_API_KEY" \
    "Notion Integration Token (notion.so → Settings → Integrations)" \
    "secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

  set_secret \
    "NOTION_KPI_DB_ID" \
    "Notion DB URL의 /d/{32자리}/ 부분 (하이픈 제거)" \
    "abcdef1234567890abcdef1234567890"

  # ─── 2. Google Sheets ────────────────────────────────────
  log_section "2/4  Google Sheets"

  set_secret \
    "GOOGLE_SHEETS_ID" \
    "Sheets URL의 /spreadsheets/d/{ID}/edit 에서 {ID}" \
    "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms"

  set_secret_from_file \
    "GOOGLE_SERVICE_ACCOUNT_JSON" \
    "GCP Console → IAM → 서비스 계정 → KEYS → JSON 다운로드"

  # ─── 3. Slack ────────────────────────────────────────────
  log_section "3/4  Slack"

  set_secret \
    "SLACK_WEBHOOK_URL" \
    "api.slack.com → Apps → Incoming Webhooks → Add Webhook" \
    "https://hooks.slack.com/services/T.../B.../xxx"

  # ─── 검증 실행 ────────────────────────────────────────────
  log_section "4/4  등록된 Secrets 검증"

  echo
  log_info "등록된 Secrets 목록:"
  gh secret list --repo "$REPO" | grep -E \
    "NOTION_API_KEY|NOTION_KPI_DB_ID|GOOGLE_SHEETS_ID|GOOGLE_SERVICE_ACCOUNT_JSON|SLACK_WEBHOOK_URL" \
    || true

  echo
  log_info "Secrets 설정 완료! PE-1/PE-2/PE-3 파이프라인 연계 준비됨."
  echo
  echo "  다음 단계:"
  echo "  1. python scripts/validate_secrets.py  ← 유효성 검증"
  echo "  2. gh workflow run pe7_daily_pipeline.yml  ← 파이프라인 테스트"
  echo
}

main "$@"
