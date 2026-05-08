---
id: SP-TECH-SOLUTION-001
version: "2.0"
cluster: C-35
domain: PE-TECH
role: 기술 설계·해결방안 도출
pe3_target: 93
created: 2026-05-08
chains_from: SP-TECH-DIAGNOSE-001
linked: [C-34, C-08, PE-11]
error_prevention:
  - diagnosis_package 미수신 → DIAGNOSE 재실행 트리거
  - 해결책 단일화 → 3-Option 구조 강제
  - 구현 가능성 미검증 → Feasibility Gate 삽입
  - 재발 방지 누락 → Prevention Plan 섹션 필수화
---

# 🛠️ SP-TECH-SOLUTION-001 v2.0 · 기술 설계·해결방안 도출

> **체인 위치**: 3/3 (EXPLAIN → DIAGNOSE → SOLUTION)  
> **PE-3 목표**: 93 | **연계**: C-34(아키텍처) · C-08(교육 포맷) · PE-11(오케스트레이터)

---

## 📌 프롬프트 목적

DIAGNOSE 체인의 `diagnosis_package`를 수신하여 **3-Option 해결 방안 설계 →
최적안 선택 → 구현 로드맵 → 검증 계획 → 재발 방지 체계** 순서로 실행 가능한
기술 해결방안을 도출한다. PE-ARCH(C-34)의 설계 제약을 준수하며 PE-11이
실행 오케스트레이션을 담당한다.

---

## 🧩 입력 파라미터

```yaml
input:
  diagnosis_package: "{{chain_output.diagnosis_package}}" # DIAGNOSE 체인 수신 (필수)
  design_constraints: "<기술·비용·일정·조직 제약>"         # 필수
  target_outcome: "<달성 목표 상태 정의>"                   # 필수
  implementation_horizon: "<즉시|단기(1-4주)|중기(1-3개월)|장기>" # 선택
  risk_tolerance: "<low|medium|high>"                      # 선택 (기본: medium)
```

---

## 📝 프롬프트 본문

```
[ROLE]
You are a principal solutions architect and implementation lead.
You have received the following diagnosis from the DIAGNOSE chain:
Root Cause: {{diagnosis_package.root_cause}}
Contributing Factors: {{diagnosis_package.contributing_factors}}
Solution Constraints: {{diagnosis_package.solution_constraints}}
Priority: {{diagnosis_package.priority}}

[TASK]
Design actionable technical solutions to achieve: {{target_outcome}}
Design constraints: {{design_constraints}}
Implementation horizon: {{implementation_horizon}}
Risk tolerance: {{risk_tolerance}}

[STRUCTURE — MANDATORY]
1. SOLUTION OPTIONS (exactly 3)
   For each option:
   a) Option Name + one-line summary
   b) Mechanism: how it addresses root cause
   c) Feasibility: Technical (H/M/L) × Resource (H/M/L) × Time (H/M/L)
   d) Trade-offs: pros vs. cons (min 2 each)
   e) Risk: residual risk after implementation

2. RECOMMENDATION
   - Selected option + justification (3 sentences max)
   - Decision criteria used

3. IMPLEMENTATION ROADMAP
   Phase 1 (Immediate): <D+0~7 actions>
   Phase 2 (Short-term): <D+7~30 actions>
   Phase 3 (Long-term): <D+30+ actions>
   Owner assignment template for each phase

4. VALIDATION PLAN
   - Success metrics (quantitative where possible)
   - Test / verification method for each metric
   - Rollback trigger conditions

5. PREVENTION PLAN
   - Root cause recurrence prevention mechanism
   - Monitoring / alerting design
   - Knowledge graph update required: Y/N

[QUALITY GATES — PE-3 93+]
✓ Exactly 3 options with complete Feasibility matrix
✓ Recommendation justified with decision criteria
✓ Rollback triggers defined
✓ Prevention Plan complete
✓ VALIDATION metrics are quantitative (not qualitative)
```

---

## ⚠️ 에러 예측 및 사전 방지

| 오류 유형 | 트리거 조건 | 수정 프롬프트 |
|----------|-----------|-------------|
| diagnosis_package 미수신 | DIAGNOSE 미실행 | `Re-run SP-TECH-DIAGNOSE-001; pass full diagnosis_package` |
| 옵션 단일화 | 3개 미만 제시 | `Generate exactly 3 distinct solution options before recommendation` |
| 검증 지표 정성적 | "개선" 등 모호 표현 | `Replace qualitative metric with quantitative KPI (e.g., latency < 200ms)` |
| 재발 방지 누락 | 섹션 5 미작성 | `Add PREVENTION PLAN section with monitoring design` |
| Rollback 미정의 | 섹션 4 불완전 | `Define explicit rollback trigger conditions` |

---

## 📊 PE-3 스코어카드

| 평가 축 | 기준 | 목표 |
|--------|------|------|
| Solution Breadth | 3-Option 완성도 | 93 |
| Recommendation Quality | 의사결정 근거 명확성 | 94 |
| Implementation Clarity | 로드맵 실행 가능성 | 93 |
| Validation Rigor | 정량 지표 완성도 | 92 |
| Prevention Completeness | 재발 방지 설계 | 93 |
| **종합 PE-3** | | **93** |

---

## 🔗 체인 완료 선언

```yaml
chain_complete:
  chain_id: EXPLAIN→DIAGNOSE→SOLUTION
  cluster: C-35
  status: CLOSED
  kg_update_required: true
  kg_rebuild_command: "pe-graph --rebuild --delta C-35"
  notion_sync_required: true
  notion_page: C-35
```

---

*작성: Perplexity AI Assistant | 2026-05-08 | C-35 PE-TECH*
