# P-03 · Brainstorming Requirements Clarification Prompt

> **버전**: v1.0 | **생성일**: 2026-04-26  
> **파일**: `scripts/brainstorming.py` → `refine_requirements()` 메서드  
> **모델**: claude-4-sonnet-20250514 | **Temperature**: `0.3` | **Max Tokens**: `4,000`  
> **역할**: 사용자 요청을 구조화된 YAML 요구사항으로 정제

---

## 프롬프트 원문

```
다음 요청을 분석하여 명확하고 구체적인 요구사항으로 refinement하세요.

<user_request>{user_request}</user_request>

다음 기준으로 검토하세요:

1. 범위 명확성
   - 시간 범위가 명시되어 있는가?
   - 지역/시장이 구체적인가?
   - 산업/제품이 명확한가?

2. 측정 가능성
   - 정량적 목표가 있는가?
   - 성공 기준이 명확한가?

3. 실행 가능성
   - 현실적으로 달성 가능한가?
   - 필요한 데이터 접근 가능한가?

4. 완전성
   - 누락된 중요 요소는 없는가?
   - 암묵적 가정은 없는가?

출력 형식: YAML
(refined_request / scope / objectives / assumptions / constraints / success_criteria)
```

---

## 출력 YAML 스키마

```yaml
refined_request: string
scope:
  time_range: string
  geography: string
  industry: string
objectives:
  - string
assumptions:
  - string
constraints:
  - string
success_criteria:
  - string
```

---

## 버전 이력

| 버전 | 날짜 | 변경 내용 |
|---|---|---|
| v1.0 | 2026-04-26 | 최초 생성 |
