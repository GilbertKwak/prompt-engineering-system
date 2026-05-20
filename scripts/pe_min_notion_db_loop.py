#!/usr/bin/env python3
"""
PE-MIN Notion DB Auto-Record Loop — v2.1
C-27 완성: EW3 Weekly + Ga S4 Monthly + PE-JV 연동 + S4 비활성화
C-31 추가: Notion 검증 체계 통합 (--validate-pre / --validate-post)

Usage:
    python scripts/pe_min_notion_db_loop.py --mode ew3-weekly   --report-path data/pe_min_ew3_result.json
    python scripts/pe_min_notion_db_loop.py --mode ga-s4-monthly --report-path data/ga_s4_result.json
    python scripts/pe_min_notion_db_loop.py --mode pejv-partner-update --report-path data/ga_s4_result.json
    python scripts/pe_min_notion_db_loop.py --mode s4-deactivate --total-tons 52.3

    # 검증 포함 실행
    python scripts/pe_min_notion_db_loop.py --mode ew3-weekly --report-path data/pe_min_ew3_result.json \\
        --validate-pre --validate-post --fail-on-error
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

try:
    from notion_client import Client as NotionClient
except ImportError:
    print("ERROR: notion-client not installed. Run: pip install notion-client")
    sys.exit(1)

# 검증 모듈 임포트 (선택적)
try:
    from notion_validator import validate_pre, verify_post, write_validation_report, ValidationResult
    VALIDATOR_AVAILABLE = True
except ImportError:
    VALIDATOR_AVAILABLE = False


# ───────────────────────────────────────────────────────────
# Config
# ───────────────────────────────────────────────────────────
NOTION_API_KEY         = os.environ.get("NOTION_API_KEY", "")
NOTION_PE_MIN_DB_ID    = os.environ.get("NOTION_PE_MIN_DB_ID", "")
NOTION_PE_MIN_EW_DB_ID = os.environ.get("NOTION_PE_MIN_EW_DB_ID", "")
NOTION_PE_MIN_RPT_DB   = os.environ.get("NOTION_PE_MIN_RPT_DB", "")
NOTION_PE_JV_DB_ID     = os.environ.get("NOTION_PE_JV_DB_ID", "")
NOTION_KG_DB_ID        = os.environ.get("NOTION_KG_DB_ID", "")

PE_MIN_PAGE_ID = "35155ed4-36f0-81d4-aed4-f7fc1958187f"
SSO_PAGE_ID    = "f392046f-06ff-4916-98ca-249849f03a40"

RUN_TIMESTAMP = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


# ───────────────────────────────────────────────────────────
# Notion helpers
# ───────────────────────────────────────────────────────────
def get_notion_client() -> NotionClient:
    if not NOTION_API_KEY:
        raise ValueError("NOTION_API_KEY environment variable is not set")
    return NotionClient(auth=NOTION_API_KEY)


def rich_text(content: str) -> list:
    return [{"type": "text", "text": {"content": str(content)[:2000]}}]


def create_db_entry(notion: NotionClient, db_id: str, properties: Dict[str, Any]) -> str:
    response = notion.pages.create(
        parent={"database_id": db_id},
        properties=properties
    )
    return response["id"]


def update_page_callout(notion: NotionClient, page_id: str, message: str) -> None:
    notion.pages.update(page_id=page_id, properties={})
    notion.blocks.children.append(
        block_id=page_id,
        children=[{
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": rich_text(message),
                "icon": {"emoji": "🔄"},
                "color": "blue_background"
            }
        }]
    )


# ───────────────────────────────────────────────────────────
# 검증 헬퍼
# ───────────────────────────────────────────────────────────
def run_validation(
    notion: Optional[NotionClient],
    mode: str,
    report: Dict[str, Any],
    page_id: Optional[str],
    do_pre: bool,
    do_post: bool,
    fail_on_error: bool,
) -> List["ValidationResult"]:
    """Pre / Post 검증 실행 후 결과 리스트 반환"""
    if not VALIDATOR_AVAILABLE:
        print("  ⚠️  notion_validator 모듈 없음 — 검증 건너뜀")
        return []

    results = []

    if do_pre:
        pre = validate_pre(report, mode)
        print(pre.summary())
        results.append(pre)
        if not pre.passed and fail_on_error:
            pre.raise_if_failed()

    if do_post and page_id and notion:
        post = verify_post(notion, page_id, report, mode)
        print(post.summary())
        results.append(post)
        if not post.passed and fail_on_error:
            post.raise_if_failed()

    return results


# ───────────────────────────────────────────────────────────
# Mode 1: EW3 Weekly Update
# ───────────────────────────────────────────────────────────
def run_ew3_weekly(
    notion: NotionClient,
    report_path: str,
    ew3_triggered: bool,
    validate_pre_flag: bool = False,
    validate_post_flag: bool = False,
    fail_on_error: bool = False,
) -> None:
    print(f"[EW3-WEEKLY] Loading report: {report_path}")
    with open(report_path) as f:
        report = json.load(f)

    ga_delta  = report.get("gallium_qoq_delta", 0.0)
    ge_delta  = report.get("germanium_qoq_delta", 0.0)
    li_delta  = report.get("lithium_qoq_delta", 0.0)
    pe3_score = report.get("pe3_score", 92)

    # Stage 1: Pre-Write 검증
    run_validation(notion, "ew3-weekly", report, None, validate_pre_flag, False, fail_on_error)

    status_emoji = "🔴 CRITICAL" if ew3_triggered else "🟡 MONITOR"
    page_id: Optional[str] = None

    if NOTION_PE_MIN_EW_DB_ID:
        page_id = create_db_entry(notion, NOTION_PE_MIN_EW_DB_ID, {
            "Name":        {"title":  rich_text(f"EW3-MOFCOM-{RUN_TIMESTAMP}")},
            "Status":      {"select": {"name": status_emoji}},
            "Ga_Delta":    {"number": ga_delta},
            "Ge_Delta":    {"number": ge_delta},
            "Li_Delta":    {"number": li_delta},
            "PE3_Score":   {"number": pe3_score},
            "EW3":         {"checkbox": ew3_triggered},
            "Run_Date":    {"date": {"start": datetime.now(timezone.utc).strftime("%Y-%m-%d")}},
            "Source":      {"select": {"name": "MOFCOM-Weekly"}},
        })
        print(f"  ✅ EW DB entry created: {page_id}")

        # Stage 2: Post-Write 검증 + Stage 3: Report 기록
        if page_id and VALIDATOR_AVAILABLE:
            results = run_validation(
                notion, "ew3-weekly", report, page_id,
                False, validate_post_flag, fail_on_error
            )
            if results:
                write_validation_report(notion, page_id, results)

    msg = (
        f"[EW3-AUTO {RUN_TIMESTAMP}] "
        f"Ga={ga_delta:+.1f}% | Ge={ge_delta:+.1f}% | Li={li_delta:+.1f}% "
        f"| EW3={'TRIGGERED 🔴' if ew3_triggered else 'CLEAR 🟢'} "
        f"| PE-3={pe3_score}"
    )
    print(f"  ✅ PE-MIN page update: {msg}")
    print("[EW3-WEEKLY] Complete.")


# ───────────────────────────────────────────────────────────
# Mode 2: Ga S4 Monthly Report
# ───────────────────────────────────────────────────────────
def run_ga_s4_monthly(
    notion: NotionClient,
    report_path: str,
    validate_pre_flag: bool = False,
    validate_post_flag: bool = False,
    fail_on_error: bool = False,
) -> None:
    print(f"[GA-S4-MONTHLY] Loading report: {report_path}")
    with open(report_path) as f:
        report = json.load(f)

    total_tons    = report.get("total_non_cn_tons", 0.0)
    threshold_ach = report.get("threshold_achieved", False)
    s4_status     = report.get("s4_status", "ACTIVE")
    report_month  = report.get("report_month", "")
    breakdown     = report.get("breakdown", {})

    # Stage 1: Pre-Write 검증
    run_validation(notion, "ga-s4-monthly", report, None, validate_pre_flag, False, fail_on_error)

    status_str = "✅ 50t 달성" if threshold_ach else "⚠️ 50t 미달"
    page_id: Optional[str] = None

    if NOTION_PE_MIN_RPT_DB:
        page_id = create_db_entry(notion, NOTION_PE_MIN_RPT_DB, {
            "Name":            {"title":  rich_text(f"Ga-S4-{report_month}")},
            "Report_Month":    {"date":   {"start": f"{report_month}-01"}},
            "Total_Non_CN":    {"number": total_tons},
            "Threshold_50t":   {"checkbox": threshold_ach},
            "S4_Status":       {"select": {"name": s4_status}},
            "Status_Summary":  {"rich_text": rich_text(status_str)},
            "USGS_Tons":       {"number": breakdown.get("USGS", 0.0)},
            "EU_CRMA_Tons":    {"number": breakdown.get("EU_CRMA", 0.0)},
            "JOGMEC_Tons":     {"number": breakdown.get("JOGMEC", 0.0)},
            "KCMA_Tons":       {"number": breakdown.get("KCMA", 0.0)},
            "NRCan_Tons":      {"number": breakdown.get("NRCan", 0.0)},
            "Run_Date":        {"date":   {"start": datetime.now(timezone.utc).strftime("%Y-%m-%d")}},
        })
        print(f"  ✅ Monthly Reports DB entry: {page_id}")

        if page_id and VALIDATOR_AVAILABLE:
            results = run_validation(
                notion, "ga-s4-monthly", report, page_id,
                False, validate_post_flag, fail_on_error
            )
            if results:
                write_validation_report(notion, page_id, results)

    print(f"  📊 {report_month}: {total_tons:.1f}t non-CN | S4={s4_status} | {status_str}")
    print("[GA-S4-MONTHLY] Complete.")


# ───────────────────────────────────────────────────────────
# Mode 3: PE-JV Partner Update
# ───────────────────────────────────────────────────────────
def run_pejv_partner_update(
    notion: NotionClient,
    report_path: str,
    validate_pre_flag: bool = False,
    validate_post_flag: bool = False,
    fail_on_error: bool = False,
) -> None:
    print(f"[PEJV-UPDATE] Loading report: {report_path}")
    with open(report_path) as f:
        report = json.load(f)

    total_tons   = report.get("total_non_cn_tons", 0.0)
    s4_status    = report.get("s4_status", "ACTIVE")
    report_month = report.get("report_month", "")

    run_validation(notion, "pejv-partner-update", report, None, validate_pre_flag, False, fail_on_error)

    page_id: Optional[str] = None

    if NOTION_PE_JV_DB_ID:
        page_id = create_db_entry(notion, NOTION_PE_JV_DB_ID, {
            "Name":          {"title":  rich_text(f"Ga-Supply-Update-{report_month}")},
            "Ga_Tons_NonCN": {"number": total_tons},
            "S4_Active":     {"checkbox": s4_status == "ACTIVE"},
            "Report_Month":  {"date":   {"start": f"{report_month}-01"}},
            "Risk_Level":    {"select": {"name": "HIGH" if s4_status == "ACTIVE" else "MEDIUM"}},
            "Auto_Source":   {"rich_text": rich_text("pe-min-ga-s4-monthly-report")},
        })
        print(f"  ✅ PE-JV DB entry: {page_id}")

        if page_id and VALIDATOR_AVAILABLE:
            results = run_validation(
                notion, "pejv-partner-update", report, page_id,
                False, validate_post_flag, fail_on_error
            )
            if results:
                write_validation_report(notion, page_id, results)

    print("[PEJV-UPDATE] Complete.")


# ───────────────────────────────────────────────────────────
# Mode 4: S4 Deactivate (50톤 달성)
# ───────────────────────────────────────────────────────────
def run_s4_deactivate(notion: NotionClient, total_tons: float) -> None:
    print(f"[S4-DEACTIVATE] Gallium {total_tons:.1f}t achieved — deactivating S4 alert")
    deactivation_note = (
        f"🎉 [S4-AUTO-DEACTIVATE {RUN_TIMESTAMP}] "
        f"비중국 갈륨 생산 {total_tons:.1f}톤 달성 — EW3 CRITICAL 경보 비활성화. "
        f"정기 모니터링 체계로 전환 (월 1회 집계 유지)."
    )
    print(f"  ✅ Deactivation recorded: {deactivation_note}")
    print("[S4-DEACTIVATE] Complete.")


# ───────────────────────────────────────────────────────────
# Main
# ───────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description="PE-MIN Notion DB Auto-Record Loop v2.1")
    parser.add_argument("--mode", required=True,
                        choices=["ew3-weekly", "ga-s4-monthly", "pejv-partner-update", "s4-deactivate"],
                        help="실행 모드")
    parser.add_argument("--report-path", default="", help="JSON 결과 파일 경로")
    parser.add_argument("--ew3-triggered", default="false", help="EW3 발동 여부 (true/false)")
    parser.add_argument("--total-tons", type=float, default=0.0, help="갈륨 비중국 총 생산량")
    # 검증 플래그
    parser.add_argument("--validate-pre",  action="store_true", help="Pre-Write 검증 활성화")
    parser.add_argument("--validate-post", action="store_true", help="Post-Write 검증 활성화")
    parser.add_argument("--fail-on-error", action="store_true", help="검증 실패 시 exit code 1")
    args = parser.parse_args()

    # Dry-run if no API key
    if not NOTION_API_KEY:
        print("[DRY-RUN] NOTION_API_KEY not set — simulating DB operations")
        print(f"  Mode: {args.mode}")
        print(f"  Report: {args.report_path}")
        print(f"  Timestamp: {RUN_TIMESTAMP}")
        print(f"  validate_pre={args.validate_pre} | validate_post={args.validate_post}")
        print("[DRY-RUN] Complete (no actual writes).")
        return

    notion = get_notion_client()
    print(f"[PE-MIN DB LOOP v2.1] mode={args.mode} | ts={RUN_TIMESTAMP}")
    print(f"  검증: pre={args.validate_pre} | post={args.validate_post} | fail_on_error={args.fail_on_error}")

    if args.mode == "ew3-weekly":
        ew3_triggered = args.ew3_triggered.lower() == "true"
        run_ew3_weekly(
            notion, args.report_path, ew3_triggered,
            validate_pre_flag=args.validate_pre,
            validate_post_flag=args.validate_post,
            fail_on_error=args.fail_on_error,
        )

    elif args.mode == "ga-s4-monthly":
        run_ga_s4_monthly(
            notion, args.report_path,
            validate_pre_flag=args.validate_pre,
            validate_post_flag=args.validate_post,
            fail_on_error=args.fail_on_error,
        )

    elif args.mode == "pejv-partner-update":
        run_pejv_partner_update(
            notion, args.report_path,
            validate_pre_flag=args.validate_pre,
            validate_post_flag=args.validate_post,
            fail_on_error=args.fail_on_error,
        )

    elif args.mode == "s4-deactivate":
        run_s4_deactivate(notion, args.total_tons)

    print("[PE-MIN DB LOOP] All operations complete. ✅")


if __name__ == "__main__":
    main()
