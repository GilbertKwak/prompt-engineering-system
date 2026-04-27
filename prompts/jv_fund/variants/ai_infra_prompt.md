# AI Infrastructure DC JV Prompt v1.0

> **Parent**: [master_prompt_v3.md](../master_prompt_v3.md)  
> **Domain**: AI Data Center Thermal & Infrastructure  
> **Date**: 2026-04-27 | **PE-3 목표**: 90/100  
> **연동**: [global-semiconductor-ai-research](https://github.com/GilbertKwak/global-semiconductor-ai-research)

---

## 목적

AI 데이터센터 냉각 및 인프라 분야의 JV 펀드 기회를 분석하는 특화 프롬프트.  
H100/B200/GB200 수준 GPU 클러스터의 열관리 수요를 JV 투자 기회로 전환한다.

---

## [CONTEXT INJECTION]

```yaml
BASE_PROMPT: master_prompt_v3.md
DOMAIN: AI-DC
COOLING_TYPE: "{type}"       # Liquid | Immersion | Air | Hybrid
GPU_GENERATION: "{gen}"      # H100 | B200 | GB200 | Next-Gen
DC_SCALE: "{scale}"          # Edge | Regional | Hyperscale
GEO_FOCUS: "{geo}"           # Korea | Japan | SEA | US
```

---

## [TASK — AI DC 특화]

### Step 1 — AI DC 냉각 수요 정량화
```
- 글로벌 AI DC 투자 규모 (2025-2030, 출처 명시)
- GPU당 열밀도 증가 트렌드 (W/chip 기준)
- 냉각 인프라 CAPEX 비중 분석
- 한국 주요 하이퍼스케일러 투자 계획 (삼성, SK, KT, 카카오)
```

### Step 2 — 냉각 기술 파트너 매핑
```
국내:
- 삼성전자 (내부 냉각 솔루션)
- SK하이닉스 (HBM 패키지 열관리)
- 한화시스템 (DC 인프라)

글로벌:
- Vertiv Holdings (랙 레벨 쿨링)
- Schneider Electric (전력·냉각 통합)
- Asetek, LiquidStack (액침 냉각)
- nVent, CoolIT (직접 액체냉각)
```

### Step 3 — AI DC JV 구조 옵션
```
Option A: 냉각 기술 JV (한국 R&D + 글로벌 유통)
Option B: DC 운영 JV (하이퍼스케일러 + 기술 공급사)
Option C: 통합 솔루션 JV (반도체 + 냉각 + 전력)
→ 각 옵션의 IRR, 회수 기간, IP 구조 비교
```

### Step 4 — AstraChips 연계 분석
```
- AstraChips HBM Salvage → AI DC 냉각 모듈 재활용 가능성
- Salvage HBM을 AI Edge DC 메모리로 재포지셔닝
- JV 파트너에 대한 AstraChips 공급 계약 구조
```

---

## [OUTPUT]

```json
{
  "domain": "AI-DC",
  "demand_quantification": {
    "global_ai_dc_investment": {"value": "", "period": "2025-2030", "source": ""},
    "thermal_density_trend": {"current_W_per_chip": "", "2027_projection": ""},
    "cooling_capex_share": {"percentage": "", "note": "est."}
  },
  "technology_readiness": {
    "liquid_cooling_TRL": "",
    "immersion_TRL": "",
    "jv_timing_recommendation": ""
  },
  "jv_options": [
    {
      "option": "A",
      "structure": "",
      "IRR_target": "",
      "payback_years": 0,
      "pros": [],
      "cons": []
    }
  ],
  "astrachips_linkage": {
    "salvage_hbm_use_case": "",
    "supply_contract_structure": "",
    "revenue_potential": {"value": "", "note": "est."}
  },
  "counter_scenario": {
    "assumption": "AI DC 투자가 2025-2030 지속 성장 가정",
    "failure_case": "AI 버블 붕괴 또는 에너지 규제 강화 시 수요 급감",
    "probability": "L-M"
  },
  "next_actions": []
}
```

---

*Last updated: 2026-04-27 | prompt-engineering-system/prompts/jv_fund/variants/ai_infra_prompt.md*
