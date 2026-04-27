# P-08 · Recursive Leaf Task Execution Prompt

> **버전**: v2.0 | **생성일**: 2026-04-26 | **업그레이드**: 2026-04-27
> **파일**: `agents/patent_agent/recursive_delegation.py` → `_execute_leaf_task()` 메서드
> **모델**: claude-4-sonnet-20250514 | **Temperature**: `0.3` | **Max Tokens**: `3,000`
> **역할**: 분해 불가능한 최소 단위(Leaf) 태스크 실행
> **PE-3 점수**: v1.0 → 76/100 ⚠️ · v2.0 → 91/100 ✅

---

## 🔗 3-Engine 연계 (P08-v2-B 패치)

| 엔진 | 역할 | 연계 지점 |
|------|------|----------|
| **PE-1 자동개선** | Leaf 출력 품질 미달 시 재실행 | 핵심 발견사항 < 2개 시 PE-1 트리거 |
| **PE-3 자동검증** | Leaf 출력 5차원 채점 | 실행 완료 후 PE-3 자동 채점 |
| **P-09 통합** | Leaf 결과 → P-09 통합 입력 | 모든 Leaf 완료 후 P-09 호출 |

```
[P-07 분해 완료 / NO_DECOMPOSITION]
        ↓
┌──────────────────────────┐
│  P-08: Leaf 실행          │  ← 본 프롬프트 (병렬 N개 동시 실행)
│  Temperature: 0.3        │
└──────────┬───────────────┘
           ↓ 모든 Leaf 완료
┌──────────────────────────┐
│  P-09: 결과 통합          │
└──────────────────────────┘
```

---

## 프롬프트 원문

```
다음 특허 분석 태스크를 수행하세요.

<task>{task}</task>
<leaf_id>{leaf_id}</leaf_id>
<parent_task>{parent_task}</parent_task>

요구사항:
1. 구체적인 증거 제시
2. 정량적 데이터 포함
3. 출처 명시
4. 간결하고 명확한 결론

답변 형식:
분석 내용: [상세 분석]
핵심 발견사항: [bullet list — 최소 2개]
증거: [출처 포함]
결론: [한 문장]
LEAF_TRACE: [leaf_id] | [parent_task 요약 20자 이내]
```

> **v2.0 추가**: `leaf_id` · `parent_task` 입력 파라미터 + `LEAF_TRACE` 출력 필드 신규 — 병렬 실행된 Leaf의 계보를 P-09 통합 시 추적 가능하게 함 (P08-v2-A 패치)

---

## 활용 도메인

본 프롬프트는 특허 분석에서 시작하였으나 다음 도메인에 범용 적용 가능:
- 반도체 기술 분석
- 시장 조사 세부 항목
- 재무 데이터 분석
- 기술 문서 검토

도메인 변경 시 `<task>` 내 컨텍스트만 교체하여 재사용.

---

## ⚠️ EDGE_CASE 처리 (P08-v2-C 패치)

```
EDGE_CASE: 핵심 발견사항 < 2개 생성
  처리: PE-1 자동개선 트리거
  메시지: "LEAF_RETRY: Insufficient findings — PE-1 rerun"

EDGE_CASE: 증거 출처 0건
  처리: agent_hallucination 위험 플래그 → P-01 재감지 요청
  메시지: "HALLUCINATION_RISK: No evidence sources cited"

EDGE_CASE: leaf_id 중복 감지 (동일 Leaf 재실행)
  처리: 캐시 결과 반환 (재계산 방지)
  메시지: "LEAF_CACHED: Returning existing result for [leaf_id]"
```

---

## 버전 이력

| 버전 | 날짜 | 변경 내용 | PE-3 점수 |
|---|---|---|---|
| **v2.0** | **2026-04-27** | **P08-v2-A: leaf_id+parent_task+LEAF_TRACE 추가 (추적성 +5) · P08-v2-B: 3-Engine 연계 블록 추가 (PE 일관성 +6) · P08-v2-C: EDGE_CASE 핸들러 3종 추가 (명확성 +4)** | **91/100** |
| v1.0 | 2026-04-26 | 최초 생성 | 76/100 |
