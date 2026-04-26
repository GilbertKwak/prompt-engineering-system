# P-04 · Brainstorming Plan Generation Prompt

> **버전**: v1.0 | **생성일**: 2026-04-26  
> **파일**: `scripts/brainstorming.py` → `generate_plan_outline()` 메서드  
> **모델**: claude-4-sonnet-20250514 | **Temperature**: `0.3` | **Max Tokens**: `4,000`  
> **역할**: P-03 정제 요구사항 기반 단계별 실행 계획 YAML 생성

---

## 프롬프트 원문

```
다음 요구사항에 대한 실행 계획을 작성하세요.

<requirements>{yaml.dump(refined_requirements)}</requirements>

각 단계를 2-5분 단위의 구체적 작업으로 분해하세요.

출력 형식: YAML
(plan[phase/duration_estimate/tasks] / dependencies / total_estimate)
```

---

## 출력 YAML 스키마

```yaml
plan:
  - phase: string
    duration_estimate: string
    tasks:
      - string
dependencies:
  - string
total_estimate: string
```

---

## 버전 이력

| 버전 | 날짜 | 변경 내용 |
|---|---|---|
| v1.0 | 2026-04-26 | 최초 생성 |
