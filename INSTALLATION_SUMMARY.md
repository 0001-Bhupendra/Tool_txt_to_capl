# PDF to CAPL Test Case Generation Toolkit
## Complete Installation & Usage Summary

---

## 📦 What You Have

A complete Python toolkit for converting PDF test case documents into automated CAPL test modules for Vector vTESTstudio.

### Created Files

```
c:\Users\XEB2KOR\Desktop\BCM\Tool\
├── pdf_test_case_extractor.py     ← PDF parsing & data extraction
├── capl_code_generator.py          ← CAPL code generation
├── workflow.py                     ← Integrated pipeline
├── requirements.txt                ← Dependencies
├── README.md                       ← Full documentation
├── TROUBLESHOOTING.md              ← FAQ & solutions
├── QUICK_START.py                  ← Usage examples
├── EXAMPLE_OUTPUTS.py              ← Sample output formats
└── INSTALLATION_SUMMARY.md         ← This file
```

---

## 🚀 Quick Start (60 seconds)

### Step 1: Install Dependencies
```bash
pip install PyPDF2
```

### Step 2: Navigate to Directory
```bash
cd c:\Users\XEB2KOR\Desktop\BCM\Tool
```

### Step 3: Run Complete Workflow
```bash
python workflow.py "TC_7778_SideMarker_FL_RR_Failure.pdf"
```

### Result
Three files are generated:
1. `TC_7778_SideMarker_FL_RR_Failure_extracted.json` - Structured test data
2. `TC_7778_SideMarker_FL_RR_Failure_extracted.txt` - Human-readable format
3. `TC_7778_SideMarker_FL_RR_Failure_extracted_generated.can` - CAPL test code

---

## 📋 Usage Examples

### Example 1: Extract Only
```bash
# Extract to JSON format
python pdf_test_case_extractor.py TC_7778.pdf json

# Extract to text format
python pdf_test_case_extractor.py TC_7778.pdf text

# Extract to both formats (default)
python pdf_test_case_extractor.py TC_7778.pdf
```

### Example 2: Generate CAPL from JSON
```bash
# Using default output name
python capl_code_generator.py TC_7778_extracted.json

# Using custom output name
python capl_code_generator.py TC_7778_extracted.json my_test.can
```

### Example 3: Python API Usage
```python
from pdf_test_case_extractor import TestCaseExtractor
from capl_code_generator import CAPLCodeGenerator

# Extract data
extractor = TestCaseExtractor()
test_data = extractor.extract_all("TC_7778.pdf")

# Generate code
generator = CAPLCodeGenerator()
capl_code = generator.generate_full_capl_code(test_data)
generator.save_capl_file(capl_code, "TC_7778.can")
```

---

## 🔧 Setup Verification

```bash
# Verify Python installation
python --version
# Expected: Python 3.7 or higher

# Verify PyPDF2 installation
python -c "import PyPDF2; print('PyPDF2 OK')"
# Expected: PyPDF2 OK

# Test extraction
python pdf_test_case_extractor.py TC_7778_SideMarker_FL_RR_Failure.pdf json
# Expected: JSON file created successfully

# Test generation
python capl_code_generator.py TC_7778_SideMarker_FL_RR_Failure_extracted.json
# Expected: CAPL code generated successfully
```

---

## 📊 Data Flow

```
┌─────────────────────────┐
│   PDF Test Case File    │
│  (TC_7778.pdf)         │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│   pdf_test_case_extractor.py            │
│  - Parse test case structure             │
│  - Extract pre-conditions                │
│  - Extract stimulation steps             │
│  - Extract expected results              │
│  - Extract post-conditions               │
└────────┬──────────────────────────────────┘
         │
         ├─→ TC_7778_extracted.json
         └─→ TC_7778_extracted.txt
         │
         ▼
┌─────────────────────────────────────────┐
│   capl_code_generator.py                │
│  - Convert JSON to CAPL structure        │
│  - Generate test functions               │
│  - Add helper functions                  │
│  - Format and save code                  │
└────────┬──────────────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│   CAPL Test Module      │
│  (TC_7778.can)         │
│                         │
│  - setup_pre_conditions │
│  - stimulation_step_1-5 │
│  - cleanup_post_cond    │
│  - helper functions     │
│  - test() main function │
└─────────────────────────┘
```

---

## 🎯 Key Features

### PDF Extraction
✅ Automatic metadata extraction (ID, title, component)
✅ Pre-condition signal assignments
✅ Stimulation step parsing with actions
✅ Expected results (signal transitions, DTCs)
✅ Post-condition cleanup
✅ Fault type detection (SCG, Open Load)
✅ Multiple output formats (JSON, text)

### CAPL Generation
✅ Complete test module structure
✅ Function for each test phase
✅ Automatic helper function templates
✅ Main test orchestration function
✅ Well-documented and formatted code
✅ Customizable output

### Workflow
✅ Single-command end-to-end execution
✅ Error handling and validation
✅ Progress reporting
✅ Flexible file naming

---

## ⚙️ Configuration

### Changing Output Formats

**Extract only text:**
```bash
python pdf_test_case_extractor.py test.pdf text
```

**Extract only JSON:**
```bash
python pdf_test_case_extractor.py test.pdf json
```

**Extract both (default):**
```bash
python pdf_test_case_extractor.py test.pdf
```

### Customizing Signal Names

Edit `parse_signal_name()` in `capl_code_generator.py`:
```python
def parse_signal_name(self, signal: str) -> str:
    """Extract clean signal name from various formats."""
    signal = signal.replace('Stimulate', '').strip()
    return signal.split('(')[0].strip()
```

### Customizing Extraction Patterns

Edit regex patterns in `pdf_test_case_extractor.py`:
```python
# Example: Modify pre-condition extraction
pattern = r'Your_Custom_Pattern:\s*(.*?)(?=Next_Section|$)'
```

---

## 🧪 Testing

### Manual Verification

```bash
# 1. Extract data
python pdf_test_case_extractor.py TC_7778.pdf json

# 2. Inspect JSON
type TC_7778_extracted.json
# or use a JSON viewer

# 3. Generate CAPL
python capl_code_generator.py TC_7778_extracted.json TC_7778.can

# 4. Review CAPL
type TC_7778.can
# or open in vTESTstudio
```

### Validation Checklist

- [ ] PDF file exists and is readable
- [ ] Extraction produces valid JSON
- [ ] JSON contains expected test data
- [ ] CAPL code generates without errors
- [ ] CAPL code has correct function names
- [ ] Helper functions marked as TODO
- [ ] Generated code matches test case steps

---

## ⚠️ Important Notes

### Placeholder Functions

The generated CAPL code contains skeleton implementations for:

```
vtsCreateFault()      ← Inject faults (SCG, OL)
vtsRemoveFault()      ← Remove faults
checkActiveDTC()      ← Verify DTCs
checkNoActiveDTC()    ← Verify no DTCs
vtsStimulateSignal()  ← Send CAN signals
```

**You must implement these** for your specific environment (vTESTstudio/CANoe).

### Environment Dependencies

Your implementation will likely need:
- Vector vTESTstudio or CANoe
- DBC file(s) for signal definitions
- Fault simulation API access
- DTC storage and querying
- CAN bus communication layer

### PDF Requirements

The toolkit works best with:
- Text-based PDFs (not scanned images)
- Consistent formatting
- Standard test case structure
- English language documents

---

## 🐛 Troubleshooting

### Common Issues

**PyPDF2 not installed:**
```bash
pip install PyPDF2
```

**PDF not found:**
```bash
# Use absolute path
python workflow.py "C:\Users\XEB2KOR\Desktop\BCM\Tool\TC_7778.pdf"
```

**JSON extraction incomplete:**
1. Check PDF format and encoding
2. Review extracted text format
3. Edit JSON manually if needed

**CAPL code has errors:**
1. Validate JSON syntax
2. Check signal naming conventions
3. Review generated code for typos

For more solutions, see **TROUBLESHOOTING.md**

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Complete documentation & API reference |
| TROUBLESHOOTING.md | FAQ, errors, and solutions |
| QUICK_START.py | Usage examples and demonstrations |
| EXAMPLE_OUTPUTS.py | Sample JSON, CAPL, and text outputs |
| requirements.txt | Python dependencies |

---

## 🔄 Batch Processing

Process multiple PDFs:

```bash
# Windows batch processing
for %F in (*.pdf) do python workflow.py "%F"

# Or create a Python script
# See batch_process_example in QUICK_START.py
```

---

## 📝 Project Structure

```
Components:
├─ Extraction Layer
│  └─ pdf_test_case_extractor.py
│
├─ Generation Layer
│  └─ capl_code_generator.py
│
├─ Orchestration Layer
│  └─ workflow.py
│
└─ Documentation Layer
   ├─ README.md
   ├─ TROUBLESHOOTING.md
   ├─ QUICK_START.py
   └─ EXAMPLE_OUTPUTS.py
```

---

## 🎓 Learning Path

1. **Install & Setup** (5 min)
   - Install PyPDF2
   - Verify installation

2. **Quick Start** (10 min)
   - Run workflow on example PDF
   - Review generated files

3. **Understand Outputs** (15 min)
   - Review extracted JSON
   - Review generated CAPL code
   - Check text format

4. **Customize** (20 min)
   - Modify extraction patterns if needed
   - Adjust CAPL code generation
   - Implement helper functions

5. **Testing** (30 min)
   - Open CAPL in vTESTstudio
   - Test signal handling
   - Validate fault injection
   - Run test cases

---

## ✅ Verification Checklist

Before using in production:

- [ ] Python 3.7+ installed
- [ ] PyPDF2 successfully installed
- [ ] All script files present in tool directory
- [ ] Documentation reviewed
- [ ] Example PDF processed successfully
- [ ] Generated JSON structure verified
- [ ] Generated CAPL code reviewed
- [ ] Helper functions planned/scoped
- [ ] vTESTstudio environment ready
- [ ] DBC files available
- [ ] Test environment configured

---

## 🚀 Next Steps

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run your first extraction:**
   ```bash
   python workflow.py "TC_7778_SideMarker_FL_RR_Failure.pdf"
   ```

3. **Review the outputs:**
   - Open `*_extracted.json` to see structured data
   - Open `*_extracted.txt` for human-readable format
   - Open `*_generated.can` to see CAPL code

4. **Implement in vTESTstudio:**
   - Import the .can file
   - Implement helper functions
   - Execute and validate

5. **Process your test cases:**
   - For single PDF: `python workflow.py "your_test.pdf"`
   - For multiple: Loop over PDFs or batch process

---

## 📞 Support Resources

- **This Document** - Installation and quick reference
- **README.md** - Complete documentation
- **TROUBLESHOOTING.md** - Common issues and solutions
- **QUICK_START.py** - Usage examples
- **EXAMPLE_OUTPUTS.py** - Sample outputs
- **Source Code** - Well-commented implementations

---

## 📄 License & Usage

This toolkit is provided for automotive test automation in Vector tools environment. Customize as needed for your specific requirements.

---

**Version:** 1.0  
**Updated:** November 2026  
**Status:** Ready for Use

For questions or issues, refer to TROUBLESHOOTING.md or review source code comments.

---

## Quick Command Reference

```bash
# Install
pip install PyPDF2

# Single test case
python workflow.py "test.pdf"

# Extract only
python pdf_test_case_extractor.py "test.pdf" json

# Generate from JSON
python capl_code_generator.py "test_extracted.json"

# Batch process (Windows)
for %F in (*.pdf) do python workflow.py "%F"

# Verify installation
python -c "import PyPDF2; print('OK')"
```

---

**Ready to start?** Run: `python workflow.py "TC_7778_SideMarker_FL_RR_Failure.pdf"`
