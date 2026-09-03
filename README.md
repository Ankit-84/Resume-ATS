<div align="center">

# 🎯 AI-Powered Resume ATS Scorer & Optimization Platform

> *Bypass automated applicant tracking systems with local, privacy-first AI analysis and targeted job description matching.*

</div>

---

## 🚀 Overview

The **ATS Resume Scorer** is a full-stack web application designed to help job seekers optimize their resumes for Applicant Tracking Systems (ATS) like Workday, Taleo, and Greenhouse. Unlike cloud-based tools that send your personal data to external APIs, this platform runs its natural language processing and semantic models locally, ensuring **100% privacy and security**.

---

## ✨ Key Features

* **📊 5-Dimension Scoring Engine:** Grades your resume across Formatting (20%), Keywords & Skills (25%), Content Quality (25%), Skill Validation (15%), and ATS Compatibility (15%).
* **🎯 Targeted Job Description Matching:** Compare your resume directly against a specific job description to compute match percentages and surface missing skills or keyword gaps.
* **🤖 Semantic AI Skill Validation:** Uses local sentence transformers to verify that your claimed skills are backed up by real achievements and projects in your work experience.
* **🔒 Secure User Authentication:** Powered by **Supabase** for secure email/password login and Google OAuth integration.
* **📈 Historical Tracking:** Automatically saves past analyses to your account so you can track your optimization progress over time.
* **📄 Professional PDF Export:** Generate and download comprehensive, beautifully formatted PDF reports of your resume analysis.

---

## 🛠️ Tech Stack

* **Frontend:** Python, Streamlit (Custom responsive design with modern top navigation, mobile drawers, and interactive dashboards).
* **Backend:** FastAPI, Uvicorn, Pydantic.
* **AI / NLP Engine:** spaCy (`en_core_web_md`), Sentence-Transformers, PyTorch.
* **Database & Auth:** Supabase (PostgreSQL).
* **Document Parsing:** PyPDF / python-docx.

---

## 📦 Package Installation & Setup

Follow these steps to set up the project environment on your local machine:

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/Resume-ATS.git](https://github.com/your-username/Resume-ATS.git)
cd Resume-ATS
 
---

## 2. Install Required Python Packages
```bash 
pip install --upgrade pip
pip install -r requirements.txt

## 3. Download spaCy Language Model
Run the following command to download the required medium English web model for NLP parsing:

```bash
python -m spacy download en_core_web_md

## ⚙️ Environment Configuration (.env)
Create a file named .env in the root directory of your project and paste your configuration credentials below:

```.env
GROQ_API_KEY="PASTE_YOUR_GROQ_API_KEY_HERE"
SENTENCE_TRANSFORMER_MODEL="all-MiniLM-L6-v2"

DATABASE_URL="PASTE_YOUR_POSTGRES_DATABASE_URL_HERE"

SUPABASE_URL="PASTE_YOUR_SUPABASE_URL_HERE"
SUPABASE_KEY="PASTE_YOUR_SUPABASE_KEY_HERE"
SUPABASE_ANON_KEY="PASTE_YOUR_SUPABASE_ANON_KEY_HERE"
AUTH_REDIRECT_URL="http://localhost:8501"

## 🚀 Running the Application
Because this application uses a decoupled architecture, you need to run two separate terminal windows simultaneously.

Terminal 1: Start the FastAPI Backend Server

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

Terminal 2: Start the Streamlit Frontend Client
Open a brand new terminal window, activate your virtual environment, and launch the UI:

```bash
streamlit run frontend/streamlit_app.py

## 💡 Usage Guide
Sign In / Register: Create an account or sign in using email/password or Google OAuth via the top navigation bar.

Choose Mode: Select between General ATS Score (resume-only audit) or Job Description Comparison (targeted keyword match).

Upload: Drop your .pdf or .docx resume into the secure upload area.

Analyze: Click Run AI Analysis and view your multi-dimensional breakdown, strength indicators, and critical gaps.

Export: Download your analysis summary or generate a clean, shareable PDF report.

## 👨‍💻 Author & Credits
Designed & Developed with ❤️ by Ankit Kumar

Institution: National Institute of Technology Nagaland (Computer Science & Engineering)

## 📝 License
© 2026 ATS Resume Scorer. All rights reserved.