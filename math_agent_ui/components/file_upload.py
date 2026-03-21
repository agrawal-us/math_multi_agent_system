from __future__ import annotations

import hashlib
import logging

import streamlit as st

from services import parser
from state import session as session_state


logger = logging.getLogger(__name__)


def render() -> None:
    uploaded_file = st.file_uploader("Upload TXT or PDF", type=["txt", "pdf"])

    if uploaded_file is not None:
        if st.button("Process file", use_container_width=True):
            raw_bytes = uploaded_file.getvalue()
            file_id = _build_file_id(uploaded_file.name, raw_bytes)
            context_state = session_state.get_context_state()
            already_processed = context_state.get("file_id") == file_id
            if already_processed:
                st.info("This file is already processed.")
            else:
                session_state.set_status("processing_file")
                logger.info("Processing upload '%s'", uploaded_file.name)
                try:
                    with st.spinner("Parsing file..."):
                        parsed = parser.parse_file(uploaded_file.name, raw_bytes, uploaded_file.type)
                    session_state.update_context(parsed, raw_bytes, uploaded_file.name, file_id)
                    st.success(f"Loaded {uploaded_file.name}")
                    logger.info("Successfully parsed '%s'", uploaded_file.name)
                except parser.ParserError as exc:
                    session_state.set_error(str(exc))
                    st.warning("Unable to process the uploaded file.")
                    logger.error("Parser error for '%s': %s", uploaded_file.name, exc)
                except Exception as exc:  # pragma: no cover - defensive
                    session_state.set_error("Unexpected error while processing the file.")
                    st.warning("Unable to process the uploaded file.")
                    logger.exception("Unexpected failure while parsing '%s'", uploaded_file.name)
                finally:
                    session_state.set_status("idle")

    context_state = session_state.get_context_state()
    if context_state.get("text"):
        st.write("### Current Context")
        st.caption(
            f"File: {context_state.get('filename')} | Pages: {context_state.get('pages') or 'N/A'}"
        )
        st.caption(f"Characters: {len(context_state.get('text') or '')}")
        if context_state.get("metadata"):
            with st.expander("Metadata", expanded=False):
                st.json(context_state["metadata"])
        if st.button("Clear context", use_container_width=True):
            session_state.clear_context()
            st.info("Context cleared")
    else:
        st.caption("No context loaded yet.")


def _build_file_id(filename: str, raw_bytes: bytes) -> str:
    digest = hashlib.sha1(raw_bytes).hexdigest()
    return f"{filename}:{digest}"
