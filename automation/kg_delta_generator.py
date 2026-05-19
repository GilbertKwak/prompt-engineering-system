#!/usr/bin/env python3
"""
kg_delta_generator.py — Knowledge Graph Delta Generator v3
AI Intel Weekly pipeline: Step 3

New in v3:
  - Entity deduplication: merges duplicate nodes by canonical name mapping
  - Relation confidence scoring: frequency + sentiment → confidence 0.0-1.0
  - Semantic versioning changelog: auto-generates CHANGELOG entry
  - JSON-LD compatible output: @context, @type, @id fields added
  - EW signal → typed relation mapping (expanded 15 signal types)
  - Source attribution: each node/edge tracks source_file + week

Inputs : output/ai_intel/*.json, ew_report.json
Outputs: knowledge_graph_v{next}.json, kg_changelog.md (append)
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

# Canonical name → aliases mapping for deduplication
ENTITY_CANONICAL: dict[str, list[str]] = {
    "NVIDIA":       ["nvidia", "nvda"],
    "Google":       ["google", "alphabet", "deepmind", "google deepmind"],
    "Microsoft":    ["microsoft", "msft", "azure"],
    "OpenAI":       ["openai", "open ai", "chatgpt"],
    "Anthropic":    ["anthropic", "claude"],
    "Meta":         ["meta", "meta ai", "llama", "meta platforms"],
    "Amazon":       ["amazon", "aws", "amazon web services"],
    "TSMC":         ["tsmc", "taiwan semiconductor"],
    "Samsung":      ["samsung", "samsung electronics", "hbm samsung"],
    "SK Hynix":     ["sk hynix", "hynix"],
    "Huawei":       ["huawei"],
    "DeepSeek":     ["deepseek", "deep seek"],
    "Mistral":      ["mistral", "mistral ai"],
    "LangChain":    ["langchain", "lang chain"],
    "HuggingFace":  ["hugging face", "huggingface"],
    "Perplexity":   ["perplexity", "perplexity ai"],
    "xAI":          ["xai", "grok", "elon musk ai"],
    "Cohere":       ["cohere"],
    "Databricks":   ["databricks", "mosaic ml"],
    "AMD":          ["amd", "advanced micro devices", "instinct"],
    "Intel":        ["intel", "intel ai", "gaudi"],
    "EU AI Act":    ["eu ai act", "european ai regulation", "eu regulation"],
    "RAG":          ["rag", "retrieval augmented generation", "retrieval-augmented"],
    "HBM":          ["hbm", "high bandwidth memory"],
    "GPT-4":        ["gpt-4", "gpt4", "o1", "o3", "o4"],
    "Gemini":       ["gemini", "gemini ultra", "gemini pro"],
}

# Entity type classification
ENTITY_TYPES: dict[str, str] = {
    "NVIDIA": "Company",     "Google": "Company",      "Microsoft": "Company",
    "OpenAI": "Company",     "Anthropic": "Company",   "Meta": "Company",
    "Amazon": "Company",     "TSMC": "Company",        "Samsung": "Company",
    "SK Hynix": "Company",   "Huawei": "Company",      "DeepSeek": "Company",
    "Mistral": "Company",    "LangChain": "Framework", "HuggingFace": "Platform",
    "Perplexity": "Company", "xAI": "Company",         "Cohere": "Company",
    "Databricks": "Company", "AMD": "Company",          "Intel": "Company",
    "EU AI Act": "Regulation", "RAG": "Technology",    "HBM": "Technology",
    "GPT-4": "Model",        "Gemini": "Model",
}

# EW signal → KG edge type
EW_EDGE_TYPES: dict[str, dict] = {
    "EW_EXPORT_CONTROL":       {"relation": "RESTRICTED_BY",     "weight": 3.0},
    "EW_CAPABILITY_JUMP":      {"relation": "OUTPERFORMS",       "weight": 2.5},
    "EW_STRATEGIC_ALLIANCE":   {"relation": "PARTNERED_WITH",    "weight": 2.5},
    "EW_REGULATORY":           {"relation": "REGULATED_BY",      "weight": 2.0},
    "EW_OPENSOURCE_PARITY":    {"relation": "COMPETES_WITH",     "weight": 2.0},
    "EW_RAG_MIGRATION":        {"relation": "DISRUPTS",          "weight": 1.5},
    "EW_HW_SUPPLY":            {"relation": "SUPPLY_CONSTRAINED","weight": 2.5},
    "EW_AGENT_AUTONOMY":       {"relation": "ENABLES",           "weight": 2.0},
    "EW_REASONING_SHIFT":      {"relation": "EVOLVES_FROM",      "weight": 1.5},
    "EW_CHINA_MODEL_PARITY":   {"relation": "COMPETES_WITH",     "weight": 2.5},
    "EW_CROSS_DOMAIN":         {"relation": "CROSS_IMPACTS",     "weight": 1.5},
    "EW_VELOCITY_SPIKE":       {"relation": "ACCELERATES",       "weight": 1.0},
    "EW_NEGATIVE_SENTIMENT":   {"relation": "RISK_FACTOR",       "weight": 1.0},
    "EW_REGULATORY":           {"relation": "REGULATED_BY",      "weight": 2.0},
    "EW_HW_SUPPLY":            {"relation": "SUPPLY_CONSTRAINED", "weight": 2.5},
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _canonical(name: str) -> str:
    """Return canonical entity name from alias lookup."""
    lower = name.lower().strip()
    for canon, aliases in ENTITY_CANONICAL.items():
        if lower == canon.lower() or lower in aliases:
            return canon
    return name.strip().title()


def _extract_entities_from_text(text: str) -> list[str]:
    """Extract entity mentions from free text."""
    found: list[str] = []
    lower = text.lower()
    for canon, aliases in ENTITY_CANONICAL.items():
        check = [canon.lower()] + aliases
        if any(a in lower for a in check):
            found.append(canon)
    return list(dict.fromkeys(found))  # preserve order, dedup


def _text_body(data: dict) -> str:
    parts = []
    for field in ("summary", "analysis", "key_facts", "recommendations", "insights"):
        val = data.get(field, "")
        if isinstance(val, list):
            parts.extend(str(v) for v in val)
        elif isinstance(val, str):
            parts.append(val)
    return " ".join(parts)


def _relation_confidence(freq: int, sentiment_negative: bool) -> float:
    """Compute confidence score 0.0–1.0 based on frequency and sentiment."""
    base = min(0.4 + freq * 0.1, 0.9)
    if sentiment_negative:
        base = min(base + 0.1, 1.0)  # negative events are more notable
    return round(base, 2)


def _load_intel_files(intel_dir: Path) -> list[dict]:
    files = sorted(intel_dir.glob("*.json"))
    files = [f for f in files if not f.name.startswith("ew_report")]
    results = []
    for jf in files:
        try:
            with open(jf, encoding="utf-8") as f:
                data = json.load(f)
            data["_source_file"] = jf.name
            results.append(data)
        except Exception as e:
            print(f"[KG] Skip {jf.name}: {e}", file=sys.stderr)
    return results


def _load_ew_report(intel_dir: Path) -> dict:
    fp = intel_dir / "ew_report.json"
    if fp.exists():
        try:
            with open(fp, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"ew_triggered": False, "severity": "NONE", "signal_tags": [], "signals": []}


def _node_id(name: str) -> str:
    return "ent:" + re.sub(r"[^a-z0-9]", "_", name.lower()).strip("_")


def _edge_id(src: str, tgt: str, rel: str, week: str) -> str:
    return f"edge:{_node_id(src)}_{rel.lower()}_{_node_id(tgt)}_{week}"


# ── Core Generator ────────────────────────────────────────────────────────────

def generate_delta(
    intel_dir: str,
    current_version: str,
    next_version: str,
    week: str,
    run_date: str,
    ew_signals_str: str,
    output_path: str,
) -> dict:
    intel_path = Path(intel_dir)
    intel_files = _load_intel_files(intel_path)
    ew_report   = _load_ew_report(intel_path)

    ew_signal_tags = ew_signals_str.split(",") if ew_signals_str.strip() else []
    ew_signal_tags += ew_report.get("signal_tags", [])
    ew_signal_tags  = list(dict.fromkeys(t for t in ew_signal_tags if t))

    # ── Build nodes ──────────────────────────────────────────────────────────
    node_freq: dict[str, int]  = {}
    node_sources: dict[str, list[str]] = {}

    for data in intel_files:
        text = _text_body(data)
        entities = _extract_entities_from_text(text)
        src_file = data.get("_source_file", "unknown")
        for ent in entities:
            canon = _canonical(ent)
            node_freq[canon] = node_freq.get(canon, 0) + 1
            node_sources.setdefault(canon, []).append(src_file)

    nodes: list[dict] = []
    for name, freq in node_freq.items():
        nodes.append({
            "@id":          _node_id(name),
            "@type":        ENTITY_TYPES.get(name, "Entity"),
            "name":         name,
            "mention_freq": freq,
            "sources":      list(dict.fromkeys(node_sources[name])),
            "week":         week,
            "added_in":     next_version,
        })
    nodes.sort(key=lambda x: -x["mention_freq"])

    # ── Build edges from co-occurrence ───────────────────────────────────────
    edges: list[dict] = []
    edge_set: set[str] = set()

    for data in intel_files:
        text = _text_body(data)
        entities = _extract_entities_from_text(text)
        src_file = data.get("_source_file", "unknown")
        negative = bool(re.search(
            r"crisis|ban|restrict|shortage|failure|setback", text, re.IGNORECASE
        ))
        for i, e1 in enumerate(entities):
            for e2 in entities[i+1:]:
                c1, c2 = _canonical(e1), _canonical(e2)
                if c1 == c2:
                    continue
                eid = _edge_id(c1, c2, "CO_MENTIONED", week)
                if eid in edge_set:
                    # Bump frequency on existing edge
                    for edge in edges:
                        if edge["@id"] == eid:
                            edge["frequency"] = edge.get("frequency", 1) + 1
                            edge["confidence"] = _relation_confidence(
                                edge["frequency"], negative
                            )
                    continue
                edge_set.add(eid)
                edges.append({
                    "@id":        eid,
                    "@type":      "Relation",
                    "source":     _node_id(c1),
                    "target":     _node_id(c2),
                    "relation":   "CO_MENTIONED",
                    "confidence": _relation_confidence(1, negative),
                    "frequency":  1,
                    "week":       week,
                    "source_file": src_file,
                    "added_in":   next_version,
                })

    # ── EW signal edges ───────────────────────────────────────────────────────
    for sig_tag in ew_signal_tags:
        cfg = EW_EDGE_TYPES.get(sig_tag)
        if not cfg:
            continue
        # Find signals from ew_report to get specific entities
        for sig in ew_report.get("signals", []):
            if sig.get("tag") != sig_tag:
                continue
            # Try to attach to domain-level entities
            domain = sig.get("domain", "")
            domain_entities = _extract_entities_from_text(domain)
            if len(domain_entities) < 2:
                continue
            c1, c2 = _canonical(domain_entities[0]), _canonical(domain_entities[-1])
            if c1 == c2:
                continue
            eid = _edge_id(c1, c2, cfg["relation"], week)
            if eid not in edge_set:
                edge_set.add(eid)
                edges.append({
                    "@id":        eid,
                    "@type":      "EWRelation",
                    "source":     _node_id(c1),
                    "target":     _node_id(c2),
                    "relation":   cfg["relation"],
                    "ew_tag":     sig_tag,
                    "weight":     cfg["weight"],
                    "confidence": min(cfg["weight"] / 3.0, 1.0),
                    "week":       week,
                    "added_in":   next_version,
                })

    # ── Assemble delta ────────────────────────────────────────────────────────
    delta = {
        "@context": {
            "@vocab":     "https://schema.org/",
            "ent":        "https://pe-system.local/entity/",
            "edge":       "https://pe-system.local/relation/",
            "added_in":   "https://pe-system.local/kg/version#",
        },
        "kg_version":      next_version,
        "prev_version":    current_version,
        "week":            week,
        "run_date":        run_date,
        "generated_at":    datetime.utcnow().isoformat() + "Z",
        "ew_triggered":    ew_report.get("ew_triggered", False),
        "ew_severity":     ew_report.get("severity", "NONE"),
        "ew_signal_tags":  ew_signal_tags,
        "node_count":      len(nodes),
        "edge_count":      len(edges),
        "top_entities":    [n["name"] for n in nodes[:10]],
        "nodes":           nodes,
        "edges":           edges,
    }

    # ── Write output ──────────────────────────────────────────────────────────
    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(delta, f, ensure_ascii=False, indent=2)
        print(f"[KG] Delta written: {output_path}")

    # ── Changelog append ──────────────────────────────────────────────────────
    changelog_path = Path(intel_dir).parent.parent / "kg_changelog.md"
    ew_icon = {"CRITICAL": "🔴", "ALERT": "🟠", "WATCH": "🟡", "NONE": "🟢"}.get(
        ew_report.get("severity", "NONE"), "⚪"
    )
    changelog_entry = (
        f"\n## v{next_version} — {run_date} ({week})\n"
        f"- Nodes added: {len(nodes)} | Edges added: {len(edges)}\n"
        f"- EW status: {ew_icon} {ew_report.get('severity', 'NONE')}\n"
        f"- Top entities: {', '.join(n['name'] for n in nodes[:5])}\n"
        f"- EW signals: {', '.join(ew_signal_tags) or 'none'}\n"
    )
    try:
        with open(changelog_path, "a", encoding="utf-8") as f:
            f.write(changelog_entry)
        print(f"[KG] Changelog updated: {changelog_path}")
    except Exception as e:
        print(f"[KG] Changelog write failed: {e}", file=sys.stderr)

    return delta


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="KG Delta Generator v3")
    p.add_argument("--intel-dir",       default="output/ai_intel",        help="Directory with intel JSON files")
    p.add_argument("--current-version", required=True,                     help="Current KG version e.g. 4.25")
    p.add_argument("--next-version",    required=True,                     help="Next KG version e.g. 4.26")
    p.add_argument("--week",            required=True,                     help="ISO week e.g. 2026-W21")
    p.add_argument("--run-date",        default=datetime.utcnow().strftime("%Y-%m-%d"), help="Run date YYYY-MM-DD")
    p.add_argument("--ew-signals",      default="",                        help="Comma-separated EW signal tags")
    p.add_argument("--output",          default="",                        help="Output JSON path")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    out = args.output or f"knowledge_graph_v{args.next_version}_delta.json"

    print(f"[KG v3] Generating delta: v{args.current_version} → v{args.next_version}")
    print(f"[KG]    Week: {args.week} | Intel dir: {args.intel_dir}")

    delta = generate_delta(
        intel_dir=args.intel_dir,
        current_version=args.current_version,
        next_version=args.next_version,
        week=args.week,
        run_date=args.run_date,
        ew_signals_str=args.ew_signals,
        output_path=out,
    )

    print(f"[KG] Nodes     : {delta['node_count']}")
    print(f"[KG] Edges     : {delta['edge_count']}")
    print(f"[KG] Top 5     : {', '.join(delta['top_entities'][:5])}")
    print(f"[KG] EW Status : {delta['ew_severity']}")

    gh_output = os.environ.get("GITHUB_OUTPUT", "")
    if gh_output:
        with open(gh_output, "a") as f:
            f.write(f"kg_version={args.next_version}\n")
            f.write(f"node_count={delta['node_count']}\n")
            f.write(f"edge_count={delta['edge_count']}\n")

    # GITHUB_STEP_SUMMARY
    step_summary = os.environ.get("GITHUB_STEP_SUMMARY", "")
    if step_summary:
        top_ents = ", ".join(f"`{n}`" for n in delta["top_entities"][:8])
        lines = [
            f"## 🧠 KG Delta v{args.next_version} — {args.week}",
            f"| Field | Value |",
            f"|---|---|",
            f"| Nodes | {delta['node_count']} |",
            f"| Edges | {delta['edge_count']} |",
            f"| EW Severity | {delta['ew_severity']} |",
            f"",
            f"**Top Entities:** {top_ents}",
        ]
        try:
            with open(step_summary, "a") as f:
                f.write("\n".join(lines) + "\n")
        except Exception:
            pass


if __name__ == "__main__":
    main()
