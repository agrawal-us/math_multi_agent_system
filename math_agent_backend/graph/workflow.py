from __future__ import annotations

import logging
import time
import uuid

from langgraph.graph import END, START, StateGraph

from .state import AgentState, INITIAL_STATE
from .trace import append_trace_event, finalize_trace, utc_now_iso
from ..nodes import concept, formatter, planner, quiz, router, solve, validator

logger = logging.getLogger(__name__)


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
    logger.info("Workflow start | input=%s", user_input)
    start_time = time.perf_counter()

    request_id = str(uuid.uuid4())
    started_at = utc_now_iso()

    initial_state: AgentState = {
        **INITIAL_STATE,
        "user_input": user_input,
        "request_id": request_id,
        "started_at": started_at,
        "trace_status": "running",
    }
    initial_state = append_trace_event(
        initial_state,
        node="workflow",
        event_type="request_started",
        details={"user_input": user_input},
    )

    try:
        final_state = GRAPH.invoke(initial_state)
    except Exception as exc:
        duration_ms = (time.perf_counter() - start_time) * 1000
        failed_state: AgentState = {
            **initial_state,
            "response_type": "error",
            "explanation": "Unhandled workflow error.",
        }
        failed_state = append_trace_event(
            failed_state,
            node="workflow",
            event_type="request_failed",
            details={
                "error_type": type(exc).__name__,
                "message": str(exc),
            },
        )
        failed_state = finalize_trace(
            failed_state,
            status="failed",
            finished_at=utc_now_iso(),
            duration_ms=duration_ms,
        )
        logger.exception("Workflow failed | request_id=%s", request_id)
        return {
            "type": "error",
            "data": {"message": "Unhandled workflow error."},
            "metadata": {
                "valid": False,
                "retries": failed_state.get("retry_count", 0),
                "request_id": failed_state.get("request_id"),
                "trace_status": failed_state.get("trace_status"),
                "duration_ms": failed_state.get("duration_ms"),
                "event_count": len(failed_state.get("trace_events", [])),
            },
            "trace": {
                "request_id": failed_state.get("request_id"),
                "events": failed_state.get("trace_events", []),
                "status": failed_state.get("trace_status"),
                "duration_ms": failed_state.get("duration_ms"),
            },
        }

    finished_at = utc_now_iso()
    duration_ms = (time.perf_counter() - start_time) * 1000
    final_state = finalize_trace(
        final_state,
        status="completed",
        finished_at=finished_at,
        duration_ms=duration_ms,
    )
    final_state = append_trace_event(
        final_state,
        node="workflow",
        event_type="request_completed",
        details={
            "response_type": final_state.get("response_type"),
            "retry_count": final_state.get("retry_count", 0),
            "duration_ms": duration_ms,
        },
    )

    output = final_state.get(
        "output",
        {
            "type": "error",
            "data": {"message": "No output produced"},
            "metadata": { "valid": False, "retries": 0},
        },
    )

    output.setdefault("metadata", {})
    output["metadata"].update(
        {
            "request_id": final_state.get("request_id"),
            "trace_status": final_state.get("trace_status"),
            "duration_ms": final_state.get("duration_ms"),
            "event_count": len(final_state.get("trace_events", [])),
            "route_selected": final_state.get("route_selected"),
            "failure_category": final_state.get("failure_category"),
        }
    )
    output["trace"] = {
        "request_id": final_state.get("request_id"),
        "started_at": final_state.get("started_at"),
        "finished_at": final_state.get("finished_at"),
        "duration_ms": final_state.get("duration_ms"),
        "status": final_state.get("trace_status"),
        "intent": final_state.get("intent"),
        "route_selected": final_state.get("route_selected"),
        "retry_count": final_state.get("retry_count", 0),
        "validation": final_state.get("trace_validation", {}),
        "events": final_state.get("trace_events", []),
    }

    logger.info(
        "Workflow completed | type=%s | retries=%s | duration_ms=%.2f",
        output.get("type"),
        final_state.get("retry_count", 0),
        duration_ms,
    )
    return output