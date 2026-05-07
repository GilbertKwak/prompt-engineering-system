# DD-FIN TRIGGER ENGINE v1.0
# GitHub SSOT: prompts/PE-DD/dd_fin_trigger_engine_v1.0.md
# 역할: OPT-DD-FIN Risk Score → PE-FIN 시리즈 자동 라우팅 엔진
# 연계: OPT-DD-FIN LAYER 10 → pe_fin_router_v1.0
# 작성일: 2026-05-07

## ══ OVERVIEW ══
# OPT-DD-FIN이 Risk Scoring Matrix 완료 후
# 종합 리스크 지수(합산/7)에 따라
# PE-FIN 01~10 중 최적 프롬프트를 자동 선택·실행합니다.
# 입력: DD_RESULT (OPT-DD-FIN 실행 출력 전체)
# 출력: PE-FIN 실행 명령어 + Context Injection Packet

## ══ ROUTING MATRIX ══

### GREEN ZONE — Risk Score 1~3 (투자 적합)
```
IF dd_risk_score <= 3.0:

  # 스테이지 × 도메인 라우팅
  IF stage IN [Pre-Seed, Seed]:
    PRIMARY   → pe_fin_05_startup_v2.0
    SECONDARY → pe_fin_01_fpa_v2.0

  IF stage IN [Series A, Series B, Series C+]:
    PRIMARY   → pe_fin_01_fpa_v2.0
    SECONDARY → pe_fin_02_advanced_fpa_v2.0
    TERTIARY  → pe_fin_10_ai_agent_v2.0  # 자동 Investment Memo

  IF stage == IPO:
    PRIMARY   → pe_fin_01_fpa_v2.0
    SECONDARY → pe_fin_02_advanced_fpa_v2.0
    TERTIARY  → pe_fin_09_quant_v2.0

  IF stage IN [M&A, LBO]:
    PRIMARY   → pe_fin_07_lbo_v2.0
    SECONDARY → pe_fin_08_mega_fund_lbo_v2.0
    TERTIARY  → pe_fin_06_pe_investment_v2.0

  # 도메인 특화 오버라이드
  IF domain == SaaS:
    PRIMARY   → pe_fin_03_saas_v2.0
  IF domain IN [반도체, 제조, 장비]:
    PRIMARY   → pe_fin_04_manufacturing_v2.0

  ACTION   = FULL_PIPELINE_EXECUTE
  MEMO_AUTO = TRUE
```

### YELLOW ZONE — Risk Score 4~6 (조건부 검토)
```
IF 3.0 < dd_risk_score <= 6.0:

  PRIMARY   → pe_fin_09_quant_v2.0        # VaR / Stress Test 우선
  SECONDARY → pe_fin_02_advanced_fpa_v2.0  # Sensitivity Analysis

  IF stage IN [Series A~C+, IPO]:
    ADD → pe_fin_01_fpa_v2.0(scenario=bear_case)
    ADD → pe_fin_06_pe_investment_v2.0

  IF stage IN [M&A, LBO]:
    ADD → pe_fin_07_lbo_v2.0(scenario=downside)
    ADD → pe_fin_08_mega_fund_lbo_v2.0

  FLAG   = "조건부 투자 검토 — 추가 실사 항목 명시"
  GATE   = "추가 실사 항목 해소 후 PE-FIN 전체 파이프라인 재실행"
  ACTION  = CONDITIONAL_EXECUTE
  MEMO_AUTO = FALSE
```

### RED ZONE — Risk Score 7~10 (투자 부적합)
```
IF dd_risk_score > 6.0:

  ACTION  = BLOCK + ESCALATE
  BLOCK   → PE-FIN 전체 실행 중단
  TRIGGER → OPT-DCA 심층 원인 분석
  NOTIFY  = "투자 부적합 — 의사결정자 에스콜레이션"
  RECHECK = "Risk Score ≤ 6.0 달성 시 YELLOW ZONE 재진입"
  MEMO_AUTO = FALSE
```

## ══ CONTEXT INJECTION PACKET ══
# OPT-DD-FIN 출력을 PE-FIN에 주입하는 표준 패킷

```json
DD_TO_FIN_PACKET = {
  "entity":            "{{ENTITY}}",
  "stage":             "{{STAGE}}",
  "domain":            "{{DOMAIN}}",
  "dd_risk_score":     "[Risk Score 합산/7]",
  "dd_risk_flags":     ["HIGH RISK 항목 목록"],
  "valuation_claim":   "IR 주장 기업가치",
  "valuation_gap":     "Comps 대비 괴리율",
  "burn_rate":         "월 소진액",
  "runway":            "잔여 개월수",
  "ltv_cac":           "LTV/CAC 비율",
  "hockey_stick_flag": "있음|없음",
  "hidden_intent":     "L2 전략적 의도 요약",
  "policy_risk":       "L6 규제 리스크 요약",
  "pearl_dag":         "Final Inference DAG"
}
```

## ══ STAGE x DOMAIN ROUTING MATRIX ══

| Stage \ Domain | SaaS | 반도체/제조 | AI | 범용 |
|---|---|---|---|---|
| Pre-Seed/Seed | FIN-05+01 | FIN-04+05 | FIN-05+01 | FIN-05+01 |
| Series A~C+ | FIN-03+01 | FIN-04+02 | FIN-01+02 | FIN-01+02 |
| IPO | FIN-03+09 | FIN-04+09 | FIN-02+09 | FIN-01+09 |
| M&A/LBO | FIN-07+06 | FIN-07+04 | FIN-07+06 | FIN-07+08 |

## ══ AUTO-GENERATED EXECUTION COMMAND ══

```bash
# GREEN ZONE 출력 예시
/pe-fin run \
  PROMPT="[stage_router 결과]" \
  ENTITY="{{ENTITY}}" STAGE="{{STAGE}}" DOMAIN="{{DOMAIN}}" \
  DD_GATE="PASSED (Score: {{RISK_SCORE}})" \
  DD_PACKET="{{DD_TO_FIN_PACKET}}" \
  SCENARIO="base_case"

# YELLOW ZONE 출력 예시
/pe-fin run \
  PROMPT="pe_fin_09_quant_v2.0" \
  ENTITY="{{ENTITY}}" STAGE="{{STAGE}}" \
  DD_GATE="CONDITIONAL (Score: {{RISK_SCORE}}, Flags: {{FLAGS}})" \
  DD_PACKET="{{DD_TO_FIN_PACKET}}" \
  SCENARIO="bear_case"

# RED ZONE 출력 예시
/dd-fin escalate \
  ENTITY="{{ENTITY}}" RISK_SCORE="{{RISK_SCORE}}" \
  TRIGGER="OPT-DCA" REASON="{{HIGH_RISK_ITEMS}}"
```

## ══ PE-FIN 전체 라우팅 요약 ══

| PE-FIN 프롬플 | 트리거 조건 | Risk Zone | 우선 |
|---|---|---|---|
| pe_fin_01_fpa | Score≤5, 범용 스테이지 | 🟢🟡 | 1순위 |
| pe_fin_02_advanced | Score≤5, Series B+/Sensitivity | 🟢🟡 | 2순위 |
| pe_fin_03_saas | Score≤5, domain=SaaS | 🟢 | 도메인 특화 |
| pe_fin_04_manufacturing | Score≤5, domain=반도체/제조 | 🟢 | 도메인 특화 |
| pe_fin_05_startup | Score≤5, Pre-Seed/Seed | 🟢 | 스테이지 특화 |
| pe_fin_06_pe_investment | Score≤6, PE/M&A | 🟢🟡 | PE 투자 |
| pe_fin_07_lbo | Score≤5, M&A/LBO | 🟢 | LBO |
| pe_fin_08_mega_lbo | Score≤5, 대형 LBO | 🟢🟡 | Mega LBO |
| pe_fin_09_quant | Score≤6, Stress 필요 | 🟢🟡 | VaR |
| pe_fin_10_ai_agent | Score≤3, 자동 실행 | 🟢 | AI Auto |
| OPT-DCA | Score≥7 | 🔴 | 에스콜레이션 |

## CHANGELOG
| 버전 | 날짜 | 내용 |
|---|---|-|
| v1.0 | 2026-05-07 | 최초 생성 — 3-Zone 라우팅, Stage×Domain 매트릭스, Context Injection Packet 표준화 |
