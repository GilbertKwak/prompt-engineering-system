#!/usr/bin/env bash
# test_ai_intel_dry_run.sh — 4개 스크립트 dry-run 검증 스크립트
# Usage: bash automation/test_ai_intel_dry_run.sh [WEEK]

set -euo pipefail

WEEK="${1:-$(python3 -c "from datetime import date; d=date.today(); print(f'{d.year}-W{d.isocalendar()[1]:02d}')" )}"
RUN_DATE="$(date +%Y-%m-%d)"
OUTPUT_DIR="output/ai_intel_test"
PAGE_ID="34a55ed436f0814d9cffe6a2f0816e29"

echo "====================================="
echo " AI Intel Pipeline DRY-RUN 테스트"
echo " 주차: ${WEEK} | 날짜: ${RUN_DATE}"
echo "====================================="

mkdir -p "${OUTPUT_DIR}"

# STEP 1: 인텔 수집 (dry-run — 전체 도메인)
echo ""
echo "[STEP 1] ai_intel_collector.py — 전체 도메인 dry-run"
python3 automation/ai_intel_collector.py \
  --all-domains \
  --week "${WEEK}" \
  --scope standard \
  --parallel \
  --dry-run \
  --output "${OUTPUT_DIR}/"

echo " ✓ 수집 dry-run 완료 (${OUTPUT_DIR}/intel_*.json)"

# STEP 2: EW 탐지
echo ""
echo "[STEP 2] ai_ew_detector.py — EW 탐지"
python3 automation/ai_ew_detector.py \
  --input-dir "${OUTPUT_DIR}" \
  --week "${WEEK}" \
  --output "${OUTPUT_DIR}/ew_report.json"

EW_TRIGGERED=$(python3 -c "
import json, sys
r = json.load(open('${OUTPUT_DIR}/ew_report.json'))
print(str(r.get('global_ew_triggered', False)).lower())
")
EW_SEVERITY=$(python3 -c "
import json
r = json.load(open('${OUTPUT_DIR}/ew_report.json'))
print(r.get('global_severity', 'NONE'))
")
EW_COUNT=$(python3 -c "
import json
r = json.load(open('${OUTPUT_DIR}/ew_report.json'))
print(r.get('total_signal_count', 0))
")
echo " ✓ EW 결과: triggered=${EW_TRIGGERED} severity=${EW_SEVERITY} signals=${EW_COUNT}"

# STEP 3: KG Delta
echo ""
echo "[STEP 3] kg_delta_generator.py — KG Delta 생성"
python3 automation/kg_delta_generator.py \
  --intel-dir "${OUTPUT_DIR}" \
  --current-version "4.25" \
  --next-version "4.26" \
  --week "${WEEK}" \
  --run-date "${RUN_DATE}" \
  --ew-signals "" \
  --ew-report "${OUTPUT_DIR}/ew_report.json" \
  --output "${OUTPUT_DIR}/kg_delta.json"

echo " ✓ KG Delta 완료"

# STEP 4: Notion 업데이터 (dry-run)
echo ""
echo "[STEP 4] notion_c31_updater.py — dry-run"
python3 automation/notion_c31_updater.py \
  --page-id "${PAGE_ID}" \
  --week "${WEEK}" \
  --run-date "${RUN_DATE}" \
  --ew-triggered "${EW_TRIGGERED}" \
  --ew-count "${EW_COUNT}" \
  --ew-signals "" \
  --ew-severity "${EW_SEVERITY}" \
  --kg-version "4.26" \
  --node-count 10 \
  --edge-count 8 \
  --intel-dir "${OUTPUT_DIR}" \
  --dry-run | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'  블록 수: {d[\"count\"]}개')"

echo ""
echo "====================================="
echo " 모든 DRY-RUN 통과 ✅"
echo " 실제 실행 전 확인 사항:"
echo "   1. export PERPLEXITY_API_KEY=pplx-xxxx"
echo "   2. export NOTION_API_KEY=secret_xxxx"
echo "   3. --dry-run 플래그 제거"
echo "====================================="
