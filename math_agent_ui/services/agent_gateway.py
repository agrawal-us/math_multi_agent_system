from __future__ import annotations

import random
from datetime import datetime
from typing import List, Optional

INTENT_KEYWORDS = {
    "clarification": ["clarify", "explain", "why", "how"],
    "calculation": ["solve", "calculate", "compute", "derivative", "integral"],
    "concept": ["definition", "theorem", "concept"],
}


def handle_user_query(user_input: str, context: Optional[str]) -> str:
    response = _build_response(user_input, context)
    timestamp = datetime.utcnow().strftime("%H:%M:%S UTC")
    return f"{response}\n\n_Response generated at {timestamp}_"


def detect_intent(user_input: str) -> str:
    lowered = user_input.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return intent
    return "general"


def generate_quiz(topic: str, difficulty: str, num_questions: int) -> List[dict]:
    if num_questions <= 0:
        raise ValueError("Number of questions must be positive.")

    questions: List[dict] = []
    for idx in range(num_questions):
        question_id = f"{topic.lower().replace(' ', '-')}-{idx + 1}"
        question_text = f"({difficulty.title()}) {topic.title()} question {idx + 1}"
        answer = f"Sample answer {idx + 1} for {topic}"
        options = _build_options(answer) if idx % 2 == 0 else None
        questions.append(
            {
                "id": question_id,
                "question": question_text,
                "answer": answer,
                "options": options,
            }
        )
    return questions


def _build_response(user_input: str, context: Optional[str]) -> str:
    baseline = f"You asked: '{user_input}'."
    if context:
        snippet = context[:200] + ("..." if len(context) > 200 else "")
        return f"{baseline} Context was considered with excerpt: {snippet}"
    hints = [
        "Try breaking the problem into smaller steps.",
        "Remember to double-check units.",
        "Visualize the problem to gain intuition.",
    ]
    return f"{baseline} {random.choice(hints)}"


def _build_options(answer: str) -> List[str]:
    distractors = [
        f"{answer} + 1",
        f"{answer} - 1",
        answer.replace("Sample", "Approximate"),
    ]
    options = distractors + [answer]
    random.shuffle(options)
    return options
