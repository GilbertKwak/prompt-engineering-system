#!/usr/bin/env python3
"""
Notion DB 스키마 자동 확장 — notion_schema_setup.py v1.0

EW / S4 / JV Notion DB에 검증 체계용 3개 필드를 추가:
  - Validation Status  (Select: PASS / WARN / FAIL)
  - Validation Log     (Rich Text)
  - Validated At       (Date)

이미 필드가 존재하면 스킵 (idempotent).

Usage:
    NOTION_API_KEY=xxx python scripts/notion_schema_setup.py
    NOTION_API_KEY=xxx python scripts/notion_schema_setup.py --dry-run
    NOTION_API_KEY=xxx python scripts/notion_schema_setup.py --db-id <DB_ID>
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Dict, List

try:
    from notion_client import Client as NotionClient
except ImportError:
    print("ERROR: notion-client not installed. Run: pip install notion-client")
    sys.exit(1)


NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "")

# 추가할 검증 필드 정의
VALIDATION_FIELDS: Dict[str, dict] = {
    "Validation Status": {
        "select": {
            "options": [
                {"name": "PASS",  "color": "green"},
                {"name": "WARN",  "color": "yellow"},
                {"name": "FAIL",  "color": "red"},
                {"name": "SKIP",  "color": "gray"},
            ]
        }
    },
    "Validation Log": {"rich_text": {}},
    "Validated At":   {"date": {}},
}

# 대상 DB 환경변수 목록
DB_ENV_VARS = [
    "NOTION_PE_MIN_EW_DB_ID",
    "NOTION_PE_MIN_RPT_DB",
    "NOTION_PE_JV_DB_ID",
]


def get_existing_properties(notion: NotionClient, db_id: str) -> List[str]:
    """DB의 현재 property 이름 목록 반환"""
    try:
        db = notion.databases.retrieve(database_id=db_id)
        return list(db.get("properties", {}).keys())
    except Exception as e:
        print(f"  ⚠️  DB 조회 실패 ({db_id}): {e}")
        return []


def add_validation_fields(
    notion: NotionClient,
    db_id: str,
    db_name: str,
    dry_run: bool = False,
) -> None:
    """DB에 검증 필드 추가 (이미 있으면 스킵)"""
    existing = get_existing_properties(notion, db_id)
    to_add = {
        name: spec
        for name, spec in VALIDATION_FIELDS.items()
        if name not in existing
    }

    if not to_add:
        print(f"  ✅ [{db_name}] 이미 모든 검증 필드 존재 — 스킵")
        return

    print(f"  📝 [{db_name}] 추가할 필드: {list(to_add.keys())}")

    if dry_run:
        print(f"  [DRY-RUN] 실제 업데이트 건너뜀")
        return

    try:
        notion.databases.update(
            database_id=db_id,
            properties=to_add,
        )
        print(f"  ✅ [{db_name}] 검증 필드 추가 완료")
    except Exception as e:
        print(f"  ❌ [{db_name}] 필드 추가 실패: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Notion DB 스키마 자동 확장 v1.0")
    parser.add_argument("--dry-run", action="store_true",
                        help="실제 업데이트 없이 변경 내용만 출력")
    parser.add_argument("--db-id", default="",
                        help="특정 DB ID만 업데이트 (생략 시 환경변수 기반 전체)")
    args = parser.parse_args()

    if not NOTION_API_KEY:
        print("[DRY-RUN] NOTION_API_KEY 없음 — 시뮬레이션 모드로 실행")
        print("추가 예정 필드:")
        for name in VALIDATION_FIELDS:
            print(f"  - {name}")
        print("대상 DB 환경변수:", DB_ENV_VARS)
        return

    notion = NotionClient(auth=NOTION_API_KEY)
    print(f"[SCHEMA-SETUP] 검증 필드 추가 시작 | dry_run={args.dry_run}")

    if args.db_id:
        # 단일 DB 지정 모드
        add_validation_fields(notion, args.db_id, "CUSTOM_DB", dry_run=args.dry_run)
    else:
        # 환경변수 기반 전체 DB
        found = 0
        for env_var in DB_ENV_VARS:
            db_id = os.environ.get(env_var, "")
            if not db_id:
                print(f"  ⏭️  [{env_var}] 환경변수 미설정 — 스킵")
                continue
            found += 1
            add_validation_fields(notion, db_id, env_var, dry_run=args.dry_run)

        if found == 0:
            print("  ⚠️  업데이트할 DB 없음. 환경변수를 확인하세요.")
            print(f"  필요 변수: {DB_ENV_VARS}")

    print("[SCHEMA-SETUP] 완료 ✅")


if __name__ == "__main__":
    main()
