"""
Triple V EXE Builder
Run this script to create a standalone executable
"""

import os
import sys
import shutil
import PyInstaller.__main__

def build_exe():
    # Clean previous builds
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    # PyInstaller arguments
    args = [
        'main.py',                    # Entry point
        '--name=TripleV',             # EXE name
        '--onefile',                  # Single EXE file
        '--windowed',                 # No console window
        '--icon=assets/triple_v_logo.ico',     # Application icon
        
        # Add data files
        '--add-data=assets;assets',
        '--add-data=config;config',
        
        # Hidden imports (if needed)
        '--hidden-import=PyQt5',
        '--hidden-import=requests',
        '--hidden-import=packaging',
        
        # Paths
        '--distpath=dist',
        '--workpath=build',
        '--specpath=.',
        
        # Clean build
        '--clean',
        '--noconfirm',
    ]
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    print("\n" + "="*50)
    print("Build complete! EXE located at: dist/TripleV.exe")
    print("="*50)

if __name__ == "__main__":
    build_exe()