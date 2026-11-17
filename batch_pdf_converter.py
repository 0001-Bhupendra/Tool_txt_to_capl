#!/usr/bin/env python3
"""
Batch PDF to TXT Converter
Processes all PDF files in the directory using the existing extraction logic.
One PDF → One TXT file (one-to-one mapping)
"""

from pathlib import Path
import subprocess
import sys
from datetime import datetime

def get_all_pdfs(directory):
    """Find all PDF files in the given directory"""
    directory = Path(directory)
    pdf_files = sorted(directory.glob("*.pdf"))
    return pdf_files

def process_pdf(pdf_path):
    """
    Process a single PDF file using pdf_test_case_extractor.py
    Returns True if successful, False otherwise
    """
    try:
        print(f"\n{'='*70}")
        print(f"Processing: {pdf_path.name}")
        print(f"{'='*70}")
        
        # Run the extractor
        result = subprocess.run(
            [sys.executable, "pdf_test_case_extractor.py", str(pdf_path)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {pdf_path.name}")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ FAILED: {pdf_path.name}")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ TIMEOUT: {pdf_path.name} took too long to process")
        return False
    except Exception as e:
        print(f"❌ ERROR processing {pdf_path.name}: {str(e)}")
        return False

def main():
    """Main batch processing loop"""
    print(f"\n{'*'*70}")
    print(f"BATCH PDF TO TXT CONVERTER")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'*'*70}")
    
    # Get current directory
    current_dir = Path.cwd()
    print(f"Directory: {current_dir}\n")
    
    # Find all PDFs
    pdf_files = get_all_pdfs(current_dir)
    
    if not pdf_files:
        print("❌ No PDF files found in the current directory!")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) to process:\n")
    for i, pdf in enumerate(pdf_files, 1):
        print(f"  {i}. {pdf.name}")
    
    # Process each PDF
    successful = 0
    failed = 0
    skipped = 0
    
    for pdf_file in pdf_files:
        # Check if TXT file already exists
        txt_file = current_dir / f"{pdf_file.stem}.txt"
        if txt_file.exists():
            print(f"\n⏭️  SKIPPED: {pdf_file.name} (TXT file already exists)")
            skipped += 1
            continue
        
        # Process the PDF
        if process_pdf(pdf_file):
            successful += 1
        else:
            failed += 1
    
    # Summary
    print(f"\n{'='*70}")
    print(f"BATCH PROCESSING COMPLETE")
    print(f"{'='*70}")
    print(f"Processed:  {successful} ✅")
    print(f"Failed:     {failed} ❌")
    print(f"Skipped:    {skipped} ⏭️")
    print(f"Total:      {len(pdf_files)}")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
