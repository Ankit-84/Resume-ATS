from typing import Any, Dict, List

import streamlit as st


_PRIORITY_STYLE = {
    "high": ("HIGH", "#991b1b", "#fef2f2"),
    "medium": ("MEDIUM", "#92400e", "#fffbeb"),
    "low": ("LOW", "#3730a3", "#eef2ff"),
}


def display_enhancement_lab(analysis: Dict[str, Any]) -> None:
    suggestions: List[Dict[str, Any]] = analysis.get("enhancement_suggestions") or []
    if not suggestions:
        return

    st.markdown("### 🧪 ATS Enhancement Lab")
    st.caption("Personalized rewrites showing what to change, where to place it, and why it improves ATS performance.")

    for suggestion in suggestions:
        priority = (suggestion.get("priority") or "medium").lower()
        label, color, background = _PRIORITY_STYLE.get(priority, _PRIORITY_STYLE["medium"])
        title = suggestion.get("title", "Resume improvement")
        category = suggestion.get("category", "Resume")

        st.markdown(
            f"<div style='border-left:4px solid {color}; background:{background}; padding:0.8rem 1rem; border-radius:6px 6px 0 0;'>"
            f"<strong style='color:{color};'>{label}</strong> &nbsp; <strong>{title}</strong>"
            f"<span style='color:#64748b; float:right;'>{category}</span></div>",
            unsafe_allow_html=True,
        )
        with st.container(border=True):
            st.markdown(f"**What to change:** {suggestion.get('what_to_change', '')}")
            st.markdown(f"**Where to place it:** {suggestion.get('where_to_place', '')}")
            if suggestion.get("current_text"):
                st.markdown("**Current signal:**")
                st.caption(suggestion["current_text"])
            if suggestion.get("example"):
                st.markdown("**Ready-to-adapt example:**")
                st.code(suggestion["example"], language="text")
            if suggestion.get("ats_reason"):
                st.info(f"ATS impact: {suggestion['ats_reason']}")
