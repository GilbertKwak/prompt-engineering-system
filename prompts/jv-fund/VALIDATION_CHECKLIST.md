# JV Fund Prompt 검증 체크리스트

> **버전**: v1.0 | **날짜**: 2026-04-28  
> **적용 대상**: master_prompt_v3.md 및 모든 파생 프롬프트

---

## PE-1 검증 — 수치·출처 정확성

```
[ ] 1. 모든 시장 규모 수치에 출처 명시 (최소 3개)
[ ] 2. CAGR 데이터는 조사 기관명 + 연도 기재
[ ] 3. 추정값은 반드시 (est.) 또는 (proj.) 표기
[ ] 4. 비교 데이터는 동일 기준연도 사용
[ ] 5. 기업별 재무 수치는 최신 공시 기준
[ ] 6. 환율 기준 명시 (USD/KRW 기준일)
```

## PE-3 검증 — 반대 시나리오

```
[ ] 1. Bear Case 시나리오 1개 이상 포함
[ ] 2. 주요 가정의 민감도 분석 수행
[ ] 3. 실패 요인 Top 3 명시
[ ] 4. 조기 경고 신호(Early Warning Indicators) 정의
[ ] 5. 대응 전략(Contingency Plan) 제시
```

## 구조 검증

```
[ ] 1. 5단계 Task Chain 모두 포함
[ ] 2. JSON 출력 구조 완전성 확인
[ ] 3. Notion 호환 MD 테이블 포함
[ ] 4. GitHub Issue/PR 생성 명령어 포함
[ ] 5. 버전 및 날짜 메타데이터 기재
[ ] 6. KR/EN 병기 여부 확인
```

## 자동 검증 실행 명령어

```bash
# 로컬 실행
python automation/auto_validate.py \
  --file prompts/jv-fund/master_prompt_v3.md \
  --rules PE-1,PE-3 \
  --output reports/validation_$(date +%Y%m%d).json

# 전체 jv-fund 폴더 일괄 검증
python automation/auto_validate.py \
  --dir prompts/jv-fund/ \
  --rules PE-1,PE-3 \
  --report
```

---

## 검증 이력

| 날짜 | 검증자 | 결과 | 비고 |
|---|---|---|---|
| 2026-04-28 | Gilbert (AI 보조) | PASS | 최초 검증 |

---

*이 파일은 모든 JV Fund 프롬프트 배포 전 반드시 체크합니다.*
