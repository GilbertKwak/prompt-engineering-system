"""
CRP-AGENT-FRAMEWORK — Cognitive Kernel (Phase 1)
The core CRP processing unit.

Implements:
  - CRP 4-stage loop: Capture → Encode → Reconfigure → Validate
  - MTI computation: MTI = f(trajectory_depth, reconfiguration_delta, validation_score)
  - QLI computation: QLI = f(specificity, coherence, novelty)
  - System 1 / System 2 routing (Kahneman dual-process)

T-09 Integration:
  - PE-3 gate: pe3_score() >= 95 required for publication
  - PE-ARCH-001: 5-Expert Fusion → n-ensemble config input
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple
from uuid import UUID, uuid4

from crp_framework.models import (
    AgentTask,
    CognitiveContext,
    CognitiveState,
    ProcessingStage,
    ProcessingStep,
    SystemType,
)


# ─── MTI Computation ─────────────────────────────────────────────────────────

def compute_mti(
    trajectory_depth: int,
    reconfiguration_delta: float,
    validation_score: float,
) -> float:
    """
    MTI = f(trajectory_depth, reconfiguration_delta, validation_score)

    Formula:
      MTI = tanh(0.2 * trajectory_depth) * 0.4
            + sigmoid(reconfiguration_delta) * 0.35
            + validation_score * 0.25

    Properties:
      - Bounded [0, 1]
      - Monotonically increasing with depth and validation
      - Saturates at high depth (tanh) — prevents gaming via volume
      - reconfiguration_delta: positive = improvement, negative = regression

    PE-3 target mapping:
      MTI >= 0.75 → PE-3 score >= 95
    """
    depth_component = math.tanh(0.2 * trajectory_depth) * 0.4
    reconfig_component = _sigmoid(reconfiguration_delta) * 0.35
    validation_component = max(0.0, min(1.0, validation_score)) * 0.25
    return depth_component + reconfig_component + validation_component


def compute_qli(
    specificity: float,
    coherence: float,
    novelty: float,
) -> float:
    """
    QLI = f(specificity, coherence, novelty)

    Formula:
      QLI = (specificity * 0.40) + (coherence * 0.35) + (novelty * 0.25)

    All inputs in [0, 1].

    Dimensions:
      - specificity: how precisely the query targets its domain
      - coherence: internal logical consistency
      - novelty: degree of new cognitive territory explored
    """
    return (
        max(0.0, min(1.0, specificity)) * 0.40
        + max(0.0, min(1.0, coherence)) * 0.35
        + max(0.0, min(1.0, novelty)) * 0.25
    )


def _sigmoid(x: float) -> float:
    """Numerically stable sigmoid."""
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    exp_x = math.exp(x)
    return exp_x / (1.0 + exp_x)


# ─── S1/S2 Router ────────────────────────────────────────────────────────────

class SystemRouter:
    """
    Routes incoming queries to S1 (fast/heuristic) or S2 (deliberate) processing.

    Heuristics (Phase 1 implementation — extensible via plugin):
      S2 indicators: multi-step reasoning, novel domain, explicit analysis request,
                     contradiction detection, comparative evaluation
      S1 indicators: factual recall, pattern matching, routine retrieval

    Phase 2: Replace heuristics with learned classifier on CognitiveTrajectory data.
    """

    S2_KEYWORDS = {
        "analyze", "compare", "evaluate", "design", "strategy", "framework",
        "why", "how might", "trade-off", "implication", "consequence",
        "optimize", "reconfigure", "synthesize", "critique", "assess",
    }

    def route(self, query: str, context: CognitiveContext) -> SystemType:
        """
        Returns SystemType.S2 if query requires deliberate processing.
        Default: S1 (conservative — escalate to S2 when needed).
        """
        query_lower = query.lower()
        s2_signals = sum(1 for kw in self.S2_KEYWORDS if kw in query_lower)

        # Context signals: novel domain → S2
        is_new_domain = len(context.prior_session_ids) == 0

        if s2_signals >= 2 or (s2_signals >= 1 and is_new_domain):
            return SystemType.S2
        return SystemType.S1


# ─── Cognitive Kernel ────────────────────────────────────────────────────────

@dataclass
class KernelConfig:
    """Configuration for CognitiveKernel."""
    mti_threshold: float = 0.75          # PE-3 quality gate
    max_reconfiguration_loops: int = 3   # Max CRP loop iterations
    s1_validation_score_default: float = 0.70
    s2_validation_score_default: float = 0.85
    enable_t09_hooks: bool = True        # T-09 ecosystem integration


class CognitiveKernel:
    """
    CRP-AGENT-FRAMEWORK Cognitive Kernel.

    Implements the CRP 4-stage loop:
      1. CAPTURE  — receive query, establish context, route S1/S2
      2. ENCODE   — extract semantic structure, compute initial QLI
      3. RECONFIGURE — apply cognitive transformation, update MTI
      4. VALIDATE — quality gate, PE-3 score check, convergence test

    Design invariants:
      - Every processing step is logged to processing_steps
      - MTI monotonically tracked across reconfiguration loops
      - PE-3 score accessible at any point via state.pe3_score()
      - T-09 hooks fire on state transitions if enable_t09_hooks=True

    Usage:
      kernel = CognitiveKernel()
      state, steps = kernel.process(task)
    """

    def __init__(self, config: Optional[KernelConfig] = None):
        self.config = config or KernelConfig()
        self.router = SystemRouter()
        self._t09_hooks: Dict[str, List[Callable]] = {
            "on_reconfigure": [],
            "on_validate": [],
            "on_mti_threshold_crossed": [],
            "on_complete": [],
        }

    # ── Public API ──────────────────────────────────────────────────────────

    def process(
        self,
        task: AgentTask,
    ) -> Tuple[CognitiveState, List[ProcessingStep]]:
        """
        Execute the CRP 4-stage loop for a given AgentTask.

        Returns:
          (final_state, processing_steps)

        Raises:
          ValueError: if task.context is missing session_id
        """
        steps: List[ProcessingStep] = []
        session_id = task.context.session_id

        # Initial state
        state = CognitiveState(
            session_id=session_id,
            system_type=self.router.route(task.query, task.context),
        )

        # ── Stage 1: CAPTURE ──────────────────────────────────────────────
        t0 = datetime.utcnow()
        state.active_stage = ProcessingStage.CAPTURE
        capture_summary = self._capture(task, state)
        steps.append(ProcessingStep(
            stage=ProcessingStage.CAPTURE,
            input_summary=task.query[:200],
            output_summary=capture_summary,
            duration_ms=self._elapsed_ms(t0),
            confidence=0.95,
            mti_contribution=0.0,  # CAPTURE does not change MTI
        ))

        # ── Stage 2: ENCODE ───────────────────────────────────────────────
        t0 = datetime.utcnow()
        state.active_stage = ProcessingStage.ENCODE
        specificity, coherence, novelty = self._encode(task, state)
        state.qli_score = compute_qli(specificity, coherence, novelty)
        encode_confidence = (specificity + coherence) / 2
        steps.append(ProcessingStep(
            stage=ProcessingStage.ENCODE,
            input_summary=capture_summary,
            output_summary=f"QLI={state.qli_score:.3f} [spec={specificity:.2f}, coh={coherence:.2f}, nov={novelty:.2f}]",
            duration_ms=self._elapsed_ms(t0),
            confidence=encode_confidence,
            mti_contribution=state.qli_score * 0.1,
        ))
        state.mti_score += state.qli_score * 0.1

        # ── Stage 3: RECONFIGURE (loop) ───────────────────────────────────
        for loop_i in range(task.max_reconfiguration_loops):
            t0 = datetime.utcnow()
            state.active_stage = ProcessingStage.RECONFIGURE
            state.reconfiguration_depth += 1

            reconfig_delta, reconfig_summary = self._reconfigure(task, state, loop_i)
            mti_before = state.mti_score
            state.mti_score = compute_mti(
                trajectory_depth=state.reconfiguration_depth,
                reconfiguration_delta=reconfig_delta,
                validation_score=self._default_validation_score(state),
            )
            mti_delta = state.mti_score - mti_before

            reconfig_confidence = min(0.95, 0.70 + loop_i * 0.08)
            steps.append(ProcessingStep(
                stage=ProcessingStage.RECONFIGURE,
                input_summary=f"Loop {loop_i + 1}/{task.max_reconfiguration_loops}",
                output_summary=f"{reconfig_summary} | MTI={state.mti_score:.3f} (Δ{mti_delta:+.3f})",
                duration_ms=self._elapsed_ms(t0),
                confidence=reconfig_confidence,
                mti_contribution=mti_delta,
            ))

            # T-09 hook
            if self.config.enable_t09_hooks:
                self._fire_hook("on_reconfigure", state=state, loop=loop_i)

            # Check convergence
            if state.mti_score >= task.mti_threshold:
                if self.config.enable_t09_hooks:
                    self._fire_hook("on_mti_threshold_crossed", state=state)
                break

        # ── Stage 4: VALIDATE ─────────────────────────────────────────────
        t0 = datetime.utcnow()
        state.active_stage = ProcessingStage.VALIDATE
        validation_score, validate_summary = self._validate(task, state)
        # Final MTI with validation
        state.mti_score = compute_mti(
            trajectory_depth=state.reconfiguration_depth,
            reconfiguration_delta=state.qli_score,
            validation_score=validation_score,
        )
        validate_confidence = validation_score
        steps.append(ProcessingStep(
            stage=ProcessingStage.VALIDATE,
            input_summary=f"MTI={state.mti_score:.3f}",
            output_summary=f"{validate_summary} | PE-3={state.pe3_score():.1f}",
            duration_ms=self._elapsed_ms(t0),
            confidence=validate_confidence,
            mti_contribution=0.0,
        ))

        if self.config.enable_t09_hooks:
            self._fire_hook("on_validate", state=state, validation_score=validation_score)
            self._fire_hook("on_complete", state=state, steps=steps)

        return state, steps

    def register_t09_hook(self, event: str, callback: Callable) -> None:
        """
        Register a T-09 integration callback.

        Events:
          on_reconfigure      — fires after each reconfiguration loop
          on_validate         — fires after validation stage
          on_mti_threshold_crossed — fires when MTI >= threshold
          on_complete         — fires when processing completes

        Example (KM-PIPE integration):
          kernel.register_t09_hook("on_complete", km_pipe.sync_to_notion)
        """
        if event not in self._t09_hooks:
            raise ValueError(f"Unknown event '{event}'. Valid: {list(self._t09_hooks)}")
        self._t09_hooks[event].append(callback)

    # ── Private: Stage Implementations ──────────────────────────────────────

    def _capture(self, task: AgentTask, state: CognitiveState) -> str:
        """Stage 1: Capture — establish cognitive context."""
        domain_ctx = f"domain={task.context.domain}"
        system_ctx = f"system_type={state.system_type.value}"
        refs_ctx = f"knowledge_refs={len(task.context.knowledge_refs)}"
        return f"Captured: {domain_ctx} | {system_ctx} | {refs_ctx}"

    def _encode(
        self, task: AgentTask, state: CognitiveState
    ) -> Tuple[float, float, float]:
        """
        Stage 2: Encode — extract semantic structure.
        Returns (specificity, coherence, novelty).

        Phase 1: Heuristic scoring based on query structure.
        Phase 2: Replace with embedding-based semantic analysis.
        """
        query = task.query
        word_count = len(query.split())

        # Specificity: longer, domain-scoped queries score higher
        specificity = min(1.0, word_count / 50) * 0.6 + (
            0.4 if task.context.domain != "general" else 0.2
        )

        # Coherence: S2 queries assumed more coherent
        coherence = 0.85 if state.system_type == SystemType.S2 else 0.65

        # Novelty: no prior sessions → high novelty
        novelty = 0.9 if not task.context.prior_session_ids else 0.5

        return (
            max(0.0, min(1.0, specificity)),
            max(0.0, min(1.0, coherence)),
            max(0.0, min(1.0, novelty)),
        )

    def _reconfigure(
        self, task: AgentTask, state: CognitiveState, loop_i: int
    ) -> Tuple[float, str]:
        """
        Stage 3: Reconfigure — cognitive transformation.
        Returns (reconfiguration_delta, summary_str).

        Phase 1: Simulated delta based on depth + system type.
        Phase 2: Actual LLM-based reconfiguration with diff tracking.
        """
        base_delta = 0.5 + (loop_i * 0.2)
        if state.system_type == SystemType.S2:
            base_delta += 0.3
        return base_delta, f"Reconfiguration loop {loop_i + 1} applied"

    def _validate(
        self, task: AgentTask, state: CognitiveState
    ) -> Tuple[float, str]:
        """
        Stage 4: Validate — quality gate.
        Returns (validation_score, summary_str).
        """
        score = self._default_validation_score(state)
        passed = state.mti_score >= task.mti_threshold
        status = "PASS" if passed else "FAIL — below MTI threshold"
        return score, f"Validation {status} (threshold={task.mti_threshold})"

    def _default_validation_score(self, state: CognitiveState) -> float:
        if state.system_type == SystemType.S2:
            return self.config.s2_validation_score_default
        return self.config.s1_validation_score_default

    def _fire_hook(self, event: str, **kwargs: Any) -> None:
        for callback in self._t09_hooks.get(event, []):
            try:
                callback(**kwargs)
            except Exception:
                pass  # Hooks are non-blocking

    @staticmethod
    def _elapsed_ms(t0: datetime) -> float:
        return (datetime.utcnow() - t0).total_seconds() * 1000
