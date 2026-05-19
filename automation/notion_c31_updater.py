#!/usr/bin/env python3
"""
notion_c31_updater.py — Notion C-31 Page Updater

AI Intel Weekly 결과를 Notion C-31 페이지에 append 방식으로 업데이트합니다.
- Notion Blocks API append (기존 내용 보존)
- 50블록 배치 처리
- EW 심각도별 callout 배경색 (red/yellow/green)
- 인텔 파일에서 섹션별 요약 자동 구성
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("[ERROR] requests 패키지 필요: pip install requests", file=sys.stderr)
    sys.exit(1)

NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
BATCH_SIZE = 50

# EW 심각도 → callout 색상 매핑
EW_COLORS = {
    "EW": "red_background",
    "WATCH": "yellow_background",
    "NONE": "green_background",
}


def notion_headers(api_key: str) -> dict:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }


def rich_text(content: str, bold: bool = False, color: str = "default") -> dict:
    """Notion rich_text 객체 생성."""
    return {
        "type": "text",
        "text": {"content": content[:2000]},  # Notion 2000자 제한
        "annotations": {
            "bold": bold,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": False,
            "color": color,
        },
    }


def make_divider() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


def make_heading(text: str, level: int = 2) -> dict:
    htype = f"heading_{max(1, min(3, level))}"
    return {
        "object": "block",
        "type": htype,
        htype: {"rich_text": [rich_text(text, bold=True)]},
    }


def make_paragraph(text: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [rich_text(text)]},
    }


def make_callout(text: str, emoji: str, color: str) -> dict:
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [rich_text(text)],
            "icon": {"type": "emoji", "emoji": emoji},
            "color": color,
        },
    }


def make_bullet(text: str) -> dict:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [rich_text(text)]},
    }


def make_toggle(title: str, children: list) -> dict:
    return {
        "object": "block",
        "type": "toggle",
        "toggle": {
            "rich_text": [rich_text(title, bold=True)],
            "children": children[:99],
        },
    }


def append_blocks(page_id: str, blocks: list, api_key: str) -> bool:
    """blocks를 BATCH_SIZE 단위로 나눠 append. rate limit 대응 포함."""
    url = f"{NOTION_API_BASE}/blocks/{page_id}/children"
    headers = notion_headers(api_key)
    total = len(blocks)
    sent = 0

    for i in range(0, total, BATCH_SIZE):
        batch = blocks[i:i + BATCH_SIZE]
        for attempt in range(3):
            try:
                resp = requests.patch(url, headers=headers, json={"children": batch}, timeout=30)
                if resp.status_code == 200:
                    sent += len(batch)
                    break
                elif resp.status_code == 429:
                    retry_after = int(resp.headers.get("Retry-After", 2))
                    print(f"[WARN] Rate limit, retrying in {retry_after}s...", file=sys.stderr)
                    time.sleep(retry_after)
                elif resp.status_code == 400:
                    print(f"[ERROR] Bad request: {resp.text[:300]}", file=sys.stderr)
                    # 블록 하나씩 개별 전송 시도
                    for single_block in batch:
                        try:
                            r2 = requests.patch(
                                url, headers=headers,
                                json={"children": [single_block]}, timeout=20
                            )
                            if r2.status_code == 200:
                                sent += 1
                        except Exception:
                            pass
                    break
                else:
                    print(f"[ERROR] HTTP {resp.status_code}: {resp.text[:300]}", file=sys.stderr)
                    if attempt == 2:
                        return False
                    time.sleep(2)
            except requests.RequestException as e:
                print(f"[ERROR] Request failed: {e}", file=sys.stderr)
                if attempt == 2:
                    return False
                time.sleep(2)

        time.sleep(0.4)  # API 호출 간 최소 간격

    print(f"[Notion] Appended {sent}/{total} blocks")
    return sent > 0


def load_intel_summary(intel_dir: str) -> list[dict]:
    """인텔 디렉토리에서 도메인별 요약 로드."""
    base = Path(intel_dir)
    summaries = []
    if not base.exists():
        return summaries

    for fp in sorted(base.glob("*.json")):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        items = data if isinstance(data, list) else [data]
        for item in items:
            domain = item.get("domain", item.get("topic", fp.stem))
            key_facts = item.get("key_facts", [])
            if isinstance(key_facts, str):
                key_facts = [key_facts]
            summary_text = item.get("summary", item.get("analysis", ""))
            summaries.append({
                "domain": domain,
                "key_facts": key_facts[:5],
                "summary": summary_text[:500] if summary_text else "",
            })
    return summaries


def build_blocks(
    week: str,
    run_date: str,
    ew_triggered: bool,
    ew_count: int,
    ew_signals: list[str],
    ew_severity: str,
    kg_version: str,
    node_count: int,
    edge_count: int,
    intel_summaries: list[dict],
) -> list:
    """Notion 블록 리스트 구성."""
    blocks = []
    run_dt = run_date or datetime.utcnow().strftime("%Y-%m-%d")

    # ── 헤더
    blocks.append(make_divider())
    blocks.append(make_heading(f"📡 AI Intel Weekly — {week}  ({run_dt})", level=2))

    # ── EW 상태 callout
    ew_color = EW_COLORS.get(ew_severity, "green_background")
    if ew_triggered:
        ew_emoji = "🚨"
        ew_msg = (
            f"Early Warning 발동!  Severity={ew_severity}  |  "
            f"{ew_count}개 시그널 탐지\n"
            + ("Signals: " + ", ".join(ew_signals[:5]) if ew_signals else "")
        )
    else:
        ew_emoji = "✅"
        ew_msg = f"EW 없음  |  Severity={ew_severity}  |  정상 범위"

    blocks.append(make_callout(ew_msg, ew_emoji, ew_color))

    # ── KG 업데이트 요약
    blocks.append(make_heading("🗺️ Knowledge Graph Update", level=3))
    blocks.append(make_paragraph(
        f"버전: → v{kg_version}  |  "
        f"신규 노드: +{node_count}  |  신규 엣지: +{edge_count}"
    ))

    # ── 도메인별 인텔 요약
    if intel_summaries:
        blocks.append(make_heading("📊 Domain Intelligence Summary", level=3))
        for s in intel_summaries[:8]:  # 최대 8개 도메인
            domain_label = s["domain"].replace("_", " ").title()
            summary_text = s.get("summary", "")

            domain_children = []
            if summary_text:
                domain_children.append(make_paragraph(summary_text[:300]))

            for fact in s.get("key_facts", [])[:4]:
                if str(fact).strip():
                    domain_children.append(make_bullet(str(fact)[:200]))

            if domain_children:
                blocks.append(make_toggle(f"▸ {domain_label}", domain_children))
            else:
                blocks.append(make_bullet(f"{domain_label}: 수집 데이터 없음"))

    # ── EW 시그널 상세 (발동 시)
    if ew_triggered and ew_signals:
        blocks.append(make_heading("⚡ EW Signal Details", level=3))
        for sig in ew_signals[:5]:
            blocks.append(make_bullet(f"• {sig}"))

    # ── 메타데이터
    blocks.append(make_divider())
    blocks.append(make_paragraph(
        f"Generated: {datetime.utcnow().isoformat()}Z  |  "
        f"Script: notion_c31_updater.py v2.0"
    ))

    return blocks


def main():
    parser = argparse.ArgumentParser(description="Notion C-31 Page Updater")
    parser.add_argument("--page-id", required=True, help="Notion 페이지 ID (dash 없이도 OK)")
    parser.add_argument("--week", required=True, help="ISO 주차 (예: 2026-W21)")
    parser.add_argument("--run-date", default=datetime.utcnow().strftime("%Y-%m-%d"),
                        help="실행 날짜")
    parser.add_argument("--ew-triggered", default="false",
                        help="EW 발동 여부 (true/false)")
    parser.add_argument("--ew-count", type=int, default=0, help="EW 시그널 수")
    parser.add_argument("--ew-signals", default="",
                        help="콤마 구분 EW 시그널 문자열")
    parser.add_argument("--ew-severity", default="NONE",
                        choices=["NONE", "WATCH", "EW"],
                        help="EW 심각도")
    parser.add_argument("--kg-version", default="4.26", help="새 KG 버전")
    parser.add_argument("--node-count", type=int, default=0, help="추가 노드 수")
    parser.add_argument("--edge-count", type=int, default=0, help="추가 엣지 수")
    parser.add_argument("--intel-dir", default="output/ai_intel",
                        help="인텔 JSON 파일 디렉토리")
    args = parser.parse_args()

    api_key = os.environ.get("NOTION_API_KEY", "")
    if not api_key:
        print("[ERROR] NOTION_API_KEY 환경변수 미설정", file=sys.stderr)
        sys.exit(1)

    # 파라미터 파싱
    ew_triggered = args.ew_triggered.lower() == "true"
    ew_signals = [s.strip() for s in args.ew_signals.split(",") if s.strip()]

    # 인텔 요약 로드
    intel_summaries = load_intel_summary(args.intel_dir)

    # 블록 생성
    blocks = build_blocks(
        week=args.week,
        run_date=args.run_date,
        ew_triggered=ew_triggered,
        ew_count=args.ew_count,
        ew_signals=ew_signals,
        ew_severity=args.ew_severity,
        kg_version=args.kg_version,
        node_count=args.node_count,
        edge_count=args.edge_count,
        intel_summaries=intel_summaries,
    )

    print(f"[Notion] Preparing {len(blocks)} blocks for page {args.page_id}")

    # page_id 정규화 (dash 포맷 맞추기)
    page_id = args.page_id.replace("-", "")
    if len(page_id) == 32:
        page_id = (
            f"{page_id[:8]}-{page_id[8:12]}-{page_id[12:16]}-"
            f"{page_id[16:20]}-{page_id[20:]}"
        )

    success = append_blocks(page_id, blocks, api_key)
    if success:
        print(f"[OK] Notion C-31 업데이트 완료: {args.week}")
        sys.exit(0)
    else:
        print(f"[FAIL] Notion 업데이트 실패", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
