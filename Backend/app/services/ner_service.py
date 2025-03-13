import spacy
import re
from typing import Dict
from docx import Document
import pdfplumber

nlp = spacy.load("en_core_web_sm")

def extract_text_from_file(file_path: str) -> str:
    """Extract text from PDF or DOCX files."""
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            return " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return " ".join([para.text for para in doc.paragraphs])
    return ""

def extract_name(text):
    """Extracts the candidate's name using Named Entity Recognition (NER)."""
    text = text.replace("\n", " ")  # Replace newlines with spaces for cleaner parsing
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()  # Return the clean name
    
    return "Not Found"

def extract_email(text):
    """Extracts email addresses using regex."""
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else "Not Found"

def extract_skills(text):
    """Extracts skills from structured or unstructured formats."""
    skills_pattern = r"(?i)(Skills|Technical Skills)\s*[:\n]"
    match = re.search(skills_pattern, text)
    if match:
        start_index = match.end()
        skills_section = text[start_index:].strip()

        # Stop when a new section like "Experience" or "Education" starts
        end_match = re.search(r"(?i)(Experience|Education|Projects|Certifications)\s*[:\n]", skills_section)
        if end_match:
            skills_section = skills_section[:end_match.start()].strip()
        
        skills_list = [line.strip("•- ") for line in skills_section.split("\n") if line.strip()]
        return ", ".join(skills_list) if skills_list else "Not Found"
    
    return "Not Found"

def extract_experience(text):
    """Extracts work experience from resume."""
    exp_pattern = r"(?i)(Experience|Work Experience)\s*[:\n]"
    match = re.search(exp_pattern, text)
    if not match:
        return "Not Found"

    start_index = match.end()
    exp_section = text[start_index:].strip()

    # Stop when a new section starts
    end_match = re.search(r"(?i)(Education|Skills|Projects|Certifications)\s*[:\n]", exp_section)
    if end_match:
        exp_section = exp_section[:end_match.start()].strip()

    experience_list = [line.strip("•- ") for line in exp_section.split("\n") if line.strip()]
    return "\n".join(experience_list) if experience_list else "Not Found"

def extract_education(text):
    """Extracts education details from resume."""
    edu_pattern = r"(?i)(Education|Academic Background)\s*[:\n]"
    match = re.search(edu_pattern, text)
    if not match:
        return "Not Found"

    start_index = match.end()
    edu_section = text[start_index:].strip()

    # Stop when a new section starts
    end_match = re.search(r"(?i)(Experience|Skills|Projects|Certifications)\s*[:\n]", edu_section)
    if end_match:
        edu_section = edu_section[:end_match.start()].strip()

    education_list = [line.strip("•- ") for line in edu_section.split("\n") if line.strip()]
    return "\n".join(education_list) if education_list else "Not Found"

def extract_entities(text: str) -> Dict[str, str]:
    """Extracts all relevant entities from the resume."""
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "education": extract_education(text),
    }
