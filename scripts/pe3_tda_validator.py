#!/usr/bin/env python3
"""
pe3_tda_validator.py  v1.0
TDA (Total Deal Attractiveness) 자동 판정 엔진

역할:
  - pe3_tda_checklist.yaml의 체크 로직을 실행
  - D6/D7/D8 입력값 → TDA 점수 계산 → 등급 판정
  - Notion DB에 결과 자동 기록

사용법:
  python scripts/pe3_tda_validator.py --page-id <notion_page_id> [--dry-run]
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from typing import Optional

import yaml

# ── Notion SDK (notion-client 패키지 필요) ──────────────────
try:
    from notion_client import Client as NotionClient
except ImportError:
    NotionClient = None

# ── 경로 설정 ───────────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECKLIST_PATH = os.path.join(ROOT, "config", "pe3_tda_checklist.yaml")


# ============================================================
# 1. 데이터 구조
# ============================================================
@dataclass
class TDAInput:
    """D6/D7/D8 입력값 컨테이너"""
    # D6 — IRR 역산
    irr_base: float = 0.0          # Base 시나리오 IRR (%)
    irr_bear: float = 0.0          # Bear 시나리오 IRR (%)
    entry_ev: float = 0.0          # 실제 Entry EV (억원)
    irr_entry_ev_cap: float = 0.0  # IRR 역산 EV 상한 (억원)
    irr_exit_sensitivity_ok: bool = False  # Exit ±1x 감응도 통과 여부
    target_irr: float = 20.0       # 목표 IRR (기본 20%)

    # D7 — Blue Ocean & NSM
    blue_ocean_score: float = 0.0  # 0~10점
    nsm_metric: str = ""           # North Star Metric 지표명
    nsm_target: str = ""           # NSM 목표값
    vanity_metric_warning: bool = False  # True면 허상 지표 경고

    # D8 — KPI 로드맵
    kpi_phase1: str = ""
    kpi_phase2: str = ""
    kpi_phase3: str = ""
    go_no_go_trigger: str = ""


@dataclass
class TDAResult:
    """판정 결과 컨테이너"""
    tda_score: float = 0.0
    grade: str = "D"
    passed_items: list = field(default_factory=list)
    failed_items: list = field(default_factory=list)
    failed_must_ids: list = field(default_factory=list)
    dimension_scores: dict = field(default_factory=dict)
    vanity_warning_text: str = ""
    irr_exit_sensitivity_summary: str = ""


# ============================================================
# 2. 체크 로직
# ============================================================
class TDAValidator:
    def __init__(self, checklist_path: str = CHECKLIST_PATH):
        with open(checklist_path, "r", encoding="utf-8") as f:
            self.spec = yaml.safe_load(f)
        self.grade_table = self.spec["grade_table"]
        self.must_override = self.spec["must_override"]["rules"]

    # ── 개별 항목 평가 ───────────────────────────────────────
    def _eval_item(self, item: dict, inp: TDAInput) -> bool:
        """eval 문자열을 Python 조건으로 안전하게 평가"""
        ctx = {
            "irr_base":               inp.irr_base,
            "irr_bear":               inp.irr_bear,
            "entry_ev":               inp.entry_ev,
            "irr_entry_ev_cap":       inp.irr_entry_ev_cap,
            "irr_exit_sensitivity_ok": inp.irr_exit_sensitivity_ok,
            "target_irr":             inp.target_irr,
            "blue_ocean_score":       inp.blue_ocean_score,
            "nsm_metric":             inp.nsm_metric,
            "nsm_target":             inp.nsm_target,
            "vanity_metric_warning":  inp.vanity_metric_warning,
            "kpi_phase1":             inp.kpi_phase1,
            "kpi_phase2":             inp.kpi_phase2,
            "kpi_phase3":             inp.kpi_phase3,
            "go_no_go_trigger":       inp.go_no_go_trigger,
            "true": True, "false": False,
        }
        try:
            return bool(eval(item["eval"], {"__builtins__": {}}, ctx))  # noqa: S307
        except Exception as e:
            print(f"  [WARN] eval 실패 ({item['id']}): {e}")
            return False

    # ── 전체 점수 계산 ───────────────────────────────────────
    def evaluate(self, inp: TDAInput) -> TDAResult:
        result = TDAResult()
        total_score = 0.0
        dim_scores = {}

        for dim_key, dim in self.spec["scoring"]["dimensions"].items():
            dim_score = 0.0
            for item in dim["sub_items"]:
                passed = self._eval_item(item, inp)
                pts = item["points"] if passed else 0
                dim_score += pts
                total_score += pts

                entry = f"{item['id']} [{item['level']}] {item['label']}"
                if passed:
                    result.passed_items.append(entry)
                else:
                    result.failed_items.append(entry)
                    if item["level"] == "MUST":
                        result.failed_must_ids.append(item["id"])

            dim_scores[dim_key] = round(dim_score, 1)

        result.tda_score = round(total_score, 1)
        result.dimension_scores = dim_scores

        # 보조 텍스트
        result.vanity_warning_text = "⚠️ 허상 지표 감지" if inp.vanity_metric_warning else ""
        result.irr_exit_sensitivity_summary = (
            f"Exit ±1x 감응도 OK" if inp.irr_exit_sensitivity_ok
            else f"Exit ±1x 감응도 미검증"
        )

        # 등급 판정
        result.grade = self._assign_grade(result)
        return result

    # ── 등급 판정 ────────────────────────────────────────────
    def _assign_grade(self, r: TDAResult) -> str:
        failed_must_count = len(r.failed_must_ids)
        d6_must_failed = any(i.startswith("D6") for i in r.failed_must_ids)
        s = r.tda_score

        # 기본 등급 (점수 기준)
        if s >= 90 and failed_must_count == 0:
            grade = "S"
        elif s >= 75 and failed_must_count == 0:
            grade = "A"
        elif s >= 55 and failed_must_count <= 1:
            grade = "B"
        elif s >= 35 or failed_must_count >= 2:
            grade = "C"
        else:
            grade = "D"

        # MUST override 강등
        grade_order = ["S", "A", "B", "C", "D"]
        max_grade = "S"

        if d6_must_failed and failed_must_count >= 1:
            max_grade = "B"
        if failed_must_count >= 2:
            max_grade = "C"
        if failed_must_count >= 4:
            max_grade = "D"

        # 낮은 등급 선택
        if grade_order.index(grade) < grade_order.index(max_grade):
            grade = max_grade

        return grade


# ============================================================
# 3. Notion 기록
# ============================================================
def write_to_notion(
    page_id: str,
    inp: TDAInput,
    result: TDAResult,
    dry_run: bool = False
) -> None:
    """TDA 결과를 Notion 페이지 속성에 기록"""
    props = {
        "PE3 Grade":            {"rich_text": [{"text": {"content": result.grade}}]},
        "PE3 Score":            {"number": result.tda_score},
        "PE3 Failed Must":      {"rich_text": [{"text": {"content": ", ".join(result.failed_must_ids)}}]},
        "IRR Result":           {"number": inp.irr_base},
        "IRR Bear":             {"number": inp.irr_bear},
        "IRR Entry EV Cap":     {"rich_text": [{"text": {"content": str(inp.irr_entry_ev_cap) + "억"}}]},
        "IRR Exit Sensitivity": {"rich_text": [{"text": {"content": result.irr_exit_sensitivity_summary}}]},
        "Entry EV":             {"rich_text": [{"text": {"content": str(inp.entry_ev) + "억"}}]},
        "NSM Metric":           {"rich_text": [{"text": {"content": inp.nsm_metric}}]},
        "NSM Target":           {"rich_text": [{"text": {"content": inp.nsm_target}}]},
        "Blue Ocean Score":     {"rich_text": [{"text": {"content": str(inp.blue_ocean_score)}}]},
        "Vanity Metric Warning":{"rich_text": [{"text": {"content": result.vanity_warning_text}}]},
        "KPI Phase1":           {"rich_text": [{"text": {"content": inp.kpi_phase1}}]},
        "KPI Phase2":           {"rich_text": [{"text": {"content": inp.kpi_phase2}}]},
        "KPI Phase3":           {"rich_text": [{"text": {"content": inp.kpi_phase3}}]},
        "Go No-Go Trigger":     {"rich_text": [{"text": {"content": inp.go_no_go_trigger}}]},
        "MECE Status":          {"select": {"name": "✅ 완료"}},
    }

    if dry_run:
        print("[DRY-RUN] Notion 기록 생략. Payload:")
        print(json.dumps(props, ensure_ascii=False, indent=2))
        return

    if NotionClient is None:
        print("[ERROR] notion-client 미설치. pip install notion-client")
        sys.exit(1)

    token = os.environ.get("NOTION_TOKEN")
    if not token:
        print("[ERROR] 환경변수 NOTION_TOKEN 미설정")
        sys.exit(1)

    notion = NotionClient(auth=token)
    notion.pages.update(page_id=page_id, properties=props)
    print(f"[OK] Notion 페이지 {page_id} 업데이트 완료")


# ============================================================
# 4. 리포트 출력
# ============================================================
def print_report(inp: TDAInput, result: TDAResult) -> None:
    grade_emoji = {"S": "🟣", "A": "🔵", "B": "🟢", "C": "🟠", "D": "🔴"}
    emoji = grade_emoji.get(result.grade, "⚪")

    print("\n" + "=" * 60)
    print(f"  TDA 판정 결과  {emoji} {result.grade}등급  |  점수: {result.tda_score}/100")
    print("=" * 60)

    print("\n[차원별 점수]")
    dim_labels = {"D6_irr": "D6 IRR역산(40)", "D7_market": "D7 시장차별(35)", "D8_execution": "D8 실행로드맵(25)"}
    for k, v in result.dimension_scores.items():
        print(f"  {dim_labels.get(k, k):25s}: {v:5.1f}점")

    if result.failed_must_ids:
        print(f"\n[MUST 미통과 항목] → {', '.join(result.failed_must_ids)}")
    else:
        print("\n[MUST] 전항목 통과 ✅")

    print("\n[통과 항목]")
    for item in result.passed_items:
        print(f"  ✅ {item}")

    print("\n[미통과 항목]")
    for item in result.failed_items:
        print(f"  ❌ {item}")

    print("\n" + "=" * 60)


# ============================================================
# 5. CLI 진입점
# ============================================================
def parse_args():
    p = argparse.ArgumentParser(description="TDA 자동 판정 엔진")
    p.add_argument("--page-id",  required=True, help="Notion 페이지 ID")
    p.add_argument("--dry-run",  action="store_true", help="Notion 기록 건너뜀")
    # D6
    p.add_argument("--irr-base",          type=float, default=0.0)
    p.add_argument("--irr-bear",          type=float, default=0.0)
    p.add_argument("--entry-ev",          type=float, default=0.0)
    p.add_argument("--irr-ev-cap",        type=float, default=0.0)
    p.add_argument("--irr-sensitivity",   action="store_true")
    p.add_argument("--target-irr",        type=float, default=20.0)
    # D7
    p.add_argument("--blue-ocean-score",  type=float, default=0.0)
    p.add_argument("--nsm-metric",        type=str,   default="")
    p.add_argument("--nsm-target",        type=str,   default="")
    p.add_argument("--vanity-warning",    action="store_true")
    # D8
    p.add_argument("--kpi-phase1",        type=str,   default="")
    p.add_argument("--kpi-phase2",        type=str,   default="")
    p.add_argument("--kpi-phase3",        type=str,   default="")
    p.add_argument("--go-no-go",          type=str,   default="")
    return p.parse_args()


def main():
    args = parse_args()

    inp = TDAInput(
        irr_base=args.irr_base,
        irr_bear=args.irr_bear,
        entry_ev=args.entry_ev,
        irr_entry_ev_cap=args.irr_ev_cap,
        irr_exit_sensitivity_ok=args.irr_sensitivity,
        target_irr=args.target_irr,
        blue_ocean_score=args.blue_ocean_score,
        nsm_metric=args.nsm_metric,
        nsm_target=args.nsm_target,
        vanity_metric_warning=args.vanity_warning,
        kpi_phase1=args.kpi_phase1,
        kpi_phase2=args.kpi_phase2,
        kpi_phase3=args.kpi_phase3,
        go_no_go_trigger=args.go_no_go,
    )

    validator = TDAValidator()
    result = validator.evaluate(inp)
    print_report(inp, result)
    write_to_notion(args.page_id, inp, result, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
