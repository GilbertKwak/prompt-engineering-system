#!/usr/bin/env python3
"""
ai_ew_detector.py  —  AI Intel Early-Warning Detector

Detection layers (in order):
  1. Threshold   : numeric metrics extracted from intel JSON vs hard limits
  2. Keyword     : weighted keyword scan across all text content
  3. Delta       : week-over-week numeric change rate

Outputs a structured EW report JSON.

Usage:
  python ai_ew_detector.py \
    --input-dir  output/ai_intel \
    --week       2026-W21 \
    --prev-dir   output/ai_intel_prev   (optional, enables delta layer) \
    --output     output/ew_report.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# EW Configuration
# ---------------------------------------------------------------------------

EW_THRESHOLDS: Dict[str, Dict[str, Any]] = {
    # key: {metric_keys, operator, value, severity, domain}
    "enterprise_ai_adoption_rapid": {
        "metric_keys": ["enterprise_adoption_rate", "adoption_rate", "enterprise_adoption"],
        "operator": ">",
        "value": 60.0,
        "severity": "HIGH",
        "domain": "enterprise_deployment",
    },
    "rag_replacement_threshold": {
        "metric_keys": ["rag_replacement_rate", "fine_tuning_to_rag_ratio", "rag_ratio"],
        "operator": ">",
        "value": 40.0,
        "severity": "MEDIUM",
        "domain": "enterprise_deployment",
    },
    "gpu_demand_spike": {
        "metric_keys": ["gpu_demand_index", "h100_demand", "gpu_demand"],
        "operator": ">",
        "value": 80.0,
        "severity": "HIGH",
        "domain": "infrastructure",
    },
    "open_source_dominance": {
        "metric_keys": ["open_source_share", "oss_market_share"],
        "operator": ">",
        "value": 50.0,
        "severity": "HIGH",
        "domain": "model_ecosystem",
    },
    "reasoning_model_latency_drop": {
        "metric_keys": ["reasoning_latency_reduction", "latency_reduction"],
        "operator": ">",
        "value": 30.0,
        "severity": "MEDIUM",
        "domain": "model_performance",
    },
    "cost_reduction_steep": {
        "metric_keys": ["api_cost_reduction", "token_cost_reduction", "cost_reduction"],
        "operator": ">",
        "value": 40.0,
        "severity": "MEDIUM",
        "domain": "economics",
    },
}

KEYWORD_WEIGHTS: Dict[str, float] = {
    # Disruption signals
    "paradigm shift": 3.0,
    "disruption": 2.5,
    "breakthrough": 2.0,
    "unprecedented": 2.0,
    "game-changing": 2.0,
    "transformative": 1.5,
    # Adoption signals
    "mass adoption": 2.5,
    "enterprise rollout": 2.0,
    "rapid deployment": 2.0,
    "scaled deployment": 1.5,
    # Technology-specific
    "replaces fine-tuning": 3.0,
    "rag dominance": 2.5,
    "agentic workflow": 2.0,
    "multi-agent": 1.5,
    "reasoning model": 1.5,
    # Market signals
    "market consolidation": 2.5,
    "winner-take-all": 2.5,
    "monopoly": 2.0,
    "dominant player": 1.5,
}

KEYWORD_EW_THRESHOLD = 6.0  # total weighted score to trigger EW

DELTA_EW_THRESHOLD = 0.25   # 25% week-over-week change in any metric


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_number(value: Any) -> Optional[float]:
    """Convert various representations to float."""
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        m = re.search(r"[\d.]+", value.replace(",", ""))
        if m:
            return float(m.group())
    return None


def _find_metric(data: Dict, keys: List[str]) -> Optional[float]:
    """Search nested dict for any of the candidate keys."""
    metrics_obj = data.get("metrics", {})
    for source in (metrics_obj, data):
        for k, v in (source.items() if isinstance(source, dict) else []):
            kn = k.lower().replace(" ", "_").replace("-", "_")
            for candidate in keys:
                cn = candidate.lower().replace(" ", "_")
                if kn == cn or kn.endswith(cn) or cn in kn:
                    n = _extract_number(v)
                    if n is not None:
                        return n
    return None


def _collect_text(obj: Any, acc: List[str]) -> None:
    """Recursively collect all string values."""
    if isinstance(obj, str):
        acc.append(obj.lower())
    elif isinstance(obj, dict):
        for v in obj.values():
            _collect_text(v, acc)
    elif isinstance(obj, list):
        for item in obj:
            _collect_text(item, acc)


# ---------------------------------------------------------------------------
# Detection Layers
# ---------------------------------------------------------------------------

def layer_threshold(
    intel_files: List[Path],
) -> Tuple[bool, List[Dict]]:
    """Layer 1 — metric threshold check."""
    triggered: List[Dict] = []
    for fp in intel_files:
        try:
            data = json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            continue
        for rule_id, rule in EW_THRESHOLDS.items():
            val = _find_metric(data, rule["metric_keys"])
            if val is None:
                continue
            threshold = rule["value"]
            op = rule["operator"]
            hit = (
                (op == ">" and val > threshold)
                or (op == "<" and val < threshold)
                or (op == ">=" and val >= threshold)
                or (op == "<=" and val <= threshold)
            )
            if hit:
                triggered.append({
                    "rule_id": rule_id,
                    "layer": "threshold",
                    "severity": rule["severity"],
                    "domain": rule["domain"],
                    "metric_value": val,
                    "threshold": threshold,
                    "operator": op,
                    "source_file": fp.name,
                })
    return bool(triggered), triggered


def layer_keyword(
    intel_files: List[Path],
) -> Tuple[bool, List[Dict]]:
    """Layer 2 — weighted keyword scan."""
    texts: List[str] = []
    for fp in intel_files:
        try:
            data = json.loads(fp.read_text(encoding="utf-8"))
            _collect_text(data, texts)
        except Exception:
            continue
    combined = " ".join(texts)

    score = 0.0
    hits: Dict[str, int] = {}
    for kw, weight in KEYWORD_WEIGHTS.items():
        count = combined.count(kw.lower())
        if count > 0:
            score += weight * count
            hits[kw] = count

    triggered = score >= KEYWORD_EW_THRESHOLD
    signals = []
    if triggered:
        for kw, cnt in sorted(hits.items(), key=lambda x: -KEYWORD_WEIGHTS[x[0]]):
            signals.append({
                "rule_id": f"kw_{kw.replace(' ', '_')}",
                "layer": "keyword",
                "severity": "MEDIUM",
                "keyword": kw,
                "hit_count": cnt,
                "weighted_score": KEYWORD_WEIGHTS[kw] * cnt,
            })
    return triggered, signals


def layer_delta(
    intel_files: List[Path],
    prev_files: List[Path],
) -> Tuple[bool, List[Dict]]:
    """Layer 3 — week-over-week delta check."""
    if not prev_files:
        return False, []

    def _build_metric_map(files: List[Path]) -> Dict[str, float]:
        result: Dict[str, float] = {}
        for fp in files:
            try:
                data = json.loads(fp.read_text(encoding="utf-8"))
                m = data.get("metrics", {})
                if isinstance(m, dict):
                    for k, v in m.items():
                        n = _extract_number(v)
                        if n is not None:
                            result[k.lower()] = n
            except Exception:
                continue
        return result

    curr_map = _build_metric_map(intel_files)
    prev_map = _build_metric_map(prev_files)

    signals = []
    for key, curr_val in curr_map.items():
        if key not in prev_map:
            continue
        prev_val = prev_map[key]
        if prev_val == 0:
            continue
        delta_rate = abs((curr_val - prev_val) / prev_val)
        if delta_rate >= DELTA_EW_THRESHOLD:
            signals.append({
                "rule_id": f"delta_{key}",
                "layer": "delta",
                "severity": "HIGH" if delta_rate >= 0.5 else "MEDIUM",
                "metric": key,
                "prev_value": prev_val,
                "curr_value": curr_val,
                "delta_rate": round(delta_rate, 4),
            })
    return bool(signals), signals


# ---------------------------------------------------------------------------
# Severity Aggregation
# ---------------------------------------------------------------------------

def _aggregate_severity(signals: List[Dict]) -> str:
    sevs = {s.get("severity", "LOW") for s in signals}
    if "HIGH" in sevs:
        return "HIGH"
    if "MEDIUM" in sevs:
        return "MEDIUM"
    if signals:
        return "LOW"
    return "NONE"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def detect(
    input_dir: Path,
    week: str,
    prev_dir: Optional[Path] = None,
    output_path: Optional[Path] = None,
) -> Dict:
    intel_files = sorted(input_dir.glob("*.json")) if input_dir.exists() else []
    prev_files = sorted(prev_dir.glob("*.json")) if (prev_dir and prev_dir.exists()) else []

    ew_t, sig_t = layer_threshold(intel_files)
    ew_k, sig_k = layer_keyword(intel_files)
    ew_d, sig_d = layer_delta(intel_files, prev_files)

    all_signals = sig_t + sig_k + sig_d
    ew_triggered = ew_t or ew_k or ew_d
    severity = _aggregate_severity(all_signals)

    report: Dict = {
        "week": week,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "ew_triggered": ew_triggered,
        "ew_count": len(all_signals),
        "severity": severity,
        "layers": {
            "threshold": {"triggered": ew_t, "signal_count": len(sig_t)},
            "keyword": {"triggered": ew_k, "signal_count": len(sig_k)},
            "delta": {"triggered": ew_d, "signal_count": len(sig_d)},
        },
        "signals": all_signals,
        "intel_files_scanned": [f.name for f in intel_files],
    }

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[EW] Report written: {output_path}")

    print(f"[EW] triggered={ew_triggered}  severity={severity}  signals={len(all_signals)}")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Intel Early-Warning Detector")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--week", required=True)
    parser.add_argument("--prev-dir", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    report = detect(
        input_dir=Path(args.input_dir),
        week=args.week,
        prev_dir=Path(args.prev_dir) if args.prev_dir else None,
        output_path=Path(args.output) if args.output else None,
    )

    if report["ew_triggered"]:
        sys.exit(1)   # non-zero → GitHub Actions can branch on EW
    sys.exit(0)


if __name__ == "__main__":
    main()
