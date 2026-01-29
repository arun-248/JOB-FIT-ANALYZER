"""
FastAPI Backend - REST API for candidate analysis
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
from pathlib import Path
import tempfile
import os

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.pipeline import CandidateIntelligencePipeline

# Initialize FastAPI app
app = FastAPI(
    title="Job Fit Analyzer API",
    description="AI-powered candidate intelligence system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline
pipeline = CandidateIntelligencePipeline()


# Response models
class AnalysisResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Job Fit Analyzer API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_candidate(
    resume: UploadFile = File(...),
    job_description: UploadFile = File(...)
):
    """
    Analyze candidate resume against job description
    
    Args:
        resume: Resume file (PDF or TXT)
        job_description: Job description file (PDF or TXT)
        
    Returns:
        Complete analysis report
    """
    # Validate file types
    allowed_extensions = ['.pdf', '.txt']
    
    resume_ext = Path(resume.filename).suffix.lower()
    jd_ext = Path(job_description.filename).suffix.lower()
    
    if resume_ext not in allowed_extensions or jd_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Only PDF and TXT files are supported. Got: {resume_ext}, {jd_ext}"
        )
    
    # Create temporary files
    temp_dir = tempfile.gettempdir()
    
    try:
        # Save uploaded files temporarily
        resume_path = Path(temp_dir) / f"resume_{os.getpid()}{resume_ext}"
        jd_path = Path(temp_dir) / f"jd_{os.getpid()}{jd_ext}"
        
        # Write files
        with open(resume_path, 'wb') as f:
            f.write(await resume.read())
        
        with open(jd_path, 'wb') as f:
            f.write(await job_description.read())
        
        # Run analysis
        print(f"📄 Analyzing: {resume.filename} vs {job_description.filename}")
        report = pipeline.analyze(resume_path, jd_path)
        
        # Clean up temp files
        resume_path.unlink()
        jd_path.unlink()
        
        return AnalysisResponse(
            success=True,
            message="Analysis completed successfully",
            data=report
        )
    
    except Exception as e:
        # Clean up on error
        if resume_path.exists():
            resume_path.unlink()
        if jd_path.exists():
            jd_path.unlink()
        
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.post("/analyze/batch")
async def analyze_batch(
    resumes: list[UploadFile] = File(...),
    job_description: UploadFile = File(...)
):
    """
    Batch analyze multiple resumes against one job description
    
    Args:
        resumes: List of resume files
        job_description: Job description file
        
    Returns:
        List of analysis reports
    """
    results = []
    
    # Save JD temporarily
    temp_dir = tempfile.gettempdir()
    jd_path = Path(temp_dir) / f"jd_batch_{os.getpid()}.txt"
    
    with open(jd_path, 'wb') as f:
        f.write(await job_description.read())
    
    # Process each resume
    for resume in resumes:
        try:
            resume_path = Path(temp_dir) / f"resume_{os.getpid()}_{resume.filename}"
            
            with open(resume_path, 'wb') as f:
                f.write(await resume.read())
            
            report = pipeline.analyze(resume_path, jd_path)
            
            results.append({
                "filename": resume.filename,
                "success": True,
                "report": report
            })
            
            resume_path.unlink()
        
        except Exception as e:
            results.append({
                "filename": resume.filename,
                "success": False,
                "error": str(e)
            })
    
    # Clean up JD
    jd_path.unlink()
    
    return {
        "success": True,
        "message": f"Processed {len(resumes)} resumes",
        "results": results
    }


# Run with: uvicorn api.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)