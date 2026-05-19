#!/usr/bin/env python3
"""
Section C — workflow_dedup_fix.py
E-02 교정: 중복 workflow 파일 탐지 및 구버전 deprecate 처리
실행: python automation/workflow_dedup_fix.py [--dry-run] [--root .]
"""
import os
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

# 중복 쌍: (신규 유지 파일, 구버전 deprecate 대상)
DUPLICATE_PAIRS = [
    (
        ".github/workflows/ai-intel-weekly.yml",   # 유지 (하이픈, 최신 12.4KB)
        ".github/workflows/ai_intel_weekly.yml",   # deprecate (언더스코어, 구버전 9.7KB)
    ),
]

DEPRECATE_HEADER = """# ============================================================
# ⚠️  DEPRECATED — E-02 자동 교정 ({date})
# 이 파일은 중복 workflow로 탐지되어 비활성화되었습니다.
# 활성 파일: {active}
# 이 파일은 삭제하거나 .deprecated 확장자로 변경하세요.
# ============================================================
# ORIGINAL CONTENT BELOW (실행 차단 — on: 제거됨)
"""


def deprecate_workflow(file_path: Path, active_path: str, dry_run: bool) -> dict:
    result = {"file": str(file_path), "action": "NONE", "detail": ""}

    if not file_path.exists():
        result["action"] = "SKIP"
        result["detail"] = "파일 없음"
        return result

    content = file_path.read_text(encoding="utf-8")

    # 이미 deprecate된 경우 스킵
    if "DEPRECATED" in content:
        result["action"] = "SKIP"
        result["detail"] = "이미 deprecate 처리됨"
        return result

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    header = DEPRECATE_HEADER.format(date=now, active=active_path)

    # on: 트리거 블록 제거 (실행 차단)
    # schedule, push, pull_request, workflow_dispatch 등 모두 제거
    neutralized = re.sub(
        r'^on:\s*\n(  .+\n)+',
        'on: {}  # DISABLED by E-02 dedup fix\n',
        content,
        flags=re.MULTILINE
    )
    # workflow_dispatch 단독 형식 처리
    neutralized = re.sub(
        r'^on:\s*workflow_dispatch.*$',
        'on: {}  # DISABLED by E-02 dedup fix',
        neutralized,
        flags=re.MULTILINE
    )

    new_content = header + neutralized

    if dry_run:
        result["action"] = "DRY_RUN"
        result["detail"] = f"[DRY-RUN] deprecate 처리 예정: {file_path.name}"
        print(f"[DRY-RUN] {file_path} → deprecate 처리 예정")
    else:
        file_path.write_text(new_content, encoding="utf-8")
        result["action"] = "DEPRECATED"
        result["detail"] = f"{file_path.name} deprecate 완료 (on: 비활성화)"
        print(f"[✅ E-02 교정] {file_path} → deprecate 처리 완료")

    return result


def run_dedup_fix(root: Path, dry_run: bool = False) -> dict:
    print(f"\n{'='*60}")
    print(f"  WORKFLOW DEDUP FIX (Section C) — E-02 교정")
    print(f"{'='*60}")

    results = []
    for active_rel, deprecated_rel in DUPLICATE_PAIRS:
        active_path = root / active_rel
        deprecated_path = root / deprecated_rel

        # 신규 파일 존재 확인
        if not active_path.exists():
            print(f"[WARN] 활성 파일 없음: {active_rel} — 쌍 스킵")
            continue

        print(f"  유지: {active_rel} ({active_path.stat().st_size}B)")
        print(f"  구버전: {deprecated_rel}")

        r = deprecate_workflow(deprecated_path, active_rel, dry_run)
        results.append(r)
        print(f"  → {r['action']}: {r['detail']}")

    print(f"{'='*60}")
    fixed = sum(1 for r in results if r["action"] == "DEPRECATED")
    skipped = sum(1 for r in results if r["action"] == "SKIP")
    print(f"  완료: 교정={fixed} / 스킵={skipped} / 대상={len(results)}")
    print(f"{'='*60}\n")

    return {"fixed": fixed, "skipped": skipped, "results": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Workflow Dedup Fix (Section C)")
    parser.add_argument("--dry-run", action="store_true", help="실제 변경 없이 시뮬레이션")
    parser.add_argument("--root", default=".", help="리포지토리 루트 경로")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    result = run_dedup_fix(root, dry_run=args.dry_run)
    sys.exit(0 if result["fixed"] >= 0 else 1)
