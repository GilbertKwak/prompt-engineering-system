# P-01 · Inception Error Detection Prompt

> **버전**: v2.0 | **생성일**: 2026-04-26 | **업그레이드**: 2026-04-27
> **파일**: `scripts/inception_module.py` → `detect_error()` 메서드
> **모델**: claude-4-sonnet-20250514 | **Temperature**: `0.0` | **Max Tokens**: `600`
> **역할**: 에이전트 응답에서 에러 유형 감지·분류·판단 근거 추적
> **PE-3 점수**: v1.0 → 80/100 ⚠️ · v2.0 → 93/100 ✅

---

## 🔗 3-Engine 연계 (PE Consistency — P01-v2-B 패치)

| 엔진 | 역할 | 연계 지점 |
|------|------|----------|
| **PE-1 자동개선** | 에러 감지 후 프롬프트 재작성 루프 | `ERROR_TYPE ≠ none` 시 PE-1 트리거 |
| **PE-3 자동검증** | 본 프롬프트 출력 품질 5차원 채점 | 신규 버전 배포 시 필수 재채점 |
| **PE-10 파이프라인** | Inception 패턴 첫 관문 | P-01 → P-02(복구 주입) 순차 실행 |

```
[멀티에이전트 실행]
        ↓
┌─────────────────────┐
│  P-01: 에러 감지     │  ← 본 프롬프트
│  Temperature: 0.0   │
│  출력: ERROR_TYPE    │
└──────┬──────────────┘
       │ ERROR_TYPE ≠ none
       ↓
┌─────────────────────┐
│  P-02: 복구 주입     │
│  (Inception Recovery)│
└─────────────────────┘
       │ ERROR_TYPE = none
       ↓
  [정상 파이프라인 계속]
```

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
   판단 트리: task_description 내 대명사 미정의 OR 조건 충돌 → 즉시 분류

2. missing_context — 필요 맥락 정보 부족
   시그널: "I don't have information about", "context needed"
   판단 트리: context.keys() 중 필수 키 누락 AND 응답에 불확실 표현 존재

3. dependency_failure — 선행 태스크 실패
   시그널: dependencies_met=False, missing previous results
   판단 트리: dependencies_met=False → 즉시 분류 (신호 강도 무관)

4. agent_hallucination — 사실이 아닌 정보 생성
   시그널: 모순된 진술, 검증되지 않은 수치·고유명사
   판단 트리: 응답 내 수치/기업명/날짜 → context 교차 검증 → 불일치 시 분류

5. none — 에러 없음, 정상 진행

답변 형식:
ERROR_TYPE: [error_type]
CONFIDENCE: [0.0-1.0]
REASON: [한 줄 설명]
EVIDENCE: [판단 근거 — 응답 내 구체적 텍스트 인용 또는 컨텍스트 키 명시]
```

> **v2.0 추가**: `EVIDENCE` 필드 신규 — 판단 근거를 응답 텍스트 또는 컨텍스트 키로 명시하여 추적성 보장 (P01-v2-A 패치)

---

## 파라미터 정의

| 변수 | 설명 | 타입 |
|---|---|---|
| `{task_description}` | 에이전트에게 부여된 원래 태스크 | string |
| `{agent_response}` | 에이전트가 반환한 응답 | string |
| `{context}` | 현재 실행 컨텍스트 딕셔너리 | dict |

---

## 판정 로직

- **Confidence ≥ 0.7** → 해당 ErrorType 반환
- **Confidence < 0.7** → `ErrorType.NONE` 반환 (오탐 방지)
- **EVIDENCE 필드 필수** → 비어있을 경우 파이프라인에서 재실행 트리거

---

## 에러 유형별 후속 처리

| ErrorType | 후속 프롬프트 | 전략 |
|---|---|---|
| `ambiguous_request` | P-02 | Clarify — 모호한 용어 정의 |
| `missing_context` | P-02 | KB Retrieve — 지식베이스 검색 주입 |
| `dependency_failure` | P-02 | Alternative — 독립 수행 가능 부분만 진행 |
| `agent_hallucination` | P-02 | Fact-Check — 모든 수치 출처 표시 |
| `none` | — | 정상 진행 |

---

## ⚠️ 엣지케이스 처리 (P01-v2-C 패치)

```
EDGE_CASE: 복합 에러 (2개 이상 에러 신호 동시 감지)
  처리: 우선순위 적용
    1순위: dependency_failure (시스템 레벨 — 즉시 중단)
    2순위: agent_hallucination (정보 신뢰성 — 즉시 격리)
    3순위: missing_context (컨텍스트 보완으로 해결 가능)
    4순위: ambiguous_request (재질의로 해결 가능)
  출력: 최고 우선순위 ErrorType 단일 반환
  EVIDENCE: 복수 신호 모두 기재 (쉼표 구분)

EDGE_CASE: context 딕셔너리 비어있음 (keys = [])
  처리: missing_context 자동 분류
  CONFIDENCE: 0.95 고정
  REASON: "Empty context — insufficient execution environment"

EDGE_CASE: agent_response 길이 < 10자
  처리: ambiguous_request 자동 분류
  CONFIDENCE: 0.90 고정
  REASON: "Response too short to evaluate"

EDGE_CASE: task_description 미제공 또는 빈 문자열
  처리: 프롬프트 실행 중단 → 호출 코드에 ValueError 반환
  메시지: "P-01 ABORT: task_description is required"
```

---

## 버전 이력

| 버전 | 날짜 | 변경 내용 | PE-3 점수 |
|---|---|---|---|
| **v2.0** | **2026-04-27** | **P01-v2-A: EVIDENCE 필드 + 에러 유형별 판단 트리 추가 (추적성 +5) · P01-v2-B: 3-Engine 연계 블록 + 표준 헤더 통일 (PE 일관성 +6) · P01-v2-C: EDGE_CASE 핸들러 4종 추가 (명확성 +2)** | **93/100** |
| v1.0 | 2026-04-26 | 최초 생성 | 80/100 |
