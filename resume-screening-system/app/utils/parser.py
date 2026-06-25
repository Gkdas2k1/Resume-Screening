import pdfplumber
import os


def extract_text(file_path: str) -> str:
    """
    Extract text from PDF, DOCX, or TXT file
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    
    elif ext == ".docx":
        try:
            from docx import Document
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except ImportError:
            raise ImportError("python-docx is required for DOCX files. Install it with: pip install python-docx")
    
    else:
        raise ValueError(f"Unsupported file type: {ext}")
