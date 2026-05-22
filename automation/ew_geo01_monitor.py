#!/usr/bin/env python3
"""
EW-GEO-01 Monitor — 지정학적 반도체 공급망 리스크 조기경보

Sub-commands:
  collect  : Perplexity sonar-pro로 GEO 신호 수집
  assess   : GPT-4o로 리스크 평가 및 심각도 판정
  notify   : Notion C-31 페이지 업데이트

Secrets (env):
  OPENAI_API_KEY       – GPT-4o assess
  PERPLEXITY_API_KEY   – sonar-pro collect
  NOTION_API_KEY       – Notion write
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx

# ──────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────
EW_ID = "EW-GEO-01"
EW_VERSION = "1.0.0"

SEVERITY_THRESHOLDS = {
    "CRITICAL": 85,
    "HIGH":     65,
    "MEDIUM":   40,
    "LOW":       0,
}

REGION_QUERY_MAP: dict[str, list[str]] = {
    "TW_CN": [
        "Taiwan China semiconductor military tension 2026 supply chain risk",
        "TSMC production risk geopolitical escalation latest",
        "China Taiwan strait semiconductor export disruption signal",
    ],
    "KR_JP": [
        "South Korea Japan semiconductor export control 2026",
        "HBM DRAM supply chain Korea Japan geopolitical risk",
        "Samsung SK Hynix Japan material export disruption",
    ],
    "US_EXPORT": [
        "US semiconductor export control China 2026 latest update",
        "BIS Entity List chip restriction AI semiconductor",
        "US CHIPS Act implementation semiconductor geopolitics",
    ],
    "EU_CHIPS": [
        "EU Chips Act semiconductor supply chain risk 2026",
        "Europe semiconductor geopolitical dependency critical",
        "ASML export restriction geopolitical semiconductor",
    ],
}

# "all" = 모든 지역 쿼리 합산
ALL_QUERIES: list[str] = [
    "semiconductor supply chain geopolitical risk 2026 latest",
    "Taiwan strait semiconductor disruption signal Q2 2026",
    "US China chip war escalation export control new measures",
    "HBM advanced packaging geopolitical supply chain threat",
    "South Korea semiconductor geopolitical risk DRAM NAND",
    "ASML EUV lithography export restriction geopolitical",
]

GPT_SYSTEM_PROMPT = """You are a senior geopolitical risk analyst specializing in semiconductor supply chains.
Your task is to analyze raw news signals and produce a structured risk assessment.

Output strictly valid JSON with this schema:
{
  "ew_id": "EW-GEO-01",
  "assessed_at": "<ISO8601 UTC>",
  "severity": "LOW|MEDIUM|HIGH|CRITICAL",
  "risk_score": <0-100 integer>,
  "ew_triggered": <true|false>,
  "top_signals": "<comma-separated top 3 signal titles max 200 chars>",
  "region_scores": {
    "TW_CN": <0-100>,
    "KR_JP": <0-100>,
    "US_EXPORT": <0-100>,
    "EU_CHIPS": <0-100>
  },
  "summary_ko": "<Korean 3-sentence executive summary>",
  "summary_en": "<English 3-sentence executive summary>",
  "recommended_action": "<MONITOR|ESCALATE|EMERGENCY>"
}

Severity thresholds: risk_score>=85→CRITICAL, >=65→HIGH, >=40→MEDIUM, <40→LOW.
ew_triggered = true when severity is HIGH or CRITICAL.
Respond with JSON only — no markdown, no explanation."""


# ──────────────────────────────────────────────────────────────
# HTTP helpers
# ──────────────────────────────────────────────────────────────

def _perplexity_search(query: str, api_key: str) -> dict[str, Any]:
    """Call Perplexity sonar-pro and return the response dict."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": "You are a geopolitical semiconductor risk monitor. Return factual, current information in JSON-friendly structured text."},
            {"role": "user",   "content": query},
        ],
        "max_tokens": 1024,
        "temperature": 0.1,
        "return_citations": True,
    }
    for attempt in range(3):
        try:
            resp = httpx.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json=payload,
                timeout=60.0,
            )
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429 and attempt < 2:
                time.sleep(10 * (attempt + 1))
                continue
            raise
    raise RuntimeError("Perplexity API failed after retries")


def _openai_chat(system: str, user: str, api_key: str, model: str = "gpt-4o") -> str:
    """Call OpenAI Chat Completions and return assistant content."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        "max_tokens": 2048,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
    }
    for attempt in range(3):
        try:
            resp = httpx.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60.0,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429 and attempt < 2:
                time.sleep(15 * (attempt + 1))
                continue
            raise
    raise RuntimeError("OpenAI API failed after retries")


def _notion_append_block(page_id: str, children: list[dict], api_key: str) -> None:
    """Append blocks to a Notion page."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    resp = httpx.patch(
        f"https://api.notion.com/v1/blocks/{page_id}/children",
        headers=headers,
        json={"children": children},
        timeout=30.0,
    )
    resp.raise_for_status()


# ──────────────────────────────────────────────────────────────
# Sub-command: collect
# ──────────────────────────────────────────────────────────────

def cmd_collect(args: argparse.Namespace) -> None:
    api_key = os.environ.get("PERPLEXITY_API_KEY", "")
    if not api_key:
        print("[WARN] PERPLEXITY_API_KEY not set — skipping live collection", file=sys.stderr)
        # Write empty placeholder so downstream jobs don't fail
        Path(args.output).write_text(json.dumps({
            "ew_id": EW_ID,
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "run_date": args.run_date,
            "week_id": args.week,
            "region": args.region,
            "signals": [],
            "_placeholder": True,
        }, ensure_ascii=False, indent=2))
        return

    region = args.region or "all"
    if region == "all":
        queries = ALL_QUERIES
    else:
        queries = REGION_QUERY_MAP.get(region, ALL_QUERIES)

    signals: list[dict] = []
    for i, q in enumerate(queries, 1):
        print(f"[collect] ({i}/{len(queries)}) {q[:80]}...")
        try:
            result = _perplexity_search(q, api_key)
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            citations = result.get("citations", [])
            signals.append({
                "query":     q,
                "content":   content,
                "citations": citations[:5],
                "region":    region,
                "collected_at": datetime.now(timezone.utc).isoformat(),
            })
        except Exception as e:
            print(f"[WARN] Query failed: {e}", file=sys.stderr)
            signals.append({"query": q, "content": "", "error": str(e), "region": region})
        time.sleep(2)  # rate-limit buffer

    output = {
        "ew_id":        EW_ID,
        "ew_version":   EW_VERSION,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "run_date":     args.run_date,
        "week_id":      args.week,
        "region":       region,
        "query_count":  len(queries),
        "signal_count": len([s for s in signals if not s.get("error")]),
        "signals":      signals,
    }
    Path(args.output).write_text(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"[collect] Done — {output['signal_count']}/{output['query_count']} signals → {args.output}")


# ──────────────────────────────────────────────────────────────
# Sub-command: assess
# ──────────────────────────────────────────────────────────────

def cmd_assess(args: argparse.Namespace) -> None:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("[WARN] OPENAI_API_KEY not set — using placeholder assessment", file=sys.stderr)
        _write_placeholder_assessment(args)
        return

    # Load signals
    signals_path = Path(args.signals)
    if not signals_path.exists():
        print(f"[WARN] Signals file not found: {args.signals} — using placeholder", file=sys.stderr)
        _write_placeholder_assessment(args)
        return

    signals_data = json.loads(signals_path.read_text())
    raw_signals = signals_data.get("signals", [])

    # Build user prompt
    signal_texts = []
    for s in raw_signals[:12]:  # limit token usage
        if s.get("content"):
            signal_texts.append(f"Q: {s['query']}\nA: {s['content'][:600]}")
    user_content = f"""Run Date: {args.run_date}
Week: {args.week}
Region Focus: {signals_data.get('region', 'all')}
Signal Count: {len(signal_texts)}

RAW SIGNALS:
{'='*60}
{chr(10).join(signal_texts[:10])}
{'='*60}

Please assess the geopolitical semiconductor supply chain risk."""

    print("[assess] Calling GPT-4o for risk assessment...")
    raw_response = _openai_chat(GPT_SYSTEM_PROMPT, user_content, api_key)

    try:
        assessment = json.loads(raw_response)
    except json.JSONDecodeError:
        print(f"[WARN] GPT-4o returned non-JSON: {raw_response[:200]}", file=sys.stderr)
        _write_placeholder_assessment(args)
        return

    # Override severity if manually set
    if args.severity and args.severity != "auto":
        assessment["severity"] = args.severity
        assessment["_severity_overridden"] = True

    # Recompute ew_triggered from final severity
    assessment["ew_triggered"] = assessment.get("severity") in ("HIGH", "CRITICAL")

    # Write outputs
    Path(args.output).write_text(json.dumps(assessment, ensure_ascii=False, indent=2))

    # Set GitHub Actions step outputs
    _set_github_output("severity",     assessment.get("severity", "LOW"))
    _set_github_output("risk_score",   str(assessment.get("risk_score", 0)))
    _set_github_output("top_signals",  assessment.get("top_signals", "")[:200])
    _set_github_output("ew_triggered", str(assessment.get("ew_triggered", False)).lower())
    _set_github_output("report_file",  str(args.output))

    print(f"[assess] Done — severity={assessment.get('severity')} score={assessment.get('risk_score')} ew_triggered={assessment.get('ew_triggered')}")
    print(f"[assess] Report → {args.output}")


def _write_placeholder_assessment(args: argparse.Namespace) -> None:
    """Write a safe placeholder when API keys are missing."""
    result = {
        "ew_id":            EW_ID,
        "assessed_at":      datetime.now(timezone.utc).isoformat(),
        "severity":         args.severity if args.severity and args.severity != "auto" else "LOW",
        "risk_score":       0,
        "ew_triggered":     False,
        "top_signals":      "placeholder — OPENAI_API_KEY not configured",
        "region_scores":    {"TW_CN": 0, "KR_JP": 0, "US_EXPORT": 0, "EU_CHIPS": 0},
        "summary_ko":       "API 키 미설정으로 평가를 수행하지 못했습니다.",
        "summary_en":       "Assessment skipped — OPENAI_API_KEY not configured.",
        "recommended_action": "MONITOR",
        "_placeholder":     True,
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2))
    _set_github_output("severity",     result["severity"])
    _set_github_output("risk_score",   "0")
    _set_github_output("top_signals",  result["top_signals"])
    _set_github_output("ew_triggered", "false")
    _set_github_output("report_file",  str(args.output))
    print(f"[assess] Placeholder written → {args.output}")


# ──────────────────────────────────────────────────────────────
# Sub-command: notify
# ──────────────────────────────────────────────────────────────

def cmd_notify(args: argparse.Namespace) -> None:
    api_key = os.environ.get("NOTION_API_KEY", "")
    page_id = args.page_id or os.environ.get("NOTION_C31_PAGE_ID", "")

    if not api_key or not page_id:
        print("[WARN] NOTION_API_KEY or page_id missing — skipping Notion update", file=sys.stderr)
        return

    severity    = args.severity    or "LOW"
    risk_score  = args.risk_score  or "0"
    signals_str = args.signals     or ""
    ew_id       = args.ew_id       or EW_ID
    run_date    = args.run_date
    week        = args.week

    # Severity → emoji
    sev_emoji = {
        "CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"
    }.get(severity, "⚪")

    header_text = f"{sev_emoji} {ew_id} | {severity} | Score {risk_score}/100 | {run_date} ({week})"

    blocks = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": header_text}}]
            },
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": f"Top Signals: {signals_str[:500]}" if signals_str else "No signals recorded."},
                }]
            },
        },
        {
            "object": "block",
            "type": "divider",
            "divider": {},
        },
    ]

    try:
        _notion_append_block(page_id, blocks, api_key)
        print(f"[notify] Notion C-31 updated — {header_text}")
    except Exception as e:
        print(f"[ERROR] Notion update failed: {e}", file=sys.stderr)
        sys.exit(1)


# ──────────────────────────────────────────────────────────────
# GitHub Actions output helper
# ──────────────────────────────────────────────────────────────

def _set_github_output(key: str, value: str) -> None:
    """Write to GITHUB_OUTPUT file (Actions v2 output syntax)."""
    github_output = os.environ.get("GITHUB_OUTPUT", "")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"{key}={value}\n")
    else:
        print(f"[output] {key}={value}")


# ──────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="EW-GEO-01 Geopolitical Semiconductor Monitor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # collect
    p_collect = sub.add_parser("collect", help="Collect GEO signals via Perplexity")
    p_collect.add_argument("--output",   required=True, help="Output JSON file path")
    p_collect.add_argument("--region",   default="all", help="Region filter")
    p_collect.add_argument("--run-date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    p_collect.add_argument("--week",     default="")

    # assess
    p_assess = sub.add_parser("assess", help="Assess risk via GPT-4o")
    p_assess.add_argument("--signals",  required=True, help="Signals JSON file")
    p_assess.add_argument("--output",   required=True, help="Assessment output JSON")
    p_assess.add_argument("--severity", default="auto", help="Override severity")
    p_assess.add_argument("--run-date", default="")
    p_assess.add_argument("--week",     default="")

    # notify
    p_notify = sub.add_parser("notify", help="Update Notion C-31")
    p_notify.add_argument("--page-id",    required=True)
    p_notify.add_argument("--run-date",   required=True)
    p_notify.add_argument("--week",       required=True)
    p_notify.add_argument("--severity",   default="LOW")
    p_notify.add_argument("--risk-score", default="0")
    p_notify.add_argument("--signals",    default="")
    p_notify.add_argument("--ew-id",      default=EW_ID)

    return parser


def main() -> None:
    parser = build_parser()
    args   = parser.parse_args()

    if args.command == "collect":
        cmd_collect(args)
    elif args.command == "assess":
        cmd_assess(args)
    elif args.command == "notify":
        cmd_notify(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
