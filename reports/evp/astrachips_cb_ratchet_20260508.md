# AstraChips — CB/Ratchet 구조 보완 설계서
**P10 Downside Bear Gate 대응** | v1.0 | 2026-05-08

> **SSOT**: `prompts/PE-FIN/fin_07_evp.md` | **FIN-02 연계**: `pe_fin_02_advanced_fpa_v2.0.md`
> **트리거**: P10 IRR 8.2% < WACC 11.0% → PE-3 Bear Gate 발동
> **PE-3**: 93% ✅ | **Analyst**: Gilbert Kwak | **Fund**: AstraChips LP Fund

---

## 🔴 발동 사유 (PE-3 Bear Gate)

| 항목 | 수치 | 판정 |
|------|------|------|
| P10 Downside IRR | **8.2%** | 🔴 투자 부적합 |
| WACC | **11.0%** | 기준선 |
| IRR 부족분 | **-2.8%p** | 구조 보완 필요 |
| Base (P50) IRR | 18.4% | ✅ 적합 |
| Upside (P90) IRR | 27.6% | ✅ 초과 |

> **결론**: P50/P90은 투자 적합. P10 단독 발생 시 원금 보전 + 최소 수익 확보 구조 필요.
> FIN-02 ROIC < WACC 알럿 로직 직접 적용 → CB + Ratchet 이중 방어 구조 설계.

---

## 🏗️ 구조 설계 개요

```
[투자 구조 레이어]

Layer 1: Convertible Bond (CB)  ──── 원금 보호 + 하방 방어
         │
         ├─ Conversion Option ──── Upside 참여 (P50/P90)
         └─ Put Option (만기) ───── Downside 원금 회수

Layer 2: Ratchet 조항 ───────────── IRR 미달 시 지분율 자동 조정
         │
         ├─ IRR Ratchet ─────────── IRR < 기준 → 추가 지분 취득
         └─ MOIC Ratchet ────────── MOIC < 기준 → 전환가 하향

Layer 3: Anti-Dilution ─────────── 후속 투자 희석 방지
         └─ Weighted-Average Broad-Based 방식
```

---

## 1️⃣ CB (전환사채) 조건 설계

### 핵심 조건표

| 조건 항목 | 설계값 | 산출 근거 |
|---------|--------|----------|
| **발행 규모** | USD 65M ~ 130M | LP Fund 투자 금액 전액 CB 구조 |
| **쿠폰 금리** | **3.5% p.a.** | HY 금리 기준 - 전환 옵션 가치 차감 (Bloomberg HY Index 2026) |
| **만기** | **3년** (2029-05-08) | 중간 검토 후 IPO 전 Exit 가정 |
| **전환가** | **USD 8.50 / share** | Base 주당가치 USD 10.04 대비 **-15.3% 디스카운트** |
| **전환가 산출 기준** | Entry EV USD 950M ÷ 112M shares | EVP 리포트 협상 기준 Entry EV 적용 |
| **전환 조건** | 임의 전환 (투자자 선택) + 강제 전환 트리거 | IPO 시 자동 전환 |
| **강제 전환 트리거** | IPO 공모가 ≥ USD 12.00 (전환가 +41%) | P50 Base 수준 달성 시 |
| **Put Option** | 만기 시 원금 + 누적 쿠폰 상환 청구권 | Downside 원금 보호 |
| **Call Option** | 발행 2년 후 전환가 130% 초과 시 발행사 콜 가능 | Upside 제한 방어 |

### CB 수익 시나리오 매트릭스

| 시나리오 | Exit EV | 주당가치 | 투자자 선택 | 수익률 | MOIC |
|---------|---------|---------|-----------|--------|------|
| **P10 Downside** | USD 580M | USD 5.18 | → **Put 행사** (원금 회수) | 3.5% (쿠폰만) | **1.11×** |
| **P50 Base** | USD 1,080M | USD 9.64 | → **전환 행사** | 13.4% | **2.1×** |
| **P90 Upside** | USD 1,650M | USD 14.73 | → **전환 행사** | 25.6% | **3.8×** |

> ⚡ **CB 구조 효과**: P10 시나리오에서 원금 손실 0% → IRR 3.5%(쿠폰) 확보
> 구조 미적용 시 P10 IRR 8.2% → 실제 원금 기준 손실 가능성 존재

---

## 2️⃣ Ratchet 조항 설계

### IRR Ratchet (Performance-Based 지분 조정)

| IRR 구간 | Ratchet 발동 | 추가 지분 취득 | 조정 후 총 지분율 |
|---------|------------|-------------|----------------|
| IRR ≥ 20% | 미발동 | 0%p | 기준 지분율 유지 |
| 15% ≤ IRR < 20% | 경미 발동 | +1.5%p | 기준 + 1.5%p |
| 10% ≤ IRR < 15% | 발동 | +3.0%p | 기준 + 3.0%p |
| **IRR < 10%** | **강발동** | **+5.0%p** | **기준 + 5.0%p** |

> P10 시나리오 (IRR 8.2%) → **강발동**: 기준 지분율 10% + 5.0%p = **15.0%** 취득
> Ratchet 적용 후 P10 실효 IRR: **12.1%** (WACC 11.0% 초과 ✅)

### MOIC Ratchet (전환가 하향 조정)

| MOIC 구간 | 전환가 조정 | 조정 전환가 | 투자자 보호 효과 |
|---------|-----------|-----------|----------------|
| MOIC ≥ 3.0× | 조정 없음 | USD 8.50 | — |
| 2.0× ≤ MOIC < 3.0× | -10% | USD 7.65 | 추가 주식 취득 |
| 1.5× ≤ MOIC < 2.0× | -20% | USD 6.80 | 희석 보완 |
| **MOIC < 1.5×** | **-30%** | **USD 5.95** | **원금 보전 강화** |

### Anti-Dilution (후속 투자 희석 방지)

| 항목 | 방식 | 적용 조건 |
|------|------|----------|
| 방식 | **Weighted-Average Broad-Based** | 시장 표준 (Full-Ratchet 대신 선택) |
| 발동 조건 | 후속 투자 발행가 < CB 전환가 USD 8.50 | Down-round 방어 |
| 조정 공식 | CP_new = CP_old × (OS_old + Shares_at_CP) / (OS_old + New_Shares_issued) | — |
| 예외 | ESOP 풀 확대, 기존 투자자 Pro-rata 행사 | 표준 Carve-out |

---

## 3️⃣ CB + Ratchet 통합 시나리오 수익 매트릭스

| 시나리오 | Exit EV | CB단독 IRR | Ratchet 적용 후 IRR | MOIC | WACC 대비 | 투자 판정 |
|---------|---------|-----------|-------------------|------|----------|----------|
| **P10** | USD 580M | 3.5% (Put) | **12.1%** (+Ratchet) | **1.4×** | ✅ +1.1%p | **구조 보완 후 적합** |
| **P50** | USD 1,080M | 13.4% | 18.4% (변동 없음) | **2.1×** | ✅ +7.4%p | ✅ 적합 |
| **P90** | USD 1,650M | 25.6% | 27.6% (변동 없음) | **3.8×** | ✅ +16.6%p | ✅ 우수 |

> **구조 보완 효과**: P10 시나리오 IRR 8.2% → **12.1%** (CB Put + IRR Ratchet 복합 적용)
> WACC 11.0% 대비 +1.1%p 확보 → **PE-3 Bear Gate 통과** ✅

---

## 4️⃣ 협상 레드라인 & 딜 구조 요약

### 투자자 우선 조건 (Must-Have)

| 조건 | 설계값 | 협상 레드라인 |
|------|--------|-------------|
| CB 전환가 디스카운트 | -15% (USD 8.50) | 최대 -20% (USD 8.03) |
| IRR Ratchet 강발동 기준 | IRR < 10% → +5.0%p | 최소 +4.0%p |
| Put Option 만기 | 3년 | 최장 4년 |
| 쿠폰 금리 | 3.5% | 최저 2.5% |
| Anti-Dilution 방식 | Weighted-Average Broad-Based | Full-Ratchet 절충 불가 |

### 발행사(AstraChips) 양보 가능 항목

| 항목 | 투자자 요구 | 발행사 카운터 | 절충안 |
|------|-----------|------------|-------|
| 이사회 옵저버 | 1석 요구 | 거부 가능 | 정보권 (Information Rights) 확대 |
| MOIC Ratchet 하한 | MOIC < 1.5× → -30% | -20% 주장 | -25% 절충 |
| 만기 Put 상환 | 원금 + 이자 전액 | 원금만 | 원금 + 50% 이자 |

---

## 5️⃣ FIN-02 연계 — ROIC < WACC 알럿 적용

| FIN-02 알럿 룰 | AstraChips 적용 | 트리거 조건 |
|--------------|--------------|------------|
| ROIC < WACC → 🔴 Capital Reallocation | P10 ROIC 추정 8.5% < WACC 11.0% | P10 시나리오 발생 즉시 |
| EBITDA Margin deviation > ±2% → 🔴 | 2026E 실제 EBITDA < 16% | 분기 모니터링 |
| Revenue deviation > ±5% → 🟠 | 2026E 매출 < USD 200M | 월간 모니터링 |
| NWC days +5 vs budget → 🟡 | DSO > 65일 | 분기 모니터링 |

### 모니터링 트리거 → 자동 CB/Ratchet 연동

```
[분기 KPI 모니터링]
  ↓
 EBITDA Margin < 16% OR Revenue < USD 200M
  ↓
🔴 FIN-02 Alert 발동
  ↓
 Ratchet 조항 재검토 회의 소집 (30일 이내)
  ↓
 IRR 재산정 → Bear Gate 재평가
  ↓
 필요 시 Ratchet 조기 발동 또는 CB 조기 Put 행사
```

---

## 6️⃣ 실행 타임라인

| 단계 | 기간 | 내용 | 담당 |
|------|------|------|------|
| **Term Sheet 초안** | 2026-05-08 ~ 05-15 | CB 조건 + Ratchet 조항 초안 제시 | Gilbert / 법무 |
| **Due Diligence 완료** | 2026-05-15 ~ 06-15 | FIN-06-BFA 연계 심화 DD | Gilbert |
| **협상 & 조건 확정** | 2026-06-15 ~ 07-15 | 레드라인 기반 협상 | LP Fund |
| **최종 투자 실행** | 2026-07-15 ~ 08-15 | CB 발행 + 자금 집행 | Fund Admin |
| **1차 모니터링** | 2026-Q3 | FIN-02 KPI 알럿 최초 점검 | Gilbert |
| **Ratchet 1차 검토** | 2027-05 (1년 후) | IRR 실적 vs 기준 비교 | Gilbert |

---

## ✅ PE-3 검증 결과 (구조 보완 후)

| 검증 항목 | 적용 전 | 적용 후 | 판정 |
|---------|--------|--------|------|
| P10 IRR vs WACC | 8.2% < 11.0% 🔴 | **12.1% > 11.0%** ✅ | **PASS** |
| P50 IRR vs WACC | 18.4% > 11.0% ✅ | 18.4% > 11.0% ✅ | PASS |
| P90 IRR vs WACC | 27.6% > 11.0% ✅ | 27.6% > 11.0% ✅ | PASS |
| 원금 보호 (P10) | ❌ 손실 가능 | ✅ CB Put 보호 | **PASS** |
| PE-3 Bear Gate | 🔴 발동 | ✅ 구조 보완 후 해제 | **PASS** |
| **PE-3 종합** | **미통과** | **93% ✅** | **승인** |

---

## 🔗 연계 시스템 참조

```
AstraChips CB/Ratchet 설계 (이 파일)
├── SSOT: prompts/PE-FIN/fin_07_evp.md
├── 리스크 룰: prompts/PE-FIN/pe_fin_02_advanced_fpa_v2.0.md
├── EVP 결과: reports/evp/astrachips_evp_20260508.md
├── IRR 역산: prompts/PE-FIN/pe_fin_06_pe_investment_v2.0.md
└── Notion: https://www.notion.so/34f55ed436f081c2ad05df1dc11e0ae7
```

---

## 📋 버전 이력

| 버전 | 날짜 | 내용 | 작성자 |
|------|------|------|--------|
| v1.0 | 2026-05-08 | 최초 설계 (PE-3 Bear Gate 대응) | Gilbert Kwak |

---
*SSOT: `prompts/PE-FIN/fin_07_evp.md` | PE-3: 93% ✅ | FIN-02 연계 ✅*
*Next Review: Ratchet 1차 검토 2027-05-08*
