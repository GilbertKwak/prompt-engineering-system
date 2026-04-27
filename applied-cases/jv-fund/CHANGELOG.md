# CHANGELOG — Global JV Fund Prompt

All notable changes to the JV Fund prompt library are documented here.

---

## [v3.0] — 2026-04-27

### Added
- PE-1 / PE-3 검증 규칙 통합
- 파라미터화: `{DOMAIN}`, `{STAGE}`, `{LP_TYPE}`, `{GEOGRAPHY}`, `{LANG}`, `{DEPTH}`
- KR + EN 병기 출력 포맷
- Domain Variants 3종: `fu_series_adapter.md`, `bstar_eco2_prompt.md`, `ai_infra_prompt.md`
- JSON 출력 스키마 (`executive_summary`, `risk_matrix`, `next_actions`, `github_commands`)
- Notion 연동 링크
- GitHub Actions 워크플로우: `jv_prompt_validate.yml`
- 월간 자동 리뷰 이슈 스케줄 (매월 1일)
- `validation_checklist.md` 추가

### Changed
- 원본 8개 모듈 → Chain-of-Thought 8단계 재구조화
- 출력 언어: EN 단일 → KR + EN 병기
- `output_verbosity_spec` → 의사결정 프레임워크 우선으로 개선
- `high_risk_self_check` → PE-3 시나리오 균형 규칙으로 강화

### Fixed
- 보장 수익률 언어 표현 제거
- 가정 사항 미선언 문제 해결

---

## [v2.0] — 2026-04 이전

### Initial
- 8개 핵심 모듈 포함 기관급 JV 펀드 마스터 프롬프트
- GP/LP 구조, 펀드 규모 설계, IC 프레임워크, Exit 최적화
- 영문 단일 출력
- XML 구조 기반

---

*Maintained by Gilbert Kwak | Prompt Engineering System*
