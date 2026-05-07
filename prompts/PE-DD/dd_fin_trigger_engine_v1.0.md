# DD-FIN TRIGGER ENGINE v1.0
# GitHub SSOT: prompts/PE-DD/dd_fin_trigger_engine_v1.0.md
# 역할: OPT-DD-FIN Risk Score → PE-FIN 시리즈 자동 라우팅 엔진
# 연계: OPT-DD-FIN LAYER 10 → PE-FIN 01~10
# 작성일: 2026-05-07

## ══════════════════════════════════════════
## TRIGGER ENGINE 개요
## ══════════════════════════════════════════
#
# OPT-DD-FIN이 Risk Scoring Matrix 완료 후
# 종합 리스크 지수(합산/7) 값에 따라
# PE-FIN 시리즈 중 최적 프롬프트를 자동 선택·실행합니다.
#
# 입력:  DD_RESULT (OPT-DD-FIN 실행 출력)
# 출력:  PE-FIN 실행 명령어 + 컨텍스트 주입 패킷

## ══════════════════════════════════════════
## ROUTING MATRIX (핵심)
## ══════════════════════════════════════════

### [GREEN ZONE] Risk Score 1~3 → 투자 적합
# 조건: 종합 리스크 지수 ≤ 3.0

```
IF dd_risk_score <= 3.0:

  IF stage IN [Pre-Seed, Seed]:
    → pe_fin_05_startup_v2.0
    → pe_fin_01_fpa_v2.0

  IF stage IN [Series A, Series B, Series C+]:
    → pe_fin_01_fpa_v2.0
    → pe_fin_02_advanced_fpa_v2.0
    → pe_fin_10_ai_agent_v2.0

  IF stage IN [IPO]:
    → pe_fin_01_fpa_v2.0
    → pe_fin_02_advanced_fpa_v2.0
    → pe_fin_09_quant_v2.0

  IF stage IN [M&A, LBO]:
    → pe_fin_07_lbo_v2.0
    → pe_fin_08_mega_fund_lbo_v2.0
    → pe_fin_06_pe_investment_v2.0

  IF domain == "SaaS":
    → pe_fin_03_saas_v2.0

  IF domain IN [반도체, 제조, 장비]:
    → pe_fin_04_manufacturing_v2.0

  # 공통 추가 (항상)
  → Investment Memo 자동 초안 생성 [pe_fin_10_ai_agent]
```

### [YELLOW ZONE] Risk Score 4~6 → 조건부 검토
# 조건: 3.0 < 종합 리스크 지수 ≤ 6.0

```
IF 3.0 < dd_risk_score <= 6.0:

  → pe_fin_09_quant_v2.0      # VaR / Stress Test 우선
  → pe_fin_02_advanced_fpa_v2.0  # Sensitivity Analysis

  FLAG: "조건부 투자 검토 — 추가 실사 항목 명시"
  REQUIRED_ITEMS: [L1~L7 중 HIGH-RISK 항목 목록]

  IF stage IN [Series A~C+, IPO]:
    → pe_fin_01_fpa_v2.0(scenario="bear_case")
    → pe_fin_06_pe_investment_v2.0

  IF stage IN [M&A, LBO]:
    → pe_fin_07_lbo_v2.0(scenario="downside")
    → pe_fin_08_mega_fund_lbo_v2.0

  GATE: "추가 실사 항목 해소 후 PE-FIN 전체 파이프라인 재실행"
```

### [RED ZONE] Risk Score 7~10 → 투자 부적합
# 조건: 종합 리스크 지수 > 6.0

```
IF dd_risk_score > 6.0:

  BLOCK: PE-FIN 전체 실행 중단
  FLAG:  "투자 부적합 — PE-FIN 모델링 선행 금지"

  → OPT-DCA 심층 원인 분석 트리거
  CAUSAL_ANALYSIS: [Risk Score ≥7 항목 Pearl DAG 재분석]

  RECHECK_CONDITION: "Risk Score ≤ 6.0 달성 시 YELLOW ZONE 재진입"
  NOTIFY: "실사 결과 투자 부적합 — 의사결정자 에스컬레이션"
```

## ══════════════════════════════════════════
## CONTEXT INJECTION PACKET 표준
## ══════════════════════════════════════════

```json
DD_TO_FIN_PACKET = {
  "entity":            "{{ENTITY}}",
  "stage":             "{{STAGE}}",
  "domain":            "{{DOMAIN}}",
  "dd_risk_score":     "{{RISK_SCORE_합산/7}}",
  "dd_risk_flags":     ["{{HIGH_RISK_ITEMS}}"],
  "valuation_claim":   "{{IR_주장_기업가치}}",
  "valuation_gap":     "{{Comps_대비_괴리율}}",
  "burn_rate":         "{{BURN_RATE}}",
  "runway":            "{{RUNWAY_개월}}",
  "ltv_cac":           "{{LTV_CAC_비율}}",
  "hockey_stick_flag": "{{있음|없음}}",
  "hidden_intent":     "{{L2_전략적_의도_요약}}",
  "policy_risk":       "{{L6_규제_리스크_요약}}",
  "pearl_dag":         "{{FINAL_INFERENCE_Pearl_DAG}}",
  "recommended_fin":   ["{{TRIGGERED_PE_FIN_LIST}}"]
}
```

## ══════════════════════════════════════════
## Stage × Domain 라우팅 매트릭스
## ══════════════════════════════════════════

| Stage \ Domain | SaaS | 반도체/제조 | AI | 범용 |
|---|---|---|---|---|
| Pre-Seed / Seed | FIN-05+01 | FIN-04+05 | FIN-05+01 | FIN-05+01 |
| Series A~C+ | FIN-03+01 | FIN-04+02 | FIN-01+02 | FIN-01+02 |
| IPO | FIN-03+09 | FIN-04+09 | FIN-02+09 | FIN-01+09 |
| M&A / LBO | FIN-07+06 | FIN-07+04 | FIN-07+06 | FIN-07+08 |

## ══════════════════════════════════════════
## PE-FIN 전체 라우팅 매트릭스 요약
## ══════════════════════════════════════════

| PE-FIN 프롬프트 | 트리거 조건 | Risk Zone | 우선순위 |
|---|---|---|---|
| pe_fin_01_fpa_v2.0 | Score≤5, 범용 스테이지 | 🟢🟡 | 1순위 (기본) |
| pe_fin_02_advanced_fpa_v2.0 | Score≤5, Series B+ / Sensitivity | 🟢🟡 | 2순위 |
| pe_fin_03_saas_v2.0 | Score≤5, domain=SaaS | 🟢 | 도메인 특화 |
| pe_fin_04_manufacturing_v2.0 | Score≤5, domain=반도체/제조 | 🟢 | 도메인 특화 |
| pe_fin_05_startup_v2.0 | Score≤5, stage=Pre-Seed/Seed | 🟢 | 스테이지 특화 |
| pe_fin_06_pe_investment_v2.0 | Score≤6, PE/M&A 검토 | 🟢🟡 | PE 투자 특화 |
| pe_fin_07_lbo_v2.0 | Score≤5, stage=M&A/LBO | 🟢 | LBO 기본 |
| pe_fin_08_mega_fund_lbo_v2.0 | Score≤5, 대형 LBO | 🟢🟡 | Mega Fund LBO |
| pe_fin_09_quant_v2.0 | Score≤6, Stress Test 필요 | 🟢🟡 | Quant/VaR |
| pe_fin_10_ai_agent_v2.0 | Score≤3, 자동 실행 | 🟢 | AI Agent 자동화 |
| OPT-DCA | Score≥7 | 🔴 | 원인 분석 에스컬레이션 |

## ══════════════════════════════════════════
## 실행 명령어 생성 템플릿
## ══════════════════════════════════════════

```bash
# GREEN ZONE 예시 출력
/pe-fin run \
  PROMPT="pe_fin_01_fpa_v2.0" \
  ENTITY="{{ENTITY}}" \
  STAGE="{{STAGE}}" \
  DOMAIN="{{DOMAIN}}" \
  DD_PACKET="{{DD_TO_FIN_PACKET}}" \
  SCENARIO="base_case" \
  DD_GATE="PASSED (Score: {{RISK_SCORE}})"

# YELLOW ZONE 예시 출력
/pe-fin run \
  PROMPT="pe_fin_09_quant_v2.0" \
  ENTITY="{{ENTITY}}" \
  DD_PACKET="{{DD_TO_FIN_PACKET}}" \
  SCENARIO="bear_case" \
  DD_GATE="CONDITIONAL (Score: {{RISK_SCORE}}, Flags: {{FLAGS}})"

# RED ZONE 예시 출력
/dd-fin escalate \
  ENTITY="{{ENTITY}}" \
  RISK_SCORE="{{RISK_SCORE}}" \
  TRIGGER="OPT-DCA" \
  REASON="{{HIGH_RISK_ITEMS}}"
```

## CHANGELOG
| 버전 | 날짜 | 변경 내용 |
|---|---|---|
| v1.0 | 2026-05-07 | 최초 생성 — OPT-DD-FIN LAYER 10 실제 연결, PE-FIN 01~10 전체 라우팅 매트릭스 구축, Context Injection Packet 표준화 |
