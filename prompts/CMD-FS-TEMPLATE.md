# CMD-FS · Financial-Semiconductor Command Template

**Domain**: Financial Signal × Semiconductor Supply Chain  
**Version**: v2.0.0  
**Updated**: 2026-05-17  
**Pipeline Integration**: `pe_ai_ecosystem_pipeline.yml` (Infra Layer)

---

## Command Registry

| CMD ID | Description | Layer Link | Output |
|--------|-------------|------------|--------|
| CMD-FS-01 | HBM/CoWoS 공급 타이트니스 스코어 | Infra | score_0-100 |
| CMD-FS-02 | 파운드리 캐파 할당 리스크 매트릭스 | Infra | risk_matrix.json |
| CMD-FS-03 | GraphSAGE 노드-엣지 전체 맵 시각화 | Infra + GNN | graph_map.png |
| CMD-FS-04 | 반도체 공급망 충격 시뮬레이션 | Infra | scenario_delta |
| CMD-FS-05 | 장비·소재 알파 신호 스크리닝 | Infra + Market | alpha_signal |

---

## Prompt Template — CMD-FS (v2)

```
[ROLE]
You are a semiconductor supply chain intelligence analyst with GraphSAGE-3L
node embedding expertise and financial signal integration capabilities.

[COMMAND]
{{CMD_ID}} — {{CMD_DESCRIPTION}}

[CONTEXT]
- Target: {{TARGET}}  (e.g. TSMC, Samsung Foundry, SK Hynix)
- Reference Layer: Infrastructure (weight 0.25 in AI Ecosystem composite)
- GNN Knowledge Graph: v4.3  (28 nodes × 41 edges, last updated {{KG_DATE}})
- Cascade Risk Baseline: −18.3pp (PE-MIN HHI S3 trigger active)

[TASK — CMD-FS-01: Supply Tightness Score]
Compute HBM/CoWoS supply tightness for {{TARGET}}:
1. Node importance score (GraphSAGE layer-3 embedding norm)
2. Edge weight sum (SUPPLY type edges incident to {{TARGET}})
3. Demand pressure index (AI accelerator capex commitments ÷ available CoWoS capacity)
4. Tightness Score = (node_importance × 0.4) + (edge_weight_avg × 0.3)
                   + (demand_pressure × 0.3)
Return JSON:
{
  "target": "{{TARGET}}",
  "tightness_score": 0.0,
  "node_importance": 0.0,
  "edge_weight_avg": 0.0,
  "demand_pressure": 0.0,
  "bottleneck_nodes": ["node_1", "node_2"],
  "risk_flag": "HIGH | MEDIUM | LOW",
  "signal": "SUPPLY_CRUNCH | BALANCED | OVERSUPPLY"
}

[TASK — CMD-FS-03: GraphSAGE Node-Edge Map]
Generate full node-edge visualization spec:
1. 5-sector layout: Equipment / Foundry / Chemical / Memory / Logic
2. Node encoding: size = importance, border = alpha signal
   (white=BUY, gold=NEUTRAL, red=AVOID)
3. Edge encoding: color by type
   SUPPLY=blue, PROCESS=green, RISK=red
4. Highlight cascade path from SMIC RISK edges
5. Return Plotly/NetworkX compatible JSON spec

[OUTPUT CONSTRAINTS]
- All numeric scores: 0–100 range
- Node names: use canonical IDs from KG v4.3
- Cascade paths: list ordered from source to sink
- No null values; use 0.0 as default

[AI ECOSYSTEM LAYER LINKAGE]
- This CMD-FS output feeds: PE-AI-ECO-01 Layer 1 (Infra) composite score
- Downstream: ai_ecosystem_synthesizer.py reads infra_*.json
- Cross-validation: PE-SEMI-01 corroboration required for risk_flag=HIGH
```

---

## Scoring Rubric (v2 update)

| Metric | Weight | Source |
|--------|--------|--------|
| Node Importance (GraphSAGE L3) | 0.40 | GNN KG v4.3 |
| Supply Edge Weight Avg | 0.30 | KG edge attributes |
| Demand Pressure Index | 0.30 | Capex/Capacity ratio |

**Signal Thresholds**:
- `tightness_score ≥ 75` → `SUPPLY_CRUNCH` (AVOID downstream)
- `tightness_score 45–74` → `BALANCED` (NEUTRAL)
- `tightness_score < 45` → `OVERSUPPLY` (BUY opportunity)

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| v2.0.0 | 2026-05-17 | AI Ecosystem pipeline 연동, PE-AI-ECO-01 Layer 1 입력 명세 추가 |
| v1.2.0 | 2026-04-30 | CMD-FS-03 GraphSAGE 시각화 스펙 추가 |
| v1.1.0 | 2026-03-15 | GNN KG v4.3 노드 28개 기준 갱신 |
| v1.0.0 | 2026-01-10 | 최초 생성 |

---

## Integration Map

```
CMD-FS (this file)
  └── feeds ──▶ PE-AI-ECO-01 [Layer 1: Infra]
                  └── feeds ──▶ ai_ecosystem_synthesizer.py
                                  └── feeds ──▶ Notion Sync (Stage 4)

Cross-references:
  PE-SEMI-01   ← corroboration for SUPPLY_CRUNCH signals
  PE-MIN-01    ← HHI cascade risk (S3 trigger: −18.3pp)
  CMD-JV-01    ← SK On JV structuring inputs Infra tightness score
```
