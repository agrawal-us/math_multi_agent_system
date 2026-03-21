import logging

import streamlit as st

from components import chat, file_upload, quiz
from state import session as session_state

_LOGGING_KEY = "_logging_initialized"


def _setup_logging() -> None:
    if not st.session_state.get(_LOGGING_KEY):
        logging.basicConfig(
            format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
            level=logging.INFO,
        )
        st.session_state[_LOGGING_KEY] = True


def _render_status_banner() -> None:
    status = session_state.get_status()
    if status and status != "idle":
        st.info(f"Status: {status.replace('_', ' ').title()}")
    else:
        st.caption("Status: Ready")


def _render_errors() -> None:
    error = session_state.consume_error()
    if error:
        logging.getLogger(__name__).error("Surface error to user: %s", error)
        st.error(error)


def main() -> None:
    st.set_page_config(page_title="Multi-Agent Math System", layout="wide")
    session_state.init_session()
    _setup_logging()

    st.title("Math Multi-Agent Workspace")
    st.write("Upload reference material, chat with the math assistant, and practice with quizzes.")

    _render_status_banner()
    _render_errors()

    with st.sidebar:
        st.header("Reference Material")
        file_upload.render()

    chat_tab, quiz_tab = st.tabs(["Chat", "Quiz Mode"])
    with chat_tab:
        chat.render()

    with quiz_tab:
        quiz.render()


if __name__ == "__main__":
    main()
