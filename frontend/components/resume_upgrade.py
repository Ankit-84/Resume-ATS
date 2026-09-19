from typing import Any, Dict, List

import streamlit as st
import streamlit.components.v1 as components


def display_section_completeness(analysis: Dict[str, Any]) -> None:
    data = analysis.get("section_completeness") or {}
    sections: List[Dict[str, Any]] = data.get("sections") or []
    if not sections:
        return
    percentage = int(data.get("percentage", 0))
    st.markdown("### Resume Health Check")
    st.caption("A quick ATS-readiness checklist for the sections recruiters expect to find.")
    st.progress(percentage / 100, text=f"{data.get('completed', 0)} of {data.get('total', len(sections))} sections complete · {percentage}%")
    cols = st.columns(2)
    for index, item in enumerate(sections):
        with cols[index % 2]:
            icon = "✓" if item.get("complete") else "!"
            color = "#047857" if item.get("complete") else "#b45309"
            st.markdown(
                f"<div style='border-left:4px solid {color}; padding:.65rem .8rem; margin:.35rem 0; background:#f8fafc;'>"
                f"<strong style='color:{color};'>{icon} {item.get('label', 'Section')}</strong>"
                f"<div style='font-size:.82rem; color:#64748b;'>{'' if item.get('complete') else item.get('tip', '')}</div></div>",
                unsafe_allow_html=True,
            )


def display_rewrite_mode(analysis: Dict[str, Any]) -> None:
    cards: List[Dict[str, Any]] = analysis.get("rewrite_mode") or []
    if not cards:
        return
    st.markdown("### Rewrite Mode")
    st.caption("Use these ATS-safe rewrites as a starting point. Keep only claims that are truthful for your experience.")
    for index, card in enumerate(cards):
        with st.expander(f"{card.get('section', 'Resume section')} rewrite", expanded=index == 0):
            before, after = st.columns(2)
            with before:
                st.markdown("**Before**")
                st.text_area("Current version", card.get("before", ""), height=130, disabled=True, key=f"before_{index}")
            with after:
                st.markdown("**After**")
                st.text_area("Suggested version", card.get("after", ""), height=130, key=f"after_{index}")
                st.caption(card.get("why", ""))
            escaped = (card.get("after", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("\n", "&#10;"))
            components.html(
                f"<button onclick=\"navigator.clipboard.writeText(this.dataset.text)\" data-text=\"{escaped}\" style=\"border:1px solid #cbd5e1;border-radius:6px;background:#fff;padding:6px 12px;cursor:pointer\">Copy suggestion</button>",
                height=38,
            )
