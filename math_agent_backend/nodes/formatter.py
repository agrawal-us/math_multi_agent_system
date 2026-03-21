from __future__ import annotations

import logging

from ..graph.state import AgentState
from ..graph.trace import append_trace_event, set_current_node

logger = logging.getLogger(__name__)


def formatter_node(state: AgentState) -> AgentState:
    next_state = set_current_node(state, "formatter_node")
    next_state = append_trace_event(
        next_state,
        node="formatter_node",
        event_type="node_started",
        details={"response_type": next_state.get("response_type", "unknown")},
    )

    response_type = next_state.get("response_type", "unknown")
    data: dict

    if response_type == "solve":
        data = {"result": next_state.get("result"), "steps": next_state.get("steps", [])}
    elif response_type == "quiz":
        data = {"quiz": next_state.get("quiz", [])}
    elif response_type == "concept":
        data = {"explanation": next_state.get("explanation")}
    else:
        data = {"message": next_state.get("explanation") or next_state.get("result")}
        response_type = "error"

    next_state = append_trace_event(
        next_state,
        node="formatter_node",
        event_type="node_completed",
        details={
            "output_type": response_type,
            "valid": bool(next_state.get("is_valid")),
        },
    )

    metadata = {
        "valid": bool(next_state.get("is_valid")),
        "retries": next_state.get("retry_count", 0),
        "request_id": next_state.get("request_id"),
        "trace_status": next_state.get("trace_status"),
        "route_selected": next_state.get("route_selected"),
        "failure_category": next_state.get("failure_category"),
        "validation_error": next_state.get("validation_error"),
        "event_count": len(next_state.get("trace_events", [])),
        "duration_ms": next_state.get("duration_ms"),
    }

    next_state["output"] = {
        "type": response_type,
        "data": data,
        "metadata": metadata,
        "trace": {
            "request_id": next_state.get("request_id"),
            "started_at": next_state.get("started_at"),
            "finished_at": next_state.get("finished_at"),
            "duration_ms": next_state.get("duration_ms"),
            "status": next_state.get("trace_status"),
            "intent": next_state.get("intent"),
            "route_selected": next_state.get("route_selected"),
            "retry_count": next_state.get("retry_count", 0),
            "validation": next_state.get("trace_validation", {}),
            "events": next_state.get("trace_events", []),
        },
    }

    logger.info(
        "Formatter output | type=%s | valid=%s | retries=%s",
        response_type,
        metadata["valid"],
        metadata["retries"],
    )
    return next_state