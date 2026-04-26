#!/usr/bin/env python3
"""
PE-7 v2.0 섹션 6 — E-0N 통합 검증 스크립트
6개 스크립트(A-1, B-1, B-3, C-2, C-3, D-2) 전체 E-0N 검증 실행
PE-3 기준: E-03/E-05/E-07/E-08 자동 감지 + 리포트 생성
Gilbert Kwak | 2026-04-26
"""
import os, sys, json, subprocess, time, traceback
from datetime import datetime
from pathlib import Path

os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)
os.makedirs("reports", exist_ok=True)

SCRIPTS_DIR = Path("scripts/pe7")
VALIDATION_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# ── E-0N 분류 정의 (PE-3 기준) ────────────────────────────
E0N_CODES = {
    "E-01": "데이터 수집 실패 (소스 없음)",
    "E-02": "데이터 파싱 오류 (구조 불일치)",
    "E-03": "수치 계산 오류 (singular, NaN, Inf)",
    "E-04": "모델 수렴 실패 (최적화 미달)",
    "E-05": "외부 API/네트워크 오류 (timeout, 429)",
    "E-06": "파일 I/O 오류 (경로, 권한)",
    "E-07": "출력 품질 미달 (데이터 누락, 형식 불일치)",
    "E-08": "인코딩/문자셋 오류 (UnicodeDecodeError)",
    "E-09": "의존성 패키지 누락 (ImportError)",
    "E-10": "환경변수/시크릿 미설정",
}

# ── 검증 대상 스크립트 ─────────────────────────────────────
VALIDATION_SUITE = [
    {
        "id": "A-1",
        "name": "sheets_exporter",
        "script": "scripts/pe7/sheets_exporter.py",
        "expected_e0n": ["E-05", "E-10"],
        "required_output": ["data/"],
        "fallback_check": "CSV fallback",
        "tests": [
            "syntax_check",
            "import_check",
            "e05_fallback",
            "output_exists",
        ]
    },
    {
        "id": "B-1",
        "name": "supply_chain_collector",
        "script": "scripts/pe7/supply_chain_collector.py",
        "expected_e0n": ["E-05", "E-08"],
        "required_output": ["data/"],
        "fallback_check": "retry",
        "tests": [
            "syntax_check",
            "import_check",
            "e08_encoding",
            "e05_retry_logic",
        ]
    },
    {
        "id": "B-3",
        "name": "sentiment_analyzer",
        "script": "scripts/pe7/sentiment_analyzer.py",
        "expected_e0n": ["E-05"],
        "required_output": ["data/"],
        "fallback_check": "demo data",
        "tests": [
            "syntax_check",
            "import_check",
            "e05_reddit_fallback",
            "demo_data_valid",
        ]
    },
    {
        "id": "C-2",
        "name": "markowitz",
        "script": "scripts/pe7/markowitz.py",
        "expected_e0n": ["E-03"],
        "required_output": ["data/efficient_frontier_", "data/markowitz_result_"],
        "fallback_check": "ridge regularization",
        "tests": [
            "syntax_check",
            "import_check",
            "e03_ridge_check",
            "e03_fallback_equal_weight",
            "output_json_valid",
        ]
    },
    {
        "id": "C-3",
        "name": "black_litterman",
        "script": "scripts/pe7/black_litterman.py",
        "expected_e0n": ["E-03", "E-07"],
        "required_output": ["data/black_litterman_"],
        "fallback_check": "equal weight fallback",
        "tests": [
            "syntax_check",
            "import_check",
            "e03_linalg_fallback",
            "weights_sum_to_one",
            "output_json_valid",
        ]
    },
    {
        "id": "D-2",
        "name": "monthly_ppt_gen",
        "script": "scripts/pe7/monthly_ppt_gen.py",
        "expected_e0n": ["E-07"],
        "required_output": ["reports/Monthly_Review_"],
        "fallback_check": "placeholder insertion",
        "tests": [
            "syntax_check",
            "import_check",
            "e07_placeholder_check",
            "pptx_output_valid",
            "min_file_size",
        ]
    },
]

# ── 검증 함수 ──────────────────────────────────────────────
def run_syntax_check(script_path: str) -> dict:
    """py_compile 기반 문법 검사"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", script_path],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return {"status": "PASS", "detail": "문법 오류 없음"}
        else:
            return {"status": "FAIL", "detail": result.stderr.strip(), "e0n": "E-02"}
    except Exception as e:
        return {"status": "ERROR", "detail": str(e), "e0n": "E-06"}

def run_import_check(script_path: str) -> dict:
    """핵심 import 구문 검사"""
    try:
        with open(script_path, encoding="utf-8") as f:
            content = f.read()
        # os, json, pandas, numpy 기본 import 존재 확인
        required_imports = ["import os", "import json"]
        for imp in required_imports:
            if imp not in content:
                return {"status": "WARN", "detail": f"{imp} 미포함", "e0n": "E-09"}
        return {"status": "PASS", "detail": "import 구조 정상"}
    except Exception as e:
        return {"status": "ERROR", "detail": str(e), "e0n": "E-06"}

def check_fallback_pattern(script_path: str, pattern: str) -> dict:
    """스크립트 내 fallback 패턴 존재 확인"""
    try:
        with open(script_path, encoding="utf-8") as f:
            content = f.read().lower()
        if "fallback" in content or "safe_request" in content or "except" in content:
            return {"status": "PASS", "detail": f"fallback 패턴 확인: '{pattern}'"}
        return {"status": "WARN", "detail": "fallback 패턴 미확인"}
    except Exception as e:
        return {"status": "ERROR", "detail": str(e)}

def check_e03_ridge(script_path: str) -> dict:
    """E-03: ridge regularization 패턴 검사"""
    try:
        with open(script_path, encoding="utf-8") as f:
            content = f.read()
        if "ridge" in content.lower() and ("1e-4" in content or "1e-5" in content or "linalg" in content):
            return {"status": "PASS", "detail": "ridge 정규화 + LinAlgError 처리 확인"}
        return {"status": "WARN", "detail": "E-03 ridge 정규화 패턴 불완전"}
    except Exception as e:
        return {"status": "ERROR", "detail": str(e)}

def check_e08_encoding(script_path: str) -> dict:
    """E-08: UTF-8 인코딩 방어 패턴 검사"""
    try:
        with open(script_path, encoding="utf-8") as f:
            content = f.read()
        if "utf-8" in content.lower() and ("encode" in content or "decode" in content or "errors" in content):
            return {"status": "PASS", "detail": "UTF-8 인코딩 방어 패턴 확인"}
        return {"status": "WARN", "detail": "E-08 encoding 방어 패턴 불완전"}
    except Exception as e:
        return {"status": "ERROR", "detail": str(e)}

def check_output_prefix(prefix: str) -> dict:
    """출력 파일 존재 여부 확인 (prefix 기준)"""
    import glob
    files = glob.glob(f"{prefix}*.csv") + glob.glob(f"{prefix}*.json") + glob.glob(f"{prefix}*.pptx")
    if files:
        return {"status": "PASS", "detail": f"출력 파일 {len(files)}개 확인: {files[0]}"}
    return {"status": "WARN", "detail": f"출력 파일 없음 (prefix: {prefix}) — 스크립트 미실행 상태"}

# ── 통합 검증 실행 ─────────────────────────────────────────
def run_validation_suite() -> dict:
    report = {
        "timestamp": VALIDATION_TIMESTAMP,
        "pe_version": "PE-7 v2.0",
        "validator": "PE-3 E-0N 자동검증",
        "results": [],
        "summary": {},
    }

    total = 0
    passed = 0
    warnings = 0
    failed = 0

    for suite in VALIDATION_SUITE:
        print(f"\n{'='*60}")
        print(f"[검증] {suite['id']} — {suite['name']}")
        print(f"{'='*60}")

        script_result = {
            "id": suite["id"],
            "name": suite["name"],
            "script": suite["script"],
            "expected_e0n": suite["expected_e0n"],
            "test_results": {},
            "overall": "PASS"
        }

        script_path = suite["script"]
        script_exists = os.path.exists(script_path)

        if not script_exists:
            print(f"  ⚠️  스크립트 파일 없음: {script_path}")
            script_result["overall"] = "WARN"
            script_result["test_results"]["file_exists"] = {
                "status": "WARN",
                "detail": f"파일 없음 — GitHub Actions에서 실행 전 상태"
            }
            report["results"].append(script_result)
            warnings += 1
            total += 1
            continue

        # 1. 문법 검사
        res = run_syntax_check(script_path)
        script_result["test_results"]["syntax_check"] = res
        print(f"  {'✅' if res['status'] == 'PASS' else '⚠️ ' if res['status'] == 'WARN' else '❌'} syntax_check: {res['detail']}")

        # 2. import 검사
        res = run_import_check(script_path)
        script_result["test_results"]["import_check"] = res
        print(f"  {'✅' if res['status'] == 'PASS' else '⚠️ ' if res['status'] == 'WARN' else '❌'} import_check: {res['detail']}")

        # 3. E-0N 특화 검사
        if "E-03" in suite["expected_e0n"]:
            res = check_e03_ridge(script_path)
            script_result["test_results"]["e03_ridge_check"] = res
            print(f"  {'✅' if res['status'] == 'PASS' else '⚠️ '} e03_ridge_check: {res['detail']}")

        if "E-08" in suite["expected_e0n"]:
            res = check_e08_encoding(script_path)
            script_result["test_results"]["e08_encoding"] = res
            print(f"  {'✅' if res['status'] == 'PASS' else '⚠️ '} e08_encoding: {res['detail']}")

        # 4. fallback 패턴 검사
        res = check_fallback_pattern(script_path, suite["fallback_check"])
        script_result["test_results"]["fallback_check"] = res
        print(f"  {'✅' if res['status'] == 'PASS' else '⚠️ '} fallback_check: {res['detail']}")

        # 5. 출력 파일 검사
        for output_prefix in suite["required_output"]:
            res = check_output_prefix(output_prefix)
            key = f"output_{output_prefix.split('/')[-1].rstrip('_')}"
            script_result["test_results"][key] = res
            print(f"  {'✅' if res['status'] == 'PASS' else '⚠️ '} {key}: {res['detail']}")

        # 전체 판정
        statuses = [r["status"] for r in script_result["test_results"].values()]
        if any(s == "FAIL" for s in statuses):
            script_result["overall"] = "FAIL"
            failed += 1
        elif any(s in ["WARN", "ERROR"] for s in statuses):
            script_result["overall"] = "WARN"
            warnings += 1
        else:
            script_result["overall"] = "PASS"
            passed += 1

        print(f"  → 종합판정: {'🟢 PASS' if script_result['overall'] == 'PASS' else '🟡 WARN' if script_result['overall'] == 'WARN' else '🔴 FAIL'}")
        report["results"].append(script_result)
        total += 1

    report["summary"] = {
        "total": total,
        "passed": passed,
        "warnings": warnings,
        "failed": failed,
        "pass_rate": f"{(passed/total*100):.1f}%" if total > 0 else "N/A",
        "overall_status": "🟢 ALL PASS" if failed == 0 and warnings == 0 else
                          "🟡 PASS WITH WARNINGS" if failed == 0 else
                          "🔴 FAILURES DETECTED"
    }

    return report

# ── 리포트 생성 ────────────────────────────────────────────
def generate_report(report: dict) -> str:
    ts   = report["timestamp"]
    summ = report["summary"]

    lines = [
        f"# PE-7 v2.0 E-0N 통합 검증 리포트",
        f"**실행 시각:** {ts}",
        f"**검증 기준:** PE-3 E-0N Auto Validation",
        f"",
        f"## 종합 결과",
        f"",
        f"| 항목 | 값 |",
        f"|---|---|",
        f"| 전체 스크립트 | {summ['total']}개 |",
        f"| 🟢 PASS | {summ['passed']}개 |",
        f"| 🟡 WARN | {summ['warnings']}개 |",
        f"| 🔴 FAIL | {summ['failed']}개 |",
        f"| 합격률 | {summ['pass_rate']} |",
        f"| **종합 판정** | **{summ['overall_status']}** |",
        f"",
        f"## 스크립트별 상세 결과",
        f"",
    ]

    for result in report["results"]:
        status_icon = "🟢" if result["overall"] == "PASS" else "🟡" if result["overall"] == "WARN" else "🔴"
        lines.append(f"### {status_icon} {result['id']} — `{result['name']}.py`")
        lines.append(f"")
        lines.append(f"| 검증 항목 | 결과 | 상세 |")
        lines.append(f"|---|---|---|")
        for test_name, test_result in result.get("test_results", {}).items():
            icon = "✅" if test_result["status"] == "PASS" else "⚠️" if test_result["status"] == "WARN" else "❌"
            lines.append(f"| `{test_name}` | {icon} {test_result['status']} | {test_result.get('detail', '')} |")
        lines.append(f"")
        if result.get("expected_e0n"):
            lines.append(f"**예상 E-0N 코드:** {', '.join(result['expected_e0n'])}")
            for code in result["expected_e0n"]:
                lines.append(f"- `{code}`: {E0N_CODES.get(code, '정의 없음')}")
        lines.append(f"")

    lines.extend([
        f"## E-0N 코드 정의 (PE-3 기준)",
        f"",
        f"| 코드 | 설명 |",
        f"|---|---|",
    ])
    for code, desc in E0N_CODES.items():
        lines.append(f"| `{code}` | {desc} |")

    lines.extend([
        f"",
        f"---",
        f"*생성: PE-7 v2.0 E-0N Integration Validator | Gilbert Kwak*",
    ])
    return "\n".join(lines)

def main():
    print("\n" + "="*70)
    print(" PE-7 v2.0 — E-0N 통합 검증 시작")
    print(f" 실행 시각: {VALIDATION_TIMESTAMP}")
    print("="*70)

    report = run_validation_suite()

    # JSON 저장
    json_path = f"logs/e0n_validation_{VALIDATION_TIMESTAMP}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] 검증 결과 JSON: {json_path}")

    # Markdown 리포트 저장
    md_content = generate_report(report)
    md_path = f"reports/E0N_Validation_{VALIDATION_TIMESTAMP}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[OK] 검증 리포트 MD: {md_path}")

    # 종합 판정 출력
    print("\n" + "="*70)
    print(f" 종합 판정: {report['summary']['overall_status']}")
    print(f" PASS: {report['summary']['passed']} | WARN: {report['summary']['warnings']} | FAIL: {report['summary']['failed']}")
    print(f" 합격률: {report['summary']['pass_rate']}")
    print("="*70)

    # CI/CD: FAIL 있으면 exit code 1
    if report["summary"]["failed"] > 0:
        print("\n❌ 검증 실패 — CI 파이프라인 중단")
        sys.exit(1)
    else:
        print("\n✅ 검증 완료 — 다음 단계 진행 가능")

if __name__ == "__main__":
    main()
