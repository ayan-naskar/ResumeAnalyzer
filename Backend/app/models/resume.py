from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    skills = Column(String, nullable=True)
    experience = Column(String, nullable=True)
    education = Column(String, nullable=True)
