from __future__ import annotations

import random
from typing import Dict, List, Tuple

from .ollama import get_quiz_model

QUIZ_MODEL = get_quiz_model()

TOPIC_SYNONYMS = {
    "derivatives": "derivative",
    "derivative": "derivative",
    "integrals": "integral",
    "integral": "integral",
    "matrices": "matrix",
    "matrix": "matrix",
}

TOPIC_BANK: Dict[str, Dict[str, List[Tuple[str, str, List[str]]]]] = {
    "algebra": {
        "easy": [
            ("Solve 2x + 3 = 7.", "x = 2", ["x = 1", "x = 3", "x = -2"]),
            ("Simplify 3(x + 2).", "3x + 6", ["3x + 2", "3x + 4", "x + 6"]),
            ("What is the value of x in x/4 = 3?", "x = 12", ["x = 7", "x = 9", "x = 4"]),
        ],
        "medium": [
            ("Factor x^2 - 5x + 6.", "(x - 2)(x - 3)", ["(x + 2)(x + 3)", "(x - 1)(x - 6)", "x(x - 5)"]),
            ("Solve 2x - y = 3 and x + y = 5 for x.", "x = 8/3", ["x = 1", "x = 3", "x = 2"]),
            ("If 3x + 4 = 19, what is x?", "x = 5", ["x = 3", "x = 6", "x = 4"]),
        ],
        "hard": [
            ("Find the real solutions to x^2 - 4x + 3 = 0.", "x = 1 or x = 3", ["x = -1 or x = -3", "x = 0", "x = 5"]),
            ("Solve the system: 3x + 2y = 12, 4x - y = 5.", "x = 2, y = 3", ["x = 1, y = 2", "x = 0, y = 4", "x = 3, y = 0"]),
            ("If f(x) = x^2 - 2x, find f(3).", "3", ["2", "5", "6"]),
        ],
    },
    "derivative": {
        "easy": [
            ("What is d/dx (x^2)?", "2x", ["x", "x^2", "2"]),
            ("Derivative of sin(x)?", "cos(x)", ["-sin(x)", "sin(x)", "-cos(x)"]),
            ("d/dx (3x)?", "3", ["x", "3x", "0"]),
        ],
        "medium": [
            ("Find d/dx (x^3 + 2x).", "3x^2 + 2", ["3x + 2", "x^2 + 2", "x^3 + 2"]),
            ("Derivative of e^{2x}?", "2e^{2x}", ["e^{2x}", "2e^{x}", "e^{x}"]),
            ("What is d/dx (ln x)?", "1/x", ["x", "ln x", "x ln x"]),
        ],
        "hard": [
            ("Find the derivative of ln(x)/x.", "(1 - ln(x))/x^2", ["ln(x)/x", "1/x^2", "(1 + ln(x))/x^2"]),
            ("Compute d/dx (sin(x) * e^x).", "e^x(sin(x) + cos(x))", ["e^x sin(x)", "e^x cos(x)", "sin(x) + cos(x)"]),
            ("Find d/dx of (x^2 + 1)/(x - 1).", "(x^2 - 2x - 1)/(x - 1)^2", ["(2x)/(x - 1)^2", "(x^2 + 1)/(x - 1)^2", "(x^2 + 2x)/(x - 1)^2"]),
        ],
    },
    "integral": {
        "easy": [
            ("Evaluate ∫ 2x dx.", "x^2 + C", ["2x + C", "x^3 + C", "x^2"]),
            ("Compute ∫ 1 dx.", "x + C", ["1 + C", "x^2 + C", "C"]),
            ("Find ∫ cos(x) dx.", "sin(x) + C", ["-sin(x) + C", "cos(x) + C", "x cos(x) + C"]),
        ],
        "medium": [
            ("Evaluate ∫ (3x^2) dx.", "x^3 + C", ["3x + C", "x^2 + C", "x^4 + C"]),
            ("Compute ∫ e^x dx.", "e^x + C", ["xe^x + C", "e^x", "C"]),
            ("Find ∫ 1/x dx.", "ln|x| + C", ["1/x + C", "x + C", "x^2/2 + C"]),
        ],
        "hard": [
            ("Find ∫ x e^x dx.", "(x - 1)e^x + C", ["xe^x + C", "x^2 e^x + C", "e^x + C"]),
            ("Evaluate ∫ 1/(1 + x^2) dx.", "arctan(x) + C", ["ln(1 + x^2) + C", "1/(1 + x^2)", "x/(1 + x^2) + C"]),
            ("Compute ∫ x/(x^2 + 1) dx.", "(1/2)ln(x^2 + 1) + C", ["x^2/(x^2 + 1) + C", "arctan(x) + C", "(x^2 + 1)/2 + C"]),
        ],
    },
    "matrix": {
        "easy": [
            ("What is the determinant of [[1,0],[0,1]]?", "1", ["0", "-1", "2"]),
            ("Add matrices [[1,2],[3,4]] and [[1,1],[1,1]].", "[[2,3],[4,5]]", ["[[2,2],[4,4]]", "[[1,3],[3,5]]", "[[2,4],[6,8]]"]),
            ("Identify the identity matrix of size 2.", "[[1,0],[0,1]]", ["[[0,1],[1,0]]", "[[1,1],[0,1]]", "[[2,0],[0,2]]"]),
        ],
        "medium": [
            ("Compute the determinant of [[2,1],[3,4]].", "5", ["-5", "2", "7"]),
            ("Find the transpose of [[1,4],[2,5]].", "[[1,2],[4,5]]", ["[[4,1],[5,2]]", "[[1,4],[2,5]]", "[[5,4],[2,1]]"]),
            ("If A is 2x3 and B is 3x4, what is the size of AB?", "2x4", ["3x3", "4x2", "2x3"]),
        ],
        "hard": [
            ("Find eigenvalues of [[2,1],[1,2]].", "λ = 3, 1", ["λ = 2,2", "λ = 4,0", "λ = 1,1"]),
            ("Compute determinant of [[1,2,3],[0,1,4],[5,6,0]].", "1", ["-1", "0", "5"]),
            ("If det(A) = 4, what is det(2A) for a 2x2 matrix?", "16", ["8", "4", "32"]),
        ],
    },
}


def generate_quiz(topic: str, difficulty: str, num_questions: int) -> List[Dict[str, object]]:
    normalized_topic = _normalize_topic(topic)
    bank = TOPIC_BANK.get(normalized_topic)
    if not bank:
        bank = TOPIC_BANK.get("algebra")
        normalized_topic = "algebra"
    difficulty = difficulty if difficulty in bank else "medium"
    items = bank[difficulty]
    questions: List[Dict[str, object]] = []
    used_indices: set[int] = set()
    used_questions: set[str] = set()

    for idx in range(num_questions):
        entry, chosen_idx = _select_question(items, idx, used_indices, used_questions)
        if entry is None:
            entry = _generate_dynamic_question(normalized_topic, idx)
            chosen_idx = -1
        used_indices.add(chosen_idx)
        q_id = f"{normalized_topic}-{idx + 1}"
        question_text, correct_answer, distractors = entry
        if question_text in used_questions:
            entry = _generate_dynamic_question(normalized_topic, idx + len(used_questions))
            question_text, correct_answer, distractors = entry
        options = _build_options(correct_answer, distractors)
        used_questions.add(question_text)
        questions.append(
            {
                "id": q_id,
                "question": question_text,
                "answer": correct_answer,
                "options": options,
            }
        )
    return questions


def generate_quiz_with_diagnostics(topic: str, difficulty: str, num_questions: int) -> tuple[list[dict], dict]:
    requested_topic = topic
    normalized_topic = _normalize_topic(topic)
    bank = TOPIC_BANK.get(normalized_topic)
    fallback_topic_used = False
    if not bank:
        bank = TOPIC_BANK.get("algebra")
        normalized_topic = "algebra"
        fallback_topic_used = True

    effective_difficulty = difficulty if difficulty in bank else "medium"
    questions = generate_quiz(topic, difficulty, num_questions)

    diagnostics = {
        "requested_topic": requested_topic,
        "normalized_topic": normalized_topic,
        "fallback_topic_used": fallback_topic_used,
        "requested_difficulty": difficulty,
        "effective_difficulty": effective_difficulty,
        "num_questions_requested": num_questions,
        "num_questions_generated": len(questions),
    }
    return questions, diagnostics


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


def _normalize_topic(topic: str) -> str:
    lowered = (topic or "").strip().lower()
    return TOPIC_SYNONYMS.get(lowered, lowered or "algebra")


def _select_question(
    pool: List[Tuple[str, str, List[str]]],
    idx: int,
    used_indices: set[int],
    used_questions: set[str],
) -> Tuple[Tuple[str, str, List[str]] | None, int]:
    if idx < len(pool):
        candidate = pool[idx]
        if candidate[0] not in used_questions:
            return candidate, idx
    for i, candidate in enumerate(pool):
        if i in used_indices or candidate[0] in used_questions:
            continue
        return candidate, i
    if pool:
        chosen = random.randrange(len(pool))
        return pool[chosen], chosen
    return None, -1


def _build_options(answer: str, distractors: List[str]) -> List[str]:
    options = distractors[:3]
    while len(options) < 3:
        options.append(answer)
    options = options[:3] + [answer]
    random.shuffle(options)
    return options


def _generate_dynamic_question(topic: str, offset: int) -> Tuple[str, str, List[str]]:
    topic = topic.lower()
    base = offset + 2
    if topic == "derivative":
        n = 2 + (base % 3)
        coeff = 1 + (base % 4)
        question = f"What is d/dx ({coeff}x^{n})?"
        answer = f"{coeff * n}x^{n-1}"
        distractors = [
            f"{coeff}x^{n-1}",
            f"{coeff * n}x^{n}",
            f"{coeff * (n-1)}x^{n-2}",
        ]
        return question, answer, distractors
    if topic == "integral":
        n = 1 + (base % 3)
        coeff = 2 + (base % 5)
        question = f"Evaluate ∫ {coeff}x^{n} dx."
        answer = f"{coeff/(n+1):g}x^{n+1} + C"
        distractors = [
            f"{coeff}x^{n+1} + C",
            f"{coeff/(n):g}x^{n} + C",
            f"{coeff*(n+1)}x^{n+2} + C",
        ]
        return question, answer, distractors
    if topic == "matrix":
        a = 1 + (base % 4)
        b = 2 + (base % 5)
        c = 3 + (base % 6)
        d = 4 + (base % 7)
        det = a * d - b * c
        question = f"What is det([[{a},{b}],[{c},{d}]])?"
        distractors = [str(det + 2), str(det - 2), str(-det)]
        return question, str(det), distractors
    # default algebra
    m = 2 + (base % 5)
    b = 1 + (base % 7)
    rhs = m * (base) + b
    question = f"Solve {m}x + {b} = {rhs}."
    answer = f"x = {base}"
    distractors = [f"x = {base + 1}", f"x = {base - 1}", f"x = {base + 2}"]
    return question, answer, distractors