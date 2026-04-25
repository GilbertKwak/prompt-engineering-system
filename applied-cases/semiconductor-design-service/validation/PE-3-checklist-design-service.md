# PE-3 자동검증 체크리스트
## 글로벌 반도체 설계 서비스 기업 발굴 — v2.0

> **연동:** MASTER-v2.0.yaml | Notion PE-7 (34955ed4...)
> **버전:** 2.0 | **생성일:** 2026-04-25

---

## Layer 1: 구조 검증 (Schema Validation)

프롬프트 실행 전 구조 완결성 확인:

- [ ] `ROLE` 섹션 존재 (persona + experience + scope 3개 이상)
- [ ] `OBJECTIVE` 섹션 존재 (output_count_min ≥ 50 명시)
- [ ] `SEARCH_SCOPE` 섹션 존재 (ISO-3166 국가코드 8개 이상)
- [ ] `INCLUSION_CRITERIA` Boolean Tree 완성 (AND/OR 명시)
- [ ] `VALIDATION_RULES` 앵커기업 5개 이상 포함
- [ ] `OUTPUT_FORMAT` D1~D4 모두 정의
- [ ] `ERROR_PREVENTION` 섹션 존재 (ERR-001 이상)

**결과:** ⬜ PASS / ⬜ FAIL (실패 시 해당 섹션 재작성 후 재검증)

---

## Layer 2: 데이터 정합성 검증 (D1 생성 후 실행)

### 앵커기업 포함 여부
- [ ] Alchip Technologies 포함 (Type B 앵커)
- [ ] GUC (Global Unichip Corp) 포함 (Type B 앵커)
- [ ] Faraday Technology 포함 (Type A 앵커)
- [ ] Flexcompute 포함 (Type C 앵커)
- [ ] AllSpice 포함 (Type C 앵커)

**결과:** ⬜ 5/5 PASS / ⬜ 미포함 기업: ___________

### 수량 기준
- [ ] Type A ≥ 8개
- [ ] Type B ≥ 13개
- [ ] Type C ≥ 3개
- [ ] Type D ≥ 4개
- [ ] 전체 ≥ 50개

**실제 수량:**
| Type | 요구 | 실제 | 결과 |
|------|------|------|------|
| A | ≥8 | | ⬜ |
| B | ≥13 | | ⬜ |
| C | ≥3 | | ⬜ |
| D | ≥4 | | ⬜ |
| Total | ≥50 | | ⬜ |

### 제외 기업 검증
- [ ] 삼성전자 Foundry 직속 계열 없음
- [ ] TSMC 자체 서비스 부문 없음
- [ ] Intel Foundry Services 직속 없음
- [ ] IDM 직속 기업 없음 (Samsung, Intel, TI captive 등)

### 데이터 형식 검증
- [ ] 설립연도 YYYY 4자리 INTEGER (미상 = 0)
- [ ] 국가코드 ISO-3166-1 alpha-2 준수
- [ ] fab_partner ENUM 준수 (허용값: TSMC/GF/Samsung/UMC/SMIC/Intel/Multiple/None/Unknown)
- [ ] type ENUM 준수 (허용값: A/B/C/D)
- [ ] data_confidence 필드 존재 (Variant C 필수, 기타 권장)
- [ ] 출처 URL 50% 이상 기입

**결과:** ⬜ PASS / ⬜ FAIL

---

## Layer 3: 변형 정합성 검증

### 변형 A v2
- [ ] `extends: MASTER-v2.0` 선언 존재
- [ ] `filter_add` 방식 사용 (SEARCH_SCOPE 전체 교체 아님)
- [ ] 인도+아세안 기업 ≥ 15개 발굴
- [ ] 앵커기업 (TW/US) 누락 없음

### 변형 B v2
- [ ] `extends: MASTER-v2.0` 선언 존재
- [ ] TSMC 파트너십 레벨 명시 (DCA/VCA/CoWoS/InFO/SoIC)
- [ ] Type C 서브변형 분리 주석 존재
- [ ] TSMC 파트너 최소 10개 발굴
- [ ] 모든 TSMC 파트너 주장에 출처 URL 첨부

### 변형 C v2
- [ ] `extends: MASTER-v2.0` 선언 존재
- [ ] `data_confidence` 필드 MANDATORY 표기
- [ ] `ipo_probability` 필드 존재
- [ ] `ma_signal` 필드 존재
- [ ] `data_confidence=Unverified` 비율 ≤ 30%
- [ ] 확인되지 않은 밸류에이션 수치 직접 출력 없음

---

## 자동 오류 예측 테이블

| ID | 오류 유형 | 발생 조건 | 예방 조치 | 심각도 |
|----|-----------|-----------|-----------|--------|
| ERR-001 | IDM 혼입 | Fab 조건 누락 | `Fab_type != IDM_Direct` 조건 실행 전 확인 | 🔴 HIGH |
| ERR-002 | 날짜 형식 오류 | `founded` 자유 텍스트 | INTEGER(YYYY) 강제, 미상=0 | 🟡 MED |
| ERR-003 | 앵커기업 누락 | SCOPE 너무 좁음 | 5개 앵커기업 포함 후 진행 | 🔴 HIGH |
| ERR-004 | 할루시네이션 | 비공개 재무 추정 | `data_confidence` 필드 의무화 | 🔴 HIGH |
| ERR-005 | 지역 편향 | US/TW 집중 | 지역별 최소 3개 이상 확인 | 🟡 MED |
| ERR-006 | Type 분류 오류 | EDA를 Type A로 분류 | Type C 정의 재확인 | 🟡 MED |
| ERR-007 | 변형 SCOPE 충돌 | 변형A에서 마스터 SCOPE 교체 | `filter_add` 방식 강제 | 🔴 HIGH |
| ERR-008 | TSMC 파트너 미검증 | 출처 없는 파트너 주장 | 출처 URL 없으면 `Unverified` 표기 | 🟡 MED |

---

## 오류 수정 워크플로우

```
Step 1. D1 생성 완료
   ↓
Step 2. Layer 1 구조 검증 실행
   → FAIL → 해당 섹션 재작성 → Step 2 재실행
   → PASS ↓
Step 3. Layer 2 데이터 정합성 검증
   → 앵커기업 누락 → SEARCH_SCOPE 확장 후 재실행
   → 수량 미달 → 해당 Type 키워드 추가 후 재실행
   → 형식 오류 → 해당 셀 수정
   → PASS ↓
Step 4. Layer 3 변형 정합성 검증 (해당 변형 실행 시)
   → FAIL → 변형 파일 수정 후 재검증
   → PASS ↓
Step 5. D2~D4 순차 생성
   ↓
Step 6. 최종 CHANGELOG 갱신
```

---

## 검증 이력

| 날짜 | 버전 | Layer 1 | Layer 2 | Layer 3 | 결과 | 비고 |
|------|------|---------|---------|---------|------|------|
| 2026-04-25 | v2.0 | ⬜ | ⬜ | ⬜ | ⬜ | 초기 버전 생성 |
