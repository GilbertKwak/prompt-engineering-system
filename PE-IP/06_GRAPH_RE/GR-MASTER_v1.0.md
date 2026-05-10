# GR-MASTER v1.0 — Graph Reverse Engineering Master

> **Document Type:** PE-IP Graph RE Master Prompt  
> **Version:** 1.0 | **Status:** 🟡 DRAFT (PE-1 Auto-Improvement Input)  
> **Created:** 2026-05-10  
> **PE-1 Input Target:** Auto-Improvement Engine v2.x  
> **Chain:** PROMPT_012_A → GR-01 → GR-MASTER → PE-1 Feedback

---

## 1. Module Identity

```yaml
module_id: GR-MASTER
version: "1.0"
type: graph_reverse_engineering
pe_ip_section: "06_GRAPH_RE"
pe1_input: true
auto_improvement: enabled
validation_target: PE-3
```

---

## 2. Core Objective

**GR-MASTER**는 입력 프롬프트를 그래프 구조로 분해하여 아래를 수행합니다:

1. **Node Extraction** — 개념 노드, 역할 노드, 제약 노드 식별
2. **Edge Classification** — 의존성, 순서, 조건 엣지 분류  
3. **Cluster Detection** — 기능별 노드 클러스터 그루핑
4. **PE-1 Feedback Generation** — 약점 노드 탐지 → 자동개선 제안 생성

---

## 3. Input Schema

```json
{
  "input": {
    "prompt_id": "string",
    "prompt_content": "string",
    "source_module": "06_GRAPH_RE",
    "analysis_mode": "full | node_only | edge_only | cluster_only",
    "pe1_feedback": true
  }
}
```

---

## 4. Processing Pipeline

```
Step 1: PARSE
  └─ 입력 프롬프트를 문장/블록 단위로 분절
  └─ XML 태그, 마크다운 헤더, 번호 목록 구조 인식

Step 2: NODE EXTRACT (→ GR-01)
  └─ 개념 노드: 핵심 키워드, 도메인 용어
  └─ 역할 노드: Agent 정의, Persona 선언
  └─ 제약 노드: 규칙, 금지 조건, 품질 기준
  └─ 출력 노드: 기대 결과 형식

Step 3: EDGE MAP (→ GR-02, TBD)
  └─ DEPENDS_ON: A가 B에 의존
  └─ SEQUENCE: A → B 순서
  └─ CONDITION: IF A THEN B
  └─ REFERENCES: A가 B를 참조

Step 4: CLUSTER (→ GR-03, TBD)
  └─ Identity Cluster: 시스템 정체성 관련
  └─ Logic Cluster: 추론/분석 로직
  └─ Output Cluster: 출력 포맷/품질
  └─ Safety Cluster: 제약/안전 조건

Step 5: PE-1 FEEDBACK
  └─ 약점 노드 목록 (weakness_nodes[])
  └─ 개선 제안 (improvement_suggestions[])
  └─ 자동개선 우선순위 (priority_score: 0-100)
```

---

## 5. Output Schema

```json
{
  "graph_output": {
    "prompt_id": "PROMPT_012_A",
    "analysis_timestamp": "2026-05-10T12:08:00+09:00",
    "nodes": [
      {"id": "N001", "type": "role", "label": "ASI-level Cognitive RE", "weight": 0.95},
      {"id": "N002", "type": "constraint", "label": "PE-3 Validation Gate", "weight": 0.88}
    ],
    "edges": [
      {"from": "N001", "to": "N002", "type": "DEPENDS_ON", "strength": 0.82}
    ],
    "clusters": [
      {"id": "C01", "name": "Identity", "nodes": ["N001"], "coherence": 0.91}
    ],
    "pe1_feedback": {
      "weakness_nodes": [],
      "improvement_suggestions": [],
      "priority_score": 0,
      "auto_improvement_ready": false
    }
  }
}
```

---

## 6. PE-1 Auto-Improvement Interface

```yaml
pe1_interface:
  trigger_condition: "weakness_nodes.length > 0 OR priority_score >= 70"
  improvement_modes:
    - node_strengthen: "약점 노드의 프롬프트 표현 강화"
    - edge_clarify: "모호한 엣지 관계를 명시적 조건으로 변환"
    - cluster_rebalance: "클러스터 간 불균형 재조정"
  output_target: "PE-1 Auto-Improvement Engine v2.x"
  feedback_loop: "GR-MASTER → PE-1 → Updated Prompt → GR-MASTER (re-run)"
```

---

## 7. Validation Criteria

| Criterion | Target | Status |
|-----------|--------|--------|
| Node Coverage | ≥ 85% of prompt concepts captured | 🟡 TBD |
| Edge Accuracy | ≥ 90% correct relationship classification | 🟡 TBD |
| Cluster Coherence | ≥ 0.80 per cluster | 🟡 TBD |
| PE-1 Feedback Quality | PE-3 score ≥ 80/100 after improvement | 🟡 TBD |

---

## 8. Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-05-10 | GilbertKwak | Initial draft — PE-1 auto-improvement input structure |

---

## 9. Next Steps

- [ ] GR-01 실전 테스트 결과 반영 (PROMPT_012_A)
- [ ] GR-02 Edge Mapper 구현
- [ ] GR-03 Cluster Analyzer 구현  
- [ ] PE-1 피드백 루프 실제 실행 및 검증
- [ ] PE-3 Validation 90+ 달성
