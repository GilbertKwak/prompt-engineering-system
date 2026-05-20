#!/usr/bin/env python3
"""
notion_c31_updater.py  v3 — Section A · Step 4
Notion C-31 AI Intel Weekly 페이지 업데이트 + 주간 하위 페이지 자동 생성

변경사항 v3:
  - create_weekly_report(): C-31 하위 페이지 자동 생성 + EW/인텔 결과 주입
  - PARENT_PAGE_ID: C-31 페이지 ID 상수 정의
  - --create-page 플래그: 기존 페이지 append 대신 새 하위 페이지 생성 모드
  - 기존 v2 기능 (append, dry-run) 유지

Usage (기존 append 모드):
  python automation/notion_c31_updater.py \\
    --page-id 34a55ed436f0814d9cffe6a2f0816e29 \\
    --week 2026-W21 ...

Usage (새 하위 페이지 생성 모드):
  python automation/notion_c31_updater.py \\
    --create-page \\
    --week 2026-W22 \\
    --run-date 2026-05-25 \\
    --ew-triggered false \\
    --ew-count 0 --ew-signals "" --ew-severity NONE \\
    --kg-version 4.27 --node-count 5 --edge-count 3 \\
    --intel-dir output/ai_intel
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("[ERROR] requests 패키지 없음: pip install requests", file=sys.stderr)
    sys.exit(1)

NOTION_API_BASE    = "https://api.notion.com/v1"
NOTION_VERSION     = "2022-06-28"
MAX_BLOCKS_PER_REQ = 50   # Notion API 제한

# C-31 부모 페이지 ID (Weekly Report 하위 페이지 생성 기준)
PARENT_PAGE_ID = "35155ed4-36f0-81a5-87c9-f949d7aaabae"

# EW 심각도 → callout 색상 매핑
EW_COLOR_MAP = {
    "CRITICAL": "red",
    "WARNING":  "yellow",
    "WATCH":    "orange",
    "NONE":     "green",
}
EW_EMOJI_MAP = {
    "CRITICAL": "🚨",
    "WARNING":  "⚠️",
    "WATCH":    "👀",
    "NONE":     "✅",
}


# ─── Notion 유틸리티 ───────────────────────────────────────────────────────────
def get_notion_key() -> str:
    key = os.environ.get("NOTION_API_KEY", "").strip()
    if not key:
        print("[ERROR] NOTION_API_KEY 환경변수 미설정", file=sys.stderr)
        sys.exit(1)
    return key


def notion_headers(key: str) -> dict:
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type":  "application/json",
        "Notion-Version": NOTION_VERSION,
    }


def append_blocks(page_id: str, blocks: list, key: str) -> None:
    """블록 배치 append (50블록 청크 처리)"""
    for i in range(0, len(blocks), MAX_BLOCKS_PER_REQ):
        chunk = blocks[i:i + MAX_BLOCKS_PER_REQ]
        url = f"{NOTION_API_BASE}/blocks/{page_id}/children"
        resp = requests.patch(url, headers=notion_headers(key),
                              json={"children": chunk}, timeout=30)
        if not resp.ok:
            print(f"[ERROR] Notion API: {resp.status_code} {resp.text[:300]}",
                  file=sys.stderr)
            resp.raise_for_status()
        print(f"  → {len(chunk)}블록 append 완료 (chunk {i//MAX_BLOCKS_PER_REQ+1})",
              file=sys.stderr)


def create_page(parent_id: str, title: str, blocks: list, key: str) -> str:
    """C-31 하위에 새 페이지 생성, 생성된 page_id 반환"""
    url = f"{NOTION_API_BASE}/pages"
    payload = {
        "parent": {"type": "page_id", "page_id": parent_id},
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": title}}]
            }
        },
        # 첫 번째 청크 (최대 50블록) 를 생성 시 함께 전달
        "children": blocks[:MAX_BLOCKS_PER_REQ],
    }
    resp = requests.post(url, headers=notion_headers(key),
                         json=payload, timeout=30)
    if not resp.ok:
        print(f"[ERROR] 페이지 생성 실패: {resp.status_code} {resp.text[:300]}",
              file=sys.stderr)
        resp.raise_for_status()
    page_id = resp.json()["id"]
    print(f"  → 새 페이지 생성 완료: {page_id}", file=sys.stderr)

    # 나머지 블록 append (50개 초과 시)
    remaining = blocks[MAX_BLOCKS_PER_REQ:]
    if remaining:
        append_blocks(page_id, remaining, key)

    return page_id


# ─── 블록 빌더 ─────────────────────────────────────────────────────────────────
def rich_text(content: str, bold: bool = False, color: str = "default") -> dict:
    return {
        "type": "text",
        "text": {"content": content},
        "annotations": {"bold": bold, "color": color},
    }


def heading3_block(text: str) -> dict:
    return {
        "object": "block", "type": "heading_3",
        "heading_3": {"rich_text": [rich_text(text, bold=True)]},
    }


def paragraph_block(text: str, color: str = "default") -> dict:
    return {
        "object": "block", "type": "paragraph",
        "paragraph": {"rich_text": [rich_text(text, color=color)]},
    }


def divider_block() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


def callout_block(text: str, emoji: str, color: str) -> dict:
    return {
        "object": "block", "type": "callout",
        "callout": {
            "rich_text": [rich_text(text)],
            "icon": {"type": "emoji", "emoji": emoji},
            "color": f"{color}_background",
        },
    }


def bulleted_list_block(items: list[str]) -> list[dict]:
    return [
        {
            "object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [rich_text(item[:2000])]},
        }
        for item in items if item.strip()
    ]


def toggle_block(summary: str, children: list[dict]) -> dict:
    return {
        "object": "block", "type": "toggle",
        "toggle": {
            "rich_text": [rich_text(summary, bold=True)],
            "children": children,
        },
    }


# ─── 섹션 빌더 ─────────────────────────────────────────────────────────────────
def build_header_section(
    week: str, run_date: str, ew_triggered: bool, ew_severity: str,
    kg_version: str, node_count: int, edge_count: int,
) -> list[dict]:
    blocks = []
    ew_emoji = EW_EMOJI_MAP.get(ew_severity, "✅")
    ew_color = EW_COLOR_MAP.get(ew_severity, "green")
    ew_text  = f"{ew_emoji} EW Status: {ew_severity}"

    blocks.append(divider_block())
    blocks.append(heading3_block(f"📡 AI Intel Weekly — {week} ({run_date})"))
    blocks.append(callout_block(ew_text, ew_emoji, ew_color))
    blocks.append(paragraph_block(
        f"🗄️ KG v{kg_version} | 노드 +{node_count} | 엣지 +{edge_count} | "
        f"실행: {run_date}"
    ))
    return blocks


def build_domain_section(intel: dict) -> list[dict]:
    """단일 도메인 인텔 → 블록 리스트"""
    domain   = intel.get("domain", "unknown")
    summary  = intel.get("summary", "요약 없음")
    facts    = intel.get("key_facts", [])[:6]   # 최대 6개
    signals  = intel.get("emerging_signals", [])[:4]
    conf     = intel.get("confidence", 0)

    domain_label = {
        "enterprise_deployment": "🏢 Enterprise Deployment",
        "model_performance":     "🧠 Model Performance",
        "infrastructure":        "⚙️ Infrastructure & Chips",
        "regulatory":            "⚖️ Regulatory & Policy",
        "open_source":           "🔓 Open Source Ecosystem",
        "investment":            "💰 Investment & M&A",
    }.get(domain, f"📊 {domain}")

    blocks = []
    blocks.append(heading3_block(f"{domain_label} (conf={conf:.2f})"))
    blocks.append(paragraph_block(summary))

    if facts:
        blocks.append(paragraph_block("📌 Key Facts:", bold=True))
        blocks.extend(bulleted_list_block(facts))

    if signals:
        children = bulleted_list_block(signals)
        if children:
            blocks.append(toggle_block(f"🔭 Emerging Signals ({len(signals)}개)",
                                        children))
    return blocks


def build_ew_section(ew_count: int, ew_signals: str, ew_severity: str) -> list[dict]:
    if ew_count == 0:
        return [paragraph_block("EW 시그널 없음 — 정상 범위", color="green")]

    blocks = []
    emoji = EW_EMOJI_MAP.get(ew_severity, "⚠️")
    color = EW_COLOR_MAP.get(ew_severity, "yellow")
    blocks.append(callout_block(
        f"{emoji} {ew_count}개 EW 시그널 탐지 — 심각도: {ew_severity}",
        emoji, color
    ))
    if ew_signals:
        sig_list = [s.strip() for s in ew_signals.split(",") if s.strip()]
        if sig_list:
            blocks.append(paragraph_block("탐지된 시그널:"))
            blocks.extend(bulleted_list_block(sig_list))
    return blocks


def build_run_log_block(week: str, run_date: str, status: str) -> dict:
    ts = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    return paragraph_block(
        f"🕐 실행 이력: {week} | {run_date} | 상태: {status} | UTC: {ts}",
        color="gray",
    )


# ─── 핵심 블록 조립 ───────────────────────────────────────────────────────────
def build_all_blocks(
    week: str,
    run_date: str,
    ew_triggered: bool,
    ew_count: int,
    ew_signals: str,
    ew_severity: str,
    kg_version: str,
    node_count: int,
    edge_count: int,
    intel_dir: Path | None,
) -> list[dict]:
    blocks = []

    # 헤더
    blocks.extend(build_header_section(
        week, run_date, ew_triggered, ew_severity,
        kg_version, node_count, edge_count,
    ))

    # EW 섹션
    if ew_triggered:
        blocks.append(heading3_block("🚨 Early Warning 상세"))
        blocks.extend(build_ew_section(ew_count, ew_signals, ew_severity))

    # 도메인별 인텔 섹션
    if intel_dir and intel_dir.exists():
        blocks.append(heading3_block("📊 도메인별 인텔 요약"))
        for f in sorted(intel_dir.glob("intel_*.json")):
            try:
                intel = json.loads(f.read_text())
                blocks.extend(build_domain_section(intel))
                blocks.append(divider_block())
            except Exception as e:
                blocks.append(paragraph_block(f"[오류] {f.name}: {e}"))

    # 실행 이력
    status = "EW_TRIGGERED" if ew_triggered else "OK"
    blocks.append(build_run_log_block(week, run_date, status))

    return blocks


# ─── 핵심 공개 API: create_weekly_report() ────────────────────────────────────
def create_weekly_report(
    week_num: int,
    ew_results: dict,
    intel_results: list[dict],
    year: int | None = None,
    parent_page_id: str = PARENT_PAGE_ID,
    dry_run: bool = False,
) -> str | None:
    """
    C-31 하위에 Weekly Intel Report 페이지를 자동 생성하고 page_id를 반환.

    Parameters
    ----------
    week_num      : ISO 주차 번호 (예: 22)
    ew_results    : EW 탐지 결과 dict
                    {
                      "triggered": bool,
                      "count": int,
                      "signals": str,   # 콤마 구분
                      "severity": str,  # NONE|WATCH|WARNING|CRITICAL
                    }
    intel_results : 도메인 인텔 dict 리스트 (intel_*.json 구조와 동일)
    year          : 연도 (기본값: 현재 연도)
    parent_page_id: 상위 페이지 ID (기본값: PARENT_PAGE_ID 상수)
    dry_run       : True 면 Notion API 호출 없이 블록 JSON 출력 후 반환

    Returns
    -------
    생성된 Notion page_id (dry_run=True 이면 None)
    """
    if year is None:
        year = datetime.utcnow().year

    week_str  = f"{year}-W{week_num:02d}"
    run_date  = datetime.utcnow().strftime("%Y-%m-%d")
    title     = f"📊 Weekly Intel Report — {week_str}"

    ew_triggered = ew_results.get("triggered", False)
    ew_count     = ew_results.get("count", 0)
    ew_signals   = ew_results.get("signals", "")
    ew_severity  = ew_results.get("severity", "NONE")

    # intel_results → 임시 Path 없이 직접 블록 조립
    blocks: list[dict] = []
    blocks.extend(build_header_section(
        week_str, run_date, ew_triggered, ew_severity,
        kg_version="auto", node_count=0, edge_count=0,
    ))

    if ew_triggered:
        blocks.append(heading3_block("🚨 Early Warning 상세"))
        blocks.extend(build_ew_section(ew_count, ew_signals, ew_severity))

    if intel_results:
        blocks.append(heading3_block("📊 도메인별 인텔 요약"))
        for intel in intel_results:
            blocks.extend(build_domain_section(intel))
            blocks.append(divider_block())

    status = "EW_TRIGGERED" if ew_triggered else "OK"
    blocks.append(build_run_log_block(week_str, run_date, status))

    if dry_run:
        print(json.dumps({"title": title, "blocks": blocks, "count": len(blocks)},
                         ensure_ascii=False, indent=2))
        print(f"[DRY-RUN] create_weekly_report: {len(blocks)}블록 (API 호출 없음)",
              file=sys.stderr)
        return None

    notion_key = get_notion_key()
    print(f"[INFO] '{title}' 페이지 생성 중 (parent: {parent_page_id})…",
          file=sys.stderr)
    page_id = create_page(parent_page_id, title, blocks, notion_key)
    print(f"[OK] 생성 완료 → page_id: {page_id}")
    print(f"     주차: {week_str} | EW: {ew_triggered}/{ew_severity} | 블록: {len(blocks)}")
    return page_id


# ─── CLI ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Notion C-31 업데이터 v3")
    parser.add_argument("--page-id",      default=None,
                        help="append 모드: 기존 페이지 ID (--create-page 미사용 시 필수)")
    parser.add_argument("--create-page",  action="store_true",
                        help="C-31 하위에 새 페이지 생성 모드")
    parser.add_argument("--week",         required=True,
                        help="예: 2026-W22")
    parser.add_argument("--run-date",     required=True)
    parser.add_argument("--ew-triggered", required=True)
    parser.add_argument("--ew-count",     type=int, default=0)
    parser.add_argument("--ew-signals",   default="")
    parser.add_argument("--ew-severity",  default="NONE")
    parser.add_argument("--kg-version",   required=True)
    parser.add_argument("--node-count",   type=int, default=0)
    parser.add_argument("--edge-count",   type=int, default=0)
    parser.add_argument("--intel-dir",    default=None)
    parser.add_argument("--dry-run",      action="store_true")
    args = parser.parse_args()

    ew_triggered = args.ew_triggered.lower() in ("true", "1", "yes")
    intel_dir    = Path(args.intel_dir) if args.intel_dir else None

    # ── 새 하위 페이지 생성 모드 ──────────────────────────────────────────────
    if args.create_page:
        # week 파싱: "2026-W22" → week_num=22, year=2026
        try:
            year_str, w_str = args.week.split("-W")
            week_num = int(w_str)
            year     = int(year_str)
        except ValueError:
            print(f"[ERROR] --week 형식 오류: {args.week} (예: 2026-W22)",
                  file=sys.stderr)
            sys.exit(1)

        # intel_dir → list[dict] 로드
        intel_results = []
        if intel_dir and intel_dir.exists():
            for f in sorted(intel_dir.glob("intel_*.json")):
                try:
                    intel_results.append(json.loads(f.read_text()))
                except Exception as e:
                    print(f"[WARN] {f.name} 로드 실패: {e}", file=sys.stderr)

        ew_results = {
            "triggered": ew_triggered,
            "count":     args.ew_count,
            "signals":   args.ew_signals,
            "severity":  args.ew_severity,
        }
        create_weekly_report(
            week_num=week_num,
            ew_results=ew_results,
            intel_results=intel_results,
            year=year,
            dry_run=args.dry_run,
        )
        return

    # ── 기존 append 모드 ──────────────────────────────────────────────────────
    if not args.page_id:
        print("[ERROR] --page-id 또는 --create-page 중 하나 필수", file=sys.stderr)
        sys.exit(1)

    blocks = build_all_blocks(
        week=args.week,
        run_date=args.run_date,
        ew_triggered=ew_triggered,
        ew_count=args.ew_count,
        ew_signals=args.ew_signals,
        ew_severity=args.ew_severity,
        kg_version=args.kg_version,
        node_count=args.node_count,
        edge_count=args.edge_count,
        intel_dir=intel_dir,
    )

    if args.dry_run:
        print(json.dumps({"blocks": blocks, "count": len(blocks)},
                         ensure_ascii=False, indent=2))
        print(f"[DRY-RUN] {len(blocks)}개 블록 생성 (API 호출 없음)",
              file=sys.stderr)
        return

    notion_key = get_notion_key()
    print(f"[INFO] {len(blocks)}개 블록 → Notion 페이지 {args.page_id} 업데이트 중...",
          file=sys.stderr)
    append_blocks(args.page_id, blocks, notion_key)
    print(f"[OK] Notion C-31 업데이트 완료")
    print(f"     주차: {args.week} | EW: {ew_triggered}/{args.ew_severity} | "
          f"KG: v{args.kg_version}")


if __name__ == "__main__":
    main()
