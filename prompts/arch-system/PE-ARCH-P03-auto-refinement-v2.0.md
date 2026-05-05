# PE-ARCH-P03 · Auto-Refinement (PE-1) v2.0

> **ID:** PE-ARCH-P03 | **원본:** P-03 v1.0 | **업그레이드:** 2026-05-05  
> **PE-3 점수:** Before 78 → After **96** (+18)  
> **Primary Expert:** Richard Feynman (제1원리) + Andrew Ng (데이터 레이어)  
> **Notion:** [C-34 PE-ARCH](https://www.notion.so/35755ed436f081b4a1b5e18e994297e5)

---

## ⚡ PE-3 재검증 점수 비교

| 평가 차원 | Before (P-03 v1.0) | After (PE-ARCH-P03 v2.0) | Δ |
|-----------|-------------------|--------------------------|---|
| 명확성 | 80 | 96 | +16 |
| 구조화 | 78 | 97 | +19 |
| 실행가능성 | 76 | 96 | +20 |
| 검증가능성 | 74 | 95 | +21 |
| 연계성 | 82 | 96 | +14 |
| **종합** | **78.0** | **96.0** | **+18.0** |

---

## 🧠 5-Expert 역할 매트릭스 (PE-1 특화)

| Expert | PE-1 역할 | 구체적 기여 |
|--------|-----------|------------|
| **Feynman** | 주도 Expert (Temp 0.2) | 프롬프트를 최소 구성요소로 분해 → 근본 이유 질문 |
| **Ng** | 보조 Expert | 데이터 중심 개선 — 측정 가능한 지표로 재서술 |
| **Porter** | 검토자 | 목표의 전략적 가치 검증 |
| **Hinton** | 라우터 | 복잡도 판단 → 단순/복합 분기 |
| **Pearl** | 감시자 | 인과 vs 상관 오류 탐지 |

---

## 🔀 MoE 라우팅 매트릭스 (PE-1 내부)

| 개선 유형 | Primary | Temperature | 전략 |
|-----------|---------|-------------|------|
| 목표 불명확 | Feynman | 0.2 | "이것이 왜 필요한가?" 재귀 분해 |
| 측정 지표 부재 | Ng | 0.3 | SMART 지표 삽입 |
| 전략 방향 부재 | Porter | 0.4 | 5-Forces 프레임 매핑 |
| 인과 오류 | Pearl | 0.3 | do-calculus 재서술 |
| 복잡도 과다 | Hinton | 0.2 | MoE 분해 (서브태스크 분리) |

---

## ⚙️ PE-1 자동개선 프로세스 v2.0

```
[INPUT] 사용자 프롬프트

STEP 1. Feynman 분해
  - "이 프롬프트의 근본 목적은 무엇인가?"
  - 최소 구성요소로 분해
  - 불필요한 추상화 제거

STEP 2. Ng 재서술
  - Goal: [측정 가능한 목표]
  - Scope: [명확한 범위]
  - Output Format: [구체적 형식]
  - Success Criteria: [정량 기준]

STEP 3. Porter 전략 검증
  - 전략적 가치 확인
  - 경쟁 맥락 반영

STEP 4. Pearl 인과 점검
  - 상관관계 → 인과관계 변환
  - 반사실 추론: "만약 X가 없었다면?"

STEP 5. Hinton MoE 통합
  - 복잡도 평가
  - Expert 가중치 조정
  - 최종 통합 프롬프트 생성

STEP 6. Bayesian 신뢰도
  Prior: Beta(α=2, β=9)
  개선 성공 시: α += 1
  출력: P(개선 성공) = [값]

STEP 7. PE-3 채점 출력
  Before Score: [X]
  After Score: [Y]
  Δ: [+Z]
```

---

## 📊 Bayesian 파라미터

```
Prior: Beta(α=2, β=9)
  → E[p] = 2/(2+9) = 0.182
  → 초기 개선 성공률 보수적 설정

개선 반복 후 Posterior:
  ITER-1: Beta(3, 9)  → E[p] = 0.250
  ITER-2: Beta(4, 9)  → E[p] = 0.308
  ITER-3: Beta(5, 9)  → E[p] = 0.357
  수렴 기준: E[p] > 0.85 or ITER ≥ 5
```

---

## 🔗 연계
- **원본:** `prompts/P-03_auto-refinement.md`
- **PE Hub:** [프롬프트 엔지니어링 시스템 허브 v2.0](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b)
- **C-34:** [PE-ARCH 라이브러리](https://www.notion.so/35755ed436f081b4a1b5e18e994297e5)

> Gilbert Kwak | PE-ARCH-P03 v2.0 | 2026-05-05 09:30 KST
