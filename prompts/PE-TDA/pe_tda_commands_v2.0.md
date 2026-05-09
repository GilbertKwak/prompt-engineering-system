# PE-TDA 업데이트 & 활용 명령어 v2.0

> **Domain**: PE-TDA | **Version**: v2.0 | **Updated**: 2026-05-09

---

## 1. 등록 & 업데이트 명령어

```bash
# === 등록 (GitHub) ===
git add prompts/PE-TDA/pe_tda_orch_v2.0.md
git commit -m "feat(PE-TDA): v2.0 — FinTech/Mobility 산업 추가 + DueDiligence 모드 + Notion 19필드 연동"
git push origin main

# === QC 검증 (pe3_tda_validator) ===
python scripts/pe3_tda_validator.py \
  --file prompts/PE-TDA/pe_tda_orch_v2.0.md \
  --target-score 95 \
  --qc-strict

# === v1.0 아카이브 (deprecated 표시, 삭제 보류) ===
git mv prompts/PE-TDA/pe_tda_orch_v1.md prompts/PE-TDA/deprecated/pe_tda_orch_v1.0.md
git commit -m "chore(PE-TDA): 아카이브 v1.0 → deprecated/"
git push origin main

# === Notion 동기화 ===
python automation/notion_sync_pipeline.py \
  --domain PE-TDA \
  --file prompts/PE-TDA/pe_tda_orch_v2.0.md \
  --notion-page 35b55ed4-36f0-81da-9c28-e05827a9ec8b
```

---

## 2. 실행 명령어 (pe7_tda_loop.py)

```bash
# [STEP 1] 반독체 기술 DD 실행 (DueDiligence 깊이)
python automation/pe7_tda_loop.py \
  --tech "HBM4" \
  --company "SK하이닉스" \
  --industry Semiconductor \
  --mode DueDiligence \
  --depth DueDiligence \
  --output Due_Diligence_Report \
  --investment-size 5000 \
  --target-irr 25 \
  --entry-ev 1200 \
  --notion-page-id <PAGE_ID> \
  --qc-strict

# [STEP 2] AI/LLM 에이전트 기술 전략 (Strategic)
python automation/pe7_tda_loop.py \
  --tech "LLM Inference Engine" \
  --company "[Company]" \
  --industry AI \
  --mode TechStrategy \
  --depth Strategic \
  --output Board_Presentation \
  --qc-strict

# [STEP 3] FinTech 투자 심사 (Investment)
python automation/pe7_tda_loop.py \
  --tech "[FinTech Core]" \
  --industry FinTech \
  --mode Investment \
  --depth DueDiligence \
  --target-irr 20 \
  --cross-fin \
  --qc-strict

# [STEP 4] 빠른 Summary (자동산업분류)
python automation/pe7_tda_loop.py \
  --tech "[\uae30\uc220\uba85]" \
  --industry AUTO \
  --mode AUTO \
  --depth Summary \
  --output Executive_Report

# [STEP 5] 전체 PE-TDA 레코드 QC 재검증
python automation/pe7_tda_loop.py --revalidate-all --qc-strict

# [STEP 6] PE-FIN IRR 연동 (FIN-06-BFA)
python automation/pe7_tda_loop.py \
  --tech "[\uae30\uc220\uba85]" \
  --cross-fin \
  --entry-ev 900 \
  --target-irr 20

# [STEP 7] 모빌리티/자동차 DD (v2.0 신규)
python automation/pe7_tda_loop.py \
  --tech "ADAS Level 3" \
  --industry Mobility \
  --mode DueDiligence \
  --depth DueDiligence \
  --output Due_Diligence_Report \
  --qc-strict

# [STEP 8] PE-3 대시보드
python automation/pe7_tda_loop.py --pe3-dashboard
```

---

## 3. 전체 에코시스템 연계 요약

```
PE-TDA v2.0
  ├─ [INPUT] TECH_NAME + INDUSTRY + MODE + DEPTH
  ├─ [DETECT] Auto-Detection Engine (8개 산업 자동분류)
  ├─ [ANALYZE] MECE D1~D5 + Industry Specialization
  ├─ [CROSS] PE-FIN(IRR/BFA) + PE-DD + PE-SEMI + PE-STRAT + PE-PROD
  ├─ [QC] pe3_tda_validator.py (95+ 목표)
  └─ [OUTPUT] Notion 19필드 자동기록 + GitHub 리포트
```
