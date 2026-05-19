#!/usr/bin/env python3
"""
sync_agents_to_notion.py

YAML→Notion Agent Index DB 업서트 스크립트
- agent_index.yaml 읽기
- Notion Agent Index DB에 각 Agent를 페이지로 upsert (agent_id 기준 중복 방지)
- Prompt Library DB와 relation 연결 (--link-prompt-library 플래그 사용 시)
- notion_page_id를 agent_index.yaml에 다시 기록 (write-back)

Usage:
  python scripts/sync_agents_to_notion.py \\
    --yaml agents/agent_index.yaml \\
    --db-id <NOTION_AGENT_DB_ID> \\
    --link-prompt-library

Secrets required:
  NOTION_API_KEY    - Notion Integration Token
  GITHUB_TOKEN      - for write-back to repo (optional)
"""

import os
import sys
import json
import time
import argparse
import logging
from pathlib import Path
from typing import Optional

import yaml
import requests

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("sync_agents")

# ---------------------------------------------------------------------------
# Notion API helpers
# ---------------------------------------------------------------------------
NOTION_VERSION = "2022-06-28"
BASE_URL = "https://api.notion.com/v1"


class NotionClient:
    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION,
        }

    def _request(self, method: str, path: str, payload: dict = None, retries=3) -> dict:
        url = f"{BASE_URL}{path}"
        for attempt in range(retries):
            try:
                resp = requests.request(
                    method, url,
                    headers=self.headers,
                    json=payload,
                    timeout=30,
                )
                if resp.status_code == 429:
                    wait = int(resp.headers.get("Retry-After", 2)) * (2 ** attempt)
                    log.warning(f"Rate limited. Waiting {wait}s...")
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.RequestException as e:
                if attempt == retries - 1:
                    raise
                time.sleep(2 ** attempt)
        return {}

    def query_db(self, db_id: str, filter_payload: dict = None) -> list:
        """DB 쿼리 (페이지네이션 처리)"""
        results = []
        start_cursor = None
        while True:
            payload = {"page_size": 100}
            if filter_payload:
                payload["filter"] = filter_payload
            if start_cursor:
                payload["start_cursor"] = start_cursor
            resp = self._request("POST", f"/databases/{db_id}/query", payload)
            results.extend(resp.get("results", []))
            if not resp.get("has_more"):
                break
            start_cursor = resp.get("next_cursor")
        return results

    def create_page(self, db_id: str, properties: dict, children: list = None) -> dict:
        payload = {
            "parent": {"database_id": db_id},
            "properties": properties,
        }
        if children:
            payload["children"] = children
        return self._request("POST", "/pages", payload)

    def update_page(self, page_id: str, properties: dict) -> dict:
        return self._request("PATCH", f"/pages/{page_id}", {"properties": properties})

    def get_db_schema(self, db_id: str) -> dict:
        return self._request("GET", f"/databases/{db_id}")


# ---------------------------------------------------------------------------
# Property builders
# ---------------------------------------------------------------------------

def build_title(text: str) -> dict:
    return {"title": [{"text": {"content": text}}]}


def build_rich_text(text: str) -> dict:
    return {"rich_text": [{"text": {"content": text[:2000]}}]}


def build_select(option: str) -> dict:
    return {"select": {"name": option}}


def build_multi_select(options: list) -> dict:
    return {"multi_select": [{"name": o} for o in options[:10]]}


def build_number(value: int) -> dict:
    return {"number": value}


def build_url(url: str) -> dict:
    return {"url": url} if url else {"url": None}


def build_relation(page_ids: list) -> dict:
    return {"relation": [{"id": pid} for pid in page_ids]}


# ---------------------------------------------------------------------------
# Core sync logic
# ---------------------------------------------------------------------------

def load_yaml(yaml_path: str) -> dict:
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_yaml(data: dict, yaml_path: str):
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def get_existing_pages(client: NotionClient, db_id: str) -> dict:
    """DB 내 기존 페이지를 agent_id → page_id 맵으로 반환"""
    pages = client.query_db(db_id)
    mapping = {}
    for page in pages:
        props = page.get("properties", {})
        agent_id_prop = props.get("Agent ID", {})
        rt = agent_id_prop.get("rich_text", [])
        if rt:
            agent_id = rt[0].get("text", {}).get("content", "")
            if agent_id:
                mapping[agent_id] = page["id"]
    return mapping


def build_properties(agent: dict, prompt_lib_page_id: Optional[str] = None) -> dict:
    """Agent 딕셔너리 → Notion DB properties 빌드"""
    github_base = "https://github.com/GilbertKwak/prompt-engineering-system/blob/main/"
    file_url = github_base + agent.get("file_path", "")

    props = {
        "Name": build_title(agent["name"]),
        "Agent ID": build_rich_text(agent["agent_id"]),
        "Domain": build_select(agent.get("domain", "")),
        "Status": build_select(agent.get("status", "active")),
        "Tier": build_select(agent.get("tier", "core")),
        "Version": build_rich_text(agent.get("version", "1.0")),
        "LLM Preference": build_select(agent.get("llm_preference", "claude-sonnet-4")),
        "Tags": build_multi_select(agent.get("tags", [])),
        "GitHub URL": build_url(file_url),
        "Priority": build_number(agent.get("priority", 99)),
        "Capabilities": build_rich_text("\n".join(agent.get("capabilities", []))),
        "Prompt Refs": build_rich_text("\n".join(agent.get("prompt_refs", []))),
    }

    if prompt_lib_page_id:
        props["Prompt Library"] = build_relation([prompt_lib_page_id])

    return props


def sync_agents(
    client: NotionClient,
    db_id: str,
    agents: list,
    link_prompt_library: bool = False,
    prompt_lib_page_id: Optional[str] = None,
) -> dict:
    """agents 리스트를 Notion DB에 upsert, agent_id→page_id 맵 반환"""
    existing = get_existing_pages(client, db_id)
    log.info(f"Found {len(existing)} existing agents in Notion DB")

    results = {}
    created = updated = failed = 0

    for agent in agents:
        agent_id = agent["agent_id"]
        plib_page = prompt_lib_page_id if link_prompt_library else None

        props = build_properties(agent, plib_page)

        try:
            if agent_id in existing:
                page_id = existing[agent_id]
                client.update_page(page_id, props)
                log.info(f"  UPDATED  {agent_id} — {agent['name']}")
                updated += 1
            else:
                page = client.create_page(db_id, props)
                page_id = page["id"]
                log.info(f"  CREATED  {agent_id} — {agent['name']}")
                created += 1

            results[agent_id] = page_id
            time.sleep(0.35)  # Notion rate limit: ~3 req/s

        except Exception as e:
            log.error(f"  FAILED   {agent_id} — {e}")
            failed += 1

    log.info(f"\nSync complete: {created} created, {updated} updated, {failed} failed")
    return results


def write_back_page_ids(yaml_data: dict, page_id_map: dict, yaml_path: str):
    """sync 결과로 얻은 notion_page_id를 YAML에 기록"""
    for agent in yaml_data.get("agents", []):
        agent_id = agent["agent_id"]
        if agent_id in page_id_map:
            agent["notion_page_id"] = page_id_map[agent_id]
    save_yaml(yaml_data, yaml_path)
    log.info(f"Write-back complete → {yaml_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="Sync agents/agent_index.yaml → Notion Agent Index DB")
    parser.add_argument("--yaml", default="agents/agent_index.yaml", help="Path to agent_index.yaml")
    parser.add_argument("--db-id", required=True, help="Notion Agent Index DB ID")
    parser.add_argument("--link-prompt-library", action="store_true",
                        help="Create relation to Prompt Library DB master page")
    parser.add_argument("--prompt-lib-page-id", default="",
                        help="Notion Prompt Library master page ID for relation")
    parser.add_argument("--write-back", action="store_true",
                        help="Write notion_page_id back to agent_index.yaml")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without executing")
    return parser.parse_args()


def main():
    args = parse_args()

    notion_token = os.environ.get("NOTION_API_KEY")
    if not notion_token:
        log.error("NOTION_API_KEY environment variable not set")
        sys.exit(1)

    yaml_path = Path(args.yaml)
    if not yaml_path.exists():
        log.error(f"YAML file not found: {yaml_path}")
        sys.exit(1)

    yaml_data = load_yaml(str(yaml_path))
    agents = yaml_data.get("agents", [])
    log.info(f"Loaded {len(agents)} agents from {yaml_path}")

    if args.dry_run:
        for a in agents:
            log.info(f"  [DRY-RUN] Would upsert: {a['agent_id']} — {a['name']}")
        return

    client = NotionClient(notion_token)

    # Validate DB exists
    try:
        db_info = client.get_db_schema(args.db_id)
        log.info(f"Connected to Notion DB: {db_info.get('title', [{}])[0].get('text', {}).get('content', args.db_id)}")
    except Exception as e:
        log.error(f"Cannot connect to Notion DB {args.db_id}: {e}")
        sys.exit(1)

    # Sync
    prompt_lib_page_id = args.prompt_lib_page_id or \
        yaml_data.get("metadata", {}).get("prompt_library_db_id", "")

    page_id_map = sync_agents(
        client=client,
        db_id=args.db_id,
        agents=agents,
        link_prompt_library=args.link_prompt_library,
        prompt_lib_page_id=prompt_lib_page_id,
    )

    # Update YAML metadata with DB ID
    if "metadata" in yaml_data:
        yaml_data["metadata"]["notion_db_id"] = args.db_id

    # Write-back page IDs to YAML
    if args.write_back:
        write_back_page_ids(yaml_data, page_id_map, str(yaml_path))

    # Print summary
    print("\n" + "=" * 60)
    print(f"AGENT INDEX SYNC SUMMARY")
    print("=" * 60)
    print(f"Total agents processed : {len(agents)}")
    print(f"Successfully synced     : {len(page_id_map)}")
    print(f"Notion DB ID           : {args.db_id}")
    print(f"YAML path              : {yaml_path}")
    if args.link_prompt_library:
        print(f"Prompt Library linked  : {prompt_lib_page_id}")
    print("=" * 60)


if __name__ == "__main__":
    main()
