# FIN-SNBS-v4.0-OIL — OIL-Integrated 통합 모델

> **ID**: `FIN-SNBS-v4.0-OIL` | **버전**: v4.0-OIL | **작성일**: 2026-05-08
> **연동**: FIN-SNBS-v4.0 + FIN-MSIA-OIL v1.1
> **목표**: Investment Grade A 91.5/100 (88~90점 예측 대비 **실제 91.5점 달성**)
> **Notion**: 35a55ed436f081439b30cdc037852364

---

## 핵심 연동 파라미터

| 파라미터 | Base (SNBS v4.0) | OIL-Integrated | 전거 |
|---|---|---|---|
| Base_EBITDA_Margin | 32.0% | **40.0%** | 업스트림 38~42% 중간값 |
| Nelson_Index_Premium | N/A | **+2.0%** | 정유 복잡도 프리미엄 |
| EBITDA_Adj (final) | 27.5% | **37.5%** | 실질 적용 마진 |
| Contagion_Index | 0.12 | **0.07** | PETRONAS 파트너십 신용 반영 |
| RA_WACC | 10.72% | **10.67%** | Contagion 하락 효과 |

---

## DCF 결과 비교

| 지표 | Base | OIL-Integrated | Δ |
|---|---|---|---|
| **NPV** | $1,244.8M | **$1,854.1M** | +$609.4M |
| TV(disc.) | $883.2M | **$1,318.3M** | +$435.1M |
| **IRR** | 53.92% | **83.67%** | +29.75pp |
| Margin Score | 60.5/100 | **87.2/100** | +26.7점 |
| **Investment Score** | 76.9 (B) | **91.5 (A)** | **+14.7점** |

### 5-Year DCF Table — OIL-Integrated

| Yr | Revenue($M) | EBITDA($M) | FCF($M) | Disc_FCF($M) |
|---|---|---|---|---|
| 1 | 486.5 | 182.4 | 119.2 | 107.7 |
| 2 | 535.1 | 200.7 | 131.1 | 107.0 |
| 3 | 599.4 | 224.8 | 146.8 | 108.3 |
| 4 | 659.3 | 247.2 | 161.5 | 107.7 |
| 5 | 712.0 | 267.0 | 174.4 | 105.1 |

---

## Sensitivity Matrix — OIL-Integrated

| 충격 | ΔNPV($M) | ΔIRR | Score | Grade |
|---|---|---|---|---|
| Carbon_Price +20% ($54) | -$51.8M | -2.47pp | 90.3 | A ✅ |
| Carbon_Price -20% ($36) | +$51.8M | +2.46pp | 92.7 | A ✅ |
| Collapse_Prob +20% (0.18) | -$50.4M | -1.75pp | 90.6 | A ✅ |
| Policy_Shift +20% (0.24) | -$14.0M | 0.00pp | 90.5 | A ✅ |
| OIL EBITDA Bear -5% (35%) | -$287.6M | -13.90pp | 84.7 | A ✅ |
| Contagion Bear +5% (0.12) | -$49.6M | -1.82pp | 90.0 | A ✅ |

> ⚠️ **핵심 리스크**: OIL EBITDA Margin -5%p가 NPV -$287.6M으로 가장 민감.
> 단, 전 충격 시나리오 모두 Grade A 유지 확인.

---

## FIN-MSIA-OIL v1.1 Step7 Bear 시나리오 연동

| Bear 종류 | NPV 충격 | Grade | 대응 (FIN-02 연동) |
|---|---|---|---|
| 유가 급락 (Brent $50↓) | -$287.6M | A(84.7) | Collar 헤지 자동 트리거 |
| OPEC+ 증산 결정 | -$180~220M | A | WTI선물 매도 후 재검토 |
| 에너지 전환 가속 | -$120~160M | A | ESG 연계 FIN-MSIA-ESG 병렬 |
| CBAM 강화 | -$50~80M | A | 탄소크레딧 새로운 수익려율 포함 |

---

## 통합 프롬프트 (FIN-SNBS-v4.0-OIL)

```xml
<STRATEGIC_NEW_BUSINESS_SYNTHESIS version="4.0-OIL" id="FIN-SNBS-OIL">

  <OilIntegration>
    <EBITDA_Override>
      <!-- FIN-MSIA-OIL v1.1 연동 시 BASE값 재정의 -->
      Upstream_E&P:      38~42% (Base 40%)
      Refinery:          12~18% (Nelson Index 연동)
      Petrochemical:     18~25% (Cracking Spread 연동)
      Trading:           2~5%  (Margin 후 재검토)
      Nelson_Index_Premium: +2% (복잡도 지수 연동)
    </EBITDA_Override>

    <Contagion_Recalibration>
      <!-- PETRONAS 파트너십 신용 반영 -->
      Default: 0.12
      PETRONAS_JV: 0.07
      International_JV: 0.09
      Standalone: 0.12
    </Contagion_Recalibration>

    <OilPriceSensitivity>
      <!-- FIN-MSIA-OIL Step7 Bear 5종 자동 통합 -->
      Brent_Bear: <$50 → EBITDA_Adj -5%p 적용 + FIN-02 연동
      OPEC_Surge: 증산 결정 → Collapse_Prob +0.05
      Energy_Transition: ESG 리스크 → FIN-MSIA-ESG 병렬 실행
      CBAM_Tightening: Carbon_Price +20% 충격 적용
    </OilPriceSensitivity>
  </OilIntegration>

</STRATEGIC_NEW_BUSINESS_SYNTHESIS>
```

---

## 명령어

```bash
# OIL-Integrated 실행
python automation/run_prompt.py \
  --prompt prompts/applied-cases/investment-decision/fin_snbs_v4.0_oil_integrated.md \
  --domain "OIL" --oil-type "Upstream" --price-ref "복합" \
  --ebitda-override 0.40 --nelson-premium 0.02 \
  --contagion-recal 0.07 --depth "Deep"

# Bear 시나리오 (Brent $50 하락)
python automation/run_prompt.py \
  --prompt fin_snbs_v4.0_oil_integrated.md \
  --scenario "OIL_BEAR" --brent-price 50
```

---

## 변경 이력

| 버전 | 날짜 | 주요 변경 |
|---|---|---|
| v4.0-OIL | 2026-05-08 | FIN-MSIA-OIL v1.1 연동 신규. NPV +$609.4M / Score 76.9(B)→91.5(A) |
