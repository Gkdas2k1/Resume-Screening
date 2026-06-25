from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
from app.utils.parser import extract_text
from app.utils.preprocess import preprocess
from app.utils.matcher import vectorize, rank_candidates

app = FastAPI(title="AI Resume Screener", version="1.0")

UPLOAD_DIR = "data/raw_resumes/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Store uploaded file paths globally for this session (or use a DB)
uploaded_files = []

@app.get("/health")
async def health():
    return {"status": "OK"}

@app.post("/upload-resumes")
async def upload_resumes(files: List[UploadFile] = File(...)):
    for file in files:
        if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]:
            raise HTTPException(400, "Invalid file type. Only PDF, DOCX, TXT allowed.")
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        uploaded_files.append(file_path)
    return {"message": f"Uploaded {len(files)} files successfully", "filenames": [f.filename for f in files]}

@app.post("/match-candidates")
async def match_candidates(job_description: str = Form(...), top_n: int = Form(5)):
    if not uploaded_files:
        raise HTTPException(400, "No resumes uploaded. Please upload resumes first.")
    
    # 1. Extract and preprocess JDs & Resumes
    jd_text = extract_text_from_text_input(job_description) # keep raw
    cleaned_jd = preprocess(jd_text)
    
    cleaned_resumes = []
    raw_resumes = []
    for path in uploaded_files:
        raw = extract_text(path)
        raw_resumes.append(raw)
        cleaned_resumes.append(preprocess(raw))
    
    # 2. Vectorize (Using TF-IDF or Transformer)
    # For TF-IDF:
    resume_vecs, job_vec = vectorize_resumes(cleaned_resumes, cleaned_jd)
    
    # 3. Rank
    results = rank_candidates(resume_vecs, job_vec, raw_resumes)
    
    # 4. Return top N
    return JSONResponse(content={"top_candidates": results[:top_n]})