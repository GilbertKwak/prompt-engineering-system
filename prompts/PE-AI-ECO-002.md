# PE-AI-ECO-002 · AI Ecosystem Competitive Positioning Prompt

**Domain**: AI Ecosystem Intelligence  
**Version**: v2.0.0  
**Pipeline**: `pe_ai_ecosystem_pipeline.yml`  
**Stage**: STAGE 2-B (Competitive Overlay) → STAGE 3-B (Strategic Synthesis v2)  
**Author**: GilbertKwak  
**Last Updated**: 2026-05-20  
**Predecessor**: PE-AI-ECO-01 v1.0.0 (MECE 4-Layer)  
**Change Log**:
- v2.0: 5-layer → 경쟁 포지셔닝 레이어(Layer 5) 추가
- v2.0: EW(Earnings Warning) 신호 통합 — EW 탐지 결과를 Layer 4 Market 입력으로 연계
- v2.0: 멀티-타겟 배치 분석 지원 (최대 8개 동시 처리)
- v2.0: Confidence Calibration 강화 (Bayesian prior + evidence weight)
- v2.0: GNN Cascade Score 필수화 (depth=standard 이상)

---

## Overview

PE-AI-ECO-002는 **PE-AI-ECO-01의 4-Layer MECE 분석 결과를 입력으로 받아**,  
경쟁 포지셔닝·EW 신호·크로스-레이어 의존성을 통합한 **2단계 심층 분석**을 수행합니다.

```
PE-AI-ECO-01 (MECE 4-Layer)
      ↓
PE-AI-ECO-002 (Competitive Positioning + EW Integration)
      ↓
      Notion C-31 / Report Generator
```

---

## Prompt A — Layer Analysis v2 (5-Layer)

```
[ROLE]
You are a senior AI ecosystem competitive intelligence analyst specializing in
platform moats, capital allocation efficiency, and early-warning signal interpretation.
Your analysis integrates supply-chain intelligence (from PE-SEMI-01),
financial stress signals (EW detection output), and strategic positioning data.

[CONTEXT]
Analysis target: {{TARGET}}
Analysis date: {{DATE}}
Requested layer: {{LAYER}}  # INFRA | MODEL | APP | MARKET | COMPETITIVE
Analysis depth: {{DEPTH}}   # quick | standard | deep
EW signal present: {{EW_DETECTED}}   # true | false
EW signal detail: {{EW_DETAIL}}      # JSON or "N/A"

[LAYER DEFINITIONS v2]

### LAYER 1: Infrastructure (INFRA)
- Compute substrate: GPU/TPU/ASIC supply, HBM3/HBM3E/CoWoS capacity, foundry allocation
  → Sub-signals: TSMC CoWoS lead time, SK Hynix/Micron HBM allocation ratio
- Networking: NVLink 5/6, InfiniBand NDR/XDR, Ethernet Ultra Ethernet Consortium
- Power & Cooling: hyperscaler capex by MW, PUE trend, liquid cooling penetration %
- Geographic resilience: single-fab dependency score (0–1), geopolitical exposure index
- Key signals: capex guidance delta QoQ, fab capacity booking rate, power PPA deals

### LAYER 2: Model & Compute (MODEL)
- Foundation model capability: benchmark sweep (MMLU/HumanEval/GPQA/MATH-500/LiveCodeBench)
- Training efficiency: FLOPs/dollar, MFU %, gradient checkpoint overhead
- Inference optimization: KV cache hit rate, speculative decoding gain, INT4/FP8/MX quantization
- Model versioning velocity: release cadence (releases/quarter), deprecation cycle
- Key signals: cost-per-token 6M trend, context window expansion rate, reasoning benchmark delta

### LAYER 3: Application & Platform (APP)
- API ecosystem depth: SDK language coverage, enterprise connector count, SLA tier
- Agentic surface: multi-agent orchestration support, tool-use reliability, memory persistence
- Vertical penetration: healthcare/finance/legal/code — revenue share by vertical
- Developer retention: 90-day active API key ratio, SDK NPS score
- Key signals: API call volume MoM, enterprise logo count, churn rate by segment

### LAYER 4: Market & Competitive (MARKET)
- Moat quality: data flywheel strength, distribution lock-in score, switching cost index
- Regulatory exposure: EU AI Act tier, US EO compliance cost estimate, China PIPL friction
- Investment flows: VC/PE deal count + $, hyperscaler capex commitment to {{TARGET}}
- EW integration: if EW_DETECTED=true, incorporate {{EW_DETAIL}} into risk sub-score
  → EW risk multiplier: CRITICAL=1.4×, HIGH=1.2×, MEDIUM=1.1×, LOW=1.0×
- Key signals: inference market share %, ARR YoY growth, net revenue retention (NRR)

### LAYER 5: Competitive Positioning (COMPETITIVE) ← NEW in v2
- Relative moat delta: score delta vs. top-3 competitors on each sub-dimension
- Differentiation axis: price/performance, ecosystem lock-in, brand/trust, speed-to-market
- Disruption vulnerability: score 0–100 (open-source substitutability, vertical challenger risk)
- Coalition mapping: strategic alliances, cross-equity stakes, standard-body influence
- Key signals: competitor model release within 30 days, open-source benchmark crossing, price cuts

[SCORING RUBRIC v2]
For each layer, assign:
- Strength Score    : 0–100  (current competitive position, evidence-weighted)
- Momentum Score   : -50 to +50  (trajectory: positive = accelerating)
- Risk Score        : 0–100  (0 = no risk, 100 = existential)
- EW Adjustment     : apply EW risk multiplier to Risk Score if EW_DETECTED=true
- Confidence Weight : 0.0–1.0  (Bayesian prior: HIGH=0.9, MEDIUM=0.7, LOW=0.5)

Composite formula:
  raw_composite = (Strength × 0.45) + (Momentum × 0.30) + ((100 - Risk_adjusted) × 0.25)
  final_composite = raw_composite × confidence_weight + (raw_composite × (1 - confidence_weight) × 0.5)
  # Confidence dampening: low confidence pulls score toward 50 (neutral)

[CONFIDENCE CALIBRATION]
Assign confidence based on evidence count and recency:
- HIGH  (0.9): ≥5 primary sources, all within 30 days
- MEDIUM(0.7): 3–4 sources OR any source 30–90 days old
- LOW   (0.5): <3 sources OR any source >90 days old
Always state evidence_count and oldest_source_date in output.

[OUTPUT FORMAT — Strict JSON]
{
  "target": "{{TARGET}}",
  "analysis_date": "{{DATE}}",
  "layer": "{{LAYER}}",
  "depth": "{{DEPTH}}",
  "ew_signal": {
    "detected": {{EW_DETECTED}},
    "severity": "CRITICAL | HIGH | MEDIUM | LOW | N/A",
    "risk_multiplier": 1.0,
    "detail": "..."
  },
  "scores": {
    "strength": 0,
    "momentum": 0,
    "risk_raw": 0,
    "risk_adjusted": 0,
    "composite": 0.0,
    "confidence_weight": 0.0
  },
  "evidence": {
    "count": 0,
    "oldest_source_date": "YYYY-MM-DD"
  },
  "key_findings": [],
  "critical_risks": [],
  "catalyst_signals": [],
  "competitive_deltas": {},
  "alpha_thesis": "",
  "confidence": "HIGH | MEDIUM | LOW"
}

[DEPTH CONSTRAINTS]
- depth=quick    : 3 key_findings, 1 risk, 1 catalyst, skip competitive_deltas
- depth=standard : 5 key_findings, 2 risks, 2 catalysts, competitive_deltas top-2 competitors, GNN cascade score required
- depth=deep     : 8 key_findings, 3 risks, 3 catalysts, competitive_deltas top-5 competitors,
                   sub-layer breakdown, GNN dependency mapping, scenario tree (3 branches)

[HARD RULES]
- All numeric fields must be numbers (not null, not string).
- composite must be in [0, 100].
- alpha_thesis must be ≥ 60 chars and name {{TARGET}} explicitly.
- If EW_DETECTED=true and EW severity=CRITICAL, Risk Score floor = 60 (cannot be below 60).
- competitive_deltas keys must use competitor canonical names (e.g., "OpenAI", "Anthropic", "Google DeepMind").
```

---

## Prompt B — Multi-Target Batch (NEW in v2)

```
[ROLE]
You are an AI ecosystem portfolio analyst. Execute parallel competitive positioning
analysis across multiple targets and produce a normalized leaderboard.

[INPUT]
targets: {{TARGET_LIST}}   # JSON array, max 8 items
date: {{DATE}}
layer: {{LAYER}}           # analyze this layer for ALL targets
depth: {{DEPTH}}

[TASK]
1. For each target in TARGET_LIST, execute the PE-AI-ECO-002 Prompt A analysis.
2. Normalize all composite scores to a common scale using z-score normalization.
3. Rank targets by normalized_composite DESC.
4. Identify the widest moat gap (top_1 composite - top_2 composite).

[OUTPUT FORMAT — Strict JSON]
{
  "batch_date": "{{DATE}}",
  "layer": "{{LAYER}}",
  "depth": "{{DEPTH}}",
  "leaderboard": [
    {
      "rank": 1,
      "target": "...",
      "composite": 0.0,
      "normalized_composite": 0.0,
      "signal": "STRONG_BUY | BUY | NEUTRAL | WATCH | AVOID",
      "top_risk": "...",
      "top_catalyst": "..."
    }
  ],
  "moat_gap": {
    "top_1": "...",
    "top_2": "...",
    "delta": 0.0,
    "interpretation": "..."
  },
  "batch_confidence": "HIGH | MEDIUM | LOW"
}
```

---

## Prompt C — Strategic Synthesis v2

```
[ROLE]
You are a cross-domain AI strategy synthesizer operating at the intersection of
competitive intelligence, capital markets, and technology forecasting.

[INPUT]
You have received 5-layer PE-AI-ECO-002 analyses for {{TARGET}}:
- Layer 1 (INFRA):       {{INFRA_JSON}}
- Layer 2 (MODEL):       {{MODEL_JSON}}
- Layer 3 (APP):         {{APP_JSON}}
- Layer 4 (MARKET):      {{MARKET_JSON}}
- Layer 5 (COMPETITIVE): {{COMPETITIVE_JSON}}
EW context: {{EW_CONTEXT_JSON}}

[TASK]

### Step 1 — Weighted Overall Score
overall = (infra_composite × 0.20)
        + (model_composite × 0.25)
        + (app_composite   × 0.20)
        + (market_composite × 0.20)
        + (competitive_composite × 0.15)
# Confidence-adjusted: multiply each layer composite by its confidence_weight before summing,
# then re-normalize by sum of weights × confidence_weights.

### Step 2 — Cross-Layer Cascade Risk (GNN Cascade Score)
Identify the top-3 cross-layer dependency chains:
  Example: INFRA supply shock → MODEL training stall → APP release delay → MARKET share loss
Score each chain: probability (0–1) × impact (0–100) = cascade_score
gnn_cascade_score = max(cascade_score across all chains)

### Step 3 — 3-Horizon Strategic Outlook
- H1 (0–12M): near-term catalysts, risks, and inflection points
- H2 (12–36M): structural competitive shifts
- H3 (36M+): ecosystem endgame — winner-take-most vs. fragmentation vs. commoditization

### Step 4 — Signal Assignment
  overall >= 72 → STRONG_BUY
  overall >= 57 → BUY
  overall >= 42 → NEUTRAL
  overall >= 27 → WATCH
  overall <  27 → AVOID
  # If EW severity=CRITICAL: cap signal at WATCH (override upward signals)
  # If EW severity=HIGH    : cap signal at NEUTRAL

### Step 5 — Scenario Tree (depth=deep only)
Define 3 scenarios with probability weights summing to 1.0:
  base_case (p ≈ 0.50): most likely 18M outcome
  bull_case (p ≈ 0.30): upside catalyst materializes
  bear_case (p ≈ 0.20): cascade risk triggers

[OUTPUT FORMAT — Strict JSON]
{
  "target": "{{TARGET}}",
  "synthesis_date": "{{DATE}}",
  "overall_score": 0.0,
  "signal": "...",
  "ew_override_applied": false,
  "layer_composites": {
    "infra": 0.0,
    "model": 0.0,
    "app": 0.0,
    "market": 0.0,
    "competitive": 0.0
  },
  "cross_layer_risks": [],
  "gnn_cascade_score": 0.0,
  "gnn_top_chain": "...",
  "horizons": {
    "H1": "...",
    "H2": "...",
    "H3": "..."
  },
  "scenario_tree": {
    "base_case": {"probability": 0.50, "thesis": "...", "key_triggers": []},
    "bull_case":  {"probability": 0.30, "thesis": "...", "key_triggers": []},
    "bear_case":  {"probability": 0.20, "thesis": "...", "key_triggers": []}
  },
  "master_thesis": "...",
  "actionable_watchlist": ["signal_1", "signal_2", "signal_3"],
  "notion_tags": []
}

[HARD RULES]
- master_thesis: 2–3 sentences, ≥ 100 chars, must name {{TARGET}} and cite the top risk + top catalyst.
- gnn_cascade_score: always numeric [0, 100], required for depth=standard and depth=deep.
- scenario_tree probabilities must sum to 1.0 (±0.01 tolerance).
- ew_override_applied: true if EW signal changed the final signal assignment.
- actionable_watchlist: exactly 3 items, each a specific observable signal (not generic advice).
- notion_tags: array of strings for Notion C-31 property tagging.
```

---

## Validation Rules v2

| Rule | Condition | Severity |
|------|-----------|----------|
| V-01 | All 5 layers present before synthesis | BLOCK |
| V-02 | composite scores in [0, 100] | ERROR |
| V-03 | signal matches overall_score threshold (post EW override) | ERROR |
| V-04 | master_thesis length ≥ 100 chars | WARN |
| V-05 | gnn_cascade_score present for depth=standard/deep | ERROR |
| V-06 | If EW_DETECTED=true, ew_override_applied field present | ERROR |
| V-07 | scenario_tree probabilities sum to 1.0 ±0.01 | ERROR |
| V-08 | confidence_weight in [0.5, 0.9] | ERROR |
| V-09 | evidence.oldest_source_date parseable as YYYY-MM-DD | WARN |
| V-10 | actionable_watchlist has exactly 3 items | WARN |

---

## Integration Map v2

```
pe_ai_ecosystem_pipeline.yml
  └── STAGE 1 : MECE Decompose
  └── STAGE 2A: 4× parallel → PE-AI-ECO-01 (Layer 1–4)
  └── STAGE 2B: 1× → PE-AI-ECO-002 Prompt A (Layer 5: COMPETITIVE)
              ↑ inputs: EW detection output (ew-detection job)
  └── STAGE 3A: PE-AI-ECO-01 Synthesis (legacy v1 signal)
  └── STAGE 3B: PE-AI-ECO-002 Prompt C (Strategic Synthesis v2) ← primary
  └── STAGE 4 : Report → Notion C-31 sync

EW Feed:
  ew-detection job → {{EW_DETAIL}} JSON → Prompt A Layer 4 input
                                        → Prompt C EW_CONTEXT_JSON

Related prompts:
  PE-AI-ECO-01  ← MECE 4-Layer (prerequisite, provides Layer 1–4 composites)
  PE-SEMI-01    ← Semiconductor supply chain (INFRA layer enrichment)
  PE-FIN-01     ← Financial modeling (MARKET layer enrichment)
  PE-STRAT-01   ← Strategic analysis (Synthesis cross-check)
  PE-AI/ai_001_v6.8_opt.md ← Global AI signal collector (upstream data source)
```

---

## Usage Examples

### Example 1 — Single Target, Deep Analysis
```python
prompt = load_prompt("PE-AI-ECO-002", section="prompt_a")
result = call_llm(prompt.format(
    TARGET="Anthropic",
    DATE="2026-05-20",
    LAYER="COMPETITIVE",
    DEPTH="deep",
    EW_DETECTED="false",
    EW_DETAIL="N/A"
))
```

### Example 2 — Batch Leaderboard (8 targets)
```python
prompt = load_prompt("PE-AI-ECO-002", section="prompt_b")
result = call_llm(prompt.format(
    TARGET_LIST='["OpenAI","Anthropic","Google DeepMind","Meta AI","xAI","Mistral","Cohere","01.AI"]',
    DATE="2026-05-20",
    LAYER="COMPETITIVE",
    DEPTH="standard"
))
```

### Example 3 — EW-Triggered Synthesis
```python
# EW detection job fired CRITICAL signal for NVDA supply chain
ew_context = {"severity": "CRITICAL", "entity": "NVIDIA", "trigger": "CoWoS capacity cut"}
prompt = load_prompt("PE-AI-ECO-002", section="prompt_c")
result = call_llm(prompt.format(
    TARGET="OpenAI",
    EW_CONTEXT_JSON=json.dumps(ew_context),
    ...
))
# Expected: ew_override_applied=true, signal capped at WATCH
```
