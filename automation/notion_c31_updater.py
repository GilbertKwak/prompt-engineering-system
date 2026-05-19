#!/usr/bin/env python3
"""
automation/notion_c31_updater.py
Notion C-31 EW 레지스트리 자동 업데이트기

Usage (workflow에서 호출되는 방식 — 정확한 인터페이스):
  python automation/notion_c31_updater.py \
    --page-id 34a55ed436f0814d9cffe6a2f0816e29 \
    --week 2026-W21 \
    --run-date 2026-05-19 \
    --ew-triggered false \
    --ew-count 0 \
    --ew-signals "" \
    --ew-severity NONE \
    --kg-version 4.26 \
    --node-count 5 \
    --edge-count 3 \
    --intel-dir output/ai_intel
"""

import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

# ──────────────────────────────────────────
# Notion API Config
# ──────────────────────────────────────────
NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
BATCH_SIZE = 50  # Notion API 최대 블록 수

# EW 심각도 → callout 색상 매핑
SEVERITY_COLOR = {
    "HIGH": "red",
    "MEDIUM": "yellow",
    "LOW": "blue",
    "NONE": "green",
}


def get_headers(api_key: str) -> dict:
    return {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def append_blocks(page_id: str, blocks: list, api_key: str) -> bool:
    """Notion blocks append (배치 처리, 최대 BATCH_SIZE)"""
    headers = get_headers(api_key)
    url = f"{NOTION_API_BASE}/blocks/{page_id}/children"

    for i in range(0, len(blocks), BATCH_SIZE):
        batch = blocks[i:i + BATCH_SIZE]
        resp = requests.patch(url, headers=headers, json={"children": batch}, timeout=30)
        if not resp.ok:
            print(f"  [ERROR] Notion API 오류 {resp.status_code}: {resp.text[:200]}")
            return False
        if i + BATCH_SIZE < len(blocks):
            time.sleep(0.3)  # API rate limit 방지

    return True


def build_divider() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


def build_heading2(text: str) -> dict:
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        },
    }


def build_heading3(text: str) -> dict:
    return {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        },
    }


def build_paragraph(text: str, bold: bool = False) -> dict:
    rich = {
        "type": "text",
        "text": {"content": text},
        "annotations": {"bold": bold},
    }
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [rich]},
    }


def build_callout(text: str, emoji: str, color: str) -> dict:
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "icon": {"type": "emoji", "emoji": emoji},
            "color": f"{color}_background",
        },
    }


def build_bulleted_item(text: str) -> dict:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        },
    }


def build_code_block(code: str, language: str = "json") -> dict:
    return {
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [{"type": "text", "text": {"content": code}}],
            "language": language,
        },
    }


def load_intel_summary(intel_dir: str) -> dict:
    """인텔 파일에서 도메인별 요약 추출"""
    summary = {}
    dir_path = Path(intel_dir)
    for f in sorted(dir_path.glob("intel_*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            domain = data.get("domain", f.stem)
            summary[domain] = {
                "model": data.get("model"),
                "key_facts": data.get("key_facts", [])[:3],
                "metrics": data.get("metrics", {}),
                "query_count": data.get("query_count", 0),
            }
        except Exception:
            pass
    return summary


def build_weekly_update_blocks(
    week: str,
    run_date: str,
    ew_triggered: bool,
    ew_count: int,
    ew_signals: list[str],
    ew_severity: str,
    kg_version: str,
    node_count: int,
    edge_count: int,
    intel_dir: str,
) -> list[dict]:
    """Notion에 추가할 블록 목록 생성"""
    blocks = []
    intel_summary = load_intel_summary(intel_dir)
    ew_color = SEVERITY_COLOR.get(ew_severity, "green")
    ew_emoji = "🔴" if ew_triggered else "🟢"
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # 구분선 + 주간 헤더
    blocks.append(build_divider())
    blocks.append(build_heading2(f"📊 AI Intel Weekly — {week}"))
    blocks.append(build_paragraph(f"실행: {timestamp} | Run Date: {run_date}"))

    # EW 상태 callout
    if ew_triggered:
        ew_text = (
            f"EW 발동 — {ew_count}개 신호 | 심각도: {ew_severity}\n"
            f"신호: {', '.join(ew_signals) if ew_signals else '없음'}"
        )
        blocks.append(build_callout(ew_text, ew_emoji, ew_color))
    else:
        blocks.append(build_callout(
            f"EW 미발동 — 정상 범위 | 심각도: {ew_severity}",
            ew_emoji, ew_color
        ))

    # KG Delta 요약
    blocks.append(build_heading3("🧠 Knowledge Graph Delta"))
    blocks.append(build_bulleted_item(f"버전: v{kg_version}"))
    blocks.append(build_bulleted_item(f"신규 노드: {node_count}개"))
    blocks.append(build_bulleted_item(f"신규 엣지: {edge_count}개"))

    # 도메인 인텔 요약
    if intel_summary:
        blocks.append(build_heading3("📡 도메인별 인텔 요약"))
        for domain, info in intel_summary.items():
            blocks.append(build_paragraph(f"▶ {domain} (모델: {info['model']})", bold=True))
            for fact in info.get("key_facts", []):
                if fact:
                    blocks.append(build_bulleted_item(str(fact)[:200]))
            if info.get("metrics"):
                metrics_str = json.dumps(info["metrics"], ensure_ascii=False)
                blocks.append(build_code_block(metrics_str, "json"))

    # EW 신호 상세 (발동 시)
    if ew_triggered and ew_signals:
        blocks.append(build_heading3("⚠️ EW 신호 상세"))
        for signal in ew_signals:
            blocks.append(build_bulleted_item(f"{signal}"))

    return blocks


def main():
    parser = argparse.ArgumentParser(description="Notion C-31 EW 레지스트리 업데이터")
    parser.add_argument("--page-id", required=True, help="Notion 페이지 ID")
    parser.add_argument("--week", required=True, help="주간 레이블 (예: 2026-W21)")
    parser.add_argument("--run-date", required=True, help="실행 날짜 (YYYY-MM-DD)")
    parser.add_argument("--ew-triggered", required=True, help="EW 발동 여부 (true/false)")
    parser.add_argument("--ew-count", type=int, default=0, help="EW 신호 수")
    parser.add_argument("--ew-signals", default="", help="EW 신호 목록 (콤마 구분)")
    parser.add_argument("--ew-severity", default="NONE", help="EW 최대 심각도")
    parser.add_argument("--kg-version", required=True, help="KG 버전 (예: 4.26)")
    parser.add_argument("--node-count", type=int, default=0, help="신규 노드 수")
    parser.add_argument("--edge-count", type=int, default=0, help="신규 엣지 수")
    parser.add_argument("--intel-dir", default="output/ai_intel", help="인텔 파일 디렉토리")
    args = parser.parse_args()

    api_key = os.environ.get("NOTION_API_KEY")
    if not api_key:
        raise EnvironmentError("NOTION_API_KEY 환경변수가 설정되지 않았습니다.")

    ew_triggered = args.ew_triggered.lower() in ("true", "1", "yes")
    ew_signals = [s.strip() for s in args.ew_signals.split(",") if s.strip()]

    print(f"\n[INFO] Notion C-31 업데이트 시작")
    print(f"  Page ID: {args.page_id}")
    print(f"  Week: {args.week} | EW: {ew_triggered} | KG: v{args.kg_version}")

    blocks = build_weekly_update_blocks(
        week=args.week,
        run_date=args.run_date,
        ew_triggered=ew_triggered,
        ew_count=args.ew_count,
        ew_signals=ew_signals,
        ew_severity=args.ew_severity,
        kg_version=args.kg_version,
        node_count=args.node_count,
        edge_count=args.edge_count,
        intel_dir=args.intel_dir,
    )

    print(f"  생성된 블록: {len(blocks)}개")

    success = append_blocks(args.page_id, blocks, api_key)
    if success:
        print(f"[OK] Notion C-31 업데이트 완료")
    else:
        print(f"[ERROR] Notion 업데이트 실패")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
