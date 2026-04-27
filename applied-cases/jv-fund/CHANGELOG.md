# CHANGELOG — JV Fund Prompt Library

## [v3.2] 2026-04-27
### Added
- auto_validate.py (PE-1/PE-3 자동검증 스크립트) 연동
- GitHub Actions workflow (`jv_prompt_validate.yml`) 추가
- SSOT 재검증 완료 (10개 항목 강화)
- 원본 v2 대비 전후(Before/After) 비교 분석 문서화
- Notion 페이지 v3.2 동기화 완료

### Changed
- master_prompt_v3.md: PE-1 6개 + PE-3 5개 검증 규칙 상세화
- output_format: Notion JSON Block + GitHub Issue Body 포맷 추가
- core_modules: 원본 v2 8개 모듈 명시적 보존 확인

### Validated
- PE-1: ✅ 6/6 항목
- PE-3: ✅ 5/5 항목
- SSOT: ✅ GitHub ↔ Notion 동기화 확인

---

## [v3.1] 2026-04-27
### Added
- Domain Variants 3종 (FU-Series / B-Star eCO2 / AI Infra)
- 저장소 이원화 전략 확정 (Notion Hub + GitHub Engine)
- 활용 명령어 alias 추가

### Changed
- README.md 업데이트

---

## [v3.0] 2026-04-27
### Added
- PE-1/PE-3 검증 규칙 최초 도입
- XML 파라미터화 ({domain}/{stage}/{depth}/{lang})
- KR+EN 병기 출력 포맷
- task_chain 6단계 CoT 구조
- validation_checklist.md 신규

### Changed
- 원본 v2 → v3.0 자동개선·자동증식 완료

---

## [v2.0] 2026-04 이전
- 원본 파일: Global_Joint_Venture_Fund_Master_Prompt_v2.txt
- 8개 core_module 구조 (EN 단일, 검증 규칙 없음)
