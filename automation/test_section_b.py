#!/usr/bin/env python3
"""
Section B — ai_ew_detector.py 단위 테스트
Mock 데이터로 EW 탐지 로직 전체 검증 (API 호출 없음)
"""
import json
import sys
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# 프로젝트 루트를 sys.path에 추가
sys.path.insert(0, str(Path(__file__).parent))


class TestEWDetectorMockData(unittest.TestCase):
    """ai_ew_detector.py 핵심 로직 — Mock 인텔 데이터로 검증"""

    def _make_intel_file(self, tmpdir: str, domain: str, payload: dict) -> str:
        path = os.path.join(tmpdir, f"intel_{domain}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)
        return path

    # ------------------------------------------------------------------
    # 1. 정상 범위 메트릭 → EW NOT triggered
    # ------------------------------------------------------------------
    def test_normal_metrics_no_ew(self):
        """adoption_rate 50%, cost_reduction 20% → EW 없음"""
        from ai_ew_detector import evaluate_domain_ew

        intel = {
            "domain": "enterprise_deployment",
            "week": "2026-W21",
            "key_facts": "Enterprise AI adoption rose to 50%.",
            "metrics": {"adoption_rate": 50, "cost_reduction": 20},
            "implications": "Steady growth trend.",
        }
        result = evaluate_domain_ew(intel, thresholds={"adoption_rate": 70, "cost_reduction": 35})
        self.assertFalse(result["ew_triggered"], "EW should NOT trigger at normal levels")
        self.assertEqual(result["severity"], "NONE")

    # ------------------------------------------------------------------
    # 2. 임계값 초과 메트릭 → EW triggered (MEDIUM)
    # ------------------------------------------------------------------
    def test_threshold_breach_medium_ew(self):
        """adoption_rate 78% > 70% → EW MEDIUM"""
        from ai_ew_detector import evaluate_domain_ew

        intel = {
            "domain": "enterprise_deployment",
            "week": "2026-W21",
            "key_facts": "Enterprise AI adoption surged to 78%.",
            "metrics": {"adoption_rate": 78, "cost_reduction": 20},
            "implications": "Rapid acceleration observed.",
        }
        result = evaluate_domain_ew(intel, thresholds={"adoption_rate": 70, "cost_reduction": 35})
        self.assertTrue(result["ew_triggered"], "EW should trigger when threshold exceeded")
        self.assertIn(result["severity"], ["MEDIUM", "HIGH", "CRITICAL"])
        self.assertGreater(len(result["signals"]), 0)

    # ------------------------------------------------------------------
    # 3. 메트릭 누락 시 키워드 휴리스틱 폴백
    # ------------------------------------------------------------------
    def test_keyword_heuristic_fallback(self):
        """metrics 없을 때 경고 키워드 2개 이상 hit → EW triggered"""
        from ai_ew_detector import evaluate_domain_ew

        intel = {
            "domain": "enterprise_deployment",
            "week": "2026-W21",
            "key_facts": "Unprecedented disruption. Critical shift in paradigm. Emergency protocols enacted.",
            "metrics": {},
            "implications": "Systemic risk detected.",
        }
        result = evaluate_domain_ew(intel, thresholds={})
        self.assertTrue(result["ew_triggered"], "Keyword heuristic should catch 3 warning terms")

    # ------------------------------------------------------------------
    # 4. 빈 인텔 파일 → graceful 처리
    # ------------------------------------------------------------------
    def test_empty_intel_graceful(self):
        """빈 dict 입력 시 크래시 없이 ew_triggered=False 반환"""
        from ai_ew_detector import evaluate_domain_ew

        result = evaluate_domain_ew({}, thresholds={})
        self.assertFalse(result.get("ew_triggered", False))

    # ------------------------------------------------------------------
    # 5. 다중 도메인 배치 처리
    # ------------------------------------------------------------------
    def test_multi_domain_batch(self):
        """5개 도메인 중 1개만 임계값 초과 → ew_count == 1"""
        from ai_ew_detector import batch_evaluate_ew

        domains = [
            {"domain": f"domain_{i}", "week": "2026-W21",
             "key_facts": "Normal.", "metrics": {"adoption_rate": 40}, "implications": ""}
            for i in range(4)
        ]
        # 하나만 초과
        domains.append({
            "domain": "hot_domain",
            "week": "2026-W21",
            "key_facts": "Adoption exploded to 85%.",
            "metrics": {"adoption_rate": 85},
            "implications": "Major shift.",
        })
        report = batch_evaluate_ew(domains, thresholds={"adoption_rate": 70})
        ew_hits = [r for r in report["results"] if r["ew_triggered"]]
        self.assertEqual(len(ew_hits), 1)
        self.assertEqual(report["summary"]["ew_count"], 1)

    # ------------------------------------------------------------------
    # 6. CRITICAL 임계값 (adoption_rate > 90)
    # ------------------------------------------------------------------
    def test_critical_severity(self):
        """adoption_rate 95% → CRITICAL severity"""
        from ai_ew_detector import evaluate_domain_ew

        intel = {
            "domain": "enterprise_deployment",
            "week": "2026-W21",
            "key_facts": "Adoption hit 95% in Fortune 500.",
            "metrics": {"adoption_rate": 95},
            "implications": "Near-saturation point reached.",
        }
        result = evaluate_domain_ew(
            intel,
            thresholds={"adoption_rate": 70},
            critical_multiplier=1.3,  # 70 * 1.3 = 91 → CRITICAL
        )
        self.assertTrue(result["ew_triggered"])
        self.assertEqual(result["severity"], "CRITICAL")


class TestEWDetectorCLI(unittest.TestCase):
    """CLI argparse 인터페이스 검증"""

    def test_cli_help_exit(self):
        """--help 호출 시 SystemExit(0) 발생 확인"""
        with self.assertRaises(SystemExit) as ctx:
            with patch("sys.argv", ["ai_ew_detector.py", "--help"]):
                import importlib
                import ai_ew_detector
                importlib.reload(ai_ew_detector)
        self.assertEqual(ctx.exception.code, 0)


if __name__ == "__main__":
    print("=" * 60)
    print("Section B — ai_ew_detector Unit Tests")
    print("=" * 60)
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestEWDetectorMockData))
    suite.addTests(loader.loadTestsFromTestCase(TestEWDetectorCLI))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
