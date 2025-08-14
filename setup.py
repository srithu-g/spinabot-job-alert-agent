#!/usr/bin/env python3
"""
Setup script for Spinabot Job Agent
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def create_env_file():
    """Create .env file from template"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if not env_example.exists():
        print("❌ env.example file not found")
        return False
    
    print("📝 Creating .env file from template...")
    try:
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ .env file created successfully")
        print("⚠️  Please update the .env file with your actual configuration values")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    # Install additional dependencies for development
    if os.getenv("DEV_MODE"):
        if not run_command("pip install -r requirements-dev.txt", "Installing development dependencies"):
            return False
    
    return True

def setup_database():
    """Setup database and run migrations"""
    print("🗄️  Setting up database...")
    
    # Check if DATABASE_URL is configured
    if not os.getenv("DATABASE_URL"):
        print("⚠️  DATABASE_URL not configured in .env file")
        print("   Please update your .env file with the correct database URL")
        return False
    
    # Run database migrations
    if not run_command("alembic upgrade head", "Running database migrations"):
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up Spinabot Job Agent...")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Create virtual environment if not exists
    if not os.path.exists(".venv"):
        print("📦 Creating virtual environment...")
        if not run_command("python -m venv .venv", "Creating virtual environment"):
            return False
    
    # Activate virtual environment
    if os.name == 'nt':  # Windows
        activate_script = ".venv\\Scripts\\activate"
    else:  # Unix/Linux/MacOS
        activate_script = ".venv/bin/activate"
    
    print("🔧 Activating virtual environment...")
    os.environ['VIRTUAL_ENV'] = str(Path(".venv").absolute())
    
    # Create .env file
    if not create_env_file():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Setup database
    if not setup_database():
        return False
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update your .env file with actual configuration values")
    print("2. Start the backend: python -m uvicorn backend.main:app --reload")
    print("3. Start the frontend: streamlit run frontend/app.py")
    print("\n🔗 Documentation: Check the README.md file for detailed instructions")

if __name__ == "__main__":
    main()
