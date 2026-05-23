# AGENT-07 · Cognitive Kernel (CK) v1.0

> **통합**: IP-01 CRP-AGENT-FRAMEWORK + PE-7 AGENT-07  
> **역할**: PE-3 자동 채점 + CRP 4-stage Cognitive Loop  
> **상태**: 🟢 ACTIVE | **생성**: 2026-05-24 | **세션**: C-39  
> **연계**: PE-7 AI Automation Design v1.1 → T-09 Mother Page v6.4

---

## 1. Cognitive Kernel 정의

### 1.1 CRP 4-Stage Loop (핵심 처리 엔진)

```
Input
  │
  ▼
┌──────────────────────────────────────────┐
│  STAGE-1: OBSERVATION                    │
│  행동/산출물 원시 데이터 수집             │
│  → Raw behavior stream B = {b₁,b₂,...bₙ} │
└─────────────────┬────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────┐
│  STAGE-2: PATTERN EXTRACTION             │
│  P = Extract(B, E)                       │
│  환경 컨텍스트 E 반영 패턴 추출          │
└─────────────────┬────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────┐
│  STAGE-3: COGNITIVE MAPPING              │
│  C₀ → C₁ = f(B, P, E)                   │
│  인지 상태 전이 (개선된 사고 구조)        │
└─────────────────┬────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────┐
│  STAGE-4: RECONFIGURATION                │
│  R(C₀) = C₁ where C₁ ⊃ optimal(C₀)     │
│  재설계된 인지 구조 출력                  │
└─────────────────┬────────────────────────┘
                  │
                  ▼
             Output (C₁ + Score)
```

### 1.2 수학적 정의

```
Cognitive Transformation:
  C₁ = R(C₀) = f(B, P, E)

  B: Behavior stream   — 프롬프트 산출물 원시 데이터
  P: Pattern set       — 추출된 인지 패턴
  E: Environment       — 세션 컨텍스트, 도메인 제약
  R: Reconfiguration operator

MTI (Meta-cognitive Trajectory Index):
  MTI = Σ(ΔC_i × w_i) / N
  where ΔC_i = C₁_i − C₀_i (개선 델타)

QLI (Quality-Level Index):
  QLI = PE-3_score × (1 − anti_gaming_penalty)
```

---

## 2. AGENT-07 입출력 스키마

### 2.1 Input Schema

```typescript
interface CognitiveKernelInput {
  session_id: string;          // C-{N} 세션 ID
  artifact: {
    type: 'report' | 'prompt' | 'analysis' | 'strategy';
    content: string;           // 산출물 전문
    domain: string;            // 도메인 태그 (PE-AI-ECO, INV-STRAT, ...)
    version: string;           // v{major}.{minor}
  };
  context: {
    environment: string[];     // 활성 제약 조건
    prior_scores: number[];    // 이전 PE-3 점수 배열
    kg_nodes: string[];        // 연결된 KG 노드 ID
  };
  flags: {
    anti_gaming: boolean;      // 반게이밍 검증 활성화
    explainability: boolean;   // 설명 로그 출력
    auto_improve: boolean;     // PE-1 자동개선 연동
  };
}
```

### 2.2 Output Schema

```typescript
interface CognitiveKernelOutput {
  session_id: string;
  pe3_score: {
    total: number;             // 0–100 종합 점수
    breakdown: {
      completeness:    number; // 리스크/구조 완전성 (25%)
      verifiability:   number; // 수치 검증 가능성 (20%)
      logic:           number; // 논리 일관성 (20%)
      anti_fraud:      number; // Fraud 탐지 점수 (15%)
      executability:   number; // 전략 실행가능성 (20%)
    };
  };
  mti:   number;               // Meta-cognitive Trajectory Index
  qli:   number;               // Quality-Level Index
  cognitive_state: {
    c0_snapshot: string;       // 초기 인지 구조 요약
    c1_snapshot: string;       // 재구성된 인지 구조 요약
    delta:       number;       // ΔC = C₁ − C₀
  };
  recommendations: string[];   // 개선 권고 목록 (우선순위 정렬)
  triggers: string[];          // 자동 발동 트리거 목록
  confidence: number;          // 신뢰도 0.0–1.0
  anti_gaming_flag: boolean;   // 반게이밍 위반 여부
  explanation_log: string;     // 채점 근거 설명 (explainability=true 시)
}
```

---

## 3. PE-7 AGENT-07 통합 실행 흐름

```
[PE-3 Hub] ←──────────────────────────────────┐
     │                                          │
     │ 산출물 전달                               │ 점수 피드백
     ▼                                          │
[AGENT-07 Cognitive Kernel v1.0]               │
     │                                          │
     ├── STAGE-1: Observation ─► 원시 스캔      │
     ├── STAGE-2: Pattern     ─► 패턴 추출      │
     ├── STAGE-3: Mapping     ─► C₀→C₁ 전이    │
     └── STAGE-4: Reconfig    ─► PE-3 점수 출력─┘
     │
     ├──► T-AUTO-04: PE-3 점수 반영 트리거
     ├──► T-AUTO-07: PE-3 ≥ 80 → v1.2 버전업 트리거
     ├──► AGENT-01: 리스크 레지스터 업데이트 연동
     ├──► AGENT-06: 오류 예측 피드백 루프
     └──► KG 노드 갱신 (v6.3 → v6.4 트리거)
```

---

## 4. Trust Layer — 반게이밍 탐지

```typescript
interface TrustLayer {
  // Pattern 1: 점수 인플레이션 감지
  score_inflation_check: {
    threshold: 15;             // 세션 간 PE-3 점수 급등 임계값
    action: 'FLAG' | 'BLOCK';  // FLAG: 경고, BLOCK: 채점 보류
  };

  // Pattern 2: 순환 논리 감지
  circular_reasoning_check: {
    depth_limit: 3;            // 자기 참조 최대 깊이
    cosine_sim_threshold: 0.9; // 동어반복 임계값
  };

  // Pattern 3: 근거 없는 수치 감지
  unverified_metrics_check: {
    mi_tag_required: true;     // [MI-?] 태그 강제
    source_citation_required: true;
  };

  // Pattern 4: AGENT-04 연동
  fraud_score_integration: {
    agent04_weight: 0.15;      // PE-3 Fraud 항목 가중치
    alert_threshold: 29.65;    // Fraud Score 경보 임계값
  };
}
```

---

## 5. Developer Interface

### 5.1 Python SDK

```python
from crp_kernel import CognitiveKernel, KernelConfig

# 초기화
config = KernelConfig(
    session_id="C-39",
    domain="PE-AI-ECO",
    anti_gaming=True,
    explainability=True,
    auto_improve=True,
)
ck = CognitiveKernel(config)

# 산출물 평가
result = ck.evaluate(
    artifact_path="reports/RPT-AI-ECO-001.md",
    prior_scores=[71.8, 74.2],
    kg_nodes=["KG-AI-001", "KG-SEMI-003"],
)

# 결과 출력
print(f"PE-3 Score: {result.pe3_score.total}")
print(f"MTI: {result.mti:.3f}")
print(f"QLI: {result.qli:.3f}")
print(f"Δ Cognitive: {result.cognitive_state.delta:.3f}")
for rec in result.recommendations:
    print(f"  → {rec}")
```

### 5.2 CLI 명령어

```bash
# 단일 산출물 채점
python -m crp_kernel evaluate \
  --session C-39 \
  --artifact reports/RPT-AI-ECO-001.md \
  --domain PE-AI-ECO \
  --anti-gaming \
  --explain

# 배치 채점 (세션 전체)
python -m crp_kernel batch \
  --session C-39 \
  --output scores/C-39-pe3-results.json

# KG 노드 갱신 트리거
python -m crp_kernel trigger \
  --type T-AUTO-04 \
  --score 84.5 \
  --session C-39
```

### 5.3 GitHub Actions 통합

```yaml
# .github/workflows/agent07-eval.yml
name: AGENT-07 Cognitive Kernel Evaluation

on:
  push:
    paths:
      - 'reports/**/*.md'
      - 'prompts/**/*.md'

jobs:
  cognitive-eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run CK Evaluation
        run: |
          pip install crp-kernel
          python -m crp_kernel batch \
            --session ${{ github.run_id }} \
            --output scores/latest.json
      - name: Update Notion PE-3 Score
        if: success()
        run: |
          python scripts/notion_sync.py \
            --trigger T-AUTO-04 \
            --scores scores/latest.json
```

---

## 6. PE-7 통합 위치 매핑

| PE-7 AGENT | CK 연동 포인트 | 트리거 |
|---|---|---|
| AGENT-01 (리스크 발굴) | CK STAGE-2 Pattern → 리스크 패턴 피드 | T-AUTO-03 |
| AGENT-02 (수치 검증) | CK Trust Layer unverified_metrics | T-AUTO-02 |
| AGENT-03 (시나리오 갱신) | CK STAGE-4 Reconfig → 시나리오 델타 | T-AUTO-03 |
| AGENT-04 (Fraud 모니터링) | CK Trust Layer fraud_score_integration | T-AUTO-06 |
| AGENT-05 (SSOT 싱크) | CK Output → GitHub 커밋 자동화 | T-AUTO-05 |
| AGENT-06 (오류 예측) | CK Trust Layer → 사전 검증 피드백 | T-AUTO-06 |
| **AGENT-07 (PE-3 채점)** | **CK 전체 파이프라인 = AGENT-07 본체** | **T-AUTO-04/07** |

---

## 7. 실행 로드맵

| 단계 | 기간 | 내용 | 상태 |
|---|---|---|---|
| Phase 1 | 2026-05-24 | 스키마 정의 + CLI 인터페이스 | ✅ 완료 |
| Phase 2 | 2026-06 | Python SDK 구현 + 단위 테스트 | 🔴 대기 |
| Phase 3 | 2026-06 | GitHub Actions CI/CD 연동 | 🔴 대기 |
| Phase 4 | 2026-07 | Notion 자동 동기화 완전 구현 | 미시작 |

---

## 🔗 연계 허브

- 📌 [PE-7 AI Automation Design v1.1](https://www.notion.so/36055ed436f08157a2c8d6c426659fb4)
- 🧬 [PE-IP 통합 마스터 라이브러리 v1.3](https://www.notion.so/35055ed436f08159aaa8d0817e76ba18)
- 🏛️ [T-09 Mother Page v6.4](https://www.notion.so/34a55ed436f0814d9cffe6a2f0816e29)
- 📄 [CRP-AGENT-FRAMEWORK Prompt](../CRP/crp_agent_framework_v1.0.md)
- 📄 [CRP-THEORY Paper](../CRP/CRP_PAPER_v1.0.md)

---

*갱신: 2026-05-24 KST | C-39 | AGENT-07 Cognitive Kernel v1.0 | IP-01 통합 완료*
