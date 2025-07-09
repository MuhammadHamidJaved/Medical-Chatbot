#!/usr/bin/env python3
"""
Run script for Medical Bot Streamlit Application
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ Packages installed successfully!")

def run_streamlit_app():
    """Run the Streamlit application"""
    print("🚀 Starting Medical Bot Application...")
    os.system("streamlit run app.py --server.port 8080 --server.address 0.0.0.0")

if __name__ == "__main__":
    print("🏥 Medical Bot Startup Script")
    print("=" * 50)
    
    # Check if requirements need to be installed
    try:
        import streamlit
        import google.generativeai
        print("✅ All packages are installed")
    except ImportError:
        install_requirements()
    
    # Run the app
    run_streamlit_app()
