from pydantic import BaseModel
from typing import Optional

class ResumeCreate(BaseModel):
    name: str
    email: str
    skills: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None

class ResumeResponse(ResumeCreate):
    id: int

    class Config:
        orm_mode = True
