#!/usr/bin/env python3
"""
auto_validate.py — JV Fund Prompt PE-1/PE-3 자동 검증기
Usage: python automation/auto_validate.py --file <path> --rules PE-1,PE-3
Version: 1.0 | Updated: 2026-04-27
"""

import argparse
import re
import json
import sys
from pathlib import Path
from datetime import datetime

# ── PE-1 검증 규칙 ──────────────────────────────────────────────────
PE1_RULES = {
    "PE-1-01": {
        "name": "수치 데이터 출처+연도 명시",
        "pattern": r"\$[\d,.]+[BMK]?.*\d{4}",
        "forbidden": [],
        "description": "금액/수치 뒤 출처 또는 연도 필요"
    },
    "PE-1-02": {
        "name": "추정값 태깅",
        "pattern": r"\(est\.\)",
        "forbidden": [],
        "description": "추정값에 (est.) 태깅"
    },
    "PE-1-03": {
        "name": "보장 수익률 표현 금지",
        "pattern": None,
        "forbidden": ["guaranteed return", "확정 수익", "guaranteed profit", "보장 수익"],
        "description": "보장/확정 수익 표현 금지"
    },
    "PE-1-04": {
        "name": "인용 데이터 최신성",
        "pattern": r"202[4-6]",
        "forbidden": [],
        "description": "최근 2년 이내 데이터 포함 권장"
    },
}

# ── PE-3 검증 규칙 ──────────────────────────────────────────────────
PE3_RULES = {
    "PE-3-01": {
        "name": "베어리시 시나리오 포함",
        "keywords": ["bearish", "downside", "비관", "리스크 시나리오", "worst case", "하락 시나리오"],
        "description": "비관 시나리오 최소 1개 포함"
    },
    "PE-3-02": {
        "name": "기술 리스크 명시",
        "keywords": ["TRL", "기술 리스크", "technical risk", "기술 성숙도"],
        "description": "기술 리스크 항목 포함"
    },
    "PE-3-03": {
        "name": "수탁자 의무 플래깅",
        "keywords": ["fiduciary", "수탁자", "신탁", "LP 보호"],
        "description": "수탁자 의무 관련 위험 언급"
    },
    "PE-3-04": {
        "name": "규제·지정학 리스크",
        "keywords": ["regulatory", "규제", "geopolitical", "지정학", "수출 규제", "ITAR"],
        "description": "규제 또는 지정학 리스크 항목"
    },
    "PE-3-05": {
        "name": "LP 이해충돌 명시",
        "keywords": ["이해충돌", "conflict of interest", "LP alignment", "LP 이해"],
        "description": "LP 이해충돌 가능성 기술"
    },
}


def validate_pe1(content: str) -> dict:
    results = {}
    for rule_id, rule in PE1_RULES.items():
        passed = True
        detail = ""
        # 금지 표현 검사
        for forbidden in rule.get("forbidden", []):
            if forbidden.lower() in content.lower():
                passed = False
                detail = f"금지 표현 발견: '{forbidden}'"
                break
        # 패턴 존재 여부 (informational — 없어도 경고만)
        if passed and rule.get("pattern"):
            if not re.search(rule["pattern"], content):
                detail = f"권장 패턴 미발견 (참고용)"
        results[rule_id] = {"name": rule["name"], "passed": passed, "detail": detail or "OK"}
    return results


def validate_pe3(content: str) -> dict:
    results = {}
    for rule_id, rule in PE3_RULES.items():
        found = any(kw.lower() in content.lower() for kw in rule["keywords"])
        results[rule_id] = {
            "name": rule["name"],
            "passed": found,
            "detail": "OK" if found else f"키워드 미발견: {rule['keywords'][:3]}"
        }
    return results


def run_validation(filepath: str, rules: list) -> dict:
    path = Path(filepath)
    if not path.exists():
        print(f"[ERROR] 파일 없음: {filepath}")
        sys.exit(1)

    content = path.read_text(encoding="utf-8")
    report = {
        "file": filepath,
        "version": "auto_validate v1.0",
        "timestamp": datetime.now().isoformat(),
        "results": {}
    }

    if "PE-1" in rules:
        report["results"]["PE-1"] = validate_pe1(content)
    if "PE-3" in rules:
        report["results"]["PE-3"] = validate_pe3(content)

    # 집계
    total = sum(len(v) for v in report["results"].values())
    passed = sum(
        1 for group in report["results"].values()
        for item in group.values() if item["passed"]
    )
    report["summary"] = {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "score": f"{passed}/{total}",
        "status": "✅ PASS" if passed == total else f"⚠️  WARNING ({total - passed} issues)"
    }
    return report


def print_report(report: dict):
    print("\n" + "═" * 60)
    print(f"  JV Fund Prompt 자동 검증 리포트")
    print(f"  파일: {report['file']}")
    print(f"  시각: {report['timestamp']}")
    print("═" * 60)
    for group_name, rules in report["results"].items():
        print(f"\n[{group_name}]")
        for rule_id, result in rules.items():
            icon = "✅" if result["passed"] else "❌"
            print(f"  {icon} {rule_id}: {result['name']}")
            if result["detail"] != "OK":
                print(f"       → {result['detail']}")
    s = report["summary"]
    print(f"\n{'═' * 60}")
    print(f"  결과: {s['status']}  ({s['score']} 항목 통과)")
    print("═" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="JV Fund Prompt PE-1/PE-3 자동 검증")
    parser.add_argument("--file", required=True, help="검증할 프롬프트 파일 경로")
    parser.add_argument("--rules", default="PE-1,PE-3", help="적용 규칙 (예: PE-1,PE-3)")
    parser.add_argument("--output", default=None, help="JSON 리포트 출력 경로 (선택)")
    args = parser.parse_args()

    rules = [r.strip() for r in args.rules.split(",")]
    report = run_validation(args.file, rules)
    print_report(report)

    if args.output:
        Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  JSON 리포트 저장: {args.output}")

    sys.exit(0 if report["summary"]["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
