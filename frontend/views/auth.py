import streamlit as st
from frontend.services import supabase_client

def render():
    # Centered layout using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>Welcome to ATS Scorer 🚀</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666;'>Sign in to save your resume scores and access history.</p>", unsafe_allow_html=True)
        st.write("") # Spacer
        
        # Display Auth Messages
        if st.session_state.auth_error:
            st.error(st.session_state.auth_error, icon="🚨")
            st.session_state.auth_error = None
        if st.session_state.auth_info:
            st.info(st.session_state.auth_info, icon="ℹ️")
            st.session_state.auth_info = None

        # Container for styling
        with st.container(border=True):
            tab_in, tab_up = st.tabs(["🔐 Sign In", "✨ Create Account"])

            with tab_in:
                with st.form("signin_form", clear_on_submit=False):
                    email = st.text_input("Email", key="signin_email", placeholder="you@example.com")
                    password = st.text_input("Password", type="password", key="signin_pw", placeholder="••••••••")
                    submitted = st.form_submit_button("Sign in", use_container_width=True, type="primary")
                    
                if submitted:
                    result = supabase_client.sign_in_with_password(email, password)
                    if "error" in result:
                        st.session_state.auth_error = result["error"]
                    else:
                        st.session_state.access_token  = result["access_token"]
                        st.session_state.refresh_token = result["refresh_token"]
                        st.session_state.user_id       = result["user_id"]
                        st.session_state.user_email    = result["email"]
                        st.session_state.current_view  = 'landing' # Redirect to home after login
                    st.rerun()

            with tab_up:
                with st.form("signup_form", clear_on_submit=False):
                    email_up = st.text_input("Email", key="signup_email", placeholder="you@example.com")
                    password_up = st.text_input("Password", type="password", key="signup_pw", placeholder="Min 6 characters")
                    submitted_up = st.form_submit_button("Create Account", use_container_width=True, type="primary")
                    
                if submitted_up:
                    result = supabase_client.sign_up_with_password(email_up, password_up)
                    if "error" in result:
                        st.session_state.auth_error = result["error"]
                    elif result.get("pending_confirmation"):
                        st.session_state.auth_info = f"Check your inbox — confirmation email sent to {result['email']}."
                    else:
                        st.session_state.access_token  = result["access_token"]
                        st.session_state.refresh_token = result["refresh_token"]
                        st.session_state.user_id       = result["user_id"]
                        st.session_state.user_email    = result["email"]
                        st.session_state.current_view  = 'landing'
                    st.rerun()

            st.markdown("<div style='text-align:center; margin: 15px 0; color:#94a3b8;'>— OR —</div>", unsafe_allow_html=True)

            oauth = supabase_client.google_oauth_url()
            if "error" in oauth:
                st.caption(f"Google sign-in unavailable: {oauth['error']}")
            else:
                st.link_button(
                    "🌐 Continue with Google",
                    url=oauth["url"],
                    use_container_width=True,
                )