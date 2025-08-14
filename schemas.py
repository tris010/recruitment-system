
from pydantic import BaseModel, EmailStr
from typing import Optional, List

class JobIn(BaseModel):
    title: str
    description: str
    skills: Optional[str] = None  # comma-separated

class JobOut(JobIn):
    id: int
    class Config:
        from_attributes = True

class CandidateIn(BaseModel):
    name: str
    email: EmailStr
    resume_text: Optional[str] = None  # alt to file upload

class CandidateOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    class Config:
        from_attributes = True

class ExpertIn(BaseModel):
    name: str
    email: EmailStr
    skills: Optional[str] = None

class ExpertOut(ExpertIn):
    id: int
    class Config:
        from_attributes = True

class MatchOut(BaseModel):
    id: int
    job_id: int
    candidate_id: int
    score: float
    class Config:
        from_attributes = True

class InterviewOut(BaseModel):
    id: int
    job_id: int
    candidate_id: int
    expert_id: int
    slot: str
    class Config:
        from_attributes = True
