# CRP-AGENT-FRAMEWORK — Phase 1 Complete

## Overview

Phase 1 delivers the **Foundation Layer** of the CRP-Native Agent Framework.
This layer surpasses LangGraph/AutoGen/CrewAI at the architectural level by embedding
cognitive measurement (MTI/QLI) natively into every processing step.

---

## Delivered Components

| Component | File | Status |
|-----------|------|--------|
| Data Models | `models.py` | ✅ Complete |
| Cognitive Kernel | `cognitive_kernel.py` | ✅ Complete |
| State Engine | `state_engine.py` | ✅ Complete |
| Flow Engine | `flow_engine.py` | ✅ Complete |
| Package Init | `__init__.py` | ✅ Complete |
| Phase 1 Smoke Tests | `tests/test_phase1_smoke.py` | ✅ Complete |

---

## Architecture

```
Input (AgentTask)
    │
    ▼
┌──────────────────────────────────────────┐
│          COGNITIVE KERNEL                 │
│  Capture → Encode → Reconfigure → Validate│
│  MTI = f(depth, reconfig_delta, val)      │
│  QLI = f(specificity, coherence, novelty) │
└──────────────┬───────────────────────────┘
               │ CognitiveState
               ▼
┌──────────────────────────────────────────┐
│           FLOW ENGINE                     │
│  DAG + Event-driven hybrid               │
│  PE-1 → PE-2 → PE-3 → KM-PIPE → KG      │
│  MTI gate: loop if score < threshold     │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│           STATE ENGINE                    │
│  TrajectoryDB (append-only)              │
│  Session state management                 │
│  CognitiveAsset creation                 │
└──────────────┬───────────────────────────┘
               │
    ┌──────────┴──────────┐
    ▼                     ▼
KM-PIPE (Notion)    KG v6.3+ (Node)
[T-09 Hook]         [T-09 Hook]
```

---

## Key Formulas

### MTI (Metacognitive Trajectory Index)
```
MTI = tanh(0.2 × depth) × 0.4
    + sigmoid(reconfig_delta) × 0.35
    + validation_score × 0.25
```
- Range: [0, 1]
- PE-3 gate: MTI ≥ 0.75 → PE-3 score ≥ 95

### QLI (Query-Level Intelligence)
```
QLI = specificity × 0.40
    + coherence × 0.35
    + novelty × 0.25
```

### PE-3 Score
```
PE-3 = 50 × MTI + 30 × QLI + 20 × reconfiguration_depth_bonus
```

---

## T-09 Integration Hooks

| Hook Event | Fires When | Connects To |
|------------|------------|-------------|
| `on_reconfigure` | After each CRP loop | PE-3 validation |
| `on_mti_threshold_crossed` | MTI ≥ 0.75 | Quality gate |
| `on_complete` | Processing done | KM-PIPE trigger |
| `on_asset_created` | Asset finalized | KM-PIPE v3.0 Notion sync |
| `on_kg_node_trigger` | Asset created | KG v6.3+ node creation |
| `on_session_complete` | Session closed | PE-3 final validation |

---

## Quick Start

```python
from crp_framework import CognitiveKernel, StateEngine, FlowEngine
from crp_framework import AgentTask, CognitiveContext
from crp_framework.flow_engine import build_pe_pipeline_flow

# 1. Create kernel
kernel = CognitiveKernel()

# 2. Register T-09 hooks
kernel.register_t09_hook("on_complete", lambda **kw: print(f"PE-3: {kw['state'].pe3_score():.1f}"))

# 3. Define task
context = CognitiveContext(domain="semiconductor-analysis")
task = AgentTask(
    query="Analyze HBM4 supply constraint implications for NVIDIA.",
    context=context,
    mti_threshold=0.75,
)

# 4. Process
state, steps = kernel.process(task)
print(f"MTI: {state.mti_score:.3f}")
print(f"QLI: {state.qli_score:.3f}")
print(f"PE-3 Score: {state.pe3_score():.1f}")

# 5. Assetize (→ KM-PIPE + KG)
engine = StateEngine()
engine.init_session(state)
asset = engine.assetize(
    state.session_id,
    content="[Analysis output here]",
    asset_type="analysis",
    tags=["semiconductor", "HBM4", "NVIDIA"],
)
print(f"Asset publication ready: {asset.is_publication_ready()}")
```

---

## Phase 2 Roadmap

| Component | Phase 2 Target |
|-----------|----------------|
| Agent Runtime | Bayesian n-ensemble fusion |
| Trust Layer | Anti-gaming detection (statistical anomaly) |
| Developer Interface | Python/TS SDK + YAML declarative agents |
| Platform Layer | Multi-tenant SaaS + REST/gRPC API |
| Cognitive Kernel | Embedding-based QLI scorer (replaces heuristics) |
| State Engine | PostgreSQL/TimescaleDB backing store |

Phase 2 start: C-39 / Week 2
