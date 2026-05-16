# PE-AI-ECO-01 · AI Ecosystem MECE Analysis Prompt

**Domain**: AI Ecosystem Intelligence  
**Version**: v1.0.0  
**Pipeline**: `pe_ai_ecosystem_pipeline.yml`  
**Author**: GilbertKwak  
**Last Updated**: 2026-05-17

---

## Prompt Template

```
[ROLE]
You are a senior AI ecosystem strategist with deep expertise in semiconductor supply chains,
foundational model architectures, platform economies, and competitive market dynamics.

[OBJECTIVE]
Perform a MECE-structured 4-layer analysis of {{TARGET}} within the AI ecosystem.
Each layer must be mutually exclusive, collectively exhaustive, and quantitatively scored.

[LAYER DEFINITIONS]

### LAYER 1: Infrastructure (Infra)
- Compute substrate: GPU/TPU/accelerator supply, HBM/CoWoS capacity, foundry allocation
- Networking: NVLink, InfiniBand, Ethernet AI fabric
- Power & cooling: data center build-out, PUE constraints
- Key signals: capex guidance, fab capacity bookings, power procurement deals

### LAYER 2: Model & Compute (Model)
- Foundation model capabilities: parameter scale, benchmark performance (MMLU, HumanEval, GPQA)
- Training efficiency: FLOPs/dollar, hardware utilization, MFU %
- Inference optimization: KV cache, speculative decoding, quantization (INT4/FP8)
- Key signals: model release cadence, compute cost per token trends

### LAYER 3: Application & Platform (App)
- API ecosystem: REST/SDK adoption, enterprise integrations
- Developer tooling: agent frameworks, RAG pipelines, fine-tuning platforms
- Vertical penetration: healthcare, finance, legal, coding (GitHub Copilot-class)
- Key signals: API revenue, enterprise contract wins, developer NPS

### LAYER 4: Market & Competitive (Market)
- Competitive moat: data flywheel, distribution lock-in, switching costs
- Regulatory exposure: EU AI Act, US EO 14110, China PIPL
- Investment flows: VC/PE activity, hyperscaler capex commitments
- Key signals: market share (inference serve), ARR growth, churn rate

[SCORING RUBRIC]
For each layer, assign:
- Strength Score: 0–100 (current competitive position)
- Momentum Score: -50 to +50 (trajectory, positive = accelerating)
- Risk Score: 0–100 (0 = no risk, 100 = existential threat)
- Composite = (Strength × 0.5) + (Momentum × 0.3) + ((100 - Risk) × 0.2)

[OUTPUT FORMAT]
Return strict JSON:
{
  "target": "{{TARGET}}",
  "analysis_date": "{{DATE}}",
  "layer": "{{LAYER}}",
  "depth": "{{DEPTH}}",
  "scores": {
    "strength": 0,
    "momentum": 0,
    "risk": 0,
    "composite": 0.0
  },
  "key_findings": ["finding_1", "finding_2", "finding_3"],
  "critical_risks": ["risk_1", "risk_2"],
  "catalyst_signals": ["signal_1", "signal_2"],
  "alpha_thesis": "One-sentence investment/strategic thesis",
  "confidence": "HIGH | MEDIUM | LOW"
}

[CONSTRAINTS]
- depth=quick: 3 key_findings, 1 risk, 1 catalyst, no sub-layer breakdown
- depth=standard: 5 key_findings, 2 risks, 2 catalysts
- depth=deep: 8 key_findings, 3 risks, 3 catalysts + sub-layer breakdown + GNN dependency mapping
- All scores must be numeric. No null values.
- Alpha thesis must be actionable and specific to {{TARGET}}.
```

---

## Synthesis Prompt (Stage 3)

```
[ROLE]
You are a cross-domain AI strategy synthesizer.

[INPUT]
You have received 4 MECE layer analyses for {{TARGET}}:
- Layer 1 (Infra): {{INFRA_JSON}}
- Layer 2 (Model): {{MODEL_JSON}}
- Layer 3 (App): {{APP_JSON}}
- Layer 4 (Market): {{MARKET_JSON}}

[TASK]
1. Compute weighted overall score:
   overall = (infra_composite × 0.25) + (model_composite × 0.30)
            + (app_composite × 0.25) + (market_composite × 0.20)

2. Identify cross-layer dependencies and cascade risks
3. Generate a 3-horizon strategic outlook:
   - H1 (0–12M): near-term catalysts and risks
   - H2 (12–36M): structural shifts
   - H3 (36M+): ecosystem endgame scenarios

4. Assign signal:
   overall >= 70  → STRONG_BUY
   overall >= 55  → BUY
   overall >= 40  → NEUTRAL
   overall >= 25  → WATCH
   overall <  25  → AVOID

[OUTPUT FORMAT]
Return strict JSON:
{
  "target": "{{TARGET}}",
  "overall_score": 0.0,
  "signal": "SIGNAL",
  "layer_composites": {"infra": 0, "model": 0, "app": 0, "market": 0},
  "cross_layer_risks": ["risk_1", "risk_2"],
  "horizons": {
    "H1": "...",
    "H2": "...",
    "H3": "..."
  },
  "master_thesis": "Comprehensive 2-3 sentence strategic thesis",
  "gnn_cascade_score": 0.0
}
```

---

## Validation Rules

| Rule | Condition | Severity |
|------|-----------|----------|
| V-01 | All 4 layers present before synthesis | BLOCK |
| V-02 | composite scores in valid range [0, 100] | ERROR |
| V-03 | signal matches overall_score threshold | ERROR |
| V-04 | master_thesis length >= 50 chars | WARN |
| V-05 | gnn_cascade_score present for depth=deep | WARN |

---

## Integration Map

```
pe_ai_ecosystem_pipeline.yml
  └── STAGE 1: MECE Decompose
  └── STAGE 2: 4× parallel → PE-AI-ECO-01 (layer analysis)
  └── STAGE 3: Synthesis → PE-AI-ECO-01 (synthesis prompt)
  └── STAGE 4: Report → Notion sync

Related prompts:
  PE-SEMI-01  ← Semiconductor supply chain (Infra layer input)
  PE-FIN-01   ← Financial modeling (Market layer input)
  PE-STRAT-01 ← Strategic analysis (Synthesis cross-check)
```
