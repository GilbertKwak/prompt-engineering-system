#!/usr/bin/env python3
"""
Section D — notion_c31_updater.py 단위 테스트
NotionAPI Mock으로 실제 네트워크 호출 없이 블록 생성 로직 전체 검증
"""
import json
import sys
import os
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock, call

sys.path.insert(0, str(Path(__file__).parent))

SAMPLE_INTEL_DIR_DATA = [
    {
        "domain": "enterprise_deployment",
        "week": "2026-W21",
        "key_facts": "Enterprise AI adoption reached 50%.",
        "metrics": {"adoption_rate": 50},
        "implications": "Steady growth.",
    }
]


class TestNotionBlockBuilder(unittest.TestCase):
    """Notion Block 빌더 함수 단위 검증"""

    def test_heading_block_structure(self):
        """heading_2 블록 구조 확인"""
        from notion_c31_updater import make_heading_block

        block = make_heading_block("Test Heading", level=2)
        self.assertEqual(block["type"], "heading_2")
        self.assertIn("heading_2", block)
        rich_text = block["heading_2"]["rich_text"]
        self.assertEqual(rich_text[0]["text"]["content"], "Test Heading")

    def test_paragraph_block_structure(self):
        """paragraph 블록 구조 확인"""
        from notion_c31_updater import make_paragraph_block

        block = make_paragraph_block("Hello world.")
        self.assertEqual(block["type"], "paragraph")
        self.assertIn("paragraph", block)

    def test_callout_block_severity_colors(self):
        """EW 심각도별 callout 색상 매핑 확인"""
        from notion_c31_updater import make_ew_callout_block

        for severity, expected_color in [
            ("CRITICAL", "red_background"),
            ("HIGH",     "orange_background"),
            ("MEDIUM",   "yellow_background"),
            ("NONE",     "green_background"),
        ]:
            block = make_ew_callout_block(
                severity=severity,
                signals=[],
                week="2026-W21",
            )
            self.assertEqual(block["type"], "callout")
            actual_color = block["callout"].get("color", "")
            self.assertEqual(
                actual_color, expected_color,
                f"Severity {severity}: expected {expected_color}, got {actual_color}",
            )

    def test_divider_block(self):
        """divider 블록 타입 확인"""
        from notion_c31_updater import make_divider_block

        block = make_divider_block()
        self.assertEqual(block["type"], "divider")

    def test_bullet_list_block(self):
        """bulleted_list_item 블록 생성 확인"""
        from notion_c31_updater import make_bullet_block

        block = make_bullet_block("Item 1")
        self.assertEqual(block["type"], "bulleted_list_item")
        content = block["bulleted_list_item"]["rich_text"][0]["text"]["content"]
        self.assertEqual(content, "Item 1")


class TestNotionBatchAppend(unittest.TestCase):
    """50-block 배치 처리 로직 검증 (Notion API Mock)"""

    @patch("notion_c31_updater.requests.patch")
    def test_batch_splits_at_50(self, mock_patch):
        """블록 130개 → requests.patch 3회 호출 확인 (50+50+30)"""
        mock_patch.return_value.status_code = 200
        mock_patch.return_value.json.return_value = {"results": []}

        from notion_c31_updater import append_blocks_batched

        blocks = [{"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": f"block {i}"}}]}}
                  for i in range(130)]

        append_blocks_batched(page_id="fake-page-id", blocks=blocks, api_key="fake-key")

        # 130 / 50 = 3 batches
        self.assertEqual(mock_patch.call_count, 3)

    @patch("notion_c31_updater.requests.patch")
    def test_empty_blocks_no_api_call(self, mock_patch):
        """빈 블록 리스트 → API 호출 없음"""
        from notion_c31_updater import append_blocks_batched

        append_blocks_batched(page_id="fake-page-id", blocks=[], api_key="fake-key")
        mock_patch.assert_not_called()

    @patch("notion_c31_updater.requests.patch")
    def test_api_error_raises(self, mock_patch):
        """API 400 응답 → RuntimeError 발생 확인"""
        mock_patch.return_value.status_code = 400
        mock_patch.return_value.json.return_value = {"message": "Invalid request"}
        mock_patch.return_value.text = "Invalid request"

        from notion_c31_updater import append_blocks_batched

        blocks = [{"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "test"}}]}}]
        with self.assertRaises(RuntimeError):
            append_blocks_batched(page_id="fake-page-id", blocks=blocks, api_key="fake-key")


class TestNotionUpdatePayload(unittest.TestCase):
    """전체 페이지 업데이트 페이로드 구성 검증"""

    def test_full_update_payload_sections(self):
        """build_update_payload가 EW·KG·인텔 섹션 포함하는지 확인"""
        from notion_c31_updater import build_update_payload

        payload = build_update_payload(
            week="2026-W21",
            run_date="2026-05-20",
            ew_triggered=False,
            ew_count=0,
            ew_signals=[],
            ew_severity="NONE",
            kg_version="4.26",
            node_count=15,
            edge_count=10,
            intel_summaries=SAMPLE_INTEL_DIR_DATA,
        )
        block_types = [b["type"] for b in payload]
        # 최소한 heading, paragraph, callout, divider 포함
        self.assertIn("heading_2", block_types)
        self.assertIn("callout", block_types)
        self.assertIn("divider", block_types)

    def test_ew_triggered_payload_has_critical_callout(self):
        """EW triggered + CRITICAL → red_background callout 확인"""
        from notion_c31_updater import build_update_payload

        payload = build_update_payload(
            week="2026-W21",
            run_date="2026-05-20",
            ew_triggered=True,
            ew_count=2,
            ew_signals=["ADOPTION_SURGE", "COST_COLLAPSE"],
            ew_severity="CRITICAL",
            kg_version="4.26",
            node_count=20,
            edge_count=15,
            intel_summaries=SAMPLE_INTEL_DIR_DATA,
        )
        callout_blocks = [b for b in payload if b["type"] == "callout"]
        red_callouts = [
            b for b in callout_blocks
            if b["callout"].get("color") == "red_background"
        ]
        self.assertGreater(len(red_callouts), 0, "CRITICAL EW should produce a red callout")

    def test_block_count_reasonable(self):
        """페이로드 블록 수 5~200 범위 (너무 적거나 많으면 이상)"""
        from notion_c31_updater import build_update_payload

        payload = build_update_payload(
            week="2026-W21",
            run_date="2026-05-20",
            ew_triggered=False,
            ew_count=0,
            ew_signals=[],
            ew_severity="NONE",
            kg_version="4.26",
            node_count=10,
            edge_count=8,
            intel_summaries=SAMPLE_INTEL_DIR_DATA,
        )
        self.assertGreaterEqual(len(payload), 5)
        self.assertLessEqual(len(payload), 200)


if __name__ == "__main__":
    print("=" * 60)
    print("Section D — notion_c31_updater Unit Tests")
    print("=" * 60)
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestNotionBlockBuilder))
    suite.addTests(loader.loadTestsFromTestCase(TestNotionBatchAppend))
    suite.addTests(loader.loadTestsFromTestCase(TestNotionUpdatePayload))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
