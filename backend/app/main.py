from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from .parsing import extract_text_from_file
from .analysis import extract_combined_keywords, compare_keywords
from pydantic import BaseModel, Field
from typing import List

class AnalysisResult(BaseModel):
    match_score: int = Field(..., example=75)
    matched_keywords: List[str] = Field(..., example=["python", "fastapi", "aws"])
    missing_keywords: List[str] = Field(..., example=["docker", "kubernetes"])

app = FastAPI(
    title="Resume Analyzer API",
    description="Analyzes resumes against job descriptions.",
    version="0.1.0"
)

@app.post("/analyze/", response_model=AnalysisResult, tags=["Analysis"])
async def analyze_resume_and_jd(
    resume_file: UploadFile = File(..., description="Resume file (PDF or DOCX)"),
    job_description: str = Form(..., description="Job description text")
):
    """
    Analyzes the uploaded resume against the provided job description.

    - Extracts text from the resume file.
    - Extracts keywords from both the resume and job description.
    - Compares keywords and calculates a match score.
    - Returns matched keywords, missing keywords, and the score.
    """
    if not resume_file.filename:
         raise HTTPException(status_code=400, detail="No resume file name found.")

    if not (resume_file.filename.lower().endswith(".pdf") or resume_file.filename.lower().endswith(".docx")):
         raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF or DOCX file.")

    try:
        resume_content = await resume_file.read()
        resume_text = extract_text_from_file(resume_content, resume_file.filename)
        if resume_text is None:
             raise HTTPException(status_code=422, detail=f"Could not parse the resume file: {resume_file.filename}. It might be corrupted, password-protected, or an unsupported format.")
    except Exception as e:
        print(f"Error processing uploaded file {resume_file.filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Server error processing resume file: {e}")
    finally:
        await resume_file.close()

    if not resume_text:
        print(f"Warning: Resume file '{resume_file.filename}' parsed successfully but resulted in empty text.")


    try:
        resume_keywords = extract_combined_keywords(resume_text)
        jd_keywords = extract_combined_keywords(job_description)
    except Exception as e:
        print(f"Error during keyword extraction: {e}")
        raise HTTPException(status_code=500, detail=f"Server error during keyword analysis: {e}")


    try:
        comparison_results = compare_keywords(resume_keywords, jd_keywords)
    except Exception as e:
        print(f"Error during keyword comparison: {e}")
        raise HTTPException(status_code=500, detail=f"Server error during result comparison: {e}")


    return AnalysisResult(**comparison_results)


@app.get("/", tags=["General"])
async def read_root():
    """Root endpoint providing basic API information."""
    return {"message": "Welcome to the Resume Analyzer API. Use the /docs endpoint for details."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)