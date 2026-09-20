import streamlit as st
import time

def render():
    # ==========================================
    # 🎨 ADVANCED CSS STYLING & ANIMATIONS
    # ==========================================
    st.markdown("""
    <style>
        /* Hero Section */
        .hero-container {
            text-align: center;
            padding: 4rem 2rem;
            margin-top : 3rem !important;
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #EC4899 100%);
            color: white;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 15px 35px rgba(124, 58, 237, 0.3);
            animation: fadeInDown 0.8s ease-out;
            
        }
        .hero-title {
            font-size: 3.5rem !important;
            font-weight: 800 !important;
            margin-bottom: 0.5rem !important;
            letter-spacing: -1px;
            color: white !important;
        }
        .hero-subtitle {
            font-size: 1.3rem !important;
            font-weight: 400 !important;
            opacity: 0.9;
            margin-bottom: 2rem !important;
            color: #f8fafc !important;
        }
        
        /* Entrance Animations */
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Card Hover Effects (Targets Streamlit Native Containers) */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            transition: all 0.3s ease-in-out;
            border-radius: 15px !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 24px rgba(124, 58, 237, 0.15);
            border-color: #7C3AED !important;
        }
        
        /* Step styling */
        .step-number {
            display: inline-block;
            width: 35px;
            height: 35px;
            line-height: 35px;
            border-radius: 50%;
            background: #7C3AED;
            color: white;
            text-align: center;
            font-weight: bold;
            font-size: 1.2rem;
            margin-right: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    # ==========================================
    # 🚀 HERO SECTION
    # ==========================================
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">🎯 Resume ATS Scorer</h1>
        <p class="hero-subtitle">Beat the bots. Optimize your resume for Applicant Tracking Systems in seconds using local, private AI analysis.</p>
    </div>
    """, unsafe_allow_html=True)

    # Call-to-Action Buttons
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if st.button("🚀 Start Analyzing Your Resume Now", use_container_width=True, type="primary"):
            st.session_state.current_view = 'scorer'
            st.rerun()

    st.write("")
    st.write("")

    # ==========================================
    # 📊 INTERACTIVE SNEAK PEEK (Tabs)
    # ==========================================
    st.markdown("### 🔍 See What You Get")
    st.caption("Interact below to preview our scoring metrics before you upload.")
    
    tab1, tab2, tab3 = st.tabs(["📈 Score Breakdown", "💡 Actionable Feedback", "🔒 Privacy First"])
    
    with tab1:
        st.write("Get a comprehensive breakdown of exactly how ATS software reads your resume.")
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Formatting & Readability", "92/100", "Excellent", delta_color="normal")
        col_m2.metric("Keyword Match", "65/100", "-15 Missing Core Skills", delta_color="inverse")
        col_m3.metric("Impact & Action Verbs", "80/100", "+5 from last edit", delta_color="normal")
        st.progress(85, text="Overall ATS Compatibility Score: 85%")
        
    with tab2:
        st.info("**Example Feedback:** Your experience section lists 'Python' as a skill, but you haven't detailed any projects using it. *Suggestion: Add a bullet point quantifying your Python experience (e.g., 'Built a web scraper using Python that saved 10 hours/week').*")
        
    with tab3:
        st.success("**100% Local Processing:** Unlike other platforms, we don't send your resume to OpenAI or external APIs. Everything runs directly on your machine. Your personal data stays entirely yours.")

    st.divider()

    # ==========================================
    # ✨ FEATURES (Using styled native containers)
    # ==========================================
    st.markdown("### ✨ Why Choose ATS Scorer?")
    
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    
    with feat_col1:
        with st.container(border=True):
            st.subheader("📊 5-Dimension Scoring")
            st.write("We go beyond keyword counting. Get graded on:")
            st.markdown("- Formatting (20%)\n- Keywords & Skills (25%)\n- Content Quality (25%)\n- Skill Validation (15%)\n- ATS Parsing (15%)")
            
    with feat_col2:
        with st.container(border=True):
            st.subheader("🤖 Semantic AI Engine")
            st.write("Our AI doesn't just read words; it understands context. It verifies that your claimed skills are actually backed up by the achievements listed in your work history.")
            st.write("*(No more empty skill claims!)*")
            
    with feat_col3:
        with st.container(border=True):
            st.subheader("📄 Multi-Format Support")
            st.write("Upload your resume exactly how you export it. We support deep text extraction from:")
            st.markdown("- `.PDF` (Standard)\n- `.DOCX` (Word)\n- `.TXT` (Plain text)")

    st.divider()

    # ==========================================
    # 🛣️ HOW IT WORKS
    # ==========================================
    st.markdown("### 🛣️ How It Works")
    
    hw_col1, hw_col2, hw_col3 = st.columns(3)
    
    with hw_col1:
        st.markdown('<div><span class="step-number">1</span><b> Upload</b></div>', unsafe_allow_html=True)
        st.caption("Drop your resume into our secure, local analyzer.")
        
    with hw_col2:
        st.markdown('<div><span class="step-number">2</span><b> AI Analysis</b></div>', unsafe_allow_html=True)
        st.caption("Our local model parses your layout, keywords, and impact.")
        
    with hw_col3:
        st.markdown('<div><span class="step-number">3</span><b> Optimize</b></div>', unsafe_allow_html=True)
        st.caption("Implement the targeted feedback and land that interview.")

    # Final Bottom CTA
    st.write("")
    st.write("")
    _, center_col, _ = st.columns([1, 1, 1])
    with center_col:
        if st.button("Ready? Let's go! 🎯", use_container_width=True):
            st.session_state.current_view = 'scorer'
            st.rerun()