#!/usr/bin/env python3
"""
test_section_a.py — Section A 전체 파이프라인 로컬 검증 스크립트

Dry-run 모드로 API 호출 없이 구조 검증 실행
Usage: python automation/test_section_a.py
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

PASS = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"
INFO = "\033[94mℹ\033[0m"


def run_cmd(cmd: list[str], env: dict = None) -> tuple[int, str, str]:
    merged_env = {**os.environ, **(env or {})}
    result = subprocess.run(cmd, capture_output=True, text=True, env=merged_env)
    return result.returncode, result.stdout, result.stderr


def test_collector_dry_run(output_dir: Path) -> bool:
    """Step 1: ai_intel_collector.py dry-run 테스트"""
    print(f"\n{INFO} Step 1: ai_intel_collector.py dry-run")
    rc, stdout, stderr = run_cmd([
        sys.executable, "automation/ai_intel_collector.py",
        "--domain", "enterprise_deployment",
        "--week", "2026-W21",
        "--scope", "standard",
        "--queries", "enterprise AI test query",
        "--output", str(output_dir / "intel_enterprise_deployment.json"),
        "--dry-run",
    ])
    if rc != 0:
        print(f"{FAIL} collector 실패: {stderr}")
        return False

    out_file = output_dir / "intel_enterprise_deployment.json"
    if not out_file.exists():
        print(f"{FAIL} 출력 파일 없음")
        return False

    data = json.loads(out_file.read_text())
    required_keys = ["domain", "week", "key_facts", "metrics", "summary"]
    missing = [k for k in required_keys if k not in data]
    if missing:
        print(f"{FAIL} 필수 키 누락: {missing}")
        return False

    print(f"{PASS} collector dry-run 성공 (키: {list(data.keys())[:6]}...)")
    return True


def test_ew_detector(output_dir: Path) -> bool:
    """Step 2: ai_ew_detector.py 테스트"""
    print(f"\n{INFO} Step 2: ai_ew_detector.py")
    rc, stdout, stderr = run_cmd([
        sys.executable, "automation/ai_ew_detector.py",
        "--input-dir", str(output_dir),
        "--week", "2026-W21",
        "--output", str(output_dir / "ew_report.json"),
    ])
    if rc != 0:
        print(f"{FAIL} ew_detector 실패: {stderr}")
        return False

    out_file = output_dir / "ew_report.json"
    if not out_file.exists():
        print(f"{FAIL} EW 리포트 없음")
        return False

    data = json.loads(out_file.read_text())
    required_keys = ["week", "total_ew_signals", "ew_triggered", "overall_severity"]
    missing = [k for k in required_keys if k not in data]
    if missing:
        print(f"{FAIL} 필수 키 누락: {missing}")
        return False

    print(f"{PASS} ew_detector 성공 (신호: {data['total_ew_signals']}개, 심각도: {data['overall_severity']})")
    return True


def test_kg_generator(output_dir: Path) -> bool:
    """Step 3: kg_delta_generator.py 테스트"""
    print(f"\n{INFO} Step 3: kg_delta_generator.py")
    output_file = output_dir / "knowledge_graph_v4.26_delta.json"
    rc, stdout, stderr = run_cmd([
        sys.executable, "automation/kg_delta_generator.py",
        "--intel-dir", str(output_dir),
        "--current-version", "4.25",
        "--next-version", "4.26",
        "--week", "2026-W21",
        "--run-date", "2026-05-20",
        "--ew-signals", "",  # 빈 문자열 처리 테스트
        "--output", str(output_file),
    ])
    if rc != 0:
        print(f"{FAIL} kg_generator 실패: {stderr}")
        return False

    if not output_file.exists():
        print(f"{FAIL} KG 델타 파일 없음")
        return False

    data = json.loads(output_file.read_text())
    required_keys = ["version_from", "version_to", "node_count", "edge_count", "nodes", "edges"]
    missing = [k for k in required_keys if k not in data]
    if missing:
        print(f"{FAIL} 필수 키 누락: {missing}")
        return False

    print(f"{PASS} kg_generator 성공 (노드: {data['node_count']}, 엣지: {data['edge_count']})")
    return True


def test_notion_updater_no_api(output_dir: Path) -> bool:
    """Step 4: notion_c31_updater.py — API 없이 모듈 임포트 및 UUID 정규화 검증"""
    print(f"\n{INFO} Step 4: notion_c31_updater.py UUID 정규화 테스트")
    test_code = """
import sys
sys.path.insert(0, '.')
from automation.notion_c31_updater import normalize_page_id

# 테스트 케이스
cases = [
    ('34a55ed436f0814d9cffe6a2f0816e29', '34a55ed4-36f0-814d-9cff-e6a2f0816e29'),
    ('34a55ed4-36f0-814d-9cff-e6a2f0816e29', '34a55ed4-36f0-814d-9cff-e6a2f0816e29'),
]
for raw, expected in cases:
    result = normalize_page_id(raw)
    assert result == expected, f'기대: {expected}, 실제: {result}'
print('UUID 정규화 테스트 통과')
"""
    rc, stdout, stderr = run_cmd([sys.executable, "-c", test_code])
    if rc != 0:
        print(f"{FAIL} UUID 정규화 실패: {stderr}")
        return False
    print(f"{PASS} UUID 정규화 테스트 통과")
    return True


def main():
    print("=" * 60)
    print("Section A — 파이프라인 로컬 검증")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmp:
        output_dir = Path(tmp)
        results = [
            test_collector_dry_run(output_dir),
            test_ew_detector(output_dir),
            test_kg_generator(output_dir),
            test_notion_updater_no_api(output_dir),
        ]

    passed = sum(results)
    total = len(results)
    print("\n" + "=" * 60)
    print(f"결과: {passed}/{total} 테스트 통과")
    if passed == total:
        print(f"{PASS} 모든 테스트 통과 — Section A 정상")
        sys.exit(0)
    else:
        print(f"{FAIL} {total - passed}개 테스트 실패")
        sys.exit(1)


if __name__ == "__main__":
    main()
