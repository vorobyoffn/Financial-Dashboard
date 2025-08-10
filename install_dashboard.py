#!/usr/bin/env python3
"""
Dashboard Installation Script
Sets up the complete Financial Forecast Dashboard environment
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print installation banner"""
    print("=" * 60)
    print("🚀 FINANCIAL FORECAST DASHBOARD INSTALLER")
    print("=" * 60)
    print("Setting up your complete financial analysis system")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python 3.7+ required. Current version: {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing Dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Install requirements
        if Path("requirements.txt").exists():
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                                  check=True, capture_output=True, text=True)
            print("✅ Dependencies installed successfully")
            return True
        else:
            print("❌ requirements.txt not found")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print("Error output:", e.stderr)
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating Directory Structure...")
    
    directories = [
        "Input",
        "Output",
        "Output/spreadsheets", 
        "Output/heatmaps",
        "Output/charts",
        "Output/summaries",
        "uploads",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {directory}")
    
    print("✅ Directory structure created")

def create_sample_files():
    """Create sample configuration and data files"""
    print("\n📄 Creating Sample Files...")
    
    # Create .gitignore if it doesn't exist
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Dashboard specific
Output/
uploads/
logs/
*.log
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    print("  ✅ .gitignore")
    
    # Create environment file template
    env_content = """# Dashboard Environment Variables
# Copy this file to .env and modify as needed

FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
"""
    
    with open(".env.template", "w") as f:
        f.write(env_content)
    print("  ✅ .env.template")
    
    print("✅ Sample files created")

def test_installation():
    """Test if the installation was successful"""
    print("\n🧪 Testing Installation...")
    
    try:
        # Test imports
        import pandas
        import xlrd
        import xlsxwriter
        import matplotlib
        import flask
        print("  ✅ All packages imported successfully")
        
        # Test file creation
        test_file = Path("test_installation.txt")
        test_file.write_text("Installation test successful")
        test_file.unlink()
        print("  ✅ File operations working")
        
        print("✅ Installation test passed")
        return True
        
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def show_next_steps():
    """Show what to do next"""
    print("\n🎉 INSTALLATION COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    
    print("\n📋 NEXT STEPS:")
    print("1. 🎯 Create demo data: python3 create_demo_data.py")
    print("2. 🚀 Launch dashboard: python3 start_dashboard.py")
    print("3. 🌐 Web interface: python3 app.py")
    print("4. 💻 Command line: python3 main_processor.py --help")
    
    print("\n📁 DIRECTORY STRUCTURE:")
    print("  Input/          - Place your Excel files here")
    print("  Output/         - Generated reports and charts")
    print("  templates/      - Web interface templates")
    print("  uploads/        - Temporary file uploads")
    
    print("\n🔧 CONFIGURATION:")
    print("  - Edit dashboard_config.py for dashboard settings")
    print("  - Edit config.py for processing settings")
    print("  - Copy .env.template to .env for environment variables")
    
    print("\n💡 QUICK START:")
    print("  python3 create_demo_data.py  # Create sample data")
    print("  python3 start_dashboard.py   # Launch dashboard")
    
    print("\n📚 DOCUMENTATION:")
    print("  - README.md for detailed usage instructions")
    print("  - Run with --help flag for command options")

def main():
    """Main installation function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        print("❌ Installation cannot continue")
        return
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return
    
    # Create directories
    create_directories()
    
    # Create sample files
    create_sample_files()
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed")
        return
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()
