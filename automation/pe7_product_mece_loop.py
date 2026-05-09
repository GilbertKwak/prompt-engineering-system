#!/usr/bin/env python3
"""
pe7_product_mece_loop.py — PE-7 Product Idea → MECE 자동분석 루프
Version : 1.0 | Date: 2026-05-09
Author  : Gilbert

Pipeline:
  Notion Product Ideas DB 폴링
    → MECE Status == '⏳ 대기중' 레코드 감지
    → PE-PROD-ORCH 프롬프트 조합
    → OpenAI API 호출 (gpt-4o)
    → 분석 초안 Notion 하위 페이지 생성
    → DB 레코드 상태 업데이트 (✅ 완료 / ❌ 오류)
    → GitHub Issue 등록 (선택)

Usage:
  python pe7_product_mece_loop.py                  # 폴링 1회
  python pe7_product_mece_loop.py --watch           # 60초 간격 반복 폴링
  python pe7_product_mece_loop.py --dry-run         # API 호출 없이 시뮬레이션
  python pe7_product_mece_loop.py --record-id <id>  # 특정 레코드만 처리

Env vars required:
  NOTION_TOKEN      — Notion Integration Token
  OPENAI_API_KEY    — OpenAI API Key
  GITHUB_TOKEN      — (선택) GitHub Issue 등록용
  NOTION_DB_ID      — Product Ideas DB ID
                      (기본: e34f78c6-d1df-4575-8a2f-a45d716c593e)
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

# ── 환경변수 ─────────────────────────────────────────────────────────────────
NOTION_TOKEN  = os.environ.get("NOTION_TOKEN", "")
OPENAI_KEY    = os.environ.get("OPENAI_API_KEY", "")
GITHUB_TOKEN  = os.environ.get("GITHUB_TOKEN", "")
DB_ID         = os.environ.get("NOTION_DB_ID",
                               "e34f78c6-d1df-4575-8a2f-a45d716c593e")
GH_REPO       = os.environ.get("GITHUB_REPO",
                               "GilbertKwak/prompt-engineering-system")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL_SEC", "60"))

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

# ── MECE 분석 프롬프트 템플릿 (PE-PROD-ORCH v1.0) ────────────────────────────
SYSTEM_PROMPT = """당신은 McKinsey/BCG급 신사업 기획 전문가이자 MECE 분석 AI입니다.
PE-PROD-ORCH v1.0 파이프라인을 실행합니다.
Temperature: 0.1 (구조 설계) / 출력 포맷은 반드시 아래 표준 템플릿을 따릅니다."""

USER_PROMPT_TEMPLATE = """PE-PROD-ORCH v1.0 전체 파이프라인을 실행해줘.

분석 대상  : {idea_name}
주체 유형  : {actor_type}
도메인     : {domain}
분석 깊이  : {depth}
목표 IRR   : {target_irr}
PE-FIN 연동: Yes

---

## 출력 표준 포맷 (반드시 준수)

===========================================
📦 {idea_name} — PE-PROD 표준 분석 보고서
분석일: {today} | 버전: v1.0
PE-PROD-ORCH | 분석 모드: {depth}
===========================================

[1/5] MECE 기회 공간 맵 (Layer A~E)
- Layer A (고객): ...
- Layer B (문제): ...
- Layer C (솔루션): ...
- Layer D (수익): ...
- Layer E (경쟁): ...

[2/5] 시장 규모 (TAM/SAM/SOM)
- TAM: $___B (출처: ___)
- SAM: $___B
- SOM (3년): $___M

[3/5] 기술 실현가능성 (TRL ___/9)
- 핵심 기술 리스크 Top 3
- 개발 로드맵 (Phase 1~3)

[4/5] 재무 모델 (목표 IRR: {target_irr})
- Unit Economics: ASP / CM% / LTV:CAC / Payback
- IRR 역산: 필요 Year-5 FCF $___M
- 3-시나리오: Bull/Base/Bear

[5/5] PE-3 검증 결과
- 점수: __/100
- 연계 권고: [PE-STRAT / PE-FIN / PE-SEMI / PE-AI]

📌 핵심 결론 (3문장)
🔗 연계 라이브러리 권고: [...]
=========================================== """


# ── Notion API 헬퍼 ──────────────────────────────────────────────────────────

def notion_query_pending(dry_run: bool = False) -> list[dict]:
    """MECE Status == '⏳ 대기중' 레코드 조회."""
    url = f"https://api.notion.com/v1/databases/{DB_ID}/query"
    payload = {
        "filter": {
            "property": "MECE Status",
            "select": {"equals": "⏳ 대기중"}
        },
        "sorts": [{"property": "Created", "direction": "ascending"}]
    }
    if dry_run:
        print("[DRY-RUN] Notion 쿼리 시뮬레이션 — 실제 API 미호출")
        return []
    resp = requests.post(url, headers=NOTION_HEADERS, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json().get("results", [])


def notion_update_status(page_id: str, status: str,
                         pe3_score: float = None,
                         irr_result: float = None,
                         tam: str = None,
                         key_insight: str = None,
                         draft_url: str = None,
                         cross_libs: list = None) -> None:
    """레코드 상태 및 분석 결과 필드 업데이트."""
    props = {
        "MECE Status": {"select": {"name": status}}
    }
    if pe3_score is not None:
        props["PE3 Score"] = {"number": pe3_score}
    if irr_result is not None:
        props["IRR Result"] = {"number": irr_result}
    if tam:
        props["TAM"] = {"rich_text": [{"text": {"content": tam[:2000]}}]}
    if key_insight:
        props["Key Insight"] = {"rich_text": [{"text": {"content": key_insight[:2000]}}]}
    if draft_url:
        props["Notion Draft URL"] = {"url": draft_url}
    if cross_libs:
        props["Cross Library"] = {"multi_select": [{"name": lib} for lib in cross_libs]}

    url = f"https://api.notion.com/v1/pages/{page_id}"
    resp = requests.patch(url, headers=NOTION_HEADERS,
                          json={"properties": props}, timeout=15)
    resp.raise_for_status()


def notion_create_draft_page(parent_page_id: str, idea_name: str,
                              analysis_md: str) -> str:
    """분석 초안을 Notion 하위 페이지로 생성 후 URL 반환."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    payload = {
        "parent": {"page_id": parent_page_id},
        "properties": {
            "title": {
                "title": [{"text": {"content": f"[PE-PROD] {idea_name} 초안 {today}"}}]
            }
        },
        "children": [{
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": analysis_md[:2000]}}]
            }
        }]
    }
    resp = requests.post("https://api.notion.com/v1/pages",
                         headers=NOTION_HEADERS, json=payload, timeout=20)
    resp.raise_for_status()
    page_id = resp.json()["id"]
    return f"https://www.notion.so/{page_id.replace('-', '')}"


# ── OpenAI API 호출 ──────────────────────────────────────────────────────────

def call_openai(user_prompt: str, dry_run: bool = False) -> str:
    """gpt-4o로 PE-PROD-ORCH 분석 실행."""
    if dry_run:
        return f"[DRY-RUN 시뮬레이션 출력]\n\n{user_prompt[:200]}..."

    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o",
            "temperature": 0.1,
            "max_tokens": 4000,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ],
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


# ── 분석 결과 파싱 ────────────────────────────────────────────────────────────

def parse_analysis(text: str) -> dict:
    """분석 텍스트에서 주요 수치 추출."""
    import re
    result = {"pe3_score": None, "irr": None, "tam": None,
              "key_insight": None, "cross_libs": []}

    # PE-3 점수
    m = re.search(r"점수[:\s]*([\d\.]+)/100", text)
    if m:
        result["pe3_score"] = float(m.group(1))

    # IRR
    m = re.search(r"IRR[:\s]*([\d\.]+)%", text)
    if m:
        result["irr"] = float(m.group(1))

    # TAM
    m = re.search(r"TAM[:\s]*\$([\d\.]+[BMT]?[^\n]*)", text)
    if m:
        result["tam"] = f"${m.group(1).strip()}"

    # 핵심 결론 (📌 이후 첫 문장)
    m = re.search(r"📌 핵심 결론.*?\n([^\n]+)", text, re.DOTALL)
    if m:
        result["key_insight"] = m.group(1).strip()

    # 연계 라이브러리
    for lib in ["PE-STRAT", "PE-FIN", "PE-SEMI", "PE-AI", "PE-DD"]:
        if lib in text:
            result["cross_libs"].append(lib)

    return result


# ── GitHub Issue 등록 ────────────────────────────────────────────────────────

def create_github_issue(idea_name: str, notion_url: str,
                        pe3_score: float, dry_run: bool = False) -> None:
    if not GITHUB_TOKEN or dry_run:
        return
    body = (
        f"**PE-PROD-ORCH 자동분석 완료**\n\n"
        f"- 아이디어: {idea_name}\n"
        f"- PE-3 점수: {pe3_score}/100\n"
        f"- Notion 초안: {notion_url}\n\n"
        f"자동 생성 by PE-7 루프 ({datetime.now().strftime('%Y-%m-%d %H:%M KST')})"
    )
    owner, repo = GH_REPO.split("/")
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    requests.post(
        url,
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}",
                 "Accept": "application/vnd.github+json"},
        json={"title": f"[PE-PROD] {idea_name} 분석 완료",
              "body": body,
              "labels": ["PE-PROD", "auto-analysis"]},
        timeout=15,
    )


# ── 레코드 단건 처리 ─────────────────────────────────────────────────────────

def process_record(record: dict, dry_run: bool = False) -> dict:
    props     = record["properties"]
    page_id   = record["id"]
    today     = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 필드 추출 헬퍼
    def get_select(key):  return (props.get(key, {}).get("select") or {}).get("name", "범용")
    def get_title(key):   return "".join(t["plain_text"] for t in props.get(key, {}).get("title", []))

    idea_name   = get_title("Idea Name") or "(무제)"
    domain      = get_select("Domain")
    actor_type  = get_select("Actor Type")
    depth       = get_select("Analysis Depth") or "Standard"
    target_irr  = get_select("Target IRR") or "20%"

    print(f"\n🔍 처리 중: [{idea_name}] | {domain} | {depth} | IRR {target_irr}")

    # 1) 상태 → 분석중
    if not dry_run:
        notion_update_status(page_id, "🔄 분석중")

    # 2) 프롬프트 조합
    user_prompt = USER_PROMPT_TEMPLATE.format(
        idea_name=idea_name, actor_type=actor_type, domain=domain,
        depth=depth, target_irr=target_irr, today=today
    )

    # 3) OpenAI 호출
    try:
        analysis_text = call_openai(user_prompt, dry_run=dry_run)
    except Exception as e:
        print(f"  ❌ OpenAI 오류: {e}")
        if not dry_run:
            notion_update_status(page_id, "❌ 오류")
        return {"idea": idea_name, "status": "error", "error": str(e)}

    # 4) 결과 파싱
    parsed = parse_analysis(analysis_text)

    # 5) Notion 초안 페이지 생성
    draft_url = ""
    if not dry_run:
        try:
            draft_url = notion_create_draft_page(page_id, idea_name, analysis_text)
            print(f"  📄 초안 페이지: {draft_url}")
        except Exception as e:
            print(f"  ⚠️  초안 페이지 생성 실패: {e}")

    # 6) DB 레코드 최종 업데이트
    if not dry_run:
        notion_update_status(
            page_id, "✅ 완료",
            pe3_score=parsed["pe3_score"],
            irr_result=parsed["irr"],
            tam=parsed["tam"],
            key_insight=parsed["key_insight"],
            draft_url=draft_url,
            cross_libs=parsed["cross_libs"],
        )

    # 7) GitHub Issue 등록
    create_github_issue(idea_name, draft_url,
                        parsed["pe3_score"] or 0, dry_run=dry_run)

    print(f"  ✅ 완료 | PE-3: {parsed['pe3_score']} | IRR: {parsed['irr']}%")
    return {"idea": idea_name, "status": "done", "parsed": parsed}


# ── 메인 폴링 루프 ────────────────────────────────────────────────────────────

def run_once(dry_run: bool = False, record_id: str = None) -> list[dict]:
    results = []
    if record_id:
        url  = f"https://api.notion.com/v1/pages/{record_id}"
        resp = requests.get(url, headers=NOTION_HEADERS, timeout=15)
        resp.raise_for_status()
        records = [resp.json()]
    else:
        records = notion_query_pending(dry_run=dry_run)

    if not records:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 대기 중인 아이디어 없음")
        return []

    print(f"[{datetime.now().strftime('%H:%M:%S')}] {len(records)}건 감지")
    for rec in records:
        res = process_record(rec, dry_run=dry_run)
        results.append(res)
        time.sleep(2)  # rate-limit 방지
    return results


def main():
    parser = argparse.ArgumentParser(description="PE-7 Product Idea → MECE 자동분석 루프")
    parser.add_argument("--watch",     action="store_true", help="반복 폴링 모드")
    parser.add_argument("--dry-run",   action="store_true", help="시뮬레이션 (API 미호출)")
    parser.add_argument("--record-id", help="특정 Notion 페이지 ID만 처리")
    parser.add_argument("--output",    help="결과 JSON 저장 경로")
    args = parser.parse_args()

    if not NOTION_TOKEN and not args.dry_run:
        print("❌ NOTION_TOKEN 환경변수 미설정"); sys.exit(1)
    if not OPENAI_KEY and not args.dry_run:
        print("❌ OPENAI_API_KEY 환경변수 미설정"); sys.exit(1)

    print("🚀 PE-7 Product Idea → MECE 자동분석 루프 시작")
    print(f"   DB ID      : {DB_ID}")
    print(f"   Dry-Run    : {args.dry_run}")
    print(f"   Watch 모드 : {args.watch}")

    all_results = []
    try:
        if args.watch:
            while True:
                results = run_once(dry_run=args.dry_run, record_id=args.record_id)
                all_results.extend(results)
                print(f"  ⏱  {POLL_INTERVAL}초 후 재폴링...")
                time.sleep(POLL_INTERVAL)
        else:
            all_results = run_once(dry_run=args.dry_run, record_id=args.record_id)
    except KeyboardInterrupt:
        print("\n🛑 루프 중단")

    if args.output and all_results:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        print(f"📄 결과 저장: {args.output}")

    failed = [r for r in all_results if r.get("status") == "error"]
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
