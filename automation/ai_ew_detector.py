#!/usr/bin/env python3
"""
ai_ew_detector.py
─────────────────
AI Intel 데이터 → C-31 EW(Early Warning) 신호 탐지기
워크플로: ai-intel-weekly.yml → STAGE 2

사용법:
  python automation/ai_ew_detector.py \
    --input-dir output/ai_intel \
    --thresholds '{"enterprise_adoption_rate": {"threshold": 40, ...}}' \
    --week 2026-W21 \
    --output output/ai_intel/ew_report.json
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


# ─────────────────────────────────────────
# EW 시그널 정의 (워크플로와 동기화)
# ─────────────────────────────────────────
DEFAULT_THRESHOLDS = {
    "enterprise_adoption_rate":           {"threshold": 40,  "direction": "below", "signal": "EW-AI-DEPLOY",  "severity": "HIGH",   "domain": "enterprise_deployment"},
    "oss_rag_migration_rate":             {"threshold": 50,  "direction": "above", "signal": "EW-RAG-OSS",    "severity": "MEDIUM", "domain": "frameworks_rag"},
    "new_model_releases_per_week":        {"threshold": 8,   "direction": "above", "signal": "EW-MODEL-FLOOD","severity": "MEDIUM", "domain": "model_releases"},
    "ai_consulting_market_disruption":    {"threshold": 0.5, "direction": "above", "signal": "EW-CONSULT",    "severity": "HIGH",   "domain": "enterprise_deployment"},
    "container_ml_adoption":              {"threshold": 55,  "direction": "below", "signal": "EW-INFRA",      "severity": "LOW",    "domain": "infra_market"},
    "multi_agent_orchestration_adoption": {"threshold": 30,  "direction": "above", "signal": "EW-ORCH",       "severity": "MEDIUM", "domain": "frameworks_rag"},
}

SEVERITY_RANK = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}


# ─────────────────────────────────────────
# 인텔 파일 로드
# ─────────────────────────────────────────
def load_intel_files(input_dir: str) -> dict[str, dict]:
    """output/ai_intel/intel_*.json 파일 전체 로드"""
    intel_dir = Path(input_dir)
    intel_data = {}

    for f in intel_dir.glob("intel_*.json"):
        domain_key = f.stem.replace("intel_", "")
        try:
            with open(f, encoding="utf-8") as fp:
                intel_data[domain_key] = json.load(fp)
            print(f"[INFO] Loaded: {f.name}", file=sys.stderr)
        except Exception as e:
            print(f"[WARN] Failed to load {f.name}: {e}", file=sys.stderr)

    print(f"[INFO] Total intel files loaded: {len(intel_data)}", file=sys.stderr)
    return intel_data


# ─────────────────────────────────────────
# 메트릭 추출 (숫자 파싱)
# ─────────────────────────────────────────
def extract_metric_value(intel_data: dict, metric_key: str) -> float | None:
    """
    인텔 데이터에서 특정 메트릭 값 추출
    우선순위: metrics 필드 직접 → key_facts 텍스트 파싱 → summary 텍스트 파싱
    """
    # 1. metrics 딕셔너리에서 직접 조회
    for domain_data in intel_data.values():
        metrics = domain_data.get("metrics", {})
        if metric_key in metrics:
            try:
                return float(metrics[metric_key])
            except (ValueError, TypeError):
                pass

        # 유사 키 매칭 (underscores → spaces 또는 부분 일치)
        for k, v in metrics.items():
            if metric_key.lower() in k.lower() or k.lower() in metric_key.lower():
                try:
                    return float(v)
                except (ValueError, TypeError):
                    pass

    # 2. key_facts 및 summary에서 숫자 추출 (키워드 매칭)
    keyword_map = {
        "enterprise_adoption_rate":           ["enterprise adoption", "enterprise ai adoption", "enterprise deployment rate"],
        "oss_rag_migration_rate":             ["oss rag", "open source rag", "rag migration", "llama rag"],
        "new_model_releases_per_week":        ["model release", "new model", "releases per week"],
        "ai_consulting_market_disruption":    ["consulting disruption", "consulting market", "ai consulting"],
        "container_ml_adoption":              ["container ml", "kubernetes ml", "containerized"],
        "multi_agent_orchestration_adoption": ["multi-agent", "multi agent", "agent orchestration"],
    }
    keywords = keyword_map.get(metric_key, [metric_key.replace("_", " ")])

    for domain_data in intel_data.values():
        texts = [domain_data.get("summary", "")] + domain_data.get("key_facts", [])
        for text in texts:
            text_lower = str(text).lower()
            for kw in keywords:
                if kw in text_lower:
                    # 퍼센트 숫자 추출
                    nums = re.findall(r"(\d+(?:\.\d+)?)", text)
                    if nums:
                        val = float(nums[0])
                        # 합리적 범위 필터 (0-100 또는 0-10)
                        if 0 <= val <= 100:
                            return val

    return None


# ─────────────────────────────────────────
# EW 탐지 로직
# ─────────────────────────────────────────
def detect_ew_signals(
    intel_data: dict[str, dict],
    thresholds: dict,
    week: str,
) -> dict:
    """임계값 기반 EW 시그널 탐지"""
    triggered_signals = []
    evaluated_metrics = []
    max_severity = "NONE"

    for metric_key, config in thresholds.items():
        threshold  = config["threshold"]
        direction  = config["direction"]
        signal_id  = config["signal"]
        severity   = config.get("severity", "MEDIUM")
        domain     = config.get("domain", "unknown")

        # 도메인별 인텔에서 메트릭 값 추출
        actual_value = extract_metric_value(intel_data, metric_key)

        triggered = False
        reason = "metric_not_found"

        if actual_value is not None:
            if direction == "below" and actual_value < threshold:
                triggered = True
                reason = f"{actual_value:.1f} < {threshold} (threshold)"
            elif direction == "above" and actual_value > threshold:
                triggered = True
                reason = f"{actual_value:.1f} > {threshold} (threshold)"
            else:
                reason = f"{actual_value:.1f} {'≥' if direction == 'below' else '≤'} {threshold} — within range"
        else:
            # 메트릭 미발견 시: key_facts 내 관련 신호 키워드 패턴으로 휴리스틱 판단
            triggered, reason = _heuristic_ew_check(intel_data, metric_key, signal_id)

        metric_eval = {
            "metric_key":   metric_key,
            "actual_value": actual_value,
            "threshold":    threshold,
            "direction":    direction,
            "triggered":    triggered,
            "reason":       reason,
            "signal_id":    signal_id,
            "severity":     severity,
            "domain":       domain,
        }
        evaluated_metrics.append(metric_eval)

        if triggered:
            triggered_signals.append({
                "id":       signal_id,
                "severity": severity,
                "metric":   metric_key,
                "value":    actual_value,
                "threshold":threshold,
                "reason":   reason,
                "domain":   domain,
            })
            # 최대 심각도 갱신
            if SEVERITY_RANK.get(severity, 0) > SEVERITY_RANK.get(max_severity, 0):
                max_severity = severity

    ew_triggered = len(triggered_signals) > 0

    print(f"[INFO] EW Evaluation: {len(triggered_signals)}/{len(thresholds)} signals triggered | Max severity: {max_severity}", file=sys.stderr)

    return {
        "week": week,
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "triggered": ew_triggered,
        "count": len(triggered_signals),
        "max_severity": max_severity if ew_triggered else "NONE",
        "signals": triggered_signals,
        "evaluated_metrics": evaluated_metrics,
        "intel_domains_evaluated": list(intel_data.keys()),
    }


def _heuristic_ew_check(intel_data: dict, metric_key: str, signal_id: str) -> tuple[bool, str]:
    """
    메트릭 값 미발견 시 신호 키워드 휴리스틱 판단
    경고성 키워드 등장 빈도로 EW 발동 여부 추정
    """
    warning_keywords = {
        "EW-AI-DEPLOY":   ["slow adoption", "low deployment", "barrier", "resistance", "under 40%"],
        "EW-RAG-OSS":     ["migration to open source", "llama rag", "pgvector", "away from openai"],
        "EW-MODEL-FLOOD": ["too many models", "model proliferation", "benchmark inflation", "8 models"],
        "EW-CONSULT":     ["consulting disrupted", "ai replaces consultant", "displaced"],
        "EW-INFRA":       ["infrastructure gap", "not containerized", "legacy infra"],
        "EW-ORCH":        ["multi-agent surge", "agent orchestration spike", "agentic boom"],
    }

    kws = warning_keywords.get(signal_id, [])
    hit_count = 0
    all_texts = []
    for domain_data in intel_data.values():
        all_texts.append(domain_data.get("summary", "").lower())
        all_texts.extend(str(f).lower() for f in domain_data.get("key_facts", []))

    for text in all_texts:
        for kw in kws:
            if kw in text:
                hit_count += 1

    if hit_count >= 2:
        return True, f"heuristic: {hit_count} warning keyword hits (metric value not found)"
    return False, f"heuristic: {hit_count} keyword hits — below threshold"


# ─────────────────────────────────────────
# CLI
# ─────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="AI EW Signal Detector for C-31 Registry")
    p.add_argument("--input-dir",   required=True, help="Directory containing intel_*.json files")
    p.add_argument("--thresholds",  default="{}",  help="JSON string of EW thresholds (overrides defaults)")
    p.add_argument("--week",        required=True, help="ISO week label")
    p.add_argument("--output",      required=True, help="Output JSON file path")
    return p.parse_args()


def main():
    args = parse_args()

    # 임계값 파싱 (워크플로에서 전달된 JSON)
    try:
        custom_thresholds = json.loads(args.thresholds) if args.thresholds.strip() != "{}" else {}
    except json.JSONDecodeError:
        print("[WARN] Could not parse --thresholds JSON. Using defaults.", file=sys.stderr)
        custom_thresholds = {}

    # 기본 임계값 + 커스텀 병합
    thresholds = {**DEFAULT_THRESHOLDS, **custom_thresholds}

    # 인텔 데이터 로드
    intel_data = load_intel_files(args.input_dir)
    if not intel_data:
        print("[WARN] No intel files found. Generating empty EW report.", file=sys.stderr)
        intel_data = {}

    # EW 탐지
    ew_report = detect_ew_signals(intel_data, thresholds, args.week)

    # 저장
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(ew_report, f, ensure_ascii=False, indent=2)

    print(f"[OK] EW report saved → {output_path}", file=sys.stderr)
    if ew_report["triggered"]:
        print(f"[ALERT] 🔴 EW TRIGGERED: {[s['id'] for s in ew_report['signals']]} | Severity: {ew_report['max_severity']}", file=sys.stderr)
    else:
        print(f"[OK] 🟢 No EW signals triggered this week.", file=sys.stderr)


if __name__ == "__main__":
    main()
