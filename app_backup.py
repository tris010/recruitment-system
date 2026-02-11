
import logging
import sys

# Configure logging to stderr for Vercel
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger("app")

try:
    from db import Base, engine, get_db
    from models import Job, Candidate, Expert, Match, Interview
    from schemas import JobIn, JobOut, CandidateIn, CandidateOut, ExpertIn, ExpertOut, MatchOut, InterviewOut
    # from utils.resume_parser import parse_resume
    # from utils.scorer import rank_candidates
    # from scheduler import pick_best_expert
    
    logger.info("Attempting to create database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")
except Exception as e:
    logger.error(f"CRITICAL STARTUP ERROR: {e}")
    # Continue so we can serve /health and debug


from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ... imports ...
from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

app = FastAPI(title="Automated Recruitment System (MVP)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", tags=["health"])
def read_index():
    return FileResponse('static/index.html')

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
