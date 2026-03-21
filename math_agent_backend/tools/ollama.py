from __future__ import annotations

import logging
import os
from typing import Optional

import requests

logger = logging.getLogger(__name__)

_DEFAULT_HOST = "http://localhost:11434"
_DEFAULT_MODEL = "qwen2.5:7b"


def get_host() -> str:
    return os.getenv("OLLAMA_HOST", _DEFAULT_HOST).rstrip("/")


def get_concept_model() -> str:
    return os.getenv("OLLAMA_CONCEPT_MODEL", _DEFAULT_MODEL)


def get_quiz_model() -> str:
    return os.getenv("OLLAMA_QUIZ_MODEL", _DEFAULT_MODEL)


def generate(prompt: str, model: Optional[str] = None, timeout: int = 60) -> str:
    host = get_host()
    model_name = model or _DEFAULT_MODEL
    url = f"{host}/api/generate"
    payload = {"model": model_name, "prompt": prompt, "stream": False}
    try:
        response = requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:  # pragma: no cover - network errors
        logger.warning("Ollama request failed: %s", exc)
        raise

    data = response.json()
    text = (data.get("response") or "").strip()
    return text
