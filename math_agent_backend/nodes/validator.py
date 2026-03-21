from __future__ import annotations

import logging

from ..graph.state import AgentState
from ..tools import quiz as quiz_tool
from ..tools import solver as solver_tool

logger = logging.getLogger(__name__)


def validator_node(state: AgentState) -> AgentState:
    response_type = state.get("response_type", "unknown")
    is_valid = True
    error_message = None

    if response_type == "error":
        logger.error("Validator received upstream error: %s", state.get("explanation"))
        return {**state, "is_valid": False}
    if response_type == "solve":
        equation_text = state.get("equation") or state.get("normalized_input") or ""
        result_text = state.get("result") or ""
        if not equation_text or not solver_tool.verify_solution(equation_text, result_text):
            is_valid = False
            error_message = "Solution could not be validated."
    elif response_type == "quiz":
        quiz_items = state.get("quiz", [])
        if not quiz_tool.validate_quiz_structure(quiz_items):
            is_valid = False
            error_message = "Quiz structure invalid."
    elif response_type == "concept":
        explanation = state.get("explanation") or ""
        if "example" not in explanation.lower():
            is_valid = False
            error_message = "Explanation missing example."
    else:
        is_valid = False
        error_message = "Unrecognized response type."

    next_state = {**state}
    next_state["is_valid"] = is_valid
    if not is_valid:
        next_state["response_type"] = "error"
        next_state["explanation"] = error_message
        next_state["retry_count"] = state.get("retry_count", 0) + 1
        logger.error("Validation failed for type=%s: %s", response_type, error_message)
    else:
        logger.info("Validation succeeded for type=%s", response_type)
    return next_state
