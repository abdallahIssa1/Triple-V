#!/usr/bin/env python3
"""
Triple V Application Launcher
Easy launcher script with dependency checking
"""

import sys
import subprocess
import os
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = ['PyQt5', 'requests', 'packaging']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Install missing dependencies"""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Dependencies installed successfully!")

def create_desktop_shortcut():
    """Create a desktop shortcut (Windows only)"""
    if sys.platform == 'win32':
        try:
            import win32com.client
            
            desktop = Path.home() / 'Desktop'
            shortcut_path = desktop / 'Triple V.lnk'
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = str(Path(__file__).parent / 'main.py')
            shortcut.WorkingDirectory = str(Path(__file__).parent)
            shortcut.IconLocation = str(Path(__file__).parent / 'assets' / 'icon.ico')
            shortcut.save()
            
            print(f"Desktop shortcut created: {shortcut_path}")
        except:
            print("Could not create desktop shortcut (pywin32 not installed)")

def main():
    """Main launcher function"""
    print("=" * 50)
    print("Triple V Desktop Application Launcher")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("ERROR: Python 3.7 or higher is required!")
        sys.exit(1)
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        response = input("Would you like to install them now? (y/n): ")
        
        if response.lower() == 'y':
            try:
                install_dependencies()
            except Exception as e:
                print(f"Error installing dependencies: {e}")
                print("Please install manually using: pip install -r triple-v-requirements.txt")
                sys.exit(1)
        else:
            print("Please install dependencies manually using: pip install -r requirements.txt")
            sys.exit(1)
    
    # Create necessary directories
    dirs_to_create = ['downloads', 'config', 'assets']
    for dir_name in dirs_to_create:
        dir_path = Path(__file__).parent / dir_name
        dir_path.mkdir(exist_ok=True)
    
    # Save the logo if it doesn't exist
    logo_path = Path(__file__).parent / 'assets' / 'logo.svg'
    if not logo_path.exists():
        print("Creating logo file...")
        # SVG logo content would be saved here
    
    # Launch the application
    print("\nLaunching Triple V...")
    print("-" * 50)
    
    try:
        # Run main.py
        subprocess.run([sys.executable, 'main.py'], cwd=Path(__file__).parent)
    except KeyboardInterrupt:
        print("\nApplication closed by user.")
    except Exception as e:
        print(f"\nError running application: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()