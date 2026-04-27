#!/usr/bin/env python3
"""
auto_validate.py — PE-1/PE-3 자동 검증 스크립트
prompt-engineering-system/automation/auto_validate.py
Version: 2.0 | Updated: 2026-04-27 | Author: GilbertKwak
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime


# ─── PE-1 검증 규칙 ───────────────────────────────────────────────

PE1_RULES = {
    "citation_present": {
        "pattern": r"\[.+?,\s*\d{4}\]",
        "description": "출처 명시 (형식: [출처명, YYYY])",
        "required": True,
        "min_count": 3
    },
    "est_marking": {
        "pattern": r"\(est\.\)",
        "description": "추정값 (est.) 표기",
        "required": False
    },
    "recency_check": {
        "pattern": r"20(2[4-6])",
        "description": "최근 2년 이내 데이터 사용",
        "required": False
    },
    "param_domain": {
        "pattern": r"DOMAIN:",
        "description": "DOMAIN 파라미터 존재",
        "required": True
    },
    "param_stage": {
        "pattern": r"STAGE:",
        "description": "STAGE 파라미터 존재",
        "required": True
    },
    "param_lang": {
        "pattern": r"LANG:",
        "description": "LANG 파라미터 존재",
        "required": True
    },
    "output_format": {
        "pattern": r"OUTPUT FORMAT",
        "description": "출력 포맷 정의 존재",
        "required": True
    },
    "validation_section": {
        "pattern": r"VALIDATION RULES",
        "description": "검증 규칙 섹션 존재",
        "required": True
    },
    "bilingual_summary": {
        "pattern": r"(ko|en).*summary|executive_summary",
        "description": "KR+EN 이중 언어 요약",
        "required": False
    },
    "no_guarantee_language": {
        "pattern": r"(보장하지 않음|수익을 보장|guaranteed return)",
        "description": "수익 보장 금지 문구 포함",
        "required": True
    }
}


# ─── PE-3 검증 규칙 ───────────────────────────────────────────────

PE3_RULES = {
    "counter_scenario": {
        "pattern": r"counter_scenario|반대 시나리오|PE-3",
        "description": "반대 시나리오 섹션 존재",
        "required": True,
        "weight": 20
    },
    "stress_scenarios": {
        "pattern": r"Scenario (1|2|3|A|B|C)|Base.*Stress|Tail Risk",
        "description": "스트레스 시나리오 (3종 이상)",
        "required": True,
        "weight": 25
    },
    "assumptions_explicit": {
        "pattern": r"assumption|가정",
        "description": "가정 명시",
        "required": True,
        "weight": 20
    },
    "geopolitical_risk": {
        "pattern": r"지정학|미중|Geopolitical|CFIUS|수출통제",
        "description": "지정학 리스크 포함",
        "required": True,
        "weight": 15
    },
    "downside_protection": {
        "pattern": r"하방 보호|downside|우선주|Anti-Dilution|Liquidation",
        "description": "하방 보호 구조",
        "required": False,
        "weight": 10
    },
    "risk_quantification": {
        "pattern": r"H/M/L|High.*Medium.*Low|발생확률|probability.*impact",
        "description": "리스크 정량화 (H/M/L)",
        "required": True,
        "weight": 10
    }
}


# ─── 검증 엔진 ────────────────────────────────────────────────────

def validate_file(filepath: str, rules_to_apply: list) -> dict:
    path = Path(filepath)
    if not path.exists():
        return {"error": f"파일 없음: {filepath}"}

    content = path.read_text(encoding="utf-8")
    results = {
        "file": filepath,
        "validation_date": datetime.now().isoformat(),
        "rules_applied": rules_to_apply,
        "pe1": {"passed": 0, "failed": 0, "details": [], "compliance_rate": 0.0},
        "pe3": {"score": 0, "max_score": 100, "details": []},
        "overall_status": "UNKNOWN"
    }

    # PE-1 검증
    if "PE-1" in rules_to_apply:
        total_required = sum(1 for r in PE1_RULES.values() if r.get("required"))
        passed_required = 0

        for rule_name, rule in PE1_RULES.items():
            flags = re.IGNORECASE | re.DOTALL
            matches = re.findall(rule["pattern"], content, flags)
            passed = len(matches) > 0
            if rule_name == "citation_present":
                passed = len(matches) >= rule.get("min_count", 1)

            detail = {
                "rule": rule_name,
                "description": rule["description"],
                "required": rule.get("required", False),
                "passed": passed,
                "match_count": len(matches)
            }
            results["pe1"]["details"].append(detail)

            if passed:
                results["pe1"]["passed"] += 1
                if rule.get("required"):
                    passed_required += 1
            else:
                if rule.get("required"):
                    results["pe1"]["failed"] += 1

        compliance = (passed_required / total_required * 100) if total_required > 0 else 0
        results["pe1"]["compliance_rate"] = round(compliance, 1)

    # PE-3 검증
    if "PE-3" in rules_to_apply:
        total_score = 0
        for rule_name, rule in PE3_RULES.items():
            flags = re.IGNORECASE | re.DOTALL
            matches = re.findall(rule["pattern"], content, flags)
            passed = len(matches) > 0
            weight = rule.get("weight", 10)
            earned = weight if passed else 0
            total_score += earned

            results["pe3"]["details"].append({
                "rule": rule_name,
                "description": rule["description"],
                "passed": passed,
                "score": earned,
                "max_score": weight
            })

        results["pe3"]["score"] = total_score

    # 최종 상태
    pe1_ok = results["pe1"]["compliance_rate"] >= 80 if "PE-1" in rules_to_apply else True
    pe3_ok = results["pe3"]["score"] >= 70 if "PE-3" in rules_to_apply else True
    results["overall_status"] = "PASS" if (pe1_ok and pe3_ok) else "FAIL"

    return results


def print_report(results: dict):
    print("\n" + "="*60)
    print(f"📋 검증 보고서: {results['file']}")
    print(f"📅 날짜: {results['validation_date']}")
    print("="*60)

    if "PE-1" in results["rules_applied"]:
        pe1 = results["pe1"]
        status = "✅ PASS" if pe1["compliance_rate"] >= 80 else "❌ FAIL"
        print(f"\n🔍 PE-1 검증 {status}")
        print(f"   준수율: {pe1['compliance_rate']}% (통과: {pe1['passed']}, 실패: {pe1['failed']})")
        for d in pe1["details"]:
            icon = "✅" if d["passed"] else ("❌" if d["required"] else "⚠️")
            print(f"   {icon} {d['description']} ({d['match_count']}건)")

    if "PE-3" in results["rules_applied"]:
        pe3 = results["pe3"]
        status = "✅ PASS" if pe3["score"] >= 70 else "❌ FAIL"
        print(f"\n🎯 PE-3 검증 {status}")
        print(f"   점수: {pe3['score']}/{pe3['max_score']}")
        for d in pe3["details"]:
            icon = "✅" if d["passed"] else "❌"
            print(f"   {icon} {d['description']} ({d['score']}/{d['max_score']}점)")

    final = "✅ 전체 PASS" if results["overall_status"] == "PASS" else "❌ 전체 FAIL"
    print(f"\n{'='*60}")
    print(f"최종 결과: {final}")
    print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="PE-1/PE-3 프롬프트 자동 검증")
    parser.add_argument("--file", required=True, help="검증 대상 파일 경로")
    parser.add_argument("--rules", default="PE-1,PE-3", help="적용 규칙 (예: PE-1,PE-3)")
    parser.add_argument("--output", help="JSON 출력 파일 경로")
    parser.add_argument("--quiet", action="store_true", help="최소 출력 모드")
    args = parser.parse_args()

    rules = [r.strip() for r in args.rules.split(",")]
    results = validate_file(args.file, rules)

    if not args.quiet:
        print_report(results)

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"📄 JSON 보고서 저장: {args.output}")

    sys.exit(0 if results["overall_status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
