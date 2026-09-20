# Resume ATS Scorer

AI-powered resume analysis and job-application optimization platform built with FastAPI, Streamlit, spaCy, Sentence Transformers, Groq, and Supabase.

## Overview

Resume ATS Scorer helps candidates understand how an Applicant Tracking System may evaluate a resume and gives practical, ready-to-use improvements. It supports PDF, DOC, and DOCX uploads, optional job-description matching, skill evidence validation, rewrite suggestions, version comparisons, and downloadable reports.

The application uses a decoupled architecture:

- `backend/`: FastAPI API, document parsing, scoring, AI analysis, persistence, and PDF generation.
- `frontend/`: Streamlit interface, authentication flow, analysis dashboard, history, and exports.
- `ml model/`: Local Sentence Transformer model assets and evaluation files.

## Features

### ATS scoring

The scoring engine evaluates five weighted dimensions:

| Dimension | Weight |
| --- | ---: |
| Formatting | 20% |
| Keywords and skills | 25% |
| Content quality | 25% |
| Skill validation | 15% |
| ATS compatibility | 15% |

### Job-description matching

Choose between a general ATS score, a targeted comparison, or a multiple-job comparison. Paste a job description or upload a `.txt` file to calculate:

- Match percentage
- Semantic similarity
- Matched keywords
- Missing keywords
- Skills gap

Multiple-job comparison accepts up to five job descriptions and ranks the roles by JD match and ATS score, with tailoring priorities for each role.

### Skill validation

The platform checks whether skills listed in the resume are supported by project or experience evidence. It identifies validated skills, unsupported skills, and the evidence locations found.

### ATS Enhancement Lab

Generates targeted improvements based on the analysis:

- What to change
- Where to place the change
- Current resume signal
- Ready-to-adapt example
- ATS reason
- Priority level

### Resume section completeness

The analysis dashboard checks for:

- Contact information
- Professional summary
- Skills
- Experience
- Projects
- Education
- Certifications
- LinkedIn, GitHub, or portfolio links

It returns a completion percentage and practical tips for missing sections.

### Resume Rewrite Mode

Provides before-and-after rewrite cards for:

- Professional summary
- Experience bullets
- Project descriptions
- Skills section

The suggested text is editable in Streamlit and includes a browser copy button. Suggestions are starting points and should only retain claims that are truthful.

### Resume version tracking

Saved analyses can be compared from the History page. Version comparison shows:

- ATS score delta
- Matched keyword changes
- Skill validation change
- Job-description match change
- Added keywords
- Removed keywords

The History page also includes an ATS score timeline and live keyword suggestions for a selected saved resume. Targeted analyses provide a JD feature suite with a gap analyzer, skill-gap recommendations, and a cover-letter draft generator.

### PDF reports

The application generates a multi-section PDF report containing score breakdowns, skill validation, job matching, recommendations, completeness, and rewrite suggestions.

On Windows, ReportLab is used automatically because WeasyPrint requires GTK/Pango native libraries. On Linux or other supported environments, WeasyPrint can be used when its native dependencies are installed.

### Authentication and history

Supabase provides:

- Email/password sign-in
- Account registration
- Google OAuth flow
- Saved analysis history
- Per-user history deletion

Supabase settings can be loaded from environment variables or Streamlit secrets. The frontend reads `.env` first and can fall back to `.streamlit/secrets.toml` for hosted deployments.

## Technology stack

- Python 3.12+
- FastAPI and Uvicorn
- Streamlit
- Pydantic
- spaCy and `en_core_web_md`/`en_core_web_sm`
- Sentence Transformers and PyTorch
- Groq API with `openai/gpt-oss-20b`
- Supabase Auth and PostgreSQL REST API
- pdfplumber, PyPDF2, and python-docx
- Jinja2
- ReportLab PDF fallback
- RapidFuzz keyword matching

## Project structure

```text
Resume-ATS/
|-- backend/
|   |-- api/
|   |   |-- auth.py              JWT verification
|   |   `-- routes.py            Analysis, history, and PDF endpoints
|   |-- core/config.py           Environment and scoring configuration
|   |-- database/supabase_db.py  History persistence
|   |-- models/schemas.py        API response models
|   |-- services/
|   |   |-- ats_scorer.py        Weighted ATS scoring
|   |   |-- enhancement_engine.py Targeted improvement suggestions
|   |   |-- feedback_engine.py   Resume issue detection
|   |   |-- groq_parser.py       Structured resume/JD extraction
|   |   |-- report_generator.py  HTML report rendering
|   |   |-- resume_analyzer.py   Main analysis orchestration
|   |   |-- resume_features.py   Completeness and rewrite mode
|   |   `-- pdf_export.py        WeasyPrint/ReportLab PDF output
|   |-- templates/               HTML report templates
|   `-- main.py                  FastAPI app and model startup
|-- frontend/
|   |-- components/              Dashboard and feature components
|   |   |-- career_features.py    JD tools, multi-job comparison, and history insights
|   |-- services/                API and Supabase clients
|   |-- views/                   Landing, scorer, history, auth, resources
|   `-- streamlit_app.py         Streamlit entry point
|-- ml model/                    Local model assets
|-- requirements.txt
`-- README.md
```

## Requirements

- Windows, macOS, or Linux
- Python 3.12 or newer recommended
- A Groq API key
- A Supabase project for authentication and history
- Internet access for Groq requests and first-time model downloads

## Installation

### Conda environment

```powershell
conda create -n resume-ats python=3.12
conda activate resume-ats
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

For an existing Conda `base` environment:

```powershell
conda activate base
python -m pip install -r requirements.txt
```

### spaCy model

Install the medium model for best entity and location detection:

```powershell
python -m spacy download en_core_web_md
```

If the medium model is unavailable, the backend tries `en_core_web_sm`, then starts with a blank English pipeline. The application remains usable, but entity-based location detection is reduced.

## Environment configuration

Create `.env` in the project root. Never commit this file or expose its values publicly.

```env
GROQ_API_KEY=your_groq_api_key
SENTENCE_TRANSFORMER_MODEL=all-MiniLM-L6-v2

SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_KEY=your_server_key
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_JWT_SECRET=your_jwt_secret
AUTH_REDIRECT_URL=http://localhost:8501

BACKEND_URL=http://127.0.0.1:8000
```

The backend uses `SUPABASE_KEY` for server-side history operations. The frontend uses `SUPABASE_ANON_KEY` for authentication. Do not use placeholder values in a running environment.

For Streamlit deployments, the equivalent values can be placed in `.streamlit/secrets.toml`:

```toml
[supabase]
SUPABASE_URL = "https://your-project-ref.supabase.co"
SUPABASE_ANON_KEY = "your_anon_key"

[backend]
url = "http://127.0.0.1:8000"

[google_oauth]
redirect_uri = "http://localhost:8501"
```

## Run locally

Start the backend from the project root in Terminal 1:

```powershell
conda activate base
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Wait for:

```text
Application startup complete.
Uvicorn running on http://127.0.0.1:8000
```

Start the frontend in Terminal 2:

```powershell
conda activate base
streamlit run frontend/streamlit_app.py --server.address 127.0.0.1 --server.port 8501
```

Open:

- Frontend: http://127.0.0.1:8501
- API root: http://127.0.0.1:8000
- Health check: http://127.0.0.1:8000/api/v1/health
- Swagger docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

Avoid running multiple Uvicorn instances on port 8000. A second instance causes Windows `WinError 10048` because the port is already in use.

## API endpoints

All analysis, history, and PDF routes are under `/api/v1` and require a Supabase bearer token except for the health check.

| Method | Route | Purpose |
| --- | --- | --- |
| `POST` | `/api/v1/analyze-resume` | Analyze a PDF, DOC, or DOCX resume with an optional JD |
| `GET` | `/api/v1/health` | Confirm that the API and its models are loaded |
| `GET` | `/api/v1/history` | List the signed-in user's saved analyses |
| `DELETE` | `/api/v1/history/{analysis_id}` | Delete one saved analysis |
| `POST` | `/api/v1/generate-pdf` | Generate a PDF from an analysis response |
| `GET` | `/api/v1/history/{analysis_id}/pdf` | Generate a PDF for a saved analysis |

## User workflow

1. Open the Streamlit frontend.
2. Sign in or create an account.
3. Select `General ATS Score`, `Job Description Comparison`, or `Multiple Job Comparison`.
4. Upload a PDF, DOC, or DOCX resume up to 5 MB.
5. Optionally paste a job description, upload a `.txt` job description, or provide up to five job descriptions for comparison.
6. Click `Run AI Analysis`.
7. Review the score breakdown, section checklist, Enhancement Lab, Rewrite Mode, and detailed recommendations.
8. Use the JD tools, generate a PDF report, or download a text summary.
9. Run improved resume versions again and compare them from History.

Protected endpoints require:

```text
Authorization: Bearer <supabase_access_token>
```


## Validation

Basic project validation:

```powershell
python -m compileall -q backend frontend
```

Runtime smoke checks:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/api/v1/health
Invoke-WebRequest http://127.0.0.1:8501/
```

## Security notes

- Keep `.env` out of version control.
- Rotate credentials if they were ever shared or committed.
- Do not expose Supabase service keys or Groq keys in frontend code.
- Use HTTPS and secure secret storage for deployment.
- Treat generated rewrite examples as suggestions and verify every claim before using it.

## License

Copyright 2026 ATS Resume Scorer. All rights reserved.
