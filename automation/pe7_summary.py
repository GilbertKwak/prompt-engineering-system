#!/usr/bin/env python3
"""
pe7_summary.py — PE-7 MECE 루프 결과 요약 출력
==============================================
GitHub Actions 워크플로우에서 호출:
  python automation/pe7_summary.py pe7_results.json >> $GITHUB_STEP_SUMMARY

L82 YAML SyntaxError 수정 목적:
  기존 'run: |' 블록 내 python3 -c "...f-string..." 구조에서
  f-string 내부 \"key\" 이스케이프가 YAML 파서를
  크래쉬하는 문제를 별도 파일로 분리하여 해결.
"""

import json
import sys
from pathlib import Path


def summarize(result_path: str) -> None:
    path = Path(result_path)
    if not path.exists():
        print(f"| ⚠️ | (no results file: {result_path}) | - | - |")
        return

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = [data]

    if not data:
        print("| ℹ️ | No records processed | - | - |")
        return

    for r in data:
        status = "✅" if r.get("status") == "done" else "❌"
        idea   = r.get("idea", "?")
        parsed = r.get("parsed", {})
        pe3    = parsed.get("pe3_score", "?")
        irr    = parsed.get("irr", "?")
        print(f"| {status} | {idea} | PE-3: {pe3} | IRR: {irr}% |")


if __name__ == "__main__":
    result_file = sys.argv[1] if len(sys.argv) > 1 else "pe7_results.json"
    summarize(result_file)
