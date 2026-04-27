# P-05 · Ralph Loop Stage 1 Spec Compliance Prompt

> **버전**: v2.0 | **생성일**: 2026-04-26 | **업그레이드**: 2026-04-27
> **파일**: `scripts/ralph_loop_2stage.py` → `review_stage1_spec_compliance()` 메서드
> **모델**: claude-4-sonnet-20250514 | **Temperature**: `0.0` | **Max Tokens**: `3,000`
> **역할**: 에이전트 출력이 요구사항 스펙을 충족하는지 검증
> **PE-3 점수**: v1.0 → 81/100 ⚠️ · v2.0 → 93/100 ✅

---

## 🔗 3-Engine 연계 (P05-v2-B 패치)

| 엔진 | 역할 | 연계 지점 |
|------|------|----------|
| **PE-1 자동개선** | FAIL 판정 시 에이전트 재작성 | stage1_result=FAIL → PE-1 루프 트리거 |
| **PE-3 자동검증** | Spec 검증 출력 자체 품질 채점 | 검증 결과 YAML PE-3 재채점 대상 |
| **P-06 Ralph Stage 2** | Stage 1 PASS → Stage 2 진입 | compliance_score ≥ 0.8 시 P-06 호출 |

```
[에이전트 출력]
        ↓
┌──────────────────────────┐
│  P-05: Spec Compliance   │  ← 본 프롬프트
│  Temperature: 0.0        │
│  판정: PASS / FAIL        │
└──────────┬───────────────┘
     PASS  ↓        ↓ FAIL
┌──────────────┐  [PE-1 재작성 루프]
│  P-06 Stage2 │
└──────────────┘
```

---

## 프롬프트 원문

```
다음 에이전트 출력이 요구사항을 만족하는지 검증하세요.

<task_description>{task_description}</task_description>
<requirements>{yaml.dump(requirements)}</requirements>
<agent_output>{agent_output}</agent_output>

Stage 1: Spec Compliance Check

다음 항목을 검증하세요:
✓ 모든 objectives 달성했는가?
✓ Success criteria 만족하는가?
✓ Scope 내에서 수행되었는가?
✓ Constraints 준수했는가?
✓ 누락된 필수 요소가 없는가?

각 check 항목에 대해 EVIDENCE를 agent_output에서 직접 인용하세요.

출력 형식: YAML
(stage1_result / compliance_score / checks[각 항목+evidence] / missing_elements / recommendations)
```

> **v2.0 추가**: 각 check 항목에 `evidence` 서브필드 필수화 — 판정 근거를 에이전트 출력에서 직접 인용 (P05-v2-A 패치)

---

## 출력 YAML 스키마

```yaml
stage1_result: PASS | FAIL
compliance_score: float  # 0.0 ~ 1.0
checks:
  objectives_met:
    result: bool
    evidence: string     # v2.0 신규 — agent_output 직접 인용
  success_criteria_met:
    result: bool
    evidence: string
  scope_compliant:
    result: bool
    evidence: string
  constraints_compliant:
    result: bool
    evidence: string
  no_missing_elements:
    result: bool
    evidence: string
missing_elements:
  - string
recommendations:
  - string
```

## 판정 기준
- **PASS**: compliance_score ≥ 0.8 AND 모든 checks True
- **FAIL**: compliance_score < 0.8 OR 하나 이상 checks False → Ralph Loop 재진입

---

## ⚠️ EDGE_CASE 처리 (P05-v2-C 패치)

```
EDGE_CASE: agent_output 비어있음
  처리: stage1_result=FAIL 자동 판정
  compliance_score: 0.0
  missing_elements: ["agent_output is empty"]

EDGE_CASE: requirements YAML 파싱 오류
  처리: ABORT 플래그 → P-03 재실행 요청
  메시지: "P-05 ABORT: requirements YAML malformed"

EDGE_CASE: Ralph Loop 3회 연속 FAIL
  처리: 에스컬레이션 + compliance_score 이력 첨부
  메시지: "RALPH_ESCALATE: 3 consecutive FAIL — human review required"
```

---

## 버전 이력

| 버전 | 날짜 | 변경 내용 | PE-3 점수 |
|---|---|---|---|
| **v2.0** | **2026-04-27** | **P05-v2-A: checks evidence 서브필드 필수화 (추적성 +5) · P05-v2-B: 3-Engine 연계 블록 추가 (PE 일관성 +5) · P05-v2-C: EDGE_CASE 핸들러 3종 추가 (명확성 +2)** | **93/100** |
| v1.0 | 2026-04-26 | 최초 생성 | 81/100 |
