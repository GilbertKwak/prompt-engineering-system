# FU-Series ↔ JV Fund Adapter Prompt

> **버전**: v1.0 | **날짜**: 2026-04-28  
> **연동 대상**: GilbertKwak/fu-semiconductor-thermal (FU-001 ~ FU-025+)  
> **목적**: FU 보고서 데이터를 JV 타당성 분석에 직접 연결

---

## [ROLE]

FU-Series 반도체 열관리 기술 보고서를 기반으로 글로벌 JV 파트너십 타당성을 검증하는 분석가.

---

## [INPUT PARAMETERS]

```yaml
FU_Number: "{fu_number}"          # e.g. FU-008, FU-012
FU_Section: "{section}"           # Market Analysis | Technical Specs | Business Case
JV_Domain: "{jv_domain}"          # 해당 FU 보고서의 기술 영역
Analysis_Date: "{date}"           # YYYY-MM-DD
```

---

## [TASK CHAIN]

### Step 1 | FU 데이터 추출
```
입력: FU-{number} 보고서의 {section} 섹션
추출 항목:
  - 핵심 기술 스펙 및 성능 지표
  - 시장 규모 데이터 (TAM/SAM)
  - 경쟁사 매핑
  - 기술 성숙도(TRL) 수준
```

### Step 2 | JV 타당성 매핑
```
FU 데이터 → JV 분석 전환:
  기술 스펙       → 파트너 역량 요구사항
  시장 규모       → JV 수익 잠재력
  경쟁사 목록     → 잠재 파트너 후보군
  TRL 수준       → 투자 단계 결정
```

### Step 3 | 갭 분석
```
FU 보고서 기준 vs. JV 파트너 현재 역량:
  - 기술 갭 (Technology Gap)
  - 시장 갭 (Market Access Gap)  
  - 재무 갭 (Capital Gap)
  - 인력 갭 (Talent Gap)
```

### Step 4 | JV 구조 권고
```
FU 기반 권고 사항:
  - 최적 파트너 프로필
  - 지분 구조 (기술 기여도 반영)
  - IP 이전 조건
  - 마일스톤 기반 투자 스케줄
```

---

## [OUTPUT]

```markdown
## FU-{number} 기반 JV 분석 결과

### 핵심 기술 포인트 (FU 보고서에서)
- ...

### JV 타당성 점수: {score}/10
- 기술 타당성: {tech_score}/10
- 시장 타당성: {market_score}/10  
- 재무 타당성: {financial_score}/10

### 권고 파트너 프로필
- 기술 역량: ...
- 지역: ...
- 재무 규모: ...

### 다음 단계
1. FU-{number} 기술팀과 파트너 후보 검토 미팅
2. GitHub Issue: `gh issue create --title "[JV-FU-{number}] Partner Screening"`
3. Notion 업데이트: JV Pipeline DB → Screening 단계
```

---

## [RELATED FILES]

- 원본: `GilbertKwak/fu-semiconductor-thermal/`
- JV 마스터: `prompts/jv_fund/master_v3.md`
- 검증: `prompts/jv_fund/validation_checklist.md`
