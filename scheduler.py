
from typing import List, Tuple
import itertools

def skill_overlap(job_skills: List[str], expert_skills: List[str]) -> int:
    js = set([s.strip().lower() for s in job_skills if s])
    es = set([s.strip().lower() for s in expert_skills if s])
    return len(js & es)

def pick_best_expert(job_skills: List[str], experts: List[Tuple[int, str]]) -> int:
    # experts: list of (expert_id, skills_csv)
    best_id = None
    best_score = -1
    for eid, csv in experts:
        score = skill_overlap(job_skills, (csv or "").split(","))
        if score > best_score:
            best_score = score
            best_id = eid
    return best_id
