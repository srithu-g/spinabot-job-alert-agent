import PyPDF2
import docx
import io
import re
from typing import Optional

def extract_text_from_pdf(pdf_data: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_file = io.BytesIO(pdf_data)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_from_docx(docx_data: bytes) -> str:
    """Extract text from DOCX file"""
    try:
        docx_file = io.BytesIO(docx_data)
        doc = docx.Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""

def extract_skills_from_resume(resume_text: str) -> list[str]:
    """Extract skills from resume text"""
    # Common technical skills
    common_skills = [
        "python", "javascript", "java", "c++", "c#", "php", "ruby", "go", "rust",
        "html", "css", "react", "angular", "vue", "node.js", "express", "django",
        "flask", "spring", "laravel", "sql", "mysql", "postgresql", "mongodb",
        "redis", "docker", "kubernetes", "aws", "azure", "gcp", "git", "github",
        "jenkins", "ci/cd", "agile", "scrum", "machine learning", "ai", "data science",
        "tableau", "power bi", "excel", "word", "powerpoint", "photoshop", "illustrator",
        "figma", "sketch", "adobe", "salesforce", "hubspot", "marketing", "seo",
        "content writing", "project management", "leadership", "communication",
        "teamwork", "problem solving", "analytical thinking", "research", "analysis"
    ]
    
    # Convert text to lowercase for matching
    text_lower = resume_text.lower()
    
    # Find skills in the resume
    found_skills = []
    for skill in common_skills:
        if skill in text_lower:
            found_skills.append(skill)
    
    return found_skills

def extract_experience_from_resume(resume_text: str) -> str:
    """Extract experience information from resume"""
    # Look for experience-related keywords
    experience_keywords = [
        "experience", "work history", "employment", "career", "professional background",
        "years of experience", "worked at", "employed at", "position at"
    ]
    
    lines = resume_text.split('\n')
    experience_lines = []
    
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in experience_keywords):
            experience_lines.append(line.strip())
    
    return '\n'.join(experience_lines)

def parse_resume(file_data: bytes, filename: str) -> dict:
    """Main function to parse resume and extract information"""
    resume_text = ""
    
    if filename.lower().endswith('.pdf'):
        resume_text = extract_text_from_pdf(file_data)
    elif filename.lower().endswith('.docx'):
        resume_text = extract_text_from_docx(file_data)
    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOCX files.")
    
    if not resume_text:
        raise ValueError("Could not extract text from the uploaded file.")
    
    # Extract information
    skills = extract_skills_from_resume(resume_text)
    experience = extract_experience_from_resume(resume_text)
    
    return {
        "text": resume_text,
        "skills": skills,
        "experience": experience,
        "word_count": len(resume_text.split())
    }
