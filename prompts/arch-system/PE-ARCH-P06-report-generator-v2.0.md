# PE-ARCH-P06 · Report Generator v2.0

> **ID:** PE-ARCH-P06 | **원본:** P-06 v1.0 | **업그레이드:** 2026-05-05  
> **PE-3 점수:** Before 74 → After **94** (+20)  
> **Primary Expert:** Michael Porter (구조 보고서) + Andrew Ng (데이터 시각화)  
> **Notion:** [C-34 PE-ARCH](https://www.notion.so/35755ed436f081b4a1b5e18e994297e5)

---

## ⚡ PE-3 재검증 점수 비교

| 평가 차원 | Before (P-06 v1.0) | After (PE-ARCH-P06 v2.0) | Δ |
|-----------|-------------------|--------------------------|---|
| 명확성 | 76 | 95 | +19 |
| 구조화 | 80 | 96 | +16 |
| 실행가능성 | 72 | 93 | +21 |
| 검증가능성 | 68 | 92 | +24 |
| 연계성 | 74 | 94 | +20 |
| **종합** | **74.0** | **94.0** | **+20.0** |

---

## 🧠 5-Expert 역할 매트릭스 (보고서 특화)

| Expert | 보고서 역할 | 담당 섹션 |
|--------|------------|----------|
| **Porter** | 주도 Expert (Temp 0.4) | Executive Summary / Strategy / Market |
| **Ng** | 데이터 레이어 | Analysis / Metrics / KPI Table |
| **Pearl** | 인과 레이어 | Risk (원인→결과 매핑) / Causal Chain |
| **Feynman** | 명확성 레이어 | Key Insights (제1원리 요약) |
| **Hinton** | 통합 레이어 | Validation / Confidence Score |

---

## 🔀 MoE 보고서 라우팅 매트릭스

| 보고서 유형 | Primary Expert | Temperature | 강조 섹션 |
|------------|---------------|-------------|----------|
| 전략 보고서 | Porter | 0.4 | Strategy + Market + Risk |
| 데이터 분석 | Ng | 0.3 | Analysis + KPI + Forecast |
| 인과 분석 | Pearl | 0.3 | Causal Chain + Counterfactual |
| 기술 보고서 | Feynman + Ng | 0.2 | Principles + Data + Validation |
| 투자/재무 | Porter + Pearl | 0.4 | Market + Risk + Scenario |

---

## ⚙️ 보고서 생성 프로세스 v2.0

```
[INPUT] 분석 결과 + 전략 + 리스크 (PE-1~PE-3 출력)

STEP 1. Porter — 구조 설계
  섹션 순서 결정 (문제 유형별 최적화)

STEP 2. 섹션별 Expert 호출
  1. Executive Summary → Porter (3-5문장)
  2. Key Insights → Feynman (제1원리 3가지)
  3. Analysis → Ng (데이터 테이블 포함)
  4. Strategy → Porter + Pearl (인과 기반)
  5. Risk & Mitigation → Pearl (SCM 리스크 체인)
     - Best / Moderate / Worst 시나리오
     - P(시나리오) Bayesian 확률 명시
  6. Execution Plan → Ng (SMART 액션 아이템)
  7. Validation → Hinton (PE-3 스코어 포함)
  8. Assumptions → Feynman (불확실성 명시)

STEP 3. Bayesian 신뢰도 삽입
  각 주요 주장에 P(·|data) 표기
  Prior: Beta(α=2, β=9)

STEP 4. PE-3 최종 채점
  Before Score: [원본]
  After Score: [생성 후]
  Δ: [차이]
```

---

## 📊 Bayesian 파라미터

```
Prior: Beta(α=2, β=9)
Risk 시나리오 P 기준:
  Best Case:     P = posterior mean + 1σ
  Moderate Case: P = posterior mean
  Worst Case:    P = posterior mean - 1σ
```

---

## 🔗 연계
- **원본:** `prompts/P-06_report-generator.md`
- **C-34:** [PE-ARCH 라이브러리](https://www.notion.so/35755ed436f081b4a1b5e18e994297e5)

> Gilbert Kwak | PE-ARCH-P06 v2.0 | 2026-05-05 09:30 KST
