# Global Joint Venture Fund Master Prompt v2 (Archive)

> ⚠️ **Archived**: 이 파일은 v2 원본 보관본입니다.  
> 현행 버전: [`master_prompt_v3.md`](../master_prompt_v3.md)

---

## Archive Metadata

- **Archive Date**: 2026-04-28
- **Archived By**: Gilbert
- **Reason**: v3.0 업그레이드 — PE-1/PE-3/PE-5 검증 룰, JSON 출력 포맷, 도메인 파라미터화, 파생 프롬프트 분리
- **Original File**: `Global_Joint_Venture_Fund_Master_Prompt_v2.txt`

---

## What Changed in v3

| 항목 | v2 (Before) | v3 (After) |
|---|---|---|
| 구조 | 단일 블록 텍스트 | ROLE/CONTEXT/TASK/OUTPUT/VALIDATION 분리 |
| 버전 관리 | 없음 | CHANGELOG + archive/ 보관 |
| 검증 규칙 | 없음 | PE-1, PE-3, PE-5 적용 |
| 출력 포맷 | 미지정 | JSON + MD 테이블 명시 |
| 파라미터화 | 없음 | {domain}/{stage}/{depth}/{lang} |
| 파생 프롬프트 | 없음 | FU/sCO2/AI 3종 분리 |
| 자동화 | 없음 | auto_validate.py + GitHub Actions |
| 언어 | 영문 | KR/EN 병기 |

---

*원본 내용은 첨부 파일 `Global_Joint_Venture_Fund_Master_Prompt_v2.txt` 참조*
