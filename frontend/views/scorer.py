from typing import Optional

import requests
import streamlit as st

from frontend.services import api_client
from frontend.components.dashboard import display_results_dashboard
from frontend.components.career_features import render_jd_feature_suite, render_multi_analysis_results


def _read_jd(jd_file, jd_text: str) -> str:
    """Turn whatever the user provided into a plain JD string for the backend."""
    if jd_text:
        return jd_text.strip()
    if jd_file is None:
        return ""
    if jd_file.name.lower().endswith(".txt"):
        return jd_file.getvalue().decode("utf-8", errors="ignore")
    st.warning(
        "Job description files must be `.txt` for now — paste the JD text instead "
        "if you have a PDF or DOCX."
    )
    return ""


def _read_multiple_jds(jd_files, jd_text: str) -> list[tuple[str, str]]:
    jobs = []
    if jd_files:
        for index, jd_file in enumerate(jd_files, start=1):
            content = jd_file.getvalue().decode("utf-8", errors="ignore").strip()
            if content:
                jobs.append((jd_file.name or f"Role {index}", content))
    if jd_text:
        for index, content in enumerate(jd_text.split("\n---\n"), start=1):
            content = content.strip()
            if content:
                jobs.append((f"Role {index}", content))
    return jobs[:5]


def _show_backend_error(exc: Exception) -> None:
    """Translate a `requests` exception into a friendly Streamlit error."""
    if isinstance(exc, requests.ConnectionError):
        st.error(
            f"🚨 Could not reach the backend at `{api_client._backend_url()}`. "
            "Start `uvicorn backend.main:app` and wait for the model-loading startup to finish."
        )
    elif isinstance(exc, requests.Timeout):
        st.error("⏳ The backend took too long to respond. Try a smaller resume or check the server logs.")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        try:
            detail = exc.response.json().get("detail", exc.response.text)
        except ValueError:
            detail = exc.response.text
        st.error(f"⚠️ Backend returned {exc.response.status_code}: {detail}")
    else:
        st.error(f"❌ Unexpected error: {exc}")


def _summary_text(analysis: dict) -> str:
    """Tiny client-side text summary for the Download button."""
    score = analysis.get("ATS_score", analysis.get("ats_score", 0))
    lines = [f"ATS Score: {score:.0f}/100", ""]
    if analysis.get("strengths"):
        lines.append("STRENGTHS:")
        lines.extend(f"  - {s}" for s in analysis["strengths"])
        lines.append("")
    if analysis.get("critical_issues"):
        lines.append("CRITICAL ISSUES:")
        lines.extend(f"  - {s}" for s in analysis["critical_issues"])
        lines.append("")
    if analysis.get("suggestions"):
        lines.append("SUGGESTIONS:")
        lines.extend(f"  - {s}" for s in analysis["suggestions"])
    return "\n".join(lines)


def _render_upload_area(analysis_mode: str):
    """Two-column styled upload widgets. Returns (resume_file, jd_file, jd_text)."""
    st.markdown("### 📄 Document Upload")
    
    left, right = st.columns(2, gap="large")

    with left:
        with st.container(border=True):
            st.markdown("#### 1️⃣ Upload Resume")
            st.caption("Supported formats: PDF, DOC, DOCX (Max 5MB)")
            resume_file = st.file_uploader(
                "Drop your resume here",
                type=["pdf", "doc", "docx"],
                label_visibility="collapsed",
                key="resume_upload",
            )
            if resume_file:
                st.success(f"✅ Loaded: {resume_file.name} ({resume_file.size / 1024:.1f} KB)")

    jd_file: Optional[object] = None
    jd_text = ""

    with right:
        with st.container(border=True):
            if analysis_mode == "Multiple Job Comparison":
                st.markdown("#### 2️⃣ Multiple Job Descriptions")
                st.caption("Add 3–5 JDs as .txt files or paste them separated by ---.")
                multi_method = st.radio(
                    "Multiple JD input method",
                    ["Paste JDs", "Upload .txt Files"],
                    horizontal=True,
                    key="multi_jd_input_method",
                    label_visibility="collapsed",
                )
                if multi_method == "Upload .txt Files":
                    jd_file = st.file_uploader(
                        "Upload 3–5 job descriptions",
                        type=["txt"],
                        accept_multiple_files=True,
                        key="multi_jd_upload",
                        label_visibility="collapsed",
                    )
                else:
                    jd_text = st.text_area(
                        "Paste multiple job descriptions",
                        height=180,
                        placeholder="Job description 1\n---\nJob description 2\n---\nJob description 3",
                        key="multi_jd_text",
                        label_visibility="collapsed",
                    )
            elif analysis_mode == "Job Description Comparison":
                st.markdown("#### 2️⃣ Target Job Description")
                st.caption("Provide the JD to calculate your match rate.")
                
                jd_method = st.radio(
                    "Input method:",
                    ["Paste Text", "Upload .txt File"],
                    horizontal=True,
                    key="jd_input_method",
                    label_visibility="collapsed"
                )
                
                if jd_method == "Upload .txt File":
                    jd_file = st.file_uploader(
                        "Drop JD file here (.txt only)",
                        type=["txt"],
                        key="jd_upload",
                        label_visibility="collapsed"
                    )
                    if jd_file:
                        st.success(f"✅ Loaded: {jd_file.name}")
                else:
                    jd_text = st.text_area(
                        "Paste JD text",
                        height=130,
                        placeholder="Paste the job description here...",
                        key="jd_text",
                        label_visibility="collapsed"
                    )
                    if jd_text:
                        st.success(f"✅ Text added ({len(jd_text)} characters)")
            else:
                st.markdown("#### 2️⃣ Target Job Description")
                st.info("💡 Switch to a targeted comparison mode above to unlock JD matching.")

    return resume_file, jd_file, jd_text


def _render_export_buttons(analysis: dict) -> None:
    st.markdown("---")
    st.markdown("### 📥 Export Your Action Plan")
    
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 📑 Detailed PDF Report")
            st.caption("Generates a beautiful, shareable PDF of your full analysis.")
            if st.button("Generate PDF Report", use_container_width=True, type="primary"):
                try:
                    with st.spinner("🎨 Crafting your PDF..."):
                        pdf_bytes = api_client.generate_pdf(
                            analysis,
                            access_token=st.session_state["access_token"],
                        )
                    st.session_state["scorer_pdf_bytes"] = pdf_bytes
                except requests.RequestException as exc:
                    _show_backend_error(exc)

            if "scorer_pdf_bytes" in st.session_state:
                st.download_button(
                    "⬇️ Download PDF",
                    data=st.session_state["scorer_pdf_bytes"],
                    file_name="ats_resume_report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="download_pdf_report",
                )

        with c2:
            st.markdown("#### 📄 Quick Text Summary")
            st.caption("A lightweight text file with your score and critical action items.")
            st.write("") # Spacer to align buttons
            st.download_button(
                "⬇️ Download Summary (.txt)",
                data=_summary_text(analysis),
                file_name="ats_summary.txt",
                mime="text/plain",
                use_container_width=True,
                key="download_summary",
            )


def render() -> None:
    # Custom CSS for the Scorer View
    st.markdown("""
    <style>
        .scorer-header {
            text-align: center;
            padding: 2.5rem 1rem;
            margin-top : 3rem !important;
            background: linear-gradient(135deg, #1e1b4b 0%, #4F46E5 100%);
            color: white;
            border-radius: 16px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(79, 70, 229, 0.2);
        }
        .scorer-header h1 {
            color: white !important;
            font-size: 2.5rem !important;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        .scorer-header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        /* Add hover effects to Streamlit Native Containers */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            background: rgba(255, 255, 255, 0.02);
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(236, 72, 153, 0.1);
            border-color: #EC4899;
        }
    </style>
    
    <div class="scorer-header">
        <h1>🎯 AI Resume Scorer</h1>
        <p>Upload your resume and get instant, actionable feedback to bypass the bots.</p>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # ⚙️ ANALYSIS SETTINGS CARD
    # ==========================================
    with st.container(border=True):
        st.markdown("### ⚙️ Analysis Mode")
        st.caption("Choose how you want our AI to evaluate your resume.")
        analysis_mode = st.radio(
            "Select Analysis Mode:",
            ["General ATS Score", "Job Description Comparison", "Multiple Job Comparison"],
            horizontal=True,
            key="analysis_mode",
            label_visibility="collapsed"
        )
        
        if analysis_mode == "General ATS Score":
            st.info("🔍 **General Mode:** Evaluates overall formatting, standard keywords, and readability.")
        elif analysis_mode == "Job Description Comparison":
            st.success("🎯 **Targeted Mode:** Compares your resume against a specific job description to find missing skills.")
        else:
            st.success("📊 **Multi-Job Mode:** Runs the same resume against 3–5 job descriptions and ranks the best fit.")

    st.write("")
    
    # ==========================================
    # 📄 UPLOAD AREA
    # ==========================================
    resume_file, jd_file, jd_text = _render_upload_area(analysis_mode)

    st.write("")
    st.write("")

    # ==========================================
    # 🚀 ANALYSIS TRIGGER
    # ==========================================
    if not resume_file:
        st.warning("👆 Please upload your resume to unlock the analysis button.")
        # If we have a prior result in session, render it again.
        if st.session_state.get("scorer_analysis"):
            st.markdown("---")
            st.markdown("### 🕒 Previous Analysis Results")
            display_results_dashboard(st.session_state["scorer_analysis"])
            if st.session_state["scorer_analysis"].get("jd_comparison") or st.session_state["scorer_analysis"].get("jd_match_analysis"):
                render_jd_feature_suite(st.session_state["scorer_analysis"], st.session_state.get("scorer_jd_text", ""))
            _render_export_buttons(st.session_state["scorer_analysis"])
        if st.session_state.get("scorer_multi_results"):
            st.markdown("---")
            render_multi_analysis_results(st.session_state["scorer_multi_results"])
        return

    access_token = st.session_state.get("access_token")
    if not access_token:
        st.error("🔒 **Authentication Required:** Please log in or create an account using the navigation bar above to analyze your resume.")
        return

    if analysis_mode == "Multiple Job Comparison":
        multiple_jobs = _read_multiple_jds(jd_file, jd_text)
        if len(multiple_jobs) < 3:
            st.warning("Add at least 3 job descriptions to run a multiple-job comparison.")
            return
    else:
        multiple_jobs = []

    _, mid, _ = st.columns([1, 1.5, 1])
    with mid:
        analyze = st.button("🚀 Run AI Analysis", use_container_width=True, type="primary")

    if not analyze:
        # Re-show previous result on rerun (e.g. after PDF generation).
        if st.session_state.get("scorer_analysis"):
            st.markdown("---")
            display_results_dashboard(st.session_state["scorer_analysis"])
            if st.session_state["scorer_analysis"].get("jd_comparison") or st.session_state["scorer_analysis"].get("jd_match_analysis"):
                render_jd_feature_suite(st.session_state["scorer_analysis"], st.session_state.get("scorer_jd_text", ""))
            _render_export_buttons(st.session_state["scorer_analysis"])
        if st.session_state.get("scorer_multi_results"):
            st.markdown("---")
            render_multi_analysis_results(st.session_state["scorer_multi_results"])
        return

    # ==========================================
    # 🧠 BACKEND PROCESSING
    # ==========================================
    # Fresh analysis — drop any cached PDF/result.
    st.session_state.pop("scorer_pdf_bytes", None)
    st.session_state.pop("scorer_analysis", None)
    st.session_state.pop("scorer_multi_results", None)

    if analysis_mode == "Multiple Job Comparison":
        try:
            multi_results = []
            with st.status("🧠 Comparing your resume with each job...", expanded=True) as status:
                for index, (label, job_description) in enumerate(multiple_jobs, start=1):
                    st.write(f"🔍 Analyzing job {index} of {len(multiple_jobs)}: {label}")
                    result = api_client.analyze_resume(
                        resume_file=resume_file,
                        access_token=access_token,
                        job_description=job_description,
                    )
                    multi_results.append({"label": label, "analysis": result})
                status.update(label="✅ Multiple job comparison complete!", state="complete", expanded=False)
        except requests.RequestException as exc:
            _show_backend_error(exc)
            return

        st.session_state["scorer_multi_results"] = multi_results
        st.balloons()
        st.markdown("---")
        render_multi_analysis_results(multi_results)
        return

    job_description = _read_jd(jd_file, jd_text) if analysis_mode == "Job Description Comparison" else ""

    try:
        with st.status("🧠 Initializing AI Engine...", expanded=True) as status:
            st.write("📄 Parsing document layout...")
            st.write("🔍 Extracting key skills and entities...")
            st.write("⚖️ Calculating ATS compatibility scores...")
            
            analysis = api_client.analyze_resume(
                resume_file=resume_file,
                access_token=access_token,
                job_description=job_description,
            )
            status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
            
    except requests.RequestException as exc:
        _show_backend_error(exc)
        return

    # Save to state and display
    st.session_state["scorer_analysis"] = analysis
    st.session_state["scorer_jd_text"] = job_description
    st.balloons() # Fun interactive celebration

    st.markdown("---")
    display_results_dashboard(analysis)
    if analysis_mode == "Job Description Comparison":
        render_jd_feature_suite(analysis, job_description)
    _render_export_buttons(analysis)