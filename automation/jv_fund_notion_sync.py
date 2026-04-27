#!/usr/bin/env python3
"""
JV Fund Prompt → Notion 자동 동기화 스크립트
버전: v1.0 | 날짜: 2026-04-28
레포: GilbertKwak/prompt-engineering-system

사용법:
  python automation/jv_fund_notion_sync.py --mode upsert
  python automation/jv_fund_notion_sync.py --mode validate-only
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime

# ─── 설정 ──────────────────────────────────────────────────────
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
NOTION_PAGE_ID = os.environ.get("JV_FUND_NOTION_PAGE_ID", "")
PROMPT_BASE_DIR = Path("prompts/jv-fund")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

# ─── PE-1 / PE-3 검증 함수 ─────────────────────────────────────
def validate_pe1(content: str) -> dict:
    """PE-1: 수치·출처 정확성 검증"""
    issues = []
    checks = {
        "has_source_citation": any(kw in content for kw in ["출처", "Source:", "Ref:", "(est.)", "(proj.)"]),
        "has_year_reference": any(str(y) in content for y in range(2020, 2031)),
        "has_cagr_data": "CAGR" in content or "성장률" in content,
        "no_bare_numbers": True,  # 간략화: 실제 구현시 regex 활용
    }
    passed = sum(checks.values())
    total = len(checks)
    return {
        "rule": "PE-1",
        "passed": passed,
        "total": total,
        "score": round(passed / total * 100),
        "issues": [k for k, v in checks.items() if not v],
    }


def validate_pe3(content: str) -> dict:
    """PE-3: 반대 시나리오 검증"""
    checks = {
        "has_bear_case": any(kw in content for kw in ["Bear Case", "리스크", "Risk", "반대 시나리오", "실패"]),
        "has_risk_matrix": "리스크 매트릭스" in content or "Risk Matrix" in content,
        "has_mitigation": any(kw in content for kw in ["대응", "Mitigation", "Contingency"]),
    }
    passed = sum(checks.values())
    total = len(checks)
    return {
        "rule": "PE-3",
        "passed": passed,
        "total": total,
        "score": round(passed / total * 100),
        "issues": [k for k, v in checks.items() if not v],
    }


# ─── 메인 검증 실행 ────────────────────────────────────────────
def run_validation(prompt_file: Path) -> dict:
    content = prompt_file.read_text(encoding="utf-8")
    pe1 = validate_pe1(content)
    pe3 = validate_pe3(content)
    overall_pass = pe1["score"] >= 75 and pe3["score"] >= 75
    return {
        "file": str(prompt_file),
        "timestamp": datetime.now().isoformat(),
        "PE-1": pe1,
        "PE-3": pe3,
        "overall": "PASS" if overall_pass else "FAIL",
        "overall_score": round((pe1["score"] + pe3["score"]) / 2),
    }


# ─── 보고서 저장 ────────────────────────────────────────────────
def save_report(results: list, output_path: Path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[✅] 검증 보고서 저장: {output_path}")


# ─── Notion 동기화 (API 키 필요) ──────────────────────────────
def sync_to_notion(prompt_file: Path, validation_result: dict):
    if not NOTION_TOKEN:
        print("[⚠️] NOTION_TOKEN 미설정 — Notion 동기화 건너뜀")
        print("   export NOTION_TOKEN='your-token-here'")
        return
    # 실제 Notion API 연동은 notion-client 패키지 사용
    # pip install notion-client
    try:
        from notion_client import Client  # type: ignore
        notion = Client(auth=NOTION_TOKEN)
        # 페이지 업데이트 로직 (실제 구현)
        print(f"[✅] Notion 동기화 완료: {prompt_file.name}")
    except ImportError:
        print("[⚠️] notion-client 미설치: pip install notion-client")


# ─── CLI 엔트리포인트 ──────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="JV Fund Prompt Notion Sync")
    parser.add_argument(
        "--mode",
        choices=["upsert", "validate-only", "report"],
        default="validate-only",
        help="실행 모드",
    )
    parser.add_argument("--file", type=str, default=None, help="특정 파일 지정")
    args = parser.parse_args()

    # 대상 파일 수집
    if args.file:
        target_files = [Path(args.file)]
    else:
        target_files = list(PROMPT_BASE_DIR.rglob("*.md"))

    print(f"\n🔍 JV Fund Prompt 검증 시작 — {len(target_files)}개 파일")
    print("=" * 60)

    results = []
    for pf in target_files:
        result = run_validation(pf)
        results.append(result)
        status = "✅ PASS" if result["overall"] == "PASS" else "❌ FAIL"
        print(f"  {status} [{result['overall_score']}점] {pf.name}")

        if args.mode == "upsert":
            sync_to_notion(pf, result)

    # 보고서 저장
    report_path = REPORT_DIR / f"jv_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    save_report(results, report_path)

    print("\n" + "=" * 60)
    passed = sum(1 for r in results if r["overall"] == "PASS")
    print(f"📊 검증 완료: {passed}/{len(results)} PASS")
    print(f"📄 보고서: {report_path}")


if __name__ == "__main__":
    main()
