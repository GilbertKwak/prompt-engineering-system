#!/usr/bin/env python3
"""
notion_c31_updater.py — Section A, Step 4
Notion Blocks API로 C-31 인텔 리포트 페이지 업데이트
50블록 배치, EW 심각도별 callout 색상, 기존 내용 보존

Usage:
  python notion_c31_updater.py \
    --page-id 34a55ed436f0814d9cffe6a2f0816e29 \
    --week 2026-W21 \
    --run-date 2026-05-20 \
    --ew-triggered false \
    --ew-count 0 \
    --ew-signals "" \
    --ew-severity NONE \
    --kg-version 4.26 \
    --node-count 5 \
    --edge-count 3 \
    --intel-dir output/ai_intel
"""

import argparse
import json
import os
import sys
import time
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("[ERROR] requests not installed: pip install requests")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("notion_c31_updater")

NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
BATCH_SIZE = 50  # Notion API max blocks per append call
RATELIMIT_DELAY = 0.35  # seconds between batch calls

# EW severity → Notion callout color mapping
EW_COLOR_MAP = {
    "CRITICAL": "red_background",
    "HIGH": "orange_background",
    "MEDIUM": "yellow_background",
    "LOW": "blue_background",
    "NONE": "green_background",
}

EW_ICON_MAP = {
    "CRITICAL": "🚨",
    "HIGH": "⚠️",
    "MEDIUM": "📋",
    "LOW": "ℹ️",
    "NONE": "✅",
}


# ─── Notion API Helpers ───────────────────────────────────────────────────────
def get_headers() -> dict:
    token = os.environ.get("NOTION_API_KEY", "")
    if not token:
        log.error("NOTION_API_KEY env var not set")
        sys.exit(1)
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }


def append_blocks(page_id: str, blocks: list[dict]) -> bool:
    """Append blocks in batches of BATCH_SIZE."""
    headers = get_headers()
    url = f"{NOTION_API_BASE}/blocks/{page_id}/children"
    total = len(blocks)
    success = True

    for i in range(0, total, BATCH_SIZE):
        batch = blocks[i : i + BATCH_SIZE]
        log.info(f"  Appending blocks {i+1}–{min(i+BATCH_SIZE, total)}/{total}")
        try:
            resp = requests.patch(
                url, headers=headers,
                json={"children": batch}, timeout=30
            )
            if resp.status_code == 429:
                retry_after = int(resp.headers.get("Retry-After", 10))
                log.warning(f"  Rate limited. Waiting {retry_after}s...")
                time.sleep(retry_after)
                resp = requests.patch(
                    url, headers=headers,
                    json={"children": batch}, timeout=30
                )
            resp.raise_for_status()
            time.sleep(RATELIMIT_DELAY)
        except requests.exceptions.RequestException as e:
            log.error(f"  Failed to append blocks {i}–{i+BATCH_SIZE}: {e}")
            success = False

    return success


# ─── Block Builders ───────────────────────────────────────────────────────────
def divider() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


def heading2(text: str) -> dict:
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": text[:200]}}]
        },
    }


def heading3(text: str) -> dict:
    return {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": text[:200]}}]
        },
    }


def paragraph(text: str, bold: bool = False) -> dict:
    content = text[:2000]  # Notion text limit
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "type": "text",
                "text": {"content": content},
                "annotations": {"bold": bold},
            }]
        },
    }


def bulleted_item(text: str) -> dict:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]
        },
    }


def callout(text: str, icon: str, color: str) -> dict:
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": text[:2000]}}],
            "icon": {"type": "emoji", "emoji": icon},
            "color": color,
        },
    }


def toggle(title: str, children: list[dict]) -> dict:
    return {
        "object": "block",
        "type": "toggle",
        "toggle": {
            "rich_text": [{"type": "text", "text": {"content": title[:200]}}],
            "children": children[:99],  # Notion child block limit
        },
    }


# ─── Report Block Assembly ────────────────────────────────────────────────────
def build_header_blocks(args, run_ts: str) -> list[dict]:
    ew_flag = args.ew_triggered.lower() == "true"
    severity = args.ew_severity.upper()
    icon = EW_ICON_MAP.get(severity, "📋")
    color = EW_COLOR_MAP.get(severity, "green_background")

    ew_status = (
        f"EW TRIGGERED: {args.ew_count} domain(s) — {args.ew_signals}"
        if ew_flag else "EW CLEAR — No early warning signals"
    )

    return [
        divider(),
        heading2(f"🤖 AI Intel Weekly — {args.week}"),
        paragraph(f"Generated: {run_ts} | KG v{args.kg_version} | Week {args.week}"),
        callout(ew_status, icon, color),
        paragraph(
            f"KG Update: v{args.kg_version} | "
            f"Nodes: +{args.node_count} | Edges: +{args.edge_count}",
            bold=True,
        ),
    ]


def build_domain_blocks(domain: str, domain_data: dict) -> list[dict]:
    blocks = [heading3(f"📂 {domain.replace('_', ' ').title()}")]

    # Signals (top 5)
    signals = domain_data.get("signals", [])[:5]
    if signals:
        for sig in signals:
            sig_text = (
                f"[{sig.get('significance', '?')}] "
                f"{sig.get('title', 'Untitled')} — "
                f"{sig.get('summary', '')[:100]}"
            )
            blocks.append(bulleted_item(sig_text))

    # Key facts (top 3)
    facts = domain_data.get("key_facts", [])[:3]
    if facts:
        blocks.append(paragraph("Key facts:", bold=True))
        for fact in facts:
            blocks.append(bulleted_item(str(fact)[:200]))

    # EW indicator
    ew = domain_data.get("ew_indicators", {})
    if ew.get("detected"):
        reasons = ew.get("reasons", []) or [ew.get("reason", "EW detected")]
        blocks.append(
            callout(
                f"EW: {'; '.join(str(r) for r in reasons[:3])}",
                "⚠️", "orange_background"
            )
        )

    return blocks


def build_all_blocks(args, intel_dir: Path, run_ts: str) -> list[dict]:
    blocks = build_header_blocks(args, run_ts)
    blocks.append(divider())
    blocks.append(heading3("📊 Domain Intelligence"))

    # Load intel files and build per-domain blocks
    intel_files = list(intel_dir.glob("intel_*.json"))
    processed = 0

    for f in intel_files:
        try:
            with open(f, encoding="utf-8") as fp:
                data = json.load(fp)

            if "domains" in data:
                for domain, domain_data in data["domains"].items():
                    blocks.extend(build_domain_blocks(domain, domain_data))
                    processed += 1
            else:
                domain = data.get("domain", f.stem)
                blocks.extend(build_domain_blocks(domain, data))
                processed += 1

        except (json.JSONDecodeError, KeyError) as e:
            log.error(f"  Skipping {f.name}: {e}")

    if processed == 0:
        blocks.append(
            callout("No intel data files found in input directory.", "⚠️", "yellow_background")
        )

    # Footer
    blocks.append(divider())
    blocks.append(
        paragraph(
            f"Section A pipeline complete — {processed} domain(s) processed. "
            f"Next run: automated via GitHub Actions."
        )
    )

    return blocks


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Notion C-31 Updater — Section A Step 4")
    parser.add_argument("--page-id", required=True, help="Notion page ID")
    parser.add_argument("--week", required=True, help="ISO week e.g. 2026-W21")
    parser.add_argument("--run-date", required=True, help="Run date YYYY-MM-DD")
    parser.add_argument("--ew-triggered", default="false",
                        help="'true' or 'false'")
    parser.add_argument("--ew-count", type=int, default=0,
                        help="Number of EW-triggered domains")
    parser.add_argument("--ew-signals", default="",
                        help="Comma-separated EW domain names")
    parser.add_argument("--ew-severity", default="NONE",
                        choices=["NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL"],
                        help="Overall EW severity")
    parser.add_argument("--kg-version", required=True,
                        help="New KG version e.g. 4.26")
    parser.add_argument("--node-count", type=int, default=0,
                        help="Number of new KG nodes")
    parser.add_argument("--edge-count", type=int, default=0,
                        help="Number of new KG edges")
    parser.add_argument("--intel-dir", required=True,
                        help="Directory with intel JSON files")
    args = parser.parse_args()

    run_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    intel_dir = Path(args.intel_dir)

    log.info(
        f"Notion C-31 Update | page={args.page_id[:8]}... | "
        f"week={args.week} | EW={args.ew_triggered} | severity={args.ew_severity}"
    )

    blocks = build_all_blocks(args, intel_dir, run_ts)
    log.info(f"Total blocks to append: {len(blocks)}")

    success = append_blocks(args.page_id, blocks)

    if success:
        log.info(f"\n✅ Notion C-31 updated successfully — {len(blocks)} blocks appended")
    else:
        log.error("\n❌ Some blocks failed to append — check logs above")
        sys.exit(1)


if __name__ == "__main__":
    main()
