# PE-DD vs PE-TDA MECE 경계 정의

> Version: 1.0 | Date: 2026-05-09 | Author: Gilbert  
> 목적: Cross-Library 태깅 왜곡 방지 및 도메인 간 중복/누락 제거

---

## 1. 도메인 정의

| 도메인 | 풀네임 | 핵심 질문 |
|---|---|---|
| **PE-TDA** | Technology & Deal Assessment | *이 기술은 실현 가능하고, 딜 조건은 기술 가치를 반영하는가?* |
| **PE-DD** | Due Diligence (非기술) | *재무·법무·운영 측면에서 투자 리스크는 수용 가능한가?* |

---

## 2. MECE 분류표

### PE-TDA 전용 영역

| 분류 | 체크 항목 | Cross 태깅 |
|---|---|---|
| D1 기술 성숙도 | TRL 레벨 평가, TRL 갭 분석 | — |
| D2 IP 포트폴리오 | 특허 건수·등록상태, 회피설계 가능성 | IP 가치평가는 PE-DD 공유 |
| D3 로드맵 실현가능성 | 마일스톤, 기술 병목, 외부 의존성 | — |
| D4 딜 구조 | 지분율·조건부·Exit 구조 | Entry EV 적정성은 PE-DD 공유 |
| D5 팀 역량 | Key Man 리스크, 채용 계획 | — |
| D6 리스크 매트릭스 | 기술×딜 교차 매트릭스, Bear Case | Bear IRR은 PE-DD 공유 |
| D7 Cross-Library 태깅 | PE-TDA 도메인 태그, 혼용 감지 | — |

### PE-DD 전용 영역

| 분류 | 체크 항목 | Cross 태깅 |
|---|---|---|
| 재무실사 | 감사보고서, 재무제표 분석, EBITDA 검증 | — |
| 법무실사 | 계약서 리뷰, 소송·분쟁, 지배구조 | — |
| 세무실사 | 세무조정, 우발채무, 이연법인세 | — |
| 노무실사 | 핵심인력 처우, 고용계약, 노동법 리스크 | — |
| IP 가치평가 | 원가법·수익접근법·시장접근법 | **PE-TDA D2 공유** |
| Entry EV 적정성 | PER/EV-EBITDA 멀티플 Comp | **PE-TDA D4 공유** |
| Bear Case IRR | 재무 시나리오 하방 분석 | **PE-TDA D6 공유** |

---

## 3. 공유 영역 (Cross-Library 이중 태깅 필수)

다음 3개 항목은 **PE-TDA와 PE-DD 양쪽 모두** 태그를 기재해야 합니다.

```
[공유 항목]         [PE-TDA 체크]  [PE-DD 체크]
IP 가치평가         TDA-D2-03      DD 독립 체크
Entry EV 적정성     TDA-D4-01      DD 독립 체크
Bear Case IRR       TDA-D6-02      DD 재무 시나리오
```

### 태깅 규칙

```yaml
# Notion Cross Library 필드 예시
cross_libs:
  - PE-TDA        # 기술실사 주도
  - PE-DD         # 재무/IP 가치평가 교차
```

> ⚠️ 공유 항목임에도 PE-TDA만 태깅하면 PE-DD 파이프라인에서 누락되고,  
> PE-DD만 태깅하면 TDA QC 점수 D2/D4/D6 항목이 미충족으로 집계됩니다.

---

## 4. 혼용 금지 패턴

### PE-TDA 문서에 포함하면 안 되는 키워드 (→ PE-DD로 이동)

```
감사보고서 / 법무실사 / 계약서 리뷰 / 우발채무 / 세무조정 / 노무실사
```

### PE-DD 문서에 포함하면 안 되는 키워드 (→ PE-TDA로 이동)

```
TRL [숫자] / 회피설계 / 기술 성숙도 / 기술 로드맵 / 기술 리스크 병목
```

---

## 5. Cross-Library 태깅 의사결정 트리

```
분석 대상 문서
    ├─ 기술 완성도·IP·로드맵 포함?
    │       YES → PE-TDA 태깅 필수
    │       NO  → PE-TDA 제외
    │
    ├─ 재무·법무·세무·노무 포함?
    │       YES → PE-DD 태깅 필수
    │       NO  → PE-DD 제외
    │
    └─ IP 가치평가 / Entry EV / Bear IRR 포함?
            YES → PE-TDA + PE-DD 이중 태깅 필수
            NO  → 단일 태깅
```

---

## 6. pe3_tda_validator.py 연동

```bash
# TDA 문서 QC 검증
python automation/pe3_tda_validator.py --file analysis.md

# PE-DD 혼용 키워드 감지
python automation/pe3_tda_validator.py --file analysis.md --domain-check

# MECE 경계 요약 출력
python automation/pe3_tda_validator.py --boundary

# strict 모드 (88점 미만 exit 1)
python automation/pe3_tda_validator.py --file analysis.md --strict
```

---

## 7. pe7_product_mece_loop.py v2.0 연동

`pe3_tda_validator.py`는 `pe7_product_mece_loop.py`의 D4(딜 구조) 파싱 결과를
TDA QC로 재검증하는 **2차 게이트**로 동작합니다.

```
pe7_product_mece_loop.py
  └─ parse_analysis()        # D1~D8 파싱
  └─ run_pe3_qc()            # PE-PROD QC (pe3_product_validator)
  └─ [NEW] run_pe3_tda_qc()  # TDA 전용 QC (pe3_tda_validator) ← 추가 예정
```

> 다음 단계: `pe7_product_mece_loop.py`에 `run_pe3_tda_qc()` 호출 추가

---

*자동 생성: PE-7 시스템 | GilbertKwak/prompt-engineering-system*
