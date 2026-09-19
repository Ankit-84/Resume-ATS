# Resume ATS Scorer

AI-powered resume analysis and job-application optimization platform built with FastAPI, Streamlit, spaCy, Sentence Transformers, Groq, and Supabase.

## Overview

Resume ATS Scorer helps candidates understand how an Applicant Tracking System may evaluate a resume and gives practical, ready-to-use improvements. It supports PDF and DOCX uploads, optional job-description matching, skill evidence validation, rewrite suggestions, version comparisons, and downloadable reports.

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

Paste a job description or upload a `.txt` file to calculate:

- Match percentage
- Semantic similarity
- Matched keywords
- Missing keywords
- Skills gap

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
- Swagger docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

Avoid running multiple Uvicorn instances on port 8000. A second instance causes Windows `WinError 10048` because the port is already in use.

## User workflow

1. Open the Streamlit frontend.
2. Sign in or create an account.
3. Select `General ATS Score` or `Job Description Comparison`.
4. Upload a PDF or DOCX resume up to 5 MB.
5. Optionally paste a job description or upload a `.txt` job description.
6. Click `Run AI Analysis`.
7. Review the score breakdown, section checklist, Enhancement Lab, Rewrite Mode, and detailed recommendations.
8. Generate a PDF report.
9. Run improved resume versions again and compare them from History.

## API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/` | API metadata and route summary |
| `GET` | `/api/v1/health` | Model readiness check |
| `POST` | `/api/v1/analyze-resume` | Analyze PDF or DOCX resume |
| `GET` | `/api/v1/history` | Get signed-in user history |
| `DELETE` | `/api/v1/history/{analysis_id}` | Delete a saved analysis |
| `POST` | `/api/v1/generate-pdf` | Generate a PDF from analysis data |
| `GET` | `/api/v1/history/{analysis_id}/pdf` | Generate a saved analysis PDF |

Protected endpoints require:

```text
Authorization: Bearer <supabase_access_token>
```

## Troubleshooting

### Port 8000 is already in use

Find the process:

```powershell
Get-NetTCPConnection -LocalPort 8000 -State Listen
```

Stop the matching Uvicorn process, then start one backend instance.

### `libmagic` or `failed to find libmagic`

The current parser detects supported PDF, DOC, and DOCX signatures without requiring native `libmagic`, so restart Uvicorn after pulling the latest code.

### WeasyPrint GTK/Pango warning on Windows

The application automatically uses ReportLab on Windows. Restart the backend after changing PDF code and regenerate the report.

### Groq model not found

The configured parser model is `openai/gpt-oss-20b`. Confirm that the Groq key has access to this model and that the backend loaded the current code.

### Missing spaCy model

Run:

```powershell
python -m spacy download en_core_web_sm
```

If downloads are blocked, the blank English fallback allows startup with reduced NER-based detection.

### Features do not appear

Restart both services and run a fresh analysis. Existing Streamlit session data or saved analyses created before the new response fields will not contain completeness, rewrite, or Enhancement Lab data.

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
