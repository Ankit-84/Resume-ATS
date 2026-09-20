import re
from datetime import datetime

import pandas as pd
import streamlit as st


def _safe_list(value):
    return value if isinstance(value, list) else []


def _normalize_terms(text: str):
    if not text:
        return set()
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9+.#/-]{2,}", str(text).lower())
    return {token.strip(" .,-/()[]{}:'\"!") for token in tokens if len(token) > 2}


def extract_resume_terms(analysis: dict):
    terms = set()
    for key in ["skills", "resume_keywords", "keywords"]:
        for item in _safe_list(analysis.get(key, [])):
            terms |= _normalize_terms(item)
    for key in ["strengths", "critical_issues", "suggestions", "professional_summary", "summary"]:
        value = analysis.get(key)
        values = value if isinstance(value, list) else [value]
        for item in values:
            terms |= _normalize_terms(item)
    return terms


def missing_keywords(analysis: dict, jd_text: str, limit: int = 12):
    return sorted(_normalize_terms(jd_text) - extract_resume_terms(analysis))[:limit]


def _score_from_entry(entry: dict) -> float:
    result = entry.get("analysis_result") or {}
    return float(entry.get("ats_score", result.get("ats_score", result.get("ATS_score", 0))) or 0)


def render_resume_timeline(history: list[dict]) -> None:
    st.markdown("### 📈 Resume Comparison Timeline")
    if not history:
        st.info("Run an analysis to start tracking your resume improvement trend.")
        return

    rows = []
    for entry in reversed(history):
        date = entry.get("created_at") or entry.get("date") or ""
        rows.append({
            "Analysis": f"{entry.get('filename', 'Resume')} · {str(date)[:10]}",
            "ATS score": round(_score_from_entry(entry), 1),
        })
    timeline = pd.DataFrame(rows).reset_index(drop=True)
    timeline.index = timeline.index + 1
    st.line_chart(timeline["ATS score"], use_container_width=True)
    st.dataframe(timeline, use_container_width=True, hide_index=False)
    st.caption("Scores are ordered from oldest to newest saved resume analysis.")


def render_keyword_suggestions(history: list[dict]) -> None:
    st.markdown("### 🔑 Real-Time Keyword Suggestions")
    if not history:
        st.info("Save a resume analysis first to receive JD keyword suggestions.")
        return

    labels = [f"{item.get('filename', 'Resume')} · {str(item.get('created_at', ''))[:10]}" for item in history]
    selected = st.selectbox("Resume version", range(len(history)), format_func=lambda i: labels[i], key="history_keyword_resume")
    jd_text = st.text_area(
        "Paste a target job description",
        height=150,
        key="history_keyword_jd",
        placeholder="Paste the job description to see missing high-impact keywords while you type...",
    )
    if not jd_text:
        st.info("Start typing or paste a JD to see suggestions immediately.")
        return

    suggestions = missing_keywords(history[selected].get("analysis_result") or {}, jd_text)
    if suggestions:
        st.write("Suggested keywords to integrate naturally:")
        st.write(", ".join(suggestions))
    else:
        st.success("Your selected resume already includes the main terms from this JD.")


def render_jd_feature_suite(analysis: dict, jd_text: str = "") -> None:
    st.markdown("### 🧰 JD Comparison Methods")
    st.caption("Use the job description you already uploaded to tailor this resume.")
    options = st.radio(
        "Choose a JD method",
        ["Gap Analyzer", "Cover Letter", "Skill Gaps"],
        horizontal=True,
        key="jd_feature_method",
    )
    if options == "Gap Analyzer":
        _render_gap_analyzer(analysis, jd_text)
    elif options == "Cover Letter":
        _render_cover_letter(analysis)
    elif options == "Skill Gaps":
        _render_skill_gap_engine(analysis, jd_text)


def render_multi_analysis_results(results: list[dict]) -> None:
    st.markdown("### 📊 Multiple Job Comparison Results")
    rows = []
    for item in results:
        analysis = item.get("analysis") or {}
        jd = analysis.get("jd_comparison") or analysis.get("jd_match_analysis") or {}
        score = float(analysis.get("ATS_score", analysis.get("ats_score", 0)) or 0)
        match = float(jd.get("match_percentage", analysis.get("keyword_match", 0)) or 0)
        missing = jd.get("missing_keywords", []) or []
        rows.append({
            "Role": item.get("label", "Job description"),
            "ATS score": round(score, 1),
            "JD match": round(match, 1),
            "Missing terms": len(missing),
            "Tailoring needed": "Low" if match >= 75 else "Medium" if match >= 50 else "High",
        })

    comparison = pd.DataFrame(rows).sort_values(
        ["JD match", "ATS score"], ascending=False
    ).reset_index(drop=True)
    comparison.index = comparison.index + 1
    st.dataframe(comparison, use_container_width=True)
    best = comparison.iloc[0]
    st.success(f"Best match: {best['Role']} with {best['JD match']:.0f}% JD match.")

    st.markdown("#### Tailoring priorities")
    for item in sorted(results, key=lambda value: float(
        ((value.get("analysis") or {}).get("jd_comparison") or {}).get("match_percentage", 0) or 0
    )):
        analysis = item.get("analysis") or {}
        jd = analysis.get("jd_comparison") or analysis.get("jd_match_analysis") or {}
        missing = jd.get("missing_keywords", []) or []
        if missing:
            st.markdown(f"- **{item.get('label', 'Role')}**: add or strengthen {', '.join(map(str, missing[:8]))}")
        else:
            st.markdown(f"- **{item.get('label', 'Role')}**: no major missing terms detected")


def _render_gap_analyzer(analysis: dict, jd_text: str) -> None:
    st.markdown("#### 🎯 Job-to-Resume Gap Analyzer")
    if not jd_text:
        st.warning("No uploaded job description is available. Run a targeted JD analysis first.")
        return
    st.success("Using the uploaded job description from this analysis.")
    missing = missing_keywords(analysis, jd_text)
    if not missing:
        st.success("Excellent match. Your resume covers the main terms in this job description.")
        return
    st.warning("High-priority terms missing from this resume:")
    st.write(", ".join(missing))
    st.markdown("Add these terms naturally to relevant experience bullets, skills, or your summary.")


def _render_cover_letter(analysis: dict) -> None:
    st.markdown("#### ✍️ Cover Letter Generator")
    job_title = st.text_input("Job title", value="Data Analyst", key="jd_cover_job_title")
    company_name = st.text_input("Company name", value="Target Company", key="jd_cover_company_name")
    strengths = _safe_list(analysis.get("strengths", []))
    skills = _safe_list(analysis.get("skills", []))[:6]
    if st.button("Generate Cover Letter", key="jd_generate_cover_letter", type="primary"):
        skill_text = ", ".join(skills) if skills else "analytical thinking and data-driven decision making"
        strength_text = ", ".join(strengths[:3]) if strengths else "clear communication and structured execution"
        letter = (
            f"Dear Hiring Manager at {company_name},\n\n"
            f"I am excited to apply for the {job_title} role at {company_name}. "
            f"My background includes {skill_text}, supported by strengths in {strength_text}. "
            "I would welcome the opportunity to bring this experience to your team and deliver measurable impact.\n\n"
            "Sincerely,\n[Your Name]"
        )
        st.text_area("Generated draft", value=letter, height=240, key="generated_cover_letter")


def _render_skill_gap_engine(analysis: dict, jd_text: str) -> None:
    st.markdown("#### 🧠 Skill Gap Recommendation Engine")
    if not jd_text:
        st.warning("No uploaded job description is available. Run a targeted JD analysis first.")
        return
    st.success("Using the uploaded job description from this analysis.")
    missing = missing_keywords(analysis, jd_text, limit=10)
    if not missing:
        st.success("No major skill gaps detected for this job description.")
        return
    for skill in missing:
        st.markdown(f"- 🔹 {skill.title()} — add a measurable result using this skill")


def _render_multi_job_compare(analysis: dict) -> None:
    st.markdown("#### 📊 Multiple Job Comparison")
    st.caption("Compare this resume against 3–5 job descriptions. Separate each JD with `---`.")
    jd_block = st.text_area("Job descriptions", height=220, key="jd_multi_job_text")
    if not jd_block:
        st.info("Paste at least two job descriptions to compare role fit.")
        return
    jobs = [section.strip() for section in re.split(r"\n\s*---\s*\n", jd_block) if section.strip()]
    if len(jobs) < 2:
        st.warning("Add at least two job descriptions separated by `---`.")
        return
    if len(jobs) > 5:
        st.warning("Only the first five job descriptions are compared.")
        jobs = jobs[:5]
    resume_terms = extract_resume_terms(analysis)
    rows = []
    for index, job in enumerate(jobs, start=1):
        job_terms = _normalize_terms(job)
        overlap = len(resume_terms & job_terms)
        rows.append({"Role": f"Role {index}", "Match %": round(overlap / max(1, len(job_terms)) * 100, 1), "Matched terms": overlap})
    result = pd.DataFrame(rows).sort_values("Match %", ascending=False).reset_index(drop=True)
    result.index = result.index + 1
    st.dataframe(result, use_container_width=True)
    st.success(f"Best current match: {result.iloc[0]['Role']} at {result.iloc[0]['Match %']:.1f}%.")