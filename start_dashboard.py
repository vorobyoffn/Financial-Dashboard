#!/usr/bin/env python3
"""
Financial Forecast Dashboard Startup Script
Simple launcher for the complete dashboard system
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("=" * 60)
    print("🚀 FINANCIAL FORECAST DASHBOARD")
    print("=" * 60)
    print("Your complete solution for financial data analysis")
    print("=" * 60)

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import pandas
        import xlrd
        import xlsxwriter
        import matplotlib
        import flask
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def show_menu():
    """Show main menu options"""
    print("\n📊 DASHBOARD OPTIONS:")
    print("1. 🌐 Launch Web Dashboard")
    print("2. 💻 Run Command Line Processor")
    print("3. 📁 Scan Input Files")
    print("4. 🔄 Process All Files")
    print("5. 📋 Show System Status")
    print("6. ❌ Exit")
    
    while True:
        try:
            choice = input("\nSelect an option (1-6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return choice
            else:
                print("Please enter a number between 1 and 6")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit(0)

def launch_web_dashboard():
    """Launch the Flask web dashboard"""
    print("\n🌐 Starting Web Dashboard...")
    print("The dashboard will open in your browser automatically.")
    print("Press Ctrl+C to stop the server when done.")
    
    try:
        # Start Flask app in background
        process = subprocess.Popen([sys.executable, 'app.py'])
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Open browser
        webbrowser.open('http://localhost:5000')
        
        print("✅ Dashboard is running at http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        
        # Wait for user to stop
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping dashboard...")
            process.terminate()
            process.wait()
            
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")

def run_command_line_processor():
    """Run the command line processor"""
    print("\n💻 Command Line Processor")
    print("Choose processing mode:")
    print("1. Scan files only")
    print("2. Process all files")
    print("3. Full scan and process")
    
    try:
        mode_choice = input("Select mode (1-3): ").strip()
        if mode_choice == '1':
            mode = 'scan'
        elif mode_choice == '2':
            mode = 'process'
        elif mode_choice == '3':
            mode = 'full'
        else:
            print("Invalid choice, using 'full' mode")
            mode = 'full'
        
        print(f"\n🔄 Running processor in '{mode}' mode...")
        result = subprocess.run([sys.executable, 'main_processor.py', '--mode', mode], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Processing completed successfully!")
            print("\nOutput:")
            print(result.stdout)
        else:
            print("❌ Processing failed!")
            print("Error:", result.stderr)
            
    except Exception as e:
        print(f"❌ Error running processor: {e}")

def scan_input_files():
    """Quick scan of input files"""
    print("\n📁 Scanning Input Directory...")
    
    input_dir = Path("Input")
    if not input_dir.exists():
        print("❌ Input directory not found. Creating it...")
        input_dir.mkdir(exist_ok=True)
        print("✅ Input directory created. Please add your Excel files there.")
        return
    
    files = list(input_dir.glob("*.xls*"))
    
    if not files:
        print("📂 Input directory is empty")
        print("Please add your Excel forecast files (.xls or .xlsx) to the Input folder")
        return
    
    print(f"📊 Found {len(files)} forecast files:")
    for file in files:
        size = file.stat().st_size / 1024  # KB
        print(f"  📄 {file.name} ({size:.1f} KB)")
    
    print(f"\n💡 To process these files, choose option 4 from the main menu")

def process_all_files():
    """Process all files in input directory"""
    print("\n🔄 Processing All Files...")
    
    try:
        result = subprocess.run([sys.executable, 'main_processor.py', '--mode', 'full'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All files processed successfully!")
            print("\nOutput:")
            print(result.stdout)
            
            # Show output summary
            output_dir = Path("Output")
            if output_dir.exists():
                print("\n📁 Generated Output Files:")
                for subdir in ['spreadsheets', 'heatmaps', 'charts', 'summaries']:
                    subdir_path = output_dir / subdir
                    if subdir_path.exists():
                        files = list(subdir_path.glob("*"))
                        print(f"  📂 {subdir}/: {len(files)} files")
        else:
            print("❌ Processing failed!")
            print("Error:", result.stderr)
            
    except Exception as e:
        print(f"❌ Error processing files: {e}")

def show_system_status():
    """Show current system status"""
    print("\n📋 SYSTEM STATUS")
    print("-" * 40)
    
    # Check directories
    directories = {
        "Input": Path("Input"),
        "Output": Path("Output"),
        "Templates": Path("templates"),
        "Uploads": Path("uploads")
    }
    
    for name, path in directories.items():
        if path.exists():
            if path.is_dir():
                files = len(list(path.glob("*")))
                print(f"✅ {name}: {files} items")
            else:
                print(f"📄 {name}: File")
        else:
            print(f"❌ {name}: Not found")
    
    # Check key files
    key_files = [
        "app.py",
        "main_processor.py", 
        "config.py",
        "utils.py",
        "requirements.txt"
    ]
    
    print("\n📄 KEY FILES:")
    for file in key_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
    
    # Check Python version
    print(f"\n🐍 Python Version: {sys.version.split()[0]}")

def main():
    """Main function"""
    print_banner()
    
    if not check_dependencies():
        return
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            launch_web_dashboard()
        elif choice == '2':
            run_command_line_processor()
        elif choice == '3':
            scan_input_files()
        elif choice == '4':
            process_all_files()
        elif choice == '5':
            show_system_status()
        elif choice == '6':
            print("\n👋 Thank you for using the Financial Forecast Dashboard!")
            break
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
