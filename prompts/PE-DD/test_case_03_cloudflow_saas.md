# E2E TEST CASE 03: CloudFlow SaaS
# GitHub SSOT: prompts/PE-DD/test_case_03_cloudflow_saas.md
# 목적: YELLOW-LIGHT Zone SaaS — 조건부 게이트 bear_case 동작 검증
# 수행일: 2026-05-07 / 버전: v1.0

## ══ 테스트 케이스 요약 ══

| 항목 | 내용 |
|---|---|
| 기업명 | CloudFlow SaaS (Fictional) |
| Stage | Series A |
| Domain | SaaS |
| 요청 밸류에이션 | $45M (Post-Money) |
| 유치 목표 | $10M |
| 테스트 목적 | YELLOW-LIGHT 판정 시 조건부 게이트 + bear_case 자동 설정 동작 확인 |

## ══ IR 핵심 주장 (Phase 0) ══

```
1. CloudFlow는 중소기업 대상 HR/급여 SaaS로
   ARR $3.2M, NRR 108%, 고객 580개사.
2. ARR 24개월 내 3배(~$9.6M) 목표,
   주요 경쟁사 대비 가격 30% 우위.
3. Series A $10M으로 영업팀 증원 + 동남아 진출 계획.
```

## ══ OPT-DD 7-Layer 분석 결과 (Phase 1~7) ══

| Layer | 발견 사항 | Risk |
|---|---|---|
| L1 출처 신뢰도 | 내부 감사, 외부 회계법인 검토 진행 중 (완료 예정 6주 후) | 🟡 |
| L2 숨은 의도 | 경영진 잔류 의지 명확, 세컨더리 없음 | 🟢 |
| L3 시장 현실성 | 한국 SMB HR SaaS TAM $1.8B — 합리적 추정 | 🟢 |
| L4 고객 실재성 | 580개사 실명 리스트 제출, NRR 108% 확인 | 🟢 |
| L5 기술 실현 가능성 | 자체 개발 코어 엔진, 외부 API 의존도 낮음 | 🟢 |
| L6 정책·규제 | 개인정보보호법 적합, 동남아 현지 법률 검토 미완 | 🟡 |
| L7 내부 논리 | ARR 3배 목표 — 과거 CAGR 89% vs 예측 200%, 2.2x 괴리 | 🟡 |

## ══ Risk Scoring Matrix (Phase 3) ══

### v1.2 가중치 스코어링

| 항목 | 점수 | 구분 | 가중치 | 적용 점수 |
|---|---|---|---|---|
| L1 출처 | 4.0 | Standard | ×1.0 | 4.0 |
| L2 의도 | 1.5 | Critical | ×1.5 | 2.25 |
| L3 시장 | 2.5 | Standard | ×1.0 | 2.5 |
| L4 고객 | 2.0 | Critical | ×1.5 | 3.0 |
| L5 기술 | 2.5 | Critical | ×1.5 | 3.75 |
| L6 정책 | 3.5 | Standard | ×1.0 | 3.5 |
| L7 논리 | 4.5 | Standard | ×1.0 | 4.5 |

```
CRITICAL_SUM = (1.5 + 2.0 + 2.5) × 1.5 = 9.0
STANDARD_SUM = (4.0 + 2.5 + 3.5 + 4.5) × 1.0 = 14.5
WEIGHTED_SCORE = (9.0 + 14.5) / 8.5 = 23.5 / 8.5 = 2.76
```

**CRITICAL FLAG 확인:** L2=1.5, L4=2.0, L5=2.5 → 모두 8 미만 → FLAG 미발동

> ⚠️ 주의: v1.0 단순평균 = (4+1.5+2.5+2+2.5+3.5+4.5)/7 = 20.5/7 = **2.93**
> v1.2 가중치 = **2.76** — Critical 항목 양호로 실제 리스크 하향 보정 정확

## ══ Trigger Engine 판정 (Phase 4) ══

```
──────────────────────────────────────────────
[TRIGGER ENGINE v1.2 OUTPUT]
Weighted Score:        2.76
Domain:                SaaS
GREEN Threshold:       ≤ 3.0
YELLOW-LIGHT Thresh:   ≤ 4.5
CRITICAL FLAG:         미발동
Risk Zone:             🟢 GREEN  ← 주목
Gate:                  PASSED
Action:                FULL_PIPELINE_EXECUTE
MEMO_AUTO:             TRUE
──────────────────────────────────────────────
⚠️  v1.0 단순평균(2.93)과 v1.2 가중치(2.76) 모두 GREEN (≤3.0)
    그러나 v1.0에서 2.93은 GREEN 경계(3.0)에 더 근접
    → L1 감사 미완료(4.0), L7 성장 과대(4.5) 항목 주의 플래그 권고
```

### YELLOW-LIGHT 강제 테스트 — L7을 5.5로 조정 시 재계산

```
# YELLOW-LIGHT 경계 동작 검증용 변형 케이스
L7_logic = 5.5 (성장률 괴리 심화 가정)

STANDARD_SUM_MOD = (4.0 + 2.5 + 3.5 + 5.5) × 1.0 = 15.5
WEIGHTED_SCORE_MOD = (9.0 + 15.5) / 8.5 = 24.5 / 8.5 = 2.88 → 여전히 GREEN

L1=5.0, L7=5.5로 동시 조정 시:
STANDARD_SUM_MOD2 = (5.0 + 2.5 + 3.5 + 5.5) = 16.5
WEIGHTED_SCORE_MOD2 = (9.0 + 16.5) / 8.5 = 25.5 / 8.5 = 3.0 → GREEN 경계

L1=5.5, L7=6.0으로 조정 시:
STANDARD_SUM_MOD3 = (5.5 + 2.5 + 3.5 + 6.0) = 17.5
WEIGHTED_SCORE_MOD3 = (9.0 + 17.5) / 8.5 = 26.5 / 8.5 = 3.12 → ✅ YELLOW-LIGHT 진입
──────────────────────────────────────────────
[YELLOW-LIGHT 검증 OUTPUT (L1=5.5, L7=6.0 조정 시)]
Weighted Score:        3.12
Domain:                SaaS
YELLOW-LIGHT Zone:     3.0 < 3.12 ≤ 4.5   ← ✅ 진입 확인
Risk Zone:             🟡 YELLOW-LIGHT
Gate:                  CONDITIONAL-LIGHT
Action:                STANDARD_CONDITIONAL
Scenario:              bear_case AUTO-SET ← ✅ 자동 설정 확인
PRIMARY_FIN:           pe_fin_03_saas_v2.0 (Series A SaaS)
SECONDARY:             pe_fin_02_advanced_fpa_v2.0
FLAG:                  "L1 감사 미완료(6주 후 완료), L7 성장률 2x 괴리 주의"
──────────────────────────────────────────────
```

### YELLOW-LIGHT 조건부 게이트 동작 확인

```
조건부 게이트 해소 조건:
1. L1: 외부 회계법인 감사보고서 제출 완료
2. L7: Bottom-up ARR 성장 모델 (채널별 분해) 재제출

조건 해소 시:
→ YELLOW-LIGHT → GREEN 재분류
→ MEMO_AUTO=TRUE 자동 전환
→ bear_case → base_case 업데이트
```

### YELLOW-LIGHT 실행 명령어
```bash
/pe-fin run PROMPT="pe_fin_03_saas_v2.0" ENTITY="CloudFlow" STAGE="Series A" \
  DOMAIN="SaaS" DD_GATE="CONDITIONAL-LIGHT (Weighted: 3.12)" \
  DD_PACKET="{NRR: 108%, ARR: $3.2M, backlog: 580 customers}" \
  SCENARIO="bear_case" \
  FLAGS="L1_audit_pending, L7_growth_gap_2x"

# Secondary
/pe-fin run PROMPT="pe_fin_02_advanced_fpa_v2.0" ENTITY="CloudFlow" \
  SCENARIO="bear_case_sensitivity"
```

## ══ 검증 결론 ══

```
✅ YELLOW-LIGHT Zone 진입 임계값(3.0~4.5) 정상 동작 확인
✅ bear_case AUTO-SET 트리거 정상 동작 확인
✅ 조건부 게이트 해소 조건 자동 생성 확인
✅ PRIMARY(FIN-03) + SECONDARY(FIN-02) 라우팅 정상
✅ v1.0 vs v1.2 가중치 차이 — Critical 양호 시 하향 보정 효과 확인
⚠️  추가 발견: GREEN 경계(~3.0) 케이스는 주의 플래그 권고 로직 추가 필요 → v1.3 반영
```

## CHANGELOG
| 버전 | 날짜 | 내용 |
|---|---|---|
| v1.0 | 2026-05-07 | 최초 생성 — YELLOW-LIGHT SaaS E2E 전체 검증 |
