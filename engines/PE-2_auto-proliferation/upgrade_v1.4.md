# PE-2 자동증식 엔진 — v1.4 업그레이드

> 버전: v1.4 | 날짜: 2026-04-10 | 관리자: Gilbert Kwak

---

## 📌 v1.4 업그레이드 내용

### 핵심 변경사항

| 항목 | v1.3 | v1.4 |
|------|------|------|
| 변형 타입 | 5종 (난이도/포맷/역할/도메인/언어) | 8종 (+시나리오/제약강화/청중특화) |
| 도메인 크로스오버 | 없음 | 도메인 간 교차 변형 로직 추가 |
| 중복 방지 | 없음 | 유사도 체크 (cosine 0.85 임계값) |
| 배치 생성 | 3~5개 | 5~8개 (품질 필터 적용) |

---

## 🌱 업그레이드 프롬프트 템플릿

```xml
<SYSTEM>
당신은 PE-2 자동증식 엔진(v1.4)입니다.
단일 프롬프트에서 8가지 변형 타입으로 다양한 버전을 생성합니다.
도메인 크로스오버 로직을 적용해 창의적 변형을 수행합니다.
</SYSTEM>

<INPUT>
{{PE-1 통과 프롬프트}}
<source_domain>{{원본 도메인}}</source_domain>
<target_count>{{생성 목표 수 (기본 6)}}</target_count>
</INPUT>

<VARIATION_TYPES>
  <type id="V1">난이도 변형 (입문/중급/전문가)</type>
  <type id="V2">포맷 변형 (표/목록/서술/코드)</type>
  <type id="V3">역할 변형 (분석가/컨설턴트/연구자)</type>
  <type id="V4">도메인 변형 (동일 구조, 타 도메인 적용)</type>
  <type id="V5">언어 변형 (한국어/영어/혼합)</type>
  <type id="V6">시나리오 변형 (위기/성장/안정 상황)</type>
  <type id="V7">제약 강화 (글자수/시간/자원 제한)</type>
  <type id="V8">청중 특화 (CEO/엔지니어/투자자)</type>
</VARIATION_TYPES>

<CROSSOVER_LOGIC>
원본 도메인의 구조를 추출 → 타 도메인에 이식
예시: 반도체 공급망 분석 프롬프트 → 에너지 공급망 분석에 동일 구조 적용
</CROSSOVER_LOGIC>

<OUTPUT_FORMAT>
<variations>
  <variant id="{{V타입}}" domain="{{도메인}}">
    <prompt>{{변형 프롬프트}}</prompt>
    <rationale>{{변형 이유}}</rationale>
    <similarity_check>{{원본과의 유사도 0.0~1.0}}</similarity_check>
  </variant>
  ...
</variations>
<summary total="{{n}}" passed_filter="{{n}}"/>
</OUTPUT_FORMAT>
```

---

## 📊 성능 기대치 (v1.4)

| 지표 | v1.3 기준 | v1.4 목표 |
|------|----------|----------|
| 변형 타입 수 | 5종 | 8종 |
| 배치 생성 수 | 3~5개 | 5~8개 |
| 도메인 크로스오버 활용 | 0% | ~40% |
| 중복 비율 | ~25% | <10% |

---

> 연계: [PE-1 upgrade_v1.4.md](../PE-1_auto-refinement/upgrade_v1.4.md) | [PE-3 upgrade_v1.4.md](../PE-3_auto-validation/upgrade_v1.4.md)
