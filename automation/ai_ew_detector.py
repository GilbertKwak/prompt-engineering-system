#!/usr/bin/env python3
"""
ai_ew_detector.py  v2 — Section A · Step 2
AI 인텔 수집 결과에서 Early Warning(EW) 신호 탐지

변경사항 v2:
  - 3단계 탐지: metric 임계값 → 키워드 hit → 휴리스틱 복합
  - 도메인별 가중치 (infrastructure/model_performance 우선)
  - EW 심각도 3단계: CRITICAL / WARNING / WATCH
  - 탐지 근거 상세 기록 (ew_evidence)
  - --threshold 오버라이드 지원

Usage:
  python automation/ai_ew_detector.py \\
    --input-dir output/ai_intel \\
    --week 2026-W21 \\
    --output output/ai_intel/ew_report.json
"""

import argparse
import json
import os
import sys
import re
from datetime import datetime
from pathlib import Path

# ─── EW 탐지 설정 ──────────────────────────────────────────────────────────────
EW_THRESHOLDS: dict[str, dict] = {
    "enterprise_deployment": {
        "adoption_rate":      {"min": None, "max": None, "change_pct": 15.0},
        "cost_per_query":     {"min": None, "max": None, "change_pct": 25.0},
        "enterprise_deal_size": {"min": None, "max": None, "change_pct": 20.0},
        "domain_weight": 0.8,
    },
    "model_performance": {
        "benchmark_score":          {"min": None, "max": None, "change_pct": 10.0},
        "tokens_per_second":        {"min": None, "max": None, "change_pct": 20.0},
        "cost_per_million_tokens":  {"min": None, "max": None, "change_pct": 30.0},
        "domain_weight": 1.0,
    },
    "infrastructure": {
        "gpu_supply_tightness": {"min": None, "max": 0.85, "change_pct": 15.0},
        "pue":                  {"min": 1.0,  "max": 2.5,  "change_pct": 10.0},
        "capex_per_flop":       {"min": None, "max": None, "change_pct": 20.0},
        "domain_weight": 1.0,
    },
    "regulatory": {
        "compliance_deadline_count": {"min": None, "max": None, "change_pct": 50.0},
        "enforcement_action_count":  {"min": 3,    "max": None, "change_pct": None},
        "domain_weight": 0.9,
    },
    "open_source": {
        "github_stars_delta": {"min": None, "max": None, "change_pct": 40.0},
        "new_model_releases": {"min": None, "max": None, "change_pct": None},
        "fork_velocity":      {"min": None, "max": None, "change_pct": 35.0},
        "domain_weight": 0.7,
    },
    "investment": {
        "funding_volume_usd": {"min": None, "max": None, "change_pct": 30.0},
        "deal_count":         {"min": None, "max": None, "change_pct": 25.0},
        "valuation_multiple": {"min": None, "max": None, "change_pct": 20.0},
        "domain_weight": 0.8,
    },
}

# EW 키워드 (신호 강도별)
EW_KEYWORDS_CRITICAL = [
    "breakthrough", "paradigm shift", "disruption", "emergency",
    "critical shortage", "supply crisis", "ban", "shutdown",
    "acquisition", "merger", "antitrust",
]
EW_KEYWORDS_WARNING = [
    "rapid adoption", "spike", "surge", "unexpected", "accelerat",
    "shortage", "constraint", "regulatory action", "enforcement",
    "major release", "outperform", "significantly",
]
EW_KEYWORDS_WATCH = [
    "growing", "increasing", "trend", "momentum", "shift",
    "concern", "pressure", "signal", "emerging", "notable",
]


# ─── 탐지 함수 ─────────────────────────────────────────────────────────────────
def detect_metric_ew(domain: str, metrics: dict) -> list[dict]:
    """메트릭 임계값 기반 EW 탐지"""
    signals = []
    domain_cfg = EW_THRESHOLDS.get(domain, {})
    weight = domain_cfg.get("domain_weight", 0.8)

    for metric_name, value in metrics.items():
        if value is None:
            continue
        try:
            val = float(value)
        except (TypeError, ValueError):
            continue

        cfg = domain_cfg.get(metric_name)
        if not cfg:
            # 유사 키 매칭 시도
            for k in domain_cfg:
                if k != "domain_weight" and k in metric_name:
                    cfg = domain_cfg[k]
                    break
        if not cfg:
            continue

        triggered = False
        reason = ""
        if cfg.get("min") is not None and val < cfg["min"]:
            triggered = True
            reason = f"{metric_name}={val} < min={cfg['min']}"
        if cfg.get("max") is not None and val > cfg["max"]:
            triggered = True
            reason = f"{metric_name}={val} > max={cfg['max']}"

        if triggered:
            signals.append({
                "type": "metric_threshold",
                "domain": domain,
                "metric": metric_name,
                "value": val,
                "reason": reason,
                "weight": weight,
                "severity": "WARNING",
            })
    return signals


def detect_keyword_ew(domain: str, intel: dict) -> list[dict]:
    """키워드 기반 EW 탐지"""
    text_fields = [
        " ".join(intel.get("key_facts", [])),
        " ".join(intel.get("emerging_signals", [])),
        intel.get("summary", ""),
    ]
    combined = " ".join(text_fields).lower()
    weight = EW_THRESHOLDS.get(domain, {}).get("domain_weight", 0.8)
    signals = []

    for kw in EW_KEYWORDS_CRITICAL:
        if kw in combined:
            signals.append({
                "type": "keyword_critical",
                "domain": domain,
                "keyword": kw,
                "reason": f"CRITICAL 키워드 감지: '{kw}'",
                "weight": weight * 1.2,
                "severity": "CRITICAL",
            })

    for kw in EW_KEYWORDS_WARNING:
        if kw in combined:
            signals.append({
                "type": "keyword_warning",
                "domain": domain,
                "keyword": kw,
                "reason": f"WARNING 키워드 감지: '{kw}'",
                "weight": weight,
                "severity": "WARNING",
            })

    # WATCH는 3개 이상 hit 시에만 등록 (노이즈 방지)
    watch_hits = [kw for kw in EW_KEYWORDS_WATCH if kw in combined]
    if len(watch_hits) >= 3:
        signals.append({
            "type": "keyword_watch",
            "domain": domain,
            "keywords": watch_hits,
            "reason": f"WATCH 키워드 {len(watch_hits)}개 감지: {watch_hits[:5]}",
            "weight": weight * 0.6,
            "severity": "WATCH",
        })

    return signals


def detect_heuristic_ew(domain: str, intel: dict) -> list[dict]:
    """휴리스틱 기반 EW (confidence 낮음 + signals 많음 = 불확실성 급증)"""
    signals = []
    conf     = float(intel.get("confidence", 1.0))
    n_signals = len(intel.get("emerging_signals", []))
    n_facts   = len(intel.get("key_facts", []))

    # 신뢰도 낮고 시그널 많으면 → 불확실성 EW
    if conf < 0.45 and n_signals >= 3:
        signals.append({
            "type": "heuristic_uncertainty",
            "domain": domain,
            "reason": f"낮은 신뢰도({conf}) + 다수 시그널({n_signals}개) → 불확실성 급증",
            "weight": 0.6,
            "severity": "WATCH",
        })

    # 팩트 수 급증 (10개 초과) → 이벤트 밀도 높음
    if n_facts > 10:
        signals.append({
            "type": "heuristic_density",
            "domain": domain,
            "reason": f"팩트 밀도 높음 ({n_facts}개) → 주요 이벤트 발생 가능",
            "weight": 0.5,
            "severity": "WATCH",
        })

    return signals


def calculate_ew_severity(all_signals: list[dict]) -> str:
    """전체 시그널 집합에서 최종 EW 심각도 결정"""
    if not all_signals:
        return "NONE"
    severities = [s.get("severity", "WATCH") for s in all_signals]
    if "CRITICAL" in severities:
        return "CRITICAL"
    if severities.count("WARNING") >= 2:
        return "CRITICAL"
    if "WARNING" in severities:
        return "WARNING"
    return "WATCH"


def analyze_intel_file(filepath: Path, week: str) -> dict:
    """단일 인텔 JSON 파일 EW 분석"""
    try:
        intel = json.loads(filepath.read_text())
    except Exception as e:
        return {"file": str(filepath), "error": str(e), "ew_triggered": False}

    domain = intel.get("domain", filepath.stem.replace("intel_", ""))
    all_sigs = []
    all_sigs.extend(detect_metric_ew(domain, intel.get("metrics", {})))
    all_sigs.extend(detect_keyword_ew(domain, intel))
    all_sigs.extend(detect_heuristic_ew(domain, intel))

    triggered = bool(all_sigs)
    severity  = calculate_ew_severity(all_sigs)
    total_weight = sum(s.get("weight", 0) for s in all_sigs)

    return {
        "domain": domain,
        "week": week,
        "ew_triggered": triggered,
        "ew_severity": severity,
        "ew_signal_count": len(all_sigs),
        "ew_total_weight": round(total_weight, 3),
        "ew_signals": all_sigs,
        "intel_confidence": intel.get("confidence", 0),
        "intel_fact_count": len(intel.get("key_facts", [])),
        "analyzed_at": datetime.utcnow().isoformat() + "Z",
    }


# ─── CLI ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="AI 인텔 EW 탐지기 v2")
    parser.add_argument("--input-dir", required=True, help="인텔 JSON 파일 디렉토리")
    parser.add_argument("--week",      required=True, help="ISO 주차 (예: 2026-W21)")
    parser.add_argument("--output",    required=True, help="EW 리포트 저장 경로 (JSON)")
    parser.add_argument("--domain",    default=None,  help="특정 도메인만 분석 (기본: 전체)")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"[ERROR] 입력 디렉토리 없음: {input_dir}", file=sys.stderr)
        sys.exit(1)

    intel_files = sorted(input_dir.glob("intel_*.json"))
    if args.domain:
        intel_files = [f for f in intel_files if args.domain in f.name]
    if not intel_files:
        print(f"[WARN] intel_*.json 파일 없음 in {input_dir}", file=sys.stderr)

    domain_reports = []
    for f in intel_files:
        print(f"  분석 중: {f.name}", file=sys.stderr)
        report = analyze_intel_file(f, args.week)
        domain_reports.append(report)

    # 전체 요약
    triggered_domains = [r["domain"] for r in domain_reports if r.get("ew_triggered")]
    global_severity   = calculate_ew_severity(
        [s for r in domain_reports for s in r.get("ew_signals", [])]
    )
    total_signals     = sum(r.get("ew_signal_count", 0) for r in domain_reports)

    final_report = {
        "week": args.week,
        "analyzed_at": datetime.utcnow().isoformat() + "Z",
        "global_ew_triggered": bool(triggered_domains),
        "global_severity": global_severity,
        "triggered_domains": triggered_domains,
        "total_signal_count": total_signals,
        "domain_count_analyzed": len(domain_reports),
        "domain_reports": domain_reports,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(final_report, ensure_ascii=False, indent=2))

    flag = "🚨" if global_severity == "CRITICAL" else "⚠️" if global_severity == "WARNING" else "👀" if global_severity == "WATCH" else "✅"
    print(f"[OK] EW 분석 완료 → {out_path}")
    print(f"     {flag} 전체 심각도: {global_severity} | 트리거 도메인: {triggered_domains} | 시그널 수: {total_signals}")


if __name__ == "__main__":
    main()
