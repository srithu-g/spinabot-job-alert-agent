# 🚀 Spinabot Job Agent

An AI-powered job matching and career assistant that helps you find your dream job with personalized recommendations, resume parsing, and direct application links.

## ✨ Features

### 🔐 Authentication & Security
- **Secure User Registration & Login**: JWT-based authentication with bcrypt password hashing
- **User Profiles**: Personalized dashboards with saved preferences
- **Session Management**: Secure token-based sessions

### 🎯 Smart Job Matching
- **AI-Powered Recommendations**: Uses Google Gemini AI for intelligent job matching
- **Resume Parsing**: Automatically extracts skills and experience from PDF/DOCX resumes
- **Company Preferences**: Specify preferred companies for prioritized recommendations
- **Skill-Based Matching**: Advanced algorithms match your skills with job requirements

### 📄 Resume Management
- **Multi-Format Support**: Upload PDF and DOCX resumes
- **Automatic Skill Extraction**: AI extracts relevant skills from your resume
- **Content Analysis**: Parses experience and qualifications for better matching

### 🔗 Direct Application Links
- **Real Application URLs**: Direct links to job application pages (not just company homepages)
- **Up to 20 Job Results**: Comprehensive job listings with detailed information
- **Job Metadata**: Salary ranges, job types, experience levels, and posting dates

### 📱 Notifications
- **WhatsApp Integration**: Receive job alerts via WhatsApp
- **Real-time Updates**: Instant notifications for new job matches

### 🎨 Modern UI/UX
- **Professional Landing Page**: Beautiful, responsive design
- **Intuitive Navigation**: Easy-to-use interface with tabbed sections
- **Mobile-Friendly**: Responsive design works on all devices

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Robust, open-source database
- **Alembic**: Database migration tool
- **JWT**: JSON Web Tokens for authentication
- **bcrypt**: Secure password hashing

### AI & ML
- **Google Gemini AI**: Advanced language model for job matching
- **Resume Parsing**: Custom algorithms for skill extraction

### Frontend
- **Streamlit**: Rapid web app development framework
- **Modern CSS**: Beautiful, responsive design
- **Lottie Animations**: Engaging user experience

### External Services
- **Twilio**: WhatsApp messaging integration
- **Google Cloud**: Gemini AI API

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Google Gemini API key
- Twilio account (for WhatsApp notifications)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd job-alert-agent_backup
```

### 2. Run Setup Script
```bash
python setup.py
```

### 3. Configure Environment
Copy the example environment file and update with your credentials:
```bash
cp env.example .env
```

Update the `.env` file with your actual values:
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/job_agent_db

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+1234567890

# Google Gemini API
GOOGLE_API_KEY=your_google_gemini_api_key
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Setup Database
```bash
# Run database migrations
alembic upgrade head
```

### 6. Start the Application

#### Backend (Terminal 1)
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend (Terminal 2)
```bash
cd frontend
streamlit run app.py
```

### 7. Access the Application
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📖 Usage Guide

### 1. User Registration
1. Visit the landing page
2. Click "Get Started" to create an account
3. Fill in your details including LinkedIn profile
4. Verify your email and complete registration

### 2. Profile Setup
1. Login to your account
2. Navigate to the "Preferences" tab
3. Upload your resume (PDF/DOCX)
4. Set your job preferences:
   - Preferred job title
   - Location preferences
   - Skills (auto-extracted from resume)
   - Preferred companies
   - Contact information

### 3. Job Search
1. Go to the "Job Search" tab
2. Enter your search criteria
3. Click "Search Jobs"
4. Browse through up to 20 personalized job recommendations
5. Click "Apply Now" for direct application links

### 4. Job History
- View your recent job searches in the "Job History" tab
- Track applications and saved positions
- Monitor your job search activity

## 🔧 API Endpoints

### Authentication
- `POST /signup` - User registration
- `POST /login` - User login

### User Preferences
- `POST /save-preferences` - Save user preferences and resume
- `GET /user-preferences` - Get user preferences

### Job Search
- `POST /search-jobs` - Search for jobs with AI matching
- `GET /job-history` - Get job search history

## 🗄️ Database Schema

### Users Table
- `id`: Primary key
- `name`: User's full name
- `email`: Unique email address
- `password_hash`: Hashed password
- `linkedin_url`: LinkedIn profile URL
- `created_at`, `updated_at`: Timestamps

### User Preferences Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `job_title`: Preferred job title
- `location`: Preferred location
- `skills`: Comma-separated skills
- `preferred_companies`: Comma-separated companies
- `whatsapp_number`: WhatsApp contact
- `linkedin_url`, `email`: Contact information
- `resume_filename`, `resume_data`, `resume_content`: Resume storage
- `created_at`, `updated_at`: Timestamps

### Job Listings Table
- `id`: Primary key
- `title`: Job title
- `company`: Company name
- `location`: Job location
- `posted_date`: Job posting date
- `description`: Job description
- `url`: Job posting URL
- `application_url`: Direct application URL
- `salary_range`: Salary information
- `job_type`: Full-time, Part-time, etc.
- `experience_level`: Entry, Mid, Senior
- `created_at`: Record creation timestamp

## 🔒 Security Features

- **Password Hashing**: bcrypt for secure password storage
- **JWT Tokens**: Secure session management
- **Input Validation**: Comprehensive data validation
- **CORS Protection**: Cross-origin request security
- **File Upload Security**: File type and size validation

## 🧪 Testing

Run the test suite:
```bash
pytest
```

## 📝 Development

### Code Style
```bash
# Format code
black .

# Lint code
flake8
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the troubleshooting section below

## 🔧 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify DATABASE_URL in .env file
   - Ensure PostgreSQL is running
   - Check database permissions

2. **API Key Issues**
   - Verify Google Gemini API key
   - Check Twilio credentials
   - Ensure API keys are valid and active

3. **Resume Upload Problems**
   - Check file format (PDF/DOCX only)
   - Verify file size (max 10MB)
   - Ensure file is not corrupted

4. **Authentication Issues**
   - Clear browser cache
   - Check JWT token expiration
   - Verify user credentials

### Logs and Debugging

Enable debug mode in `.env`:
```env
DEBUG=True
```

Check application logs for detailed error information.

## 🚀 Deployment

### Production Setup

1. **Environment Variables**
   - Set `DEBUG=False`
   - Use strong `SECRET_KEY`
   - Configure production database
   - Set up proper CORS origins

2. **Database**
   - Use production PostgreSQL instance
   - Configure connection pooling
   - Set up regular backups

3. **Security**
   - Enable HTTPS
   - Configure firewall rules
   - Set up monitoring and logging

4. **Scaling**
   - Use load balancer
   - Configure caching
   - Set up CDN for static assets

## 📊 Performance

- **Response Time**: < 2 seconds for job searches
- **Concurrent Users**: Supports 100+ concurrent users
- **Database**: Optimized queries with proper indexing
- **File Upload**: Efficient resume processing

## 🔮 Future Enhancements

- [ ] Email notifications
- [ ] Job application tracking
- [ ] Interview scheduling
- [ ] Salary negotiation tools
- [ ] Career path recommendations
- [ ] Mobile app development
- [ ] Integration with job boards
- [ ] Advanced analytics dashboard

---

**Built with ❤️ by the Spinabot Team** 
