#!/usr/bin/env python3
"""
cowork-plugins Finance Runner v1.0
PE-7 P1 즉시 실행: Core/Satellite/Hedge 포트폴리오 재무 모델
작성: 2026-04-26 | Gilbert Kwak
"""

import argparse
import json
import math
import os
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import yaml

# ──────────────────────────────────────────────────────────
# IRR 계산 (Newton-Raphson)
# ──────────────────────────────────────────────────────────
def calc_irr(cash_flows: list, max_iter: int = 1000, tol: float = 1e-8) -> float:
    """Internal Rate of Return via Newton-Raphson."""
    rate = 0.10
    for _ in range(max_iter):
        npv = sum(cf / (1 + rate) ** t for t, cf in enumerate(cash_flows))
        d_npv = sum(-t * cf / (1 + rate) ** (t + 1) for t, cf in enumerate(cash_flows))
        if abs(d_npv) < 1e-12:
            break
        rate -= npv / d_npv
        if abs(npv) < tol:
            break
    return rate


# ──────────────────────────────────────────────────────────
# NPV 계산
# ──────────────────────────────────────────────────────────
def calc_npv(cash_flows: list, discount_rate: float) -> float:
    return sum(cf / (1 + discount_rate) ** t for t, cf in enumerate(cash_flows))


# ──────────────────────────────────────────────────────────
# MOIC 계산
# ──────────────────────────────────────────────────────────
def calc_moic(total_proceeds: float, total_invested: float) -> float:
    if total_invested == 0:
        return 0.0
    return total_proceeds / total_invested


# ──────────────────────────────────────────────────────────
# 시나리오별 현금흐름 생성
# ──────────────────────────────────────────────────────────
def build_cash_flows(investment_M: float, irr_base: float,
                     projection_years: int, vintage_year: int) -> dict:
    """
    J-Curve 형태 현금흐름 생성:
    - Year 0~2: 투자 집행 (음수)
    - Year 3~5: 점진적 수익 실현
    - Year 6~7: 대규모 엑시트
    """
    invested = investment_M * 1e6  # USD
    
    # 투자 집행 스케줄 (J-Curve)
    deploy_schedule = [0.40, 0.35, 0.25]  # Year 0, 1, 2
    
    cash_flows = []
    for y in range(projection_years + 1):
        if y <= 2:
            cf = -invested * deploy_schedule[y]
        elif y <= 5:
            # 점진적 수익: 연 IRR 복리 성장
            base = invested * (1 + irr_base) ** y
            cf = base * 0.15  # 분기 회수
        else:
            # 엑시트: 잔여 가치 전체 회수
            exit_multiple = (1 + irr_base) ** projection_years
            cf = invested * exit_multiple * 0.45
    
        cash_flows.append(round(cf / 1e6, 4))  # M USD
    
    return {
        "years": list(range(vintage_year, vintage_year + projection_years + 1)),
        "cash_flows_M": cash_flows,
        "total_invested_M": investment_M,
        "total_proceeds_M": round(sum(cf for cf in cash_flows if cf > 0), 4)
    }


# ──────────────────────────────────────────────────────────
# Monte Carlo 시뮬레이션
# ──────────────────────────────────────────────────────────
def run_monte_carlo(irr_base: float, irr_std: float = 0.08,
                    n_iterations: int = 10000) -> dict:
    np.random.seed(42)
    irr_samples = np.random.normal(irr_base, irr_std, n_iterations)
    irr_samples = np.clip(irr_samples, -0.50, 1.50)  # 현실적 범위 클리핑
    
    return {
        "p10": round(float(np.percentile(irr_samples, 10)), 4),
        "p25": round(float(np.percentile(irr_samples, 25)), 4),
        "p50": round(float(np.percentile(irr_samples, 50)), 4),
        "p75": round(float(np.percentile(irr_samples, 75)), 4),
        "p90": round(float(np.percentile(irr_samples, 90)), 4),
        "mean": round(float(np.mean(irr_samples)), 4),
        "std": round(float(np.std(irr_samples)), 4),
        "prob_above_hurdle_8pct": round(float(np.mean(irr_samples > 0.08)), 4),
        "prob_above_20pct": round(float(np.mean(irr_samples > 0.20)), 4)
    }


# ──────────────────────────────────────────────────────────
# 메인 실행
# ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="cowork-plugins Finance Runner v1.0")
    parser.add_argument("--config", default="plugins/finance/finance_config.yaml")
    parser.add_argument("--scenarios", default="all",
                        help="Comma-separated scenario names or 'all'")
    parser.add_argument("--output", default="reports/finance_output.json")
    args = parser.parse_args()

    # 설정 로드
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"[ERROR] Config not found: {config_path}")
        sys.exit(1)

    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    global_cfg = cfg["global"]
    portfolio_cfg = cfg["portfolio"]
    scenarios_cfg = cfg["scenarios"]
    risk_cfg = cfg["risk_factors"]

    # 실행할 시나리오 결정
    if args.scenarios == "all":
        selected = list(scenarios_cfg.keys())
    else:
        selected = [s.strip() for s in args.scenarios.split(",")]

    results = {
        "meta": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "pe_version": "v3.0",
            "config": str(config_path),
            "fund_size_M": portfolio_cfg["total_fund_size_M"],
            "projection_years": global_cfg["projection_years"],
            "discount_rate": global_cfg["discount_rate"]
        },
        "scenarios": {},
        "portfolio_summary": {}
    }

    portfolio_irrs = []
    portfolio_moics = []

    for scen_key in selected:
        if scen_key not in scenarios_cfg:
            print(f"[WARN] Scenario '{scen_key}' not found — skipping")
            continue

        scen = scenarios_cfg[scen_key]
        alloc = scen["allocations"]
        irr_assumptions = scen["irr_assumptions"]
        moic_targets = scen["moic_targets"]
        print(f"\n📊 Processing scenario: {scen['name']}")

        scen_result = {
            "name": scen["name"],
            "description": scen.get("description", ""),
            "probability": scen.get("probability", 0),
            "risk_score": scen.get("risk_score", 0),
            "types": {}
        }

        total_invested = 0
        total_proceeds = 0

        for type_key in ["type_a", "type_b", "type_c"]:
            weight = alloc[type_key]
            inv_M = portfolio_cfg["total_fund_size_M"] * weight
            irr_base = irr_assumptions[type_key]["base"]
            irr_bull = irr_assumptions[type_key]["bull"]
            irr_bear = irr_assumptions[type_key]["bear"]
            moic = moic_targets[type_key]

            # 현금흐름 생성
            cf_data = build_cash_flows(
                investment_M=inv_M,
                irr_base=irr_base,
                projection_years=global_cfg["projection_years"],
                vintage_year=global_cfg["base_year"]
            )

            # NPV 계산
            npv = calc_npv(cf_data["cash_flows_M"], global_cfg["discount_rate"])

            # IRR 검증
            try:
                calc_irr_result = calc_irr(cf_data["cash_flows_M"])
            except Exception:
                calc_irr_result = irr_base  # fallback

            # Monte Carlo
            mc = run_monte_carlo(
                irr_base=irr_base,
                irr_std=abs(irr_bull - irr_bear) / 4
            )

            type_label = portfolio_cfg["allocations"][type_key]["label"]
            scen_result["types"][type_key] = {
                "label": type_label,
                "weight": weight,
                "investment_M": round(inv_M, 2),
                "irr_base_pct": round(irr_base * 100, 2),
                "irr_bull_pct": round(irr_bull * 100, 2),
                "irr_bear_pct": round(irr_bear * 100, 2),
                "irr_calc_pct": round(calc_irr_result * 100, 2),
                "npv_M": round(npv, 2),
                "moic": moic,
                "total_proceeds_M": cf_data["total_proceeds_M"],
                "cash_flows": cf_data,
                "monte_carlo": mc
            }

            total_invested += inv_M
            total_proceeds += cf_data["total_proceeds_M"]

        # 포트폴리오 MOIC
        portfolio_moic = calc_moic(total_proceeds, total_invested)
        scen_result["portfolio_moic"] = round(portfolio_moic, 2)
        scen_result["total_invested_M"] = round(total_invested, 2)
        scen_result["total_proceeds_M"] = round(total_proceeds, 2)

        portfolio_moics.append(portfolio_moic)
        results["scenarios"][scen_key] = scen_result

        print(f"  ✅ Portfolio MOIC: {portfolio_moic:.2f}x | Risk Score: {scen.get('risk_score', 0):.3f}")

    # 기대값 가중 평균 MOIC
    if portfolio_moics:
        probs = [scenarios_cfg[k].get("probability", 1/len(selected))
                 for k in selected if k in scenarios_cfg]
        prob_sum = sum(probs)
        weighted_moic = sum(m * p for m, p in zip(portfolio_moics, probs)) / prob_sum if prob_sum > 0 else 0
        results["portfolio_summary"] = {
            "expected_moic": round(weighted_moic, 2),
            "scenarios_run": len(portfolio_moics),
            "base_scenario": "balanced"
        }

    # 출력
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Finance output written: {out_path}")
    print(f"   Expected Portfolio MOIC: {results['portfolio_summary'].get('expected_moic', 'N/A')}x")
    return 0


if __name__ == "__main__":
    sys.exit(main())
