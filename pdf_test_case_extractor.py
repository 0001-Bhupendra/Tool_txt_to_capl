"""
PDF Test Case Extractor for BCM/Vehicle Test Cases
Extracts Pre-Condition, Stimulation, Expected Results, and Post-Condition data
from PDF test case documents and outputs structured JSON/text for CAPL code generation.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import sys

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("WARNING: PyPDF2 not installed. Install with: pip install PyPDF2")


class TestCaseExtractor:
    """Extract structured test case data from PDF documents."""
    
    def __init__(self):
        self.test_case_data = {}
    
    def extract_pdf_text(self, pdf_path: str) -> str:
        """Extract all text from PDF file."""
        if not PDF_AVAILABLE:
            raise ImportError("PyPDF2 is required. Install with: pip install PyPDF2")
        
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
            raise
        
        return text
    
    def clean_text(self, text: str) -> str:
        """Clean extracted text: normalize whitespace and line breaks."""
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        # Fix line endings
        text = text.replace(' \n ', '\n')
        return text.strip()
    
    def remove_urls(self, text: str) -> str:
        """Remove all URLs from text - they are metadata, not test steps."""
        # Remove http(s):// URLs
        text = re.sub(r'https?://\S+\s*', '', text, flags=re.IGNORECASE)
        return text.strip()
    
    def extract_pre_condition(self, text: str) -> Dict[str, str]:
        """Extract Pre-Condition section."""
        pre_cond = {}
        
        # Match Pre-Condition section
        pattern = r'Pre-Condition:\s*(.*?)(?=Stimulation|Test Case Design|Formal Review|$)'
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        
        if match:
            content = match.group(1).strip()
            # Remove URLs first (they can break extraction patterns)
            content = self.remove_urls(content)
            
            # Extract individual conditions - maintain order by position
            conditions_with_pos = []
            
            # Extract si_sys_* and Proxy_* assignments with better value capture
            # Pattern: (si_sys_XXX or Proxy_XXX) = VALUE (until next signal keyword)
            for m in re.finditer(r'(si_sys_[^=\s]+|Proxy_[^=\s]+)\s*=\s*(.+?)(?=\s+(?:si_sys_|Proxy_|Stimulate\s+sys_|$))', content):
                signal_name = m.group(1).strip()
                value_raw = m.group(2).strip()
                # Clean up value: normalize spaces but preserve content including comments
                value_clean = re.sub(r'\s+', ' ', value_raw).strip()
                if value_clean:
                    conditions_with_pos.append((m.start(), signal_name, value_clean))
            
            # Extract Stimulate statements with better value capture
            # Pattern: Stimulate sys_XXX to VALUE (until next signal keyword or end)
            for m in re.finditer(r'(Stimulate\s+sys_[^\s]+)\s+to\s+(.+?)(?=\s+(?:si_sys_|Proxy_|Stimulate\s+sys_|$))', content):
                stmt = m.group(1).strip()
                value_raw = m.group(2).strip()
                # Clean up value
                value_clean = re.sub(r'\s+', ' ', value_raw).strip()
                if value_clean:
                    conditions_with_pos.append((m.start(), stmt + ' to', value_clean))
            
            # Sort by position to maintain order
            conditions_with_pos.sort(key=lambda x: x[0])
            
            # Add to pre_cond dict in order
            for _, var, value in conditions_with_pos:
                pre_cond[var] = value
        
        return pre_cond
    
    def extract_stimulations(self, text: str) -> List[Dict[str, Any]]:
        """Extract all Stimulation sections with their Expected Results."""
        stimulations = []
        
        # Match each Stimulation-N section
        stim_pattern = r'Stimulation-(\d+):\s*["\']?([^"\']*)["\']?\s*(.*?)(?=Expected Results-\1|Stimulation-\d+|Post-Condition|$)'
        matches = re.finditer(stim_pattern, text, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            stim_num = match.group(1)
            stim_title = match.group(2).strip()
            stim_content = match.group(3)
            
            # Extract Expected Results for this stimulation
            expected_pattern = r'Expected Results-' + stim_num + r':\s*["\']?([^"\']*)["\']?\s*(.*?)(?=Stimulation-\d+|Post-Condition|$)'
            expected_match = re.search(expected_pattern, text, re.IGNORECASE | re.DOTALL)
            
            expected_title = ""
            expected_data = {}
            
            if expected_match:
                expected_title = expected_match.group(1).strip()
                expected_content = expected_match.group(2)
                # Remove URLs from expected content
                expected_content = self.remove_urls(expected_content)
                
                # Extract DTC entries (both active and passive)
                dtc_active_pattern = r'DTC[_\s]*active\s*=\s*["\']?([^"\']*)["\']?'
                dtc_active_matches = re.findall(dtc_active_pattern, expected_content, re.IGNORECASE)
                if dtc_active_matches:
                    expected_data['DTC_active'] = dtc_active_matches
                
                dtc_passive_pattern = r'DTC[_\s]*passive\s*=\s*["\']?([^"\']*)["\']?'
                dtc_passive_matches = re.findall(dtc_passive_pattern, expected_content, re.IGNORECASE)
                if dtc_passive_matches:
                    expected_data['DTC_passive'] = dtc_passive_matches
                
                # Extract signal transitions (signal = 0->1 format)
                # Use position-based extraction to handle page breaks and spacing issues
                # NOTE: Content has been cleaned, so whitespace is normalized to spaces (no newlines)
                signals_with_pos = []
                
                # Extract all signal types with position tracking
                # Capture signal name and value, stopping at next signal keyword or keywords
                for m in re.finditer(r'(XCP_sys_[^=\s]+|so_sys_[^=\s]+|Proxy_[^=\s]+)\s*=\s*(.+?)(?=\s+(?:XCP_sys_|so_sys_|Proxy_|No\s+DTC|DTC[_\s])|$)', expected_content):
                    signal_name = m.group(1).strip()
                    value_raw = m.group(2).strip()
                    # Clean up value: remove trailing spaces and normalize spaces within value
                    value_clean = re.sub(r'\s+', ' ', value_raw).strip()
                    if value_clean:
                        signals_with_pos.append((m.start(), signal_name, value_clean))
                
                # Sort by position to maintain original PDF order
                signals_with_pos.sort(key=lambda x: x[0])
                
                # Add signals in order
                for _, signal, value in signals_with_pos:
                    # Remove URLs from signal values
                    value_clean = self.remove_urls(value.strip())
                    expected_data[signal] = value_clean
                
                # Check for NO DTC
                if re.search(r'NO\s+DTC', expected_content, re.IGNORECASE):
                    expected_data['NO_DTC'] = True
            
            # Extract stimulation actions - maintain order as they appear in PDF
            stim_actions = {}
            # Remove URLs from stimulation content
            stim_content_clean = self.remove_urls(stim_content)
            
            # Create fault (SCG/OL) pattern
            fault_pattern = r'Create\s+(SCG|OL)\s+on\s+["\']?([^"\']*)["\']?'
            fault_match = re.search(fault_pattern, stim_content_clean, re.IGNORECASE)
            if fault_match:
                stim_actions['fault_type'] = fault_match.group(1)
                stim_actions['fault_target'] = fault_match.group(2).strip()
            
            # Remove Fault action
            if re.search(r'Remove\s+Fault', stim_content_clean, re.IGNORECASE):
                stim_actions['remove_fault'] = True
            
            # Extract actions in order of appearance (by position in text)
            # This preserves the PDF order: Proxy_write, Stimulate, si_sys assignments
            actions_with_pos = []
            
            # Proxy_write statements - with position
            for m in re.finditer(r'(Proxy_write_[^=\s]+)\s*=\s*(\S+?)(?=\s+(?:Proxy_write|Stimulate|si_sys_|wait|Clear|Expected|Create|Remove)|\s*$)', stim_content_clean):
                actions_with_pos.append((m.start(), m.group(1).strip(), m.group(2).strip(), 'value'))
            
            # Stimulate statements - with position
            for m in re.finditer(r'Stimulate\s+(\S+)\s+to\s+(\S+?)(?=\s+(?:Proxy_write|Stimulate|si_sys_|wait|Clear|Expected|Create|Remove)|\s*$)', stim_content_clean):
                actions_with_pos.append((m.start(), f'Stimulate {m.group(1)} to', m.group(2).strip(), 'value'))
            
            # si_sys_* signal assignments - with position
            for m in re.finditer(r'(si_sys_[^=\s]+)\s*=\s*(\S+?)(?=\s+(?:Proxy_write|Stimulate|si_sys_|wait|Clear|Expected|Create|Remove)|\s*$)', stim_content_clean):
                actions_with_pos.append((m.start(), m.group(1).strip(), m.group(2).strip(), 'value'))
            
            # wait timing - with position
            for m in re.finditer(r'wait\s+(\S+)', stim_content_clean, re.IGNORECASE):
                actions_with_pos.append((m.start(), 'wait', m.group(1).strip(), 'value'))
            
            # Sort by position (first element of tuple) to maintain order
            actions_with_pos.sort(key=lambda x: x[0])
            
            # Add to stim_actions dict in order
            for _, key, value, _ in actions_with_pos:
                stim_actions[key] = value
            
            stimulation = {
                'number': stim_num,
                'title': stim_title,
                'actions': stim_actions,
                'expected_title': expected_title,
                'expected_results': expected_data
            }
            
            stimulations.append(stimulation)
        
        return stimulations
    
    def extract_post_condition(self, text: str) -> Dict[str, str]:
        """Extract Post-Condition section."""
        post_cond = {}
        
        # Match Post-Condition section
        pattern = r'Post-Condition:\s*(.*?)(?=Test scripts|Attachments|$)'
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        
        if match:
            content = match.group(1).strip()
            # Remove URLs first (they can break extraction patterns)
            content = self.remove_urls(content)
            
            # Extract individual conditions - maintain order by position
            conditions_with_pos = []
            
            # Extract si_sys_* and Proxy_* assignments with better value capture
            # Pattern: (si_sys_XXX or Proxy_XXX) = VALUE (until next signal keyword)
            for m in re.finditer(r'(si_sys_[^=\s]+|Proxy_[^=\s]+)\s*=\s*(.+?)(?=\s+(?:si_sys_|Proxy_|Stimulate\s+sys_|$))', content):
                signal_name = m.group(1).strip()
                value_raw = m.group(2).strip()
                # Clean up value: normalize spaces but preserve content including comments
                value_clean = re.sub(r'\s+', ' ', value_raw).strip()
                if value_clean:
                    conditions_with_pos.append((m.start(), signal_name, value_clean))
            
            # Extract Stimulate statements with better value capture
            # Pattern: Stimulate sys_XXX to VALUE (until next signal keyword or end)
            for m in re.finditer(r'(Stimulate\s+sys_[^\s]+)\s+to\s+(.+?)(?=\s+(?:si_sys_|Proxy_|Stimulate\s+sys_|$))', content):
                stmt = m.group(1).strip()
                value_raw = m.group(2).strip()
                # Clean up value
                value_clean = re.sub(r'\s+', ' ', value_raw).strip()
                if value_clean:
                    conditions_with_pos.append((m.start(), stmt + ' to', value_clean))
            
            # Sort by position to maintain order
            conditions_with_pos.sort(key=lambda x: x[0])
            
            # Add to post_cond dict in order
            for _, var, value in conditions_with_pos:
                post_cond[var] = value
        
        return post_cond
    
    def extract_test_case_metadata(self, text: str) -> Dict[str, str]:
        """Extract test case metadata (title, ID, etc.)."""
        metadata = {}
        
        # Extract test case ID and title
        title_pattern = r'(\d+):\s*([^\n]+?)(?:\s*Creation Date|$)'
        title_match = re.search(title_pattern, text)
        if title_match:
            metadata['id'] = title_match.group(1).strip()
            # Remove URLs from title
            title_clean = self.remove_urls(title_match.group(2).strip())
            metadata['title'] = title_clean
        
        # Extract component
        comp_pattern = r'Component:\s*([^\n]+)'
        comp_match = re.search(comp_pattern, text)
        if comp_match:
            # Remove URLs from component
            comp_clean = self.remove_urls(comp_match.group(1).strip())
            metadata['component'] = comp_clean
        
        # Extract configuration
        config_pattern = r'Configuration:\s*([^\n]+)'
        config_match = re.search(config_pattern, text)
        if config_match:
            # Remove URLs from configuration
            config_clean = self.remove_urls(config_match.group(1).strip())
            metadata['configuration'] = config_clean
        
        return metadata
    
    def extract_all(self, pdf_path: str) -> Dict[str, Any]:
        """Extract all test case data from PDF."""
        # Extract text from PDF
        pdf_text = self.extract_pdf_text(pdf_path)
        pdf_text = self.clean_text(pdf_text)
        
        # Extract all sections
        result = {
            'metadata': self.extract_test_case_metadata(pdf_text),
            'pre_condition': self.extract_pre_condition(pdf_text),
            'stimulations': self.extract_stimulations(pdf_text),
            'post_condition': self.extract_post_condition(pdf_text)
        }
        
        return result
    
    def save_as_json(self, data: Dict[str, Any], output_path: str) -> None:
        """Save extracted data as JSON file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"JSON saved to: {output_path}")
    
    def save_as_text(self, data: Dict[str, Any], output_path: str) -> None:
        """Save extracted data as formatted text file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # Pre-Condition
            f.write("// PRE-CONDITION\n")
            for var, value in data['pre_condition'].items():
                # Clean up pre-condition values to remove any remaining URLs
                value_clean = self.remove_urls(str(value))
                f.write(f"{var} = {value_clean}\n")
            
            # Stimulations
            for stim in data['stimulations']:
                f.write(f"\n// STIMULATION-{stim['number']}: {stim['title']}\n")
                
                for action, value in stim['actions'].items():
                    if isinstance(value, bool):
                        f.write(f"{action}\n")
                    else:
                        # Clean URLs from action values
                        value_clean = self.remove_urls(str(value))
                        f.write(f"{action} = {value_clean}\n")
                
                f.write(f"\n// EXPECTED RESULTS-{stim['number']}: {stim['expected_title']}\n")
                for result, value in stim['expected_results'].items():
                    if isinstance(value, bool):
                        f.write(f"{result}\n")
                    elif isinstance(value, list):
                        for item in value:
                            # Clean URLs from result values
                            item_clean = self.remove_urls(str(item))
                            f.write(f"{result} = {item_clean}\n")
                    else:
                        # Clean URLs from result values
                        value_clean = self.remove_urls(str(value))
                        
                        # Check if value contains multiple signals merged on one line
                        # Split on space followed by known signal name patterns
                        signal_keywords = r'(?:XCP_sys_|so_sys_|Proxy_|si_sys_)'
                        if re.search(r'\s+' + signal_keywords, value_clean):
                            # This value contains multiple signals - split and format each one
                            # Split on space followed by signal keyword
                            parts = re.split(r'\s+(?=' + signal_keywords + ')', value_clean)
                            for part in parts:
                                part = part.strip()
                                if part and '=' in part:
                                    # This contains a signal assignment
                                    f.write(f"{part}\n")
                                elif part and part.lower().startswith(('xcp_', 'so_', 'proxy', 'si_')):
                                    # Continuation of signal value that got split
                                    f.write(f"{part}\n")
                        else:
                            # Single signal, write normally
                            f.write(f"{result} = {value_clean}\n")
            
            # Post-Condition
            f.write("\n// POST-CONDITION\n")
            for var, value in data['post_condition'].items():
                # Clean URLs from post-condition values
                value_clean = self.remove_urls(str(value))
                # Check if value contains multiple signals merged on one line
                # Split on space followed by known signal name patterns
                signal_keywords = r'(?:si_sys_|Stimulate\s)'
                if re.search(r'\s+' + signal_keywords, value_clean):
                    # This value contains multiple signals - split and format each one
                    # Split on space followed by signal keyword
                    parts = re.split(r'\s+(?=' + signal_keywords + ')', value_clean)
                    for part in parts:
                        part = part.strip()
                        if part and '=' in part:
                            # This contains a signal assignment
                            f.write(f"{part}\n")
                        elif part and part.lower().startswith(('si_', 'stimulate')):
                            # Continuation of signal value that got split
                            f.write(f"{part}\n")
                else:
                    # Single signal, write normally
                    f.write(f"{var} = {value_clean}\n")
        
        print(f"Text file saved to: {output_path}")


def main():
    """Main function to run the extractor."""
    if len(sys.argv) < 2:
        print("Usage: python pdf_test_case_extractor.py <pdf_file> [output_format]")
        print("\nExample:")
        print("  python pdf_test_case_extractor.py TC_7778.pdf")
        print("  python pdf_test_case_extractor.py TC_7778.pdf json")
        print("  python pdf_test_case_extractor.py TC_7778.pdf text")
        print("\nSupported output formats: json, text (default: both)")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "both"
    
    # Validate PDF file exists
    pdf_path = Path(pdf_file)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_file}")
        sys.exit(1)
    
    # Extract data
    print(f"Extracting test case data from: {pdf_file}")
    extractor = TestCaseExtractor()
    
    try:
        data = extractor.extract_all(str(pdf_path))
        
        # Generate output file names
        base_name = pdf_path.stem
        
        # Extract test case name from metadata for text file
        test_case_id = data['metadata'].get('id', 'unknown')
        test_case_title = data['metadata'].get('title', base_name)
        # Create a safe filename from test case name
        safe_title = "".join(c for c in test_case_title if c.isalnum() or c in (' ', '_', '-')).rstrip()
        text_filename = f"TC_{test_case_id}_{safe_title}.txt"
        
        # Save in requested format
        if output_format in ('both', 'json'):
            json_output = pdf_path.parent / f"{base_name}_extracted.json"
            extractor.save_as_json(data, str(json_output))
        
        # Always save text format with test case name
        text_output = pdf_path.parent / text_filename
        extractor.save_as_text(data, str(text_output))
        
        # Also save with _extracted suffix if specifically requested
        if output_format in ('both', 'text'):
            extracted_text_output = pdf_path.parent / f"{base_name}_extracted.txt"
            # Only create if different from the named version
            if str(extracted_text_output) != str(text_output):
                extractor.save_as_text(data, str(extracted_text_output))
        
        # Print summary
        print("\n" + "=" * 70)
        print("EXTRACTION SUMMARY")
        print("=" * 70)
        print(f"Test Case ID: {data['metadata'].get('id', 'N/A')}")
        print(f"Test Case Title: {data['metadata'].get('title', 'N/A')}")
        print(f"Pre-Conditions: {len(data['pre_condition'])} items")
        print(f"Stimulations: {len(data['stimulations'])} steps")
        print(f"Post-Conditions: {len(data['post_condition'])} items")
        print("\n" + "=" * 70)
        print("GENERATED FILES")
        print("=" * 70)
        if output_format in ('both', 'json'):
            print(f"[OK] JSON Data:  {json_output.name}")
        print(f"[OK] Test Info:  {text_filename}")
        if output_format in ('both', 'text'):
            if str(extracted_text_output) != str(text_output):
                print(f"[OK] Text Data:  {extracted_text_output.name}")
        print("=" * 70)
        
    except Exception as e:
        print(f"Error during extraction: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
