# FU-Series Report Adapter Prompt v1.0

> **Version**: v1.0  
> **Date**: 2026-04-27  
> **Parent**: `master_prompt_v3.md`  
> **Purpose**: FU-Series 보고서(FU-001~FU-025+) 데이터를 JV 펀드 분석에 직접 연동  

---

## [CONTEXT]

```yaml
parent_prompt: master_prompt_v3.md
fu_report_number: "{FU_NUMBER}"   # e.g. FU-019, FU-022
fu_section: "{FU_SECTION}"        # Market-Analysis | Technical-Specs | Thermal-Data
domain: "{domain}"                # HBM | Thermal | sCO2 | AI-DC
```

---

## [TASK]

```
INPUT:
  FU-Series 보고서 #{FU_NUMBER}의 [{FU_SECTION}] 섹션 데이터

TASK:
  1. FU 보고서 데이터를 기반으로 JV 타당성 재검증
  2. 시장 규모/성장률 데이터를 Master Prompt Step 1에 자동 연결
  3. 기술 스펙 데이터를 리스크 매트릭스(Step 4)에 반영
  4. 불일치 데이터 플래그 (⚠️ Conflict: ...)

OUTPUT:
  - Notion 페이지 업데이트 초안 (MD 포맷)
  - GitHub PR 본문 초안
  - 충돌 데이터 리스트 (있을 경우)
```

---

## [CHAIN]

```
Step 1 → FU 보고서에서 핵심 수치 추출
  (TAM, CAGR, 기술 TRL, 예상 시장 진입 시점)

Step 2 → JV Master Prompt Step 1~4에 데이터 매핑
  - 수치 충돌 시 ⚠️ 플래그 + 양쪽 출처 병기

Step 3 → JV 타당성 스코어 산출 (1~10점)
  - 기술 성숙도 × 시장 규모 × 파트너 역량

Step 4 → 권장 액션 생성
  - Notion 업데이트 항목
  - GitHub Issue 생성 명령어
```

---

## [OUTPUT FORMAT]

```markdown
## FU-{FU_NUMBER} × JV Fund 연동 분석

### 추출 데이터
| 항목 | FU 보고서 값 | JV 분석 반영값 | 충돌 여부 |
|---|---|---|---|
| TAM | | | |
| CAGR | | | |
| TRL | | | |

### JV 타당성 스코어: {SCORE}/10
- 기술 성숙도: {x}/10
- 시장 규모: {x}/10  
- 파트너 역량: {x}/10

### 권장 액션
1. ...
2. ...
3. ...
```

---

## [GITHUB ISSUE TEMPLATE]

```bash
gh issue create \
  --title "[FU-{FU_NUMBER} × JV] 연동 분석 결과 검토" \
  --label "jv-analysis,fu-series,review" \
  --body "FU-{FU_NUMBER} 데이터 기반 JV 타당성 분석 완료. 검토 요망."
```
