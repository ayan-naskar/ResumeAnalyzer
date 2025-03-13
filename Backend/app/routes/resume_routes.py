from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.controllers.resume_controller import create_resume, get_job_recommendations, save_parsed_resume
from app.models.resume import Resume
import shutil
import uuid
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a resume file and process it."""
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume = create_resume(db, file_path)
    return resume


@router.post("/save-resume/")
async def save_resume(data: dict, db: Session = Depends(get_db)):
    """Save the updated resume."""

    new_resume = save_parsed_resume(db, data)
    return {
        "message": "Resume stored successfully",
        "resume_id": new_resume.id
    }


@router.get("/recommend-jobs/{email}")
def recommend_jobs(email: str, db: Session = Depends(get_db)):
    """Returns user's skills"""
    
    email = email.replace("%40", "@")  # Manually convert %40 to @
    recommendations = get_job_recommendations(db, email)

    # print("inside")
    print("Job Recommendations: ", recommendations)
    return {"email": email, "recommended_jobs": recommendations}