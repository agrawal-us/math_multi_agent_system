from __future__ import annotations

import logging
from typing import Dict

from ..graph.state import AgentState
from ..graph.trace import append_trace_event, set_current_node

ROUTE_MAP: Dict[str, str] = {
    "solve": "solve_node",
    "quiz": "quiz_node",
    "concept": "concept_node",
    "unknown": "concept_node",
}

logger = logging.getLogger(__name__)


def router_node(state: AgentState) -> AgentState:
    next_state = set_current_node(state, "router_node")

    intent = next_state.get("intent", "concept") or "concept"
    route = ROUTE_MAP.get(intent, "concept_node")

    next_state["route_selected"] = route
    next_state = append_trace_event(
        next_state,
        node="router_node",
        event_type="node_started",
        details={"intent": intent},
    )
    next_state = append_trace_event(
        next_state,
        node="router_node",
        event_type="route_selected",
        details={
            "intent": intent,
            "route": route,
            "used_fallback": intent not in ROUTE_MAP,
        },
    )

    logger.info("Router selected route=%s for intent=%s", route, intent)
    return next_state


def next_node_key(state: AgentState) -> str:
    route = state.get("route_selected") or "concept_node"
    return route