# PE-7 Auto-Automation Design — CHANGELOG

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
