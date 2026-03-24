from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from .state import AgentState


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_trace_event(
    state: AgentState,
    *,
    node: str,
    event_type: str,
    details: Optional[Dict[str, Any]] = None,
) -> AgentState:
    next_state = {**state}
    seq = int(next_state.get("trace_seq", 0)) + 1
    events = list(next_state.get("trace_events", []))
    events.append(
        {
            "seq": seq,
            "timestamp": utc_now_iso(),
            "node": node,
            "event_type": event_type,
            "details": details or {},
        }
    )
    next_state["trace_seq"] = seq
    next_state["trace_events"] = events
    return next_state


def set_current_node(state: AgentState, node: str) -> AgentState:
    next_state = {**state}
    next_state["current_node"] = node
    return next_state


def mark_validation(
    state: AgentState,
    *,
    passed: bool,
    failure_reason: str | None = None,
    failure_category: str | None = None,
    details: Optional[Dict[str, Any]] = None,
) -> AgentState:
    next_state = {**state}
    next_state["trace_validation"] = {
        "passed": passed,
        "failure_reason": failure_reason,
        "failure_category": failure_category,
        "details": details or {},
    }
    next_state["validation_error"] = failure_reason
    next_state["failure_category"] = failure_category
    next_state["validation_details"] = details or {}
    return next_state


def finalize_trace(
    state: AgentState,
    *,
    status: str,
    finished_at: str,
    duration_ms: float,
) -> AgentState:
    next_state = {**state}
    next_state["trace_status"] = status
    next_state["finished_at"] = finished_at
    next_state["duration_ms"] = duration_ms
    return next_state