#!/usr/bin/env python3
"""
QUICK START EXAMPLE: PDF to CAPL Test Case Generation
This script demonstrates how to use the toolkit for your test case.
"""

from pathlib import Path
import sys

# Example 1: One-command workflow (recommended)
print("=" * 70)
print("EXAMPLE 1: Complete Workflow in One Command")
print("=" * 70)
print("""
python workflow.py "TC_7778_SideMarker_FL_RR_Failure.pdf"

This single command will:
1. Extract all test data from the PDF
2. Generate structured JSON
3. Create CAPL test code
4. Display all results and paths
""")

# Example 2: Step-by-step workflow
print("\n" + "=" * 70)
print("EXAMPLE 2: Step-by-Step Manual Workflow")
print("=" * 70)
print("""
# Step 1: Extract PDF to JSON
python pdf_test_case_extractor.py "TC_7778_SideMarker_FL_RR_Failure.pdf" json

# Step 2: Review the extracted data (optional)
type TC_7778_SideMarker_FL_RR_Failure_extracted.txt

# Step 3: Generate CAPL code
python capl_code_generator.py "TC_7778_SideMarker_FL_RR_Failure_extracted.json" TC_7778.can

# Step 4: Review generated CAPL code
type TC_7778.can
""")

# Example 3: Processing multiple PDFs
print("\n" + "=" * 70)
print("EXAMPLE 3: Batch Process Multiple PDFs")
print("=" * 70)
print("""
# Option A: Process each PDF individually
for %F in (*.pdf) do python workflow.py "%F"

# Option B: Create a custom batch script
# See batch_process_example.py below
""")

# Example 4: Python API usage
print("\n" + "=" * 70)
print("EXAMPLE 4: Using the Tools via Python API")
print("=" * 70)
print("""
from pdf_test_case_extractor import TestCaseExtractor
from capl_code_generator import CAPLCodeGenerator

# Extract test data
extractor = TestCaseExtractor()
test_data = extractor.extract_all("TC_7778_SideMarker_FL_RR_Failure.pdf")

# Generate CAPL code
generator = CAPLCodeGenerator()
capl_code = generator.generate_full_capl_code(test_data)
generator.save_capl_file(capl_code, "my_test.can")
""")

# Example 5: Filtering and customization
print("\n" + "=" * 70)
print("EXAMPLE 5: Customizing Extracted Data")
print("=" * 70)
print("""
import json

# Load extracted JSON
with open("TC_7778_extracted.json", "r") as f:
    test_data = json.load(f)

# Modify/filter data
# Example: Keep only stimulation steps 1 and 2
test_data['stimulations'] = [s for s in test_data['stimulations'] if int(s['number']) <= 2]

# Generate CAPL from modified data
from capl_code_generator import CAPLCodeGenerator
generator = CAPLCodeGenerator()
capl_code = generator.generate_full_capl_code(test_data)
generator.save_capl_file(capl_code, "partial_test.can")
""")

# Example 6: Error handling
print("\n" + "=" * 70)
print("EXAMPLE 6: Error Handling and Validation")
print("=" * 70)
print("""
from pdf_test_case_extractor import TestCaseExtractor
from pathlib import Path

extractor = TestCaseExtractor()

pdf_file = "TC_7778.pdf"
pdf_path = Path(pdf_file)

try:
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_file}")
    
    test_data = extractor.extract_all(str(pdf_path))
    
    # Validate extracted data
    if not test_data['metadata'].get('id'):
        print("WARNING: Test case ID not found in PDF")
    
    if not test_data['stimulations']:
        print("ERROR: No stimulation steps found")
        exit(1)
    
    print(f"✓ Successfully extracted {len(test_data['stimulations'])} steps")
    
except FileNotFoundError as e:
    print(f"ERROR: {e}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
""")

print("\n" + "=" * 70)
print("QUICK SETUP INSTRUCTIONS")
print("=" * 70)
print("""
1. Install dependencies:
   pip install PyPDF2

2. Navigate to tool directory:
   cd c:\\Users\\XEB2KOR\\Desktop\\BCM\\Tool

3. Run the workflow:
   python workflow.py "TC_7778_SideMarker_FL_RR_Failure.pdf"

4. Generated files will appear in the same directory:
   - TC_7778_SideMarker_FL_RR_Failure_extracted.json
   - TC_7778_SideMarker_FL_RR_Failure_extracted_generated.can

5. Open the .can file in vTESTstudio and implement the helper functions
""")

print("\n" + "=" * 70)
print("TESTING THE GENERATED CAPL CODE")
print("=" * 70)
print("""
In vTESTstudio:

1. Create a new test module or open existing one
2. Import the generated .can file
3. Implement these functions based on your environment:
   - vtsCreateFault()     → Fault injection API
   - vtsRemoveFault()     → Fault removal
   - checkActiveDTC()     → DTC verification
   - vtsStimulateSignal() → Signal sending

4. Example implementation for vtsStimulateSignal:
   void vtsStimulateSignal(char signalName[], long value)
   {
       // Send CAN signal
       write(signalName, value);
   }

5. Run the test via the test execution framework
6. Verify outputs match expected results
""")

print("\n" + "=" * 70)
print("NEXT STEPS")
print("=" * 70)
print("""
1. Review this README.md for complete documentation
2. Run: python workflow.py <your_pdf.pdf>
3. Examine the generated JSON output
4. Review the generated CAPL code
5. Implement helper functions in vTESTstudio
6. Execute and validate test cases
7. For multiple PDFs, batch process using similar commands

For detailed documentation, see: README.md
For API reference, check individual source files
""")
