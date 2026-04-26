# P-06 · Ralph Loop Stage 2 Quality Check Prompt

> **버전**: v1.0 | **생성일**: 2026-04-26  
> **파일**: `scripts/ralph_loop_2stage.py` → `review_stage2_quality()` 메서드  
> **모델**: claude-4-sonnet-20250514 | **Temperature**: `0.0` | **Max Tokens**: `3,000`  
> **역할**: 4개 차원(정확성/완전성/명확성/실용성) 품질 검증 및 SHIP/ITERATE 판정

---

## 프롬프트 원문

```
다음 에이전트 출력의 품질을 검증하세요.

<task_description>{task_description}</task_description>
<agent_output>{agent_output}</agent_output>

Stage 2: Quality Check — 4개 차원 평가

1. 정확성 (Accuracy)
   - 사실 관계 정확성 / 데이터 검증 가능 여부 / 오류·모순 여부

2. 완전성 (Completeness)
   - 충분한 상세도 / 중요 측면 누락 여부 / 맥락 충분성

3. 명확성 (Clarity)
   - 이해 용이성 / 논리적 구조 / 전문용어 설명

4. 실용성 (Actionability)
   - 실행 가능한 인사이트 / 의사결정 지원 / 구체적 권장사항

출력 형식: YAML
(stage2_result / quality_score / dimensions[4개] / overall_assessment / decision: SHIP|ITERATE / iteration_guidance)
```

---

## 출력 YAML 스키마

```yaml
stage2_result: PASS | FAIL
quality_score: float  # 0.0 ~ 1.0
dimensions:
  accuracy: { score: float, issues: [string] }
  completeness: { score: float, issues: [string] }
  clarity: { score: float, issues: [string] }
  actionability: { score: float, issues: [string] }
overall_assessment: string
decision: SHIP | ITERATE
iteration_guidance:
  - string
```

## 판정 기준
- **SHIP**: quality_score ≥ 0.75 AND decision = SHIP
- **ITERATE**: quality_score < 0.75 OR decision = ITERATE → 최대 3회 반복
- **최대 반복 초과**: 경고 플래그 설정 후 현재 상태로 SHIP

---

## 버전 이력

| 버전 | 날짜 | 변경 내용 |
|---|---|---|
| v1.0 | 2026-04-26 | 최초 생성 |
