from typing import List, Tuple
import math
from collections import Counter

def tokenize(text: str) -> List[str]:
    return [word.lower() for word in text.split() if word.isalnum()]

def get_cosine_similarity(vec1: Counter, vec2: Counter) -> float:
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    return float(numerator) / denominator

def rank_candidates(job_text: str, candidates: List[Tuple[int, str]]) -> List[Tuple[int, float]]:
    """
    Rank candidates based on cosine similarity of term frequency (simplified).
    candidates: List of (candidate_id, resume_text)
    Returns: List of (candidate_id, score) sorted by score desc.
    """
    if not candidates:
        return []

    job_tokens = tokenize(job_text)
    job_vec = Counter(job_tokens)

    ranked = []
    for cid, text in candidates:
        cand_tokens = tokenize(text)
        cand_vec = Counter(cand_tokens)
        score = get_cosine_similarity(job_vec, cand_vec)
        ranked.append((cid, score))

    # Sort descending
    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked
