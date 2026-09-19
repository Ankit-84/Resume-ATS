from typing import Any, Dict, List

import streamlit as st


def _metrics(entry: Dict[str, Any]) -> Dict[str, float]:
    result = entry.get("analysis_result") or {}
    components = result.get("component_scores") or {}
    validation = result.get("skill_validation_details") or {}
    jd = result.get("jd_comparison") or result.get("jd_match_analysis") or {}
    keywords = result.get("matched_keywords") or []
    return {
        "ATS score": float(entry.get("ats_score", result.get("ats_score", 0)) or 0),
        "Keywords": float(len(keywords)),
        "Skill validation": float(validation.get("validation_pct", components.get("skill_validation", 0)) or 0),
        "JD match": float(jd.get("match_percentage", entry.get("keyword_match", 0)) or 0),
    }


def _keyword_changes(first: Dict[str, Any], second: Dict[str, Any]) -> tuple[list[str], list[str]]:
    first_result = first.get("analysis_result") or {}
    second_result = second.get("analysis_result") or {}
    first_words = {str(item).lower() for item in first_result.get("matched_keywords", [])}
    second_words = {str(item).lower() for item in second_result.get("matched_keywords", [])}
    return sorted(second_words - first_words), sorted(first_words - second_words)


def display_version_compare(history: List[Dict[str, Any]]) -> None:
    if len(history) < 2:
        return
    st.markdown("### Version Compare")
    st.caption("Compare any two saved resume analyses and see whether your optimization work improved the signal.")
    labels = [f"{item.get('filename', 'Resume')} · {item.get('created_at', '')[:10]}" for item in history]
    left, right = st.columns(2)
    with left:
        first_index = st.selectbox("Older version", range(len(history)), format_func=lambda i: labels[i], key="compare_first")
    with right:
        second_index = st.selectbox("Newer version", range(len(history)), index=min(1, len(history) - 1), format_func=lambda i: labels[i], key="compare_second")
    first = _metrics(history[first_index])
    second = _metrics(history[second_index])
    cols = st.columns(4)
    for column, metric in zip(cols, first):
        delta = second[metric] - first[metric]
        with column:
            st.metric(metric, f"{second[metric]:.0f}", delta=f"{delta:+.0f}")
    added, removed = _keyword_changes(history[first_index], history[second_index])
    added_col, removed_col = st.columns(2)
    with added_col:
        st.markdown("**Added keywords**")
        st.write(", ".join(added) if added else "No new matched keywords")
    with removed_col:
        st.markdown("**Removed keywords**")
        st.write(", ".join(removed) if removed else "No matched keywords removed")
