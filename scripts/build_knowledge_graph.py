#!/usr/bin/env python3
"""
build_knowledge_graph.py
========================
Repo: GilbertKwak/prompt-engineering-system
Purpose: Parse all MD files under docs/ and engines/ and emit knowledge_graph.json
         consumable by auto_validate.py (KG check).

Usage:
    python scripts/build_knowledge_graph.py
    python scripts/build_knowledge_graph.py --input docs engines --output knowledge_graph.json
    python scripts/build_knowledge_graph.py --verbose

Output schema  (knowledge_graph.json)
---------------------------------------
{
  "meta": {
    "generated_at": "<ISO-8601>",
    "version": "1.0",
    "total_nodes": N,
    "total_edges": N
  },
  "nodes": [
    {
      "id": "<relative/path/to/file.md>",
      "type": "rca" | "engine" | "report" | "agent" | "support" | "doc",
      "title": "<first H1 heading>",
      "status": "resolved" | "open" | "wip" | "unknown",
      "version": "<vX.Y from frontmatter>",
      "date": "<YYYY-MM-DD>",
      "tags": ["<tag>"],
      "notion_url": "<url or null>",
      "file_size": <bytes>,
      "sha": "<git-sha if available>"
    }
  ],
  "edges": [
    {
      "source": "<node-id>",
      "target": "<node-id>",
      "relation": "links_to" | "next" | "prev" | "references"
    }
  ]
}
"""

import os
import re
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_SCAN_DIRS = ["docs", "engines"]
DEFAULT_OUTPUT    = "knowledge_graph.json"
KG_VERSION        = "1.0"

# Map path prefixes → node type
TYPE_MAP = [
    ("docs/rca-capa",            "rca"),
    ("docs/report",              "report"),
    ("docs/agent",               "agent"),
    ("docs/support",             "support"),
    ("docs/new",                 "doc"),
    ("engines/PE-1",             "engine"),
    ("engines/PE-2",             "engine"),
    ("engines/PE-3",             "engine"),
    ("engines",                  "engine"),
    ("docs",                     "doc"),
]

STATUS_PATTERNS = [
    (r"✅\s*해결\s*완료",                 "resolved"),
    (r"status.*?resolved",               "resolved"),
    (r"상태.*?해결",                      "resolved"),
    (r"🔄.*?(진행|WIP|in.progress)",     "wip"),
    (r"❌.*?(미해결|open|실패)",           "open"),
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def infer_type(path: str) -> str:
    p = path.replace("\\", "/")
    for prefix, t in TYPE_MAP:
        if p.startswith(prefix):
            return t
    return "doc"


def extract_title(text: str) -> str:
    m = re.search(r"^#\s+(.+)", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def extract_status(text: str) -> str:
    for pattern, status in STATUS_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return status
    return "unknown"


def extract_version(text: str) -> str:
    m = re.search(r"해결\s*버전[:\s]*([vV][\d.]+)", text)
    if not m:
        m = re.search(r"version[:\s]*([vV][\d.]+)", text, re.IGNORECASE)
    return m.group(1) if m else ""


def extract_date(text: str) -> str:
    m = re.search(r"발행일[:\s]*(\d{4}-\d{2}-\d{2})", text)
    if not m:
        m = re.search(r"(\d{4}-\d{2}-\d{2})", text)
    return m.group(1) if m else ""


def extract_notion_url(text: str) -> str | None:
    m = re.search(r"https://www\.notion\.so/[\w\-]+", text)
    return m.group(0) if m else None


def extract_tags(path: str, text: str) -> list[str]:
    tags = []
    # derive from path segments
    parts = Path(path).parts
    for p in parts[:-1]:
        if p not in ("docs", "engines", "."):
            tags.append(p)
    # RCA ids
    for m in re.finditer(r"\bRCA-\d{3}\b", text):
        t = m.group(0)
        if t not in tags:
            tags.append(t)
    # version tags
    for m in re.finditer(r"\bv\d+\.\d+\b", text):
        t = m.group(0)
        if t not in tags:
            tags.append(t)
    return tags


def extract_links(path: str, text: str) -> list[dict]:
    """Return list of {source, target, relation} dicts."""
    base_dir = str(Path(path).parent)
    edges = []
    # Markdown links  [text](./relative)
    for m in re.finditer(r"\[[^\]]+\]\((\.{1,2}/[^)]+\.md)", text):
        rel = m.group(1)
        target = str((Path(base_dir) / rel).resolve().relative_to(Path.cwd()))
        target = target.replace("\\", "/")
        relation = "links_to"
        # detect next/prev from anchor text
        anchor = re.search(r"다음", m.group(0))
        if anchor:
            relation = "next"
        anchor2 = re.search(r"이전", m.group(0))
        if anchor2:
            relation = "prev"
        edges.append({"source": path, "target": target, "relation": relation})
    return edges


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------

def build_graph(scan_dirs: list[str], output: str, verbose: bool = False) -> dict:
    nodes = []
    edges = []
    seen_ids = set()

    for scan_dir in scan_dirs:
        base = Path(scan_dir)
        if not base.exists():
            if verbose:
                print(f"[SKIP] Directory not found: {scan_dir}")
            continue
        for md_path in sorted(base.rglob("*.md")):
            rel = str(md_path).replace("\\", "/")
            if rel in seen_ids:
                continue
            seen_ids.add(rel)

            try:
                text = md_path.read_text(encoding="utf-8")
            except Exception as e:
                if verbose:
                    print(f"[ERROR] Cannot read {rel}: {e}")
                continue

            node = {
                "id":          rel,
                "type":        infer_type(rel),
                "title":       extract_title(text),
                "status":      extract_status(text),
                "version":     extract_version(text),
                "date":        extract_date(text),
                "tags":        extract_tags(rel, text),
                "notion_url":  extract_notion_url(text),
                "file_size":   md_path.stat().st_size,
                "sha":         None,   # populated by CI if needed
            }
            nodes.append(node)

            for edge in extract_links(rel, text):
                edges.append(edge)

            if verbose:
                print(f"[NODE] {rel}  type={node['type']}  status={node['status']}")

    # Deduplicate edges
    seen_edges = set()
    unique_edges = []
    for e in edges:
        key = (e["source"], e["target"], e["relation"])
        if key not in seen_edges:
            seen_edges.add(key)
            unique_edges.append(e)

    graph = {
        "meta": {
            "generated_at":  datetime.now(timezone.utc).isoformat(),
            "version":       KG_VERSION,
            "total_nodes":   len(nodes),
            "total_edges":   len(unique_edges),
            "scan_dirs":     scan_dirs,
        },
        "nodes": nodes,
        "edges": unique_edges,
    }

    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n✅ knowledge_graph.json generated → {output}")
    print(f"   nodes : {len(nodes)}")
    print(f"   edges : {len(unique_edges)}")
    return graph


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build knowledge_graph.json from MD files")
    parser.add_argument(
        "--input", nargs="+", default=DEFAULT_SCAN_DIRS,
        help=f"Directories to scan (default: {DEFAULT_SCAN_DIRS})"
    )
    parser.add_argument(
        "--output", default=DEFAULT_OUTPUT,
        help=f"Output path (default: {DEFAULT_OUTPUT})"
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Print each node as it is processed"
    )
    args = parser.parse_args()
    build_graph(scan_dirs=args.input, output=args.output, verbose=args.verbose)
