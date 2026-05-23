"""
CRP-AGENT-FRAMEWORK v0.1.0 — Phase 1
Cognitive Reconfiguration Protocol Native Agent Framework

Architecture: Cognitive Kernel → Agent Runtime → Flow Engine
             → State Engine → Trust Layer → Output

T-09 Integration:
  - KM-PIPE-MASTER v3.0: output pipeline hook
  - PE-3: Trust Layer confidence → validation score
  - PE-7: Flow Engine as automation substrate
  - knowledge_graph v6.3+: CognitiveAsset → KG node
"""

__version__ = "0.1.0"
__phase__ = "Phase 1 — Foundation"

from crp_framework.models import (
    CognitiveEvent,
    CognitiveState,
    CognitiveTrajectory,
    CognitiveAsset,
    CognitiveContext,
    AgentTask,
    AgentResult,
    TrustReport,
    TrajectoryRecord,
)
from crp_framework.cognitive_kernel import CognitiveKernel
from crp_framework.state_engine import StateEngine
from crp_framework.flow_engine import FlowEngine

__all__ = [
    "CognitiveKernel",
    "StateEngine",
    "FlowEngine",
    "CognitiveEvent",
    "CognitiveState",
    "CognitiveTrajectory",
    "CognitiveAsset",
    "CognitiveContext",
    "AgentTask",
    "AgentResult",
    "TrustReport",
    "TrajectoryRecord",
]
