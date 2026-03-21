from __future__ import annotations

import logging

from ..graph.state import AgentState
from ..graph.trace import append_trace_event, set_current_node
from ..tools import quiz as quiz_tool

logger = logging.getLogger(__name__)


def quiz_node(state: AgentState) -> AgentState:
    next_state = set_current_node(state, "quiz_node")
    next_state = append_trace_event(
        next_state,
        node="quiz_node",
        event_type="node_started",
        details={
            "topic": next_state.get("topic") or next_state.get("normalized_input"),
            "difficulty": next_state.get("difficulty") or "medium",
            "num_questions": int(next_state.get("num_questions") or 3),
        },
    )

    topic = next_state.get("topic") or next_state.get("normalized_input") or "general math"
    difficulty = next_state.get("difficulty") or "medium"
    num_questions = int(next_state.get("num_questions") or 3)

    questions, quiz_diagnostics = quiz_tool.generate_quiz_with_diagnostics(
        topic, difficulty, num_questions
    )

    logger.info(
        "Quiz generated | topic=%s difficulty=%s questions=%s",
        topic,
        difficulty,
        len(questions),
    )

    next_state.update(
        {
            "quiz": questions,
            "response_type": "quiz",
        }
    )
    next_state = append_trace_event(
        next_state,
        node="quiz_node",
        event_type="node_completed",
        details=quiz_diagnostics,
    )
    return next_state