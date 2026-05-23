"""
CRP-AGENT-FRAMEWORK — Flow Engine (Phase 1)
DAG + event-driven hybrid orchestration.

Implements:
  - Static DAG: pre-defined workflows (e.g., PE-1 → PE-2 → PE-3 pipeline)
  - Event-driven layer: triggers on cognitive state transitions
  - Conditional branching: if MTI < threshold → reconfiguration route
  - Trajectory-based loops: iterate until convergence

T-09 Integration:
  - PE-7 AI automation: Flow Engine as execution substrate
  - KM-PIPE-MASTER: output node → Notion sync trigger
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from uuid import UUID, uuid4

from crp_framework.models import CognitiveState


# ─── Flow Node Types ─────────────────────────────────────────────────────────

class NodeType(str, Enum):
    START = "start"
    PROCESS = "process"       # Standard processing node
    CONDITION = "condition"   # Branching node (MTI check)
    LOOP = "loop"             # Reconfiguration loop node
    SYNC = "sync"             # Join multiple branches
    END = "end"
    T09_HOOK = "t09_hook"     # T-09 ecosystem integration node


@dataclass
class FlowNode:
    """
    Single node in the flow DAG.

    T09_HOOK nodes represent:
      - PE-1 prompt execution
      - PE-2 validation
      - PE-3 quality scoring
      - KM-PIPE Notion sync
      - KG node creation
    """
    node_id: str
    node_type: NodeType
    label: str
    handler: Optional[Callable] = None  # Callable that executes this node
    condition: Optional[Callable[[CognitiveState], bool]] = None  # For CONDITION nodes
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FlowEdge:
    """Directed edge in the flow DAG."""
    from_node: str
    to_node: str
    label: str = ""
    # For conditional edges: only traverse if condition(state) is True
    condition: Optional[Callable[[CognitiveState], bool]] = None


@dataclass
class FlowDAG:
    """
    Flow definition: nodes + directed edges.

    Predefined flows (Phase 1):
      - PE_PIPELINE: PE-1 → PE-2 → PE-3 (T-09 standard pipeline)
      - CRP_LOOP: Capture → Encode → Reconfigure → Validate
      - MTI_GATE: Process → [MTI check] → Reconfigure or Complete
    """
    flow_id: str
    name: str
    nodes: Dict[str, FlowNode] = field(default_factory=dict)
    edges: List[FlowEdge] = field(default_factory=list)
    entry_node: str = "start"

    def add_node(self, node: FlowNode) -> "FlowDAG":
        self.nodes[node.node_id] = node
        return self

    def add_edge(self, edge: FlowEdge) -> "FlowDAG":
        self.edges.append(edge)
        return self

    def get_successors(
        self,
        node_id: str,
        state: Optional[CognitiveState] = None,
    ) -> List[str]:
        """Get next node IDs, evaluating conditional edges."""
        successors = []
        for edge in self.edges:
            if edge.from_node != node_id:
                continue
            if edge.condition is None:
                successors.append(edge.to_node)
            elif state is not None and edge.condition(state):
                successors.append(edge.to_node)
        return successors


# ─── Predefined T-09 Flows ───────────────────────────────────────────────────

def build_crp_loop_flow(mti_threshold: float = 0.75) -> FlowDAG:
    """
    Standard CRP 4-stage loop flow.
    Branches back to RECONFIGURE if MTI < threshold.
    """
    dag = FlowDAG(flow_id="crp-loop-v1", name="CRP 4-Stage Loop")

    dag.add_node(FlowNode("start", NodeType.START, "Session Start"))
    dag.add_node(FlowNode("capture", NodeType.PROCESS, "Stage 1: Capture"))
    dag.add_node(FlowNode("encode", NodeType.PROCESS, "Stage 2: Encode"))
    dag.add_node(FlowNode("reconfigure", NodeType.LOOP, "Stage 3: Reconfigure"))
    dag.add_node(FlowNode(
        "mti_gate", NodeType.CONDITION, "MTI Quality Gate",
        condition=lambda s: s.mti_score >= mti_threshold,
    ))
    dag.add_node(FlowNode("validate", NodeType.PROCESS, "Stage 4: Validate"))
    dag.add_node(FlowNode("end", NodeType.END, "Session Complete"))

    dag.add_edge(FlowEdge("start", "capture"))
    dag.add_edge(FlowEdge("capture", "encode"))
    dag.add_edge(FlowEdge("encode", "reconfigure"))
    dag.add_edge(FlowEdge("reconfigure", "mti_gate"))
    # Conditional: MTI sufficient → validate
    dag.add_edge(FlowEdge(
        "mti_gate", "validate", label="MTI >= threshold",
        condition=lambda s: s.mti_score >= mti_threshold,
    ))
    # Conditional: MTI insufficient → loop back
    dag.add_edge(FlowEdge(
        "mti_gate", "reconfigure", label="MTI < threshold (loop)",
        condition=lambda s: s.mti_score < mti_threshold,
    ))
    dag.add_edge(FlowEdge("validate", "end"))

    return dag


def build_pe_pipeline_flow() -> FlowDAG:
    """
    T-09 PE pipeline: PE-1 → PE-2 → PE-3 → KM-PIPE → KG.
    Maps to Gilbert's existing automation pipeline.
    """
    dag = FlowDAG(flow_id="t09-pe-pipeline-v1", name="T-09 PE Pipeline")

    dag.add_node(FlowNode("start", NodeType.START, "Pipeline Start"))
    dag.add_node(FlowNode("pe1", NodeType.T09_HOOK, "PE-1: Prompt Execution"))
    dag.add_node(FlowNode("pe2", NodeType.T09_HOOK, "PE-2: Validation"))
    dag.add_node(FlowNode("pe3_gate", NodeType.CONDITION, "PE-3 Quality Gate (≥95)"))
    dag.add_node(FlowNode("pe3_pass", NodeType.PROCESS, "PE-3 Passed"))
    dag.add_node(FlowNode("pe3_fail", NodeType.LOOP, "PE-3 Failed → Reconfigure"))
    dag.add_node(FlowNode("km_pipe", NodeType.T09_HOOK, "KM-PIPE: Notion Sync"))
    dag.add_node(FlowNode("kg_node", NodeType.T09_HOOK, "KG: Node Creation"))
    dag.add_node(FlowNode("end", NodeType.END, "Asset Published"))

    dag.add_edge(FlowEdge("start", "pe1"))
    dag.add_edge(FlowEdge("pe1", "pe2"))
    dag.add_edge(FlowEdge("pe2", "pe3_gate"))
    dag.add_edge(FlowEdge(
        "pe3_gate", "pe3_pass", label="score >= 95",
        condition=lambda s: s.pe3_score() >= 95.0,
    ))
    dag.add_edge(FlowEdge(
        "pe3_gate", "pe3_fail", label="score < 95",
        condition=lambda s: s.pe3_score() < 95.0,
    ))
    dag.add_edge(FlowEdge("pe3_fail", "pe1", label="retry"))
    dag.add_edge(FlowEdge("pe3_pass", "km_pipe"))
    dag.add_edge(FlowEdge("km_pipe", "kg_node"))
    dag.add_edge(FlowEdge("kg_node", "end"))

    return dag


# ─── Flow Engine ─────────────────────────────────────────────────────────────

@dataclass
class ExecutionTrace:
    """Record of flow execution — audit trail."""
    flow_id: str
    execution_id: UUID = field(default_factory=uuid4)
    visited_nodes: List[str] = field(default_factory=list)
    loop_counts: Dict[str, int] = field(default_factory=dict)
    final_state: Optional[CognitiveState] = None
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    success: bool = False

    @property
    def total_loops(self) -> int:
        return sum(self.loop_counts.values())


class FlowEngine:
    """
    CRP-AGENT-FRAMEWORK Flow Engine.

    Executes FlowDAG with:
      - Topological traversal (DAG execution)
      - Event-driven branching on CognitiveState
      - Loop detection and max-iteration guard
      - Execution trace for observability

    Usage:
      engine = FlowEngine()
      flow = build_pe_pipeline_flow()
      trace = engine.execute(flow, initial_state, handlers)
    """

    def __init__(self, max_loop_iterations: int = 10):
        self.max_loop_iterations = max_loop_iterations

    def execute(
        self,
        flow: FlowDAG,
        initial_state: CognitiveState,
        node_handlers: Optional[Dict[str, Callable[[CognitiveState], CognitiveState]]] = None,
    ) -> Tuple[ExecutionTrace, CognitiveState]:
        """
        Execute a FlowDAG from entry_node to END.

        Args:
          flow: FlowDAG definition
          initial_state: Starting CognitiveState
          node_handlers: {node_id: callable(state) -> state}
                         Called when a PROCESS or T09_HOOK node is visited.

        Returns:
          (ExecutionTrace, final_state)
        """
        handlers = node_handlers or {}
        trace = ExecutionTrace(flow_id=flow.flow_id)
        state = initial_state
        current_node = flow.entry_node
        loop_count: Dict[str, int] = {}
        visited: List[str] = []

        while current_node:
            node = flow.nodes.get(current_node)
            if node is None:
                break

            visited.append(current_node)

            # Loop guard
            loop_count[current_node] = loop_count.get(current_node, 0) + 1
            if loop_count[current_node] > self.max_loop_iterations:
                # Force exit to END
                break

            # Execute node handler if provided
            if node.node_type in (
                NodeType.PROCESS, NodeType.T09_HOOK, NodeType.LOOP
            ):
                handler = handlers.get(current_node) or node.handler
                if handler:
                    try:
                        state = handler(state)
                    except Exception:
                        pass  # Node failure is non-fatal in Phase 1

            # Terminal node
            if node.node_type == NodeType.END:
                trace.success = True
                break

            # Traverse to next node(s)
            successors = flow.get_successors(current_node, state)
            current_node = successors[0] if successors else None

        trace.visited_nodes = visited
        trace.loop_counts = loop_count
        trace.final_state = state
        trace.completed_at = datetime.utcnow()
        return trace, state
