# CHANGELOG — JV Fund Prompt Library

---

## [v3.1] — 2026-04-27

### Added
- `parameters` 블록에 `DATE` 필드 추가
- PE-1 검증 규칙 6개 항목으로 세분화 (PE-1-01 ~ PE-1-06)
- PE-3 검증 규칙 5개 항목으로 세분화 (PE-3-01 ~ PE-3-05)
- `output_format`에 JSON 구조 스키마 추가
- `task_chain` Step 6 추가 (Output Packaging)
- `high_risk_self_check`에 PE-1/PE-3 실행 지시 추가
- `auto_validate_jv.py` 검증 스크립트 신규 추가
- `notion_sync_jv.py` Notion 동기화 스크립트 신규 추가
- `.github/workflows/jv_prompt_validate.yml` GitHub Actions 워크플로우 신규 추가
- Bash alias 4종 추가 (jv-validate, jv-sync, jv-new, jv-review)
- 관련 파일 인덱스 테이블 추가

### Changed
- 전후 비교표 업데이트 (v2 → v3.1 전체 항목)
- 버전 태그 v3.0 → v3.1
- Domain Variant 3종 출력 구조 명확화

### Fixed
- 원본 v2 대비 구조적 누락 항목 전부 보완
- 이중 아이콘(`💼 💼`) Notion 페이지 타이틀 정리 예정

---

## [v3.0] — 2026-04-27

### Added
- 파라미터화 구조 (`DOMAIN`, `STAGE`, `DEPTH`, `LANG`)
- `task_chain` 6단계 CoT 추가
- PE-1 / PE-3 검증 규칙 내장
- KR + EN 병기 출력 포맷
- Domain Variants 3종: FU-Series / B-Star eCO2 / AI Infrastructure
- 저장소 이원화 전략 (Notion Hub + GitHub Engine)

### Changed
- 원본 v2.0 단일 XML → 구조화 MD 포맷으로 전환
- 출력 언어 EN 단일 → KR+EN 병기

---

## [v2.0] — 2026-04 이전 (원본)

### Original
- 8개 core_modules XML 구조
- GP/LP/Fund/IC/Post-Investment/Exit/Risk 섹션
- EN 단일 언어
- 검증 규칙 없음
- 파라미터화 없음
