import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os


def rank_candidates(resume_vecs, job_vec, raw_resumes, job_description, file_paths):
    """
    Rank candidates by cosine similarity and find matched keywords
    """
    # Calculate cosine similarity
    similarities = cosine_similarity(resume_vecs, job_vec.reshape(1, -1)).flatten()
    
    # Get filenames
    filenames = [os.path.basename(path) for path in file_paths]
    
    # Find matched keywords
    results = []
    jd_words = set(job_description.lower().split())
    
    for i, (score, resume) in enumerate(zip(similarities, raw_resumes)):
        resume_words = set(resume.lower().split())
        matched_keywords = list(jd_words & resume_words)
        
        results.append({
            "filename": filenames[i],
            "score": float(score),
            "matched_keywords": matched_keywords[:10]  # Top 10 keywords
        })
    
    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return results
