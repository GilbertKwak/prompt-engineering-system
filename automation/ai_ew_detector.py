#!/usr/bin/env python3
"""
ai_ew_detector.py — AI Intel Early Warning Detector

Perplexity API 수집 결과에서 Early Warning 시그널을 탐지합니다.
- 메트릭 기반 임계값 체크 (adoption_rate, cost_reduction, market_share)
- 키워드 히트 기반 휴리스틱 보완
- 심각도 분류: NONE / WATCH / EW
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# ──────────────────────────────────────────
# EW 판단 기준
# ──────────────────────────────────────────
EW_THRESHOLDS = {
    "adoption_rate": {"operator": ">=", "value": 40, "unit": "%"},
    "cost_reduction": {"operator": ">=", "value": 30, "unit": "%"},
    "market_share": {"operator": ">=", "value": 20, "unit": "%"},
    "growth_rate": {"operator": ">=", "value": 50, "unit": "%"},
    "latency_reduction": {"operator": ">=", "value": 40, "unit": "%"},
}

WATCH_THRESHOLDS = {
    "adoption_rate": {"operator": ">=", "value": 25, "unit": "%"},
    "cost_reduction": {"operator": ">=", "value": 15, "unit": "%"},
    "market_share": {"operator": ">=", "value": 10, "unit": "%"},
    "growth_rate": {"operator": ">=", "value": 30, "unit": "%"},
    "latency_reduction": {"operator": ">=", "value": 20, "unit": "%"},
}

EW_KEYWORDS = [
    "breakthrough", "disruption", "paradigm shift", "game changer",
    "dominates", "captures market", "replaces", "obsoletes",
    "rapid adoption", "explosive growth", "market leader",
    "unprecedented", "transformative", "revolutionary",
]

WATCH_KEYWORDS = [
    "significant", "notable", "emerging", "growing adoption",
    "accelerating", "gaining traction", "expanding rapidly",
    "strong momentum", "competitive threat",
]


def extract_number(text: str, pattern_hint: str = "") -> float | None:
    """텍스트에서 숫자 추출. 퍼센트 포함 여부 확인."""
    patterns = [
        r"(\d+(?:\.\d+)?)\s*%",   # 퍼센트
        r"(\d+(?:\.\d+)?)x",       # 배수
        r"(\d+(?:\.\d+)?)",         # 일반 숫자
    ]
    for pat in patterns:
        m = re.search(pat, str(text))
        if m:
            return float(m.group(1))
    return None


def check_threshold(value: float, threshold: dict) -> bool:
    """임계값 초과 여부 확인."""
    op = threshold["operator"]
    t_val = threshold["value"]
    if op == ">=":
        return value >= t_val
    elif op == ">":
        return value > t_val
    elif op == "<=":
        return value <= t_val
    elif op == "<":
        return value < t_val
    return False


def find_metric_value(intel_data: dict, metric_key: str) -> float | None:
    """인텔 데이터에서 특정 메트릭 값 추출. 3단계 폴백."""
    # 1단계: metrics 딕셔너리 직접 접근
    if "metrics" in intel_data and isinstance(intel_data["metrics"], dict):
        metrics = intel_data["metrics"]
        if metric_key in metrics:
            return extract_number(str(metrics[metric_key]))
        # 유사 키 매칭 (부분 문자열)
        for k, v in metrics.items():
            if metric_key.replace("_", " ") in k.lower() or k.lower() in metric_key:
                val = extract_number(str(v))
                if val is not None:
                    return val

    # 2단계: key_facts / summary 텍스트에서 숫자 파싱
    text_fields = []
    for field in ["key_facts", "summary", "analysis", "content", "raw_text"]:
        if field in intel_data:
            val = intel_data[field]
            if isinstance(val, list):
                text_fields.extend([str(v) for v in val])
            elif isinstance(val, str):
                text_fields.append(val)

    search_text = " ".join(text_fields).lower()
    metric_label = metric_key.replace("_", " ")
    pattern = rf"{metric_label}[^\d]{{0,30}}(\d+(?:\.\d+)?)\s*%?"
    m = re.search(pattern, search_text)
    if m:
        return float(m.group(1))

    return None


def count_keyword_hits(intel_data: dict, keywords: list) -> tuple[int, list]:
    """키워드 히트 카운트 반환."""
    text_parts = []
    for field in ["key_facts", "summary", "analysis", "content", "raw_text",
                  "title", "headline", "description"]:
        val = intel_data.get(field, "")
        if isinstance(val, list):
            text_parts.extend([str(v) for v in val])
        elif isinstance(val, str):
            text_parts.append(val)

    combined = " ".join(text_parts).lower()
    hits = [kw for kw in keywords if kw.lower() in combined]
    return len(hits), hits


def evaluate_intel_file(filepath: Path) -> dict:
    """단일 인텔 파일에 대한 EW 평가 수행."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        return {"file": str(filepath), "error": str(e), "severity": "NONE", "signals": []}

    # 단일 객체 vs 배열 처리
    items = data if isinstance(data, list) else [data]

    ew_signals = []
    watch_signals = []
    metric_results = {}

    for item in items:
        domain = item.get("domain", item.get("topic", filepath.stem))

        # ① 메트릭 기반 체크
        for metric, threshold in EW_THRESHOLDS.items():
            val = find_metric_value(item, metric)
            if val is not None:
                metric_results[f"{domain}.{metric}"] = val
                if check_threshold(val, threshold):
                    ew_signals.append({
                        "type": "metric_ew",
                        "domain": domain,
                        "metric": metric,
                        "value": val,
                        "threshold": threshold["value"],
                    })
                elif check_threshold(val, WATCH_THRESHOLDS.get(metric, {"operator": ">=", "value": 9999})):
                    watch_signals.append({
                        "type": "metric_watch",
                        "domain": domain,
                        "metric": metric,
                        "value": val,
                    })

        # ② 키워드 히트 보완
        ew_hits, ew_matched = count_keyword_hits(item, EW_KEYWORDS)
        watch_hits, watch_matched = count_keyword_hits(item, WATCH_KEYWORDS)

        if ew_hits >= 2:
            ew_signals.append({
                "type": "keyword_ew",
                "domain": domain,
                "hit_count": ew_hits,
                "keywords": ew_matched[:5],
            })
        elif ew_hits == 1 or watch_hits >= 2:
            watch_signals.append({
                "type": "keyword_watch",
                "domain": domain,
                "ew_hits": ew_hits,
                "watch_hits": watch_hits,
                "keywords": (ew_matched + watch_matched)[:5],
            })

    # 심각도 결정
    if ew_signals:
        severity = "EW"
    elif watch_signals:
        severity = "WATCH"
    else:
        severity = "NONE"

    return {
        "file": str(filepath.name),
        "severity": severity,
        "ew_signal_count": len(ew_signals),
        "watch_signal_count": len(watch_signals),
        "ew_signals": ew_signals,
        "watch_signals": watch_signals,
        "metric_values": metric_results,
    }


def run_detection(input_dir: str, week: str, output_path: str) -> dict:
    """디렉토리 내 모든 인텔 JSON 파일에 대해 EW 탐지 실행."""
    base_dir = Path(input_dir)
    if not base_dir.exists():
        print(f"[WARN] input-dir not found: {input_dir}, creating empty report", file=sys.stderr)
        base_dir.mkdir(parents=True, exist_ok=True)

    json_files = sorted(base_dir.glob("*.json"))
    if not json_files:
        print(f"[INFO] No JSON files in {input_dir}", file=sys.stderr)

    results = []
    total_ew = 0
    all_ew_signals = []

    for fp in json_files:
        result = evaluate_intel_file(fp)
        results.append(result)
        if result["severity"] == "EW":
            total_ew += 1
            all_ew_signals.extend(result.get("ew_signals", []))

    # 전체 심각도 집계
    if total_ew >= 2:
        overall_severity = "EW"
    elif total_ew == 1 or any(r["severity"] == "WATCH" for r in results):
        overall_severity = "WATCH"
    else:
        overall_severity = "NONE"

    report = {
        "week": week,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "overall_severity": overall_severity,
        "total_files_checked": len(results),
        "ew_triggered_count": total_ew,
        "ew_triggered": total_ew > 0,
        "ew_signals_summary": all_ew_signals[:10],
        "file_results": results,
    }

    # 출력 저장
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"[EW] Severity={overall_severity} | EW files={total_ew}/{len(results)} | Output={output_path}")
    return report


def main():
    parser = argparse.ArgumentParser(description="AI Intel Early Warning Detector")
    parser.add_argument("--input-dir", default="output/ai_intel",
                        help="수집된 인텔 JSON 파일 디렉토리")
    parser.add_argument("--week", required=True, help="ISO 주차 (예: 2026-W21)")
    parser.add_argument("--output", default="output/ai_intel/ew_report.json",
                        help="EW 리포트 출력 경로")
    args = parser.parse_args()

    report = run_detection(args.input_dir, args.week, args.output)

    # GitHub Actions 출력 호환
    print(f"ew_triggered={str(report['ew_triggered']).lower()}")
    print(f"ew_count={report['ew_triggered_count']}")
    print(f"ew_severity={report['overall_severity']}")
    ew_signal_str = ",".join(
        s.get("domain", "") for s in report.get("ew_signals_summary", [])[:5]
    )
    print(f"ew_signals={ew_signal_str}")

    sys.exit(0 if not report["ew_triggered"] else 1)


if __name__ == "__main__":
    main()
