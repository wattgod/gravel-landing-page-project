#!/usr/bin/env python3
"""
ELEMENTOR UPLOAD REGRESSION TEST
================================
Tests that generated Elementor JSON files will upload successfully.
Catches issues that cause "Invalid Content In File" errors.

Exit codes:
    0 = All tests passed
    1 = Issues detected that will cause upload failures
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any

def test_elementor_file(file_path: Path) -> List[str]:
    """
    Test an Elementor JSON file for upload compatibility.
    Returns list of error messages.
    """
    errors = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return [f"Failed to parse file: {e}"]
    
    # Check required top-level structure
    required_keys = ['content', 'page_settings', 'version', 'title', 'type']
    for key in required_keys:
        if key not in data:
            errors.append(f"Missing required top-level key: {key}")
    
    # Check for null values in critical places
    def find_nulls(obj, path='', found=None):
        if found is None:
            found = []
        if obj is None:
            # _inline_size can be null, that's OK
            if '_inline_size' not in path:
                found.append(f"Null value at {path}")
        elif isinstance(obj, dict):
            for k, v in obj.items():
                find_nulls(v, f"{path}.{k}" if path else k, found)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                find_nulls(item, f"{path}[{i}]", found)
        return found
    
    nulls = find_nulls(data)
    # Filter out acceptable nulls
    acceptable_nulls = ['_inline_size']
    nulls = [n for n in nulls if not any(acceptable in n for acceptable in acceptable_nulls)]
    
    if nulls:
        errors.extend([f"{file_path.name}: {null}" for null in nulls[:5]])
    
    # Check for HTML tags that might cause issues
    def find_html_tags(obj, path=''):
        html_errors = []
        if isinstance(obj, str):
            # Check for problematic HTML tags
            # Script tags are OK if they're for SVG generation (common in Elementor)
            # Only flag if script contains dangerous patterns
            script_matches = re.findall(r'<script[^>]*>([^<]*)</script>', obj, re.IGNORECASE | re.DOTALL)
            for script_content in script_matches:
                # Allow SVG generation scripts, but flag potentially dangerous ones
                if 'document.createElementNS' in script_content or 'querySelector' in script_content:
                    continue  # SVG generation script, OK
                elif 'eval(' in script_content or 'innerHTML' in script_content or 'document.write' in script_content:
                    html_errors.append(f"Potentially dangerous script at {path}")
            # Check for unclosed tags that might break parsing
            open_tags = len(re.findall(r'<[^/!][^>]*>', obj))
            close_tags = len(re.findall(r'</[^>]+>', obj))
            if abs(open_tags - close_tags) > 10:  # Allow some imbalance for self-closing tags
                html_errors.append(f"Unbalanced HTML tags at {path} ({open_tags} open, {close_tags} close)")
        elif isinstance(obj, dict):
            for k, v in obj.items():
                html_errors.extend(find_html_tags(v, f"{path}.{k}" if path else k))
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                html_errors.extend(find_html_tags(item, f"{path}[{i}]"))
        return html_errors
    
    html_issues = find_html_tags(data)
    if html_issues:
        errors.extend([f"{file_path.name}: {issue}" for issue in html_issues])
    
    # Check for encoding issues
    try:
        with open(file_path, 'rb') as f:
            raw = f.read()
            raw.decode('utf-8')
    except UnicodeDecodeError as e:
        errors.append(f"{file_path.name}: Encoding issue - {e}")
    
    # Check file size (very large files might cause issues)
    file_size = file_path.stat().st_size
    if file_size > 10 * 1024 * 1024:  # 10MB
        errors.append(f"{file_path.name}: File very large ({file_size / 1024 / 1024:.1f}MB), may cause upload issues")
    
    return errors

def test_against_working_reference(test_file: Path, working_file: Path) -> List[str]:
    """
    Compare a test file against a known-working reference file.
    Checks for structural differences that might cause upload failures.
    """
    errors = []
    
    try:
        with open(working_file, 'r', encoding='utf-8') as f:
            working = json.load(f)
        with open(test_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
    except Exception as e:
        return [f"Failed to parse files: {e}"]
    
    # Check top-level keys match
    w_keys = set(working.keys())
    t_keys = set(test_data.keys())
    
    missing = w_keys - t_keys
    extra = t_keys - w_keys
    
    if missing:
        errors.append(f"{test_file.name}: Missing top-level keys: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"{test_file.name}: Extra top-level keys: {', '.join(sorted(extra))}")
    
    # Check content structure
    if 'content' in working and 'content' in test_data:
        if len(working['content']) != len(test_data['content']):
            errors.append(f"{test_file.name}: Content sections count differs: {len(working['content'])} vs {len(test_data['content'])}")
    
    # Check metadata
    for key in ['version', 'type']:
        if working.get(key) != test_data.get(key):
            errors.append(f"{test_file.name}: {key} differs: {working.get(key)} vs {test_data.get(key)}")
    
    return errors

def main():
    """Run all Elementor upload regression tests."""
    output_dir = Path('output')
    downloads_dir = Path('/Users/mattirowe/Downloads')
    
    if not output_dir.exists():
        print("ERROR: output/ directory not found")
        return 1
    
    all_errors = []
    
    # Test all Elementor JSON files in output
    for json_file in output_dir.glob('elementor-*.json'):
        print(f"Testing {json_file.name}...")
        errors = test_elementor_file(json_file)
        all_errors.extend(errors)
    
    # If we have a working reference file, compare against it
    working_file = downloads_dir / 'elementor-belgian-waffle-ride.json'
    if working_file.exists():
        print(f"\nComparing against working reference: {working_file.name}...")
        for json_file in output_dir.glob('elementor-*.json'):
            if 'belgian-waffle-ride' in json_file.name.lower():
                ref_errors = test_against_working_reference(json_file, working_file)
                all_errors.extend(ref_errors)
    
    # Report results
    if all_errors:
        print("\n" + "="*70)
        print("ELEMENTOR UPLOAD ISSUES DETECTED")
        print("="*70)
        for error in all_errors:
            print(f"  ❌ {error}")
        print("\n" + "="*70)
        print(f"Total issues: {len(all_errors)}")
        print("\nThese issues may cause 'Invalid Content In File' upload errors.")
        return 1
    else:
        print("\n" + "="*70)
        print("✅ ALL ELEMENTOR UPLOAD TESTS PASSED")
        print("="*70)
        print("All Elementor JSON files are ready for upload.")
        return 0

if __name__ == '__main__':
    sys.exit(main())

