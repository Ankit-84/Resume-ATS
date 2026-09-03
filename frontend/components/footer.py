import streamlit as st

def render_footer():
    st.markdown("""
<style>
.custom-footer {
background: linear-gradient(90deg, #0f172a 0%, #1e1b4b 100%);
color: #94a3b8;
padding: 3rem 2.5rem 1.5rem 2.5rem;
border-radius: 15px;
margin-top: 5rem;
box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.05);
font-family: sans-serif;
}
.footer-container {
display: flex;
justify-content: space-between;
flex-wrap: wrap;
gap: 2rem;
margin-bottom: 2.5rem;
}
.footer-col {
flex: 1;
min-width: 220px;
}
.footer-col h4 {
color: #f8fafc;
font-size: 1.25rem;
font-weight: 600;
margin-bottom: 1.2rem;
position: relative;
padding-bottom: 10px;
}
.footer-col h4::after {
content: '';
position: absolute;
left: 0;
bottom: 0;
width: 35px;
height: 3px;
background: #EC4899;
transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
border-radius: 2px;
}
.footer-col:hover h4::after {
width: 65px;
}
.footer-col p {
font-size: 0.95rem;
line-height: 1.6;
margin-bottom: 1rem;
}
.footer-links {
list-style: none;
padding: 0;
margin: 0;
}
.footer-links li {
margin-bottom: 0.8rem;
}
.footer-links a {
color: #94a3b8;
text-decoration: none;
transition: all 0.3s ease;
display: inline-flex;
align-items: center;
gap: 8px;
}
.footer-links a:hover {
color: #EC4899;
transform: translateX(6px);
}
.footer-bottom {
text-align: center;
padding-top: 2rem;
border-top: 1px solid rgba(255, 255, 255, 0.08);
font-size: 0.9rem;
display: flex;
flex-direction: column;
gap: 0.5rem;
}
.creator-highlight {
background: linear-gradient(135deg, #EC4899 0%, #7C3AED 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
font-weight: 700;
font-size: 1.05rem;
text-decoration: none;
transition: opacity 0.3s ease;
}
.creator-highlight:hover {
opacity: 0.8;
}
</style>

<div class="custom-footer">
<div class="footer-container">
<div class="footer-col">
<h4>🎯 ATS Scorer</h4>
<p>Empowering job seekers with local, AI-driven insights to bypass automated filters and land more interviews.</p>
<p>Build your career with confidence. 🚀</p>
</div>
<div class="footer-col">
<h4>🔗 Quick Nav</h4>
<ul class="footer-links">
<li><a href="#"><span>🏠</span> Home</a></li>
<li><a href="#"><span>🎯</span> Try ATS Scorer</a></li>
<li><a href="#"><span>📊</span> View History</a></li>
<li><a href="#"><span>📚</span> Tips & Resources</a></li>
</ul>
</div>
<div class="footer-col">
<h4>💡 Connect</h4>
<ul class="footer-links">
<li><a href="#" target="_blank"><span>🐙</span> GitHub Repository</a></li>
<li><a href="#" target="_blank"><span>💼</span> LinkedIn</a></li>
<li><a href="#" target="_blank"><span>✉️</span> Contact Support</a></li>
<li><a href="#" target="_blank"><span>🔒</span> Privacy Policy</a></li>
</ul>
</div>
</div>
<div class="footer-bottom">
<div>Designed & Developed with ❤️ by <a href="#" class="creator-highlight">Ankit Kumar</a></div>
<div>© 2026 Resume ATS Scorer. All rights reserved.</div>
</div>
</div>
""", unsafe_allow_html=True)