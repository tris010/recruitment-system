
import os
from datetime import datetime, timedelta
from typing import List

from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import Job, Candidate, Expert, Match, Interview
from .schemas import JobIn, JobOut, CandidateIn, CandidateOut, ExpertIn, ExpertOut, MatchOut, InterviewOut
from .utils.resume_parser import parse_resume
from .utils.scorer import rank_candidates
from .scheduler import pick_best_expert

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Automated Recruitment System (MVP)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["health"])
def health():
    return {"status": "ok"}

# Jobs
@app.post("/jobs", response_model=JobOut)
def create_job(payload: JobIn, db: Session = Depends(get_db)):
    job = Job(title=payload.title, description=payload.description, skills=payload.skills or "")
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

@app.get("/jobs", response_model=List[JobOut])
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()

# Candidates
@app.post("/candidates", response_model=CandidateOut)
def create_candidate(payload: CandidateIn, db: Session = Depends(get_db)):
    if not payload.resume_text:
        raise HTTPException(400, "resume_text is required if not uploading a file.")
    cand = Candidate(name=payload.name, email=payload.email, resume_text=payload.resume_text)
    db.add(cand)
    db.commit()
    db.refresh(cand)
    return cand

@app.post("/candidates/upload", response_model=CandidateOut)
async def create_candidate_with_file(
    name: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    temp_dir = "uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, file.filename)
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    text = parse_resume(temp_path)
    if not text.strip():
        raise HTTPException(400, "Could not extract text from the uploaded resume.")
    cand = Candidate(name=name, email=email, resume_text=text)
    db.add(cand)
    db.commit()
    db.refresh(cand)
    return cand

@app.get("/candidates", response_model=List[CandidateOut])
def list_candidates(db: Session = Depends(get_db)):
    return db.query(Candidate).all()

# Experts
@app.post("/experts", response_model=ExpertOut)
def create_expert(payload: ExpertIn, db: Session = Depends(get_db)):
    exp = Expert(name=payload.name, email=payload.email, skills=payload.skills or "")
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

@app.get("/experts", response_model=List[ExpertOut])
def list_experts(db: Session = Depends(get_db)):
    return db.query(Expert).all()

# Matching
@app.post("/match/{job_id}", response_model=List[MatchOut])
def match_candidates(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")

    cands = db.query(Candidate).all()
    if not cands:
        return []

    job_text = f"{job.title}\n{job.description}\nSkills: {job.skills}"
    pairs = [(c.id, c.resume_text) for c in cands]
    ranked = rank_candidates(job_text, pairs)

    # Clear old matches for this job
    db.query(Match).filter(Match.job_id == job_id).delete()
    db.commit()

    out = []
    for cid, score in ranked:
        m = Match(job_id=job_id, candidate_id=cid, score=float(score))
        db.add(m)
        db.commit()
        db.refresh(m)
        out.append(m)
    # Return sorted by score desc
    out.sort(key=lambda x: x.score, reverse=True)
    return out

@app.get("/matches/{job_id}", response_model=List[MatchOut])
def get_matches(job_id: int, db: Session = Depends(get_db)):
    return db.query(Match).filter(Match.job_id == job_id).order_by(Match.score.desc()).all()

# Scheduling
@app.post("/schedule/{job_id}", response_model=InterviewOut)
def schedule_interview(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")

    top_match = db.query(Match).filter(Match.job_id == job_id).order_by(Match.score.desc()).first()
    if not top_match:
        raise HTTPException(400, "Run /match/{job_id} first to compute matches.")

    experts = db.query(Expert).all()
    if not experts:
        raise HTTPException(400, "No experts available. Add via POST /experts.")

    best_expert_id = pick_best_expert((job.skills or "").split(","), [(e.id, e.skills or "") for e in experts])
    if not best_expert_id:
        best_expert_id = experts[0].id

    slot = (datetime.utcnow() + timedelta(days=1)).replace(microsecond=0).isoformat() + "Z"
    interview = Interview(job_id=job.id, candidate_id=top_match.candidate_id, expert_id=best_expert_id, slot=slot)
    db.add(interview)
    db.commit()
    db.refresh(interview)
    return interview
