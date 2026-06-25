# AI-Powered Resume Screening System

## Project Overview
This system automates resume screening by parsing resumes (PDF/DOCX/TXT), preprocessing text, and ranking candidates against a job description using TF-IDF vectorization and Cosine Similarity. It provides explainable outputs (matched keywords) and exposes functionality via a RESTful API built with FastAPI.

## Setup Instructions
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Download the spaCy model: `python -m spacy download en_core_web_sm`

## Usage Guide
1. Run the API server: `uvicorn app.main:app --reload`
2. Access Swagger UI documentation at: `http://127.0.0.1:8000/docs`
3. **Upload Resumes:** Use the `/upload-resumes` endpoint to upload PDF/DOCX files.
4. **Match Candidates:** Use the `/match-candidates` endpoint to submit a job description and get ranked results with scores and matched keywords.

## API Endpoints
- `GET /health` - Health check.
- `POST /upload-resumes` - Upload multiple resume files.
- `POST /match-candidates` - Rank uploaded resumes against a job description.