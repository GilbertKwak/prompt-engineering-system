#!/usr/bin/env python3
"""
ai_ew_detector.py — Early Warning (EW) Detector v3
AI Intel Weekly pipeline: Step 2

New in v3:
  - Velocity tracking: compares current week vs prev week score (week-over-week delta)
  - Sentiment scorer: negative sentiment amplification
  - Multi-source JSON merge: handles nested domain arrays
  - GITHUB_STEP_SUMMARY markdown output
  - Dry-run mode: --dry-run flag prints report without writing

Inputs : output/ai_intel/*.json  (from ai_intel_collector.py)
Outputs: ew_report.json, GITHUB_STEP_SUMMARY

EW Trigger Logic:
  1. Metric threshold breach  → score += weight
  2. Keyword frequency hit    → score += weight * min(hits/2, 2.0)
  3. Sentiment negativity     → score += 0.3 per negative keyword
  4. Cross-domain correlation → score *= 1.2 bonus
  5. Velocity spike           → score *= 1.3 if delta > 50%
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
    "training_cost_reduction_pct":  {"threshold": 50,  "op": "gte", "weight": 2.0, "domain": "model_architecture"},
    "inference_cost_reduction_pct": {"threshold": 40,  "op": "gte", "weight": 1.5, "domain": "model_architecture"},
    "new_model_releases_count":     {"threshold": 3,   "op": "gte", "weight": 1.0, "domain": "model_architecture"},
    "context_window_tokens":        {"threshold": 500000, "op": "gte", "weight": 1.5, "domain": "model_architecture"},
    "enterprise_adoption_pct":      {"threshold": 40,  "op": "gte", "weight": 1.5, "domain": "enterprise_deployment"},
    "rag_migration_rate_pct":       {"threshold": 30,  "op": "gte", "weight": 1.0, "domain": "enterprise_deployment"},
    "ai_infrastructure_spend_bn":   {"threshold": 20,  "op": "gte", "weight": 1.5, "domain": "enterprise_deployment"},
    "open_source_share_pct":        {"threshold": 50,  "op": "gte", "weight": 1.5, "domain": "open_source_dynamics"},
    "open_source_model_count":      {"threshold": 10,  "op": "gte", "weight": 1.0, "domain": "open_source_dynamics"},
    "regulatory_actions_count":     {"threshold": 2,   "op": "gte", "weight": 2.0, "domain": "regulatory_geopolitical"},
    "china_export_restriction_new": {"threshold": 1,   "op": "gte", "weight": 2.5, "domain": "regulatory_geopolitical"},
    "geopolitical_risk_score":      {"threshold": 7,   "op": "gte", "weight": 2.0, "domain": "regulatory_geopolitical"},
    "gpu_supply_shortage_severity": {"threshold": 7,   "op": "gte", "weight": 2.0, "domain": "hardware_infrastructure"},
    "hbm_price_change_pct":         {"threshold": 20,  "op": "gte", "weight": 1.5, "domain": "hardware_infrastructure"},
    "datacenter_capex_bn":          {"threshold": 10,  "op": "gte", "weight": 1.0, "domain": "hardware_infrastructure"},
    "agent_deployment_incidents":   {"threshold": 3,   "op": "gte", "weight": 1.5, "domain": "agentic_multimodal"},
    "multimodal_capability_jump":   {"threshold": 1,   "op": "gte", "weight": 1.0, "domain": "agentic_multimodal"},
    "autonomous_agent_deploy_pct":  {"threshold": 15,  "op": "gte", "weight": 1.5, "domain": "agentic_multimodal"},
}

EW_KEYWORDS: list[dict] = [
    {"pattern": r"export.{0,10}restrict|ban.{0,10}chip|sanction.{0,10}(nvidia|tsmc|asml|smic)",
     "weight": 2.5, "tag": "EW_EXPORT_CONTROL"},
    {"pattern": r"breakthrough|paradigm.shift|10x.{0,5}(faster|cheaper|better)|order.of.magnitude",
     "weight": 1.5, "tag": "EW_CAPABILITY_JUMP"},
    {"pattern": r"(openai|anthropic|google|meta).{0,20}(acqui|merger|partner).{0,20}(microsoft|amazon|apple|nvidia)",
     "weight": 2.0, "tag": "EW_STRATEGIC_ALLIANCE"},
    {"pattern": r"regulation.{0,15}(pass|sign|enforce|implement)|EU AI Act|AI Safety.{0,10}(law|bill|mandate|executive)",
     "weight": 2.0, "tag": "EW_REGULATORY"},
    {"pattern": r"open.?source.{0,20}(match|surpass|beat|outperform).{0,20}(gpt|claude|gemini|o[234])",
     "weight": 1.5, "tag": "EW_OPENSOURCE_PARITY"},
    {"pattern": r"rag.{0,15}(dead|obsolete|replac|displace).{0,15}(fine.?tun|long.context|memory)",
     "weight": 1.0, "tag": "EW_RAG_MIGRATION"},
    {"pattern": r"(hbm|gpu|tpu|npu).{0,20}(shortage|supply.{0,10}crunch|allocation.{0,10}cut|lead.time)",
     "weight": 2.0, "tag": "EW_HW_SUPPLY"},
    {"pattern": r"agent.{0,20}(autonom|self.direct|unsupervised|recursive).{0,20}(deploy|production|enterprise)",
     "weight": 1.5, "tag": "EW_AGENT_AUTONOMY"},
    {"pattern": r"reasoning.{0,20}(replac|supersede|make.obsolete).{0,20}(rag|retrieval|search)",
     "weight": 1.5, "tag": "EW_REASONING_SHIFT"},
    {"pattern": r"(deepseek|mistral|qwen|llama).{0,20}(match|beat|outperform).{0,20}(gpt-4|claude|gemini.ultra)",
     "weight": 2.0, "tag": "EW_CHINA_MODEL_PARITY"},
]

NEGATIVE_SENTIMENT_PATTERNS = [
    r"crisis|collapse|crash|ban|halt|suspend|shutdown|catastroph",
    r"major.{0,10}(setback|failure|breach|incident|outage)",
    r"(emergency|urgent|immediate).{0,10}(action|response|recall)",
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
    {"regulatory_geopolitical", "open_source_dynamics"},
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
    """Search metrics dict with 3-level fuzzy key matching."""
    metrics: dict = data.get("metrics", {})
    if not metrics:
        return None
    if metric_key in metrics:
        return _extract_number(metrics[metric_key])
    norm = metric_key.lower().replace("_", "")
    for k, v in metrics.items():
        if norm in k.lower().replace("_", ""):
            return _extract_number(v)
    # Try numeric extraction from text fields
    text = _text_body(data)
    label_pat = metric_key.replace("_", ".{0,5}")
    m = re.search(label_pat + r".{0,20}(\d+\.?\d*)", text, re.IGNORECASE)
    if m:
        return float(m.group(1))
    return None


def _text_body(data: dict) -> str:
    """Combine all text fields from an intel JSON for scanning."""
    parts = []
    for field in ("summary", "analysis", "key_facts", "recommendations",
                  "raw_content", "insights", "highlights"):
        val = data.get(field, "")
        if isinstance(val, list):
            parts.extend(str(v) for v in val)
        elif isinstance(val, str):
            parts.append(val)
    return " ".join(parts).lower()


def _score_sentiment(text: str) -> float:
    """Returns negative sentiment amplification score."""
    score = 0.0
    for pat in NEGATIVE_SENTIMENT_PATTERNS:
        hits = len(re.findall(pat, text, re.IGNORECASE))
        score += hits * 0.3
    return min(score, 2.0)  # cap at 2.0


def _load_prev_score(intel_dir: Path, week: str) -> float | None:
    """Load previous week's EW score for velocity tracking."""
    # Look for any ew_report_*.json or prev_ew_report.json
    for fname in ["ew_report_prev.json", "ew_report_previous.json"]:
        fp = intel_dir / fname
        if fp.exists():
            try:
                with open(fp) as f:
                    d = json.load(f)
                return float(d.get("total_score", 0.0))
            except Exception:
                pass
    return None


# ── Step Summary (GitHub Actions) ─────────────────────────────────────────────

def _write_step_summary(report: dict) -> None:
    step_summary = os.environ.get("GITHUB_STEP_SUMMARY", "")
    if not step_summary:
        return
    sev = report["severity"]
    icon = {"CRITICAL": "🔴", "ALERT": "🟠", "WATCH": "🟡", "NONE": "🟢"}.get(sev, "⚪")
    lines = [
        f"## {icon} EW Report — {report['week']}",
        f"| Field | Value |",
        f"|---|---|",
        f"| Severity | **{sev}** |",
        f"| Score | {report['total_score']} |",
        f"| Signals | {report['signal_count']} |",
        f"| Velocity | {report.get('velocity_note', 'N/A')} |",
        "",
        "### Signal Tags",
        ", ".join(f"`{t}`" for t in report["signal_tags"]) or "_none_",
        "",
        "### Domain Scores",
    ]
    for dom, sc in report.get("domain_scores", {}).items():
        lines.append(f"- `{dom}`: {sc}")
    try:
        with open(step_summary, "a") as f:
            f.write("\n".join(lines) + "\n")
    except Exception:
        pass


# ── Core Detection ────────────────────────────────────────────────────────────

def detect_ew(intel_dir: str, week: str, threshold_override: float = 2.0) -> dict:
    intel_path = Path(intel_dir)
    if not intel_path.exists():
        print(f"[EW] Directory not found: {intel_dir}", file=sys.stderr)
        sys.exit(1)

    json_files = sorted(intel_path.glob("*.json"))
    # Exclude ew_report*.json from input
    json_files = [f for f in json_files if not f.name.startswith("ew_report")]
    if not json_files:
        print(f"[EW] No intel JSON files found in {intel_dir}", file=sys.stderr)
        sys.exit(1)

    triggered_signals: list[dict] = []
    domain_scores: dict[str, float] = {}
    total_score: float = 0.0
    domains_triggered: set[str] = set()
    sentiment_score: float = 0.0

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
            target_domain = cfg["domain"]
            # Match by domain substring or allow 'all'/'overview'
            domain_match = (
                target_domain in domain or
                domain in ("all", "overview", "multi") or
                target_domain == domain
            )
            if not domain_match:
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
                domains_triggered.add(target_domain)
                triggered_signals.append({
                    "type":        "METRIC_BREACH",
                    "domain":      domain,
                    "metric":      metric_key,
                    "value":       val,
                    "threshold":   threshold,
                    "weight":      w,
                    "tag":         f"EW_{metric_key.upper()}",
                    "source_file": jf.name,
                })

        # ── 2. Keyword frequency hits ──
        for kw_cfg in EW_KEYWORDS:
            hits = len(re.findall(kw_cfg["pattern"], text, re.IGNORECASE))
            if hits >= 2:
                w = kw_cfg["weight"] * min(hits / 2, 2.0)
                total_score += w
                domain_scores[domain] = domain_scores.get(domain, 0.0) + w
                domains_triggered.add(domain)
                triggered_signals.append({
                    "type":        "KEYWORD_HIT",
                    "domain":      domain,
                    "pattern":     kw_cfg["pattern"][:60],
                    "hits":        hits,
                    "weight":      round(w, 2),
                    "tag":         kw_cfg["tag"],
                    "source_file": jf.name,
                })

        # ── 3. Sentiment score ──
        sent = _score_sentiment(text)
        if sent > 0:
            sentiment_score += sent
            total_score += sent
            domain_scores[domain] = domain_scores.get(domain, 0.0) + sent
            triggered_signals.append({
                "type":        "SENTIMENT_NEG",
                "domain":      domain,
                "weight":      round(sent, 2),
                "tag":         "EW_NEGATIVE_SENTIMENT",
                "source_file": jf.name,
            })

    # ── 4. Cross-domain correlation bonus ──
    cross_bonus_applied = False
    for corr_set in DOMAIN_CROSS_CORRELATIONS:
        if corr_set.issubset(domains_triggered):
            total_score *= 1.2
            cross_bonus_applied = True
            triggered_signals.append({
                "type":    "CROSS_DOMAIN_CORRELATION",
                "domains": list(corr_set),
                "bonus":   "×1.2",
                "tag":     "EW_CROSS_DOMAIN",
            })
            break

    # ── 5. Velocity tracking ──
    velocity_note = "N/A"
    velocity_multiplier = 1.0
    prev_score = _load_prev_score(intel_path, week)
    if prev_score is not None and prev_score > 0:
        delta_pct = (total_score - prev_score) / prev_score * 100
        velocity_note = f"+{delta_pct:.1f}%" if delta_pct >= 0 else f"{delta_pct:.1f}%"
        if delta_pct > 50:
            velocity_multiplier = 1.3
            total_score *= 1.3
            triggered_signals.append({
                "type":     "VELOCITY_SPIKE",
                "prev_score": prev_score,
                "curr_score": round(total_score / 1.3, 2),
                "delta_pct":  round(delta_pct, 1),
                "bonus":      "×1.3",
                "tag":        "EW_VELOCITY_SPIKE",
            })

    # Apply threshold override
    severity = _score_severity(total_score)
    ew_triggered = severity != "NONE" and total_score >= threshold_override

    signal_tags = list(dict.fromkeys(
        s["tag"] for s in triggered_signals if s.get("tag")
    ))

    report = {
        "week":             week,
        "generated_at":     datetime.utcnow().isoformat() + "Z",
        "ew_triggered":     ew_triggered,
        "severity":         severity,
        "total_score":      round(total_score, 2),
        "signal_count":     len([s for s in triggered_signals if s["type"] not in ("CROSS_DOMAIN_CORRELATION", "VELOCITY_SPIKE")]),
        "signal_tags":      signal_tags,
        "domain_scores":    {k: round(v, 2) for k, v in sorted(domain_scores.items(), key=lambda x: -x[1])},
        "sentiment_score":  round(sentiment_score, 2),
        "cross_bonus":      cross_bonus_applied,
        "velocity_note":    velocity_note,
        "velocity_multiplier": velocity_multiplier,
        "signals":          triggered_signals,
        "summary": (
            f"EW {severity}: score={total_score:.1f}, "
            f"{len(triggered_signals)} signals across "
            f"{len(domain_scores)} domains. velocity={velocity_note}"
        ),
    }
    return report


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="AI Intel Early Warning Detector v3")
    p.add_argument("--input-dir",  default="output/ai_intel", help="Directory with intel JSON files")
    p.add_argument("--week",       required=True,              help="ISO week tag e.g. 2026-W21")
    p.add_argument("--output",     default="",                 help="Output JSON path")
    p.add_argument("--threshold",  type=float, default=2.0,    help="Minimum score to trigger EW")
    p.add_argument("--dry-run",    action="store_true",        help="Print report without writing files")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    print(f"[EW v3] Scanning: {args.input_dir}  |  Week: {args.week}")

    report = detect_ew(args.input_dir, args.week, args.threshold)

    out_path = args.output or str(Path(args.input_dir) / "ew_report.json")

    if args.dry_run:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"[EW] Output   : {out_path}")

    print(f"[EW] Severity : {report['severity']}")
    print(f"[EW] Score    : {report['total_score']}")
    print(f"[EW] Signals  : {report['signal_count']}")
    print(f"[EW] Velocity : {report['velocity_note']}")
    print(f"[EW] Tags     : {', '.join(report['signal_tags']) or 'none'}")

    _write_step_summary(report)

    gh_output = os.environ.get("GITHUB_OUTPUT", "")
    if gh_output:
        with open(gh_output, "a") as f:
            f.write(f"ew_triggered={str(report['ew_triggered']).lower()}\n")
            f.write(f"ew_severity={report['severity']}\n")
            f.write(f"ew_score={report['total_score']}\n")
            f.write(f"ew_count={report['signal_count']}\n")
            f.write(f"ew_signals={','.join(report['signal_tags'])}\n")

    sys.exit(0 if not report["ew_triggered"] else 2)


if __name__ == "__main__":
    main()
