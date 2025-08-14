from sqlalchemy import Column, Date, Integer, String, Text, DateTime, LargeBinary
from sqlalchemy.sql import func
from .database import Base
import bcrypt

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    linkedin_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def set_password(self, password: str):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    job_title = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    skills = Column(Text, nullable=False)  # store as comma-separated string
    preferred_companies = Column(Text)  # store as comma-separated string
    whatsapp_number = Column(String(20))
    linkedin_url = Column(String(255))
    email = Column(String(100))
    resume_filename = Column(String(255))
    resume_data = Column(LargeBinary)
    resume_content = Column(Text)  # Extracted text from resume
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class JobListing(Base):
    __tablename__ = "job_listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    company = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    posted_date = Column(Date)
    description = Column(Text)
    url = Column(String(500))
    application_url = Column(String(500))  # Direct application link
    salary_range = Column(String(100))
    job_type = Column(String(50))  # Full-time, Part-time, Contract, etc.
    experience_level = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())