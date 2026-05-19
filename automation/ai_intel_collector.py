#!/usr/bin/env python3
"""
ai_intel_collector.py — Section A, Step 1
Perplexity sonar/sonar-pro API 기반 AI 도메인별 인텔 수집기

Usage:
  python ai_intel_collector.py \
    --domain enterprise_deployment \
    --week 2026-W21 \
    --scope standard \
    --queries "enterprise AI adoption" \
    --output output/ai_intel/intel_enterprise.json
"""

import argparse
import json
import os
import sys
import time
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("[ERROR] requests not installed: pip install requests")
    sys.exit(1)

# ─── Logging ───────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("ai_intel_collector")

# ─── Constants ──────────────────────────────────────────────────────────────
API_URL = "https://api.perplexity.ai/chat/completions"
MODEL_STANDARD = "sonar"
MODEL_DEEP = "sonar-pro"
MAX_RETRIES = 3
RETRY_BASE_DELAY = 5  # seconds, exponential backoff

DOMAINS = [
    "enterprise_deployment",
    "model_architecture",
    "regulatory_policy",
    "investment_funding",
    "open_source",
    "hardware_infrastructure",
    "safety_alignment",
]

DEFAULT_QUERIES = {
    "enterprise_deployment": [
        "enterprise AI deployment adoption trends 2026",
        "Fortune 500 AI implementation ROI case studies",
        "AI integration barriers enterprise software",
    ],
    "model_architecture": [
        "new LLM model releases architecture improvements 2026",
        "multimodal AI model capabilities benchmarks",
        "reasoning model performance comparisons",
    ],
    "regulatory_policy": [
        "AI regulation policy EU US China 2026",
        "AI governance framework enterprise compliance",
        "AI liability legislation updates",
    ],
    "investment_funding": [
        "AI startup funding rounds investments 2026",
        "AI infrastructure venture capital trends",
        "enterprise AI M&A activity",
    ],
    "open_source": [
        "open source AI model releases 2026",
        "Hugging Face Meta AI open models updates",
        "open source LLM enterprise adoption",
    ],
    "hardware_infrastructure": [
        "AI chip GPU supply demand 2026 NVIDIA AMD",
        "AI data center infrastructure investment",
        "edge AI hardware deployment",
    ],
    "safety_alignment": [
        "AI safety alignment research 2026",
        "LLM hallucination reduction techniques",
        "responsible AI governance practices",
    ],
}


# ─── Core Functions ─────────────────────────────────────────────────────────
def get_api_key() -> str:
    key = os.environ.get("PERPLEXITY_API_KEY", "")
    if not key:
        log.error("PERPLEXITY_API_KEY env var not set")
        sys.exit(1)
    return key


def select_model(scope: str) -> str:
    """scope: standard → sonar, deep/emergency → sonar-pro"""
    if scope in ("deep", "emergency"):
        log.info(f"Scope '{scope}' → escalating to {MODEL_DEEP}")
        return MODEL_DEEP
    return MODEL_STANDARD


def build_system_prompt(domain: str, week: str) -> str:
    return (
        f"You are an AI industry intelligence analyst. "
        f"Week: {week}. Domain focus: {domain.replace('_', ' ')}. "
        f"Respond ONLY with a JSON object matching this schema:\n"
        f"{{\"domain\": str, \"week\": str, \"collected_at\": str (ISO8601), "
        f"\"signals\": [{{\"title\": str, \"summary\": str (≤120 chars), "
        f"\"significance\": \"HIGH\" | \"MEDIUM\" | \"LOW\", "
        f"\"source_hint\": str, \"tags\": [str]}}], "
        f"\"key_facts\": [str], \"metrics\": {{str: str}}, "
        f"\"ew_indicators\": {{\"detected\": bool, \"reason\": str}}}}\n"
        f"Do not include markdown fences or extra text."
    )


def call_perplexity(
    api_key: str, model: str, system_prompt: str, user_query: str
) -> Optional[dict]:
    """Single API call with exponential backoff retry."""
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

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            log.info(f"  API call attempt {attempt}/{MAX_RETRIES} [model={model}]")
            resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)

            if resp.status_code == 429:
                delay = RETRY_BASE_DELAY * (2 ** (attempt - 1))
                log.warning(f"  Rate limit (429). Retrying in {delay}s...")
                time.sleep(delay)
                continue

            resp.raise_for_status()
            raw = resp.json()["choices"][0]["message"]["content"]
            return parse_json_response(raw)

        except requests.exceptions.Timeout:
            log.warning(f"  Timeout on attempt {attempt}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BASE_DELAY)
        except requests.exceptions.RequestException as e:
            log.error(f"  Request error: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BASE_DELAY)

    log.error("  Max retries exceeded")
    return None


def parse_json_response(raw: str) -> Optional[dict]:
    """Extract JSON from LLM response, handling markdown fences."""
    raw = raw.strip()
    # Strip markdown fences
    if raw.startswith("```"):
        lines = raw.split("\n")
        start = 1 if lines[0].startswith("```") else 0
        end = len(lines)
        for i in range(len(lines) - 1, 0, -1):
            if lines[i].strip() == "```":
                end = i
                break
        raw = "\n".join(lines[start:end])
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Try to extract first JSON object
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(raw[start : end + 1])
            except json.JSONDecodeError:
                pass
    log.warning("  Could not parse JSON from response")
    return None


def merge_signals(results: list[dict]) -> dict:
    """Merge multiple query results into a single domain intel object."""
    merged = {
        "signals": [],
        "key_facts": [],
        "metrics": {},
        "ew_indicators": {"detected": False, "reasons": []},
    }
    for r in results:
        if not r:
            continue
        merged["signals"].extend(r.get("signals", []))
        merged["key_facts"].extend(r.get("key_facts", []))
        merged["metrics"].update(r.get("metrics", {}))
        ew = r.get("ew_indicators", {})
        if ew.get("detected"):
            merged["ew_indicators"]["detected"] = True
            if ew.get("reason"):
                merged["ew_indicators"]["reasons"].append(ew["reason"])

    # Deduplicate key_facts
    merged["key_facts"] = list(dict.fromkeys(merged["key_facts"]))
    return merged


def collect_domain(
    domain: str,
    week: str,
    scope: str,
    queries: list[str],
    api_key: str,
) -> dict:
    model = select_model(scope)
    system_prompt = build_system_prompt(domain, week)
    log.info(f"Collecting domain: {domain} | week: {week} | model: {model}")

    results = []
    for q in queries:
        log.info(f"  Query: {q[:80]}")
        result = call_perplexity(api_key, model, system_prompt, q)
        if result:
            results.append(result)
        time.sleep(1)  # Polite delay between queries

    merged = merge_signals(results)
    output = {
        "domain": domain,
        "week": week,
        "scope": scope,
        "model_used": model,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "query_count": len(queries),
        "success_count": len([r for r in results if r]),
        **merged,
    }
    return output


# ─── Main ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="AI Intel Collector — Section A Step 1")
    parser.add_argument("--domain", required=True, choices=DOMAINS + ["all"],
                        help="Domain to collect or 'all'")
    parser.add_argument("--week", required=True, help="ISO week e.g. 2026-W21")
    parser.add_argument("--scope", default="standard",
                        choices=["standard", "deep", "emergency"],
                        help="Collection scope (affects model selection)")
    parser.add_argument("--queries", nargs="+",
                        help="Custom query strings (overrides defaults)")
    parser.add_argument("--output", required=True,
                        help="Output JSON file path")
    args = parser.parse_args()

    api_key = get_api_key()
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    domains_to_run = DOMAINS if args.domain == "all" else [args.domain]
    all_results = {}

    for domain in domains_to_run:
        queries = args.queries if args.queries else DEFAULT_QUERIES.get(domain, [])
        if not queries:
            log.warning(f"No queries for domain: {domain}, skipping")
            continue
        result = collect_domain(domain, args.week, args.scope, queries, api_key)
        all_results[domain] = result
        log.info(
            f"  ✓ {domain}: {result['success_count']}/{result['query_count']} queries OK, "
            f"{len(result['signals'])} signals, EW={result['ew_indicators']['detected']}"
        )

    # Write output
    if args.domain == "all":
        output_data = {
            "week": args.week,
            "scope": args.scope,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "domains": all_results,
        }
    else:
        output_data = all_results.get(args.domain, {})

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    log.info(f"\n✅ Output saved → {args.output}")

    # Exit 1 if EW detected (allows workflow conditional)
    ew_detected = any(
        v.get("ew_indicators", {}).get("detected", False)
        for v in all_results.values()
    )
    if ew_detected:
        log.warning("⚠️  EW signal detected in collection results")
        sys.exit(2)  # exit 2 = EW flag, not hard failure


if __name__ == "__main__":
    main()
