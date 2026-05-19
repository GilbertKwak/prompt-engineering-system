#!/usr/bin/env python3
"""
kg_delta_generator.py — Knowledge Graph Delta Generator
Generates KG node/edge deltas from collected AI intel JSON files.

Usage:
    python kg_delta_generator.py \\
        --intel-dir output/ai_intel \\
        --current-version 4.25 --next-version 4.26 \\
        --week 2026-W21 --run-date 2026-05-20 \\
        --ew-signals "" \\
        --output knowledge_graph_v4.26_delta.json
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# ── Known entity catalogue (keyword → canonical name, type) ───────────────────
ENTITY_CATALOGUE: list[tuple[str, str, str]] = [
    # (keyword, canonical_name, node_type)
    ("nvidia",        "NVIDIA",        "Company"),
    ("openai",        "OpenAI",         "Company"),
    ("anthropic",     "Anthropic",      "Company"),
    ("google",        "Google DeepMind","Company"),
    ("meta",          "Meta AI",        "Company"),
    ("microsoft",     "Microsoft",      "Company"),
    ("hugging face",  "Hugging Face",   "Platform"),
    ("langchain",     "LangChain",      "Framework"),
    ("llamaindex",    "LlamaIndex",     "Framework"),
    ("claude",        "Claude",         "Model"),
    ("gpt",           "GPT Series",     "Model"),
    ("gemini",        "Gemini",         "Model"),
    ("llama",         "LLaMA",          "Model"),
    ("mistral",       "Mistral",        "Model"),
    ("rag",           "RAG",            "Technique"),
    ("agent",         "AI Agent",       "Concept"),
    ("multimodal",    "Multimodal AI",  "Concept"),
    ("fine-tuning",   "Fine-Tuning",    "Technique"),
    ("inference",     "LLM Inference",  "Concept"),
    ("enterprise",    "Enterprise AI",  "Segment"),
    ("open source",   "Open Source AI", "Segment"),
]

EW_EDGE_TYPES: dict[str, str] = {
    "RAG Migration":         "EW_RAG_MIGRATION",
    "Enterprise Adoption":   "EW_ENTERPRISE_SURGE",
    "Model Release":         "EW_RAPID_RELEASE",
    "Cost Reduction":        "EW_COST_COLLAPSE",
    "Open Source":           "EW_OS_DOMINANCE",
    "Agent Autonomy":        "EW_AGENT_AUTONOMY",
    "Multimodal":            "EW_MULTIMODAL_SURGE",
}


# ── helpers ────────────────────────────────────────────────────────────────────

def _make_node_id(name: str) -> str:
    return name.upper().replace(" ", "_").replace("-", "_")


def _extract_entities_from_text(text: str) -> list[tuple[str, str, str]]:
    """Return list of (keyword, canonical_name, node_type) found in text."""
    found: list[tuple[str, str, str]] = []
    text_lower = text.lower()
    for kw, name, ntype in ENTITY_CATALOGUE:
        if kw in text_lower:
            found.append((kw, name, ntype))
    return found


def _intel_to_text(data: dict) -> str:
    """Flatten all string values in a dict to a single searchable text."""
    parts: list[str] = []
    for v in data.values():
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, list):
            parts.extend(str(x) for x in v)
        elif isinstance(v, dict):
            parts.extend(str(x) for x in v.values())
    return " ".join(parts)


def _build_nodes_from_intel(intel_files: list[Path]) -> list[dict]:
    """Build KG node list from intel files."""
    seen: set[str] = set()
    nodes: list[dict] = []

    for fp in intel_files:
        try:
            with open(fp, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[WARN] Cannot read {fp.name}: {e}", file=sys.stderr)
            continue

        text = _intel_to_text(data)
        domain = data.get("domain", fp.stem)
        entities = _extract_entities_from_text(text)

        for kw, name, ntype in entities:
            nid = _make_node_id(name)
            if nid not in seen:
                seen.add(nid)
                nodes.append({
                    "id": nid,
                    "label": name,
                    "type": ntype,
                    "source_domain": domain,
                    "extracted_from": fp.name,
                    "properties": {
                        "keyword": kw,
                        "last_seen_week": "",  # filled in run_generation
                    },
                })
    return nodes


def _build_edges_from_nodes(nodes: list[dict], ew_signals: list[str]) -> list[dict]:
    """Build edges: co-occurrence within same domain + EW signal edges."""
    edges: list[dict] = []
    edge_set: set[tuple[str, str, str]] = set()

    # Co-occurrence edges (same domain)
    from collections import defaultdict
    domain_nodes: dict[str, list[str]] = defaultdict(list)
    for n in nodes:
        domain_nodes[n["source_domain"]].append(n["id"])

    for domain, nids in domain_nodes.items():
        for i, a in enumerate(nids):
            for b in nids[i + 1:]:
                key = (min(a, b), max(a, b), "CO_OCCURS")
                if key not in edge_set:
                    edge_set.add(key)
                    edges.append({
                        "source": a,
                        "target": b,
                        "type": "CO_OCCURS",
                        "domain": domain,
                        "weight": 1.0,
                    })

    # EW signal edges
    for signal in ew_signals:
        etype = "EW_SIGNAL"
        for kw, ew_type in EW_EDGE_TYPES.items():
            if kw.lower() in signal.lower():
                etype = ew_type
                break
        edges.append({
            "source": "EW_TRIGGER",
            "target": "AI_ECOSYSTEM",
            "type": etype,
            "signal": signal,
            "weight": 2.0,
        })

    return edges


# ── core generation ────────────────────────────────────────────────────────────

def run_generation(
    intel_dir: str,
    current_version: str,
    next_version: str,
    week: str,
    run_date: str,
    ew_signals_raw: str,
    output_path: str,
) -> dict:
    intel_files = list(Path(intel_dir).glob("*.json"))
    if not intel_files:
        print(f"[WARN] No JSON files found in {intel_dir}", file=sys.stderr)

    ew_signals = [s.strip() for s in ew_signals_raw.split(",") if s.strip()] if ew_signals_raw else []

    nodes = _build_nodes_from_intel(intel_files)
    # Backfill week
    for n in nodes:
        n["properties"]["last_seen_week"] = week

    edges = _build_edges_from_nodes(nodes, ew_signals)

    # Summary stats
    node_count = len(nodes)
    edge_count = len(edges)
    node_types: dict[str, int] = {}
    for n in nodes:
        t = n["type"]
        node_types[t] = node_types.get(t, 0) + 1

    delta = {
        "metadata": {
            "current_version": current_version,
            "next_version": next_version,
            "week": week,
            "run_date": run_date,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "intel_files_processed": len(intel_files),
            "ew_signals": ew_signals,
        },
        "summary": {
            "node_count": node_count,
            "edge_count": edge_count,
            "node_types": node_types,
        },
        "nodes": nodes,
        "edges": edges,
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(delta, f, ensure_ascii=False, indent=2)

    print(f"\n[KG Delta] v{current_version} → v{next_version}")
    print(f"  Nodes: {node_count} | Edges: {edge_count} | EW signals: {len(ew_signals)}")
    print(f"  Node types: {node_types}")
    print(f"  Saved → {output_path}")
    return delta


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Knowledge Graph Delta Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--intel-dir",         required=True,  help="Directory with intel JSON files")
    parser.add_argument("--current-version",   required=True,  help="Current KG version e.g. 4.25")
    parser.add_argument("--next-version",       required=True,  help="Next KG version e.g. 4.26")
    parser.add_argument("--week",               required=True,  help="ISO week e.g. 2026-W21")
    parser.add_argument("--run-date",           required=True,  help="Run date YYYY-MM-DD")
    parser.add_argument("--ew-signals",         default="",     help="Comma-separated EW signal labels")
    parser.add_argument("--output",             required=True,  help="Output JSON file path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(f"\n{'='*60}")
    print(f"KG Delta Generator — {args.week}  (v{args.current_version} → v{args.next_version})")
    print(f"{'='*60}")

    run_generation(
        intel_dir=args.intel_dir,
        current_version=args.current_version,
        next_version=args.next_version,
        week=args.week,
        run_date=args.run_date,
        ew_signals_raw=args.ew_signals,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()
