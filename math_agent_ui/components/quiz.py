from __future__ import annotations

import logging

import streamlit as st

from services import agent_gateway
from state import session as session_state


DIFFICULTIES = ["easy", "medium", "hard"]
PLACEHOLDER_OPTION = "-- Select an option --"

logger = logging.getLogger(__name__)


def render() -> None:
    quiz_state = session_state.get_quiz_state()

    st.subheader("Quiz Builder")
    config = quiz_state.get("config", {})

    with st.form("quiz_config"):
        topic = st.text_input("Topic", value=config.get("topic", ""))
        difficulty_value = config.get("difficulty", "medium")
        default_index = DIFFICULTIES.index(difficulty_value) if difficulty_value in DIFFICULTIES else 1
        difficulty = st.selectbox(
            "Difficulty",
            DIFFICULTIES,
            index=default_index,
        )
        num_questions = int(
            st.number_input(
                "Number of questions",
                min_value=1,
                max_value=10,
                value=int(config.get("num_questions", 3)),
            )
        )
        generate = st.form_submit_button("Generate quiz")

    rerun_required = False
    if generate:
        session_state.set_status("quiz_generating")
        logger.info(
            "Generating quiz | topic=%s difficulty=%s num_questions=%s",
            topic,
            difficulty,
            int(num_questions),
        )
        try:
            with st.spinner("Generating quiz..."):
                quiz_result = agent_gateway.generate_quiz(topic, difficulty, num_questions)
            questions = quiz_result["questions"]
            session_state.store_quiz_data(
                {"topic": topic, "difficulty": difficulty, "num_questions": num_questions},
                questions,
                trace=quiz_result.get("trace"),
            )
            _reset_quiz_widgets()
            quiz_state = session_state.get_quiz_state()
            logger.debug(
                "Quiz debug | requested=%s generated=%s stored=%s",
                num_questions,
                len(questions),
                len(quiz_state.get("questions", [])),
            )
            rerun_required = True
        except Exception as exc:  # pragma: no cover
            session_state.set_error(f"Quiz generation failed: {exc}")
            logger.exception("Quiz generation failed")
        finally:
            session_state.set_status("idle")

    if rerun_required:
        st.rerun()

    if quiz_state.get("last_trace"):
        with st.expander("Quiz generation trace", expanded=False):
            st.json(quiz_state["last_trace"])

    if not quiz_state.get("questions"):
        st.info("Create a quiz to see questions here.")
        return

    _render_questions(quiz_state)
    if st.button("Submit answers", use_container_width=True):
        session_state.set_status("quiz_scoring")
        responses = quiz_state.get("responses", {})
        with st.spinner("Scoring quiz..."):
            correct = 0
            for question in quiz_state["questions"]:
                expected = (question.get("answer") or "").strip().lower()
                actual = (responses.get(question["id"], "") or "").strip().lower()
                if actual and actual == expected:
                    correct += 1
            session_state.set_quiz_score(correct, len(quiz_state["questions"]))
        logger.info(
            "Quiz scored | correct=%s total=%s",
            correct,
            len(quiz_state["questions"]),
        )
        session_state.set_status("idle")

    if quiz_state.get("score"):
        score = quiz_state["score"]
        st.success(f"Score: {score['correct']} / {score['total']}")


def _render_questions(quiz_state: dict) -> None:
    st.write("### Questions")
    for idx, question in enumerate(quiz_state["questions"], start=1):
        st.markdown(f"**Q{idx}. {question['question']}**")
        _render_response_input(quiz_state, question)
        st.divider()


def _render_response_input(quiz_state: dict, question: dict) -> None:
    question_id = question["id"]
    responses = quiz_state.get("responses", {})
    existing = responses.get(question_id, "")

    if question.get("options"):
        options = [PLACEHOLDER_OPTION, *question["options"]]
        default_value = existing if existing in question["options"] else PLACEHOLDER_OPTION
        widget_key = f"quiz_option_{question_id}"
        _ensure_widget_state(widget_key, default_value)
        current_value = st.session_state.get(widget_key, PLACEHOLDER_OPTION)
        if current_value in options:
            index = options.index(current_value)
        else:
            index = 0
            st.session_state[widget_key] = PLACEHOLDER_OPTION
        st.radio(
            "Choose an answer",
            options,
            index=index,
            key=widget_key,
            on_change=_handle_option_change,
            args=(question_id,),
        )
    else:
        widget_key = f"quiz_text_{question_id}"
        _ensure_widget_state(widget_key, existing)
        st.text_input(
            "Your answer",
            key=widget_key,
            on_change=_handle_text_change,
            args=(question_id,),
        )


def _handle_text_change(question_id: str) -> None:
    widget_key = f"quiz_text_{question_id}"
    answer = st.session_state.get(widget_key, "")
    session_state.update_quiz_response(question_id, answer.strip())


def _handle_option_change(question_id: str) -> None:
    widget_key = f"quiz_option_{question_id}"
    selection = st.session_state.get(widget_key, PLACEHOLDER_OPTION)
    answer = "" if selection == PLACEHOLDER_OPTION else selection
    session_state.update_quiz_response(question_id, answer)


def _ensure_widget_state(key: str, default: str) -> None:
    if key not in st.session_state:
        st.session_state[key] = default


def _reset_quiz_widgets() -> None:
    for key in list(st.session_state.keys()):
        if key.startswith("quiz_text_") or key.startswith("quiz_option_"):
            del st.session_state[key]