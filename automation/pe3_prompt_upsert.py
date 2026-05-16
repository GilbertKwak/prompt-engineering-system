# ============================================================
# automation/pe3_prompt_upsert.py
# PE-7 파이프라인 통합용 — 최적화 프롬프트 → Notion PE-3 DB Upsert
# Version : 1.0 | Date: 2026-05-16
# ============================================================
from __future__ import annotations
import os
import sys
from datetime import date
from notion_client import Client
from notion_client.errors import APIResponseError

# ── 환경변수 ──────────────────────────────────────────────────
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
DB_ID        = os.environ.get("PE3_STRAT_DB_ID", "")

if not NOTION_TOKEN:
    print("❌ NOTION_TOKEN 미설정", file=sys.stderr)
    sys.exit(1)
if not DB_ID:
    print("❌ PE3_STRAT_DB_ID 미설정", file=sys.stderr)
    sys.exit(1)

notion = Client(auth=NOTION_TOKEN)

# ── Upsert 대상 프롬프트 목록 ─────────────────────────────────
TODAY = date.today().isoformat()  # 실행 시점 날짜 자동 적용

PROMPTS: list[dict] = [
    {
        "Name"         : "Porter_ValueChain_Sustainability_v4_OPT",
        "Domain"       : "PE-STRAT",
        "Version"      : "4.0",
        "Status"       : "Active",
        "LinkedHub"    : "PE-3",
        "LastValidated": TODAY,
    },
    {
        "Name"         : "Porter_ValueChain_B2B_SaaS_v5_OPT",
        "Domain"       : "PE-STRAT",
        "Version"      : "5.0",
        "Status"       : "Active",
        "LinkedHub"    : "PE-3",
        "LastValidated": TODAY,
    },
    {
        "Name"         : "SaaS_Competitive_Moat_Analyzer_v2_OPT",
        "Domain"       : "PE-STRAT",
        "Version"      : "2.0",
        "Status"       : "Active",
        "LinkedHub"    : "PE-7",
        "LastValidated": TODAY,
    },
]


def _build_properties(p: dict) -> dict:
    """Notion API properties 페이로드 빌드."""
    return {
        "Name": {
            "title": [{"text": {"content": p["Name"]}}]
        },
        "Domain": {
            "select": {"name": p["Domain"]}
        },
        "Version": {
            "rich_text": [{"text": {"content": p["Version"]}}]
        },
        "Status": {
            "select": {"name": p["Status"]}
        },
        "LinkedHub": {
            "rich_text": [{"text": {"content": p["LinkedHub"]}}]
        },
        "LastValidated": {
            "date": {"start": p["LastValidated"]}
        },
    }


def _find_existing_page(name: str) -> str | None:
    """DB 내 동일 Name 페이지 존재 여부 확인 → page_id 반환 (없으면 None)."""
    resp = notion.databases.query(
        database_id=DB_ID,
        filter={
            "property": "Name",
            "title": {"equals": name},
        },
    )
    results = resp.get("results", [])
    return results[0]["id"] if results else None


def upsert_prompt(p: dict) -> None:
    """Create or Update 단일 프롬프트 레코드."""
    properties = _build_properties(p)
    existing_id = _find_existing_page(p["Name"])

    try:
        if existing_id:
            notion.pages.update(
                page_id=existing_id,
                properties=properties,
            )
            print(f"🔄 Updated : {p['Name']} (id={existing_id[:8]}...)")
        else:
            notion.pages.create(
                parent={"database_id": DB_ID},
                properties=properties,
            )
            print(f"✅ Created : {p['Name']}")
    except APIResponseError as exc:
        print(f"❌ API Error [{p['Name']}]: {exc.status} — {exc.message}", file=sys.stderr)
        raise


if __name__ == "__main__":
    print(f"📋 Upsert 시작: {len(PROMPTS)}개 프롬프트 → PE-3 DB")
    errors = 0
    for prompt in PROMPTS:
        try:
            upsert_prompt(prompt)
        except Exception:
            errors += 1

    if errors:
        print(f"\n⚠️  {errors}개 레코드 실패 — 위 오류 메시지를 확인하세요", file=sys.stderr)
        sys.exit(1)

    print(f"\n🎉 완료: {len(PROMPTS) - errors}/{len(PROMPTS)}개 정상 처리")
