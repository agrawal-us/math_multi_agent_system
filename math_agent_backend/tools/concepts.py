from __future__ import annotations

from typing import Dict

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


def fetch_concept(topic: str) -> Dict[str, str]:
    key = topic.lower().strip()
    if key in CONCEPT_KB:
        return CONCEPT_KB[key]
    return {
        "explanation": f"{topic.title()} is a mathematical concept needing further elaboration.",
        "example": f"Example: Provide a concrete instance of {topic} in practice.",
    }
