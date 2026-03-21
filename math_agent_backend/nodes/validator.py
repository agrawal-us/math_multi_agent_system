from __future__ import annotations

import logging

from ..graph.state import AgentState
from ..graph.trace import append_trace_event, mark_validation, set_current_node
from ..tools import quiz as quiz_tool
from ..tools import solver as solver_tool

logger = logging.getLogger(__name__)


def validator_node(state: AgentState) -> AgentState:
    next_state = set_current_node(state, "validator_node")
    next_state = append_trace_event(
        next_state,
        node="validator_node",
        event_type="node_started",
        details={"response_type": next_state.get("response_type", "unknown")},
    )

    response_type = next_state.get("response_type", "unknown")
    error_message = None
    failure_category = None

    if response_type == "error":
        error_message = next_state.get("explanation") or "Upstream error."
        failure_category = "upstream_error"
        logger.error("Validator received upstream error: %s", error_message)

    elif response_type == "solve":
        equation_text = next_state.get("equation") or next_state.get("normalized_input") or ""
        result_text = next_state.get("result") or ""
        if not equation_text or not solver_tool.verify_solution(equation_text, result_text):
            error_message = "Solution could not be validated."
            failure_category = "solution_verification_failed"

    elif response_type == "quiz":
        quiz_items = next_state.get("quiz", [])
        if not quiz_tool.validate_quiz_structure(quiz_items):
            error_message = "Quiz structure invalid."
            failure_category = "quiz_structure_invalid"

    elif response_type == "concept":
        explanation = next_state.get("explanation") or ""
        if "example" not in explanation.lower():
            error_message = "Explanation missing example."
            failure_category = "concept_missing_example"

    else:
        error_message = "Unrecognized response type."
        failure_category = "unknown_response_type"

    if error_message is None:
        next_state["is_valid"] = True
        next_state = mark_validation(
            next_state,
            passed=True,
            details={"response_type": response_type},
        )
        next_state = append_trace_event(
            next_state,
            node="validator_node",
            event_type="validation_passed",
            details={"response_type": response_type},
        )
        logger.info("Validation succeeded for type=%s", response_type)
        return next_state

    next_state["is_valid"] = False
    next_state["original_response_type"] = response_type
    next_state["response_type"] = "error"
    next_state["explanation"] = error_message
    next_state["retry_count"] = state.get("retry_count", 0) + 1
    next_state = mark_validation(
        next_state,
        passed=False,
        failure_reason=error_message,
        failure_category=failure_category,
        details={"response_type": response_type},
    )
    next_state = append_trace_event(
        next_state,
        node="validator_node",
        event_type="validation_failed",
        details={
            "response_type": response_type,
            "failure_reason": error_message,
            "failure_category": failure_category,
            "retry_count": next_state["retry_count"],
        },
    )
    logger.error("Validation failed for type=%s: %s", response_type, error_message)
    return next_state