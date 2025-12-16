#!/usr/bin/env python3
"""
Validate generated Elementor JSON for quality issues.
"""

import json
import re
import sys
from typing import Dict, Any, List


def check_placeholders(json_data: Dict) -> List[str]:
    """Check for unreplaced template placeholders."""
    errors = []
    placeholder_pattern = re.compile(r'\{\{[A-Z_]+\}\}')
    
    def search_in_dict(obj, path=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                search_in_dict(value, new_path)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                search_in_dict(item, new_path)
        elif isinstance(obj, str):
            matches = placeholder_pattern.findall(obj)
            if matches:
                errors.append(f"Unreplaced placeholder at {path}: {matches[0]}")
    
    search_in_dict(json_data)
    return errors


def check_json_valid(json_path: str) -> bool:
    """Check if JSON is valid and parseable."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True
    except json.JSONDecodeError:
        return False


def check_section_ids(json_data: Dict) -> List[str]:
    """Check for expected section IDs in HTML."""
    errors = []
    expected_sections = ['vitals', 'blackpill', 'training']
    
    def search_html_widgets(elements, found_ids=set()):
        for element in elements:
            if element.get('widgetType') == 'html':
                settings = element.get('settings', {})
                if isinstance(settings, dict):
                    html = settings.get('html', '')
                    # Check for element IDs
                    elem_id = settings.get('_element_id', '')
                    if elem_id:
                        found_ids.add(elem_id)
                    # Also check HTML for id attributes
                    id_matches = re.findall(r'id="([^"]+)"', html)
                    found_ids.update(id_matches)
            if 'elements' in element:
                search_html_widgets(element['elements'], found_ids)
        return found_ids
    
    found_ids = search_html_widgets(json_data.get('content', []))
    
    for expected in expected_sections:
        if expected not in found_ids:
            errors.append(f"Expected section ID '{expected}' not found")
    
    return errors


def check_tp_urls(json_data: Dict) -> List[str]:
    """Check that TrainingPeaks URLs are well-formed."""
    errors = []
    tp_url_pattern = re.compile(r'https://www\.trainingpeaks\.com/training-plans/cycling/[^"\s]+')
    
    def search_urls(elements):
        for element in elements:
            if element.get('widgetType') == 'html':
                settings = element.get('settings', {})
                if isinstance(settings, dict):
                    html = settings.get('html', '')
                    urls = tp_url_pattern.findall(html)
                    for url in urls:
                        # Check URL structure
                        if '/tp-' not in url:
                            errors.append(f"Malformed TP URL: {url[:50]}...")
            if 'elements' in element:
                search_urls(element['elements'])
    
    search_urls(json_data.get('content', []))
    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_output.py <elementor_json.json>")
        sys.exit(1)
    
    json_path = sys.argv[1]
    
    # Check JSON is valid
    if not check_json_valid(json_path):
        print("ERROR: Invalid JSON file")
        sys.exit(1)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    all_errors = []
    
    # Check for placeholders
    placeholder_errors = check_placeholders(json_data)
    all_errors.extend(placeholder_errors)
    
    # Check section IDs
    section_errors = check_section_ids(json_data)
    all_errors.extend(section_errors)
    
    # Check TP URLs
    url_errors = check_tp_urls(json_data)
    all_errors.extend(url_errors)
    
    if all_errors:
        print("VALIDATION FAILED:")
        for error in all_errors:
            print(f"  ✗ {error}")
        sys.exit(1)
    else:
        print("✓ Valid")
        sys.exit(0)


if __name__ == '__main__':
    main()


