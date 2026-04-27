# JV Fund Prompt — CHANGELOG

## [v3.0] — 2026-04-27

### Added
- `master_prompt_v3.md`: v2 대비 전면 구조화 (CONTEXT PARAMETERS 파라미터화)
- `variants/fu_series_adapter.md`: FU-Series 보고서 연동 어댑터
- `variants/bstar_eco2_prompt.md`: B-Star sCO2 전용 JV 프롬프트
- `variants/ai_infra_prompt.md`: AI 인프라 열관리 JV 프롬프트
- PE-1 / PE-3 검증 룰 전 파일 적용
- JSON 구조화 출력 포맷 추가
- GitHub CLI 퀵 커맨드 섹션 추가
- Notion 양방향 링크 추가

### Changed
- v2: 단일 XML 블록 → v3: 모듈화 마크다운 + 파라미터화
- 출력 언어: 영문 단일 → KR/EN 병기 (Bilingual 기본)
- 리스크 섹션: 단순 나열 → 3-시나리오 매트릭스 (Base/Bull/Bear)

### Fixed
- v2에서 누락된 출처 표기 (PE-1 준수)
- v2에서 누락된 반대 시나리오 (PE-3 준수)
- 버전 이력 없음 → CHANGELOG 신설

## [v2.0] — 2026-04-27 (보관)

- 원본 파일: `Global_Joint_Venture_Fund_Master_Prompt_v2.txt`
- XML 구조, 8개 Core Module, 영문 단일 출력
- PE 검증 룰 미적용 상태

---

## [향후 계획]

- v3.1: AstraChips LP Fund 피치덱 연동 자동화
- v3.2: auto_validate.py PE-1/PE-3 자동 검증 통합
- v4.0: Multi-Agent 연동 (PE-11 Master Agent 활용)
