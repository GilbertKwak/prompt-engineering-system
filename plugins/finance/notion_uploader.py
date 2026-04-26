#!/usr/bin/env python3
"""
PE-7 P2-3: Notion Auto-Uploader
================================
finance_output JSON 데이터를 읽어
 Notion 「📊 PE-7 Finance Reports DB」에 메타데이터를 Upsert합니다.

지원 상태:
  Step 1 완료 후 → Status = "Pending Approval"
  Step 2 완료 후 → Status = "Generated"
  Step 실패   → Status = "Failed"

Usage:
  # Step 1 완료 후 (Pending Approval 기록)
  python notion_uploader.py --json reports/finance_output_v1.1.json \\
                             --status "Pending Approval"

  # Step 2 완료 후 (Generated 로 업데이트)
  python notion_uploader.py --json reports/finance_output_v1.1.json \\
                             --xlsx reports/AstraChips_Finance_Model_v1.1.xlsx \\
                             --status "Generated"

  # 실패 기록
  python notion_uploader.py --json reports/finance_output_v1.1.json \\
                             --status "Failed" --notes "실패 사유"

Environment Variables:
  NOTION_TOKEN : Notion Integration Token (required)
  NOTION_DB_ID : Data Source ID (default: c74b578b-2092-4ace-b590-59dffe37633f)
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("[ERROR] requests 패키지 필요: pip install requests")
    sys.exit(1)

# ────────────────────────────────────────
NOTION_API   = "https://api.notion.com/v1"
NOTION_VER   = "2022-06-28"
DEFAULT_DB   = "c74b578b-2092-4ace-b590-59dffe37633f"   # PE-7 Finance Reports DB
NOTION_HUB   = "34855ed436f081219806e8ca4210eb26"         # AstraChips 허브

# 레코드 ID 캐시 (중복 upsert 용)
RECORD_CACHE = Path("reports/.notion_record_cache.json")


# ────────────────────────────────────────
def get_token() -> str:
    token = os.environ.get("NOTION_TOKEN", "")
    if not token:
        raise EnvironmentError(
            "NOTION_TOKEN 환경변수가 설정되지 않았습니다.\n"
            "export NOTION_TOKEN='secret_xxxx'"
        )
    return token


def notion_headers(token: str) -> dict:
    return {
        "Authorization":  f"Bearer {token}",
        "Notion-Version": NOTION_VER,
        "Content-Type":   "application/json",
    }


# ────────────────────────────────────────
# JSON 데이터 로드
def load_json(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"JSON 파일 없음: {path}")
    return json.loads(p.read_text(encoding="utf-8"))


# Git 코밋 SHA 자동 확인
def get_git_commit() -> str:
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return sha
    except Exception:
        return "unknown"


# XLSX 커버 사이즈 확인
def get_file_size(path: str) -> str:
    p = Path(path)
    if p.exists():
        kb = p.stat().st_size / 1024
        return f"{kb:.1f} KB"
    return "N/A"


# ────────────────────────────────────────
# Notion Properties 빌더
def build_properties(
    data: dict,
    report_name: str,
    file_type: str,
    status: str,
    xlsx_path: str,
    notes: str,
    commit: str,
) -> dict:
    """
    Notion Pages API 형식으로 properties dict 리턴.
    """
    # 시나리오에서 IRR/MOIC 추출 (JSON 구조 의존)
    scenarios = data.get("scenarios", {})
    balanced  = scenarios.get("balanced", {})
    irr       = balanced.get("irr_assumptions", {})
    moic      = balanced.get("moic_targets", {})
    portfolio = data.get("portfolio", {})

    irr_a = irr.get("type_a", {}).get("base", "N/A")
    irr_b = irr.get("type_b", {}).get("base", "N/A")
    irr_c = irr.get("type_c", {}).get("base", "N/A")

    # MOIC 가중 평균 계산
    alloc = balanced.get("allocations", {"type_a": 0.4, "type_b": 0.35, "type_c": 0.25})
    moic_portfolio = (
        moic.get("type_a", 0) * alloc.get("type_a", 0) +
        moic.get("type_b", 0) * alloc.get("type_b", 0) +
        moic.get("type_c", 0) * alloc.get("type_c", 0)
    )

    fund_size = portfolio.get("total_fund_size_M", 1000)
    config_ver = data.get("plugin", {}).get("version", "v1.1.0")
    scenario_keys = list(scenarios.keys())  # ["balanced", "conservative", ...]

    # Scenario multi-select 맵핑
    scenario_label_map = {
        "balanced":    "Balanced",
        "conservative": "Conservative",
        "aggressive":  "Aggressive",
        "geo_hedge":   "Geo-Hedge",
    }
    scenario_labels = [scenario_label_map.get(k, k) for k in scenario_keys]

    xlsx_size = get_file_size(xlsx_path) if xlsx_path else "N/A"
    today     = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    props = {
        "Report Name": {
            "title": [{"text": {"content": report_name}}]
        },
        "Version": {
            "rich_text": [{"text": {"content": "v1.1"}}]
        },
        "Type": {
            "select": {"name": file_type}
        },
        "Scenario": {
            "multi_select": [{"name": s} for s in scenario_labels]
        },
        "Status": {
            "select": {"name": status}
        },
        "Config Version": {
            "rich_text": [{"text": {"content": config_ver}}]
        },
        "Portfolio MOIC": {
            "rich_text": [{"text": {"content": f"{moic_portfolio:.2f}x"}}]
        },
        "IRR Base A": {
            "rich_text": [{"text": {"content": f"{float(irr_a)*100:.0f}%" if irr_a != 'N/A' else 'N/A'}}]
        },
        "IRR Base B": {
            "rich_text": [{"text": {"content": f"{float(irr_b)*100:.0f}%" if irr_b != 'N/A' else 'N/A'}}]
        },
        "IRR Base C": {
            "rich_text": [{"text": {"content": f"{float(irr_c)*100:.0f}%" if irr_c != 'N/A' else 'N/A'}}]
        },
        "Fund Size M": {
            "rich_text": [{"text": {"content": f"${fund_size}M"}}]
        },
        "Generated At": {
            "date": {"start": today}
        },
        "GitHub Commit": {
            "rich_text": [{"text": {"content": commit}}]
        },
        "Notes": {
            "rich_text": [{"text": {"content":
                notes or (
                    f"XLSX크기: {xlsx_size} | "
                    f"IRR(A/B/C): {irr_a}/{irr_b}/{irr_c} | "
                    f"PE-7 P2-3 자동업로드"
                )
            }}]
        },
    }
    return props


# ────────────────────────────────────────
# Notion API: 페이지 생성
def create_page(token: str, db_id: str, properties: dict) -> dict:
    url  = f"{NOTION_API}/pages"
    body = {
        "parent": {"database_id": db_id},
        "properties": properties,
        "icon": {"type": "emoji", "emoji": "📊"},
    }
    resp = requests.post(url, headers=notion_headers(token), json=body)
    resp.raise_for_status()
    return resp.json()


# Notion API: 페이지 업데이트 (upsert)
def update_page(token: str, page_id: str, properties: dict) -> dict:
    url  = f"{NOTION_API}/pages/{page_id}"
    body = {"properties": properties}
    resp = requests.patch(url, headers=notion_headers(token), json=body)
    resp.raise_for_status()
    return resp.json()


# ────────────────────────────────────────
# Cache 관리 (중복 Upsert)
def load_cache() -> dict:
    if RECORD_CACHE.exists():
        return json.loads(RECORD_CACHE.read_text())
    return {}


def save_cache(cache: dict):
    RECORD_CACHE.parent.mkdir(parents=True, exist_ok=True)
    RECORD_CACHE.write_text(json.dumps(cache, indent=2, ensure_ascii=False))


# ────────────────────────────────────────
# 메인 Upsert 로직
def upsert_report(
    token: str,
    db_id: str,
    data: dict,
    report_name: str,
    file_type: str,
    status: str,
    xlsx_path: str = "",
    notes: str = "",
    commit: str = "",
) -> str:
    """
    캐시에 page_id가 있으면 PATCH, 없으면 POST.
    반환: Notion 페이지 URL
    """
    cache     = load_cache()
    cache_key = f"{db_id}::{report_name}"
    props     = build_properties(data, report_name, file_type, status,
                                  xlsx_path, notes, commit)

    if cache_key in cache:
        page_id = cache[cache_key]
        print(f"[UPSERT] 업데이트 중: {report_name} (page_id={page_id})")
        result  = update_page(token, page_id, props)
        page_url = result.get("url", "")
    else:
        print(f"[UPSERT] 신규 생성: {report_name}")
        result   = create_page(token, db_id, props)
        page_id  = result.get("id", "")
        page_url = result.get("url", "")
        cache[cache_key] = page_id
        save_cache(cache)

    print(f"[OK] Notion 업로드 완료 -> {page_url}")
    return page_url


# ────────────────────────────────────────
# run_finance_pipeline.py 통합 휴크
def upload_from_pipeline(
    json_path: str,
    xlsx_path: str = "",
    status: str = "Pending Approval",
    notes: str = "",
):
    """
    pipeline에서 직접 호출할 수 있는 진입점.
    """
    token  = get_token()
    db_id  = os.environ.get("NOTION_DB_ID", DEFAULT_DB)
    data   = load_json(json_path)
    commit = get_git_commit()

    # Excel 레코드
    if xlsx_path:
        xlsx_name = Path(xlsx_path).name
        upsert_report(
            token=token, db_id=db_id, data=data,
            report_name=xlsx_name, file_type="Excel",
            status=status, xlsx_path=xlsx_path,
            notes=notes, commit=commit,
        )

    # JSON 레코드
    json_name = Path(json_path).name
    upsert_report(
        token=token, db_id=db_id, data=data,
        report_name=json_name, file_type="JSON",
        status=status, xlsx_path="",
        notes=notes, commit=commit,
    )


# ────────────────────────────────────────
# 메인
def main():
    parser = argparse.ArgumentParser(description="PE-7 Notion Uploader")
    parser.add_argument("--json",   required=True,  help="finance_output JSON 경로")
    parser.add_argument("--xlsx",   default="",     help="Excel 파일 경로 (optional)")
    parser.add_argument("--status", default="Pending Approval",
                        choices=["Generated", "Pending Approval", "Failed", "Archived"],
                        help="Notion Status 값")
    parser.add_argument("--notes",  default="",     help="선택적 메모")
    parser.add_argument("--db",     default="",     help="Notion DB ID (env 우선)")
    args = parser.parse_args()

    token = get_token()
    db_id = args.db or os.environ.get("NOTION_DB_ID", DEFAULT_DB)
    data  = load_json(args.json)
    commit = get_git_commit()

    if args.xlsx:
        xlsx_name = Path(args.xlsx).name
        print(f"\n▶ Excel 레코드 업로드: {xlsx_name}")
        upsert_report(
            token=token, db_id=db_id, data=data,
            report_name=xlsx_name, file_type="Excel",
            status=args.status, xlsx_path=args.xlsx,
            notes=args.notes, commit=commit,
        )

    json_name = Path(args.json).name
    print(f"\n▶ JSON 레코드 업로드: {json_name}")
    upsert_report(
        token=token, db_id=db_id, data=data,
        report_name=json_name, file_type="JSON",
        status=args.status, xlsx_path="",
        notes=args.notes, commit=commit,
    )

    print("\n✔ Notion 업로드 완료")


if __name__ == "__main__":
    main()
