# P-07 · Recursive Task Decomposition Prompt

> **버전**: v1.0 | **생성일**: 2026-04-26  
> **파일**: `agents/patent_agent/recursive_delegation.py` → `_decompose_task()` 메서드  
> **모델**: claude-4-sonnet-20250514 | **Temperature**: `0.0` | **Max Tokens**: `1,000`  
> **역할**: 복잡한 태스크를 병렬 처리 가능한 2-4개 서브태스크로 분해

---

## 프롬프트 원문

```
다음 특허 분석 태스크를 2-4개의 독립적인 서브태스크로 분해하세요.

현재 깊이: {depth}/{max_depth}

<task>{task}</task>

각 서브태스크는:
1. 독립적으로 수행 가능해야 함
2. 병렬 처리 가능해야 함
3. 명확한 산출물이 있어야 함

만약 더 이상 분해할 필요가 없다면 "NO_DECOMPOSITION"을 반환하세요.

출력 형식:
SUBTASK_1: [서브태스크 1]
SUBTASK_2: [서브태스크 2]
SUBTASK_3: [서브태스크 3]
```

---

## 파라미터 정의

| 변수 | 설명 | 기본값 |
|---|---|---|
| `{depth}` | 현재 재귀 깊이 | 0 |
| `{max_depth}` | 최대 재귀 깊이 | 2 |
| `{task}` | 분해할 태스크 설명 | — |

## 분해 중단 조건
- `NO_DECOMPOSITION` 반환 시 → P-08 Leaf 실행으로 전환
- `depth >= max_depth` 시 → 강제 P-08 전환

---

## 버전 이력

| 버전 | 날짜 | 변경 내용 |
|---|---|---|
| v1.0 | 2026-04-26 | 최초 생성 |
