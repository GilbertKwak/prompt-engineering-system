"""
CRP-AGENT-FRAMEWORK — Data Models (Phase 1)
Full type hierarchy: CognitiveEvent → CognitiveState → CognitiveTrajectory → CognitiveAsset

TypeScript-compatible schemas for API surface.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional
from uuid import UUID, uuid4


# ─── Enumerations ────────────────────────────────────────────────────────────

class SystemType(str, Enum):
    """Kahneman S1/S2 routing signal."""
    S1 = "S1"  # Fast, heuristic, associative
    S2 = "S2"  # Deliberate, analytical, costly


class ProcessingStage(str, Enum):
    """CRP 4-stage loop stages."""
    CAPTURE = "capture"
    ENCODE = "encode"
    RECONFIGURE = "reconfigure"
    VALIDATE = "validate"


class ExecutionMode(str, Enum):
    DETERMINISTIC = "deterministic"
    PROBABILISTIC = "probabilistic"
    ENSEMBLE = "ensemble"


class IsolationLevel(str, Enum):
    STRICT = "strict"    # Full tenant isolation
    SHARED = "shared"    # Shared infra, isolated data
    HYBRID = "hybrid"    # Shared compute, isolated state


# ─── Core Cognitive Types ────────────────────────────────────────────────────

@dataclass
class CognitiveContext:
    """
    Ambient context for a cognitive session.
    Carries: domain, prior knowledge refs, session lineage.
    
    TypeScript equivalent:
      interface CognitiveContext {
        domain: string;
        session_id: string;  // UUID
        prior_session_ids: string[];
        knowledge_refs: string[];
        metadata: Record<string, any>;
      }
    """
    domain: str
    session_id: UUID = field(default_factory=uuid4)
    prior_session_ids: List[UUID] = field(default_factory=list)
    knowledge_refs: List[str] = field(default_factory=list)  # KG node IDs
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProcessingStep:
    """
    Single step in the CRP 4-stage loop.
    Represents one atomic cognitive operation.
    """
    stage: ProcessingStage
    input_summary: str
    output_summary: str
    duration_ms: float
    confidence: float  # [0.0, 1.0]
    mti_contribution: float  # delta MTI for this step
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CognitiveState:
    """
    Snapshot of cognitive state at a point in time.
    
    MTI (Metacognitive Trajectory Index):
      Measures depth of self-aware reasoning.
      Range: [0.0, 1.0]; threshold for quality gate: 0.75
    
    QLI (Query-Level Intelligence):
      Measures query sophistication (specificity × coherence × novelty).
      Range: [0.0, 1.0]
    
    TypeScript equivalent:
      interface CognitiveState {
        state_id: string;
        session_id: string;
        mti_score: number;   // [0, 1]
        qli_score: number;   // [0, 1]
        reconfiguration_depth: number;
        active_stage: ProcessingStage;
        system_type: SystemType;
        timestamp: string;  // ISO 8601
      }
    """
    session_id: UUID
    mti_score: float = 0.0
    qli_score: float = 0.0
    reconfiguration_depth: int = 0  # Number of reconfiguration cycles completed
    active_stage: ProcessingStage = ProcessingStage.CAPTURE
    system_type: SystemType = SystemType.S1
    state_id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def pe3_score(self) -> float:
        """
        Map CognitiveState to PE-3 validation score.
        PE-3 target: 95+ maps to MTI >= 0.75, QLI >= 0.80
        
        Score = 50 * mti + 30 * qli + 20 * reconfiguration_depth_bonus
        where reconfiguration_depth_bonus = min(reconfiguration_depth / 5, 1.0)
        """
        depth_bonus = min(self.reconfiguration_depth / 5.0, 1.0)
        return 50 * self.mti_score + 30 * self.qli_score + 20 * depth_bonus


# ─── Event & Trajectory ──────────────────────────────────────────────────────

@dataclass
class CognitiveEvent:
    """
    Atomic cognitive event. Lowest granularity in the hierarchy.
    
    Hierarchy position: CognitiveEvent → (aggregates to) CognitiveState
    
    TypeScript equivalent:
      interface CognitiveEvent {
        event_id: string;
        session_id: string;
        event_type: string;
        payload: Record<string, any>;
        state_delta: Partial<CognitiveState>;
        timestamp: string;
      }
    """
    session_id: UUID
    event_type: str  # e.g. "reconfiguration_triggered", "mti_threshold_crossed"
    payload: Dict[str, Any]
    state_delta: Dict[str, Any]  # Fields that changed in CognitiveState
    event_id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class TrajectoryRecord:
    """
    Append-only log entry for the Trajectory Database.
    Immutable after creation — forms the audit trail.
    
    Used by:
      - Trust Layer: anti-gaming detection via trajectory_consistency_score
      - PE-3: confidence chain validation
      - KM-PIPE: assetization trigger
    
    TypeScript equivalent:
      interface TrajectoryRecord {
        record_id: string;
        session_id: string;
        timestamp: string;
        state_before: CognitiveState;
        action: string;
        state_after: CognitiveState;
        mti_delta: number;
        events: CognitiveEvent[];
      }
    """
    session_id: UUID
    state_before: CognitiveState
    action: str
    state_after: CognitiveState
    mti_delta: float
    events: List[CognitiveEvent] = field(default_factory=list)
    record_id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_regression(self) -> bool:
        """True if MTI decreased — potential gaming signal."""
        return self.mti_delta < -0.05


@dataclass
class CognitiveTrajectory:
    """
    Full session trajectory: ordered list of TrajectoryRecords.
    
    Hierarchy position: CognitiveTrajectory = List[TrajectoryRecord]
    
    Provides:
      - trajectory_consistency_score: 1 - variance(mti_deltas)
      - peak_mti: maximum MTI achieved
      - convergence_rate: steps to reach MTI threshold
    """
    session_id: UUID
    records: List[TrajectoryRecord] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def append(self, record: TrajectoryRecord) -> None:
        """Append a new record (immutable after append)."""
        assert record.session_id == self.session_id, "Session ID mismatch"
        self.records.append(record)

    @property
    def mti_deltas(self) -> List[float]:
        return [r.mti_delta for r in self.records]

    @property
    def trajectory_consistency_score(self) -> float:
        """
        Trust Layer anti-gaming metric.
        Score = 1 - variance(mti_deltas)
        Flag if < 0.6 for 3 consecutive records.
        """
        if len(self.mti_deltas) < 2:
            return 1.0
        import statistics
        try:
            var = statistics.variance(self.mti_deltas)
            return max(0.0, 1.0 - var)
        except statistics.StatisticsError:
            return 1.0

    @property
    def peak_mti(self) -> float:
        if not self.records:
            return 0.0
        return max(r.state_after.mti_score for r in self.records)

    @property
    def current_state(self) -> Optional[CognitiveState]:
        if not self.records:
            return None
        return self.records[-1].state_after


@dataclass
class CognitiveAsset:
    """
    Finalized cognitive output ready for assetization.
    
    Hierarchy position: CognitiveTrajectory → (distilled to) CognitiveAsset
    
    Integration:
      - KM-PIPE-MASTER v3.0: triggers Notion sync
      - knowledge_graph v6.3+: creates KG node (n+1 node, e+2 edges)
      - PE-3: asset.quality_score maps to PE-3 validation result
    
    TypeScript equivalent:
      interface CognitiveAsset {
        asset_id: string;
        session_id: string;
        asset_type: 'report' | 'prompt' | 'framework' | 'analysis' | 'insight';
        content: string;
        quality_score: number;  // [0, 100], PE-3 scale
        kg_node_id?: string;
        notion_page_id?: string;
        github_path?: string;
        tags: string[];
        created_at: string;
      }
    """
    session_id: UUID
    asset_type: Literal["report", "prompt", "framework", "analysis", "insight"]
    content: str
    quality_score: float  # PE-3 scale [0, 100]
    tags: List[str] = field(default_factory=list)
    kg_node_id: Optional[str] = None
    notion_page_id: Optional[str] = None
    github_path: Optional[str] = None
    asset_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def is_publication_ready(self) -> bool:
        """PE-3 gate: quality_score >= 95 required for publication."""
        return self.quality_score >= 95.0


# ─── Agent Task & Result ─────────────────────────────────────────────────────

@dataclass
class AgentTask:
    """
    Input specification for Agent Runtime.
    
    TypeScript equivalent:
      interface AgentTask {
        task_id: string;
        query: string;
        context: CognitiveContext;
        execution_mode: ExecutionMode;
        n_ensemble: number;  // used if mode == 'ensemble'
        mti_threshold: number;  // convergence criterion
        max_reconfiguration_loops: number;
      }
    """
    query: str
    context: CognitiveContext
    execution_mode: ExecutionMode = ExecutionMode.DETERMINISTIC
    n_ensemble: int = 1
    mti_threshold: float = 0.75  # Convergence criterion
    max_reconfiguration_loops: int = 3
    task_id: UUID = field(default_factory=uuid4)


@dataclass
class AgentResult:
    """
    Output from Agent Runtime.
    
    TypeScript equivalent:
      interface AgentResult {
        result_id: string;
        task_id: string;
        output: string;
        final_state: CognitiveState;
        confidence: number;  // product of per-step confidences
        ensemble_variance: number;
        pe3_score: number;
        processing_steps: ProcessingStep[];
      }
    """
    task_id: UUID
    output: str
    final_state: CognitiveState
    confidence: float
    ensemble_variance: float = 0.0
    processing_steps: List[ProcessingStep] = field(default_factory=list)
    result_id: UUID = field(default_factory=uuid4)

    @property
    def pe3_score(self) -> float:
        return self.final_state.pe3_score()


@dataclass
class TrustReport:
    """
    Trust Layer output.
    Anti-gaming analysis + confidence chain + explainability.
    
    TypeScript equivalent:
      interface TrustReport {
        report_id: string;
        session_id: string;
        gaming_risk: number;    // [0, 1]; > 0.4 = flag
        confidence_chain: number[];  // per-step confidences
        confidence_final: number;    // product of chain
        consistency_score: number;   // trajectory consistency
        explanations: string[];      // causal attribution per step
        is_trusted: boolean;
      }
    """
    session_id: UUID
    gaming_risk: float  # [0, 1]; > 0.4 triggers flag
    confidence_chain: List[float]
    consistency_score: float
    explanations: List[str]
    report_id: UUID = field(default_factory=uuid4)
    generated_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def confidence_final(self) -> float:
        """Product of confidence chain (propagated confidence)."""
        result = 1.0
        for c in self.confidence_chain:
            result *= c
        return result

    @property
    def is_trusted(self) -> bool:
        """True if gaming risk low AND confidence acceptable."""
        return self.gaming_risk < 0.4 and self.confidence_final > 0.5
