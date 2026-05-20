#!/usr/bin/env python3
"""
notion_c31_updater.py  —  Notion C-31 Page Updater (Blocks API)

Appends a weekly AI Intel digest section to the C-31 Notion page.
Uses append_block_children with 50-block batches (API limit).

EW Severity → callout background:
  HIGH   → red_background
  MEDIUM → yellow_background
  LOW    → orange_background
  NONE   → green_background

Page ID resolution order:
  1. --page-id CLI argument (highest priority)
  2. NOTION_C31_PAGE_ID environment variable
  3. Error if neither is provided

Usage:
  python notion_c31_updater.py \\
    --page-id        35355ed4-36f0-8123-b87b-ddd9195d2e54 \\
    --week           2026-W21 \\
    --run-date       2026-05-20 \\
    --ew-triggered   false \\
    --ew-count       0 \\
    --ew-signals     '' \\
    --ew-severity    NONE \\
    --kg-version     4.26 \\
    --node-count     8 \\
    --edge-count     14 \\
    --intel-dir      output/ai_intel

  Or with env var (no --page-id needed):
  export NOTION_C31_PAGE_ID="35355ed4-36f0-8123-b87b-ddd9195d2e54"
  python notion_c31_updater.py --week 2026-W21 ...
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# Notion API helpers
# ---------------------------------------------------------------------------

NOTION_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
BATCH_SIZE = 50


def _notion_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def _api_request(
    method: str,
    url: str,
    token: str,
    payload: Optional[Dict] = None,
    retries: int = 3,
) -> Dict:
    headers = _notion_headers(token)
    body = json.dumps(payload).encode("utf-8") if payload else None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            status = e.code
            body_txt = e.read().decode("utf-8", errors="replace")
            if status == 429:  # rate limit
                wait = int(e.headers.get("Retry-After", 2 ** attempt))
                print(f"[Notion] Rate limited. Waiting {wait}s...")
                time.sleep(wait)
                continue
            raise RuntimeError(f"Notion API {status}: {body_txt}") from e
        except Exception as exc:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"Notion API error: {exc}") from exc
    raise RuntimeError("Max retries exceeded")


def append_blocks(page_id: str, token: str, blocks: List[Dict]) -> None:
    """Append blocks in batches of BATCH_SIZE."""
    # Normalize page_id: strip dashes for API calls
    normalized_id = page_id.replace("-", "")
    url = f"{NOTION_BASE}/blocks/{normalized_id}/children"
    for i in range(0, len(blocks), BATCH_SIZE):
        batch = blocks[i: i + BATCH_SIZE]
        _api_request("PATCH", url, token, {"children": batch})
        print(f"[Notion] Appended batch {i // BATCH_SIZE + 1} ({len(batch)} blocks)")
        if i + BATCH_SIZE < len(blocks):
            time.sleep(0.35)  # stay within rate limits


# ---------------------------------------------------------------------------
# Block Builders
# ---------------------------------------------------------------------------

def _txt(content: str, bold: bool = False, color: str = "default") -> Dict:
    return {
        "type": "text",
        "text": {"content": content},
        "annotations": {
            "bold": bold, "italic": False, "strikethrough": False,
            "underline": False, "code": False, "color": color,
        },
    }


def _heading2(text: str) -> Dict:
    return {
        "object": "block", "type": "heading_2",
        "heading_2": {"rich_text": [_txt(text, bold=True)], "color": "default"},
    }


def _heading3(text: str) -> Dict:
    return {
        "object": "block", "type": "heading_3",
        "heading_3": {"rich_text": [_txt(text)], "color": "default"},
    }


def _paragraph(parts: List[Dict]) -> Dict:
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": parts}}


def _bullet(parts: List[Dict]) -> Dict:
    return {
        "object": "block", "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": parts},
    }


def _divider() -> Dict:
    return {"object": "block", "type": "divider", "divider": {}}


def _callout(text: str, emoji: str, color: str) -> Dict:
    return {
        "object": "block", "type": "callout",
        "callout": {
            "rich_text": [_txt(text)],
            "icon": {"type": "emoji", "emoji": emoji},
            "color": color,
        },
    }


def _toggle(title: str, children: List[Dict]) -> Dict:
    return {
        "object": "block", "type": "toggle",
        "toggle": {
            "rich_text": [_txt(title, bold=True)],
            "children": children,
        },
    }


def _code_block(code: str, language: str = "json") -> Dict:
    return {
        "object": "block", "type": "code",
        "code": {
            "rich_text": [_txt(code)],
            "language": language,
        },
    }


# ---------------------------------------------------------------------------
# Severity Helpers
# ---------------------------------------------------------------------------

SEVERITY_CONFIG = {
    "HIGH":   {"color": "red_background",    "emoji": "🚨", "label": "HIGH ALERT"},
    "MEDIUM": {"color": "yellow_background", "emoji": "⚠️",  "label": "WATCH"},
    "LOW":    {"color": "orange_background", "emoji": "📌", "label": "NOTICE"},
    "NONE":   {"color": "green_background",  "emoji": "✅",  "label": "NORMAL"},
}


def _severity_cfg(severity: str) -> Dict:
    return SEVERITY_CONFIG.get(severity.upper(), SEVERITY_CONFIG["NONE"])


# ---------------------------------------------------------------------------
# Intel Summary Extraction
# ---------------------------------------------------------------------------

def _load_intel_summaries(intel_dir: Path) -> List[Dict]:
    summaries: List[Dict] = []
    if not intel_dir.exists():
        return summaries
    for fp in sorted(intel_dir.glob("*.json")):
        try:
            data = json.loads(fp.read_text(encoding="utf-8"))
            summaries.append({
                "domain": data.get("domain", fp.stem),
                "key_facts": data.get("key_facts", [])[:5],
                "strategic_implications": data.get("strategic_implications", [])[:3],
                "outlook": data.get("outlook", ""),
                "metrics": data.get("metrics", {}),
            })
        except Exception:
            continue
    return summaries


# ---------------------------------------------------------------------------
# Block Assembly
# ---------------------------------------------------------------------------

def _build_blocks(
    week: str,
    run_date: str,
    ew_triggered: bool,
    ew_count: int,
    ew_signals: str,
    ew_severity: str,
    kg_version: str,
    node_count: int,
    edge_count: int,
    intel_summaries: List[Dict],
) -> List[Dict]:
    blocks: List[Dict] = []
    sev = _severity_cfg(ew_severity)

    # ── Header ──────────────────────────────────────────────────────────────
    blocks.append(_divider())
    blocks.append(_heading2(f"📡 AI Intel Weekly Digest — {week}"))
    blocks.append(
        _paragraph([
            _txt("Run Date: ", bold=True),
            _txt(run_date),
            _txt("   │   KG Version: ", bold=True),
            _txt(f"v{kg_version}"),
            _txt("   │   Generated: ", bold=True),
            _txt(datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")),
        ])
    )

    # ── EW Status Callout ────────────────────────────────────────────────────
    ew_status_text = (
        f"{sev['label']}  │  EW Triggered: {'YES' if ew_triggered else 'NO'}  "
        f"│  Signals: {ew_count}  │  Severity: {ew_severity}"
    )
    blocks.append(_callout(ew_status_text, sev["emoji"], sev["color"]))

    # EW signal list (if any)
    if ew_signals and ew_signals.strip():
        blocks.append(_heading3("⚡ Early Warning Signals"))
        for sig in [s.strip() for s in ew_signals.split(",") if s.strip()]:
            blocks.append(_bullet([_txt(sig, color="red")]))

    # ── KG Delta Summary ─────────────────────────────────────────────────────
    blocks.append(_heading3("🗺️ Knowledge Graph Delta"))
    blocks.append(
        _paragraph([
            _txt(f"New Nodes: {node_count}", bold=True),
            _txt("   │   "),
            _txt(f"New Edges: {edge_count}", bold=True),
            _txt(f"   │   Version: v{kg_version}"),
        ])
    )

    # ── Intel Domain Summaries ────────────────────────────────────────────────
    if intel_summaries:
        blocks.append(_heading3("🔍 Domain Intelligence"))
        for summary in intel_summaries:
            domain_label = summary["domain"].replace("_", " ").title()
            children: List[Dict] = []

            # Key Facts
            if summary["key_facts"]:
                children.append(_paragraph([_txt("Key Facts:", bold=True)]))
                for fact in summary["key_facts"]:
                    children.append(_bullet([_txt(str(fact))]))

            # Strategic Implications
            if summary["strategic_implications"]:
                children.append(_paragraph([_txt("Strategic Implications:", bold=True)]))
                for impl in summary["strategic_implications"]:
                    children.append(_bullet([_txt(str(impl))]))

            # Outlook
            if summary["outlook"]:
                children.append(
                    _paragraph([_txt("Outlook: ", bold=True), _txt(str(summary["outlook"]))])
                )

            # Metrics
            if summary["metrics"] and isinstance(summary["metrics"], dict):
                metrics_str = json.dumps(summary["metrics"], ensure_ascii=False, indent=2)
                if len(metrics_str) < 1500:
                    children.append(_code_block(metrics_str, "json"))

            if children:
                blocks.append(_toggle(f"📂 {domain_label}", children))

    # ── Footer ────────────────────────────────────────────────────────────────
    blocks.append(_divider())
    blocks.append(
        _paragraph([
            _txt("Auto-generated by "),
            _txt("ai_intel_weekly", bold=True),
            _txt(f" pipeline  │  {week}  │  PE System v3"),
        ])
    )

    return blocks


# ---------------------------------------------------------------------------
# Page ID Resolution
# ---------------------------------------------------------------------------

def resolve_page_id(cli_page_id: Optional[str]) -> str:
    """
    Resolve Notion C-31 page ID with fallback priority:
      1. --page-id CLI argument
      2. NOTION_C31_PAGE_ID environment variable
    """
    if cli_page_id and cli_page_id.strip():
        return cli_page_id.strip()
    env_id = os.environ.get("NOTION_C31_PAGE_ID", "").strip()
    if env_id:
        return env_id
    print(
        "[ERROR] Notion C-31 page ID not found.\n"
        "  Provide via --page-id argument OR set NOTION_C31_PAGE_ID env var.",
        file=sys.stderr,
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def update_c31(
    page_id: str,
    week: str,
    run_date: str,
    ew_triggered: bool,
    ew_count: int,
    ew_signals: str,
    ew_severity: str,
    kg_version: str,
    node_count: int,
    edge_count: int,
    intel_dir: Path,
    notion_token: str,
) -> None:
    intel_summaries = _load_intel_summaries(intel_dir)
    blocks = _build_blocks(
        week=week,
        run_date=run_date,
        ew_triggered=ew_triggered,
        ew_count=ew_count,
        ew_signals=ew_signals,
        ew_severity=ew_severity,
        kg_version=kg_version,
        node_count=node_count,
        edge_count=edge_count,
        intel_summaries=intel_summaries,
    )
    print(f"[Notion] Appending {len(blocks)} blocks to page {page_id}...")
    append_blocks(page_id, notion_token, blocks)
    print(f"[Notion] C-31 update complete for {week}.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Notion C-31 Page Updater")
    parser.add_argument(
        "--page-id",
        default=None,
        help="Notion C-31 page ID. Falls back to NOTION_C31_PAGE_ID env var.",
    )
    parser.add_argument("--week",          required=True)
    parser.add_argument("--run-date",      required=True)
    parser.add_argument("--ew-triggered",  default="false")
    parser.add_argument("--ew-count",      type=int, default=0)
    parser.add_argument("--ew-signals",    default="")
    parser.add_argument("--ew-severity",   default="NONE")
    parser.add_argument("--kg-version",    required=True)
    parser.add_argument("--node-count",    type=int, default=0)
    parser.add_argument("--edge-count",    type=int, default=0)
    parser.add_argument("--intel-dir",     default="output/ai_intel")
    args = parser.parse_args()

    token = os.environ.get("NOTION_API_KEY", "")
    if not token:
        print("[ERROR] NOTION_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    page_id = resolve_page_id(args.page_id)
    print(f"[Notion] Target page ID: {page_id}")

    update_c31(
        page_id=page_id,
        week=args.week,
        run_date=args.run_date,
        ew_triggered=args.ew_triggered.lower() == "true",
        ew_count=args.ew_count,
        ew_signals=args.ew_signals,
        ew_severity=args.ew_severity,
        kg_version=args.kg_version,
        node_count=args.node_count,
        edge_count=args.edge_count,
        intel_dir=Path(args.intel_dir),
        notion_token=token,
    )


if __name__ == "__main__":
    main()
