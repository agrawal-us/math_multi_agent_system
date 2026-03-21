from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Sequence

import sympy as sp


@dataclass
class SolveResult:
    solution: str
    steps: List[str]


class EquationParseError(Exception):
    pass


# ----------------------------
# Input Validation (CRITICAL FIX)
# ----------------------------
def _is_valid_math_input(text: str) -> bool:
    """
    Prevent invalid inputs like 'nonsense'
    """

    # Must contain at least one digit or math operator
    if not re.search(r"[0-9=+\-*/()]", text):
        return False

    # Reject purely alphabetic strings
    if re.fullmatch(r"[a-zA-Z\s]+", text):
        return False

    return True


# ----------------------------
# Normalization Layer
# ----------------------------
def _normalize_expression(expr: str) -> str:
    expr = expr.strip()

    # 2x -> 2*x
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)

    # 2(x+1) -> 2*(x+1)
    expr = re.sub(r'(\d)\(', r'\1*(', expr)

    # )( -> )*(
    expr = re.sub(r'\)\(', r')*(', expr)

    return expr


# ----------------------------
# Parsing
# ----------------------------
def parse_equation(text: str) -> sp.Eq:
    cleaned = text.strip()

    if not cleaned:
        raise EquationParseError("No equation provided.")

    # 🔥 NEW VALIDATION
    if not _is_valid_math_input(cleaned):
        raise EquationParseError("Input does not appear to be a valid math expression.")

    try:
        if "=" in cleaned:
            left_str, right_str = cleaned.split("=", maxsplit=1)

            left_str = _normalize_expression(left_str.strip())
            right_str = _normalize_expression(right_str.strip())

            left = sp.sympify(left_str)
            right = sp.sympify(right_str)

            return sp.Eq(left, right)

        else:
            expr = _normalize_expression(cleaned)
            return sp.Eq(sp.sympify(expr), 0)

    except Exception as e:
        raise EquationParseError(f"Failed to parse equation: {e}")


# ----------------------------
# Solve Logic
# ----------------------------
def solve_equation(equation_text: str) -> SolveResult:
    equation = parse_equation(equation_text)

    symbols = list(equation.free_symbols)
    target_symbol = symbols[0] if symbols else sp.symbols("x")

    solution = sp.solve(equation, target_symbol)

    solution_text = _format_solution(target_symbol, solution)
    steps = _build_steps(equation_text, target_symbol, solution)

    return SolveResult(solution=solution_text, steps=steps)


# ----------------------------
# Validation Logic
# ----------------------------
def verify_solution(equation_text: str, proposed: str) -> bool:
    if "=" not in proposed:
        return False

    equation = parse_equation(equation_text)

    symbols = list(equation.free_symbols)
    target_symbol = symbols[0] if symbols else sp.symbols("x")

    try:
        proposed_expr = sp.sympify(proposed.split("=")[-1])
    except (sp.SympifyError, ValueError):
        return False

    lhs = equation.lhs.subs(target_symbol, proposed_expr)
    rhs = equation.rhs.subs(target_symbol, proposed_expr)

    return sp.simplify(lhs - rhs) == 0


# ----------------------------
# Helpers
# ----------------------------
def _format_solution(symbol: sp.Symbol, solution: Sequence[sp.Expr]) -> str:
    if not solution:
        return "No solution found"

    if len(solution) == 1:
        return f"{symbol} = {sp.simplify(solution[0])}"

    joined = ", ".join(str(sp.simplify(val)) for val in solution)
    return f"{symbol} ∈ {{{joined}}}"


def _build_steps(
    equation_text: str,
    symbol: sp.Symbol,
    solution: Sequence[sp.Expr],
) -> List[str]:
    return [
        f"Start with equation: {equation_text}",
        f"Solve for {symbol}",
        f"Computed solution: {solution if solution else 'No solution'}",
    ]
