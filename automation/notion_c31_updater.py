#!/usr/bin/env python3
"""
notion_c31_updater.py  — Section A · Step 4
Notion C-31 페이지에 AI Intel Weekly 결과 업데이트

Usage:
  python automation/notion_c31_updater.py \
    --page-id 34a55ed436f0814d9cffe6a2f0816e29 \
    --week 2026-W21 \
    --run-date 2026-05-20 \
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
import re
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("[ERROR] requests 패키지 없음: pip install requests", file=sys.stderr)
    sys.exit(1)

# ─── 상수 ────────────────────────────────────────────────────────────────────
NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
BATCH_SIZE = 50  # Notion API 최대 블록 배치 크기

# EW 심각도 → Notion callout 색상
SEVERITY_COLOR = {
    "HIGH": "red_background",
    "MEDIUM": "yellow_background",
    "LOW": "blue_background",
    "NONE": "green_background",
}


# ─── UUID 정규화 ───────────────────────────────────────────────────────────────
def normalize_page_id(raw_id: str) -> str:
    """Notion page ID를 하이픈 포함 UUID 형식으로 정규화
    
    FIX: 하이픈 없는 UUID(32자), 하이픈 있는 UUID(36자) 모두 처리
    예: '34a55ed436f0814d9cffe6a2f0816e29' → '34a55ed4-36f0-814d-9cff-e6a2f0816e29'
    """
    if not raw_id or not raw_id.strip():
        print("[ERROR] page-id가 비어있음", file=sys.stderr)
        sys.exit(1)

    # URL에서 ID 추출 (notion.so/xxx/Title-{id} 형식)
    url_match = re.search(r"[a-f0-9]{32}$", raw_id.replace("-", "").lower())
    clean = raw_id.replace("-", "").strip().lower()

    if len(clean) != 32 or not re.match(r"^[a-f0-9]+$", clean):
        # 32자 hex가 아니면 그대로 반환 (이미 올바른 형식이거나 다른 형식)
        return raw_id.strip()

    # 32자 hex → 8-4-4-4-12 UUID 형식
    return f"{clean[:8]}-{clean[8:12]}-{clean[12:16]}-{clean[16:20]}-{clean[20:32]}"


# ─── API 클라이언트 ────────────────────────────────────────────────────────────
def get_notion_headers() -> dict:
    key = os.environ.get("NOTION_API_KEY", "").strip()
    if not key:
        print("[ERROR] NOTION_API_KEY 환경변수 미설정", file=sys.stderr)
        sys.exit(1)
    return {
        "Authorization": f"Bearer {key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def append_blocks(page_id: str, blocks: list[dict], headers: dict) -> bool:
    """블록 배치 append (50개씩 분할)"""
    url = f"{NOTION_API_BASE}/blocks/{page_id}/children"
    success = True

    for i in range(0, len(blocks), BATCH_SIZE):
        batch = blocks[i:i + BATCH_SIZE]
        for attempt in range(3):
            try:
                resp = requests.patch(
                    url,
                    headers=headers,
                    json={"children": batch},
                    timeout=30,
                )
                if resp.status_code == 429:
                    delay = 2 ** attempt
                    print(f"[WARN] Rate limit. {delay}s 대기", file=sys.stderr)
                    time.sleep(delay)
                    continue
                resp.raise_for_status()
                print(f"  ✓ 블록 배치 {i//BATCH_SIZE + 1} 추가 ({len(batch)}개)",
                      file=sys.stderr)
                break
            except requests.exceptions.RequestException as e:
                print(f"  ✗ 블록 추가 실패 (attempt {attempt+1}): {e}", file=sys.stderr)
                if attempt == 2:
                    success = False
        time.sleep(0.3)  # 배치 간 딜레이

    return success


# ─── Notion 블록 빌더 ──────────────────────────────────────────────────────────
def heading_2(text: str) -> dict:
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        },
    }


def heading_3(text: str) -> dict:
    return {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        },
    }


def paragraph(text: str, bold: bool = False) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "type": "text",
                "text": {"content": text},
                "annotations": {"bold": bold},
            }]
        },
    }


def bullet(text: str) -> dict:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        },
    }


def divider() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


def callout(text: str, color: str = "green_background", emoji: str = "✅") -> dict:
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "icon": {"type": "emoji", "emoji": emoji},
            "color": color,
        },
    }


# ─── 리포트 블록 조립 ──────────────────────────────────────────────────────────
def build_report_blocks(
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
) -> list[dict]:
    """C-31 업데이트용 Notion 블록 리스트 구성"""
    blocks = []
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    color = SEVERITY_COLOR.get(ew_severity, "green_background")
    ew_emoji = "🚨" if ew_severity == "HIGH" else "⚠️" if ew_severity == "MEDIUM" else "✅"

    # 섹션 헤더
    blocks.append(divider())
    blocks.append(heading_2(f"🤖 AI Intel Weekly · {week}"))
    blocks.append(paragraph(f"실행일시: {now} | KG v{kg_version}"))

    # EW 상태 callout
    if ew_triggered and ew_count > 0:
        ew_text = (
            f"Early Warning {ew_count}개 탐지 | 심각도: {ew_severity}\n"
            f"신호: {', '.join(ew_signals) if ew_signals else 'N/A'}"
        )
        blocks.append(callout(ew_text, color=color, emoji=ew_emoji))
    else:
        blocks.append(callout(
            f"Early Warning 없음 — 정상 범위 | 심각도: {ew_severity}",
            color="green_background", emoji="✅"
        ))

    # KG 델타 요약
    blocks.append(heading_3("📊 Knowledge Graph 업데이트"))
    blocks.append(bullet(f"버전: {kg_version}"))
    blocks.append(bullet(f"신규 노드: {node_count}개"))
    blocks.append(bullet(f"신규 엣지: {edge_count}개"))

    # 도메인별 인텔 요약
    if intel_summaries:
        blocks.append(heading_3("📡 도메인별 인텔 요약"))
        for summary in intel_summaries:
            domain = summary.get("domain", "unknown")
            confidence = summary.get("confidence", 0.0)
            text = summary.get("summary", "")
            blocks.append(paragraph(
                f"[{domain}] (신뢰도: {confidence:.2f}) {text}",
                bold=False
            ))

    # 수집 통계
    blocks.append(heading_3("📈 수집 통계"))
    blocks.append(bullet(f"분석 도메인: {len(intel_summaries)}개"))
    blocks.append(bullet(f"실행 일자: {run_date}"))
    blocks.append(bullet(f"EW 상태: {'발동' if ew_triggered else '정상'}"))

    return blocks


def load_intel_summaries(intel_dir: Path) -> list[dict]:
    """인텔 디렉토리에서 도메인 요약 로드"""
    summaries = []
    for f in sorted(intel_dir.glob("intel_*.json")):
        try:
            data = json.loads(f.read_text())
            summaries.append({
                "domain": data.get("domain", f.stem),
                "confidence": data.get("confidence", 0.0),
                "summary": data.get("summary", ""),
                "key_facts_count": len(data.get("key_facts", [])),
            })
        except Exception as e:
            print(f"[WARN] {f} 읽기 실패: {e}", file=sys.stderr)
    return summaries


# ─── CLI 진입점 ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Notion C-31 페이지 AI Intel 업데이트")
    parser.add_argument("--page-id", required=True,
                        help="Notion 페이지 ID (하이픈 유무 모두 가능)")
    parser.add_argument("--week", required=True)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--ew-triggered", default="false",
                        choices=["true", "false", "True", "False"])
    parser.add_argument("--ew-count", type=int, default=0)
    parser.add_argument("--ew-signals", default="",
                        help="EW 신호 목록 (쉼표 구분, 없으면 빈 문자열)")
    parser.add_argument("--ew-severity", default="NONE",
                        choices=["HIGH", "MEDIUM", "LOW", "NONE"])
    parser.add_argument("--kg-version", required=True)
    parser.add_argument("--node-count", type=int, default=0)
    parser.add_argument("--edge-count", type=int, default=0)
    parser.add_argument("--intel-dir", default="output/ai_intel",
                        help="인텔 JSON 파일 디렉토리")
    args = parser.parse_args()

    # FIX: page_id UUID 정규화
    page_id = normalize_page_id(args.page_id)
    print(f"[INFO] Page ID 정규화: {args.page_id} → {page_id}", file=sys.stderr)

    # FIX: ew_signals 안전 파싱
    ew_signals = []
    if args.ew_signals and args.ew_signals.strip():
        ew_signals = [s.strip() for s in args.ew_signals.split(",") if s.strip()]

    ew_triggered = args.ew_triggered.lower() == "true"

    intel_dir = Path(args.intel_dir)
    intel_summaries = load_intel_summaries(intel_dir) if intel_dir.exists() else []

    headers = get_notion_headers()

    blocks = build_report_blocks(
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

    print(f"[INFO] 총 {len(blocks)}개 블록 생성. Notion에 업데이트 시작...",
          file=sys.stderr)
    success = append_blocks(page_id, blocks, headers)

    if success:
        print(f"[OK] Notion C-31 업데이트 완료")
        print(f"     Page ID: {page_id} | 블록 수: {len(blocks)}")
    else:
        print("[ERROR] 일부 블록 업데이트 실패", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
