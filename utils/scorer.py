import math
import re
from collections import Counter
from typing import List, Tuple, Dict, Set

def tokenize(text: str) -> List[str]:
    """Simple tokenizer: lowercase and remove non-alphanumeric characters."""
    return re.findall(r'\b\w\w+\b', text.lower())

def compute_tf(text: str) -> Dict[str, float]:
    """Compute Term Frequency (TF)."""
    tokens = tokenize(text)
    if not tokens:
        return {}
    tf = Counter(tokens)
    total = len(tokens)
    return {t: count / total for t, count in tf.items()}

def compute_idf(corpus: List[str]) -> Dict[str, float]:
    """Compute Inverse Document Frequency (IDF)."""
    N = len(corpus)
    if N == 0:
        return {}
    
    idf = {}
    all_tokens = set()
    for text in corpus:
        tokens = set(tokenize(text))
        all_tokens.update(tokens)
        for token in tokens:
            idf[token] = idf.get(token, 0) + 1
            
    for token in all_tokens:
        idf[token] = math.log(N / (1 + idf.get(token, 0))) # +1 smoothing
    return idf

def compute_tfidf(text: str, idf: Dict[str, float]) -> Dict[str, float]:
    """Compute TF-IDF vector."""
    tf = compute_tf(text)
    return {token: val * idf.get(token, 0) for token, val in tf.items()}

def cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
    """Compute Cosine Similarity between two sparse vectors."""
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum(vec1[x] * vec2[x] for x in intersection)
    
    sum1 = sum(v**2 for v in vec1.values())
    sum2 = sum(v**2 for v in vec2.values())
    
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    
    if denominator == 0:
        return 0.0
    return numerator / denominator

def rank_candidates(job_text: str, candidates: List[Tuple[int, str]]) -> List[Tuple[int, float]]:
    """
    Rank candidates based on cosine similarity between job description and resume text.
    candidates: List of (candidate_id, resume_text)
    Returns: List of (candidate_id, score) sorted by score desc.
    """
    if not candidates:
        return []

    # Corpus includes job text and all candidate texts to compute IDF
    corpus = [job_text] + [c[1] for c in candidates]
    idf = compute_idf(corpus)
    
    # Vectorize Job
    job_vec = compute_tfidf(job_text, idf)
    
    ranked = []
    for cid, text in candidates:
        cand_vec = compute_tfidf(text, idf)
        score = cosine_similarity(job_vec, cand_vec)
        ranked.append((cid, float(score)))

    # Sort descending
    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked
