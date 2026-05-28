#!/usr/bin/env python3
"""
notion_pe_sync.py

GitHub Actions → Notion PE Hub 단방향 Push 파이프라인

3-Engine 구조 (PE-CON / PE-FIN / PE-IP) ↔ Notion PE 허브 데이터베이스

환경변수 필수:
  NOTION_TOKEN        - Notion Integration Token (secret)
  NOTION_DATABASE_ID  - PE Hub 데이터베이스 ID (secret)

실행:
  python scripts/notion_pe_sync.py [--engine PE-FIN] [--dry-run]
"""

import os
import sys
import json
import argparse
import hashlib
import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("[ERROR] 'requests' 패키지가 없습니다. pip install requests")
    sys.exit(1)

# ─────────────────────────────────────────────
# 설정
# ─────────────────────────────────────────────
NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION  = "2022-06-28"

ENGINE_DIRS = {
    "PE-CON": "PE-CON",
    "PE-FIN": "PE-FIN",
    "PE-IP":  "PE-IP",
}

# Notion 데이터베이스 프로퍼티 매핑
# → Notion PE 허브 DB에 아래 컬럼이 존재해야 함
DB_PROP_MAP = {
    "title":       "Name",          # TITLE
    "engine":      "Engine",        # SELECT (PE-CON / PE-FIN / PE-IP)
    "file_path":   "File Path",     # RICH_TEXT
    "sha256":      "SHA-256",       # RICH_TEXT  (변경 감지용)
    "synced_at":   "Synced At",     # DATE
    "status":      "Status",        # SELECT (Active / Archived)
    "content":     "Content",       # RICH_TEXT (본문 앞 2000자)
}


# ─────────────────────────────────────────────
# Notion API 헬퍼
# ─────────────────────────────────────────────
class NotionClient:
    def __init__(self, token: str):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        })

    def query_database(self, db_id: str, filter_payload: dict | None = None) -> list:
        url = f"{NOTION_API_BASE}/databases/{db_id}/query"
        results, cursor = [], None
        while True:
            body = {}
            if filter_payload:
                body["filter"] = filter_payload
            if cursor:
                body["start_cursor"] = cursor
            resp = self.session.post(url, json=body)
            resp.raise_for_status()
            data = resp.json()
            results.extend(data.get("results", []))
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
        return results

    def create_page(self, db_id: str, properties: dict) -> dict:
        url = f"{NOTION_API_BASE}/pages"
        body = {
            "parent": {"database_id": db_id},
            "properties": properties,
        }
        resp = self.session.post(url, json=body)
        resp.raise_for_status()
        return resp.json()

    def update_page(self, page_id: str, properties: dict) -> dict:
        url = f"{NOTION_API_BASE}/pages/{page_id}"
        resp = self.session.patch(url, json={"properties": properties})
        resp.raise_for_status()
        return resp.json()


# ─────────────────────────────────────────────
# 유틸리티
# ─────────────────────────────────────────────
def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()[:16]   # 앞 16자만 저장


def build_properties(name: str, engine: str, file_path: str,
                     sha: str, content_preview: str) -> dict:
    now_iso = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return {
        DB_PROP_MAP["title"]: {
            "title": [{"text": {"content": name}}]
        },
        DB_PROP_MAP["engine"]: {
            "select": {"name": engine}
        },
        DB_PROP_MAP["file_path"]: {
            "rich_text": [{"text": {"content": file_path[:500]}}]
        },
        DB_PROP_MAP["sha256"]: {
            "rich_text": [{"text": {"content": sha}}]
        },
        DB_PROP_MAP["synced_at"]: {
            "date": {"start": now_iso}
        },
        DB_PROP_MAP["status"]: {
            "select": {"name": "Active"}
        },
        DB_PROP_MAP["content"]: {
            "rich_text": [{"text": {"content": content_preview[:2000]}}]
        },
    }


def extract_existing(pages: list) -> dict:
    """기존 Notion 페이지를 {file_path: {page_id, sha}} 로 인덱싱"""
    index = {}
    for page in pages:
        props = page.get("properties", {})
        fp_prop = props.get(DB_PROP_MAP["file_path"], {})
        sha_prop = props.get(DB_PROP_MAP["sha256"], {})
        fp_list = fp_prop.get("rich_text", [])
        sha_list = sha_prop.get("rich_text", [])
        if fp_list:
            fp_val  = fp_list[0]["text"]["content"]
            sha_val = sha_list[0]["text"]["content"] if sha_list else ""
            index[fp_val] = {"page_id": page["id"], "sha": sha_val}
    return index


# ─────────────────────────────────────────────
# 메인 동기화 로직
# ─────────────────────────────────────────────
def sync_engine(client: NotionClient, db_id: str,
                engine_name: str, engine_dir: str,
                dry_run: bool, repo_root: Path) -> dict:
    """단일 Engine 디렉토리를 Notion DB에 동기화"""
    stats = {"created": 0, "updated": 0, "skipped": 0, "errors": 0}
    engine_path = repo_root / engine_dir

    if not engine_path.exists():
        print(f"  [SKIP] {engine_dir} 디렉토리가 존재하지 않습니다.")
        return stats

    # 현재 Notion DB에서 해당 엔진 페이지 로드
    existing = extract_existing(
        client.query_database(db_id, {
            "property": DB_PROP_MAP["engine"],
            "select": {"equals": engine_name}
        })
    )

    # MD / JSON / PY 파일 순회
    for ext in ("*.md", "*.json", "*.py", "*.yaml", "*.yml", "*.txt"):
        for fpath in sorted(engine_path.rglob(ext)):
            rel = str(fpath.relative_to(repo_root))
            sha = file_sha256(fpath)
            name = fpath.stem

            try:
                content = fpath.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                print(f"  [ERROR] 파일 읽기 실패: {rel} → {e}")
                stats["errors"] += 1
                continue

            props = build_properties(name, engine_name, rel, sha, content)

            if rel in existing:
                if existing[rel]["sha"] == sha:
                    print(f"  [SKIP]  변경 없음: {rel}")
                    stats["skipped"] += 1
                    continue
                # 변경 감지 → Update
                print(f"  [UPDATE] {rel}")
                if not dry_run:
                    client.update_page(existing[rel]["page_id"], props)
                stats["updated"] += 1
            else:
                # 신규 → Create
                print(f"  [CREATE] {rel}")
                if not dry_run:
                    client.create_page(db_id, props)
                stats["created"] += 1

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="prompt-engineering-system → Notion PE Hub 동기화")
    parser.add_argument("--engine", choices=list(ENGINE_DIRS.keys()) + ["ALL"],
                        default="ALL", help="동기화할 엔진 (기본: ALL)")
    parser.add_argument("--dry-run", action="store_true",
                        help="실제 Notion API 호출 없이 변경 예상 목록만 출력")
    args = parser.parse_args()

    token = os.environ.get("NOTION_TOKEN")
    db_id = os.environ.get("NOTION_DATABASE_ID")

    if not token:
        print("[ERROR] NOTION_TOKEN 환경변수가 설정되지 않았습니다.")
        sys.exit(1)
    if not db_id:
        print("[ERROR] NOTION_DATABASE_ID 환경변수가 설정되지 않았습니다.")
        sys.exit(1)

    client    = NotionClient(token)
    repo_root = Path(__file__).parent.parent.resolve()
    total     = {"created": 0, "updated": 0, "skipped": 0, "errors": 0}

    engines = ENGINE_DIRS if args.engine == "ALL" \
              else {args.engine: ENGINE_DIRS[args.engine]}

    dry_tag = " [DRY-RUN]" if args.dry_run else ""
    print(f"\n{'='*60}")
    print(f"  Notion PE Hub 동기화 시작{dry_tag}")
    print(f"  DB: {db_id}")
    print(f"  대상 엔진: {', '.join(engines.keys())}")
    print(f"{'='*60}\n")

    for eng_name, eng_dir in engines.items():
        print(f"\n── Engine: {eng_name} ({eng_dir})")
        stats = sync_engine(client, db_id, eng_name, eng_dir,
                            args.dry_run, repo_root)
        for k, v in stats.items():
            total[k] += v

    print(f"\n{'='*60}")
    print(f"  완료 — Created:{total['created']}  "
          f"Updated:{total['updated']}  "
          f"Skipped:{total['skipped']}  "
          f"Errors:{total['errors']}")
    print(f"{'='*60}\n")

    if total["errors"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
