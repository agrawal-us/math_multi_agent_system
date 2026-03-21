from __future__ import annotations

import logging

from ..graph.state import AgentState
from ..tools.concepts import fetch_concept

logger = logging.getLogger(__name__)


def concept_node(state: AgentState) -> AgentState:
    topic = state.get("topic") or state.get("normalized_input") or "mathematics"
    concept = fetch_concept(topic)
    explanation = f"{concept['explanation']}\n{concept['example']}"
    logger.info("Concept explanation prepared for topic='%s'", topic)
    next_state = {**state}
    next_state.update(
        {
            "explanation": explanation,
            "response_type": "concept",
        }
    )
    return next_state
