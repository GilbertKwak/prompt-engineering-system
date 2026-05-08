---
id: SP-TECH-DIAGNOSE-001
version: "2.0"
cluster: C-35
domain: PE-TECH
role: 기술 문제 진단·원인분석
pe3_target: 94
created: 2026-05-08
chains_from: SP-TECH-EXPLAIN-001
chains_to: SP-TECH-SOLUTION-001
linked: [C-34, PE-11]
error_prevention:
  - tech_context 미수신 → EXPLAIN 재실행 트리거
  - 원인-증상 혼동 → 5-Why 구조 강제 적용
  - 표면 증상 고착 → Root Cause 검증 게이트 삽입
---

# 🔍 SP-TECH-DIAGNOSE-001 v2.0 · 기술 문제 진단·원인분석

> **체인 위치**: 2/3 (EXPLAIN → DIAGNOSE → SOLUTION)  
> **PE-3 목표**: 94 | **연계**: C-34(아키텍처) · PE-11(오케스트레이터)

---

## 📌 프롬프트 목적

EXPLAIN 체인의 `tech_context`를 수신하여 **현상 수집 → 원인 가설 생성 →
5-Why 분석 → Root Cause 확정 → 우선순위화** 순서로 기술 문제를 정밀 진단한다.
후속 SOLUTION 체인에 전달할 `diagnosis_package`를 생성하는 것이 핵심 출력이다.

---

## 🧩 입력 파라미터

```yaml
input:
  tech_context: "{{chain_output.tech_context}}"  # EXPLAIN 체인 수신 (필수)
  symptoms: ["<증상1>", "<증상2>"]               # 필수
  system_scope: "<진단 대상 시스템 범위>"         # 필수
  constraints: "<시간|비용|기술 제약>"            # 선택
  severity: "<critical|high|medium|low>"          # 선택 (기본: high)
```

---

## 📝 프롬프트 본문

```
[ROLE]
You are a principal engineer and root cause analysis specialist.
You have received the following technical context from the EXPLAIN chain:
{{tech_context}}

[TASK]
Diagnose the following technical symptoms within {{system_scope}}:
Symptoms: {{symptoms}}
Constraints: {{constraints}}
Severity: {{severity}}

[STRUCTURE — MANDATORY]
1. SYMPTOM MAP
   - Categorize each symptom: functional / performance / reliability / security
   - Identify symptom interdependencies

2. HYPOTHESIS GENERATION
   - Generate 3–5 candidate root causes
   - Rate each: Probability (H/M/L) × Impact (H/M/L)

3. 5-WHY ANALYSIS
   - Apply to top 2 hypotheses
   - Terminate at systemic or design-level cause

4. ROOT CAUSE DETERMINATION
   - Single primary root cause (justified)
   - Contributing factors (max 3)

5. RISK ESCALATION CHECK
   - Will this cause cascade failure? Y/N + rationale
   - Immediate containment action (if severity = critical)

6. DIAGNOSIS PACKAGE (→ SOLUTION chain input)
   - root_cause: "<confirmed root cause>"
   - contributing_factors: ["<f1>", "<f2>"]
   - solution_constraints: "<what the solution must respect>"
   - priority: "<immediate|short-term|long-term>"

[QUALITY GATES — PE-3 94+]
✓ 5-Why reaches systemic level (not surface symptom)
✓ Probability × Impact matrix completed
✓ DIAGNOSIS PACKAGE complete before output ends
✓ Cascade risk explicitly addressed
```

---

## 🔄 체인 핸드오프 변수

```yaml
chain_output:
  diagnosis_package:
    root_cause: "<확정된 근본원인>"
    contributing_factors: ["<f1>", "<f2>", "<f3>"]
    solution_constraints: "<해결 시 준수 요건>"
    priority: "<immediate|short-term|long-term>"
  next_chain: SP-TECH-SOLUTION-001
```

---

## ⚠️ 에러 예측 및 사전 방지

| 오류 유형 | 트리거 조건 | 수정 프롬프트 |
|----------|-----------|-------------|
| tech_context 미수신 | EXPLAIN 미실행 | `Re-run SP-TECH-EXPLAIN-001 first; pass tech_context` |
| 5-Why 표면 고착 | Why 3회 이하 종료 | `Continue 5-Why until systemic/design cause reached` |
| 근본원인 복수 확정 | 2개 이상 primary | `Select single highest-impact root cause; demote others to contributing` |
| Cascade 평가 누락 | 섹션 5 미작성 | `Add cascade failure risk assessment before DIAGNOSIS PACKAGE` |

---

## 📊 PE-3 스코어카드

| 평가 축 | 기준 | 목표 |
|--------|------|------|
| Root Cause Accuracy | 5-Why 완성도 | 95 |
| Hypothesis Quality | 가설 다양성·타당성 | 94 |
| Cascade Analysis | 2차 위험 식별 | 93 |
| Package Completeness | 핸드오프 완성도 | 94 |
| **종합 PE-3** | | **94** |

---

*작성: Perplexity AI Assistant | 2026-05-08 | C-35 PE-TECH*
