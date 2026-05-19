#!/usr/bin/env python3
"""
automation/ai_intel_collector.py
Perplexity sonar/sonar-pro API 기반 AI 인텔리전스 주간 수집기

Usage:
  python automation/ai_intel_collector.py \
    --domain enterprise_deployment \
    --week 2026-W21 \
    --scope standard \
    --queries "query1" "query2" \
    --output output/ai_intel/intel_enterprise.json
"""

import argparse
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

# ──────────────────────────────────────────
# Config
# ──────────────────────────────────────────
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

MODEL_MAP = {
    "standard": "sonar",
    "deep": "sonar-pro",
    "emergency": "sonar-pro",
}

MAX_RETRIES = 3
RETRY_BASE_DELAY = 5  # seconds


def call_perplexity(query: str, model: str, api_key: str) -> dict:
    """Perplexity API 단일 쿼리 호출 (지수 백오프 재시도)"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an AI industry intelligence analyst. "
                    "Provide structured, factual, quantified insights in JSON format. "
                    "Focus on metrics, adoption rates, market data, and specific company actions. "
                    "Always include numeric values where available."
                ),
            },
            {"role": "user", "content": query},
        ],
        "max_tokens": 2000,
        "temperature": 0.2,
        "return_citations": True,
    }

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(
                PERPLEXITY_API_URL,
                headers=headers,
                json=payload,
                timeout=60,
            )
            if resp.status_code == 429:  # Rate limit
                delay = RETRY_BASE_DELAY * (2 ** attempt)
                print(f"  [WARN] Rate limited. Waiting {delay}s... (attempt {attempt+1}/{MAX_RETRIES})")
                time.sleep(delay)
                continue
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            citations = data.get("citations", [])
            return {"content": content, "citations": citations, "model": model}
        except requests.exceptions.RequestException as e:
            if attempt == MAX_RETRIES - 1:
                raise
            delay = RETRY_BASE_DELAY * (2 ** attempt)
            print(f"  [WARN] Request failed: {e}. Retrying in {delay}s...")
            time.sleep(delay)

    return {"content": "", "citations": [], "model": model}


def parse_json_from_content(content: str) -> dict:
    """LLM 응답에서 JSON 블록 자동 파싱 (3단계 폴백)"""
    # 1순위: ```json ... ``` 블록
    match = re.search(r"```json\s*([\s\S]*?)```", content)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # 2순위: 중괄호 블록
    match = re.search(r"(\{[\s\S]*\})", content)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # 3순위: raw 텍스트를 구조화
    return {"raw_text": content, "parsed": False}


def extract_metrics(parsed: dict) -> dict:
    """파싱된 응답에서 수치 메트릭 추출"""
    metrics = {}
    metric_keys = [
        "enterprise_adoption_rate",
        "oss_rag_migration_rate",
        "new_model_releases_per_week",
        "ai_consulting_market_disruption",
        "container_ml_adoption",
        "multi_agent_orchestration_adoption",
    ]

    def _find_value(d: dict, keys: list) -> float | None:
        """중첩 딕셔너리에서 유사 키 매칭으로 값 추출"""
        for k in keys:
            if k in d:
                val = d[k]
                if isinstance(val, (int, float)):
                    return float(val)
                if isinstance(val, str):
                    nums = re.findall(r"[\d.]+", val)
                    if nums:
                        return float(nums[0])
            # 유사 키 매칭 (부분 문자열)
            for dk in d:
                if k.replace("_", " ") in dk.replace("_", " "):
                    val = d[dk]
                    if isinstance(val, (int, float)):
                        return float(val)
        return None

    for key in metric_keys:
        val = _find_value(parsed, [key])
        if val is not None:
            metrics[key] = val

    return metrics


def collect_domain_intel(
    domain: str,
    week: str,
    scope: str,
    queries: list[str],
    api_key: str,
) -> dict:
    """도메인별 인텔리전스 수집 메인 로직"""
    model = MODEL_MAP.get(scope, "sonar")
    print(f"\n[INFO] Domain: {domain} | Week: {week} | Model: {model}")
    print(f"[INFO] Queries: {len(queries)}개")

    results = []
    all_metrics = {}
    all_key_facts = []
    all_citations = []

    for i, query in enumerate(queries, 1):
        print(f"  [{i}/{len(queries)}] Query: {query[:60]}...")
        try:
            raw = call_perplexity(query, model, api_key)
            parsed = parse_json_from_content(raw["content"])
            metrics = extract_metrics(parsed)
            all_metrics.update(metrics)

            # key_facts 추출
            key_facts = parsed.get("key_facts", [])
            if isinstance(key_facts, list):
                all_key_facts.extend(key_facts)
            elif parsed.get("raw_text"):
                # raw 텍스트에서 bullet 포인트 추출
                bullets = re.findall(r"[-•*]\s+(.+)", parsed.get("raw_text", ""))
                all_key_facts.extend(bullets[:5])

            all_citations.extend(raw.get("citations", []))

            results.append({
                "query": query,
                "content_raw": raw["content"],
                "content_parsed": parsed,
                "metrics": metrics,
                "citations": raw.get("citations", []),
            })

            # Rate limit 방지 (표준 0.5초, emergency 즉시)
            if scope != "emergency":
                time.sleep(0.5)

        except Exception as e:
            print(f"  [ERROR] Query failed: {e}")
            results.append({"query": query, "error": str(e)})

    output = {
        "domain": domain,
        "week": week,
        "scope": scope,
        "model": model,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "query_count": len(queries),
        "metrics": all_metrics,
        "key_facts": all_key_facts[:20],  # 최대 20개
        "citations": list(set(all_citations))[:30],  # 중복 제거, 최대 30개
        "query_results": results,
    }

    print(f"[OK] 수집 완료: metrics={len(all_metrics)}, key_facts={len(all_key_facts)}, citations={len(all_citations)}")
    return output


def main():
    parser = argparse.ArgumentParser(description="AI Intel Collector — Perplexity API 기반")
    parser.add_argument("--domain", required=True, help="수집 도메인 식별자")
    parser.add_argument("--week", required=True, help="주간 레이블 (예: 2026-W21)")
    parser.add_argument(
        "--scope",
        choices=["standard", "deep", "emergency"],
        default="standard",
        help="수집 범위 및 모델 선택",
    )
    parser.add_argument("--queries", nargs="+", required=True, help="수집 쿼리 목록")
    parser.add_argument("--output", required=True, help="출력 JSON 파일 경로")
    args = parser.parse_args()

    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        raise EnvironmentError("PERPLEXITY_API_KEY 환경변수가 설정되지 않았습니다.")

    result = collect_domain_intel(
        domain=args.domain,
        week=args.week,
        scope=args.scope,
        queries=args.queries,
        api_key=api_key,
    )

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[SAVED] {out_path}")


if __name__ == "__main__":
    main()
