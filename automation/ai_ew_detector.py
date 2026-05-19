#!/usr/bin/env python3
"""
ai_ew_detector.py  — Section A · Step 2
수집된 인텔에서 Early Warning(EW) 신호 탐지

Usage:
  python automation/ai_ew_detector.py \
    --input-dir output/ai_intel \
    --week 2026-W21 \
    --output output/ai_intel/ew_report.json
"""

import argparse
import json
import os
import sys
import re
from datetime import datetime
from pathlib import Path

# ─── EW 탐지 규칙 정의 ─────────────────────────────────────────────────────────
# 각 도메인별 임계값 규칙 + 키워드 기반 휴리스틱
EW_RULES = {
    "enterprise_deployment": [
        {"metric": "adoption_rate", "threshold": 0.30, "direction": "below",
         "signal": "EW_ENTERPRISE_STALL", "severity": "MEDIUM",
         "description": "기업 AI 도입률 30% 미만 — 성장 둔화 신호"},
        {"metric": "enterprise_deal_size", "threshold": 1_000_000, "direction": "below",
         "signal": "EW_DEAL_SIZE_DROP", "severity": "LOW",
         "description": "평균 계약 규모 $1M 미만 — 예산 압박 가능성"},
    ],
    "model_performance": [
        {"metric": "cost_per_million_tokens", "threshold": 50, "direction": "above",
         "signal": "EW_MODEL_COST_SPIKE", "severity": "HIGH",
         "description": "토큰당 비용 급등 — 경쟁 모델 전환 압력"},
        {"metric": "benchmark_score", "threshold": 0.80, "direction": "below",
         "signal": "EW_BENCHMARK_REGRESSION", "severity": "MEDIUM",
         "description": "벤치마크 점수 하락 — 모델 품질 이슈"},
    ],
    "infrastructure": [
        {"metric": "gpu_supply_tightness", "threshold": 0.80, "direction": "above",
         "signal": "EW_GPU_SHORTAGE", "severity": "HIGH",
         "description": "GPU 공급 긴축 80% 초과 — 인프라 병목 위험"},
        {"metric": "pue", "threshold": 1.6, "direction": "above",
         "signal": "EW_DATACENTER_INEFFICIENCY", "severity": "LOW",
         "description": "PUE 1.6 초과 — 에너지 효율 저하"},
    ],
    "regulatory": [
        {"metric": "enforcement_action_count", "threshold": 3, "direction": "above",
         "signal": "EW_REGULATORY_SURGE", "severity": "HIGH",
         "description": "주간 규제 조치 3건 초과 — 컴플라이언스 긴급 대응 필요"},
        {"metric": "compliance_deadline_count", "threshold": 2, "direction": "above",
         "signal": "EW_COMPLIANCE_DEADLINE", "severity": "MEDIUM",
         "description": "임박 컴플라이언스 데드라인 2건 초과"},
    ],
    "open_source": [
        {"metric": "new_model_releases", "threshold": 5, "direction": "above",
         "signal": "EW_OSS_EXPLOSION", "severity": "MEDIUM",
         "description": "주간 오픈소스 모델 5개 초과 릴리스 — 파편화 위험"},
    ],
    "investment": [
        {"metric": "funding_volume_usd", "threshold": 5_000_000_000, "direction": "above",
         "signal": "EW_INVESTMENT_SPIKE", "severity": "HIGH",
         "description": "주간 AI 투자 $5B 초과 — 버블 징후 또는 구조적 전환"},
        {"metric": "deal_count", "threshold": 1, "direction": "below",
         "signal": "EW_INVESTMENT_DROUGHT", "severity": "MEDIUM",
         "description": "주간 딜 1건 미만 — 투자 위축"},
    ],
}

# 키워드 기반 EW 휴리스틱 (메트릭 데이터 없을 때 보완)
EW_KEYWORDS = {
    "EW_SECURITY_BREACH": {
        "keywords": ["breach", "vulnerability", "exploit", "attack", "hack", "zero-day"],
        "severity": "HIGH", "min_hits": 2,
        "description": "보안 위협 키워드 다수 탐지",
    },
    "EW_LEADERSHIP_CHANGE": {
        "keywords": ["CEO", "CTO", "resign", "fired", "replaced", "departure", "leadership"],
        "severity": "MEDIUM", "min_hits": 2,
        "description": "주요 리더십 변동 신호",
    },
    "EW_RAG_MIGRATION": {
        "keywords": ["RAG", "retrieval-augmented", "vector database", "migration", "pipeline shift"],
        "severity": "MEDIUM", "min_hits": 2,
        "description": "RAG 아키텍처 대규모 전환 신호",
    },
    "EW_GEOPOLITICAL": {
        "keywords": ["sanction", "export control", "ban", "geopolitical", "China", "Taiwan", "trade war"],
        "severity": "HIGH", "min_hits": 2,
        "description": "지정학적 리스크 신호",
    },
}


# ─── 유틸리티 ─────────────────────────────────────────────────────────────────
def safe_float(value) -> float | None:
    """안전한 숫자 변환 (문자열 포함)"""
    if value is None:
        return None
    try:
        # 퍼센트 문자열 처리 (예: "45%" → 0.45)
        if isinstance(value, str):
            value = value.replace("%", "").replace(",", "").strip()
            v = float(value)
            # 0-1 범위를 벗어난 퍼센트를 비율로 변환 (50 → 0.5)
            # 단, 1보다 큰 값은 그대로 유지 (예: 5000000000)
            return v
        return float(value)
    except (ValueError, TypeError):
        return None


def extract_metric_flexible(metrics_dict: dict, target_key: str) -> float | None:
    """유사 키 매칭으로 메트릭 값 추출 (예: 'cost_per_million_tokens' ↔ 'cost_per_token')"""
    if not metrics_dict:
        return None
    # 1순위: 정확한 키
    if target_key in metrics_dict:
        return safe_float(metrics_dict[target_key])
    # 2순위: 부분 문자열 매칭
    for k, v in metrics_dict.items():
        if target_key in k or k in target_key:
            return safe_float(v)
    # 3순위: 키워드 토큰 매칭
    target_tokens = set(target_key.split("_"))
    for k, v in metrics_dict.items():
        k_tokens = set(k.split("_"))
        if len(target_tokens & k_tokens) >= 2:
            return safe_float(v)
    return None


def check_metric_rule(rule: dict, metrics: dict) -> dict | None:
    """단일 메트릭 규칙 평가 → 위반 시 EW 결과 반환"""
    value = extract_metric_flexible(metrics, rule["metric"])
    if value is None:
        return None  # 데이터 없으면 스킵 (휴리스틱으로 보완)

    triggered = False
    if rule["direction"] == "above" and value > rule["threshold"]:
        triggered = True
    elif rule["direction"] == "below" and value < rule["threshold"]:
        triggered = True

    if triggered:
        return {
            "signal": rule["signal"],
            "severity": rule["severity"],
            "description": rule["description"],
            "metric": rule["metric"],
            "observed_value": value,
            "threshold": rule["threshold"],
            "direction": rule["direction"],
            "source": "metric_rule",
        }
    return None


def check_keyword_heuristics(intel: dict) -> list[dict]:
    """key_facts + emerging_signals 텍스트에서 키워드 EW 탐지"""
    text_corpus = " ".join(
        intel.get("key_facts", []) +
        intel.get("emerging_signals", []) +
        [intel.get("summary", "")]
    ).lower()

    triggered = []
    for signal_name, rule in EW_KEYWORDS.items():
        hits = sum(1 for kw in rule["keywords"] if kw.lower() in text_corpus)
        if hits >= rule["min_hits"]:
            triggered.append({
                "signal": signal_name,
                "severity": rule["severity"],
                "description": rule["description"],
                "keyword_hits": hits,
                "source": "keyword_heuristic",
            })
    return triggered


def analyze_domain(intel_path: Path) -> dict:
    """단일 인텔 파일 EW 분석"""
    try:
        intel = json.loads(intel_path.read_text())
    except Exception as e:
        return {"file": str(intel_path), "error": str(e), "signals": []}

    domain = intel.get("domain", "unknown")
    metrics = intel.get("metrics", {})
    ew_signals = []

    # 메트릭 규칙 검사
    for rule in EW_RULES.get(domain, []):
        result = check_metric_rule(rule, metrics)
        if result:
            ew_signals.append(result)

    # 키워드 휴리스틱 (메트릭 신호가 없을 때 보완)
    if not ew_signals:
        ew_signals.extend(check_keyword_heuristics(intel))

    return {
        "domain": domain,
        "week": intel.get("week"),
        "analyzed_at": datetime.utcnow().isoformat() + "Z",
        "ew_triggered": len(ew_signals) > 0,
        "signal_count": len(ew_signals),
        "signals": ew_signals,
        "max_severity": _max_severity(ew_signals),
        "intel_confidence": intel.get("confidence", 0.0),
        "source_file": str(intel_path),
    }


def _max_severity(signals: list[dict]) -> str:
    priority = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "NONE": 0}
    if not signals:
        return "NONE"
    return max(signals, key=lambda s: priority.get(s.get("severity", "NONE"), 0))["severity"]


# ─── CLI 진입점 ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="AI 인텔 Early Warning 탐지")
    parser.add_argument("--input-dir", required=True, help="ai_intel_collector 출력 디렉토리")
    parser.add_argument("--week", required=True, help="분석 대상 주차 (예: 2026-W21)")
    parser.add_argument("--output", required=True, help="EW 리포트 저장 경로 (JSON)")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"[ERROR] 입력 디렉토리 없음: {input_dir}", file=sys.stderr)
        sys.exit(1)

    intel_files = list(input_dir.glob("intel_*.json"))
    if not intel_files:
        print(f"[WARN] intel_*.json 파일 없음: {input_dir}", file=sys.stderr)

    domain_results = [analyze_domain(f) for f in intel_files]

    total_signals = [s for r in domain_results for s in r.get("signals", [])]
    all_signal_names = [s["signal"] for s in total_signals]
    overall_severity = _max_severity(total_signals)

    report = {
        "week": args.week,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_domains_analyzed": len(domain_results),
        "total_ew_signals": len(total_signals),
        "overall_severity": overall_severity,
        "ew_triggered": len(total_signals) > 0,
        "signal_names": all_signal_names,
        "domain_results": domain_results,
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2))

    print(f"[OK] EW 분석 완료 → {output_path}")
    print(f"     총 신호: {len(total_signals)} | 최고 심각도: {overall_severity}")
    if all_signal_names:
        print(f"     신호 목록: {', '.join(all_signal_names)}")


if __name__ == "__main__":
    main()
