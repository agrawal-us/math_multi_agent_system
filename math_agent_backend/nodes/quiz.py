from __future__ import annotations

import logging

from ..graph.state import AgentState
from ..tools import quiz as quiz_tool

logger = logging.getLogger(__name__)


def quiz_node(state: AgentState) -> AgentState:
    topic = state.get("topic") or state.get("normalized_input") or "general math"
    difficulty = state.get("difficulty") or "medium"
    num_questions = int(state.get("num_questions") or 3)
    questions = quiz_tool.generate_quiz(topic, difficulty, num_questions)
    logger.info(
        "Quiz generated | topic=%s difficulty=%s questions=%s",
        topic,
        difficulty,
        len(questions),
    )
    next_state = {**state}
    next_state.update(
        {
            "quiz": questions,
            "response_type": "quiz",
        }
    )
    return next_state
