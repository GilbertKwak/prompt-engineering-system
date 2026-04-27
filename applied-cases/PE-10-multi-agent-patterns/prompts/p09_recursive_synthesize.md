# P-09 · Recursive Result Synthesis Prompt

> **버전**: v2.0 | **생성일**: 2026-04-26 | **업그레이드**: 2026-04-27
> **파일**: `agents/patent_agent/recursive_delegation.py` → `_synthesize_results()` 메서드
> **모델**: claude-4-sonnet-20250514 | **Temperature**: `0.3` | **Max Tokens**: `4,000`
> **역할**: 병렬 실행된 서브태스크 결과들을 통합하여 원래 태스크 최종 답변 생성
> **PE-3 점수**: v1.0 → 79/100 ⚠️ · v2.0 → 93/100 ✅

---

## 🔗 3-Engine 연계 (P09-v2-B 패치)

| 엔진 | 역할 | 연계 지점 |
|------|------|----------|
| **PE-1 자동개선** | 통합 품질 미달 시 재통합 | synthesis_confidence < 0.7 시 PE-1 트리거 |
| **PE-3 자동검증** | 통합 결과 최종 5차원 채점 | P-09 출력 → PE-3 파이프라인 최종 관문 |
| **P-08 → P-09** | Leaf 결과 → 통합 | 모든 P-08 Leaf 완료 후 자동 호출 |

```
[P-08 Leaf 결과 N개 (병렬 완료)]
        ↓
┌──────────────────────────┐
│  P-09: 결과 통합          │  ← 본 프롬프트
│  Temperature: 0.3        │
│  LEAF_TRACE 추적          │
└──────────┬───────────────┘
           ↓ synthesis_confidence ≥ 0.7
[PE-3 최종 채점 → 출력 확정]
```

---

## 프롬프트 원문

```
다음 서브태스크 결과들을 통합하여 원래 태스크에 대한 종합 분석을 작성하세요.

<original_task>{original_task}</original_task>

<subtask_results>
=== Subtask 1 === {result_1} [LEAF_TRACE: {leaf_trace_1}]
=== Subtask 2 === {result_2} [LEAF_TRACE: {leaf_trace_2}]
=== Subtask 3 === {result_3} [LEAF_TRACE: {leaf_trace_3}]
</subtask_results>

통합 요구사항:
1. 모든 서브태스크 결과를 포괄
2. 중복 제거
3. 일관된 서술
4. 핵심 인사이트 도출
5. 실행 가능한 권장사항
6. LEAF_TRACE를 활용하여 각 인사이트의 출처 Leaf를 명시

답변 형식:
종합 분석 / 핵심 인사이트(3개+출처 Leaf ID) / 권장사항(2개) / 종합 결론(1문장) / synthesis_confidence(0.0~1.0)
```

> **v2.0 추가**: `LEAF_TRACE` 입력 컨텍스트 + 인사이트별 출처 Leaf ID 명시 + `synthesis_confidence` 출력 필드 — 통합 신뢰도 정량화 및 근거 추적 (P09-v2-A 패치)

---

## 통합 전략

| 상황 | 처리 방법 |
|---|---|
| 서브태스크 결과 충돌 | 더 구체적 증거를 가진 결과 우선 채택, 충돌 명시 |
| 서브태스크 결과 누락 | 가용 결과만으로 통합, 누락 항목 명시 |
| 결과 간 중복 | 중복 제거 후 핵심만 유지 |

---

## ⚠️ EDGE_CASE 처리 (P09-v2-C 패치)

```
EDGE_CASE: 서브태스크 결과 1개만 존재
  처리: 통합 없이 단일 결과 직접 출력
  synthesis_confidence: 단일 결과 confidence 그대로 사용
  경고: "SINGLE_LEAF_SYNTHESIS: No cross-validation possible"

EDGE_CASE: 서브태스크 결과 충돌 (핵심 수치 불일치)
  처리: 충돌 쌍을 종합 분석에 명시 + synthesis_confidence -0.15 패널티
  메시지: "CONFLICT_DETECTED: [leaf_id_A] vs [leaf_id_B] — [수치/주장]"

EDGE_CASE: synthesis_confidence < 0.7
  처리: PE-1 자동개선 루프 트리거
  메시지: "LOW_CONFIDENCE_SYNTHESIS: PE-1 rerun recommended"
```

---

## 버전 이력

| 버전 | 날짜 | 변경 내용 | PE-3 점수 |
|---|---|---|---|
| **v2.0** | **2026-04-27** | **P09-v2-A: LEAF_TRACE+synthesis_confidence+인사이트 출처 추가 (추적성 +5) · P09-v2-B: 3-Engine 연계 블록 추가 (PE 일관성 +6) · P09-v2-C: EDGE_CASE 핸들러 3종 추가 (명확성 +3)** | **93/100** |
| v1.0 | 2026-04-26 | 최초 생성 | 79/100 |
