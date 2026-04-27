# JV Fund Prompt — PE-1/PE-3 Validation Checklist

> **버전**: v1.0 | **생성일**: 2026-04-27  
> **적용 대상**: `master_prompt_v3.md` + 모든 variants

---

## PE-1 자동개선 체크리스트 (출력 품질)

### 데이터 품질
- [ ] 모든 수치에 출처 + 연도 기재
- [ ] 추정값은 `(est.)` 명시
- [ ] 시장 데이터는 최근 2년 이내 자료 우선
- [ ] 파트너사 정보는 공개 자료 기반 (IR / 언론 / 특허)

### 구조 품질
- [ ] JSON 출력 포맷 완전성 (모든 필드 비어있지 않음)
- [ ] executive_summary 500자 이내 (KR+EN)
- [ ] 리스크 매트릭스 4개 축 (기술/상업/규제/지정학) 모두 작성
- [ ] 로드맵 3단계 (90일/6개월/1년) 모두 작성

### 연계 품질
- [ ] 관련 FU-Series / B-Star / AstraChips 레포지토리 링크 명시
- [ ] Notion 페이지 URL 기재 (해당 시)
- [ ] GitHub 이슈/PR 번호 연결 (해당 시)

---

## PE-3 자동검증 체크리스트 (논리 완결성)

### 필수 요건
- [ ] `counter_scenario` 필드: 반대 시나리오 1개 이상
- [ ] `confidence` 수치: 0.0~1.0 범위 내 출력
- [ ] `pe3_score` 목표: 90/100 이상

### 논리 검증
- [ ] 시장 분석 → 파트너 매핑 → JV 구조 논리적 연계 확인
- [ ] 리스크 대응 전략이 리스크 항목과 1:1 매핑
- [ ] 실행 로드맵이 JV 구조와 정합성 확보

### 편향 방지
- [ ] 긍정 시나리오와 부정 시나리오 균형 유지
- [ ] 특정 파트너사 편향 없음 (3개 이상 비교)
- [ ] 지역 편향 없음 (최소 2개 지역 커버)

---

## 점수 산정 기준

| 항목 | 배점 | 합격 기준 |
|---|---|---|
| 데이터 품질 (PE-1) | 30점 | 27점 이상 |
| 구조 품질 (PE-1) | 25점 | 22점 이상 |
| 논리 완결성 (PE-3) | 30점 | 27점 이상 |
| 편향 방지 (PE-3) | 15점 | 13점 이상 |
| **합계** | **100점** | **90점 이상** |

---

## 자동 실행 명령어

```bash
# 검증 실행
python automation/auto_validate.py \
  --file prompts/jv_fund/master_prompt_v3.md \
  --rules PE-1,PE-3 \
  --output reports/validation/jv_fund_v3_validation.json

# 전체 variants 일괄 검증
for f in prompts/jv_fund/variants/*.md; do
  python automation/auto_validate.py --file "$f" --rules PE-1,PE-3
done
```
