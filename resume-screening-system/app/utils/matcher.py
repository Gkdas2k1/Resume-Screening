from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def vectorize_resumes(resumes: list[str], job_description: str):
    """
    Vectorize resumes and job description using TF-IDF
    """
    # Combine job description with resumes for vectorization
    all_texts = resumes + [job_description]
    
    # Initialize TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Split back into resumes and job vector
    resume_vecs = tfidf_matrix[:-1]
    job_vec = tfidf_matrix[-1]
    
    return resume_vecs, job_vec
