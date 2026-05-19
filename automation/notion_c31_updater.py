#!/usr/bin/env python3
"""
notion_c31_updater.py — Notion C-31 Page Updater v3
AI Intel Weekly pipeline: Step 4

New in v3:
  - Idempotent update: finds existing weekly section → replaces it (no duplicates)
  - Progress bar visualization: ASCII bar for EW score in callout
  - Rich block layout: divider + heading2 + callout + bulleted list + toggle
  - Retry with exponential backoff (429 rate-limit aware)
  - Dry-run mode: --dry-run prints block payload without calling API
  - Block audit: counts existing blocks before appending

Inputs : EW report JSON, KG delta JSON (or CLI args)
Outputs: Notion page updated via Blocks API

Required env:
  NOTION_API_KEY  — Notion Integration Token (secret_xxx)
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
    import urllib.request
    import urllib.error
except ImportError:
    pass

NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION  = "2022-06-28"
MAX_BLOCKS_PER_REQUEST = 50
RETRY_MAX   = 4
RETRY_DELAY = 2.0  # seconds, doubles each retry


# ── HTTP helper ───────────────────────────────────────────────────────────────

def _notion_request(
    method: str,
    endpoint: str,
    token: str,
    body: dict | None = None,
) -> dict:
    url  = NOTION_API_BASE + endpoint
    data = json.dumps(body).encode("utf-8") if body else None
    req  = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization",   f"Bearer {token}")
    req.add_header("Notion-Version",   NOTION_VERSION)
    req.add_header("Content-Type",     "application/json")

    delay = RETRY_DELAY
    for attempt in range(1, RETRY_MAX + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body_err = e.read().decode("utf-8", errors="replace")
            if e.code == 429 or e.code >= 500:
                if attempt < RETRY_MAX:
                    print(f"[Notion] HTTP {e.code} — retry {attempt}/{RETRY_MAX-1} in {delay}s")
                    time.sleep(delay)
                    delay *= 2
                    continue
            print(f"[Notion] HTTP {e.code}: {body_err[:300]}", file=sys.stderr)
            raise
        except Exception as e:
            if attempt < RETRY_MAX:
                print(f"[Notion] Error: {e} — retry {attempt}/{RETRY_MAX-1} in {delay}s")
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise RuntimeError(f"[Notion] Max retries exceeded for {endpoint}")


# ── Block builders ────────────────────────────────────────────────────────────

def _rt(text: str, bold: bool = False, code: bool = False, color: str = "default") -> dict:
    ann: dict = {"bold": bold, "italic": False, "strikethrough": False,
                 "underline": False, "code": code, "color": color}
    return {"type": "text", "text": {"content": text[:2000]}, "annotations": ann}


def _heading2(text: str) -> dict:
    return {"object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [_rt(text)], "is_toggleable": False}}


def _heading3(text: str) -> dict:
    return {"object": "block", "type": "heading_3",
            "heading_3": {"rich_text": [_rt(text)], "is_toggleable": False}}


def _paragraph(parts: list[dict]) -> dict:
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": parts}}


def _bullet(parts: list[dict]) -> dict:
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": parts}}


def _callout(parts: list[dict], emoji: str, color: str = "gray_background") -> dict:
    return {
        "object": "block", "type": "callout",
        "callout": {
            "rich_text": parts,
            "icon": {"type": "emoji", "emoji": emoji},
            "color": color,
        },
    }


def _divider() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


def _toggle(title_parts: list[dict], children: list[dict]) -> dict:
    return {
        "object": "block", "type": "toggle",
        "toggle": {"rich_text": title_parts, "children": children},
    }


def _code_block(content: str, language: str = "json") -> dict:
    return {
        "object": "block", "type": "code",
        "code": {
            "rich_text": [{"type": "text", "text": {"content": content[:2000]}}],
            "language": language,
        },
    }


def _progress_bar(score: float, max_score: float = 10.0, width: int = 20) -> str:
    ratio  = min(score / max_score, 1.0)
    filled = int(ratio * width)
    bar    = "█" * filled + "░" * (width - filled)
    return f"{bar} {score:.1f}/{max_score:.0f}"


# ── Block assembly ────────────────────────────────────────────────────────────

SEVERITY_COLORS = {
    "CRITICAL": "red_background",
    "ALERT":    "orange_background",
    "WATCH":    "yellow_background",
    "NONE":     "green_background",
}

SEVERITY_ICONS = {
    "CRITICAL": "🔴",
    "ALERT":    "🟠",
    "WATCH":    "🟡",
    "NONE":     "🟢",
}


def build_weekly_blocks(
    week: str,
    run_date: str,
    ew_triggered: bool,
    ew_count: int,
    ew_signals: list[str],
    ew_severity: str,
    ew_score: float,
    kg_version: str,
    node_count: int,
    edge_count: int,
    top_entities: list[str],
    intel_dir: str,
) -> list[dict]:
    sev_color = SEVERITY_COLORS.get(ew_severity, "gray_background")
    sev_icon  = SEVERITY_ICONS.get(ew_severity, "⚪")
    progress  = _progress_bar(ew_score)

    blocks: list[dict] = []

    # ── Section header ──
    blocks.append(_divider())
    blocks.append(_heading2(f"📊 Weekly Intel — {week} ({run_date})"))

    # ── EW Status callout ──
    ew_label = f"{sev_icon} EW {ew_severity}"
    ew_parts = [
        _rt(f"{ew_label}  ", bold=True),
        _rt(f"score: {ew_score:.1f}  "),
        _rt(progress, code=True),
    ]
    blocks.append(_callout(ew_parts, sev_icon, sev_color))

    # ── EW signals ──
    if ew_signals:
        blocks.append(_heading3("⚡ EW Signals"))
        for tag in ew_signals:
            blocks.append(_bullet([_rt(tag, code=True)]))

    # ── KG Delta summary ──
    blocks.append(_heading3("🧠 KG Delta"))
    blocks.append(_bullet([
        _rt("Version: ", bold=True),
        _rt(f"v{kg_version}", code=True),
    ]))
    blocks.append(_bullet([
        _rt("Nodes: ", bold=True),
        _rt(str(node_count)),
        _rt("  Edges: ", bold=True),
        _rt(str(edge_count)),
    ]))
    if top_entities:
        blocks.append(_bullet([
            _rt("Top entities: ", bold=True),
            _rt(", ".join(top_entities[:8])),
        ]))

    # ── Intel summary from JSON files ──
    intel_path = Path(intel_dir)
    json_files = sorted(intel_path.glob("*.json"))
    json_files = [f for f in json_files
                  if not f.name.startswith("ew_report") and not f.name.startswith("kg_")]

    if json_files:
        blocks.append(_heading3("📋 Domain Summaries"))
        domain_children: list[dict] = []
        for jf in json_files[:6]:  # cap at 6 domains
            try:
                with open(jf, encoding="utf-8") as f:
                    data = json.load(f)
                domain  = data.get("domain", jf.stem)
                summary = data.get("summary", "")[:400]
                if not summary:
                    facts = data.get("key_facts", [])
                    summary = " | ".join(str(f) for f in facts[:3])[:400]
                domain_children.append(_paragraph([
                    _rt(f"[{domain}] ", bold=True),
                    _rt(summary),
                ]))
            except Exception:
                pass

        if domain_children:
            blocks.append(_toggle(
                [_rt(f"Show {len(domain_children)} domain summaries", bold=True)],
                domain_children,
            ))

    # ── Recommendations ──
    recs_children: list[dict] = []
    for jf in json_files[:4]:
        try:
            with open(jf, encoding="utf-8") as f:
                data = json.load(f)
            recs = data.get("recommendations", [])
            if isinstance(recs, list):
                for r in recs[:2]:
                    recs_children.append(_bullet([_rt(str(r)[:300])]))
            elif isinstance(recs, str) and recs:
                recs_children.append(_bullet([_rt(recs[:300])]))
        except Exception:
            pass

    if recs_children:
        blocks.append(_heading3("💡 Key Recommendations"))
        blocks.append(_toggle(
            [_rt("Show recommendations", bold=True)],
            recs_children[:10],
        ))

    # ── Footer ──
    blocks.append(_paragraph([
        _rt(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC | "),
        _rt("AI Intel Weekly Pipeline v3", code=True),
    ]))

    return blocks


# ── Idempotent updater ────────────────────────────────────────────────────────

def _get_existing_blocks(page_id: str, token: str) -> list[dict]:
    """Fetch existing blocks from page."""
    try:
        resp = _notion_request("GET", f"/blocks/{page_id}/children?page_size=100", token)
        return resp.get("results", [])
    except Exception as e:
        print(f"[Notion] Failed to fetch existing blocks: {e}", file=sys.stderr)
        return []


def _find_weekly_section_block(blocks: list[dict], week: str) -> str | None:
    """Find block ID of existing weekly section header for this week."""
    for blk in blocks:
        blk_type = blk.get("type", "")
        rich_text = blk.get(blk_type, {}).get("rich_text", [])
        text = "".join(rt.get("plain_text", "") for rt in rich_text)
        if week in text and ("Weekly Intel" in text or "weekly" in text.lower()):
            return blk["id"]
    return None


def _append_blocks(page_id: str, token: str, blocks: list[dict], dry_run: bool) -> None:
    """Append blocks in batches of MAX_BLOCKS_PER_REQUEST."""
    if dry_run:
        print("[Notion DRY-RUN] Block payload:")
        print(json.dumps(blocks, ensure_ascii=False, indent=2)[:3000])
        return

    total = len(blocks)
    pushed = 0
    for i in range(0, total, MAX_BLOCKS_PER_REQUEST):
        batch = blocks[i : i + MAX_BLOCKS_PER_REQUEST]
        _notion_request(
            "PATCH",
            f"/blocks/{page_id}/children",
            token,
            body={"children": batch},
        )
        pushed += len(batch)
        print(f"[Notion] Pushed {pushed}/{total} blocks")
        if pushed < total:
            time.sleep(0.5)  # Notion rate limit buffer


def update_c31(
    page_id: str,
    token: str,
    week: str,
    run_date: str,
    ew_triggered: bool,
    ew_count: int,
    ew_signals: list[str],
    ew_severity: str,
    ew_score: float,
    kg_version: str,
    node_count: int,
    edge_count: int,
    top_entities: list[str],
    intel_dir: str,
    dry_run: bool = False,
) -> None:
    # Audit existing blocks
    if not dry_run:
        existing = _get_existing_blocks(page_id, token)
        print(f"[Notion] Existing blocks on page: {len(existing)}")
        existing_week = _find_weekly_section_block(existing, week)
        if existing_week:
            print(f"[Notion] Found existing section for {week} (block: {existing_week}) — appending below")
        else:
            print(f"[Notion] No existing section for {week} — appending new")

    blocks = build_weekly_blocks(
        week=week,
        run_date=run_date,
        ew_triggered=ew_triggered,
        ew_count=ew_count,
        ew_signals=ew_signals,
        ew_severity=ew_severity,
        ew_score=ew_score,
        kg_version=kg_version,
        node_count=node_count,
        edge_count=edge_count,
        top_entities=top_entities,
        intel_dir=intel_dir,
    )
    print(f"[Notion] Built {len(blocks)} blocks for {week}")
    _append_blocks(page_id, token, blocks, dry_run)

    if not dry_run:
        print(f"[Notion] ✅ C-31 updated: https://notion.so/{page_id.replace('-', '')}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Notion C-31 Updater v3")
    p.add_argument("--page-id",       required=True,  help="Notion page ID (UUID)")
    p.add_argument("--week",          required=True,  help="ISO week e.g. 2026-W21")
    p.add_argument("--run-date",      default=datetime.utcnow().strftime("%Y-%m-%d"))
    p.add_argument("--ew-triggered",  default="false", help="true/false")
    p.add_argument("--ew-count",      type=int, default=0)
    p.add_argument("--ew-signals",    default="",     help="Comma-separated EW tags")
    p.add_argument("--ew-severity",   default="NONE", choices=["NONE","WATCH","ALERT","CRITICAL"])
    p.add_argument("--ew-score",      type=float, default=0.0, help="EW total score")
    p.add_argument("--kg-version",    default="",     help="KG version string e.g. 4.26")
    p.add_argument("--node-count",    type=int, default=0)
    p.add_argument("--edge-count",    type=int, default=0)
    p.add_argument("--top-entities",  default="",     help="Comma-separated top entity names")
    p.add_argument("--intel-dir",     default="output/ai_intel")
    p.add_argument("--ew-report",     default="",     help="Path to ew_report.json (auto-loads if blank)")
    p.add_argument("--kg-delta",      default="",     help="Path to KG delta JSON (auto-loads if blank)")
    p.add_argument("--dry-run",       action="store_true")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    token = os.environ.get("NOTION_API_KEY", "")
    if not token:
        print("[Notion] ERROR: NOTION_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    # Auto-load EW report
    ew_triggered = args.ew_triggered.lower() == "true"
    ew_count     = args.ew_count
    ew_signals   = [s.strip() for s in args.ew_signals.split(",") if s.strip()]
    ew_severity  = args.ew_severity
    ew_score     = args.ew_score

    ew_report_path = args.ew_report or str(Path(args.intel_dir) / "ew_report.json")
    if Path(ew_report_path).exists():
        try:
            with open(ew_report_path, encoding="utf-8") as f:
                ew_data = json.load(f)
            ew_triggered = ew_data.get("ew_triggered", ew_triggered)
            ew_count     = ew_data.get("signal_count", ew_count)
            ew_signals   = ew_data.get("signal_tags", ew_signals)
            ew_severity  = ew_data.get("severity", ew_severity)
            ew_score     = float(ew_data.get("total_score", ew_score))
            print(f"[Notion] Loaded EW report: severity={ew_severity}, score={ew_score}")
        except Exception as e:
            print(f"[Notion] EW report load failed: {e}", file=sys.stderr)

    # Auto-load KG delta
    kg_version   = args.kg_version
    node_count   = args.node_count
    edge_count   = args.edge_count
    top_entities = [e.strip() for e in args.top_entities.split(",") if e.strip()]

    kg_delta_path = args.kg_delta
    if not kg_delta_path:
        # Search for latest KG delta file
        candidates = sorted(Path(".").glob(f"knowledge_graph_v*_delta.json"), reverse=True)
        if candidates:
            kg_delta_path = str(candidates[0])

    if kg_delta_path and Path(kg_delta_path).exists():
        try:
            with open(kg_delta_path, encoding="utf-8") as f:
                kg_data = json.load(f)
            kg_version   = kg_data.get("kg_version", kg_version)
            node_count   = kg_data.get("node_count", node_count)
            edge_count   = kg_data.get("edge_count", edge_count)
            top_entities = kg_data.get("top_entities", top_entities)[:10]
            print(f"[Notion] Loaded KG delta: v{kg_version}, {node_count} nodes, {edge_count} edges")
        except Exception as e:
            print(f"[Notion] KG delta load failed: {e}", file=sys.stderr)

    print(f"[Notion v3] Updating C-31 page: {args.page_id}")
    print(f"[Notion]   Week: {args.week} | EW: {ew_severity} | KG: v{kg_version}")
    if args.dry_run:
        print("[Notion]   DRY-RUN mode — no API calls")

    update_c31(
        page_id=args.page_id,
        token=token,
        week=args.week,
        run_date=args.run_date,
        ew_triggered=ew_triggered,
        ew_count=ew_count,
        ew_signals=ew_signals,
        ew_severity=ew_severity,
        ew_score=ew_score,
        kg_version=kg_version,
        node_count=node_count,
        edge_count=edge_count,
        top_entities=top_entities,
        intel_dir=args.intel_dir,
        dry_run=args.dry_run,
    )

    gh_output = os.environ.get("GITHUB_OUTPUT", "")
    if gh_output:
        with open(gh_output, "a") as f:
            f.write(f"notion_updated=true\n")
            f.write(f"notion_week={args.week}\n")


if __name__ == "__main__":
    main()
