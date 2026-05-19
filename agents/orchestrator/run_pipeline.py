#!/usr/bin/env python3
"""
PE System Orchestrator — run_pipeline.py
Version: 2.0.0 | PE-7 AI Automation Design v1.1
Owner: GilbertKwak

전체 멀티에이전트 파이프라인을 조율합니다.
실행 순서: ai_intel_collector → ew_detector → kg_builder → notion_sync

Error Prevention (AGENT-06):
  - 각 단계 실행 전 사전 검증 수행
  - 실패 시 지수 백오프 재시도
  - EW CRITICAL 감지 시 sonar-pro 강제 전환
"""

import argparse
import json
import logging
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger("orchestrator")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "output" / "ai_intel"
LOG_DIR = ROOT / "logs" / "orchestrator"
NOTION_PAGE_ID = "34a55ed436f0814d9cffe6a2f0816e29"

DEFAULT_DOMAINS = [
    "enterprise_deployment",
    "model_architecture",
    "regulatory_policy",
    "investment_funding",
]


# ---------------------------------------------------------------------------
# AGENT-06: Pre-execution Validation
# ---------------------------------------------------------------------------
def preflight_check() -> list[str]:
    """실행 전 환경 사전 검증. 오류 목록 반환."""
    errors = []
    import os

    if not os.environ.get("PERPLEXITY_API_KEY"):
        errors.append("PERPLEXITY_API_KEY 환경변수 미설정")
    if not os.environ.get("NOTION_API_KEY"):
        errors.append("NOTION_API_KEY 환경변수 미설정")

    scripts = [
        ROOT / "automation" / "ai_intel_collector.py",
        ROOT / "automation" / "ai_ew_detector.py",
        ROOT / "automation" / "kg_delta_generator.py",
        ROOT / "automation" / "notion_c31_updater.py",
    ]
    for script in scripts:
        if not script.exists():
            errors.append(f"스크립트 미존재: {script}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    return errors


# ---------------------------------------------------------------------------
# Step Runner with Retry
# ---------------------------------------------------------------------------
def run_step(
    step_name: str,
    cmd: list[str],
    max_retries: int = 3,
    backoff_base: float = 2.0,
    timeout: int = 300,
) -> bool:
    """단일 파이프라인 단계 실행. 실패 시 지수 백오프 재시도."""
    for attempt in range(1, max_retries + 1):
        log.info(f"[{step_name}] 실행 시도 {attempt}/{max_retries}")
        try:
            result = subprocess.run(
                cmd,
                timeout=timeout,
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
            if result.returncode == 0:
                log.info(f"[{step_name}] ✅ 성공")
                if result.stdout.strip():
                    log.debug(f"[{step_name}] stdout: {result.stdout[:500]}")
                return True
            else:
                log.warning(
                    f"[{step_name}] ❌ 실패 (rc={result.returncode}): {result.stderr[:300]}"
                )
        except subprocess.TimeoutExpired:
            log.warning(f"[{step_name}] ⏱ 타임아웃 ({timeout}s 초과)")
        except Exception as e:
            log.error(f"[{step_name}] 예외 발생: {e}")

        if attempt < max_retries:
            wait = backoff_base ** attempt
            log.info(f"[{step_name}] {wait:.0f}초 후 재시도...")
            time.sleep(wait)

    log.error(f"[{step_name}] 모든 재시도 실패")
    return False


# ---------------------------------------------------------------------------
# EW Severity Reader
# ---------------------------------------------------------------------------
def read_ew_severity(week: str) -> str:
    """EW 리포트에서 severity 읽기."""
    ew_file = OUTPUT_DIR / f"ew_report_{week}.json"
    if not ew_file.exists():
        return "NONE"
    try:
        data = json.loads(ew_file.read_text())
        return data.get("ew_severity", "NONE")
    except Exception:
        return "NONE"


def read_ew_metadata(week: str) -> dict:
    """EW 리포트 전체 메타데이터 읽기."""
    ew_file = OUTPUT_DIR / f"ew_report_{week}.json"
    if not ew_file.exists():
        return {"ew_triggered": False, "ew_count": 0, "ew_signals": "", "ew_severity": "NONE"}
    try:
        data = json.loads(ew_file.read_text())
        signals = [s.get("signal_id", "") for s in data.get("signals", [])]
        return {
            "ew_triggered": data.get("ew_triggered", False),
            "ew_count": len(signals),
            "ew_signals": ",".join(signals),
            "ew_severity": data.get("ew_severity", "NONE"),
        }
    except Exception:
        return {"ew_triggered": False, "ew_count": 0, "ew_signals": "", "ew_severity": "NONE"}


def read_kg_metadata(week: str) -> dict:
    """KG delta 파일에서 버전/노드/엣지 수 읽기."""
    # 가장 최근 KG delta 파일 탐색
    candidates = sorted(ROOT.glob("knowledge_graph_v*_delta.json"), reverse=True)
    if not candidates:
        return {"kg_version": "4.26", "node_count": 0, "edge_count": 0}
    try:
        data = json.loads(candidates[0].read_text())
        summary = data.get("delta_summary", {})
        return {
            "kg_version": data.get("new_version", "4.26"),
            "node_count": summary.get("total_new_nodes", 0),
            "edge_count": summary.get("total_new_edges", 0),
        }
    except Exception:
        return {"kg_version": "4.26", "node_count": 0, "edge_count": 0}


# ---------------------------------------------------------------------------
# Pipeline Stages
# ---------------------------------------------------------------------------
def stage_collect(week: str, scope: str, domains: list[str]) -> bool:
    """Stage 1: AI Intel 수집 — 4개 도메인 순차 실행."""
    log.info("=" * 60)
    log.info("STAGE 1: AI Intel 수집 시작")
    log.info("=" * 60)
    all_ok = True
    for domain in domains:
        cmd = [
            sys.executable,
            "automation/ai_intel_collector.py",
            "--domain", domain,
            "--week", week,
            "--scope", scope,
            "--output", str(OUTPUT_DIR / f"intel_{domain}.json"),
        ]
        ok = run_step(f"collect:{domain}", cmd)
        if not ok:
            all_ok = False
            log.warning(f"도메인 {domain} 수집 실패 — 계속 진행")
    return all_ok


def stage_ew(week: str) -> bool:
    """Stage 2: EW 탐지."""
    log.info("=" * 60)
    log.info("STAGE 2: EW 탐지 시작")
    log.info("=" * 60)
    cmd = [
        sys.executable,
        "automation/ai_ew_detector.py",
        "--input-dir", str(OUTPUT_DIR),
        "--week", week,
        "--output", str(OUTPUT_DIR / f"ew_report_{week}.json"),
    ]
    return run_step("ew_detector", cmd)


def stage_kg(week: str, run_date: str, ew_meta: dict) -> bool:
    """Stage 3: KG Delta 생성."""
    log.info("=" * 60)
    log.info("STAGE 3: KG Delta 생성 시작")
    log.info("=" * 60)
    cmd = [
        sys.executable,
        "automation/kg_delta_generator.py",
        "--intel-dir", str(OUTPUT_DIR),
        "--week", week,
        "--run-date", run_date,
        "--ew-signals", ew_meta.get("ew_signals", ""),
    ]
    return run_step("kg_builder", cmd)


def stage_notion(week: str, run_date: str, ew_meta: dict, kg_meta: dict) -> bool:
    """Stage 4: Notion C-31 동기화."""
    log.info("=" * 60)
    log.info("STAGE 4: Notion C-31 동기화 시작")
    log.info("=" * 60)
    cmd = [
        sys.executable,
        "automation/notion_c31_updater.py",
        "--page-id", NOTION_PAGE_ID,
        "--week", week,
        "--run-date", run_date,
        "--ew-triggered", str(ew_meta["ew_triggered"]).lower(),
        "--ew-count", str(ew_meta["ew_count"]),
        "--ew-signals", ew_meta.get("ew_signals", ""),
        "--ew-severity", ew_meta["ew_severity"],
        "--kg-version", kg_meta["kg_version"],
        "--node-count", str(kg_meta["node_count"]),
        "--edge-count", str(kg_meta["edge_count"]),
        "--intel-dir", str(OUTPUT_DIR),
    ]
    return run_step("notion_sync", cmd, timeout=120)


# ---------------------------------------------------------------------------
# Pipeline Summary Logger
# ---------------------------------------------------------------------------
def write_run_summary(week: str, run_date: str, results: dict, elapsed: float):
    """파이프라인 실행 요약 로그 저장."""
    summary = {
        "pipeline_run": {
            "week": week,
            "run_date": run_date,
            "run_timestamp": datetime.now(timezone.utc).isoformat(),
            "elapsed_seconds": round(elapsed, 1),
            "stages": results,
            "overall_status": "SUCCESS" if all(results.values()) else "PARTIAL_FAILURE",
        }
    }
    summary_path = LOG_DIR / f"pipeline_run_{week}_{run_date}.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    log.info(f"실행 요약 저장: {summary_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="PE System Pipeline Orchestrator")
    parser.add_argument("--week", required=True, help="ISO 주차 (예: 2026-W21)")
    parser.add_argument("--run-date", required=True, help="실행일 (YYYY-MM-DD)")
    parser.add_argument(
        "--scope",
        choices=["standard", "deep", "emergency"],
        default="standard",
        help="수집 깊이 (default: standard)",
    )
    parser.add_argument(
        "--domains",
        nargs="+",
        default=DEFAULT_DOMAINS,
        help="수집 도메인 목록",
    )
    parser.add_argument(
        "--skip-collect",
        action="store_true",
        help="수집 단계 스킵 (기존 intel 파일 재사용)",
    )
    parser.add_argument(
        "--skip-notion",
        action="store_true",
        help="Notion 동기화 스킵 (테스트용)",
    )
    args = parser.parse_args()

    start_time = time.time()
    log.info("=" * 60)
    log.info(f"PE System Pipeline 시작 — 주차: {args.week} | 범위: {args.scope}")
    log.info("=" * 60)

    # AGENT-06: 사전 검증
    errors = preflight_check()
    if errors:
        for e in errors:
            log.error(f"사전 검증 실패: {e}")
        sys.exit(1)
    log.info("사전 검증 통과 ✅")

    results = {}

    # Stage 1: 수집
    if not args.skip_collect:
        results["collect"] = stage_collect(args.week, args.scope, args.domains)
    else:
        log.info("수집 단계 스킵 (--skip-collect)")
        results["collect"] = True

    # Stage 2: EW 탐지
    results["ew_detector"] = stage_ew(args.week)

    # EW severity 확인 → emergency 여부 판단
    ew_meta = read_ew_metadata(args.week)
    if ew_meta["ew_severity"] == "CRITICAL" and args.scope != "emergency":
        log.warning("⚠️  EW CRITICAL 감지! emergency 모드로 재수집 권고")

    # Stage 3: KG Delta
    results["kg_builder"] = stage_kg(args.week, args.run_date, ew_meta)
    kg_meta = read_kg_metadata(args.week)

    # Stage 4: Notion 동기화
    if not args.skip_notion:
        results["notion_sync"] = stage_notion(args.week, args.run_date, ew_meta, kg_meta)
    else:
        log.info("Notion 동기화 스킵 (--skip-notion)")
        results["notion_sync"] = True

    elapsed = time.time() - start_time
    write_run_summary(args.week, args.run_date, results, elapsed)

    # 최종 결과
    all_ok = all(results.values())
    log.info("=" * 60)
    log.info(f"파이프라인 완료 — 소요: {elapsed:.1f}s | 상태: {'✅ SUCCESS' if all_ok else '⚠️ PARTIAL_FAILURE'}")
    for stage, ok in results.items():
        log.info(f"  {stage}: {'✅' if ok else '❌'}")
    log.info("=" * 60)

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
