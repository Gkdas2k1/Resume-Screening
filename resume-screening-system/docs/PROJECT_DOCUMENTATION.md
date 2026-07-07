# Resume Screening System Documentation

## 1. Project Purpose
The application screens uploaded resumes against a job description and returns the best-matching candidates. It is designed as a lightweight proof-of-concept that combines:

- a FastAPI backend
- a single HTML frontend page
- text extraction for resumes
- basic preprocessing
- TF-IDF vectorization
- cosine-similarity ranking
- keyword overlap for explainability

In simple terms, the system asks:
"Which uploaded resumes are textually closest to this job description?"

## 2. High-Level Architecture
The project has three main layers:

### Backend API
The backend lives in `app/main.py` and exposes the routes used by the frontend and API users.

### Processing Utilities
The utility modules in `app/utils/` do the actual resume-processing work:

- `parser.py` extracts text from files
- `preprocess.py` cleans raw text
- `matcher.py` converts text into vectors
- `explainer.py` computes similarity scores and matched keywords

### Frontend
The frontend is a single static HTML page in `app/static/index.html`. It lets a user:

- upload resumes
- enter a job description
- choose how many top candidates to show
- view ranked results in the browser

## 3. Folder Structure
```text
resume-screening-system/
|-- app/
|   |-- main.py
|   |-- models.py
|   |-- static/
|   |   `-- index.html
|   `-- utils/
|       |-- explainer.py
|       |-- matcher.py
|       |-- parser.py
|       `-- preprocess.py
|-- data/
|   |-- raw_resumes/
|   `-- sample_data/
|-- models/
|   `-- tfidf.pkl
|-- requirements.txt
`-- README.md
```

## 4. How the System Works End to End
The application flow is:

1. A user uploads one or more resumes.
2. The files are saved into `data/raw_resumes/`.
3. The application stores the saved file paths in a global list called `uploaded_files`.
4. The user submits a job description and optionally selects how many top matches to return.
5. Each uploaded resume is read and converted into raw text.
6. The resume text and the job description are cleaned.
7. TF-IDF vectors are created for all resumes plus the job description.
8. Cosine similarity is calculated between each resume vector and the job-description vector.
9. The results are sorted from highest score to lowest score.
10. The API returns the top `N` candidates with filenames, scores, and matched keywords.

## 5. Detailed Code Explanation

### 5.1 `app/main.py`
This is the main application entrypoint.

#### Responsibilities
- creates the FastAPI app
- ensures the upload directory exists
- mounts static files
- serves the main HTML page
- accepts uploaded resumes
- triggers the matching pipeline

#### Important Variables
- `app = FastAPI(...)`
  Creates the API application.

- `UPLOAD_DIR = "data/raw_resumes/"`
  Defines where uploaded resumes are stored.

- `uploaded_files = []`
  Keeps the uploaded file paths in memory for the active server session.

#### Route: `GET /`
This route reads `app/static/index.html` and returns it as HTML.

This is the user-facing page of the application.

#### Route: `GET /health`
Returns:
```json
{"status": "OK"}
```

This is a basic health-check endpoint useful for verifying the API is running.

#### Route: `POST /upload-resumes`
This route:

- accepts multiple uploaded files
- validates MIME type
- saves each file into `data/raw_resumes/`
- stores each path in the `uploaded_files` list
- returns a success message and the filenames

Accepted file types:

- PDF
- DOCX
- TXT

If an unsupported file is uploaded, the route raises HTTP 400.

#### Route: `POST /match-candidates`
This route is the main business workflow.

It:

1. validates that resumes were uploaded first
2. keeps the original job description as `jd_text`
3. preprocesses the job description
4. loops through every uploaded resume
5. extracts raw resume text
6. preprocesses each resume
7. vectorizes resumes and job description
8. ranks candidates
9. returns only the top `N` results

The final response format is:
```json
{
  "top_candidates": [
    {
      "filename": "resume1.pdf",
      "score": 0.73,
      "matched_keywords": ["python", "sql", "api"]
    }
  ]
}
```

### 5.2 `app/utils/parser.py`
This module extracts text from resume files.

#### Function: `extract_text(file_path: str) -> str`
It checks the file extension and uses a different extraction strategy per format:

- `.pdf`
  Uses `pdfplumber` to iterate over pages and combine their extracted text.

- `.txt`
  Opens the text file directly and reads it.

- `.docx`
  Uses `python-docx` to read paragraph text and join it into one string.

- anything else
  Raises `ValueError`

This function is the bridge between uploaded files and the text-processing pipeline.

### 5.3 `app/utils/preprocess.py`
This module performs lightweight text cleaning.

#### Function: `preprocess(text: str) -> str`
It applies three steps:

1. converts text to lowercase
2. removes punctuation
3. collapses extra whitespace

Example:

Input:
```text
Python, SQL, and FastAPI!
```

Output:
```text
python sql and fastapi
```

This improves consistency before vectorization.

### 5.4 `app/utils/matcher.py`
This module turns text into numeric vectors.

#### Function: `vectorize_resumes(resumes, job_description)`
It:

1. combines all resume texts plus the job description into one list
2. creates a `TfidfVectorizer`
3. fits the vectorizer on the combined text set
4. transforms the text into TF-IDF vectors
5. separates the result into:
   - resume vectors
   - one job-description vector

#### Why TF-IDF?
TF-IDF gives more weight to important words and less weight to common words. That makes resume-to-job comparison more useful than plain word counting.

#### Current Vectorizer Settings
- `stop_words="english"`
- `max_features=1000`

That means:

- common English stop words are ignored
- only the top 1000 features are kept

### 5.5 `app/utils/explainer.py`
This module ranks candidates and adds explainability.

#### Function: `rank_candidates(...)`
It:

1. computes cosine similarity between each resume vector and the job-description vector
2. extracts filenames from stored paths
3. builds a set of words from the job description
4. builds a set of words from each raw resume
5. finds overlapping words
6. returns a result object for each resume
7. sorts all results by descending score

Each result contains:

- `filename`
- `score`
- `matched_keywords`

#### Important Detail
The similarity score uses cleaned/vectorized text, but `matched_keywords` are derived from simple word overlap on raw split text. So the explanation logic is simpler than the ranking logic.

### 5.6 `app/static/index.html`
This is the only custom UI page in the project.

It contains:

- page layout and styling
- file upload controls
- job description form fields
- buttons for upload and matching
- JavaScript that calls backend endpoints
- a result area for ranked candidates

The page does not use React, Vue, or a separate CSS/JS build step. Everything is embedded directly in the HTML file.

### 5.7 `app/models.py`
This file defines Pydantic models for:

- request payloads
- candidate results
- upload responses
- health responses

These models describe the intended API schema clearly, but in the current implementation they are not actively attached to the route decorators as `response_model` or request-body models for the live endpoints.

That means the file is useful for documentation and future cleanup, but it is not yet fully wired into runtime validation and OpenAPI output.

## 6. Frontend Pages and Sections

### 6.1 Home Page: `/`
This is the main application page served from `index.html`.

It has three visible sections:

#### Upload Resumes Section
Purpose:
- lets the user select multiple resume files
- sends them to `/upload-resumes`

Main UI elements:
- file input with `multiple`
- upload button
- upload status message area

What happens on click:
- JavaScript creates a `FormData` object
- each selected file is appended using the `files` field name
- a `POST` request is sent to `/upload-resumes`
- success or failure text is shown on the page

#### Job Description Section
Purpose:
- collects the text to compare against resumes
- allows the user to choose how many candidates to return

Main UI elements:
- textarea for the job description
- number input for `top_n`
- "Match Candidates" button

What happens on click:
- JavaScript creates another `FormData`
- the job description is added as `job_description`
- the candidate count is added as `top_n`
- a `POST` request is sent to `/match-candidates`

#### Results Section
Purpose:
- displays ranked candidate results returned by the API

For each candidate, the page shows:
- rank number
- filename
- score as a percentage
- matched keywords

### 6.2 Swagger UI Page: `/docs`
This page is auto-generated by FastAPI.

Purpose:
- lets developers test endpoints in the browser
- shows request fields and response structures
- is useful for debugging without using the custom HTML page

Because the live routes mainly use form fields and manual JSON responses, this page reflects the API behavior but not every schema from `app/models.py`.

### 6.3 ReDoc Page: `/redoc`
This page is also auto-generated by FastAPI.

Purpose:
- provides a more documentation-style API view
- helps readers understand the available routes

It is especially useful for formal API reading, while `/docs` is better for interactive testing.

### 6.4 Static Path: `/static/...`
FastAPI mounts the `app/static` folder at `/static`.

Purpose:
- serves frontend assets
- currently used so the app can expose the HTML file and any future CSS, JS, or image files

In the current project, styling and script logic are embedded inside `index.html`, so `/static` is more of an infrastructure setup for future expansion.

## 7. API Reference

### `GET /health`
Checks whether the backend is running.

Response:
```json
{"status": "OK"}
```

### `POST /upload-resumes`
Uploads resume files.

Input:
- form-data field: `files`

Behavior:
- validates file types
- saves files into `data/raw_resumes/`
- stores saved paths in memory

Response:
```json
{
  "message": "Uploaded 3 files successfully",
  "filenames": ["a.pdf", "b.docx", "c.txt"]
}
```

### `POST /match-candidates`
Ranks uploaded resumes against a job description.

Input:
- form-data field: `job_description`
- form-data field: `top_n`

Behavior:
- preprocesses input text
- extracts resume text
- vectorizes text
- scores and sorts candidates

Response:
```json
{
  "top_candidates": [
    {
      "filename": "resume.pdf",
      "score": 0.8123,
      "matched_keywords": ["python", "ml", "sql"]
    }
  ]
}
```

## 8. Data and State Handling

### Uploaded Files
Uploaded resume paths are stored in the global list:
```python
uploaded_files = []
```

This means:

- the uploaded resume state is kept only in server memory
- if the server restarts, the list resets
- files remain on disk, but the active session list is lost
- all users share the same in-memory list while the app is running

This is acceptable for a demo, but not ideal for production.

### Saved Resume Files
Uploaded files are saved into:
```text
data/raw_resumes/
```

This gives the backend a stable file path for later text extraction.

## 9. Dependencies and Their Role

### Core Web Stack
- `fastapi`
  builds the API

- `uvicorn`
  runs the ASGI server

- `python-multipart`
  enables form-data and file uploads

### Resume Parsing
- `pdfplumber`
  extracts text from PDFs

- `python-docx`
  reads DOCX files

### Matching and Scoring
- `scikit-learn`
  provides TF-IDF vectorization and cosine similarity support

- `numpy`
  supports numerical operations

### Extra Libraries Present
- `spacy`
- `nltk`
- `pandas`
- `pymupdf`

These are listed in `requirements.txt`, but they are not used directly in the currently active code path shown in this project version.

## 10. Current Limitations
The code works as a simple prototype, but there are some important limitations:

### 1. Global In-Memory State
`uploaded_files` is shared globally and is not user-specific.

### 2. No File Deduplication or Cleanup
Uploads are saved directly and remain in `data/raw_resumes/` unless manually removed.

### 3. Basic Preprocessing Only
The current cleaner only lowercases, removes punctuation, and normalizes spaces.

It does not:
- lemmatize words
- normalize synonyms
- remove all noisy artifacts from resumes

### 4. Basic Explainability
`matched_keywords` are based on simple word overlap, not true feature importance.

### 5. Limited Error Feedback in Frontend
The UI shows generic failure messages and does not surface detailed API error text.

### 6. Pydantic Models Not Fully Integrated
`app/models.py` defines useful schemas, but the routes do not yet fully use them in FastAPI decorators.

### 7. Unused Artifact
`models/tfidf.pkl` exists in the repository, but the current runtime code does not load it.

## 11. Suggested Improvements
If this project is extended, the strongest next steps would be:

1. replace global upload state with a database or session-aware design
2. attach `response_model` definitions from `app/models.py` to the routes
3. improve preprocessing with lemmatization, skill normalization, and phrase handling
4. make keyword explanations come from the vectorizer features instead of raw overlap
5. add better frontend error handling
6. add automated tests for upload, parsing, and ranking behavior
7. support resume deletion, reset, and file management
8. separate CSS and JavaScript into dedicated static files

## 12. Running the Project
From the project root:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## 13. Summary
This project is a clean prototype of an AI-assisted resume screener built on classical NLP methods rather than a large language model workflow.

Its core logic is:

1. upload resumes
2. extract text
3. clean text
4. vectorize with TF-IDF
5. score with cosine similarity
6. show ranked results with keyword overlap

That makes it easy to understand, easy to demo, and a good base for future improvements.
