#!/usr/bin/env bash
# ============================================================
# AI Intel Weekly Pipeline — 로컬 테스트 스크립트
# 사용법: bash scripts/test_pipeline_local.sh [mode]
#   mode: quick   (1개 도메인, standard 스코프)
#         full    (전체 도메인, standard 스코프)
#         ew      (EW emergency 시뮬레이션)
# ============================================================
set -euo pipefail

# ── 환경변수 체크 ────────────────────────────────────────────
check_env() {
  local missing=0
  for var in PERPLEXITY_API_KEY NOTION_API_KEY; do
    if [ -z "${!var:-}" ]; then
      echo "[ERROR] 환경변수 미설정: $var"
      missing=1
    fi
  done
  if [ $missing -eq 1 ]; then
    echo ""
    echo "설정 방법:"
    echo "  export PERPLEXITY_API_KEY=pplx-xxxx"
    echo "  export NOTION_API_KEY=secret_xxxx"
    echo ""
    exit 1
  fi
  echo "[OK] 환경변수 확인 완료"
}

# ── 디렉토리 초기화 ──────────────────────────────────────────
MODE="${1:-quick}"
RUN_DATE=$(date +%Y-%m-%d)
WEEK_ID=$(date +%Y-W%V)
OUTPUT_DIR="output/ai_intel_${RUN_DATE}_${MODE}"
NOTION_PAGE_ID="34a55ed436f0814d9cffe6a2f0816e29"

mkdir -p "$OUTPUT_DIR"

echo ""
echo "======================================"
echo " AI Intel Pipeline — LOCAL TEST"
echo "======================================"
echo " Mode    : $MODE"
echo " Date    : $RUN_DATE"
echo " Week    : $WEEK_ID"
echo " Output  : $OUTPUT_DIR"
echo "======================================"
echo ""

check_env

# ── Python 의존성 확인 ───────────────────────────────────────
echo "[STEP 0] 의존성 설치 확인..."
pip install -q -r automation/requirements.txt
echo "[OK] 의존성 준비 완료"
echo ""

# ── QUICK MODE: 1개 도메인만 테스트 ─────────────────────────
if [ "$MODE" = "quick" ]; then
  echo "[STEP 1] Intel 수집 (enterprise_deployment, standard)"
  python automation/ai_intel_collector.py \
    --domain enterprise_deployment \
    --week "$WEEK_ID" \
    --scope standard \
    --queries \
      "enterprise AI deployment adoption rate 2026" \
      "LLM enterprise ROI measurement latest" \
    --output "$OUTPUT_DIR/intel_enterprise_deployment.json"
  echo "[OK] 수집 완료: $OUTPUT_DIR/intel_enterprise_deployment.json"
  echo ""

  echo "[STEP 2] EW 탐지"
  python automation/ai_ew_detector.py \
    --input-dir "$OUTPUT_DIR" \
    --week "$WEEK_ID" \
    --output "$OUTPUT_DIR/ew_report.json"
  echo "[OK] EW 탐지 완료"
  echo ""

  # EW 결과 파싱
  EW_TRIGGERED=$(python -c "import json; d=json.load(open('$OUTPUT_DIR/ew_report.json')); print(str(d.get('ew_triggered',False)).lower())" 2>/dev/null || echo "false")
  EW_COUNT=$(python -c "import json; d=json.load(open('$OUTPUT_DIR/ew_report.json')); print(d.get('ew_count',0))" 2>/dev/null || echo "0")
  EW_SIGNALS=$(python -c "import json; d=json.load(open('$OUTPUT_DIR/ew_report.json')); print(','.join(d.get('ew_signals',[])))" 2>/dev/null || echo "")
  EW_SEVERITY=$(python -c "import json; d=json.load(open('$OUTPUT_DIR/ew_report.json')); print(d.get('severity','NONE'))" 2>/dev/null || echo "NONE")

  echo "[INFO] EW 결과: triggered=$EW_TRIGGERED, count=$EW_COUNT, severity=$EW_SEVERITY"
  echo ""

  echo "[STEP 3] KG Delta 생성"
  python automation/kg_delta_generator.py \
    --intel-dir "$OUTPUT_DIR" \
    --current-version "4.25" \
    --next-version "4.26" \
    --week "$WEEK_ID" \
    --run-date "$RUN_DATE" \
    --ew-signals "$EW_SIGNALS" \
    --output "$OUTPUT_DIR/kg_delta_test.json"
  echo "[OK] KG Delta 생성 완료"
  echo ""

  echo "[STEP 4] Notion C-31 업데이트"
  python automation/notion_c31_updater.py \
    --page-id "$NOTION_PAGE_ID" \
    --week "$WEEK_ID" \
    --run-date "$RUN_DATE" \
    --ew-triggered "$EW_TRIGGERED" \
    --ew-count "$EW_COUNT" \
    --ew-signals "$EW_SIGNALS" \
    --ew-severity "$EW_SEVERITY" \
    --kg-version "4.26" \
    --node-count 5 \
    --edge-count 3 \
    --intel-dir "$OUTPUT_DIR"
  echo "[OK] Notion 업데이트 완료"

# ── EW MODE: EW Emergency 시뮬레이션 ────────────────────────
elif [ "$MODE" = "ew" ]; then
  echo "[STEP 1] EW Emergency Intel 수집 (sonar-pro)"
  python automation/ai_intel_collector.py \
    --domain enterprise_deployment \
    --week "$WEEK_ID" \
    --scope deep \
    --queries \
      "enterprise AI deployment major disruption 2026" \
      "LLM adoption rate sudden spike enterprise" \
      "OpenAI Anthropic enterprise contract wave" \
    --output "$OUTPUT_DIR/ew_emergency_intel.json"
  echo "[OK] EW 수집 완료"
  echo ""

  echo "[STEP 2] KG Emergency Delta"
  python automation/kg_delta_generator.py \
    --intel-dir "$OUTPUT_DIR" \
    --current-version "4.25" \
    --next-version "4.26_EW" \
    --week "$WEEK_ID" \
    --run-date "$RUN_DATE" \
    --ew-signals "enterprise_deployment_spike,rag_adoption_surge" \
    --output "$OUTPUT_DIR/kg_ew_delta.json"
  echo "[OK] EW KG Delta 생성 완료"
  echo ""

  echo "[STEP 3] Notion EW Alert"
  python automation/notion_c31_updater.py \
    --page-id "$NOTION_PAGE_ID" \
    --week "$WEEK_ID" \
    --run-date "$RUN_DATE" \
    --ew-triggered true \
    --ew-count 2 \
    --ew-signals "enterprise_deployment_spike,rag_adoption_surge" \
    --ew-severity "HIGH" \
    --kg-version "4.26_EW" \
    --node-count 3 \
    --edge-count 2 \
    --intel-dir "$OUTPUT_DIR"
  echo "[OK] EW Notion Alert 완료"

# ── FULL MODE: 전체 도메인 ───────────────────────────────────
elif [ "$MODE" = "full" ]; then
  DOMAINS=("enterprise_deployment" "model_capabilities" "regulatory_policy" "investment_funding")

  echo "[STEP 1] 전체 도메인 Intel 수집 (${#DOMAINS[@]}개)"
  for DOMAIN in "${DOMAINS[@]}"; do
    echo "  → $DOMAIN 수집 중..."
    python automation/ai_intel_collector.py \
      --domain "$DOMAIN" \
      --week "$WEEK_ID" \
      --scope standard \
      --queries "$DOMAIN AI trends analysis 2026" "$DOMAIN latest developments" \
      --output "$OUTPUT_DIR/intel_${DOMAIN}.json"
    echo "  [OK] $DOMAIN 완료"
    sleep 2  # Rate limit 방지
  done
  echo ""

  echo "[STEP 2] EW 탐지 (전체 도메인)"
  python automation/ai_ew_detector.py \
    --input-dir "$OUTPUT_DIR" \
    --week "$WEEK_ID" \
    --output "$OUTPUT_DIR/ew_report.json"
  echo ""

  EW_TRIGGERED=$(python -c "import json; d=json.load(open('$OUTPUT_DIR/ew_report.json')); print(str(d.get('ew_triggered',False)).lower())" 2>/dev/null || echo "false")
  EW_COUNT=$(python -c "import json; d=json.load(open('$OUTPUT_DIR/ew_report.json')); print(d.get('ew_count',0))" 2>/dev/null || echo "0")
  EW_SIGNALS=$(python -c "import json; d=json.load(open('$OUTPUT_DIR/ew_report.json')); print(','.join(d.get('ew_signals',[])))" 2>/dev/null || echo "")
  EW_SEVERITY=$(python -c "import json; d=json.load(open('$OUTPUT_DIR/ew_report.json')); print(d.get('severity','NONE'))" 2>/dev/null || echo "NONE")

  echo "[STEP 3] KG Delta 생성"
  python automation/kg_delta_generator.py \
    --intel-dir "$OUTPUT_DIR" \
    --current-version "4.25" \
    --next-version "4.26" \
    --week "$WEEK_ID" \
    --run-date "$RUN_DATE" \
    --ew-signals "$EW_SIGNALS" \
    --output "$OUTPUT_DIR/kg_delta_full.json"
  echo ""

  echo "[STEP 4] Notion C-31 업데이트"
  python automation/notion_c31_updater.py \
    --page-id "$NOTION_PAGE_ID" \
    --week "$WEEK_ID" \
    --run-date "$RUN_DATE" \
    --ew-triggered "$EW_TRIGGERED" \
    --ew-count "$EW_COUNT" \
    --ew-signals "$EW_SIGNALS" \
    --ew-severity "$EW_SEVERITY" \
    --kg-version "4.26" \
    --node-count 0 \
    --edge-count 0 \
    --intel-dir "$OUTPUT_DIR"

else
  echo "[ERROR] 알 수 없는 mode: $MODE"
  echo "사용법: bash scripts/test_pipeline_local.sh [quick|full|ew]"
  exit 1
fi

echo ""
echo "======================================"
echo " 테스트 완료!"
echo "======================================"
echo " 결과물: $OUTPUT_DIR/"
echo ""
ls -lh "$OUTPUT_DIR/"
