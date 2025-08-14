#!/usr/bin/env python3
"""
Startup script for Spinabot Job Agent Frontend
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Start the Streamlit frontend application"""
    print("🎨 Starting Spinabot Job Agent Frontend...")
    print("📍 URL: http://localhost:8501")
    print("=" * 50)
    
    # Change to frontend directory
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        sys.exit(1)
    
    os.chdir(frontend_dir)
    
    # Start Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Frontend stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start frontend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
