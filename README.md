
# Automated Recruitment System (MVP)

A minimal FastAPI-based system that:
- Ingests jobs, candidates, and interviewers
- Parses resumes (PDF/DOCX/TXT)
- Computes role relevancy scores (TF–IDF + cosine similarity)
- Auto-creates an interview schedule with the best-matching interviewer

## Quickstart

```bash
# 1) Create & activate a virtual env (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Run the API
uvicorn src.app:app --reload

# 4) Open docs
# Swagger UI: http://127.0.0.1:8000/docs
# ReDoc:      http://127.0.0.1:8000/redoc
```

## API Highlights
- `POST /jobs` – create a job
- `POST /candidates` – create a candidate (upload resume file or paste text)
- `POST /experts` – add interviewers with skills
- `POST /match/{job_id}` – compute relevancy scores for all candidates for a job
- `POST /schedule/{job_id}` – schedule top candidate with best matching interviewer
- `GET /matches/{job_id}` – list matches sorted by score desc

## Data Model (SQLite)
- **Job**: id, title, description, skills (csv)
- **Candidate**: id, name, email, resume_text
- **Expert**: id, name, email, skills (csv)
- **Match**: id, job_id, candidate_id, score
- **Interview**: id, job_id, candidate_id, expert_id, slot

> This is a hackathon-friendly MVP: simple, readable, and easy to extend.
