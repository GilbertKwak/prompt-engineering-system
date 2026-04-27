# CHANGELOG — JV Fund Prompt Library

> **저장소**: prompt-engineering-system/prompts/jv_fund/  
> **관리자**: GilbertKwak  
> **업데이트 주기**: 버전 릴리즈 시 + 월간 검토 시

---

## [v4.0] — 2026-04-27

### 🆕 Added
- `master_prompt_v4.md`: v2 원본 8개 core_module 완전 통합판
  - Module 1: GP & Governance Architecture (완전 파라미터화)
  - Module 2: LP Segmentation & Economic Terms (워터폴 상세)
  - Module 3: Fund Structuring & Legal Design (Master-Feeder/Parallel)
  - Module 4: Capital Engineering (보텀업 펀드 사이징)
  - Module 5: Investment Policy & IC Framework (의결 구조)
  - Module 6: Post-Investment Value Creation (100일 플랜)
  - Module 7: Exit & Return Optimization (DPI/TVPI/IRR)
  - Module 8: Risk & Scenario Management (3종 스트레스)
- LP_TYPE 파라미터 추가 (Pension/Sovereign/Corporate/FamilyOffice/Mixed)
- FUND_SIZE_USD, JURISDICTION, SECTOR_STAGE 파라미터 추가
- PE-3 스트레스 시나리오 3종 (Base/Stress/Tail Risk)
- LP Pitch Template 파생 프롬프트 예정 추가
- QUICK COMMAND 섹션 (GitHub CLI alias 포함)

### 🔧 Changed
- OUTPUT FORMAT: 8모듈 완료 상태 체크 추가
- VALIDATION RULES: PE-1 LP조건 출처 + 규제 법령 근거 추가
- PE-3: 지정학 리스크 + LP 유동성 위기 시나리오 추가
- HIGH-RISK SELF-CHECK: v2 원본 언어 충실 반영

### 📊 Metrics
- 파일 크기: ~12KB (v3 8KB 대비 +50%)
- 모듈 커버리지: 8/8 (v3: 구조 개선만, v4: 내용 완전 통합)
- 파라미터 수: 10개 (v3: 6개)
- PE-1 목표 준수율: 95%
- PE-3 목표 점수: 92/100

---

## [v3.0] — 2026-04-27

### 🆕 Added
- `master_prompt_v3.md`: v2 → v3 구조 개선
- `master_v3.md`: 병행 저장본
- `fu_adapter_v1.md`, `bstar_eco2_v1.md`, `ai_infra_v1.md`: 파생 프롬프트 3종
- `validation_checklist.md`, `VALIDATION_CHECKLIST.md`: 검증 체크리스트
- `variants/` 디렉터리 생성

### 🔧 Changed
- v2 단일 XML 블록 → 5구조 분리 (ROLE/CONTEXT/TASK/OUTPUT/VALIDATION)
- 파라미터: DOMAIN, STAGE, DEPTH, LANG 표준화
- 출력: JSON + MD 병기
- 언어: 영문 단일 → KR+EN 병기

---

## [v2.0] — 2026-04-26 (원본)

### 원본 파일 특성
- 파일명: `Global_Joint_Venture_Fund_Master_Prompt_v2.txt`
- 구조: XML 단일 블록
- 언어: 영문 단일
- 모듈: 8개 (GP_Governance, LP_Segmentation, Fund_Structuring, Capital_Engineering, Investment_Policy, Post_Investment, Exit_Return, Risk_Scenario)
- 검증 기준: 없음
- 파라미터: 없음

---

## 다음 계획 (v5.0 예정)

- [ ] `lp_pitch_template.md` 완성 (LP Pitch Deck 전용)
- [ ] GitHub Actions 자동 검증 워크플로우 연동
- [ ] `auto_validate.py` PE-1/PE-3 규칙 업데이트
- [ ] Notion 자동 동기화 스크립트 개선
- [ ] 월간 검토 이슈 자동 생성 스케줄 등록

---

*CHANGELOG 관리: prompt-engineering-system/prompts/jv_fund/CHANGELOG.md*
