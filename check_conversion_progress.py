#!/usr/bin/env python3
"""
Batch PDF Conversion Statistics & Monitoring Tool
Track progress of batch conversions
"""

from pathlib import Path
import json
from datetime import datetime

def get_conversion_status():
    """Check how many PDFs have been converted"""
    root = Path.cwd()
    
    pdfs = list(root.glob("*.pdf"))
    converted = []
    pending = []
    
    for pdf in pdfs:
        # Check if either the JSON or main TXT file exists (both are created together)
        json_file = root / f"{pdf.stem}_extracted.json"
        txt_file = root / f"TC_{pdf.stem}.txt"
        
        if json_file.exists() or txt_file.exists():
            converted.append(pdf.name)
        else:
            pending.append(pdf.name)
    
    return {
        'total_pdfs': len(pdfs),
        'converted': len(converted),
        'pending': len(pending),
        'percent_complete': (len(converted) / len(pdfs) * 100) if pdfs else 0,
        'pending_files': sorted(pending)
    }

def print_status_report():
    """Print conversion progress"""
    status = get_conversion_status()
    
    print("\n" + "="*70)
    print("PDF CONVERSION STATUS REPORT")
    print("="*70)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Directory: {Path.cwd()}")
    print(f"\nTotal PDFs found:    {status['total_pdfs']}")
    print(f"Converted:           {status['converted']} ✅")
    print(f"Pending:             {status['pending']} ⏳")
    print(f"Progress:            {status['percent_complete']:.1f}%")
    
    if status['pending'] > 0:
        print(f"\nNext to convert ({min(5, status['pending'])} of {status['pending']}):")
        for fname in status['pending_files'][:5]:
            print(f"  - {fname}")
        if status['pending'] > 5:
            print(f"  ... and {status['pending'] - 5} more")
    
    print("="*70 + "\n")
    
    # Estimate time remaining
    if status['converted'] > 0:
        avg_time_per_pdf = 1.0  # seconds (empirical)
        estimated_remaining = status['pending'] * avg_time_per_pdf
        hours = int(estimated_remaining / 3600)
        minutes = int((estimated_remaining % 3600) / 60)
        if hours > 0:
            print(f"⏱️  Estimated time for pending: ~{hours}h {minutes}m")
        else:
            print(f"⏱️  Estimated time for pending: ~{minutes}m")
    
    return status

def generate_json_summary():
    """Generate statistics from extracted JSON files"""
    root = Path.cwd()
    json_files = list(root.glob("*_extracted.json"))
    
    if not json_files:
        print("No extracted JSON files found yet.")
        return
    
    stats = {
        'total_test_cases': len(json_files),
        'avg_pre_condition_items': 0,
        'avg_stimulations': 0,
        'avg_post_condition_items': 0,
        'signal_types_found': set()
    }
    
    total_pre = total_stim = total_post = 0
    
    for json_file in json_files:
        try:
            with open(json_file) as f:
                data = json.load(f)
            total_pre += len(data.get('pre_condition', {}))
            total_stim += len(data.get('stimulations', []))
            total_post += len(data.get('post_condition', {}))
            
            # Collect signal types
            for stim in data.get('stimulations', []):
                for signal_key in stim.get('expected_results', {}).keys():
                    if '_' in signal_key:
                        prefix = signal_key.split('_')[0] + '_' + signal_key.split('_')[1]
                        stats['signal_types_found'].add(prefix)
        except:
            pass
    
    stats['avg_pre_condition_items'] = total_pre / len(json_files) if json_files else 0
    stats['avg_stimulations'] = total_stim / len(json_files) if json_files else 0
    stats['avg_post_condition_items'] = total_post / len(json_files) if json_files else 0
    
    print("\n" + "="*70)
    print("EXTRACTION STATISTICS")
    print("="*70)
    print(f"Test Cases Extracted:         {stats['total_test_cases']}")
    print(f"Avg Pre-Condition Items:      {stats['avg_pre_condition_items']:.1f}")
    print(f"Avg Stimulations per Test:    {stats['avg_stimulations']:.1f}")
    print(f"Avg Post-Condition Items:     {stats['avg_post_condition_items']:.1f}")
    print(f"Signal Type Prefixes Found:   {len(stats['signal_types_found'])}")
    if stats['signal_types_found']:
        print(f"  Detected: {', '.join(sorted(stats['signal_types_found']))}")
    print("="*70 + "\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--stats':
        generate_json_summary()
    else:
        status = print_status_report()
        generate_json_summary()
        
        if status['pending'] > 0:
            print("\n💡 TIP: Run batch_pdf_converter.py to process pending PDFs")
            print("   Command: .\\.venv\\Scripts\\python.exe batch_pdf_converter.py\n")
