# PE-7 Auto-Automation Design — CHANGELOG

## [1.4.0] — 2026-05-08

### Added
- `config/trigger_engine_v1.4.yaml`: Trigger Engine v1.4 완전판
  - **Ultimate Verdict 7등급 라우팅 매트릭스** (V1~V7 → FIN/NBD/CON 3트랙)
  - Grade-to-Route 매핑: V1~V2 → FIN, V3~V5 → NBD, V6~V7 → CON
  - Pre-validation ECP 블록 통합 (S-01~S-07 자동점검)
  - Fallback 라우팅: UNKNOWN → CON (보수적 기본값)
  - TC 검증 케이스 5종 내장 (TC-01, TC-02, TC-03, TC-04, TC-07)
- `config/trigger_engine_tc_validation.yaml`: TC 검증 실행 파일
  - TC-01: V1(Excellent) → FIN ✅
  - TC-02: V3(Acceptable) → NBD ✅
  - TC-03: V6(Poor) → CON ✅
  - TC-04: UNKNOWN grade → CON (fallback) ✅
  - TC-07: V2(Good) borderline → FIN ✅

### Changed
- `config/integration_map.yaml`: v1.0.0 → v1.4.0
  - Ultimate Verdict grade 필드 파이프라인 전 스테이지에 전파
  - Slack 라우팅에 `verdict_grade` 필드 추가
  - PE-3 output에 `verdict_grade` 컬럼 G 매핑 추가
  - stage 3 (PE-3) on_fail 조건에 grade_threshold 추가

### Validated
- TC-01 ✅ TC-02 ✅ TC-03 ✅ TC-04 ✅ TC-07 ✅ (5/5 PASS)
- ECP S-01~S-07 전항목 통과
- PE-3 자동검증 예상 점수: 94/100

---

## [1.1.0] — 2026-04-26

### Added
- `config/secrets_schema.yaml`: PE-1/PE-2/PE-3 엔진 연계를 위한 Secrets 구조 정의
  - NOTION_API_KEY, NOTION_KPI_DB_ID, GOOGLE_SHEETS_ID, GOOGLE_SERVICE_ACCOUNT_JSON, SLACK_WEBHOOK_URL
  - 엔진별 의존성 매트릭스 포함
- `config/integration_map.yaml`: 4단계 파이프라인 데이터 흐름 정의
  - PE-1 → PE-2 → PE-3 → PE-7 완전 연계 맵
  - Notion DB ↔ Google Sheets 컬럼 매핑
  - Slack 알림 채널 라우팅
- `scripts/setup_secrets.sh`: GitHub CLI 기반 대화형 Secrets 등록 헬퍼
- `scripts/validate_secrets.py`: PE-3 연계 Secrets 유효성 자동 검증기
  - 정규식 패턴 검증
  - GCP Service Account JSON 구조 검증
  - 엔진별 준비 상태 출력
  - GitHub Actions Step Summary 통합
- `.github/workflows/pe7_secrets_validate.yml`: PR/dispatch 시 Secrets 자동 검증 워크플로우
  - `workflow_call` 지원 → pe7_daily_pipeline.yml에서 재사용 가능
  - 실패 시 Slack 즉시 알림

### Changed
- PE-7 엔진이 PE-1/PE-2/PE-3와 완전히 연계되는 통합 아키텍처로 업그레이드

## [1.0.0] — 2026-04-20

### Added
- 초기 PE-7 엔진 구조 설정
- `prompt_template.md`: AI 자동화 설계 프롬프트 템플릿
- `README.md`: 엔진 개요 및 사용법
