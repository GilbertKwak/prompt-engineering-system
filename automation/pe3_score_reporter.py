#!/usr/bin/env python3
"""
Section D — pe3_score_reporter.py
PE-3 자동 5차원 채점 리포터 (목표: ≥90점)
실행: python automation/pe3_score_reporter.py --input-dir output/ai_intel [--preflight preflight_report.json] [--output pe3_score.json]
"""
import os
import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

# ──────────────────────────────────────────────
# 5차원 채점 기준
# ──────────────────────────────────────────────
DIMENSIONS = [
    "completeness",   # 완결성
    "accuracy",       # 정확성
    "executability",  # 실행가능성
    "ssot_integrity", # SSOT 정합성
    "e0n_resolution", # E-0N 해소율
]

DIMENSION_KR = {
    "completeness":   "완결성",
    "accuracy":       "정확성",
    "executability":  "실행가능성",
    "ssot_integrity": "SSOT 정합성",
    "e0n_resolution": "E-0N 해소율",
}

PASS_THRESHOLD = 90  # 90점 이상 PASS


def score_completeness(intel_files: list, preflight: dict) -> dict:
    """완결성: 필수 intel JSON 파일 수 + 키 필드 존재 여부"""
    score = 0
    details = []
    required_keys = ["domain", "week", "summary", "key_facts"]

    if not intel_files:
        return {"score": 0, "max": 20, "details": ["intel 파일 없음 — 0점"]}

    per_file = 20 / max(len(intel_files), 1)
    for f in intel_files:
        try:
            data = json.loads(Path(f).read_text())
            found = [k for k in required_keys if k in data]
            ratio = len(found) / len(required_keys)
            file_score = per_file * ratio
            score += file_score
            details.append(f"{Path(f).name}: {len(found)}/{len(required_keys)} keys ({file_score:.1f}pt)")
        except Exception as e:
            details.append(f"{Path(f).name}: 파싱 실패 ({e})")

    return {"score": round(min(score, 20), 2), "max": 20, "details": details}


def score_accuracy(intel_files: list) -> dict:
    """정확성: key_facts 항목 수 + metrics 존재 여부"""
    score = 0
    details = []

    for f in intel_files:
        try:
            data = json.loads(Path(f).read_text())
            facts = data.get("key_facts", [])
            metrics = data.get("metrics", {})
            fact_score = min(len(facts) * 1.5, 8)  # 최대 8점
            metric_score = 4 if metrics else 0
            file_score = fact_score + metric_score
            score += file_score
            details.append(f"{Path(f).name}: facts={len(facts)} metrics={'있음' if metrics else '없음'} ({file_score:.1f}pt)")
        except Exception as e:
            details.append(f"{Path(f).name}: 파싱 실패 ({e})")

    return {"score": round(min(score, 20), 2), "max": 20, "details": details}


def score_executability(root: Path) -> dict:
    """실행가능성: 필수 스크립트 존재 + requirements 완전성"""
    required = [
        "automation/ai_intel_collector.py",
        "automation/ai_ew_detector.py",
        "automation/kg_delta_generator.py",
        "automation/notion_c31_updater.py",
        "automation/preflight_check.py",
        "automation/ssot_sha_validator.py",
    ]
    req_file = root / "automation" / "requirements_ai_intel.txt"

    present = [r for r in required if (root / r).exists()]
    missing = [r for r in required if not (root / r).exists()]
    script_score = (len(present) / len(required)) * 15

    req_score = 0
    req_detail = ""
    if req_file.exists():
        content = req_file.read_text().lower()
        pkgs = ["requests", "openai", "notion"]
        found_pkgs = [p for p in pkgs if p in content]
        req_score = (len(found_pkgs) / len(pkgs)) * 5
        req_detail = f"requirements: {found_pkgs}"
    else:
        req_detail = "requirements_ai_intel.txt 없음"

    total = script_score + req_score
    details = [
        f"스크립트 {len(present)}/{len(required)} 존재 ({script_score:.1f}pt)",
        req_detail + f" ({req_score:.1f}pt)",
    ]
    if missing:
        details.append(f"누락: {[Path(m).name for m in missing]}")

    return {"score": round(min(total, 20), 2), "max": 20, "details": details}


def score_ssot_integrity(preflight: dict) -> dict:
    """SSOT 정합성: preflight E-01 결과 + SHA 기록 존재"""
    if not preflight:
        return {"score": 10, "max": 20, "details": ["preflight 데이터 없음 — 기본 10점"]}

    checks = {c["tag"]: c for c in preflight.get("checks", [])}
    e01 = checks.get("E-01", {})
    e08 = checks.get("E-08", {})

    score = 0
    details = []

    if e01.get("status") == "PASS":
        score += 12
        details.append(f"E-01 PASS: SHA 일치 (12pt)")
    elif e01.get("status") == "WARN":
        score += 6
        details.append(f"E-01 WARN: {e01.get('detail', '')} (6pt)")
    else:
        details.append(f"E-01 FAIL: SHA 불일치 (0pt)")

    if e08.get("status") == "PASS":
        score += 8
        details.append(f"E-08 PASS: Secrets 주입 확인 (8pt)")
    else:
        details.append(f"E-08 FAIL: Secrets 미설정 (0pt)")

    return {"score": round(min(score, 20), 2), "max": 20, "details": details}


def score_e0n_resolution(preflight: dict) -> dict:
    """E-0N 해소율: PASS+WARN 비율 기반 채점"""
    if not preflight:
        return {"score": 10, "max": 20, "details": ["preflight 데이터 없음 — 기본 10점"]}

    checks = preflight.get("checks", [])
    total = len(checks)
    if total == 0:
        return {"score": 0, "max": 20, "details": ["checks 없음"]}

    passed = sum(1 for c in checks if c["status"] in ("PASS", "WARN", "MANUAL"))
    failed = sum(1 for c in checks if c["status"] == "FAIL")
    ratio = passed / total
    score = ratio * 20

    details = [
        f"총 {total}개 체크: PASS/WARN/MANUAL={passed} FAIL={failed}",
        f"해소율 {ratio*100:.0f}% → {score:.1f}pt",
    ]
    if failed > 0:
        fail_tags = [c["tag"] for c in checks if c["status"] == "FAIL"]
        details.append(f"미해소 오류: {fail_tags}")

    return {"score": round(min(score, 20), 2), "max": 20, "details": details}


def run_pe3_scoring(
    input_dir: str,
    preflight_path: str,
    root: Path,
) -> dict:
    print(f"\n{'='*60}")
    print(f"  PE-3 자동채점 리포터 (Section D) — 목표 ≥{PASS_THRESHOLD}점")
    print(f"{'='*60}")

    # preflight 데이터 로드
    preflight = {}
    if preflight_path and Path(preflight_path).exists():
        try:
            preflight = json.loads(Path(preflight_path).read_text())
            print(f"[INFO] preflight 데이터 로드: {preflight_path}")
        except Exception as e:
            print(f"[WARN] preflight 로드 실패: {e}")

    # intel JSON 파일 수집
    intel_files = []
    if input_dir and Path(input_dir).exists():
        intel_files = list(Path(input_dir).glob("intel_*.json"))
        intel_files = [str(f) for f in intel_files]
    print(f"[INFO] intel 파일 {len(intel_files)}개 발견")

    # 5차원 채점
    dim_scores = {
        "completeness":   score_completeness(intel_files, preflight),
        "accuracy":       score_accuracy(intel_files),
        "executability":  score_executability(root),
        "ssot_integrity": score_ssot_integrity(preflight),
        "e0n_resolution": score_e0n_resolution(preflight),
    }

    total_score = sum(d["score"] for d in dim_scores.values())
    max_score = sum(d["max"] for d in dim_scores.values())
    pct = (total_score / max_score) * 100 if max_score > 0 else 0
    status = "PASS" if total_score >= PASS_THRESHOLD else "FAIL — 재작성 루프 필요"

    # 결과 출력
    print(f"\n  {'차원':<18} {'점수':>6} / {'만점':>5}  {'세부':<}")
    print(f"  {'-'*60}")
    for dim in DIMENSIONS:
        d = dim_scores[dim]
        kr = DIMENSION_KR[dim]
        bar = "█" * int(d["score"] / d["max"] * 20)
        print(f"  {kr:<14} {d['score']:>6.1f} / {d['max']:>5}  {bar}")
        for detail in d["details"][:2]:
            print(f"    └ {detail}")
    print(f"  {'-'*60}")
    print(f"  {'TOTAL':<14} {total_score:>6.1f} / {max_score:>5}  ({pct:.1f}%)")
    print(f"\n  판정: {'✅ ' if total_score >= PASS_THRESHOLD else '❌ '}{status}")
    print(f"{'='*60}\n")

    report = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "total_score": round(total_score, 2),
        "max_score": max_score,
        "percentage": round(pct, 2),
        "status": "PASS" if total_score >= PASS_THRESHOLD else "FAIL",
        "threshold": PASS_THRESHOLD,
        "dimensions": dim_scores,
        "rewrite_required": total_score < PASS_THRESHOLD,
        "low_dims": [
            dim for dim in DIMENSIONS
            if dim_scores[dim]["score"] / dim_scores[dim]["max"] < 0.7
        ],
    }

    if report["rewrite_required"]:
        print(f"[⚠️  재작성 필요] 미달 차원: {report['low_dims']}")
        print("  → 해당 섹션 자동 재작성 루프를 실행하세요")

    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PE-3 Score Reporter (Section D)")
    parser.add_argument("--input-dir", default="output/ai_intel", help="intel JSON 파일 디렉터리")
    parser.add_argument("--preflight", default="", help="preflight_report.json 경로")
    parser.add_argument("--output", default="", help="채점 결과 JSON 출력 경로")
    parser.add_argument("--root", default=".", help="리포지토리 루트 경로")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    report = run_pe3_scoring(
        input_dir=args.input_dir,
        preflight_path=args.preflight,
        root=root,
    )

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2))
        print(f"채점 리포트 저장: {out}")

    sys.exit(0 if report["status"] == "PASS" else 1)
