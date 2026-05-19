#!/usr/bin/env python3
"""
kg_delta_generator.py — Knowledge Graph Delta Generator

수집된 AI 인텔로부터 지식 그래프 노드/엣지 델타를 자동 생성합니다.
- key_facts에서 엔티티 추출 (21개 주요 키워드 매핑)
- EW 시그널별 전용 엣지 타입 삽입
- 버전 메타데이터 포함 JSON 출력
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# ──────────────────────────────────────────
# 엔티티 추출 매핑 (키워드 → 노드 타입)
# ──────────────────────────────────────────
ENTITY_MAP = {
    # LLM / 모델
    "gpt-4": "MODEL", "gpt-5": "MODEL", "gpt4": "MODEL",
    "claude": "MODEL", "gemini": "MODEL", "llama": "MODEL",
    "mistral": "MODEL", "qwen": "MODEL", "deepseek": "MODEL",
    "phi-": "MODEL", "falcon": "MODEL",
    # 기업
    "openai": "COMPANY", "anthropic": "COMPANY", "google": "COMPANY",
    "microsoft": "COMPANY", "meta": "COMPANY", "nvidia": "COMPANY",
    "amazon": "COMPANY", "aws": "COMPANY", "azure": "COMPANY",
    "hugging face": "COMPANY", "mistralai": "COMPANY",
    "cohere": "COMPANY", "databricks": "COMPANY", "snowflake": "COMPANY",
    # 프레임워크 / 도구
    "langchain": "FRAMEWORK", "langraph": "FRAMEWORK",
    "llamaindex": "FRAMEWORK", "dspy": "FRAMEWORK",
    "autogen": "FRAMEWORK", "crewai": "FRAMEWORK",
    "semantic kernel": "FRAMEWORK", "haystack": "FRAMEWORK",
    "vllm": "FRAMEWORK", "triton": "FRAMEWORK",
    # 기술 개념
    "rag": "CONCEPT", "retrieval augmented": "CONCEPT",
    "agentic": "CONCEPT", "multi-agent": "CONCEPT",
    "fine-tuning": "CONCEPT", "finetune": "CONCEPT",
    "inference": "CONCEPT", "embedding": "CONCEPT",
    "context window": "CONCEPT", "mixture of experts": "CONCEPT",
    "moe": "CONCEPT", "quantization": "CONCEPT",
    # 하드웨어
    "h100": "HARDWARE", "h200": "HARDWARE", "b200": "HARDWARE",
    "a100": "HARDWARE", "tpu": "HARDWARE", "hbm": "HARDWARE",
    "gb200": "HARDWARE", "blackwell": "HARDWARE", "hopper": "HARDWARE",
}

# EW 시그널 → 엣지 타입 매핑
EW_EDGE_MAP = {
    "rag": "EW_RAG_MIGRATION",
    "agentic": "EW_AGENTIC_SHIFT",
    "nvidia": "EW_NVIDIA_DOMINANCE",
    "langchain": "EW_FRAMEWORK_ADOPTION",
    "claude": "EW_CLAUDE_SURGE",
    "openai": "EW_OPENAI_MOVE",
    "inference": "EW_INFERENCE_COST_DROP",
    "multi-agent": "EW_MULTI_AGENT_RISE",
    "default": "EW_GENERAL_SIGNAL",
}


def extract_entities_from_text(text: str) -> list[dict]:
    """텍스트에서 엔티티 추출."""
    text_lower = text.lower()
    found = {}
    for keyword, node_type in ENTITY_MAP.items():
        if keyword in text_lower:
            canonical = keyword.replace("-", "_").replace(" ", "_").upper()
            if canonical not in found:
                found[canonical] = {
                    "id": canonical,
                    "label": keyword.title(),
                    "type": node_type,
                    "source_mention": keyword,
                }
    return list(found.values())


def extract_entities_from_intel(intel_data: dict) -> list[dict]:
    """인텔 데이터 전체에서 엔티티 추출."""
    text_parts = []
    for field in ["key_facts", "summary", "analysis", "content", "title",
                  "headline", "description", "raw_text"]:
        val = intel_data.get(field, "")
        if isinstance(val, list):
            text_parts.extend([str(v) for v in val])
        elif isinstance(val, str):
            text_parts.append(val)
    return extract_entities_from_text(" ".join(text_parts))


def generate_edges_from_entities(entities: list[dict], domain: str) -> list[dict]:
    """엔티티 간 기본 관계 엣지 생성."""
    edges = []
    models = [e for e in entities if e["type"] == "MODEL"]
    companies = [e for e in entities if e["type"] == "COMPANY"]
    frameworks = [e for e in entities if e["type"] == "FRAMEWORK"]
    concepts = [e for e in entities if e["type"] == "CONCEPT"]
    hardware = [e for e in entities if e["type"] == "HARDWARE"]

    # MODEL ← COMPANY
    for model in models:
        for company in companies:
            edges.append({
                "source": company["id"],
                "target": model["id"],
                "relation": "DEVELOPS",
                "domain": domain,
            })

    # FRAMEWORK → CONCEPT
    for fw in frameworks:
        for concept in concepts:
            edges.append({
                "source": fw["id"],
                "target": concept["id"],
                "relation": "IMPLEMENTS",
                "domain": domain,
            })

    # MODEL ↔ HARDWARE
    for model in models:
        for hw in hardware:
            edges.append({
                "source": model["id"],
                "target": hw["id"],
                "relation": "RUNS_ON",
                "domain": domain,
            })

    return edges[:20]  # 엣지 수 제한


def generate_ew_edges(ew_signals: list[str], existing_entities: list[dict]) -> list[dict]:
    """EW 시그널별 특수 엣지 삽입."""
    edges = []
    existing_ids = {e["id"] for e in existing_entities}

    for signal in ew_signals:
        signal_lower = signal.lower()
        edge_type = EW_EDGE_MAP.get(
            next((k for k in EW_EDGE_MAP if k != "default" and k in signal_lower), "default"),
            EW_EDGE_MAP["default"]
        )

        # 관련 엔티티 찾기
        related = [
            eid for eid in existing_ids
            if any(k in signal_lower for k in [eid.lower(), signal_lower[:8]])
        ]
        if not related:
            related = ["AI_ECOSYSTEM"]  # 폴백 노드

        edges.append({
            "source": "EW_SIGNAL",
            "target": related[0],
            "relation": edge_type,
            "signal_text": signal[:100],
            "is_ew": True,
        })

    return edges


def process_intel_dir(intel_dir: str) -> tuple[list, list]:
    """디렉토리의 모든 인텔 파일에서 노드/엣지 수집."""
    base_dir = Path(intel_dir)
    all_nodes = []
    all_edges = []
    seen_ids = set()

    if not base_dir.exists():
        print(f"[WARN] Intel dir not found: {intel_dir}", file=sys.stderr)
        return all_nodes, all_edges

    for fp in sorted(base_dir.glob("*.json")):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"[WARN] Skip {fp.name}: {e}", file=sys.stderr)
            continue

        items = data if isinstance(data, list) else [data]
        for item in items:
            domain = item.get("domain", item.get("topic", fp.stem))
            entities = extract_entities_from_intel(item)

            for entity in entities:
                if entity["id"] not in seen_ids:
                    entity["first_seen_domain"] = domain
                    all_nodes.append(entity)
                    seen_ids.add(entity["id"])

            edges = generate_edges_from_entities(entities, domain)
            all_edges.extend(edges)

    return all_nodes, all_edges


def main():
    parser = argparse.ArgumentParser(description="Knowledge Graph Delta Generator")
    parser.add_argument("--intel-dir", default="output/ai_intel",
                        help="인텔 JSON 파일 디렉토리")
    parser.add_argument("--current-version", default="4.25",
                        help="현재 KG 버전 (예: 4.25)")
    parser.add_argument("--next-version", default="4.26",
                        help="새 KG 버전 (예: 4.26)")
    parser.add_argument("--week", required=True, help="ISO 주차 (예: 2026-W21)")
    parser.add_argument("--run-date", default=datetime.utcnow().strftime("%Y-%m-%d"),
                        help="실행 날짜 (YYYY-MM-DD)")
    parser.add_argument("--ew-signals", default="",
                        help="콤마 구분 EW 시그널 문자열")
    parser.add_argument("--ew-triggered", default="false",
                        help="EW 발동 여부 (true/false)")
    parser.add_argument("--output", default="knowledge_graph_delta.json",
                        help="출력 파일 경로")
    args = parser.parse_args()

    # EW 시그널 파싱
    ew_signals = [s.strip() for s in args.ew_signals.split(",") if s.strip()]
    ew_triggered = args.ew_triggered.lower() == "true"

    # 노드/엣지 생성
    nodes, edges = process_intel_dir(args.intel_dir)

    # EW 전용 엣지 추가
    if ew_triggered and ew_signals:
        ew_edges = generate_ew_edges(ew_signals, nodes)
        edges.extend(ew_edges)
        # EW 신호 노드 추가
        nodes.append({
            "id": "EW_SIGNAL",
            "label": "Early Warning Signal",
            "type": "EW_NODE",
            "week": args.week,
        })

    # 버전 메타데이터 계산
    try:
        current_ver = float(args.current_version)
        next_ver = float(args.next_version)
    except ValueError:
        current_ver = 4.25
        next_ver = 4.26

    delta = {
        "meta": {
            "week": args.week,
            "run_date": args.run_date,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "version_from": args.current_version,
            "version_to": args.next_version,
            "version_delta": round(next_ver - current_ver, 3),
            "ew_triggered": ew_triggered,
            "ew_signal_count": len(ew_signals),
        },
        "nodes": {
            "added": nodes,
            "modified": [],
            "removed": [],
            "count_added": len(nodes),
        },
        "edges": {
            "added": edges,
            "removed": [],
            "count_added": len(edges),
        },
        "ew_edges": [e for e in edges if e.get("is_ew", False)],
        "summary": (
            f"v{args.current_version} → v{args.next_version} | "
            f"{len(nodes)} nodes, {len(edges)} edges added"
            + (f" | EW: {len(ew_signals)} signals" if ew_triggered else "")
        ),
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(delta, f, ensure_ascii=False, indent=2)

    print(f"[KG] Delta: {len(nodes)} nodes | {len(edges)} edges | Output={args.output}")
    print(delta["summary"])


if __name__ == "__main__":
    main()
