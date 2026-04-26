# P-01 · Inception Error Detection Prompt

> **버전**: v1.0 | **생성일**: 2026-04-26  
> **파일**: `scripts/inception_module.py` → `detect_error()` 메서드  
> **모델**: claude-4-sonnet-20250514 | **Temperature**: `0.0` | **Max Tokens**: `500`  
> **역할**: 에이전트 응답에서 에러 유형 감지 및 분류

---

## 프롬프트 원문

```
다음 상황을 분석하여 에러 타입을 판단하세요.

<task>{task_description}</task>
<agent_response>{agent_response}</agent_response>
<context>
Available context: {list(context.keys())}
Previous results: {len(context.get('previous_results', []))}
Dependencies met: {context.get('dependencies_met', False)}
</context>

에러 타입을 다음 중 하나로 분류하세요:

1. ambiguous_request — 요청 모호/불명확
   시그널: "what do you mean", "unclear", "multiple interpretations"

2. missing_context — 필요 맥락 정보 부족
   시그널: "I don't have information about", "context needed"

3. dependency_failure — 선행 태스크 실패
   시그널: dependencies_met=False, missing previous results

4. agent_hallucination — 사실이 아닌 정보 생성
   시그널: 모순된 진술, 검증되지 않은 주장

5. none — 에러 없음, 정상 진행

답변 형식:
ERROR_TYPE: [error_type]
CONFIDENCE: [0.0-1.0]
REASON: [한 줄 설명]
```

---

## 파라미터 정의

| 변수 | 설명 | 타입 |
|---|---|---|
| `{task_description}` | 에이전트에게 부여된 원래 태스크 | string |
| `{agent_response}` | 에이전트가 반환한 응답 | string |
| `{context}` | 현재 실행 컨텍스트 딕셔너리 | dict |

## 판정 로직

- **Confidence ≥ 0.7** → 해당 ErrorType 반환
- **Confidence < 0.7** → `ErrorType.NONE` 반환 (오탐 방지)

## 에러 유형별 후속 처리

| ErrorType | 후속 프롬프트 | 전략 |
|---|---|---|
| `ambiguous_request` | P-02 | Clarify — 모호한 용어 정의 |
| `missing_context` | P-02 | KB Retrieve — 지식베이스 검색 주입 |
| `dependency_failure` | P-02 | Alternative — 독립 수행 가능 부분만 진행 |
| `agent_hallucination` | P-02 | Fact-Check — 모든 수치 출처 표시 |
| `none` | — | 정상 진행 |

---

## 버전 이력

| 버전 | 날짜 | 변경 내용 |
|---|---|---|
| v1.0 | 2026-04-26 | 최초 생성 |
