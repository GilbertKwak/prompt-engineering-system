"""
CRP-AGENT-FRAMEWORK — State Engine (Phase 1)
Cognitive state persistence and trajectory management.

Implements:
  - Session state: in-memory CognitiveState per agent session
  - Trajectory database: append-only TrajectoryRecord log
  - Time-series indexing: query cognitive evolution over time
  - Event logs: full audit trail for anti-gaming analysis

T-09 Integration:
  - KM-PIPE-MASTER v3.0: assetization trigger on trajectory completion
  - knowledge_graph v6.3+: CognitiveAsset → KG node creation hook
"""

from __future__ import annotations
from collections import defaultdict
from datetime import datetime
from typing import Callable, Dict, Iterator, List, Optional, Tuple
from uuid import UUID

from crp_framework.models import (
    CognitiveAsset,
    CognitiveEvent,
    CognitiveState,
    CognitiveTrajectory,
    TrajectoryRecord,
)


class TrajectoryDB:
    """
    Append-only in-memory trajectory database.

    Design:
      - Immutable records: once appended, records cannot be modified
      - Indexed by session_id for O(1) lookup
      - Time-range queries supported: between(t1, t2)
      - Phase 2: swap backing store to PostgreSQL/TimescaleDB

    Query API (mirrors the spec):
      db.where(session_id=X).between(t1, t2).aggregate("mti_delta")
    """

    def __init__(self):
        self._records: Dict[UUID, List[TrajectoryRecord]] = defaultdict(list)
        self._events: Dict[UUID, List[CognitiveEvent]] = defaultdict(list)
        self._assets: Dict[UUID, List[CognitiveAsset]] = defaultdict(list)

    # ── Write Operations ─────────────────────────────────────────────────────

    def append_record(self, record: TrajectoryRecord) -> None:
        """Append a TrajectoryRecord. Immutable after append."""
        self._records[record.session_id].append(record)

    def append_event(self, event: CognitiveEvent) -> None:
        """Append a CognitiveEvent to the event log."""
        self._events[event.session_id].append(event)

    def store_asset(self, asset: CognitiveAsset) -> None:
        """Store a finalized CognitiveAsset."""
        self._assets[asset.session_id].append(asset)

    # ── Query Operations ─────────────────────────────────────────────────────

    def where(self, session_id: UUID) -> "TrajectoryQuery":
        """Start a fluent query for a session."""
        return TrajectoryQuery(self._records.get(session_id, []))

    def get_trajectory(self, session_id: UUID) -> Optional[CognitiveTrajectory]:
        """Reconstruct full CognitiveTrajectory for a session."""
        records = self._records.get(session_id)
        if not records:
            return None
        traj = CognitiveTrajectory(session_id=session_id)
        for r in records:
            traj.records.append(r)
        return traj

    def get_events(
        self,
        session_id: UUID,
        event_type: Optional[str] = None,
    ) -> List[CognitiveEvent]:
        """Retrieve events, optionally filtered by type."""
        events = self._events.get(session_id, [])
        if event_type:
            return [e for e in events if e.event_type == event_type]
        return events

    def get_assets(
        self,
        session_id: UUID,
        min_quality_score: float = 0.0,
    ) -> List[CognitiveAsset]:
        """Retrieve assets above quality threshold."""
        return [
            a for a in self._assets.get(session_id, [])
            if a.quality_score >= min_quality_score
        ]

    def all_sessions(self) -> List[UUID]:
        """List all session IDs with records."""
        return list(self._records.keys())

    def stats(self) -> Dict:
        """DB-level statistics for observability."""
        total_records = sum(len(v) for v in self._records.values())
        total_events = sum(len(v) for v in self._events.values())
        total_assets = sum(len(v) for v in self._assets.values())
        return {
            "sessions": len(self._records),
            "records": total_records,
            "events": total_events,
            "assets": total_assets,
        }


class TrajectoryQuery:
    """
    Fluent query builder for TrajectoryDB.

    Usage:
      db.where(session_id).between(t1, t2).aggregate("mti_delta")
    """

    def __init__(self, records: List[TrajectoryRecord]):
        self._records = list(records)

    def between(self, t1: datetime, t2: datetime) -> "TrajectoryQuery":
        """Filter records within time range."""
        self._records = [
            r for r in self._records
            if t1 <= r.timestamp <= t2
        ]
        return self

    def regressions_only(self) -> "TrajectoryQuery":
        """Filter to records where MTI decreased (anti-gaming signal)."""
        self._records = [r for r in self._records if r.is_regression]
        return self

    def aggregate(self, field: str) -> float:
        """
        Aggregate a numeric field across filtered records.
        Supported: 'mti_delta'
        """
        if not self._records:
            return 0.0
        values = [getattr(r, field, 0.0) for r in self._records]
        return sum(values)

    def count(self) -> int:
        return len(self._records)

    def to_list(self) -> List[TrajectoryRecord]:
        return self._records


class StateEngine:
    """
    CRP-AGENT-FRAMEWORK State Engine.

    Manages:
      1. Active session states (in-memory CognitiveState per session)
      2. Trajectory database (append-only audit log)
      3. T-09 hooks for assetization and KG node creation

    Usage:
      engine = StateEngine()
      engine.init_session(session_id, context)
      engine.record_transition(session_id, state_before, action, state_after, events)
      trajectory = engine.get_trajectory(session_id)
    """

    def __init__(self):
        self.db = TrajectoryDB()
        self._active_states: Dict[UUID, CognitiveState] = {}
        self._t09_hooks: Dict[str, List[Callable]] = {
            "on_asset_created": [],    # → KM-PIPE-MASTER v3.0
            "on_kg_node_trigger": [],  # → knowledge_graph v6.3+
            "on_session_complete": [], # → PE-3 validation
        }

    # ── Session Lifecycle ────────────────────────────────────────────────────

    def init_session(self, state: CognitiveState) -> None:
        """Initialize a new cognitive session."""
        self._active_states[state.session_id] = state

    def get_state(self, session_id: UUID) -> Optional[CognitiveState]:
        """Retrieve current state for a session."""
        return self._active_states.get(session_id)

    def close_session(self, session_id: UUID) -> Optional[CognitiveTrajectory]:
        """
        Close a session and return its full trajectory.
        Fires T-09 on_session_complete hook.
        """
        trajectory = self.db.get_trajectory(session_id)
        self._active_states.pop(session_id, None)
        if trajectory:
            self._fire_hook("on_session_complete", trajectory=trajectory)
        return trajectory

    # ── State Transitions ─────────────────────────────────────────────────────

    def record_transition(
        self,
        state_before: CognitiveState,
        action: str,
        state_after: CognitiveState,
        events: Optional[List[CognitiveEvent]] = None,
    ) -> TrajectoryRecord:
        """
        Record a cognitive state transition.
        Updates active state and appends to trajectory DB.
        """
        mti_delta = state_after.mti_score - state_before.mti_score
        record = TrajectoryRecord(
            session_id=state_after.session_id,
            state_before=state_before,
            action=action,
            state_after=state_after,
            mti_delta=mti_delta,
            events=events or [],
        )
        self.db.append_record(record)
        self._active_states[state_after.session_id] = state_after
        for event in (events or []):
            self.db.append_event(event)
        return record

    # ── Assetization (T-09 Hook) ──────────────────────────────────────────────

    def assetize(
        self,
        session_id: UUID,
        content: str,
        asset_type: str = "analysis",
        tags: Optional[List[str]] = None,
    ) -> CognitiveAsset:
        """
        Convert session output to a CognitiveAsset.
        Fires KM-PIPE and KG hooks.

        T-09 flow:
          assetize() → on_asset_created → KM-PIPE-MASTER v3.0 (Notion sync)
                     → on_kg_node_trigger → knowledge_graph v6.3+ (KG node)
        """
        state = self._active_states.get(session_id)
        quality_score = state.pe3_score() if state else 0.0

        asset = CognitiveAsset(
            session_id=session_id,
            asset_type=asset_type,  # type: ignore
            content=content,
            quality_score=quality_score,
            tags=tags or [],
        )
        self.db.store_asset(asset)
        self._fire_hook("on_asset_created", asset=asset)
        self._fire_hook("on_kg_node_trigger", asset=asset)
        return asset

    # ── T-09 Hook Registration ────────────────────────────────────────────────

    def register_t09_hook(self, event: str, callback: Callable) -> None:
        """
        Register T-09 ecosystem hooks.

        Events:
          on_asset_created    → KM-PIPE-MASTER v3.0 Notion sync
          on_kg_node_trigger  → knowledge_graph v6.3+ node creation
          on_session_complete → PE-3 final validation trigger

        Example:
          engine.register_t09_hook("on_asset_created", km_pipe.sync)
          engine.register_t09_hook("on_kg_node_trigger", kg.create_node)
        """
        if event not in self._t09_hooks:
            raise ValueError(f"Unknown event: {event}")
        self._t09_hooks[event].append(callback)

    def _fire_hook(self, event: str, **kwargs) -> None:
        for cb in self._t09_hooks.get(event, []):
            try:
                cb(**kwargs)
            except Exception:
                pass
