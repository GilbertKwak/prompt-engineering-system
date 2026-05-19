#!/usr/bin/env python3
"""
ai_intel_collector.py
─────────────────────
Perplexity API 없는 무료 멀티소스 AI 인텔리전스 수집기
수집 우선순위:
  1순위  RSS 피드  (완전 무료, 무제한)
  2순위  NewsAPI   (무료 티어 100req/day, NEWSAPI_KEY 선택)
  3순위  SerpAPI   (무료 100req/month, SERPAPI_KEY 선택)
  4순위  OpenRouter free tier LLM 요약 (OPENROUTER_API_KEY 선택)

API 키가 하나도 없어도 RSS만으로 동작합니다.

사용법:
  python automation/ai_intel_collector.py \\
    --domain enterprise_deployment \\
    --week 2026-W21 \\
    --scope standard \\
    --queries "enterprise AI deployment" "AI agent production" \\
    --output output/ai_intel/intel_enterprise.json
"""

import argparse
import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import quote_plus
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# ─────────────────────────────────────────
# RSS 피드 — 완전 무료, 키 불필요
# ─────────────────────────────────────────
RSS_FEEDS = {
    "enterprise_deployment": [
        "https://techcrunch.com/feed/",
        "https://feeds.feedburner.com/venturebeat/SZYF",
        "https://www.infoq.com/feed/?topicNames=ai-ml-data-eng",
        "https://tldr.tech/ai/rss",
    ],
    "frameworks_rag": [
        "https://blog.langchain.dev/rss/",
        "https://www.llamaindex.ai/blog/rss.xml",
        "https://huggingface.co/blog/feed.xml",
        "https://feeds.feedburner.com/venturebeat/SZYF",
    ],
    "model_releases": [
        "https://openai.com/blog/rss.xml",
        "https://www.anthropic.com/rss.xml",
        "https://blog.google/technology/ai/rss/",
        "https://mistral.ai/news/rss.xml",
        "https://huggingface.co/blog/feed.xml",
    ],
    "infra_market": [
        "https://techcrunch.com/feed/",
        "https://feeds.feedburner.com/venturebeat/SZYF",
        "https://semianalysis.com/feed/",
        "https://www.semiengineering.com/feed/",
    ],
    "semiconductor_chips": [
        "https://semianalysis.com/feed/",
        "https://www.semiengineering.com/feed/",
        "https://techcrunch.com/feed/",
        "https://feeds.feedburner.com/AnandTech",
    ],
    "_default": [
        "https://techcrunch.com/feed/",
        "https://feeds.feedburner.com/venturebeat/SZYF",
        "https://huggingface.co/blog/feed.xml",
    ],
}

# 도메인별 키워드 필터
DOMAIN_KEYWORDS = {
    "enterprise_deployment": ["enterprise", "deployment", "production", "adoption", "ROI", "consulting"],
    "frameworks_rag": ["RAG", "LangChain", "LlamaIndex", "vector", "embedding", "retrieval", "framework"],
    "model_releases": ["GPT", "Claude", "Gemini", "Llama", "Mistral", "benchmark", "release", "model"],
    "infra_market": ["GPU", "inference", "cloud", "market", "investment", "funding", "infrastructure"],
    "semiconductor_chips": ["NVIDIA", "AMD", "Intel", "HBM", "chip", "semiconductor", "DRAM", "supply"],
    "_default": ["AI", "LLM", "agent", "machine learning"],
}

# ─────────────────────────────────────────
# 유틸
# ─────────────────────────────────────────
def _http_get(url: str, timeout: int = 15) -> str:
    """단순 HTTP GET, User-Agent 포함"""
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (AI-Intel-Collector/2.0)"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(charset, errors="replace")
    except Exception as e:
        print(f"[WARN] GET failed {url}: {e}", file=sys.stderr)
        return ""


def _keywords_match(text: str, keywords: list[str]) -> bool:
    """텍스트에서 키워드 하나 이상 매칭"""
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


def _extract_metrics(text: str) -> dict:
    """텍스트에서 숫자/퍼센트/달러 수치 자동 추출"""
    metrics = {}
    patterns = {
        "percent": r"(\d+(?:\.\d+)?)\s*%",
        "billion_usd": r"\$\s*(\d+(?:\.\d+)?)\s*[Bb](?:illion)?",
        "million_usd": r"\$\s*(\d+(?:\.\d+)?)\s*[Mm](?:illion)?",
        "year": r"\b(202[4-9]|203\d)\b",
    }
    for key, pat in patterns.items():
        matches = re.findall(pat, text)
        if matches:
            metrics[key] = matches[:5]
    return metrics


def _clean_html(text: str) -> str:
    """간단한 HTML 태그 제거"""
    return re.sub(r"<[^>]+>", "", text).strip()


# ─────────────────────────────────────────
# STAGE 1 — RSS 수집 (무료)
# ─────────────────────────────────────────
def collect_rss(domain: str, keywords: list[str], days_back: int = 7) -> list[dict]:
    """RSS 피드에서 키워드 매칭 아이템 수집"""
    feeds = RSS_FEEDS.get(domain, RSS_FEEDS["_default"])
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)
    items = []

    for feed_url in feeds:
        print(f"  [RSS] {feed_url}", file=sys.stderr)
        raw = _http_get(feed_url)
        if not raw:
            continue
        try:
            root = ET.fromstring(raw)
        except ET.ParseError:
            continue

        ns = {"atom": "http://www.w3.org/2005/Atom"}
        # RSS 2.0
        for item in root.iter("item"):
            title = item.findtext("title", "")
            desc  = _clean_html(item.findtext("description", ""))
            link  = item.findtext("link", "")
            pub   = item.findtext("pubDate", "")
            text  = f"{title} {desc}"
            if _keywords_match(text, keywords):
                items.append({"title": title, "desc": desc[:300], "link": link, "pub": pub, "source": "rss"})
        # Atom
        for entry in root.findall(".//atom:entry", ns):
            title = entry.findtext("atom:title", "", ns)
            summary = _clean_html(entry.findtext("atom:summary", "", ns))
            link_el = entry.find("atom:link", ns)
            link = link_el.get("href", "") if link_el is not None else ""
            text = f"{title} {summary}"
            if _keywords_match(text, keywords):
                items.append({"title": title, "desc": summary[:300], "link": link, "pub": "", "source": "rss"})

        time.sleep(0.5)

    print(f"  [RSS] {len(items)} items matched", file=sys.stderr)
    return items[:30]


# ─────────────────────────────────────────
# STAGE 2 — NewsAPI (선택, 무료 100req/day)
# ─────────────────────────────────────────
def collect_newsapi(query: str, api_key: str) -> list[dict]:
    """NewsAPI everything endpoint"""
    url = (
        f"https://newsapi.org/v2/everything"
        f"?q={quote_plus(query)}"
        f"&language=en&sortBy=publishedAt&pageSize=10"
        f"&apiKey={api_key}"
    )
    raw = _http_get(url)
    if not raw:
        return []
    try:
        data = json.loads(raw)
        articles = data.get("articles", [])
        return [
            {
                "title": a.get("title", ""),
                "desc": (a.get("description") or "")[:300],
                "link": a.get("url", ""),
                "pub": a.get("publishedAt", ""),
                "source": "newsapi",
            }
            for a in articles
        ]
    except Exception as e:
        print(f"  [WARN] NewsAPI parse error: {e}", file=sys.stderr)
        return []


# ─────────────────────────────────────────
# STAGE 3 — SerpAPI Google News (선택, 무료 100req/month)
# ─────────────────────────────────────────
def collect_serpapi(query: str, api_key: str) -> list[dict]:
    """SerpAPI Google News search"""
    url = (
        f"https://serpapi.com/search.json"
        f"?engine=google_news&q={quote_plus(query)}&num=10&api_key={api_key}"
    )
    raw = _http_get(url)
    if not raw:
        return []
    try:
        data = json.loads(raw)
        results = data.get("news_results", [])
        return [
            {
                "title": r.get("title", ""),
                "desc": (r.get("snippet") or "")[:300],
                "link": r.get("link", ""),
                "pub": r.get("date", ""),
                "source": "serpapi",
            }
            for r in results
        ]
    except Exception as e:
        print(f"  [WARN] SerpAPI parse error: {e}", file=sys.stderr)
        return []


# ─────────────────────────────────────────
# STAGE 4 — OpenRouter Free LLM 요약 (선택)
# 무료 모델: meta-llama/llama-3.1-8b-instruct:free
#            mistralai/mistral-7b-instruct:free
# ─────────────────────────────────────────
OPENROUTER_FREE_MODELS = [
    "meta-llama/llama-3.1-8b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
]

def summarize_with_openrouter(articles: list[dict], domain: str, api_key: str) -> dict:
    """OpenRouter 무료 LLM으로 수집된 기사 요약 및 구조화"""
    if not articles:
        return {}

    headlines = "\n".join(
        f"- {a['title']}: {a['desc'][:150]}" for a in articles[:15]
    )
    prompt = (
        f"Domain: {domain}\n"
        f"Recent AI news headlines:\n{headlines}\n\n"
        "Analyze and return JSON with keys: summary (str), key_facts (list of str), "
        "signals (list of str, emerging trends), metrics (dict of numeric values found).\n"
        "Return ONLY valid JSON."
    )

    import urllib.request, urllib.error
    payload = json.dumps({
        "model": OPENROUTER_FREE_MODELS[0],
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 600,
        "temperature": 0.2,
    }).encode()

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/GilbertKwak/prompt-engineering-system",
            "X-Title": "AI-Intel-Collector",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            content = data["choices"][0]["message"]["content"]
            return _safe_parse_json(content)
    except Exception as e:
        print(f"  [WARN] OpenRouter error: {e}", file=sys.stderr)
        return {}


def _safe_parse_json(text: str) -> dict:
    """LLM 응답에서 JSON 블록 추출"""
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass
    brace = re.search(r"(\{[\s\S]*\})", text)
    if brace:
        try:
            return json.loads(brace.group(1))
        except json.JSONDecodeError:
            pass
    return {"summary": text[:300], "key_facts": [], "metrics": {}, "signals": []}


# ─────────────────────────────────────────
# 로컬 통계 기반 키팩트 추출 (LLM 없이)
# ─────────────────────────────────────────
def extract_facts_local(articles: list[dict]) -> dict:
    """기사 제목/설명에서 key_facts, signals, metrics를 규칙 기반으로 추출"""
    key_facts = []
    signals = []
    all_text = ""

    for a in articles:
        text = f"{a['title']} {a['desc']}"
        all_text += text + " "
        if len(a["title"]) > 20:
            key_facts.append(a["title"])

    # 시그널 키워드 탐지
    signal_patterns = [
        (r"(raises?|secures?|closes?).{0,30}\$[\d.]+[BbMm]", "funding"),
        (r"(launches?|releases?|announces?).{0,30}(model|version|update)", "product_release"),
        (r"(acquires?|acqui|buys?|merges?).{0,40}", "M&A"),
        (r"(partners?|partnership|collaborat).{0,40}", "partnership"),
        (r"(ban|restrict|regulat|comply|complian).{0,40}", "regulatory"),
        (r"(surpass|exceed|outperform|beat).{0,40}(GPT|Claude|human|benchmark)", "benchmark"),
    ]
    for pat, sig_type in signal_patterns:
        if re.search(pat, all_text, re.IGNORECASE):
            signals.append(sig_type)

    metrics = _extract_metrics(all_text)
    summary = f"{len(articles)} articles collected. Topics: " + ", ".join(
        set(re.findall(r"\b(GPT|Claude|Gemini|Llama|NVIDIA|RAG|LangChain|HBM)\b", all_text))
    )[:500]

    return {
        "summary": summary,
        "key_facts": list(dict.fromkeys(key_facts))[:20],
        "signals": list(set(signals)),
        "metrics": metrics,
    }


# ─────────────────────────────────────────
# 메인 수집 오케스트레이터
# ─────────────────────────────────────────
def collect_domain_intel(
    domain: str,
    queries: list[str],
    week: str,
    scope: str,
) -> dict:
    keywords = DOMAIN_KEYWORDS.get(domain, DOMAIN_KEYWORDS["_default"])
    # 쿼리에서 키워드 보강
    for q in queries:
        keywords.extend(q.split()[:3])
    keywords = list(set(keywords))

    newsapi_key    = os.environ.get("NEWSAPI_KEY", "")
    serpapi_key    = os.environ.get("SERPAPI_KEY", "")
    openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")

    print(f"[INFO] Domain={domain} | Week={week} | Scope={scope}", file=sys.stderr)
    print(f"       Sources: RSS=✅  NewsAPI={'✅' if newsapi_key else '❌(키 없음)'}  "
          f"SerpAPI={'✅' if serpapi_key else '❌(키 없음)'}  "
          f"OpenRouter={'✅' if openrouter_key else '❌(키 없음, 로컬 추출 사용)'}", file=sys.stderr)

    all_articles = []

    # 1순위: RSS (항상 실행)
    rss_items = collect_rss(domain, keywords)
    all_articles.extend(rss_items)

    # 2순위: NewsAPI
    if newsapi_key:
        for q in queries[:2]:
            print(f"  [NewsAPI] query: {q}", file=sys.stderr)
            items = collect_newsapi(q, newsapi_key)
            all_articles.extend(items)
            time.sleep(1)

    # 3순위: SerpAPI
    if serpapi_key:
        for q in queries[:2]:
            print(f"  [SerpAPI] query: {q}", file=sys.stderr)
            items = collect_serpapi(q, serpapi_key)
            all_articles.extend(items)
            time.sleep(1)

    # 중복 URL 제거
    seen_links = set()
    unique_articles = []
    for a in all_articles:
        if a["link"] not in seen_links:
            seen_links.add(a["link"])
            unique_articles.append(a)

    print(f"[INFO] Total unique articles: {len(unique_articles)}", file=sys.stderr)

    # 4순위: OpenRouter LLM 요약 (키 있을 때)
    if openrouter_key and unique_articles:
        print(f"  [OpenRouter] Summarizing {len(unique_articles)} articles...", file=sys.stderr)
        llm_result = summarize_with_openrouter(unique_articles, domain, openrouter_key)
    else:
        # 로컬 규칙 기반 추출 (LLM 없이)
        print(f"  [Local] Rule-based extraction (no LLM)", file=sys.stderr)
        llm_result = extract_facts_local(unique_articles)

    return {
        "domain": domain,
        "week": week,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "query_count": len(queries),
        "article_count": len(unique_articles),
        "source_breakdown": {
            "rss": sum(1 for a in unique_articles if a["source"] == "rss"),
            "newsapi": sum(1 for a in unique_articles if a["source"] == "newsapi"),
            "serpapi": sum(1 for a in unique_articles if a["source"] == "serpapi"),
        },
        "summary": llm_result.get("summary", ""),
        "key_facts": llm_result.get("key_facts", []),
        "metrics": llm_result.get("metrics", {}),
        "signals": llm_result.get("signals", []),
        "sources": [a["link"] for a in unique_articles[:10] if a["link"]],
        "articles": unique_articles[:30],  # 원본 기사 보존
    }


# ─────────────────────────────────────────
# CLI
# ─────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="AI Intel Collector — Perplexity API 없는 무료 버전")
    p.add_argument("--domain",  required=True)
    p.add_argument("--week",    required=True)
    p.add_argument("--scope",   default="standard", choices=["standard", "deep", "emergency"])
    p.add_argument("--queries", nargs="+", required=True)
    p.add_argument("--output",  required=True)
    return p.parse_args()


def main():
    args = parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    intel = collect_domain_intel(
        domain=args.domain,
        queries=args.queries,
        week=args.week,
        scope=args.scope,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(intel, f, ensure_ascii=False, indent=2)

    print(f"[OK] Saved → {output_path}", file=sys.stderr)
    print(f"     Articles: {intel['article_count']} | Facts: {len(intel['key_facts'])} | "
          f"Signals: {len(intel['signals'])}", file=sys.stderr)


if __name__ == "__main__":
    main()
