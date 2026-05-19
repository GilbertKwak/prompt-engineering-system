#!/usr/bin/env python3
"""
notion_c31_updater.py — Notion C-31 Page Updater
Appends weekly AI Intel digest blocks to a Notion page via the Blocks API.

Usage:
    python notion_c31_updater.py \\
        --page-id <NOTION_PAGE_ID> \\
        --week 2026-W21 --run-date 2026-05-20 \\
        --ew-triggered false --ew-count 0 \\
        --ew-signals "" --ew-severity NONE \\
        --kg-version 4.26 --node-count 5 --edge-count 3 \\
        --intel-dir output/ai_intel
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:
    print("[ERROR] 'requests' not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)


# ── Notion API helpers ─────────────────────────────────────────────────────────

NOTION_VERSION = "2022-06-28"
NOTION_BASE    = "https://api.notion.com/v1"
BATCH_SIZE     = 50   # Notion allows up to 100 children per request; 50 is safe


def _headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json",
        "Notion-Version": NOTION_VERSION,
    }


def _append_blocks(page_id: str, token: str, blocks: list[dict]) -> None:
    """Append blocks to a Notion page in batches of BATCH_SIZE."""
    url = f"{NOTION_BASE}/blocks/{page_id}/children"
    for i in range(0, len(blocks), BATCH_SIZE):
        chunk = blocks[i : i + BATCH_SIZE]
        resp = requests.patch(url, headers=_headers(token), json={"children": chunk})
        if resp.status_code == 429:  # rate limit
            wait = int(resp.headers.get("Retry-After", "5"))
            print(f"  [Rate Limit] waiting {wait}s …")
            time.sleep(wait)
            resp = requests.patch(url, headers=_headers(token), json={"children": chunk})
        if resp.status_code not in (200, 201):
            print(f"[ERROR] Notion API {resp.status_code}: {resp.text[:300]}", file=sys.stderr)
            resp.raise_for_status()
        print(f"  Appended {len(chunk)} blocks (batch {i // BATCH_SIZE + 1})")
        time.sleep(0.3)  # gentle rate-limit buffer


# ── Block constructors ─────────────────────────────────────────────────────────

def _rt(text: str, bold: bool = False, code: bool = False, color: str = "default") -> dict:
    """Rich text object."""
    return {
        "type": "text",
        "text": {"content": text},
        "annotations": {
            "bold": bold, "italic": False, "strikethrough": False,
            "underline": False, "code": code, "color": color,
        },
    }


def _divider() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


def _heading2(text: str) -> dict:
    return {
        "object": "block", "type": "heading_2",
        "heading_2": {"rich_text": [_rt(text, bold=True)], "color": "default"},
    }


def _heading3(text: str) -> dict:
    return {
        "object": "block", "type": "heading_3",
        "heading_3": {"rich_text": [_rt(text)], "color": "default"},
    }


def _para(parts: list[dict]) -> dict:
    return {
        "object": "block", "type": "paragraph",
        "paragraph": {"rich_text": parts, "color": "default"},
    }


def _bullet(parts: list[dict]) -> dict:
    return {
        "object": "block", "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": parts, "color": "default"},
    }


def _callout(text: str, icon: str = "ℹ️", color: str = "blue_background") -> dict:
    return {
        "object": "block", "type": "callout",
        "callout": {
            "rich_text": [_rt(text)],
            "icon": {"type": "emoji", "emoji": icon},
            "color": color,
        },
    }


def _toggle(title: str, children: list[dict]) -> dict:
    return {
        "object": "block", "type": "toggle",
        "toggle": {
            "rich_text": [_rt(title, bold=True)],
            "color": "default",
            "children": children,
        },
    }


# ── Block builder ──────────────────────────────────────────────────────────────

def build_weekly_blocks(
    week: str,
    run_date: str,
    ew_triggered: bool,
    ew_count: int,
    ew_signals: list[str],
    ew_severity: str,
    kg_version: str,
    node_count: int,
    edge_count: int,
    intel_dir: str,
) -> list[dict]:
    blocks: list[dict] = []
    
    # ── Section header ──
    blocks.append(_divider())
    blocks.append(_heading2(f"📊 AI Intel Weekly — {week}"))
    blocks.append(_para([_rt(f"Run Date: ", bold=True), _rt(run_date)]))

    # ── EW Status ──
    if ew_triggered:
        severity_color_map = {
            "CRITICAL": "red_background",
            "HIGH":     "red_background",
            "MEDIUM":   "yellow_background",
            "LOW":      "yellow_background",
        }
        callout_color = severity_color_map.get(ew_severity, "yellow_background")
        icon = "🚨" if ew_severity in ("CRITICAL", "HIGH") else "⚠️"
        blocks.append(_callout(
            f"Early Warning Triggered — Severity: {ew_severity} | Signals: {ew_count}",
            icon=icon,
            color=callout_color,
        ))
        if ew_signals:
            blocks.append(_heading3("EW Signals Detected"))
            for sig in ew_signals:
                blocks.append(_bullet([_rt(sig)]))
    else:
        blocks.append(_callout(
            f"No Early Warning — Normal Operations | Week: {week}",
            icon="✅",
            color="green_background",
        ))

    # ── KG Delta summary ──
    blocks.append(_heading3("Knowledge Graph Update"))
    blocks.append(_para([
        _rt("Version: ", bold=True), _rt(kg_version), _rt("  |  "),
        _rt("Nodes: ",   bold=True), _rt(str(node_count)), _rt("  |  "),
        _rt("Edges: ",   bold=True), _rt(str(edge_count)),
    ]))

    # ── Domain highlights from intel files ──
    intel_files = sorted(Path(intel_dir).glob("*.json"))
    if intel_files:
        domain_items: list[dict] = []
        for fp in intel_files[:10]:  # cap at 10 to avoid block limit
            try:
                with open(fp, encoding="utf-8") as f:
                    data = json.load(f)
                domain = data.get("domain", fp.stem)
                summary = data.get("executive_summary", data.get("summary", ""))
                if isinstance(summary, list):
                    summary = " ".join(str(x) for x in summary[:2])
                summary = str(summary)[:120]
                domain_items.append(_bullet([_rt(f"{domain}: ", bold=True), _rt(summary)]))
            except Exception:
                pass
        if domain_items:
            blocks.append(_heading3("Domain Highlights"))
            blocks.extend(domain_items)

    blocks.append(_para([_rt(f"Generated at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
                             color="gray")]))
    return blocks


# ── Core runner ────────────────────────────────────────────────────────────────

def run_update(
    page_id: str,
    week: str,
    run_date: str,
    ew_triggered: bool,
    ew_count: int,
    ew_signals_raw: str,
    ew_severity: str,
    kg_version: str,
    node_count: int,
    edge_count: int,
    intel_dir: str,
    token: str,
) -> None:
    ew_signals = [s.strip() for s in ew_signals_raw.split(",") if s.strip()] if ew_signals_raw else []

    print(f"  Building Notion blocks for {week} …")
    blocks = build_weekly_blocks(
        week=week, run_date=run_date,
        ew_triggered=ew_triggered, ew_count=ew_count,
        ew_signals=ew_signals, ew_severity=ew_severity,
        kg_version=kg_version, node_count=node_count, edge_count=edge_count,
        intel_dir=intel_dir,
    )
    print(f"  Total blocks to append: {len(blocks)}")
    _append_blocks(page_id, token, blocks)
    print(f"  ✅ Notion C-31 page updated successfully.")


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Notion C-31 Weekly Intel Updater",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--page-id",       required=True,  help="Notion page ID (32-char UUID without dashes)")
    parser.add_argument("--week",           required=True,  help="ISO week e.g. 2026-W21")
    parser.add_argument("--run-date",       required=True,  help="Run date YYYY-MM-DD")
    parser.add_argument("--ew-triggered",   required=True,  help="'true' or 'false'")
    parser.add_argument("--ew-count",       type=int, default=0, help="Number of EW signals")
    parser.add_argument("--ew-signals",     default="",     help="Comma-separated EW signal labels")
    parser.add_argument("--ew-severity",    default="NONE", help="NONE/LOW/MEDIUM/HIGH/CRITICAL")
    parser.add_argument("--kg-version",     required=True,  help="KG version string e.g. 4.26")
    parser.add_argument("--node-count",     type=int, default=0, help="Number of new KG nodes")
    parser.add_argument("--edge-count",     type=int, default=0, help="Number of new KG edges")
    parser.add_argument("--intel-dir",      default="output/ai_intel", help="Intel JSON directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    token = os.environ.get("NOTION_API_KEY", "")
    if not token:
        print("[ERROR] NOTION_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    ew_triggered = args.ew_triggered.lower() == "true"

    print(f"\n{'='*60}")
    print(f"Notion C-31 Updater — {args.week}")
    print(f"{'='*60}")
    print(f"Page ID      : {args.page_id}")
    print(f"EW triggered : {ew_triggered} | Severity: {args.ew_severity}")
    print(f"KG version   : {args.kg_version} | Nodes: {args.node_count} | Edges: {args.edge_count}\n")

    run_update(
        page_id=args.page_id,
        week=args.week,
        run_date=args.run_date,
        ew_triggered=ew_triggered,
        ew_count=args.ew_count,
        ew_signals_raw=args.ew_signals,
        ew_severity=args.ew_severity,
        kg_version=args.kg_version,
        node_count=args.node_count,
        edge_count=args.edge_count,
        intel_dir=args.intel_dir,
        token=token,
    )


if __name__ == "__main__":
    main()
