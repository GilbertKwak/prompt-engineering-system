# JV Fund Prompt — PE-1/PE-3 검증 체크리스트

> **버전**: v1.0 | **기준일**: 2026-04-27  
> **적용 범위**: prompts/jv_fund/ 전체

---

## [PE-1 자동개선 체크리스트] — 수치 출처 의무화

### 시장 수치 검증
- [ ] TAM/SAM/SOM 수치에 출처 명시 (기관명 + 연도)
- [ ] CAGR 수치에 예측 기관 명시
- [ ] 추정값은 `(est.)` 또는 `(추정)` 표기
- [ ] 수치 범위 제시 시 최소-최대 근거 포함
- [ ] 오래된 데이터(2년 이상) 사용 시 경고 표시 ⚠️

### 기술 수치 검증
- [ ] TRL(기술성숙도) 수준 명시
- [ ] 성능 수치(W/mK, TDP, COP 등) 출처 포함
- [ ] 특허 수 기재 시 검색 기준일 명시
- [ ] 제조 비용 추정 시 가정(Assumption) 명시

### 재무 수치 검증
- [ ] 투자 금액 환율 기준 명시 (KRW/USD/SGD)
- [ ] ROI/IRR 계산 시 가정 조건 명시
- [ ] 비교 대상 기업 재무 데이터 출처 명시

---

## [PE-3 자동검증 체크리스트] — 반대 시나리오 의무화

### 시장 리스크
- [ ] 시장 축소 시나리오 1개 이상 명시
- [ ] 주요 경쟁자 반격 시나리오 포함
- [ ] 규제 강화 시나리오 (수출통제/환경규제) 포함
- [ ] 지정학적 리스크 (미-중 갈등, 한-일 관계) 분석

### JV 구조 리스크
- [ ] JV 실패 케이스 (파트너 역량 부족) 명시
- [ ] IP 분쟁 시나리오 포함
- [ ] 지분 분쟁 해결 메커니즘 명시
- [ ] Exit 조건 미달 시 대안 명시

### 기술 리스크
- [ ] TRL 진입 실패 시나리오 포함
- [ ] 대체 기술 출현 리스크 분석
- [ ] 핵심 인력 이탈 리스크 언급

---

## [PE-10 v2.0 표준 — EVIDENCE 필드]

- [ ] 각 분석 섹션에 `evidence` 서브필드 포함
- [ ] `confidence_score` 수치 출력 (0~100)
- [ ] `EDGE_CASE` 핸들러 포함 (예외 상황 처리)
- [ ] `synthesis_confidence` 최종 종합 신뢰도 출력

---

## [출력 품질 기준]

| 항목 | 최소 기준 | 권장 기준 |
|---|---|---|
| PE-3 점수 | 80/100 이상 | 90/100 이상 |
| confidence_score | 70 이상 | 85 이상 |
| 출처 수 | 3개 이상 | 5개 이상 |
| 반대 시나리오 | 1개 이상 | 3개 이상 |
| 리스크 매트릭스 항목 | 5개 이상 | 10개 이상 |

---

## [자동 검증 스크립트 연동]

```bash
# 단일 파일 검증
python engines/auto_validate.py \
  --file prompts/jv_fund/master_prompt_v3.md \
  --rules PE-1,PE-3,PE-10 \
  --output reports/validation_$(date +%Y%m%d).json

# 전체 jv_fund 디렉터리 검증
python engines/auto_validate.py \
  --dir prompts/jv_fund/ \
  --rules PE-1,PE-3 \
  --report-format markdown

# Notion 검증 결과 동기화
python automation/notion_sync.py \
  --source reports/validation_$(date +%Y%m%d).json \
  --target notion://JV-Fund-Validation-Log
```

---

## [관련 파일]

| 파일 | 경로 | 설명 |
|---|---|---|
| Master Prompt v3 | `prompts/jv_fund/master_prompt_v3.md` | 핵심 마스터 프롬프트 |
| FU-Series 어댑터 | `prompts/jv_fund/variants/fu_series_adapter.md` | FU 보고서 연동 |
| B-Star eCO2 | `prompts/jv_fund/variants/bstar_eco2_prompt.md` | sCO2 JV 특화 |
| AI 인프라 | `prompts/jv_fund/variants/ai_infra_prompt.md` | AI DC JV 특화 |
| 자동 검증 엔진 | `engines/auto_validate.py` | PE-1/PE-3 검증 |
| Notion 동기화 | `automation/notion_sync.py` | Notion 연동 |
