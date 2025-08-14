#!/usr/bin/env python3
"""
Startup script for Spinabot Job Agent Backend
"""

import uvicorn
import os
from dotenv import load_dotenv

def main():
    """Start the FastAPI backend server"""
    load_dotenv()
    
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("DEBUG", "False").lower() == "true"
    
    print("🚀 Starting Spinabot Job Agent Backend...")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔄 Reload: {reload}")
    print("=" * 50)
    
    # Start the server
    uvicorn.run(
        "backend.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    main()
