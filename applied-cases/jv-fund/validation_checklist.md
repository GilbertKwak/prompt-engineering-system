# ✅ JV Fund Prompt 검증 체크리스트

> **버전:** v1.0 | **날짜:** 2026-04-27  
> **적용 대상:** `applied-cases/jv-fund/` 내 모든 프롬프트 파일  
> **검증 기준:** PE-1 (정확성·출처) / PE-3 (시나리오 균형)

---

## PE-1 검증 항목 (정확성·출처 기준)

| # | 항목 | 기준 | 통과 조건 |
|---|---|---|---|
| PE-1-01 | 수치 데이터 출처 명시 | 모든 정량적 수치 | 출처명 + 연도 기재 |
| PE-1-02 | 추정값 태깅 | 추정/예측 수치 | `(est.)` 접미어 |
| PE-1-03 | 보장수익률 금지 | 수익률 표현 | `guaranteed`, `확정` 표현 없음 |
| PE-1-04 | 최소 인용 출처 수 | 전체 출처 | 3개 이상 |
| PE-1-05 | 데이터 기준 시점 | 모든 시장 데이터 | YYYY 또는 YYYY-Q# 형식 |
| PE-1-06 | 통화/환율 기준 | 금융 수치 | 통화 단위 + 기준일 명시 |

---

## PE-3 검증 항목 (시나리오 균형 기준)

| # | 항목 | 기준 | 통과 조건 |
|---|---|---|---|
| PE-3-01 | 3-시나리오 구조 | 전망 섹션 | Bull/Base/Bear 3종 모두 존재 |
| PE-3-02 | 수탁자 의무 리스크 | 거버넌스 섹션 | 명시적 언급 |
| PE-3-03 | 규제 리스크 | 규제 섹션 | 최소 1개 섹션 |
| PE-3-04 | LP 이해충돌 | LP 조건 섹션 | 충돌 항목 명시 |
| PE-3-05 | 반대 시나리오 | 전체 분석 | 약세/부정 케이스 포함 |

---

## 구조 품질 검증

| # | 항목 | 통과 조건 |
|---|---|---|
| SQ-01 | 파라미터 변수 명시 | `{domain}`, `{stage}` 등 주입 가능 구조 |
| SQ-02 | Task Chain 존재 | Step 1~N 순서 명시 |
| SQ-03 | JSON 또는 테이블 출력 포맷 | 구조화된 출력 형식 정의 |
| SQ-04 | 언어 설정 | KR/EN/Bilingual 명시 |
| SQ-05 | 버전 및 날짜 | 파일 상단 메타데이터 존재 |

---

## Domain Variant 검증

| 파일 | PE-1 | PE-3 | 구조 품질 | 특화 파라미터 |
|---|---|---|---|---|
| `master_prompt_v3.md` | ✅ | ✅ | ✅ | {domain}/{stage}/{depth}/{lang} |
| `fu_series_adapter.md` | ✅ | ✅ | ✅ | {FU_NUMBER}/{SECTION}/{JV_STAGE} |
| `bstar_eco2_prompt.md` | ✅ | ✅ | ✅ | {sub_domain}/{geo}/{stage} |
| `ai_infra_prompt.md` | ✅ | ✅ | ✅ | {cooling_type}/{chip}/{geo}/{stage} |

---

## 자동 검증 실행

```bash
# 전체 JV 프롬프트 검증
python automation/auto_validate.py \
  --dir applied-cases/jv-fund/ \
  --rules PE-1,PE-3,SQ \
  --output reports/validation/jv_validation_$(date +%Y%m%d).json

# 특정 파일 검증
python automation/auto_validate.py \
  --file applied-cases/jv-fund/master_prompt_v3.md \
  --rules PE-1,PE-3
```

---

## 월간 리뷰 체크포인트

- [ ] 신규 시장 데이터로 수치 업데이트 필요 여부 확인
- [ ] Domain Variants 성능 점수 비교
- [ ] PE-1/PE-3 새 규칙 추가 필요 여부 검토
- [ ] Notion 연동 페이지 내용 동기화 확인
- [ ] GitHub Actions 워크플로우 정상 실행 여부 확인
