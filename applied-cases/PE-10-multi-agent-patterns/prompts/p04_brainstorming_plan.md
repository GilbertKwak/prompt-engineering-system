# P-04 · Brainstorming Plan Generation Prompt

> **버전**: v2.0 | **생성일**: 2026-04-26 | **업그레이드**: 2026-04-27
> **파일**: `scripts/brainstorming.py` → `generate_plan_outline()` 메서드
> **모델**: claude-4-sonnet-20250514 | **Temperature**: `0.3` | **Max Tokens**: `4,000`
> **역할**: P-03 정제 요구사항 기반 단계별 실행 계획 YAML 생성
> **PE-3 점수**: v1.0 → 75/100 ⚠️ · v2.0 → 90/100 ✅

---

## 🔗 3-Engine 연계 (P04-v2-B 패치)

| 엔진 | 역할 | 연계 지점 |
|------|------|----------|
| **PE-1 자동개선** | 계획 품질 미달 시 재작성 | YAML quality_score < 0.7 시 PE-1 트리거 |
| **PE-3 자동검증** | 계획 YAML 5차원 채점 | 출력 후 PE-3 자동 검증 |
| **P-03 → P-04** | 정제 요구사항 → 계획 생성 | P-03 YAML이 본 프롬프트 입력 |

```
[P-03 refined_requirements YAML]
        ↓
┌──────────────────────────┐
│  P-04: 실행 계획 생성     │  ← 본 프롬프트
│  Temperature: 0.3        │
│  출력: plan YAML          │
└──────────┬───────────────┘
           ↓ ambiguities 처리
[P-05/P-07 Ralph/Recursive 패턴으로 진입]
```

---

## 프롬프트 원문

```
다음 요구사항에 대한 실행 계획을 작성하세요.

<requirements>{yaml.dump(refined_requirements)}</requirements>

각 단계를 2-5분 단위의 구체적 작업으로 분해하세요.

요구사항 내 ambiguities 항목이 있다면 각 phase에 리스크 플래그를 포함하세요.

출력 형식: YAML
(plan[phase/duration_estimate/tasks/risk_flags] / dependencies / total_estimate / confidence_score)
```

> **v2.0 추가**: `risk_flags` 및 `confidence_score` 필드 신규 — P-03 ambiguities를 계획 단계별 리스크로 변환, 계획 신뢰도 정량화 (P04-v2-A 패치)

---

## 출력 YAML 스키마

```yaml
plan:
  - phase: string
    duration_estimate: string
    tasks:
      - string
    risk_flags:        # v2.0 신규
      - string
dependencies:
  - string
total_estimate: string
confidence_score: float   # v2.0 신규 — 0.0~1.0
```

---

## ⚠️ EDGE_CASE 처리 (P04-v2-C 패치)

```
EDGE_CASE: refined_requirements.ambiguities HIGH 항목 ≥ 3개
  처리: plan 생성 전 경고 발행
  경고: "HIGH_RISK_PLAN: 3+ critical ambiguities unresolved"
  confidence_score: 자동 상한 0.6

EDGE_CASE: total_estimate > 60분
  처리: 자동 단계 분할 권고 (P-07 Recursive 패턴 전환 제안)
  risk_flags: ["SCOPE_OVERRUN — consider P-07 decomposition"]

EDGE_CASE: dependencies 순환 참조 감지
  처리: YAML에 [CIRCULAR_DEP] 태그 부착 후 순환 경로 명시
  조치: 순환 해소 방안 recommendations 필드에 추가
```

---

## 버전 이력

| 버전 | 날짜 | 변경 내용 | PE-3 점수 |
|---|---|---|---|
| **v2.0** | **2026-04-27** | **P04-v2-A: risk_flags+confidence_score 필드 추가 (추적성 +5) · P04-v2-B: 3-Engine 연계 블록 추가 (PE 일관성 +6) · P04-v2-C: EDGE_CASE 핸들러 3종 추가 (명확성 +4)** | **90/100** |
| v1.0 | 2026-04-26 | 최초 생성 | 75/100 |
