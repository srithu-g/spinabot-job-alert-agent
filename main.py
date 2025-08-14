from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import models, database, auth
from .gemini_client import search_jobs_with_resume
from .resume_parser import parse_resume
from twilio.rest import Client
import re
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import List, Optional

load_dotenv()

# Twilio WhatsApp Config (Sandbox)
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_FROM")

twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_whatsapp_message(to_number: str, body_text: str):
    if not to_number.startswith("whatsapp:"):
        to_number = f"whatsapp:{to_number}"
    message = twilio_client.messages.create(
        body=body_text,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=to_number
    )
    return message.sid

app = FastAPI(title="Spinabot Job Agent API", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

# Pydantic models
class UserSignup(BaseModel):
    name: str
    email: str
    password: str
    linkedin_url: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserPreferences(BaseModel):
    job_title: str
    location: str
    skills: List[str]
    preferred_companies: Optional[List[str]] = None
    whatsapp_number: Optional[str] = None
    linkedin_url: Optional[str] = None
    email: Optional[str] = None

class JobSearchRequest(BaseModel):
    job_title: str
    location: str
    skills: Optional[List[str]] = None
    preferred_companies: Optional[List[str]] = None

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
def signup(user_data: UserSignup, db: Session = Depends(database.get_db)):
    """User registration with secure password storage"""
    try:
        # Check if user already exists
        existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        new_user = models.User(
            name=user_data.name,
            email=user_data.email,
            linkedin_url=user_data.linkedin_url
        )
        new_user.set_password(user_data.password)
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {
            "status": "success",
            "message": "User registered successfully",
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "linkedin_url": new_user.linkedin_url
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/login")
def login(user_data: UserLogin, db: Session = Depends(database.get_db)):
    """User login with JWT token generation"""
    try:
        user = db.query(models.User).filter(models.User.email == user_data.email).first()
        if not user or not user.check_password(user_data.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Generate JWT token
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        return {
            "status": "success",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "linkedin_url": user.linkedin_url
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@app.post("/save-preferences")
async def save_preferences(
    job_title: str = Form(...),
    location: str = Form(...),
    skills: str = Form(...),
    preferred_companies: Optional[str] = Form(None),
    whatsapp_number: Optional[str] = Form(None),
    linkedin_url: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    resume: Optional[UploadFile] = File(None),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """Save user preferences with optional resume upload"""
    try:
        # Parse skills and companies
        skills_list = [s.strip() for s in skills.split(",") if s.strip()]
        companies_list = None
        if preferred_companies:
            companies_list = [c.strip() for c in preferred_companies.split(",") if c.strip()]
        
        # Handle resume upload
        resume_filename = None
        resume_data = None
        resume_content = None
        
        if resume:
            if resume.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
            
            if resume.size > 10 * 1024 * 1024:  # 10MB limit
                raise HTTPException(status_code=400, detail="File size too large. Maximum 10MB allowed")
            
            resume_filename = resume.filename
            resume_data = resume.file.read()
            
            # Parse resume content
            parsed_resume = parse_resume(resume_data, resume_filename)
            resume_content = parsed_resume["text"]
            
            # Update skills with resume-extracted skills
            resume_skills = parsed_resume["skills"]
            skills_list.extend(resume_skills)
            skills_list = list(set(skills_list))  # Remove duplicates
        
        # Check if user already has preferences
        existing_pref = db.query(models.UserPreference).filter(
            models.UserPreference.user_id == current_user.id
        ).first()
        
        if existing_pref:
            # Update existing preferences
            existing_pref.job_title = job_title
            existing_pref.location = location
            existing_pref.skills = ",".join(skills_list)
            existing_pref.preferred_companies = ",".join(companies_list) if companies_list else None
            existing_pref.whatsapp_number = whatsapp_number
            existing_pref.linkedin_url = linkedin_url
            existing_pref.email = email
            if resume_filename:
                existing_pref.resume_filename = resume_filename
                existing_pref.resume_data = resume_data
                existing_pref.resume_content = resume_content
        else:
            # Create new preferences
            new_pref = models.UserPreference(
                user_id=current_user.id,
                job_title=job_title,
                location=location,
                skills=",".join(skills_list),
                preferred_companies=",".join(companies_list) if companies_list else None,
                whatsapp_number=whatsapp_number,
                linkedin_url=linkedin_url,
                email=email,
                resume_filename=resume_filename,
                resume_data=resume_data,
                resume_content=resume_content
            )
            db.add(new_pref)
        
        db.commit()
        
        return {
            "status": "success",
            "message": "Preferences saved successfully",
            "skills_extracted": skills_list,
            "resume_parsed": resume_filename is not None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save preferences: {str(e)}")

@app.get("/user-preferences")
def get_user_preferences(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """Get current user's preferences"""
    try:
        prefs = db.query(models.UserPreference).filter(
            models.UserPreference.user_id == current_user.id
        ).first()
        
        if not prefs:
            return {"status": "success", "preferences": None}
        
        return {
            "status": "success",
            "preferences": {
                "job_title": prefs.job_title,
                "location": prefs.location,
                "skills": prefs.skills.split(",") if prefs.skills else [],
                "preferred_companies": prefs.preferred_companies.split(",") if prefs.preferred_companies else [],
                "whatsapp_number": prefs.whatsapp_number,
                "linkedin_url": prefs.linkedin_url,
                "email": prefs.email,
                "has_resume": prefs.resume_filename is not None
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get preferences: {str(e)}")

@app.post("/search-jobs")
async def search_jobs(
    search_request: JobSearchRequest,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """Enhanced job search with resume matching and company preferences"""
    try:
        # Get user preferences for additional context
        user_prefs = db.query(models.UserPreference).filter(
            models.UserPreference.user_id == current_user.id
        ).first()
        
        # Prepare search parameters
        skills = search_request.skills or []
        preferred_companies = search_request.preferred_companies or []
        resume_content = None
        
        if user_prefs:
            # Use user's saved skills if not provided in request
            if not skills and user_prefs.skills:
                skills = user_prefs.skills.split(",")
            
            # Use user's preferred companies if not provided in request
            if not preferred_companies and user_prefs.preferred_companies:
                preferred_companies = user_prefs.preferred_companies.split(",")
            
            # Use resume content for better matching
            if user_prefs.resume_content:
                resume_content = user_prefs.resume_content
        
        # Search for jobs
        jobs = await run_in_threadpool(
            search_jobs_with_resume,
            job_title=search_request.job_title,
            location=search_request.location,
            skills=skills,
            preferred_companies=preferred_companies,
            resume_content=resume_content
        )
        
        if jobs:
            # Save job listings to database
            for job in jobs:
                posted_date_str = job.get('posted_date')
                posted_date = None
                if posted_date_str:
                    try:
                        posted_date = datetime.strptime(posted_date_str, '%Y-%m-%d').date()
                    except:
                        posted_date = datetime.now().date()
                
                db_job = models.JobListing(
                    title=job['title'],
                    company=job['company'],
                    location=job['location'],
                    posted_date=posted_date,
                    description=job['description'],
                    url=job['url'],
                    application_url=job['application_url'],
                    salary_range=job['salary_range'],
                    job_type=job['job_type'],
                    experience_level=job['experience_level']
                )
                db.add(db_job)
            
            db.commit()
            
            # Send WhatsApp notification if user has preferences
            if user_prefs and user_prefs.whatsapp_number and jobs:
                message_lines = [f"👋 Hello {current_user.name}! Welcome to Spinabot job alerts.\n"]
                message_lines.append(f"We found {len(jobs)} jobs for '{search_request.job_title}' in {search_request.location}:\n")
                
                max_message_length = 1500
                current_length = sum(len(line) for line in message_lines)
                
                for job in jobs[:5]:  # Send first 5 jobs via WhatsApp
                    title = job.get('title', 'No title')
                    company = job.get('company', 'Unknown')
                    location = job.get('location', 'Unknown')
                    description = job.get('description', 'No description provided')
                    url = job.get('application_url') or job.get('url', 'No link available')
                    
                    if len(description) > 100:
                        description = description[:100] + "..."
                    
                    job_text = (
                        f"🔹 {title} at {company}\n"
                        f"📍 Location: {location}\n"
                        f"📝 {description}\n"
                        f"🔗 Apply: {url}\n\n"
                    )
                    
                    if current_length + len(job_text) > max_message_length:
                        message_lines.append("...and more jobs available. Check the app for details.")
                        break
                    
                    message_lines.append(job_text)
                    current_length += len(job_text)
                
                message = "\n".join(message_lines)
                
                try:
                    send_whatsapp_message(user_prefs.whatsapp_number, message)
                except Exception as e:
                    print(f"Failed to send WhatsApp message: {e}")
        
        return {
            "status": "success",
            "results": jobs,
            "total_jobs": len(jobs),
            "search_criteria": {
                "job_title": search_request.job_title,
                "location": search_request.location,
                "skills_used": skills,
                "companies_prioritized": preferred_companies,
                "resume_matching": resume_content is not None
            }
        }
        
    except Exception as e:
        print(f"Error in job search: {e}")
        raise HTTPException(status_code=500, detail=f"Job search failed: {str(e)}")

@app.get("/job-history")
def get_job_history(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """Get user's job search history"""
    try:
        jobs = db.query(models.JobListing).order_by(models.JobListing.created_at.desc()).limit(50).all()
        
        return {
            "status": "success",
            "jobs": [
                {
                    "id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                    "posted_date": job.posted_date.isoformat() if job.posted_date else None,
                    "description": job.description,
                    "url": job.url,
                    "application_url": job.application_url,
                    "salary_range": job.salary_range,
                    "job_type": job.job_type,
                    "experience_level": job.experience_level,
                    "created_at": job.created_at.isoformat()
                }
                for job in jobs
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get job history: {str(e)}")