import streamlit as st
from frontend.services import supabase_client

def render_navbar():
    # 🎨 CSS to color the navbar and update button styles for dark backgrounds
    st.markdown("""
    <style>
    /* =========================================
       🎨 NAVBAR BACKGROUND COLOR
       ========================================= */
       
    /* Desktop Navbar Container Color */
    div[data-testid="stHorizontalBlock"]:has(#desktop-nav) {
        /* 👇 CHANGED BACKGROUND COLOR HERE 👇 */
        background: linear-gradient(90deg, #0f172a 0%, #1e1b4b 100%);
        
        padding: 12px 20px;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        margin-bottom: 10px;
        margin-top: 10px;
    }

    /* Mobile Sidebar Background Color (Kept Dark) */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%) !important;
    }

    /* 1. Desktop Navbar Buttons Styling (White text, glass effect) */
    div[data-testid="stHorizontalBlock"]:has(#desktop-nav) button {
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        background-color: rgba(255, 255, 255, 0.05); /* Slight glassmorphism */
        transition: all 0.3s ease;
    }
    
    /* Force button text to be white for contrast */
    div[data-testid="stHorizontalBlock"]:has(#desktop-nav) button p {
        color: #f8fafc !important; 
        font-weight: 600;
    }
    
    div[data-testid="stHorizontalBlock"]:has(#desktop-nav) button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(236, 72, 153, 0.3);
        border-color: #EC4899;
        background-color: rgba(236, 72, 153, 0.1);
    }
    
    /* Force mobile sidebar text to be white */
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
    }

    /* 2. Responsive Display Logic */
    
    /* 📱 MOBILE VIEW: Hide Top Navbar */
    @media (max-width: 768px) {
        div[data-testid="stHorizontalBlock"]:has(#desktop-nav),
        hr.desktop-divider {
            display: none !important;
        }
    }

    /* 💻 DESKTOP VIEW: Hide Sidebar and its Toggle */
    @media (min-width: 769px) {
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        button[data-testid="collapsedControl"],
        div[data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # ==========================================
    # 📱 MOBILE NAVBAR (Streamlit Native Sidebar)
    # ==========================================
    with st.sidebar:
        st.markdown("### 🧭 Menu")
        if st.button("🏠 Home", key="mob_home", use_container_width=True):
            st.session_state.current_view = 'landing'
            st.rerun()
        if st.button("🎯 ATS Scorer", key="mob_scorer", use_container_width=True):
            st.session_state.current_view = 'scorer'
            st.rerun()
        if st.button("📊 History", key="mob_history", use_container_width=True):
            st.session_state.current_view = 'history'
            st.rerun()
        if st.button("📚 Resources", key="mob_resources", use_container_width=True):
            st.session_state.current_view = 'resources'
            st.rerun()
        
        st.divider()
        
        if st.session_state.access_token:
            st.caption(f"👤 Logged in as:<br>**{st.session_state.user_email}**", unsafe_allow_html=True)
            if st.button("🚪 Logout", key="mob_logout", use_container_width=True, type="primary"):
                supabase_client.sign_out()
                for k in ("access_token", "refresh_token", "user_id", "user_email"):
                    st.session_state[k] = None
                st.session_state.current_view = 'landing'
                st.rerun()
        else:
            if st.button("🔑 Login / Register", key="mob_login", type="primary", use_container_width=True):
                st.session_state.current_view = 'auth'
                st.rerun()

    # ==========================================
    # 💻 DESKTOP NAVBAR (Horizontal Columns)
    # ==========================================
    cols = st.columns([1, 1.2, 1, 1.2, 2, 1.5], gap="small", vertical_alignment="center")
    
    with cols[0]:
        # Unique ID anchor allows CSS to safely target this horizontal block
        st.markdown('<span id="desktop-nav"></span>', unsafe_allow_html=True)
        if st.button("🏠 Home", key="desk_home", use_container_width=True):
            st.session_state.current_view = 'landing'
            st.rerun()
            
    with cols[1]:
        if st.button("🎯 ATS Scorer", key="desk_scorer", use_container_width=True):
            st.session_state.current_view = 'scorer'
            st.rerun()
            
    with cols[2]:
        if st.button("📊 History", key="desk_history", use_container_width=True):
            st.session_state.current_view = 'history'
            st.rerun()
            
    with cols[3]:
        if st.button("📚 Resources", key="desk_resources", use_container_width=True):
            st.session_state.current_view = 'resources'
            st.rerun()
            
    with cols[4]:
        st.empty() # Spacer
        
    with cols[5]:
        if st.session_state.access_token:
            display_email = st.session_state.user_email.split('@')[0]
            if st.button(f"👤 {display_email} (Logout)", key="desk_logout", use_container_width=True):
                supabase_client.sign_out()
                for k in ("access_token", "refresh_token", "user_id", "user_email"):
                    st.session_state[k] = None
                st.session_state.current_view = 'landing'
                st.rerun()
        else:
            if st.button("🔑 Login / Register", key="desk_login", type="primary", use_container_width=True):
                st.session_state.current_view = 'auth'
                st.rerun()