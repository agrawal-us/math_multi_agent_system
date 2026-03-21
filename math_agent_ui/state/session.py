from __future__ import annotations

import copy
import logging
from datetime import datetime
from typing import Any, Dict

import streamlit as st

from services.parser import ParsedDocument


logger = logging.getLogger(__name__)

DEFAULT_STATE: Dict[str, Any] = {
    "context": {
        "text": None,
        "filename": None,
        "pages": None,
        "metadata": {},
        "raw_bytes": None,
        "file_id": None,
    },
    "chat": {
        "history": [],
        "last_intent": None,
        "use_context": True,
    },
    "quiz": {
        "config": {"topic": "", "difficulty": "medium", "num_questions": 3},
        "questions": [],
        "responses": {},
        "score": None,
    },
    "ui": {"status": "idle", "error": None},
}


def init_session() -> None:
    for key, default in DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = copy.deepcopy(default)


def get_context_state() -> Dict[str, Any]:
    return st.session_state["context"]


def update_context(parsed: ParsedDocument, raw_bytes: bytes, filename: str, file_id: str) -> None:
    st.session_state["context"] = {
        **copy.deepcopy(DEFAULT_STATE["context"]),
        "text": parsed.text,
        "pages": parsed.pages,
        "metadata": copy.deepcopy(parsed.metadata),
        "filename": filename,
        "raw_bytes": raw_bytes,
        "file_id": file_id,
    }


def clear_context() -> None:
    st.session_state["context"] = copy.deepcopy(DEFAULT_STATE["context"])


def get_chat_state() -> Dict[str, Any]:
    return st.session_state["chat"]


def add_chat_message(role: str, message: str, context_used: bool) -> None:
    entry = {
        "role": role,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "context_used": context_used,
    }
    chat_state = get_chat_state()
    history = [*chat_state.get("history", []), entry]
    st.session_state["chat"] = {**chat_state, "history": history}


def update_chat_context_usage(use_context: bool) -> None:
    chat_state = get_chat_state()
    st.session_state["chat"] = {**chat_state, "use_context": use_context}


def set_last_intent(intent: str) -> None:
    chat_state = get_chat_state()
    st.session_state["chat"] = {**chat_state, "last_intent": intent}


def get_quiz_state() -> Dict[str, Any]:
    return st.session_state["quiz"]


def store_quiz_data(config: Dict[str, Any], questions: list) -> None:
    quiz_state = get_quiz_state()
    st.session_state["quiz"] = {
        **quiz_state,
        "config": config,
        "questions": questions,
        "responses": {},
        "score": None,
    }


def update_quiz_response(question_id: str, answer: str) -> None:
    quiz_state = get_quiz_state()
    responses = {**quiz_state.get("responses", {})}
    responses[question_id] = answer
    st.session_state["quiz"] = {**quiz_state, "responses": responses}


def set_quiz_score(correct: int, total: int) -> None:
    quiz_state = get_quiz_state()
    st.session_state["quiz"] = {**quiz_state, "score": {"correct": correct, "total": total}}


def set_status(status: str) -> None:
    ui_state = st.session_state["ui"].copy()
    ui_state["status"] = status
    st.session_state["ui"] = ui_state


def get_status() -> str:
    return st.session_state["ui"].get("status", "idle")


def set_error(message: str) -> None:
    logger.error("Session error recorded: %s", message)
    ui_state = st.session_state["ui"].copy()
    ui_state["error"] = message
    st.session_state["ui"] = ui_state


def consume_error() -> str | None:
    error = st.session_state["ui"].get("error")
    if error is None:
        return None
    ui_state = st.session_state["ui"].copy()
    ui_state["error"] = None
    st.session_state["ui"] = ui_state
    return error
