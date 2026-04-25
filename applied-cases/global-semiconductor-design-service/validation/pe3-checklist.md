# PE-3 자동검증 체크리스트 — 글로벌 반도체 설계 서비스 (P-007)

> **Prompt ID:** P-007 | **Version:** v2.0 | **Created:** 2026-04-25
> **검증 기준:** PE-3 프레임워크 v2.0 (prompt-engineering-system 기준)

---

## 검증 결과 요약

| 카테고리 | 항목 수 | 통과 | 경고 | 실패 | 점수 |
|---|---|---|---|---|---|
| 구조 완전성 | 7 | 7 | 0 | 0 | 100/100 |
| 논리 정합성 | 5 | 5 | 0 | 0 | 100/100 |
| 데이터 명세 | 6 | 6 | 0 | 0 | 100/100 |
| 오류 예방 | 5 | 5 | 0 | 0 | 100/100 |
| 산출물 정의 | 4 | 4 | 0 | 0 | 100/100 |
| **종합** | **27** | **27** | **0** | **0** | **100/100** |

> ⚠️ 위 점수는 프롬프트 **구조** 기준 점수입니다. 실제 실행 후 D-1 데이터 품질 기반 재검증 필요.

---

## Section 1: 구조 완전성 (Structure Completeness)

- [x] **S-01** SYSTEM HEADER 존재 (prompt_id, version, title, status)
- [x] **S-02** ROLE 섹션 존재 및 전문 영역 명시
- [x] **S-03** OBJECTIVE 섹션 존재 및 Type A~D 정의
- [x] **S-04** SEARCH SCOPE 섹션 존재 및 지역 코드(ISO-3166) 명시
- [x] **S-05** INCLUSION CRITERIA Boolean Tree 구조
- [x] **S-06** OUTPUT FORMAT 필드 타입 강제 (INTEGER, ENUM, STRING)
- [x] **S-07** FINAL DELIVERABLE 트리거 조건 명시

---

## Section 2: 논리 정합성 (Logic Consistency)

- [x] **L-01** Boolean Tree `(TypeA OR TypeB OR TypeC OR TypeD) AND (Fab≠IDM)` 구조 정확
- [x] **L-02** IDM 제외 기준 명시 (예시 기업 5개 이상)
- [x] **L-03** Tier 1 VC 기준 수치 목록 존재 (8개 이상)
- [x] **L-04** MA_signal HIGH/MEDIUM/LOW 판단 기준 명시
- [x] **L-05** D-3 Gap 분석 자동 트리거 조건 명시

---

## Section 3: 데이터 명세 (Data Specification)

- [x] **D-01** 설립연도 `INTEGER(YYYY)` 타입 강제
- [x] **D-02** 주요 파운드리 파트너 `ENUM` 값 목록 명시
- [x] **D-03** 상장 거래소 `STRING` + 조건부 필수 정의
- [x] **D-04** 매출 규모 `$XM/$XB` 형식 강제, 비공개 시 'N/A'
- [x] **D-05** 신뢰도 등급 `ENUM(A/B/C)` 필수 기재
- [x] **D-06** URL `https://` 포함 강제

---

## Section 4: 오류 예방 (Error Prevention)

- [x] **E-01** IDM 혼입 방지 Rule 존재 (CRITICAL 등급)
- [x] **E-02** 지역 편중 방지 기준 (APAC 비대만/비중국 ≥15%)
- [x] **E-03** 설립연도 불명확 시 대체 데이터 소스 명시
- [x] **E-04** 매출 데이터 N/A 처리 기준 명시
- [x] **E-05** D-3/D-4 재생성 방지 트리거 조건 명시

---

## Section 5: 산출물 정의 (Deliverable Definition)

- [x] **O-01** D-1 최소 항목 수 명시 (30개 이상)
- [x] **O-02** D-2 범위 명시 (Top 30, 매출 기준)
- [x] **O-03** D-3 트리거 조건 명시 (Type 최소 기준 미달 시)
- [x] **O-04** D-4 트리거 조건 명시 (명시적 요청 또는 변형 C)

---

## 변형 검증 (Variant Validation)

| 변형 | Master와 충돌 | 수정 사항 | 상태 |
|---|---|---|---|
| A (지역 집중) | ❌ 없음 (FILTER_ADD 방식으로 수정) | v1.0의 REPLACE → FILTER_ADD 변경 | ✅ 통과 |
| B (TSMC 파트너) | ❌ 없음 (TypeC 서브-변형 분리) | TypeC 별도 섹션 D-1B_TypeC 추가 | ✅ 통과 |
| C (재무 분석) | ❌ 없음 (신뢰도 등급 추가) | MA_signal 판단 기준 5개 추가 | ✅ 통과 |
| v2.1 (유럽) | ❌ 없음 | 변형 A 지역 교체 | ✅ 통과 |
| v2.2 (RISC-V) | ❌ 없음 | 변형 B 키워드 추가 | ✅ 통과 |
| v2.3 (AI 칩) | ❌ 없음 | SEARCH SCOPE 키워드 추가 | ✅ 통과 |
| v2.4 (상장사) | ❌ 없음 | 변형 C 필터 강화 | ✅ 통과 |
| v2.5 (M&A) | ❌ 없음 | 변형 C 확장 + 패턴 DB | ✅ 통과 |
| v2.6 (EDA/SW) | ❌ 없음 | TypeD 독립 실행 | ✅ 통과 |

---

## 실행 후 재검증 항목 (Post-Execution)

> D-1 데이터 생성 후 아래 항목을 수동 또는 자동으로 재검증합니다.

- [ ] **PE-01** Anchor Company 5종 포함 여부 (Alchip, GUC, PGC, Flexcompute, AllSpice)
- [ ] **PE-02** Type 분포: A≥8, B≥13, C≥3, D≥4
- [ ] **PE-03** IDM 혼입 여부 (Intel, Samsung Foundry, Micron 등)
- [ ] **PE-04** 설립연도 전수 YYYY 형식 확인
- [ ] **PE-05** URL 전수 유효성 확인
- [ ] **PE-06** 신뢰도 등급 전수 기재 확인
- [ ] **PE-07** 지역 분포: APAC 비대만/비중국 ≥15% 확인
- [ ] **PE-08** D-3 Gap 분석 필요 여부 자동 판단

---

*PE-3 체크리스트 | P-007 v2.0 | 2026-04-25 | GilbertKwak/prompt-engineering-system*
