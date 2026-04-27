#!/usr/bin/env python3
"""
auto_validate_jv.py — JV Fund Prompt Auto-Validation Engine
Version: 1.0.0 | 2026-04-27
Author: Gilbert Kwak
SSoT: github.com/GilbertKwak/prompt-engineering-system

Validation Rules:
  PE-1: Citation completeness (sources + years + est. markers)
  PE-3: Counter-scenario inclusion (Bear Case)
  PE-5: 7-Step Framework completeness

Usage:
  python automation/auto_validate_jv.py --file <path> [--rules PE-1,PE-3,PE-5] [--verbose]
"""

import argparse
import re
import sys
import json
from pathlib import Path
from datetime import datetime

# ─── Rule Definitions ─────────────────────────────────────────────────────────

PE1_PATTERNS = {
    "year_citation":    r"\b(20[0-9]{2})\b",
    "source_marker":    r"\(출처[:\s]|Source:|\[\d+\]|\(est\.\)",
    "numeric_data":     r"\$[\d,\.]+[BMK]?|[\d\.]+%|[\d,]+ units",
}

PE3_PATTERNS = {
    "bear_case":        r"Bear Case|약세 시나리오|하락 시나리오|리스크 시나리오",
    "bull_case":        r"Bull Case|강세 시나리오|상승 시나리오",
    "trigger":          r"트리거|Trigger|조건|Condition",
}

PE5_STEPS = [
    ("Step 1", ["TAM", "SAM", "SOM", "시장 규모", "Market"]),
    ("Step 2", ["Competitive", "경쟁", "플레이어", "Player"]),
    ("Step 3", ["Partner", "파트너", "후보", "Candidate"]),
    ("Step 4", ["JV Structure", "지분", "거버넌스", "Governance"]),
    ("Step 5", ["Risk", "리스크", "위험"]),
    ("Step 6", ["IRR", "NPV", "Financial", "재무"]),
    ("Step 7", ["Roadmap", "로드맵", "실행", "Execution"]),
]

# ─── Validators ───────────────────────────────────────────────────────────────

def validate_pe1(content: str) -> dict:
    """PE-1: Citation & Source completeness"""
    results = {"rule": "PE-1", "passed": False, "score": 0, "issues": [], "details": {}}

    # Check year citations
    years = re.findall(PE1_PATTERNS["year_citation"], content)
    results["details"]["years_found"] = list(set(years))

    # Check source markers
    sources = re.findall(PE1_PATTERNS["source_marker"], content)
    results["details"]["source_markers"] = len(sources)

    # Check numeric data
    numerics = re.findall(PE1_PATTERNS["numeric_data"], content)
    results["details"]["numeric_data_count"] = len(numerics)

    # Check est. markers for estimates
    est_count = len(re.findall(r"\(est\.\)", content))
    results["details"]["est_markers"] = est_count

    # Scoring
    score = 0
    if len(years) >= 3:      score += 25; 
    else: results["issues"].append(f"연도 인용 부족: {len(years)}개 (최소 3개 필요)")
    
    if len(sources) >= 3:    score += 25;
    else: results["issues"].append(f"출처 마커 부족: {len(sources)}개 (최소 3개 필요)")
    
    if len(numerics) >= 2:   score += 25;
    else: results["issues"].append(f"수치 데이터 부족: {len(numerics)}개 (최소 2개 필요)")
    
    if est_count > 0 or len(numerics) == 0:  score += 25;  # Pass if no estimates needed
    
    results["score"] = score
    results["passed"] = score >= 75
    return results


def validate_pe3(content: str) -> dict:
    """PE-3: Counter-scenario (Bear Case) inclusion"""
    results = {"rule": "PE-3", "passed": False, "score": 0, "issues": [], "details": {}}

    bear = bool(re.search(PE3_PATTERNS["bear_case"], content, re.IGNORECASE))
    bull = bool(re.search(PE3_PATTERNS["bull_case"], content, re.IGNORECASE))
    trigger = bool(re.search(PE3_PATTERNS["trigger"], content, re.IGNORECASE))

    results["details"] = {"bear_case": bear, "bull_case": bull, "trigger_conditions": trigger}

    score = 0
    if bear:    score += 50;
    else: results["issues"].append("Bear Case 시나리오 없음 (필수)")
    
    if bull:    score += 25;
    else: results["issues"].append("Bull Case 시나리오 없음 (권장)")
    
    if trigger: score += 25;
    else: results["issues"].append("트리거 조건 명시 없음 (권장)")

    results["score"] = score
    results["passed"] = score >= 50  # Bear Case 필수
    return results


def validate_pe5(content: str) -> dict:
    """PE-5: 7-Step Framework completeness"""
    results = {"rule": "PE-5", "passed": False, "score": 0, "issues": [], "details": {}}

    covered = []
    missing = []
    for step_name, keywords in PE5_STEPS:
        found = any(re.search(kw, content, re.IGNORECASE) for kw in keywords)
        if found:
            covered.append(step_name)
        else:
            missing.append(step_name)
            results["issues"].append(f"{step_name} 커버리지 부족 (키워드: {', '.join(keywords[:2])} 등)")

    coverage_pct = int(len(covered) / len(PE5_STEPS) * 100)
    results["details"] = {"covered_steps": covered, "missing_steps": missing, "coverage_pct": coverage_pct}
    results["score"] = coverage_pct
    results["passed"] = coverage_pct >= 70
    return results


# ─── Report Generator ─────────────────────────────────────────────────────────

def generate_report(file_path: str, rules: list, verbose: bool = False) -> dict:
    path = Path(file_path)
    if not path.exists():
        print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
        sys.exit(1)

    content = path.read_text(encoding="utf-8")
    report = {
        "file": str(path),
        "timestamp": datetime.now().isoformat(),
        "rules_applied": rules,
        "results": {},
        "overall_passed": False,
        "summary": "",
    }

    validators = {"PE-1": validate_pe1, "PE-3": validate_pe3, "PE-5": validate_pe5}

    all_passed = True
    for rule in rules:
        if rule in validators:
            result = validators[rule](content)
            report["results"][rule] = result
            if not result["passed"]:
                all_passed = False
            if verbose:
                status = "✅ PASS" if result["passed"] else "❌ FAIL"
                print(f"\n{status} {rule} — Score: {result['score']}/100")
                if result["issues"]:
                    for issue in result["issues"]:
                        print(f"  ⚠️  {issue}")

    report["overall_passed"] = all_passed
    passed_count = sum(1 for r in report["results"].values() if r["passed"])
    total = len(rules)
    report["summary"] = f"{passed_count}/{total} rules passed"

    return report


# ─── CLI Entry Point ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="JV Fund Prompt Auto-Validation (PE-1/PE-3/PE-5)"
    )
    parser.add_argument("--file",    required=True, help="검증할 파일 경로")
    parser.add_argument("--rules",   default="PE-1,PE-3,PE-5", help="적용 룰 (쉼표 구분)")
    parser.add_argument("--output",  default=None, help="결과 JSON 저장 경로")
    parser.add_argument("--verbose", action="store_true", help="상세 출력")
    args = parser.parse_args()

    rules = [r.strip() for r in args.rules.split(",")]

    print(f"\n🔍 JV Prompt Validator v1.0")
    print(f"📄 File  : {args.file}")
    print(f"📏 Rules : {', '.join(rules)}")
    print("=" * 50)

    report = generate_report(args.file, rules, verbose=args.verbose)

    print(f"\n{'='*50}")
    overall = "✅ ALL PASSED" if report["overall_passed"] else "❌ VALIDATION FAILED"
    print(f"Result  : {overall}")
    print(f"Summary : {report['summary']}")
    print(f"Time    : {report['timestamp']}")

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2))
        print(f"📁 Report saved: {args.output}")

    sys.exit(0 if report["overall_passed"] else 1)


if __name__ == "__main__":
    main()
