#!/usr/bin/env python3
"""
monte_carlo_sim.py  —  Agent 3 / OUTPUT 3-4
4-World Scenario Monte Carlo Simulation (N=10,000)
Author: Gilbert | Version: 1.0.0 | Date: 2026-05-02
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import json, logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# ── 1. World 정의 ────────────────────────────────────────────────────────────
WORLDS = {
    "A": {"name": "Hard Decoupling",        "prior": 0.019},
    "B": {"name": "Managed De-risking",     "prior": 0.558},
    "C": {"name": "AI-Boom Cooperation",    "prior": 0.400},
    "D": {"name": "Multilateral Rebalance", "prior": 0.024},
}

# ── 2. Layer 충격 파라미터 (μ, σ) ────────────────────────────────────────────
@dataclass
class LayerParams:
    name: str
    impact_by_world: Dict[str, Tuple[float, float]]

LAYER_PARAMS: List[LayerParams] = [
    LayerParams("L1_Rare_Earth",     {"A":(95,5), "B":(40,8), "C":(20,5), "D":(30,7)}),
    LayerParams("L2_Photoresist",    {"A":(85,6), "B":(35,7), "C":(20,5), "D":(25,6)}),
    LayerParams("L3_EUV",           {"A":(90,5), "B":(40,8), "C":(15,4), "D":(30,7)}),
    LayerParams("L4_Water_Energy",  {"A":(70,8), "B":(30,6), "C":(25,5), "D":(35,7)}),
    LayerParams("L5_HBM",           {"A":(80,7), "B":(35,7), "C":(20,5), "D":(35,7)}),
    LayerParams("L6_Foundry",       {"A":(95,4), "B":(35,7), "C":(25,5), "D":(40,8)}),
    LayerParams("L7_Packaging",     {"A":(75,8), "B":(30,6), "C":(20,5), "D":(35,7)}),
    LayerParams("L8_AI_Chip",       {"A":(85,6), "B":(35,7), "C":(30,6), "D":(40,8)}),
    LayerParams("L9_SW_IP",         {"A":(80,7), "B":(30,6), "C":(25,5), "D":(40,8)}),
    LayerParams("L10_Geopolitics",  {"A":(95,4), "B":(40,8), "C":(45,8), "D":(55,9)}),
    LayerParams("L11_Talent_RD",    {"A":(85,6), "B":(35,7), "C":(20,5), "D":(30,7)}),
    LayerParams("L12_ESG_Carbon",   {"A":(40,8), "B":(45,8), "C":(55,8), "D":(60,9)}),
]

COMPANY_REVENUE_2026 = {
    "SK_Hynix":  36.7, "Samsung": 85.0, "TSMC": 85.0, "Nvidia": 80.0, "ASML": 35.0,
}

CAGR_BY_WORLD = {
    "SK_Hynix": {"A":-0.054, "B":0.084, "C":0.110, "D":0.036},
    "Samsung":  {"A":-0.030, "B":0.060, "C":0.080, "D":0.030},
    "TSMC":     {"A":-0.080, "B":0.071, "C":0.110, "D":0.040},
    "Nvidia":   {"A": 0.012, "B":0.095, "C":0.065, "D":0.055},
    "ASML":     {"A":-0.026, "B":0.081, "C":0.100, "D":0.060},
}
CAGR_SIGMA = 0.02

class MonteCarloSimulator:
    def __init__(self, n_sim: int = 10_000, horizon_years: int = 4, seed: int = 42):
        self.n_sim = n_sim
        self.horizon = horizon_years
        self.rng = np.random.default_rng(seed)
        logger.info(f"MC Simulator init: N={n_sim}, horizon={horizon_years}yr, seed={seed}")

    def _sample_world(self) -> np.ndarray:
        priors = np.array([WORLDS[w]["prior"] for w in "ABCD"])
        priors /= priors.sum()
        return self.rng.choice(list("ABCD"), size=self.n_sim, p=priors)

    def run_layer_simulation(self) -> pd.DataFrame:
        world_samples = self._sample_world()
        records = []
        for i, w in enumerate(world_samples):
            row = {"sim_id": i, "world": w}
            composite = 0.0
            for lp in LAYER_PARAMS:
                mu, sigma = lp.impact_by_world[w]
                score = float(np.clip(self.rng.normal(mu, sigma), 0, 100))
                row[lp.name] = round(score, 2)
                composite += score
            row["composite_risk"] = round(composite / len(LAYER_PARAMS), 2)
            records.append(row)
        return pd.DataFrame(records)

    def run_revenue_simulation(self) -> pd.DataFrame:
        world_samples = self._sample_world()
        records = []
        for i, w in enumerate(world_samples):
            row = {"sim_id": i, "world": w}
            for co, base in COMPANY_REVENUE_2026.items():
                mu_cagr = CAGR_BY_WORLD[co][w]
                actual_cagr = float(self.rng.normal(mu_cagr, CAGR_SIGMA))
                rev_2030 = base * (1 + actual_cagr) ** self.horizon
                row[f"{co}_rev2030"] = round(rev_2030, 3)
            records.append(row)
        return pd.DataFrame(records)

    def summarize(self, df: pd.DataFrame, value_cols: List[str]) -> pd.DataFrame:
        rows = []
        for w in "ABCD":
            sub = df[df["world"] == w]
            for col in value_cols:
                vals = sub[col].values
                rows.append({
                    "world": w, "metric": col,
                    "p5":   round(np.percentile(vals, 5), 2),
                    "p25":  round(np.percentile(vals, 25), 2),
                    "median": round(np.median(vals), 2),
                    "p75":  round(np.percentile(vals, 75), 2),
                    "p95":  round(np.percentile(vals, 95), 2),
                    "mean": round(vals.mean(), 2),
                    "std":  round(vals.std(), 2),
                })
        return pd.DataFrame(rows)

def main():
    sim = MonteCarloSimulator(n_sim=10_000)
    out = Path("output")
    out.mkdir(exist_ok=True)
    layer_df = sim.run_layer_simulation()
    layer_df.to_csv(out / "mc_layer_risk.csv", index=False)
    layer_cols = [lp.name for lp in LAYER_PARAMS] + ["composite_risk"]
    sim.summarize(layer_df, layer_cols).to_csv(out / "mc_layer_summary.csv", index=False)
    rev_df = sim.run_revenue_simulation()
    rev_df.to_csv(out / "mc_revenue_raw.csv", index=False)
    rev_cols = [f"{co}_rev2030" for co in COMPANY_REVENUE_2026]
    sim.summarize(rev_df, rev_cols).to_csv(out / "mc_revenue_summary.csv", index=False)
    meta = {"version":"1.0.0","n_simulations":10_000,"horizon_years":4,"worlds":WORLDS,"created":"2026-05-02"}
    (out / "mc_meta.json").write_text(json.dumps(meta, indent=2))
    logger.info("All outputs written to output/")

if __name__ == "__main__":
    main()
