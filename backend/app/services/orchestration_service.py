"""Adapter layer around the preserved MVP orchestration package."""

from app.orchestration.math_agent_backend.graph.workflow import run_workflow


def process_chat_message(message: str) -> dict:
    """
    Safe pass-through to existing orchestrator.

    TODO: add persistence, telemetry fan-out, and auth context propagation.
    """
    return run_workflow(message)
