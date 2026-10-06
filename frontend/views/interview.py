import html
import json

import requests
import streamlit as st
import streamlit.components.v1 as components

from frontend.services import api_client


def _show_error(exc: Exception) -> None:
    if isinstance(exc, requests.ConnectionError):
        st.error(
            f"Could not reach the backend at `{api_client._backend_url()}`. "
            "Start the API with `uvicorn backend.main:app` and wait for startup."
        )
    elif isinstance(exc, requests.Timeout):
        st.error("The AI service took too long to respond. Please try again.")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        try:
            detail = exc.response.json().get("detail", exc.response.text)
        except ValueError:
            detail = exc.response.text
        st.error(f"Request failed ({exc.response.status_code}): {detail}")
    else:
        st.error(f"Something went wrong: {exc}")


def _render_speak_button(question: str, key: str) -> None:
    safe_question = json.dumps(question).replace("<", "\\u003c")
    components.html(
        f"""
        <button id="speak-{html.escape(key)}" style="
            border: 1px solid #c4b5fd; border-radius: 10px; padding: 9px 14px;
            background: #f5f3ff; color: #5b21b6; font-weight: 600; cursor: pointer;">
            🔊 Hear this question
        </button>
        <script>
          document.getElementById("speak-{html.escape(key)}").addEventListener("click", () => {{
            window.speechSynthesis.cancel();
            const prompt = new SpeechSynthesisUtterance({safe_question});
            prompt.rate = 0.95;
            window.speechSynthesis.speak(prompt);
          }});
        </script>
        """,
        height=50,
    )


def _render_setup(access_token: str) -> None:
    st.markdown("### Set up your mock interview")
    st.caption(
        "Add your resume and the role you want. The coach will identify preparation gaps "
        "and create a focused interview."
    )
    with st.form("interview_setup"):
        resume_file = st.file_uploader(
            "Resume (PDF or DOCX, up to 5 MB)",
            type=["pdf", "doc", "docx"],
            key="interview_resume",
        )
        job_description = st.text_area(
            "Target job description",
            placeholder="Paste the role, requirements, and responsibilities here...",
            height=220,
            max_chars=20000,
            key="interview_job_description",
        )
        question_count = st.select_slider(
            "Questions in this practice session",
            options=[3, 4, 5, 6, 7, 8],
            value=5,
        )
        start = st.form_submit_button(
            "✨ Build my tailored interview",
            type="primary",
            use_container_width=True,
        )

    if not start:
        return
    if resume_file is None:
        st.error("Upload your resume to tailor the interview.")
        return
    if len(job_description.strip()) < 30:
        st.error("Add a job description with at least 30 characters.")
        return

    try:
        with st.spinner("Reading your resume and preparing role-specific questions..."):
            plan = api_client.create_interview_session(
                resume_file,
                job_description.strip(),
                access_token,
                question_count,
            )
        st.session_state.interview_plan = plan
        st.session_state.interview_session_job_description = job_description.strip()
        st.session_state.interview_answers = []
        st.session_state.interview_question_index = 0
        st.rerun()
    except Exception as exc:
        _show_error(exc)


def _render_feedback(result: dict, question_number: int) -> None:
    with st.expander(
        f"Question {question_number} feedback · {result['score']}/10",
        expanded=question_number == len(st.session_state.interview_answers),
    ):
        st.write(result.get("feedback", ""))
        strengths = result.get("strengths", [])
        improvements = result.get("improvements", [])
        if strengths:
            st.markdown("**What worked well**")
            for strength in strengths:
                st.markdown(f"- {strength}")
        if improvements:
            st.markdown("**Try this next time**")
            for improvement in improvements:
                st.markdown(f"- {improvement}")
        if result.get("example_direction"):
            st.info(result["example_direction"])


def _render_results(plan: dict, answers: list[dict]) -> None:
    st.success("Practice session complete — nice work showing up and practicing!")
    average = sum(item["score"] for item in answers) / len(answers)
    metric, detail = st.columns([1, 3])
    metric.metric("Practice score", f"{average:.1f} / 10")
    detail.write(
        "Use the notes below to choose one or two improvements for your next practice round."
    )
    for index, result in enumerate(answers, start=1):
        question = plan["questions"][index - 1]["question"]
        with st.expander(f"Q{index}: {question}", expanded=False):
            st.metric("Score", f"{result['score']} / 10")
            st.write(result.get("feedback", ""))
            if result.get("improvements"):
                st.markdown("**Focus for next time**")
                for item in result["improvements"]:
                    st.markdown(f"- {item}")

    if st.button("Start another interview", type="primary"):
        for key in (
            "interview_plan",
            "interview_job_description",
            "interview_session_job_description",
            "interview_answers",
            "interview_question_index",
        ):
            st.session_state.pop(key, None)
        for index in range(8):
            for prefix in (
                "interview_answer_",
                "interview_audio_",
                "interview_transcribe_",
                "interview_submit_",
            ):
                st.session_state.pop(f"{prefix}{index}", None)
        st.rerun()


def _render_active_interview(access_token: str) -> None:
    plan = st.session_state.interview_plan
    answers = st.session_state.interview_answers
    question_index = st.session_state.interview_question_index
    questions = plan["questions"]

    st.markdown(f"### {plan['role_title']}")
    if plan.get("overview"):
        st.write(plan["overview"])
    gaps = plan.get("skill_gaps", [])
    if gaps:
        with st.expander("📌 Preparation areas from your resume", expanded=False):
            for gap in gaps:
                st.markdown(f"**{gap['skill']}** — {gap['note']}")

    progress = min(question_index, len(questions)) / len(questions)
    st.progress(progress, text=f"Question {min(question_index + 1, len(questions))} of {len(questions)}")

    if question_index >= len(questions):
        _render_results(plan, answers)
        return

    current = questions[question_index]
    st.markdown(f"#### {current['type']} question")
    with st.container(border=True):
        st.markdown(f"### {current['question']}")
        _render_speak_button(current["question"], f"q{question_index}")

    answer_key = f"interview_answer_{question_index}"
    audio_input = getattr(st, "audio_input", None)
    if audio_input is not None:
        recording = audio_input(
            "Record your answer",
            key=f"interview_audio_{question_index}",
        )
        if recording is not None and st.button(
            "Convert recording to text",
            key=f"interview_transcribe_{question_index}",
        ):
            try:
                with st.spinner("Transcribing your answer..."):
                    st.session_state[answer_key] = api_client.transcribe_interview_answer(
                        recording,
                        access_token,
                    )
            except Exception as exc:
                _show_error(exc)

    answer = st.text_area(
        "Your answer",
        placeholder="Record your answer above or type it here...",
        height=180,
        key=answer_key,
    )
    if st.button(
        "Submit answer and get feedback",
        type="primary",
        key=f"interview_submit_{question_index}",
        use_container_width=True,
    ):
        if not answer.strip():
            st.error("Record or type an answer before continuing.")
            return
        try:
            with st.spinner("Reviewing your answer..."):
                feedback = api_client.evaluate_interview_answer(
                    plan["role_title"],
                    st.session_state.interview_session_job_description,
                    current["question"],
                    answer.strip(),
                    access_token,
                )
            st.session_state.interview_answers.append(feedback)
            st.session_state.interview_question_index += 1
            st.rerun()
        except Exception as exc:
            _show_error(exc)

    for index, result in enumerate(answers, start=1):
        _render_feedback(result, index)


def render() -> None:
    st.markdown(
        """
        <div style="padding: 1.5rem 1.8rem; border-radius: 18px; color: white;
                    background: linear-gradient(120deg, #312e81, #7c3aed 60%, #db2777);">
          <h1 style="color: white; margin-bottom: .35rem;">🎙️ Interview Co-Pilot</h1>
          <p style="margin: 0; color: #f5f3ff;">
            Practice out loud. Get questions shaped around your resume and the role you want.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    st.caption(
        "Your resume and job description are sent to the configured Groq AI service to create "
        "questions; recordings are sent for transcription and answers for feedback. Interview "
        "sessions are not saved to your account history. Scores are for practice, not hiring."
    )

    access_token = st.session_state.get("access_token")
    if not access_token:
        st.info("Sign in to create a personalized interview practice session.")
        if st.button("Go to sign in", type="primary"):
            st.session_state.current_view = "auth"
            st.rerun()
        return

    if st.session_state.get("interview_plan"):
        _render_active_interview(access_token)
    else:
        _render_setup(access_token)
