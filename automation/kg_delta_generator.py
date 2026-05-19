#!/usr/bin/env python3
"""
kg_delta_generator.py  —  Knowledge Graph Delta Generator

Reads collected intel JSON files and produces a version-controlled KG delta:
  - New ENTITY nodes (companies, models, technologies, concepts)
  - RELATIONSHIP edges with typed predicates
  - EW-triggered special edges when signals are present
  - Metadata: version, week, provenance, confidence scores

Usage:
  python kg_delta_generator.py \
    --intel-dir      output/ai_intel \
    --current-version 4.25 \
    --next-version    4.26 \
    --week            2026-W21 \
    --run-date        2026-05-20 \
    --ew-signals      '' \
    --output          knowledge_graph_v4.26_delta.json
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Entity Catalog  (keyword → {id, type, label})
# ---------------------------------------------------------------------------

ENTITY_CATALOG: Dict[str, Dict] = {
    # Companies
    "openai":      {"id": "openai",      "type": "company",     "label": "OpenAI"},
    "anthropic":   {"id": "anthropic",   "type": "company",     "label": "Anthropic"},
    "google":      {"id": "google",      "type": "company",     "label": "Google DeepMind"},
    "deepmind":    {"id": "google",      "type": "company",     "label": "Google DeepMind"},
    "meta":        {"id": "meta_ai",     "type": "company",     "label": "Meta AI"},
    "microsoft":   {"id": "microsoft",   "type": "company",     "label": "Microsoft"},
    "nvidia":      {"id": "nvidia",      "type": "company",     "label": "NVIDIA"},
    "mistral":     {"id": "mistral",     "type": "company",     "label": "Mistral AI"},
    "cohere":      {"id": "cohere",      "type": "company",     "label": "Cohere"},
    "hugging face":{"id": "huggingface", "type": "company",     "label": "Hugging Face"},
    "xai":         {"id": "xai",         "type": "company",     "label": "xAI"},
    "groq":        {"id": "groq",        "type": "company",     "label": "Groq"},
    "cerebras":    {"id": "cerebras",    "type": "company",     "label": "Cerebras"},
    # Models
    "gpt-4o":      {"id": "gpt4o",       "type": "model",      "label": "GPT-4o"},
    "gpt-5":       {"id": "gpt5",        "type": "model",      "label": "GPT-5"},
    "claude":      {"id": "claude4",     "type": "model",      "label": "Claude"},
    "gemini":      {"id": "gemini25",    "type": "model",      "label": "Gemini 2.5"},
    "llama":       {"id": "llama4",      "type": "model",      "label": "Llama 4"},
    "grok":        {"id": "grok3",       "type": "model",      "label": "Grok-3"},
    # Technologies
    "rag":         {"id": "rag",         "type": "technology", "label": "RAG"},
    "fine-tuning": {"id": "fine_tuning", "type": "technology", "label": "Fine-Tuning"},
    "agentic":     {"id": "agentic_ai",  "type": "technology", "label": "Agentic AI"},
    "multi-agent": {"id": "multi_agent", "type": "technology", "label": "Multi-Agent"},
    "langchain":   {"id": "langchain",   "type": "technology", "label": "LangChain"},
    "langgraph":   {"id": "langgraph",   "type": "technology", "label": "LangGraph"},
    "mcp":         {"id": "mcp_protocol","type": "technology", "label": "MCP Protocol"},
    "a2a":         {"id": "a2a_protocol","type": "technology", "label": "A2A Protocol"},
    "h100":        {"id": "h100",        "type": "hardware",   "label": "NVIDIA H100"},
    "b200":        {"id": "b200",        "type": "hardware",   "label": "NVIDIA B200"},
    "hbm":         {"id": "hbm",         "type": "hardware",   "label": "HBM Memory"},
}

# Relationship predicate inference rules
REL_RULES: List[Dict] = [
    {"pattern": r"(\w+)\s+(?:releases?|launches?|introduces?)\s+(\w+)",
     "predicate": "RELEASES", "conf": 0.85},
    {"pattern": r"(\w+)\s+(?:partners?|collaborates?|integrates?)\s+with\s+(\w+)",
     "predicate": "PARTNERS_WITH", "conf": 0.80},
    {"pattern": r"(\w+)\s+(?:acquires?|buys?|purchases?)\s+(\w+)",
     "predicate": "ACQUIRES", "conf": 0.90},
    {"pattern": r"(\w+)\s+(?:competes?|rivals?)\s+(?:with\s+)?(\w+)",
     "predicate": "COMPETES_WITH", "conf": 0.75},
    {"pattern": r"(\w+)\s+(?:replaces?|supersedes?)\s+(\w+)",
     "predicate": "REPLACES", "conf": 0.85},
    {"pattern": r"(\w+)\s+(?:uses?|adopts?|deploys?)\s+(\w+)",
     "predicate": "ADOPTS", "conf": 0.70},
    {"pattern": r"(\w+)\s+(?:powers?|runs?)\s+on\s+(\w+)",
     "predicate": "RUNS_ON", "conf": 0.80},
]

# EW signal → special edge predicate
EW_EDGE_MAP: Dict[str, str] = {
    "enterprise_ai_adoption_rapid": "EW_ENTERPRISE_ADOPTION_SPIKE",
    "rag_replacement_threshold":    "EW_RAG_MIGRATION",
    "gpu_demand_spike":             "EW_GPU_DEMAND_SURGE",
    "open_source_dominance":        "EW_OSS_DOMINANCE",
    "reasoning_model_latency_drop": "EW_LATENCY_BREAKTHROUGH",
    "cost_reduction_steep":         "EW_COST_COLLAPSE",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _collect_text(obj: Any, acc: List[str]) -> None:
    if isinstance(obj, str):
        acc.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            _collect_text(v, acc)
    elif isinstance(obj, list):
        for item in obj:
            _collect_text(item, acc)


def _entity_slug(label: str) -> str:
    return re.sub(r"[^a-z0-9_]", "_", label.lower()).strip("_")


def _extract_entities_from_text(text: str) -> List[Dict]:
    """Match entity catalog keywords in text, return unique entity dicts."""
    found: Dict[str, Dict] = {}
    tl = text.lower()
    for keyword, meta in ENTITY_CATALOG.items():
        if keyword in tl:
            found[meta["id"]] = meta.copy()
    return list(found.values())


def _extract_relations_from_text(text: str, known_ids: Set[str]) -> List[Dict]:
    """Pattern-match relationship sentences."""
    rels: List[Dict] = []
    seen: Set[Tuple] = set()
    tl = text.lower()
    for rule in REL_RULES:
        for m in re.finditer(rule["pattern"], tl):
            src_raw, tgt_raw = m.group(1), m.group(2)
            # resolve to entity IDs
            src_id = next(
                (meta["id"] for kw, meta in ENTITY_CATALOG.items() if kw in src_raw), None
            )
            tgt_id = next(
                (meta["id"] for kw, meta in ENTITY_CATALOG.items() if kw in tgt_raw), None
            )
            if not src_id or not tgt_id or src_id == tgt_id:
                continue
            key = (src_id, rule["predicate"], tgt_id)
            if key in seen:
                continue
            seen.add(key)
            rels.append({
                "source": src_id,
                "predicate": rule["predicate"],
                "target": tgt_id,
                "confidence": rule["conf"],
                "evidence_snippet": text[max(0, m.start() - 40): m.end() + 40].strip(),
            })
    return rels


def _build_ew_edges(ew_signals_str: str) -> List[Dict]:
    """Generate EW-specific graph edges from signal IDs (comma-separated)."""
    edges: List[Dict] = []
    if not ew_signals_str or not ew_signals_str.strip():
        return edges
    for sig_id in [s.strip() for s in ew_signals_str.split(",") if s.strip()]:
        predicate = EW_EDGE_MAP.get(sig_id, f"EW_SIGNAL_{sig_id.upper()}")
        edges.append({
            "source": "ai_intel_system",
            "predicate": predicate,
            "target": "knowledge_graph",
            "confidence": 1.0,
            "ew_signal_id": sig_id,
            "is_ew_edge": True,
        })
    return edges


# ---------------------------------------------------------------------------
# Domain-level meta-node extraction from intel JSON
# ---------------------------------------------------------------------------

def _extract_from_intel_file(fp: Path) -> Tuple[List[Dict], List[Dict]]:
    """Return (entities, relations) from a single intel JSON."""
    try:
        data = json.loads(fp.read_text(encoding="utf-8"))
    except Exception:
        return [], []

    texts: List[str] = []
    _collect_text(data, texts)
    combined = " ".join(texts)

    entities = _extract_entities_from_text(combined)
    known_ids = {e["id"] for e in entities}

    # Add domain as a concept node
    domain = data.get("domain", "")
    if domain:
        domain_id = _entity_slug(domain)
        entities.append({"id": domain_id, "type": "domain", "label": domain.replace("_", " ").title()})
        known_ids.add(domain_id)

    # Add key_facts summary nodes
    for i, fact in enumerate(data.get("key_facts", [])[:5]):
        # Extract any entities mentioned in the fact
        fact_entities = _extract_entities_from_text(fact)
        entities.extend(fact_entities)
        known_ids.update(e["id"] for e in fact_entities)

    relations = _extract_relations_from_text(combined, known_ids)

    # Add domain ↔ entity edges
    if domain:
        domain_id = _entity_slug(domain)
        for ent in entities:
            if ent["id"] != domain_id and ent["type"] in ("company", "model", "technology"):
                relations.append({
                    "source": domain_id,
                    "predicate": "COVERS",
                    "target": ent["id"],
                    "confidence": 0.95,
                    "evidence_snippet": f"domain={domain}",
                })

    return entities, relations


# ---------------------------------------------------------------------------
# Delta Construction
# ---------------------------------------------------------------------------

def build_delta(
    intel_dir: Path,
    current_version: str,
    next_version: str,
    week: str,
    run_date: str,
    ew_signals_str: str,
    output_path: Optional[Path] = None,
) -> Dict:
    intel_files = sorted(intel_dir.glob("*.json")) if intel_dir.exists() else []

    all_entities: Dict[str, Dict] = {}
    all_relations: List[Dict] = []
    provenance: List[str] = []

    for fp in intel_files:
        ents, rels = _extract_from_intel_file(fp)
        provenance.append(fp.name)
        for ent in ents:
            if ent["id"] not in all_entities:
                all_entities[ent["id"]] = {
                    **ent,
                    "first_seen_week": week,
                    "source_file": fp.name,
                }
        all_relations.extend(rels)

    # Deduplicate relations
    seen_rels: Set[Tuple] = set()
    unique_rels: List[Dict] = []
    for rel in all_relations:
        key = (rel["source"], rel["predicate"], rel["target"])
        if key not in seen_rels:
            seen_rels.add(key)
            unique_rels.append({**rel, "week": week})

    # EW edges
    ew_edges = _build_ew_edges(ew_signals_str)
    unique_rels.extend(ew_edges)

    delta = {
        "metadata": {
            "kg_version_from": current_version,
            "kg_version_to": next_version,
            "week": week,
            "run_date": run_date,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "intel_files_processed": provenance,
            "ew_signals_applied": ew_signals_str,
        },
        "summary": {
            "new_nodes": len(all_entities),
            "new_edges": len(unique_rels),
            "ew_edges": len(ew_edges),
        },
        "nodes": list(all_entities.values()),
        "edges": unique_rels,
    }

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(delta, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[KG] Delta written: {output_path}")

    print(
        f"[KG] v{current_version}→v{next_version}  "
        f"nodes={len(all_entities)}  edges={len(unique_rels)}  ew_edges={len(ew_edges)}"
    )
    return delta


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Knowledge Graph Delta Generator")
    parser.add_argument("--intel-dir",        required=True)
    parser.add_argument("--current-version",  required=True)
    parser.add_argument("--next-version",     required=True)
    parser.add_argument("--week",             required=True)
    parser.add_argument("--run-date",         required=True)
    parser.add_argument("--ew-signals",       default="")
    parser.add_argument("--output",           default=None)
    args = parser.parse_args()

    build_delta(
        intel_dir=Path(args.intel_dir),
        current_version=args.current_version,
        next_version=args.next_version,
        week=args.week,
        run_date=args.run_date,
        ew_signals_str=args.ew_signals,
        output_path=Path(args.output) if args.output else None,
    )


if __name__ == "__main__":
    main()
