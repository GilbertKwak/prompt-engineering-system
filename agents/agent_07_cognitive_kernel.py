#!/usr/bin/env python3
"""
AGENT-07: Cognitive Kernel (CRP-AGENT-FRAMEWORK Integration) v1.0
Session: C-39 | Date: 2026-05-24 | PE-7 AI Automation Design v1.2

CRP 4-Stage Loop:
  Stage 1: Observation   → B = {b1..bn}, P = Π(B, E)
  Stage 2: Encoding      → C0 = φ(P), MTI, QLI
  Stage 3: Analysis      → C1 = R(C0, Δ)  [Reconfiguration Operator]
  Stage 4: Output        → PE-3 scores + recommendations + C_target

T-09 Ecosystem Connections:
  → PE-3 Hub (auto-scoring)
  → AGENT-04 (anti-gaming flags)
  → AGENT-05 (GitHub auto-commit)
  → KM-PIPE-MASTER (KG node registration)
  → PE-IP Library (prompt assetization)
  → T-AUTO-04 (master auto-update trigger)
"""

import argparse
import json
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


# ─────────────────────────────────────────────
# DATA MODELS
# ─────────────────────────────────────────────

@dataclass
class BehaviorLog:
    timestamp: str
    action: str
    input_tokens: int
    output_quality: float  # 0.0–1.0


@dataclass
class PE3Weights:
    risk_completeness: float = 0.25
    numeric_verifiability: float = 0.20
    scenario_logic: float = 0.20
    fraud_detection: float = 0.15
    strategic_executability: float = 0.20


@dataclass
class CognitiveKernelInput:
    session_id: str
    artifact_text: str
    behavior_log: list[BehaviorLog] = field(default_factory=list)
    domain: str = "PE-7"
    target_prompt_id: str = "AGENT-07"
    pe3_weights: PE3Weights = field(default_factory=PE3Weights)


@dataclass
class ReconfRecommendation:
    priority: int  # 1=highest
    target: str
    action: str
    expected_delta: float


@dataclass
class CognitiveKernelOutput:
    session_id: str
    timestamp: str
    crp_observation: float
    crp_encoding: float
    crp_analysis: float
    crp_reconfiguration: float
    crp_total: float
    pe3_risk_completeness: float
    pe3_numeric_verifiability: float
    pe3_scenario_logic: float
    pe3_fraud_detection: float
    pe3_strategic_executability: float
    pe3_total: float
    mti: float  # Meta-Thinking Index
    qli: float  # Quality Learning Index
    trust_flags: list[str]
    recommendations: list[ReconfRecommendation]
    next_c_target: str


# ─────────────────────────────────────────────
# CRP 4-STAGE ENGINE
# ─────────────────────────────────────────────

class CognitiveCernel:
    """CRP Cognitive Kernel: C1 = R(C0, Δ) where R: Ω → Ω"""

    # Stage 1: Observation — extract behavior sequence B, pattern P
    def observe(self, logs: list[BehaviorLog], env: str) -> dict:
        n = len(logs)
        if n == 0:
            return {"pattern_density": 0.5, "sequence_length": 0}
        avg_quality = sum(b.output_quality for b in logs) / n
        # Pattern Π(B, E): detect repetition and quality trend
        quality_trend = 0.0
        if n >= 2:
            deltas = [logs[i].output_quality - logs[i-1].output_quality
                      for i in range(1, n)]
            quality_trend = sum(deltas) / len(deltas)
        return {
            "pattern_density": avg_quality,
            "quality_trend": quality_trend,
            "sequence_length": n,
            "env": env
        }

    # Stage 2: Encoding — C0 = φ(P), compute MTI and QLI
    def encode(self, pattern: dict, artifact: str) -> dict:
        pd = pattern.get("pattern_density", 0.5)
        qt = pattern.get("quality_trend", 0.0)
        n = pattern.get("sequence_length", 1)

        # MTI = Σ(wi × qi) / n  (weighted average quality)
        mti = pd  # simplified: pattern density as proxy

        # QLI = ΔC / Δt  (quality growth rate)
        qli = qt

        # C0: current cognitive structure score (0–100)
        word_count = len(artifact.split())
        structure_score = min(100, word_count / 50)  # heuristic
        c0 = (mti * 60) + (structure_score * 0.4)
        c0 = min(100, max(0, c0))

        return {"c0": c0, "mti": mti, "qli": qli}

    # Stage 3: Analysis — C1 = R(C0, Δ), Δ = Gap(C0, C_target)
    def analyze(self, c0: float, artifact: str) -> dict:
        c_target = 90.0  # PE-3 target score
        delta = c_target - c0

        # PE-3 axis scoring (heuristic from artifact analysis)
        text_lower = artifact.lower()

        risk_score = self._score_axis(text_lower,
            ["risk", "리스크", "위험", "annex", "fraud"], 25)
        numeric_score = self._score_axis(text_lower,
            ["irr", "npv", "ebitda", "단가", "수치", "\%", "검증"], 25)
        scenario_score = self._score_axis(text_lower,
            ["시나리오", "base", "bull", "bear", "scenario", "확률"], 25)
        fraud_score = self._score_axis(text_lower,
            ["fraud", "심리", "조작", "agent-04", "anti", "trust"], 20)
        strategy_score = self._score_axis(text_lower,
            ["전략", "실행", "strategy", "implementation", "roadmap"], 25)

        # Weighted PE-3 total
        pe3_total = (
            risk_score     * 0.25 +
            numeric_score  * 0.20 +
            scenario_score * 0.20 +
            fraud_score    * 0.15 +
            strategy_score * 0.20
        )

        # Reconfiguration: C1 = R(C0, Δ)
        c1 = min(100, c0 + (delta * 0.3))  # 30% gap closure per iteration

        return {
            "c1": c1,
            "delta": delta,
            "pe3": {
                "risk": risk_score,
                "numeric": numeric_score,
                "scenario": scenario_score,
                "fraud": fraud_score,
                "strategy": strategy_score,
                "total": round(pe3_total, 1)
            }
        }

    def _score_axis(self, text: str, keywords: list[str], max_score: int) -> float:
        hits = sum(1 for kw in keywords if kw in text)
        return min(max_score, (hits / max(len(keywords), 1)) * max_score * 1.5)

    # Stage 4: Reconfiguration Output
    def reconfigurate(self, analysis: dict, mti: float, qli: float,
                       session_id: str) -> CognitiveKernelOutput:
        pe3 = analysis["pe3"]
        c1 = analysis["c1"]
        delta = analysis["delta"]

        # Trust Layer — Anti-Gaming Detection
        trust_flags = []
        if delta < -15:
            trust_flags.append("SCORE_SPIKE: Δ > 15 — re-verification required")
        if qli < 0:
            trust_flags.append("QLI_NEGATIVE: Quality regression — C0 rollback")
        if mti < 0.5:
            trust_flags.append("MTI_LOW: Pattern stagnation — forced reconfiguration")

        # Recommendations (prioritized)
        recs = []
        lowest = sorted([
            ("risk_completeness", pe3["risk"]),
            ("numeric_verifiability", pe3["numeric"]),
            ("scenario_logic", pe3["scenario"]),
            ("fraud_detection", pe3["fraud"]),
            ("strategic_executability", pe3["strategy"])
        ], key=lambda x: x[1])

        for i, (axis, score) in enumerate(lowest[:3]):
            recs.append(ReconfRecommendation(
                priority=i + 1,
                target=axis,
                action=f"Improve {axis} (current: {score:.1f})",
                expected_delta=round((100 - score) * 0.2, 1)
            ))

        return CognitiveKernelOutput(
            session_id=session_id,
            timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S KST"),
            crp_observation=min(25, analysis["c1"] * 0.25),
            crp_encoding=min(25, mti * 25),
            crp_analysis=min(25, (1 - abs(qli)) * 20 if qli >= 0 else 15),
            crp_reconfiguration=min(25, (analysis["c1"] / 100) * 25),
            crp_total=round(c1, 1),
            pe3_risk_completeness=round(pe3["risk"], 1),
            pe3_numeric_verifiability=round(pe3["numeric"], 1),
            pe3_scenario_logic=round(pe3["scenario"], 1),
            pe3_fraud_detection=round(pe3["fraud"], 1),
            pe3_strategic_executability=round(pe3["strategy"], 1),
            pe3_total=pe3["total"],
            mti=round(mti, 3),
            qli=round(qli, 3),
            trust_flags=trust_flags,
            recommendations=recs,
            next_c_target=f"C{int(session_id.replace('C','')) + 1} target: PE-3 ≥ {min(100, pe3['total'] + 5):.0f}"
        )


# ─────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────

def run_cognitive_kernel(inp: CognitiveKernelInput) -> CognitiveKernelOutput:
    kernel = CognitiveCernel()

    # Stage 1
    pattern = kernel.observe(inp.behavior_log, inp.domain)

    # Stage 2
    encoding = kernel.encode(pattern, inp.artifact_text)

    # Stage 3
    analysis = kernel.analyze(encoding["c0"], inp.artifact_text)
    analysis["c1"] = max(analysis["c1"], encoding["c0"])  # no regression

    # Stage 4
    output = kernel.reconfigurate(
        analysis, encoding["mti"], encoding["qli"], inp.session_id
    )
    return output


def print_report(out: CognitiveKernelOutput):
    print("\n" + "=" * 60)
    print(f"  AGENT-07 · Cognitive Kernel Report")
    print(f"  Session: {out.session_id} | {out.timestamp}")
    print("=" * 60)
    print(f"\n[CRP Scores]")
    print(f"  Observation:      {out.crp_observation:.1f}/25")
    print(f"  Encoding:         {out.crp_encoding:.1f}/25")
    print(f"  Analysis:         {out.crp_analysis:.1f}/25")
    print(f"  Reconfiguration:  {out.crp_reconfiguration:.1f}/25")
    print(f"  CRP Total:        {out.crp_total:.1f}/100")
    print(f"\n[PE-3 Scores]")
    print(f"  Risk Completeness:      {out.pe3_risk_completeness:.1f}/25")
    print(f"  Numeric Verifiability:  {out.pe3_numeric_verifiability:.1f}/25")
    print(f"  Scenario Logic:         {out.pe3_scenario_logic:.1f}/25")
    print(f"  Fraud Detection:        {out.pe3_fraud_detection:.1f}/20")
    print(f"  Strategic Executability:{out.pe3_strategic_executability:.1f}/25")
    print(f"  PE-3 Total:             {out.pe3_total:.1f}/100")
    print(f"\n[Indices]")
    print(f"  MTI (Meta-Thinking):   {out.mti:.3f}")
    print(f"  QLI (Quality Growth):  {out.qli:.3f}")
    if out.trust_flags:
        print(f"\n[⚠ Trust Flags]")
        for flag in out.trust_flags:
            print(f"  • {flag}")
    print(f"\n[Top Recommendations]")
    for rec in out.recommendations:
        print(f"  P{rec.priority}: {rec.action} (+{rec.expected_delta:.1f} expected)")
    print(f"\n[Next Target]  {out.next_c_target}")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AGENT-07 Cognitive Kernel")
    parser.add_argument("--session", default="C-39")
    parser.add_argument("--artifact", default="",
                        help="Artifact text OR path to .md file")
    parser.add_argument("--domain", default="PE-7")
    parser.add_argument("--output", default="stdout",
                        choices=["stdout", "json", "notion+github"])
    args = parser.parse_args()

    # Load artifact
    artifact_text = args.artifact
    if artifact_text.endswith(".md"):
        try:
            with open(artifact_text, "r", encoding="utf-8") as f:
                artifact_text = f.read()
        except FileNotFoundError:
            print(f"[WARN] File not found: {artifact_text}")

    inp = CognitiveKernelInput(
        session_id=args.session,
        artifact_text=artifact_text,
        domain=args.domain
    )

    result = run_cognitive_kernel(inp)

    if args.output == "json":
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print_report(result)
        if args.output == "notion+github":
            print("\n[→] notion+github sync: use AGENT-05 pipeline")
            print("    python agents/run_pipeline.py --agents 07,05,04 "
                  f"--session {args.session}")
