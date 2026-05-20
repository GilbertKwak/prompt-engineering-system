#!/usr/bin/env python3
"""
notion_c31_updater.py  v2 — Section A · Step 4
Notionの C-31 AI Intel Weekly 페이지 업데이트

변경사항 v2:
  - 도메인 섹션 분리 출력 (도메인별 카드)
  - EW 심각도 컬러 코딩 (red/yellow/green/blue callout)
  - 인텔 요약 카드 포맷 개선
  - --dry-run: 블록 JSON만 출력, API 호출 없음
  - 실행 이력 블록 자동 append

Usage:
  python automation/notion_c31_updater.py \\
    --page-id 34a55ed436f0814d9cffe6a2f0816e29 \\
    --week 2026-W21 \\
    --run-date 2026-05-20 \\
    --ew-triggered false \\
    --ew-count 0 \\
    --ew-signals "" \\
    --ew-severity NONE \\
    --kg-version 4.26 \\
    --node-count 5 \\
    --edge-count 3 \\
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
            "bulleted_list_item": {"rich_text": [rich_text(item[:2000))]},
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
    status   = intel.get("_status", "ok")

    domain_label = {
        "enterprise_deployment": "🏢 Enterprise Deployment",
        "model_performance":     "🧠 Model Performance",
        "infrastructure":        "⚙️ Infrastructure & Chips",
        "regulatory":            "⚖️ Regulatory & Policy",
        "open_source":           "🔓 Open Source Ecosystem",
        "investment":            "💰 Investment & M&A",
    }.get(domain, f"📊 {domain}")

    blocks = []
    conf_color = "red" if conf < 0.4 else "yellow" if conf < 0.65 else "green"
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


# ─── 메인 로직 ─────────────────────────────────────────────────────────────────
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
                domain_blocks = build_domain_section(intel)
                blocks.extend(domain_blocks)
                blocks.append(divider_block())
            except Exception as e:
                blocks.append(paragraph_block(f"[오류] {f.name}: {e}"))

    # 실행 이력
    status = "EW_TRIGGERED" if ew_triggered else "OK"
    blocks.append(build_run_log_block(week, run_date, status))

    return blocks


# ─── CLI ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Notion C-31 업데이터 v2")
    parser.add_argument("--page-id",      required=True)
    parser.add_argument("--week",         required=True)
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
