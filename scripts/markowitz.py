#!/usr/bin/env python3
"""Track C-2: Markowitz 효율적 프론티어 + 최대 Sharpe 포트폴리오
PE-7 v2.0 | E-03 singular matrix → ridge 처리 | Gilbert Kwak 2026-04-26"""
import os, json
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datetime import datetime

os.makedirs("data", exist_ok=True)

TICKERS       = ["TSMC","Nvidia","SKHynix","Intel","ASML","SMIC","Cash"]
ANNUAL_RETURNS = np.array([0.25, 0.45, 0.30, 0.05, 0.20, 0.10, 0.04])
ANNUAL_VOLS    = np.array([0.28, 0.55, 0.40, 0.30, 0.25, 0.45, 0.001])
RISK_FREE      = 0.045  # 4.5% T-bill

# ── E-03: ridge 공분산 행렬 ───────────────────────────────────────────────────
def build_cov_matrix(vols: np.ndarray, ridge: float = 1e-4) -> np.ndarray:
    """E-03 singular matrix → ridge regularization으로 방지"""
    n    = len(vols)
    corr = np.full((n, n), 0.30)
    np.fill_diagonal(corr, 1.0)
    cov  = np.outer(vols, vols) * corr
    cov += ridge * np.eye(n)  # E-03 방지
    return cov

def portfolio_stats(weights, mu, cov) -> dict:
    ret    = float(weights @ mu)
    vol    = float(np.sqrt(weights @ cov @ weights))
    sharpe = (ret - RISK_FREE) / vol if vol > 0 else 0.0
    return {"return": round(ret, 4), "volatility": round(vol, 4), "sharpe": round(sharpe, 4)}

def neg_sharpe(weights, mu, cov) -> float:
    return -portfolio_stats(weights, mu, cov)["sharpe"]

# ── 효율적 프론티어 ───────────────────────────────────────────────────────────
def efficient_frontier(mu, cov, n_points: int = 50) -> pd.DataFrame:
    n       = len(mu)
    bounds  = [(0, 1)] * n
    base_c  = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
    targets = np.linspace(mu.min() * 1.05, mu.max() * 0.95, n_points)
    frontier = []
    for target in targets:
        constraints = base_c + [{"type": "eq",
            "fun": lambda w, t=target: portfolio_stats(w, mu, cov)["return"] - t}]
        res = minimize(lambda w: portfolio_stats(w, mu, cov)["volatility"],
                       x0=np.ones(n) / n, method="SLSQP",
                       bounds=bounds, constraints=constraints,
                       options={"maxiter": 1000, "ftol": 1e-9})
        if res.success:
            row = {"target_return": round(target, 4), **portfolio_stats(res.x, mu, cov)}
            for i, t in enumerate(TICKERS): row[t] = round(res.x[i], 4)
            frontier.append(row)
    return pd.DataFrame(frontier)

# ── 최대 Sharpe 포트폴리오 ────────────────────────────────────────────────────
def max_sharpe_portfolio(mu, cov) -> dict:
    n      = len(mu)
    bounds = [(0, 1)] * n
    constr = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
    result = minimize(neg_sharpe, x0=np.ones(n) / n, args=(mu, cov),
                      method="SLSQP", bounds=bounds, constraints=constr,
                      options={"maxiter": 2000, "ftol": 1e-10})
    # E-03 fallback
    weights = result.x if result.success else np.ones(n) / n
    if not result.success: print("[E-03] 최적화 수렴 실패 — 균등 배분 fallback")
    stats  = portfolio_stats(weights, mu, cov)
    alloc  = {t: round(float(w), 4) for t, w in zip(TICKERS, weights)}
    return {"weights": alloc, "stats": stats, "converged": result.success}

# ── main ──────────────────────────────────────────────────────────────────────
def main():
    print("[Track C-2] Markowitz 최적화 ...")
    cov = build_cov_matrix(ANNUAL_VOLS)

    # 1. 최대 Sharpe
    max_s = max_sharpe_portfolio(ANNUAL_RETURNS, cov)
    print("\n[최대 Sharpe 포트폴리오]")
    for t, w in max_s["weights"].items(): print(f"  {t:12s} {w:.1%}")
    s = max_s["stats"]
    print(f"  수익률 {s['return']:.1%} | 변동성 {s['volatility']:.1%} | Sharpe {s['sharpe']:.2f}")

    # 2. 효율적 프론티어
    ef = efficient_frontier(ANNUAL_RETURNS, cov)
    print(f"\n[효율적 프론티어] {len(ef)}개 포인트")
    today = datetime.now().strftime("%Y%m%d")
    ef.to_csv(f"data/efficient_frontier_{today}.csv", index=False)
    with open(f"data/markowitz_result_{today}.json", "w") as f:
        json.dump({"max_sharpe": max_s, "tickers": TICKERS, "risk_free": RISK_FREE}, f, indent=2)
    print(f"[OK] 저장 완료")

if __name__ == "__main__":
    main()
