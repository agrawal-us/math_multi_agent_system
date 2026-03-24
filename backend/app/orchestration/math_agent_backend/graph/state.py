from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, TypedDict


Intent = Literal["solve", "quiz", "concept", "unknown"]
ResponseType = Literal["solve", "quiz", "concept", "error", "unknown"]

TraceStatus = Literal["running", "completed", "failed"]
TraceEventType = Literal[
    "request_started",
    "node_started",
    "node_completed",
    "route_selected",
    "validation_passed",
    "validation_failed",
    "node_failed",
    "retry_scheduled",
    "request_completed",
    "request_failed",
]


class TraceEvent(TypedDict, total=False):
    seq: int
    timestamp: str
    node: str
    event_type: TraceEventType
    details: Dict[str, Any]


class TraceValidation(TypedDict, total=False):
    passed: bool
    failure_reason: Optional[str]
    failure_category: Optional[str]
    details: Dict[str, Any]


class AgentState(TypedDict, total=False):
    user_input: str
    intent: Intent
    normalized_input: str
    equation: Optional[str]
    topic: Optional[str]
    difficulty: Optional[str]
    num_questions: Optional[int]
    result: Optional[str]
    steps: List[str]
    quiz: List[Dict[str, object]]
    explanation: Optional[str]
    is_valid: bool
    response_type: ResponseType
    retry_count: int
    output: Dict[str, object]

    request_id: str
    started_at: str
    finished_at: Optional[str]
    duration_ms: Optional[float]
    current_node: Optional[str]
    trace_status: TraceStatus
    trace_seq: int
    trace_events: List[TraceEvent]
    route_selected: Optional[str]
    original_response_type: Optional[str]
    failure_category: Optional[str]
    validation_error: Optional[str]
    validation_details: Dict[str, object]
    trace_validation: TraceValidation
    context_summary: Dict[str, object]


INITIAL_STATE: AgentState = {
    "intent": "unknown",
    "normalized_input": "",
    "equation": None,
    "topic": None,
    "difficulty": None,
    "num_questions": None,
    "result": None,
    "steps": [],
    "quiz": [],
    "explanation": None,
    "is_valid": False,
    "response_type": "unknown",
    "retry_count": 0,
    "output": {"type": "unknown", "data": {}},
    "request_id": "",
    "started_at": "",
    "finished_at": None,
    "duration_ms": None,
    "current_node": None,
    "trace_status": "running",
    "trace_seq": 0,
    "trace_events": [],
    "route_selected": None,
    "original_response_type": None,
    "failure_category": None,
    "validation_error": None,
    "validation_details": {},
    "trace_validation": {
        "passed": False,
        "failure_reason": None,
        "failure_category": None,
        "details": {},
    },
    "context_summary": {},
}