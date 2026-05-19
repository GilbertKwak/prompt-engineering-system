#!/usr/bin/env python3
"""
PE System Orchestrator — Multi-Agent Pipeline Runner
Version: 2.0.0 | Updated: 2026-05-20

실행 방법:
  # 전체 파이프라인 (기본)
  python agents/orchestrator/run_pipeline.py --week 2026-W21

  # 특정 도메인만
  python agents/orchestrator/run_pipeline.py --week 2026-W21 --domains enterprise_deployment,model_architecture

  # 긴급 모드 (EW CRITICAL)
  python agents/orchestrator/run_pipeline.py --week 2026-W21 --mode emergency

  # dry-run (실제 API 호출 없이 파이프라인 검증)
  python agents/orchestrator/run_pipeline.py --week 2026-W21 --dry-run
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml

# ---------------------------------------------------------------------------
# 설정
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent.parent
AGENT_INDEX_PATH = REPO_ROOT / "agents" / "agent_index.yaml"
LOG_DIR = REPO_ROOT / "logs" / "orchestrator"
OUTPUT_DIR = REPO_ROOT / "output"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [ORCHESTRATOR] %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("orchestrator")


# ---------------------------------------------------------------------------
# 에이전트 인덱스 로더
# ---------------------------------------------------------------------------
def load_agent_index() -> dict:
    """agent_index.yaml 로드"""
    with open(AGENT_INDEX_PATH) as f:
        return yaml.safe_load(f)


def get_agent_config(agent_index: dict, agent_id: str) -> Optional[dict]:
    """에이전트 ID로 설정 조회"""
    for agent in agent_index["agents"]:
        if agent["id"] == agent_id:
            return agent
    return None


# ---------------------------------------------------------------------------
# 파이프라인 라우터
# ---------------------------------------------------------------------------
def resolve_pipeline(agent_index: dict, mode: str, ew_severity: str = "NONE") -> list:
    """실행 모드와 EW 심각도에 따라 파이프라인 결정"""
    routing = agent_index["routing"]

    if mode == "emergency" or ew_severity == "CRITICAL":
        for route in routing["conditional_routes"]:
            if route["condition"] == "ew_severity == CRITICAL":
                return route["pipeline"]

    return routing["default_pipeline"]


# ---------------------------------------------------------------------------
# 에이전트 실행기
# ---------------------------------------------------------------------------
def run_agent(
    agent_id: str,
    script_path: str,
    args: list,
    dry_run: bool = False,
    timeout: int = 300,
) -> dict:
    """
    단일 에이전트 실행 및 결과 반환
    Returns: {success: bool, duration: float, returncode: int, stdout: str, stderr: str}
    """
    start_time = time.time()
    script_abs = REPO_ROOT / script_path

    logger.info(f"▶ Starting agent: {agent_id}")
    logger.info(f"  Script: {script_abs}")
    logger.info(f"  Args: {' '.join(args)}")

    if dry_run:
        logger.info(f"  [DRY-RUN] Skipping actual execution")
        duration = time.time() - start_time
        return {"success": True, "duration": duration, "returncode": 0,
                "stdout": "[dry-run]", "stderr": "", "dry_run": True}

    try:
        cmd = [sys.executable, str(script_abs)] + args
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(REPO_ROOT),
        )
        duration = time.time() - start_time
        success = result.returncode == 0

        if success:
            logger.info(f"  ✅ {agent_id} completed in {duration:.1f}s")
        else:
            logger.error(f"  ❌ {agent_id} failed (rc={result.returncode}) in {duration:.1f}s")
            logger.error(f"  STDERR: {result.stderr[:500]}")

        return {
            "success": success,
            "duration": duration,
            "returncode": result.returncode,
            "stdout": result.stdout[:2000],
            "stderr": result.stderr[:1000],
        }

    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        logger.error(f"  ⏰ {agent_id} timed out after {timeout}s")
        return {"success": False, "duration": duration, "returncode": -1,
                "stdout": "", "stderr": f"Timeout after {timeout}s"}
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"  💥 {agent_id} exception: {e}")
        return {"success": False, "duration": duration, "returncode": -2,
                "stdout": "", "stderr": str(e)}


# ---------------------------------------------------------------------------
# 메인 파이프라인
# ---------------------------------------------------------------------------
def run_pipeline(
    week: str,
    run_date: str,
    mode: str = "standard",
    intel_scope: str = "standard",
    domains: Optional[list] = None,
    kg_version_current: str = "4.25",
    kg_version_next: str = "4.26",
    notion_page_id: str = "34a55ed436f0814d9cffe6a2f0816e29",
    dry_run: bool = False,
) -> dict:
    """전체 파이프라인 실행"""

    logger.info("=" * 60)
    logger.info(f"PE SYSTEM ORCHESTRATOR v2.0.0")
    logger.info(f"Week: {week} | Mode: {mode} | DryRun: {dry_run}")
    logger.info("=" * 60)

    # 에이전트 인덱스 로드
    agent_index = load_agent_index()
    pipeline = resolve_pipeline(agent_index, mode)
    logger.info(f"Pipeline: {' → '.join(pipeline)}")

    # 출력 디렉토리 준비
    intel_dir = OUTPUT_DIR / "ai_intel"
    intel_dir.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    results = {}
    ew_triggered = False
    ew_count = 0
    ew_signals = ""
    ew_severity = "NONE"

    # 도메인 목록 결정
    all_domains = ["enterprise_deployment", "model_architecture",
                   "regulatory_policy", "investment_funding"]
    active_domains = domains or all_domains

    # -------------------------------------------------------------------------
    # STEP 1: AI Intel Collector
    # -------------------------------------------------------------------------
    if "ai_intel_collector" in pipeline:
        for domain in active_domains:
            args = [
                "--domain", domain,
                "--week", week,
                "--scope", intel_scope,
                "--queries", f"{domain} AI trends 2026",
                "--output", str(intel_dir / f"intel_{domain}.json"),
            ]
            result = run_agent(
                f"ai_intel_collector.{domain}",
                "automation/ai_intel_collector.py",
                args,
                dry_run=dry_run,
                timeout=agent_index["global"].get("timeout_per_agent", 300) // len(active_domains),
            )
            results[f"ai_intel.{domain}"] = result

    # -------------------------------------------------------------------------
    # STEP 2: EW Detector
    # -------------------------------------------------------------------------
    if "ew_detector" in pipeline:
        ew_output = str(intel_dir / "ew_report.json")
        args = [
            "--input-dir", str(intel_dir),
            "--week", week,
            "--output", ew_output,
        ]
        result = run_agent("ew_detector", "automation/ai_ew_detector.py", args,
                           dry_run=dry_run)
        results["ew_detector"] = result

        # EW 결과 파싱
        if result["success"] and not dry_run:
            try:
                ew_report_path = Path(ew_output)
                if ew_report_path.exists():
                    with open(ew_report_path) as f:
                        ew_report = json.load(f)
                    ew_triggered = ew_report.get("ew_triggered", False)
                    ew_count = ew_report.get("ew_count", 0)
                    ew_severity = ew_report.get("severity", "NONE")
                    ew_signals = json.dumps(
                        ew_report.get("signals", []), ensure_ascii=False
                    )
                    logger.info(f"EW Check: triggered={ew_triggered}, "
                                f"severity={ew_severity}, count={ew_count}")
            except Exception as e:
                logger.warning(f"EW report parsing failed: {e}")

    # EW CRITICAL 시 모드 업그레이드
    if ew_severity == "CRITICAL" and mode != "emergency":
        logger.warning("🚨 EW CRITICAL detected! Upgrading to emergency mode.")
        mode = "emergency"
        pipeline = resolve_pipeline(agent_index, "emergency", "CRITICAL")

    # -------------------------------------------------------------------------
    # STEP 3: KG Builder
    # -------------------------------------------------------------------------
    if "kg_builder" in pipeline:
        args = [
            "--intel-dir", str(intel_dir),
            "--current-version", kg_version_current,
            "--next-version", kg_version_next,
            "--week", week,
            "--run-date", run_date,
            "--ew-signals", ew_signals,
            "--output", f"knowledge_graph_v{kg_version_next}_delta.json",
        ]
        if ew_triggered:
            args += ["--ew-triggered"]
        result = run_agent("kg_builder", "automation/kg_delta_generator.py", args,
                           dry_run=dry_run)
        results["kg_builder"] = result

    # -------------------------------------------------------------------------
    # STEP 4: Notion Sync
    # -------------------------------------------------------------------------
    if "notion_sync" in pipeline:
        args = [
            "--page-id", notion_page_id,
            "--week", week,
            "--run-date", run_date,
            "--ew-triggered", str(ew_triggered).lower(),
            "--ew-count", str(ew_count),
            "--ew-signals", ew_signals,
            "--ew-severity", ew_severity,
            "--kg-version", kg_version_next,
            "--node-count", "5",
            "--edge-count", "3",
            "--intel-dir", str(intel_dir),
        ]
        result = run_agent("notion_sync", "automation/notion_c31_updater.py", args,
                           dry_run=dry_run)
        results["notion_sync"] = result

    # -------------------------------------------------------------------------
    # 파이프라인 결과 집계
    # -------------------------------------------------------------------------
    