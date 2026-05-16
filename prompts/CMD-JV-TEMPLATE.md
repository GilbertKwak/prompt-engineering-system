# CMD-JV · Joint Venture / Financial Restructuring Command Template

**Domain**: JV Structuring × Financial Scenario Modeling  
**Version**: v2.0.0  
**Updated**: 2026-05-17  
**Pipeline Integration**: `pe_ai_ecosystem_pipeline.yml` (Market Layer)

---

## Command Registry

| CMD ID | Description | Layer Link | Output |
|--------|-------------|------------|--------|
| CMD-JV-01 | SK On 재무 구조 조정 시나리오 | Market + Infra | scenario_matrix |
| CMD-JV-02 | JV 파트너 적합성 스코어링 | Market | partner_score |
| CMD-JV-03 | 분사·IPO 적정 밸류에이션 | Market + FIN | valuation_range |
| CMD-JV-04 | 광물충격 스트레스 테스트 | Market + MIN | stress_delta |
| CMD-JV-05 | 회사채 리파이낸싱 리스크 | Market + FIN | refi_risk_score |

---

## Prompt Template — CMD-JV (v2)

```
[ROLE]
You are a senior restructuring advisor and financial scenario modeler
specializing in battery/EV supply chain JV structures and distressed asset analysis.

[COMMAND]
{{CMD_ID}} — {{CMD_DESCRIPTION}}

[CONTEXT]
- Target Company: {{TARGET}}  (default: SK On)
- Reference Layer: Market & Competitive (weight 0.20 in AI Ecosystem composite)
- GNN Cascade Score: −18.3pp  (PE-MIN HHI S3 active, Samsung_F S3→S4 prob 0.569)
- Base Year: 2025A  |  Forecast Horizon: 2026F–2029F

[SCENARIO DEFINITIONS]

Scenario A — JV 파트너 유치 (Ford / VW 공동투자)
  Assumptions:
  - CAPEX sharing ratio: 35% partner contribution
  - Revenue uplift: +23% by 2029F (committed offtake)
  - Net debt reduction: partner equity injection KRW 3.0T (2027F)
  - irr_adj threshold: +131bps above Base for "JV_PREFERRED" signal
  Key risks: partner credit quality, technology IP clauses, termination provisions

Scenario B — 분사·상장 (SK이노베이션 분리 + IPO)
  Assumptions:
  - IPO proceeds: KRW 2.0–3.5T (2027F, Kospi)
  - Net debt post-IPO: KRW 4.5T (minimum)
  - Revenue growth cap: +5% CAGR (standalone, no committed offtake)
  - Trigger: debt/EBITDA < 3.0× required for investment-grade rating
  Key risks: market window, valuation discount vs. peers, governance separation

Scenario C — 無재조정 + 광물충격 (Base stress)
  Assumptions:
  - Lithium carbonate price shock: +40% YoY (2027F)
  - EBITDA re-entry to negative: 2027F
  - Net debt breach: KRW 22T+ (2028F)
  - Bond refinancing risk: triggers PE-MIN HHI S4 cascade
  Key risks: covenant breach, credit rating downgrade, counterparty termination clauses

Scenario D — Base (no restructuring, no shock)
  Assumptions:
  - Revenue CAGR: +12% (2026F–2029F)
  - EBITDA margin recovery: 6%→12% by 2029F
  - Net debt: KRW 12.8T (2029F)
  - CAPEX: KRW 4.0T/year flat

[TASK — CMD-JV-01: Scenario Matrix Output]
For each scenario A/B/C/D, compute 2026F–2029F:
1. Revenue (KRW 조원)
2. EBITDA (KRW 조원)
3. Net Debt (KRW 조원)
4. CAPEX (KRW 조원/year)
5. EBITDA margin %
6. Net Debt / EBITDA ratio
7. Scenario signal: JV_PREFERRED | IPO_STABLE | STRESS_WATCH | BASE

Return JSON:
{
  "target": "{{TARGET}}",
  "base_year": "2025A",
  "scenarios": {
    "A": {"2026F": {...}, "2027F": {...}, "2028F": {...}, "2029F": {...}, "signal": "JV_PREFERRED"},
    "B": {"2026F": {...}, "2027F": {...}, "2028F": {...}, "2029F": {...}, "signal": "IPO_STABLE"},
    "C": {"2026F": {...}, "2027F": {...}, "2028F": {...}, "2029F": {...}, "signal": "STRESS_WATCH"},
    "D": {"2026F": {...}, "2027F": {...}, "2028F": {...}, "2029F": {...}, "signal": "BASE"}
  },
  "recommended_path": "A | B | D",
  "irr_adj_bps": 0,
  "gnn_cascade_linkage": "Samsung_F S3→S4 prob: 0.569 if Scenario C triggered"
}

[OUTPUT CONSTRAINTS]
- All financials in KRW 조원, 1 decimal place
- EBITDA margin in %, 1 decimal place
- Signal must match threshold logic above
- recommended_path must exclude Scenario C unless all other paths blocked

[AI ECOSYSTEM LAYER LINKAGE]
- CMD-JV output feeds: PE-AI-ECO-01 Layer 4 (Market) composite score
- Downstream: ai_ecosystem_synthesizer.py reads market_*.json
- Cross-validation: PE-FIN-01 (financial modeling) + PE-STRAT-01 (strategic analysis)
- GNN trigger: Scenario C activation → PE-MIN HHI S3 cascade → infra layer re-score
```

---

## 2029F Reference Targets (v2 update)

| 지표 | Base | A: JV | B: IPO | C: Stress |
|------|-----:|------:|-------:|----------:|
| 매출 (조원) | 17.0 | 21.0 | 17.8 | 13.2 |
| EBITDA (조원) | +6.1 | +10.5 | +7.2 | −0.5 |
| 순부채 (조원) | 12.8 | 6.5 | 4.5 | 25.3 |
| CAPEX (조원) | 4.0 | 2.8 | 3.4 | 5.5 |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| v2.0.0 | 2026-05-17 | AI Ecosystem pipeline 연동, PE-AI-ECO-01 Layer 4 입력 명세 추가 |
| v1.1.0 | 2026-04-30 | CMD-JV-01 SK On 4-scenario matrix 완성, 2029F 기준값 확정 |
| v1.0.0 | 2026-02-20 | 최초 생성 |

---

## Integration Map

```
CMD-JV (this file)
  └── feeds ──▶ PE-AI-ECO-01 [Layer 4: Market]
                  └── feeds ──▶ ai_ecosystem_synthesizer.py
                                  └── feeds ──▶ Notion Sync (Stage 4)

Cross-references:
  PE-FIN-01    ← financial modeling (DCF, LBO)
  PE-STRAT-01  ← strategic analysis (M&A, JV structure)
  CMD-FS-01    ← Infra tightness inputs Scenario C stress multiplier
  PE-MIN-01    ← mineral shock HHI cascade (Scenario C trigger)

Scenario C activation cascade:
  CMD-JV-01 Scenario C
    └──▶ PE-MIN HHI S3 active
          └──▶ Samsung_F S3→S4 cascade prob 0.569
                └──▶ CMD-FS infra score re-scored (−delta)
                      └──▶ PE-AI-ECO overall score downgrade
```
