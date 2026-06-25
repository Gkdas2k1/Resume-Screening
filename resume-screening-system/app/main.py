from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Request
import os
import shutil
from typing import List
from app.utils.parser import extract_text
from app.utils.preprocess import preprocess
from app.utils.matcher import vectorize_resumes
from app.utils.explainer import rank_candidates

app = FastAPI(title="AI Resume Screener", version="1.0")

UPLOAD_DIR = "data/raw_resumes/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Store uploaded file paths globally for this session
uploaded_files = []

# --- NEW: Mount static folder and serve the HTML UI --- 
# Make sure the "static" folder exists inside your "app" directory 
app.mount("/static", StaticFiles(directory="app/static"), name="static") 

@app.get("/", response_class=HTMLResponse) 
async def serve_ui(): 
    # Serves the HTML file from the static folder 
    with open("app/static/index.html", "r", encoding="utf-8") as f: 
        return f.read() 

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
    
    # 1. Keep raw JD and cleaned JD
    jd_text = job_description  # FIXED: removed undefined function
    cleaned_jd = preprocess(jd_text)
    
    cleaned_resumes = []
    raw_resumes = []
    for path in uploaded_files:
        raw = extract_text(path)
        raw_resumes.append(raw)
        cleaned_resumes.append(preprocess(raw))
    
    # 2. Vectorize
    resume_vecs, job_vec = vectorize_resumes(cleaned_resumes, cleaned_jd)
    
    # 3. Rank - passing jd_text and uploaded_files as arguments
    results = rank_candidates(resume_vecs, job_vec, raw_resumes, jd_text, uploaded_files)
    
    # 4. Return top N
    return JSONResponse(content={"top_candidates": results[:top_n]})
    # Clear