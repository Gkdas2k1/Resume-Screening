# app/utils/matcher.py

import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize the vectorizer globally (or inside the function)
def vectorize_resumes(resume_texts, job_desc_text):
    # Combine to fit the vectorizer
    all_texts = resume_texts + [job_desc_text]
    
    # Create and fit the TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(all_texts)
    
    # --- SAVE THE MODEL ARTIFACT (ADD THIS CODE HERE) ---
    # Ensure the 'models/' directory exists
    os.makedirs("models", exist_ok=True)
    
    # Save the fitted vectorizer to a pickle file
    with open("models/tfidf.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    print("TF-IDF Vectorizer saved to models/tfidf.pkl")  # Optional confirmation
    # --- END OF SAVING CODE ---
    
    # Return resume vectors and job vector
    # (The last vector is the job description, the rest are resumes)
    return vectors[:-1], vectors[-1]