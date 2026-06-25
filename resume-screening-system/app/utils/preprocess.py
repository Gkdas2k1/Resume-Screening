import re
import string


def preprocess(text: str) -> str:
    """
    Clean and preprocess text for better matching
    """
    # Lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    
    return text
