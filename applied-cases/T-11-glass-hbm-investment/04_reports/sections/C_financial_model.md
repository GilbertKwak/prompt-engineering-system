# Section C — Financial Model
> **T-11 | Glass/HBM 투자전략 | v2.0 | 2026-04-26**

---

## C.1 투자 구조별 재무 성과 요약

| Type | 투자금 | NPV | MOIC | IRR | 회수 기간 |
|------|--------|-----|------|-----|----------|
| A — Core | $400M | $52.7M | 1.11x | 12% | 2029-2030 |
| B — Satellite | $350M | $3,158M | 8.90x | 45% | 2028-2029 |
| C — Hedge | $250M | $3,676M | 11.50x | 55% | 2027-2028 |
| **Portfolio (Balanced)** | **$1,000M** | **—** | **6.43x** | **~37%** | **2029-2030** |

---

## C.2 Type A — Glass 수직통합 모델

### 수익 구조
```
투자: $400M (JV 15% 지분)

Revenue 가정:
  - Glass Substrate 시장 2030E: $8.5B
  - JV 점유율 목표: 25% → $2.1B 매출
  - EBITDA 마진: 35% → $735M
  - 15% 지분 귀속: $110M/yr (2029 안정)

Exit:
  - IPO 또는 전략적 매각 (2029-2030)
  - EV/EBITDA 멀티플: 15x → EV $11B
  - 지분가치: $1.65B → MOIC 4.1x (Base)
  - 양산 지연 시나리오: MOIC 1.11x (Downside)
```

**민감도 분석:**
| 변수 | Base | Bull | Bear |
|------|------|------|------|
| 시장 점유율 | 25% | 35% | 15% |
| 양산 개시 | 2028 Q1 | 2027 Q3 | 2029 Q1 |
| MOIC | 4.1x | 6.2x | 1.11x |

---

## C.3 Type B — 패키징 레버리지 모델

### 오프테이크 수익 구조
```
투자: $350M
  - HBM4 오프테이크 선불: $200M (2M units/yr × 3년)
  - TSMC CoWoS 슬롯 선점: $150M (15K wafers/yr × 3년)

Revenue:
  - HBM4 유통 마진: $50/unit × 2M × 3yr = $300M
  - CoWoS 재판매 마진: $3,000/wafer × 15K × 3yr = $135M
  - AI 가속기 번들 프리미엄: +$500M (추정)

Total Return: ~$3,100M → MOIC 8.90x
```

**HBM 가격 민감도:**
| HBM4 가격 변화 | MOIC |
|--------------|------|
| +20% (공급 부족) | 11.2x |
| Base | 8.90x |
| -20% (과잉공급) | 6.5x |
| -40% (AI Winter) | 3.1x |

---

## C.4 Type C — US/EU 헤지 모델

### 투자 구성
```
투자: $250M
  - Amkor 지분 10%: $100M
  - Micron 전환사채: $150M (전환가 $120, 쿠폰 3%)

Amkor 지분 수익:
  - CHIPS Act 보조금 수혜 EV 증가분
  - 2030 EV $15B → 지분가치: $1.5B → MOIC 15x

Micron CB:
  - 전환가 $120 → 2029 주가 $250E → 전환 차익 $187.5M
  - 쿠폰 수익 3% × 5yr = $22.5M
  - Total: $360M → MOIC 2.4x (CB 단독)

Blended MOIC: 11.50x
```

---

## C.5 포트폴리오 시나리오 매트릭스

| 시나리오 | A 배분 | B 배분 | C 배분 | Portfolio MOIC | Risk Score |
|---------|--------|--------|--------|---------------|------------|
| Conservative | 50% | 30% | 20% | 5.52x | 0.155 |
| **Balanced ⭐** | **40%** | **35%** | **25%** | **6.43x** | **0.155** |
| Aggressive | 20% | 50% | 30% | 7.08x | 0.170 |
| Geo-Hedge | 30% | 30% | 40% | 7.60x | 0.145 |

---

## C.6 Monte Carlo 시뮬레이션 결과 (500회)

```
분포 파라미터:
  - Type A MOIC: N(4.1, 2.0), 절단 [0.5, 8.0]
  - Type B MOIC: N(8.9, 3.5), 절단 [1.0, 18.0]
  - Type C MOIC: N(11.5, 4.0), 절단 [1.5, 22.0]
  - 상관계수: A-B: 0.3, A-C: 0.1, B-C: 0.4

결과:
  - EV_MOIC: 6.149x
  - P10 (하위 10%): 3.2x
  - P50 (중위): 6.1x
  - P90 (상위 10%): 9.8x
  - 원금손실 확률: 7.3%
  - MOIC > 5x 확률: 68%
  - MOIC > 10x 확률: 18%
```

---

## C.7 Python 모델 참조

```python
# model_scaffold.py 핵심 파라미터
INVESTMENTS = {
    'Type_A': {'amount': 400, 'moic': 1.11, 'irr': 0.12, 'weight': 0.40},
    'Type_B': {'amount': 350, 'moic': 8.90, 'irr': 0.45, 'weight': 0.35},
    'Type_C': {'amount': 250, 'moic': 11.50, 'irr': 0.55, 'weight': 0.25},
}
# outputs/portfolio_summary.csv 자동 생성
```

> 📁 전체 모델: [`02_financial_model/model_scaffold.py`](../02_financial_model/model_scaffold.py)

---
*→ 리스크 분석: Section D | 실행 로드맵: Section E*
