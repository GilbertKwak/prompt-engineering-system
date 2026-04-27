# Validation Checklist — JV Fund Prompt
> Version: v3.2 | Updated: 2026-04-27

## PE-1: 정확성·출처 규칙 (6개 항목)

| # | 항목 | 기준 | 상태 |
|---|------|------|------|
| PE-1-01 | 수치 데이터 출처+연도 명시 | 모든 수치에 (Source, YYYY) 태깅 | ✅ |
| PE-1-02 | 추정값 태깅 | (est.) 표기 | ✅ |
| PE-1-03 | 보장 수익률 표현 금지 | "guaranteed", "확정" 사용 불가 | ✅ |
| PE-1-04 | 인용 데이터 최신성 | 최근 2년 이내 우선 | ✅ |
| PE-1-05 | 시장 점유율 기준 명시 | 연도 + 조사기관 | ✅ |
| PE-1-06 | 재무 가정값 분리 | Assumptions 섹션 별도 | ✅ |

## PE-3: 시나리오 균형·리스크 규칙 (5개 항목)

| # | 항목 | 기준 | 상태 |
|---|------|------|------|
| PE-3-01 | 베어리시 시나리오 포함 | 최소 1개 비관 시나리오 | ✅ |
| PE-3-02 | 기술 리스크 명시 | TRL < 6 시 명시 | ✅ |
| PE-3-03 | 수탁자 의무 플래깅 | Fiduciary duty 위험 | ✅ |
| PE-3-04 | 규제·지정학 리스크 | 항목 포함 | ✅ |
| PE-3-05 | LP 이해충돌 명시 | 가능성 기술 | ✅ |

## 구조 품질 (5개 항목)

| # | 항목 | 기준 | 상태 |
|---|------|------|------|
| SQ-01 | XML 파라미터화 | {domain}/{stage}/{depth}/{lang} | ✅ |
| SQ-02 | task_chain CoT | 6단계 순서 완결 | ✅ |
| SQ-03 | output_format 완결성 | JSON + MD + IM 구조 | ✅ |
| SQ-04 | KR+EN 병기 | Bilingual 명시 | ✅ |
| SQ-05 | core_modules 보존 | 원본 v2 8개 유지 | ✅ |

## Domain Variant 개별 점검 (3개)

| # | Variant | PE-1 | PE-3 | 상태 |
|---|---------|------|------|------|
| DV-01 | FU-Series Adapter | ✅ | ✅ | Active |
| DV-02 | B-Star eCO2 | ✅ | ✅ | Active |
| DV-03 | AI Infrastructure | ✅ | ✅ | Active |

## SSOT 동기화

| 저장소 | 최신 버전 | 동기화 상태 |
|--------|-----------|------------|
| GitHub (SSOT) | v3.2 | ✅ Primary |
| Notion (Mirror) | v3.2 | ✅ 동기화됨 |

---

**총 검증 항목:** 19개 / 19개 ✅  
**최종 검증일:** 2026-04-27  
**검증자:** Auto-validated (PE-1 + PE-3 + SSOT)
