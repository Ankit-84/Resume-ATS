import streamlit as st

def render():
    """Render the creative and interactive resources page"""
    
    # ==========================================
    # 🎨 CUSTOM CSS STYLING
    # ==========================================
    st.markdown("""
    <style>
        .resource-header {
            text-align: center;
            padding: 3rem 1.5rem;
            margin-top : 3rem !important;
            background: linear-gradient(135deg, #10b981 0%, #047857 50%, #064e3b 100%);
            color: white;
            border-radius: 16px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(16, 185, 129, 0.2);
        }
        .resource-header h1 {
            color: white !important;
            font-size: 2.8rem !important;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        .resource-header p {
            font-size: 1.15rem;
            opacity: 0.9;
            margin-bottom: 0;
        }
        
        /* Container Hover Effects */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            background: rgba(255, 255, 255, 0.01);
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(16, 185, 129, 0.15);
            border-color: #10b981;
        }
        
        /* Styled checkmarks/crosses */
        .do-item { color: #10b981; font-weight: 500; }
        .dont-item { color: #ef4444; font-weight: 500; }
    </style>
    
    <div class="resource-header">
        <h1>📚 ATS Resource Hub</h1>
        <p>Master the algorithms. Optimize your formatting. Land the interview.</p>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # 📝 INTERACTIVE CHECKLIST (New Feature)
    # ==========================================
    st.markdown("### 📋 Interactive Pre-Scan Checklist")
    st.caption("Check off these essential formatting rules before you run your resume through the scorer.")
    
    with st.container(border=True):
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            c1 = st.checkbox("No tables, columns, or hidden text boxes used")
            c2 = st.checkbox("Standard fonts only (Arial, Calibri, Times New Roman)")
            c3 = st.checkbox("Saved as a text-searchable PDF or DOCX")
            
        with col_c2:
            c4 = st.checkbox("Contact info is in the body, not the header/footer")
            c5 = st.checkbox("All acronyms are spelled out at least once")
            c6 = st.checkbox("Section titles are standard (e.g., 'Work Experience')")
            
        # Calculate and display progress
        checks = [c1, c2, c3, c4, c5, c6]
        score = sum(checks)
        progress = score / len(checks)
        
        st.write("")
        if progress == 1.0:
            st.success("🎉 100% Ready! Your formatting is perfectly ATS-safe.")
            st.progress(progress)
        elif progress > 0:
            st.info(f"Keep going! You meet {score} out of 6 basic ATS requirements.")
            st.progress(progress)
        else:
            st.progress(0.0)

    st.write("")
    st.write("")

    # ==========================================
    # ⚖️ DO'S & DON'TS CARDS
    # ==========================================
    st.markdown("### ⚖️ The Golden Rules of ATS")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        with st.container(border=True):
            st.markdown("#### ✅ Always Do This")
            st.markdown("""
            - <span class="do-item">✔</span> Use standard section headings (Education, Experience, Skills)
            - <span class="do-item">✔</span> Mirror exact keywords from the job description
            - <span class="do-item">✔</span> Keep formatting incredibly simple and linear
            - <span class="do-item">✔</span> Quantify your achievements (e.g., "Increased sales by 15%")
            - <span class="do-item">✔</span> List hard skills explicitly in a dedicated section
            """, unsafe_allow_html=True)
            
            with st.expander("💡 Why does simple formatting matter?"):
                st.write("ATS bots read text sequentially from left to right, top to bottom. Complex layouts confuse the parser, causing your text to scramble or get deleted entirely.")

    with col2:
        with st.container(border=True):
            st.markdown("#### ❌ Never Do This")
            st.markdown("""
            - <span class="dont-item">✖</span> Avoid multi-column layouts completely
            - <span class="dont-item">✖</span> Do not use headers/footers for contact info
            - <span class="dont-item">✖</span> Never include photos, graphics, or charts
            - <span class="dont-item">✖</span> Do not "keyword stuff" invisibly (white text)
            - <span class="dont-item">✖</span> Avoid unusual section names (e.g., "My Journey")
            """, unsafe_allow_html=True)
            
            with st.expander("💡 Why are headers/footers dangerous?"):
                st.write("Many older ATS systems completely drop data located in the document's header or footer blocks. If your email is there, the recruiter might never see it.")

    st.write("")
    st.markdown("---")
    st.write("")

    # ==========================================
    # 🔑 KEYWORDS EXPLORER
    # ==========================================
    st.markdown("### 🔑 High-Impact ATS Keywords")
    st.caption("Click through the tabs to see highly parsed terms by industry.")
    
    tab1, tab2, tab3 = st.tabs(["💻 Software & ML", "💼 Business & Product", "🎨 Creative & UI"])
    
    with tab1:
        st.markdown("""
        **Core Tech Stack & AI:**
        *   **Languages:** Python, C, C++, JavaScript, SQL
        *   **Machine Learning:** PyTorch, Scikit-Learn, Pandas, NumPy, NLP
        *   **Backend & Data:** Supabase, ChromaDB, REST APIs, Streamlit
        *   **Concepts:** Object-Oriented Programming, Data Structures, Vector Databases, Time Complexity
        """)
    
    with tab2:
        st.markdown("""
        **Management & Operations:**
        *   **Methodologies:** Agile, Scrum, Kanban, Lean
        *   **Execution:** Cross-functional collaboration, Stakeholder management, KPI tracking
        *   **Strategy:** Market research, Product roadmap, Revenue growth, Go-to-market (GTM)
        """)
    
    with tab3:
        st.markdown("""
        **Design & User Experience:**
        *   **Tools:** Figma, Adobe Creative Suite, Sketch, InVision
        *   **Processes:** Wireframing, Rapid Prototyping, A/B Testing, User Research
        *   **Concepts:** Human-Computer Interaction (HCI), Accessibility (WCAG), Responsive Design
        """)

    st.write("")
    st.markdown("---")
    st.write("")

    # ==========================================
    # 📄 UPCOMING FEATURE TEASER
    # ==========================================
    st.markdown("### 📄 ATS-Optimized Templates")
    
    with st.container(border=True):
        t_col1, t_col2 = st.columns([3, 1])
        
        with t_col1:
            st.markdown("#### The 'Zero-Fail' Template Pack")
            st.write("We are currently designing a set of beautiful, 100% ATS-compliant templates that guarantee perfect text parsing across Workday, Taleo, and Greenhouse.")
            
        with t_col2:
            st.button("🔒 Coming Soon", disabled=True, use_container_width=True)