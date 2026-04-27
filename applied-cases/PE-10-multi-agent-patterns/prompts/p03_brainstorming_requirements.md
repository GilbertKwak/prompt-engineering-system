# P-03 · Brainstorming Requirements Clarification Prompt

> **버전**: v2.0 | **생성일**: 2026-04-26 | **업그레이드**: 2026-04-27
> **파일**: `scripts/brainstorming.py` → `refine_requirements()` 메서드
> **모델**: claude-4-sonnet-20250514 | **Temperature**: `0.3` | **Max Tokens**: `4,000`
> **역할**: 사용자 요청을 구조화된 YAML 요구사항으로 정제
> **PE-3 점수**: v1.0 → 78/100 ⚠️ · v2.0 → 92/100 ✅

---

## 🔗 3-Engine 연계 (P03-v2-B 패치)

| 엔진 | 역할 | 연계 지점 |
|------|------|----------|
| **PE-1 자동개선** | 요구사항 정제 재루프 | YAML 품질 미달 시 PE-1 재실행 |
| **PE-3 자동검증** | 정제 결과 5차원 채점 | YAML 출력 후 PE-3 자동 트리거 |
| **P-04 연계** | 정제 완료 → 계획 생성 | P-03 YAML → P-04 입력으로 전달 |

```
[사용자 원본 요청]
        ↓
┌──────────────────────────┐
│  P-03: 요구사항 정제      │  ← 본 프롬프트
│  Temperature: 0.3        │
│  출력: YAML              │
└──────────┬───────────────┘
           ↓ refined_requirements
┌──────────────────────────┐
│  P-04: 실행 계획 생성     │
└──────────────────────────┘
```

---

## 프롬프트 원문

```
다음 요청을 분석하여 명확하고 구체적인 요구사항으로 refinement하세요.

<user_request>{user_request}</user_request>

다음 기준으로 검토하세요:

1. 범위 명확성
   - 시간 범위가 명시되어 있는가?
   - 지역/시장이 구체적인가?
   - 산업/제품이 명확한가?

2. 측정 가능성
   - 정량적 목표가 있는가?
   - 성공 기준이 명확한가?

3. 실행 가능성
   - 현실적으로 달성 가능한가?
   - 필요한 데이터 접근 가능한가?

4. 완전성
   - 누락된 중요 요소는 없는가?
   - 암묵적 가정은 없는가?

출력 형식: YAML
(refined_request / scope / objectives / assumptions / constraints / success_criteria / ambiguities)

ambiguities: 정제 과정에서 발견된 불명확 항목 — 후속 명확화 요청 목록
```

> **v2.0 추가**: `ambiguities` 필드 신규 — 정제 과정 불명확 항목을 추적하여 P-04 계획 생성 시 리스크 사전 식별 (P03-v2-A 패치)

---

## 출력 YAML 스키마

```yaml
refined_request: string
scope:
  time_range: string
  geography: string
  industry: string
objectives:
  - string
assumptions:
  - string
constraints:
  - string
success_criteria:
  - string
ambiguities:          # v2.0 신규
  - item: string
    impact: HIGH | MEDIUM | LOW
    suggested_resolution: string
```

---

## ⚠️ EDGE_CASE 처리 (P03-v2-C 패치)

```
EDGE_CASE: user_request 길이 < 20자
  처리: ambiguities에 "요청이 너무 짧음" HIGH 등록 후 정제 진행
  YAML: refined_request에 원문 그대로 유지, scope 전체 null

EDGE_CASE: 시간 범위 완전 미명시
  처리: scope.time_range = "미지정 — 명확화 필요"
  ambiguities: item 자동 추가 (impact: HIGH)

EDGE_CASE: 상충하는 constraints 감지
  처리: constraints 항목에 [CONFLICT] 태그 부착
  ambiguities: 충돌 쌍 명시 후 해결 방안 제시
```

---

## 버전 이력

| 버전 | 날짜 | 변경 내용 | PE-3 점수 |
|---|---|---|---|
| **v2.0** | **2026-04-27** | **P03-v2-A: ambiguities 필드 추가 (추적성 +5) · P03-v2-B: 3-Engine 연계 블록 추가 (PE 일관성 +5) · P03-v2-C: EDGE_CASE 핸들러 3종 추가 (명확성 +4)** | **92/100** |
| v1.0 | 2026-04-26 | 최초 생성 | 78/100 |
