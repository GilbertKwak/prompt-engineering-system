#!/usr/bin/env python3
"""
ai_ew_detector.py — Early Warning (EW) Detector v2
AI Intel Weekly pipeline: Step 2

Inputs : output/ai_intel/*.json  (from ai_intel_collector.py)
Outputs: ew_report.json          (EW signals, severity, domain weights)

EW Trigger Logic:
  1. Metric threshold breach  → score += weight
  2. Keyword frequency hit    → score += 0.5 per hit
  3. Cross-domain correlation → score *= 1.2 bonus
  Severity: NONE(<2) / WATCH(2-4) / ALERT(4-6) / CRITICAL(6+)
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# ── EW Configuration ──────────────────────────────────────────────────────────

EW_METRIC_THRESHOLDS: dict[str, dict] = {
    "training_cost_reduction_pct": {"threshold": 50, "op": "gte", "weight": 2.0, "domain": "model_architecture"},
    "inference_cost_reduction_pct": {"threshold": 40, "op": "gte", "weight": 1.5, "domain": "model_architecture"},
    "new_model_releases_count":     {"threshold": 3,  "op": "gte", "weight": 1.0, "domain": "model_architecture"},
    "enterprise_adoption_pct":      {"threshold": 40, "op": "gte", "weight": 1.5, "domain": "enterprise_deployment"},
    "rag_migration_rate_pct":       {"threshold": 30, "op": "gte", "weight": 1.0, "domain": "enterprise_deployment"},
    "open_source_share_pct":        {"threshold": 50, "op": "gte", "weight": 1.5, "domain": "open_source_dynamics"},
    "regulatory_actions_count":     {"threshold": 2,  "op": "gte", "weight": 2.0, "domain": "regulatory_geopolitical"},
    "china_export_restriction_new": {"threshold": 1,  "op": "gte", "weight": 2.5, "domain": "regulatory_geopolitical"},
    "gpu_supply_shortage_severity": {"threshold": 7,  "op": "gte", "weight": 2.0, "domain": "hardware_infrastructure"},
    "hbm_price_change_pct":         {"threshold": 20, "op": "gte", "weight": 1.5, "domain": "hardware_infrastructure"},
    "agent_deployment_incidents":   {"threshold": 3,  "op": "gte", "weight": 1.5, "domain": "agentic_multimodal"},
    "multimodal_capability_jump":   {"threshold": 1,  "op": "gte", "weight": 1.0, "domain": "agentic_multimodal"},
}

EW_KEYWORDS: list[dict] = [
    {"pattern": r"export.{0,10}restrict|ban.{0,10}chip|sanction.{0,10}(nvidia|tsmc|asml)",
     "weight": 2.5, "tag": "EW_EXPORT_CONTROL"},
    {"pattern": r"breakthrou|paradigm.shift|10x.{0,5}(faster|cheaper|better)",
     "weight": 1.5, "tag": "EW_CAPABILITY_JUMP"},
    {"pattern": r"(openai|anthropic|google).{0,20}(acqui|merger|partner).{0,20}(microsoft|amazon|apple)",
     "weight": 2.0, "tag": "EW_STRATEGIC_ALLIANCE"},
    {"pattern": r"regulation.{0,15}(pass|sign|enforce)|EU AI Act|AI Safety.{0,10}(law|bill|mandate)",
     "weight": 2.0, "tag": "EW_REGULATORY"},
    {"pattern": r"open.?source.{0,20}(match|surpass|beat).{0,20}(gpt|claude|gemini)",
     "weight": 1.5, "tag": "EW_OPENSOURCE_PARITY"},
    {"pattern": r"rag.{0,15}(dead|obsolete|replac).{0,15}(fine.?tun|memory|context)",
     "weight": 1.0, "tag": "EW_RAG_MIGRATION"},
    {"pattern": r"(hbm|gpu|tpu).{0,20}(shortage|supply.{0,10}crunch|allocation)",
     "weight": 2.0, "tag": "EW_HW_SUPPLY"},
    {"pattern": r"agent.{0,20}(autonom|self.direct|unsupervised).{0,20}(deploy|production)",
     "weight": 1.5, "tag": "EW_AGENT_AUTONOMY"},
]

SEVERITY_MATRIX = [
    (6.0, "CRITICAL"),
    (4.0, "ALERT"),
    (2.0, "WATCH"),
    (0.0, "NONE"),
]

DOMAIN_CROSS_CORRELATIONS: list[set] = [
    {"model_architecture", "hardware_infrastructure"},
    {"regulatory_geopolitical", "hardware_infrastructure"},
    {"enterprise_deployment", "agentic_multimodal"},
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _score_severity(score: float) -> str:
    for threshold, label in SEVERITY_MATRIX:
        if score >= threshold:
            return label
    return "NONE"


def _extract_number(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        m = re.search(r"[-+]?\d+\.?\d*", value.replace(",", ""))
        if m:
            return float(m.group())
    return None


def _find_metric(data: dict, metric_key: str) -> float | None:
    """Search metrics dict with fuzzy key matching."""
    metrics: dict = data.get("metrics", {})
    if not metrics:
        return None
    # exact match
    if metric_key in metrics:
        return _extract_number(metrics[metric_key])
    # partial / underscore-tolerant match
    norm = metric_key.lower().replace("_", "")
    for k, v in metrics.items():
        if norm in k.lower().replace("_", ""):
            return _extract_number(v)
    return None


def _text_body(data: dict) -> str:
    """Combine all text fields from an intel JSON for keyword scanning."""
    parts = []
    for field in ("summary", "analysis", "key_facts", "recommendations"):
        val = data.get(field, "")
        if isinstance(val, list):
            parts.extend(val)
        elif isinstance(val, str):
            parts.append(val)
    return " ".join(parts).lower()


# ── Core Detection ────────────────────────────────────────────────────────────

def detect_ew(intel_dir: str, week: str) -> dict:
    intel_path = Path(intel_dir)
    if not intel_path.exists():
        print(f"[EW] Directory not found: {intel_dir}", file=sys.stderr)
        sys.exit(1)

    json_files = sorted(intel_path.glob("*.json"))
    if not json_files:
        print(f"[EW] No JSON files found in {intel_dir}", file=sys.stderr)
        sys.exit(1)

    triggered_signals: list[dict] = []
    domain_scores: dict[str, float] = {}
    total_score: float = 0.0
    domains_triggered: set[str] = set()

    for jf in json_files:
        try:
            with open(jf, encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"[EW] Skip {jf.name}: {e}", file=sys.stderr)
            continue

        domain = data.get("domain", jf.stem)
        text   = _text_body(data)

        # ── 1. Metric threshold checks ──
        for metric_key, cfg in EW_METRIC_THRESHOLDS.items():
            if cfg["domain"] not in domain:
                # still check cross-domain if file domain is ambiguous
                if domain not in ("all", "overview"):
                    continue
            val = _find_metric(data, metric_key)
            if val is None:
                continue
            threshold = cfg["threshold"]
            op = cfg["op"]
            triggered = (
                (op == "gte" and val >= threshold) or
                (op == "lte" and val <= threshold) or
                (op == "gt"  and val >  threshold) or
                (op == "lt"  and val <  threshold)
            )
            if triggered:
                w = cfg["weight"]
                total_score += w
                domain_scores[domain] = domain_scores.get(domain, 0.0) + w
                domains_triggered.add(cfg["domain"])
                triggered_signals.append({
                    "type":    "METRIC_BREACH",
                    "domain":  domain,
                    "metric":  metric_key,
                    "value":   val,
                    "threshold": threshold,
                    "weight":  w,
                    "tag":     f"EW_{metric_key.upper()}",
                    "source_file": jf.name,
                })

        # ── 2. Keyword frequency hits ──
        for kw_cfg in EW_KEYWORDS:
            hits = len(re.findall(kw_cfg["pattern"], text, re.IGNORECASE))
            if hits >= 2:
                w = kw_cfg["weight"] * min(hits / 2, 2.0)  # cap at 2x
                total_score += w
                domain_scores[domain] = domain_scores.get(domain, 0.0) + w
                domains_triggered.add(domain)
                triggered_signals.append({
                    "type":    "KEYWORD_HIT",
                    "domain":  domain,
                    "pattern": kw_cfg["pattern"][:60],
                    "hits":    hits,
                    "weight":  round(w, 2),
                    "tag":     kw_cfg["tag"],
                    "source_file": jf.name,
                })

    # ── 3. Cross-domain correlation bonus ──
    cross_bonus_applied = False
    for corr_set in DOMAIN_CROSS_CORRELATIONS:
        if corr_set.issubset(domains_triggered):
            total_score *= 1.2
            cross_bonus_applied = True
            triggered_signals.append({
                "type":   "CROSS_DOMAIN_CORRELATION",
                "domains": list(corr_set),
                "bonus":  "×1.2",
                "tag":    "EW_CROSS_DOMAIN",
            })
            break  # apply once

    severity   = _score_severity(total_score)
    ew_triggered = severity != "NONE"

    # top signal tags (deduplicated)
    signal_tags = list(dict.fromkeys(
        s["tag"] for s in triggered_signals if s.get("tag")
    ))

    report = {
        "week":          week,
        "generated_at":  datetime.utcnow().isoformat() + "Z",
        "ew_triggered":  ew_triggered,
        "severity":      severity,
        "total_score":   round(total_score, 2),
        "signal_count":  len(triggered_signals),
        "signal_tags":   signal_tags,
        "domain_scores": {k: round(v, 2) for k, v in sorted(domain_scores.items(), key=lambda x: -x[1])},
        "cross_bonus":   cross_bonus_applied,
        "signals":       triggered_signals,
        "summary": (
            f"EW {severity}: score={total_score:.1f}, "
            f"{len(triggered_signals)} signals across "
            f"{len(domain_scores)} domains"
        ),
    }

    return report


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="AI Intel Early Warning Detector")
    p.add_argument("--input-dir",  default="output/ai_intel", help="Directory with intel JSON files")
    p.add_argument("--week",       required=True,              help="ISO week tag e.g. 2026-W21")
    p.add_argument("--output",     default="",                 help="Output JSON path (default: input-dir/ew_report.json)")
    p.add_argument("--threshold",  type=float, default=2.0,    help="Minimum score to trigger EW (default 2.0)")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    print(f"[EW] Scanning: {args.input_dir}  |  Week: {args.week}")
    report = detect_ew(args.input_dir, args.week)

    # Apply custom threshold override
    if report["total_score"] < args.threshold:
        report["ew_triggered"] = False
        report["severity"]     = "NONE"

    # Output path
    out_path = args.output or str(Path(args.input_dir) / "ew_report.json")
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"[EW] Severity : {report['severity']}")
    print(f"[EW] Score    : {report['total_score']}")
    print(f"[EW] Signals  : {report['signal_count']}")
    print(f"[EW] Tags     : {', '.join(report['signal_tags']) or 'none'}")
    print(f"[EW] Output   : {out_path}")

    # GitHub Actions outputs
    gh_output = os.environ.get("GITHUB_OUTPUT", "")
    if gh_output:
        with open(gh_output, "a") as f:
            f.write(f"ew_triggered={str(report['ew_triggered']).lower()}\n")
            f.write(f"ew_severity={report['severity']}\n")
            f.write(f"ew_score={report['total_score']}\n")
            f.write(f"ew_count={report['signal_count']}\n")
            tags_str = ",".join(report["signal_tags"])
            f.write(f"ew_signals={tags_str}\n")

    sys.exit(0 if not report["ew_triggered"] else 2)


if __name__ == "__main__":
    main()
