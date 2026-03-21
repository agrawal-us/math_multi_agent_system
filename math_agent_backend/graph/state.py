from __future__ import annotations

from typing import Dict, List, Literal, Optional, TypedDict


Intent = Literal["solve", "quiz", "concept", "unknown"]
ResponseType = Literal["solve", "quiz", "concept", "error", "unknown"]


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
}
