# FU-Series Adapter Prompt — JV Fund 연동

<!-- Version: v2.0 | Date: 2026-04-28 -->

## [PURPOSE]

FU-Series 기술 보고서 데이터를 JV Fund 분석에 직접 연결하는 브릿지 프롬프트.

---

## [CONTEXT]

```yaml
FU Report Number: {FU_NUMBER}      # e.g. FU-001, FU-022
Target Section:   {section}        # Market-Analysis | Technical-Specs | Competitive
JV Stage:         {jv_stage}       # Screening | DD | Structuring
```

---

## [TASK]

1. FU-{FU_NUMBER} 보고서의 `{section}` 섹션 데이터 추출
2. 해당 데이터를 JV 타당성 관점으로 재해석
3. 파트너사 역량 평가에 FU 기술 스펙 반영
4. 다음 출력 생성:

### 출력 형식

```markdown
## JV Feasibility — FU-{FU_NUMBER} 기반

### 기술 요약
- 핵심 사양: ...
- 시장 적용성: ...
- 파트너 요구 역량: ...

### JV 타당성 점수
| 항목 | 점수 (1-10) | 근거 |
|---|---|---|
| 기술 성숙도 | X | ... |
| 시장 수요 | X | ... |
| 파트너 가용성 | X | ... |
| 규제 리스크 | X | ... |
| **종합** | **X.X** | ... |

### 권장 액션
1. ...
2. ...
3. ...
```

---

## [VALIDATION]
- [ ] PE-1: FU 보고서 섹션 번호 명시
- [ ] PE-3: 기술 리스크 반대 시나리오 포함
- [ ] FU 버전 번호 및 날짜 기재

---

## [QUICK COMMAND]

```bash
# FU 보고서 JV 분석 이슈 생성
gh issue create \
  --title "[FU-JV] FU-{FU_NUMBER} JV Feasibility Analysis" \
  --label "jv-analysis,fu-series" \
  --body "FU Report: FU-{FU_NUMBER}\nSection: {section}\nJV Stage: {jv_stage}"
```
