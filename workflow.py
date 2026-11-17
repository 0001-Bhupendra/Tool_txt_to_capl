"""
Integrated Workflow: PDF Test Case to CAPL Code Generation
Combines PDF extraction and CAPL code generation in a single workflow.
"""

import sys
import subprocess
from pathlib import Path
from typing import Optional


class TestCaseWorkflow:
    """Orchestrate the complete workflow from PDF to CAPL code."""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.extractor_script = self.script_dir / "pdf_test_case_extractor.py"
        self.generator_script = self.script_dir / "capl_code_generator.py"
    
    def run_extraction(self, pdf_file: str) -> Optional[str]:
        """Run the PDF extraction step and return JSON output path."""
        print("\n" + "=" * 70)
        print("STEP 1: EXTRACTING TEST CASE DATA FROM PDF")
        print("=" * 70)
        
        pdf_path = Path(pdf_file)
        if not pdf_path.exists():
            print(f"Error: PDF file not found: {pdf_file}")
            return None
        
        # Run extractor
        cmd = [sys.executable, str(self.extractor_script), str(pdf_path), "json"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            
            # Determine output JSON file
            json_output = pdf_path.parent / f"{pdf_path.stem}_extracted.json"
            return str(json_output)
        
        except subprocess.CalledProcessError as e:
            print(f"Error running extraction: {e}")
            print("STDOUT:", e.stdout)
            print("STDERR:", e.stderr)
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def run_generation(self, json_file: str, output_capl: Optional[str] = None) -> bool:
        """Run the CAPL code generation step."""
        print("\n" + "=" * 70)
        print("STEP 2: GENERATING CAPL TEST CODE")
        print("=" * 70)
        
        json_path = Path(json_file)
        if not json_path.exists():
            print(f"Error: JSON file not found: {json_file}")
            return False
        
        # Build command
        cmd = [sys.executable, str(self.generator_script), str(json_path)]
        if output_capl:
            cmd.append(output_capl)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            return True
        
        except subprocess.CalledProcessError as e:
            print(f"Error running generation: {e}")
            print("STDOUT:", e.stdout)
            print("STDERR:", e.stderr)
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def run_full_workflow(self, pdf_file: str, output_capl: Optional[str] = None) -> bool:
        """Run the complete workflow from PDF to CAPL."""
        print("\n" + "=" * 70)
        print("TEST CASE CONVERSION WORKFLOW")
        print("=" * 70)
        print(f"Input PDF: {pdf_file}")
        if output_capl:
            print(f"Output CAPL: {output_capl}")
        
        # Step 1: Extract PDF
        json_file = self.run_extraction(pdf_file)
        if not json_file:
            print("\nWorkflow failed during extraction step")
            return False
        
        # Step 2: Generate CAPL
        success = self.run_generation(json_file, output_capl)
        if success:
            print("\n" + "=" * 70)
            print("WORKFLOW COMPLETED SUCCESSFULLY")
            print("=" * 70)
            print(f"JSON Data: {json_file}")
            if output_capl:
                print(f"CAPL Code: {output_capl}")
            return True
        else:
            print("\nWorkflow failed during generation step")
            return False


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python workflow.py <pdf_file> [output_capl_file]")
        print("\nExample:")
        print("  python workflow.py TC_7778.pdf")
        print("  python workflow.py TC_7778.pdf my_test.can")
        print("\nThis workflow will:")
        print("  1. Extract test case data from PDF")
        print("  2. Convert to JSON format")
        print("  3. Generate CAPL test code")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_capl = sys.argv[2] if len(sys.argv) > 2 else None
    
    workflow = TestCaseWorkflow()
    success = workflow.run_full_workflow(pdf_file, output_capl)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
