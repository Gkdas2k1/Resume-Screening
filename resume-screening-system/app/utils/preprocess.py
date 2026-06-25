import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')

def clean_text(text):
    # Lowercase
    text = text.lower()
    # Remove special characters (keep letters and spaces)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

def preprocess(text):
    # Clean
    text = clean_text(text)
    # Tokenize
    tokens = text.split()
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t not in stop_words]
    # Lemmatize (e.g., "running" -> "run")
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(tokens)  # Return as string for vectorization