from __future__ import annotations

import logging

from ..tools import solver
from ..tools.solver import EquationParseError
from ..graph.state import AgentState

logger = logging.getLogger(__name__)


def solve_node(state: AgentState) -> AgentState:
    logger.info("Running solve node")

    equation_text = state.get("normalized_input", "")

    try:
        solve_result = solver.solve_equation(equation_text)

        return {
            **state,
            "result": solve_result.solution,
            "steps": solve_result.steps,
            "response_type": "solve",
            "is_valid": True,
        }

    except EquationParseError as e:
        logger.error(f"Equation parse failed: {e}")

        return {
            **state,
            "response_type": "error",
            "explanation": str(e),
            "is_valid": False,
        }

    except Exception as e:
        logger.error(f"Unexpected solve error: {e}")

        return {
            **state,
            "response_type": "error",
            "explanation": "Unexpected error during solving.",
            "is_valid": False,
        }
