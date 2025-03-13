from sqlalchemy.orm import Session
from app.models.resume import Resume
from app.schemas.resume_schema import ResumeCreate
from app.services.ner_service import extract_text_from_file, extract_entities

def create_resume(db: Session, file_path: str):
    """Extract data from a resume file and save it to the database."""
    text = extract_text_from_file(file_path)
    extracted_data = extract_entities(text)

    resume = Resume(
        name=extracted_data["name"],
        email=extracted_data["email"],
        skills=extracted_data["skills"],
        experience=extracted_data["experience"],
        education=extracted_data["education"],
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


def save_parsed_resume(db: Session, resume_dict: dict):
    """Save it in db."""

    resume = Resume(
        name=resume_dict["name"],
        email=resume_dict["email"],
        skills=resume_dict["skills"],
        experience=resume_dict["experience"],
        education=resume_dict["education"],
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


# Job-Skill Mapping
job_skills = {
    "TCS": {"Python", "Java", "C++", "Algorithms", "Data Structures"},
    "Facebook": {"HTML", "CSS", "JavaScript", "React", "Node.js"},
    "MuSigma": {"Python", "SQL", "Excel", "Statistics", "Power BI"},
    "Google": {"Python", "TensorFlow", "Pandas", "Deep Learning"},
}

def get_job_recommendations(db: Session, email: str):
    """Get job recommendations based on user's skills with ranking."""
    user = db.query(Resume).filter(Resume.email == email).first()

    if not user:
        return None

    extracted_skills = set(user.skills.replace("\n", ", ").split(", "))

    # Rank jobs by the number of matched skills
    ranked_jobs = sorted(
        [
            {
                "job": job,
                "matched_skills": list(extracted_skills & required_skills),
                "match_count": len(extracted_skills & required_skills),
            }
            for job, required_skills in job_skills.items()
            if extracted_skills & required_skills  # Only include jobs with matches
        ],
        key=lambda x: x["match_count"],
        reverse=True,  # Sort by highest match count
    )

    # Return only the top 2 results
    return ranked_jobs[:2]