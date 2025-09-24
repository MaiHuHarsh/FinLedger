"""
ExpenseTracker Setup Script
Installs dependencies and initializes the application
"""

import os
import sys
import subprocess

def install_requirements():
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def initialize_database():
    print("🗃️ Initializing database...")
    try:
        subprocess.run([sys.executable, 'database.py'], check=True)
        print("✅ Database initialized successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to initialize database")
        return False

def main():
    print("🛠️ ExpenseTracker Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install dependencies
    if not install_requirements():
        return
    
    # Initialize database
    if not initialize_database():
        return
    
    print("=" * 40)
    print("🎉 Setup completed successfully!")
    print("🚀 Run 'python run.py' to start the application")
    print("🌐 Then open http://localhost:5000 in your browser")
    print("🔐 Demo login: admin / admin123")

if __name__ == '__main__':
    main()