from __future__ import annotations

import logging
import re
from typing import Tuple

from ..graph.state import AgentState, Intent
from ..graph.trace import append_trace_event, set_current_node

INTENT_KEYWORDS = {
    "solve": ["solve", "equation", "compute"],
    "quiz": ["quiz", "question", "test"],
    "concept": ["explain", "concept", "what is"],
}

DIFFICULTY_KEYWORDS = {"easy", "medium", "hard"}

logger = logging.getLogger(__name__)


def planner_node(state: AgentState) -> AgentState:
    next_state = set_current_node(state, "planner_node")
    next_state = append_trace_event(
        next_state,
        node="planner_node",
        event_type="node_started",
        details={"user_input": state.get("user_input", "")},
    )

    user_input = next_state.get("user_input", "") or ""
    normalized = user_input.strip()

    intent, intent_reason = _detect_intent_with_reason(normalized)
    math_text = _strip_intent_prefix(normalized).strip() if intent == "solve" else normalized
    equation, equation_reason = (
        _extract_equation_with_reason(math_text) if intent == "solve" else (None, "not_solve_intent")
    )
    topic, difficulty, num_questions = _extract_quiz_entities(normalized)

    next_state.update(
        {
            "normalized_input": math_text,
            "intent": intent,
            "equation": equation,
            "topic": topic or next_state.get("topic"),
            "difficulty": difficulty or next_state.get("difficulty", "medium"),
            "num_questions": num_questions or next_state.get("num_questions", 3),
        }
    )

    next_state = append_trace_event(
        next_state,
        node="planner_node",
        event_type="node_completed",
        details={
            "intent": intent,
            "intent_reason": intent_reason,
            "normalized_input": math_text,
            "equation": equation,
            "equation_reason": equation_reason,
            "topic": next_state.get("topic"),
            "difficulty": next_state.get("difficulty"),
            "num_questions": next_state.get("num_questions"),
        },
    )

    logger.info(
        "Planner intent=%s | equation=%s | topic=%s | difficulty=%s | num_questions=%s",
        intent,
        equation,
        next_state.get("topic"),
        next_state.get("difficulty"),
        next_state.get("num_questions"),
    )
    return next_state


def _detect_intent(text: str) -> Intent:
    intent, _ = _detect_intent_with_reason(text)
    return intent


def _detect_intent_with_reason(text: str) -> tuple[Intent, str]:
    lowered = text.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in lowered:
                return intent, f"keyword_match:{keyword}"
    if any(op in lowered for op in "=+-*/"):
        return "solve", "operator_present"
    if "?" in lowered:
        return "concept", "question_mark_fallback"
    return "concept", "default_concept_fallback"


def _extract_equation(text: str) -> str | None:
    equation, _ = _extract_equation_with_reason(text)
    return equation


def _extract_equation_with_reason(text: str) -> tuple[str | None, str]:
    equation_match = re.search(r"solve\s*(.+)", text, re.IGNORECASE)
    if equation_match:
        return equation_match.group(1).strip(), "solve_prefix_regex"
    equal_match = re.search(r"([\w\s\^\+\-\*/]+=[\w\s\^\+\-\*/]+)", text)
    if equal_match:
        return equal_match.group(1).strip(), "equation_regex"
    if any(op in text for op in "=+-*/"):
        return text, "operator_fallback"
    return None, "no_equation_found"


def _strip_intent_prefix(text: str) -> str:
    pattern = r"^(?:\s*(?:solve|calculate|compute|find)\b)+\s*"
    return re.sub(pattern, "", text, flags=re.IGNORECASE).strip()


def _extract_quiz_entities(text: str) -> Tuple[str | None, str | None, int | None]:
    lowered = text.lower()
    topic = None
    difficulty = None
    num_questions = None

    for level in DIFFICULTY_KEYWORDS:
        if level in lowered:
            difficulty = level
            break

    count_match = re.search(r"(\d+)(?:\s+(?:[a-z]+)\s+)?questions?", lowered)
    if count_match:
        num_questions = int(count_match.group(1))

    topic_match = re.search(r"(?:about|on|regarding)\s+([\w\s]+)", lowered)
    if topic_match:
        topic = topic_match.group(1).strip()
    elif "quiz" in lowered:
        topic = text.strip()

    return topic, difficulty, num_questions