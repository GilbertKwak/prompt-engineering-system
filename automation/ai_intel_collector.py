#!/usr/bin/env python3
"""
ai_intel_collector.py  — Section A · Step 1
Perplexity sonar/sonar-pro API를 통해 AI 도메인별 주간 인텔 수집

Usage:
  python automation/ai_intel_collector.py \
    --domain enterprise_deployment \
    --week 2026-W21 \
    --scope standard \
    --queries "enterprise AI deployment 2026" "LLM cost trends" \
    --output output/ai_intel/intel_enterprise.json
"""

import argparse
import json
import os
import sys
import time
import re
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("[ERROR] requests 패키지 없음: pip install requests", file=sys.stderr)
    sys.exit(1)

# ─── 상수 ────────────────────────────────────────────────────────────────────
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
MODEL_STANDARD = "sonar"
MODEL_DEEP = "sonar-pro"
MAX_RETRIES = 3
RETRY_BASE_DELAY = 2  # seconds

DOMAIN_META = {
    "enterprise_deployment": {
        "label": "Enterprise AI Deployment",
        "description": "기업 AI 도입 현황, ROI 사례, 거버넌스",
        "ew_metrics": ["adoption_rate", "cost_per_query", "enterprise_deal_size"],
    },
    "model_performance": {
        "label": "Model Performance Benchmarks",
        "description": "LLM/MLLM 벤치마크, 추론 속도, 비용 효율",
        "ew_metrics": ["benchmark_score", "tokens_per_second", "cost_per_million_tokens"],
    },
    "infrastructure": {
        "label": "AI Infrastructure & Chips",
        "description": "GPU/NPU 공급, 데이터센터, 전력 효율",
        "ew_metrics": ["gpu_supply_tightness", "pue", "capex_per_flop"],
    },
    "regulatory": {
        "label": "AI Regulation & Policy",
        "description": "글로벌 AI 규제, 컴플라이언스, 정책 변화",
        "ew_metrics": ["compliance_deadline_count", "enforcement_action_count"],
    },
    "open_source": {
        "label": "Open Source AI Ecosystem",
        "description": "오픈소스 모델, 프레임워크, 커뮤니티 동향",
        "ew_metrics": ["github_stars_delta", "new_model_releases", "fork_velocity"],
    },
    "investment": {
        "label": "AI Investment & M&A",
        "description": "VC 투자, M&A, AI 스타트업 동향",
        "ew_metrics": ["funding_volume_usd", "deal_count", "valuation_multiple"],
    },
}


# ─── 유틸리티 ─────────────────────────────────────────────────────────────────
def get_api_key() -> str:
    """환경변수에서 Perplexity API 키 조회"""
    key = os.environ.get("PERPLEXITY_API_KEY", "").strip()
    if not key:
        print("[ERROR] PERPLEXITY_API_KEY 환경변수 미설정", file=sys.stderr)
        sys.exit(1)
    return key


def select_model(scope: str) -> str:
    """scope에 따라 모델 선택"""
    return MODEL_DEEP if scope in ("deep", "emergency") else MODEL_STANDARD


def build_system_prompt(domain: str, week: str) -> str:
    meta = DOMAIN_META.get(domain, {"label": domain, "description": "", "ew_metrics": []})
    return (
        f"You are an expert AI industry analyst. "
        f"Your task is to provide a structured weekly intelligence report for the domain: "
        f"{meta['label']} ({meta['description']}) for the week {week}.\n\n"
        f"Always respond in STRICT JSON format with this schema:\n"
        f"{{\n"
        f'  "domain": "{domain}",\n'
        f'  "week": "{week}",\n'
        f'  "collected_at": "ISO8601_datetime",\n'
        f'  "key_facts": ["<concise factual statement>", ...],\n'
        f'  "emerging_signals": ["<weak signal or trend>", ...],\n'
        f'  "metrics": {{"<metric_name>": <numeric_value_or_null>, ...}},\n'
        f'  "sources": ["<url_or_reference>", ...],\n'
        f'  "confidence": 0.0_to_1.0,\n'
        f'  "summary": "<2-3 sentence executive summary>"\n'
        f"}}\n\n"
        f"Target metrics to extract if available: {', '.join(meta['ew_metrics'])}\n"
        f"Be concise, factual, and cite sources where possible."
    )


def parse_json_from_response(text: str) -> dict:
    """LLM 응답에서 JSON 블록 추출 (마크다운 코드블록 포함)"""
    # 1순위: ```json ... ``` 블록
    match = re.search(r"```(?:json)?\s*\n?({.*?})\s*\n?```", text, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    # 2순위: 첫 번째 { ... } 블록
    match = re.search(r"({[\s\S]*})", text)
    if match:
        return json.loads(match.group(1))
    raise ValueError(f"JSON 파싱 실패. 응답 앞부분: {text[:300]}")


# ─── API 호출 ─────────────────────────────────────────────────────────────────
def call_perplexity(
    api_key: str,
    model: str,
    system_prompt: str,
    user_query: str,
    attempt: int = 0,
) -> dict:
    """Perplexity API 호출 (지수 백오프 재시도)"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query},
        ],
        "temperature": 0.2,
        "max_tokens": 2048,
    }

    try:
        resp = requests.post(
            PERPLEXITY_API_URL,
            headers=headers,
            json=payload,
            timeout=60,
        )
        if resp.status_code == 429 and attempt < MAX_RETRIES:
            delay = RETRY_BASE_DELAY * (2 ** attempt)
            print(f"[WARN] Rate limit hit. {delay}s 후 재시도 (attempt {attempt+1}/{MAX_RETRIES})",
                  file=sys.stderr)
            time.sleep(delay)
            return call_perplexity(api_key, model, system_prompt, user_query, attempt + 1)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.Timeout:
        if attempt < MAX_RETRIES:
            delay = RETRY_BASE_DELAY * (2 ** attempt)
            print(f"[WARN] Timeout. {delay}s 후 재시도", file=sys.stderr)
            time.sleep(delay)
            return call_perplexity(api_key, model, system_prompt, user_query, attempt + 1)
        raise


# ─── 수집 핵심 로직 ────────────────────────────────────────────────────────────
def collect_intel(
    domain: str,
    week: str,
    scope: str,
    queries: list[str],
    api_key: str,
) -> dict:
    """단일 도메인 인텔 수집 → 통합 결과 dict 반환"""
    model = select_model(scope)
    system_prompt = build_system_prompt(domain, week)
    results = []
    errors = []

    for i, query in enumerate(queries):
        if not query.strip():
            continue  # 빈 쿼리 스킵
        print(f"[{i+1}/{len(queries)}] 쿼리: {query[:80]}...", file=sys.stderr)
        try:
            raw = call_perplexity(api_key, model, system_prompt, query)
            content = raw["choices"][0]["message"]["content"]
            parsed = parse_json_from_response(content)
            parsed["_query"] = query
            parsed["_model"] = model
            parsed["collected_at"] = datetime.utcnow().isoformat() + "Z"
            results.append(parsed)
            print(f"  ✓ 수집 완료 (신뢰도: {parsed.get('confidence', 'N/A')})", file=sys.stderr)
        except Exception as e:
            print(f"  ✗ 오류: {e}", file=sys.stderr)
            errors.append({"query": query, "error": str(e)})
        time.sleep(0.5)  # 쿼리 간 최소 딜레이

    # 여러 결과 병합
    if not results:
        print(f"[ERROR] 도메인 {domain}에서 수집된 결과 없음", file=sys.stderr)
        sys.exit(1)

    merged = merge_results(domain, week, results)
    merged["_collection_errors"] = errors
    merged["_scope"] = scope
    return merged


def merge_results(domain: str, week: str, results: list[dict]) -> dict:
    """복수 쿼리 결과를 단일 도메인 인텔로 병합"""
    all_facts = []
    all_signals = []
    all_sources = []
    merged_metrics = {}
    confidence_sum = 0.0
    summaries = []

    for r in results:
        all_facts.extend(r.get("key_facts", []))
        all_signals.extend(r.get("emerging_signals", []))
        all_sources.extend(r.get("sources", []))
        for k, v in r.get("metrics", {}).items():
            if v is not None:
                merged_metrics[k] = v
        confidence_sum += float(r.get("confidence", 0.7))
        if r.get("summary"):
            summaries.append(r["summary"])

    return {
        "domain": domain,
        "week": week,
        "collected_at": datetime.utcnow().isoformat() + "Z",
        "key_facts": list(dict.fromkeys(all_facts)),  # 중복 제거
        "emerging_signals": list(dict.fromkeys(all_signals)),
        "metrics": merged_metrics,
        "sources": list(set(all_sources)),
        "confidence": round(confidence_sum / len(results), 3),
        "summary": " | ".join(summaries[:3]),  # 최대 3개 요약 병합
        "_query_count": len(results),
    }


# ─── CLI 진입점 ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Perplexity API로 AI 도메인 인텔 수집",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--domain",
        required=True,
        choices=list(DOMAIN_META.keys()),
        help="수집 대상 도메인",
    )
    parser.add_argument(
        "--week",
        required=True,
        help="ISO 주차 (예: 2026-W21)",
    )
    parser.add_argument(
        "--scope",
        default="standard",
        choices=["standard", "deep", "emergency"],
        help="수집 깊이 (standard=sonar, deep/emergency=sonar-pro)",
    )
    parser.add_argument(
        "--queries",
        nargs="+",  # FIX: '*'에서 '+'로 변경 — 최소 1개 필수
        required=True,
        help="Perplexity에 전달할 검색 쿼리 1개 이상",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="결과 저장 경로 (JSON)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="API 실제 호출 없이 구조만 검증",
    )

    args = parser.parse_args()

    # 출력 디렉토리 생성
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        # Dry-run: 더미 결과 출력
        dummy = {
            "domain": args.domain,
            "week": args.week,
            "collected_at": datetime.utcnow().isoformat() + "Z",
            "key_facts": ["[DRY-RUN] 실제 API 호출 없음"],
            "emerging_signals": [],
            "metrics": {},
            "sources": [],
            "confidence": 0.0,
            "summary": "[DRY-RUN] 테스트 실행",
            "_scope": args.scope,
            "_query_count": len(args.queries),
            "_collection_errors": [],
        }
        output_path.write_text(json.dumps(dummy, ensure_ascii=False, indent=2))
        print(f"[DRY-RUN] 결과 저장: {output_path}")
        return

    api_key = get_api_key()
    result = collect_intel(
        domain=args.domain,
        week=args.week,
        scope=args.scope,
        queries=args.queries,
        api_key=api_key,
    )

    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[OK] 인텔 수집 완료 → {output_path}")
    print(f"     도메인: {args.domain} | 쿼리 수: {result['_query_count']} | 신뢰도: {result['confidence']}")


if __name__ == "__main__":
    main()
