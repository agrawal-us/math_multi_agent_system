from __future__ import annotations

import logging

from ..tools import solver
from ..tools.solver import EquationParseError
from ..graph.state import AgentState
from ..graph.trace import append_trace_event, set_current_node

logger = logging.getLogger(__name__)


def solve_node(state: AgentState) -> AgentState:
    next_state = set_current_node(state, "solve_node")
    next_state = append_trace_event(
        next_state,
        node="solve_node",
        event_type="node_started",
        details={"equation_text": next_state.get("normalized_input", "")},
    )
    equation_text = next_state.get("normalized_input", "")

    try:
        solve_result = solver.solve_equation(equation_text)
        logger.info(
            "Solved equation | equation=%s | solution=%s",
            equation_text,
            solve_result.solution,
        )

        next_state = {
            **next_state,
            "result": solve_result.solution,
            "steps": solve_result.steps,
            "response_type": "solve",
            "is_valid": True,
        }
        next_state = append_trace_event(
            next_state,
            node="solve_node",
            event_type="node_completed",
            details={
                "equation_text": equation_text,
                "solution": solve_result.solution,
                "step_count": len(solve_result.steps),
            },
        )
        return next_state

    except EquationParseError as e:
        logger.error("Equation parse failed | equation=%s | error=%s", equation_text, e)

        error_state: AgentState = {
            **next_state,
            "response_type": "error",
            "explanation": str(e),
            "is_valid": False,
            "failure_category": "parse_error",
        }
        error_state = append_trace_event(
            error_state,
            node="solve_node",
            event_type="node_failed",
            details={
                "error_type": "EquationParseError",
                "message": str(e),
                "equation_text": equation_text,
            },
        )
        return error_state

    except Exception as e:
        logger.error("Unexpected solve error | equation=%s | error=%s", equation_text, e)

        error_state = {
            **next_state,
            "response_type": "error",
            "explanation": "Unexpected error during solving.",
            "is_valid": False,
            "failure_category": "unexpected_worker_error",
        }
        error_state = append_trace_event(
            error_state,
            node="solve_node",
            event_type="node_failed",
            details={
                "error_type": type(e).__name__,
                "message": str(e),
                "equation_text": equation_text,
            },
        )
        return error_state