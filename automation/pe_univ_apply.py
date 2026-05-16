#!/usr/bin/env python3
"""
PE-UNIV · Universal Prompt Optimization Apply Engine v1.0
=========================================================
P1 MVP — C-31 AI 최신 프롬프트를 PE-CON·PE-STR·PE-JV 3개 도메인 수동 테스트 적용
PE-3 점수 변화 측정 및 E-09 트리거 자동 실행
"""

import os
import json
import hashlib
import datetime
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────────
# 0. DOMAIN REGISTRY  (14+1 전 도메인)
# ─────────────────────────────────────────────
DOMAIN_REGISTRY = {
    "C-31":      {"path": "prompts/ai-platform/",        "threshold": 95, "mode": "upsert"},
    "PE-CON":    {"path": "PE-CON/",                     "threshold": 91, "mode": "upsert"},
    "PE-STR":    {"path": "prompts/strategy/",           "threshold": 95, "mode": "upsert"},
    "PE-JV":     {"path": "applied-cases/jv-fund/",      "threshold": 94, "mode": "upsert"},
    "PE-7":      {"path": "PE-7/",                       "threshold": 94, "mode": "append"},
    "PE-11":     {"path": "PE-11/",                      "threshold": 95, "mode": "upsert"},
    "PE-MEM":    {"path": "PE-MEM/",                     "threshold": 92, "mode": "append"},
    "PE-EDU":    {"path": "PE-EDU/",                     "threshold": 91, "mode": "append"},
    "PE-ICD":    {"path": "PE-ICD/",                     "threshold": 93, "mode": "upsert"},
    "PE-MFG":    {"path": "PE-MFG/",                     "threshold": 92, "mode": "append"},
    "PE-NBD":    {"path": "PE-NBD/",                     "threshold": 93, "mode": "upsert"},
    "PE-BOARD":  {"path": "PE-BOARD/",                   "threshold": 94, "mode": "upsert"},
    "PE-PAT":    {"path": "applied-cases/PE-PAT/",       "threshold": 96, "mode": "upsert"},
    "PE-INTL":   {"path": "applied-cases/PE-INTL/",      "threshold": 91, "mode": "append"},
    "PE-LR":     {"path": "applied-cases/PE-LR/",        "threshold": 92, "mode": "append"},
}

# ─────────────────────────────────────────────
# 1. PE-3 VALIDATION  (5-dimension heuristic)
# ─────────────────────────────────────────────
PE3_DIMENSIONS = [
    ("structural_completeness",  0.25),  # 역할/목표/출력 3요소 포함
    ("reusability",              0.20),  # 도메인 변수 파라미터화
    ("reasoning_precision",      0.20),  # 단계별 추론 명시
    ("output_format_compliance", 0.20),  # JSON/MD 출력 정합
    ("cross_domain_bridge",      0.15),  # 타 도메인 연계 가능성
]

def run_pe3_validation(content: str, domain: str) -> dict:
    """Heuristic PE-3 scorer — 실제 LLM 검증 전 1차 필터"""
    scores = {}
    text_lower = content.lower()

    # 구조 완전성
    has_role    = any(k in text_lower for k in ["역할", "role", "당신은", "you are"])
    has_output  = any(k in text_lower for k in ["출력", "output", "json", "결과"])
    has_goal    = any(k in text_lower for k in ["목적", "goal", "목표", "objective"])
    scores["structural_completeness"] = (has_role + has_output + has_goal) / 3 * 100

    # 재사용성
    param_count = content.count("{{") + content.count("{{")
    scores["reusability"] = min(100, 70 + param_count * 3)

    # 추론 정밀도
    step_markers = sum(1 for k in ["단계", "step", "phase", "1.", "2.", "3."] if k in text_lower)
    scores["reasoning_precision"] = min(100, 60 + step_markers * 5)

    # 출력 형식 정합성
    has_json   = "json" in text_lower or "```" in content
    has_schema = any(k in text_lower for k in ["schema", "스키마", "format", "형식"])
    scores["output_format_compliance"] = (has_json * 60 + has_schema * 40)

    # 크로스 도메인 브리지
    cross_refs = sum(1 for d in DOMAIN_REGISTRY if d.lower() in text_lower)
    scores["cross_domain_bridge"] = min(100, 50 + cross_refs * 10)

    # 가중 합산
    total = sum(scores[dim] * w for dim, w in PE3_DIMENSIONS)
    return {
        "domain":     domain,
        "total":      round(total, 1),
        "dimensions": {k: round(v, 1) for k, v in scores.items()},
        "timestamp":  datetime.datetime.utcnow().isoformat(),
    }

# ─────────────────────────────────────────────
# 2. CROSS-DOMAIN ADAPTATION  (GR-05 simplified)
# ─────────────────────────────────────────────
DOMAIN_VARIABLE_MAP = {
    "PE-CON":  {"[DOMAIN]": "컨설팅 전략",  "[LIBRARY]": "PE-CON v3.0",  "[THRESHOLD]": "91"},
    "PE-STR":  {"[DOMAIN]": "전략·의사결정", "[LIBRARY]": "PE-STR v1.0",  "[THRESHOLD]": "95"},
    "PE-JV":   {"[DOMAIN]": "JV 펀드",       "[LIBRARY]": "PE-JV v4.1",   "[THRESHOLD]": "94"},
    "PE-MEM":  {"[DOMAIN]": "메모리 제품",   "[LIBRARY]": "PE-MEM v1.4",  "[THRESHOLD]": "92"},
    "PE-BOARD":{"[DOMAIN]": "M&A 전략",      "[LIBRARY]": "PE-BOARD v1.1","[THRESHOLD]": "94"},
    "PE-PAT":  {"[DOMAIN]": "특허 분석",     "[LIBRARY]": "PE-PAT v1.0",  "[THRESHOLD]": "96"},
}

def cross_domain_adapt(content: str, target_domain: str) -> str:
    """소스 프롬프트를 타겟 도메인 컨텍스트로 파라미터 치환"""
    adapted = content
    var_map = DOMAIN_VARIABLE_MAP.get(target_domain, {})
    for placeholder, value in var_map.items():
        adapted = adapted.replace(placeholder, value)
    # 도메인 헤더 주입
    header = (
        f"\n<!-- PE-UNIV AUTO-ADAPTED: {target_domain} | "
        f"{datetime.date.today().isoformat()} -->\n"
    )
    return header + adapted

# ─────────────────────────────────────────────
# 3. APPLY ENGINE
# ─────────────────────────────────────────────
def sha256_content(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12]

def apply_to_domain(
    source_path: str,
    target_domain: str,
    dry_run: bool = False,
) -> dict:
    """
    소스 프롬프트를 지정 도메인에 적용
    Returns: result dict with PE-3 before/after scores
    """
    if not os.path.exists(source_path):
        return {"status": "ERROR", "reason": f"Source not found: {source_path}"}

    config = DOMAIN_REGISTRY.get(target_domain)
    if not config:
        return {"status": "ERROR", "reason": f"Unknown domain: {target_domain}"}

    with open(source_path, "r", encoding="utf-8") as f:
        source_content = f.read()

    # ── PE-3 BEFORE ──
    before_score = run_pe3_validation(source_content, target_domain)

    # ── E-09 gate ──
    if before_score["total"] < config["threshold"]:
        return {
            "status":       "E-09_TRIGGERED",
            "domain":       target_domain,
            "pe3_before":   before_score["total"],
            "threshold":    config["threshold"],
            "action":       "PE-1 자동개선 루프 필요 — 수동 실행: pe-refine --target " + source_path,
        }

    # ── GR-05 Cross-Domain Adaptation ──
    adapted_content = cross_domain_adapt(source_content, target_domain)

    # ── PE-3 AFTER ──
    after_score = run_pe3_validation(adapted_content, target_domain)

    # ── Output filename ──
    src_stem    = Path(source_path).stem
    out_dir     = config["path"]
    out_filename = f"{out_dir}ADAPTED_{src_stem}_{target_domain}_v1.0.md"
    sha_tag      = sha256_content(adapted_content)

    result = {
        "status":        "DRY_RUN" if dry_run else "APPLIED",
        "domain":        target_domain,
        "source":        source_path,
        "output_path":   out_filename,
        "sha_tag":       sha_tag,
        "pe3_before":    before_score["total"],
        "pe3_after":     after_score["total"],
        "delta":         round(after_score["total"] - before_score["total"], 1),
        "dimensions_after": after_score["dimensions"],
        "timestamp":     datetime.datetime.utcnow().isoformat(),
    }

    if not dry_run:
        os.makedirs(out_dir, exist_ok=True)
        with open(out_filename, "w", encoding="utf-8") as f:
            f.write(adapted_content)
        print(f"  ✅ [{target_domain}] → {out_filename} (PE-3: {before_score['total']} → {after_score['total']}, Δ{result['delta']:+.1f})")

    return result

# ─────────────────────────────────────────────
# 4. BATCH RUNNER  (P1 MVP: 3-domain test)
# ─────────────────────────────────────────────
def run_p1_mvp_test(
    source: str = "prompts/ai-platform/notion_005_v1.0.md",
    targets: list = None,
    dry_run: bool = False,
) -> dict:
    """
    P1 MVP — C-31 AI 최신 프롬프트를 PE-CON·PE-STR·PE-JV 3개 도메인 적용 테스트
    """
    if targets is None:
        targets = ["PE-CON", "PE-STR", "PE-JV"]

    print(f"\n{'='*60}")
    print(f"PE-UNIV P1 MVP Test Run — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S KST')}")
    print(f"Source : {source}")
    print(f"Targets: {targets}")
    print(f"Mode   : {'DRY RUN' if dry_run else 'LIVE APPLY'}")
    print(f"{'='*60}\n")

    results = []
    for domain in targets:
        print(f"[→] Applying to {domain}...")
        r = apply_to_domain(source, domain, dry_run=dry_run)
        results.append(r)
        if r["status"] == "E-09_TRIGGERED":
            print(f"  ⚠️  E-09: PE-3 {r['pe3_before']} < threshold {r['threshold']} → PE-1 필요")

    # ── Summary report ──
    applied   = [r for r in results if r["status"] in ("APPLIED", "DRY_RUN")]
    e09_count = sum(1 for r in results if r["status"] == "E-09_TRIGGERED")
    avg_before = sum(r["pe3_before"] for r in applied) / max(len(applied), 1)
    avg_after  = sum(r["pe3_after"]  for r in applied) / max(len(applied), 1)

    summary = {
        "run_type":      "P1_MVP_TEST",
        "source":        source,
        "targets":       targets,
        "applied_count": len(applied),
        "e09_count":     e09_count,
        "avg_pe3_before":round(avg_before, 1),
        "avg_pe3_after": round(avg_after, 1),
        "avg_delta":     round(avg_after - avg_before, 1),
        "results":       results,
        "timestamp":     datetime.datetime.utcnow().isoformat(),
    }

    print(f"\n{'─'*60}")
    print(f"PE-UNIV P1 Result Summary")
    print(f"  Applied    : {len(applied)}/{len(targets)} domains")
    print(f"  E-09 flags : {e09_count}")
    print(f"  PE-3 avg   : {avg_before} → {avg_after}  (Δ{summary['avg_delta']:+.1f})")
    print(f"{'─'*60}\n")

    # JSON 리포트 저장
    report_path = f"automation/pe_univ_p1_report_{datetime.date.today().isoformat()}.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"📄 Report saved → {report_path}")

    return summary

# ─────────────────────────────────────────────
# 5. CLI ENTRY
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PE-UNIV Universal Prompt Apply Engine")
    parser.add_argument("--source",  default="prompts/ai-platform/notion_005_v1.0.md")
    parser.add_argument("--domains", default="PE-CON,PE-STR,PE-JV",
                        help="콤마 구분 도메인 목록 또는 ALL")
    parser.add_argument("--dry-run", action="store_true", help="파일 쓰기 없이 점수만 측정")
    args = parser.parse_args()

    if args.domains.upper() == "ALL":
        target_list = list(DOMAIN_REGISTRY.keys())
    else:
        target_list = [d.strip() for d in args.domains.split(",")]

    run_p1_mvp_test(
        source  = args.source,
        targets = target_list,
        dry_run = args.dry_run,
    )
