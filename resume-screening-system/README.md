# AI-Powered Resume Screening System

## Overview
This project is a FastAPI-based resume screening application that:

- accepts resume uploads in `PDF`, `DOCX`, and `TXT`
- extracts raw text from each resume
- cleans the text for comparison
- converts resumes and the job description into TF-IDF vectors
- ranks candidates using cosine similarity
- returns matched keywords for a lightweight explanation layer

The project also includes a simple browser UI at `/` and interactive API docs at `/docs`.

## Quick Start
1. Install dependencies:
   `pip install -r requirements.txt`
2. Start the app:
   `uvicorn app.main:app --reload`
3. Open one of these routes:
   `http://127.0.0.1:8000/` for the HTML interface
   `http://127.0.0.1:8000/docs` for Swagger UI

## Main Endpoints
- `GET /` serves the frontend page
- `GET /health` returns a simple health status
- `POST /upload-resumes` stores uploaded resumes for the current running session
- `POST /match-candidates` ranks uploaded resumes against a job description

## Full Documentation
Detailed project documentation is available here:

- [Project Documentation](./docs/PROJECT_DOCUMENTATION.md)

It includes:

- architecture and data flow
- file-by-file code explanation
- API behavior
- frontend page and section explanation
- current limitations and improvement ideas
