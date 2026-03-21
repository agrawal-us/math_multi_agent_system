from __future__ import annotations

import logging
from typing import Dict

from .ollama import generate as ollama_generate, get_concept_model

CONCEPT_KB: Dict[str, Dict[str, str]] = {
    "derivative": {
        "explanation": "A derivative measures how a function changes as its input changes.",
        "example": "Example: d/dx (x^2) = 2x.",
    },
    "integral": {
        "explanation": "An integral accumulates quantities, representing area under a curve.",
        "example": "Example: ∫_0^1 x dx = 1/2.",
    },
    "matrix": {
        "explanation": "A matrix is a rectangular array of numbers representing linear transformations.",
        "example": "Example: [[1,0],[0,1]] is the identity matrix.",
    },
}

PROMPT_TEMPLATE = (
    "You are a math tutor. Explain the mathematical concept '{topic}' clearly and briefly. "
    "Avoid finance or non-math meanings unless explicitly asked. "
    "Provide exactly one concrete math example. Respond in two lines:\n"
    "Explanation: <text>\nExample: <text>."
)

logger = logging.getLogger(__name__)


def fetch_concept(topic: str) -> Dict[str, str]:
    key = topic.lower().strip()
    try:
        response = _query_ollama(topic)
        if response:
            return response
    except Exception as exc:  # pragma: no cover - best effort
        logger.warning("Ollama concept generation failed: %s", exc)

    if key in CONCEPT_KB:
        return CONCEPT_KB[key]
    return {
        "explanation": f"{topic.title()} is a mathematical concept needing further elaboration.",
        "example": f"Example: Provide a concrete instance of {topic} in practice.",
    }


def _query_ollama(topic: str) -> Dict[str, str] | None:
    prompt = PROMPT_TEMPLATE.format(topic=topic)
    text = ollama_generate(prompt, model=get_concept_model())
    if not text:
        return None
    explanation, example = _parse_response(text)
    if not explanation and not example:
        return None
    return {
        "explanation": explanation or f"{topic.title()} is a mathematical concept requiring explanation.",
        "example": example or f"Example: Consider a basic scenario featuring {topic}.",
    }


def _parse_response(text: str) -> tuple[str | None, str | None]:
    lowered = text.lower()
    example_idx = lowered.find("example:")
    explanation = text
    example = None
    if example_idx != -1:
        explanation = text[:example_idx]
        example = text[example_idx:]
    explanation = explanation.replace("Explanation:", "").strip()
    if example is not None:
        example = example.replace("Example:", "").strip()
    return (explanation or None, example or None)
