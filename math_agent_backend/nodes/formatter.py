from __future__ import annotations

import logging

from ..graph.state import AgentState

logger = logging.getLogger(__name__)


def formatter_node(state: AgentState) -> AgentState:
    response_type = state.get("response_type", "unknown")
    data: dict
    if response_type == "solve":
        data = {"result": state.get("result"), "steps": state.get("steps", [])}
    elif response_type == "quiz":
        data = {"quiz": state.get("quiz", [])}
    elif response_type == "concept":
        data = {"explanation": state.get("explanation")}
    else:
        data = {"message": state.get("explanation") or state.get("result")}
        response_type = "error"

    metadata = {
        "valid": bool(state.get("is_valid")),
        "retries": state.get("retry_count", 0),
    }

    next_state = {**state}
    next_state["output"] = {"type": response_type, "data": data, "metadata": metadata}
    logger.info(
        "Formatter output | type=%s | valid=%s | retries=%s",
        response_type,
        metadata["valid"],
        metadata["retries"],
    )
    return next_state
