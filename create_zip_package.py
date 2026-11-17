#!/usr/bin/env python3
"""
ZIP Package Builder - Creates standalone distribution
Packages PDF Test Case Converter into a shareable ZIP file

Run this ONCE:
    python create_zip_package.py
"""

import zipfile
import shutil
from pathlib import Path
import os

def create_zip_package():
    """Create the final ZIP package."""
    
    print("\n" + "█"*80)
    print("█ PDF TEST CASE CONVERTER - ZIP PACKAGE BUILDER")
    print("█"*80)
    
    app_dir = Path(__file__).parent
    zip_path = app_dir / "PDFConverter_Standalone.zip"
    
    print(f"\n✓ Creating ZIP package...")
    print(f"  Output: {zip_path}\n")
    
    # Files to include in ZIP with descriptions
    files_to_include = [
        # Launcher (most important!)
        ("RUN_CONVERTER.bat", "🎯 Double-click this to run the tool!"),
        
        # Core application files
        ("app.py", "Web interface (Streamlit)"),
        ("pdf_test_case_extractor.py", "PDF extraction engine"),
        ("app_requirements.txt", "Python dependencies"),
        
        # Documentation
        ("TEAM_EDITION.md", "Team usage guide"),
        ("CONVERSION_SUMMARY.md", "What was fixed and new features"),
        ("QUICK_REFERENCE_4000_PDFS.md", "Batch processing guide"),
        ("BATCH_CONVERSION_GUIDE.md", "Detailed reference"),
        ("README_V2.0.md", "Complete documentation"),
        
        # Batch processing tools
        ("batch_pdf_converter.py", "Command-line batch processor"),
        ("check_conversion_progress.py", "Progress monitor"),
    ]
    
    # Create ZIP file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for src_name, description in files_to_include:
            src_path = app_dir / src_name
            if src_path.exists():
                zf.write(src_path, arcname=src_name)
                print(f"  ✓ {description:<45} {src_name}")
            else:
                print(f"  ⚠ MISSING: {src_name}")
        
        # Add a startup guide
        startup_guide = """
╔═════════════════════════════════════════════════════════════════════════════╗
║                                                                             ║
║     📄 PDF TEST CASE CONVERTER - STANDALONE EDITION v2.0                   ║
║                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════╝

🚀 QUICK START (Windows):
═══════════════════════════════════════════════════════════════════════════════

   1. Double-click: RUN_CONVERTER.bat
   2. Wait for browser to open (http://localhost:8501)
   3. Upload your PDFs and start converting!
   
   That's it! 🎉

✨ WHAT YOU GET:
═══════════════════════════════════════════════════════════════════════════════

   Tab 1: Convert 🔄
   • Upload single or multiple PDFs
   • Real-time progress bar
   • Extract test signals automatically

   Tab 2: Download 📥
   • Download individual TXT/JSON files
   • Download all as ZIP archive
   • Easy file management

   Tab 3: Statistics 📊
   • View conversion metrics
   • See signal counts
   • Distribution analysis

   Tab 4: Help ❓
   • Complete user guide
   • Troubleshooting FAQ
   • Signal type reference

📋 WHAT GETS EXTRACTED:
═══════════════════════════════════════════════════════════════════════════════

   Pre-Condition:  Initial system setup and signal values
   Stimulations:   Test actions and expected results
   Post-Condition: Final system state and cleanup

   Output Formats:
   • TXT: Human-readable test case format
   • JSON: Structured data for processing

🔧 SYSTEM REQUIREMENTS:
═══════════════════════════════════════════════════════════════════════════════

   • Windows 7, 10, 11, or later
   • Python 3.8+ installed on your computer
   • ~500 MB free disk space
   • Internet connection: Optional

   Note: Python must be installed! Get it from https://www.python.org/

💡 TIPS:
═══════════════════════════════════════════════════════════════════════════════

   ✓ For large batch (100+ PDFs): Use command-line tools
   ✓ For team use: Share the extracted folder
   ✓ For single/few PDFs: Use the web interface

📖 DOCUMENTATION:
═══════════════════════════════════════════════════════════════════════════════

   • README_V2.0.md - Complete guide
   • TEAM_EDITION.md - Team sharing instructions
   • CONVERSION_SUMMARY.md - What was improved
   • QUICK_REFERENCE_4000_PDFS.md - Batch processing

⚙️ ADVANCED (Command Line):
═══════════════════════════════════════════════════════════════════════════════

   Single PDF:
   python pdf_test_case_extractor.py "filename.pdf"

   Batch (All PDFs in folder):
   python batch_pdf_converter.py

   Monitor Progress:
   python check_conversion_progress.py

🆘 TROUBLESHOOTING:
═══════════════════════════════════════════════════════════════════════════════

   Q: "Python is not installed"
   A: Download from https://www.python.org/ and run installer

   Q: "RUN_CONVERTER.bat won't open"
   A: Right-click → Open with → Choose Python 3.x

   Q: "Some signals are missing"
   A: Ensure PDF is text-extractable (not scanned image)

   Q: "Port 8501 already in use"
   A: Close other Streamlit apps or use different port

📤 SHARE WITH YOUR TEAM:
═══════════════════════════════════════════════════════════════════════════════

   1. Send this entire extracted folder
   2. They just run: RUN_CONVERTER.bat
   3. That's it! No complex setup!

✅ VERSION 2.0 IMPROVEMENTS:
═══════════════════════════════════════════════════════════════════════════════

   ✓ Fixed Pre-Condition extraction (3→7 items for TC_26107)
   ✓ Added Proxy_* signal support (was completely missing)
   ✓ Created web interface (Streamlit)
   ✓ Created team launcher (auto-setup)
   ✓ Progress tracking for batch jobs
   ✓ Comprehensive documentation

🎯 RECOMMENDED WORKFLOW:
═══════════════════════════════════════════════════════════════════════════════

   Single/Few PDFs:
   1. Run RUN_CONVERTER.bat
   2. Upload PDFs through web interface
   3. Download results

   Many PDFs (100+):
   1. Copy PDFs to this folder
   2. Open Command Prompt here
   3. Run: python batch_pdf_converter.py
   4. Wait for completion
   5. Files are ready!

═══════════════════════════════════════════════════════════════════════════════

Questions? See the included documentation files or the Help tab in the app!

Happy converting! 📄✨

═══════════════════════════════════════════════════════════════════════════════
"""
        zf.writestr("START_HERE.txt", startup_guide)
        print(f"  ✓ {'Quick start guide':<45} START_HERE.txt")
    
    # Print summary
    zip_size = zip_path.stat().st_size / (1024*1024)
    
    print(f"\n" + "="*80)
    print("✓ PACKAGE CREATED SUCCESSFULLY!")
    print("="*80)
    print(f"\n📦 File: {zip_path}")
    print(f"   Size: {zip_size:.1f} MB")
    print(f"   Contains: {len(files_to_include)} files + documentation")
    
    print(f"\n📤 HOW TO SHARE WITH YOUR TEAM:")
    print(f"""
   1. Send file: PDFConverter_Standalone.zip
   2. They extract it anywhere (right-click → Extract All)
   3. They double-click: RUN_CONVERTER.bat
   4. Browser opens automatically
   5. They can start converting PDFs!
   
   ✨ NO SETUP REQUIRED! (Just needs Python 3.8+)
""")
    
    print("="*80)
    print("\n✓ Ready to distribute!")
    
    return zip_path

if __name__ == "__main__":
    try:
        zip_path = create_zip_package()
        print(f"\n✅ Success! ZIP package is ready: {zip_path}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
