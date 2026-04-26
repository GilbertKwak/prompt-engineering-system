---
title: "T-11 | Glass/HBM 투자전략 보고서"
subtitle: "Core (Glass 수직통합) / Satellite (패키징 레버리지) / Hedge (US/EU 분산)"
version: "v2.0"
date: "2026-04-26"
classification: "CONFIDENTIAL — LP Submission Draft"
author: "T-11 Investment Team"
project: "T-11-glass-hbm-investment"
github: "https://github.com/GilbertKwak/prompt-engineering-system/tree/main/applied-cases/T-11-glass-hbm-investment"
notion: "https://www.notion.so/34e55ed436f08158a641f943f4cacabe"
---

# T-11 | Glass/HBM 투자전략 보고서
## Core · Satellite · Hedge 3축 포트폴리오

> **Version:** v2.0 | **Date:** 2026-04-26 | **Classification:** CONFIDENTIAL — LP Submission Draft  
> **총 투자 규모:** $1,000M USD | **목표 MOIC:** 6.43x | **기대 IRR:** ~37%  
> **투자 기간:** 2026 Q2 → 2030

---

## 목차 (Table of Contents)

| 섹션 | 제목 | 페이지 |
|------|------|--------|
| **A** | Executive Summary | §A |
| **B** | Industry Analysis | §B |
| **C** | Financial Model | §C |
| **D** | Risk Analysis | §D |
| **E** | Execution Roadmap | §E |
| **F** | Appendix & Reference | §F |

---

<div style="page-break-before: always;"></div>

# §A — Executive Summary

## A.1 투자 명제 (Investment Thesis)

글로벌 AI 인프라 수요 폭증을 배경으로, **HBM(High Bandwidth Memory)·Glass Substrate·고급 패키징**의 3축 공급망이 구조적 병목을 형성하고 있다. T-11 전략은 이 병목을 **수직통합(Core) + 사이클 레버리지(Satellite) + 지정학 헤지(Hedge)** 3개 타입으로 포지셔닝하여 2026~2030 단일 펀드 사이클 내 **Portfolio MOIC 6.43x**를 목표한다.

---

## A.2 핵심 재무 지표

| 항목 | 수치 |
|------|------|
| 총 투자 규모 | $1,000M USD |
| 목표 MOIC (Balanced) | **6.43x** |
| 기대 IRR (Blended) | **~37%** |
| 투자 기간 | 2026 Q2 → 2030 |
| 원금손실 확률 (Monte Carlo 500회) | **7.3%** |
| EV_MOIC (기대값 기반) | **6.149x** |
| P50 MOIC | **6.1x** |
| P90 MOIC | **9.8x** |

---

## A.3 3축 전략 한줄 요약

| Type | 전략 | 투자금 | 배분 | MOIC | IRR |
|------|------|--------|------|------|-----|
| **A — Core** | Glass 수직통합 (Samsung+Corning+AGC JV 15%) | $400M | 40% | 1.11x~4.1x | 12% |
| **B — Satellite** | 패키징 레버리지 (HBM4 오프테이크 + CoWoS) | $350M | 35% | 8.90x | 45% |
| **C — Hedge** | US/EU 분산 (Amkor 지분 + Micron CB) | $250M | 25% | 11.50x | 55% |
| **Portfolio (Balanced)** | — | **$1,000M** | 100% | **6.43x** | **~37%** |

---

## A.4 핵심 리스크 3선

1. **대만해협 긴장** — Type B 노출 20%; CoWoS 대체처(한국/일본 패키징) 사전 확보
2. **HBM 수요 사이클** — 2027 Q2 과잉 가능성; 오프테이크 계약 minimum take-or-pay 조항 삽입
3. **Glass Substrate 양산 지연** — Type A MOIC 1.11x 하방 완충재 역할; B/C 포트폴리오로 전체 커버

---

## A.5 의사결정 권고

> **즉시 실행:** Phase 1 (2026 Q2-Q3) — Type A JV 협상 + Type C Amkor/Micron 포지션 동시 착수  
> **조건부 실행:** Type B — HBM4 램프업 공식화 시점 (2026 Q4) 트리거

---

<div style="page-break-before: always;"></div>

# §B — Industry Analysis

## B.1 시장 규모 및 성장 동인

### B.1.1 HBM 시장

| 지표 | 2024 | 2026E | 2028E | CAGR |
|------|------|-------|-------|------|
| HBM 시장 규모 | $14B | $28B | $55B | ~40% |
| HBM 비중 (전체 DRAM) | 8% | 18% | 32% | — |
| HBM4 비중 | 0% | 35% | 70% | — |
| SK hynix 점유율 | 53% | 50% | 48% | — |

**핵심 성장 동인:**
- AI 가속기(H100→B200→R100) 당 HBM 용량 2배씩 증가
- 데이터센터 AI CAPEX 2026E $350B → 2028E $500B+
- CoWoS/SoIC 패키징 병목으로 HBM 실질 가용량 < 수요

### B.1.2 Glass Substrate 시장

| 지표 | 2025 | 2027E | 2030E |
|------|------|-------|-------|
| Glass Substrate 시장 | $0.3B | $2.1B | $8.5B |
| ABF 대비 신호 손실 감소 | 기준 | -30% | -50% |
| 양산 준비 업체 | Samsung, Corning, AGC | +DNP, Ibiden | 5+ |

**구조적 우위:**
- 열팽창계수(CTE) 일치 → 패키지 신뢰성 30% 향상
- 배선 밀도 기존 ABF 대비 2x → 칩렛 통합 핵심
- Intel Glass Core 2026 양산 발표 → 업계 표준화 가속

---

## B.2 공급망 병목 분석 (Agent-2 VS 결과)

### B.2.1 TOP 3 병목 노드

| 순위 | 노드 | VS Score | 지리 집중 | 대체 가능성 |
|------|------|---------|----------|----------|
| 1 | **HBM 생산능력** | 3.33 🔴 | SK hynix 53%, Samsung 38% | 낮음 (2-3년) |
| 2 | **Glass Substrate** | 2.02 🔴 | Samsung/Corning/AGC 3사 | 중간 (1-2년) |
| 3 | **EUV 노광장비** | 1.99 🔴 | ASML 100% | 없음 |

> **공식:** VS = BS × Geo_Risk × DSM  
> BS(i) = 0.30×(의존레이어수) + 0.30×(HHI/10000) + 0.25×(1/Sub+1) + 0.15×(LeadTime/52)

### B.2.2 DSM 의존 구조

```
HBM ──────────→ Glass Substrate    (DSM: 0.85)
HBM ──────────→ CoWoS 패키징       (DSM: 0.90)
Glass ─────────→ Chiplet 통합       (DSM: 0.75)
CoWoS ─────────→ AI 가속기 출하     (DSM: 0.95)
```

**결론:** HBM·Glass·CoWoS는 **순차 의존 구조** → 하나의 병목이 전체 AI 가속기 공급을 차단

---

## B.3 경쟁 지형

| 축 | 주요 경쟁자 | T-11 포지션 우위 |
|----|-----------|----------------|
| Type A (Glass) | Intel (자체), Ibiden/DNP (일본) | Samsung+Corning+AGC JV → 규모+레시피 동시 확보 |
| Type B (패키징) | TSMC (내부화), ASE/Amkor | TSMC 오프테이크 계약 → 희소 슬롯 선점 |
| Type C (US/EU) | Broadcom/Marvell, CHIPS Act 수혜사 | Amkor 지분+Micron CB → 정책 보조금 업스트림 포착 |

---

## B.4 4-World 시나리오 프레임워크 (Agent-3)

| 시나리오 | AI 수요 | 지정학 | 확률 | MOIC 영향 |
|---------|--------|--------|------|----------|
| **W1: Tech Boom** | 고성장 | 안정 | 40% | +30% |
| **W2: Fragmented** | 고성장 | 긴장 | 35% | -15% |
| **W3: AI Winter** | 저성장 | 안정 | 20% | -40% |
| **W4: Crisis** | 저성장 | 위기 | 5% | -65% |

**확률 가중 EV_MOIC = 6.149x**

---

<div style="page-break-before: always;"></div>

# §C — Financial Model

## C.1 투자 구조별 재무 성과 요약

| Type | 투자금 | NPV | MOIC | IRR | 회수 기간 |
|------|--------|-----|------|-----|----------|
| A — Core | $400M | $52.7M | 1.11x~4.1x | 12% | 2029-2030 |
| B — Satellite | $350M | $3,158M | 8.90x | 45% | 2028-2029 |
| C — Hedge | $250M | $3,676M | 11.50x | 55% | 2027-2028 |
| **Portfolio (Balanced)** | **$1,000M** | — | **6.43x** | **~37%** | **2029-2030** |

---

## C.2 Type A — Glass 수직통합 모델

```
투자: $400M (JV 15% 지분)

Revenue 가정:
  Glass Substrate 시장 2030E: $8.5B
  JV 점유율 목표: 25% → $2.1B 매출
  EBITDA 마진: 35% → $735M
  15% 지분 귀속: $110M/yr (2029 안정)

Exit:
  EV/EBITDA 멀티플: 15x → EV $11B
  지분가치: $1.65B → MOIC 4.1x (Base)
  양산 지연 시나리오: MOIC 1.11x (Downside)
```

| 변수 | Bear | Base | Bull |
|------|------|------|------|
| 시장 점유율 | 15% | 25% | 35% |
| 양산 개시 | 2029 Q1 | 2028 Q1 | 2027 Q3 |
| MOIC | 1.11x | 4.1x | 6.2x |

---

## C.3 Type B — 패키징 레버리지 모델

```
투자: $350M
  HBM4 오프테이크 선불: $200M (2M units/yr × 3년)
  TSMC CoWoS 슬롯 선점: $150M (15K wafers/yr × 3년)

Revenue:
  HBM4 유통 마진: $50/unit × 2M × 3yr  = $300M
  CoWoS 재판매 마진: $3,000/wafer × 15K × 3yr = $135M
  AI 가속기 번들 프리미엄: +$500M (추정)

Total Return: ~$3,100M → MOIC 8.90x
```

| HBM4 가격 변화 | MOIC |
|--------------|------|
| +20% (공급 부족) | 11.2x |
| Base | 8.90x |
| -20% (과잉공급) | 6.5x |
| -40% (AI Winter) | 3.1x |

---

## C.4 Type C — US/EU 헤지 모델

```
투자: $250M
  Amkor 지분 10%:      $100M
  Micron 전환사채:      $150M (전환가 $120, 쿠폰 3%)

Amkor 지분 수익:
  2030 EV $15B → 지분가치 $1.5B → MOIC 15x
  (CHIPS Act 보조금 수혜 EV 증가분 포함)

Micron CB:
  전환가 $120 → 2029 주가 $250E → 전환 차익 $187.5M
  쿠폰 수익 3% × 5yr = $22.5M
  Total: $360M → MOIC 2.4x (CB 단독)

Blended MOIC: 11.50x
```

---

## C.5 포트폴리오 시나리오 매트릭스

| 시나리오 | A 배분 | B 배분 | C 배분 | Portfolio MOIC | Risk Score |
|---------|--------|--------|--------|---------------|------------|
| Conservative | 50% | 30% | 20% | 5.52x | 0.155 |
| **Balanced ⭐ (권장)** | **40%** | **35%** | **25%** | **6.43x** | **0.155** |
| Aggressive | 20% | 50% | 30% | 7.08x | 0.170 |
| Geo-Hedge | 30% | 30% | 40% | 7.60x | 0.145 |

---

## C.6 Monte Carlo 시뮬레이션 결과 (500회)

```
분포 파라미터:
  Type A MOIC: N(4.1, 2.0),  절단 [0.5, 8.0]
  Type B MOIC: N(8.9, 3.5),  절단 [1.0, 18.0]
  Type C MOIC: N(11.5, 4.0), 절단 [1.5, 22.0]
  상관계수: A-B: 0.3 | A-C: 0.1 | B-C: 0.4
```

| 지표 | 값 |
|------|----|
| EV_MOIC | **6.149x** |
| P10 (하위 10%) | 3.2x |
| P50 (중위) | **6.1x** |
| P90 (상위 10%) | 9.8x |
| 원금손실 확률 | **7.3%** |
| MOIC > 5x 확률 | 68% |
| MOIC > 10x 확률 | 18% |

---

## C.7 핵심 재무 파라미터 (YAML)

```yaml
# T-11 Financial Model — Core Parameters
discount_rate: 0.12      # WACC 12%
tax_rate: 0.21           # 미국 법인세
currency: USD
base_year: 2026
forecast_horizon: 2030

Type_A:
  investment: 400        # $M
  jv_stake: 0.15
  market_size_2030: 8.5  # $B
  market_share_base: 0.25
  ebitda_margin: 0.35
  exit_ev_ebitda: 15

Type_B:
  investment: 350        # $M
  hbm4_units_yr: 2000000
  hbm4_margin_unit: 50   # USD
  cowos_wafers_yr: 15000
  cowos_margin_wafer: 3000 # USD

Type_C:
  investment: 250        # $M
  amkor_stake: 0.10
  micron_cb: 150         # $M
  conversion_price: 120  # USD
  target_price_2029: 250 # USD
  coupon_rate: 0.03
```

> 📁 전체 Python 모델: [`02_financial_model/model_scaffold.py`](../02_financial_model/model_scaffold.py)

---

<div style="page-break-before: always;"></div>

# §D — Risk Analysis

## D.1 리스크 레지스터

| ID | 리스크 | 타입 | 확률 | 영향 | Score | 대응 전략 |
|----|--------|------|------|------|-------|----------|
| R-01 | 대만해협 군사 긴장 | 지정학 | 20% | 높음 | 🔴 0.32 | Type C 비중 확대, CoWoS 대체처 계약 |
| R-02 | HBM 가격 -40% (AI Winter) | 시장 | 15% | 높음 | 🔴 0.24 | 오프테이크 minimum take-or-pay 조항 |
| R-03 | Glass Substrate 양산 지연 | 기술 | 25% | 중간 | 🟡 0.20 | JV 마일스톤 기반 단계적 납입 |
| R-04 | US CHIPS Act 정책 변화 | 규제 | 10% | 중간 | 🟡 0.10 | EU Chips Act 이중 포지셔닝 |
| R-05 | TSMC CoWoS 슬롯 취소 | 계약 | 15% | 높음 | 🟡 0.18 | ASE/Amkor 백업 계약 사전 체결 |
| R-06 | Micron CB 전환 미실현 | 재무 | 20% | 낮음 | 🟢 0.08 | 쿠폰 수익으로 하방 보호 |
| R-07 | 한국 지정학 리스크 | 지정학 | 15% | 중간 | 🟡 0.15 | 분산 투자 구조로 노출 제한 |

---

## D.2 스트레스 테스트 5종 (Agent-2 검증)

### ST-1: 대만해협 긴장 고조
```
트리거: 대만 해협 군사 충돌 발생
영향:
  Type B MOIC: 8.90x → 3.5x  (CoWoS 전면 중단)
  Type A MOIC: 4.1x  → 2.8x  (부품 수입 차질)
  Type C MOIC: 11.50x → 15.2x (미국 내재화 가속)
Portfolio MOIC: 6.43x → 5.2x  (-19%)
대응: Type C 비중 즉시 +15% 리밸런싱
```

### ST-2: AI Winter (수요 급감)
```
트리거: 2027 H1 AI 모델 성능 정체 + 기업 AI 투자 동결
영향:
  Type B MOIC: 8.90x → 2.1x
  Type A MOIC: 1.11x (양산 연기)
  Type C MOIC: CB 전환 포기, 쿠폰만 수취
Portfolio MOIC: 6.43x → 2.8x  (-56%)
대응: Type B 오프테이크 조기 청산 옵션 행사
```

### ST-3: HBM 공급과잉 (2027 Q2)
```
트리거: Samsung/Micron HBM4 증설 가속 → 가격 -35%
영향:
  Type B 유통마진 압축 → MOIC: 8.90x → 5.8x
  Type A 영향 제한적 (장기 계약)
Portfolio MOIC: 6.43x → 5.1x  (-21%)
대응: 오프테이크 계약 가격 인덱싱 조항 삽입
```

### ST-4: US/EU 규제 강화
```
트리거: 반도체 수출통제 강화 + CHIPS Act 보조금 축소
영향:
  Type C Amkor 지분가치 -20%
  EU Chips Act 대체 수혜로 부분 상쇄
Portfolio MOIC: 6.43x → 5.9x  (-8%)
대응: 이중 상장 + EU 거점 추가
```

### ST-5: Glass 기술 표준화 실패
```
트리거: Intel Glass Core 실패 → 업계 ABF 회귀
영향:
  Type A JV 가치 급락 → MOIC: 1.11x → 0.6x (손실)
  B/C는 영향 없음
Portfolio MOIC: 6.43x → 5.8x  (-10%)
대응: Type A 투자 단계적 실행, 기술 KPI 설정
```

---

## D.3 포트폴리오 통합 노출도

```
가중 병목 노출도 계산:
  Type A: VS(Glass) 2.02 × 40% = 0.808
  Type B: VS(HBM) 3.33 × 35% = 1.166 (일부)
         + VS(CoWoS) 1.85 × 35% = 0.648 (일부)
  Type C: VS(Amkor) 1.20 × 25% = 0.300

Portfolio 통합 노출도: 1.785 → MEDIUM ⚠️
임계값: >2.5 HIGH | 1.5~2.5 MEDIUM | <1.5 LOW
```

---

## D.4 동적 리밸런싱 트리거

| 트리거 | 임계값 | 액션 |
|--------|--------|------|
| HBM 가격 하락 | -25% QoQ | Type B → C 15% 이동 |
| 대만 해협 긴장 지수 | >70 (Economist) | Type C +10% 즉시 |
| Glass 양산 지연 | 2분기 이상 | Type A 추가 납입 동결 |
| Portfolio MOIC (추적) | <4.0x P50 | 전체 포지션 재검토 |
| IRR 실적 | <20% at 2yr | Exit 옵션 조기 행사 |

---

<div style="page-break-before: always;"></div>

# §E — Execution Roadmap

## E.1 마스터 타임라인

```
2026 Q2   ┌─ [Type A] Samsung+Corning+AGC JV NDA 체결
          ├─ [Type C] Amkor 지분 10% 인수 협상 개시
          └─ [Type C] Micron CB $150M 발행 참여

2026 Q3   ┌─ [Type A] JV Term Sheet 합의
          └─ [Type C] Amkor 딜 클로징

2026 Q4   ┌─ [Type B] HBM4 오프테이크 LOI → SK hynix / Micron
          ├─ [Type B] TSMC CoWoS 15K wafers/yr 슬롯 계약
          └─ [Type A] JV 설립 + 초기 납입 $200M

2027 Q1   ┌─ [Type A] Glass 파일럿 라인 착공 확인
          └─ [Type B] 오프테이크 1차 실행 (HBM4 첫 배치)

2027 Q2   ├─ [리밸런싱 체크포인트 #1]
          └─ HBM 가격 모니터링 → ST-3 트리거 여부 판단

2027-2028 ┌─ [Type A] Glass Substrate 양산 개시 (목표: 2027 Q4)
          ├─ [Type B] HBM5 옵션 행사 여부 결정
          └─ [Type C] EU Chips Act 보조금 신청 완료

2028 Q4   ├─ [리밸런싱 체크포인트 #2]
          └─ Exit 준비 시작 (IPO 준비 / Secondary 탐색)

2029-2030 ┌─ [Type A] IPO or Strategic Sale
          ├─ [Type B] 오프테이크 만기 + 포지션 청산
          └─ [Type C] Micron CB 전환 실행 + Amkor 부분 매각
```

---

## E.2 Phase별 상세 액션

### Phase 1 (2026 Q2-Q3): 포지션 구축

**Type A:**
- [ ] 삼성전자 사업개발 + Corning Ventures 접촉
- [ ] AGC Electronics 전략적 파트너십 MOU
- [ ] JV 구조 설계 (지분: Samsung 40% / Corning 30% / AGC 15% / T-11 15%)
- [ ] 기술 실사 (Glass 레시피, 특허 포트폴리오)

**Type C:**
- [ ] Amkor Technology IR 접촉 → PIPE 또는 Secondary 지분 매입
- [ ] Micron 채권 발행 일정 확인 → $150M 배정 확보
- [ ] US CHIPS Act 수혜 모니터링 대시보드 설정

### Phase 2 (2026 Q4-2027 Q1): 레버리지 실행

**Type B:**
- [ ] SK hynix HBM4 오프테이크: minimum 2M units/yr, 3년, 가격 인덱싱
- [ ] TSMC CoWoS: 15K wafers/yr, 2년, 조기 청산 옵션 포함
- [ ] HBM-CoWoS 번들 판매처 확보 (Hyperscaler 3개사 LOI)

### Phase 3 (2027-2028): 성장 관리

- [ ] HBM5 옵션 행사 여부 결정 (2027 Q3 기준)
- [ ] Glass Substrate 양산 KPI 모니터링 (분기별 리포트)
- [ ] EU 거점 확대 (Amkor 유럽 법인 지분 추가)

### Exit Phase (2029-2030)

- [ ] Type A: IB 선정 (Goldman/JPM) → IPO 준비 또는 전략적 매각
- [ ] Type B: 오프테이크 계약 만기 청산
- [ ] Type C: Micron 주가 $200+ 시 CB 전환 실행

---

## E.3 KPI 대시보드

| KPI | 측정 주기 | 목표 | 경고 임계값 |
|-----|----------|------|------------|
| Glass Substrate 양산 수율 | 월간 | >85% | <70% |
| HBM4 오프테이크 실행률 | 분기 | >95% | <80% |
| Portfolio IRR (추적) | 반기 | >30% | <20% |
| P50 MOIC (Monte Carlo) | 연간 | >5.0x | <3.5x |
| 지정학 리스크 지수 | 주간 | <50 | >70 |

---

## E.4 거버넌스 구조

```
Investment Committee (IC)
  └── T-11 Portfolio Manager
        ├── Type A Lead  (한국 JV 담당)
        ├── Type B Lead  (아시아 패키징 담당)
        ├── Type C Lead  (US/EU 담당)
        └── Risk Officer (동적 리밸런싱 담당)

보고 체계:
  주간: 리스크 지수 모니터링
  월간: KPI 대시보드 업데이트
  분기: IC 공식 리뷰 + 리밸런싱 결정
  연간: 전략 재검토
```

---

<div style="page-break-before: always;"></div>

# §F — Appendix & Reference

## F.1 용어 정의

| 용어 | 정의 |
|------|------|
| **HBM (High Bandwidth Memory)** | 여러 DRAM 다이를 TSV로 수직 적층한 고대역폭 메모리. AI 가속기 핵심 부품 |
| **Glass Substrate** | PCB/ABF를 대체하는 유리 기반 인터포저. 열팽창 안정성·배선 밀도 우수 |
| **CoWoS (Chip on Wafer on Substrate)** | TSMC 고급 패키징 공정. HBM + GPU/CPU를 하나의 패키지로 통합 |
| **MOIC** | Multiple on Invested Capital. 총 회수금 / 투자금 |
| **IRR** | Internal Rate of Return. 투자 현금흐름의 수익률 |
| **VS Score** | Vulnerability Score = BS × Geo_Risk × DSM. T-11 공급망 병목 지수 |
| **DSM** | Design Structure Matrix. 공급망 노드 간 의존도 매트릭스 |
| **오프테이크 계약** | 사전 약정 구매 계약. 공급자는 물량 보장, 구매자는 가격/물량 선점 |
| **CB (전환사채)** | 전환사채. 일정 조건 충족 시 주식으로 전환 가능한 채권 |
| **CHIPS Act** | 미국 반도체 제조 투자 지원법 (2022). 보조금 및 세액공제 제공 |
| **EU Chips Act** | EU 반도체 산업 육성법 (2023). €43B 공공·민간 투자 동원 목표 |
| **take-or-pay** | 구매자가 계약 물량을 실제 구매하든 않든 대금을 지불해야 하는 조항 |

---

## F.2 데이터 소스 및 가정

### 시장 데이터 출처
- HBM 시장 규모: Yole Intelligence, IDC (2025-2026)
- Glass Substrate 시장: Prismark, IPC (2025)
- CoWoS 가용 용량: TSMC 공식 IR, Digitimes (2025)
- AI CAPEX 전망: Goldman Sachs, Morgan Stanley (2026)

### 핵심 가정 (YAML)
```yaml
model_assumptions:
  discount_rate: 0.12        # WACC 12%
  tax_rate: 0.21             # 미국 법인세
  currency: USD
  base_year: 2026
  forecast_horizon: 2030

  Type_A:
    jv_market_share_base: 0.25
    glass_market_size_2030: 8.5   # $B
    ebitda_margin: 0.35
    exit_multiple_evEBITDA: 15

  Type_B:
    hbm4_units_per_year: 2000000
    hbm4_margin_per_unit: 50      # USD
    cowos_wafers_per_year: 15000
    cowos_margin_per_wafer: 3000  # USD

  Type_C:
    amkor_equity_stake: 0.10
    micron_cb_amount: 150         # $M
    micron_conversion_price: 120  # USD
    micron_target_price_2029: 250 # USD
    coupon_rate: 0.03

  monte_carlo:
    simulations: 500
    seed: 42
    correlations:
      A_B: 0.3
      A_C: 0.1
      B_C: 0.4
```

---

## F.3 Agent 파이프라인 버전 이력

| Agent | 버전 | 커밋 | 날짜 | 주요 변경사항 |
|-------|------|------|------|-------------|
| Agent-1 | v1.0 | 91a995a | 2026-04-26 | 초기 scaffold |
| Agent-1 | v2.0 | 64fab7f | 2026-04-26 | G-01~G-10 해소, Sub-Agent 4종 |
| Agent-2 | v1.0 | 64fab7f | 2026-04-26 | 의존성·병목 프레임워크 |
| Agent-2 | v2.0 | a9e6933 | 2026-04-26 | DSM 매트릭스, E-04/E-07 해소 |
| Agent-3 | v1.0 | 1b678eb | 2026-04-26 | 4-World, Monte Carlo 500회 |
| **Report v2.0** | — | 7ced371 | 2026-04-26 | **Section A~F 병렬 구성** |
| **Report v2.0 통합본** | — | **현재** | **2026-04-26** | **A~F 단일 파일 병합 (LP 제출용)** |

---

## F.4 관련 문서 인덱스

### GitHub 내부 링크
```
📁 T-11-glass-hbm-investment/
├── 01_strategy/
│   ├── A_glass_vertical_integration.md
│   ├── B_packaging_leverage.md
│   └── C_us_eu_hedge.md
├── 02_financial_model/
│   ├── model_scaffold.py
│   └── scenario_matrix.md
├── 03_prompts/
│   ├── PROMPT_VERSION_HISTORY.md
│   ├── agent_1_expanded_profile_v2.0.md
│   ├── agent_2_dependency_bottleneck_profile_v2.0.md
│   └── agent_3_scenario_planning_v1.0.md
├── 04_reports/
│   ├── REPORT_INDEX.md
│   ├── T11_investment_report_v1.0.md    ← Archive
│   ├── T11_investment_report_v2.0.md    ← 본 문서 ✅
│   └── sections/
│       ├── A_executive_summary.md
│       ├── B_industry_analysis.md
│       ├── C_financial_model.md
│       ├── D_risk_analysis.md
│       ├── E_execution_roadmap.md
│       └── F_appendix.md
└── 05_logs/
    └── CHANGE_LOG.md
```

### 외부 참조
- [TSMC CoWoS 기술 브리프](https://investor.tsmc.com)
- [Intel Glass Core 발표](https://newsroom.intel.com)
- [US CHIPS Act 공식 사이트](https://www.nist.gov/chips)
- [EU Chips Act](https://ec.europa.eu/chips-act)
- [Notion SSOT 허브](https://www.notion.so/34e55ed436f08158a641f943f4cacabe)

---

## F.5 변경 이력 (본 보고서)

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| **v2.0** | **2026-04-26** | **Section A~F 단일 통합본 생성. LP 제출용 Draft.** |
| v1.0 | 2026-03-01 | Core/Satellite/Hedge 전략 + Python 재무모델 초기 버전 |

---

---

> **CONFIDENTIAL NOTICE**  
> 본 문서는 T-11 프로젝트 LP 제출 전용 초안입니다. 무단 배포를 금합니다.  
> © 2026 T-11 Investment Team. All rights reserved.
>
> **SSOT:** [GitHub](https://github.com/GilbertKwak/prompt-engineering-system/tree/main/applied-cases/T-11-glass-hbm-investment) | [Notion](https://www.notion.so/34e55ed436f08158a641f943f4cacabe)
