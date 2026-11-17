# Troubleshooting & FAQ - PDF to CAPL Toolkit

## Installation Issues

### Q: PyPDF2 is not installed
**Error:** `ImportError: No module named 'PyPDF2'` or `PDF_AVAILABLE = False`

**Solution:**
```bash
pip install PyPDF2
```

Verify installation:
```bash
python -c "import PyPDF2; print(PyPDF2.__version__)"
```

### Q: Python version is too old
**Error:** `SyntaxError` or various compatibility errors

**Solution:**
Requires Python 3.7+. Check your version:
```bash
python --version
```

If needed, install a newer Python version or update your existing one.

---

## PDF Extraction Issues

### Q: PDF text extraction is garbled or empty
**Symptoms:** 
- Generated JSON has empty sections
- Signal names are corrupted or incomplete

**Causes:**
- PDF uses embedded fonts
- PDF is scanned image (not text-based)
- PDF has unusual encoding

**Solutions:**
1. Convert PDF to text using Adobe Reader or online tools
2. Manually edit the extracted JSON file
3. Check PDF is not password-protected

**Example manual fix:**
```bash
# View extracted data
type TC_7778_extracted.json

# Edit if needed (using your favorite editor)
# Then regenerate CAPL:
python capl_code_generator.py TC_7778_extracted.json
```

### Q: Test case metadata not extracted correctly
**Check:**
1. PDF title format matches expected pattern
2. Test case ID is visible in PDF
3. Component and configuration sections are present

**Fix:** Edit JSON manually or modify extraction regex in `pdf_test_case_extractor.py`:

```python
# In extract_test_case_metadata() method
title_pattern = r'YOUR_PATTERN_HERE:\s*([^\n]+?)(?:\s*Creation Date|$)'
```

### Q: Signals or stimulations are not detected
**Causes:**
- Different naming conventions than expected
- Different formatting in PDF
- Typos in signal names

**Debug steps:**
```python
# Run extraction with debug output
from pdf_test_case_extractor import TestCaseExtractor

extractor = TestCaseExtractor()
test_data = extractor.extract_all("your_test.pdf")

# Print what was extracted
import json
print(json.dumps(test_data, indent=2))
```

**Fix:** Modify extraction patterns in `pdf_test_case_extractor.py`:

```python
# Example: To capture different signal pattern
signal_pattern = r'(YOUR_PREFIX_[^=\n]+|ANOTHER_PREFIX[^=\n]+)\s*=\s*([^\n]+)'
```

---

## CAPL Code Generation Issues

### Q: Generated CAPL code has errors
**Check:**
1. JSON file is valid (no syntax errors)
2. Signal names don't contain special characters
3. All required fields in JSON structure exist

**Validate JSON:**
```bash
python -m json.tool TC_7778_extracted.json > /dev/null && echo "Valid JSON"
```

### Q: Signal values are not parsed correctly
**Example:** `Stimulate sys_F040_KeySts to ON(4)` becomes `Stimulate` instead of `ON(4)`

**Fix:** Modify the `parse_signal_value()` method in `capl_code_generator.py`:

```python
def parse_signal_value(self, value_str: str) -> str:
    """Parse signal value from various formats."""
    # Handle "value" in parentheses format: "ON(4)" -> "4"
    if '(' in value_str and ')' in value_str:
        return value_str.split('(')[1].rstrip(')')
    # Handle "0->1" format: return target value "1"
    if '->' in value_str:
        return value_str.split('->')[-1].strip()
    # Handle plain values
    return value_str.strip().strip('"\'')
```

### Q: Helper functions are not implemented
**Message:** `// TODO: Implement XYZ function`

**Solution:** This is expected. You must implement these for your environment:

```capl
// Example implementation for vtsStimulateSignal
void vtsStimulateSignal(char signalName[], long value)
{
  // Using CANoe/vTESTstudio API
  write(signalName, value);
  
  // Or using XCP if available
  // vtsStimulateXCP(signalName, value);
}

// Example implementation for checkActiveDTC
int checkActiveDTC(char dtcCode[])
{
  // Read DTC list from vehicle
  char activeDTCs[256];
  read("ActiveDTCList", activeDTCs);
  
  // Check if our DTC is in the list
  if (StrFind(activeDTCs, dtcCode) >= 0)
    return 1;
  return 0;
}

// Example implementation for vtsCreateFault
void vtsCreateFault(char nodeName[], char faultType[])
{
  if (faultType == "SCG") {
    // Short Circuit to Ground: Connect signal to GND
    write("FaultInjection_SCG", nodeName);
  }
  else if (faultType == "OL") {
    // Open Load: Disconnect signal from circuit
    write("FaultInjection_OL", nodeName);
  }
}
```

---

## Workflow Issues

### Q: Workflow script fails with "PDF file not found"
**Solution:**
```bash
# Use absolute path
python workflow.py "C:\Users\XEB2KOR\Desktop\BCM\Tool\TC_7778.pdf"

# Or ensure you're in correct directory
cd C:\Users\XEB2KOR\Desktop\BCM\Tool
python workflow.py TC_7778.pdf
```

### Q: Workflow stops at extraction step
**Check extraction directly:**
```bash
python pdf_test_case_extractor.py "TC_7778.pdf" json
```

If this fails, see "PDF Extraction Issues" section above.

### Q: Workflow stops at generation step
**Check generation directly:**
```bash
python capl_code_generator.py "TC_7778_extracted.json"
```

If this fails, see "CAPL Code Generation Issues" section above.

---

## Testing & Validation

### Q: How do I test the generated CAPL code?
**Steps:**
1. Open vTESTstudio
2. Create new test module
3. Import the `.can` file
4. Implement placeholder helper functions
5. Run test execution

### Q: Signal values are not updated in test
**Check:**
1. Signal names match your DBC file exactly
2. Signal addresses are correct
3. Test environment (CANoe/vTESTstudio) is running
4. CAN bus simulation is active

### Q: DTCs are not being detected
**Check:**
1. DTC code format is correct (e.g., "B104813")
2. DTC storage is enabled in test configuration
3. `checkActiveDTC()` implementation is correct
4. Vehicle sends DTCs on expected bus/protocol

### Q: Fault injection is not working
**Troubleshoot:**
1. Verify fault types supported by your environment (SCG, OL)
2. Check node names match your hardware setup
3. Enable fault simulation in test configuration
4. Verify `vtsCreateFault()` and `vtsRemoveFault()` implementation

---

## Performance & Optimization

### Q: Script runs slowly on large PDFs
**Solutions:**
```python
# Option 1: Extract text first, then process
# Option 2: Use simple text format instead of JSON
python pdf_test_case_extractor.py large_test.pdf text

# Option 3: Extract only specific sections
# Edit pdf_test_case_extractor.py to skip unnecessary parsing
```

### Q: Generated CAPL code is very long
**Solutions:**
1. Split multiple test cases into separate files
2. Remove unnecessary stimulation steps
3. Combine similar stimulation steps

```python
# Example: Keep only first 2 stimulations
import json

with open("test_extracted.json", "r") as f:
    data = json.load(f)

data['stimulations'] = data['stimulations'][:2]  # Keep first 2

with open("test_modified.json", "w") as f:
    json.dump(data, f, indent=2)
```

---

## Customization Examples

### Q: How do I add custom fields to extracted data?

**Example:** Add severity level to stimulations

1. Modify `extract_stimulations()` in `pdf_test_case_extractor.py`:
```python
# Add after extracting title
severity_pattern = r'Severity:\s*([^\n]+)'
severity_match = re.search(severity_pattern, stim_content)
stimulation['severity'] = severity_match.group(1) if severity_match else "Normal"
```

2. Use in CAPL generation:
```python
# In generate_stimulation_section() method
severity = stim.get('severity', 'Normal')
lines.append(f"{self.indent(1)}// Severity: {severity}")
```

### Q: How do I add logging to understand what's extracted?

```python
# Add debug logging to extraction
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# In extract_stimulations()
logger.debug(f"Found stimulation {stim_num}: {stim_title}")
logger.debug(f"Actions: {actions}")
logger.debug(f"Expected results: {expected_data}")
```

### Q: How do I batch process multiple PDFs?

```python
# batch_process.py
from pathlib import Path
import subprocess
import sys

pdf_dir = Path(sys.argv[1] if len(sys.argv) > 1 else ".")

for pdf_file in pdf_dir.glob("*.pdf"):
    print(f"Processing {pdf_file.name}...")
    result = subprocess.run([
        sys.executable, "workflow.py",
        str(pdf_file)
    ])
    if result.returncode != 0:
        print(f"  ERROR: Failed to process {pdf_file.name}")
    else:
        print(f"  OK")

print("Batch processing complete")
```

---

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `FileNotFoundError: PDF file not found` | Wrong file path | Use absolute path or verify file exists |
| `JSONDecodeError` | Invalid JSON format | Validate JSON: `python -m json.tool file.json` |
| `KeyError: 'metadata'` | JSON missing expected structure | Check extracted JSON has required fields |
| `TypeError: NoneType object is not subscriptable` | None returned from extraction | Check PDF format, enable debug logging |
| `SyntaxError` in generated CAPL | Invalid signal names or values | Check signal parsing, verify DBC compatibility |

---

## Debugging Tips

### Enable Verbose Output
```python
# Add to any script
import sys
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Print Intermediate Results
```python
# Check what PDF extraction produces
extractor = TestCaseExtractor()
raw_text = extractor.extract_pdf_text("test.pdf")
print("RAW TEXT LENGTH:", len(raw_text))
print("FIRST 500 CHARS:")
print(raw_text[:500])
```

### Validate Each Step
```bash
# Step 1: Extract
python pdf_test_case_extractor.py test.pdf json

# Step 2: Validate JSON
python -c "import json; json.load(open('test_extracted.json'))" && echo "JSON valid"

# Step 3: Generate
python capl_code_generator.py test_extracted.json

# Step 4: Inspect output
head -50 test_extracted_generated.can
```

---

## Getting Help

### Where to Look
1. **This document** - Most common issues and solutions
2. **README.md** - Complete documentation and examples
3. **Source code comments** - Implementation details
4. **vTESTstudio documentation** - For helper function APIs

### Information to Provide
When asking for help, include:
1. PDF test case file (if possible)
2. Generated JSON output
3. Generated CAPL code
4. Full error message and stack trace
5. Python version and PyPDF2 version
6. Your vTESTstudio/CANoe version

### Quick Reference
```bash
# Check Python version
python --version

# Check PyPDF2 version
python -c "import PyPDF2; print(PyPDF2.__version__)"

# Run with debug output
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from pdf_test_case_extractor import TestCaseExtractor
extractor = TestCaseExtractor()
data = extractor.extract_all('test.pdf')
"
```

---

**Still having issues?** Review the source code comments in:
- `pdf_test_case_extractor.py` - Extraction logic
- `capl_code_generator.py` - Code generation logic
- `workflow.py` - Workflow orchestration
