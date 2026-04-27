#!/usr/bin/env python3
"""
auto_validate.py — JV Fund Prompt PE-1/PE-3/PE-5 Validation Script
Version: 1.0 | Date: 2026-04-28
Author: Gilbert

Usage:
  python auto_validate.py --file <path> --rules PE-1,PE-3,PE-5
  python auto_validate.py --dir <directory> --rules PE-1,PE-3
  python auto_validate.py --file <path> --rules PE-1 --output report.json
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


# ── Validation Rule Definitions ────────────────────────────────────────────

PE1_CHECKS = {
    "numeric_source": {
        "pattern": r"\$[\d\.]+[BMT].*?(?:Source|출처|\(est\.\)|IDC|Gartner|McKinsey|IEA|DOE|KIER)",
        "description": "수치에 출처 명시",
        "weight": 0.35,
    },
    "year_tag": {
        "pattern": r"20(2[3-9]|3[0-9])",
        "description": "연도 기재",
        "weight": 0.25,
    },
    "est_tag": {
        "pattern": r"\(est\.\)|추정|estimated",
        "description": "추정값 표기",
        "weight": 0.20,
    },
    "source_count": {
        "description": "3개 이상 독립 출처",
        "weight": 0.20,
    },
}

PE3_CHECKS = {
    "bull_case": {
        "pattern": r"낙관|Bull Case|Upside|optimistic",
        "description": "낙관 시나리오",
        "weight": 0.30,
    },
    "base_case": {
        "pattern": r"기준|Base Case|Baseline|base scenario",
        "description": "기준 시나리오",
        "weight": 0.30,
    },
    "bear_case": {
        "pattern": r"비관|Bear Case|Downside|pessimistic|리스크",
        "description": "비관 시나리오",
        "weight": 0.25,
    },
    "counter_argument": {
        "pattern": r"반론|반대|그러나|However|On the other hand|단점|한계",
        "description": "반대 의견/반론",
        "weight": 0.15,
    },
}

PE5_CHECKS = {
    "task_chain": {
        "pattern": r"Step [1-5]|TASK CHAIN",
        "description": "Task Chain 5단계",
        "weight": 0.20,
    },
    "json_output": {
        "pattern": r"```json|\{\s*\"summary\"",
        "description": "JSON 출력 포맷",
        "weight": 0.20,
    },
    "md_table": {
        "pattern": r"\|.*\|.*\|\n\|[-:]+\|",
        "description": "MD 테이블",
        "weight": 0.15,
    },
    "github_command": {
        "pattern": r"gh issue create",
        "description": "GitHub Issue 명령어",
        "weight": 0.20,
    },
    "roadmap": {
        "pattern": r"90일|90.days|6개월|6.months|1년|1.year",
        "description": "실행 로드맵",
        "weight": 0.25,
    },
}

RULE_MAP = {"PE-1": PE1_CHECKS, "PE-3": PE3_CHECKS, "PE-5": PE5_CHECKS}


# ── Core Validation Logic ──────────────────────────────────────────────────

def validate_file(filepath: str, rules: list[str]) -> dict:
    path = Path(filepath)
    if not path.exists():
        return {"error": f"File not found: {filepath}"}

    content = path.read_text(encoding="utf-8")
    results = {
        "file": str(path),
        "timestamp": datetime.now().isoformat(),
        "rules": {},
        "overall_score": 0.0,
        "status": "",
    }

    total_weighted = 0.0
    total_weight = 0.0

    for rule_name in rules:
        rule_name = rule_name.strip()
        if rule_name not in RULE_MAP:
            print(f"  ⚠️  Unknown rule: {rule_name}")
            continue

        checks = RULE_MAP[rule_name]
        rule_result = {"checks": {}, "score": 0.0, "pass": False}
        rule_score = 0.0
        rule_weight_sum = 0.0

        # Special: source_count for PE-1
        if rule_name == "PE-1":
            sources = re.findall(
                r"(?:IDC|Gartner|McKinsey|IEA|DOE|KIER|Bloomberg|SEMI|Yole|TrendForce)",
                content, re.IGNORECASE
            )
            unique_sources = len(set(s.lower() for s in sources))
            checks["source_count"]["found"] = unique_sources >= 3

        for check_name, check in checks.items():
            w = check["weight"]
            if check_name == "source_count":
                passed = check.get("found", False)
            else:
                pattern = check.get("pattern", "")
                passed = bool(re.search(pattern, content, re.IGNORECASE | re.MULTILINE))

            rule_result["checks"][check_name] = {
                "description": check["description"],
                "passed": passed,
                "weight": w,
            }
            if passed:
                rule_score += w
            rule_weight_sum += w

        normalized = (rule_score / rule_weight_sum * 100) if rule_weight_sum > 0 else 0
        rule_result["score"] = round(normalized, 1)
        rule_result["pass"] = normalized >= 70
        results["rules"][rule_name] = rule_result
        total_weighted += normalized
        total_weight += 1

    overall = (total_weighted / total_weight) if total_weight > 0 else 0
    results["overall_score"] = round(overall, 1)

    if overall >= 90:
        results["status"] = "✅ PASS"
    elif overall >= 70:
        results["status"] = "⚠️  REVIEW"
    elif overall >= 50:
        results["status"] = "🔄 REWORK"
    else:
        results["status"] = "❌ FAIL"

    return results


def print_report(results: dict) -> None:
    if "error" in results:
        print(f"ERROR: {results['error']}")
        return

    print(f"\n{'='*60}")
    print(f"  Validation Report — {Path(results['file']).name}")
    print(f"  {results['timestamp']}")
    print(f"{'='*60}")

    for rule_name, rule_data in results["rules"].items():
        status = "✅" if rule_data["pass"] else "❌"
        print(f"\n  {status} {rule_name} — Score: {rule_data['score']}%")
        for check_name, check in rule_data["checks"].items():
            icon = "  ✓" if check["passed"] else "  ✗"
            print(f"    {icon} [{check['weight']:.2f}] {check['description']}")

    print(f"\n{'─'*60}")
    print(f"  Overall Score : {results['overall_score']}%")
    print(f"  Status        : {results['status']}")
    print(f"{'='*60}\n")


# ── CLI Entry Point ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="JV Fund Prompt Validator (PE-1/PE-3/PE-5)"
    )
    parser.add_argument("--file", help="단일 파일 경로")
    parser.add_argument("--dir", help="디렉터리 (*.md 전체 검증)")
    parser.add_argument(
        "--rules", default="PE-1,PE-3,PE-5",
        help="검증 룰 (쉼표 구분, 기본: PE-1,PE-3,PE-5)"
    )
    parser.add_argument("--output", help="JSON 출력 파일 경로")
    args = parser.parse_args()

    rules = [r.strip() for r in args.rules.split(",")]
    all_results = []

    if args.file:
        res = validate_file(args.file, rules)
        print_report(res)
        all_results.append(res)

    elif args.dir:
        md_files = list(Path(args.dir).glob("*.md"))
        if not md_files:
            print(f"No .md files found in {args.dir}")
            sys.exit(1)
        for f in md_files:
            res = validate_file(str(f), rules)
            print_report(res)
            all_results.append(res)
    else:
        parser.print_help()
        sys.exit(1)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(all_results if len(all_results) > 1 else all_results[0],
                      f, ensure_ascii=False, indent=2)
        print(f"📄 Report saved: {args.output}")

    # Exit code: 1 if any file fails
    failed = [r for r in all_results if "❌" in r.get("status", "") or "🔄" in r.get("status", "")]
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
