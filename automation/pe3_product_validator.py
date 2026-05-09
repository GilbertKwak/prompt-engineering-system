#!/usr/bin/env python3
"""
pe3_product_validator.py — PE-3 제품 PM용 QC 자동검증
Version : 1.0 | Date: 2026-05-09
Author  : Gilbert

연동: config/pe3_product_checklist.yaml
         automation/pe7_product_mece_loop.py

Usage:
  python pe3_product_validator.py --file <prompt.md>
  python pe3_product_validator.py --dir prompts/PE-PROD/
  python pe3_product_validator.py --file <prompt.md> --output report.json
  python pe3_product_validator.py --file <prompt.md> --strict   # 88점 미만 실패
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# ── 쯄크리스트 포함 내장 (YAML 미설치 시 폴백) ──────────────────────
BUILTIN_CHECKS = [
    # D1 명확성
    {"id":"D1-C1","dim":"D1","name":"필수 입력필드 MECE 정의",
     "pattern":r"PRODUCT_IDEA|\{\{.*\}\}|\uae30본값|default",
     "weight":7, "level":"MUST"},
    {"id":"D1-C2","dim":"D1","name":"출력 포맷 표준 준수",
     "pattern":r"={10,}|\[\d/5\]",
     "weight":7, "level":"MUST"},
    {"id":"D1-C3","dim":"D1","name":"SYSTEM ROLE 명시",
     "pattern":r"SYSTEM ROLE|당신은|You are",
     "weight":6, "level":"MUST"},
    # D2 구조·MECE성
    {"id":"D2-C1","dim":"D2","name":"Layer A (고객) 포함",
     "pattern":r"Layer A|B2B|B2C|고객|사용자 세그먼트",
     "weight":4, "level":"MUST"},
    {"id":"D2-C2","dim":"D2","name":"Layer B (문제) 포함",
     "pattern":r"Layer B|문제 정의|기회 공간|Pain Point|Gap",
     "weight":4, "level":"MUST"},
    {"id":"D2-C3","dim":"D2","name":"Layer C (솔루션) 포함",
     "pattern":r"Layer C|Build|Buy|Partner|MVP",
     "weight":4, "level":"MUST"},
    {"id":"D2-C4","dim":"D2","name":"Layer D (수익모델) 포함",
     "pattern":r"Layer D|SaaS|거래수수료|Unit Economics|LTV|CAC",
     "weight":4, "level":"MUST"},
    {"id":"D2-C5","dim":"D2","name":"Layer E (경쟁) 포함",
     "pattern":r"Layer E|지접 경쟁|대체재|Moat|특허",
     "weight":4, "level":"MUST"},
    # D3 시장·재무
    {"id":"D3-C1","dim":"D3","name":"TAM/SAM/SOM 수치 기재",
     "pattern":r"TAM.*\$|SAM.*\$|SOM.*\$|\$[\d]+[BMTbmt]|TAM.*[\d]+",
     "weight":6, "level":"MUST"},
    {"id":"D3-C2","dim":"D3","name":"Unit Economics 4지표",
     "pattern":r"ASP|Contribution Margin|LTV.*CAC|CAC.*LTV|Payback|CM%",
     "weight":5, "level":"MUST"},
    {"id":"D3-C3","dim":"D3","name":"IRR 역산 수식 명시",
     "pattern":r"IRR.*%|\d+%.*IRR|역산|NPV.*=.*0",
     "weight":5, "level":"MUST"},
    {"id":"D3-C4","dim":"D3","name":"3-시나리오 (Bull/Base/Bear)",
     "pattern":r"Bull.*Base|Base.*Bear|\U0001f7e2.*\U0001f7e1|\ub099연.*기준",
     "weight":4, "level":"MUST"},
    # D4 실행가능성
    {"id":"D4-C1","dim":"D4","name":"TRL 수준 명시",
     "pattern":r"TRL [1-9]|TRL\d|Technology Readiness",
     "weight":5, "level":"SHOULD"},
    {"id":"D4-C2","dim":"D4","name":"MVP 정의 명시",
     "pattern":r"MVP|Phase [123]|로드맵|개발 로드맵",
     "weight":5, "level":"SHOULD"},
    {"id":"D4-C3","dim":"D4","name":"리스크 매트릭스",
     "pattern":r"Critical|\U0001f534.*Critical|크리티컈|리스크 매트릭스",
     "weight":5, "level":"MUST"},
    {"id":"D4-C4","dim":"D4","name":"대응방안 명시",
     "pattern":r"대응 방안|대안|Mitigation|Contingency",
     "weight":5, "level":"MUST"},
    # D5 적용가능성
    {"id":"D5-C1","dim":"D5","name":"Executive Summary 포함",
     "pattern":r"Executive Summary|\U0001f4cb.*핵심|햅심 결론",
     "weight":5, "level":"MUST"},
    {"id":"D5-C2","dim":"D5","name":"근거수준 표시",
     "pattern":r"\[HIGH\]|\[MEDIUM\]|\[LOW\]|\[ESTIMATED\]",
     "weight":4, "level":"MUST"},
    {"id":"D5-C3","dim":"D5","name":"크로스 라이브러리 권고",
     "pattern":r"PE-STRAT|PE-FIN|PE-SEMI|PE-AI|PE-DD",
     "weight":5, "level":"SHOULD"},
    {"id":"D5-C4","dim":"D5","name":"Perplexity 실행 명령어",
     "pattern":r"PE-PROD-0[1-9]|PE-PROD-ORCH|```javascript",
     "weight":6, "level":"MUST"},
]

DIM_NAMES = {
    "D1": "명확성 (Clarity)",
    "D2": "구조·MECE성 (Structure)",
    "D3": "시장·재무 특이성 (Market & Finance)",
    "D4": "실행가능성 (Executability)",
    "D5": "적용가능성 (Applicability)",
}

GRADE_MAP = [
    (95, "⭐ S-Grade — 배포 싦시 사용마"),
    (88, "✅ A-Grade — PASS (정식 사용 가능)"),
    (75, "⚠️  B-Grade — REVIEW (수정 후 사용)"),
    (60, "🔄 C-Grade — REWORK (구조 재설계)"),
    ( 0, "❌ F-Grade — FAIL (실사용 불가)"),
]


# ── 콜 실행 ──────────────────────────────────────────────────────────────

def load_checks(yaml_path: str = None) -> list[dict]:
    if yaml_path and YAML_AVAILABLE:
        with open(yaml_path, encoding="utf-8") as f:
            spec = yaml.safe_load(f)
        checks = []
        for dim in spec.get("dimensions", []):
            for c in dim.get("checks", []):
                checks.append({
                    "id"     : c["id"],
                    "dim"    : dim["id"],
                    "name"   : c["name"],
                    "pattern": c["pattern"],
                    "weight" : c["weight"],
                    "level"  : c["level"],
                })
        return checks
    return BUILTIN_CHECKS


def grade(score: float) -> str:
    for threshold, label in GRADE_MAP:
        if score >= threshold:
            return label
    return GRADE_MAP[-1][1]


def validate(content: str, checks: list[dict]) -> dict:
    dim_results: dict[str, dict] = {}

    for c in checks:
        d = c["dim"]
        if d not in dim_results:
            dim_results[d] = {"name": DIM_NAMES.get(d, d),
                              "checks": [], "raw_score": 0,
                              "max_score": 0, "pct": 0.0}

        passed = bool(re.search(c["pattern"], content,
                                re.IGNORECASE | re.MULTILINE))
        dim_results[d]["checks"].append({
            "id"     : c["id"],
            "name"   : c["name"],
            "passed" : passed,
            "weight" : c["weight"],
            "level"  : c["level"],
        })
        if passed:
            dim_results[d]["raw_score"] += c["weight"]
        dim_results[d]["max_score"] += c["weight"]

    # 차원별 단순 점수 비율
    total_raw = total_max = 0
    for d, dr in dim_results.items():
        pct = (dr["raw_score"] / dr["max_score"] * 100) if dr["max_score"] else 0
        dr["pct"] = round(pct, 1)
        total_raw += dr["raw_score"]
        total_max += dr["max_score"]

    overall = round(total_raw / total_max * 100, 1) if total_max else 0
    return {"dimensions": dim_results, "overall": overall,
            "grade": grade(overall), "timestamp": datetime.now().isoformat()}


def print_report(filename: str, result: dict) -> None:
    sep = "=" * 62
    thin = "─" * 62
    print(f"\n{sep}")
    print(f"  PE-3-PROD QC Report — {Path(filename).name}")
    print(f"  {result['timestamp']}")
    print(sep)

    dims = result["dimensions"]
    for d_id in sorted(dims):
        dr = dims[d_id]
        bar_filled = int(dr["pct"] / 5)  # max 20
        bar = "█" * bar_filled + "░" * (20 - bar_filled)
        print(f"\n  {d_id} {dr['name']}")
        print(f"  [{bar}] {dr['pct']}%  "
              f"({dr['raw_score']}/{dr['max_score']}점)")
        for chk in dr["checks"]:
            icon  = "✔" if chk["passed"] else "✘"
            level = f"[{chk['level']}]"
            print(f"    {icon} {level:<8} {chk['id']}: {chk['name']}")

    print(f"\n{thin}")
    print(f"  Overall Score : {result['overall']}%")
    print(f"  Grade         : {result['grade']}")
    print(sep)


def validate_file(path: str, checks: list[dict]) -> dict:
    content = Path(path).read_text(encoding="utf-8")
    result  = validate(content, checks)
    result["file"] = path
    return result


def main():
    parser = argparse.ArgumentParser(
        description="PE-3-PROD 제품 PM용 QC 자동검증"
    )
    parser.add_argument("--file",      help="단일 .md 파일 경로")
    parser.add_argument("--dir",       help="디렉토리 (해당 내 *.md 전체 검증)")
    parser.add_argument("--yaml",      help="YAML 체크리스트 경로",
                        default="config/pe3_product_checklist.yaml")
    parser.add_argument("--output",    help="JSON 리포트 저장 경로")
    parser.add_argument("--strict",    action="store_true",
                        help="88점 미만 시 exit code 1 반환")
    parser.add_argument("--no-yaml",   action="store_true",
                        help="내장 체크리스트 사용 (제비모드)")
    args = parser.parse_args()

    yaml_path = None if args.no_yaml else args.yaml
    if yaml_path and not Path(yaml_path).exists():
        yaml_path = None  # YAML 없으면 내장 쯄크리스트 사용

    checks = load_checks(yaml_path)
    print(f"🔎 콜 항목 수: {len(checks)} | "
          f"{'YAML' if yaml_path else '내장'} 모드")

    all_results = []

    if args.file:
        res = validate_file(args.file, checks)
        print_report(args.file, res)
        all_results.append(res)

    elif args.dir:
        md_files = sorted(Path(args.dir).glob("*.md"))
        if not md_files:
            print(f"No .md files in {args.dir}")
            sys.exit(1)
        for f in md_files:
            res = validate_file(str(f), checks)
            print_report(str(f), res)
            all_results.append(res)
    else:
        parser.print_help()
        sys.exit(0)

    # 요약 테이블
    if len(all_results) > 1:
        print("\n  파일별 요약")
        print(f"  {'File':<35} {'Score':>6} {'Grade'}")
        print("  " + "─" * 58)
        for r in all_results:
            print(f"  {Path(r['file']).name:<35} "
                  f"{r['overall']:>5.1f}%  {r['grade']}")

    if args.output:
        out = all_results if len(all_results) > 1 else all_results[0]
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"\n📄 리포트 저장: {args.output}")

    if args.strict:
        failed = [r for r in all_results if r["overall"] < 88]
        sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
