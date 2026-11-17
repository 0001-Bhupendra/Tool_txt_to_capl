"""
PDF Test Case Converter - Streamlit Web Application
Interactive tool for teammates to upload PDFs, convert them, and download results.
"""

import streamlit as st
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import io
import zipfile
import pandas as pd
from pdf_test_case_extractor import TestCaseExtractor

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="PDF Test Case Converter",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 4px;
        padding: 12px;
        margin: 10px 0;
        color: #155724;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 4px;
        padding: 12px;
        margin: 10px 0;
        color: #721c24;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 4px;
        padding: 12px;
        margin: 10px 0;
        color: #0c5460;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'conversion_results' not in st.session_state:
    st.session_state.conversion_results = []

if 'temp_dir' not in st.session_state:
    temp_dir = tempfile.mkdtemp()
    st.session_state.temp_dir = temp_dir

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def process_pdf_file(uploaded_file, temp_dir):
    """Process a single uploaded PDF file."""
    try:
        # Save uploaded file to temp directory
        temp_pdf_path = Path(temp_dir) / uploaded_file.name
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Extract test case data
        extractor = TestCaseExtractor()
        result = extractor.extract_all(str(temp_pdf_path))
        
        if not result:
            return {
                'status': 'error',
                'filename': uploaded_file.name,
                'error': 'Failed to extract test case data'
            }
        
        # Save JSON output
        json_filename = f"{temp_pdf_path.stem}_extracted.json"
        json_path = Path(temp_dir) / json_filename
        with open(json_path, "w") as f:
            json.dump(result, f, indent=2)
        
        # Save TXT output
        txt_filename = f"TC_{temp_pdf_path.stem}.txt"
        txt_path = Path(temp_dir) / txt_filename
        extractor.save_as_text(result, str(txt_path))
        
        # Return success result
        return {
            'status': 'success',
            'filename': uploaded_file.name,
            'test_id': result.get('metadata', {}).get('id', 'Unknown'),
            'title': result.get('metadata', {}).get('title', 'Unknown'),
            'pre_condition_count': len(result.get('pre_condition', {})),
            'stimulations_count': len(result.get('stimulations', [])),
            'post_condition_count': len(result.get('post_condition', {})),
            'json_path': str(json_path),
            'json_filename': json_filename,
            'txt_path': str(txt_path),
            'txt_filename': txt_filename
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'filename': uploaded_file.name,
            'error': str(e)
        }

# ============================================================================
# PAGE HEADER
# ============================================================================

st.markdown("# 📄 PDF Test Case Converter")
st.markdown("*Convert PDF test cases to structured TXT and JSON formats*")
st.markdown("---")

# ============================================================================
# TABS
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs(["🔄 Convert", "📥 Download", "📊 Statistics", "❓ Help"])

# ============================================================================
# TAB 1: CONVERT
# ============================================================================

with tab1:
    st.markdown("## Upload and Convert PDF Files")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload PDF test case files",
        type=["pdf"],
        accept_multiple_files=True,
        help="Select one or multiple PDF files to convert"
    )
    
    if uploaded_files:
        st.info(f"📋 {len(uploaded_files)} file(s) selected")
        
        # Convert button
        if st.button("🚀 Start Conversion", key="convert_btn"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            conversion_results = []
            
            for idx, uploaded_file in enumerate(uploaded_files):
                # Update progress
                progress = (idx + 1) / len(uploaded_files)
                progress_bar.progress(progress)
                status_text.text(f"Processing: {uploaded_file.name}")
                
                # Process file
                result = process_pdf_file(uploaded_file, st.session_state.temp_dir)
                conversion_results.append(result)
            
            # Store results in session state
            st.session_state.conversion_results.extend(conversion_results)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Show results
            st.success("✅ Conversion complete!")
            
            # Results table
            st.markdown("### Conversion Results")
            
            successful = [r for r in conversion_results if r['status'] == 'success']
            failed = [r for r in conversion_results if r['status'] == 'error']
            
            if successful:
                results_data = []
                for r in successful:
                    results_data.append({
                        'PDF File': r['filename'],
                        'Test ID': r['test_id'],
                        'Title': r['title'][:40] + '...' if len(r['title']) > 40 else r['title'],
                        'Pre-Cond': r['pre_condition_count'],
                        'Stimulations': r['stimulations_count'],
                        'Post-Cond': r['post_condition_count'],
                        'Status': '✅ Success'
                    })
                
                df = pd.DataFrame(results_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
            
            if failed:
                st.markdown("### ❌ Failed Conversions")
                for r in failed:
                    st.error(f"**{r['filename']}**: {r['error']}")
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Successful", len(successful))
            with col2:
                st.metric("Failed", len(failed))
            with col3:
                st.metric("Total", len(conversion_results))

# ============================================================================
# TAB 2: DOWNLOAD
# ============================================================================

with tab2:
    st.markdown("## Download Converted Files")
    
    if not st.session_state.conversion_results:
        st.info("📌 No converted files yet. Use the Convert tab to process PDFs.")
    else:
        successful_results = [r for r in st.session_state.conversion_results if r['status'] == 'success']
        failed_results = [r for r in st.session_state.conversion_results if r['status'] == 'error']
        
        # Download format selector
        download_format = st.radio(
            "Choose download format:",
            ["Individual Files", "All as ZIP"],
            horizontal=True
        )
        
        if download_format == "Individual Files":
            st.markdown("### Download Individual Files")
            
            if successful_results:
                for result in successful_results:
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.text(result['filename'])
                    
                    with col2:
                        # TXT download
                        with open(result['txt_path'], 'r') as f:
                            txt_content = f.read()
                        st.download_button(
                            label="📄 TXT",
                            data=txt_content,
                            file_name=result['txt_filename'],
                            mime="text/plain"
                        )
                    
                    with col3:
                        # JSON download
                        with open(result['json_path'], 'r') as f:
                            json_content = f.read()
                        st.download_button(
                            label="📋 JSON",
                            data=json_content,
                            file_name=result['json_filename'],
                            mime="application/json"
                        )
        
        else:  # ZIP format
            st.markdown("### Download All Files as ZIP")
            
            if successful_results:
                # Create ZIP file
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for result in successful_results:
                        # Add TXT file
                        zip_file.write(result['txt_path'], arcname=result['txt_filename'])
                        # Add JSON file
                        zip_file.write(result['json_path'], arcname=result['json_filename'])
                
                zip_buffer.seek(0)
                
                # Download button
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                st.download_button(
                    label="📦 Download All as ZIP",
                    data=zip_buffer.getvalue(),
                    file_name=f"converted_test_cases_{timestamp}.zip",
                    mime="application/zip"
                )
                
                st.success(f"✅ {len(successful_results)} file(s) ready to download")
        
        # Failed files section
        if failed_results:
            st.markdown("### ⚠️ Failed Files")
            for result in failed_results:
                st.error(f"**{result['filename']}**: {result['error']}")

# ============================================================================
# TAB 3: STATISTICS
# ============================================================================

with tab3:
    st.markdown("## Extraction Statistics")
    
    if not st.session_state.conversion_results:
        st.info("📌 No data yet. Convert some PDFs to see statistics.")
    else:
        successful_results = [r for r in st.session_state.conversion_results if r['status'] == 'success']
        
        if successful_results:
            # Overall metrics
            st.markdown("### Overall Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            total_pre = sum(r['pre_condition_count'] for r in successful_results)
            total_stim = sum(r['stimulations_count'] for r in successful_results)
            total_post = sum(r['post_condition_count'] for r in successful_results)
            avg_pre = total_pre / len(successful_results) if successful_results else 0
            avg_stim = total_stim / len(successful_results) if successful_results else 0
            avg_post = total_post / len(successful_results) if successful_results else 0
            
            with col1:
                st.metric("Files Converted", len(successful_results))
            with col2:
                st.metric("Avg Pre-Conditions", f"{avg_pre:.1f}")
            with col3:
                st.metric("Avg Stimulations", f"{avg_stim:.1f}")
            with col4:
                st.metric("Avg Post-Conditions", f"{avg_post:.1f}")
            
            # Detailed breakdown
            st.markdown("### Detailed Breakdown")
            
            breakdown_data = []
            for result in successful_results:
                breakdown_data.append({
                    'Test ID': result['test_id'],
                    'Title': result['title'][:30] + '...' if len(result['title']) > 30 else result['title'],
                    'Pre-Cond Items': result['pre_condition_count'],
                    'Stimulations': result['stimulations_count'],
                    'Post-Cond Items': result['post_condition_count'],
                    'Total': result['pre_condition_count'] + result['stimulations_count'] + result['post_condition_count']
                })
            
            df = pd.DataFrame(breakdown_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Distribution charts
            st.markdown("### Distribution Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                pre_cond_data = [r['pre_condition_count'] for r in successful_results]
                st.bar_chart({
                    'Pre-Condition Counts': pre_cond_data
                })
            
            with col2:
                stim_data = [r['stimulations_count'] for r in successful_results]
                st.bar_chart({
                    'Stimulations Counts': stim_data
                })

# ============================================================================
# TAB 4: HELP
# ============================================================================

with tab4:
    st.markdown("## 📖 User Guide")
    
    st.markdown("### How to Use This Tool")
    
    with st.expander("📋 Step 1: Upload PDF Files", expanded=True):
        st.markdown("""
        1. Go to the **Convert** tab
        2. Click "Upload PDF files"
        3. Select one or multiple PDF test case files
        4. Files will appear in a list
        """)
    
    with st.expander("🔄 Step 2: Start Conversion"):
        st.markdown("""
        1. Click the **"🚀 Start Conversion"** button
        2. Watch the progress bar as files are processed
        3. See the results table with extraction details
        """)
    
    with st.expander("📥 Step 3: Download Results"):
        st.markdown("""
        1. Go to the **Download** tab
        2. Choose download format:
           - **Individual Files**: Download each file separately
           - **All as ZIP**: Download everything in one ZIP archive
        3. Click the download button(s)
        """)
    
    with st.expander("📊 Step 4: View Statistics (Optional)"):
        st.markdown("""
        1. Go to the **Statistics** tab
        2. See overall metrics and detailed breakdown
        3. View distribution charts
        """)
    
    st.markdown("---")
    st.markdown("### What Gets Extracted")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📌 Pre-Condition")
        st.markdown("""
        - Initial system state
        - Signal values
        - Setup requirements
        """)
    
    with col2:
        st.markdown("#### ⚡ Stimulations")
        st.markdown("""
        - Test actions
        - Multiple steps
        - Expected results for each
        """)
    
    with col3:
        st.markdown("#### ✓ Post-Condition")
        st.markdown("""
        - Final system state
        - Cleanup actions
        - Verification signals
        """)
    
    st.markdown("---")
    st.markdown("### Output Formats")
    
    with st.expander("📄 TXT Format"):
        st.markdown("""
        **Readable text file** with structured formatting:
        - Easy to read in any text editor
        - Organized sections for each part
        - Good for documentation
        - File: `TC_[ID]_[Test_Name].txt`
        """)
    
    with st.expander("📋 JSON Format"):
        st.markdown("""
        **Structured data format** for processing:
        - Machine-readable format
        - Hierarchical structure
        - Easy for database import
        - Programmatic access
        - File: `[ID]_[Test_Name]_extracted.json`
        """)
    
    st.markdown("---")
    st.markdown("### Supported Signal Types")
    
    signal_types = {
        "si_sys_*": "System input signals",
        "so_sys_*": "System output signals",
        "XCP_sys_*": "XCP protocol signals",
        "Proxy_*": "Proxy/control signals",
        "Stimulate sys_*": "Stimulation commands",
        "DTC_active": "Active diagnostic trouble codes",
        "DTC_passive": "Passive diagnostic trouble codes",
        "NO_DTC": "No diagnostic trouble codes indicator"
    }
    
    for signal_type, description in signal_types.items():
        st.markdown(f"- **{signal_type}**: {description}")
    
    st.markdown("---")
    st.markdown("### Tips for Best Results")
    
    tips = [
        "📌 Ensure PDFs are text-extractable (not scanned images)",
        "📌 Use original PDF files from the CANoe test case format",
        "📌 Check that signal names are properly formatted in PDFs",
        "📌 For large batches, upload in groups of 10-20 files",
        "📌 Downloaded TXT files are ready for immediate use"
    ]
    
    for tip in tips:
        st.markdown(tip)
    
    st.markdown("---")
    st.markdown("### Troubleshooting")
    
    with st.expander("❓ Why are some signals missing?"):
        st.markdown("""
        - PDF might not be text-extractable
        - Try opening PDF in Adobe Reader - can you select text?
        - If text is not selectable, it's a scanned image (not supported)
        """)
    
    with st.expander("❓ What if conversion fails?"):
        st.markdown("""
        - Check the error message in the Failed section
        - Verify the PDF is a valid test case file
        - Try another PDF to confirm it's working
        """)
    
    with st.expander("❓ Can I convert multiple times?"):
        st.markdown("""
        - Yes! Convert different PDFs in multiple runs
        - Each conversion adds to your results
        - Download all files together when ready
        """)
    
    with st.expander("❓ Are my files stored securely?"):
        st.markdown("""
        - Files are processed locally (not uploaded to cloud)
        - Temporary files are auto-cleaned after download
        - No personal data collection
        """)
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    **PDF Test Case Converter v2.0**
    
    - 🎯 Purpose: Convert automotive test case PDFs to structured data
    - 🔧 Technology: Streamlit + PyPDF2 + Python
    - 📊 Data: Extracts test structure, signals, and results
    - ✨ Features: Web UI, batch processing, multiple formats
    
    **Free to use. No limitations. Share with your team!**
    """)
