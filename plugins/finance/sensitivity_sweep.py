#!/usr/bin/env python3
"""
PE-7 P2-4: Sensitivity Sweep
==============================
irr_shock_pp \u00b12pp 루프 — 모든 시나리오\u00d7타입 조합에대해
{base-2pp, base-1pp, base, base+1pp, base+2pp} IRR을 충격하고
 MOIC / NPV / 자본론 유입 변화를 측정 → Notion DB 자동 업로드.

Usage:
  python sensitivity_sweep.py                              # 기본 (\u00b12pp, 단계=1pp)
  python sensitivity_sweep.py --shock_range 3 --step 0.5  # \u00b13pp, 0.5pp 단계
  python sensitivity_sweep.py --scenarios balanced         # 특정 시나리오만
  python sensitivity_sweep.py --no-notion                  # Notion 업로드 스킵
  python sensitivity_sweep.py --dry-run                    # 실행만, 업로드 안 함

Environment:
  NOTION_TOKEN : Notion Integration Token
  NOTION_DB_ID : Reports DB (default: c74b578b-2092-4ace-b590-59dffe37633f)
"""

import argparse
import json
import math
import os
import subprocess
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

try:
    import numpy as np
except ImportError:
    print("[ERROR] numpy 필요: pip install numpy")
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("[ERROR] pyyaml 필요: pip install pyyaml")
    sys.exit(1)

try:
    import requests
except ImportError:
    requests = None  # Notion 엁로드 스킵 시 허용

# ────────────────────────────────────────
DEFAULT_CONFIG = "plugins/finance/finance_config.yaml"
DEFAULT_OUTPUT = "reports/sensitivity"
NOTION_API     = "https://api.notion.com/v1"
NOTION_VER     = "2022-06-28"
DEFAULT_DB     = "c74b578b-2092-4ace-b590-59dffe37633f"
CACHE_FILE     = Path("reports/.notion_sweep_cache.json")

SCENARIO_LABEL = {
    "balanced":     "Balanced",
    "conservative": "Conservative",
    "aggressive":   "Aggressive",
    "geo_hedge":    "Geo-Hedge",
}
TYPE_LABEL = {
    "type_a": "A(Glass 수직통합)",
    "type_b": "B(패키징 레버리지)",
    "type_c": "C(US/EU 분산)",
}


# ────────────────────────────────────────
# 수학 함수 (cowork_finance_runner 복사 안 하도록 인라인)
def calc_irr(cash_flows: list, max_iter=1000, tol=1e-8) -> float:
    rate = 0.10
    for _ in range(max_iter):
        npv   = sum(cf / (1 + rate) ** t for t, cf in enumerate(cash_flows))
        d_npv = sum(-t * cf / (1 + rate) ** (t + 1) for t, cf in enumerate(cash_flows))
        if abs(d_npv) < 1e-12:
            break
        rate -= npv / d_npv
        if abs(npv) < tol:
            break
    return rate


def calc_npv(cash_flows: list, discount_rate: float) -> float:
    return sum(cf / (1 + discount_rate) ** t for t, cf in enumerate(cash_flows))


def build_cash_flows(investment_M: float, irr_base: float,
                     projection_years: int, vintage_year: int) -> list:
    invested = investment_M * 1e6
    deploy   = [0.40, 0.35, 0.25]
    cfs = []
    for y in range(projection_years + 1):
        if y <= 2:
            cf = -invested * deploy[y]
        elif y <= 5:
            cf = invested * (1 + irr_base) ** y * 0.15
        else:
            cf = invested * (1 + irr_base) ** projection_years * 0.45
        cfs.append(round(cf / 1e6, 4))
    return cfs


# ────────────────────────────────────────
# ±pp Shock 적용
def apply_shock(irr_base: float, shock_pp: float) -> float:
    """irr_base에 shock_pp (%p) 적용. 0 미만 클립."""
    shocked = irr_base + shock_pp / 100.0
    return max(shocked, 0.0)  # 음수 IRR 미허용


# ────────────────────────────────────────
# 실제 Sweep 실행
def run_sweep(
    cfg: dict,
    selected_scenarios: list,
    shock_range: float,
    step: float,
) -> list:
    """
    Returns: list of row dicts
    [
      {
        scenario, type_key, shock_pp,
        irr_base, irr_shocked,
        npv_base_M, npv_shocked_M, delta_npv_M,
        moic_base, moic_shocked,
        hurdle_ok (bool: irr_shocked > 8%)
      }, ...
    ]
    """
    global_cfg    = cfg["global"]
    portfolio_cfg = cfg["portfolio"]
    scenarios_cfg = cfg["scenarios"]
    discount_rate = global_cfg["discount_rate"]
    proj_years    = global_cfg["projection_years"]
    vintage_year  = global_cfg["base_year"]

    # shock 포인트 생성: -shock_range ~ +shock_range (inclusive), step 단위
    n_steps = int(shock_range / step)
    shock_points = [round(-shock_range + i * step, 4) for i in range(2 * n_steps + 1)]

    rows = []
    for scen_key in selected_scenarios:
        if scen_key not in scenarios_cfg:
            print(f"[WARN] scenario '{scen_key}' not found")
            continue
        scen = scenarios_cfg[scen_key]
        alloc         = scen["allocations"]
        irr_assum     = scen["irr_assumptions"]
        moic_targets  = scen["moic_targets"]

        for type_key in ["type_a", "type_b", "type_c"]:
            inv_M    = portfolio_cfg["total_fund_size_M"] * alloc[type_key]
            irr_base = irr_assum[type_key]["base"]

            # Base 현금흐름
            cfs_base  = build_cash_flows(inv_M, irr_base, proj_years, vintage_year)
            npv_base  = calc_npv(cfs_base, discount_rate)
            proceeds_base = sum(cf for cf in cfs_base if cf > 0)
            moic_base = proceeds_base / inv_M if inv_M else 0

            for shock_pp in shock_points:
                irr_shocked = apply_shock(irr_base, shock_pp)
                cfs_shocked = build_cash_flows(inv_M, irr_shocked, proj_years, vintage_year)
                npv_shocked = calc_npv(cfs_shocked, discount_rate)
                proceeds_shocked = sum(cf for cf in cfs_shocked if cf > 0)
                moic_shocked = proceeds_shocked / inv_M if inv_M else 0

                # IRR 직접 쪼 유효성 코멘트
                try:
                    irr_calc = calc_irr(cfs_shocked)
                except Exception:
                    irr_calc = irr_shocked

                rows.append({
                    "scenario":       scen_key,
                    "scenario_label": SCENARIO_LABEL.get(scen_key, scen_key),
                    "type_key":       type_key,
                    "type_label":     TYPE_LABEL.get(type_key, type_key),
                    "investment_M":   round(inv_M, 2),
                    "shock_pp":       shock_pp,
                    "shock_label":    f"{'+' if shock_pp >= 0 else ''}{shock_pp:+.1f}pp",
                    "irr_base_pct":   round(irr_base * 100, 2),
                    "irr_shocked_pct": round(irr_shocked * 100, 2),
                    "irr_calc_pct":   round(irr_calc * 100, 2),
                    "npv_base_M":     round(npv_base, 2),
                    "npv_shocked_M":  round(npv_shocked, 2),
                    "delta_npv_M":    round(npv_shocked - npv_base, 2),
                    "moic_base":      round(moic_base, 3),
                    "moic_shocked":   round(moic_shocked, 3),
                    "delta_moic":     round(moic_shocked - moic_base, 3),
                    "hurdle_ok":      irr_shocked >= 0.08,   # 8% 허들
                    "hurdle_20_ok":   irr_shocked >= 0.20,   # PE 벤치마크
                })

    return rows


# ────────────────────────────────────────
# Notion 헬퍼
def get_git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "unknown"


def notion_headers(token: str) -> dict:
    return {
        "Authorization":  f"Bearer {token}",
        "Notion-Version": NOTION_VER,
        "Content-Type":   "application/json",
    }


def load_cache() -> dict:
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=2, ensure_ascii=False))


def build_notion_props(row: dict, commit: str) -> dict:
    """
    Sensitivity 행 1개 → Notion property dict
    Report Name 패턴: [Scenario]_[Type]_IRR[shock_label]
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    report_name = (
        f"SWEEP_{row['scenario_label']}_{row['type_key'].upper()}"
        f"_IRR{row['shock_label']}"
    )
    hurdle_note = "✔ Hurdle OK" if row["hurdle_ok"] else "⚠️ Below Hurdle"
    pe_note = " | ✅ PE 20% OK" if row["hurdle_20_ok"] else " | 🔴 Below 20%"
    notes = (
        f"IRR {row['irr_base_pct']:.1f}% → {row['irr_shocked_pct']:.1f}% "
        f"| MOIC Δ{row['delta_moic']:+.3f} "
        f"| NPV Δ{row['delta_npv_M']:+.1f}M "
        f"| {hurdle_note}{pe_note}"
    )

    return {
        "Report Name": {
            "title": [{"text": {"content": report_name}}]
        },
        "Version": {
            "rich_text": [{"text": {"content": f"sweep-{row['shock_label']}"}}]
        },
        "Type": {
            "select": {"name": "JSON"}
        },
        "Scenario": {
            "multi_select": [{"name": row["scenario_label"]}]
        },
        "Status": {
            "select": {"name": "Generated"}
        },
        "Config Version": {
            "rich_text": [{"text": {"content": f"{row['type_label']} | shock={row['shock_label']}"}}]
        },
        "Portfolio MOIC": {
            "rich_text": [{"text": {"content": f"{row['moic_shocked']:.3f}x (base: {row['moic_base']:.3f}x)"}}]
        },
        "IRR Base A": {
            "rich_text": [{"text": {"content":
                f"{row['irr_shocked_pct']:.1f}%" if row["type_key"]=="type_a" else "-"
            }}]
        },
        "IRR Base B": {
            "rich_text": [{"text": {"content":
                f"{row['irr_shocked_pct']:.1f}%" if row["type_key"]=="type_b" else "-"
            }}]
        },
        "IRR Base C": {
            "rich_text": [{"text": {"content":
                f"{row['irr_shocked_pct']:.1f}%" if row["type_key"]=="type_c" else "-"
            }}]
        },
        "Fund Size M": {
            "rich_text": [{"text": {"content": f"${row['investment_M']:.0f}M"}}]
        },
        "Generated At": {
            "date": {"start": today}
        },
        "GitHub Commit": {
            "rich_text": [{"text": {"content": commit}}]
        },
        "Notes": {
            "rich_text": [{"text": {"content": notes}}]
        },
    }


def upsert_notion_row(
    token: str, db_id: str,
    row: dict, commit: str, cache: dict
) -> str:
    cache_key = (
        f"{db_id}::{row['scenario_label']}_"
        f"{row['type_key']}_{row['shock_label']}"
    )
    props = build_notion_props(row, commit)

    if cache_key in cache:
        page_id  = cache[cache_key]
        url      = f"{NOTION_API}/pages/{page_id}"
        resp     = requests.patch(url,
                                  headers=notion_headers(token),
                                  json={"properties": props})
    else:
        url      = f"{NOTION_API}/pages"
        body     = {
            "parent":     {"database_id": db_id},
            "properties": props,
            "icon":       {"type": "emoji", "emoji": "📈"},
        }
        resp = requests.post(url, headers=notion_headers(token), json=body)

    resp.raise_for_status()
    result   = resp.json()
    page_id  = result.get("id", "")
    page_url = result.get("url", "")
    cache[cache_key] = page_id
    return page_url


# ────────────────────────────────────────
# JSON 출력
def save_sweep_json(rows: list, output_dir: str, shock_range: float, step: float):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    fname = out / f"sweep_irr_shock_{ts}.json"

    payload = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "shock_range_pp": shock_range,
            "step_pp": step,
            "total_rows": len(rows),
        },
        "rows": rows,
    }
    fname.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"\n[SAVE] Sweep JSON 저장: {fname}")
    return str(fname)


# ────────────────────────────────────────
# 콘솔 요약 테이블
def print_summary(rows: list, shock_range: float):
    print(f"\n{'='*70}")
    print(f"PE-7 Sensitivity Sweep Summary (±{shock_range}pp)")
    print(f"{'='*70}")
    print(f"{'Scenario':<14} {'Type':<8} {'Shock':>8} "
          f"{'IRR%':>7} {'MOIC':>7} {'\u0394MOIC':>8} "
          f"{'\u0394NPV_M':>9} {'Hurdle':>7}")
    print("-" * 70)

    # base row만 표시 (shock==0)
    base_rows = [r for r in rows if r["shock_pp"] == 0.0]
    for r in base_rows:
        print(
            f"{r['scenario_label']:<14} "
            f"{r['type_key'].upper():<8} "
            f"{'BASE':>8} "
            f"{r['irr_base_pct']:>6.1f}% "
            f"{r['moic_base']:>7.3f} "
            f"{'---':>8} "
            f"{'---':>9} "
            f"{'✔' if r['hurdle_ok'] else '⚠':>7}"
        )

    print()
    # 추가 shock extremes
    for scen in set(r["scenario_label"] for r in rows):
        for typ in ["type_a", "type_b", "type_c"]:
            for shock in [-shock_range, shock_range]:
                target = [r for r in rows
                          if r["scenario_label"]==scen
                          and r["type_key"]==typ
                          and abs(r["shock_pp"]-shock) < 0.01]
                if not target:
                    continue
                r = target[0]
                print(
                    f"{r['scenario_label']:<14} "
                    f"{r['type_key'].upper():<8} "
                    f"{r['shock_label']:>8} "
                    f"{r['irr_shocked_pct']:>6.1f}% "
                    f"{r['moic_shocked']:>7.3f} "
                    f"{r['delta_moic']:>+8.3f} "
                    f"{r['delta_npv_M']:>+9.1f} "
                    f"{'✔' if r['hurdle_ok'] else '⚠':>7}"
                )
    print("="*70)

    # Hurdle 충족 통계
    total = len(rows)
    hurdle_ok = sum(1 for r in rows if r["hurdle_ok"])
    pe20_ok   = sum(1 for r in rows if r["hurdle_20_ok"])
    print(f"\n[Hurdle 8%]  {hurdle_ok}/{total} rows ({hurdle_ok/total*100:.1f}%) OK")
    print(f"[Hurdle 20%] {pe20_ok}/{total} rows ({pe20_ok/total*100:.1f}%) OK")


# ────────────────────────────────────────
# Notion 업로드 루프
def upload_all_to_notion(
    rows: list, token: str, db_id: str,
    batch_size: int = 10, delay: float = 0.3
):
    import time
    commit = get_git_commit()
    cache  = load_cache()
    total  = len(rows)
    ok     = 0
    failed = []

    print(f"\n[📊 Notion] {total}개 행 업로드 시작...")
    for i, row in enumerate(rows):
        try:
            page_url = upsert_notion_row(token, db_id, row, commit, cache)
            ok += 1
            label = f"{row['scenario_label']}/{row['type_key']}/{row['shock_label']}"
            print(f"  [{i+1:03d}/{total}] ✔ {label} -> {page_url}")
        except Exception as e:
            failed.append({"row": row, "error": str(e)})
            print(f"  [{i+1:03d}/{total}] ⚠ FAIL: {e}")

        # batch 대기 (레이트리미트 방지)
        if (i + 1) % batch_size == 0:
            time.sleep(delay)

    save_cache(cache)
    print(f"\n[📊 Notion] 완료: {ok}/{total} 성공")
    if failed:
        fail_path = Path("reports/sweep_notion_failed.json")
        fail_path.write_text(json.dumps(failed, indent=2, ensure_ascii=False))
        print(f"[WARN] 실패 {len(failed)}개 -> {fail_path}")
    return ok, failed


# ────────────────────────────────────────
# 메인
def main():
    parser = argparse.ArgumentParser(description="PE-7 Sensitivity Sweep")
    parser.add_argument("--config",      default=DEFAULT_CONFIG)
    parser.add_argument("--output",      default=DEFAULT_OUTPUT,
                        help="출력 디렉토리 (JSON 저장 위치)")
    parser.add_argument("--shock_range", type=float, default=2.0,
                        help="\u00b1pp 범위 (default=2.0)")
    parser.add_argument("--step",        type=float, default=1.0,
                        help="shock 단계 pp (default=1.0)")
    parser.add_argument("--scenarios",   default="all",
                        help="comma-separated 시나리오 or 'all'")
    parser.add_argument("--no-notion",   action="store_true",
                        help="Notion 업로드 스킵")
    parser.add_argument("--dry-run",     action="store_true",
                        help="쪼만 하고 저장/업로드 안 함")
    parser.add_argument("--db",          default="",
                        help="Notion DB ID override")
    args = parser.parse_args()

    # 1) Config 로드
    cfg_path = Path(args.config)
    if not cfg_path.exists():
        print(f"[ERROR] Config 없음: {cfg_path}")
        sys.exit(1)
    with open(cfg_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # 2) 시나리오 선택
    all_scen = list(cfg["scenarios"].keys())
    if args.scenarios == "all":
        selected = all_scen
    else:
        selected = [s.strip() for s in args.scenarios.split(",")]

    print(f"📊 PE-7 Sensitivity Sweep 시작")
    print(f"   Config  : {cfg_path}")
    print(f"   Shock   : \u00b1{args.shock_range}pp (step={args.step}pp)")
    print(f"   Scenario: {selected}")

    # 3) Sweep 실행
    rows = run_sweep(cfg, selected, args.shock_range, args.step)
    print(f"   → {len(rows)}개 rows 생성 "
          f"({len(selected)} scenarios x 3 types x "
          f"{int(2*args.shock_range/args.step)+1} shock pts)")

    # 4) 콘솔 요약
    print_summary(rows, args.shock_range)

    if args.dry_run:
        print("\n[DRY-RUN] 저장/업로드 안 함. 종료.")
        return 0

    # 5) JSON 저장
    json_path = save_sweep_json(rows, args.output, args.shock_range, args.step)

    # 6) Notion 업로드
    if args.no_notion:
        print("[--no-notion] Notion 업로드 스킵.")
        return 0

    if requests is None:
        print("[WARN] requests 미설치 — Notion 업로드 불가. pip install requests")
        return 0

    token = os.environ.get("NOTION_TOKEN", "")
    if not token:
        print("[WARN] NOTION_TOKEN 미설정 — Notion 업로드 스킵.")
        return 0

    db_id = args.db or os.environ.get("NOTION_DB_ID", DEFAULT_DB)
    upload_all_to_notion(rows, token, db_id)

    print("\n✔ Sensitivity Sweep 완료")
    return 0


if __name__ == "__main__":
    sys.exit(main())
