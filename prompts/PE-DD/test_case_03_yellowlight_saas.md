# E2E TEST CASE 03: YELLOW-LIGHT — SaaS 조건부 게이트
# GitHub SSOT: prompts/PE-DD/test_case_03_yellowlight_saas.md
# 목적: YELLOW-LIGHT Zone bear_case 조건부 게이트 동작 검증
# 수행일: 2026-05-07 | 버전: v1.0

## ══ 테스트 케이스 요약 ══

| 항목 | 내용 |
|---|---|
| 기업명 | ClearFlow SaaS (Fictional Test Case) |
| Stage | Series A |
| Domain | SaaS / 소프트웨어 |
| 요청 밸류에이션 | $35M (Post-Money) |
| 유치 목표 | $7M |
| 테스트 목적 | YELLOW-LIGHT Zone bear_case 게이트 + FIN 조건부 라우팅 검증 |

## ══ IR 핵심 주장 ══

```
1. ClearFlow: 중소기업 대상 B2B 재무 자동화 SaaS
   ARR $3.5M, NRR 108%, Churn 2.1%/월
2. 주요 고객 85개사 (기업명 공개 가능), 평균 계약기간 18개월
3. Series A $7M: 영업팀 확충(SDR 8명) + 신기능 개발(AI 자동분류)
```

## ══ OPT-DD 7-Layer 분석 ══

| Layer | 발견 사항 | 리스크 | 점수 | 구분 |
|---|---|---|---|---|
| L1 출처 | 내부 감사(자체), 외부 감사 미완료 — 단 Stripe/Chargebee 로 검증 가능 | 🟡 | 4 | Standard |
| L2 의도 | 세컨더리 없음, 목적 명확 — 단 창업자 급여 1.5x 인상 계획 포함 | 🟡 | 3 | Critical |
| L3 시장 | SMB 재무 자동화 SAM $4.2B — 합리적, 크게 과장 없음 | 🟢 | 2 | Standard |
| L4 고객 | 85개사 고객명 공개, NRR 108% — 단 월 Churn 2.1%는 SaaS 기준 경계치 | 🟡 | 4 | Critical |
| L5 기술 | AI 자동분류는 로드맵 단계 (현재 Rule-based), 기술 과장 없음 | 🟡 | 3 | Critical |
| L6 정책 | 금융 자동화 관련 한국 전자금융거래법 준수 여부 미확인 | 🟡 | 4 | Standard |
| L7 논리 | 영업팀 확충으로 ARR $3.5M → $9M (18개월) 예측 — 근거 있으나 낙관적 | 🟡 | 4 | Standard |

## ══ v1.2 Weighted Score 산출 ══

```
Critical (L2=3, L4=4, L5=3) × 1.5 = 15.0
Standard (L1=4, L3=2, L6=4, L7=4) × 1.0 = 14.0
Weighted = (15.0 + 14.0) / 8.5 = 29.0 / 8.5 = 3.41

Domain Threshold (SaaS/AI): GREEN ≤ 3.0 / YELLOW-LIGHT ≤ 4.5
CRITICAL FLAG 체크: L2=3, L4=4, L5=3 → 모두 기준값(8/9/8) 미만 → FLAG 미발동

→ 🟡 YELLOW-LIGHT ZONE (3.0 < 3.41 ≤ 4.5)
```

## ══ Trigger Engine 판정 + 조건부 게이트 라우팅 ══

```
ZONE:        🟡 YELLOW-LIGHT
GATE:        CONDITIONAL-LIGHT (Weighted: 3.41)
MEMO_AUTO:   FALSE
STAGE:       Series A
DOMAIN:      SaaS

Stage×Domain 매트릭스 → SaaS/Series A → FIN-03 + FIN-01
SECONDARY:   pe_fin_02_advanced_fpa (Sensitivity 필수)
SCENARIO:    bear_case
FLAG_ITEMS:  ["L4: Churn 2.1% 경계치", "L6: 전자금융거래법 준수 미확인", "L7: ARR 예측 낙관적"]
```

## ══ 조건부 게이트 해소 요건 ══

```
투자 진행 조건 (YELLOW-LIGHT 게이트):
□ L4: 월 Churn ≤ 1.5% 목표 경로 제시 또는 연간 Churn 기준 재계산
□ L6: 전자금융거래법 준수 확인서 제출 (법무팀 검토)
□ L7: bear_case ARR 시나리오 ($5M, 18개월) 재무 모델 제출

게이트 해소 시: PE-FIN-03 + PE-FIN-01 전체 파이프라인 자동 재실행
```

## ══ 실행 명령어 ══

```bash
/pe-fin run PROMPT="pe_fin_03_saas_v2.0" \
  ENTITY="ClearFlow SaaS" STAGE="Series A" DOMAIN="SaaS" \
  DD_GATE="CONDITIONAL-LIGHT (Weighted: 3.41, Flags: L4/L6/L7)" \
  DD_PACKET="{arr:3.5M, nrr:108%, churn:2.1%, customers:85}" \
  SCENARIO="bear_case"
```

## ══ 검증 결과 ══

| 검증 항목 | 기대값 | 실제값 | 통과 |
|---|---|---|---|
| Zone 판정 | YELLOW-LIGHT | YELLOW-LIGHT (3.41) | ✅ |
| CRITICAL FLAG | 미발동 | 미발동 | ✅ |
| Stage×Domain 라우팅 | FIN-03+01 | FIN-03+01 | ✅ |
| SCENARIO 강제 | bear_case | bear_case | ✅ |
| MEMO_AUTO | FALSE | FALSE | ✅ |
| 게이트 해소 요건 출력 | 3개 항목 | L4/L6/L7 3개 | ✅ |

## CHANGELOG
| 버전 | 날짜 | 내용 |
|---|---|---|
| v1.0 | 2026-05-07 | 최초 생성 — YELLOW-LIGHT SaaS 조건부 게이트 검증 완료 |
