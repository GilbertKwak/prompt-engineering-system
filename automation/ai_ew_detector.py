#!/usr/bin/env python3
"""
ai_ew_detector.py — AI Intel Early Warning Detector
Detects paradigm shift signals from collected intel JSON files.

Usage:
    python ai_ew_detector.py --input-dir output/ai_intel --week 2026-W21 --output ew_report.json
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# ── EW threshold config ────────────────────────────────────────────────────────
EW_THRESHOLDS = {
    "adoption_rate_enterprise": {"field": "adoption_rate_enterprise", "operator": ">=", "value": 35.0, "label": "Enterprise Adoption Surge"},
    "model_release_frequency":  {"field": "model_release_frequency",  "operator": ">=", "value": 3.0,  "label": "Rapid Model Release Cycle"},
    "cost_reduction_pct":       {"field": "cost_reduction_pct",       "operator": ">=", "value": 40.0, "label": "Dramatic Cost Reduction"},
    "open_source_share":        {"field": "open_source_share",        "operator": ">=", "value": 50.0, "label": "Open Source Dominance"},
    "agent_autonomy_index":     {"field": "agent_autonomy_index",     "operator": ">=", "value": 0.7,  "label": "High Agent Autonomy"},
    "multimodal_adoption":      {"field": "multimodal_adoption",      "operator": ">=", "value": 60.0, "label": "Multimodal Mass Adoption"},
}

EW_KEYWORDS = [
    "paradigm shift", "breakthrough", "disruption", "transformation",
    "10x improvement", "order of magnitude", "unprecedented",
    "emergency", "critical inflection", "game changer", "revolutionary",
]

SEVERITY_MAP = {
    0: "NONE",
    1: "LOW",
    2: "MEDIUM",
    3: "HIGH",
    4: "CRITICAL",
}


# ── helpers ────────────────────────────────────────────────────────────────────

def _compare(value: float, operator: str, threshold: float) -> bool:
    ops = {">=": lambda a, b: a >= b, ">": lambda a, b: a > b,
           "<=": lambda a, b: a <= b, "<": lambda a, b: a < b,
           "==": lambda a, b: a == b}
    fn = ops.get(operator)
    return fn(value, threshold) if fn else False


def _extract_metric(data: dict, field: str) -> float | None:
    """Multi-level metric extraction with fuzzy key matching."""
    # Direct key
    if field in data:
        try:
            return float(data[field])
        except (TypeError, ValueError):
            pass
    # Nested under 'metrics'
    metrics = data.get("metrics", {})
    if isinstance(metrics, dict) and field in metrics:
        try:
            return float(metrics[field])
        except (TypeError, ValueError):
            pass
    # Fuzzy: partial key match
    for key, val in {**data, **metrics}.items():
        if field.replace("_", "") in key.replace("_", ""):
            try:
                return float(val)
            except (TypeError, ValueError):
                pass
    # Text parsing fallback: look for numbers near the field name in analysis text
    text = " ".join(str(v) for v in data.values() if isinstance(v, str))
    pattern = rf"{re.escape(field.replace('_', ' '))}[^\d]*(\d+\.?\d*)"
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            pass
    return None


def _keyword_hit_count(data: dict) -> int:
    """Count EW keyword hits in all string values."""
    text = json.dumps(data).lower()
    return sum(1 for kw in EW_KEYWORDS if kw.lower() in text)


# ── core detection ─────────────────────────────────────────────────────────────

def detect_ew_from_file(filepath: Path) -> dict:
    """Analyse a single intel JSON file for EW signals."""
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    triggered_signals: list[dict] = []
    metric_values: dict = {}

    # Metric-based detection
    for rule_key, rule in EW_THRESHOLDS.items():
        val = _extract_metric(data, rule["field"])
        if val is not None:
            metric_values[rule["field"]] = val
            if _compare(val, rule["operator"], rule["value"]):
                triggered_signals.append({
                    "signal": rule["label"],
                    "field": rule["field"],
                    "detected_value": val,
                    "threshold": rule["value"],
                    "operator": rule["operator"],
                    "source": "metric",
                })

    # Keyword-based heuristic fallback
    hit_count = _keyword_hit_count(data)
    if hit_count >= 2 and not triggered_signals:
        triggered_signals.append({
            "signal": "Keyword-based EW Heuristic",
            "field": "keyword_hits",
            "detected_value": hit_count,
            "threshold": 2,
            "operator": ">=",
            "source": "keyword",
        })

    domain = data.get("domain", filepath.stem)
    return {
        "file": str(filepath),
        "domain": domain,
        "triggered": len(triggered_signals) > 0,
        "signals": triggered_signals,
        "metric_values": metric_values,
        "keyword_hits": hit_count,
    }


def run_detection(input_dir: str, week: str, output_path: str) -> dict:
    """Run EW detection across all JSON files in input_dir."""
    intel_files = list(Path(input_dir).glob("*.json"))
    if not intel_files:
        print(f"[WARN] No JSON files found in {input_dir}", file=sys.stderr)

    all_results = []
    all_signals: list[str] = []
    total_triggered = 0

    for fp in intel_files:
        try:
            result = detect_ew_from_file(fp)
            all_results.append(result)
            if result["triggered"]:
                total_triggered += 1
                all_signals.extend(s["signal"] for s in result["signals"])
            print(f"  {'🚨' if result['triggered'] else '✅'} {fp.name}: "
                  f"{len(result['signals'])} signal(s), keyword_hits={result['keyword_hits']}")
        except Exception as e:
            print(f"[ERROR] {fp.name}: {e}", file=sys.stderr)

    # Severity
    severity_level = min(total_triggered, 4)
    severity = SEVERITY_MAP[severity_level]

    report = {
        "week": week,
        "run_timestamp": datetime.utcnow().isoformat() + "Z",
        "ew_triggered": total_triggered > 0,
        "ew_count": total_triggered,
        "severity": severity,
        "ew_signals": list(set(all_signals)),
        "files_analysed": len(intel_files),
        "detail": all_results,
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n[EW Report] triggered={report['ew_triggered']}, "
          f"count={report['ew_count']}, severity={severity}")
    print(f"[EW Report] saved → {output_path}")
    return report


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="AI Intel Early Warning Detector",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--input-dir",  required=True,  help="Directory containing intel JSON files")
    parser.add_argument("--week",        required=True,  help="ISO week string e.g. 2026-W21")
    parser.add_argument("--output",      required=True,  help="Output JSON file path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(f"\n{'='*60}")
    print(f"AI Intel Early Warning Detector — {args.week}")
    print(f"{'='*60}")
    print(f"Input dir : {args.input_dir}")
    print(f"Output    : {args.output}\n")

    report = run_detection(args.input_dir, args.week, args.output)
    sys.exit(0 if not report["ew_triggered"] else 2)  # exit 2 = EW triggered


if __name__ == "__main__":
    main()
