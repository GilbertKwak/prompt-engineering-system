# FU-Series JV Adapter Prompt

> **Version:** v1.0  
> **Date:** 2026-04-28  
> **Parent:** master_prompt_v3.md  
> **Scope:** FU-001 ~ FU-025+ 시리즈 연동 JV 타당성 분석  

---

## [PURPOSE]

FU-Series 기술 보고서의 분석 데이터를 JV 펀드 타당성 검토에 직접 연결하는 어댑터 프롬프트입니다.  
FU 보고서의 시장 분석 / 기술 스펙 섹션을 입력값으로 받아, JV 구조 권고안을 자동 생성합니다.

---

## [INPUT PARAMETERS]

```yaml
FU_NUMBER: "{fu_number}"        # e.g. FU-008, FU-015
FU_SECTION: "{section}"         # Market-Analysis | Technical-Specs | Business-Case
JV_STAGE: "{stage}"             # Screening | DD | Structuring
TARGET_PARTNER_REGION: "{region}" # KR | US | EU | JP
```

---

## [ADAPTER CHAIN]

### Step 1: FU 보고서 데이터 추출
```
[FU-{fu_number}] 보고서에서 다음을 추출하라:
- 시장 규모 (TAM/SAM) 수치
- 핵심 기술 파라미터 (TRL 수준)
- 경쟁사 분석 결과
- 사업화 권고 타임라인
```

### Step 2: JV 타당성 매핑
```
추출된 FU 데이터를 기반으로:
1. JV 파트너 후보 선정 기준 도출
2. 기술 시너지 점수 계산 (0~10)
3. 시장 진입 전략 (단독 vs JV vs 라이선싱) 비교
```

### Step 3: 권고 출력
```json
{
  "fu_reference": "FU-{fu_number}",
  "jv_feasibility_score": 0,
  "recommended_structure": "...",
  "top_3_partners": [],
  "synergy_matrix": {},
  "next_step": "master_prompt_v3.md Step 3으로 진행"
}
```

---

## [VALIDATION]
- [ ] FU 보고서 버전 확인 (최신본 참조)
- [ ] 기술 파라미터 단위 일치 여부 확인
- [ ] PE-1: 수치 출처 FU 보고서 섹션 명시

---

## [LINKED FU REPORTS]

| FU 번호 | 주제 | JV 연관성 |
|---|---|---|
| FU-008 | HBM4-GPU Thermal | HBM Salvage JV |
| FU-015 | Vapor Chamber Advanced | Thermal JV |
| FU-021 | sCO2 Cooling Integration | B-Star JV |
| FU-025 | AI DC Thermal | AI Infra JV |

---

*Parent: prompts/jv_fund/master_prompt_v3.md*
