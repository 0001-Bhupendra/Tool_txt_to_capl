# 🌐 PDF Test Case Converter - Team Edition
## Share This Tool With Your Teammates!

---

## 🚀 Quick Start for Teammates

### **For Windows Users:**

**Step 1: Get the Tool**
```
Folder: c:\Users\XEB2KOR\Desktop\BCM\Tool\
```

**Step 2: Double-click to Launch**
```
Run: launch_app.py
```
OR in PowerShell:
```powershell
python launch_app.py
```

**Step 3: Wait for Browser to Open**
- Application opens at: `http://localhost:8501`
- If not auto-opened, copy URL to browser

**Step 4: Use the Tool**
✅ Upload PDFs  
✅ Click "Start Conversion"  
✅ Download converted files  

---

## 🎯 For Linux/Mac Users:

```bash
cd /path/to/BCM/Tool
python3 launch_app.py
```

---

## 📚 What Teammates Will See

### **Tab 1: Convert** 🔄
- Upload PDF files (single or multiple)
- Real-time progress bar
- Extraction summary with counts
- Status: Success/Error for each file

### **Tab 2: Download** 📥
- Download individual TXT/JSON files
- Download all as ZIP archive
- Simple one-click downloads

### **Tab 3: Statistics** 📊
- Conversion metrics
- Pre-condition/Stimulation/Post-condition breakdown
- Distribution charts

### **Tab 4: Help** ❓
- Complete documentation
- Troubleshooting guide
- Example usage
- Signal types explained

---

## 🔧 System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.8+ | 3.10+ |
| RAM | 1 GB | 4 GB |
| Disk Space | 500 MB | 2 GB |
| OS | Windows 7+ | Windows 10+ |

---

## 🛠️ Setup Instructions (For IT/Admins)

### **One-Time Setup:**

```bash
# Navigate to tool directory
cd c:\Users\XEB2KOR\Desktop\BCM\Tool

# Install Streamlit (if not already installed)
pip install -r app_requirements.txt

# Test the app
python launch_app.py
```

### **For Network/Shared Drive:**

```bash
# To run on specific host/port
streamlit run app.py --server.address 0.0.0.0 --server.port 8501

# Team members access via: http://[your-ip]:8501
```

---

## 📋 Features for Teammates

✅ **Easy File Upload**
- Drag & drop multiple PDFs
- Simple file browser interface

✅ **Automatic Processing**
- One-click conversion
- Real-time progress tracking
- Error handling with clear messages

✅ **Multiple Download Formats**
- Individual TXT files
- Individual JSON files
- Batch ZIP download

✅ **Data Visualization**
- Extraction statistics
- Chart breakdowns
- Summary metrics

✅ **User-Friendly Help**
- In-app documentation
- Troubleshooting guide
- Example outputs

---

## 🎓 Tutorial for Teammates

### **Converting PDF Test Cases:**

1. **Open Application**
   ```
   Run: launch_app.py
   Wait for browser to open
   ```

2. **Go to Convert Tab** (Default)
   ```
   Already on the right tab!
   ```

3. **Upload PDFs**
   ```
   Click "Upload PDF files"
   Select one or many PDFs
   Files appear in list
   ```

4. **Start Conversion**
   ```
   Click "🚀 Start Conversion"
   Watch progress bar
   See results table
   ```

5. **Download Results**
   ```
   Go to "Download" tab
   Choose format (Individual or ZIP)
   Click download button
   Files saved to Downloads folder
   ```

### **Example Workflow:**

```
Input: 5 PDF test case files
       ↓
Upload to web tool
       ↓
Click Start Conversion
       ↓
Wait ~5 seconds
       ↓
View results (all 5 successful)
       ↓
Download as ZIP
       ↓
Output: converted_test_cases_20261117.zip
        ├─ TC_26107_*.txt
        ├─ 26107_*_extracted.json
        ├─ TC_7778_*.txt
        ├─ 7778_*_extracted.json
        └─ ... (and more)
```

---

## 💾 Output Files Explained

### **TXT File** (Readable Format)
```
TC_[ID]_[Test_Name].txt

Contains:
- TEST CASE METADATA
- PRE-CONDITION (formatted)
- STIMULATION-1, STIMULATION-2, ...
  - Actions
  - Expected Results
- POST-CONDITION
```

**Use for:** Documentation, review, sharing

### **JSON File** (Structured Format)
```
[ID]_[Test_Name]_extracted.json

Contains:
{
  "test_case_id": "26107",
  "test_case_title": "...",
  "pre_condition": { ... },
  "stimulations": [ ... ],
  "post_condition": { ... }
}
```

**Use for:** Data processing, automation, database import

---

## 🔐 Security & Privacy

- ✅ Files processed locally (no cloud upload)
- ✅ Temporary files auto-deleted after download
- ✅ No personal data collection
- ✅ HTTPS ready for network deployment

---

## ⚡ Performance Tips

| Scenario | Time | Notes |
|----------|------|-------|
| 1 PDF | ~1 sec | Very fast |
| 5 PDFs | ~5 sec | Still instant |
| 10 PDFs | ~10 sec | Still responsive |
| 50 PDFs | ~50 sec | A bit slower |
| 100 PDFs | ~2 min | Noticeable wait |

**For many files:** Upload in batches of 10-20

---

## 🐛 Troubleshooting

### **Q: "Application failed to start"**
**A:** 
- Check Python 3.8+ installed: `python --version`
- Delete `.venv` folder and restart launcher
- Run: `pip install streamlit`

### **Q: "No module named 'pdf_test_case_extractor'"**
**A:** Ensure files are in same directory:
- app.py ✅
- pdf_test_case_extractor.py ✅
- launch_app.py ✅

### **Q: "Can't see converted files"**
**A:** 
- Check conversion status (should show ✅ Success)
- Try different PDF if one fails
- Use Download tab (not file explorer)

### **Q: "Some signals missing"**
**A:**
- PDF might not be text-extractable
- Try opening PDF in Adobe Reader - can you select text?
- If not selectable, it's a scanned image

### **Q: "Port 8501 already in use"**
**A:**
- Another instance running
- Close other Streamlit apps
- Or use different port: `streamlit run app.py --server.port 8502`

### **Q: "Can't download files"**
**A:**
- Wait for conversion to complete fully
- Check browser download settings
- Try ZIP format instead

---

## 👥 Sharing with Team

### **Method 1: Shared Network Drive**
1. Copy entire folder to shared drive
2. Share folder link with team
3. Team runs: `python launch_app.py`

### **Method 2: Central Server**
1. Set up on central machine
2. Run: `streamlit run app.py --server.address 0.0.0.0`
3. Share URL: `http://[server-ip]:8501`

### **Method 3: Cloud Deployment** (Advanced)
Deploy to cloud services (Heroku, AWS, Azure, Google Cloud, etc.)

---

## 📞 Support for Your Team

**For Issues:**
1. Check Help tab in app
2. Try restarting the app
3. Contact tool maintainer with:
   - Error message (from browser console)
   - PDF file name
   - Your OS/Python version

**For Feature Requests:**
- Share feedback with team lead
- Include specific use case
- Suggest which signal types to add

---

## 📊 Sample Outputs

### **What teammates will get:**

**Input PDF:** `26107 - TC_F027_LCU_Feedback_Plausibility_RightPL_Key_OFF.pdf`

**Output - TXT File:**
```
======================================================================
PRE-CONDITION
======================================================================
Stimulate sys_F040_KeySts to = ON(4)
si_sys_TcSen_bTerm15_1 = 1 // 0x0 - Not_Active , 0x1 - Active
Stimulate sys_F858_NBC_Night_DaySts_for_IE to = Night(0)
Proxy_write_Side_Marker = 0 // 0 - Enabled , 1 - Disabled

======================================================================
STIMULATION-1: Activation of Follow Me Home Mode
======================================================================

Actions:
  si_sys_F027_LCU_Left_PL_Feedback = 1
  si_sys_F027_LCU_Right_PL_Feedback = 1

Expected Results:
  XCP_sys_F247_FrontPosLightCmd = 0->1
  so_sys_F027_NBC_LeftPL = 0->1
  NO_DTC
...
```

**Output - JSON File:**
```json
{
  "test_case_id": "26107",
  "test_case_title": "TC_F027_LCU_Feedback_Plausibility_RightPL_Key_OFF",
  "pre_condition": {
    "Stimulate sys_F040_KeySts to": "ON(4)",
    "si_sys_TcSen_bTerm15_1": "1 // 0x0 - Not_Active"
  },
  "stimulations": [...]
}
```

---

## ✨ Why Your Team Will Love This

✅ **Easy to Use** - No technical knowledge needed  
✅ **Fast** - Converts files in seconds  
✅ **Reliable** - Handles errors gracefully  
✅ **Flexible** - Multiple download formats  
✅ **Beautiful** - Professional, modern interface  
✅ **Shareable** - Works on any Windows/Mac/Linux  
✅ **Local** - No data sent to cloud  
✅ **Free** - No licensing costs  

---

## 🎯 Ready to Share!

**Everything your team needs is in this folder:**
- ✅ app.py (Web application)
- ✅ launch_app.py (Easy launcher)
- ✅ pdf_test_case_extractor.py (Core engine)
- ✅ app_requirements.txt (Dependencies)
- ✅ This guide (TEAM_EDITION.md)

**Just share the folder and they can start converting PDFs immediately!**

---

## 🚀 Launch Command Summary

### **For Your Teammates:**

**Windows PowerShell:**
```powershell
python launch_app.py
```

**Windows CMD:**
```cmd
python launch_app.py
```

**Mac/Linux Terminal:**
```bash
python3 launch_app.py
```

**Wait 10-30 seconds → Browser opens automatically**

---

## 📝 Changelog

**Version 2.0** (November 17, 2026)
- ✨ Streamlit web UI
- ✨ Drag & drop file upload
- ✨ Real-time progress tracking
- ✨ Multiple download formats (TXT, JSON, ZIP)
- ✨ Extraction statistics & charts
- ✨ Interactive help documentation
- ✨ Improved error messages
- ✨ Proxy_* signal support
- ✨ Team-friendly interface

**Version 1.0** (Previous)
- Command-line batch converter

---

## 📄 License & Distribution

**Free to use and share with your team!**
- No licensing required
- No usage limits
- Fully redistributable
- Internal use only

---

**🎉 Your teammates are ready to convert PDFs!**

Just share this folder and they can start using the tool immediately.

Questions? Check the **Help** tab in the app!
