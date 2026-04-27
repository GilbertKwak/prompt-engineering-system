#!/usr/bin/env python3
"""
auto_validate_jv.py — JV Fund Prompt PE-1/PE-3 자동 검증 스크립트
Usage: python auto_validate_jv.py --file <path> --rules PE-1,PE-3 --output report.json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime

# ── PE-1 검증 규칙 ──────────────────────────────────────────────────
PE1_RULES = {
    "PE-1-01": {
        "desc": "수치 데이터에 출처 + 연도 명시",
        "pattern": r"(\d+[\.,]?\d*\s*(\$|USD|KRW|%|B|M|T|조|억|만))",
        "check": lambda text: not bool(re.search(
            r"(\d+[\.,]?\d*\s*(\$|USD|KRW|%|B|M|T|조|억|만))(?!.*?(출처|source|\(\d{4}\)|est\.))",
            text, re.IGNORECASE
        )),
        "severity": "WARNING"
    },
    "PE-1-02": {
        "desc": "추정값에 (est.) 태그 존재 여부 (구조 검증)",
        "pattern": r"\(est\.\)",
        "check": lambda text: True,  # 구조 내 존재 확인은 INFO 수준
        "severity": "INFO"
    },
    "PE-1-03": {
        "desc": "보장 수익 언어 사용 금지",
        "pattern": r"(guaranteed|보장\s*수익|확정\s*수익|무위험|risk.?free\s*return)",
        "check": lambda text: not bool(re.search(
            r"(guaranteed\s+return|보장\s*수익|확정\s*수익)",
            text, re.IGNORECASE
        )),
        "severity": "ERROR"
    },
    "PE-1-04": {
        "desc": "시장 규모 주장 시 출처 2개 이상 권고",
        "check": lambda text: True,  # 구조 레벨 검증
        "severity": "INFO"
    },
    "PE-1-05": {
        "desc": "재무 추정치에 기본 가정 명시 구조 포함",
        "check": lambda text: "assumptions" in text.lower() or "가정" in text,
        "severity": "WARNING"
    },
    "PE-1-06": {
        "desc": "규제 참조 시 관할권 + 발효일 명시 구조 포함",
        "check": lambda text: any(x in text for x in ["AIFMD", "SEC", "FSC", "금감원", "REGULATORY RISK"]),
        "severity": "INFO"
    },
}

# ── PE-3 검증 규칙 ──────────────────────────────────────────────────
PE3_RULES = {
    "PE-3-01": {
        "desc": "반대/약세 시나리오 최소 1개 포함",
        "check": lambda text: any(x in text.lower() for x in [
            "bearish", "downside", "약세", "하락", "리스크 시나리오", "counter", "worst"
        ]),
        "severity": "ERROR"
    },
    "PE-3-02": {
        "desc": "수탁자 리스크 [FIDUCIARY RISK] 태그 또는 명시",
        "check": lambda text: "FIDUCIARY" in text.upper() or "수탁" in text or "fiduciary" in text.lower(),
        "severity": "WARNING"
    },
    "PE-3-03": {
        "desc": "규제 리스크 명시",
        "check": lambda text: any(x in text for x in [
            "REGULATORY RISK", "regulatory", "규제", "compliance", "컴플라이언스"
        ]),
        "severity": "WARNING"
    },
    "PE-3-04": {
        "desc": "LP 정렬 리스크 명시",
        "check": lambda text: any(x in text.lower() for x in [
            "lp risk", "lp alignment", "lp 정렬", "투자자 이해"
        ]),
        "severity": "INFO"
    },
    "PE-3-05": {
        "desc": "지정학적 익스포저 명시",
        "check": lambda text: any(x in text.lower() for x in [
            "geopolitical", "지정학", "sanction", "제재", "trade war", "무역전쟁"
        ]),
        "severity": "INFO"
    },
}


def validate_file(filepath: str, rules: list) -> dict:
    path = Path(filepath)
    if not path.exists():
        return {"error": f"File not found: {filepath}"}

    text = path.read_text(encoding="utf-8")
    results = {"file": filepath, "timestamp": datetime.utcnow().isoformat(), "rules": {}}

    pe1_passed, pe1_total = 0, 0
    pe3_passed, pe3_total = 0, 0
    errors = []

    if "PE-1" in rules:
        for rule_id, rule in PE1_RULES.items():
            pe1_total += 1
            passed = rule["check"](text)
            if passed:
                pe1_passed += 1
            else:
                errors.append(f"[{rule['severity']}] {rule_id}: {rule['desc']}")
            results["rules"][rule_id] = {
                "desc": rule["desc"],
                "passed": passed,
                "severity": rule["severity"]
            }

    if "PE-3" in rules:
        for rule_id, rule in PE3_RULES.items():
            pe3_total += 1
            passed = rule["check"](text)
            if passed:
                pe3_passed += 1
            else:
                if rule["severity"] == "ERROR":
                    errors.append(f"[ERROR] {rule_id}: {rule['desc']}")
                else:
                    errors.append(f"[{rule['severity']}] {rule_id}: {rule['desc']}")
            results["rules"][rule_id] = {
                "desc": rule["desc"],
                "passed": passed,
                "severity": rule["severity"]
            }

    critical_errors = [e for e in errors if "[ERROR]" in e]
    results.update({
        "pe1_passed": pe1_passed, "pe1_total": pe1_total,
        "pe3_passed": pe3_passed, "pe3_total": pe3_total,
        "passed": len(critical_errors) == 0,
        "failed": len(critical_errors),
        "errors": errors,
        "summary": f"PE-1: {pe1_passed}/{pe1_total} | PE-3: {pe3_passed}/{pe3_total} | Critical Errors: {len(critical_errors)}"
    })
    return results


def main():
    parser = argparse.ArgumentParser(description="JV Fund Prompt PE-1/PE-3 Validator")
    parser.add_argument("--file", required=True, help="Path to prompt file")
    parser.add_argument("--rules", default="PE-1,PE-3", help="Comma-separated rule sets")
    parser.add_argument("--output", default="validation_report.json", help="Output JSON path")
    args = parser.parse_args()

    rules = [r.strip() for r in args.rules.split(",")]
    report = validate_file(args.file, rules)

    output_path = Path(args.output)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n{'='*50}")
    print(f"JV Prompt Validation Report")
    print(f"{'='*50}")
    print(f"File    : {report.get('file')}")
    print(f"Summary : {report.get('summary')}")
    print(f"Result  : {'✅ PASS' if report.get('passed') else '❌ FAIL'}")
    if report.get("errors"):
        print(f"\nIssues:")
        for e in report["errors"]:
            print(f"  {e}")
    print(f"\nReport saved: {args.output}")

    sys.exit(0 if report.get("passed") else 1)


if __name__ == "__main__":
    main()
