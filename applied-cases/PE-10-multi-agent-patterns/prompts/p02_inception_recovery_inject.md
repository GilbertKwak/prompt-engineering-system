# P-02 · Inception Recovery Injection Prompt

> **버전**: v2.0 | **생성일**: 2026-04-26 | **업그레이드**: 2026-04-27
> **파일**: `scripts/inception_module.py` → `inject_reasoning()` 메서드
> **방식**: 프리픽스(Prefix) 주입 — 원본 프롬프트 앞에 삽입
> **역할**: P-01 에러 감지 후 복구 계획을 프롬프트에 주입
> **PE-3 점수**: v1.0 → 76/100 ⚠️ · v2.0 → 91/100 ✅

---

## 🔗 3-Engine 연계 (P02-v2-B 패치)

| 엔진 | 역할 | 연계 지점 |
|------|------|----------|
| **PE-1 자동개선** | 복구 주입 후 재작성 루프 | 주입 완료 → PE-1 재실행 트리거 |
| **PE-3 자동검증** | 복구 후 출력 품질 재채점 | 복구 완료 시 PE-3 재점수 산정 |
| **P-01 Inception** | 에러 감지 → 본 프롬프트 호출 | P-01 ERROR_TYPE ≠ none 시 활성화 |

```
[P-01 에러 감지]
        ↓ ERROR_TYPE ≠ none
┌─────────────────────────┐
│  P-02: 복구 주입        │  ← 본 프롬프트
│  PREFIX + original      │
└──────────┬──────────────┘
           ↓ 주입 완료
[에이전트 재실행 → PE-3 재채점]
```

---

## 프롬프트 원문

```
<inception_recovery>
이전 시도에서 문제가 감지되었습니다. 다음 복구 계획을 따라 진행하세요:

{recovery_plan}

SOURCE_ERROR_TYPE: {error_type}
SOURCE_EVIDENCE: {evidence}

이제 원래 태스크를 복구 계획을 고려하여 다시 수행하세요.
</inception_recovery>

{original_prompt}
```

> **v2.0 추가**: `SOURCE_ERROR_TYPE` / `SOURCE_EVIDENCE` 필드 신규 — P-01 판단 근거를 복구 컨텍스트에 전달하여 추적성 보장 (P02-v2-A 패치)

---

## 에러 유형별 복구 메시지

### ambiguous_request
```
요청의 모호성이 감지되었습니다.
다음을 명확히 하여 답변하세요:
1. 모호한 용어가 있다면 정의하세요
2. 해석의 범위를 명확히 하세요
3. 가정하는 내용이 있다면 명시하세요
```

### missing_context
```
필요한 컨텍스트 정보가 부족합니다.
지식베이스 검색 결과:
{kb_results}

위 정보를 활용하여 태스크를 수행하세요.
```

### dependency_failure
```
선행 태스크의 결과를 사용할 수 없습니다.
다음 방식으로 진행하세요:
1. 독립적으로 수행 가능한 부분만 진행하세요
2. 의존성이 필요한 부분은 명확히 표시하세요
3. 완료 후 추가 정보 필요 여부를 명시하세요
```

### agent_hallucination
```
출력에 검증되지 않은 정보가 포함될 수 있습니다.
다음 기준을 반드시 준수하세요:
1. 모든 수치에 출처를 표시하세요
2. 확실하지 않은 정보는 명확히 표시하세요 (예: "추정", "가정")
3. 검증 가능한 사실만 단언하세요
```

---

## ⚠️ EDGE_CASE 처리 (P02-v2-C 패치)

```
EDGE_CASE: recovery_plan 비어있음
  처리: P-01 재실행 요청 → ABORT 플래그 발행
  메시지: "P-02 ABORT: recovery_plan is empty — re-trigger P-01"

EDGE_CASE: kb_results 비어있음 (missing_context 전용)
  처리: 외부 KB 검색 없이 원본 프롬프트만 재실행
  경고: "KB_EMPTY — proceeding without supplemental context"

EDGE_CASE: 동일 error_type 3회 연속 복구 실패
  처리: 에스컬레이션 플래그 설정 → 인간 검토 요청
  메시지: "ESCALATE: Recovery loop exceeded 3 attempts"
```

---

## 파라미터 정의

| 변수 | 설명 | 타입 |
|---|---|---|
| `{recovery_plan}` | 에러 유형에 따른 복구 지침 | string |
| `{original_prompt}` | 원래 에이전트 프롬프트 | string |
| `{kb_results}` | 지식베이스 검색 결과 (missing_context 전용) | string |
| `{error_type}` | P-01이 감지한 ErrorType | string |
| `{evidence}` | P-01 EVIDENCE 필드 값 | string |

---

## 버전 이력

| 버전 | 날짜 | 변경 내용 | PE-3 점수 |
|---|---|---|---|
| **v2.0** | **2026-04-27** | **P02-v2-A: SOURCE_ERROR_TYPE+EVIDENCE 필드 추가 (추적성 +5) · P02-v2-B: 3-Engine 연계 블록 추가 (PE 일관성 +6) · P02-v2-C: EDGE_CASE 핸들러 3종 추가 (명확성 +4)** | **91/100** |
| v1.0 | 2026-04-26 | 최초 생성 | 76/100 |
