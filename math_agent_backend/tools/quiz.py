from __future__ import annotations

import random
from typing import Dict, List

DifficultyWeights = {
    "easy": (2, 4),
    "medium": (3, 5),
    "hard": (4, 6),
}


def generate_quiz(topic: str, difficulty: str, num_questions: int) -> List[Dict[str, object]]:
    difficulty = difficulty if difficulty in DifficultyWeights else "medium"
    questions: List[Dict[str, object]] = []
    for idx in range(num_questions):
        q_id = f"{topic.lower().replace(' ', '-')}-{idx + 1}"
        base = f"{topic.title()} concept {idx + 1}"
        prompt = f"[{difficulty.title()}] What is {base}?"
        answer = f"Explanation for {base}"
        if idx % 2 == 0:
            options = _build_options(answer)
        else:
            options = None
        questions.append(
            {
                "id": q_id,
                "question": prompt,
                "answer": answer,
                "options": options,
            }
        )
    return questions


def validate_quiz_structure(quiz: List[Dict[str, object]]) -> bool:
    if not quiz:
        return False
    required = {"id", "question", "answer"}
    for item in quiz:
        if not required.issubset(item.keys()):
            return False
        if not isinstance(item["id"], str) or not isinstance(item["question"], str):
            return False
        if item.get("options") is not None:
            options = item["options"]
            if not isinstance(options, list) or not all(isinstance(opt, str) for opt in options):
                return False
    return True


def _build_options(answer: str) -> List[str]:
    distractors = [
        f"{answer} (approx)",
        f"Not {answer}",
        f"Alternate view of {answer}",
    ]
    options = distractors + [answer]
    random.shuffle(options)
    return options
