"""
FIN-PE3-ISSB-SLB Trigger Engine v1.0
작성일: 2026-05-08 | 연동: FIN-MSIA-ESG v1.1 + FIN-SNBS-v4.0-ESG-OPT

PE-3 × ISSB S2 조인트 체크포인트 자동화 + SLB step-up 트리거 엔진
"""
from dataclasses import dataclass, field
from typing import Optional


# ── 상수 ──────────────────────────────────────────────────────────
SLB_PRINCIPAL   = 200_000_000   # $200M
BASE_COUPON     = 0.045         # 4.5%
STEPUP_25BPS    = 0.0025
STEPUP_50BPS    = 0.0050
STEPUP_75BPS    = 0.0075
STEPUP_100BPS   = 0.0100

THRESHOLDS = {
    "T+12M": {"ghg_reduction": 50_000, "issb_score": 60,  "pe3_score": 90},
    "T+24M": {"issb_score": 70,        "pe3_score": 92},
    "T+36M": {"issb_score": 78,        "pe3_score": 95},   # ★ 핵심 조인트 체크포인트
    "T+48M": {"issb_score": 82,        "pe3_score": 95,  "sbti_approved": True},
    "T+60M": {"issb_score": 85,        "pe3_score": 95},
}

ISSB_GRADE = {
    (85, 100): "ISSB S2 Ready (Full Disclosure Capable)",
    (65,  84): "ISSB S2 Partial (Gap-fill required)",
    (40,  64): "ISSB S2 Developing (Material gaps)",
    (0,   39): "ISSB S2 Non-Compliant",
}


@dataclass
class CheckpointResult:
    milestone: str
    issb_score: float
    pe3_score: float
    spread_bps: float
    annual_penalty_m: float
    cumul_5y_penalty_m: float
    actions: list
    grade: str          # PASS / WATCH / TRIGGER / EXTREME
    irr_impact_pp: float
    investment_score: float = 94.22   # ESG-Optimal base
    slb_grade: str = "A"              # Grade A 유지 여부


class SLBStepUpEngine:
    """
    PE-3 x ISSB S2 조인트 체크포인트 자동화 엔진
    FIN-MSIA-ESG v1.1 Step7 + FIN-SNBS-v4.0-ESG-OPT 연동
    """

    def evaluate(self, milestone: str, actuals: dict) -> CheckpointResult:
        th = THRESHOLDS[milestone]
        issb_score = actuals.get("issb_score", 0)
        pe3_score  = actuals.get("pe3_score",  0)
        ghg_red    = actuals.get("ghg_reduction", 999_999)
        sbti_ok    = actuals.get("sbti_approved", False)

        issb_ok = issb_score >= th.get("issb_score", 0)
        pe3_ok  = pe3_score  >= th.get("pe3_score",  0)
        ghg_ok  = ghg_red    >= th.get("ghg_reduction", 0)
        sbti_req = th.get("sbti_approved", False)

        spread  = 0.0
        actions = []
        grade   = "PASS"

        # T+12M GHG 트리거
        if milestone == "T+12M" and not ghg_ok:
            spread += STEPUP_25BPS
            actions.append(f"⚠️  SLB +25bps: GHG {ghg_red:,}t < {th['ghg_reduction']:,}t 목표")
            grade = "TRIGGER"

        # ISSB + PE-3 분기 트리
        if issb_score < 65 and not pe3_ok:
            spread = STEPUP_100BPS    # Extreme override
            actions = ["🔴 SLB +100bps EXTREME: ISSB<65 + PE-3 Fail → LP 즉시 통보"]
            grade = "EXTREME"
        elif not issb_ok and not pe3_ok:
            spread += STEPUP_75BPS
            actions.append(f"🔴 SLB +75bps Double: ISSB {issb_score:.0f}<{th['issb_score']} AND PE-3 {pe3_score:.0f}<{th['pe3_score']}")
            grade = "TRIGGER"
        elif not issb_ok:
            spread += STEPUP_50BPS
            actions.append(f"⚠️  SLB +50bps: ISSB {issb_score:.0f} < 목표 {th['issb_score']} → 30일 Action Plan 제출")
            grade = "TRIGGER" if grade != "EXTREME" else grade
        elif not pe3_ok:
            actions.append(f"🔶 PE-3 재검증 30일 유예 (PE-3 {pe3_score:.0f}<{th['pe3_score']}) — 쿠폰 변동 없음")
            grade = "WATCH" if grade == "PASS" else grade

        # SBTi 체크 (T+48M)
        if sbti_req and not sbti_ok:
            actions.append("📣 SBTi 미승인 → LP 경보 발송 (쿠폰 변동 없음, 차기 체크포인트 가중)")
            grade = "WATCH" if grade == "PASS" else grade

        annual_penalty   = SLB_PRINCIPAL * spread / 1_000_000
        cumul_5y_penalty = annual_penalty * 5
        irr_impact       = -spread * 100

        # ISSB 등급 라벨
        issb_label = next(
            (v for (lo, hi), v in ISSB_GRADE.items() if lo <= issb_score <= hi),
            "Unknown"
        )

        if not actions:
            actions.append(f"✅ PASS: ISSB {issb_score:.0f}점({issb_label[:20]}) | PE-3 {pe3_score:.0f}점 — Step-Up 없음")

        return CheckpointResult(
            milestone=milestone,
            issb_score=issb_score,
            pe3_score=pe3_score,
            spread_bps=spread * 10_000,
            annual_penalty_m=annual_penalty,
            cumul_5y_penalty_m=cumul_5y_penalty,
            actions=actions,
            grade=grade,
            irr_impact_pp=irr_impact,
        )

    def run_full_roadmap(self, roadmap: list[dict]) -> list[CheckpointResult]:
        """T+0 → T+60M 전체 체크포인트 일괄 평가"""
        return [self.evaluate(r["milestone"], r) for r in roadmap]


# ── CLI 엔트리포인트 ───────────────────────────────────────────────
if __name__ == "__main__":
    import argparse, json

    parser = argparse.ArgumentParser(description="SLB Step-Up Trigger Engine")
    parser.add_argument("--milestone",     required=True, choices=list(THRESHOLDS.keys()))
    parser.add_argument("--issb-score",    type=float, required=True)
    parser.add_argument("--pe3-score",     type=float, required=True)
    parser.add_argument("--ghg-reduction", type=int,   default=999_999)
    parser.add_argument("--sbti-approved", action="store_true")
    parser.add_argument("--output",        choices=["text", "json"], default="text")
    args = parser.parse_args()

    engine = SLBStepUpEngine()
    result = engine.evaluate(args.milestone, {
        "issb_score":    args.issb_score,
        "pe3_score":     args.pe3_score,
        "ghg_reduction": args.ghg_reduction,
        "sbti_approved": args.sbti_approved,
    })

    if args.output == "json":
        print(json.dumps(result.__dict__, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"  PE-3 × ISSB S2 체크포인트: {result.milestone}")
        print(f"{'='*60}")
        print(f"  ISSB S2 Score : {result.issb_score:.0f}점")
        print(f"  PE-3 Score    : {result.pe3_score:.0f}점")
        print(f"  Grade         : {result.grade}")
        print(f"  SLB Spread    : +{result.spread_bps:.0f}bps")
        print(f"  연간 페널티    : ${result.annual_penalty_m:.3f}M")
        print(f"  IRR 충격       : {result.irr_impact_pp:+.2f}pp")
        print(f"  Actions:")
        for a in result.actions:
            print(f"    {a}")
        print(f"{'='*60}\n")
