# JV Fund Prompt Suite — PE-1/PE-3 검증 체크리스트

> **Version**: v1.0 | **Date**: 2026-04-27  
> **적용 범위**: prompts/jv_fund/ 전체 파일

---

## PE-1 검증 체크리스트 (출처·품질)

### 필수 항목 (모두 통과해야 커밋 허용)

- [ ] **수치 출처**: 모든 수치 데이터에 `[출처, YYYY]` 형식 출처 명시
- [ ] **추정값 표기**: 추정값은 반드시 `(est.)` 표기
- [ ] **최신성**: 시장 데이터는 최근 2년 이내 (2024-2026) 우선
- [ ] **교차 검증**: 핵심 수치는 최소 2개 출처 교차 검증
- [ ] **공개 출처**: 파트너 정보는 공개 출처 기반 (IR 공시, 뉴스, 특허 DB)

### 권장 항목

- [ ] 상반된 데이터 존재 시 양쪽 병기
- [ ] 데이터 한계 명시 ("데이터 부족", "추정치")
- [ ] 분석 일자 명시

---

## PE-3 검증 체크리스트 (반대 시나리오)

### 필수 항목

- [ ] **counter_scenario 필드**: JSON 출력에 반드시 포함
- [ ] **주요 가정 3개 이상**: 분석의 핵심 전제 명시
- [ ] **실패 시나리오**: 각 가정 실패 시 결과 기술
- [ ] **확률 등급**: H (High) / M (Medium) / L (Low) 표기
- [ ] **PE-3 자체 점수**: 0-100 출력 (목표: 90 이상)

### PE-3 점수 산정 기준

| 항목 | 배점 | 충족 기준 |
|---|---|---|
| 주요 가정 명시 | 20점 | 3개 이상 |
| 반대 시나리오 기술 | 25점 | 구체적 실패 케이스 |
| 확률 정량화 | 15점 | H/M/L 등급 |
| 리스크 완화 방안 | 20점 | 대응 전략 포함 |
| 출처 교차 검증 | 20점 | 2개 이상 |
| **합계** | **100점** | **목표: 90+** |

---

## 파일별 검증 현황

| 파일 | PE-1 | PE-3 목표 | 최종 검증일 |
|---|---|---|---|
| master_prompt_v3.md | ✅ 구조 내장 | 90/100 | 2026-04-27 |
| variants/fu_series_adapter.md | ✅ 구조 내장 | 90/100 | 2026-04-27 |
| variants/bstar_eco2_prompt.md | ✅ 구조 내장 | 90/100 | 2026-04-27 |
| variants/ai_infra_prompt.md | ✅ 구조 내장 | 90/100 | 2026-04-27 |

---

## 자동 검증 실행 명령어

```bash
# PE-1/PE-3 검증 실행
python automation/auto_validate.py \
  --dir prompts/jv_fund/ \
  --rules PE-1,PE-3 \
  --output validation_report_jv_fund.json

# 결과 확인
cat validation_report_jv_fund.json | python -m json.tool
```

---

## 다음 리뷰 일정

- **정기 리뷰**: 매월 27일
- **트리거 리뷰**: 관련 저장소 (fu-semiconductor-thermal, B-Star-eCO2-Strategy) 주요 업데이트 시
- **GitHub Issue**: `[Monthly Review] JV Fund Prompt` 자동 생성 (매월 1일)

---

*Last updated: 2026-04-27 | prompt-engineering-system/prompts/jv_fund/VALIDATION_CHECKLIST.md*
