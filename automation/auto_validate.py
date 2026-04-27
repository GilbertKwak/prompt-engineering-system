#!/usr/bin/env python3
"""
auto_validate.py — PE-1 / PE-3 Prompt Validation Script
Repository: GilbertKwak/prompt-engineering-system
Version: v1.0 | 2026-04-27

Usage:
  python automation/auto_validate.py --file prompts/jv_fund/master_v3.md --rules PE-1,PE-3
  python automation/auto_validate.py --dir prompts/jv_fund/ --rules PE-1,PE-3 --output report.json
"""

import argparse
import json
import os
import re
from pathlib import Path
from datetime import datetime


# ─────────────────────────────────────────
# PE-1: Factual Accuracy Rules
# ─────────────────────────────────────────
PE1_RULES = {
    "has_sources": {
        "pattern": r"(출처|Source|Reference|Ref\.|\[\d+\]|https?://)",
        "min_count": 3,
        "message": "PE-1: 출처 3개 이상 필요"
    },
    "has_year_on_numbers": {
        "pattern": r"\d+[%억조만달러원].*20(2[3-9]|[3-9]\d)",
        "min_count": 1,
        "message": "PE-1: 수치 데이터에 연도 기재 필요"
    },
    "has_est_marker": {
        "pattern": r"\(est\.\)|\(추정\)|estimated|추정값",
        "min_count": 0,  # optional but flagged if numbers present without it
        "message": "PE-1: 추정값에 (est.) 표기 권장"
    },
    "no_guaranteed_return": {
        "pattern": r"(보장|guaranteed|확정 수익|무조건)",
        "max_count": 0,
        "message": "PE-1: 보장 수익률 표현 금지 위반"
    }
}

# ─────────────────────────────────────────
# PE-3: Scenario Completeness Rules
# ─────────────────────────────────────────
PE3_RULES = {
    "has_bearish_scenario": {
        "pattern": r"(Bearish|Bear Case|하락|부정적 시나리오|리스크 시나리오|Downside)",
        "min_count": 1,
        "message": "PE-3: Bearish/Downside 시나리오 1개 이상 필요"
    },
    "has_risk_matrix": {
        "pattern": r"(리스크 매트릭스|Risk Matrix|Risk Map|위험 요인|risk factor)",
        "min_count": 1,
        "message": "PE-3: 리스크 매트릭스 항목 필요"
    },
    "has_regulatory_risk": {
        "pattern": r"(규제|Regulatory|법률|AIFMD|SEC|금융위|FSC|제재|Sanction)",
        "min_count": 1,
        "message": "PE-3: 규제/법률 리스크 명시 필요"
    }
}


def validate_file(filepath: str, rules: list) -> dict:
    """Validate a single prompt file against specified rules."""
    path = Path(filepath)
    if not path.exists():
        return {"file": filepath, "status": "ERROR", "message": "File not found"}

    content = path.read_text(encoding="utf-8")
    results = []
    passed = 0
    failed = 0
    warnings = 0

    rule_sets = {}
    if "PE-1" in rules:
        rule_sets["PE-1"] = PE1_RULES
    if "PE-3" in rules:
        rule_sets["PE-3"] = PE3_RULES

    for rule_name, rule_dict in rule_sets.items():
        for check_name, check in rule_dict.items():
            matches = re.findall(check["pattern"], content, re.IGNORECASE)
            count = len(matches)

            # Check minimum count
            if "min_count" in check and count < check["min_count"]:
                results.append({
                    "rule": f"{rule_name}.{check_name}",
                    "status": "FAIL",
                    "message": check["message"],
                    "found": count,
                    "required": check["min_count"]
                })
                failed += 1
            # Check maximum count (e.g., no guaranteed return)
            elif "max_count" in check and count > check["max_count"]:
                results.append({
                    "rule": f"{rule_name}.{check_name}",
                    "status": "FAIL",
                    "message": check["message"],
                    "found": count,
                    "required": f"max {check['max_count']}"
                })
                failed += 1
            else:
                results.append({
                    "rule": f"{rule_name}.{check_name}",
                    "status": "PASS",
                    "message": f"OK ({count} matches)",
                    "found": count
                })
                passed += 1

    overall = "PASS" if failed == 0 else "FAIL"
    score = round((passed / max(passed + failed, 1)) * 100, 1)

    return {
        "file": str(path),
        "status": overall,
        "score": f"{score}%",
        "passed": passed,
        "failed": failed,
        "warnings": warnings,
        "rules_applied": rules,
        "checks": results,
        "validated_at": datetime.utcnow().isoformat() + "Z"
    }


def validate_directory(dirpath: str, rules: list) -> list:
    """Validate all .md files in a directory."""
    results = []
    for md_file in Path(dirpath).glob("**/*.md"):
        results.append(validate_file(str(md_file), rules))
    return results


def print_report(results):
    """Print validation results to console."""
    if isinstance(results, dict):
        results = [results]

    print("\n" + "=" * 60)
    print("  PE Validation Report")
    print(f"  Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 60)

    for r in results:
        icon = "✅" if r["status"] == "PASS" else "❌"
        print(f"\n{icon} {r['file']}")
        print(f"   Status: {r['status']} | Score: {r.get('score', 'N/A')} | "
              f"Passed: {r.get('passed', 0)} | Failed: {r.get('failed', 0)}")
        if r.get("checks"):
            for check in r["checks"]:
                c_icon = "  ✅" if check["status"] == "PASS" else "  ❌"
                print(f"{c_icon} [{check['rule']}] {check['message']}")

    print("\n" + "=" * 60)
    total_pass = sum(1 for r in results if r["status"] == "PASS")
    print(f"  Total: {total_pass}/{len(results)} files passed")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="PE-1/PE-3 Prompt Validation Tool"
    )
    parser.add_argument("--file", help="Validate a single file")
    parser.add_argument("--dir", help="Validate all .md files in directory")
    parser.add_argument(
        "--rules", default="PE-1,PE-3",
        help="Comma-separated rules to apply (default: PE-1,PE-3)"
    )
    parser.add_argument("--output", help="Save JSON report to file")
    parser.add_argument("--quiet", action="store_true", help="Suppress console output")
    args = parser.parse_args()

    rules = [r.strip() for r in args.rules.split(",")]

    if args.file:
        results = validate_file(args.file, rules)
    elif args.dir:
        results = validate_directory(args.dir, rules)
    else:
        # Default: validate all jv_fund prompts
        results = validate_directory("prompts/jv_fund", rules)

    if not args.quiet:
        print_report(results)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"📄 Report saved: {args.output}")

    # Exit code: 0 if all passed, 1 if any failed
    if isinstance(results, list):
        exit_code = 0 if all(r["status"] == "PASS" for r in results) else 1
    else:
        exit_code = 0 if results["status"] == "PASS" else 1
    exit(exit_code)


if __name__ == "__main__":
    main()
