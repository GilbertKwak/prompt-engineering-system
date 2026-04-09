# PE-1 자동개선 엔진 — v1.4 업그레이드

> 버전: v1.4 | 날짜: 2026-04-10 | 관리자: Gilbert Kwak

---

## 📌 v1.4 업그레이드 내용

### 핵심 변경사항

| 항목 | v1.3 | v1.4 |
|------|------|------|
| 약점 탐지 방식 | 키워드 기반 스캔 | Chain-of-Thought 구조 분해 탐지 |
| 재작성 루프 | 단순 반복 (max 3회) | 약점 유형별 분기 재작성 |
| 출력 포맷 | Markdown 자유 형식 | XML 구조화 출력 |
| 자가 점검 | 없음 | 재작성 후 품질 사전 스캔 |

---

## 🔁 업그레이드 프롬프트 템플릿

```xml
<SYSTEM>
당신은 PE-1 자동개선 엔진(v1.4)입니다.
Chain-of-Thought 구조 분해 방식으로 프롬프트 약점을 탐지하고 재작성합니다.
</SYSTEM>

<INPUT>
{{원본 프롬프트}}
</INPUT>

<PROCESS>
<STEP id="1">구조 분해: 역할/목적/지시/제약/출력 5요소로 분해</STEP>
<STEP id="2">약점 탐지: 각 요소별 모호성·누락·충돌 식별</STEP>
<STEP id="3">우선순위: 탐지된 약점을 Critical/Major/Minor로 분류</STEP>
<STEP id="4">재작성: Critical → Major 순서로 수정, 각 수정 이유 명기</STEP>
<STEP id="5">사전 스캔: 재작성 결과를 PE-3 기준으로 자가 점검 (85점 이상 통과)</STEP>
</PROCESS>

<OUTPUT_FORMAT>
<weakness_report>
  <critical count="{{n}}">{{목록}}</critical>
  <major count="{{n}}">{{목록}}</major>
  <minor count="{{n}}">{{목록}}</minor>
</weakness_report>
<rewritten_prompt>{{재작성 결과}}</rewritten_prompt>
<self_check_score>{{0-100}}</self_check_score>
<iteration_needed>{{true/false}}</iteration_needed>
</OUTPUT_FORMAT>
```

---

## 📊 성능 기대치 (v1.4)

| 지표 | v1.3 기준 | v1.4 목표 |
|------|----------|----------|
| 약점 탐지율 | ~70% | ~88% |
| 재작성 1회 통과율 | ~60% | ~80% |
| 평균 반복 횟수 | 2.1회 | 1.4회 |

---

> 연계: [PE-2 upgrade_v1.4.md](../PE-2_auto-proliferation/upgrade_v1.4.md) | [PE-3 upgrade_v1.4.md](../PE-3_auto-validation/upgrade_v1.4.md)
