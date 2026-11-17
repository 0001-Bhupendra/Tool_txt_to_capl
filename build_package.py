#!/usr/bin/env python3
"""
Build Script: Creates standalone .exe and ZIP package
Converts the PDF Test Case Converter into a shareable executable

Run this ONCE to build the standalone package:
    python build_package.py
"""

import subprocess
import sys
import shutil
import zipfile
from pathlib import Path
import os

def run_command(cmd, description):
    """Run a command and report status."""
    print(f"\n✓ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  Warning: {result.stderr[:200]}")
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def build_exe():
    """Build the standalone .exe using PyInstaller."""
    
    print("\n" + "="*80)
    print("BUILDING STANDALONE EXECUTABLE")
    print("="*80)
    
    # Check if PyInstaller is installed
    print("\n✓ Checking PyInstaller...")
    result = subprocess.run([sys.executable, "-m", "pip", "show", "pyinstaller"], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print("  Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "-q"], check=True)
    
    # Build the .exe
    app_dir = Path(__file__).parent
    
    cmd = (
        f'{sys.executable} -m PyInstaller '
        f'--onefile '
        f'--windowed '
        f'--icon=NONE '
        f'--name=PDFConverter '
        f'--distpath=dist '
        f'--buildpath=build '
        f'--specpath=specs '
        f'--add-data "{app_dir}/app.py:." '
        f'--add-data "{app_dir}/pdf_test_case_extractor.py:." '
        f'--add-data "{app_dir}/app_requirements.txt:." '
        f'--hidden-import=streamlit '
        f'--hidden-import=PyPDF2 '
        f'--hidden-import=pandas '
        f'"{app_dir}/standalone_launcher.py"'
    )
    
    if run_command(cmd, "Building executable with PyInstaller"):
        exe_path = app_dir / "dist" / "PDFConverter.exe"
        if exe_path.exists():
            print(f"  ✓ Created: {exe_path}")
            return exe_path
    
    return None

def create_zip_package(exe_path):
    """Create the final ZIP package."""
    
    print("\n✓ Creating ZIP package...")
    
    app_dir = Path(__file__).parent
    zip_path = app_dir / "PDFConverter_Standalone.zip"
    
    # Files to include in ZIP
    files_to_include = [
        ("dist/PDFConverter.exe", "PDFConverter.exe"),
        ("app.py", "app.py"),
        ("pdf_test_case_extractor.py", "pdf_test_case_extractor.py"),
        ("app_requirements.txt", "app_requirements.txt"),
        ("TEAM_EDITION.md", "TEAM_EDITION.md"),
        ("CONVERSION_SUMMARY.md", "CONVERSION_SUMMARY.md"),
        ("QUICK_REFERENCE_4000_PDFS.md", "QUICK_REFERENCE_4000_PDFS.md"),
        ("BATCH_CONVERSION_GUIDE.md", "BATCH_CONVERSION_GUIDE.md"),
        ("README_V2.0.md", "README.md"),
    ]
    
    # Create ZIP file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for src, arcname in files_to_include:
            src_path = app_dir / src
            if src_path.exists():
                zf.write(src_path, arcname=arcname)
                print(f"  ✓ Added: {arcname}")
            else:
                print(f"  ⚠ Skipped (not found): {src}")
        
        # Add a README for extraction
        readme_content = """PDF TEST CASE CONVERTER - STANDALONE EDITION
============================================

QUICK START:
1. Double-click PDFConverter.exe
2. Browser opens automatically
3. Upload PDFs and convert!

FEATURES:
- 🔄 Convert PDFs to TXT/JSON
- 📥 Download individual or batch files
- 📊 View conversion statistics
- ❓ Built-in help documentation

SYSTEM REQUIREMENTS:
- Windows 7 or later
- ~300 MB disk space
- Internet: Optional

NO INSTALLATION NEEDED!
Just extract and run PDFConverter.exe

For more info, see README.md or TEAM_EDITION.md
"""
        zf.writestr("START_HERE.txt", readme_content)
        print(f"  ✓ Added: START_HERE.txt")
    
    print(f"\n✓ Package created: {zip_path}")
    print(f"  Size: {zip_path.stat().st_size / (1024*1024):.1f} MB")
    return zip_path

def cleanup():
    """Clean up build artifacts."""
    print("\n✓ Cleaning up build files...")
    
    app_dir = Path(__file__).parent
    dirs_to_remove = ["build", "specs"]
    
    for dir_name in dirs_to_remove:
        dir_path = app_dir / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"  ✓ Removed: {dir_name}")

def main():
    """Main build process."""
    
    print("\n" + "█"*80)
    print("█ PDF TEST CASE CONVERTER - STANDALONE PACKAGE BUILDER")
    print("█"*80)
    
    # Step 1: Build .exe
    exe_path = build_exe()
    if not exe_path:
        print("\n✗ Failed to build executable")
        return False
    
    # Step 2: Create ZIP package
    zip_path = create_zip_package(exe_path)
    if not zip_path:
        print("\n✗ Failed to create ZIP package")
        return False
    
    # Step 3: Cleanup
    cleanup()
    
    # Success!
    print("\n" + "="*80)
    print("✓ BUILD COMPLETE!")
    print("="*80)
    print(f"\n📦 Standalone package ready: {zip_path}")
    print(f"\nWhat's inside:")
    print(f"  • PDFConverter.exe - Standalone executable")
    print(f"  • app.py - Web interface")
    print(f"  • pdf_test_case_extractor.py - Extraction engine")
    print(f"  • app_requirements.txt - Dependencies")
    print(f"  • Documentation files")
    print(f"  • START_HERE.txt - Quick start guide")
    
    print(f"\n📤 SHARE WITH YOUR TEAM:")
    print(f"  1. Send: {zip_path}")
    print(f"  2. They extract the ZIP anywhere")
    print(f"  3. They double-click PDFConverter.exe")
    print(f"  4. Done! Converter opens in browser")
    
    print(f"\n✨ No Python installation needed on their computer!")
    print("="*80)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
