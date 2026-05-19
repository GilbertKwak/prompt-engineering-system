#!/usr/bin/env python3
"""
automation/ai_ew_detector.py
C-31 EW (Early Warning) 자동 탐지기

Usage (workflow에서 호출되는 방식 — 정확한 인터페이스):
  python automation/ai_ew_detector.py \
    --input-dir output/ai_intel \
    --thresholds '{"enterprise_adoption_rate": {"threshold": 40, ...}}' \
    --week 2026-W21 \
    --output output/ai_intel/ew_report.json

NOTE: --thresholds는 JSON 문자열 또는 JSON 파일 경로를 모두 허용
"""

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

# ──────────────────────────────────────────
# EW 기본 임계값 (workflow에서 --thresholds로 오버라이드 가능)
# ──────────────────────────────────────────
DEFAULT_THRESHOLDS = {
    "enterprise_adoption_rate": {"threshold": 40, "direction": "below", "signal": "EW-AI-DEPLOY"},
    "oss_rag_migration_rate": {"threshold": 50, "direction": "above", "signal": "EW-RAG-OSS"},
    "new_model_releases_per_week": {"threshold": 8, "direction": "above", "signal": "EW-MODEL-FLOOD"},
    "ai_consulting_market_disruption": {"threshold": 0.5, "direction": "above", "signal": "EW-CONSULT"},
    "container_ml_adoption": {"threshold": 55, "direction": "below", "signal": "EW-INFRA"},
    "multi_agent_orchestration_adoption": {"threshold": 30, "direction": "above", "signal": "EW-ORCH"},
}

# EW 경고 키워드 (휴리스틱 보완)
EW_KEYWORDS = {
    "EW-AI-DEPLOY": [
        "enterprise adoption slow", "deployment stall", "low adoption",
        "enterprises struggle", "adoption barrier", "deployment blocked",
    ],
    "EW-RAG-OSS": [
        "oss rag", "open source rag", "migrate from openai", "langchain migration",
        "pgvector adoption", "self-hosted rag",
    ],
    "EW-MODEL-FLOOD": [
        "model release surge", "new model every week", "model proliferation",
        "too many models", "weekly model",
    ],
    "EW-CONSULT": [
        "consulting disruption", "ai replaces consultant", "mckinsey automation",
        "consulting market shift",
    ],
    "EW-INFRA": [
        "container adoption low", "kubernetes ai", "ml infrastructure gap",
        "gpu shortage", "compute bottleneck",
    ],
    "EW-ORCH": [
        "multi-agent", "agent orchestration", "agentic workflow",
        "langgraph production", "crewai production",
    ],
}

SEVERITY_MAP = {
    0: "NONE",
    1: "LOW",
    2: "MEDIUM",
    3: "HIGH",
}


def load_thresholds(thresholds_arg: str | None) -> dict:
    """--thresholds 인자 파싱: JSON 문자열 또는 파일 경로 모두 허용"""
    if not thresholds_arg:
        return DEFAULT_THRESHOLDS

    # 파일 경로인 경우
    if os.path.isfile(thresholds_arg):
        with open(thresholds_arg, encoding="utf-8") as f:
            return json.load(f)

    # JSON 문자열인 경우
    try:
        parsed = json.loads(thresholds_arg)
        return parsed if parsed else DEFAULT_THRESHOLDS
    except json.JSONDecodeError:
        print(f"[WARN] --thresholds 파싱 실패. 기본 임계값 사용.")
        return DEFAULT_THRESHOLDS


def load_intel_files(input_dir: str) -> list[dict]:
    """input-dir에서 intel_*.json 파일 전체 로드"""
    dir_path = Path(input_dir)
    intel_files = list(dir_path.glob("intel_*.json"))
    if not intel_files:
        print(f"[WARN] {input_dir}에서 intel_*.json 파일을 찾을 수 없음")
        return []

    results = []
    for f in intel_files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            results.append(data)
            print(f"  [LOADED] {f.name}: metrics={len(data.get('metrics', {}))}")
        except Exception as e:
            print(f"  [ERROR] {f.name} 로드 실패: {e}")
    return results


def check_metric_threshold(value: float, threshold: float, direction: str) -> bool:
    """방향성에 따른 임계값 체크"""
    if direction == "above":
        return value > threshold
    elif direction == "below":
        return value < threshold
    return False


def keyword_heuristic_check(
    intel_list: list[dict], signal_id: str, keywords: list[str]
) -> int:
    """모든 인텔 텍스트에서 키워드 hit count 반환"""
    combined_text = ""
    for intel in intel_list:
        for qr in intel.get("query_results", []):
            combined_text += qr.get("content_raw", "").lower() + " "
        combined_text += " ".join(intel.get("key_facts", [])).lower() + " "

    hits = sum(1 for kw in keywords if kw.lower() in combined_text)
    return hits


def detect_ew_signals(intel_list: list[dict], thresholds: dict, week: str) -> dict:
    """EW 신호 탐지 메인 로직"""
    signals = []
    metrics_found = {}

    # 전체 인텔에서 메트릭 통합
    for intel in intel_list:
        for k, v in intel.get("metrics", {}).items():
            if k not in metrics_found:
                metrics_found[k] = v
            else:
                # 평균값 사용
                metrics_found[k] = (metrics_found[k] + v) / 2

    print(f"\n[INFO] 통합 메트릭: {list(metrics_found.keys())}")

    for metric_key, config in thresholds.items():
        threshold = config["threshold"]
        direction = config["direction"]
        signal_id = config["signal"]

        triggered = False
        trigger_source = None
        value_used = None

        # 1순위: 실제 메트릭 값 체크
        if metric_key in metrics_found:
            val = metrics_found[metric_key]
            value_used = val
            if check_metric_threshold(val, threshold, direction):
                triggered = True
                trigger_source = "metric"
                print(f"  [EW] {signal_id} 발동: {metric_key}={val} ({direction} {threshold})")

        # 2순위: 키워드 휴리스틱 (메트릭 없거나 미발동 시 보완)
        if not triggered and signal_id in EW_KEYWORDS:
            hits = keyword_heuristic_check(intel_list, signal_id, EW_KEYWORDS[signal_id])
            if hits >= 2:  # 2회 이상 hit 시 EW 발동
                triggered = True
                trigger_source = "heuristic"
                value_used = hits
                print(f"  [EW] {signal_id} 발동 (휴리스틱): keyword_hits={hits}")

        if triggered:
            signals.append({
                "id": signal_id,
                "metric": metric_key,
                "value": value_used,
                "threshold": threshold,
                "direction": direction,
                "trigger_source": trigger_source,
                "severity": _calc_severity(value_used, threshold, direction),
            })

    # 최대 심각도 계산
    max_severity_num = max(
        [_severity_num(s["severity"]) for s in signals], default=0
    )
    max_severity = SEVERITY_MAP.get(max_severity_num, "NONE")

    report = {
        "week": week,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "triggered": len(signals) > 0,
        "signal_count": len(signals),
        "signals": signals,
        "max_severity": max_severity,
        "metrics_found": metrics_found,
        "intel_domain_count": len(intel_list),
    }

    print(f"\n[RESULT] EW 발동: {report['triggered']} | 신호: {len(signals)}개 | 최대 심각도: {max_severity}")
    return report


def _calc_severity(value, threshold, direction) -> str:
    """값과 임계값 차이로 심각도 계산"""
    if value is None:
        return "LOW"
    try:
        v = float(value)
        t = float(threshold)
        diff_pct = abs(v - t) / max(t, 1) * 100
        if diff_pct >= 30:
            return "HIGH"
        elif diff_pct >= 15:
            return "MEDIUM"
        else:
            return "LOW"
    except (TypeError, ValueError):
        return "LOW"


def _severity_num(severity: str) -> int:
    return {"NONE": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3}.get(severity, 0)


def main():
    parser = argparse.ArgumentParser(description="AI EW Detector — C-31 신호 탐지")
    parser.add_argument("--input-dir", required=True, help="intel_*.json 파일이 있는 디렉토리")
    parser.add_argument(
        "--thresholds",
        default=None,
        help="EW 임계값 JSON 문자열 또는 파일 경로 (미입력시 기본값 사용)",
    )
    parser.add_argument("--week", required=True, help="주간 레이블 (예: 2026-W21)")
    parser.add_argument("--output", required=True, help="EW 리포트 출력 경로")
    args = parser.parse_args()

    thresholds = load_thresholds(args.thresholds)
    intel_list = load_intel_files(args.input_dir)

    if not intel_list:
        print("[WARN] 인텔 데이터 없음. 빈 EW 리포트 생성.")
        report = {
            "week": args.week,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "triggered": False,
            "signal_count": 0,
            "signals": [],
            "max_severity": "NONE",
            "metrics_found": {},
            "intel_domain_count": 0,
        }
    else:
        report = detect_ew_signals(intel_list, thresholds, args.week)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[SAVED] {out_path}")


if __name__ == "__main__":
    main()
