#!/usr/bin/env python3
"""
Section A — preflight_check.py
E-0N 런타임 자동 탐지 스크립트
실행: python automation/preflight_check.py [--strict] [--output preflight_report.json]
"""
import os
import sys
import json
import subprocess
import argparse
from datetime import datetime, timezone
from pathlib import Path

# ──────────────────────────────────────────────
# E-0N 태그 정의
# ──────────────────────────────────────────────
E_TAGS = {
    "E-01": "SHA 불일치 (Notion Hub vs GitHub)",
    "E-02": "Workflow 파일 중복",
    "E-03": "Notion Integration 미연결 (수동 검토 필요)",
    "E-04": "requirements 패키지 누락",
    "E-05": "Section A 파일 미완성",
    "E-06": "병렬 workflow 의존성 충돌",
    "E-07": "KG delta 버전 파라미터 불일치",
    "E-08": "Secrets 미주입 (API 키 미설정)",
}

REQUIRED_SECRETS = ["PERPLEXITY_API_KEY", "NOTION_API_KEY"]
REQUIRED_SCRIPTS = [
    "automation/ai_intel_collector.py",
    "automation/ai_ew_detector.py",
    "automation/kg_delta_generator.py",
    "automation/notion_c31_updater.py",
]
DUPLICATE_WORKFLOW_PAIRS = [
    (".github/workflows/ai-intel-weekly.yml", ".github/workflows/ai_intel_weekly.yml"),
]
REQUIRED_PACKAGES = ["requests", "openai", "notion-client"]


def check_e01_sha(root: Path) -> dict:
    """E-01: .ssot_sha 파일과 git HEAD 비교"""
    result = {"tag": "E-01", "status": "PASS", "detail": ""}
    ssot_file = root / ".ssot_sha"
    try:
        git_sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip()
        if ssot_file.exists():
            stored_sha = ssot_file.read_text().strip()
            if stored_sha != git_sha:
                result["status"] = "FAIL"
                result["detail"] = f"stored={stored_sha[:8]} | git={git_sha[:8]}"
            else:
                result["detail"] = f"SHA match: {git_sha[:8]}"
        else:
            # 파일 없으면 현재 SHA 기록
            ssot_file.write_text(git_sha)
            result["status"] = "WARN"
            result["detail"] = f".ssot_sha 없어 신규 생성: {git_sha[:8]}"
    except Exception as e:
        result["status"] = "WARN"
        result["detail"] = f"git 명령 실패 (non-git env): {e}"
    return result


def check_e02_duplicate_workflows(root: Path) -> dict:
    """E-02: workflow 중복 파일 탐지"""
    result = {"tag": "E-02", "status": "PASS", "detail": ""}
    found_pairs = []
    for a, b in DUPLICATE_WORKFLOW_PAIRS:
        if (root / a).exists() and (root / b).exists():
            found_pairs.append((a, b))
    if found_pairs:
        result["status"] = "FAIL"
        result["detail"] = f"중복 workflow: {found_pairs}"
    else:
        result["detail"] = "중복 없음"
    return result


def check_e03_notion_connection() -> dict:
    """E-03: Notion API 키 존재 여부로 간접 확인 (실제 연결은 수동)"""
    result = {"tag": "E-03", "status": "MANUAL", "detail": "Notion Integration 연결은 UI에서 수동 확인 필요"}
    notion_key = os.environ.get("NOTION_API_KEY", "")
    if notion_key.startswith("secret_"):
        result["status"] = "WARN"
        result["detail"] = "NOTION_API_KEY 형식 확인됨 — UI 연결 상태는 수동 검토 필요"
    elif notion_key:
        result["status"] = "WARN"
        result["detail"] = f"NOTION_API_KEY 존재하나 형식 비표준 (secret_ 접두사 없음)"
    return result


def check_e04_requirements(root: Path) -> dict:
    """E-04: requirements_ai_intel.txt 패키지 포함 여부"""
    result = {"tag": "E-04", "status": "PASS", "detail": ""}
    req_file = root / "automation" / "requirements_ai_intel.txt"
    if not req_file.exists():
        result["status"] = "FAIL"
        result["detail"] = "requirements_ai_intel.txt 없음"
        return result
    content = req_file.read_text().lower()
    missing = [pkg for pkg in REQUIRED_PACKAGES if pkg.replace("-", "_").split("==")[0] not in content and pkg.split("==")[0] not in content]
    if missing:
        result["status"] = "WARN"
        result["detail"] = f"누락 가능 패키지: {missing}"
    else:
        result["detail"] = "필수 패키지 모두 확인됨"
    return result


def check_e05_section_files(root: Path) -> dict:
    """E-05: 필수 automation 스크립트 존재 여부"""
    result = {"tag": "E-05", "status": "PASS", "detail": ""}
    missing = [s for s in REQUIRED_SCRIPTS if not (root / s).exists()]
    if missing:
        result["status"] = "FAIL"
        result["detail"] = f"누락 파일: {missing}"
    else:
        result["detail"] = f"{len(REQUIRED_SCRIPTS)}개 필수 스크립트 모두 존재"
    return result


def check_e06_parallel_workflow(root: Path) -> dict:
    """E-06: pe7_parallel_v3.yml needs 체인 검증"""
    result = {"tag": "E-06", "status": "PASS", "detail": ""}
    wf = root / ".github" / "workflows" / "pe7_parallel_v3.yml"
    if not wf.exists():
        result["status"] = "WARN"
        result["detail"] = "pe7_parallel_v3.yml 없음"
        return result
    content = wf.read_text()
    # needs: 가 있는데 참조 job이 실제 존재하는지 간단 체크
    import re
    needs_refs = re.findall(r'needs:\s*\[?([\w,\s]+)\]?', content)
    jobs = re.findall(r'^  (\w+):$', content, re.MULTILINE)
    issues = []
    for ref_block in needs_refs:
        for ref in re.split(r'[,\s]+', ref_block.strip()):
            ref = ref.strip()
            if ref and ref not in jobs:
                issues.append(ref)
    if issues:
        result["status"] = "WARN"
        result["detail"] = f"needs 참조 불명 job: {issues}"
    else:
        result["detail"] = "needs 체인 정상"
    return result


def check_e07_kg_version(root: Path) -> dict:
    """E-07: kg_delta_generator.py default version 인자 확인"""
    result = {"tag": "E-07", "status": "PASS", "detail": ""}
    kg = root / "automation" / "kg_delta_generator.py"
    if not kg.exists():
        result["status"] = "FAIL"
        result["detail"] = "kg_delta_generator.py 없음"
        return result
    content = kg.read_text()
    if "--current-version" in content or "current_version" in content:
        result["detail"] = "--current-version 파라미터 확인됨"
    else:
        result["status"] = "WARN"
        result["detail"] = "--current-version 파라미터 미확인 — 수동 점검 필요"
    return result


def check_e08_secrets() -> dict:
    """E-08: 환경변수로 Secrets 주입 여부 확인"""
    result = {"tag": "E-08", "status": "PASS", "detail": ""}
    missing = [k for k in REQUIRED_SECRETS if not os.environ.get(k)]
    if missing:
        result["status"] = "FAIL"
        result["detail"] = f"미설정 Secrets: {missing}"
    else:
        result["detail"] = "모든 필수 Secrets 주입 확인"
    return result


def run_preflight(root: Path, strict: bool = False) -> dict:
    checks = [
        check_e01_sha(root),
        check_e02_duplicate_workflows(root),
        check_e03_notion_connection(),
        check_e04_requirements(root),
        check_e05_section_files(root),
        check_e06_parallel_workflow(root),
        check_e07_kg_version(root),
        check_e08_secrets(),
    ]

    summary = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "total": len(checks),
        "pass": sum(1 for c in checks if c["status"] == "PASS"),
        "warn": sum(1 for c in checks if c["status"] == "WARN"),
        "fail": sum(1 for c in checks if c["status"] == "FAIL"),
        "manual": sum(1 for c in checks if c["status"] == "MANUAL"),
        "checks": checks,
    }

    # 콘솔 출력
    print(f"\n{'='*60}")
    print(f"  PRE-FLIGHT CHECK — {summary['run_at']}")
    print(f"{'='*60}")
    icons = {"PASS": "✅", "WARN": "⚠️ ", "FAIL": "❌", "MANUAL": "🔧"}
    for c in checks:
        icon = icons.get(c["status"], "?")
        print(f"  {icon} [{c['tag']}] {E_TAGS[c['tag']]}")
        if c["detail"]:
            print(f"       → {c['detail']}")
    print(f"{'='*60}")
    print(f"  결과: PASS={summary['pass']} WARN={summary['warn']} FAIL={summary['fail']} MANUAL={summary['manual']}")
    print(f"{'='*60}\n")

    if strict and summary["fail"] > 0:
        print("[STRICT MODE] FAIL 항목 존재 → 파이프라인 중단")
        sys.exit(1)

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="E-0N Pre-flight checker")
    parser.add_argument("--strict", action="store_true", help="FAIL 시 exit(1)")
    parser.add_argument("--output", default="", help="JSON 리포트 출력 경로")
    parser.add_argument("--root", default=".", help="리포지토리 루트 경로")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    report = run_preflight(root, strict=args.strict)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2))
        print(f"리포트 저장: {out}")
