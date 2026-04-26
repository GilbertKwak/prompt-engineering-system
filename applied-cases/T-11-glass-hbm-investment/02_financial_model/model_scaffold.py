"""
T-11 Glass/HBM Investment Strategy — Financial Model v1.0
Core / Satellite / Hedge Portfolio IRR, MOIC, NPV Simulator
2026-04-26 | GilbertKwak | SSOT: prompt-engineering-system/applied-cases/T-11
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List

# ── 1. Investment Type Definitions ──────────────────────────────────────────

@dataclass
class InvestmentType:
    name: str
    label: str          # A / B / C
    investment_usd: float
    npv_usd: float
    moic: float
    irr_pct: float
    risk_score: float   # 0~1 (higher = riskier)
    payback_years: float

TYPE_A = InvestmentType(
    name="Glass 수직통합 (Core)",
    label="A",
    investment_usd=500_000_000,
    npv_usd=52_700_000,
    moic=1.11,
    irr_pct=12.0,
    risk_score=0.15,
    payback_years=6.0
)

TYPE_B = InvestmentType(
    name="패키징 레버리지 (Satellite)",
    label="B",
    investment_usd=400_000_000,
    npv_usd=3_158_000_000,
    moic=8.90,
    irr_pct=45.0,
    risk_score=0.20,
    payback_years=2.5
)

TYPE_C = InvestmentType(
    name="US/EU 헤지 (Hedge)",
    label="C",
    investment_usd=350_000_000,
    npv_usd=3_676_000_000,
    moic=11.50,
    irr_pct=55.0,
    risk_score=0.10,
    payback_years=2.0
)

# ── 2. Portfolio Scenarios ────────────────────────────────────────────────

SCENARIOS: Dict[str, Dict[str, float]] = {
    "Conservative": {"A": 0.50, "B": 0.30, "C": 0.20},
    "Balanced":     {"A": 0.40, "B": 0.35, "C": 0.25},
    "Aggressive":   {"A": 0.20, "B": 0.50, "C": 0.30},
    "Geo-Hedge":    {"A": 0.30, "B": 0.30, "C": 0.40},
}

TOTAL_FUND_USD = 1_000_000_000

# ── 3. Portfolio Calculator ───────────────────────────────────────────────

def calc_portfolio(scenario_name: str, weights: Dict[str, float]) -> Dict:
    types = {"A": TYPE_A, "B": TYPE_B, "C": TYPE_C}
    total_return = 0.0
    total_invest = 0.0
    weighted_risk = 0.0
    rows = []

    for label, w in weights.items():
        t = types[label]
        alloc = TOTAL_FUND_USD * w
        ret = alloc * t.moic
        total_return += ret
        total_invest += alloc
        weighted_risk += w * t.risk_score
        rows.append({
            "Type": f"{label} — {t.name}",
            "Allocation ($M)": round(alloc / 1e6, 0),
            "Weight (%)": round(w * 100, 0),
            "MOIC": t.moic,
            "IRR (%)": t.irr_pct,
            "Return ($M)": round(ret / 1e6, 0),
            "Risk Score": t.risk_score,
        })

    portfolio_moic = total_return / total_invest
    df = pd.DataFrame(rows)

    return {
        "scenario": scenario_name,
        "total_investment_m": round(total_invest / 1e6, 0),
        "total_return_m": round(total_return / 1e6, 0),
        "portfolio_moic": round(portfolio_moic, 2),
        "weighted_risk": round(weighted_risk, 3),
        "detail_df": df,
    }

# ── 4. Main Execution ─────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 70)
    print("T-11 Glass/HBM Investment Portfolio Simulator v1.0")
    print("=" * 70)

    results = []
    for name, weights in SCENARIOS.items():
        r = calc_portfolio(name, weights)
        results.append(r)
        print(f"\n[{name}] MOIC: {r['portfolio_moic']}x | "
              f"Return: ${r['total_return_m']:,.0f}M | "
              f"Risk: {r['weighted_risk']}")
        print(r["detail_df"].to_string(index=False))

    # Export summary CSV
    summary = pd.DataFrame([{
        "Scenario": r["scenario"],
        "Total Return ($M)": r["total_return_m"],
        "Portfolio MOIC": r["portfolio_moic"],
        "Weighted Risk": r["weighted_risk"],
    } for r in results])
    summary.to_csv("outputs/portfolio_summary.csv", index=False)
    print("\n✅ Exported: outputs/portfolio_summary.csv")
