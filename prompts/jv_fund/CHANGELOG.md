# CHANGELOG — JV Fund Prompt Series

모든 버전 변경 이력을 기록합니다.

---

## [v3.0] — 2026-04-28

### Added
- Master Prompt v3.0 (PE-1/PE-3 검증 내장)
- Variant A: FU-Series 연동 특화 프롬프트
- Variant B: B-Star sCO2 전용 프롬프트
- Variant C: AI Infrastructure 특화 프롬프트
- validation_checklist.md — 통합 검증 체크리스트
- 5단계 Task Chain 프레임워크
- YAML Context Parameters 구조화
- Notion MD 호환 출력 포맷
- GitHub Issue 자동 생성 명령 통합

### Changed
- v2 단일 블록 텍스트 → v3 구조화된 모듈 형식
- 역할/맥락/출력 섹션 분리
- KR+EN 병기 옵션 추가

### Fixed
- 버전 관리 체계 신설 (이전 v2에 없음)
- PE-1/PE-3 검증 룰 적용 (이전 없음)
- 도메인별 특화 로직 분리 (이전 단일 프롬프트)

---

## [v2.0] — 2026-04-27 (원본)

### Notes
- 원본 파일: `Global_Joint_Venture_Fund_Master_Prompt_v2.txt`
- 단일 블록 텍스트 구조
- PE 검증 미적용
- Domain Variants 없음
- 버전 이력 없음

---

## [예정] v3.1 — 자동화 연동 업그레이드

### Planned
- [ ] `auto_validate.py` PE-1/PE-3 자동 검증 스크립트 연동
- [ ] GitHub Actions 워크플로우 (push → validate → Notion sync)
- [ ] Notion API 자동 동기화 구현
- [ ] 월간 성능 리뷰 Issue 자동 생성
- [ ] Variant D: HBM Salvage 전용 (AstraChips 직결)

---

*CHANGELOG v1.0 — GilbertKwak/prompt-engineering-system*
