from __future__ import annotations

import logging

from ..tools import solver
from ..tools.solver import EquationParseError
from ..graph.state import AgentState

logger = logging.getLogger(__name__)


def solve_node(state: AgentState) -> AgentState:
    equation_text = state.get("normalized_input", "")

    try:
        solve_result = solver.solve_equation(equation_text)
        logger.info(
            "Solved equation | equation=%s | solution=%s",
            equation_text,
            solve_result.solution,
        )
        return {
            **state,
            "result": solve_result.solution,
            "steps": solve_result.steps,
            "response_type": "solve",
            "is_valid": True,
        }

    except EquationParseError as e:
        logger.error("Equation parse failed | equation=%s | error=%s", equation_text, e)

        return {
            **state,
            "response_type": "error",
            "explanation": str(e),
            "is_valid": False,
        }

    except Exception as e:
        logger.error("Unexpected solve error | equation=%s | error=%s", equation_text, e)

        return {
            **state,
            "response_type": "error",
            "explanation": "Unexpected error during solving.",
            "is_valid": False,
        }
