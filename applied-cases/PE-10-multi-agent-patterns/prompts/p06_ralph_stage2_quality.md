# P-06 · Ralph Loop Stage 2 Quality Check Prompt

> **버전**: v2.0 | **생성일**: 2026-04-26 | **업그레이드**: 2026-04-27
> **파일**: `scripts/ralph_loop_2stage.py` → `review_stage2_quality()` 메서드
> **모델**: claude-4-sonnet-20250514 | **Temperature**: `0.0` | **Max Tokens**: `3,000`
> **역할**: 4개 차원(정확성/완전성/명확성/실용성) 품질 검증 및 SHIP/ITERATE 판정
> **PE-3 점수**: v1.0 → 82/100 ⚠️ · v2.0 → 94/100 ✅

---

## 🔗 3-Engine 연계 (P06-v2-B 패치)

| 엔진 | 역할 | 연계 지점 |
|------|------|----------|
| **PE-1 자동개선** | ITERATE 판정 시 에이전트 재작성 | decision=ITERATE → PE-1 루프 |
| **PE-3 자동검증** | Stage 2 출력 자체 품질 메타채점 | SHIP 판정 후 PE-3 최종 확인 |
| **P-05 → P-06** | Stage 1 PASS → Stage 2 진입 | compliance_score ≥ 0.8 시 자동 호출 |

```
[P-05 PASS]
        ↓
┌──────────────────────────┐
│  P-06: Quality Check     │  ← 본 프롬프트
│  Temperature: 0.0        │
│  판정: SHIP / ITERATE     │
└──────────┬───────────────┘
     SHIP  ↓        ↓ ITERATE (max 3회)
[최종 출력 확정]  [PE-1 재작성 루프]
```

---

## 프롬프트 원문

```
다음 에이전트 출력의 품질을 검증하세요.

<task_description>{task_description}</task_description>
<agent_output>{agent_output}</agent_output>
<p05_compliance_score>{compliance_score}</p05_compliance_score>

Stage 2: Quality Check — 4개 차원 평가

1. 정확성 (Accuracy)
   - 사실 관계 정확성 / 데이터 검증 가능 여부 / 오류·모순 여부
   - 각 issue에 agent_output 직접 인용 필수

2. 완전성 (Completeness)
   - 충분한 상세도 / 중요 측면 누락 여부 / 맥락 충분성

3. 명확성 (Clarity)
   - 이해 용이성 / 논리적 구조 / 전문용어 설명

4. 실용성 (Actionability)
   - 실행 가능한 인사이트 / 의사결정 지원 / 구체적 권장사항

출력 형식: YAML
(stage2_result / quality_score / dimensions[4개+evidence] / overall_assessment / decision: SHIP|ITERATE / iteration_guidance / iteration_count)
```

> **v2.0 추가**: `p05_compliance_score` 입력 컨텍스트 + `iteration_count` 추적 + 각 dimension issues에 `evidence` 서브필드 필수화 (P06-v2-A 패치)

---

## 출력 YAML 스키마

```yaml
stage2_result: PASS | FAIL
quality_score: float  # 0.0 ~ 1.0
dimensions:
  accuracy:
    score: float
    issues:
      - text: string
        evidence: string    # v2.0 신규
  completeness:
    score: float
    issues:
      - text: string
        evidence: string
  clarity:
    score: float
    issues:
      - text: string
        evidence: string
  actionability:
    score: float
    issues:
      - text: string
        evidence: string
overall_assessment: string
decision: SHIP | ITERATE
iteration_guidance:
  - string
iteration_count: int       # v2.0 신규 — 현재 반복 횟수 추적
```

## 판정 기준
- **SHIP**: quality_score ≥ 0.75 AND decision = SHIP
- **ITERATE**: quality_score < 0.75 OR decision = ITERATE → 최대 3회 반복
- **최대 반복 초과**: 경고 플래그 설정 후 현재 상태로 SHIP

---

## ⚠️ EDGE_CASE 처리 (P06-v2-C 패치)

```
EDGE_CASE: iteration_count ≥ 3 AND decision = ITERATE
  처리: decision 강제 SHIP + 경고 플래그
  메시지: "MAX_ITER_EXCEEDED: Forced SHIP after 3 iterations"

EDGE_CASE: quality_score ≥ 0.75 AND accuracy.score < 0.5
  처리: decision = ITERATE 강제 (정확성 임계값 우선)
  메시지: "ACCURACY_OVERRIDE: Low accuracy score blocks SHIP"

EDGE_CASE: p05_compliance_score < 0.5 (Stage 1 약통과)
  처리: quality_score에 -0.1 페널티 자동 적용
  경고: "LOW_STAGE1_PENALTY: compliance_score below 0.5"
```

---

## 버전 이력

| 버전 | 날짜 | 변경 내용 | PE-3 점수 |
|---|---|---|---|
| **v2.0** | **2026-04-27** | **P06-v2-A: evidence 서브필드+iteration_count+p05 컨텍스트 추가 (추적성 +5) · P06-v2-B: 3-Engine 연계 블록 추가 (PE 일관성 +5) · P06-v2-C: EDGE_CASE 핸들러 3종 추가 (명확성 +2)** | **94/100** |
| v1.0 | 2026-04-26 | 최초 생성 | 82/100 |
