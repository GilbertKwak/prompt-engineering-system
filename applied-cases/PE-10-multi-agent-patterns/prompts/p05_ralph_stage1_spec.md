# P-05 · Ralph Loop Stage 1 Spec Compliance Prompt

> **버전**: v1.0 | **생성일**: 2026-04-26  
> **파일**: `scripts/ralph_loop_2stage.py` → `review_stage1_spec_compliance()` 메서드  
> **모델**: claude-4-sonnet-20250514 | **Temperature**: `0.0` | **Max Tokens**: `3,000`  
> **역할**: 에이전트 출력이 요구사항 스펙을 충족하는지 검증

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

출력 형식: YAML
(stage1_result / compliance_score / checks / missing_elements / recommendations)
```

---

## 출력 YAML 스키마

```yaml
stage1_result: PASS | FAIL
compliance_score: float  # 0.0 ~ 1.0
checks:
  objectives_met: bool
  success_criteria_met: bool
  scope_compliant: bool
  constraints_compliant: bool
  no_missing_elements: bool
missing_elements:
  - string
recommendations:
  - string
```

## 판정 기준
- **PASS**: compliance_score ≥ 0.8 AND 모든 checks True
- **FAIL**: compliance_score < 0.8 OR 하나 이상 checks False → Ralph Loop 재진입

---

## 버전 이력

| 버전 | 날짜 | 변경 내용 |
|---|---|---|
| v1.0 | 2026-04-26 | 최초 생성 |
