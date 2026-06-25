from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def rank_candidates(resume_vectors, job_vector, resume_texts_raw, job_text_raw):
    # Calculate similarity
    similarities = cosine_similarity(resume_vectors, job_vector.reshape(1, -1))
    
    # Create ranked list
    ranked = []
    for idx, score in enumerate(similarities.flatten()):
        # Explainability: Find common keywords
        resume_tokens = set(resume_texts_raw[idx].split())
        jd_tokens = set(job_text_raw.split())
        matched_keywords = list(resume_tokens.intersection(jd_tokens))[:10]
        ranked.append({
            "candidate_id": idx,
            "score": round(float(score) * 100, 2),
            "matched_keywords": matched_keywords
        })
    
    # Sort descending by score
    ranked = sorted(ranked, key=lambda x: x['score'], reverse=True)
    return ranked