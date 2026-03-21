from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from .state import AgentState, INITIAL_STATE
from ..nodes import concept, formatter, planner, quiz, router, solve, validator


def build_workflow() -> StateGraph[AgentState]:
    graph = StateGraph(AgentState)

    # ---- Nodes ----
    graph.add_node("planner_node", planner.planner_node)
    graph.add_node("router_node", router.router_node)
    graph.add_node("solve_node", solve.solve_node)
    graph.add_node("quiz_node", quiz.quiz_node)
    graph.add_node("concept_node", concept.concept_node)
    graph.add_node("validator_node", validator.validator_node)
    graph.add_node("formatter_node", formatter.formatter_node)

    # ---- Edges ----
    graph.add_edge(START, "planner_node")
    graph.add_edge("planner_node", "router_node")

    # ---- Router conditional edges ----
    graph.add_conditional_edges(
        "router_node",
        router.next_node_key,
        {
            "solve_node": "solve_node",
            "quiz_node": "quiz_node",
            "concept_node": "concept_node",
        },
    )

    # ---- Worker → Validator ----
    graph.add_edge("solve_node", "validator_node")
    graph.add_edge("quiz_node", "validator_node")
    graph.add_edge("concept_node", "validator_node")

    # ---- Validator conditional edges ----
    graph.add_conditional_edges(
        "validator_node",
        _validator_route,
        {
            "retry": "planner_node",
            "complete": "formatter_node",
        },
    )

    # ---- Final ----
    graph.add_edge("formatter_node", END)

    return graph


def _validator_route(state: AgentState) -> str:
    """
    Determines whether to retry or complete.
    Max 1 retry allowed.
    """
    if state.get("response_type") == "error":
        return "complete"
    if state.get("is_valid"):
        return "complete"

    if state.get("retry_count", 0) >= 1:
        return "complete"

    return "retry"


# ---- Compile graph ONCE (performance optimization) ----
GRAPH = build_workflow().compile()


def run_workflow(user_input: str) -> dict:
    """
    Entry point for executing the LangGraph workflow.
    """
    initial_state: AgentState = {
        **INITIAL_STATE,
        "user_input": user_input,
    }

    final_state = GRAPH.invoke(initial_state)

    return final_state.get(
        "output",
        {
            "type": "error",
            "data": {"message": "No output produced"},
            "metadata": {"valid": False, "retries": 0},
        },
    )
