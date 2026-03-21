from __future__ import annotations

from typing import List, Optional

from math_agent_backend.graph.workflow import run_workflow

INTENT_KEYWORDS = {
    "clarification": ["clarify", "explain", "why", "how"],
    "calculation": ["solve", "calculate", "compute", "derivative", "integral"],
    "concept": ["definition", "theorem", "concept"],
}


def handle_user_query(user_input: str, context: Optional[str]) -> str:
    backend_response = run_workflow(user_input)
    response_type = backend_response.get("type", "error")
    data = backend_response.get("data", {})

    if response_type == "solve":
        result_text = data.get("result", "No result returned.")
        steps = data.get("steps", []) or []
        steps_block = ""
        if steps:
            steps_block = "\n\nSteps:\n" + "\n".join(f"- {step}" for step in steps)
        return f"{result_text}{steps_block}"

    if response_type == "concept":
        return data.get("explanation", "No explanation available.")

    if response_type == "quiz":
        return "Switch to the quiz tab to review the generated questions."

    message = data.get("message") or backend_response.get("metadata", {}).get("error")
    return message or "The assistant could not process your request."


def detect_intent(user_input: str) -> str:
    lowered = user_input.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return intent
    return "general"


def generate_quiz(topic: str, difficulty: str, num_questions: int) -> List[dict]:
    if num_questions <= 0:
        raise ValueError("Number of questions must be positive.")
    prompt = f"Generate {num_questions} {difficulty} questions on {topic}"
    backend_response = run_workflow(prompt)
    if backend_response.get("type") != "quiz":
        message = backend_response.get("data", {}).get("message", "Failed to generate quiz.")
        raise ValueError(message)

    quiz_payload = backend_response.get("data", {}).get("quiz")
    if not isinstance(quiz_payload, list):
        raise ValueError("Quiz payload missing or invalid.")
    return quiz_payload
