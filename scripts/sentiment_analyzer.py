#!/usr/bin/env python3
"""Track B-3: Reddit 감성분석 — FinBERT + VADER fallback
PE-7 v2.0 | E-05 Reddit 429 rate limit | Gilbert Kwak 2026-04-26"""
import os, json, time, pandas as pd
from datetime import datetime, timezone

os.makedirs("data", exist_ok=True)

REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID", "")
REDDIT_SECRET    = os.environ.get("REDDIT_SECRET", "")
REDDIT_UA        = "PE7-SentimentBot/2.0 by GilbertKwak"

TICKERS    = ["TSMC","Nvidia","NVDA","SK Hynix","Intel","ASML","HBM","CoWoS"]
SUBREDDITS = ["hardware","investing","stocks","semiconductors","SecurityAnalysis"]

# ── FinBERT 로드 ──────────────────────────────────────────────────────────────
def load_sentiment_model():
    try:
        from transformers import pipeline
        model = pipeline("sentiment-analysis", model="ProsusAI/finbert",
                         truncation=True, max_length=512)
        print("[OK] FinBERT 로드 완료")
        return model
    except Exception as e:
        print(f"[WARN] FinBERT 로드 실패: {e} — VADER fallback 사용")
        return None

# ── 데모 데이터 (Reddit API 미설정 시) ────────────────────────────────────────
def demo_reddit_data() -> list[dict]:
    return [
        {"subreddit":"hardware","title":"TSMC CoWoS capacity finally expanding in 2026",
         "text":"TSMC announced CoWoS capacity +40% vs 2025. Bullish for Nvidia.",
         "score":1240,"comments":89,"url":"","created":"2026-04-25",
         "tickers":["TSMC","Nvidia","CoWoS"]},
        {"subreddit":"investing","title":"SK Hynix HBM3E dominating — 53% market share",
         "text":"Samsung still struggling. Hynix quality advantage clear.",
         "score":876,"comments":54,"url":"","created":"2026-04-24",
         "tickers":["SK Hynix","HBM"]},
        {"subreddit":"semiconductors","title":"Intel 18A yield concerns remain — below 55%",
         "text":"Multiple fab sources confirm yield still lagging target.",
         "score":543,"comments":112,"url":"","created":"2026-04-23",
         "tickers":["Intel"]},
    ]

# ── Reddit 수집 ───────────────────────────────────────────────────────────────
def collect_reddit(subreddits: list, keywords: list, limit: int = 50) -> list[dict]:
    if not REDDIT_CLIENT_ID:
        print("[SKIP] REDDIT_CLIENT_ID 미설정 — 데모 데이터 사용")
        return demo_reddit_data()
    try:
        import praw
        reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_SECRET,
                             user_agent=REDDIT_UA, ratelimit_seconds=60)
    except Exception as e:
        print(f"[E-05] Reddit 초기화 오류: {e}")
        return demo_reddit_data()
    posts = []
    for sub in subreddits:
        try:
            subreddit = reddit.subreddit(sub)
            for post in subreddit.new(limit=limit):
                combined = f"{post.title} {post.selftext}"
                if not any(kw.lower() in combined.lower() for kw in keywords): continue
                posts.append({
                    "subreddit": sub, "title": post.title[:300],
                    "text": post.selftext[:500], "score": post.score,
                    "comments": post.num_comments,
                    "url": f"https://reddit.com{post.permalink}",
                    "created": datetime.fromtimestamp(post.created_utc, tz=timezone.utc).strftime("%Y-%m-%d"),
                    "tickers": [t for t in keywords if t.lower() in combined.lower()],
                })
            time.sleep(1)
        except Exception as e:
            print(f"[E-05] r/{sub} 오류: {e}")
    return posts

# ── 감성 분석 ─────────────────────────────────────────────────────────────────
def analyze_sentiment(posts: list[dict], model) -> list[dict]:
    for post in posts:
        text = f"{post['title']} {post.get('text', '')}"[:512]
        if model:
            try:
                result = model(text)[0]
                label = result["label"].lower()  # positive/negative/neutral
                score = round(result["score"], 4)
            except Exception:
                label, score = "neutral", 0.5
        else:
            import nltk
            from nltk.sentiment import SentimentIntensityAnalyzer
            nltk.download("vader_lexicon", quiet=True)
            sia      = SentimentIntensityAnalyzer()
            compound = sia.polarity_scores(text)["compound"]
            label    = "positive" if compound > 0.05 else "negative" if compound < -0.05 else "neutral"
            score    = abs(compound)
        post["sentiment"]      = label
        post["sentiment_score"] = score
        post["bullish_signal"]  = label == "positive" and score > 0.7
    return posts

# ── 티커별 집계 ───────────────────────────────────────────────────────────────
def aggregate_by_ticker(posts: list[dict]) -> pd.DataFrame:
    records = []
    for ticker in TICKERS:
        related = [p for p in posts if ticker in p.get("tickers", [])]
        if not related: continue
        total = len(related)
        pos   = sum(1 for p in related if p.get("sentiment") == "positive")
        neg   = sum(1 for p in related if p.get("sentiment") == "negative")
        records.append({
            "ticker":           ticker,
            "total_mentions":   total,
            "positive":         pos,
            "negative":         neg,
            "neutral":          total - pos - neg,
            "sentiment_score":  round(sum(p.get("sentiment_score", 0.5) for p in related) / max(total, 1), 3),
            "bullish_pct":      round(pos / max(total, 1) * 100, 1),
            "avg_reddit_score": round(sum(p.get("score", 0) for p in related) / max(total, 1), 0),
        })
    return pd.DataFrame(records).sort_values("bullish_pct", ascending=False)

# ── main ──────────────────────────────────────────────────────────────────────
def main():
    print("[Track B-3] 감성분석 시작 ...")
    model  = load_sentiment_model()
    posts  = collect_reddit(SUBREDDITS, TICKERS, limit=50)
    print(f"[OK] {len(posts)}건 수집")
    posts  = analyze_sentiment(posts, model)
    df_agg = aggregate_by_ticker(posts)
    today_str = datetime.now().strftime("%Y%m%d")
    df_agg.to_csv(f"data/sentiment_summary_{today_str}.csv", index=False)
    pd.DataFrame(posts).to_csv(f"data/sentiment_raw_{today_str}.csv", index=False)
    print("\n[집계 결과]")
    print(df_agg.to_string(index=False))

if __name__ == "__main__":
    main()
