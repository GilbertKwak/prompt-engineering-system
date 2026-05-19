#!/usr/bin/env python3
"""
ai_intel_collector.py
─────────────────────
Perplexity sonar-pro API 기반 AI 인텔리전스 수집기
워크플로: ai-intel-weekly.yml → STAGE 1 (5개 도메인 병렬 호출)

사용법:
  python automation/ai_intel_collector.py \
    --domain enterprise_deployment \
    --week 2026-W21 \
    --scope standard \
    --queries "OpenAI enterprise consulting" "AI agent production 2026" \
    --output output/ai_intel/intel_enterprise.json
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

# ─────────────────────────────────────────
# 상수
# ─────────────────────────────────────────
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

SCOPE_CONFIG = {
    "standard": {"model": "sonar",      "max_tokens": 800,  "temperature": 0.2},
    "deep":     {"model": "sonar-pro",  "max_tokens": 1500, "temperature": 0.1},
    "emergency":{"model": "sonar-pro",  "max_tokens": 2000, "temperature": 0.05},
}

DOMAIN_SYSTEM_PROMPTS = {
    "enterprise_deployment": (
        "You are an enterprise AI deployment analyst. "
        "Extract concrete data points: adoption rates (%), company names, "
        "deployment timelines, ROI metrics. "
        "Format output as structured JSON with keys: summary, key_facts (list), "
        "metrics (dict with numeric values), companies (list), signals (list), sources (list)."
    ),
    "frameworks_rag": (
        "You are an AI framework and RAG architecture specialist. "
        "Track version releases, migration patterns, benchmark scores, adoption shifts. "
        "Format output as structured JSON with keys: summary, key_facts, metrics, "
        "frameworks (list with version info), migration_trends (list), signals, sources."
    ),
    "model_releases": (
        "You are an AI model benchmark analyst. "
        "Track new model releases, benchmark scores (MMLU, HumanEval, MATH), capability deltas. "
        "Format output as structured JSON with keys: summary, key_facts, metrics, "
        "models (list with name/provider/benchmark_scores), capability_shifts (list), signals, sources."
    ),
    "infra_market": (
        "You are an AI infrastructure and market analyst. "
        "Extract market size figures ($B), growth rates (%), investment deals, "
        "infrastructure adoption rates. "
        "Format output as structured JSON with keys: summary, key_facts, metrics, "
        "market_data (dict), investment_events (list), signals, sources."
    ),
    "semiconductor_chips": (
        "You are a semiconductor and AI chip supply chain analyst. "
        "Track chip releases, HBM/DRAM supply, yield rates, pricing, "
        "inference efficiency metrics. "
        "Format output as structured JSON with keys: summary, key_facts, metrics, "
        "chip_releases (list), supply_chain_events (list), signals, sources."
    ),
}

DEFAULT_SYSTEM_PROMPT = (
    "You are an AI intelligence analyst. "
    "Extract key facts, metrics, and signals. "
    "Format output as structured JSON with keys: summary, key_facts, metrics, signals, sources."
)


# ─────────────────────────────────────────
# Perplexity API 호출
# ─────────────────────────────────────────
def call_perplexity(
    query: str,
    system_prompt: str,
    api_key: str,
    model: str,
    max_tokens: int,
    temperature: float,
    retry: int = 3,
) -> dict:
    """단일 Perplexity API 호출 (재시도 포함)"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "return_citations": True,
        "search_recency_filter": "week",  # 최신 1주 우선
    }

    for attempt in range(retry):
        try:
            resp = requests.post(
                PERPLEXITY_API_URL,
                headers=headers,
                json=payload,
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            citations = data.get("citations", [])

            # JSON 파싱 시도
            parsed = _safe_parse_json(content)
            parsed["_raw"] = content[:500]  # 디버그용 원문 일부 보존
            parsed["_citations"] = citations[:5]  # 상위 5개 출처
            parsed["_query"] = query
            return parsed

        except requests.exceptions.HTTPError as e:
            if resp.status_code == 429:  # Rate limit
                wait = 2 ** attempt * 5
                print(f"[WARN] Rate limit hit. Waiting {wait}s... (attempt {attempt+1}/{retry})", file=sys.stderr)
                time.sleep(wait)
            else:
                print(f"[ERROR] HTTP {resp.status_code}: {e}", file=sys.stderr)
                if attempt == retry - 1:
                    return {"error": str(e), "_query": query, "summary": "API call failed", "key_facts": [], "metrics": {}, "signals": []}
                time.sleep(3)

        except Exception as e:
            print(f"[ERROR] Unexpected error on attempt {attempt+1}: {e}", file=sys.stderr)
            if attempt == retry - 1:
                return {"error": str(e), "_query": query, "summary": "API call failed", "key_facts": [], "metrics": {}, "signals": []}
            time.sleep(3)

    return {"error": "max_retry_exceeded", "_query": query, "summary": "Max retries exceeded", "key_facts": [], "metrics": {}, "signals": []}


def _safe_parse_json(text: str) -> dict:
    """LLM 응답에서 JSON 블록 추출 및 파싱"""
    import re

    # ```json ... ``` 블록 우선 추출
    pattern = r"```(?:json)?\s*([\s\S]*?)```"
    match = re.search(pattern, text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # { ... } 직접 추출 시도
    brace_match = re.search(r"(\{[\s\S]*\})", text)
    if brace_match:
        try:
            return json.loads(brace_match.group(1))
        except json.JSONDecodeError:
            pass

    # 파싱 실패 → 원문을 summary로
    return {
        "summary": text[:300],
        "key_facts": [],
        "metrics": {},
        "signals": [],
    }


# ─────────────────────────────────────────
# 멀티쿼리 수집 및 통합
# ─────────────────────────────────────────
def collect_domain_intel(
    domain: str,
    queries: list[str],
    week: str,
    scope: str,
    api_key: str,
) -> dict:
    """도메인별 멀티쿼리 실행 후 결과 통합"""
    cfg = SCOPE_CONFIG.get(scope, SCOPE_CONFIG["standard"])
    system_prompt = DOMAIN_SYSTEM_PROMPTS.get(domain, DEFAULT_SYSTEM_PROMPT)

    print(f"[INFO] Domain={domain} | Scope={scope} | Model={cfg['model']} | Queries={len(queries)}", file=sys.stderr)

    raw_results = []
    for i, query in enumerate(queries):
        print(f"  [{i+1}/{len(queries)}] Query: {query[:80]}...", file=sys.stderr)
        result = call_perplexity(
            query=query,
            system_prompt=system_prompt,
            api_key=api_key,
            model=cfg["model"],
            max_tokens=cfg["max_tokens"],
            temperature=cfg["temperature"],
        )
        raw_results.append(result)
        time.sleep(1.5)  # API rate limit 보호

    # 멀티쿼리 결과 통합
    merged = _merge_results(raw_results, domain, week)
    return merged


def _merge_results(results: list[dict], domain: str, week: str) -> dict:
    """복수 쿼리 결과 → 단일 도메인 인텔 객체로 통합"""
    all_facts = []
    all_signals = []
    all_sources = []
    merged_metrics = {}
    summaries = []

    for r in results:
        if r.get("error"):
            print(f"[WARN] Skipping errored result: {r.get('error')}", file=sys.stderr)
            continue
        summaries.append(r.get("summary", ""))
        all_facts.extend(r.get("key_facts", []))
        all_signals.extend(r.get("signals", []))
        all_sources.extend(r.get("_citations", []))
        merged_metrics.update(r.get("metrics", {}))

    # 중복 제거
    unique_facts = list(dict.fromkeys(all_facts))[:20]  # 최대 20개
    unique_signals = list(dict.fromkeys(str(s) for s in all_signals if s))[:10]

    return {
        "domain": domain,
        "week": week,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "query_count": len(results),
        "summary": " | ".join(s for s in summaries if s)[:1000],
        "key_facts": unique_facts,
        "metrics": merged_metrics,
        "signals": unique_signals,
        "sources": list(set(str(s) for s in all_sources if s))[:10],
        "raw_results": results,  # 전체 원본 보존
    }


# ─────────────────────────────────────────
# CLI
# ─────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="AI Intel Collector via Perplexity API")
    p.add_argument("--domain",  required=True, help="Intel domain key")
    p.add_argument("--week",    required=True, help="ISO week label (e.g. 2026-W21)")
    p.add_argument("--scope",   default="standard", choices=["standard", "deep", "emergency"])
    p.add_argument("--queries", nargs="+", required=True, help="Search query strings")
    p.add_argument("--output",  required=True, help="Output JSON file path")
    return p.parse_args()


def main():
    args = parse_args()

    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        print("[ERROR] PERPLEXITY_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    # 출력 디렉토리 생성
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 인텔 수집 실행
    intel = collect_domain_intel(
        domain=args.domain,
        queries=args.queries,
        week=args.week,
        scope=args.scope,
        api_key=api_key,
    )

    # JSON 저장
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(intel, f, ensure_ascii=False, indent=2)

    print(f"[OK] Saved → {output_path}", file=sys.stderr)
    print(f"     Facts: {len(intel['key_facts'])} | Signals: {len(intel['signals'])} | Metrics: {len(intel['metrics'])}", file=sys.stderr)


if __name__ == "__main__":
    main()
