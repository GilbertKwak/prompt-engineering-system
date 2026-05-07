# E2E TEST CASE 02: SteelCore Manufacturing
# GitHub SSOT: prompts/PE-DD/test_case_02_steelcore_manufacturing.md
# 목적: GREEN Zone 제조업 — Stage×Domain 매트릭스 6개 코드 전체 검증
# 수행일: 2026-05-07 / 버전: v1.0

## ══ 테스트 케이스 요약 ══

| 항목 | 내용 |
|---|---|
| 기업명 | SteelCore Manufacturing (Fictional) |
| Stage | Series B |
| Domain | 제조/에너지 |
| 요청 밸류에이션 | $85M (Post-Money) |
| 유치 목표 | $20M |
| 테스트 목적 | GREEN Zone 판정 시 Stage×Domain 6개 라우팅 코드 정상 동작 확인 |

## ══ IR 핵심 주장 (Phase 0) ══

```
1. SteelCore는 산업용 정밀 부품 제조 전문기업으로
   매출 $28M, EBITDA Margin 22%, 3년 연속 흑자.
2. 주요 고객사 7곳(자동차 OEM 5곳, 항공 2곳) 장기 공급 계약 확보,
   총 계약 잔고(Backlog) $64M.
3. 한국/동남아 생산 거점 이원화로 공급망 리스크 분산,
   CapEx $12M 투자로 CAGR 18% 성장 예측.
```

## ══ OPT-DD 7-Layer 분석 결과 (Phase 1~7) ══

| Layer | 발견 사항 | Risk |
|---|---|---|
| L1 출처 신뢰도 | Big4 감사보고서 완비, 3년 연속 감사의견 적정 | 🟢 |
| L2 숨은 의도 | 경영진 100% 잔류 약정 + 세컨더리 없음 | 🟢 |
| L3 시장 현실성 | 정밀 부품 TAM $42B, 보수적 SAM $3.2B 제시 | 🟢 |
| L4 고객 실재성 | 7개 고객사 실명 공개 + 계약서 제출, Backlog $64M 확인 | 🟢 |
| L5 기술 실현 가능성 | 기존 생산라인 증설, 공정 기술 특허 12건 보유 | 🟢 |
| L6 정책·규제 | 한국 산업안전보건법 적합, 동남아 투자 인허가 완료 | 🟢 |
| L7 내부 논리 | 과거 CAGR 16% → 예측 18% — 현실적 수렴 | 🟢 |

## ══ Risk Scoring Matrix (Phase 3) ══

### v1.2 가중치 스코어링

| 항목 | 점수 | 구분 | 가중치 | 적용 점수 |
|---|---|---|---|---|
| L1 출처 | 1.5 | Standard | ×1.0 | 1.5 |
| L2 의도 | 1.0 | Critical | ×1.5 | 1.5 |
| L3 시장 | 2.0 | Standard | ×1.0 | 2.0 |
| L4 고객 | 1.5 | Critical | ×1.5 | 2.25 |
| L5 기술 | 2.0 | Critical | ×1.5 | 3.0 |
| L6 정책 | 2.0 | Standard | ×1.0 | 2.0 |
| L7 논리 | 2.5 | Standard | ×1.0 | 2.5 |

```
CRITICAL_SUM = (1.0 + 1.5 + 2.0) × 1.5 = 6.75
STANDARD_SUM = (1.5 + 2.0 + 2.0 + 2.5) × 1.0 = 8.0
WEIGHTED_SCORE = (6.75 + 8.0) / 8.5 = 14.75 / 8.5 = 1.74
```

**CRITICAL FLAG 확인:** L2=1.0, L4=1.5, L5=2.0 → 모두 8 미만 → FLAG 미발동

## ══ Trigger Engine 판정 (Phase 4) ══

```
──────────────────────────────────────────────
[TRIGGER ENGINE v1.2 OUTPUT]
Weighted Score:   1.74
Domain:           제조/에너지
GREEN Threshold:  ≤ 3.5
CRITICAL FLAG:    미발동
Risk Zone:        🟢 GREEN
Gate:             PASSED
Action:           FULL_PIPELINE_EXECUTE
MEMO_AUTO:        TRUE
──────────────────────────────────────────────
```

## ══ Stage × Domain 라우팅 매트릭스 6개 코드 검증 ══

### 대상: Domain = 제조/에너지, 각 Stage별 라우팅 코드

| Stage | 라우팅 코드 | 검증 항목 | 판정 |
|---|---|---|---|
| Pre-Seed/Seed | FIN-04+05 | pe_fin_04_manufacturing + pe_fin_05_startup | ✅ 정상 |
| Series A | FIN-04+02 | pe_fin_04_manufacturing + pe_fin_02_advanced_fpa | ✅ 정상 |
| **Series B (본 케이스)** | **FIN-04+02** | pe_fin_04_manufacturing + pe_fin_02_advanced_fpa | ✅ 정상 |
| Series C+ | FIN-04+02 | pe_fin_04_manufacturing + pe_fin_02_advanced_fpa | ✅ 정상 |
| IPO | FIN-04+09 | pe_fin_04_manufacturing + pe_fin_09_quant | ✅ 정상 |
| M&A/LBO | FIN-07+04 | pe_fin_07_lbo + pe_fin_04_manufacturing | ✅ 정상 |

**검증 결과: 6/6 코드 정상 라우팅 확인 ✅**

### 실행 명령어 (GREEN, Series B 제조)
```bash
/pe-fin run PROMPT="pe_fin_04_manufacturing_v2.0" ENTITY="SteelCore" STAGE="Series B" \
  DOMAIN="제조/에너지" DD_GATE="PASSED (Weighted: 1.74)" \
  DD_PACKET="{backlog: $64M, EBITDA_margin: 22%, CAGR_target: 18%}" \
  SCENARIO="base_case" MEMO_AUTO=TRUE

# Secondary: Advanced FPA (항상 추가)
/pe-fin run PROMPT="pe_fin_02_advanced_fpa_v2.0" ENTITY="SteelCore" \
  SCENARIO="sensitivity_capex_12M"
```

## ══ Context Injection Packet (Phase 5) ══

```json
{
  "entity":            "SteelCore Manufacturing",
  "stage":             "Series B",
  "domain":            "제조/에너지",
  "dd_risk_score":     "1.74 (Weighted v1.2)",
  "dd_risk_flags":     [],
  "valuation_claim":   "$85M Post-Money",
  "valuation_gap":     "EV/EBITDA 4.3x — 업계 평균 4~6x 내 적정",
  "backlog":           "$64M (2.3x 연매출)",
  "ebitda_margin":     "22%",
  "runway":            "해당없음 (흑자 기업)",
  "capex_plan":        "$12M (CapEx / 동남아 거점 이원화)",
  "policy_risk":       "없음 (인허가 완료)",
  "scenario_weight":   {"conservative": 0.2, "base": 0.6, "optimistic": 0.2}
}
```

## ══ 검증 결론 ══

```
✅ GREEN Zone 판정 정상 동작 확인
✅ Stage×Domain 라우팅 6/6 코드 검증 완료
✅ MEMO_AUTO=TRUE 트리거 정상
✅ Context Injection Packet 구조 제조업 도메인 적합 확인
⚠️  발견: Series A~C+ 동일 코드(FIN-04+02) → v1.3에서 Stage별 세분화 고려
```

## CHANGELOG
| 버전 | 날짜 | 내용 |
|---|---|---|
| v1.0 | 2026-05-07 | 최초 생성 — GREEN Zone 제조업 E2E 전체 검증 |
