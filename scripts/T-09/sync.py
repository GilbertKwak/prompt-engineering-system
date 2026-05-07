#!/usr/bin/env python3
"""
T-09 Notion Sync Engine — PE-CON v6.1
=======================================
[CHANGELOG]
  v6.1 (2026-05-07): PE2-variants/ 경로 자동 인식 추가
                      PROMPT_DIRS 재귀 스캔 로직 통합
                      validate_pe3_score() 검증 게이트 추가
  v6.0 (2026-05-07): PE-1 자동개선 루프 완료 후 초기 sync 통합
  v5.0 (2025-xx-xx): 기존 CON-01~05 단일 디렉토리 스캔
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[2]

# v6.1: PE2-variants/ 경로 추가 — 재귀 스캔 대상
PROMPT_DIRS: List[str] = [
    "PE-CON",                  # CON-01~05 원본 (5종)
    "PE-CON/PE2-variants",     # ★ v6.1 신규: A/B 파생 10종
    "PE-FIN",                  # FIN 도메인
    "prompts",                 # 범용 프롬프트
]

# PE-3 점수 최저 기준 — 이 값 미만은 경고 로그 출력
PE3_SCORE_THRESHOLD = 92

# Notion sync 대상 DB ID (환경변수 우선)
NOTION_DB_ID = os.environ.get("NOTION_PE_DB_ID", "")
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")

# ─────────────────────────────────────────────
# CORE SCAN LOGIC
# ─────────────────────────────────────────────

def discover_prompts(repo_root: Path, dirs: List[str]) -> List[Dict]:
    """
    PROMPT_DIRS 목록을 재귀 스캔하여 .md 프롬프트 파일을 수집.
    v6.1: PE2-variants/ 하위 파일도 자동 포함.
    """
    discovered = []
    for rel_dir in dirs:
        base = repo_root / rel_dir
        if not base.exists():
            print(f"[WARN] 디렉토리 없음, 스킵: {rel_dir}")
            continue
        # 재귀 glob으로 하위 디렉토리까지 수집
        for md_file in sorted(base.rglob("*.md")):
            # README, CHANGELOG 등 메타 파일 제외
            if md_file.stem.upper() in {"README", "CHANGELOG", "INDEX", "TEMPLATE"}:
                continue
            rel_path = md_file.relative_to(repo_root)
            meta = extract_metadata(md_file)
            discovered.append({
                "path": str(rel_path),
                "name": md_file.stem,
                "domain": infer_domain(rel_path),
                "variant_type": infer_variant_type(md_file.stem),
                "pe3_score": meta.get("pe3_score"),
                "version": meta.get("version", "—"),
                "last_updated": meta.get("last_updated", "—"),
            })
    return discovered


def extract_metadata(filepath: Path) -> Dict:
    """파일 헤더에서 PE-3 점수, 버전, 날짜 추출."""
    meta = {}
    try:
        content = filepath.read_text(encoding="utf-8")
        # PE-3 점수 패턴: "PE-3: 92" 또는 "PE3_SCORE: 93"
        m = re.search(r"PE-?3[_\s:\-]+score[^\d]*(\d+)", content, re.IGNORECASE)
        if m:
            meta["pe3_score"] = int(m.group(1))
        # 버전 패턴: "version: v6.1" 또는 "## v6.1"
        m2 = re.search(r"(?:version|ver)[:\s]+v?([\d.]+)", content, re.IGNORECASE)
        if m2:
            meta["version"] = f"v{m2.group(1)}"
        # 날짜 패턴: "2026-05-07"
        m3 = re.search(r"(\d{4}-\d{2}-\d{2})", content)
        if m3:
            meta["last_updated"] = m3.group(1)
    except Exception as e:
        print(f"[WARN] 메타데이터 추출 실패 ({filepath.name}): {e}")
    return meta


def infer_domain(rel_path: Path) -> str:
    """경로 기반 도메인 추론."""
    parts = rel_path.parts
    if "PE-CON" in parts:
        return "PE-CON"
    elif "PE-FIN" in parts:
        return "PE-FIN"
    elif "PE-SEMI" in parts:
        return "PE-SEMI"
    return "GENERAL"


def infer_variant_type(stem: str) -> str:
    """파일명에서 A형/B형/원본 구분."""
    stem_upper = stem.upper()
    if stem_upper.endswith("-A"):
        return "A_DEEPSPEC"
    elif stem_upper.endswith("-B"):
        return "B_COMPRESSED"
    else:
        return "ORIGINAL"


# ─────────────────────────────────────────────
# VALIDATION GATE
# ─────────────────────────────────────────────

def validate_pe3_scores(prompts: List[Dict]) -> Dict:
    """
    PE-3 점수 검증 게이트.
    임계값(92) 미달 프롬프트를 식별하여 경고 출력.
    """
    below_threshold = []
    no_score = []
    for p in prompts:
        score = p.get("pe3_score")
        if score is None:
            no_score.append(p["name"])
        elif score < PE3_SCORE_THRESHOLD:
            below_threshold.append({"name": p["name"], "score": score})

    report = {
        "total": len(prompts),
        "passed": len(prompts) - len(below_threshold) - len(no_score),
        "below_threshold": below_threshold,
        "no_score": no_score,
        "threshold": PE3_SCORE_THRESHOLD,
        "timestamp": datetime.now().isoformat(),
    }

    if below_threshold:
        print(f"[WARN] PE-3 {PE3_SCORE_THRESHOLD}점 미달 {len(below_threshold)}종:")
        for item in below_threshold:
            print(f"       - {item['name']}: {item['score']}pt")
    if no_score:
        print(f"[INFO] PE-3 점수 미기재 {len(no_score)}종: {no_score}")

    return report


# ─────────────────────────────────────────────
# NOTION SYNC (stub — 실제 API 키 필요)
# ─────────────────────────────────────────────

def sync_to_notion(prompts: List[Dict], dry_run: bool = True) -> None:
    """
    Notion DB에 프롬프트 목록 동기화.
    dry_run=True: 실제 API 호출 없이 로컬 JSON 출력만 수행.
    """
    if not NOTION_TOKEN or not NOTION_DB_ID:
        print("[INFO] NOTION_TOKEN / NOTION_DB_ID 미설정 — dry_run 모드로 실행")
        dry_run = True

    output_path = REPO_ROOT / "PE-CON" / "scores" / "sync_manifest.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    manifest = {
        "generated_at": datetime.now().isoformat(),
        "version": "v6.1",
        "dry_run": dry_run,
        "prompt_count": len(prompts),
        "prompts": prompts,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"[OK] sync_manifest.json 저장 완료 ({len(prompts)}종) → {output_path}")

    if not dry_run:
        # 실제 Notion API 호출 로직 (향후 구현)
        print("[TODO] Notion API 실제 호출 로직 구현 필요")


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

def main():
    print("="*60)
    print(f"T-09 Sync Engine v6.1 — {datetime.now().strftime('%Y-%m-%d %H:%M KST')}")
    print(f"스캔 대상 디렉토리: {PROMPT_DIRS}")
    print("="*60)

    # Step 1: 프롬프트 탐색
    prompts = discover_prompts(REPO_ROOT, PROMPT_DIRS)
    print(f"\n[SCAN] 총 {len(prompts)}종 프롬프트 발견")
    for p in prompts:
        score_str = f"PE-3:{p['pe3_score']}" if p['pe3_score'] else "점수없음"
        print(f"  [{p['domain']}][{p['variant_type']:<12}] {p['name']:<30} {score_str}")

    # Step 2: PE-3 검증 게이트
    print("\n[VALIDATE] PE-3 점수 검증 중...")
    validation = validate_pe3_scores(prompts)
    print(f"  통과: {validation['passed']}/{validation['total']} | "
          f"미달: {len(validation['below_threshold'])} | "
          f"미기재: {len(validation['no_score'])}")

    # Step 3: Notion 동기화
    print("\n[SYNC] Notion 동기화 실행 중...")
    sync_to_notion(prompts, dry_run=True)

    print("\n[DONE] T-09 sync 완료")
    return validation


if __name__ == "__main__":
    main()
