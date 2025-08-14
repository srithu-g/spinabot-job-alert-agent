from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Spinabot Job Agent API", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory storage for testing
users = {}
user_preferences = {}
job_history = []

class UserSignup(BaseModel):
    name: str
    email: str
    password: str
    linkedin_url: str = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserPreferences(BaseModel):
    job_title: str
    location: str
    skills: list
    preferred_companies: list = []
    whatsapp_number: str = None
    linkedin_url: str = None
    email: str = None

class JobSearchRequest(BaseModel):
    job_title: str
    location: str
    skills: list = []
    preferred_companies: list = []

@app.get("/")
def home():
    return {
        "message": "Spinabot Job Agent API v2.0",
        "features": [
            "User Authentication",
            "Resume Upload & Parsing",
            "Personalized Job Matching",
            "Company Preferences",
            "Direct Application Links",
            "WhatsApp Notifications"
        ]
    }

@app.post("/signup")
def signup(user_data: UserSignup):
    """Simple user registration"""
    if user_data.email in users:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    users[user_data.email] = {
        "name": user_data.name,
        "email": user_data.email,
        "password": user_data.password,  # In production, hash this
        "linkedin_url": user_data.linkedin_url
    }
    
    return {
        "status": "success",
        "message": "User registered successfully",
        "user": {
            "name": user_data.name,
            "email": user_data.email,
            "linkedin_url": user_data.linkedin_url
        }
    }

@app.post("/login")
def login(user_data: UserLogin):
    """Simple user login"""
    if user_data.email not in users:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    user = users[user_data.email]
    if user["password"] != user_data.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return {
        "status": "success",
        "access_token": "dummy_token_" + user_data.email,
        "token_type": "bearer",
        "user": {
            "name": user["name"],
            "email": user["email"],
            "linkedin_url": user["linkedin_url"]
        }
    }

@app.post("/save-preferences")
def save_preferences(prefs: UserPreferences):
    """Save user preferences"""
    user_preferences[prefs.email] = prefs.dict()
    
    return {
        "status": "success",
        "message": "Preferences saved successfully",
        "skills_extracted": prefs.skills,
        "resume_parsed": False
    }

@app.get("/user-preferences")
def get_user_preferences(email: str):
    """Get user preferences"""
    if email not in user_preferences:
        return {"status": "success", "preferences": None}
    
    return {
        "status": "success",
        "preferences": user_preferences[email]
    }

@app.post("/search-jobs")
def search_jobs(search_request: JobSearchRequest):
    """Mock job search"""
    # Mock job data
    mock_jobs = [
        {
            "title": f"{search_request.job_title} Developer",
            "company": "Tech Corp",
            "location": search_request.location,
            "description": f"Looking for a {search_request.job_title} developer in {search_request.location}",
            "url": "https://example.com/job1",
            "application_url": "https://example.com/apply1",
            "salary_range": "$80,000 - $120,000",
            "job_type": "Full-time",
            "experience_level": "Mid-level",
            "posted_date": "2024-01-01"
        },
        {
            "title": f"Senior {search_request.job_title}",
            "company": "Innovation Inc",
            "location": search_request.location,
            "description": f"Senior {search_request.job_title} position available",
            "url": "https://example.com/job2",
            "application_url": "https://example.com/apply2",
            "salary_range": "$100,000 - $150,000",
            "job_type": "Full-time",
            "experience_level": "Senior",
            "posted_date": "2024-01-02"
        }
    ]
    
    # Add to job history
    job_history.extend(mock_jobs)
    
    return {
        "status": "success",
        "results": mock_jobs,
        "total_jobs": len(mock_jobs),
        "search_criteria": {
            "job_title": search_request.job_title,
            "location": search_request.location,
            "skills_used": search_request.skills,
            "companies_prioritized": search_request.preferred_companies,
            "resume_matching": False
        }
    }

@app.get("/job-history")
def get_job_history():
    """Get job history"""
    return {
        "status": "success",
        "jobs": job_history[-20:]  # Last 20 jobs
    }
