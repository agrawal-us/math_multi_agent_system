from __future__ import annotations

import logging
import re
from typing import Tuple

from ..graph.state import AgentState, Intent

INTENT_KEYWORDS = {
    "solve": ["solve", "equation", "compute"],
    "quiz": ["quiz", "question", "test"],
    "concept": ["explain", "concept", "what is"],
}

DIFFICULTY_KEYWORDS = {"easy", "medium", "hard"}

logger = logging.getLogger(__name__)


def planner_node(state: AgentState) -> AgentState:
    user_input = state.get("user_input", "") or ""
    normalized = user_input.strip()
    intent = _detect_intent(normalized)
    math_text = _strip_intent_prefix(normalized).strip() if intent == "solve" else normalized
    equation = _extract_equation(math_text) if intent == "solve" else None
    topic, difficulty, num_questions = _extract_quiz_entities(normalized)

    next_state = {**state}
    next_state.update(
        {
            "normalized_input": math_text,
            "intent": intent,
            "equation": equation,
            "topic": topic or state.get("topic"),
            "difficulty": difficulty or state.get("difficulty", "medium"),
            "num_questions": num_questions or state.get("num_questions", 3),
        }
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
    lowered = text.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in lowered:
                return intent  # type: ignore[return-value]
    if any(op in lowered for op in "=+-*/"):
        return "solve"
    if "?" in lowered:
        return "concept"
    return "concept"


def _extract_equation(text: str) -> str | None:
    equation_match = re.search(r"solve\s*(.+)", text, re.IGNORECASE)
    if equation_match:
        return equation_match.group(1).strip()
    equal_match = re.search(r"([\w\s\^\+\-\*/]+=[\w\s\^\+\-\*/]+)", text)
    if equal_match:
        return equal_match.group(1).strip()
    return text if any(op in text for op in "=+-*/") else None


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
