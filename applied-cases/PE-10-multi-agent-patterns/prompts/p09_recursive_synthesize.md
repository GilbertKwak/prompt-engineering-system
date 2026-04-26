# P-09 · Recursive Result Synthesis Prompt

> **버전**: v1.0 | **생성일**: 2026-04-26  
> **파일**: `agents/patent_agent/recursive_delegation.py` → `_synthesize_results()` 메서드  
> **모델**: claude-4-sonnet-20250514 | **Temperature**: `0.3` | **Max Tokens**: `4,000`  
> **역할**: 병렬 실행된 서브태스크 결과들을 통합하여 원래 태스크 최종 답변 생성

---

## 프롬프트 원문

```
다음 서브태스크 결과들을 통합하여 원래 태스크에 대한 종합 분석을 작성하세요.

<original_task>{original_task}</original_task>

<subtask_results>
=== Subtask 1 === {result_1}
=== Subtask 2 === {result_2}
=== Subtask 3 === {result_3}
</subtask_results>

통합 요구사항:
1. 모든 서브태스크 결과를 포괄
2. 중복 제거
3. 일관된 서술
4. 핵심 인사이트 도출
5. 실행 가능한 권장사항

답변 형식:
종합 분석 / 핵심 인사이트(3개) / 권장사항(2개) / 종합 결론(1문장)
```

---

## 통합 전략

| 상황 | 처리 방법 |
|---|---|
| 서브태스크 결과 충돌 | 더 구체적 증거를 가진 결과 우선 채택, 충돌 명시 |
| 서브태스크 결과 누락 | 가용 결과만으로 통합, 누락 항목 명시 |
| 결과 간 중복 | 중복 제거 후 핵심만 유지 |

---

## 버전 이력

| 버전 | 날짜 | 변경 내용 |
|---|---|---|
| v1.0 | 2026-04-26 | 최초 생성 |
