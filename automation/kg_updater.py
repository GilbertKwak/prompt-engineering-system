#!/usr/bin/env python3
"""
KG Updater — Gilbert PE System Knowledge Graph Node Manager
Version: 1.0.0  |  Compatible with KG v6.3

Usage:
  # Add / update a node
  python automation/kg_updater.py --add-node OPT-MASTER-001 --version 2.1 --domain opt-master

  # Query a node
  python automation/kg_updater.py --query-node OPT-MASTER-001

  # List all nodes
  python automation/kg_updater.py --list

  # List nodes in a domain
  python automation/kg_updater.py --list --domain opt-master

  # Delete a node
  python automation/kg_updater.py --delete-node OPT-MASTER-001

  # Export full KG as JSON
  python automation/kg_updater.py --export kg_export.json
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────
REPO_ROOT   = Path(__file__).resolve().parent.parent
KG_DIR      = REPO_ROOT / "automation" / "kg_nodes"
KG_INDEX    = REPO_ROOT / "automation" / "kg_index.json"

KG_DIR.mkdir(parents=True, exist_ok=True)


# ─── Helpers ──────────────────────────────────────────────────────────────────
def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_index() -> dict:
    if KG_INDEX.exists():
        with open(KG_INDEX, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": "6.3", "updated": now_iso(), "nodes": {}}


def save_index(index: dict) -> None:
    index["updated"] = now_iso()
    with open(KG_INDEX, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"[KG] Index saved → {KG_INDEX.relative_to(REPO_ROOT)}")


def node_path(node_id: str) -> Path:
    return KG_DIR / f"{node_id}.json"


def load_node(node_id: str) -> dict | None:
    p = node_path(node_id)
    if not p.exists():
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def save_node(node: dict) -> None:
    node_id = node["id"]
    p = node_path(node_id)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(node, f, ensure_ascii=False, indent=2)
    print(f"[KG] Node saved  → {p.relative_to(REPO_ROOT)}")


# ─── Commands ────────────────────────────────────────────────────────────────
def cmd_add(args) -> None:
    node_id: str = args.add_node
    version: str = args.version or "1.0"
    domain:  str = args.domain  or "general"
    tags:    list = args.tags   or []

    # Domain → auto-derive Notion & GitHub links if known
    notion_links = {
        "opt-master":     "https://app.notion.com/p/39055ed436f081b9a7a0ced964cb7b8a",
        "pe-intel":       "https://app.notion.com/p/36855ed436f08192a4d0ce8054028be9",
        "financial":      "https://app.notion.com/p/36f55ed436f081f5b875c0320816901c",
        "semiconductor":  "https://app.notion.com/p/34a55ed436f0814d9cffe6a2f0816e29",
    }
    github_base = (
        f"https://github.com/GilbertKwak/prompt-engineering-system/blob/main"
        f"/prompts/{domain}/{node_id}_v{version}.md"
    )

    # Load existing node to preserve history
    existing = load_node(node_id)
    history  = existing.get("history", []) if existing else []

    if existing:
        history.append({
            "version":    existing["version"],
            "updated_at": existing["updated_at"],
            "action":     "superseded"
        })
        print(f"[KG] Updating existing node '{node_id}' "
              f"(v{existing['version']} → v{version})")
    else:
        print(f"[KG] Creating new node '{node_id}' v{version}")

    node = {
        "id":          node_id,
        "version":     version,
        "domain":      domain,
        "tags":        tags,
        "kg_version":  "6.3",
        "created_at":  existing.get("created_at", now_iso()) if existing else now_iso(),
        "updated_at":  now_iso(),
        "notion_url":  notion_links.get(domain, ""),
        "github_url":  github_base,
        "status":      "active",
        "history":     history
    }

    save_node(node)

    # Update index
    index = load_index()
    index["nodes"][node_id] = {
        "version":    version,
        "domain":     domain,
        "updated_at": node["updated_at"],
        "status":     "active"
    }
    save_index(index)

    print(f"\n✅  Node '{node_id}' v{version} registered in KG v6.3")
    print(f"   Domain   : {domain}")
    print(f"   Notion   : {node['notion_url'] or '(not mapped)'}")
    print(f"   GitHub   : {node['github_url']}")


def cmd_query(args) -> None:
    node_id: str = args.query_node
    node = load_node(node_id)

    if node is None:
        print(f"[KG] ❌ Node '{node_id}' not found.")
        sys.exit(1)

    print(f"\n{'═'*54}")
    print(f"  KG Node: {node['id']}  (v{node['version']})")
    print(f"{'═'*54}")
    for key, val in node.items():
        if key == "history":
            continue
        print(f"  {key:<15}: {val}")
    if node.get("history"):
        print(f"  {'history':<15}: {len(node['history'])} previous version(s)")
        for h in node["history"]:
            print(f"    • v{h['version']} @ {h['updated_at']}  [{h['action']}]")
    print(f"{'═'*54}\n")


def cmd_list(args) -> None:
    index = load_index()
    nodes = index.get("nodes", {})

    if args.domain:
        nodes = {k: v for k, v in nodes.items() if v["domain"] == args.domain}

    if not nodes:
        print("[KG] No nodes found.")
        return

    domain_filter = f" (domain: {args.domain})" if args.domain else ""
    print(f"\n  KG Index — {len(nodes)} node(s){domain_filter}")
    print(f"  KG Version: {index.get('version', '?')}  |  Updated: {index.get('updated', '?')}")
    print(f"  {'ID':<25} {'VER':<8} {'DOMAIN':<20} {'STATUS':<10} UPDATED")
    print(f"  {'─'*80}")
    for node_id, meta in sorted(nodes.items()):
        print(
            f"  {node_id:<25} "
            f"v{meta['version']:<7} "
            f"{meta['domain']:<20} "
            f"{meta['status']:<10} "
            f"{meta['updated_at']}"
        )
    print()


def cmd_delete(args) -> None:
    node_id: str = args.delete_node
    p = node_path(node_id)

    if not p.exists():
        print(f"[KG] ❌ Node '{node_id}' not found.")
        sys.exit(1)

    # Soft-delete: mark status in node file
    node = load_node(node_id)
    node["status"]     = "deleted"
    node["deleted_at"] = now_iso()
    save_node(node)

    # Update index
    index = load_index()
    if node_id in index["nodes"]:
        index["nodes"][node_id]["status"] = "deleted"
    save_index(index)

    print(f"[KG] 🗑  Node '{node_id}' soft-deleted (status=deleted).")


def cmd_export(args) -> None:
    out_path = Path(args.export)
    index    = load_index()
    all_nodes = {}

    for node_id in index.get("nodes", {}):
        n = load_node(node_id)
        if n:
            all_nodes[node_id] = n

    export = {
        "kg_version":  index.get("version", "6.3"),
        "exported_at": now_iso(),
        "node_count":  len(all_nodes),
        "nodes":       all_nodes
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(export, f, ensure_ascii=False, indent=2)

    print(f"[KG] ✅ Exported {len(all_nodes)} node(s) → {out_path}")


# ─── CLI ─────────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        prog="kg_updater",
        description="Gilbert PE System — Knowledge Graph Node Manager (KG v6.3)"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--add-node",    metavar="NODE_ID",
                       help="Add or update a KG node")
    group.add_argument("--query-node",  metavar="NODE_ID",
                       help="Query details of a KG node")
    group.add_argument("--delete-node", metavar="NODE_ID",
                       help="Soft-delete a KG node")
    group.add_argument("--list",        action="store_true",
                       help="List all KG nodes")
    group.add_argument("--export",      metavar="FILE",
                       help="Export full KG to JSON file")

    parser.add_argument("--version",  help="Node version (e.g. 2.1)")
    parser.add_argument("--domain",   help="Node domain (e.g. opt-master)")
    parser.add_argument("--tags",     nargs="*", help="Tags for this node")

    args = parser.parse_args()

    if args.add_node:
        cmd_add(args)
    elif args.query_node:
        cmd_query(args)
    elif args.delete_node:
        cmd_delete(args)
    elif args.list:
        cmd_list(args)
    elif args.export:
        cmd_export(args)


if __name__ == "__main__":
    main()
