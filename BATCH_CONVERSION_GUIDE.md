# PDF to TXT Batch Conversion Guide
## For 4000+ PDF Test Cases

---

## 🚀 Quick Start

### Step 1: Add Your PDFs
Place all your PDF test case files in: `c:\Users\XEB2KOR\Desktop\BCM\Tool\`

### Step 2: Run the Batch Converter
```powershell
cd c:\Users\XEB2KOR\Desktop\BCM\Tool
.\.venv\Scripts\python.exe batch_pdf_converter.py
```

### Step 3: Results
- **One PDF → One TXT file** (one-to-one mapping)
- Each PDF gets extracted to both JSON and formatted TXT
- Files automatically skip if already converted

---

## 📊 Output Structure

### For Each PDF, You Get:
1. **`TC_XXXXX_TestCase_Name.txt`** ← Formatted readable text file
2. **`XXXXX - TestCase_Name_extracted.json`** ← Structured JSON data
3. **`XXXXX - TestCase_Name_extracted.txt`** ← Raw extracted text

### Example:
```
Input PDF:  26107 - TC_F027_LCU_Feedback_Plausibility_RightPL_Key_OFF.pdf
Output:
  ✓ TC_26107_TC_F027_LCU_Feedback_Plausibility_RightPL_Key_OFF.txt
  ✓ 26107 - TC_F027_LCU_Feedback_Plausibility_RightPL_Key_OFF_extracted.json
  ✓ 26107 - TC_F027_LCU_Feedback_Plausibility_RightPL_Key_OFF_extracted.txt
```

---

## ✅ What Gets Extracted

### Pre-Condition Section
- ✅ `si_sys_*` signal assignments
- ✅ `Proxy_*` signal assignments  
- ✅ `Stimulate sys_*` commands
- ✅ Comments/documentation (preserved with `//`)

### Stimulation Sections (1-N)
- ✅ Stimulation title and description
- ✅ All action commands
  - Stimulate statements
  - Signal assignments
  - Wait timing
  - Fault injection (SCG/OL)
- ✅ Expected results with:
  - Signal transitions (0->1, 0->100, etc.)
  - DTC entries (active/passive)
  - NO_DTC indicators

### Post-Condition Section
- ✅ Cleanup `Stimulate` commands
- ✅ Signal resets
- ✅ Proxy signal resets

---

## 📈 Extraction Improvements (November 17, 2026)

### Fixed in Latest Version:
1. **Proxy Signal Capture** 
   - Now detects `Proxy_write_Side_Marker` and similar patterns
   - Was missing before, now included

2. **Better Value Capture**
   - Captures values with comments: `0 // 0x0 - Not_Active`
   - Handles multi-word values correctly

3. **Comprehensive Signal Matching**
   - `si_sys_*` ✅
   - `Proxy_*` ✅  
   - `XCP_sys_*` ✅
   - `so_sys_*` ✅
   - `Stimulate sys_*` ✅

### Results on 3 Test Cases:
| Test Case | Pre-Cond Items | Stimulations | Post-Cond Items |
|-----------|----------------|--------------|-----------------|
| TC_26107  | 7 ✅          | 7            | 4 ✅            |
| TC_7778   | 3 ✅          | 5            | 5 ✅            |
| TC_9716   | 5 ✅          | 7            | 4 ✅            |

---

## 🔄 How to Process 4000 PDFs

### Method 1: Single Command (Recommended)
```powershell
# Process ALL PDFs at once
.\.venv\Scripts\python.exe batch_pdf_converter.py

# Then run again to skip already-processed files and do new ones
.\.venv\Scripts\python.exe batch_pdf_converter.py
```

### Method 2: Batch by Folder (If PDFs are in subfolders)
```powershell
# Create subfolders: PDF_Batch_1, PDF_Batch_2, etc.
# Run converter in each folder separately

cd .\PDF_Batch_1
.\.venv\Scripts\python.exe ..\batch_pdf_converter.py

cd ..\PDF_Batch_2
.\.venv\Scripts\python.exe ..\batch_pdf_converter.py
```

### Method 3: Monitor Progress (Real-time)
```powershell
# Run with verbose output
.\.venv\Scripts\python.exe batch_pdf_converter.py | Tee-Object -FilePath conversion_log.txt
```

---

## 🛠️ System Architecture

### Core Components:

#### 1. **pdf_test_case_extractor.py**
- Reads PDF test cases
- Extracts structured data:
  - Pre-condition signals
  - Stimulation actions & expected results
  - Post-condition signals
  - DTC entries
  - Fault injection details
- Outputs JSON + formatted text

#### 2. **batch_pdf_converter.py**
- Finds all PDFs in directory
- Processes each one automatically
- Skips already-converted files
- Shows progress summary

#### 3. **workflow.py** (Optional)
- Orchestrates extraction → CAPL generation
- For one-off conversions: `python workflow.py "TC_XXXX.pdf"`

---

## 📋 JSON Structure Example

```json
{
  "test_case_id": "26107",
  "test_case_title": "TC_F027_LCU_Feedback_Plausibility_RightPL_Key_OFF",
  "pre_condition": {
    "Stimulate sys_F040_KeySts to": "ON(4)",
    "si_sys_TcSen_bTerm15_1": "1 // 0x0 - Not_Active , 0x1 - Active",
    "Proxy_write_Side_Marker": "0 // 0 - Enabled , 1 - Disabled",
    ...
  },
  "stimulations": [
    {
      "number": "1",
      "title": "Activation of Follow Me Home Mode",
      "actions": {
        "si_sys_F027_LCU_Left_PL_Feedback": "1",
        "wait": "0.3"
      },
      "expected_results": {
        "XCP_sys_F247_FrontPosLightCmd": "0->1",
        "so_sys_F027_NBC_LeftPL": "0->1",
        "NO_DTC": true
      }
    }
  ],
  "post_condition": { ... }
}
```

---

## ⚙️ Configuration & Customization

### Add New Signal Patterns
Edit `pdf_test_case_extractor.py`:

**Pre-Condition/Post-Condition** (Lines 70-115, 228-270):
```python
# Add new prefixes to this regex:
for m in re.finditer(r'(si_sys_[^=\s]+|Proxy_[^=\s]+|YOUR_PREFIX_[^=\s]+)\s*=\s*(...', content):
```

**Expected Results** (Lines 130-150):
```python
# Add new signal types to this regex:
for m in re.finditer(r'(XCP_sys_|so_sys_|Proxy_|YOUR_TYPE_)[^=\s]+\s*=\s*(...', expected_content):
```

### Adjust Text Extraction
Edit cleanup function:
```python
def remove_urls(self, text: str) -> str:
    """Remove embedded URLs and hyperlinks"""
    # Customize URL patterns here
```

---

## 🐛 Troubleshooting

### Issue: "No PDF files found"
**Solution:** 
- Check PDFs are in the working directory
- Verify file extension is exactly `.pdf` (lowercase)

### Issue: "TypeError: 'list' object is not subscriptable"
**Solution:** 
- Ensure PyPDF2 is installed: `.\.venv\Scripts\pip install PyPDF2==3.0.1`

### Issue: Some signals missing in output
**Solution:** 
- Check if signal prefix matches extraction patterns
- Add new prefix to regex patterns (see Configuration section)
- Review the PDF to ensure text is extractable (not image-based)

### Issue: Conversion stops/crashes
**Solution:** 
- Rerun the batch converter - it will skip completed files
- Check for corrupted PDFs (try converting individually)

---

## 📊 Performance Expectations

| Number of PDFs | Estimated Time | Hardware |
|----------------|----------------|----------|
| 10 | ~10 seconds | Standard PC |
| 100 | ~90 seconds | Standard PC |
| 1,000 | ~15 minutes | Standard PC |
| 4,000 | ~60 minutes | Standard PC |

**Optimization Tips:**
- Run on SSD (faster than HDD)
- Close other applications
- Use PowerShell (faster than CMD)

---

## ✨ Sample Output (Formatted TXT)

```
======================================================================
PRE-CONDITION
======================================================================
Stimulate sys_F040_KeySts to = ON(4)
si_sys_TcSen_bTerm15_1 = 1 // 0x0 - Not_Active , 0x1 - Active
si_sys_TcSen_bTerm15_2 = 1 // 0x0 - Not_Active , 0x1 - Active
Stimulate sys_F858_NBC_Night_DaySts_for_IE to = Night(0)
Proxy_write_Side_Marker = 0 // 0 - Enabled , 1 - Disabled

======================================================================
STIMULATION-1: Activation of Follow Me Home Mode
======================================================================

Actions:
  si_sys_F027_LCU_Left_PL_Feedback = 1
  si_sys_F027_LCU_Right_PL_Feedback = 1

Expected Results: Following Results Should be Observed
  XCP_sys_F247_FrontPosLightCmd = 0->1
  so_sys_F027_NBC_LeftPL = 0->1
  so_sys_F027_NBC_RightPL = 0->1
  NO_DTC

======================================================================
POST-CONDITION
======================================================================
Stimulate sys_F040_KeySts to = STOP(1)
Stimulate sys_F858_NBC_Night_DaySts_for_IE to = Night(0)
si_sys_LCC_RearFog_Button = 0
```

---

## 🎯 Next Steps

1. ✅ Verify extracted TXT files are correct
2. ✅ Check JSON structure matches your needs
3. ✅ Run batch converter on all 4000 PDFs
4. 📊 Generate statistics/reports from JSON files
5. 🤖 (Optional) Generate CAPL test modules: `python capl_code_generator.py`

---

## 📞 Support

For issues:
1. Check TROUBLESHOOTING section above
2. Review pdf_test_case_extractor.py comments
3. Verify PDF is text-extractable (open in Adobe Reader - check if text can be selected)
4. Test with a single PDF first: `.\.venv\Scripts\python.exe pdf_test_case_extractor.py "test.pdf"`

---

**Last Updated:** November 17, 2026  
**Version:** 2.0 (Proxy_* signal support added)
