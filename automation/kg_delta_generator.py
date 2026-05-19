#!/usr/bin/env python3
"""
kg_delta_generator.py — Section A, Step 3
지식 그래프 델타 자동 생성: 엔티티 추출 + EW 엣지 삽입

Usage:
  python kg_delta_generator.py \
    --intel-dir output/ai_intel \
    --current-version 4.25 \
    --next-version 4.26 \
    --week 2026-W21 \
    --run-date 2026-05-20 \
    --ew-signals "" \
    --output knowledge_graph_v4.26_delta.json
"""

import argparse
import json
import re
import sys
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("kg_delta_generator")

# ─── Known Entities ──────────────────────────────────────────────────────────
ENTITY_CATALOG = {
    # Companies
    "OpenAI": {"type": "COMPANY", "sector": "AI_LAB"},
    "Anthropic": {"type": "COMPANY", "sector": "AI_LAB"},
    "Google": {"type": "COMPANY", "sector": "BIG_TECH"},
    "DeepMind": {"type": "COMPANY", "sector": "AI_LAB"},
    "Meta": {"type": "COMPANY", "sector": "BIG_TECH"},
    "Microsoft": {"type": "COMPANY", "sector": "BIG_TECH"},
    "NVIDIA": {"type": "COMPANY", "sector": "HARDWARE"},
    "AMD": {"type": "COMPANY", "sector": "HARDWARE"},
    "Intel": {"type": "COMPANY", "sector": "HARDWARE"},
    "AWS": {"type": "COMPANY", "sector": "CLOUD"},
    "Azure": {"type": "COMPANY", "sector": "CLOUD"},
    "Hugging Face": {"type": "COMPANY", "sector": "OPEN_SOURCE"},
    "Mistral": {"type": "COMPANY", "sector": "AI_LAB"},
    "Cohere": {"type": "COMPANY", "sector": "AI_LAB"},
    "xAI": {"type": "COMPANY", "sector": "AI_LAB"},
    # Models
    "GPT-4": {"type": "MODEL", "family": "GPT"},
    "GPT-5": {"type": "MODEL", "family": "GPT"},
    "Claude": {"type": "MODEL", "family": "Claude"},
    "Gemini": {"type": "MODEL", "family": "Gemini"},
    "Llama": {"type": "MODEL", "family": "Llama"},
    "Grok": {"type": "MODEL", "family": "Grok"},
    # Frameworks
    "LangChain": {"type": "FRAMEWORK", "category": "ORCHESTRATION"},
    "LlamaIndex": {"type": "FRAMEWORK", "category": "RAG"},
    "AutoGen": {"type": "FRAMEWORK", "category": "MULTI_AGENT"},
    "CrewAI": {"type": "FRAMEWORK", "category": "MULTI_AGENT"},
    # Concepts
    "RAG": {"type": "CONCEPT", "category": "ARCHITECTURE"},
    "MoE": {"type": "CONCEPT", "category": "ARCHITECTURE"},
    "RLHF": {"type": "CONCEPT", "category": "TRAINING"},
    "Constitutional AI": {"type": "CONCEPT", "category": "SAFETY"},
}

# ─── EW Edge Type Mapping ─────────────────────────────────────────────────────
EW_EDGE_TEMPLATES = {
    "enterprise_deployment": {
        "edge_type": "EW_ENTERPRISE_DEPLOYMENT",
        "label": "Enterprise adoption EW signal",
        "weight": 0.9,
    },
    "model_architecture": {
        "edge_type": "EW_MODEL_RELEASE",
        "label": "Unexpected model architecture shift",
        "weight": 0.85,
    },
    "regulatory_policy": {
        "edge_type": "EW_REGULATORY",
        "label": "Regulatory action detected",
        "weight": 0.95,
    },
    "investment_funding": {
        "edge_type": "EW_FUNDING",
        "label": "Funding anomaly detected",
        "weight": 0.8,
    },
    "open_source": {
        "edge_type": "EW_OPEN_SOURCE",
        "label": "Open-source surge signal",
        "weight": 0.75,
    },
    "hardware_infrastructure": {
        "edge_type": "EW_HARDWARE",
        "label": "Hardware supply disruption",
        "weight": 0.9,
    },
    "safety_alignment": {
        "edge_type": "EW_SAFETY",
        "label": "Safety/alignment incident",
        "weight": 1.0,
    },
}


# ─── Entity Extraction ────────────────────────────────────────────────────────
def extract_entities_from_text(text: str) -> list[dict]:
    """Match known entities in text (case-sensitive keyword scan)."""
    found = []
    for entity_name, props in ENTITY_CATALOG.items():
        if entity_name in text:
            found.append({"name": entity_name, **props})
    return found


def extract_entities_from_intel(domain_data: dict) -> list[dict]:
    """Extract entities from signals, key_facts, and metrics."""
    all_text = ""
    for signal in domain_data.get("signals", []):
        all_text += signal.get("title", "") + " " + signal.get("summary", "") + " "
    all_text += " ".join(domain_data.get("key_facts", []))
    all_text += " ".join(str(v) for v in domain_data.get("metrics", {}).values())

    entities = extract_entities_from_text(all_text)
    return list({e["name"]: e for e in entities}.values())  # deduplicate


# ─── Node/Edge Builders ───────────────────────────────────────────────────────
def build_entity_nodes(entities: list[dict], domain: str, week: str) -> list[dict]:
    nodes = []
    for e in entities:
        node_id = f"{e['name'].replace(' ', '_').upper()}_{week}"
        nodes.append({
            "id": node_id,
            "label": e["name"],
            "type": e["type"],
            "domain": domain,
            "week": week,
            "properties": {k: v for k, v in e.items() if k not in ("name", "type")},
        })
    return nodes


def build_domain_signal_node(domain: str, week: str, signal_count: int,
                              ew_detected: bool) -> dict:
    return {
        "id": f"DOMAIN_{domain.upper()}_{week}",
        "label": f"{domain.replace('_', ' ').title()} — {week}",
        "type": "DOMAIN_SIGNAL",
        "domain": domain,
        "week": week,
        "properties": {
            "signal_count": signal_count,
            "ew_detected": ew_detected,
        },
    }


def build_edges_from_entities(entities: list[dict], domain: str,
                               week: str) -> list[dict]:
    edges = []
    domain_node_id = f"DOMAIN_{domain.upper()}_{week}"
    for e in entities:
        node_id = f"{e['name'].replace(' ', '_').upper()}_{week}"
        edges.append({
            "source": domain_node_id,
            "target": node_id,
            "edge_type": "MENTIONS",
            "weight": 0.6,
            "domain": domain,
            "week": week,
        })
    return edges


def build_ew_edges(ew_signals: list[str], week: str) -> list[dict]:
    """Generate EW-specific edges for triggered domains."""
    edges = []
    for domain in ew_signals:
        if not domain:
            continue
        template = EW_EDGE_TEMPLATES.get(domain, {
            "edge_type": "EW_GENERIC",
            "label": f"EW signal: {domain}",
            "weight": 0.7,
        })
        domain_node = f"DOMAIN_{domain.upper()}_{week}"
        ew_node = f"EW_{domain.upper()}_{week}"
        edges.append({
            "source": ew_node,
            "target": domain_node,
            "edge_type": template["edge_type"],
            "label": template["label"],
            "weight": template["weight"],
            "week": week,
            "ew_triggered": True,
        })
    return edges


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="KG Delta Generator — Section A Step 3")
    parser.add_argument("--intel-dir", required=True,
                        help="Directory with intel JSON files")
    parser.add_argument("--current-version", required=True,
                        help="Current KG version e.g. 4.25")
    parser.add_argument("--next-version", required=True,
                        help="Next KG version e.g. 4.26")
    parser.add_argument("--week", required=True, help="ISO week e.g. 2026-W21")
    parser.add_argument("--run-date", required=True, help="Run date YYYY-MM-DD")
    parser.add_argument("--ew-signals", default="",
                        help="Comma-separated EW-triggered domain names")
    parser.add_argument("--output", required=True, help="Output delta JSON path")
    args = parser.parse_args()

    input_dir = Path(args.intel_dir)
    ew_signals = [s.strip() for s in args.ew_signals.split(",") if s.strip()]

    log.info(
        f"KG Delta Generation | v{args.current_version}→v{args.next_version} "
        f"| week={args.week} | EW domains={ew_signals}"
    )

    all_nodes = []
    all_edges = []
    processed_domains = []

    # Load and process each intel file
    intel_files = list(input_dir.glob("intel_*.json"))
    log.info(f"Processing {len(intel_files)} intel files")

    for f in intel_files:
        try:
            with open(f, encoding="utf-8") as fp:
                data = json.load(fp)

            # Handle single or multi-domain
            if "domains" in data:
                domains_data = data["domains"].items()
            else:
                domains_data = [(data.get("domain", f.stem), data)]

            for domain, domain_data in domains_data:
                entities = extract_entities_from_intel(domain_data)
                signals = domain_data.get("signals", [])
                ew_detected = domain_data.get(
                    "ew_indicators", {}
                ).get("detected", domain in ew_signals)

                # Build nodes
                domain_node = build_domain_signal_node(
                    domain, args.week, len(signals), ew_detected
                )
                entity_nodes = build_entity_nodes(entities, domain, args.week)
                all_nodes.append(domain_node)
                all_nodes.extend(entity_nodes)

                # Build edges
                mention_edges = build_edges_from_entities(
                    entities, domain, args.week
                )
                all_edges.extend(mention_edges)

                processed_domains.append(domain)
                log.info(
                    f"  {domain}: {len(entities)} entities, "
                    f"{len(signals)} signals, EW={ew_detected}"
                )

        except (json.JSONDecodeError, KeyError) as e:
            log.error(f"Failed to process {f.name}: {e}")

    # Add EW edges
    ew_edges = build_ew_edges(ew_signals, args.week)
    all_edges.extend(ew_edges)
    if ew_edges:
        log.info(f"  EW edges added: {len(ew_edges)}")

    # Deduplicate nodes by id
    seen_ids = set()
    unique_nodes = []
    for n in all_nodes:
        if n["id"] not in seen_ids:
            unique_nodes.append(n)
            seen_ids.add(n["id"])

    delta = {
        "meta": {
            "delta_type": "weekly_intel",
            "from_version": args.current_version,
            "to_version": args.next_version,
            "week": args.week,
            "run_date": args.run_date,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "processed_domains": processed_domains,
            "ew_signals": ew_signals,
        },
        "stats": {
            "new_nodes": len(unique_nodes),
            "new_edges": len(all_edges),
            "ew_edges": len(ew_edges),
            "entity_nodes": len([n for n in unique_nodes if n["type"] != "DOMAIN_SIGNAL"]),
        },
        "nodes": unique_nodes,
        "edges": all_edges,
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(delta, f, ensure_ascii=False, indent=2)

    log.info(
        f"\n✅ KG Delta → {args.output}\n"
        f"   nodes={delta['stats']['new_nodes']} "
        f"edges={delta['stats']['new_edges']} "
        f"ew_edges={delta['stats']['ew_edges']}"
    )


if __name__ == "__main__":
    main()
