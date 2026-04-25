# PE-3 자동검증 체크리스트 — 글로벌 반도체 설계 서비스 프로젝트

## 메타데이터
- **버전**: 2.0.0
- **적용 대상**: Master Prompt v2.0 + 변형 A/B/C v2.0
- **생성일**: 2026-04-25
- **검증 엔진**: PE-3 Auto-Validate

---

## Layer 1: 구조 검증 (Schema Validation)

### 1.1 Master Prompt 섹션 완전성

| 섹션 | 필수 여부 | 체크 | 비고 |
|---|---|---|---|
| SECTION 1: ROLE | ✅ CRITICAL | ☐ | persona + constraints 포함 |
| SECTION 2: OBJECTIVE | ✅ CRITICAL | ☐ | primary + anchor_companies |
| SECTION 3: SEARCH SCOPE | ✅ CRITICAL | ☐ | ISO-3166 코드 명시 |
| SECTION 4: INCLUSION CRITERIA | ✅ CRITICAL | ☐ | Boolean Tree 형식 |
| SECTION 5: OUTPUT FORMAT | ✅ CRITICAL | ☐ | 필드 타입 강제 |
| SECTION 6: VALIDATION RULES | ✅ CRITICAL | ☐ | 수치 기준 포함 |
| SECTION 7: EXECUTION PROTOCOL | ✅ HIGH | ☐ | PARALLEL 모드 명시 |

### 1.2 필드 타입 강제 검증

```
□ Founded: INTEGER(YYYY) — REGEX '^[0-9]{4}$'
□ Type: ENUM(A,B,C,D) — 4개 값 외 불가
□ FabPartner: ENUM(TSMC,GF,Samsung,UMC,SMIC,Intel,Other,NA)
□ Listed: BOOLEAN — true/false only
□ VC_Tier1: BOOLEAN — true/false only
□ URL: STARTSWITH 'https://'
□ Country: ISO-3166-ALPHA2 (2자리 대문자)
```

---

## Layer 2: 데이터 정합성 검증

### 2.1 Anchor Company 포함 여부

```
□ Alchip Technologies — Type A, TW, TWSE 상장
□ Global Unichip Corp (GUC) — Type A, TW, TSMC 자회사
□ Faraday Technology — Type A, TW, TWSE 상장
□ Flexcompute — Type D, US, VC 투자
□ AllSpice — Type D, US, VC 투자
```

### 2.2 최소 기업 수 충족

```
□ Type A: COUNT >= 8  (현재: ___ )
□ Type B: COUNT >= 13 (현재: ___ )
□ Type C: COUNT >= 3  (현재: ___ )
□ Type D: COUNT >= 4  (현재: ___ )
□ Total:  COUNT >= 28 (현재: ___ )
```

### 2.3 IDM 제외 확인

```
□ Intel (직속 설계팀) — 미포함 확인
□ Samsung Electronics (직속) — 미포함 확인
□ SK Hynix — 미포함 확인
□ Micron — 미포함 확인
□ TSMC (파운드리 서비스만) — 미포함 확인
□ Semifive (Samsung Foundry 계열) — Type C로 재분류 OR 제외
```

### 2.4 데이터 신뢰도

```
□ 비공개 데이터 사용 기업: confidence=LOW 표기 확인
□ URL 전체 기업 포함 여부: ALL rows have URL
□ 설립연도 4자리 정수: YYYY format
```

---

## Layer 3: 변형 정합성 검증

### 3.1 변형 A v2.0

```
□ SCOPE가 "교체"가 아닌 "필터 추가" 방식으로 작성되었는지
□ Master Anchor 5개사 지역 상충 없이 병합 가능한지
□ region_focus 태그 추가 후 Master D-1 병합 가능한지
□ Type 분류 Master v2.0 기준과 동일한지
```

### 3.2 변형 B v2.0

```
□ Type C 서브-변형 B-C 분리 적용되었는지
□ TSMC Partner Level ENUM 정의되었는지
□ TSMC_Node 필드 추가 확인
□ CoWoS_Capable BOOLEAN 추가 확인
```

### 3.3 변형 C v2.0

```
□ confidence ENUM(HIGH/MEDIUM/LOW) 적용되었는지
□ IPO Signal 5개 지표 + 임계값(7점) 명시되었는지
□ M&A 패턴 3개 레퍼런스 케이스 포함되었는지
□ Gap Matrix 5개 축 정의되었는지
```

---

## 자동 교정 규칙 (Auto-Correction Triggers)

| 오류 유형 | 자동 처리 방식 | 알림 레벨 |
|---|---|---|
| Anchor Company 누락 | 강제 추가 + 데이터 보완 요청 | CRITICAL |
| Type 수 미달 | 지역 범위 확대 후 재탐색 | HIGH |
| IDM 혼입 | 즉시 제거 + 대체 기업 탐색 | CRITICAL |
| Founded 형식 오류 | 자동 변환 시도, 불가 시 NULL | MEDIUM |
| URL 누락 | 공식 사이트 탐색 자동 실행 | MEDIUM |
| 비공개 데이터 미표기 | confidence=LOW 자동 삽입 | HIGH |
