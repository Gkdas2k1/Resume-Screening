import pdfplumber
import docx
import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    text = ""
    # Try pdfplumber first (good for text-based PDFs)
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    # If empty (scanned), fallback to PyMuPDF or OCR (Optional)
    if not text.strip():
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
    return text

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    else: # .txt
        with open(file_path, 'r') as f:
            return f.read()