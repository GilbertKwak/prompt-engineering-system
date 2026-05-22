"""
EW-GEO-01 Monitor  v1.0
========================
지정학적 리스크 얼리워닝 모니터 — 반도체 공급망 영향 분석

Trigger 대상:
  - 미·중 갈등 / 수출규제 신호
  - 대만 해협 군사·정치 동향
  - TSMC / 삼성 / SK하이닉스 공급망 리스크
  - HBM / 첨단 패키징 수출 제한
  - 한일 소재·장비 공급망 이슈

Outputs:
  - output/ew_geo01_YYYYMMDD_HHMM.json
  - Notion EW DB 업데이트 (NOTION_TOKEN 설정 시)

Schedule: 6시간마다 (GitHub Actions cron)
"""

import os
import json
import datetime
import sys

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: openai 패키지 미설치. pip install openai")
    sys.exit(1)

try:
    from notion_client import Client as NotionClient
    NOTION_AVAILABLE = True
except ImportError:
    NOTION_AVAILABLE = False

# ─── Config ───────────────────────────────────────────────────────────────────
OPENAI_API_KEY  = os.environ.get("OPENAI_API_KEY", "")
NOTION_TOKEN    = os.environ.get("NOTION_TOKEN", "")
NOTION_EW_DB_ID = os.environ.get("NOTION_EW_DB_ID", "")
DEBUG_MODE      = os.environ.get("DEBUG_MODE", "false").lower() == "true"
OUTPUT_DIR      = "output"

if not OPENAI_API_KEY:
    print("ERROR: OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
    sys.exit(1)

# 모니터링 대상 지정학 이슈
GEO_WATCH_ITEMS = [
    "US China semiconductor export controls latest developments",
    "Taiwan Strait military activity semiconductor supply risk",
    "TSMC supply chain disruption geopolitical risk",
    "South Korea Japan semiconductor materials equipment supply",
    "HBM advanced packaging export restrictions",
]

TRIGGER_THRESHOLD = 7   # 0-10 스케일, 이상이면 HIGH ALERT


# ─── OpenAI 분석 ──────────────────────────────────────────────────────────────
def analyze_geo_risk(item: str, client: OpenAI) -> dict:
    """GPT-4o로 지정학 리스크 분석 후 구조화된 JSON 반환"""

    prompt = f"""당신은 반도체 공급망 지정학 리스크 전문 분석가입니다.
아래 이슈에 대해 2026년 현재 시점 기준으로 분석하세요.

이슈: {item}

반드시 아래 JSON 형식으로만 응답하세요 (다른 텍스트 금지):
{{
  "issue": "{item}",
  "risk_score": <0-10 정수, 10=최고위험>,
  "status": "<LOW|MEDIUM|HIGH|CRITICAL>",
  "summary_ko": "<한국어 요약 2-3문장. 구체적 국가/기업명 포함>",
  "summary_en": "<English summary 1-2 sentences>",
  "affected_players": ["<영향 받는 기업 또는 국가 목록>"],
  "semiconductor_impact": "<HBM/로직칩/파운드리/소재/장비/AI칩 중 주요 영향 영역>",
  "timeline": "<단기(1-3개월)/중기(3-12개월)/장기(1년+) 중 예상 영향 기간>",
  "recommended_action": "<반도체 투자자/전략가를 위한 구체적 모니터링 권고사항>"
}}"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.3,
        max_tokens=800,
    )

    result = json.loads(response.choices[0].message.content)
    result["analyzed_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    result["model"] = "gpt-4o"
    result["trigger_id"] = "EW-GEO-01"
    return result


# ─── Notion 업데이트 ──────────────────────────────────────────────────────────
def push_to_notion(result: dict, notion: NotionClient) -> bool:
    """분석 결과를 Notion EW DB에 기록"""
    if not NOTION_EW_DB_ID:
        if DEBUG_MODE:
            print(f"    ℹ NOTION_EW_DB_ID 미설정 — Notion 업데이트 스킵")
        return False

    try:
        notion.pages.create(
            parent={"database_id": NOTION_EW_DB_ID},
            properties={
                "Name": {
                    "title": [{"text": {"content": f"EW-GEO-01 | {result['issue'][:60]}"}}]
                },
                "Status": {"select": {"name": result.get("status", "MEDIUM")}},
                "Score":  {"number": result.get("risk_score", 0)},
                "Date":   {"date": {"start": result["analyzed_at"][:10]}},
            },
            children=[
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "📊 분석 요약"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": result.get("summary_ko", "")}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {"type": "text", "text": {"content": f"🎯 반도체 영향: {result.get('semiconductor_impact', 'N/A')}\n"}},
                            {"type": "text", "text": {"content": f"⏱ 영향 기간: {result.get('timeline', 'N/A')}\n"}},
                            {"type": "text", "text": {"content": f"💡 권고사항: {result.get('recommended_action', 'N/A')}"}},
                        ]
                    }
                },
            ]
        )
        print(f"    ✅ Notion 업데이트: {result['issue'][:50]}")
        return True
    except Exception as e:
        print(f"    ⚠ Notion 업데이트 실패: {e}")
        return False


# ─── 메인 ─────────────────────────────────────────────────────────────────────
def main():
    run_ts = datetime.datetime.utcnow()
    print("=" * 65)
    print(f"  EW-GEO-01 Monitor  |  {run_ts.strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"  DEBUG: {DEBUG_MODE}  |  Notion: {'✅' if NOTION_TOKEN and NOTION_AVAILABLE else '❌'}")
    print("=" * 65)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    client = OpenAI(api_key=OPENAI_API_KEY)
    notion = NotionClient(auth=NOTION_TOKEN) if (NOTION_TOKEN and NOTION_AVAILABLE) else None

    results = []
    alerts  = []
    errors  = []

    for i, item in enumerate(GEO_WATCH_ITEMS, 1):
        print(f"\n[{i}/{len(GEO_WATCH_ITEMS)}] 🔍 {item}")
        try:
            result = analyze_geo_risk(item, client)
            results.append(result)

            score  = result.get("risk_score", 0)
            status = result.get("status", "UNKNOWN")

            # 상태 아이콘
            icon = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🟠", "CRITICAL": "🔴"}.get(status, "⚪")
            print(f"    {icon} Score: {score}/10  |  Status: {status}")
            print(f"    📝 {result.get('summary_ko', '')[:100]}...")
            print(f"    🏭 영향: {result.get('semiconductor_impact', 'N/A')}")

            if score >= TRIGGER_THRESHOLD:
                alerts.append(result)
                print(f"    🚨 ALERT TRIGGERED (score={score} >= threshold={TRIGGER_THRESHOLD})")

            if notion:
                push_to_notion(result, notion)

        except Exception as e:
            error_msg = f"분석 실패 [{item[:40]}]: {str(e)}"
            print(f"    ❌ {error_msg}")
            errors.append({"item": item, "error": str(e)})

    # ─── 리포트 저장 ─────────────────────────────────────────────────────────
    ts = run_ts.strftime("%Y%m%d_%H%M")
    report_path = f"{OUTPUT_DIR}/ew_geo01_{ts}.json"

    report = {
        "trigger_id":   "EW-GEO-01",
        "trigger_name": "Geopolitical Risk Monitor",
        "run_at":       run_ts.isoformat() + "Z",
        "total":        len(results),
        "alerts":       len(alerts),
        "errors":       len(errors),
        "threshold":    TRIGGER_THRESHOLD,
        "results":      results,
        "high_risk":    alerts,
        "error_log":    errors,
    }

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # ─── 최종 요약 출력 ──────────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print(f"  📊 분석 완료")
    print(f"     총 분석: {len(results)}건  |  알림: {len(alerts)}건  |  오류: {len(errors)}건")
    print(f"     리포트: {report_path}")

    if alerts:
        print(f"\n  🚨 HIGH RISK 항목:")
        for a in alerts:
            print(f"     - [{a.get('status')} {a.get('risk_score')}/10] {a.get('issue')[:60]}")

    print("=" * 65)

    # CRITICAL 감지 시 exit code 1 → GitHub Actions에서 경고 표시
    if any(r.get("status") == "CRITICAL" for r in results):
        print("\n🔴 CRITICAL 상태 감지 — 즉시 검토 필요!")
        sys.exit(1)


if __name__ == "__main__":
    main()
