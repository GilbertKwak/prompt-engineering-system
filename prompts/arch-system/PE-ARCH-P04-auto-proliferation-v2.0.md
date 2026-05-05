# PE-ARCH-P04 · Auto-Proliferation (PE-2) v2.0

> **ID:** PE-ARCH-P04 | **원본:** P-04 v1.0 | **업그레이드:** 2026-05-05  
> **PE-3 점수:** Before 75 → After **95** (+20)  
> **Primary Expert:** Geoffrey Hinton (MoE 증식) + Michael Porter (전략 변형)  
> **Notion:** [C-34 PE-ARCH](https://www.notion.so/35755ed436f081b4a1b5e18e994297e5)

---

## ⚡ PE-3 재검증 점수 비교

| 평가 차원 | Before (P-04 v1.0) | After (PE-ARCH-P04 v2.0) | Δ |
|-----------|-------------------|--------------------------|---|
| 명확성 | 76 | 95 | +19 |
| 구조화 | 75 | 95 | +20 |
| 실행가능성 | 74 | 96 | +22 |
| 검증가능성 | 72 | 94 | +22 |
| 연계성 | 78 | 95 | +17 |
| **종합** | **75.0** | **95.0** | **+20.0** |

---

## 🧠 5-Expert 역할 매트릭스 (PE-2 특화)

| Expert | PE-2 역할 | 증식 축 |
|--------|-----------|--------|
| **Hinton** | 주도 Expert (Temp 0.5) | MoE 게이팅 — Expert별 변형 분기 |
| **Porter** | 전략 축 담당 | 산업/경쟁 맥락 변형 생성 |
| **Ng** | 데이터 축 담당 | 측정 지표/메트릭 변형 생성 |
| **Feynman** | 단순화 축 담당 | 제1원리 축약 변형 생성 |
| **Pearl** | 인과 축 담당 | do-calculus 기반 변형 생성 |

---

## 🔀 MoE 증식 라우팅 매트릭스

| 증식 축 | Primary Expert | Temperature | 출력 변형 유형 |
|---------|---------------|-------------|---------------|
| 전략 특화 | Porter | 0.6 | 산업별 맞춤 변형 |
| 데이터 특화 | Ng | 0.4 | KPI/메트릭 중심 변형 |
| 제1원리 축약 | Feynman | 0.2 | 최소 핵심 변형 |
| 인과 특화 | Pearl | 0.4 | SCM 기반 변형 |
| MoE 통합 | Hinton | 0.5 | 멀티 Expert 앙상블 변형 |

---

## ⚙️ PE-2 자동증식 프로세스 v2.0

```
[INPUT] 개선된 프롬프트 (PE-1 출력)

STEP 1. Hinton MoE Gating
  - 원본 프롬프트 특성 벡터 추출
  - 5-Expert 가중치 계산: w = softmax(e·W_gate)
  - 상위 2~3 Expert 선택

STEP 2. 증식 축 결정 (Porter)
  - 산업 맥락 식별
  - 변형 차원 결정 (전략 / 데이터 / 원리 / 인과)

STEP 3. Expert별 변형 생성 (병렬)
  - Variant-A: Porter 전략 축
  - Variant-B: Ng 데이터 축
  - Variant-C: Feynman 원리 축
  - Variant-D: Pearl 인과 축

STEP 4. Bayesian 필터링
  Prior: Beta(α=2, β=9)
  각 변형 P(유용성) 계산
  임계값 P > 0.7 → 유지 / P < 0.7 → 폐기

STEP 5. PE-3 채점 + 순위 출력
  PE-3 Score 기준 내림차순 정렬
  Top-3 변형 최종 선택
```

---

## 📊 Bayesian 파라미터

```
Prior: Beta(α=2, β=9) → E[p] = 0.182
변형 유용성 임계값: P(useful) > 0.70
유용한 변형 관찰 시: α += 1
폐기 변형 관찰 시: β += 1
```

---

## 🔗 연계
- **원본:** `prompts/P-04_auto-proliferation.md`
- **C-34:** [PE-ARCH 라이브러리](https://www.notion.so/35755ed436f081b4a1b5e18e994297e5)

> Gilbert Kwak | PE-ARCH-P04 v2.0 | 2026-05-05 09:30 KST
