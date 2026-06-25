from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize globally
vectorizer = TfidfVectorizer()

def vectorize_resumes(resume_texts, job_desc_text):
    # Combine to fit the vectorizer
    all_texts = resume_texts + [job_desc_text]
    vectors = vectorizer.fit_transform(all_texts)
    # Save this vectorizer later via pickle
    return vectors[:-1], vectors[-1]  # Resume vectors, Job vector