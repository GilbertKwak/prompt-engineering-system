#!/usr/bin/env python3
"""
kg_delta_generator.py
─────────────────────
AI Intel + EW 시그널 → knowledge_graph_vX.XX_delta.json 자동 생성기
워크플로: ai-intel-weekly.yml → STAGE 3

사용법:
  python automation/kg_delta_generator.py \
    --intel-dir output/ai_intel \
    --current-version 4.25 \
    --next-version 4.26 \
    --week 2026-W21 \
    --run-date 2026-05-19 \
    --ew-signals EW-RAG-OSS,EW-MODEL-FLOOD \
    --output knowledge_graph_v4.26_delta.json
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


# ─────────────────────────────────────────
# 노드 타입 정의 (KG 스키마)
# ─────────────────────────────────────────
NODE_TYPE_MAP = {
    "enterprise_deployment": "ENTERPRISE_INTEL",
    "frameworks_rag":        "FRAMEWORK_NODE",
    "model_releases":        "MODEL_NODE",
    "infra_market":          "MARKET_INTEL",
    "semiconductor_chips":   "CHIP_NODE",
}

EDGE_TYPE_MAP = {
    ("ENTERPRISE_INTEL", "FRAMEWORK_NODE"): "DEPLOYS_WITH",
    ("ENTERPRISE_INTEL", "MODEL_NODE"):     "USES_MODEL",
    ("MODEL_NODE",       "CHIP_NODE"):      "RUNS_ON",
    ("FRAMEWORK_NODE",   "MODEL_NODE"):     "INTEGRATES",
    ("MARKET_INTEL",     "CHIP_NODE"):      "DRIVEN_BY",
    ("MARKET_INTEL",     "ENTERPRISE_INTEL"): "REFLECTS",
}

EW_SIGNAL_TO_EDGE = {
    "EW-AI-DEPLOY":   ("ENTERPRISE_INTEL", "ENTERPRISE_INTEL", "EW_SIGNAL_DEPLOY"),
    "EW-RAG-OSS":     ("ENTERPRISE_INTEL", "FRAMEWORK_NODE",   "EW_RAG_MIGRATION"),
    "EW-MODEL-FLOOD": ("MODEL_NODE",       "MARKET_INTEL",     "EW_MODEL_PROLIFERATION"),
    "EW-CONSULT":     ("ENTERPRISE_INTEL", "MARKET_INTEL",     "EW_CONSULT_DISRUPTION"),
    "EW-INFRA":       ("MARKET_INTEL",     "CHIP_NODE",        "EW_INFRA_GAP"),
    "EW-ORCH":        ("FRAMEWORK_NODE",   "MODEL_NODE",       "EW_ORCH_SURGE"),
}


# ─────────────────────────────────────────
# 인텔 데이터 로드
# ─────────────────────────────────────────
def load_intel(intel_dir: str) -> dict[str, dict]:
    """intel_*.json 파일 전체 로드"""
    data = {}
    for f in Path(intel_dir).glob("intel_*.json"):
        key = f.stem.replace("intel_", "")
        try:
            with open(f, encoding="utf-8") as fp:
                data[key] = json.load(fp)
        except Exception as e:
            print(f"[WARN] Skip {f.name}: {e}", file=sys.stderr)
    return data


# ─────────────────────────────────────────
# 노드 생성
# ─────────────────────────────────────────
def build_nodes(
    intel_data: dict[str, dict],
    week: str,
    run_date: str,
) -> list[dict]:
    """도메인 인텔 데이터 → KG 노드 목록 생성"""
    nodes = []
    node_id_counter = 1

    for domain, data in intel_data.items():
        node_type = NODE_TYPE_MAP.get(domain, "GENERIC_NODE")
        summary = data.get("summary", "")[:300]
        key_facts = data.get("key_facts", [])[:5]
        metrics = data.get("metrics", {})
        signals = data.get("signals", [])[:5]

        node = {
            "id": f"N{node_id_counter:03d}_{domain[:12].upper()}",
            "type": node_type,
            "domain": domain,
            "week": week,
            "created_at": run_date,
            "properties": {
                "summary": summary,
                "key_facts": key_facts,
                "metrics": metrics,
                "raw_signals": signals,
                "source_count": len(data.get("sources", [])),
                "query_count": data.get("query_count", 0),
            },
            "confidence": _calc_confidence(data),
        }
        nodes.append(node)
        node_id_counter += 1

        # 핵심 팩트에서 개별 엔티티 노드 추출 (기업명, 모델명, 수치)
        entity_nodes = _extract_entity_nodes(key_facts, domain, node_type, week, run_date, node_id_counter)
        nodes.extend(entity_nodes)
        node_id_counter += len(entity_nodes)

    return nodes


def _extract_entity_nodes(
    facts: list[str],
    domain: str,
    parent_type: str,
    week: str,
    run_date: str,
    start_id: int,
) -> list[dict]:
    """key_facts 텍스트에서 기업/모델/수치 엔티티 추출 후 노드화"""
    entity_nodes = []
    known_entities = {
        "COMPANY":   ["nvidia", "amd", "intel", "openai", "anthropic", "google", "microsoft",
                      "meta", "mistral", "cohere", "sambanova", "groq"],
        "FRAMEWORK": ["langchain", "langgraph", "llamaindex", "ragas", "galileo",
                      "autogen", "crewai", "dspy", "haystack"],
        "MODEL":     ["gpt-4", "gpt-5", "claude", "gemini", "llama", "mistral",
                      "grok", "qwen", "deepseek"],
        "CHIP":      ["h100", "h200", "b200", "mi300", "hbm3", "hbm3e", "b300"],
    }

    found = set()
    for fact in facts:
        fact_lower = fact.lower()
        for etype, names in known_entities.items():
            for name in names:
                if name in fact_lower and name not in found:
                    found.add(name)
                    entity_nodes.append({
                        "id": f"E{start_id + len(entity_nodes):03d}_{name[:8].upper()}",
                        "type": f"ENTITY_{etype}",
                        "domain": domain,
                        "week": week,
                        "created_at": run_date,
                        "properties": {
                            "name": name,
                            "extracted_from": fact[:150],
                            "entity_type": etype,
                        },
                        "confidence": 0.7,
                    })
                    if len(entity_nodes) >= 8:  # 도메인당 최대 8개
                        return entity_nodes
    return entity_nodes


def _calc_confidence(data: dict) -> float:
    """인텔 데이터 품질 기반 신뢰도 스코어 계산 (0.0~1.0)"""
    score = 0.5
    if data.get("key_facts"):    score += 0.1 * min(len(data["key_facts"]) / 5, 1.0)
    if data.get("metrics"):      score += 0.15 * min(len(data["metrics"]) / 3, 1.0)
    if data.get("sources"):      score += 0.1 * min(len(data["sources"]) / 3, 1.0)
    if data.get("query_count",0) >= 3: score += 0.1
    if data.get("summary") and len(data["summary"]) > 100: score += 0.05
    return round(min(score, 1.0), 2)


# ─────────────────────────────────────────
# 엣지 생성
# ─────────────────────────────────────────
def build_edges(
    nodes: list[dict],
    ew_signals: list[str],
    week: str,
) -> list[dict]:
    """노드 간 관계 엣지 + EW 시그널 엣지 생성"""
    edges = []
    edge_id_counter = 1

    # 노드 타입 인덱스 구성
    type_to_nodes: dict[str, list[dict]] = {}
    for node in nodes:
        t = node["type"]
        if t not in type_to_nodes:
            type_to_nodes[t] = []
        type_to_nodes[t].append(node)

    # 표준 관계 엣지 생성
    for (src_type, tgt_type), rel in EDGE_TYPE_MAP.items():
        src_nodes = type_to_nodes.get(src_type, [])
        tgt_nodes = type_to_nodes.get(tgt_type, [])
        if src_nodes and tgt_nodes:
            # 첫 번째 노드끼리만 연결 (과도한 엣지 방지)
            edge = {
                "id": f"R{edge_id_counter:03d}_{rel[:10]}",
                "source": src_nodes[0]["id"],
                "target": tgt_nodes[0]["id"],
                "relation": rel,
                "week": week,
                "weight": 0.8,
                "ew_driven": False,
            }
            edges.append(edge)
            edge_id_counter += 1

    # EW 시그널 기반 특수 엣지 생성
    for signal_id in ew_signals:
        signal_id = signal_id.strip()
        if signal_id in EW_SIGNAL_TO_EDGE:
            src_type, tgt_type, rel = EW_SIGNAL_TO_EDGE[signal_id]
            src_nodes = type_to_nodes.get(src_type, [])
            tgt_nodes = type_to_nodes.get(tgt_type, [])
            if src_nodes and tgt_nodes:
                edge = {
                    "id": f"EW{edge_id_counter:03d}_{signal_id}",
                    "source": src_nodes[0]["id"],
                    "target": tgt_nodes[0]["id"],
                    "relation": rel,
                    "week": week,
                    "weight": 1.0,  # EW 엣지는 최고 가중치
                    "ew_driven": True,
                    "ew_signal": signal_id,
                }
                edges.append(edge)
                edge_id_counter += 1

    return edges


# ─────────────────────────────────────────
# Delta 메타데이터 및 요약
# ─────────────────────────────────────────
def build_delta_metadata(
    current_version: str,
    next_version: str,
    week: str,
    run_date: str,
    nodes: list[dict],
    edges: list[dict],
    ew_signals: list[str],
) -> dict:
    """KG Delta 전체 메타데이터 구성"""
    node_type_counts = {}
    for n in nodes:
        t = n["type"]
        node_type_counts[t] = node_type_counts.get(t, 0) + 1

    avg_confidence = sum(n.get("confidence", 0) for n in nodes) / max(len(nodes), 1)
    ew_edge_count = sum(1 for e in edges if e.get("ew_driven"))

    return {
        "version": f"v{next_version}",
        "base_version": f"v{current_version}",
        "week": week,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "run_date": run_date,
        "delta_type": "weekly_intel_update",
        "stats": {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "ew_edges": ew_edge_count,
            "node_type_distribution": node_type_counts,
            "avg_node_confidence": round(avg_confidence, 3),
            "ew_signals_embedded": ew_signals,
        },
        "schema_version": "2.0",
        "pipeline": "ai-intel-weekly",
    }


# ─────────────────────────────────────────
# CLI
# ─────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Knowledge Graph Delta Generator")
    p.add_argument("--intel-dir",       required=True)
    p.add_argument("--current-version", required=True)
    p.add_argument("--next-version",    required=True)
    p.add_argument("--week",            required=True)
    p.add_argument("--run-date",        required=True)
    p.add_argument("--ew-signals",      default="", help="Comma-separated EW signal IDs")
    p.add_argument("--output",          required=True)
    return p.parse_args()


def main():
    args = parse_args()

    ew_signals = [s.strip() for s in args.ew_signals.split(",") if s.strip()]
    print(f"[INFO] Generating KG Delta: v{args.current_version} → v{args.next_version}", file=sys.stderr)
    print(f"[INFO] Week: {args.week} | EW Signals: {ew_signals}", file=sys.stderr)

    # 인텔 데이터 로드
    intel_data = load_intel(args.intel_dir)
    if not intel_data:
        print("[WARN] No intel data found. Generating minimal delta.", file=sys.stderr)
        intel_data = {}

    # 노드 & 엣지 생성
    nodes = build_nodes(intel_data, args.week, args.run_date)
    edges = build_edges(nodes, ew_signals, args.week)
    metadata = build_delta_metadata(
        args.current_version,
        args.next_version,
        args.week,
        args.run_date,
        nodes,
        edges,
        ew_signals,
    )

    # Delta JSON 구성
    delta = {
        "metadata": metadata,
        "nodes": nodes,
        "edges": edges,
    }

    # 저장
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(delta, f, ensure_ascii=False, indent=2)

    print(f"[OK] KG Delta saved → {output_path}", file=sys.stderr)
    print(f"     Nodes: {len(nodes)} | Edges: {len(edges)} | EW edges: {metadata['stats']['ew_edges']}", file=sys.stderr)


if __name__ == "__main__":
    main()
