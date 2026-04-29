#!/usr/bin/env python3
"""
knowledge_graph_rebuild_v4.1.py
PE-SEMI C-29 신설 반영 — knowledge_graph v4.1 재생성

New Nodes (+5):
  - SEMI-001-MASTER (PE-3: 96+, domain: SEMI-STRATEGY)
  - SEMI-001-KR (PE-3: 95, domain: SEMI-STRATEGY, variant: KR)
  - SEMI-001-GLOBAL (PE-3: 94, domain: SEMI-STRATEGY, variant: GLOBAL)
  - PE-SEMI-HUB (type: hub, child: C-29)
  - FAB-STATE-MACHINE (type: framework, version: 1.0)

New Edges (+8):
  - PE-SEMI-HUB → PE-AI (trigger: HBM/CoWoS bottleneck)
  - PE-SEMI-HUB → PE-MIN (trigger: Ga/Ge export control)
  - PE-SEMI-HUB → PE-PWR (trigger: FAB energy cost)
  - PE-SEMI-HUB → PE-EQP (trigger: ASML/Lam export control)
  - PE-SEMI-HUB → PE-CHEM (trigger: EUV PR/CMP Slurry shortage)
  - PE-SEMI-HUB → PE-11 (parent: Master Multi-Agent System)
  - PE-SEMI-HUB → C-24-SEMI-PROCESS (sibling: process analysis library)
  - C-29 → T-09 (parent: Mother Page v3.9)

Total after rebuild: 120 nodes / 177 edges
"""

NEW_NODES = [
    {"id": "SEMI-001-MASTER", "type": "prompt", "domain": "SEMI-STRATEGY",
     "pe3": 96, "version": "7.0-MASTER", "child": "C-29"},
    {"id": "SEMI-001-KR", "type": "prompt", "domain": "SEMI-STRATEGY",
     "pe3": 95, "version": "7.0-KR", "variant": "KR", "child": "C-29"},
    {"id": "SEMI-001-GLOBAL", "type": "prompt", "domain": "SEMI-STRATEGY",
     "pe3": 94, "version": "7.0-GLOBAL", "variant": "GLOBAL", "child": "C-29"},
    {"id": "PE-SEMI-HUB", "type": "hub", "child": "C-29",
     "notion": "https://app.notion.com/p/35155ed436f081bc89aacc6035cbe4f1"},
    {"id": "FAB-STATE-MACHINE", "type": "framework", "version": "1.0",
     "states": ["S0", "S1", "S2", "S3", "S4"]},
]

NEW_EDGES = [
    {"source": "PE-SEMI-HUB", "target": "PE-AI",
     "trigger": "HBM/CoWoS → AI 훈련 컴퓨트 병목"},
    {"source": "PE-SEMI-HUB", "target": "PE-MIN",
     "trigger": "Ga/Ge 수출통제 → GaN/SiC 차질"},
    {"source": "PE-SEMI-HUB", "target": "PE-PWR",
     "trigger": "AI-DC 전력 → FAB 에너지 비용"},
    {"source": "PE-SEMI-HUB", "target": "PE-EQP",
     "trigger": "ASML/Lam 수출통제 → 장비 조달 위기"},
    {"source": "PE-SEMI-HUB", "target": "PE-CHEM",
     "trigger": "EUV PR·CMP Slurry 공급 차질"},
    {"source": "PE-SEMI-HUB", "target": "PE-11",
     "trigger": "parent: Master Multi-Agent System v11.0"},
    {"source": "PE-SEMI-HUB", "target": "C-24-SEMI-PROCESS",
     "trigger": "sibling: 반도체 공정 조사 분석 라이브러리 v1.0"},
    {"source": "C-29", "target": "T-09",
     "trigger": "parent: Mother Page v3.9"},
]

GRAPH_METADATA = {
    "version": "4.1",
    "previous_version": "4.0",
    "nodes_before": 115,
    "edges_before": 169,
    "nodes_added": 5,
    "edges_added": 8,
    "nodes_after": 120,
    "edges_after": 177,
    "rebuild_date": "2026-04-29",
    "patch_package": "PP-18",
    "trigger": "C-29 PE-SEMI 신설",
}

if __name__ == "__main__":
    print(f"knowledge_graph v{GRAPH_METADATA['version']} rebuild plan:")
    print(f"  Nodes: {GRAPH_METADATA['nodes_before']} + {GRAPH_METADATA['nodes_added']}"
          f" = {GRAPH_METADATA['nodes_after']}")
    print(f"  Edges: {GRAPH_METADATA['edges_before']} + {GRAPH_METADATA['edges_added']}"
          f" = {GRAPH_METADATA['edges_after']}")
    print("  Status: READY — run pe-graph --rebuild v4.1 to apply")
