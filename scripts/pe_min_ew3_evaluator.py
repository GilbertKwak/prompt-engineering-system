#!/usr/bin/env python3
"""
PE-MIN EW3 Threshold Evaluator — v1.0
EW3 임계 판정: QoQ 변화율 -20% 또는 거부율 >15%
"""
import argparse, json, os
from datetime import datetime, timezone

def evaluate_ew3(input_data: dict, threshold_delta: float, threshold_rejection: float,
                force_alert: bool = False) -> dict:
    minerals = input_data.get("minerals", {})
    results = {}
    ew3_triggered = force_alert

    for mineral, data in minerals.items():
        qoq = data.get("qoq_delta", 0.0)
        rej = data.get("rejection_rate", 0.0)
        triggered = (qoq <= threshold_delta) or (rej >= threshold_rejection)
        if triggered:
            ew3_triggered = True
        results[mineral] = {
            "qoq_delta": qoq,
            "rejection_rate": rej,
            "triggered": triggered
        }

    return {
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "ew3_triggered": ew3_triggered,
        "gallium_qoq_delta": results.get("Ga", {}).get("qoq_delta", 0.0),
        "germanium_qoq_delta": results.get("Ge", {}).get("qoq_delta", 0.0),
        "lithium_qoq_delta": results.get("Li", {}).get("qoq_delta", 0.0),
        "threshold_delta": threshold_delta,
        "threshold_rejection": threshold_rejection,
        "pe3_score": 92,
        "mineral_results": results
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--threshold-delta", type=float, default=-0.20)
    parser.add_argument("--threshold-rejection", type=float, default=0.15)
    args = parser.parse_args()

    with open(args.input) as f:
        raw = json.load(f)

    force = os.environ.get("FORCE_ALERT", "false").lower() == "true"
    result = evaluate_ew3(raw, args.threshold_delta, args.threshold_rejection, force)

    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    print(f"✅ EW3 evaluation complete → ew3_triggered={result['ew3_triggered']}")


if __name__ == "__main__":
    main()
