#!/usr/bin/env python3
"""
notion_c31_updater.py
─────────────────────
Notion C-31 PE-AI Intel EW 레지스트리 자동 업데이트
워크플로: ai-intel-weekly.yml → STAGE 4

사용법:
  python automation/notion_c31_updater.py \
    --page-id 34a55ed436f0814d9cffe6a2f0816e29 \
    --week 2026-W21 \
    --run-date 2026-05-19 \
    --ew-triggered true \
    --ew-count 2 \
    --ew-signals EW-RAG-OSS,EW-MODEL-FLOOD \
    --ew-severity MEDIUM \
    --kg-version 4.26 \
    --node-count 42 \
    --edge-count 28 \
    --intel-dir output/ai_intel
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests


# ─────────────────────────────────────────
# Notion API 상수
# ─────────────────────────────────────────
NOTION_API_BASE  = "https://api.notion.com/v1"
NOTION_VERSION   = "2022-06-28"

SEVERITY_EMOJI = {
    "CRITICAL": "🚨",
    "HIGH":     "🔴",
    "MEDIUM":   "🟡",
    "LOW":      "🟢",
    "NONE":     "⚪",
}

EW_SIGNAL_LABELS = {
    "EW-AI-DEPLOY":   "기업 AI 배포 저조",
    "EW-RAG-OSS":     "OSS RAG 전환 가속",
    "EW-MODEL-FLOOD": "모델 출시 과다",
    "EW-CONSULT":     "AI 컨설팅 시장 교란",
    "EW-INFRA":       "ML 인프라 격차",
    "EW-ORCH":        "멀티에이전트 오케스트레이션 급증",
}


# ─────────────────────────────────────────
# Notion API 헬퍼
# ─────────────────────────────────────────
class NotionClient:
    def __init__(self, api_key: str):
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }

    def get_page(self, page_id: str) -> dict:
        resp = requests.get(
            f"{NOTION_API_BASE}/pages/{page_id}",
            headers=self.headers,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def append_blocks(self, page_id: str, children: list[dict]) -> dict:
        """페이지에 블록 추가"""
        resp = requests.patch(
            f"{NOTION_API_BASE}/blocks/{page_id}/children",
            headers=self.headers,
            json={"children": children},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def get_blocks(self, block_id: str) -> list[dict]:
        """블록의 자식 목록 조회"""
        resp = requests.get(
            f"{NOTION_API_BASE}/blocks/{block_id}/children",
            headers=self.headers,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json().get("results", [])


# ─────────────────────────────────────────
# Notion 블록 빌더
# ─────────────────────────────────────────
def rich_text(content: str, bold: bool = False, color: str = "default") -> dict:
    """Notion rich_text 객체 생성"""
    return {
        "type": "text",
        "text": {"content": content},
        "annotations": {
            "bold": bold,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": False,
            "color": color,
        },
    }


def heading2_block(text: str) -> dict:
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [rich_text(text, bold=True)]},
    }


def heading3_block(text: str) -> dict:
    return {
        "object": "block",
        "type": "heading_3",
        "heading_3": {"rich_text": [rich_text(text)]},
    }


def paragraph_block(parts: list[dict]) -> dict:
    """rich_text 파트 배열로 paragraph 블록 생성"""
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": parts},
    }


def bullet_block(text: str, color: str = "default") -> dict:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [rich_text(text, color=color)]},
    }


def callout_block(text: str, emoji: str = "📊", color: str = "gray_background") -> dict:
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [rich_text(text)],
            "icon": {"type": "emoji", "emoji": emoji},
            "color": color,
        },
    }


def divider_block() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


# ─────────────────────────────────────────
# 주간 업데이트 블록 구성
# ─────────────────────────────────────────
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
    intel_summaries: dict[str, str],
) -> list[dict]:
    """C-31 페이지에 추가할 주간 업데이트 블록 구성"""
    blocks = []
    sev_emoji = SEVERITY_EMOJI.get(ew_severity, "⚪")
    ew_status = f"{sev_emoji} EW 발동" if ew_triggered else "🟢 EW 없음"

    # ── 섹션 헤더 ──
    blocks.append(divider_block())
    blocks.append(heading2_block(f"📅 {week} — 주간 AI 인텔 업데이트"))
    blocks.append(paragraph_block([
        rich_text("수집일: ", bold=True),
        rich_text(run_date),
        rich_text("  |  "),
        rich_text("파이프라인: ", bold=True),
        rich_text("ai-intel-weekly (자동)"),
    ]))

    # ── EW 현황 ──
    blocks.append(heading3_block("⚠️ EW(Early Warning) 현황"))

    ew_bg_color = "red_background" if ew_triggered and ew_severity in ["HIGH", "CRITICAL"] else "yellow_background" if ew_triggered else "green_background"
    ew_summary_text = (
        f"{ew_status} — {ew_count}개 신호 발동 | 심각도: {ew_severity}"
        if ew_triggered else
        "이번 주 EW 임계값 초과 신호 없음 — 정상 범위"
    )
    blocks.append(callout_block(ew_summary_text, emoji=sev_emoji if ew_triggered else "✅", color=ew_bg_color))

    if ew_triggered and ew_signals:
        for sig_id in ew_signals:
            sig_label = EW_SIGNAL_LABELS.get(sig_id, sig_id)
            color = "red" if ew_severity in ["HIGH", "CRITICAL"] else "orange"
            blocks.append(bullet_block(f"{sig_id} — {sig_label}", color=color))

    # ── KG Delta 현황 ──
    blocks.append(heading3_block("🧠 Knowledge Graph Delta"))
    blocks.append(paragraph_block([
        rich_text("버전: ", bold=True),
        rich_text(f"v{kg_version}"),
        rich_text("  |  "),
        rich_text("노드: ", bold=True),
        rich_text(f"+{node_count}"),
        rich_text("  |  "),
        rich_text("엣지: ", bold=True),
        rich_text(f"+{edge_count}"),
        rich_text("  |  "),
        rich_text("파일: ", bold=True),
        rich_text(f"knowledge_graph_v{kg_version}_delta.json", color="blue"),
    ]))

    # ── 도메인별 인텔 요약 ──
    if intel_summaries:
        blocks.append(heading3_block("📡 도메인별 인텔 수집 요약"))
        domain_labels = {
            "enterprise": "🏢 엔터프라이즈 AI 배포",
            "frameworks":  "🛠️ AI 프레임워크 & RAG",
            "models":      "🤖 모델 출시 & 벤치마크",
            "infra":       "☁️ AI 인프라 & 시장",
            "semiconductor": "💾 반도체 & AI 칩",
        }
        for domain_key, summary_text in intel_summaries.items():
            label = domain_labels.get(domain_key, f"📌 {domain_key}")
            blocks.append(bullet_block(f"{label}: {summary_text[:200]}"))

    return blocks


# ─────────────────────────────────────────
# 인텔 요약 로드
# ─────────────────────────────────────────
def load_intel_summaries(intel_dir: str) -> dict[str, str]:
    """intel_*.json에서 summary 필드만 추출"""
    summaries = {}
    for f in Path(intel_dir).glob("intel_*.json"):
        key = f.stem.replace("intel_", "")
        try:
            with open(f, encoding="utf-8") as fp:
                data = json.load(fp)
            summaries[key] = data.get("summary", "")[:200]
        except Exception:
            pass
    return summaries


# ─────────────────────────────────────────
# CLI
# ─────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Notion C-31 EW Registry Updater")
    p.add_argument("--page-id",      required=True)
    p.add_argument("--week",         required=True)
    p.add_argument("--run-date",     required=True)
    p.add_argument("--ew-triggered", required=True, help="'true' or 'false'")
    p.add_argument("--ew-count",     required=True, type=int)
    p.add_argument("--ew-signals",   default="",    help="Comma-separated signal IDs")
    p.add_argument("--ew-severity",  default="NONE")
    p.add_argument("--kg-version",   required=True)
    p.add_argument("--node-count",   required=True, type=int)
    p.add_argument("--edge-count",   required=True, type=int)
    p.add_argument("--intel-dir",    required=True)
    return p.parse_args()


def main():
    args = parse_args()

    api_key = os.environ.get("NOTION_API_KEY")
    if not api_key:
        print("[ERROR] NOTION_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    # 파라미터 정규화
    ew_triggered = args.ew_triggered.lower() == "true"
    ew_signals   = [s.strip() for s in args.ew_signals.split(",") if s.strip()]
    page_id      = args.page_id.replace("-", "")  # 하이픈 제거

    print(f"[INFO] Updating Notion C-31 page: {page_id}", file=sys.stderr)
    print(f"[INFO] EW triggered: {ew_triggered} | Signals: {ew_signals}", file=sys.stderr)

    # 인텔 요약 로드
    intel_summaries = load_intel_summaries(args.intel_dir)

    # Notion 클라이언트
    client = NotionClient(api_key)

    # 페이지 존재 확인
    try:
        page = client.get_page(page_id)
        print(f"[INFO] Page found: {page.get('url', 'N/A')}", file=sys.stderr)
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] Could not access Notion page {page_id}: {e}", file=sys.stderr)
        sys.exit(1)

    # 주간 업데이트 블록 구성
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
        intel_summaries=intel_summaries,
    )

    # Notion 페이지에 블록 추가 (append)
    # Notion API 제한: 한 번에 최대 100 블록
    BATCH_SIZE = 50
    for i in range(0, len(blocks), BATCH_SIZE):
        batch = blocks[i:i + BATCH_SIZE]
        result = client.append_blocks(page_id, batch)
        print(f"[INFO] Appended batch {i//BATCH_SIZE + 1}: {len(batch)} blocks", file=sys.stderr)

    print(f"[OK] Notion C-31 updated successfully: {len(blocks)} blocks added.", file=sys.stderr)


if __name__ == "__main__":
    main()
