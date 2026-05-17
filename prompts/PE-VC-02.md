# PE-VC-02 · Layer 2 — 전도메인 전처리 게이트

## 메타데이터

| 항목 | 값 |
|------|----|
| Prompt ID | PE-VC-02 |
| Layer | 2 — Universal Preprocessing Gate |
| 적용 범위 | **전 도메인** (PE-SEMI / PE-DD / PE-AI-ECO / PE-FIN / PE-STRAT / PE-MIN / PE-PROD / PE-NBD / PE-DC / PE-SAT / PE-TDA / PE-THERM / PE-PWR 등) |
| 실행 시점 | 각 도메인 프롬프트 **호출 직전** |
| 버전 | v1.0 |
| 작성일 | 2026-05-17 |

---

## 역할 정의

PE-VC-02는 **도메인 프롬프트 실행 전** 입력 쿼리를 표준화·분류·컨텍스트 보강하는 **전처리 게이트**입니다.  
모든 도메인에 균일하게 적용되어 출력 일관성과 토큰 효율을 동시에 확보합니다.

---

## 전처리 파이프라인 (5단계)

### STAGE 1 — 쿼리 정규화
```
[INPUT_QUERY] 수신
↓
1-1. 한국어/영어 혼합 → 단일 언어 정렬 (기본값: 한국어)
1-2. 약어·코드 확장 (HBM → High Bandwidth Memory / CoWoS → Chip-on-Wafer-on-Substrate)
1-3. 불필요 필러 제거 ("좀", "한번", "빠르게" 등)
```

### STAGE 2 — 의도 분류 (Intent Classification)
```
CLASS-A: 시장분석 / 경쟁정보 → PE-SEMI, PE-MIN, PE-AI-ECO 우선 라우팅
CLASS-B: 재무모델링 / 밸류에이션 → PE-FIN, PE-DD 우선 라우팅  
CLASS-C: 전략수립 / 의사결정 → PE-STRAT, PE-NBD 우선 라우팅
CLASS-D: 기술분석 / 설계 → PE-SEMI, PE-TDA, PE-THERM 우선 라우팅
CLASS-E: 복합/크로스도메인 → Layer 3(PE-VC-03) 에스컬레이션 플래그 ON
```

### STAGE 3 — 컨텍스트 인젝션
```
- 세션 컨텍스트: 직전 3회 CMD 이력 참조
- 도메인 컨텍스트: 해당 도메인 최신 SSOT 스냅샷 헤더 삽입
- 시간 컨텍스트: 현재 날짜 + 분기 태그 자동 삽입
```

### STAGE 4 — 출력 포맷 사전 지정
```
[FORMAT_SPEC]
- depth: {QUERY_CLASS에 따른 자동 결정: A→Level3 / B→Level4 / C→Level3 / D→Level4 / E→Layer3 위임}
- lang: ko
- citation_mode: inline
- table_required: CLASS-B, CLASS-D → True / 기타 → 쿼리 길이 기반 판단
```

### STAGE 5 — 라우팅 결정 출력
```yaml
# PE-VC-02 라우팅 패킷 (도메인 프롬프트에 전달)
preprocess:
  normalized_query: "[정규화된 쿼리]"
  intent_class: "[A/B/C/D/E]"
  primary_domain: "[PE-XXX]"
  context_injected: true
  layer3_escalate: [true/false]  # CLASS-E 시 true
  format_spec:
    depth: [3/4/"L3_delegate"]
    lang: ko
    table_required: [true/false]
```

---

## 도메인 라우팅 매트릭스

| 도메인 | Intent Class 우선순위 | Layer3 에스컬레이션 조건 |
|--------|----------------------|-------------------------|
| PE-SEMI | A, D | 공급망 크로스 충격 |
| PE-DD | B | 복합 리스크 스코어 > 7.0 |
| PE-AI-ECO | A, E | AI 밸류체인 전방위 분석 |
| PE-FIN | B | 시나리오 수 ≥ 3 |
| PE-STRAT | C | 지정학 요인 포함 시 |
| PE-MIN | A, D | 광물-반도체 연계 |
| PE-PROD | C, D | 제품-시장 핏 복합 |
| PE-NBD | C | 신규 시장 진입 전략 |
| PE-DC / PE-SAT | D | 기술 스펙 다중 비교 |
| PE-TDA / PE-THERM / PE-PWR | D | 물리 시뮬레이션 요청 시 |

---

## 연동 인터페이스

```python
# automation/vc_layer_router.py 참조
from vc_layer_router import preprocess_gate
result = preprocess_gate(query=raw_query, domain=target_domain)
# result.layer3_required → True이면 PE-VC-03 자동 호출
```

---

## 품질 기준 (QA Gate)

- [ ] 정규화 후 쿼리 길이 축소율 ≥ 10%
- [ ] Intent Class 분류 신뢰도 ≥ 0.85
- [ ] 컨텍스트 인젝션 토큰 증가 ≤ 200 tokens
- [ ] 라우팅 패킷 YAML 유효성 통과
