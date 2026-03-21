from __future__ import annotations

import logging
from typing import Dict

from ..graph.state import AgentState

ROUTE_MAP: Dict[str, str] = {
    "solve": "solve_node",
    "quiz": "quiz_node",
    "concept": "concept_node",
    "unknown": "concept_node",
}

logger = logging.getLogger(__name__)


def router_node(state: AgentState) -> AgentState:
    return state


def next_node_key(state: AgentState) -> str:
    intent = state.get("intent", "concept") or "concept"
    route = ROUTE_MAP.get(intent, "concept_node")
    logger.info("Router selected route=%s for intent=%s", route, intent)
    return route
