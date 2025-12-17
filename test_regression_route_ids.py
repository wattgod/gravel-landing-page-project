#!/usr/bin/env python3
"""
Regression test specifically for RideWithGPS route IDs.
Ensures data files and generated JSONs never have placeholder route IDs.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List


def check_data_file(data_path: Path) -> List[str]:
    """Check a data JSON file for valid route IDs."""
    errors = []
    
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        race_name = data.get('race', {}).get('display_name', 'Unknown')
        course_desc = data.get('race', {}).get('course_description', {})
        rwgps_id = course_desc.get('ridewithgps_id', '')
        rwgps_name = course_desc.get('ridewithgps_name', '')
        
        # Check if route ID exists
        if not rwgps_id:
            errors.append(f"{race_name}: Missing 'ridewithgps_id' in course_description")
            return errors
        
        # Check for placeholder values
        if 'PLACEHOLDER' in rwgps_id.upper() or 'NEEDS_RESEARCH' in rwgps_id.upper():
            errors.append(f"{race_name}: Route ID is still a placeholder: {rwgps_id}")
            return errors
        
        # Check that it's numeric
        if not rwgps_id.isdigit():
            errors.append(f"{race_name}: Route ID must be numeric, found: {rwgps_id}")
            return errors
        
        # Check reasonable length
        if len(rwgps_id) < 6 or len(rwgps_id) > 10:
            errors.append(f"{race_name}: Route ID length suspicious: {rwgps_id} (expected 6-10 digits)")
        
        # Check route name exists
        if not rwgps_name:
            errors.append(f"{race_name}: Missing 'ridewithgps_name' in course_description")
        
    except Exception as e:
        errors.append(f"Error reading {data_path}: {e}")
    
    return errors


def check_generated_json(json_path: Path) -> List[str]:
    """Check a generated Elementor JSON for valid route IDs in HTML."""
    errors = []
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract all HTML content
        html_content = extract_html_from_json(data)
        
        # Find RideWithGPS URLs
        rwgps_pattern = re.compile(r'ridewithgps\.com/embeds\?[^"\s]+')
        urls = rwgps_pattern.findall(html_content)
        
        if not urls:
            # If there's a course map section, there should be a URL
            if 'gg-route-section' in html_content or 'course-map' in html_content:
                errors.append(f"{json_path.name}: Course map section found but no RideWithGPS URL")
            return errors
        
        # Check each URL
        for url in urls:
            id_match = re.search(r'[?&]id=([^&"\s]+)', url)
            if not id_match:
                errors.append(f"{json_path.name}: RideWithGPS URL missing route ID")
                continue
            
            route_id = id_match.group(1)
            
            if 'PLACEHOLDER' in route_id.upper() or 'NEEDS_RESEARCH' in route_id.upper():
                errors.append(f"{json_path.name}: Route ID is still a placeholder: {route_id}")
            elif not route_id.isdigit():
                errors.append(f"{json_path.name}: Route ID must be numeric, found: {route_id}")
            elif len(route_id) < 6 or len(route_id) > 10:
                errors.append(f"{json_path.name}: Route ID length suspicious: {route_id}")
    
    except Exception as e:
        errors.append(f"Error reading {json_path}: {e}")
    
    return errors


def extract_html_from_json(data: Dict) -> str:
    """Recursively extract all HTML content from Elementor JSON."""
    html_parts = []
    
    def traverse(obj):
        if isinstance(obj, dict):
            if obj.get('widgetType') == 'html':
                html = obj.get('settings', {}).get('html', '')
                if html:
                    html_parts.append(html)
            for value in obj.values():
                traverse(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)
    
    traverse(data)
    return '\n'.join(html_parts)


def main():
    """Run route ID regression tests."""
    project_root = Path(__file__).parent
    data_dir = project_root / 'data'
    output_dir = project_root / 'output'
    
    all_errors = []
    
    # Check all data files
    print("Checking data files for valid route IDs...")
    print("=" * 60)
    data_files = list(data_dir.glob('*-data.json'))
    for data_file in sorted(data_files):
        errors = check_data_file(data_file)
        if errors:
            all_errors.extend(errors)
            for error in errors:
                print(f"  ❌ {error}")
        else:
            print(f"  ✓ {data_file.name}")
    
    print()
    
    # Check all generated JSON files (skip backups)
    print("Checking generated JSON files for valid route IDs...")
    print("=" * 60)
    json_files = [f for f in output_dir.glob('elementor-*.json') 
                  if 'FIXED' not in f.name and 'OLD' not in f.name and 'BACKUP' not in f.name]
    
    for json_file in sorted(json_files):
        errors = check_generated_json(json_file)
        if errors:
            all_errors.extend(errors)
            for error in errors:
                print(f"  ❌ {error}")
        else:
            print(f"  ✓ {json_file.name}")
    
    print()
    
    if all_errors:
        print(f"\nFAILED: {len(all_errors)} error(s) found\n")
        for i, error in enumerate(all_errors, 1):
            print(f"  {i}. {error}")
        sys.exit(1)
    else:
        print("✓ All route ID tests passed")
        sys.exit(0)


if __name__ == '__main__':
    main()
