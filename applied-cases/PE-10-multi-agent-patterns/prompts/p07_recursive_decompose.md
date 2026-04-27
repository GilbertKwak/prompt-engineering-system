# P-07 · Recursive Task Decomposition Prompt

> **버전**: v2.0 | **생성일**: 2026-04-26 | **업그레이드**: 2026-04-27
> **파일**: `agents/patent_agent/recursive_delegation.py` → `_decompose_task()` 메서드
> **모델**: claude-4-sonnet-20250514 | **Temperature**: `0.0` | **Max Tokens**: `1,000`
> **역할**: 복잡한 태스크를 병렬 처리 가능한 2-4개 서브태스크로 분해
> **PE-3 점수**: v1.0 → 77/100 ⚠️ · v2.0 → 91/100 ✅

---

## 🔗 3-Engine 연계 (P07-v2-B 패치)

| 엔진 | 역할 | 연계 지점 |
|------|------|----------|
| **PE-1 자동개선** | 분해 품질 미달 시 재분해 | 서브태스크 독립성 위반 시 PE-1 재실행 |
| **PE-3 자동검증** | 분해 결과 검증 | 서브태스크 YAML PE-3 채점 |
| **P-08 Leaf 실행** | 분해 완료 → Leaf 실행 | NO_DECOMPOSITION 또는 max_depth 도달 시 P-08 전환 |

```
[복잡한 태스크]
        ↓
┌──────────────────────────┐
│  P-07: 태스크 분해        │  ← 본 프롬프트 (재귀 호출 가능)
│  Temperature: 0.0        │
│  depth: {depth}/{max}    │
└──────────┬───────────────┘
  분해 가능 ↓        ↓ NO_DECOMPOSITION
[P-07 재귀]    [P-08 Leaf 실행]
```

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

각 서브태스크에 DECOMP_REASON을 포함하여 분해 근거를 명시하세요.

출력 형식:
SUBTASK_1: [서브태스크 1]
DECOMP_REASON_1: [분해 근거 — 독립성·병렬성 설명]
SUBTASK_2: [서브태스크 2]
DECOMP_REASON_2: [분해 근거]
SUBTASK_3: [서브태스크 3] (선택)
DECOMP_REASON_3: [분해 근거] (선택)
```

> **v2.0 추가**: `DECOMP_REASON_N` 필드 신규 — 각 서브태스크 분해 근거를 독립성·병렬성 관점에서 명시 (P07-v2-A 패치)

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

## ⚠️ EDGE_CASE 처리 (P07-v2-C 패치)

```
EDGE_CASE: 서브태스크 간 의존성 감지 (독립성 위반)
  처리: DECOMP_REASON에 [DEPENDENCY_RISK] 태그 부착
  권고: 의존 서브태스크를 순차 실행으로 전환

EDGE_CASE: 분해 결과가 1개 서브태스크만 생성
  처리: NO_DECOMPOSITION으로 자동 전환 → P-08 진입
  이유: 단일 서브태스크 분해는 무의미

EDGE_CASE: task 설명 모호 (< 30자 또는 동사 없음)
  처리: P-03/P-04 재실행 권고 메시지 발행
  메시지: "DECOMP_ABORT: task too ambiguous — re-run P-03"
```

---

## 버전 이력

| 버전 | 날짜 | 변경 내용 | PE-3 점수 |
|---|---|---|---|
| **v2.0** | **2026-04-27** | **P07-v2-A: DECOMP_REASON 필드 추가 (추적성 +5) · P07-v2-B: 3-Engine 연계 블록 추가 (PE 일관성 +6) · P07-v2-C: EDGE_CASE 핸들러 3종 추가 (명확성 +3)** | **91/100** |
| v1.0 | 2026-04-26 | 최초 생성 | 77/100 |
