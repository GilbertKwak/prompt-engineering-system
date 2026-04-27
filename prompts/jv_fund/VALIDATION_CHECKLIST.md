# JV Fund Prompt — PE-1 / PE-3 검증 체크리스트

> **버전**: v1.0 | **작성일**: 2026-04-27  
> **적용 범위**: `prompts/jv_fund/` 전체

---

## PE-1 자동 검증 항목 (출력 품질)

### 수치 검증
- [ ] 모든 시장 규모 수치에 출처 명시 (기관명 + 연도)
- [ ] 성장률(CAGR) 추정값에 `(est.)` 표기
- [ ] 재무 프로젝션은 가정 사항 명시
- [ ] 보장 수익률 표현 완전 배제

### 구조 검증
- [ ] 8대 Core Module 모두 포함 여부
- [ ] JSON 출력 포맷 준수
- [ ] Notion 호환 MD 포맷 제공
- [ ] KR+EN 병기 (LANG: KR+EN 설정 시)

### 연결성 검증
- [ ] 관련 GitHub 레포 링크 포함
- [ ] FU-Series / B-Star / AI-Infra 연계 시 참조 번호 기재

---

## PE-3 자동 검증 항목 (리스크 품질)

### 리스크 커버리지
- [ ] 기술 리스크 (Technical Risk) 명시
- [ ] 상업 리스크 (Commercial Risk) 명시
- [ ] 규제 리스크 (Regulatory Risk) 명시 + 관련 법령
- [ ] 지정학적 리스크 (Geopolitical Risk) 명시

### 반대 시나리오
- [ ] 최소 1개 이상의 반대 시나리오 (Downside Scenario) 포함
- [ ] 반대 시나리오에 대한 대응 전략 제시

### LP 관련
- [ ] 수탁 리스크 (Fiduciary Risk) 플래그
- [ ] LP 정렬 리스크 (LP Alignment Risk) 플래그
- [ ] LPAC 설계 포함 여부

---

## 도메인별 추가 검증

### FU-Series 연동 시
- [ ] FU 보고서 번호 + 섹션 인용 명시
- [ ] 기술 TRL 수준 기재
- [ ] AstraChips 전략 시너지 명시

### B-Star eCO₂ 전용 시
- [ ] sCO2 TRL 수준 명시
- [ ] 전기사업법 · 집단에너지법 언급
- [ ] 정부 보조금 프로그램 명시

### AI 인프라 전용 시
- [ ] AI 칩 전력 밀도 데이터 출처
- [ ] 하이퍼스케일러 냉각 CAPEX 인용
- [ ] AstraChips 연계 명시

---

## 검증 점수 산출 기준

| 항목 | 배점 | 합격 기준 |
|---|---|---|
| PE-1 수치 검증 (4개) | 각 10점 = 40점 | 30점 이상 |
| PE-1 구조 검증 (4개) | 각 5점 = 20점 | 15점 이상 |
| PE-3 리스크 커버리지 (4개) | 각 5점 = 20점 | 15점 이상 |
| PE-3 반대 시나리오 (2개) | 각 5점 = 10점 | 5점 이상 |
| PE-3 LP 관련 (3개) | 각 3점 = 10점 | 6점 이상 |
| **합계** | **100점** | **71점 이상** |

---

## 검증 실행 명령어

```bash
# PE-1 검증
python automation/auto_validate.py \
  --file prompts/jv_fund/master_prompt_v3.md \
  --rules PE-1 \
  --checklist prompts/jv_fund/VALIDATION_CHECKLIST.md

# PE-3 검증
python automation/auto_validate.py \
  --file prompts/jv_fund/master_prompt_v3.md \
  --rules PE-3 \
  --output reports/jv_fund_validation_$(date +%Y%m%d).json

# 전체 변형 일괄 검증
python automation/auto_validate.py \
  --dir prompts/jv_fund/ \
  --rules PE-1,PE-3 \
  --report-format markdown
```
