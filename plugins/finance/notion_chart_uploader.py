#!/usr/bin/env python3
"""
notion_chart_uploader.py — PE-7 P4
Uploads SMR chart PNGs as image blocks to a Notion page.
Usage:
  python notion_chart_uploader.py \
    --charts-dir output/charts \
    --page-id <NOTION_PAGE_ID> \
    --timestamp 20260426_160000 \
    --version v1.2 \
    --token <NOTION_TOKEN>
"""
import argparse, os, json, sys, base64, time
from pathlib import Path

CHART_META = {
    "moic_grouped_bar": {
        "title": "MOIC Absolute by Type & SMR Scenario",
        "section": "Sheet 8 — MOIC Analysis",
        "order": 1,
    },
    "moic_delta_bar": {
        "title": "MOIC Uplift Δ vs Grid Only Baseline",
        "section": "Sheet 8 — MOIC Analysis",
        "order": 2,
    },
    "moic_waterfall": {
        "title": "Portfolio MOIC Waterfall: Grid → SMR Full",
        "section": "Sheet 9 — Integrated DCF",
        "order": 3,
    },
    "tco_heatmap": {
        "title": "TCO NPV Savings: Facility Tier × Electricity Price",
        "section": "Sheet 8 — TCO Analysis",
        "order": 4,
    },
    "irr_moic_bubble": {
        "title": "IRR Alpha vs Portfolio MOIC (Bubble = Net Alpha $M)",
        "section": "Sheet 9 — Integrated DCF",
        "order": 5,
    },
}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--charts-dir", required=True)
    p.add_argument("--page-id",    required=True)
    p.add_argument("--timestamp",  required=True)
    p.add_argument("--version",    default="v1.2")
    p.add_argument("--token",      required=True)
    p.add_argument("--dry-run",    action="store_true")
    return p.parse_args()


def get_notion_client(token: str):
    try:
        from notion_client import Client
        return Client(auth=token)
    except ImportError:
        print("❌ notion-client not installed. Run: pip install notion-client")
        sys.exit(1)


def find_chart_file(charts_dir: Path, key: str) -> Path | None:
    """Find chart PNG by prefix key."""
    candidates = sorted(charts_dir.glob(f"{key}*.png"))
    return candidates[0] if candidates else None


def build_page_header_blocks(timestamp: str, version: str, scenario: str = "all") -> list:
    """Notion blocks for the run header section."""
    return [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {
                    "content": f"🚀 SMR Power Model — Run {timestamp} ({version})"
                }}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {
                    "content": f"PE-7 P4 Auto-generated | Scenario: {scenario} | Version: {version} | {timestamp}"
                }}],
                "icon": {"emoji": "📊"},
                "color": "blue_background"
            }
        },
        {
            "object": "block",
            "type": "divider",
            "divider": {}
        },
    ]


def build_chart_blocks(title: str, section: str, image_url: str) -> list:
    """Notion blocks for a single chart section."""
    return [
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": title}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {
                    "content": f"Section: {section}"
                }, "annotations": {"color": "gray"}}]
            }
        },
        {
            "object": "block",
            "type": "image",
            "image": {
                "type": "external",
                "external": {"url": image_url}
            }
        },
    ]


def upload_image_to_notion_file_api(token: str, page_id: str, filename: str, data: bytes) -> str | None:
    """
    Upload image via Notion File Upload API (beta).
    Returns the file upload URL or None if unavailable.
    """
    import urllib.request, urllib.error
    # Step 1: Create upload
    create_url = "https://api.notion.com/v1/file_uploads"
    payload = json.dumps({"filename": filename, "content_type": "image/png"}).encode()
    req = urllib.request.Request(create_url, data=payload, headers={
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            info = json.loads(resp.read())
            upload_id = info.get("id")
            upload_url = info.get("upload_url")
    except urllib.error.HTTPError as e:
        print(f"  ⚠️ File Upload API unavailable ({e.code}) — using external URL fallback")
        return None

    if not upload_url:
        return None

    # Step 2: Send binary
    req2 = urllib.request.Request(upload_url, data=data, method="PUT", headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "image/png",
    })
    try:
        urllib.request.urlopen(req2)
    except Exception as e:
        print(f"  ⚠️ PUT failed: {e}")
        return None

    return f"notion://file_uploads/{upload_id}"


def main():
    args = parse_args()
    charts_dir = Path(args.charts_dir)
    result_path = Path("/tmp/notion_upload_result.json")

    if not charts_dir.exists():
        print(f"❌ Charts dir not found: {charts_dir}")
        sys.exit(1)

    notion = get_notion_client(args.token)
    page_id = args.page_id.replace("-", "")

    # ── Build blocks ──────────────────────────────────────────
    all_blocks = build_page_header_blocks(args.timestamp, args.version)
    uploaded = 0
    skipped  = 0
    results  = []

    ordered_charts = sorted(CHART_META.items(), key=lambda x: x[1]["order"])

    for key, meta in ordered_charts:
        chart_path = find_chart_file(charts_dir, key)
        if not chart_path:
            print(f"  ⚠️ Chart not found: {key} — skipping")
            skipped += 1
            continue

        print(f"  📤 Processing: {chart_path.name}")

        if args.dry_run:
            print(f"  [DRY-RUN] Would upload: {chart_path.name}")
            uploaded += 1
            continue

        # Try File Upload API first, fall back to GitHub raw URL
        with open(chart_path, "rb") as f:
            img_data = f.read()

        notion_file_url = upload_image_to_notion_file_api(
            args.token, page_id, chart_path.name, img_data
        )

        # Fallback: use GitHub raw URL (requires charts committed to repo)
        if not notion_file_url:
            repo_raw = (
                f"https://raw.githubusercontent.com/GilbertKwak/prompt-engineering-system/main/"
                f"output/charts/{chart_path.name}"
            )
            notion_file_url = repo_raw

        chart_blocks = build_chart_blocks(
            title=meta["title"],
            section=meta["section"],
            image_url=notion_file_url,
        )
        all_blocks.extend(chart_blocks)
        uploaded += 1
        results.append({"key": key, "url": notion_file_url})

    # Append divider + timestamp footer
    all_blocks.append({"object": "block", "type": "divider", "divider": {}})
    all_blocks.append({
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {
                "content": f"Auto-generated by PE-7 P4 Pipeline | {args.timestamp} | {uploaded} charts"
            }, "annotations": {"color": "gray", "italic": True}}]
        }
    })

    # ── Append to Notion page (batch, max 100 blocks per call) ──
    if not args.dry_run:
        BATCH = 100
        for i in range(0, len(all_blocks), BATCH):
            batch = all_blocks[i:i+BATCH]
            try:
                notion.blocks.children.append(block_id=page_id, children=batch)
                time.sleep(0.3)  # rate limit
            except Exception as e:
                print(f"❌ Notion API error: {e}")
                sys.exit(1)

    # ── Result output ─────────────────────────────────────────
    page_url = f"https://notion.so/{page_id}"
    output = {
        "page_url": page_url,
        "uploaded": uploaded,
        "skipped": skipped,
        "timestamp": args.timestamp,
        "version": args.version,
    }
    with open(result_path, "w") as f:
        json.dump(output, f)
        f.write("\n")

    print(f"\n✅ Notion upload complete: {uploaded} charts → {page_url}")
    print(f"   Skipped: {skipped}")


if __name__ == "__main__":
    main()
