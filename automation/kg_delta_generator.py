#!/usr/bin/env python3
"""
automation/kg_delta_generator.py
Knowledge Graph Delta 자동 생성기

Usage (workflow에서 호출되는 방식 — 정확한 인터페이스):
  python automation/kg_delta_generator.py \
    --intel-dir output/ai_intel \
    --current-version 4.25 \
    --next-version 4.26 \
    --week 2026-W21 \
    --run-date 2026-05-19 \
    --ew-signals EW-RAG-OSS,EW-ORCH \
    --output knowledge_graph_v4.26_delta.json
"""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

# ──────────────────────────────────────────
# Entity 인식 키워드 맵 (21개 주요 엔티티)
# ──────────────────────────────────────────
ENTITY_KEYWORDS = {
    "NVIDIA": ["nvidia", "h100", "h200", "gb200", "blackwell", "cuda"],
    "AMD": ["amd", "instinct", "mi300", "rocm"],
    "Intel": ["intel", "gaudi", "habana"],
    "OpenAI": ["openai", "gpt-4", "gpt-5", "chatgpt", "o1", "o3"],
    "Anthropic": ["anthropic", "claude"],
    "Google": ["google", "gemini", "deepmind", "gemma"],
    "Meta": ["meta", "llama", "llama-3"],
    "Mistral": ["mistral"],
    "LangChain": ["langchain", "langgraph"],
    "LlamaIndex": ["llamaindex", "llama_index", "llama index"],
    "AWS": ["aws", "amazon", "bedrock", "sagemaker"],
    "Azure": ["azure", "microsoft", "copilot"],
    "GCP": ["gcp", "google cloud", "vertex ai"],
    "HBM": ["hbm", "hbm3", "hbm4", "high bandwidth memory"],
    "RAG": ["rag", "retrieval augmented", "vector store", "pgvector"],
    "MCP": ["mcp", "model context protocol"],
    "TSMC": ["tsmc", "taiwan semiconductor"],
    "Samsung": ["samsung", "samsung semiconductor"],
    "SK Hynix": ["sk hynix", "hynix"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Docker": ["docker", "container"],
}

# EW 신호별 전용 엣지 타입
EW_EDGE_TYPES = {
    "EW-AI-DEPLOY": "DEPLOYMENT_BARRIER",
    "EW-RAG-OSS": "EW_RAG_MIGRATION",
    "EW-MODEL-FLOOD": "MODEL_PROLIFERATION",
    "EW-CONSULT": "MARKET_DISRUPTION",
    "EW-INFRA": "INFRA_GAP",
    "EW-ORCH": "ORCHESTRATION_ADOPTION",
}


def load_intel_files(intel_dir: str) -> list[dict]:
    """intel_*.json 및 ew_report.json 로드"""
    dir_path = Path(intel_dir)
    results = []
    for f in sorted(dir_path.glob("intel_*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            results.append(data)
        except Exception as e:
            print(f"  [WARN] {f.name} 로드 실패: {e}")
    return results


def extract_entities_from_facts(key_facts: list[str]) -> list[str]:
    """key_facts 텍스트에서 엔티티 키워드 매칭으로 추출"""
    found = set()
    combined = " ".join(key_facts).lower()
    for entity, keywords in ENTITY_KEYWORDS.items():
        if any(kw in combined for kw in keywords):
            found.add(entity)
    return sorted(found)


def build_nodes(intel_list: list[dict], week: str, run_date: str) -> list[dict]:
    """인텔 데이터에서 KG 노드 생성"""
    nodes = []
    seen_entities = set()

    # 도메인 노드
    for intel in intel_list:
        domain = intel.get("domain", "unknown")
        domain_node_id = f"domain:{domain}:{week}"
        nodes.append({
            "id": domain_node_id,
            "type": "DOMAIN_INTEL",
            "label": f"{domain} ({week})",
            "domain": domain,
            "week": week,
            "model": intel.get("model"),
            "metrics": intel.get("metrics", {}),
            "key_facts_count": len(intel.get("key_facts", [])),
            "collected_at": intel.get("collected_at"),
            "created_at": run_date,
        })

        # 엔티티 노드
        entities = extract_entities_from_facts(intel.get("key_facts", []))
        for entity in entities:
            if entity not in seen_entities:
                seen_entities.add(entity)
                nodes.append({
                    "id": f"entity:{entity.lower().replace(' ', '_')}",
                    "type": "ENTITY",
                    "label": entity,
                    "category": _classify_entity(entity),
                    "first_seen_week": week,
                    "created_at": run_date,
                })

    return nodes


def _classify_entity(entity: str) -> str:
    """엔티티 카테고리 분류"""
    chip_makers = {"NVIDIA", "AMD", "Intel", "TSMC", "Samsung", "SK Hynix", "HBM"}
    ai_labs = {"OpenAI", "Anthropic", "Google", "Meta", "Mistral"}
    frameworks = {"LangChain", "LlamaIndex", "RAG", "MCP", "Kubernetes", "Docker"}
    cloud = {"AWS", "Azure", "GCP"}

    if entity in chip_makers:
        return "SEMICONDUCTOR"
    elif entity in ai_labs:
        return "AI_LAB"
    elif entity in frameworks:
        return "FRAMEWORK"
    elif entity in cloud:
        return "CLOUD"
    return "OTHER"


def build_edges(
    intel_list: list[dict],
    nodes: list[dict],
    ew_signals: list[str],
    week: str,
    run_date: str,
) -> list[dict]:
    """노드 간 관계 엣지 생성"""
    edges = []
    domain_node_ids = [
        n["id"] for n in nodes if n["type"] == "DOMAIN_INTEL"
    ]
    entity_node_ids = {
        n["label"]: n["id"] for n in nodes if n["type"] == "ENTITY"
    }

    # 도메인 → 엔티티 엣지
    for intel in intel_list:
        domain = intel.get("domain", "unknown")
        domain_node_id = f"domain:{domain}:{week}"
        entities = extract_entities_from_facts(intel.get("key_facts", []))

        for entity in entities:
            if entity in entity_node_ids:
                edges.append({
                    "id": f"edge:{domain}:{entity.lower()}:{week}",
                    "type": "MENTIONED_IN",
                    "source": domain_node_id,
                    "target": entity_node_ids[entity],
                    "week": week,
                    "created_at": run_date,
                })

    # EW 신호 엣지
    for signal in ew_signals:
        if signal and signal in EW_EDGE_TYPES:
            edge_type = EW_EDGE_TYPES[signal]
            edges.append({
                "id": f"edge:ew:{signal.lower()}:{week}",
                "type": edge_type,
                "source": f"ew_signal:{signal}",
                "target": "c31_ew_registry",
                "ew_signal": signal,
                "week": week,
                "created_at": run_date,
            })

    return edges


def generate_delta(
    intel_list: list[dict],
    current_version: str,
    next_version: str,
    week: str,
    run_date: str,
    ew_signals: list[str],
) -> dict:
    """KG Delta JSON 생성 메인 로직"""
    print(f"\n[INFO] KG Delta 생성: v{current_version} → v{next_version}")
    print(f"[INFO] EW 신호: {ew_signals if ew_signals else '없음'}")

    nodes = build_nodes(intel_list, week, run_date)
    edges = build_edges(intel_list, nodes, ew_signals, week, run_date)

    # 메트릭 요약
    all_metrics = {}
    for intel in intel_list:
        all_metrics.update(intel.get("metrics", {}))

    delta = {
        "version": next_version,
        "previous_version": current_version,
        "week": week,
        "run_date": run_date,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "ew_signals_active": ew_signals,
        "summary": {
            "new_nodes": len(nodes),
            "new_edges": len(edges),
            "domains_processed": len(intel_list),
            "metrics_captured": len(all_metrics),
        },
        "nodes": nodes,
        "edges": edges,
        "metrics_snapshot": all_metrics,
    }

    print(f"[OK] Delta 생성: nodes={len(nodes)}, edges={len(edges)}")
    return delta


def main():
    parser = argparse.ArgumentParser(description="KG Delta Generator — AI Intel 기반")
    parser.add_argument("--intel-dir", required=True, help="intel_*.json 디렉토리")
    parser.add_argument("--current-version", required=True, help="현재 KG 버전 (예: 4.25)")
    parser.add_argument("--next-version", required=True, help="신규 Delta 버전 (예: 4.26)")
    parser.add_argument("--week", required=True, help="주간 레이블 (예: 2026-W21)")
    parser.add_argument("--run-date", required=True, help="실행 날짜 (YYYY-MM-DD)")
    parser.add_argument(
        "--ew-signals",
        default="",
        help="활성 EW 신호 목록 (콤마 구분, 예: EW-RAG-OSS,EW-ORCH)",
    )
    parser.add_argument("--output", required=True, help="출력 JSON 파일 경로")
    args = parser.parse_args()

    ew_signals = [
        s.strip() for s in args.ew_signals.split(",") if s.strip()
    ]

    intel_list = load_intel_files(args.intel_dir)
    if not intel_list:
        print("[WARN] 인텔 데이터 없음. 빈 Delta 생성.")
        intel_list = []

    delta = generate_delta(
        intel_list=intel_list,
        current_version=args.current_version,
        next_version=args.next_version,
        week=args.week,
        run_date=args.run_date,
        ew_signals=ew_signals,
    )

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(delta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[SAVED] {out_path}")


if __name__ == "__main__":
    main()
