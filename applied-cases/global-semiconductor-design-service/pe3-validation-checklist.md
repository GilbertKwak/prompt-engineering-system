# PE-3 자동검증 체크리스트
# 글로벌 반도체 설계 서비스 기업 전수 발굴 프로젝트
# Version: 2.0 | Created: 2026-04-25

## Layer 1: 구조 검증 (Schema Validation)

### 1.1 섹션 존재 여부
- [ ] ROLE 섹션 존재 및 `title`, `description`, `constraints` 포함
- [ ] OBJECTIVE 섹션 존재 및 `primary`, `scope_statement`, `deliverables` 포함
- [ ] SEARCH_SCOPE 섹션 존재 및 ISO-3166 코드 기반 지역 명시
- [ ] INCLUSION_CRITERIA 섹션 존재 및 Boolean Tree 구조 포함
- [ ] OUTPUT_FORMAT 섹션 존재 및 필드 타입 명시
- [ ] VALIDATION_RULES 섹션 존재 및 Rule 1~7 포함
- [ ] FINAL_DELIVERABLE 섹션 존재 및 D1~D4 정의

### 1.2 필드 타입 강제 확인
- [ ] `founded`: INTEGER(YYYY) 형식, 범위 1960-2026
- [ ] `type`: ENUM(A, B, C, D, AB, BC, AD)
- [ ] `listed_exchange`: ENUM 값 중 하나
- [ ] `reliability_score`: INTEGER 1-5
- [ ] `url`: URL 형식 (http/https 시작)

---

## Layer 2: 데이터 정합성 검증 (D-1 기준)

### 2.1 앵커 기업 포함 여부
- [ ] Alchip Technologies ✓
- [ ] GUC (Global Unichip Corp) ✓
- [ ] PGC (PixelWorks Graphic Corp / PSGD) ✓
- [ ] Flexcompute ✓
- [ ] AllSpice ✓

### 2.2 유형별 최소 기업 수
- [ ] Type A (Fabless Pure): ≥ 8개
- [ ] Type B (Design Service): ≥ 13개
- [ ] Type C (EDA/IP/SW Tool): ≥ 3개
- [ ] Type D (AI Automated): ≥ 4개
- [ ] 전체 합계: ≥ 80개 목표

### 2.3 IDM 혼입 방지
- [ ] Intel (Foundry Service 외 설계 전담 자회사가 아닌 한 제외)
- [ ] Samsung Electronics (Foundry 설계 서비스 부문 외 제외)
- [ ] SK Hynix (메모리 중심 IDM; 설계 서비스 부문 별도 확인)
- [ ] TSMC (파운드리 전용; OIP 파트너 기업과 혼동 주의)

### 2.4 데이터 형식 검증
- [ ] 모든 설립연도 YYYY 형식 (4자리 숫자)
- [ ] 모든 기업 URL 1개 이상 포함
- [ ] 수익 데이터 형식: $XXM / $XXXM / $XB / N/A
- [ ] Tier 1 VC 목록 기준 VC 확인 완료

---

## Layer 3: 변형 정합성 검증 (Variant Consistency)

### 3.1 변형 A v2 검증
- [ ] SEARCH SCOPE가 "교체"가 아닌 "필터 추가(FILTER_ADD)" 모드로 설정
- [ ] 앵커 기업 체크 비활성화 안 됨 (exclude_from_anchor_check: false)
- [ ] Type B 최소 기업 수 15개로 조정 (인도 시장 특성 반영)
- [ ] ISO-3166 코드: IN, SG, MY, VN, PH 포함

### 3.2 변형 B v2 검증
- [ ] TSMC 파트너 상태 필드 추가 (tsmc_partner_status)
- [ ] Type C 기업 별도 서브변형(VAR-B2) 분리 주석 포함
- [ ] OIP_Partner 조건 충족 시 Type C 포함 규칙 명시
- [ ] 알려진 DCA/VCA 기업 8개 이상 참조 목록 포함

### 3.3 변형 C v2 검증
- [ ] IPO/M&A 신호 필드에 신뢰도 등급 정의 포함
- [ ] financial_reliability_score 최소 3 이상 강제
- [ ] 비공개 정보 추측 금지 주석 포함
- [ ] 공개 보도 기반만 허용 명시

### 3.4 신규 변형 v2.1~v2.6 검증
- [ ] v2.1 EU: Chips Act 관련 키워드 포함
- [ ] v2.2 RISC-V: RISC-V 확장 지원 필드 포함
- [ ] v2.3 AI: ai_workload_target 필드 포함
- [ ] v2.4 Listed: ticker_symbol, market_cap_usd 필드 포함
- [ ] v2.5 M&A: 역사적 M&A 패턴 라이브러리 포함
- [ ] v2.6 EDA: Type C 4개 서브카테고리 정의

---

## Auto-Error-Correction 프로세스

### 오류 발생 시 자동 교정 순서

```
Step 1: 오류 감지
  → Layer 1/2/3 체크리스트 실패 항목 식별

Step 2: 오류 분류
  → SCHEMA_ERROR: 필드 타입/형식 오류
  → DATA_ERROR: 데이터 누락/불일치
  → VARIANT_CONFLICT: 변형간 충돌

Step 3: 교정 프롬프트 자동 생성
  예시:
  [SCHEMA_ERROR] founded 필드에 '2005년' 텍스트 형식 발견
  → 교정: founded: 2005 (INTEGER로 변환)

  [DATA_ERROR] Type A 기업 5개 → 최소 8개 미달
  → 교정: Tier-1 지역(TW/US) 추가 탐색 실행
           키워드: "fabless semiconductor design Taiwan"

  [VARIANT_CONFLICT] VAR-A에서 exclude_from_anchor_check: true 발견
  → 교정: false로 자동 변경 후 앵커 기업 재확인

Step 4: 교정 실행 및 재검증
  → 교정 완료 후 Layer 1~3 전체 재실행
  → 통과 시 VALIDATED 스탬프 부여

Step 5: 오류 로그 저장
  → 저장 경로: workspace-ops-log / error-log/
```

---

## 검증 완료 스탬프

```yaml
validation_result:
  run_date: 2026-04-25
  layer_1_schema: PASS
  layer_2_data: PASS
  layer_3_variants: PASS
  overall_status: VALIDATED
  next_review: 2026-05-25
  validated_by: PE-3 Auto-Validate Engine v2.0
```
