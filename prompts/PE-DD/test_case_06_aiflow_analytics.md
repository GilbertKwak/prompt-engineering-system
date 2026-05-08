# TC-06: AIFlow Analytics (AFA) — AI SaaS Series C+ 실전 케이스

> **검증 목적**: DD-010-E IRR Gate × FIN-06-BFA 연동 검증 (TC-06)
> **실행일**: 2026-05-08 | **프롬프트**: DD-010-E Ultimate Framework v1.0
> **Industry Module**: AI (자동 선택)

---

## 1. 대상 기업 개요

| 항목 | 내용 |
|------|------|
| 기업명 | AIFlow Analytics (AFA) |
| 도메인 | AI/SaaS (엔터프라이즈 분석) |
| 거래 유형 | Series C+ 투자 |
| 현재 ARR | 180억원 |
| ARR 성장률 | 35%/yr |
| NRR | 108% (AI Module 임계 120% 미달) |
| 주요 이슈 | Down-round 방어용 TAM 과장 |

---

## 2. DD-010-E 7-Layer 분석 결과

| Layer | Score | Weight | 가중점수 | 비고 |
|-------|-------|--------|---------|------|
| L1 출처 신뢰도 | 3 | 1.0 | 3.00 | 3자 감사 없음, 자체 MRR 주장 |
| L2 숨은 의도 | 5 | 1.2 | 6.00 | Down-round 방어용 업사이드 과장 ⚠️ |
| L3 시장 현실 | 4 | 1.0 | 4.00 | TAM $80B 주장, 실제 SAM $4.2B |
| L4 고객 수요 | 3 | 1.5 | 4.50 | NRR 108% (CRITICAL, 기준 120%) |
| L5 기술 가능성 | 3 | 1.5 | 4.50 | Fine-tuning 수준, Moat 약함 |
| L6 정책·규제 | 3 | 1.2 | 3.60 | EU AI Act 준수 비용 미반영 |
| L7 내부 논리 | 4 | 1.0 | 4.00 | CAC 급등에도 GM 75% 주장 |
| **합계** | — | **8.4** | **29.60** | **Risk Score: 3.52** |

### 판정 결과
- **Risk Score**: 3.52
- **Zone**: 🟡 YELLOW-LIGHT (3.1 ~ 4.5)
- **CRITICAL FLAG**: L2=5 ⚠️ (Down-round 의도 — 즉시 차단 아님, 페널티 부과)
- **DD→FIN 라우팅**: FIN-06-BFA + bear_case 시나리오 자동 설정

### DD-010-E AI Module 특화 플래그
- 🔴 **TAM 과장**: 주장 $80B vs 실제 SAM $4.2B → 19x 과장 (CRITICAL 수준)
- 🟡 **NRR < 120%**: 108% → AI SaaS Module 자동 페널티 부과
- 🟡 **Moat 약함**: Fine-tuning 기반, 경쟁사 6개월 내 복제 가능

---

## 3. DD-010-E IRR Gate 산출 (AI Module 특화 페널티 3종)

| 구성 항목 | 조정값 | 근거 |
|---------|--------|------|
| Base Hurdle (AI SaaS C+) | 22.00% | Series C+ AI 기본 |
| Risk Premium | +5.28% | RS 3.52 × 1.5 |
| Down-round 의도 페널티 | +2.50% | L2=5 자동 트리거 |
| NRR < 120% 페널티 | +1.00% | AI Module 내장 로직 |
| TAM 과장 패널티 | +1.50% | L3=4, 19x 과장 |
| **최종 IRR Hurdle** | **32.29%** | **FIN-06-BFA 투입 기준** |

---

## 4. FIN-06-BFA IRR 역산 결과

### 재무 가정
| 항목 | 값 |
|------|----|
| 현재 ARR | 180억원 |
| 성장률 | 35%/yr |
| Y5 ARR | 807.1억원 |
| Exit Multiple | 6.0x ARR |
| Exit EV | 4,843억원 |
| 레버리지 | 35% |
| 보유기간 | 5년 |

### ARR 추정
| 연도 | ARR |
|------|-----|
| Y1 | 243.0억 |
| Y2 | 328.1억 |
| Y3 | 442.9억 |
| Y4 | 597.9억 |
| Y5 | 807.1억 |

### Entry EV 시나리오별 IRR
| Entry EV | ARR Multiple | IRR | 허들 판정 |
|----------|-------------|-----|----------|
| 900억 | 5.0x | 56.1% | ✅ PASS |
| 1,200억 | 6.7x | 46.3% | ✅ PASS |
| 1,600억 | 8.9x | 32.3% | ✅ MAX |
| **1,600억** | **8.9x** | **32.3%** | **✅ MAX (허들 충족 상한)** |
| 2,000억 | 11.1x | 21.8% | ❌ FAIL |
| 2,500억 | 13.9x | 11.2% | ❌ FAIL |

### 협상 전략 (매도측 제시가 vs DD-010-E 기준)
- **매도측 제시**: 2,500억원 (13.9x ARR)
- **DD-010-E 기준 상한**: 1,600억원 (8.9x ARR)
- **할인 협상 근거**: **36% 디스카운트** (TAM 과장 + Down-round 의도 + NRR 미달)
- **목표 협상가**: 1,200~1,350억원 (IRR 40~46% 확보)
- **조건부 투자 조건**: NRR 120% 달성 마일스톤 클로즈업 조항 삽입

---

## 5. Context Injection Packet → FIN-06-BFA

```yaml
dd_risk_score: 3.52
dd_zone: YELLOW-LIGHT
dd_risk_flags:
  - Down-round 의도: L2=5, 업사이드 과장 (bear_case 필수)
  - TAM 과장: $80B → SAM $4.2B (19x), DCF TAM 가정 조정 필요
  - NRR 미달: 108% < 120% (이탈률 상승 리스크)
  - EU AI Act: 준수 비용 CapEx +15% 조정
irr_hurdle: 32.29
max_entry_ev: 1600  # 억원
valuation_gap: 900  # 매도측 2500억 - 기준 1600억
hidden_intent: Down-round 방어 + 경영진 exit 목표
policy_risk: EU AI Act 준수 비용 미계상 → CapEx +15% 시나리오
scenario_weights:
  conservative: 0.40
  base: 0.40
  optimistic: 0.20
bear_case_trigger: true
condition_precedent:
  - NRR ≥ 120% (2026-Q4 기준)
  - 독립 감사 MRR 검증
  - TAM 재산정 (독립 시장조사 기관)
```

---

## 6. 검증 결과 요약

| 검증 항목 | 결과 |
|---------|------|
| DD-010-E AI Module 자동 선택 | ✅ 정상 |
| IRR Gate Risk Premium 연산 | ✅ 3.52 × 1.5 = 5.28% |
| Down-round L2=5 페널티 자동 부과 | ✅ +2.5% |
| NRR < 120% 페널티 자동 부과 | ✅ +1.0% |
| TAM 과장 패널티 자동 부과 | ✅ +1.5% |
| bear_case 시나리오 자동 설정 | ✅ 가중치 0.40 |
| FIN-06-BFA Entry EV 역산 | ✅ 1,600억 |
| Valuation Gap 자동 산출 | ✅ 900억 (36% 할인 근거) |
| Context Injection Packet 생성 | ✅ 완료 |

**TC-06 검증 상태**: ✅ PASSED (YELLOW-LIGHT 조건부)

---

## 메타데이터
- **DD 프롬프트**: DD-010-E Ultimate Framework v1.0
- **FIN 프롬프트**: FIN-06-BFA (Buyout Financial Analysis)
- **검증일**: 2026-05-08
- **다음 단계**: Investment Memo AFA v1.0 생성 → 조건부 투자 심의 제출
