#!/usr/bin/env python3
"""
notion_c31_updater.py — Notion C-31 Page Updater v2
AI Intel Weekly pipeline: Step 4 (Final)

Inputs : ew_report.json, kg_delta.json, intel JSON files
Outputs: Updated Notion C-31 page via Blocks API

Block Structure:
  ─ Weekly header (divider + h1 + metadata)
  ─ EW Status callout (color-coded by severity)
  ─ Domain Intel digest table
  ─ KG Delta summary
  ─ Key Signals & Recommendations bullets
  ─ Footer divider

Design notes:
  - Append-only: does NOT delete existing blocks (safe idempotent runs)
  - Batches 100 blocks per API call (Notion limit: 100)
  - Severity color map: CRITICAL=red / ALERT=orange / WATCH=yellow / NONE=green
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

# ── Constants ─────────────────────────────────────────────────────────────────

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
BATCH_SIZE = 100
RETRY_LIMIT = 3
RETRY_DELAY = 2.0

SEVERITY_COLOR: dict[str, str] = {
    "CRITICAL": "red_background",
    "ALERT":    "orange_background",
    "WATCH":    "yellow_background",
    "NONE":     "green_background",
}

SEVERITY_EMOJI: dict[str, str] = {
    "CRITICAL": "🚨",
    "ALERT":    "⚠️",
    "WATCH":    "👁️",
    "NONE":     "✅",
}

DOMAIN_EMOJI: dict[str, str] = {
    "model_architecture":       "🧠",
    "enterprise_deployment":    "🏢",
    "open_source_dynamics":     "🔓",
    "regulatory_geopolitical":  "🏛️",
    "hardware_infrastructure":  "⚙️",
    "agentic_multimodal":       "🤖",
}


# ── Notion API Helpers ────────────────────────────────────────────────────────

def _headers(api_key: str) -> dict:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type":  "application/json",
        "Notion-Version": NOTION_VERSION,
    }


def _post_blocks(page_id: str, blocks: list[dict], api_key: str) -> None:
    """Append blocks in batches of BATCH_SIZE."""
    url = f"{NOTION_API}/blocks/{page_id}/children"
    for i in range(0, len(blocks), BATCH_SIZE):
        batch = blocks[i:i + BATCH_SIZE]
        for attempt in range(RETRY_LIMIT):
            resp = requests.patch(url, headers=_headers(api_key), json={"children": batch}, timeout=30)
            if resp.status_code == 200:
                print(f"[Notion] Batch {i//BATCH_SIZE + 1}: {len(batch)} blocks appended")
                break
            elif resp.status_code == 429:
                wait = float(resp.headers.get("Retry-After", RETRY_DELAY * (attempt + 1)))
                print(f"[Notion] Rate limited — waiting {wait:.1f}s")
                time.sleep(wait)
            elif resp.status_code == 403:
                print(f"[Notion] 403 Forbidden — check Integration connection on page", file=sys.stderr)
                sys.exit(1)
            else:
                print(f"[Notion] Error {resp.status_code}: {resp.text[:200]}", file=sys.stderr)
                if attempt == RETRY_LIMIT - 1:
                    sys.exit(1)
                time.sleep(RETRY_DELAY)
        time.sleep(0.3)  # avoid burst


# ── Block Builders ────────────────────────────────────────────────────────────

def _rich(text: str, bold: bool = False, code: bool = False, color: str = "default") -> dict:
    return {
        "type": "text",
        "text": {"content": text},
        "annotations": {"bold": bold, "code": code, "color": color,
                        "italic": False, "strikethrough": False, "underline": False},
    }


def b_divider() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


def b_h1(text: str) -> dict:
    return {"object": "block", "type": "heading_1",
            "heading_1": {"rich_text": [_rich(text)], "color": "default"}}


def b_h2(text: str) -> dict:
    return {"object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [_rich(text)], "color": "default"}}


def b_h3(text: str) -> dict:
    return {"object": "block", "type": "heading_3",
            "heading_3": {"rich_text": [_rich(text)], "color": "default"}}


def b_para(text: str) -> dict:
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [_rich(text)]}}


def b_bullet(text: str, bold_prefix: str = "") -> dict:
    rt = []
    if bold_prefix:
        rt.append(_rich(bold_prefix + " ", bold=True))
    rt.append(_rich(text))
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": rt}}


def b_callout(text: str, emoji: str, color: str) -> dict:
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [_rich(text)],
            "icon": {"type": "emoji", "emoji": emoji},
            "color": color,
        },
    }


def b_table_row(cells: list[str]) -> dict:
    return {
        "object": "block",
        "type": "table_row",
        "table_row": {
            "cells": [[_rich(c)] for c in cells]
        },
    }


def b_table(headers: list[str], rows: list[list[str]]) -> dict:
    """Build a Notion table block with header row."""
    table_rows = [b_table_row(headers)] + [b_table_row(r) for r in rows]
    return {
        "object": "block",
        "type": "table",
        "table": {
            "table_width":       len(headers),
            "has_column_header": True,
            "has_row_header":    False,
            "children":          table_rows,
        },
    }


# ── Data Loaders ──────────────────────────────────────────────────────────────

def _load_json(path: str | Path, label: str) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[Notion] Warning — could not load {label}: {e}", file=sys.stderr)
        return {}


def load_intel_summaries(intel_dir: str) -> dict[str, str]:
    """Return {domain: summary_snippet} from all intel JSON files."""
    summaries: dict[str, str] = {}
    for jf in sorted(Path(intel_dir).glob("*.json")):
        if jf.name == "ew_report.json":
            continue
        data = _load_json(jf, jf.name)
        domain = data.get("domain", jf.stem)
        summary = data.get("summary", "")
        if isinstance(summary, list):
            summary = " ".join(str(s) for s in summary)
        summaries[domain] = (summary[:150] + "…") if len(summary) > 150 else summary
    return summaries


def load_key_signals(intel_dir: str) -> list[str]:
    """Collect top key_facts bullets from all intel files."""
    signals: list[str] = []
    for jf in sorted(Path(intel_dir).glob("*.json")):
        if jf.name == "ew_report.json":
            continue
        data = _load_json(jf, jf.name)
        facts = data.get("key_facts", [])
        if isinstance(facts, list):
            signals.extend(str(f) for f in facts[:2])  # top 2 per domain
        elif isinstance(facts, str):
            signals.append(facts[:200])
    return signals[:12]  # cap at 12 bullets


def load_recommendations(intel_dir: str) -> list[str]:
    """Collect strategic recommendations."""
    recs: list[str] = []
    for jf in sorted(Path(intel_dir).glob("*.json")):
        if jf.name == "ew_report.json":
            continue
        data = _load_json(jf, jf.name)
        r = data.get("recommendations", [])
        if isinstance(r, list):
            recs.extend(str(i) for i in r[:1])  # top 1 per domain
        elif isinstance(r, str):
            recs.append(r[:200])
    return recs[:6]  # cap at 6


# ── Block Assembly ────────────────────────────────────────────────────────────

def build_blocks(
    week: str,
    run_date: str,
    ew_triggered: bool,
    ew_count: int,
    ew_signals: list[str],
    ew_severity: str,
    kg_version: str,
    node_count: int,
    edge_count: int,
    intel_summaries: dict[str, str],
    key_signals: list[str],
    recommendations: list[str],
) -> list[dict]:
    blocks: list[dict] = []

    # ── Header ──
    blocks.append(b_divider())
    blocks.append(b_h1(f"📡 AI Intel Weekly — {week}"))
    blocks.append(b_para(
        f"Generated: {run_date}  |  KG v{kg_version}  |  "
        f"Nodes: {node_count}  Edges: {edge_count}"
    ))

    # ── EW Status Callout ──
    sev_color = SEVERITY_COLOR.get(ew_severity, "gray_background")
    sev_emoji = SEVERITY_EMOJI.get(ew_severity, "📊")
    if ew_triggered:
        ew_text = (
            f"EW {ew_severity} — {ew_count} signal(s) detected  |  "
            f"Tags: {', '.join(ew_signals) or 'N/A'}"
        )
    else:
        ew_text = f"No Early Warning triggered  |  Monitoring: {', '.join(ew_signals) or 'All clear'}"
    blocks.append(b_callout(ew_text, sev_emoji, sev_color))

    # ── Domain Intel Digest Table ──
    blocks.append(b_h2("📊 Domain Intel Digest"))
    table_rows: list[list[str]] = []
    for domain, summary in intel_summaries.items():
        emoji = DOMAIN_EMOJI.get(domain, "📌")
        table_rows.append([f"{emoji} {domain.replace('_', ' ').title()}", summary])
    if table_rows:
        blocks.append(b_table(["Domain", "Weekly Summary"], table_rows))
    else:
        blocks.append(b_para("No domain intel available for this week."))

    # ── KG Delta Summary ──
    blocks.append(b_h2("🕸️ Knowledge Graph Delta"))
    blocks.append(b_para(
        f"Version: {kg_version}  |  New nodes: {node_count}  |  New edges: {edge_count}"
    ))
    if ew_signals:
        blocks.append(b_bullet(", ".join(ew_signals), bold_prefix="EW-tagged edges:"))

    # ── Key Signals ──
    if key_signals:
        blocks.append(b_h2("🔑 Key Signals"))
        for sig in key_signals:
            blocks.append(b_bullet(str(sig)))

    # ── Strategic Recommendations ──
    if recommendations:
        blocks.append(b_h2("💡 Strategic Recommendations"))
        for rec in recommendations:
            blocks.append(b_bullet(str(rec)))

    # ── Footer ──
    blocks.append(b_divider())
    blocks.append(b_para(
        f"Auto-generated by notion_c31_updater.py v2  |  {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC"
    ))

    return blocks


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Update Notion C-31 page with AI Intel Weekly digest")
    p.add_argument("--page-id",        required=True,  help="Notion page ID (32-char hex or UUID)")
    p.add_argument("--week",           required=True,  help="e.g. 2026-W21")
    p.add_argument("--run-date",       required=True,  help="YYYY-MM-DD")
    p.add_argument("--ew-triggered",   default="false")
    p.add_argument("--ew-count",       type=int, default=0)
    p.add_argument("--ew-signals",     default="")
    p.add_argument("--ew-severity",    default="NONE")
    p.add_argument("--kg-version",     default="0.0")
    p.add_argument("--node-count",     type=int, default=0)
    p.add_argument("--edge-count",     type=int, default=0)
    p.add_argument("--intel-dir",      default="output/ai_intel")
    p.add_argument("--dry-run",        action="store_true", help="Print blocks without calling API")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    api_key = os.environ.get("NOTION_API_KEY", "")
    if not api_key and not args.dry_run:
        print("[Notion] NOTION_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    ew_signals = [s.strip() for s in args.ew_signals.split(",") if s.strip()]
    ew_triggered = args.ew_triggered.lower() in ("true", "1", "yes")

    # Load supporting data
    intel_summaries = load_intel_summaries(args.intel_dir)
    key_signals     = load_key_signals(args.intel_dir)
    recommendations = load_recommendations(args.intel_dir)

    print(f"[Notion] Building blocks for {args.week} | EW={args.ew_severity}")
    blocks = build_blocks(
        week=args.week,
        run_date=args.run_date,
        ew_triggered=ew_triggered,
        ew_count=args.ew_count,
        ew_signals=ew_signals,
        ew_severity=args.ew_severity,
        kg_version=args.kg_version,
        node_count=args.node_count,
        edge_count=args.edge_count,
        intel_summaries=intel_summaries,
        key_signals=key_signals,
        recommendations=recommendations,
    )

    print(f"[Notion] Total blocks: {len(blocks)}")

    if args.dry_run:
        print(json.dumps(blocks, ensure_ascii=False, indent=2))
        print("[Notion] --dry-run: no API call made")
        return

    _post_blocks(args.page_id, blocks, api_key)
    print(f"[Notion] C-31 page updated: https://notion.so/{args.page_id.replace('-', '')}")


if __name__ == "__main__":
    main()
