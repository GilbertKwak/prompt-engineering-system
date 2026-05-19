#!/usr/bin/env python3
"""
kg_delta_generator.py  — Section A · Step 3
수집된 인텔에서 Knowledge Graph 델타(노드/엣지) 생성

Usage:
  python automation/kg_delta_generator.py \
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
from datetime import datetime
from pathlib import Path

# ─── 엔티티 추출 규칙 ──────────────────────────────────────────────────────────
# 주요 AI 엔티티 사전 (이름 → 카테고리)
ENTITY_DICT = {
    # 기업
    "OpenAI": "company", "Anthropic": "company", "Google": "company",
    "Microsoft": "company", "Meta": "company", "NVIDIA": "company",
    "AMD": "company", "Intel": "company", "AWS": "company",
    "Hugging Face": "company", "Mistral": "company", "Cohere": "company",
    "DeepMind": "company", "xAI": "company", "Perplexity": "company",
    # 모델
    "GPT-4": "model", "GPT-4o": "model", "Claude": "model",
    "Gemini": "model", "LLaMA": "model", "Mistral": "model",
    "Grok": "model", "Phi": "model", "Qwen": "model",
    # 기술/개념
    "RAG": "technology", "LangChain": "technology", "LlamaIndex": "technology",
    "RLHF": "technology", "LoRA": "technology", "QLoRA": "technology",
    "MoE": "technology", "Chain-of-Thought": "technology",
    # 인프라
    "H100": "hardware", "A100": "hardware", "B200": "hardware",
    "TPU": "hardware", "HBM3": "hardware",
    # 규제
    "EU AI Act": "regulation", "NIST": "regulation",
    "Executive Order": "regulation", "GDPR": "regulation",
}

# 도메인 → 관계 유형 매핑
DOMAIN_EDGE_TYPES = {
    "enterprise_deployment": "DEPLOYED_IN",
    "model_performance": "BENCHMARKED_AGAINST",
    "infrastructure": "POWERS",
    "regulatory": "REGULATED_BY",
    "open_source": "OPEN_SOURCED_BY",
    "investment": "INVESTED_IN",
}

# EW 신호 → 특수 엣지 타입
EW_EDGE_TYPES = {
    "EW_GPU_SHORTAGE": "SUPPLY_CONSTRAINED_BY",
    "EW_REGULATORY_SURGE": "URGENTLY_REGULATED_BY",
    "EW_INVESTMENT_SPIKE": "SURGE_FUNDED_BY",
    "EW_SECURITY_BREACH": "SECURITY_RISK_FROM",
    "EW_RAG_MIGRATION": "MIGRATING_TO",
    "EW_GEOPOLITICAL": "GEOPOLITICALLY_IMPACTED_BY",
    "EW_LEADERSHIP_CHANGE": "LEADERSHIP_CHANGE_AT",
}


# ─── 파싱 유틸리티 ─────────────────────────────────────────────────────────────
def parse_ew_signals(raw: str) -> list[str]:
    """EW 신호 문자열을 리스트로 안전하게 파싱
    
    FIX: 빈 문자열, None, 공백 문자열 모두 안전 처리
    """
    if not raw or not raw.strip():
        return []
    # 쉼표 또는 세미콜론 구분자 지원
    signals = re.split(r"[,;]+", raw)
    return [s.strip() for s in signals if s.strip()]


def extract_entities_from_text(text: str) -> list[tuple[str, str]]:
    """텍스트에서 알려진 엔티티 추출 → [(name, category), ...]"""
    found = []
    for entity, category in ENTITY_DICT.items():
        if entity in text:
            found.append((entity, category))
    return found


def make_node_id(name: str, category: str, version: str) -> str:
    safe_name = re.sub(r"[^a-zA-Z0-9]", "_", name)
    return f"{category}_{safe_name}_v{version.replace('.', '_')}"


def make_edge_id(src: str, rel: str, tgt: str) -> str:
    return f"{src}__{rel}__{tgt}"


# ─── 델타 생성 핵심 로직 ───────────────────────────────────────────────────────
def generate_nodes_from_intel(intel: dict, version: str) -> list[dict]:
    """인텔 파일에서 KG 노드 생성"""
    nodes = []
    domain = intel.get("domain", "unknown")
    week = intel.get("week", "")

    # key_facts에서 엔티티 추출
    all_text = " ".join(
        intel.get("key_facts", []) +
        intel.get("emerging_signals", []) +
        [intel.get("summary", "")]
    )

    for entity_name, category in extract_entities_from_text(all_text):
        node_id = make_node_id(entity_name, category, version)
        nodes.append({
            "id": node_id,
            "label": entity_name,
            "category": category,
            "source_domain": domain,
            "source_week": week,
            "kg_version": version,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "properties": {
                "confidence": intel.get("confidence", 0.0),
                "mentions": all_text.count(entity_name),
            },
        })

    # 도메인 자체도 노드로 추가
    domain_node_id = make_node_id(domain, "domain", version)
    nodes.append({
        "id": domain_node_id,
        "label": domain,
        "category": "domain",
        "source_domain": domain,
        "source_week": week,
        "kg_version": version,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "properties": {"confidence": intel.get("confidence", 0.0)},
    })

    return nodes


def generate_edges_from_intel(intel: dict, nodes: list[dict], version: str) -> list[dict]:
    """인텔 파일에서 KG 엣지 생성"""
    edges = []
    domain = intel.get("domain", "unknown")
    rel_type = DOMAIN_EDGE_TYPES.get(domain, "RELATED_TO")
    week = intel.get("week", "")

    # 도메인 노드 ID
    domain_node_id = make_node_id(domain, "domain", version)

    # 각 엔티티 노드를 도메인 노드와 연결
    for node in nodes:
        if node["category"] == "domain":
            continue
        edge_id = make_edge_id(node["id"], rel_type, domain_node_id)
        edges.append({
            "id": edge_id,
            "source": node["id"],
            "target": domain_node_id,
            "relation": rel_type,
            "source_week": week,
            "kg_version": version,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "properties": {"confidence": intel.get("confidence", 0.0)},
        })

    return edges


def generate_ew_edges(ew_signals: list[str], version: str, week: str) -> list[dict]:
    """EW 신호에 따른 특수 엣지 생성"""
    edges = []
    for signal in ew_signals:
        rel_type = EW_EDGE_TYPES.get(signal, "EW_FLAGGED")
        edge_id = make_edge_id(f"ew_{signal}", rel_type, f"ew_system_v{version.replace('.','_')}")
        edges.append({
            "id": edge_id,
            "source": f"ew_signal_{signal}",
            "target": f"ew_system",
            "relation": rel_type,
            "ew_signal": signal,
            "source_week": week,
            "kg_version": version,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "properties": {"triggered": True},
        })
    return edges


# ─── CLI 진입점 ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="AI 인텔에서 KG 델타 생성")
    parser.add_argument("--intel-dir", required=True)
    parser.add_argument("--current-version", required=True)
    parser.add_argument("--next-version", required=True)
    parser.add_argument("--week", required=True)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--ew-signals", default="",
                        help="EW 신호 목록 (쉼표 구분, 없으면 빈 문자열)")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    intel_dir = Path(args.intel_dir)
    if not intel_dir.exists():
        print(f"[ERROR] 인텔 디렉토리 없음: {intel_dir}", file=sys.stderr)
        sys.exit(1)

    # FIX: ew_signals 안전 파싱
    ew_signals = parse_ew_signals(args.ew_signals)

    intel_files = list(intel_dir.glob("intel_*.json"))
    all_nodes = []
    all_edges = []

    for f in intel_files:
        try:
            intel = json.loads(f.read_text())
        except Exception as e:
            print(f"[WARN] 파일 읽기 실패 {f}: {e}", file=sys.stderr)
            continue

        nodes = generate_nodes_from_intel(intel, args.next_version)
        edges = generate_edges_from_intel(intel, nodes, args.next_version)
        all_nodes.extend(nodes)
        all_edges.extend(edges)

    # EW 특수 엣지 추가
    if ew_signals:
        ew_edges = generate_ew_edges(ew_signals, args.next_version, args.week)
        all_edges.extend(ew_edges)
        print(f"[INFO] EW 엣지 {len(ew_edges)}개 추가: {ew_signals}")

    # 중복 노드/엣지 제거 (id 기준)
    unique_nodes = {n["id"]: n for n in all_nodes}
    unique_edges = {e["id"]: e for e in all_edges}

    delta = {
        "version_from": args.current_version,
        "version_to": args.next_version,
        "week": args.week,
        "run_date": args.run_date,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "node_count": len(unique_nodes),
        "edge_count": len(unique_edges),
        "ew_signals_processed": ew_signals,
        "nodes": list(unique_nodes.values()),
        "edges": list(unique_edges.values()),
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(delta, ensure_ascii=False, indent=2))

    print(f"[OK] KG 델타 생성 완료 → {output_path}")
    print(f"     노드: {delta['node_count']} | 엣지: {delta['edge_count']}")
    print(f"     버전: {args.current_version} → {args.next_version}")


if __name__ == "__main__":
    main()
