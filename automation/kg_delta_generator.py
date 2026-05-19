#!/usr/bin/env python3
"""
kg_delta_generator.py — Knowledge Graph Delta Generator v2
AI Intel Weekly pipeline: Step 3

Inputs : output/ai_intel/*.json  (intel files)
         ew_report.json          (EW signals from step 2)
Outputs: knowledge_graph_vX.Y_delta.json

KG Node types  : COMPANY / MODEL / TECHNOLOGY / CONCEPT / REGULATION / PERSON
KG Edge types  : DEVELOPS / COMPETES / ENABLES / REGULATES / THREATENS / LEADS
                 ACQUIRES / PARTNERS / BENCHMARKS / EW_<TAG>

Delta logic:
  - Extract entities from intel key_facts + summary
  - Generate edges from co-occurrence + explicit relation phrases
  - Detect conflicts with previous version patterns
  - Output versioned delta JSON ready for Notion KG DB import
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# ── Entity Extraction Config ──────────────────────────────────────────────────

ENTITY_PATTERNS: dict[str, list[str]] = {
    "COMPANY": [
        "OpenAI", "Anthropic", "Google DeepMind", "Google", "Microsoft", "Meta",
        "Amazon", "Apple", "NVIDIA", "AMD", "Intel", "TSMC", "Samsung",
        "SK Hynix", "Micron", "ASML", "Mistral", "Cohere", "AI21 Labs",
        "Stability AI", "Inflection", "xAI", "Baidu", "Alibaba", "Tencent",
        "Huawei", "ByteDance", "Arm", "Qualcomm",
    ],
    "MODEL": [
        "GPT-5", "GPT-4o", "GPT-4", "Claude 4", "Claude 3.7", "Claude 3.5",
        "Gemini 2.5", "Gemini 2.0", "Gemini 1.5", "Llama 4", "Llama 3",
        "Mistral Large", "Mixtral", "Grok 3", "Grok 2", "DeepSeek V3",
        "DeepSeek R2", "Qwen 3", "Command R+", "Phi-4",
    ],
    "TECHNOLOGY": [
        "RAG", "MoE", "MoE architecture", "LoRA", "QLoRA", "RLHF", "DPO",
        "speculative decoding", "flash attention", "quantization",
        "HBM3e", "HBM4", "CoWoS", "SoW", "NVLink", "InfiniBand",
        "H100", "H200", "B200", "GB200", "MI300X", "Gaudi 3",
        "multi-agent", "agentic AI", "tool use", "function calling",
        "long context", "computer use", "code interpreter",
    ],
    "CONCEPT": [
        "inference scaling", "test-time compute", "chain-of-thought",
        "in-context learning", "few-shot", "zero-shot", "fine-tuning",
        "model distillation", "model pruning", "knowledge distillation",
        "AI safety", "alignment", "constitutional AI", "red-teaming",
        "enterprise AI", "AI governance", "responsible AI",
    ],
    "REGULATION": [
        "EU AI Act", "AI Safety Act", "CHIPS Act", "Export Control",
        "BIS Rule", "EAR regulation", "ITAR", "NSF AI",
        "Senate AI", "House AI bill", "G7 AI", "UN AI resolution",
    ],
}

RELATION_PHRASES: list[dict] = [
    {"pattern": r"(\w[\w\s]+)\s+acquir(?:es|ed|ing)\s+([\w\s]+)",        "edge": "ACQUIRES"},
    {"pattern": r"(\w[\w\s]+)\s+partner(?:s|ed|ing)\s+with\s+([\w\s]+)",  "edge": "PARTNERS"},
    {"pattern": r"(\w[\w\s]+)\s+(?:beats?|surpass(?:es|ed)|outperform(?:s|ed))\s+([\w\s]+)",  "edge": "BENCHMARKS"},
    {"pattern": r"(\w[\w\s]+)\s+(?:threaten|disrupt|replac)(?:es|ed|ing)\s+([\w\s]+)",       "edge": "THREATENS"},
    {"pattern": r"(\w[\w\s]+)\s+(?:enables?|powers?|supports?)\s+([\w\s]+)",                 "edge": "ENABLES"},
    {"pattern": r"(\w[\w\s]+)\s+(?:competes?|rival(?:s|ed))\s+with\s+([\w\s]+)",             "edge": "COMPETES"},
    {"pattern": r"(\w[\w\s]+)\s+(?:develops?|release[sd]?|launch(?:es|ed))\s+([\w\s]+)",     "edge": "DEVELOPS"},
    {"pattern": r"(\w[\w\s]+)\s+(?:leads?|lead(?:s|ing))\s+(?:in|on)\s+([\w\s]+)",          "edge": "LEADS"},
]

EW_EDGE_MAP: dict[str, str] = {
    "EW_EXPORT_CONTROL":     "REGULATES",
    "EW_CAPABILITY_JUMP":    "ENABLES",
    "EW_STRATEGIC_ALLIANCE": "PARTNERS",
    "EW_REGULATORY":         "REGULATES",
    "EW_OPENSOURCE_PARITY":  "BENCHMARKS",
    "EW_RAG_MIGRATION":      "THREATENS",
    "EW_HW_SUPPLY":          "THREATENS",
    "EW_AGENT_AUTONOMY":     "ENABLES",
    "EW_CROSS_DOMAIN":       "ENABLES",
}


# ── Entity Extraction ─────────────────────────────────────────────────────────

def extract_entities(text: str) -> list[dict]:
    """Find all known entities in text, return deduplicated node list."""
    found: dict[str, dict] = {}
    text_lower = text.lower()
    for node_type, names in ENTITY_PATTERNS.items():
        for name in names:
            if name.lower() in text_lower:
                key = name.lower()
                if key not in found:
                    found[key] = {
                        "id":    name.replace(" ", "_").upper(),
                        "label": name,
                        "type":  node_type,
                    }
    return list(found.values())


def extract_edges_from_relations(text: str, known_entities: set[str]) -> list[dict]:
    """Match relation phrases and return edges between known entities."""
    edges = []
    for rp in RELATION_PHRASES:
        for m in re.finditer(rp["pattern"], text, re.IGNORECASE):
            src_raw = m.group(1).strip()
            tgt_raw = m.group(2).strip()
            # fuzzy match to known entity labels
            src = _fuzzy_entity(src_raw, known_entities)
            tgt = _fuzzy_entity(tgt_raw, known_entities)
            if src and tgt and src != tgt:
                edges.append({
                    "source":   src.replace(" ", "_").upper(),
                    "target":   tgt.replace(" ", "_").upper(),
                    "relation": rp["edge"],
                    "context":  m.group(0)[:120],
                })
    return edges


def _fuzzy_entity(raw: str, known: set[str]) -> str | None:
    raw_lower = raw.lower()
    for name in known:
        if name.lower() in raw_lower or raw_lower in name.lower():
            return name
    return None


def cooccurrence_edges(entities: list[dict], domain: str) -> list[dict]:
    """Generate COMPETES / DEVELOPS edges for co-occurring entities in same domain."""
    edges = []
    companies = [e for e in entities if e["type"] == "COMPANY"]
    models    = [e for e in entities if e["type"] == "MODEL"]
    techs     = [e for e in entities if e["type"] == "TECHNOLOGY"]

    # Company → Model (DEVELOPS)
    for c in companies:
        for m in models:
            edges.append({
                "source":   c["id"],
                "target":   m["id"],
                "relation": "DEVELOPS",
                "context":  f"Co-occurrence in {domain}",
            })

    # Company ↔ Company (COMPETES) — limit to first 3 pairs
    for i, c1 in enumerate(companies[:4]):
        for c2 in companies[i+1:4]:
            edges.append({
                "source":   c1["id"],
                "target":   c2["id"],
                "relation": "COMPETES",
                "context":  f"Co-occurrence in {domain}",
            })

    # Technology → Concept (ENABLES)
    for t in techs[:3]:
        for e in entities:
            if e["type"] == "CONCEPT":
                edges.append({
                    "source":   t["id"],
                    "target":   e["id"],
                    "relation": "ENABLES",
                    "context":  f"Co-occurrence in {domain}",
                })
                break  # one per tech

    return edges


def ew_edges(ew_signals: list[str], all_entities: list[dict]) -> list[dict]:
    """Inject EW-tagged edges into KG for triggered signals."""
    edges = []
    entity_ids = [e["id"] for e in all_entities]
    if len(entity_ids) < 2:
        return edges
    src, tgt = entity_ids[0], entity_ids[1]
    for tag in ew_signals:
        rel = EW_EDGE_MAP.get(tag, "ENABLES")
        edges.append({
            "source":   src,
            "target":   tgt,
            "relation": rel,
            "context":  f"EW signal: {tag}",
            "ew_tag":   tag,
        })
    return edges


def detect_conflicts(new_edges: list[dict]) -> list[dict]:
    """Detect contradictory edges (e.g. A COMPETES B and A PARTNERS B)."""
    conflicts = []
    pair_relations: dict[tuple, list[str]] = {}
    for e in new_edges:
        key = (min(e["source"], e["target"]), max(e["source"], e["target"]))
        pair_relations.setdefault(key, []).append(e["relation"])
    for pair, rels in pair_relations.items():
        if "COMPETES" in rels and "PARTNERS" in rels:
            conflicts.append({
                "pair":      list(pair),
                "relations": rels,
                "note":      "Coopetition: competitors also partnering",
            })
        if "ACQUIRES" in rels and "COMPETES" in rels:
            conflicts.append({
                "pair":      list(pair),
                "relations": rels,
                "note":      "M&A target was previously competitor",
            })
    return conflicts


# ── Main Delta Generation ──────────────────────────────────────────────────────

def generate_delta(
    intel_dir: str,
    current_version: str,
    next_version: str,
    week: str,
    run_date: str,
    ew_signals: list[str],
) -> dict:
    intel_path = Path(intel_dir)
    all_nodes: dict[str, dict] = {}
    all_edges: list[dict] = []
    domain_summaries: dict[str, str] = {}

    json_files = sorted(intel_path.glob("*.json"))
    for jf in json_files:
        if jf.name == "ew_report.json":
            continue
        try:
            with open(jf, encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"[KG] Skip {jf.name}: {e}", file=sys.stderr)
            continue

        domain = data.get("domain", jf.stem)
        parts  = []
        for field in ("summary", "analysis", "key_facts", "recommendations"):
            val = data.get(field, "")
            if isinstance(val, list):
                parts.extend(str(v) for v in val)
            elif val:
                parts.append(str(val))
        text = " ".join(parts)

        # Extract entities
        entities = extract_entities(text)
        for e in entities:
            all_nodes[e["id"]] = e

        known_names = set(ENTITY_PATTERNS[t][i]
                         for t in ENTITY_PATTERNS
                         for i in range(len(ENTITY_PATTERNS[t])))
        # Relation edges
        rel_edges = extract_edges_from_relations(text, known_names)
        all_edges.extend(rel_edges)

        # Co-occurrence edges
        co_edges = cooccurrence_edges(entities, domain)
        all_edges.extend(co_edges)

        domain_summaries[domain] = (
            data.get("summary", "")[:200]
            if isinstance(data.get("summary"), str)
            else ""
        )

    # EW signal edges
    ew_edge_list = ew_edges(ew_signals, list(all_nodes.values()))
    all_edges.extend(ew_edge_list)

    # Deduplicate edges by (source, target, relation)
    seen_edges: set[tuple] = set()
    dedup_edges = []
    for e in all_edges:
        key = (e["source"], e["target"], e["relation"])
        if key not in seen_edges:
            seen_edges.add(key)
            dedup_edges.append(e)

    # Conflict detection
    conflicts = detect_conflicts(dedup_edges)

    delta = {
        "version_from":      current_version,
        "version_to":        next_version,
        "week":              week,
        "generated_at":      datetime.utcnow().isoformat() + "Z",
        "run_date":          run_date,
        "node_count":        len(all_nodes),
        "edge_count":        len(dedup_edges),
        "ew_edge_count":     len(ew_edge_list),
        "conflict_count":    len(conflicts),
        "nodes":             list(all_nodes.values()),
        "edges":             dedup_edges,
        "conflicts":         conflicts,
        "domain_summaries":  domain_summaries,
        "ew_signals":        ew_signals,
    }
    return delta


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="KG Delta Generator")
    p.add_argument("--intel-dir",        default="output/ai_intel")
    p.add_argument("--current-version",  required=True,  help="e.g. 4.25")
    p.add_argument("--next-version",     required=True,  help="e.g. 4.26")
    p.add_argument("--week",             required=True,  help="e.g. 2026-W21")
    p.add_argument("--run-date",         required=True,  help="YYYY-MM-DD")
    p.add_argument("--ew-signals",       default="",     help="Comma-separated EW tags")
    p.add_argument("--output",           default="",     help="Output JSON path")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    ew_signals = [s.strip() for s in args.ew_signals.split(",") if s.strip()]

    print(f"[KG] Generating delta: v{args.current_version} → v{args.next_version}")
    delta = generate_delta(
        intel_dir=args.intel_dir,
        current_version=args.current_version,
        next_version=args.next_version,
        week=args.week,
        run_date=args.run_date,
        ew_signals=ew_signals,
    )

    out_path = args.output or f"knowledge_graph_v{args.next_version}_delta.json"
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(delta, f, ensure_ascii=False, indent=2)

    print(f"[KG] Nodes     : {delta['node_count']}")
    print(f"[KG] Edges     : {delta['edge_count']} ({delta['ew_edge_count']} EW)")
    print(f"[KG] Conflicts : {delta['conflict_count']}")
    print(f"[KG] Output    : {out_path}")

    # GitHub Actions outputs
    gh_output = os.environ.get("GITHUB_OUTPUT", "")
    if gh_output:
        with open(gh_output, "a") as f:
            f.write(f"node_count={delta['node_count']}\n")
            f.write(f"edge_count={delta['edge_count']}\n")
            f.write(f"conflict_count={delta['conflict_count']}\n")


if __name__ == "__main__":
    main()
