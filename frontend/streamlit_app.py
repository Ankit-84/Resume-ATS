import streamlit as st
import sys
from pathlib import Path

# Put the repo root on sys.path so `from frontend.views import ...` resolves
# regardless of the directory streamlit was launched from.
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure page
st.set_page_config(
    page_title="Resume ATS Scorer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed" # Collapsed since we are using a top navbar
)

# Auth state. Populated by Supabase sign-in / sign-up / OAuth.
# All four are None when signed out, all four are set when signed in.
for key, default in [
    ("access_token", None),
    ("refresh_token", None),
    ("user_id", None),       # Supabase auth user id (uuid); also used by api_client
    ("user_email", None),
    ("auth_error", None),
    ("auth_info", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# If we just came back from Google OAuth, Supabase appends `?code=<authcode>`
# to the redirect URL. Exchange it for a session before rendering anything.
if (
    not st.session_state.access_token
    and "code" in st.query_params
):
    from frontend.services import supabase_client
    result = supabase_client.exchange_code_for_session(st.query_params["code"])

    #Always clear the ?code= param so a refresh doesn't try to re-exchange.
    st.query_params.clear()
    if "error" in result:
        st.session_state.auth_error = f"Google sign-in failed: {result['error']}"
        st.session_state.current_view = 'auth' # Route to auth page to show error
    else:
        st.session_state.access_token  = result["access_token"]
        st.session_state.refresh_token = result["refresh_token"]
        st.session_state.user_id       = result["user_id"]
        st.session_state.user_email    = result["email"]
        st.session_state.current_view  = 'landing'
        st.rerun()

#Load custom CSS
def load_css():
    try:
        css_path = Path(__file__).parent / 'assets' / 'styles.css'
        with open(css_path, 'r') as f:
            return f'<style>{f.read()}</style>'
    except FileNotFoundError:
        return ''

st.markdown(load_css(), unsafe_allow_html=True)
st.markdown("""
<style>
    /* Remove blank space on left and right edges */
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 0rem !important; /* Keep a little space at the top */
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for view management
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'landing'

# Render Top Navigation Bar
from frontend.components import navbar
navbar.render_navbar()

# Main content area - render based on current view
if st.session_state.current_view == 'landing':
    from frontend.views import landing
    landing.render()

elif st.session_state.current_view == 'scorer':
    from frontend.views import scorer
    scorer.render()

elif st.session_state.current_view == 'history':
    from frontend.views import history
    history.render()

elif st.session_state.current_view == 'resources':
    from frontend.views import resources
    resources.render()

elif st.session_state.current_view == 'auth':
    from frontend.views import auth
    auth.render()


from frontend.components import footer
footer.render_footer()