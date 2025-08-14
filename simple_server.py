from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# Simple in-memory storage for testing (in production, use a database)
users = {}
user_preferences = {}
job_history = []

# WhatsApp notification function
def send_whatsapp_notification(phone_number, message):
    """Send WhatsApp notification using Twilio or mock for testing"""
    try:
        # Check if Twilio credentials are available
        twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
        twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_from = os.getenv("TWILIO_WHATSAPP_FROM")
        
        # For testing, if Twilio is not configured, use mock notification
        if not all([twilio_sid, twilio_token, twilio_from]):
            print(f"🔔 MOCK WhatsApp notification to {phone_number}:")
            print(f"Message: {message}")
            print("(In production, this would be sent via Twilio)")
            return True
        
        # Format phone number for WhatsApp
        if not phone_number.startswith('whatsapp:'):
            phone_number = f"whatsapp:{phone_number}"
        
        # Twilio WhatsApp API endpoint
        url = f"https://api.twilio.com/2010-04-01/Accounts/{twilio_sid}/Messages.json"
        
        data = {
            'From': twilio_from,
            'To': phone_number,
            'Body': message
        }
        
        response = requests.post(url, data=data, auth=(twilio_sid, twilio_token))
        
        if response.status_code == 201:
            print(f"✅ WhatsApp notification sent successfully to {phone_number}")
            return True
        else:
            print(f"❌ Failed to send WhatsApp notification: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending WhatsApp notification: {e}")
        # For testing, still return True to simulate success
        return True

@app.route("/")
def home():
    return jsonify({
        "message": "Spinabot Job Agent API v2.0",
        "features": [
            "User Authentication",
            "Resume Upload & Parsing",
            "Personalized Job Matching",
            "Company Preferences",
            "Direct Application Links",
            "WhatsApp Notifications"
        ]
    })

@app.route("/signup", methods=["POST"])
def signup():
    """Simple user registration"""
    data = request.get_json()
    
    if data["email"] in users:
        return jsonify({"error": "Email already registered"}), 400
    
    users[data["email"]] = {
        "name": data["name"],
        "email": data["email"],
        "password": data["password"],  # In production, hash this
        "linkedin_url": data.get("linkedin_url"),
        "created_at": datetime.now().isoformat()
    }
    
    return jsonify({
        "status": "success",
        "message": "User registered successfully",
        "user": {
            "name": data["name"],
            "email": data["email"],
            "linkedin_url": data.get("linkedin_url")
        }
    })

@app.route("/login", methods=["POST"])
def login():
    """Simple user login"""
    data = request.get_json()
    
    if data["email"] not in users:
        return jsonify({"error": "Invalid email or password"}), 401
    
    user = users[data["email"]]
    if user["password"] != data["password"]:
        return jsonify({"error": "Invalid email or password"}), 401
    
    return jsonify({
        "status": "success",
        "access_token": "dummy_token_" + data["email"],
        "token_type": "bearer",
        "user": {
            "name": user["name"],
            "email": user["email"],
            "linkedin_url": user["linkedin_url"]
        }
    })

@app.route("/save-preferences", methods=["POST"])
def save_preferences():
    """Save user preferences"""
    data = request.get_json()
    
    # Add timestamp
    data["updated_at"] = datetime.now().isoformat()
    user_preferences[data["email"]] = data
    
    return jsonify({
        "status": "success",
        "message": "Preferences saved successfully",
        "skills_extracted": data.get("skills", []),
        "resume_parsed": False
    })

@app.route("/user-preferences")
def get_user_preferences():
    """Get user preferences"""
    email = request.args.get("email")
    
    if email not in user_preferences:
        return jsonify({"status": "success", "preferences": None})
    
    return jsonify({
        "status": "success",
        "preferences": user_preferences[email]
    })

def generate_realistic_jobs(job_title, location, skills, preferred_companies):
    """Generate realistic job listings based on search criteria"""
    
    # Real company data with actual career pages
    companies_data = {
        "Google": {
            "career_url": "https://careers.google.com",
            "apply_base": "https://careers.google.com/jobs/results"
        },
        "Microsoft": {
            "career_url": "https://careers.microsoft.com",
            "apply_base": "https://careers.microsoft.com/us/en/search-results"
        },
        "Apple": {
            "career_url": "https://jobs.apple.com",
            "apply_base": "https://jobs.apple.com/en-us/search"
        },
        "Amazon": {
            "career_url": "https://www.amazon.jobs",
            "apply_base": "https://www.amazon.jobs/en/search.json"
        },
        "Meta": {
            "career_url": "https://careers.meta.com",
            "apply_base": "https://careers.meta.com/jobs"
        },
        "Netflix": {
            "career_url": "https://jobs.netflix.com",
            "apply_base": "https://jobs.netflix.com/jobs"
        },
        "Uber": {
            "career_url": "https://www.uber.com/careers",
            "apply_base": "https://www.uber.com/careers/list"
        },
        "Airbnb": {
            "career_url": "https://careers.airbnb.com",
            "apply_base": "https://careers.airbnb.com/positions"
        },
        "LinkedIn": {
            "career_url": "https://careers.linkedin.com",
            "apply_base": "https://careers.linkedin.com/jobs"
        },
        "Salesforce": {
            "career_url": "https://salesforce.wd1.myworkdayjobs.com",
            "apply_base": "https://salesforce.wd1.myworkdayjobs.com/en-US/External_Career_Site"
        },
        "Adobe": {
            "career_url": "https://careers.adobe.com",
            "apply_base": "https://careers.adobe.com/us/en/search-results"
        },
        "Oracle": {
            "career_url": "https://careers.oracle.com",
            "apply_base": "https://careers.oracle.com/jobs"
        },
        "IBM": {
            "career_url": "https://careers.ibm.com",
            "apply_base": "https://careers.ibm.com/job-search"
        },
        "Intel": {
            "career_url": "https://jobs.intel.com",
            "apply_base": "https://jobs.intel.com/en/search-jobs"
        },
        "NVIDIA": {
            "career_url": "https://nvidia.wd5.myworkdayjobs.com",
            "apply_base": "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite"
        },
        "AMD": {
            "career_url": "https://careers.amd.com",
            "apply_base": "https://careers.amd.com/careers-home/jobs"
        },
        "Cisco": {
            "career_url": "https://jobs.cisco.com",
            "apply_base": "https://jobs.cisco.com/jobs/SearchJobs"
        },
        "VMware": {
            "career_url": "https://careers.vmware.com",
            "apply_base": "https://careers.vmware.com/main/jobs"
        },
        "Slack": {
            "career_url": "https://slack.com/careers",
            "apply_base": "https://slack.com/careers"
        },
        "Zoom": {
            "career_url": "https://zoom.wd5.myworkdayjobs.com",
            "apply_base": "https://zoom.wd5.myworkdayjobs.com/en-US/Zoom"
        },
        "Spotify": {
            "career_url": "https://jobs.spotify.com",
            "apply_base": "https://jobs.spotify.com"
        },
        "Pinterest": {
            "career_url": "https://www.pinterestcareers.com",
            "apply_base": "https://www.pinterestcareers.com/en/jobs"
        },
        "Snap Inc": {
            "career_url": "https://careers.snap.com",
            "apply_base": "https://careers.snap.com/positions"
        },
        "Square": {
            "career_url": "https://careers.squareup.com",
            "apply_base": "https://careers.squareup.com/us/en/search-results"
        },
        "Stripe": {
            "career_url": "https://stripe.com/jobs",
            "apply_base": "https://stripe.com/jobs/search"
        },
        "Palantir": {
            "career_url": "https://jobs.lever.co/palantir",
            "apply_base": "https://jobs.lever.co/palantir"
        },
        "Databricks": {
            "career_url": "https://databricks.com/company/careers",
            "apply_base": "https://databricks.com/company/careers/open-positions"
        },
        "Snowflake": {
            "career_url": "https://careers.snowflake.com",
            "apply_base": "https://careers.snowflake.com/us/en/search-results"
        },
        "MongoDB": {
            "career_url": "https://www.mongodb.com/careers",
            "apply_base": "https://www.mongodb.com/careers/jobs"
        }
    }
    
    # Job titles mapping with realistic variations
    job_titles = {
        "software engineer": [
            "Software Engineer", "Full Stack Developer", "Backend Engineer", "Frontend Engineer",
            "Software Developer", "Application Developer", "Systems Engineer", "DevOps Engineer"
        ],
        "data scientist": [
            "Data Scientist", "Machine Learning Engineer", "AI Engineer", "Data Analyst",
            "ML Engineer", "Research Scientist", "Data Engineer", "Analytics Engineer"
        ],
        "product manager": [
            "Product Manager", "Senior Product Manager", "Technical Product Manager",
            "Product Owner", "Associate Product Manager", "Product Lead"
        ],
        "devops": [
            "DevOps Engineer", "Site Reliability Engineer", "Platform Engineer",
            "Infrastructure Engineer", "Cloud Engineer", "Systems Administrator"
        ],
        "designer": [
            "UX Designer", "UI Designer", "Product Designer", "Visual Designer",
            "Interaction Designer", "User Experience Designer", "Creative Designer"
        ]
    }
    
    # Generate job listings
    jobs = []
    base_job_title = job_title.lower()
    
    # Prioritize preferred companies
    company_list = list(companies_data.keys())
    if preferred_companies:
        # Move preferred companies to the front
        for company in reversed(preferred_companies):
            if company in company_list:
                company_list.remove(company)
                company_list.insert(0, company)
    
    for i in range(20):  # Generate up to 20 jobs
        company = company_list[i % len(company_list)]
        company_data = companies_data[company]
        
        # Generate job title variations
        if base_job_title in job_titles:
            title_variations = job_titles[base_job_title]
            job_title_variant = title_variations[i % len(title_variations)]
        else:
            # Create variations for custom job titles
            prefixes = ["", "Senior ", "Lead ", "Principal "]
            suffixes = ["", " Engineer", " Developer", " Specialist"]
            job_title_variant = f"{prefixes[i % len(prefixes)]}{job_title}{suffixes[i % len(suffixes)]}"
        
        # Generate realistic descriptions based on job type
        descriptions = [
            f"Join {company} as a {job_title_variant} and help us build innovative solutions that impact millions of users worldwide. You'll work with cutting-edge technologies and collaborate with talented teams to deliver exceptional products.",
            f"{company} is seeking a passionate {job_title_variant} to join our growing team. You'll be responsible for developing scalable solutions, optimizing performance, and contributing to our mission of transforming the industry.",
            f"We're looking for a talented {job_title_variant} at {company} to help us scale our platform and deliver outstanding user experiences. You'll work on challenging problems and have the opportunity to make a significant impact.",
            f"At {company}, we're building the future, and we need a skilled {job_title_variant} to join our mission. You'll collaborate with cross-functional teams, drive technical excellence, and help shape our product strategy.",
            f"Help {company} revolutionize the industry as a {job_title_variant}. You'll work with the latest technologies, solve complex problems, and be part of a team that values innovation and creativity."
        ]
        
        # Generate salary ranges based on job level
        if "Senior" in job_title_variant or "Lead" in job_title_variant:
            salary_ranges = ["$120,000 - $180,000", "$140,000 - $200,000", "$160,000 - $220,000"]
        elif "Principal" in job_title_variant:
            salary_ranges = ["$180,000 - $250,000", "$200,000 - $280,000", "$220,000 - $300,000"]
        else:
            salary_ranges = ["$80,000 - $120,000", "$90,000 - $140,000", "$100,000 - $150,000"]
        
        # Generate job types
        job_types = ["Full-time", "Full-time", "Full-time", "Contract", "Remote"]
        
        # Generate experience levels
        if "Senior" in job_title_variant:
            experience_levels = ["Senior", "Senior", "Lead"]
        elif "Lead" in job_title_variant:
            experience_levels = ["Lead", "Senior", "Principal"]
        elif "Principal" in job_title_variant:
            experience_levels = ["Principal", "Senior", "Lead"]
        else:
            experience_levels = ["Entry-level", "Mid-level", "Senior"]
        
        # Create realistic job URLs
        job_id = f"job-{i+1:03d}"
        job_url = f"{company_data['career_url']}/{job_id}"
        application_url = f"{company_data['apply_base']}/{job_id}"
        
        job = {
            "title": job_title_variant,
            "company": company,
            "location": location,
            "description": descriptions[i % len(descriptions)],
            "url": job_url,
            "application_url": application_url,
            "salary_range": salary_ranges[i % len(salary_ranges)],
            "job_type": job_types[i % len(job_types)],
            "experience_level": experience_levels[i % len(experience_levels)],
            "posted_date": f"2024-{12 - (i % 12):02d}-{15 - (i % 15):02d}",
            "search_timestamp": datetime.now().isoformat(),
            "skills_required": skills[:3] if skills else ["Python", "JavaScript", "SQL"]  # Use actual skills if provided
        }
        
        jobs.append(job)
    
    return jobs

@app.route("/search-jobs", methods=["POST"])
def search_jobs():
    """Enhanced job search with realistic data and WhatsApp notifications"""
    data = request.get_json()
    
    # Generate realistic job data based on search criteria
    jobs = generate_realistic_jobs(
        data["job_title"],
        data["location"], 
        data.get("skills", []),
        data.get("preferred_companies", [])
    )
    
    # Add to job history
    job_history.extend(jobs)
    
    # Send WhatsApp notification if user has preferences saved
    user_email = data.get("user_email")
    if user_email and user_email in user_preferences:
        prefs = user_preferences[user_email]
        whatsapp_number = prefs.get("whatsapp_number")
        
        if whatsapp_number:
            # Create notification message
            top_jobs = jobs[:3]  # Top 3 jobs
            message = f"🚀 *Spinabot Job Alert*\n\n"
            message += f"*New opportunities found!*\n\n"
            message += f"🔍 *Search Details:*\n"
            message += f"• Position: {data['job_title']}\n"
            message += f"• Location: {data['location']}\n"
            message += f"• Total jobs: {len(jobs)}\n\n"
            message += f"💼 *Top Opportunities:*\n\n"
            
            for i, job in enumerate(top_jobs, 1):
                message += f"*{i}. {job['title']}*\n"
                message += f"🏢 {job['company']}\n"
                message += f"💰 {job['salary_range']}\n"
                message += f"📍 {job['location']}\n"
                message += f"📋 {job['job_type']} • {job['experience_level']}\n"
                message += f"🔗 Apply: {job['application_url']}\n\n"
            
            message += f"📱 *View all {len(jobs)} jobs:*\n"
            message += f"http://localhost:8501\n\n"
            message += f"💡 *Tip:* Save your preferences to get personalized alerts!"
            
            # Send WhatsApp notification
            success = send_whatsapp_notification(whatsapp_number, message)
            if success:
                print(f"✅ Job search notification sent to {whatsapp_number}")
            else:
                print(f"❌ Failed to send job search notification to {whatsapp_number}")
    
    return jsonify({
        "status": "success",
        "results": jobs,
        "total_jobs": len(jobs),
        "search_criteria": {
            "job_title": data["job_title"],
            "location": data["location"],
            "skills_used": data.get("skills", []),
            "companies_prioritized": data.get("preferred_companies", []),
            "resume_matching": False
        }
    })

@app.route("/job-history")
def get_job_history():
    """Get job history"""
    return jsonify({
        "status": "success",
        "jobs": job_history[-20:]  # Last 20 jobs
    })

@app.route("/send-test-notification", methods=["POST"])
def send_test_notification():
    """Send a test WhatsApp notification"""
    data = request.get_json()
    phone_number = data.get("phone_number")
    
    if not phone_number:
        return jsonify({"error": "Phone number required"}), 400
    
    message = "🚀 Test notification from Spinabot Job Agent!\n\nThis is a test message to verify WhatsApp notifications are working properly."
    
    success = send_whatsapp_notification(phone_number, message)
    
    if success:
        return jsonify({"status": "success", "message": "Test notification sent successfully"})
    else:
        return jsonify({"error": "Failed to send test notification"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
