#!/usr/bin/env python3
"""
AGENT-07: Cognitive Kernel (CRP-Native Framework) v2.0
═══════════════════════════════════════════════════════
Session : C-39 | Date: 2026-05-24 | PE-7 AI Automation Design v1.2
Author  : Gilbert (T-09 Ecosystem)

CRP Formal Definition
─────────────────────
  Cognitive Space   : Ω = {C | C = (P, M, S)}
                        P = Pattern vector
                        M = Meta-cognition index
                        S = State trajectory
  Reconfiguration   : C₁ = R(C₀, Δ) where R: Ω → Ω
  Transformation    : C  = f(B, P, E)
                        B = Behavior sequence
                        P = Pattern extraction
                        E = Environment context
  Indices           : MTI = Σ(wᵢ × qᵢ) / n   (Meta-Thinking Index)
                      QLI = ΔC / Δt             (Quality Learning Index)

CRP 4-Stage Pipeline
────────────────────
  Stage 1: Observation   → B={b₁..bₙ}, Π(B,E)
  Stage 2: Encoding      → C₀=φ(P), compute MTI, QLI
  Stage 3: Analysis      → C₁=R(C₀,Δ), PE-3 axis scoring
  Stage 4: Reconfiguration → Trust Layer + Recommendations + next C_target

T-09 Ecosystem Connectors (v2.0)
─────────────────────────────────
  [PE-3 Hub]          → auto-scoring pipeline trigger
  [AGENT-04]          → anti-gaming flag injection
  [AGENT-05]          → GitHub auto-commit on score improvement
  [KM-PIPE-MASTER]    → KG node registration (CRP_SESSION node type)
  [PE-IP Library]     → prompt assetization on QLI > 0.1
  [T-AUTO-04]         → master session log auto-update
  [INV-STRAT-MASTER]  → CRP scores → investment decision weight
  [RPT-AI-ECO-001]    → AI Ecosystem report enrichment hook
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


# ══════════════════════════════════════════════════════════════════
# §1  DATA MODELS
# ══════════════════════════════════════════════════════════════════

@dataclass
class BehaviorLog:
    """Single observation unit in behavior sequence B."""
    timestamp: str
    action: str
    input_tokens: int
    output_quality: float       # normalised 0.0–1.0
    domain: str = "general"
    pe3_score: Optional[float] = None   # previous PE-3 score, if known


@dataclass
class PE3Weights:
    """Configurable PE-3 axis weights (must sum to 1.0)."""
    risk_completeness: float       = 0.25
    numeric_verifiability: float   = 0.20
    scenario_logic: float          = 0.20
    fraud_detection: float         = 0.15
    strategic_executability: float = 0.20

    def validate(self) -> bool:
        total = (self.risk_completeness + self.numeric_verifiability
                 + self.scenario_logic + self.fraud_detection
                 + self.strategic_executability)
        return abs(total - 1.0) < 1e-6


@dataclass
class CognitiveKernelInput:
    """Full input schema for a CRP kernel run."""
    session_id: str
    artifact_text: str
    behavior_log: list[BehaviorLog]    = field(default_factory=list)
    domain: str                        = "PE-7"
    target_prompt_id: str              = "AGENT-07"
    c_target: float                    = 90.0           # desired PE-3 score
    pe3_weights: PE3Weights            = field(default_factory=PE3Weights)
    ecosystem_hooks: list[str]         = field(default_factory=lambda: [
        "PE-3", "AGENT-04", "AGENT-05", "KM-PIPE", "PE-IP"
    ])


@dataclass
class ReconfRecommendation:
    """Prioritised reconfiguration action."""
    priority: int               # 1 = highest urgency
    axis: str
    current_score: float
    action: str
    expected_delta: float
    hook: Optional[str] = None  # which ecosystem hook to trigger


@dataclass
class TrustFlag:
    """Anti-gaming / trust signal."""
    code: str
    severity: str               # WARN | ERROR | CRITICAL
    message: str
    suggested_action: str


@dataclass
class KGRegistration:
    """KG node to be created in KM-PIPE-MASTER (v6.3+)."""
    node_type: str              # CRP_SESSION
    session_id: str
    crp_total: float
    pe3_total: float
    mti: float
    qli: float
    domain: str
    timestamp: str


@dataclass
class CognitiveKernelOutput:
    """Full output schema — matches T-09 logging standard."""
    # Identity
    session_id: str
    timestamp: str
    domain: str

    # CRP 4-Stage scores (each /25, total /100)
    crp_observation: float
    crp_encoding: float
    crp_analysis: float
    crp_reconfiguration: float
    crp_total: float

    # PE-3 axis scores
    pe3_risk_completeness: float
    pe3_numeric_verifiability: float
    pe3_scenario_logic: float
    pe3_fraud_detection: float
    pe3_strategic_executability: float
    pe3_total: float

    # Cognitive indices
    mti: float          # Meta-Thinking Index  ∈ [0,1]
    qli: float          # Quality Learning Index (signed rate)

    # Reconfiguration state
    c0: float           # initial cognitive state
    c1: float           # reconfigured cognitive state
    delta: float        # C_target − C₀

    # Trust layer
    trust_flags: list[TrustFlag]
    trust_ok: bool

    # Recommendations
    recommendations: list[ReconfRecommendation]

    # Ecosystem
    next_c_target: str
    kg_registration: KGRegistration
    ecosystem_triggers: list[str]


# ══════════════════════════════════════════════════════════════════
# §2  KEYWORD BANKS  (domain-aware, extendable)
# ══════════════════════════════════════════════════════════════════

AXIS_KEYWORDS: dict[str, list[str]] = {
    "risk_completeness": [
        "risk", "리스크", "위험", "annex", "fraud", "downside",
        "mitigation", "exposure", "worst case", "tail risk",
        "변동성", "민감도", "sensitivity"
    ],
    "numeric_verifiability": [
        "irr", "npv", "ebitda", "cagr", "단가", "수치", "%",
        "검증", "basis point", "margin", "revenue", "cost",
        "billion", "million", "십억", "억원", "확률", "probability"
    ],
    "scenario_logic": [
        "시나리오", "base", "bull", "bear", "scenario",
        "upside", "downside", "base case", "sensitivity",
        "monte carlo", "stress test", "dcf", "valuation"
    ],
    "fraud_detection": [
        "fraud", "심리", "조작", "agent-04", "anti", "trust",
        "manipulation", "bias", "conflict", "verification",
        "audit", "compliance", "검증", "이해충돌"
    ],
    "strategic_executability": [
        "전략", "실행", "strategy", "implementation", "roadmap",
        "milestone", "kpi", "okr", "timeline", "phase",
        "execution", "go-to-market", "gtm", "priority"
    ],
}

# CRP-stage-specific keywords for Stage-1 pattern detection
CRP_STAGE_KEYWORDS: dict[str, list[str]] = {
    "observation": ["observe", "detect", "pattern", "sequence", "behavior"],
    "encoding":    ["encode", "structure", "model", "index", "mti", "qli"],
    "analysis":    ["analyze", "delta", "gap", "improve", "reconfig"],
    "output":      ["recommend", "action", "target", "next", "score"],
}


# ══════════════════════════════════════════════════════════════════
# §3  CRP COGNITIVE KERNEL ENGINE
# ══════════════════════════════════════════════════════════════════

class CognitiveKernel:
    """
    CRP Engine: C₁ = R(C₀, Δ)   where R: Ω → Ω

    Public interface
    ────────────────
      kernel = CognitiveKernel()
      output = kernel.run(inp: CognitiveKernelInput) -> CognitiveKernelOutput
    """

    # ── Stage 1: Observation ──────────────────────────────────────
    def _stage1_observe(
        self,
        logs: list[BehaviorLog],
        env: str
    ) -> dict:
        """
        Extract behavior sequence B, compute pattern Π(B, E).
        Returns pattern dict with density, trend, and stage coverage.
        """
        n = len(logs)
        if n == 0:
            return {
                "pattern_density": 0.50,
                "quality_trend": 0.0,
                "sequence_length": 0,
                "pe3_history": [],
                "env": env,
                "stage_coverage": 0.0,
            }

        avg_quality  = sum(b.output_quality for b in logs) / n
        quality_diff = [
            logs[i].output_quality - logs[i - 1].output_quality
            for i in range(1, n)
        ]
        quality_trend = sum(quality_diff) / len(quality_diff) if quality_diff else 0.0

        # PE-3 history (last 5 known scores)
        pe3_hist = [b.pe3_score for b in logs if b.pe3_score is not None][-5:]

        # Stage coverage: how many CRP stages are mentioned across logs
        all_actions = " ".join(b.action.lower() for b in logs)
        stages_hit = sum(
            1 for stage_kws in CRP_STAGE_KEYWORDS.values()
            if any(kw in all_actions for kw in stage_kws)
        )
        stage_coverage = stages_hit / len(CRP_STAGE_KEYWORDS)

        return {
            "pattern_density": avg_quality,
            "quality_trend": quality_trend,
            "sequence_length": n,
            "pe3_history": pe3_hist,
            "env": env,
            "stage_coverage": stage_coverage,
        }

    # ── Stage 2: Encoding ─────────────────────────────────────────
    def _stage2_encode(self, pattern: dict, artifact: str) -> dict:
        """
        C₀ = φ(P)
        MTI = Σ(wᵢ × qᵢ) / n   — Meta-Thinking Index
        QLI = ΔC / Δt           — Quality Learning Index
        """
        pd  = pattern.get("pattern_density", 0.5)
        qt  = pattern.get("quality_trend", 0.0)
        sc  = pattern.get("stage_coverage", 0.5)
        pe3h = pattern.get("pe3_history", [])

        # MTI: weighted quality + stage coverage bonus
        mti = (pd * 0.70) + (sc * 0.30)
        mti = max(0.0, min(1.0, mti))

        # QLI: rate of quality change (signed)
        if len(pe3h) >= 2:
            qli = (pe3h[-1] - pe3h[0]) / max(len(pe3h) - 1, 1) / 100.0
        else:
            qli = qt

        # C₀: current cognitive state score (0–100)
        word_count    = len(artifact.split())
        sentence_count = max(1, artifact.count(".") + artifact.count("。"))
        avg_sentence_len = word_count / sentence_count

        # Heuristic richness: lexical density via unique word ratio
        words_lower = [w.lower().strip(".,;:()[]") for w in artifact.split()]
        lexical_density = len(set(words_lower)) / max(len(words_lower), 1)

        # C₀ composite
        length_score   = min(40.0, word_count / 80)         # /40
        richness_score = lexical_density * 30               # /30
        structure_score = min(30.0, sc * 30)                # /30
        c0 = length_score + richness_score + structure_score
        c0 = max(0.0, min(100.0, c0))

        return {
            "c0": round(c0, 2),
            "mti": round(mti, 4),
            "qli": round(qli, 4),
            "word_count": word_count,
            "lexical_density": round(lexical_density, 3),
        }

    # ── Stage 3: Analysis ─────────────────────────────────────────
    def _stage3_analyze(
        self,
        c0: float,
        artifact: str,
        c_target: float,
        weights: PE3Weights,
    ) -> dict:
        """
        Δ = C_target − C₀
        C₁ = R(C₀, Δ) via reconfiguration operator
        PE-3 axis scoring via keyword density.
        """
        delta = c_target - c0
        text  = artifact.lower()

        def score_axis(keywords: list[str], max_score: float) -> float:
            total_kw = len(keywords)
            hits     = sum(1 for kw in keywords if kw in text)
            raw      = (hits / max(total_kw, 1)) * max_score * 1.6
            return round(min(max_score, raw), 2)

        axis_maxes = {
            "risk_completeness":       25.0,
            "numeric_verifiability":   25.0,
            "scenario_logic":          25.0,
            "fraud_detection":         20.0,
            "strategic_executability": 25.0,
        }

        pe3_scores = {
            axis: score_axis(AXIS_KEYWORDS[axis], axis_maxes[axis])
            for axis in axis_maxes
        }

        # Weighted PE-3 total
        pe3_total = (
            pe3_scores["risk_completeness"]       * weights.risk_completeness       / (25 * weights.risk_completeness)       * 25 +
            pe3_scores["numeric_verifiability"]   * weights.numeric_verifiability   / (25 * weights.numeric_verifiability)   * 25 +
            pe3_scores["scenario_logic"]          * weights.scenario_logic          / (25 * weights.scenario_logic)          * 25 +
            pe3_scores["fraud_detection"]         * weights.fraud_detection         / (20 * weights.fraud_detection)         * 20 +
            pe3_scores["strategic_executability"] * weights.strategic_executability / (25 * weights.strategic_executability) * 25
        )
        pe3_total = round(min(100.0, pe3_total), 1)

        # Reconfiguration: C₁ = C₀ + α·Δ  (α = 0.35, one iteration)
        alpha = 0.35
        c1 = min(100.0, c0 + alpha * delta)
        c1 = max(c0, c1)                # non-regressing

        return {
            "c1": round(c1, 2),
            "delta": round(delta, 2),
            "pe3": pe3_scores,
            "pe3_total": pe3_total,
        }

    # ── Stage 4: Reconfiguration (Output Construction) ───────────
    def _stage4_reconfigurate(
        self,
        inp: CognitiveKernelInput,
        encoding: dict,
        analysis: dict,
    ) -> CognitiveKernelOutput:
        """
        Build full output: Trust Layer + Recommendations + KG node + Triggers.
        """
        mti  = encoding["mti"]
        qli  = encoding["qli"]
        c0   = encoding["c0"]
        c1   = analysis["c1"]
        delta= analysis["delta"]
        pe3  = analysis["pe3"]
        pe3t = analysis["pe3_total"]
        ts   = datetime.now().strftime("%Y-%m-%dT%H:%M:%S KST")

        # ── CRP sub-scores (each /25) ──────────────────────────────
        crp_obs   = round(min(25.0, (c0 / 100) * 25), 1)
        crp_enc   = round(min(25.0, mti * 25),         1)
        crp_ana   = round(min(25.0, max(0.0, (1 - abs(min(qli, 0.3))) * 22)), 1)
        crp_recon = round(min(25.0, (c1 / 100) * 25),  1)
        crp_total = round(c1, 1)

        # ── Trust Layer v2 ────────────────────────────────────────
        trust_flags: list[TrustFlag] = []

        if delta < -20:
            trust_flags.append(TrustFlag(
                code="SCORE_SPIKE",
                severity="ERROR",
                message=f"Δ={delta:.1f} — C₁ exceeds C_target by >20pts",
                suggested_action="Trigger AGENT-04 anti-gaming re-verification"
            ))
        if qli < -0.05:
            trust_flags.append(TrustFlag(
                code="QLI_NEGATIVE",
                severity="WARN",
                message=f"QLI={qli:.3f} — quality regression detected",
                suggested_action="Roll back to C₀ snapshot; review behavior log"
            ))
        if mti < 0.40:
            trust_flags.append(TrustFlag(
                code="MTI_LOW",
                severity="WARN",
                message=f"MTI={mti:.3f} — meta-cognitive stagnation",
                suggested_action="Forced reconfiguration; increase stage coverage"
            ))
        if encoding.get("lexical_density", 1.0) < 0.30:
            trust_flags.append(TrustFlag(
                code="LOW_LEXICAL_DENSITY",
                severity="WARN",
                message="Artifact lexical density < 30% — possible repetitive output",
                suggested_action="Expand artifact vocabulary; add domain-specific terms"
            ))
        if pe3t < 60:
            trust_flags.append(TrustFlag(
                code="PE3_CRITICAL",
                severity="CRITICAL",
                message=f"PE-3 total {pe3t} < 60 — below minimum threshold",
                suggested_action="Re-run full PE-7 pipeline before continuing"
            ))

        trust_ok = not any(f.severity == "CRITICAL" for f in trust_flags)

        # ── Recommendations ───────────────────────────────────────
        axis_map = {
            "risk_completeness":       ("PE-3", 25.0),
            "numeric_verifiability":   ("PE-IP", 25.0),
            "scenario_logic":          ("PE-3", 25.0),
            "fraud_detection":         ("AGENT-04", 20.0),
            "strategic_executability": ("INV-STRAT", 25.0),
        }
        sorted_axes = sorted(
            [(ax, pe3[ax]) for ax in axis_map],
            key=lambda x: x[1] / axis_map[x[0]][1]   # normalised score
        )
        recs: list[ReconfRecommendation] = []
        for i, (axis, score) in enumerate(sorted_axes[:3]):
            hook, max_s = axis_map[axis]
            gap   = max_s - score
            edelt = round(gap * 0.25, 1)
            recs.append(ReconfRecommendation(
                priority=i + 1,
                axis=axis,
                current_score=round(score, 1),
                action=f"Improve {axis}: add {_axis_hint(axis)}",
                expected_delta=edelt,
                hook=hook
            ))

        # ── Ecosystem triggers ────────────────────────────────────
        triggers: list[str] = []
        if qli > 0.05:
            triggers.append("PE-IP: assetize prompt (QLI improvement detected)")
        if pe3t >= 85:
            triggers.append("AGENT-05: auto-commit to GitHub (PE-3 ≥ 85)")
        if trust_ok and c1 >= 80:
            triggers.append("KM-PIPE: register CRP_SESSION node to KG v6.3+")
        if any(f.code == "SCORE_SPIKE" for f in trust_flags):
            triggers.append("AGENT-04: anti-gaming verification required")
        triggers.append("T-AUTO-04: update master session log")

        # ── KG Registration payload ───────────────────────────────
        kg = KGRegistration(
            node_type="CRP_SESSION",
            session_id=inp.session_id,
            crp_total=crp_total,
            pe3_total=pe3t,
            mti=round(mti, 3),
            qli=round(qli, 3),
            domain=inp.domain,
            timestamp=ts,
        )

        # ── Next target ───────────────────────────────────────────
        next_target_score = min(100.0, pe3t + 5)
        next_session_num  = _increment_session_id(inp.session_id)
        next_c = (
            f"{next_session_num} target: "
            f"PE-3 ≥ {next_target_score:.0f} | "
            f"MTI ≥ {min(1.0, mti + 0.05):.2f} | "
            f"QLI > 0"
        )

        return CognitiveKernelOutput(
            session_id=inp.session_id,
            timestamp=ts,
            domain=inp.domain,
            crp_observation=crp_obs,
            crp_encoding=crp_enc,
            crp_analysis=crp_ana,
            crp_reconfiguration=crp_recon,
            crp_total=crp_total,
            pe3_risk_completeness=round(pe3["risk_completeness"], 1),
            pe3_numeric_verifiability=round(pe3["numeric_verifiability"], 1),
            pe3_scenario_logic=round(pe3["scenario_logic"], 1),
            pe3_fraud_detection=round(pe3["fraud_detection"], 1),
            pe3_strategic_executability=round(pe3["strategic_executability"], 1),
            pe3_total=pe3t,
            mti=round(mti, 4),
            qli=round(qli, 4),
            c0=round(c0, 2),
            c1=round(c1, 2),
            delta=round(delta, 2),
            trust_flags=trust_flags,
            trust_ok=trust_ok,
            recommendations=recs,
            next_c_target=next_c,
            kg_registration=kg,
            ecosystem_triggers=triggers,
        )

    # ── Public entry point ────────────────────────────────────────
    def run(self, inp: CognitiveKernelInput) -> CognitiveKernelOutput:
        """Execute full CRP 4-stage loop."""
        if not inp.pe3_weights.validate():
            raise ValueError("PE3Weights must sum to 1.0")

        pattern  = self._stage1_observe(inp.behavior_log, inp.domain)
        encoding = self._stage2_encode(pattern, inp.artifact_text)
        analysis = self._stage3_analyze(
            encoding["c0"], inp.artifact_text,
            inp.c_target, inp.pe3_weights
        )
        return self._stage4_reconfigurate(inp, encoding, analysis)


# ══════════════════════════════════════════════════════════════════
# §4  UTILITIES
# ══════════════════════════════════════════════════════════════════

def _axis_hint(axis: str) -> str:
    hints = {
        "risk_completeness":       "risk quantification, tail-risk scenarios, sensitivity tables",
        "numeric_verifiability":   "IRR/NPV/EBITDA numbers, % margins, verifiable data points",
        "scenario_logic":          "bull/base/bear cases, DCF, probability-weighted outcomes",
        "fraud_detection":         "bias checks, conflict-of-interest disclosure, AGENT-04 flags",
        "strategic_executability": "phased roadmap, KPI milestones, Go-To-Market specifics",
    }
    return hints.get(axis, "more domain-specific content")


def _increment_session_id(sid: str) -> str:
    """C-39 → C-40"""
    match = re.search(r"(\d+)$", sid)
    if match:
        n = int(match.group(1))
        return sid[:match.start()] + str(n + 1)
    return sid + "-next"


def load_artifact(path_or_text: str) -> str:
    """Load artifact from file path or return raw text."""
    p = Path(path_or_text)
    if p.suffix in (".md", ".txt", ".json") and p.exists():
        return p.read_text(encoding="utf-8")
    return path_or_text


# ══════════════════════════════════════════════════════════════════
# §5  REPORTER
# ══════════════════════════════════════════════════════════════════

_SEV_ICON = {"WARN": "⚠", "ERROR": "✗", "CRITICAL": "🚨"}
_PRI_ICON = {1: "🔴", 2: "🟡", 3: "🟢"}


def print_report(out: CognitiveKernelOutput) -> None:
    W = 64
    bar = "═" * W

    def line(label: str, val: str, width: int = 28) -> str:
        return f"  {label:<{width}} {val}"

    print(f"\n{bar}")
    print(f"  AGENT-07 · Cognitive Kernel  v2.0")
    print(f"  Session: {out.session_id}  |  {out.timestamp}")
    print(f"  Domain : {out.domain}  |  Trust: {'✓ OK' if out.trust_ok else '✗ FLAGGED'}")
    print(bar)

    print(f"\n{'─'*W}")
    print("  [CRP 4-Stage Scores]")
    print(line("  Stage 1 · Observation",  f"{out.crp_observation:>5.1f} / 25"))
    print(line("  Stage 2 · Encoding",     f"{out.crp_encoding:>5.1f} / 25"))
    print(line("  Stage 3 · Analysis",     f"{out.crp_analysis:>5.1f} / 25"))
    print(line("  Stage 4 · Reconfiguration", f"{out.crp_reconfiguration:>5.1f} / 25"))
    print(line("  ──── CRP Total",         f"{out.crp_total:>5.1f} / 100"))
    print(line("  C₀ (initial state)",     f"{out.c0:>5.1f}"))
    print(line("  C₁ (reconfigured)",      f"{out.c1:>5.1f}"))
    print(line("  Δ  (gap to target)",     f"{out.delta:>+5.1f}"))

    print(f"\n{'─'*W}")
    print("  [PE-3 Axis Scores]")
    print(line("  Risk Completeness",        f"{out.pe3_risk_completeness:>5.1f} / 25"))
    print(line("  Numeric Verifiability",    f"{out.pe3_numeric_verifiability:>5.1f} / 25"))
    print(line("  Scenario Logic",           f"{out.pe3_scenario_logic:>5.1f} / 25"))
    print(line("  Fraud Detection",          f"{out.pe3_fraud_detection:>5.1f} / 20"))
    print(line("  Strategic Executability",  f"{out.pe3_strategic_executability:>5.1f} / 25"))
    print(line("  ──── PE-3 Total",          f"{out.pe3_total:>5.1f} / 100"))

    print(f"\n{'─'*W}")
    print("  [Cognitive Indices]")
    print(line("  MTI (Meta-Thinking Index)",   f"{out.mti:.4f}"))
    print(line("  QLI (Quality Learning Index)", f"{out.qli:+.4f}"))

    if out.trust_flags:
        print(f"\n{'─'*W}")
        print("  [Trust Flags]")
        for flag in out.trust_flags:
            icon = _SEV_ICON.get(flag.severity, "?")
            print(f"  {icon} [{flag.severity}] {flag.code}")
            print(f"    → {flag.message}")
            print(f"    ⤷ {flag.suggested_action}")

    print(f"\n{'─'*W}")
    print("  [Top Recommendations]")
    for rec in out.recommendations:
        icon = _PRI_ICON.get(rec.priority, "•")
        print(f"  {icon} P{rec.priority}: {rec.axis}  (score: {rec.current_score})")
        print(f"       {rec.action}")
        print(f"       Expected Δ: +{rec.expected_delta}  |  Hook: {rec.hook or '—'}")

    print(f"\n{'─'*W}")
    print("  [Ecosystem Triggers]")
    for trig in out.ecosystem_triggers:
        print(f"    ▶ {trig}")

    print(f"\n{'─'*W}")
    print("  [KG Registration]")
    kg = out.kg_registration
    print(f"    node_type : {kg.node_type}")
    print(f"    session   : {kg.session_id}  domain: {kg.domain}")
    print(f"    crp_total : {kg.crp_total}  pe3: {kg.pe3_total}  mti: {kg.mti}  qli: {kg.qli}")

    print(f"\n{'─'*W}")
    print(f"  [Next Target]")
    print(f"    {out.next_c_target}")
    print(bar + "\n")


# ══════════════════════════════════════════════════════════════════
# §6  CLI ENTRY POINT
# ══════════════════════════════════════════════════════════════════

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="AGENT-07 Cognitive Kernel v2.0 — CRP 4-Stage Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic run with inline artifact
  python agent_07_cognitive_kernel.py --session C-39 --artifact "risk analysis..."

  # Load from markdown file
  python agent_07_cognitive_kernel.py --session C-39 --artifact reports/rpt_ai_eco.md

  # JSON output for downstream agents
  python agent_07_cognitive_kernel.py --session C-39 --artifact input.md --output json

  # Full pipeline with Notion+GitHub sync
  python agent_07_cognitive_kernel.py --session C-39 --artifact input.md --output notion+github

  # Custom C_target
  python agent_07_cognitive_kernel.py --session C-39 --artifact input.md --target 95
        """
    )
    p.add_argument("--session",  default="C-39",   help="Session ID (e.g. C-39)")
    p.add_argument("--artifact", default="",       help="Artifact text OR path to .md/.txt file")
    p.add_argument("--domain",   default="PE-7",   help="Domain tag (PE-7, INV-STRAT, etc.)")
    p.add_argument("--target",   default=90.0, type=float, help="C_target score (default 90)")
    p.add_argument("--output",   default="stdout",
                   choices=["stdout", "json", "notion+github"],
                   help="Output mode")
    return p


def main() -> None:
    args = _build_parser().parse_args()

    artifact_text = load_artifact(args.artifact) if args.artifact else (
        "risk scenario analysis with IRR NPV EBITDA metrics "
        "strategy roadmap milestone execution fraud detection "
        "bear bull base case DCF valuation sensitivity"
    )

    inp = CognitiveKernelInput(
        session_id=args.session,
        artifact_text=artifact_text,
        domain=args.domain,
        c_target=args.target,
    )

    kernel = CognitiveKernel()
    result = kernel.run(inp)

    if args.output == "json":
        # Serialise dataclasses to JSON
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print_report(result)
        if args.output == "notion+github":
            print("  [→] Triggering downstream AGENT-05 pipeline...")
            print(f"      python agents/run_pipeline.py "
                  f"--agents 07,05,04 --session {args.session}")
            print("  [→] KG registration payload ready for KM-PIPE-MASTER v6.3+")


if __name__ == "__main__":
    main()
