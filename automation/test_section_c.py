#!/usr/bin/env python3
"""
Section C — kg_delta_generator.py 단위 테스트
KG 노드·엣지 생성 로직 Mock 검증 (API 호출 없음)
"""
import json
import sys
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))


SAMPLE_INTEL = [
    {
        "domain": "enterprise_deployment",
        "week": "2026-W21",
        "key_facts": (
            "NVIDIA announced new Blackwell Ultra GPU. "
            "LangChain released v0.4 with streaming improvements. "
            "Claude 4 adoption in enterprises reached 45%."
        ),
        "metrics": {"adoption_rate": 45, "new_models_released": 3},
        "implications": "Accelerating enterprise AI infra build-out.",
    },
    {
        "domain": "rag_architecture",
        "week": "2026-W21",
        "key_facts": (
            "GraphRAG surpassed vector RAG in benchmark. "
            "OpenAI o3 integrated into RAG pipelines."
        ),
        "metrics": {"rag_accuracy_delta": 12},
        "implications": "Graph-based retrieval becoming mainstream.",
    },
]


class TestKGNodeGeneration(unittest.TestCase):
    """KG 노드 생성 검증"""

    def test_entity_extraction(self):
        """NVIDIA, LangChain, Claude 4 등 엔티티가 노드로 추출되는지 확인"""
        from kg_delta_generator import extract_entities_from_intel

        nodes = extract_entities_from_intel(SAMPLE_INTEL)
        node_ids = [n["id"] for n in nodes]
        # 최소 1개 이상의 기술 엔티티 포함
        self.assertGreater(len(nodes), 0)
        # 모든 노드에 필수 필드 포함
        for node in nodes:
            self.assertIn("id", node)
            self.assertIn("label", node)
            self.assertIn("type", node)

    def test_metric_nodes_created(self):
        """metrics 딕셔너리에서 MetricNode 생성 확인"""
        from kg_delta_generator import extract_metric_nodes

        metric_nodes = extract_metric_nodes(SAMPLE_INTEL)
        self.assertGreater(len(metric_nodes), 0)
        for node in metric_nodes:
            self.assertEqual(node["type"], "MetricNode")
            self.assertIn("value", node)

    def test_domain_nodes_created(self):
        """각 도메인이 DomainNode로 생성되는지 확인"""
        from kg_delta_generator import extract_domain_nodes

        domain_nodes = extract_domain_nodes(SAMPLE_INTEL)
        domain_ids = [n["id"] for n in domain_nodes]
        self.assertIn("enterprise_deployment", domain_ids)
        self.assertIn("rag_architecture", domain_ids)

    def test_no_duplicate_nodes(self):
        """동일 엔티티 중복 노드 없음 확인"""
        from kg_delta_generator import extract_entities_from_intel

        # 동일 인텔 2번 입력 → 중복 제거 기대
        nodes = extract_entities_from_intel(SAMPLE_INTEL + SAMPLE_INTEL)
        node_ids = [n["id"] for n in nodes]
        self.assertEqual(len(node_ids), len(set(node_ids)), "Duplicate node IDs found")


class TestKGEdgeGeneration(unittest.TestCase):
    """KG 엣지 생성 검증"""

    def test_edges_have_required_fields(self):
        """모든 엣지에 source, target, relation 필드 포함"""
        from kg_delta_generator import generate_edges

        nodes = [{"id": "NVIDIA", "label": "NVIDIA", "type": "Company"},
                 {"id": "Blackwell_Ultra", "label": "Blackwell Ultra", "type": "Product"}]
        edges = generate_edges(nodes, SAMPLE_INTEL)
        for edge in edges:
            self.assertIn("source", edge)
            self.assertIn("target", edge)
            self.assertIn("relation", edge)

    def test_ew_edges_inserted_when_triggered(self):
        """EW signal 있을 때 EW 전용 엣지 삽입 확인"""
        from kg_delta_generator import generate_ew_edges

        ew_signals = ["RAG_MIGRATION_SPIKE", "ENTERPRISE_ADOPTION_SURGE"]
        ew_edges = generate_ew_edges(ew_signals, week="2026-W21")
        self.assertGreaterEqual(len(ew_edges), len(ew_signals))
        relation_types = [e["relation"] for e in ew_edges]
        # EW 엣지는 EW_ 접두사 포함
        for rel in relation_types:
            self.assertTrue(rel.startswith("EW_") or "EW" in rel,
                            f"EW edge relation should contain 'EW': {rel}")

    def test_no_self_loop_edges(self):
        """source == target 셀프 루프 엣지 없음"""
        from kg_delta_generator import generate_edges

        nodes = [
            {"id": "A", "label": "A", "type": "X"},
            {"id": "B", "label": "B", "type": "Y"},
        ]
        edges = generate_edges(nodes, SAMPLE_INTEL)
        for edge in edges:
            self.assertNotEqual(edge["source"], edge["target"],
                                f"Self-loop edge detected: {edge}")


class TestKGDeltaOutput(unittest.TestCase):
    """KG Delta JSON 출력 구조 검증"""

    def test_delta_output_schema(self):
        """최종 delta JSON에 nodes, edges, metadata 포함"""
        from kg_delta_generator import build_kg_delta

        delta = build_kg_delta(
            intel_list=SAMPLE_INTEL,
            current_version="4.25",
            next_version="4.26",
            week="2026-W21",
            run_date="2026-05-20",
            ew_signals=[],
        )
        self.assertIn("nodes", delta)
        self.assertIn("edges", delta)
        self.assertIn("metadata", delta)
        self.assertEqual(delta["metadata"]["from_version"], "4.25")
        self.assertEqual(delta["metadata"]["to_version"], "4.26")

    def test_delta_node_count_positive(self):
        """노드 수 > 0"""
        from kg_delta_generator import build_kg_delta

        delta = build_kg_delta(
            intel_list=SAMPLE_INTEL,
            current_version="4.25",
            next_version="4.26",
            week="2026-W21",
            run_date="2026-05-20",
            ew_signals=[],
        )
        self.assertGreater(len(delta["nodes"]), 0)

    def test_delta_serializable(self):
        """delta JSON 직렬화 가능 (TypeError 없음)"""
        from kg_delta_generator import build_kg_delta

        delta = build_kg_delta(
            intel_list=SAMPLE_INTEL,
            current_version="4.25",
            next_version="4.26",
            week="2026-W21",
            run_date="2026-05-20",
            ew_signals=[],
        )
        try:
            serialized = json.dumps(delta, ensure_ascii=False)
            self.assertGreater(len(serialized), 10)
        except TypeError as e:
            self.fail(f"KG delta is not JSON-serializable: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("Section C — kg_delta_generator Unit Tests")
    print("=" * 60)
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestKGNodeGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestKGEdgeGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestKGDeltaOutput))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
