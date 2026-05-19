#!/usr/bin/env python3
"""
ai_ew_detector.py — Section A, Step 2
Early Warning 탐지: 임계값 기반 + 키워드 휴리스틱 3-tier 폴백

Usage:
  python ai_ew_detector.py \
    --input-dir output/ai_intel \
    --week 2026-W21 \
    --output output/ai_intel/ew_report.json
"""

import argparse
import json
import os
import re
import sys
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("ai_ew_detector")

# ─── EW Thresholds ──────────────────────────────────────────────────────────
# Format: metric_key → (min_threshold, max_threshold, severity)
# None = no bound in that direction
EW_THRESHOLDS = {
    "enterprise_adoption_rate": (None, 15.0, "CRITICAL"),   # <15% = slow
    "model_release_velocity": (3.0, None, "HIGH"),           # >3 major/wk = fast
    "regulatory_action_count": (2.0, None, "HIGH"),          # >2 actions
    "funding_decline_pct": (20.0, None, "MEDIUM"),           # >20% YoY decline
    "open_source_adoption_surge": (40.0, None, "MEDIUM"),    # >40% surge
    "safety_incident_count": (1.0, None, "CRITICAL"),        # any incident
    "chip_shortage_severity": (7.0, None, "HIGH"),           # scale 1-10
}

# ─── Keyword Heuristics (Tier-3 fallback) ───────────────────────────────────
EW_KEYWORDS = {
    "CRITICAL": [
        "emergency", "crisis", "ban", "shutdown", "breach", "exploit",
        "critical vulnerability", "regulatory halt", "market crash",
        "supply disruption", "data leak", "system failure",
    ],
    "HIGH": [
        "unexpected", "surge", "spike", "rapid adoption", "major release",
        "acquisition", "merger", "breakthrough", "disruption", "pivot",
        "significant regulatory", "major funding", "partnership",
    ],
    "MEDIUM": [
        "accelerating", "growing concern", "watch", "emerging trend",
        "notable", "increasing", "shifting", "transition",
    ],
}

EW_KEYWORD_HIT_THRESHOLD = 2  # hits needed to trigger EW


# ─── Detection Logic ─────────────────────────────────────────────────────────
def extract_metric_value(metrics: dict, key: str) -> Optional[float]:
    """Tier-1: exact key match. Tier-2: fuzzy key match. Tier-3: text parse."""
    # Tier-1: exact
    if key in metrics:
        try:
            val = str(metrics[key]).replace("%", "").replace(",", "").strip()
            return float(val)
        except (ValueError, TypeError):
            pass

    # Tier-2: fuzzy — find key with most token overlap
    key_tokens = set(key.lower().split("_"))
    best_score, best_val = 0, None
    for k, v in metrics.items():
        k_tokens = set(k.lower().replace("-", "_").split("_"))
        score = len(key_tokens & k_tokens)
        if score > best_score:
            try:
                val = str(v).replace("%", "").replace(",", "").strip()
                best_val = float(val)
                best_score = score
            except (ValueError, TypeError):
                pass
    if best_score >= 2:
        return best_val

    # Tier-3: scan all metric values for a number
    for v in metrics.values():
        nums = re.findall(r"[\d]+\.?[\d]*", str(v))
        if nums:
            try:
                return float(nums[0])
            except ValueError:
                pass
    return None


def check_thresholds(metrics: dict) -> list[dict]:
    """Tier-1+2+3: metric threshold checks."""
    triggered = []
    for metric_key, (min_val, max_val, severity) in EW_THRESHOLDS.items():
        value = extract_metric_value(metrics, metric_key)
        if value is None:
            continue
        breach = False
        direction = ""
        if min_val is not None and value < min_val:
            breach = True
            direction = f"< {min_val} (actual: {value:.2f})"
        if max_val is not None and value > max_val:
            breach = True
            direction = f"> {max_val} (actual: {value:.2f})"
        if breach:
            triggered.append({
                "type": "threshold",
                "metric": metric_key,
                "condition": direction,
                "severity": severity,
            })
    return triggered


def check_keywords(signals: list[dict], key_facts: list[str]) -> list[dict]:
    """Tier-3 heuristic: keyword frequency across signals + facts."""
    all_text = " ".join(
        [
            s.get("title", "") + " " + s.get("summary", "")
            for s in signals
        ]
        + key_facts
    ).lower()

    triggered = []
    for severity, keywords in EW_KEYWORDS.items():
        hits = [kw for kw in keywords if kw.lower() in all_text]
        if len(hits) >= EW_KEYWORD_HIT_THRESHOLD:
            triggered.append({
                "type": "keyword_heuristic",
                "severity": severity,
                "hits": hits[:5],  # top 5
                "hit_count": len(hits),
            })
    return triggered


def check_collector_ew_flags(domain_data: dict) -> list[dict]:
    """Pass-through: respect EW flags already set by ai_intel_collector."""
    triggered = []
    ew = domain_data.get("ew_indicators", {})
    if ew.get("detected"):
        reasons = ew.get("reasons", []) or [ew.get("reason", "collector flag")]
        triggered.append({
            "type": "collector_flag",
            "severity": "HIGH",
            "reasons": reasons,
        })
    return triggered


def detect_domain(domain: str, domain_data: dict) -> dict:
    """Run all 3 EW detection tiers for a single domain."""
    metrics = domain_data.get("metrics", {})
    signals = domain_data.get("signals", [])
    key_facts = domain_data.get("key_facts", [])

    all_triggers = []
    all_triggers.extend(check_collector_ew_flags(domain_data))
    all_triggers.extend(check_thresholds(metrics))
    all_triggers.extend(check_keywords(signals, key_facts))

    # Determine overall severity
    severity_order = {"CRITICAL": 3, "HIGH": 2, "MEDIUM": 1, "NONE": 0}
    max_severity = "NONE"
    for t in all_triggers:
        s = t.get("severity", "NONE")
        if severity_order.get(s, 0) > severity_order.get(max_severity, 0):
            max_severity = s

    ew_detected = len(all_triggers) > 0
    log.info(
        f"  {domain}: EW={ew_detected} | severity={max_severity} | "
        f"triggers={len(all_triggers)}"
    )

    return {
        "domain": domain,
        "ew_detected": ew_detected,
        "severity": max_severity,
        "trigger_count": len(all_triggers),
        "triggers": all_triggers,
        "signal_count": len(signals),
        "metric_count": len(metrics),
    }


# ─── Main ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="AI EW Detector — Section A Step 2")
    parser.add_argument("--input-dir", required=True,
                        help="Directory containing intel JSON files")
    parser.add_argument("--week", required=True, help="ISO week e.g. 2026-W21")
    parser.add_argument("--output", required=True, help="Output EW report JSON path")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        log.error(f"Input directory not found: {input_dir}")
        sys.exit(1)

    # Load all intel JSON files
    intel_files = list(input_dir.glob("intel_*.json"))
    if not intel_files:
        log.warning("No intel_*.json files found in input directory")

    log.info(f"EW Detection — week={args.week} | files={len(intel_files)}")

    domain_results = []
    ew_domains = []

    for f in intel_files:
        try:
            with open(f, encoding="utf-8") as fp:
                data = json.load(fp)

            # Handle both single-domain and multi-domain JSON
            if "domains" in data:
                for domain, domain_data in data["domains"].items():
                    result = detect_domain(domain, domain_data)
                    domain_results.append(result)
                    if result["ew_detected"]:
                        ew_domains.append(domain)
            else:
                domain = data.get("domain", f.stem)
                result = detect_domain(domain, data)
                domain_results.append(result)
                if result["ew_detected"]:
                    ew_domains.append(domain)

        except (json.JSONDecodeError, KeyError) as e:
            log.error(f"Failed to process {f.name}: {e}")

    # Overall EW status
    severity_order = {"CRITICAL": 3, "HIGH": 2, "MEDIUM": 1, "NONE": 0}
    overall_severity = "NONE"
    for r in domain_results:
        s = r.get("severity", "NONE")
        if severity_order.get(s, 0) > severity_order.get(overall_severity, 0):
            overall_severity = s

    report = {
        "week": args.week,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "ew_triggered": len(ew_domains) > 0,
        "ew_domain_count": len(ew_domains),
        "ew_domains": ew_domains,
        "overall_severity": overall_severity,
        "domain_results": domain_results,
        "summary": (
            f"EW {'TRIGGERED' if ew_domains else 'CLEAR'} — "
            f"{len(ew_domains)}/{len(domain_results)} domains, "
            f"severity={overall_severity}"
        ),
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    log.info(f"\n{'⚠️ ' if ew_domains else '✅'} EW Report → {args.output}")
    log.info(f"   {report['summary']}")

    # Exit codes: 0=clear, 2=EW triggered (not hard failure)
    sys.exit(2 if ew_domains else 0)


if __name__ == "__main__":
    main()
