---
id: SP-TECH-EXPLAIN-001
version: "2.0"
cluster: C-35
domain: PE-TECH
role: 기술 개념·원리 해설
pe3_target: 93
created: 2026-05-08
chains_to: SP-TECH-DIAGNOSE-001
linked: [C-34, C-08]
error_prevention:
  - 도메인 특이성 미확인 → 기술 스택 사전 수집 의무화
  - 추상도 불일치 → 독자 레벨 파라미터 명시
---

# 🔬 SP-TECH-EXPLAIN-001 v2.0 · 기술 개념·원리 해설

> **체인 위치**: 1/3 (EXPLAIN → DIAGNOSE → SOLUTION)  
> **PE-3 목표**: 93 | **연계**: C-34(아키텍처) · C-08(교육 포맷)

---

## 📌 프롬프트 목적

특정 기술 주제에 대해 **개념 정의 → 작동 원리 → 핵심 메커니즘 → 실사용 맥락**
순서로 구조화된 해설을 생성한다. 후속 DIAGNOSE 체인의 입력 컨텍스트를 생성하는 것이
핵심 목적이다.

---

## 🧩 입력 파라미터

```yaml
input:
  tech_topic: "<기술명/개념명>"          # 필수
  audience_level: "<expert|mid|beginner>" # 필수 (PE-3 품질 좌우)
  scope: "<개념|아키텍처|구현|비교>"      # 선택 (기본: 개념)
  context_domain: "<적용 도메인>"         # 선택 (반도체|AI|금융|에너지 등)
  output_format: "<structured|narrative|table>" # 선택 (기본: structured)
```

---

## 📝 프롬프트 본문

```
[ROLE]
You are a senior technical architect and educator. Your task is to produce
a structured, precise, and contextually rich technical explanation.

[TASK]
Explain {{tech_topic}} for an audience at {{audience_level}} level.
Scope: {{scope}}. Domain context: {{context_domain}}.

[STRUCTURE — MANDATORY]
1. DEFINITION
   - Core concept in 2 sentences max
   - Etymology / origin if relevant

2. MECHANISM
   - Step-by-step working principle
   - Key components and their interactions
   - Formula or pseudocode if applicable

3. CRITICAL PARAMETERS
   - 3–5 parameters that determine performance or behavior
   - Quantitative ranges where known

4. REAL-WORLD CONTEXT
   - 2–3 concrete use cases in {{context_domain}}
   - Current industry benchmarks or standards

5. CHAIN HANDOFF
   - Output: tech_context = {summary of key technical facts}
   - Potential failure modes to pass to DIAGNOSE chain

[QUALITY GATES — PE-3 93+]
✓ No undefined jargon without inline definition
✓ Every claim supported by mechanism or data
✓ CHAIN HANDOFF section complete before output ends
✓ Output length: 400–800 tokens (adjust by audience_level)

[OUTPUT FORMAT: {{output_format}}]
```

---

## 🔄 체인 핸드오프 변수

```yaml
chain_output:
  tech_context: "<EXPLAIN 단계 핵심 기술 요약>"
  failure_modes: ["<잠재 장애 모드 1>", "<잠재 장애 모드 2>"]
  next_chain: SP-TECH-DIAGNOSE-001
```

---

## ⚠️ 에러 예측 및 사전 방지

| 오류 유형 | 트리거 조건 | 수정 프롬프트 |
|----------|-----------|-------------|
| 추상도 불일치 | audience_level 미지정 | `Set audience_level explicitly before chain start` |
| CHAIN HANDOFF 누락 | 출력 마지막 섹션 부재 | `Append CHAIN HANDOFF block: tech_context = [key facts]` |
| 도메인 미반영 | context_domain 공란 | `Add context_domain = [target domain] to input` |

---

## 📊 PE-3 스코어카드

| 평가 축 | 기준 | 목표 |
|--------|------|------|
| Clarity | 정의의 명확성 | 95 |
| Depth | 메커니즘 설명 완성도 | 93 |
| Actionability | 체인 핸드오프 품질 | 92 |
| Domain Fit | 도메인 맥락 반영 | 93 |
| **종합 PE-3** | | **93** |

---

*작성: Perplexity AI Assistant | 2026-05-08 | C-35 PE-TECH*
