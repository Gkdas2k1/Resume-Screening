# app/models.py

from pydantic import BaseModel, Field
from typing import List, Optional

# --- Request Schemas (What the client sends to the API) ---

class MatchRequest(BaseModel):
    """
    Request body expected by the /match-candidates endpoint.
    Used if you choose to accept JSON instead of Form data.
    """
    job_description: str = Field(
        ..., 
        description="The full text of the job description to match against."
    )
    top_n: Optional[int] = Field(
        5, 
        description="The number of top candidates to return (default is 5)."
    )


# --- Response Schemas (What the API sends back to the client) ---

class CandidateResult(BaseModel):
    """
    Schema for a single ranked candidate.
    This is the core output required by the assignment.
    """
    candidate_id: str = Field(
        ..., 
        description="The filename or unique identifier of the candidate's resume."
    )
    score: float = Field(
        ..., 
        description="The matching similarity score (e.g., 0.85 for 85% match)."
    )
    matched_keywords: List[str] = Field(
        ..., 
        description="A list of key skills or keywords that matched between the resume and the job description."
    )
    
    class Config:
        # This ensures that if you return a dictionary from your endpoint,
        # it will be automatically converted to this schema.
        from_attributes = True


class MatchResponse(BaseModel):
    """
    Schema for the full response of the /match-candidates endpoint.
    """
    top_candidates: List[CandidateResult] = Field(
        ..., 
        description="The ranked list of candidates, sorted from best match to worst."
    )


class UploadResponse(BaseModel):
    """
    Schema for the response of the /upload-resumes endpoint.
    """
    message: str = Field(..., description="Confirmation message for the upload.")
    filenames: List[str] = Field(
        ..., 
        description="List of filenames that were successfully uploaded."
    )


class HealthResponse(BaseModel):
    """
    Schema for the response of the /health endpoint.
    """
    status: str = Field(..., description="Current status of the API (e.g., 'OK').")