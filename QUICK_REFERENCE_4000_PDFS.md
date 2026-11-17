# Processing 4000 PDFs - Quick Reference
## Complete Setup & Execution Guide

---

## 📦 What You Have

✅ **batch_pdf_converter.py** - Processes all PDFs with one command  
✅ **pdf_test_case_extractor.py** - Core extraction engine (improved Nov 17, 2026)  
✅ **check_conversion_progress.py** - Track conversion progress  
✅ **BATCH_CONVERSION_GUIDE.md** - Detailed documentation  

---

## 🚀 For 4000 PDFs: Three Approaches

### **APPROACH 1: Single Folder (Simple - Recommended)**
Best if all 4000 PDFs are in one folder.

```powershell
# Step 1: Copy all 4000 PDFs to one folder
# C:\Users\XEB2KOR\Desktop\BCM\Tool\

# Step 2: Run once
cd c:\Users\XEB2KOR\Desktop\BCM\Tool
.\.venv\Scripts\python.exe batch_pdf_converter.py

# Step 3: Monitor progress
.\.venv\Scripts\python.exe check_conversion_progress.py

# Step 4: Run again to catch any failures
.\.venv\Scripts\python.exe batch_pdf_converter.py
```

**Pros:** Simple, fast, automatic  
**Cons:** All files in one directory (might be slower for 4000)  
**Time Estimate:** ~60-90 minutes for 4000 PDFs

---

### **APPROACH 2: Batch Processing (Recommended for 4000+)**
Split 4000 PDFs into smaller batches.

```powershell
# Step 1: Create batch folders
mkdir Batch_01, Batch_02, Batch_03, Batch_04

# Step 2: Distribute PDFs (e.g., 1000 per batch)
# Copy PDFs_1-1000 → Batch_01
# Copy PDFs_1001-2000 → Batch_02
# Copy PDFs_2001-3000 → Batch_03
# Copy PDFs_3001-4000 → Batch_04

# Step 3: Process each batch
cd Batch_01
.\.venv\Scripts\python.exe ..\batch_pdf_converter.py
.\.venv\Scripts\python.exe ..\check_conversion_progress.py
cd ..

cd Batch_02
.\.venv\Scripts\python.exe ..\batch_pdf_converter.py
cd ..

# ... repeat for Batch_03, Batch_04
```

**Pros:** Better performance, monitor each batch  
**Cons:** More setup, manual folder creation  
**Time Estimate:** ~60-80 minutes (parallelizable)

---

### **APPROACH 3: Automated Batch Script (Advanced)**
Let PowerShell handle batch creation & processing.

```powershell
# Create: batch_process_all.ps1
$baseDir = "C:\Users\XEB2KOR\Desktop\BCM\Tool"
$batchSize = 1000
$pdfFiles = @(Get-ChildItem "$baseDir\*.pdf" | Select-Object -ExpandProperty FullName)
$batches = @()

# Split into batches
for ($i = 0; $i -lt $pdfFiles.Count; $i += $batchSize) {
    $batchNum = [int]($i / $batchSize) + 1
    $batchDir = "$baseDir\Batch_$('{0:D2}' -f $batchNum)"
    
    if (-not (Test-Path $batchDir)) { mkdir $batchDir }
    
    $pdfFiles[$i..($i + $batchSize - 1)] | Copy-Item -Destination $batchDir
    
    echo "Processing $batchDir..."
    Push-Location $batchDir
    & .\..\\.venv\Scripts\python.exe ..\batch_pdf_converter.py
    Pop-Location
}

echo "All batches complete!"
```

**Pros:** Fully automated  
**Cons:** More complex, requires PowerShell knowledge  
**Time Estimate:** ~60-80 minutes

---

## 📊 Expected Performance

| Approach | Setup Time | Processing Time | Total |
|----------|-----------|-----------------|-------|
| Single Folder | 5 min | 90 min | **95 min** |
| Batch (4 batches) | 15 min | 75 min | **90 min** |
| Automated Script | 10 min | 75 min | **85 min** |

**Hardware Impact:**
- SSD: ~1 PDF/sec = ~67 minutes for 4000
- HDD: ~0.5 PDF/sec = ~133 minutes for 4000
- RAM: 4GB+ recommended
- CPU: Single-threaded (can't parallelize due to output file naming)

---

## 🔄 Real-Time Monitoring

### Track conversion while running:

```powershell
# Terminal 1: Run conversion
.\.venv\Scripts\python.exe batch_pdf_converter.py

# Terminal 2: Monitor progress (every 30 seconds)
while ($true) {
    .\.venv\Scripts\python.exe check_conversion_progress.py
    Start-Sleep -Seconds 30
}

# Terminal 3: Show live JSON statistics
while ($true) {
    .\.venv\Scripts\python.exe check_conversion_progress.py --stats
    Start-Sleep -Seconds 60
}
```

---

## ✅ Quality Assurance Checklist

After converting 4000 PDFs:

```powershell
# Check 1: Count converted files
Get-ChildItem *.txt | Measure-Object

# Check 2: Verify JSON structure
$jsons = Get-ChildItem "*_extracted.json" -ErrorAction SilentlyContinue
Write-Host "Total JSON files: $($jsons.Count)"

# Check 3: Spot-check a few files
Get-Content (Get-ChildItem "TC_*.txt" | Select-Object -First 1 | Select-Object -ExpandProperty FullName) | Select-Object -First 50

# Check 4: Run statistics
.\.venv\Scripts\python.exe check_conversion_progress.py --stats

# Check 5: Look for errors
Get-ChildItem *.json | ForEach-Object {
    $content = Get-Content $_.FullName | ConvertFrom-Json
    if ($content.stimulations.Count -eq 0) {
        Write-Host "ERROR: No stimulations in $_"
    }
}
```

---

## 🔧 If Processing Fails

### Restart safely:
```powershell
# 1. See what's converted
.\.venv\Scripts\python.exe check_conversion_progress.py

# 2. Continue processing (skips already-done files)
.\.venv\Scripts\python.exe batch_pdf_converter.py

# 3. For stuck/corrupted files:
# Option A: Delete outputs and retry
Remove-Item "*_extracted.json", "TC_*.txt" -ErrorAction SilentlyContinue
.\.venv\Scripts\python.exe batch_pdf_converter.py

# Option B: Move problematic PDF to separate folder
mkdir problem_pdfs
Move-Item problem_pdf.pdf problem_pdfs\
.\.venv\Scripts\python.exe batch_pdf_converter.py
```

---

## 📈 Output Organization

### After 4000 PDFs are converted:

```
C:\Users\XEB2KOR\Desktop\BCM\Tool\
├── TC_26107_*.txt                    (4000 formatted TXT files)
├── TC_7778_*.txt
├── TC_9716_*.txt
├── ...
├── 26107_extracted.json              (4000 JSON files)
├── 7778_extracted.json
├── ...
└── [extracted TXT files]             (optional - duplicate of TC_*.txt)
```

**Total Output Size:** ~400-500 MB (depending on PDF complexity)

---

## 🎯 Next Steps After Conversion

### Option 1: Generate CAPL Test Modules
```powershell
# Generate CAPL code from JSON
.\.venv\Scripts\python.exe capl_code_generator.py \
    "26107 - TC_F027_LCU_Feedback_Plausibility_RightPL_Key_OFF_extracted.json"
```

### Option 2: Analyze Extracted Data
```python
import json
from pathlib import Path

# Load all JSON files
json_files = Path('.').glob('*_extracted.json')
all_data = []

for json_file in json_files:
    with open(json_file) as f:
        data = json.load(f)
        all_data.append(data)

# Generate statistics
print(f"Total test cases: {len(all_data)}")
print(f"Avg stimulations: {sum(len(d['stimulations']) for d in all_data) / len(all_data)}")

# Export to CSV
import csv
with open('test_case_summary.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Test ID', 'Title', 'Stimulations', 'Pre-Cond Items', 'Post-Cond Items'])
    for data in all_data:
        writer.writerow([
            data['test_case_id'],
            data['test_case_title'],
            len(data['stimulations']),
            len(data['pre_condition']),
            len(data['post_condition'])
        ])
```

### Option 3: Import to Excel/Database
```powershell
# Export all pre-conditions to Excel
$jsons = Get-ChildItem "*_extracted.json"
$results = @()

foreach ($json in $jsons) {
    $data = Get-Content $json | ConvertFrom-Json
    foreach ($precond in $data.pre_condition.PSObject.Properties) {
        $results += [PSCustomObject]@{
            TestID = $data.test_case_id
            Signal = $precond.Name
            Value = $precond.Value
        }
    }
}

$results | Export-Csv "all_pre_conditions.csv" -NoTypeInformation
```

---

## 🚨 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Process terminates silently" | PDF might be corrupted - move to problem folder |
| "Only 50% of PDFs converted" | Rerun converter - it skips successful ones |
| "JSON files empty" | PDF might be image-based (not text) |
| "Very slow processing" | Use SSD, close other apps, check disk usage |
| "Missing signals in output" | Check BATCH_CONVERSION_GUIDE.md signal patterns |

---

## 📞 Support Commands

```powershell
# Help & Information
.\.venv\Scripts\python.exe batch_pdf_converter.py --help
.\.venv\Scripts\python.exe pdf_test_case_extractor.py --help

# Single PDF test
.\.venv\Scripts\python.exe pdf_test_case_extractor.py "test_pdf.pdf"

# Check Python version
.\.venv\Scripts\python.exe --version

# Verify dependencies
.\.venv\Scripts\pip list | grep PyPDF2
```

---

## ✨ Success Metrics

You'll know it's working when:
- ✅ Each PDF → 1 TXT file + 1 JSON file
- ✅ TXT files are readable and formatted
- ✅ JSON contains pre_condition, stimulations, post_condition
- ✅ All signal types captured (si_sys_, Proxy_, XCP_sys_, so_sys_)
- ✅ Processing time is consistent (~1 PDF/sec on SSD)
- ✅ No error messages in final summary

---

## 📋 Checklist Before Processing 4000 PDFs

- [ ] All 4000 PDFs in correct folder
- [ ] Venv activated (.venv present)
- [ ] PyPDF2 installed (`pip list | grep PyPDF2`)
- [ ] 1-2 GB free disk space
- [ ] Read BATCH_CONVERSION_GUIDE.md
- [ ] Test with 1-2 PDFs first
- [ ] Have patience - ~90 minutes total time

---

**Version:** 2.0 | **Date:** November 17, 2026  
**Tested On:** Windows 11, Python 3.14, PyPDF2 3.0.1
