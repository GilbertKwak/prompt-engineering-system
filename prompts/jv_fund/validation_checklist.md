# JV Fund Prompt Validation Checklist

> **버전**: v1.0 | **날짜**: 2026-04-28  
> **규칙**: PE-1 (출처 명시) + PE-3 (반대 시나리오)  

---

## PE-1: 출처 및 데이터 품질 검증

```
[ ] 모든 시장 규모 수치에 출처 + 연도 기재
[ ] CAGR / 성장률에 조사기관명 명기 (e.g. IDC, Gartner, Bloomberg)
[ ] 추정값은 반드시 (est.) 또는 (추정) 표기
[ ] 인용 출처 최소 3개 이상
[ ] 데이터 신선도: 최근 2년 이내 우선 (2024~2026)
[ ] 1차 데이터 vs. 2차 데이터 구분
[ ] 상충 데이터 존재 시 복수 출처 병기
```

## PE-3: 반대 시나리오 검증

```
[ ] Downside 시나리오 최소 1개 명시
[ ] 리스크 매트릭스 각 항목에 완화 방안 병기
[ ] 상반된 시장 전망 존재 시 양측 서술
[ ] 기술 실패 시나리오 포함
[ ] 파트너 이탈 시나리오 포함
[ ] 규제 강화 시나리오 포함
```

## 구조 완결성 검증

```
[ ] SYSTEM ROLE 명확히 정의
[ ] 모든 파라미터 변수화 (하드코딩 없음)
[ ] Task Chain 5단계 완비
[ ] OUTPUT FORMAT JSON/MD 명세
[ ] 빠른 참조 명령어 포함
[ ] 관련 파일 링크 명시
[ ] CHANGELOG 업데이트
```

## 도메인별 추가 검증

### FU-Series 연동 시
```
[ ] FU 번호 및 섹션 명시
[ ] TRL 수준 포함
[ ] FU 데이터 → JV 타당성 매핑 완료
```

### B-Star eCO2 시
```
[ ] sCO2 기술 스펙 포함
[ ] 정부 보조금 연계 방안 포함
[ ] 액침냉각 경쟁 기술과 비교
```

### AI 인프라 시
```
[ ] GPU 전력 밀도 트렌드 포함
[ ] 하이퍼스케일러 자체 개발 리스크 포함
[ ] HBM Salvage 연계 가능성 검토
```

---

## 자동 검증 명령어

```bash
# PE-1+PE-3 자동 검증
python automation/auto_validate.py \
  --file prompts/jv_fund/master_v3.md \
  --rules PE-1,PE-3 \
  --output validation_report.json

# 전체 JV 프롬프트 배치 검증
for f in prompts/jv_fund/**/*.md; do
  python automation/auto_validate.py --file $f --rules PE-1,PE-3
done
```

---

## 검증 이력

| 날짜 | 파일 | PE-1 | PE-3 | 구조 | 검증자 |
|------|------|------|------|------|---------|
| 2026-04-28 | master_v3.md | ✅ | ✅ | ✅ | Auto+Gilbert |
| 2026-04-28 | fu_series_adapter.md | ✅ | ✅ | ✅ | Auto+Gilbert |
| 2026-04-28 | bstar_eco2_prompt.md | ✅ | ✅ | ✅ | Auto+Gilbert |
| 2026-04-28 | ai_infra_prompt.md | ✅ | ✅ | ✅ | Auto+Gilbert |
