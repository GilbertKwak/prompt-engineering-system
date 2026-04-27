# FU-Series JV Adapter Prompt v1.0

> **Parent**: [master_prompt_v3.md](../master_prompt_v3.md)  
> **Domain**: HBM · Thermal Management  
> **Date**: 2026-04-27 | **PE-3 목표**: 90/100  
> **연동**: [fu-semiconductor-thermal](https://github.com/GilbertKwak/fu-semiconductor-thermal)

---

## 목적

FU-Series 보고서 (FU-001 ~ FU-025+) 데이터를 JV 펀드 분석에 직접 연결하는 어댑터 프롬프트.  
FU 보고서의 기술 분석 결과를 투자 타당성 지표로 변환한다.

---

## [CONTEXT INJECTION]

```yaml
BASE_PROMPT: master_prompt_v3.md
DOMAIN: HBM | Thermal
FU_REPORT_REF: "FU-{number}"   # e.g. FU-008, FU-015
FU_SECTION: "{section}"        # Market-Analysis | Technical-Specs | Commercialization
INPUT_DATA: FU 보고서 해당 섹션 텍스트 (paste)
```

---

## [TASK]

입력된 FU 보고서 섹션을 기반으로 다음을 수행하라:

1. **기술 성숙도 평가**: TRL 수준 → JV 타이밍 적합성 판단
2. **시장 데이터 추출**: FU 보고서 내 수치 → TAM/SAM/SOM 매핑
3. **파트너 후보 도출**: 기술 섹션의 플레이어 → JV 파트너 적합도 재평가
4. **JV 타당성 스코어**: 0-100점 산출 (기술성·시장성·파트너 가용성 가중 평균)
5. **Notion 업데이트 초안**: FU 보고서 페이지에 추가할 JV 분석 섹션 생성

---

## [OUTPUT]

```json
{
  "fu_report": "{FU_REPORT_REF}",
  "section": "{FU_SECTION}",
  "trl_assessment": {
    "current_trl": 0,
    "jv_timing": "Optimal | Early | Late",
    "rationale": ""
  },
  "market_data_extracted": {
    "TAM": {"value": "", "source": "FU-Report"},
    "SAM": {"value": "", "source": "FU-Report"}
  },
  "jv_feasibility_score": {
    "technology": 0,
    "market": 0,
    "partner_availability": 0,
    "total": 0,
    "recommendation": "Proceed | Hold | Pass"
  },
  "notion_update_draft": "## JV 타당성 분석\n{content}",
  "counter_scenario": {
    "assumption": "",
    "failure_case": "",
    "probability": ""
  }
}
```

---

## FU-Series 빠른 참조 인덱스

| FU 번호 | 주제 | JV 관련성 |
|---|---|---|
| FU-008 | HBM4-GPU 패키지 열관리 | 높음 — 냉각 기술 JV |
| FU-015~020 | 첨단 패키징 열관리 | 높음 — OSAT JV |
| FU-001~007 | AI 가속기 열관리 기초 | 중간 — 기술 참조 |

---

*Last updated: 2026-04-27 | prompt-engineering-system/prompts/jv_fund/variants/fu_series_adapter.md*
