from __future__ import annotations

import logging

from ..graph.state import AgentState
from ..graph.trace import append_trace_event, set_current_node
from ..tools.concepts import fetch_concept

logger = logging.getLogger(__name__)


def concept_node(state: AgentState) -> AgentState:
    next_state = set_current_node(state, "concept_node")
    topic = next_state.get("topic") or next_state.get("normalized_input") or "mathematics"
    next_state = append_trace_event(
        next_state,
        node="concept_node",
        event_type="node_started",
        details={"topic": topic},
    )

    concept = fetch_concept(topic)
    source = concept.get("source", "unknown")
    example_text = concept.get("example", "")
    if example_text and not example_text.lower().startswith("example"):
        example_text = f"Example: {example_text}"
    explanation = f"{concept.get('explanation', '').strip()}\n{example_text.strip()}".strip()

    logger.info("Concept explanation prepared for topic='%s'", topic)

    next_state.update(
        {
            "explanation": explanation,
            "response_type": "concept",
        }
    )
    next_state = append_trace_event(
        next_state,
        node="concept_node",
        event_type="node_completed",
        details={
            "topic": topic,
            "source": source,
            "explanation_length": len(explanation),
            "example_present": "example" in explanation.lower(),
        },
    )
    return next_state