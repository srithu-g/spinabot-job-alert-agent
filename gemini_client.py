from google import genai
import json
import re
from typing import List, Dict, Any

client = genai.Client()

def search_jobs_gemini(
    job_title: str, 
    location: str, 
    skills: List[str] = None,
    preferred_companies: List[str] = None,
    resume_content: str = None
) -> str:
    """
    Enhanced job search with resume matching and company preferences
    """
    
    # Build the prompt with all available information
    prompt_parts = [
        f"Find up to 20 job openings for '{job_title}' in '{location}'."
    ]
    
    if skills:
        skills_text = ", ".join(skills)
        prompt_parts.append(f"Focus on jobs that require these skills: {skills_text}")
    
    if preferred_companies:
        companies_text = ", ".join(preferred_companies)
        prompt_parts.append(f"Prioritize these companies: {companies_text}")
    
    if resume_content:
        # Extract key information from resume for better matching
        prompt_parts.append(f"Match jobs based on this resume content: {resume_content[:500]}...")
    
    prompt_parts.extend([
        "Return results as a JSON array with these exact keys:",
        "- title: Job title",
        "- company: Company name", 
        "- location: Job location",
        "- description: Brief job description (max 200 characters)",
        "- url: Direct application URL (not just company homepage)",
        "- application_url: Direct link to apply for the job",
        "- salary_range: Salary range if available",
        "- job_type: Full-time, Part-time, Contract, etc.",
        "- experience_level: Entry, Mid, Senior, etc.",
        "- posted_date: Date in YYYY-MM-DD format"
    ])
    
    prompt_parts.append("Ensure all URLs are direct application links, not just company homepages.")
    prompt_parts.append("If no direct application URL is available, use the job posting URL.")
    
    prompt_text = " ".join(prompt_parts)
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text,
        )
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "[]"

def parse_jobs_response(response_text: str) -> List[Dict[str, Any]]:
    """
    Parse the Gemini response and extract job listings
    """
    try:
        # Try to extract JSON from the response
        json_match = re.search(r"```json(.*?)```", response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1).strip()
        else:
            # If no JSON block, try to find JSON in the response
            json_str = response_text.strip()
            if not json_str.startswith('['):
                # Try to find array in the text
                array_match = re.search(r'\[.*\]', response_text, re.DOTALL)
                if array_match:
                    json_str = array_match.group(0)
        
        jobs = json.loads(json_str)
        if not isinstance(jobs, list):
            jobs = []
        
        # Validate and clean job data
        cleaned_jobs = []
        for job in jobs:
            if isinstance(job, dict):
                cleaned_job = {
                    'title': job.get('title', 'No title'),
                    'company': job.get('company', 'Unknown company'),
                    'location': job.get('location', 'Unknown location'),
                    'description': job.get('description', 'No description'),
                    'url': job.get('url') or job.get('application_url', '#'),
                    'application_url': job.get('application_url') or job.get('url', '#'),
                    'salary_range': job.get('salary_range', 'Not specified'),
                    'job_type': job.get('job_type', 'Not specified'),
                    'experience_level': job.get('experience_level', 'Not specified'),
                    'posted_date': job.get('posted_date', '2024-01-01')
                }
                cleaned_jobs.append(cleaned_job)
        
        return cleaned_jobs[:20]  # Ensure max 20 jobs
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response text: {response_text}")
        return []
    except Exception as e:
        print(f"Error parsing jobs response: {e}")
        return []

def search_jobs_with_resume(
    job_title: str,
    location: str,
    skills: List[str] = None,
    preferred_companies: List[str] = None,
    resume_content: str = None
) -> List[Dict[str, Any]]:
    """
    Main function to search jobs with all parameters
    """
    response = search_jobs_gemini(
        job_title=job_title,
        location=location,
        skills=skills,
        preferred_companies=preferred_companies,
        resume_content=resume_content
    )
    
    return parse_jobs_response(response)
