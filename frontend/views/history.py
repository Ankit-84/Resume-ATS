import requests
import streamlit as st
from datetime import datetime

from frontend.services import api_client
from frontend.components.version_compare import display_version_compare

def _show_backend_error(exc: Exception) -> None:
    if isinstance(exc, requests.ConnectionError):
        st.error("🚨 Could not reach the backend. Is it running on port 8000?")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        st.error(f"⚠️ Backend returned {exc.response.status_code}: {exc.response.text}")
    else:
        st.error(f"❌ Unexpected error: {exc}")


def render() -> None:
    # ==========================================
    # 🎨 CUSTOM CSS STYLING
    # ==========================================
    st.markdown("""
    <style>
        .history-header {
            text-align: center;
            padding: 2.5rem 1rem;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            border-radius: 16px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(139, 92, 246, 0.2);
        }
        .history-header h1 {
            color: white !important;
            font-size: 2.5rem !important;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        .history-header p {
            font-size: 1.1rem;
            opacity: 0.9;
            margin-bottom: 0;
        }
        
        /* Card Hover Effects */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            background: rgba(255, 255, 255, 0.01);
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(139, 92, 246, 0.15);
            border-color: #8b5cf6;
        }
        
        /* Score Badges */
        .score-badge {
            padding: 8px 15px;
            border-radius: 25px;
            font-weight: 700;
            font-size: 1rem;
            display: inline-block;
            width: 100%;
        }
        .score-high { background-color: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid #10b981; }
        .score-med { background-color: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid #f59e0b; }
        .score-low { background-color: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid #ef4444; }
        .score-jd { background-color: rgba(139, 92, 246, 0.15); color: #8b5cf6; border: 1px solid #8b5cf6; }
    </style>
    
    <div class="history-header">
        <h1>📊 Analysis History</h1>
        <p>Track your optimization progress and review past resume scores.</p>
    </div>
    """, unsafe_allow_html=True)

    access_token = st.session_state.get("access_token")
    if not access_token:
        st.warning("⚠️ **Authentication Required:** Please log in via the navigation menu to view your saved history.")
        return

    try:
        with st.spinner("⏳ Fetching your history..."):
            history = api_client.get_history(access_token)
    except requests.RequestException as exc:
        _show_backend_error(exc)
        return

    # ==========================================
    # 📭 EMPTY STATE
    # ==========================================
    if not history:
        with st.container(border=True):
            st.info("📭 No analyses found for this account.")
            st.write("Ready to optimize your first resume and bypass the bots?")
            st.write("")
            _, mid, _ = st.columns([1, 1, 1])
            with mid:
                if st.button("🎯 Go to ATS Scorer", use_container_width=True, type="primary"):
                    st.session_state.current_view = "scorer"
                    st.rerun()
        return

    # ==========================================
    # 📈 HISTORY DASHBOARD
    # ==========================================
    st.markdown(f"### 📈 Your Track Record (Total: {len(history)})")
    st.write("")
    display_version_compare(history)
    st.markdown("---")

    for idx, entry in enumerate(history):
        filename = entry.get("filename", "resume.pdf")
        ats_score = float(entry.get("ats_score", 0))
        created_at_raw = entry.get("created_at", "Unknown date")
        
        # Make the ISO date human-readable
        try:
            if 'T' in created_at_raw:
                dt = datetime.fromisoformat(created_at_raw.replace('Z', '+00:00'))
                display_date = dt.strftime("%b %d, %Y • %I:%M %p")
            else:
                display_date = created_at_raw
        except Exception:
            display_date = created_at_raw
            
        analysis = entry.get("analysis_result", {}) or {}
        component_scores = analysis.get("component_scores", {}) or {}
        jd_comparison = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")

        # Determine color tier for the main score
        badge_class = "score-high" if ats_score >= 80 else "score-med" if ats_score >= 60 else "score-low"
        
        with st.container(border=True):
            # 1️⃣ Top Row: Basic Info & Main Metrics
            col_info, col_score, col_jd, col_del = st.columns([3.5, 1.5, 1.5, 0.8], vertical_alignment="center")
            
            with col_info:
                st.markdown(f"#### 📄 {filename}")
                st.caption(f"🕒 {display_date}")
                
            with col_score:
                st.markdown(f"<div class='score-badge {badge_class}' style='text-align: center;'>Score: {ats_score:.0f}/100</div>", unsafe_allow_html=True)
                
            with col_jd:
                if jd_comparison:
                    match_pct = jd_comparison.get('match_percentage', 0)
                    st.markdown(f"<div class='score-badge score-jd' style='text-align: center;'>JD Match: {match_pct:.0f}%</div>", unsafe_allow_html=True)
                else:
                    st.write("") # Keep spacing aligned if no JD was provided
                    
            with col_del:
                entry_id = entry.get("id")
                if entry_id:
                    if st.button("🗑️", key=f"delete_{idx}", help="Delete this entry permanently", use_container_width=True):
                        try:
                            api_client.delete_history_entry(str(entry_id), access_token)
                            st.toast("✅ Analysis deleted successfully!")
                            st.rerun()
                        except requests.RequestException as exc:
                            _show_backend_error(exc)
                            
            # 2️⃣ Bottom Row: Detailed Breakdown Expander
            with st.expander("📊 View Detailed Breakdown"):
                c1, c2, c3, c4, c5 = st.columns(5)
                with c1:
                    st.metric("Formatting", f"{component_scores.get('formatting', 0):.0f}/20")
                with c2:
                    st.metric("Keywords", f"{component_scores.get('keywords', 0):.0f}/25")
                with c3:
                    st.metric("Content", f"{component_scores.get('content', 0):.0f}/25")
                with c4:
                    st.metric("Skill Validation", f"{component_scores.get('skill_validation', 0):.0f}/15")
                with c5:
                    st.metric("ATS Parsing", f"{component_scores.get('ats_compatibility', 0):.0f}/15")