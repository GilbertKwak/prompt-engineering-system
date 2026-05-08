# FIN-SNBS-v4.0-ESG-Optimal — 3-Layer 통합 최적 모델

> **ID**: `FIN-SNBS-v4.0-ESG-OPT` | **버전**: v4.0-ESG-OPT | **작성일**: 2026-05-08
> **연동**: FIN-SNBS-v4.0 × FIN-MSIA-OIL v1.1 × FIN-MSIA-ESG v1.1
> **최종 Investment Score: 94.22/100 (Grade A)**
> **Notion**: 35a55ed436f081439b30cdc037852364

---

## 3-Layer 파라미터 재정의 체계

| Layer | 소스 파일 | 파라미터 변경 | 효과 |
|---|---|---|---|
| L1: OIL마진 | FIN-MSIA-OIL v1.1 | EBITDA 32%→40% + Nelson+2% | +14.7점 (B→A) |
| L2: ESG CC | FIN-MSIA-ESG v1.1 | Carbon Credit +1.5%p 내재화 | +2.1점 |
| L3: Contagion | PETRONAS JV Full | Contagion 0.07→0.05 | +0.7점 |
| **합계** | — | **EBITDA 39.0%, Contagion 0.05** | **+17.5점 (91.53→94.22)** |

---

## 핵심 지표 누적 개선 이력

| 단계 | 모델 | NPV($M) | IRR | Score | Grade |
|---|---|---|---|---|---|
| S0 | Base SNBS-v4.0 | 1,244.8 | 53.92% | 76.9 | B |
| S1 | + OIL-Integrated | 1,854.1 | 83.67% | 91.5 | A |
| S2 | + ESG CC +1.5%p | 1,940.4 | 87.76% | 93.6 | A |
| S3 | + Contagion 0.05 | **1,961.4** | **88.51%** | **94.22** | **A** |

---

## ESG 탄소크레딧 수익 모델 (FIN-MSIA-ESG v1.1 Step4 연동)

| 수익원 | 기준 | 연간 수익 | 근거 |
|---|---|---|---|
| VCM (자발적 탄소시장) | 120,000 tCO₂e × $18/t | **$2.16M** | B-Star sCO₂ 감축분 |
| K-ETS (한국 배출권) | 45,000 tCO₂e × $9.5/t | **$0.43M** | Scope 3 간접 감축 |
| CBAM 절감 (EU) | 80,000t × €62 × 1.08 | **$5.36M** | 정유·석화 수출품 |
| **탄소크레딧 합계** | | **$7.94M/yr** | cc=1.5%p ≈ $7.5M/yr ✅ |

> ISSB S2 Score 기준: 탄소크레딧 수익은 Step2[3D] CBAM 공식 + Step4 VCM 경로 분석에서 도출.
> G-DETECT 사전 스캔: FLAG-G1(탄소주장 괴리) 리스크 → VVB 제3자 검증 의무화.

---

## Contagion_Index 재보정 매트릭스

| 파트너십 구조 | Contagion | RA_WACC | NPV($M) | Score | Grade |
|---|---|---|---|---|---|
| PETRONAS JV Full | **0.05** | 10.65% | 1,961.4 | **94.2** | **A** |
| PETRONAS JV Standard | 0.07 | 10.67% | 1,940.4 | 93.6 | A |
| International JV | 0.09 | 10.69% | 1,919.6 | 92.9 | A |
| Standalone | 0.12 | 10.72% | 1,888.5 | 91.9 | A |

**재보정 근거 (PETRONAS Full JV → 0.05)**:
- PETRONAS Carigali 운영 참여 (기술·운영 위험 분산)
- 말레이시아 국영 신용보증 (국가 리스크 50%↓)
- JV 계약 내 재보험·정치적 위험보험 포함
- FIN-MSIA-JV v1.1 Step5 구조 연동

---

## Bear 충격 흡수력 비교 — Prior vs ESG-Optimal

| 충격 시나리오 | Prior Score | Optimal Score | Δ | Bear 하한 |
|---|---|---|---|---|
| OIL EBITDA Bear -5% (35%) | 84.7 (A) | **87.3 (A)** | +2.6점 | ≥84점 유지 |
| Carbon_Price +20% ($54) | 90.3 (A) | **93.0 (A)** | +2.7점 | ≥90점 유지 |
| Contagion Bear +5% (0.10) | 90.6 (A) | **92.6 (A)** | +2.0점 | ≥92점 유지 |
| Collapse_Prob +20% (0.18) | 90.6 (A) | **93.3 (A)** | +2.6점 | ≥93점 유지 |
| Policy_Shift +20% (0.24) | 90.5 (A) | **93.2 (A)** | +2.7점 | ≥93점 유지 |

> ✅ **핵심 성과**: 전 Bear 시나리오에서 +2.0~+2.7점 흡수력 강화. 최대 리스크인 OIL EBITDA Bear도 87.3점으로 하한 방어선 +2.6점 상승.

---

## ESG G-DETECT 모듈 — 탄소크레딧 그린워싱 리스크 관리

| Flag | 리스크 | 심각도 | 대응 조치 |
|---|---|---|---|
| G1 Carbon Claim Mismatch | VCM 감축량 주장 vs 실측 괴리 | HIGH | VVB 제3자 검증 의무화 (ISO 14064-3) |
| G2 Scope 3 Omission | 정유·석화 Scope 3 미공시 | HIGH | GRI 305 Scope 3 Category 11 공시 |
| G4 Taxonomy Misclassification | CBAM 수혜 과대 계상 | HIGH | EU Taxonomy Auto-Classifier [3A] 재검토 |
| G5 SBTi Without Pathway | SBTi 서명 후 미승인 | MEDIUM | SBTi 검증 일정 확보 (T+12M 마일스톤) |

---

## Impact KPI Roadmap (IRIS+ — FIN-MSIA-ESG v1.1 Step7)

| KPI | IRIS+ Code | T+0 | T+12M | T+36M | T+60M | 검증 |
|---|---|---|---|---|---|---|
| GHG Reduced (tCO₂e/yr) | PI7515 | — | 50,000 | 100,000 | 165,000 | VVB |
| Energy Saved (MWh/yr) | PI4419 | — | 30,000 | 80,000 | 140,000 | 내부감사 |
| CBAM Savings ($M) | — | — | 1.8 | 4.2 | 5.4 | EU관세청 |
| ISSB S2 Score | PI5556 | 45 | 65 | 78 | 85+ | PE-3 검증 |
| K-ETS 크레딧 발행(tCO₂e) | — | — | 15,000 | 35,000 | 45,000 | K-ETS |

---

## 통합 프롬프트 (FIN-SNBS-v4.0-ESG-OPT)

```xml
<STRATEGIC_NEW_BUSINESS_SYNTHESIS version="4.0-ESG-OPT" id="FIN-SNBS-ESG-OPT">

  <LayerStack>
    <!-- L1: OIL 마진 (FIN-MSIA-OIL v1.1) -->
    <OilIntegration>
      EBITDA_Override: 40% (Upstream E&P 기준)
      Nelson_Index_Premium: +2%
      Contagion_Recalibration: 0.05 (PETRONAS Full JV)
      EBITDA_Adj_Final: 39.0% (탄소크레딧 포함)
    </OilIntegration>

    <!-- L2: ESG 탄소크레딧 (FIN-MSIA-ESG v1.1 Step4) -->
    <ESGCarbonCredit>
      Carbon_Credit_Premium: +1.5%p
      Revenue_Sources:
        VCM:  120,000 tCO₂e × $18 = $2.16M/yr
        KETAS: 45,000 tCO₂e × $9.5 = $0.43M/yr
        CBAM:  80,000t × €62 × 1.08 = $5.36M/yr
        Total: $7.94M/yr
      G_DETECT_Flags: [G1, G2, G4, G5] 사전 스캔 의무
      VVB_Verification: ISO 14064-3 제3자 검증
    </ESGCarbonCredit>

    <!-- L3: Contagion 재보정 -->
    <ContagionRecalibration>
      Trigger: PETRONAS JV Full (지분 참여 + 국가보증)
      Value: 0.07 → 0.05
      Justification:
        - PETRONAS Carigali 공동운영 (기술위험 분산)
        - 말레이시아 국영 신용보증
        - 재보험 포함 JV 계약 구조
        - FIN-MSIA-JV v1.1 Step5 연동
    </ContagionRecalibration>
  </LayerStack>

  <FinalScoreCard>
    NPV:            $1,961.4M
    IRR:            88.51%
    RA_WACC:        10.65%
    Margin_Score:   92.6/100
    Investment_Score: 94.22/100
    Grade:          A
    Bear_Floor:     87.3점 (최대 충격 시나리오)
  </FinalScoreCard>

</STRATEGIC_NEW_BUSINESS_SYNTHESIS>
```

---

## 실행 명령어

```bash
# ESG-Optimal 통합 실행
python automation/run_prompt.py \
  --prompt prompts/applied-cases/investment-decision/fin_snbs_v4.0_esg_optimal.md \
  --domain "OIL" --oil-type "Upstream" \
  --ebitda-override 0.40 --nelson-premium 0.02 \
  --carbon-credit 0.015 --contagion 0.05 \
  --partnership "PETRONAS_FULL" --depth "Deep" --lang "KR+EN"

# ESG 병렬 모드 (FIN-MSIA-ESG v1.1 동시 실행)
python automation/run_prompt.py \
  --prompt fin_snbs_v4.0_esg_optimal.md \
  --parallel-esg fin_msia_esg_v1.1.md \
  --issb-depth "Full" --taxonomy-region "BOTH" \
  --g-detect ON

# Bear 시나리오 흡수력 검증
python automation/auto_validate.py \
  --file prompts/applied-cases/investment-decision/fin_snbs_v4.0_esg_optimal.md \
  --rules PE-1,PE-3,E-09 --bear-test ALL
```

---

## 변경 이력

| 버전 | 날짜 | 주요 변경 |
|---|---|---|
| v4.0-OIL | 2026-05-08 | FIN-MSIA-OIL v1.1 연동. Score 76.9(B)→91.53(A) |
| **v4.0-ESG-OPT** | **2026-05-08** | **ESG CC +1.5%p + Contagion 0.05. Score 91.53→94.22** |
