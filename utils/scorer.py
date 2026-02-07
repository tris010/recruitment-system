from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_candidates(job_text: str, candidates: List[Tuple[int, str]]) -> List[Tuple[int, float]]:
    """
    Rank candidates based on cosine similarity between job description and resume text.
    candidates: List of (candidate_id, resume_text)
    Returns: List of (candidate_id, score) sorted by score desc.
    """
    if not candidates:
        return []

    # Prepare corpus: [job_text, cand1_text, cand2_text, ...]
    ids = [c[0] for c in candidates]
    texts = [job_text] + [c[1] for c in candidates]

    # Vectorize
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform(texts)
    except ValueError:
        # Possible if empty vocabulary, e.g. text is all stop words or empty
        return [(cid, 0.0) for cid in ids]

    # Calculate cosine similarity of job (index 0) vs all candidates (indices 1..)
    # cosine_similarity returns a matrix. We want row 0 (job) vs all others.
    # shape: (1, n_candidates)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Pair up ids with scores
    ranked = []
    for i, score in enumerate(cosine_sim):
        ranked.append((ids[i], float(score)))

    # Sort descending
    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked
