#!/usr/bin/env python3
"""
distill_output.py
=================
Prompt Engineering System — Output Distillation Utility

Purpose:
  Reads raw LLM output files (JSON / Markdown / plain text) from the
  `output/` directory, applies configurable distillation rules, and
  writes structured summaries to `output/distilled/`.

Distillation steps
------------------
1. Load raw output (single file or batch directory scan)
2. Parse content by type  (json | markdown | text)
3. Extract key signals     (score, verdict, reasoning, action-items)
4. Score & rank entries    (optional weight config via config/distill_config.yaml)
5. Write distilled output  (JSON + optional Markdown report)

Usage
-----
  # Single file
  python distill_output.py --input output/session_abc.json

  # Batch (all JSON files under output/)
  python distill_output.py --batch

  # Batch with custom config
  python distill_output.py --batch --config config/distill_config.yaml

  # Dry-run (preview without writing)
  python distill_output.py --batch --dry-run

Output
------
  output/distilled/<original_stem>_distilled.json
  output/distilled/report_<timestamp>.md   (only with --report flag)
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml  # pip install pyyaml

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("distill_output")

# ---------------------------------------------------------------------------
# Constants / default paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent
OUTPUT_DIR = ROOT / "output"
DISTILLED_DIR = OUTPUT_DIR / "distilled"
DEFAULT_CONFIG = ROOT / "config" / "distill_config.yaml"

DEFAULT_DISTILL_CONFIG: dict[str, Any] = {
    "score_weights": {
        "clarity": 0.30,
        "relevance": 0.35,
        "actionability": 0.35,
    },
    "min_score_threshold": 0.50,
    "extract_keys": ["verdict", "score", "reasoning", "action_items", "tags"],
    "include_raw_excerpt": True,
    "excerpt_max_chars": 500,
}


# ---------------------------------------------------------------------------
# Config loader
# ---------------------------------------------------------------------------

def load_config(path: Path | None = None) -> dict[str, Any]:
    """Load YAML distillation config, falling back to defaults."""
    cfg_path = path or DEFAULT_CONFIG
    if cfg_path.exists():
        with open(cfg_path, encoding="utf-8") as f:
            loaded = yaml.safe_load(f) or {}
        log.info("Loaded config: %s", cfg_path)
        # Merge with defaults (loaded values take precedence)
        merged = {**DEFAULT_DISTILL_CONFIG, **loaded}
        return merged
    log.warning("Config not found at %s — using built-in defaults.", cfg_path)
    return DEFAULT_DISTILL_CONFIG


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

def parse_json(raw: str) -> dict[str, Any]:
    """Parse JSON string, return dict. Returns empty dict on failure."""
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        log.debug("JSON parse error: %s", exc)
        return {}


def parse_markdown(raw: str) -> dict[str, Any]:
    """
    Minimal Markdown extractor.
    Looks for YAML front-matter (---) and key: value patterns.
    """
    data: dict[str, Any] = {}

    # --- YAML front-matter ---
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", raw, re.DOTALL)
    if fm_match:
        try:
            data.update(yaml.safe_load(fm_match.group(1)) or {})
        except yaml.YAMLError:
            pass

    # --- Inline key: value lines ---
    for line in raw.splitlines():
        kv = re.match(r"^\s*[-*]?\s*\*{0,2}(\w[\w\s]*?)\*{0,2}:\s*(.+)$", line)
        if kv:
            key = kv.group(1).strip().lower().replace(" ", "_")
            val = kv.group(2).strip()
            data.setdefault(key, val)

    # --- Body as fallback ---
    data.setdefault("body", raw.strip())
    return data


def parse_text(raw: str) -> dict[str, Any]:
    """Treat plain text as a single body field."""
    return {"body": raw.strip()}


def parse_content(raw: str, suffix: str) -> dict[str, Any]:
    """Dispatch to the correct parser based on file extension."""
    if suffix in {".json"}:
        return parse_json(raw)
    if suffix in {".md", ".markdown"}:
        return parse_markdown(raw)
    return parse_text(raw)


# ---------------------------------------------------------------------------
# Extraction helpers
# ---------------------------------------------------------------------------

def extract_signals(data: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any]:
    """
    Pull known signal keys from parsed data.
    Gracefully handles missing keys by returning None.
    """
    keys = cfg.get("extract_keys", DEFAULT_DISTILL_CONFIG["extract_keys"])
    signals: dict[str, Any] = {}
    for k in keys:
        # Try exact match, then case-insensitive match
        if k in data:
            signals[k] = data[k]
        else:
            for dk, dv in data.items():
                if dk.lower() == k.lower():
                    signals[k] = dv
                    break
            else:
                signals[k] = None
    return signals


def compute_composite_score(signals: dict[str, Any], cfg: dict[str, Any]) -> float:
    """
    Derive a 0-1 composite score from numeric signal values.
    If signals contain an explicit 'score', normalise it to 0-1.
    Otherwise default to 0.
    """
    weights: dict[str, float] = cfg.get(
        "score_weights", DEFAULT_DISTILL_CONFIG["score_weights"]
    )

    # Prefer an explicit top-level score
    raw_score = signals.get("score")
    if raw_score is not None:
        try:
            val = float(raw_score)
            # Normalise: if > 1 assume 0-100 scale
            return round(min(val / 100, 1.0) if val > 1.0 else val, 4)
        except (TypeError, ValueError):
            pass

    # Try to aggregate sub-dimension scores from data
    total_weight = sum(weights.values()) or 1.0
    composite = 0.0
    for dim, w in weights.items():
        raw = signals.get(dim)
        if raw is not None:
            try:
                val = float(raw)
                composite += (val / 100 if val > 1.0 else val) * (w / total_weight)
            except (TypeError, ValueError):
                pass
    return round(composite, 4)


# ---------------------------------------------------------------------------
# Core distillation
# ---------------------------------------------------------------------------

def distill_entry(
    path: Path,
    cfg: dict[str, Any],
) -> dict[str, Any] | None:
    """
    Distill a single output file.

    Returns a distilled dict, or None if the entry is below the score threshold.
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        log.error("Cannot read %s: %s", path, exc)
        return None

    parsed = parse_content(raw, path.suffix.lower())
    signals = extract_signals(parsed, cfg)
    score = compute_composite_score(signals, cfg)

    threshold: float = cfg.get(
        "min_score_threshold", DEFAULT_DISTILL_CONFIG["min_score_threshold"]
    )
    if score < threshold:
        log.info("  SKIP  %s  (score=%.3f < threshold=%.3f)", path.name, score, threshold)
        return None

    entry: dict[str, Any] = {
        "source_file": str(path.relative_to(ROOT)),
        "distilled_at": datetime.utcnow().isoformat() + "Z",
        "composite_score": score,
        "signals": signals,
    }

    if cfg.get("include_raw_excerpt", True):
        max_chars: int = cfg.get("excerpt_max_chars", 500)
        entry["raw_excerpt"] = raw[:max_chars] + ("…" if len(raw) > max_chars else "")

    log.info("  OK    %s  (score=%.3f)", path.name, score)
    return entry


# ---------------------------------------------------------------------------
# Batch helpers
# ---------------------------------------------------------------------------

def collect_output_files(directory: Path) -> list[Path]:
    """Return all distillable files under *directory* (non-recursive by default)."""
    supported = {".json", ".md", ".markdown", ".txt"}
    files = [
        p for p in sorted(directory.iterdir())
        if p.is_file() and p.suffix.lower() in supported
        and p.stem != "distilled"  # avoid re-processing old outputs
    ]
    return files


def write_distilled(entry: dict[str, Any], source: Path, dry_run: bool) -> Path:
    """Write a single distilled JSON entry to DISTILLED_DIR."""
    out_path = DISTILLED_DIR / f"{source.stem}_distilled.json"
    if dry_run:
        log.info("[DRY-RUN] Would write → %s", out_path)
    else:
        DISTILLED_DIR.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8")
        log.info("  Written → %s", out_path.relative_to(ROOT))
    return out_path


def write_report(entries: list[dict[str, Any]], dry_run: bool) -> Path:
    """Generate a Markdown summary report of all distilled entries."""
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    report_path = DISTILLED_DIR / f"report_{timestamp}.md"

    lines = [
        f"# Distillation Report",
        f"",
        f"**Generated:** {datetime.utcnow().isoformat()}Z  ",
        f"**Entries:** {len(entries)}",
        f"",
        f"---",
        f"",
    ]

    for e in sorted(entries, key=lambda x: x["composite_score"], reverse=True):
        lines += [
            f"## {Path(e['source_file']).name}",
            f"",
            f"- **Score:** `{e['composite_score']:.3f}`",
            f"- **Verdict:** {e['signals'].get('verdict') or '_n/a_'}",
        ]
        reasoning = e["signals"].get("reasoning")
        if reasoning:
            lines.append(f"- **Reasoning:** {str(reasoning)[:200]}")
        action_items = e["signals"].get("action_items")
        if action_items:
            if isinstance(action_items, list):
                lines.append("- **Action items:**")
                for ai in action_items[:5]:
                    lines.append(f"  - {ai}")
            else:
                lines.append(f"- **Action items:** {str(action_items)[:200]}")
        lines.append("")

    content = "\n".join(lines)

    if dry_run:
        log.info("[DRY-RUN] Would write report → %s", report_path)
    else:
        DISTILLED_DIR.mkdir(parents=True, exist_ok=True)
        report_path.write_text(content, encoding="utf-8")
        log.info("Report written → %s", report_path.relative_to(ROOT))

    return report_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Distill LLM output files into structured summaries.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = p.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--input", "-i",
        type=Path,
        metavar="FILE",
        help="Single output file to distill.",
    )
    group.add_argument(
        "--batch", "-b",
        action="store_true",
        help=f"Distill all supported files under {OUTPUT_DIR}/.",
    )
    p.add_argument(
        "--config", "-c",
        type=Path,
        metavar="YAML",
        default=None,
        help="Path to distill_config.yaml (default: config/distill_config.yaml).",
    )
    p.add_argument(
        "--output-dir", "-o",
        type=Path,
        metavar="DIR",
        default=None,
        help=f"Override distilled output directory (default: {DISTILLED_DIR}).",
    )
    p.add_argument(
        "--report",
        action="store_true",
        help="Generate a Markdown summary report after batch distillation.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without writing any files.",
    )
    p.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable DEBUG logging.",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Override distilled dir if requested
    global DISTILLED_DIR
    if args.output_dir:
        DISTILLED_DIR = args.output_dir

    cfg = load_config(args.config)

    # ---- Single file mode ----
    if args.input:
        if not args.input.exists():
            log.error("File not found: %s", args.input)
            return 1
        entry = distill_entry(args.input, cfg)
        if entry is None:
            log.warning("Entry did not pass distillation threshold.")
            return 0
        write_distilled(entry, args.input, args.dry_run)
        return 0

    # ---- Batch mode (default if no --input) ----
    if not OUTPUT_DIR.exists():
        log.error("Output directory not found: %s", OUTPUT_DIR)
        return 1

    files = collect_output_files(OUTPUT_DIR)
    if not files:
        log.warning("No distillable files found in %s", OUTPUT_DIR)
        return 0

    log.info("Found %d file(s) to process.", len(files))
    distilled_entries: list[dict[str, Any]] = []

    for f in files:
        entry = distill_entry(f, cfg)
        if entry:
            write_distilled(entry, f, args.dry_run)
            distilled_entries.append(entry)

    log.info(
        "Distillation complete: %d/%d entries passed threshold.",
        len(distilled_entries),
        len(files),
    )

    if args.report and distilled_entries:
        write_report(distilled_entries, args.dry_run)

    return 0


if __name__ == "__main__":
    sys.exit(main())
