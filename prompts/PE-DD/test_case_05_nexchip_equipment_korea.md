# TC-05: NexChip Equipment Korea (NEK) — 반도체 M&A 실전 케이스

> **검증 목적**: DD-010-E IRR Gate × FIN-06-BFA 연동 검증 (TC-05)
> **실행일**: 2026-05-08 | **프롬프트**: DD-010-E Ultimate Framework v1.0
> **Industry Module**: SEMI (자동 선택)

---

## 1. 대상 기업 개요

| 항목 | 내용 |
|------|------|
| 기업명 | NexChip Equipment Korea (NEK) |
| 도메인 | 반도체 HBM 공정 장비 |
| 거래 유형 | PE Buyout (M&A) |
| 현재 EBITDA | 85억원 |
| EBITDA 성장률 | 22%/yr (HBM4 CapEx 사이클) |
| 주요 고객 | SK하이닉스 (LOI 존재) |
| 규제 이슈 | EAR §742.4 주의 |

---

## 2. DD-010-E 7-Layer 분석 결과

| Layer | Score | Weight | 가중점수 | 비고 |
|-------|-------|--------|---------|------|
| L1 출처 신뢰도 | 2 | 1.0 | 2.00 | 1차 IR + 감사보고서 일치 |
| L2 숨은 의도 | 3 | 1.2 | 3.60 | 매각 후 경영권 유지 의도 경미 |
| L3 시장 현실 | 2 | 1.0 | 2.00 | HBM4 CapEx 사이클 확인 |
| L4 고객 수요 | 2 | 1.5 | 3.00 | SK하이닉스 LOI 존재 (CRITICAL) |
| L5 기술 가능성 | 3 | 1.5 | 4.50 | TRL-7, 양산 검증 중 (CRITICAL) |
| L6 정책·규제 | 4 | 1.2 | 4.80 | EAR §742.4 주의 필요 |
| L7 내부 논리 | 2 | 1.0 | 2.00 | 재무 수치 일관성 확인 |
| **합계** | — | **8.4** | **21.90** | **Risk Score: 2.61** |

### 판정 결과
- **Risk Score**: 2.61
- **Zone**: 🟢 GREEN (≤ 3.0)
- **CRITICAL FLAG**: 없음 (L4=2, L5=3 모두 임계값 미만)
- **DD→FIN 라우팅**: FIN-06-BFA (M&A LBO) 자동 선택

---

## 3. DD-010-E IRR Gate 산출

| 구성 항목 | 조정값 | 근거 |
|---------|--------|------|
| Base Hurdle (SEMI M&A) | 18.00% | PE Buyout 반도체 장비 기본 |
| Risk Premium | +3.92% | RS 2.61 × 1.5 |
| EAR §742.4 규제 페널티 | +1.50% | L6=4 자동 트리거 |
| SK하이닉스 LOI 보너스 | −1.00% | L4 CRITICAL 통과 인정 |
| **최종 IRR Hurdle** | **22.41%** | **FIN-06-BFA 투입 기준** |

---

## 4. FIN-06-BFA IRR 역산 결과

### 재무 가정
| 항목 | 값 |
|------|----|
| 현재 EBITDA | 85억원 |
| 성장률 | 22%/yr |
| Y5 EBITDA | 229.7억원 |
| Exit Multiple | 8.5x EV/EBITDA |
| Exit EV | 1,953억원 |
| LBO 레버리지 | 55% |
| 보유기간 | 5년 |

### EBITDA 추정
| 연도 | EBITDA |
|------|-------|
| Y1 | 103.7억 |
| Y2 | 126.5억 |
| Y3 | 154.3억 |
| Y4 | 188.3억 |
| Y5 | 229.7억 |

### Entry EV 시나리오별 IRR
| Entry EV | IRR | 허들 판정 |
|----------|-----|----------|
| 600억 | 43.1% | ✅ PASS |
| 800억 | 33.3% | ✅ PASS |
| 1,000억 | 26.4% | ✅ PASS |
| **1,080억** | **22.4%** | **✅ MAX (허들 충족 상한)** |
| 1,200억 | 17.8% | ❌ FAIL |

### 최종 협상 권고
- **협상 상한 Entry EV**: **1,080억원 (12.7x EBITDA)**
- **목표 협상가**: 900~950억원 (IRR 28~30% 확보)
- **BATNA**: 800억 이하 (IRR 33% 이상, 보수적 시나리오 헤지)

---

## 5. Context Injection Packet → FIN-06-BFA

```yaml
dd_risk_score: 2.61
dd_zone: GREEN
dd_risk_flags:
  - EAR §742.4: 규제 리스크 (수출 허가 지연 가능성)
  - TRL-7: 양산 검증 미완 (6개월 내 완료 목표)
irr_hurdle: 22.41
max_entry_ev: 1080  # 억원
valuation_gap: null  # GREEN Zone, 갭 없음
hidden_intent: 매각 후 경영권 유지 협상 예상
policy_risk: EAR §742.4 수출 허가 필요 → CapEx 시나리오 보수적 조정
scenario_weights:
  conservative: 0.30
  base: 0.50
  optimistic: 0.20
```

---

## 6. 검증 결과 요약

| 검증 항목 | 결과 |
|---------|------|
| DD-010-E SEMI Module 자동 선택 | ✅ 정상 |
| IRR Gate Risk Premium 연산 | ✅ 2.61 × 1.5 = 3.92% |
| EAR L6=4 페널티 자동 부과 | ✅ +1.5% |
| LOI 보너스 자동 적용 | ✅ −1.0% |
| FIN-06-BFA Entry EV 역산 | ✅ 1,080억 |
| Context Injection Packet 생성 | ✅ 완료 |

**TC-05 검증 상태**: ✅ PASSED

---

## 메타데이터
- **DD 프롬프트**: DD-010-E Ultimate Framework v1.0
- **FIN 프롬프트**: FIN-06-BFA (PE Buyout Financial Analysis)
- **검증일**: 2026-05-08
- **GitHub 커밋**: feat(PE-DD) TC-05/TC-06 실전 케이스 등록
- **다음 단계**: Investment Memo NEK v1.0 생성 → 실전 투자 심의 제출
