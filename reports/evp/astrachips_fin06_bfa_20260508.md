# FIN-06-BFA · AstraChips Entry EV 협상 시뮬레이션 v1.0

> **SSOT**: `prompts/PE-FIN/pe_fin_06_pe_investment_v2.0.md` | **PE-3**: 92% ✅  
> **Notion**: [FIN-06-BFA Entry EV 협상 시뮬레이션 v1.0](https://www.notion.so/35a55ed436f081169ddcc0eb0951acbc)  
> **Analyst**: Gilbert Kwak | **기준일**: 2026-05-08  
> **GitHub Sync**: 2026-05-09 13:52 KST

---

## 1. 개요 (딥스 구조)

| 항목 | 내용 |
|---|---|
| 투자금 | USD 65M (Tranche A CB) |
| 쿠폰 | 3.5% p.a. |
| 전환가 기준 | Entry EV 연동 × (1 − 15.3%) |
| 홀딩 기간 | 5년 (2026 → 2031) |
| Fund 목표 IRR | 20%+ |
| Fund 목표 MOIC | 3.0× ∼ 3.5× |
| WACC | 11.0% |

---

## 2. IRR 역산 핵심 결과

### Entry EV × IRR 매트릭스 (전환가 연동)

| Entry EV | 전환가 | 지분율 | P10 IRR | P50 IRR | P90 IRR | Gate |
|---|---|---|---|---|---|---|
| USD 700M | $5.63 | 10.3% | 6.6% | 15.1% | 24.3% | ⚠️ WACC 상회 |
| USD 800M | $6.39 | 9.1% | 6.6% | 12.4% | 21.4% | ⚠️ WACC 상회 |
| USD 850M | $6.77 | 8.6% | 6.6% | 11.2% | 20.1% | ⚠️ WACC 상회 |
| **USD 900M** | **$7.15** | **8.1%** | **6.6%** | **10.1%** | **18.9%** | **❌ BEAR** |
| USD 1,000M | $7.90 | 7.3% | 6.6% | 8.1% | 16.6% | ❌ BEAR |
| USD 1,080M | $8.51 | 6.8% | 6.6% | 6.7% | 15.0% | ❌ BEAR |

### Fund 목표 IRR 20% 달성 역산 (Entry EV 900M 기준)

| Target IRR | 필요 Exit EV | EV CAGR | 실현가능성 |
|---|---|---|---|
| 15% | USD 1,376M | 8.9% | 🟡 P50–P90 |
| 18% | USD 1,586M | 12.0% | 🟡 P50–P90 |
| **20%** | **USD 1,738M** | **14.1%** | **❌ P90 초과** |
| 25% | USD 2,168M | 19.2% | ❌ P90 초과 |

> ⚠️ **PE-3 Bear Gate**: Entry EV 900M + CB 단순 구조로는 P50 기준 Fund 목표 IRR 20% 달성 **불가**

---

## 3. 핵심 진단

- EV 증분 +20% (5년 CAGR 3.7%) → WACC 11% 대비 심각하게 낙음
- 소수 지분 8.1% × 낙은 EV 성장 → MOIC 1.4× 수준
- CB 쿠폰 3.5% 단독으로는 수익 보강 불충분

---

## 4. 구조 개선 5가지 옵션

| 옵션 | 내용 | 협상 현실성 | 우선순위 |
|---|---|---|---|
| Option 1 | Entry EV 인하 900M→551M | ❌ 불가 | 5위 |
| Option 2 | 투자금 증액 130M (A+B) | 🟡 Tranche 분할 | 2위 |
| **Option 3** | **쿠폰 인상 + PIK (3%현금+5%PIK)** | **✅ 협상 가능** | **1위** |
| Option 4 | Ratchet 강화 (Term Sheet 보강) | ✅ 가능 | 3위 |
| Option 5 | MOIC Floor 1.5× Put 조항 추가 | ✅ 즉시 가능 | 3위 |

### 권고안: Option 3 + Option 4 복합 구조

```
투자금:     USD 65M (유지)
쿠폰:       현금 3% + PIK 5% = 8.5% 실효
전환가:     $7.15 (Entry 900M, 15.3% 디스카운트 유지)
Ratchet:    P50 IRR 미달 시 전환가 추가 −10%
MOIC Floor: 1.5× 보장 Put (만기 시 행사 가능)

예상 효과: P50 IRR 10.1% → 14~16% (구조 보완 후)
```

---

## 5. Next Actions

| # | Action | 담당 | 기한 |
|---|---|---|---|
| 🔴 1 | Option 3+4 복합안 → Term Sheet v2.1 법무 반영 | Gilbert | 2026-05-12 |
| 🔴 2 | Entry EV 카운터오퍼 준비 (820M 제시, 850M 수용 상한) | Gilbert | 2026-05-13 |
| 🟠 3 | Tranche B 65M 마일스톤 KPI 설계 (2027 매출 273M+) | IC | 2026-05-15 |
| 🟠 4 | PIK 쿠폰 세금 처리 검토 (원첸징수 이슈) | 세무법인 | 2026-05-20 |
| 🟡 5 | IRR 역산 모델 v2 재실행 (PIK 복리 + Ratchet 통합) | Gilbert | 2026-05-15 |

---

## 6. 연계 시스템

```
astrachips_fin06_bfa_20260508.md
├── EVP 기반:    AstraChips EVP v1.0
├── Term Sheet:  CB Term Sheet v2.0
├── Ratchet:     CB/Ratchet 구조 보완 v1.0
└── SSOT:        PE-FIN/pe_fin_06_pe_investment_v2.0.md
```

---

## 7. 합산 정리 — 1주 세션 Entry EV 협상 시뮬레이션

| 항목 | 결과 |
|---|---|
| 세션 날짜 | 2026-05-08 (1주) → 2026-05-09 (GitHub 동기화) |
| 핵심 발견 | Entry EV 900M 기준 P50 IRR 10.1% — Fund 목표 20% 미달 |
| 권고 구조 | Option 3(PIK 8.5%) + Option 4(Ratchet) 복합 → 예상 P50 14~16% |
| 협상 레인지 | Entry EV 820M 제시 / 850M 수용 상한 |
| 다음 세션 | IRR 모델 v2 (PIK 복리 + Ratchet 통합) + fin06_irr_simulator.py 제작 |
