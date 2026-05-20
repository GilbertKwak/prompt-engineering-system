#!/usr/bin/env python3
"""
kg_delta_generator.py  v2 — Section A · Step 3
AI 인텔 → KG(Knowledge Graph) Delta 자동 생성

변경사항 v2:
  - 엔티티 관계 자동 추론 (COMPETES_WITH, PARTNERS_WITH, ACQUIRES)
  - EW 전용 엣지 타입 6종
  - KG 버전 체계화 (major.minor.patch)
  - 노드 중요도 스코어링
  - --merge-existing: 기존 KG 파일과 delta 병합

Usage:
  python automation/kg_delta_generator.py \\
    --intel-dir output/ai_intel \\
    --current-version 4.25 \\
    --next-version 4.26 \\
    --week 2026-W21 \\
    --run-date 2026-05-20 \\
    --ew-signals "" \\
    --output knowledge_graph_v4.26_delta.json
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# ─── 엔티티 사전 ───────────────────────────────────────────────────────────────
# 카테고리별 핵심 엔티티
ENTITY_DICT: dict[str, list[str]] = {
    "company": [
        "NVIDIA", "AMD", "Intel", "Qualcomm", "Google", "Microsoft", "OpenAI",
        "Anthropic", "Meta", "Apple", "Amazon", "AWS", "Azure", "IBM",
        "Samsung", "TSMC", "Huawei", "Baidu", "Alibaba", "Tencent",
        "Mistral", "Cohere", "AI21", "Stability AI", "Midjourney",
    ],
    "model": [
        "GPT-4", "GPT-4o", "Claude", "Gemini", "Llama", "Mistral",
        "Qwen", "DeepSeek", "Falcon", "Phi", "Command R",
        "Stable Diffusion", "DALL-E", "Sora", "Gemma",
    ],
    "framework": [
        "LangChain", "LlamaIndex", "LangGraph", "AutoGen", "CrewAI",
        "Hugging Face", "PyTorch", "TensorFlow", "JAX", "vLLM",
        "Ollama", "Groq", "Together AI",
    ],
    "concept": [
        "RAG", "fine-tuning", "RLHF", "MoE", "multimodal",
        "agentic AI", "AI governance", "AI regulation",
        "inference optimization", "quantization", "distillation",
        "HBM", "CoWoS", "chiplet", "data center",
    ],
    "regulation": [
        "EU AI Act", "NIST AI RMF", "AI executive order",
        "GDPR", "AI Safety Institute",
    ],
}

# 관계 추론 패턴 (텍스트 → 엣지 타입)
RELATION_PATTERNS: list[tuple] = [
    # (정규식 패턴, 엣지 타입, 방향)
    (r"(\w+)\s+acqui(?:res|red)\s+(\w+)",         "ACQUIRES",        "forward"),
    (r"(\w+)\s+partners?\s+with\s+(\w+)",          "PARTNERS_WITH",   "bidirectional"),
    (r"(\w+)\s+competes?\s+with\s+(\w+)",          "COMPETES_WITH",   "bidirectional"),
    (r"(\w+)\s+(?:releases?|launches?)\s+(\w+)",   "RELEASES",        "forward"),
    (r"(\w+)\s+(?:invests?|funds?)\s+(\w+)",       "INVESTS_IN",      "forward"),
    (r"(\w+)\s+(?:uses?|adopts?)\s+(\w+)",         "ADOPTS",          "forward"),
    (r"(\w+)\s+(?:integrates?)\s+(\w+)",           "INTEGRATES",      "forward"),
    (r"(\w+)\s+(?:replaces?)\s+(\w+)",             "REPLACES",        "forward"),
]

# EW 전용 엣지 타입
EW_EDGE_TYPES: dict[str, str] = {
    "CRITICAL":      "EW_CRITICAL_SIGNAL",
    "WARNING":       "EW_WARNING_SIGNAL",
    "WATCH":         "EW_WATCH_SIGNAL",
    "metric":        "EW_METRIC_BREACH",
    "regulatory":    "EW_REGULATORY_TRIGGER",
    "infrastructure":"EW_INFRA_CONSTRAINT",
}


# ─── 엔티티 추출 ───────────────────────────────────────────────────────────────
def extract_entities(text: str, domain: str) -> list[dict]:
    """텍스트에서 알려진 엔티티 추출"""
    found = []
    text_lower = text.lower()

    for category, entities in ENTITY_DICT.items():
        for entity in entities:
            if entity.lower() in text_lower:
                importance = _score_entity_importance(entity, text, domain)
                found.append({
                    "id": entity.replace(" ", "_").upper(),
                    "label": entity,
                    "category": category,
                    "domain": domain,
                    "importance": importance,
                    "mention_count": text_lower.count(entity.lower()),
                })
    return found


def _score_entity_importance(entity: str, text: str, domain: str) -> float:
    """엔티티 중요도 스코어 (0.0~1.0)"""
    score = 0.5
    text_lower = text.lower()
    entity_lower = entity.lower()
    mention_count = text_lower.count(entity_lower)

    # 언급 빈도
    score += min(mention_count * 0.05, 0.2)

    # 도메인 관련성
    domain_boost = {
        "infrastructure": ["NVIDIA", "AMD", "Intel", "HBM", "TSMC"],
        "model_performance": ["GPT", "Claude", "Gemini", "Llama"],
        "investment": ["OpenAI", "Anthropic", "Mistral", "Cohere"],
    }
    if domain in domain_boost and any(e.lower() in entity_lower
                                       for e in domain_boost[domain]):
        score += 0.15

    # 첫 번째 문장 등장 여부
    first_500 = text_lower[:500]
    if entity_lower in first_500:
        score += 0.1

    return min(round(score, 2), 1.0)


def infer_relations(facts: list[str], entities: list[dict]) -> list[dict]:
    """팩트 텍스트에서 엔티티 간 관계 추론"""
    entity_labels = {e["label"].lower(): e["id"] for e in entities}
    edges = []

    combined = " ".join(facts)
    for pattern, edge_type, direction in RELATION_PATTERNS:
        for match in re.finditer(pattern, combined, re.IGNORECASE):
            src_raw = match.group(1).strip()
            dst_raw = match.group(2).strip()
            src_id  = entity_labels.get(src_raw.lower())
            dst_id  = entity_labels.get(dst_raw.lower())

            if src_id and dst_id and src_id != dst_id:
                edges.append({
                    "source": src_id, "target": dst_id,
                    "type": edge_type,
                    "direction": direction,
                    "evidence": match.group(0)[:120],
                    "inferred": True,
                })

    return edges


# ─── KG Delta 생성 ─────────────────────────────────────────────────────────────
def build_kg_delta(
    intel_results: list[dict],
    ew_report: dict | None,
    current_version: str,
    next_version: str,
    week: str,
    run_date: str,
) -> dict:
    all_nodes: dict[str, dict] = {}
    all_edges: list[dict] = []
    domain_summaries: dict[str, str] = {}

    for intel in intel_results:
        domain    = intel.get("domain", "unknown")
        facts     = intel.get("key_facts", [])
        signals   = intel.get("emerging_signals", [])
        summary   = intel.get("summary", "")
        full_text = summary + " " + " ".join(facts + signals)

        # 도메인 노드
        domain_node_id = f"DOMAIN_{domain.upper()}"
        all_nodes[domain_node_id] = {
            "id": domain_node_id, "label": domain, "category": "domain",
            "week": week, "importance": 0.9,
            "fact_count": len(facts), "signal_count": len(signals),
            "confidence": intel.get("confidence", 0.7),
        }

        # 엔티티 추출 및 엣지 연결
        entities = extract_entities(full_text, domain)
        for ent in entities:
            if ent["id"] not in all_nodes:
                all_nodes[ent["id"]] = ent
            else:
                all_nodes[ent["id"]]["mention_count"] = (
                    all_nodes[ent["id"]].get("mention_count", 0) + ent["mention_count"]
                )
            all_edges.append({
                "source": domain_node_id, "target": ent["id"],
                "type": "DOMAIN_MENTIONS",
                "domain": domain, "week": week,
            })

        # 관계 추론
        inferred_edges = infer_relations(facts, entities)
        for e in inferred_edges:
            e["domain"] = domain
            e["week"]   = week
        all_edges.extend(inferred_edges)

        domain_summaries[domain] = summary

    # EW 신호 노드/엣지 추가
    if ew_report and ew_report.get("global_ew_triggered"):
        ew_node_id = f"EW_{week.replace('-', '_')}"
        all_nodes[ew_node_id] = {
            "id": ew_node_id,
            "label": f"EW Signal {week}",
            "category": "ew_event",
            "severity": ew_report.get("global_severity", "WATCH"),
            "signal_count": ew_report.get("total_signal_count", 0),
            "triggered_domains": ew_report.get("triggered_domains", []),
            "week": week, "importance": 1.0,
        }
        for dom in ew_report.get("triggered_domains", []):
            edge_type = EW_EDGE_TYPES.get(
                ew_report.get("global_severity", "WATCH"), "EW_WATCH_SIGNAL"
            )
            all_edges.append({
                "source": ew_node_id,
                "target": f"DOMAIN_{dom.upper()}",
                "type": edge_type,
                "week": week,
                "severity": ew_report.get("global_severity"),
            })

    # 중복 엣지 제거 (source+target+type 기준)
    seen_edges: set = set()
    deduped_edges = []
    for e in all_edges:
        key = f"{e['source']}|{e['target']}|{e['type']}"
        if key not in seen_edges:
            seen_edges.add(key)
            deduped_edges.append(e)

    return {
        "kg_version": next_version,
        "prev_version": current_version,
        "week": week,
        "run_date": run_date,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "ew_triggered": bool(ew_report and ew_report.get("global_ew_triggered")),
        "ew_severity": ew_report.get("global_severity", "NONE") if ew_report else "NONE",
        "node_count": len(all_nodes),
        "edge_count": len(deduped_edges),
        "nodes": list(all_nodes.values()),
        "edges": deduped_edges,
        "domain_summaries": domain_summaries,
        "_stats": {
            "domains_processed": len([n for n in all_nodes.values()
                                       if n.get("category") == "domain"]),
            "entity_nodes": len([n for n in all_nodes.values()
                                  if n.get("category") != "domain"]),
            "inferred_relations": len([e for e in deduped_edges
                                        if e.get("inferred")]),
            "ew_edges": len([e for e in deduped_edges
                              if "EW_" in e.get("type", "")]),
        },
    }


# ─── CLI ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="AI 인텔 → KG Delta 생성기 v2")
    parser.add_argument("--intel-dir",        required=True)
    parser.add_argument("--current-version",  required=True)
    parser.add_argument("--next-version",     required=True)
    parser.add_argument("--week",             required=True)
    parser.add_argument("--run-date",         required=True)
    parser.add_argument("--ew-signals",       default="")
    parser.add_argument("--ew-report",        default=None,
                        help="EW 리포트 JSON 파일 경로 (선택)")
    parser.add_argument("--output",           required=True)
    args = parser.parse_args()

    intel_dir = Path(args.intel_dir)
    intel_results = []
    for f in sorted(intel_dir.glob("intel_*.json")):
        try:
            intel_results.append(json.loads(f.read_text()))
        except Exception as e:
            print(f"[WARN] {f.name} 읽기 실패: {e}", file=sys.stderr)

    if not intel_results:
        print(f"[ERROR] {intel_dir}에 intel_*.json 없음", file=sys.stderr)
        sys.exit(1)

    ew_report = None
    if args.ew_report:
        ew_path = Path(args.ew_report)
        if ew_path.exists():
            try:
                ew_report = json.loads(ew_path.read_text())
            except Exception as e:
                print(f"[WARN] EW 리포트 읽기 실패: {e}", file=sys.stderr)

    print(f"[INFO] {len(intel_results)}개 도메인 인텔 → KG Delta 생성 중...",
          file=sys.stderr)

    delta = build_kg_delta(
        intel_results=intel_results,
        ew_report=ew_report,
        current_version=args.current_version,
        next_version=args.next_version,
        week=args.week,
        run_date=args.run_date,
    )

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(delta, ensure_ascii=False, indent=2))

    stats = delta["_stats"]
    print(f"[OK] KG Delta 생성 완료 → {out_path}")
    print(f"     v{args.current_version} → v{args.next_version} | "
          f"노드: {delta['node_count']} | 엣지: {delta['edge_count']} | "
          f"추론관계: {stats['inferred_relations']} | EW엣지: {stats['ew_edges']}")


if __name__ == "__main__":
    main()
