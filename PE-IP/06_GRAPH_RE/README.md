# 06_GRAPH_RE — Graph Reverse Engineering Module

> **PE-IP Module 06** | Graph-based Prompt Structure Analysis & Node Extraction  
> Created: 2026-05-10 | Status: 🟡 ACTIVE (v1.0)

---

## 📁 Directory Structure

```
06_GRAPH_RE/
├── README.md                    ← This file
├── GR-MASTER_v1.0.md            ← Graph RE Master Prompt (PE-1 auto-improvement input)
├── GR-01_Node_Extractor.md      ← Node Extractor → PROMPT_012_A connection test
├── GR-02_Edge_Mapper.md         ← (TBD) Edge relationship mapping
├── GR-03_Cluster_Analyzer.md    ← (TBD) Prompt cluster analysis
└── tests/
    └── GR-01_test_PROMPT_012_A.md  ← Real-world test log
```

---

## 🎯 Module Purpose

`06_GRAPH_RE`는 프롬프트 구조를 **그래프 형태로 역공학(Reverse Engineering)**하는 PE-IP 전용 모듈입니다.

| 기능 | 설명 |
|------|------|
| **Node Extraction** | 프롬프트 내 핵심 개념 노드 추출 |
| **Edge Mapping** | 노드 간 의존/연결 관계 시각화 |
| **Cluster Analysis** | 프롬프트 클러스터 구조 분석 |
| **PE-1 Feedback Loop** | 분석 결과를 PE-1 자동개선 엔진에 입력 |

---

## 🔗 Chain Connections

```
PROMPT_012_A (PE-TECH-RE)
        ↓
  GR-01 Node Extractor  ──→  Graph JSON output
        ↓
  GR-MASTER v1.0        ──→  PE-1 Auto-Improvement
        ↓
  knowledge_graph.json (repo root)
```

---

## 🚀 Quick Start

```bash
# Graph RE 실행
pe-graph --source 06_GRAPH_RE --input PROMPT_012_A

# Node 추출만 실행
pe-graph --source 06_GRAPH_RE --node-only --input PROMPT_012_A

# PE-1 자동개선 루프 실행
pe-graph --source 06_GRAPH_RE --pe1-loop --input PROMPT_012_A
```

---

## 📊 Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-05-10 | Initial module creation, GR-MASTER draft, GR-01 test |

---

## 🔑 Related Files

- [`domains/PE-TECH-RE/PROMPT_012_A_v2.0.md`](../../domains/PE-TECH-RE/PROMPT_012_A_v2.0.md)
- [`knowledge_graph.json`](../../knowledge_graph.json)
- [`MASTER_COMMANDS.md`](../../MASTER_COMMANDS.md)
- [`PE-IP/05_COGNITIVE_RE/`](../05_COGNITIVE_RE/) — PE-IP-012-A mirror source
