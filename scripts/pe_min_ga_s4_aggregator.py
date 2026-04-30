#!/usr/bin/env python3
"""
PE-MIN Ga S4 Aggregator — v1.0
비중국 갈륨 생산량 집계 & 50톤 임계 판정
"""
import argparse, json
from datetime import datetime, timezone

def aggregate_and_evaluate(raw: dict, threshold: float) -> dict:
    agencies = raw.get("agencies", {})
    breakdown = {}
    total_tons = 0.0

    for agency, data in agencies.items():
        tons = data.get("tons", 0.0)
        breakdown[agency] = tons
        total_tons += tons

    threshold_achieved = total_tons >= threshold
    s4_status = "INACTIVE" if threshold_achieved else "ACTIVE"

    return {
        "report_month": raw.get("reference_month", ""),
        "total_non_cn_tons": round(total_tons, 2),
        "threshold_tons": threshold,
        "threshold_achieved": threshold_achieved,
        "s4_status": s4_status,
        "breakdown": breakdown,
        "evaluated_at": datetime.now(timezone.utc).isoformat()
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--threshold", type=float, default=50.0)
    args = parser.parse_args()

    with open(args.input) as f:
        raw = json.load(f)

    result = aggregate_and_evaluate(raw, args.threshold)

    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)

    print(f"✅ Aggregation: {result['total_non_cn_tons']:.1f}t | "
          f"threshold={'✅' if result['threshold_achieved'] else '⚠️'} | S4={result['s4_status']}")


if __name__ == "__main__":
    main()
