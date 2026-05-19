#!/usr/bin/env python3
"""
Section A·B·C·D 병렬 실행 Runner
ThreadPoolExecutor로 4개 테스트 섹션을 동시 실행 → 결과 집계

Usage:
    python automation/test_runner_parallel.py
    python automation/test_runner_parallel.py --sections A B C   # 선택 실행
    python automation/test_runner_parallel.py --fail-fast         # 첫 실패 시 중단
"""
import sys
import os
import time
import argparse
import unittest
import importlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Tuple

# 스크립트가 있는 디렉토리를 path에 추가
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

# 섹션 정의
SECTIONS: Dict[str, str] = {
    "A": "test_section_a",
    "B": "test_section_b",
    "C": "test_section_c",
    "D": "test_section_d",
}

SECTION_LABELS: Dict[str, str] = {
    "A": "ai_intel_collector    (Perplexity API Mock)",
    "B": "ai_ew_detector        (EW 탐지 로직)",
    "C": "kg_delta_generator    (KG 노드·엣지 생성)",
    "D": "notion_c31_updater    (Notion Block Builder)",
}


def run_section(section_id: str, module_name: str) -> Tuple[str, bool, int, int, float, str]:
    """
    단일 섹션 실행 → (section_id, success, passed, failed, elapsed_sec, error_msg)
    """
    start = time.perf_counter()
    try:
        module = importlib.import_module(module_name)
        importlib.reload(module)  # 캐시 무효화

        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(module)

        stream = open(os.devnull, "w")  # 개별 출력 억제 (집계 출력으로 대체)
        runner = unittest.TextTestRunner(stream=stream, verbosity=0)
        result = runner.run(suite)
        stream.close()

        elapsed = time.perf_counter() - start
        passed = result.testsRun - len(result.failures) - len(result.errors)
        failed = len(result.failures) + len(result.errors)
        success = result.wasSuccessful()

        error_details = ""
        if not success:
            lines = []
            for test, tb in result.failures + result.errors:
                lines.append(f"  FAIL: {test}")
                # traceback 마지막 줄만 표시
                last_line = [l.strip() for l in tb.strip().splitlines() if l.strip()][-1]
                lines.append(f"    → {last_line}")
            error_details = "\n".join(lines)

        return section_id, success, passed, failed, elapsed, error_details

    except Exception as e:
        elapsed = time.perf_counter() - start
        return section_id, False, 0, 1, elapsed, str(e)


def print_header():
    print()
    print("╔" + "═" * 62 + "╗")
    print("║  AI Intel Weekly — Section A·B·C·D 병렬 테스트 러너       ║")
    print("║  GilbertKwak/prompt-engineering-system                   ║")
    print("╚" + "═" * 62 + "╝")
    print()


def print_result_table(results: List[Tuple]):
    print()
    print("─" * 70)
    print(f"  {'섹션':<6} {'모듈':<38} {'통과':>4} {'실패':>4} {'시간':>7}  {'상태'}")
    print("─" * 70)

    total_passed = total_failed = 0
    all_success = True

    sorted_results = sorted(results, key=lambda x: x[0])
    for section_id, success, passed, failed, elapsed, errors in sorted_results:
        label = SECTION_LABELS.get(section_id, section_id)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  [{section_id}]  {label:<38} {passed:>4} {failed:>4} {elapsed:>6.2f}s  {status}")
        if errors:
            for line in errors.splitlines():
                print(f"         {line}")
        total_passed += passed
        total_failed += failed
        if not success:
            all_success = False

    print("─" * 70)
    overall = "✅ ALL PASSED" if all_success else "❌ SOME FAILED"
    print(f"  {'TOTAL':<44} {total_passed:>4} {total_failed:>4}          {overall}")
    print("─" * 70)
    print()
    return all_success


def main():
    parser = argparse.ArgumentParser(
        description="Section A·B·C·D 병렬 테스트 실행기"
    )
    parser.add_argument(
        "--sections", nargs="+", choices=["A", "B", "C", "D"],
        default=["A", "B", "C", "D"],
        help="실행할 섹션 (기본: 전체)",
    )
    parser.add_argument(
        "--fail-fast", action="store_true",
        help="첫 실패 섹션 발견 시 나머지 취소",
    )
    parser.add_argument(
        "--sequential", action="store_true",
        help="병렬 대신 순차 실행 (디버그용)",
    )
    args = parser.parse_args()

    print_header()

    selected = {s: SECTIONS[s] for s in args.sections}
    print(f"  실행 섹션: {', '.join(args.sections)}  "
          f"| 모드: {'순차' if args.sequential else '병렬'}  "
          f"| fail-fast: {args.fail_fast}")
    print()

    results = []
    wall_start = time.perf_counter()

    if args.sequential:
        # 순차 실행 (디버그)
        for sid, mod in selected.items():
            print(f"  ▶ Section {sid} 실행 중...", end=" ", flush=True)
            r = run_section(sid, mod)
            results.append(r)
            print("완료" if r[1] else "실패")
            if args.fail_fast and not r[1]:
                print("  ⚠ fail-fast: 나머지 섹션 취소")
                break
    else:
        # ThreadPoolExecutor 병렬 실행
        futures = {}
        with ThreadPoolExecutor(max_workers=4) as executor:
            for sid, mod in selected.items():
                future = executor.submit(run_section, sid, mod)
                futures[future] = sid
                print(f"  ▶ Section {sid} 병렬 시작")

            print()
            for future in as_completed(futures):
                r = future.result()
                results.append(r)
                status = "✅" if r[1] else "❌"
                print(f"  {status} Section {r[0]} 완료  ({r[4]:.2f}s)")

                if args.fail_fast and not r[1]:
                    # 진행 중인 나머지 Future 취소
                    for f in futures:
                        f.cancel()
                    print("  ⚠ fail-fast: 나머지 취소")
                    break

    wall_elapsed = time.perf_counter() - wall_start
    print(f"\n  총 wall-clock 시간: {wall_elapsed:.2f}s")

    all_ok = print_result_table(results)

    if all_ok:
        print("  🎉 모든 섹션 통과 — AI Intel Weekly 스크립트 검증 완료")
    else:
        print("  ⚠  실패한 섹션이 있습니다. 위 에러 메시지를 확인하세요.")
        print("  힌트: --sequential 옵션으로 순차 실행하면 디버그가 쉽습니다.")

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
