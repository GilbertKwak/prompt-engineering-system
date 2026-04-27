# JV Fund Master Prompt — 자동 검증 보고서 (Section 1)

> 생성일: 2026-04-27 | 버전: v2 → v3 전환 검증

---

## 1. 전후 비교 (Before vs After)

| 검증 항목 | v2 원본 상태 | 문제점 | v3 개선 방향 |
|---|---|---|---|
| 프롬프트 구조 | 단일 XML 블록 | ROLE/CONTEXT/TASK/OUTPUT 분리 없음 | 4-Block 분리 구조 적용 |
| 버전 관리 | v2 명시, CHANGELOG 없음 | 변경 이력 추적 불가 | CHANGELOG.md 별도 관리 |
| 언어 정책 | 영문 단일 | KR 병행본 없음 | KR+EN Bilingual 출력 지원 |
| 검증 기준 | `high_risk_self_check` 서술형 | PE-1/PE-3 룰 미적용 | Structured Validation Checklist 추가 |
| 출력 포맷 | "Ready for LP-facing" 추상적 | JSON/MD 구조 미지정 | JSON Schema + MD Table 포맷 명시 |
| 재사용성 | 단독 파일 | 모듈화/파라미터화 없음 | `{domain}`, `{stage}`, `{lang}` 파라미터 적용 |
| Domain 연결 | 없음 | FU/sCO2/AI 시리즈와 단절 | Domain Variants 3종 신설 |
| 자동화 연결 | 없음 | GitHub Actions/Notion Sync 미연결 | CI/CD 파이프라인 연결 |

---

## 2. PE-1 검증 결과 (v2 기준)

| PE-1 체크 항목 | v2 상태 | 판정 |
|---|---|---|
| 수치 데이터 출처 명시 | 없음 | ❌ FAIL |
| 연도 기재 (수치 데이터) | 없음 | ❌ FAIL |
| 추정값 (est.) 표기 | 없음 | ❌ FAIL |
| 상반된 시나리오 병기 | Risk module에 서술형으로 일부 존재 | ⚠️ PARTIAL |
| 출처 최소 3개 이상 | 없음 | ❌ FAIL |

**PE-1 점수: 1/5 (20%) → v3 목표: 5/5 (100%)**

---

## 3. PE-3 검증 결과 (v2 기준)

| PE-3 체크 항목 | v2 상태 | 판정 |
|---|---|---|
| 반대 시나리오 1개 이상 | Risk module에 암시적 존재 | ⚠️ PARTIAL |
| 리스크 정량화 | 서술형만 존재 | ❌ FAIL |
| 컨티전시 플레이북 구체성 | 모듈명만 존재, 내용 없음 | ❌ FAIL |

**PE-3 점수: 1/3 (33%) → v3 목표: 3/3 (100%)**

---

## 4. 구조 완성도 평가

| 모듈 | 존재 여부 | 완성도 |
|---|---|---|
| GP_and_Governance_Architecture | ✅ | 60% — 구체적 조항 없음 |
| LP_Segmentation_and_Economic_Terms | ✅ | 55% — 수치 없음 |
| Fund_Structuring_and_Legal_Design | ✅ | 50% — 관할권별 세부 없음 |
| Target_Fund_Size_and_Capital_Engineering | ✅ | 45% — 계산 로직 없음 |
| Investment_Policy_and_IC_Framework | ✅ | 60% — 투표 임계값 없음 |
| Post_Investment_Value_Creation | ✅ | 55% — KPI 없음 |
| Exit_and_Return_Optimization | ✅ | 65% — 수익률 모델 없음 |
| Risk_and_Scenario_Management | ✅ | 40% — 정량 시나리오 없음 |
| Domain Variants (FU/sCO2/AI) | ❌ | 0% — 신규 추가 필요 |
| Automation / CI-CD | ❌ | 0% — 신규 추가 필요 |

**전체 완성도: v2 = 47% → v3 목표 = 90%+**

---

## 5. 즉시 조치 항목

- [ ] `master_prompt_v3.md` 생성 (Phase 2)
- [ ] Domain Variants 3종 생성 (Phase 2)
- [ ] `auto_validate.py` PE-1/PE-3 룰 업데이트 (Phase 3)
- [ ] GitHub Actions 워크플로우 설정 (Phase 3)
- [ ] Notion 페이지 생성 및 동기화 (Phase 4)
