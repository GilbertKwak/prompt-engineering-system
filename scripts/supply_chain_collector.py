#!/usr/bin/env python3
"""Track B-1: RSS/Web → LLM 요약 공급망 수집기
PE-7 v2.0 | E-05 timeout, E-08 encoding | Gilbert Kwak 2026-04-26"""
import os, json, time, feedparser, requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd

os.makedirs("data", exist_ok=True)
os.makedirs("logs", exist_ok=True)

OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")
TODAY  = datetime.now()
CUTOFF = TODAY - timedelta(days=7)

RSS_FEEDS = {
    "SemiAnalysis":  "https://semianalysis.com/feed",
    "EETimes":       "https://www.eetimes.com/feed",
    "IEEE Spectrum": "https://spectrum.ieee.org/feeds/topic/semiconductors.rss",
    "DigiTimes SC":  "https://www.digitimes.com/rss/supply-chain.xml",
}
KEYWORDS = ["CoWoS", "HBM", "HBM3E", "TSMC", "packaging",
            "supply chain", "OSAT", "chiplet", "SK Hynix",
            "Samsung", "Intel Foundry", "SMIC"]

# ── E-08: 인코딩 안전화 ────────────────────────────────────────────────────────
def safe_text(text: str) -> str:
    if not text: return ""
    try:    return text.encode("utf-8", errors="replace").decode("utf-8")
    except: return ""

# ── RSS 수집 ──────────────────────────────────────────────────────────────────
def collect_rss(feeds: dict) -> list[dict]:
    articles = []
    for source, url in feeds.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:20]:
                pub  = entry.get("published", "")
                title   = safe_text(entry.get("title", ""))
                summary = safe_text(entry.get("summary", ""))
                link    = entry.get("link", "")
                combined = (title + " " + summary).lower()
                if not any(kw.lower() in combined for kw in KEYWORDS):
                    continue
                articles.append({
                    "source":   source,
                    "title":    title,
                    "summary":  summary[:500],
                    "url":      link,
                    "date":     pub[:10],
                    "keywords": [kw for kw in KEYWORDS if kw.lower() in combined],
                })
        except Exception as e:
            print(f"[E-05] {source} RSS 오류: {e}")
    return articles

# ── LLM 요약 (배치) ───────────────────────────────────────────────────────────
def llm_summarize_batch(articles: list[dict]) -> list[dict]:
    if not OPENAI_KEY:
        print("[SKIP] OPENAI_API_KEY 미설정 — LLM 요약 건너뜀")
        return articles
    headers = {"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"}
    for i, art in enumerate(articles):
        prompt = (
            f"반도체 공급망 뉴스를 한국어 3줄로 요약하고 영향도를 평가하라.\n"
            f"제목: {art['title']}\n내용: {art['summary']}\n"
            f"JSON: {{\"summary_ko\": str, \"impact\": \"high|medium|low\", \"companies\": list}}"
        )
        try:
            res = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}], "max_tokens": 200},
                timeout=15,
            )
            res.raise_for_status()
            parsed = json.loads(res.json()["choices"][0]["message"]["content"])
            articles[i].update(parsed)
        except Exception as e:
            print(f"[E-05] LLM 오류 항목 {i}: {e}")
            articles[i]["summary_ko"] = articles[i]["summary"][:200]
            articles[i]["impact"]     = "medium"
        time.sleep(0.5)
    return articles

# ── main ──────────────────────────────────────────────────────────────────────
def main():
    print("[Track B-1] 공급망 수집 시작 ...")
    articles = collect_rss(RSS_FEEDS)
    print(f"[OK] {len(articles)}건 수집")
    if articles:
        articles = llm_summarize_batch(articles)
    df = pd.DataFrame(articles)
    today_str = datetime.now().strftime("%Y%m%d")
    csv_path  = f"data/supply_chain_{today_str}.csv"
    json_path = f"data/supply_chain_{today_str}.json"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"[OK] {csv_path}")
    if "impact" in df.columns:
        for level in ["high", "medium", "low"]:
            print(f"  Impact {level.upper()}: {len(df[df['impact']==level])}건")

if __name__ == "__main__":
    main()
