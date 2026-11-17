# PDF Test Case to CAPL Code Generation Toolkit

A comprehensive Python toolkit for extracting test case data from PDF documents and automatically generating CAPL test code for Vector vTESTstudio.

## Overview

This toolkit streamlines the process of converting test case specifications from PDF format into executable CAPL test modules. It includes:

1. **PDF Test Case Extractor** - Parses PDF documents and extracts structured test case data
2. **CAPL Code Generator** - Converts extracted data into CAPL test module code
3. **Integrated Workflow** - Combines both tools for end-to-end automation

## Features

### PDF Extractor (`pdf_test_case_extractor.py`)
- Extracts metadata (test case ID, title, component, configuration)
- Identifies and parses Pre-Condition sections
- Extracts Stimulation steps with actions and expected results
- Parses Post-Condition cleanup steps
- Handles multiple fault types (SCG, OL) and signal transitions
- Outputs in JSON and formatted text formats
- Supports batch processing of multiple PDFs

### CAPL Generator (`capl_code_generator.py`)
- Generates complete CAPL test modules from extracted JSON data
- Automatic function generation for:
  - Pre-condition setup
  - Stimulation steps (one function per step)
  - Post-condition cleanup
  - Helper functions for common operations
- Main test execution function with orchestration
- Customizable indentation and code formatting
- Well-documented and easily maintainable generated code

### Workflow (`workflow.py`)
- Single-command execution of complete pipeline
- Error handling and progress reporting
- Output file generation and validation

## Installation

### Prerequisites
- Python 3.7 or higher
- PyPDF2 library for PDF parsing

### Setup
```bash
# Install required dependencies
pip install PyPDF2

# Navigate to your tool directory
cd c:\Users\XEB2KOR\Desktop\BCM\Tool
```

## Usage

### Quick Start (Recommended)

For end-to-end conversion from PDF to CAPL in one command:

```bash
# Basic usage - outputs to default location
python workflow.py "TC_7778_SideMarker_FL_RR_Failure.pdf"

# Specify custom output file
python workflow.py "TC_7778_SideMarker_FL_RR_Failure.pdf" "my_test.can"
```

### Step-by-Step Usage

#### Step 1: Extract Test Case Data from PDF

```bash
# Extract to both JSON and text formats (default)
python pdf_test_case_extractor.py "TC_7778_SideMarker_FL_RR_Failure.pdf"

# Extract to JSON only
python pdf_test_case_extractor.py "TC_7778_SideMarker_FL_RR_Failure.pdf" json

# Extract to text format only
python pdf_test_case_extractor.py "TC_7778_SideMarker_FL_RR_Failure.pdf" text
```

**Output:**
- `TC_7778_SideMarker_FL_RR_Failure_extracted.json` - Structured test data in JSON
- `TC_7778_SideMarker_FL_RR_Failure_extracted.txt` - Human-readable formatted text

#### Step 2: Generate CAPL Test Code

```bash
# Generate CAPL code with default output name
python capl_code_generator.py "TC_7778_SideMarker_FL_RR_Failure_extracted.json"

# Generate CAPL code with custom output file
python capl_code_generator.py "TC_7778_SideMarker_FL_RR_Failure_extracted.json" "test_7778.can"
```

**Output:**
- `TC_7778_SideMarker_FL_RR_Failure_extracted_generated.can` (default)
- Or your specified `.can` file

## Extracted JSON Format

The JSON file structure contains all test case data organized as follows:

```json
{
  "metadata": {
    "id": "7778",
    "title": "TC_F027_SideMarker_FrontLeft_RearRight_Failure",
    "component": "rbg.Ferrari_BCM_Testing_F027",
    "configuration": "rbg.Ferrari_BCM_Testing_F027_Development_F244"
  },
  "pre_condition": {
    "si_sys_F027_LCU_Left_DRL_Feedback": "0",
    "si_sys_F027_LCU_Right_DRL_Feedback": "0",
    "si_sys_F027_LCU_Left_PL_Feedback": "0",
    "si_sys_F027_LCU_Right_PL_Feedback": "0"
  },
  "stimulations": [
    {
      "number": "1",
      "title": "Activation Side Marker FL RR",
      "actions": {
        "Proxy_write_LCU": "1",
        "Proxy_write_Side Maker": "1",
        "Stimulate sys_F040_KeySts": "ON(4)",
        "Stimulate sys_F858_NBC_Night_DaySts_for_IE": "Night(0)",
        "si_sys_F027_LCU_Left_PL_Feedback": "1",
        "si_sys_F027_LCU_Right_PL_Feedback": "1"
      },
      "expected_title": "Activation Side Marker FL RR",
      "expected_results": {
        "XCP_sys_F247_FrontPosLightCmd": "0->1",
        "XCP_sys_F247_RearPositionCmd": "0->1",
        "so_sys_F027_NBC_LeftPL": "0->1"
      }
    }
  ],
  "post_condition": {
    "si_sys_F027_LCU_Left_DRL_Feedback": "0",
    "si_sys_F027_LCU_Right_DRL_Feedback": "0",
    "Stimulate sys_F040_KeySts": "STOP(1)"
  }
}
```

## Generated CAPL Code Structure

The generated `.can` file contains:

1. **Header Section**
   - Test case metadata and documentation
   - Include statements for necessary libraries

2. **Pre-Condition Setup** (`setup_pre_conditions()`)
   - Signal initialization
   - System preparation
   - Initial waits for settling

3. **Stimulation Functions** (`stimulation_step_1()` through `stimulation_step_N()`)
   - Signal stimulation actions
   - Fault injection/removal
   - Expected result validations
   - DTC checking

4. **Post-Condition Cleanup** (`cleanup_post_conditions()`)
   - Signal reset
   - System restoration
   - Cleanup waits

5. **Helper Functions**
   - `checkActiveDTC()` - Verify specific DTC is active
   - `checkNoActiveDTC()` - Verify no DTCs present
   - `checkSignalValue()` - Validate signal values
   - `vtsCreateFault()` - Inject faults (SCG, OL)
   - `vtsRemoveFault()` - Remove faults
   - `vtsStimulateSignal()` - Stimulate CAN signals

6. **Main Test Function** (`test_7778()`)
   - Orchestrates complete test execution
   - Calls all setup, stimulation, and cleanup functions
   - Logs execution time and results

## Customization Guide

### Modifying the Extractor

To customize PDF parsing for your specific test case format:

1. Edit `TestCaseExtractor` class methods:
   - `extract_pre_condition()` - Modify regex patterns for your format
   - `extract_stimulations()` - Adjust stimulation parsing
   - `extract_post_condition()` - Customize cleanup extraction

Example - Modifying stimulation pattern:
```python
# In extract_stimulations() method
stim_pattern = r'Your_Custom_Pattern:\s*(.*?)(?=Next_Section|$)'
```

### Modifying the CAPL Generator

To customize generated CAPL code:

1. Edit `CAPLCodeGenerator` class methods:
   - `generate_helper_functions()` - Add or modify helper implementations
   - `generate_stimulation_section()` - Change how actions are coded
   - `parse_signal_value()` - Adjust value parsing logic

Example - Add custom helper function:
```python
def add_custom_helper(self) -> str:
    return """
// Custom helper for your specific use case
void myCustomHelper()
{
  // Your implementation here
}
"""
```

## Implementation Notes

The generated CAPL code contains **placeholder implementations** for the following critical functions that you must implement for your specific environment:

### Must Implement:

1. **`vtsCreateFault(nodeName, faultType)`**
   - Should inject SCG (Short Circuit to Ground) or OL (Open Load) faults
   - Use Vector vTESTstudio Fault Insertion API
   - Example for SCG: Create short circuit fault between signal and ground

2. **`vtsRemoveFault(nodeName)`**
   - Should remove previously injected faults
   - Restore normal signal behavior

3. **`vtsStimulateSignal(signalName, value)`**
   - Should send CAN signal values
   - Consider using CANoe or vTESTstudio signal injection APIs
   - Example: `write(signalName, value);`

4. **`checkActiveDTC(dtcCode)`**
   - Should query active DTC list
   - Return true if specified DTC is active
   - Use DBC or XCP protocol for DTC reading

5. **`checkNoActiveDTC()`**
   - Verify DTC list is empty
   - Return true if no DTCs are active

### Fault Types Supported:
- **SCG**: Short Circuit to Ground
- **OL**: Open Load (Open Circuit)

## Example Workflow

```bash
# Step 1: Extract data from PDF
python pdf_test_case_extractor.py "TC_7778_SideMarker_FL_RR_Failure.pdf" json

# Step 2: Review extracted data (optional)
type TC_7778_SideMarker_FL_RR_Failure_extracted.txt

# Step 3: Generate CAPL code
python capl_code_generator.py "TC_7778_SideMarker_FL_RR_Failure_extracted.json" "TC_7778.can"

# Step 4: Open generated CAPL in vTESTstudio
# - Review the code
# - Implement placeholder helper functions
# - Test and validate
```

## Batch Processing Multiple PDFs

To process multiple test case PDFs:

```python
# Create a batch_process.py script
from pathlib import Path
from pdf_test_case_extractor import TestCaseExtractor
from capl_code_generator import CAPLCodeGenerator

pdf_dir = Path(".")
extractor = TestCaseExtractor()
generator = CAPLCodeGenerator()

for pdf_file in pdf_dir.glob("*.pdf"):
    print(f"Processing {pdf_file.name}...")
    
    # Extract
    data = extractor.extract_all(str(pdf_file))
    json_file = pdf_file.parent / f"{pdf_file.stem}_extracted.json"
    extractor.save_as_json(data, str(json_file))
    
    # Generate
    capl_code = generator.generate_full_capl_code(data)
    can_file = pdf_file.parent / f"{pdf_file.stem}.can"
    generator.save_capl_file(capl_code, str(can_file))
    
    print(f"  → Generated {can_file.name}")
```

## Troubleshooting

### Common Issues

**Issue: "PyPDF2 is required" error**
```bash
pip install PyPDF2
```

**Issue: PDF text extraction is garbled or incomplete**
- Some PDFs may have embedded fonts or encoding issues
- Review the generated JSON manually
- Edit JSON file directly if needed
- Regenerate CAPL code

**Issue: Generated CAPL code has incorrect signal names**
- Check the extracted JSON for proper signal name parsing
- Modify `parse_signal_name()` method in CAPL generator
- Verify PDF contains exact signal names from DBC

**Issue: Helper functions need vTESTstudio-specific APIs**
- Review vTESTstudio documentation for:
  - Fault Insertion API
  - Signal stimulation functions
  - DTC reading protocols
- Implement helper functions based on your tools

## File Structure

```
c:\Users\XEB2KOR\Desktop\BCM\Tool\
├── pdf_test_case_extractor.py      # Main PDF extraction tool
├── capl_code_generator.py          # CAPL code generation tool
├── workflow.py                     # Integrated workflow
├── README.md                       # This file
├── TC_7778_SideMarker_FL_RR_Failure.pdf     # Input PDF
├── TC_7778_SideMarker_FL_RR_Failure_extracted.json    # Generated JSON
├── TC_7778_SideMarker_FL_RR_Failure_extracted.txt     # Generated text
└── TC_7778.can                     # Generated CAPL code
```

## API Reference

### TestCaseExtractor

```python
class TestCaseExtractor:
    def extract_pdf_text(pdf_path: str) -> str
    def extract_all(pdf_path: str) -> Dict[str, Any]
    def save_as_json(data: Dict, output_path: str) -> None
    def save_as_text(data: Dict, output_path: str) -> None
```

### CAPLCodeGenerator

```python
class CAPLCodeGenerator:
    def generate_full_capl_code(test_data: Dict) -> str
    def save_capl_file(capl_code: str, output_path: str) -> None
```

## Best Practices

1. **Always review extracted JSON** before generating CAPL
   - Verify all signals and values are correctly identified
   - Check stimulation steps are in proper order

2. **Implement helper functions carefully**
   - Test fault injection independently
   - Verify DTC reading works as expected
   - Validate signal stimulation

3. **Keep generated code as template**
   - Don't modify the generated code directly
   - Instead, regenerate from JSON if changes needed
   - Maintain customizations in separate include files

4. **Version control**
   - Track original PDF files
   - Keep extracted JSON for reference
   - Version control generated CAPL code

5. **Testing**
   - Execute generated CAPL in vTESTstudio sandbox first
   - Validate with known test signals
   - Gradually enable actual fault injection

## Support & Limitations

### Supported Test Case Elements
- ✅ Pre-conditions with signal assignments
- ✅ Multiple stimulation steps
- ✅ Fault injection (SCG, OL)
- ✅ Fault removal
- ✅ DTC verification
- ✅ Signal value transitions (0->1 format)
- ✅ Post-condition cleanup

### Known Limitations
- PDF parsing depends on consistent formatting
- Complex nested conditions may need manual adjustment
- Proprietary DBC extensions might need customization
- Helper functions are templates only (must be implemented)

## Future Enhancements

Potential improvements to consider:
- Support for other test case formats (XML, Excel)
- Automatic helper function implementation using DBC analysis
- Multi-layer fault scenarios
- Test report generation
- Integration with CANoe test environments
- Python-CAN backend support

## Contributing

To extend or improve this toolkit:

1. Create a new branch for your feature
2. Update the extraction/generation logic
3. Test with multiple PDF formats
4. Document changes in this README
5. Submit for review

## License & Usage

This toolkit is provided for automotive test automation in Vector tools environment.
Adapt as needed for your specific test requirements and hardware setup.

## Contact & Support

For issues or questions:
1. Review the generated JSON structure
2. Check vTESTstudio documentation
3. Verify DBC signal definitions
4. Test helper functions independently

---

**Last Updated:** November 2026  
**Version:** 1.0  
**Tested With:** Python 3.9+, PyPDF2 2.x+
