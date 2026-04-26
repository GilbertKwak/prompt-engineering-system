#!/usr/bin/env python3
"""Track C-3: Black-Litterman 포트폴리오 최적화
PE-7 v2.0 | E-03 LinAlgError Fallback | Gilbert Kwak 2026-04-26"""
import os, json
import numpy as np
import pandas as pd
from datetime import datetime

os.makedirs("data", exist_ok=True)

TICKERS      = ["TSMC","Nvidia","SKHynix","Intel","ASML","SMIC","Cash"]
MKT_CAPS     = np.array([500, 350, 120, 95, 380, 60, 0.01])  # B USD
ANNUAL_VOLS  = np.array([0.28, 0.55, 0.40, 0.30, 0.25, 0.45, 0.001])
RISK_AVERSION = 2.5
TAU           = 0.05
RISK_FREE     = 0.045

def build_cov(vols: np.ndarray, ridge: float = 1e-4) -> np.ndarray:
    n    = len(vols)
    corr = np.full((n, n), 0.3)
    np.fill_diagonal(corr, 1.0)
    return np.outer(vols, vols) * corr + ridge * np.eye(n)

# ── BL Step 1: 역최적화 (Market Equilibrium) ─────────────────────────────────
def market_equilibrium_returns(mkt_caps, cov, delta) -> tuple:
    w_mkt = mkt_caps / mkt_caps.sum()
    pi    = delta * cov @ w_mkt
    return pi, w_mkt

# ── BL Step 2: Views 정의 ─────────────────────────────────────────────────────
def define_views() -> tuple:
    """투자 View 3개: TSMC>Intel (+20%), Nvidia 절대수익 40%, SKHynix>SMIC (+25%)"""
    idx = {t: i for i, t in enumerate(TICKERS)}
    n   = len(TICKERS)
    P   = np.zeros((3, n))
    # View 1: TSMC outperforms Intel by 20%
    P[0, idx["TSMC"]]    =  1
    P[0, idx["Intel"]]   = -1
    # View 2: Nvidia absolute return 40%
    P[1, idx["Nvidia"]]  =  1
    # View 3: SKHynix outperforms SMIC by 25%
    P[2, idx["SKHynix"]] =  1
    P[2, idx["SMIC"]]    = -1
    Q     = np.array([0.20, 0.40, 0.25])
    Omega = np.diag([0.05**2, 0.08**2, 0.06**2])
    return P, Q, Omega

# ── BL Step 3: Posterior 계산 ─────────────────────────────────────────────────
def black_litterman_posterior(pi, cov, P, Q, Omega, tau) -> tuple:
    """E-03: LinAlgError → prior로 fallback"""
    try:
        tau_cov_inv = np.linalg.inv(tau * cov)
        omega_inv   = np.linalg.inv(Omega)
        M_inv       = tau_cov_inv + P.T @ omega_inv @ P
        M           = np.linalg.inv(M_inv)
        mu_bl       = M @ (tau_cov_inv @ pi + P.T @ omega_inv @ Q)
        sigma_bl    = M + cov
        return mu_bl, sigma_bl
    except np.linalg.LinAlgError:
        print("[E-03] BL 행렬 연산 오류 → prior 수익률 fallback")
        return pi, tau * cov

# ── BL Step 4: 최적 비중 ──────────────────────────────────────────────────────
def bl_optimal_weights(mu_bl, sigma_bl, delta) -> np.ndarray:
    """E-03: LinAlgError → 균등 배분 fallback"""
    try:
        w_raw = np.linalg.solve(delta * sigma_bl, mu_bl)
        w_raw = np.clip(w_raw, 0, None)
        return w_raw / w_raw.sum() if w_raw.sum() > 0 else np.ones(len(mu_bl)) / len(mu_bl)
    except np.linalg.LinAlgError:
        print("[E-03] BL 가중치 계산 오류 → 균등 배분 fallback")
        return np.ones(len(mu_bl)) / len(mu_bl)

# ── main ──────────────────────────────────────────────────────────────────────
def main():
    print("[Track C-3] Black-Litterman 시작 ...")
    cov        = build_cov(ANNUAL_VOLS)
    pi, w_mkt  = market_equilibrium_returns(MKT_CAPS, cov, RISK_AVERSION)
    print("[Step 1] 시장 균형 수익률")
    for t, r in zip(TICKERS, pi): print(f"  {t:12s} {r:.1%}")

    P, Q, Omega = define_views()
    print(f"[Step 2] View {len(Q)}개 정의 완료")

    mu_bl, sigma_bl = black_litterman_posterior(pi, cov, P, Q, Omega, TAU)
    print("[Step 3] BL Posterior 수익률")
    for t, r, r0 in zip(TICKERS, mu_bl, pi):
        delta = r - r0
        sign  = "▲" if delta > 0 else "▼"
        print(f"  {t:12s} {r:.1%}  ({sign}{abs(delta):.1%} vs prior)")

    w_opt = bl_optimal_weights(mu_bl, sigma_bl, RISK_AVERSION)
    print("[Step 4] BL 최적 비중")
    result = {}
    for t, w, wm in zip(TICKERS, w_opt, w_mkt):
        diff = w - wm
        sign = "+" if diff >= 0 else "-"
        print(f"  {t:12s} BL={w:.1%}  Mkt={wm:.1%}  ({sign}{abs(diff):.1%})")
        result[t] = {"bl_weight": round(float(w), 4), "mkt_weight": round(float(wm), 4)}

    today = datetime.now().strftime("%Y%m%d")
    with open(f"data/black_litterman_{today}.json", "w") as f:
        json.dump({
            "model": "Black-Litterman", "tau": TAU, "delta": RISK_AVERSION,
            "n_views": len(Q), "weights": result,
            "bl_returns": {t: round(float(r), 4) for t, r in zip(TICKERS, mu_bl)},
        }, f, indent=2)
    print(f"[OK] 저장 완료")

if __name__ == "__main__":
    main()
