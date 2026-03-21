from __future__ import annotations

import logging

import streamlit as st

from services import agent_gateway
from state import session as session_state


logger = logging.getLogger(__name__)


def render() -> None:
    chat_state = session_state.get_chat_state()
    context_state = session_state.get_context_state()

    st.subheader("Assistant Chat")
    if chat_state.get("last_intent"):
        st.caption(f"Last detected intent: {chat_state['last_intent']}")

    for entry in chat_state["history"]:
        role = "assistant" if entry["role"] == "agent" else "user"
        with st.chat_message(role):
            st.markdown(entry["message"])
            if entry["context_used"]:
                st.caption("Context attached")

    with st.form("chat_form", clear_on_submit=True):
        default_use_context = chat_state.get("use_context", True) and bool(context_state.get("text"))
        use_context = st.checkbox(
            "Include uploaded context",
            value=default_use_context,
            disabled=not bool(context_state.get("text")),
        )
        prompt = st.text_area("Ask a math question", placeholder="How do I integrate sin(x)?")
        submitted = st.form_submit_button("Send")

    if submitted:
        message = prompt.strip()
        if not message:
            st.warning("Please enter a question before sending.")
            return

        session_state.update_chat_context_usage(use_context)
        session_state.set_status("chat_submitting")
        intent = agent_gateway.detect_intent(message)
        session_state.set_last_intent(intent)
        session_state.add_chat_message("user", message, context_used=use_context)
        context_text = context_state.get("text") if use_context else None
        logger.info(
            "Chat request submitted | intent=%s context_used=%s message_length=%s",
            intent,
            use_context,
            len(message),
        )
        try:
            with st.spinner("Generating response..."):
                response = agent_gateway.handle_user_query(message, context_text)
            session_state.add_chat_message("agent", response, context_used=use_context)
        except Exception as exc:  # pragma: no cover - defensive
            session_state.set_error(f"Chat failed: {exc}")
            logger.exception("Chat request failed")
        finally:
            session_state.set_status("idle")
        st.rerun()
