# CHANGELOG — JV Fund Prompt Library

## [v3.0] — 2026-04-28

### Added
- `master_prompt_v3.md`: ROLE/CONTEXT/TASK-CHAIN/OUTPUT/VALIDATION 완전 재구조화
- PE-5 검증 룰 신규 추가 (출력 완결성)
- JSON 출력 포맷 명시 (Notion 호환 MD 테이블 병행)
- `{domain}` / `{stage}` / `{depth}` / `{lang}` 파라미터화
- `archive/v2/` — v2 원본 보관
- `automation/auto_validate.py` — PE-1/PE-3/PE-5 자동 검증 스크립트
- `.github/workflows/prompt_validate.yml` — CI 검증 + Notion sync 트리거

### Updated
- `fu_series_adapter.md` → v2.0: FU 보고서 섹션 파라미터화, 출력 포맷 명시
- `bstar_eco2_prompt.md` → v2.0: 3-tier Investment Memo 구조, 파트너 목록 업데이트
- `ai_infra_prompt.md` → v2.0: HBM TDP 수치 업데이트 (B200: 1000W+), PoC 로드맵 추가
- `validation_checklist.md` → v2.0: PE-5 추가, 점수 기준표 포함

### Archived
- `Global_Joint_Venture_Fund_Master_Prompt_v2.txt` → `archive/v2/`

---

## [v2.0] — 2026-04-27

### Added
- `master_prompt_v3.md` (초기 v3 초안)
- `fu_series_adapter.md`, `bstar_eco2_prompt.md`, `ai_infra_prompt.md` (신규)
- `validation_checklist.md`, `README.md`, `CHANGELOG.md`

### Source
- 원본: `Global_Joint_Venture_Fund_Master_Prompt_v2.txt` (사용자 제공)

---

## [v2.0-original] — 2026-04-27 (Archive)

- 원본 파일: `Global_Joint_Venture_Fund_Master_Prompt_v2.txt`
- 구조: 단일 블록 텍스트, 검증 룰 없음, 출력 포맷 미지정
