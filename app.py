import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie
import base64
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Spinabot Job Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark purple/black theme
st.markdown("""
<style>
    /* Dark purple/black theme */
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2d1b69 0%, #1a1a2e 100%);
    }
    
    /* Card styling */
    .card {
        background: linear-gradient(135deg, #2d1b69 0%, #1a1a2e 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin: 1rem 0;
        border: 1px solid #4a4a6a;
        color: white;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6);
        background: linear-gradient(135deg, #a855f7 0%, #9333ea 100%);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: #2d1b69;
        border-radius: 10px;
        border: 2px solid #4a4a6a;
        padding: 0.75rem;
        transition: all 0.3s ease;
        color: white;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #8b5cf6;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
        background: #3d2b79;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #a0a0a0;
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        background: #2d1b69;
        border-radius: 10px;
        border: 2px solid #4a4a6a;
        padding: 0.75rem;
        color: white;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #a0a0a0;
    }
    
    /* Job card styling */
    .job-card {
        background: linear-gradient(135deg, #2d1b69 0%, #1a1a2e 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin: 1rem 0;
        border-left: 4px solid #8b5cf6;
        transition: all 0.3s ease;
        color: white;
    }
    
    .job-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        border-left-color: #a855f7;
    }
    
    .job-title {
        color: #f8fafc;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .job-company {
        color: #8b5cf6;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .job-location {
        color: #cbd5e1;
        font-size: 0.9rem;
    }
    
    .job-description {
        color: #e2e8f0;
        margin: 1rem 0;
        line-height: 1.6;
    }
    
    .job-meta {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    
    .job-meta-item {
        background: #4a4a6a;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        color: #e2e8f0;
    }
    
    .apply-button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        text-decoration: none;
        display: inline-block;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
    }
    
    .apply-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
        background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
    }
    
    /* Header styling */
    .header {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, #2d1b69 0%, #1a1a2e 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        border: 1px solid #4a4a6a;
    }
    
    .header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: #f8fafc;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .header p {
        font-size: 1.2rem;
        opacity: 0.9;
        color: #e2e8f0;
    }
    
    /* Feature grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .feature-item {
        background: linear-gradient(135deg, #2d1b69 0%, #1a1a2e 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        border: 1px solid #4a4a6a;
        color: white;
    }
    
    .feature-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        border-color: #8b5cf6;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Success/Error messages */
    .success-message {
        background: #065f46;
        color: #d1fae5;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #10b981;
    }
    
    .error-message {
        background: #7f1d1d;
        color: #fecaca;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ef4444;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #2d1b69;
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #1a1a2e;
        border-radius: 8px;
        color: #e2e8f0;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: #8b5cf6;
        color: white;
    }
    
    /* Form styling */
    .stForm {
        background: linear-gradient(135deg, #2d1b69 0%, #1a1a2e 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #4a4a6a;
    }
    
    /* Label styling */
    .stTextInput > label, .stTextArea > label {
        color: #e2e8f0 !important;
        font-weight: 600;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: #2d1b69;
        border: 2px solid #4a4a6a;
        border-radius: 10px;
        color: white;
    }
    
    /* Info box styling */
    .stAlert {
        background: #2d1b69;
        border: 1px solid #4a4a6a;
        color: #e2e8f0;
    }
    
    /* Landing page content styling */
    .landing-content {
        color: #e2e8f0;
        font-size: 1.1rem;
        line-height: 1.8;
        margin: 2rem 0;
    }
    
    .landing-content h2 {
        color: #f8fafc;
        margin-bottom: 1.5rem;
        font-size: 2rem;
    }
    
    .landing-content p {
        margin-bottom: 1.5rem;
    }
    </style>

<script>
// Prevent Enter key from submitting forms
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                return false;
            }
        });
    });
    
    // Also prevent Enter on input fields
    const inputs = document.querySelectorAll('input, textarea');
    inputs.forEach(function(input) {
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                return false;
            }
        });
    });
});
</script>
""", unsafe_allow_html=True)

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'landing'

def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

def make_api_request(endpoint, method='GET', data=None):
    """Make API requests to Flask backend"""
    url = f"http://127.0.0.1:8000{endpoint}"
    
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data)
        
        return response
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None

def landing_page():
    """Professional landing page"""
    st.markdown("""
        <div class="header">
            <h1>🚀 Spinabot Job Agent</h1>
            <p>AI-Powered Job Matching & Career Assistant</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Hero section with animation
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
            <div class="landing-content">
                <h2>Find Your Dream Job with AI</h2>
                <p>
                    Spinabot Job Agent revolutionizes your job search experience with cutting-edge AI technology. 
                    Our intelligent platform analyzes your resume, understands your career goals, and matches you 
                    with the perfect job opportunities from top companies worldwide.
                </p>
                <p>
                    With advanced machine learning algorithms, we parse your resume to extract key skills and 
                    experience, then use this information to find jobs that truly match your profile. Our 
                    personalized recommendations save you hours of searching and help you discover opportunities 
                    you might have missed.
                </p>
                <p>
                    Set your preferred companies, locations, and salary expectations, and let our AI do the 
                    heavy lifting. Get direct application links, real-time job alerts via WhatsApp, and 
                    comprehensive job details to make informed decisions about your next career move.
                </p>
            </div>
    """, unsafe_allow_html=True)

        if st.button("Get Started", key="landing_cta"):
            st.session_state.current_page = 'signup'
            st.rerun()

    with col2:
    lottie_job = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json")
        if lottie_job:
            st_lottie(lottie_job, height=400, key="hero_animation")
    
    # Features section
    st.markdown("""
        <div class="feature-grid">
            <div class="feature-item">
                <div class="feature-icon">🤖</div>
                <h3>AI-Powered Matching</h3>
                <p>Advanced algorithms analyze your resume and preferences to find the perfect job matches.</p>
            </div>
            <div class="feature-item">
                <div class="feature-icon">📄</div>
                <h3>Resume Parsing</h3>
                <p>Automatically extract skills and experience from your resume for better job matching.</p>
            </div>
            <div class="feature-item">
                <div class="feature-icon">🏢</div>
                <h3>Company Preferences</h3>
                <p>Specify your preferred companies and get prioritized job recommendations.</p>
            </div>
            <div class="feature-item">
                <div class="feature-icon">🔗</div>
                <h3>Direct Applications</h3>
                <p>Get direct links to job applications, not just company homepages.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def signup_page():
    """User registration page"""
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #f8fafc;">Create Your Account</h1>
            <p style="color: #e2e8f0;">Join Spinabot Job Agent and start your journey to your dream job</p>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        with st.form("signup_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name *", placeholder="Enter your full name")
                email = st.text_input("Email Address *", placeholder="Enter your email")
            
            with col2:
                password = st.text_input("Password *", type="password", placeholder="Create a strong password")
                linkedin = st.text_input("LinkedIn Profile (Optional)", placeholder="https://linkedin.com/in/yourprofile")
            
            submitted = st.form_submit_button("Create Account", use_container_width=True)
            
            if submitted:
                # Validate all required fields
                if not name or not email or not password:
                    st.error("Please fill in all required fields marked with *")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long")
                elif '@' not in email:
                    st.error("Please enter a valid email address")
            else:
                    data = {
                        "name": name,
                        "email": email,
                        "password": password,
                        "linkedin_url": linkedin if linkedin else None
                    }
                    
                    response = make_api_request("/signup", method='POST', data=data)
                    
                    if response and response.status_code == 200:
                        st.success("Account created successfully! Please login.")
                        st.session_state.current_page = 'login'
                        st.rerun()
                    else:
                        error_msg = "Signup failed"
                        if response:
                            try:
                                error_data = response.json()
                                error_msg = error_data.get('error', error_msg)
                            except:
                                pass
                        st.error(error_msg)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("Already have an account? Login", key="signup_to_login"):
            st.session_state.current_page = 'login'
            st.rerun()

def login_page():
    """User login page"""
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #f8fafc;">Welcome Back</h1>
            <p style="color: #e2e8f0;">Login to access your personalized job recommendations</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Email Address", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                if not email or not password:
                    st.error("Please fill in all fields")
            else:
                    data = {"email": email, "password": password}
                    response = make_api_request("/login", method='POST', data=data)
                    
                    if response and response.status_code == 200:
                        result = response.json()
                        st.session_state.authenticated = True
                        st.session_state.user = result['user']
                        st.session_state.current_page = 'dashboard'
                        st.success("Login successful!")
                        st.rerun()
    else:
                        error_msg = "Login failed"
                        if response:
                            try:
                                error_data = response.json()
                                error_msg = error_data.get('error', error_msg)
                            except:
                                pass
                        st.error(error_msg)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("Don't have an account? Sign up", key="login_to_signup"):
            st.session_state.current_page = 'signup'
            st.rerun()

def dashboard_page():
    """Main dashboard with job search and preferences"""
    if not st.session_state.authenticated:
        st.error("Please login to access the dashboard")
        st.session_state.current_page = 'login'
        st.rerun()
        return
    
    # Header with user info
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #2d1b69 0%, #1a1a2e 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.3); border: 1px solid #4a4a6a;">
            <h2 style="color: #f8fafc; margin-bottom: 0.5rem;">Welcome back, {st.session_state.user['name']}! 👋</h2>
            <p style="color: #e2e8f0; margin: 0;">Ready to find your next opportunity?</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["🎯 Job Search", "⚙️ Preferences", "📊 Job History"])
    
    with tab1:
        job_search_section()
    
    with tab2:
        preferences_section()
    
    with tab3:
        job_history_section()
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.current_page = 'landing'
        st.rerun()

def job_search_section():
    """Job search functionality"""
    st.markdown("""
        <h3 style="color: #f8fafc; margin-bottom: 1rem;">🔍 Search for Jobs</h3>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        with st.form("job_search_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
            
        with col1:
                job_title = st.text_input("Job Title *", placeholder="e.g., Software Engineer, Data Scientist")
                location = st.text_input("Location *", placeholder="e.g., New York, Remote, San Francisco")
            
        with col2:
                skills = st.text_area("Skills (Optional)", placeholder="e.g., Python, React, Machine Learning")
                companies = st.text_area("Preferred Companies (Optional)", placeholder="e.g., Google, Microsoft, Apple")
            
            submitted = st.form_submit_button("Search Jobs", use_container_width=True)
            
            if submitted:
                if not job_title or not location:
                    st.error("Please provide job title and location")
                else:
                    with st.spinner("Searching for jobs..."):
            data = {
                "job_title": job_title,
                "location": location,
                            "skills": [s.strip() for s in skills.split(",")] if skills else [],
                            "preferred_companies": [c.strip() for c in companies.split(",")] if companies else [],
                            "user_email": st.session_state.user['email']  # Add user email for notifications
                        }
                        
                        response = make_api_request("/search-jobs", method='POST', data=data)
                        
                        if response and response.status_code == 200:
                            result = response.json()
                            jobs = result.get('results', [])
                            
                            if jobs:
                                st.success(f"Found {len(jobs)} jobs!")
                                display_jobs(jobs)
                else:
                                st.info("No jobs found. Try adjusting your search criteria.")
                else:
                            st.error("Failed to search jobs. Please try again.")
        
        st.markdown('</div>', unsafe_allow_html=True)

def preferences_section():
    """User preferences management"""
    st.markdown("""
        <h3 style="color: #f8fafc; margin-bottom: 1rem;">⚙️ Manage Your Preferences</h3>
    """, unsafe_allow_html=True)
    
    # Load existing preferences
    response = make_api_request(f"/user-preferences?email={st.session_state.user['email']}")
    existing_prefs = None
    if response and response.status_code == 200:
        existing_prefs = response.json().get('preferences')
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        with st.form("preferences_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            
            with col1:
                job_title = st.text_input(
                    "Preferred Job Title", 
                    value=existing_prefs.get('job_title', '') if existing_prefs else '',
                    placeholder="e.g., Software Engineer"
                )
                location = st.text_input(
                    "Preferred Location", 
                    value=existing_prefs.get('location', '') if existing_prefs else '',
                    placeholder="e.g., New York, Remote"
                )
                skills = st.text_area(
                    "Skills", 
                    value=", ".join(existing_prefs.get('skills', [])) if existing_prefs else '',
                    placeholder="e.g., Python, React, Machine Learning"
                )
                companies = st.text_area(
                    "Preferred Companies", 
                    value=", ".join(existing_prefs.get('preferred_companies', [])) if existing_prefs else '',
                    placeholder="e.g., Google, Microsoft, Apple"
                )
            
            with col2:
                whatsapp = st.text_input(
                    "WhatsApp Number (with country code)", 
                    value=existing_prefs.get('whatsapp_number', '') if existing_prefs else '',
                    placeholder="e.g., +1234567890"
                )
                linkedin = st.text_input(
                    "LinkedIn Profile", 
                    value=existing_prefs.get('linkedin_url', '') if existing_prefs else '',
                    placeholder="https://linkedin.com/in/yourprofile"
                )
                email = st.text_input(
                    "Email", 
                    value=existing_prefs.get('email', '') if existing_prefs else '',
                    placeholder="your.email@example.com"
                )
                resume_file = st.file_uploader(
                    "Upload Resume (PDF/DOCX)", 
                    type=["pdf", "docx"],
                    help="Upload your resume for better job matching"
                )
            
            submitted = st.form_submit_button("Save Preferences", use_container_width=True)
            
            if submitted:
                if not job_title or not location or not skills:
                    st.error("Please fill in job title, location, and skills")
                else:
                    with st.spinner("Saving preferences..."):
            data = {
                "job_title": job_title,
                "location": location,
                            "skills": [s.strip() for s in skills.split(",") if s.strip()],
                            "preferred_companies": [c.strip() for c in companies.split(",") if c.strip()],
                            "whatsapp_number": whatsapp,
                            "linkedin_url": linkedin,
                "email": email
            }
                        
                        response = make_api_request("/save-preferences", method='POST', data=data)
                        
                        if response and response.status_code == 200:
                            result = response.json()
                            st.success("Preferences saved successfully!")
                            if result.get('resume_parsed'):
                                st.info("Resume uploaded and parsed successfully!")
                        else:
                            st.error("Failed to save preferences. Please try again.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Test WhatsApp notification section
        if existing_prefs and existing_prefs.get('whatsapp_number'):
            st.markdown("""
                <h4 style="color: #f8fafc; margin: 2rem 0 1rem 0;">📱 Test WhatsApp Notifications</h4>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            st.info(f"Test WhatsApp notifications will be sent to: {existing_prefs.get('whatsapp_number')}")
            
            if st.button("Send Test Notification", key="test_notification"):
                with st.spinner("Sending test notification..."):
                    data = {"phone_number": existing_prefs.get('whatsapp_number')}
                    response = make_api_request("/send-test-notification", method='POST', data=data)
                    
                    if response and response.status_code == 200:
                        st.success("Test notification sent successfully! Check your WhatsApp.")
                    else:
                        st.error("Failed to send test notification. Please check your WhatsApp number and try again.")
            
            st.markdown('</div>', unsafe_allow_html=True)

def job_history_section():
    """Display job search history"""
    st.markdown("""
        <h3 style="color: #f8fafc; margin-bottom: 1rem;">📊 Recent Job Searches</h3>
    """, unsafe_allow_html=True)
    
    response = make_api_request("/job-history")
    
    if response and response.status_code == 200:
        jobs = response.json().get('jobs', [])
        
                    if jobs:
            st.info(f"Showing {len(jobs)} recent job listings")
            display_jobs(jobs, show_meta=True)
                    else:
            st.info("No job history found. Start searching for jobs to see your history here.")
                else:
        st.error("Failed to load job history")

def display_jobs(jobs, show_meta=False):
    """Display job listings in a modern card format"""
    for i, job in enumerate(jobs):
        # Create job card with proper content (no HTML tags)
        job_title = job.get('title', 'No title')
        company = job.get('company', 'Unknown company')
        location = job.get('location', 'Unknown location')
        description = job.get('description', 'No description provided')
        salary = job.get('salary_range', 'Not specified')
        job_type = job.get('job_type', 'Not specified')
        experience = job.get('experience_level', 'Not specified')
        posted_date = job.get('posted_date', 'Not specified')
        application_url = job.get('application_url') or job.get('url', '#')
        
        # Use st.container for better control
        with st.container():
            st.markdown(f"""
                <div class="job-card">
                    <div class="job-title">{job_title}</div>
                    <div class="job-company">{company}</div>
                    <div class="job-location">📍 {location}</div>
                    
                    <div class="job-description">{description}</div>
                    
                    {f'''
                    <div class="job-meta">
                        <span class="job-meta-item">💰 {salary}</span>
                        <span class="job-meta-item">📋 {job_type}</span>
                        <span class="job-meta-item">👤 {experience}</span>
                        {f'<span class="job-meta-item">📅 {posted_date}</span>' if show_meta else ''}
                    </div>
                    ''' if show_meta else ''}
                    
                    <a href="{application_url}" target="_blank" class="apply-button">
                        Apply Now
                    </a>
                </div>
            """, unsafe_allow_html=True)
            
            # Add some spacing between job cards
            st.markdown("<br>", unsafe_allow_html=True)

# Main app logic
def main():
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2 style="color: #f8fafc;">🚀 Spinabot</h2>
                <p style="color: #e2e8f0; font-size: 0.9rem;">Job Agent</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.authenticated:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #2d1b69 0%, #1a1a2e 100%); padding: 1rem; border-radius: 10px; margin-bottom: 1rem; border: 1px solid #4a4a6a;">
                    <p style="margin: 0; font-weight: 600; color: #f8fafc;">{st.session_state.user['name']}</p>
                    <p style="margin: 0; font-size: 0.9rem; color: #e2e8f0;">{st.session_state.user['email']}</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Page routing
    if st.session_state.current_page == 'landing':
        landing_page()
    elif st.session_state.current_page == 'signup':
        signup_page()
    elif st.session_state.current_page == 'login':
        login_page()
    elif st.session_state.current_page == 'dashboard':
        dashboard_page()

if __name__ == "__main__":
    main()
