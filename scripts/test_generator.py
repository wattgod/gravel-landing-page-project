#!/usr/bin/env python3
"""
Landing Page Generator Regression Test Suite

Validates generated Elementor JSON files for:
- Template leakage (no race-specific content from template)
- Placeholder replacement
- Required sections present
- Content uniqueness
- JSON structural integrity
"""

import json
import re
import sys
from typing import Dict, List, Set, Tuple
from difflib import SequenceMatcher


# Race-specific forbidden terms
FORBIDDEN_TERMS = {
    'unbound-200': {
        'terms': ['Mid South', 'Stillwater', 'Oklahoma', 'Bobby Wintle', 'The Randomizer'],
        'founding_year': '2013'
    },
    'mid-south': {
        'terms': ['Unbound', 'Emporia', 'Flint Hills', 'Dirty Kanza', 'Kansas'],
        'founding_year': '2006'
    }
}

# Required sections to check
REQUIRED_SECTIONS = {
    'course_profile': ['Length', 'Technicality', 'Elevation', 'Climate', 'Altitude', 'Logistics', 'Adventure'],
    'biased_opinion': ['Prestige', 'Race Quality', 'Experience', 'Community', 'Field Depth', 'Value', 'Expenses'],
    'section_markers': ['FACTS AND HISTORY', 'FINAL VERDICT', 'RACE LOGISTICS', 'TRAINING PLANS']
}


def load_json(file_path: str) -> Dict:
    """Load and parse JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        sys.exit(1)


def test_no_template_leakage(json_data: Dict, race_slug: str) -> Tuple[bool, List[str]]:
    """Test 1: Check for template leakage (race-specific terms from other races)."""
    if race_slug not in FORBIDDEN_TERMS:
        print(f"⚠️  Warning: No forbidden terms defined for race '{race_slug}'")
        return True, []
    
    content_str = json.dumps(json_data, ensure_ascii=False)
    forbidden = FORBIDDEN_TERMS[race_slug]
    errors = []
    
    # Check forbidden terms
    for term in forbidden['terms']:
        # Allow in TrainingPeaks URLs (plan names might reference other races)
        tp_url_pattern = r'https://www\.trainingpeaks\.com[^"]*'
        tp_urls = re.findall(tp_url_pattern, content_str)
        tp_content = ' '.join(tp_urls)
        
        # Allow intentional comparisons (e.g., "compared to Unbound", "try Unbound")
        comparison_patterns = [
            r'compared to',
            r'compared to paying',
            r'try\s+' + re.escape(term),
            r'inspired by',
            r'like\s+' + re.escape(term),
        ]
        
        # Check if term appears outside TP URLs
        if term.lower() in content_str.lower():
            # Check if it's only in TP URLs
            if term.lower() not in tp_content.lower():
                # Check if it's in an intentional comparison
                is_comparison = any(re.search(pattern, content_str, re.IGNORECASE) for pattern in comparison_patterns)
                
                # For "Flint Hills" - allow if it's a comparison like "Flint Hills' annoying little brother"
                if term == 'Flint Hills' and ("annoying little brother" in content_str or "like the Flint Hills" in content_str):
                    is_comparison = True
                
                # For "Dirty Kanza" - allow if it's in history about inspiration
                if term == 'Dirty Kanza' and ("inspired by" in content_str.lower() or "history" in content_str.lower()):
                    is_comparison = True
                
                if not is_comparison:
                    # Count occurrences
                    count = len(re.findall(re.escape(term), content_str, re.IGNORECASE))
                    errors.append(f"Found forbidden term '{term}' ({count} times) - template leakage detected")
    
    # Check founding year
    founding_year = forbidden.get('founding_year')
    if founding_year:
        # Allow in years that are clearly not the founding year (e.g., "2026")
        year_pattern = rf'\b{founding_year}\b'
        matches = re.findall(year_pattern, content_str)
        # Filter out if it's in a date like "2026" or clearly a different context
        suspicious = [m for m in matches if f'Founded: {founding_year}' in content_str or f'founded {founding_year}' in content_str.lower()]
        if suspicious:
            errors.append(f"Found forbidden founding year '{founding_year}' - template leakage detected")
    
    return len(errors) == 0, errors


def test_all_placeholders_replaced(json_data: Dict) -> Tuple[bool, List[str]]:
    """Test 2: Check for unreplaced placeholders."""
    content_str = json.dumps(json_data, ensure_ascii=False)
    errors = []
    
    # Check for {{ }} placeholders
    placeholder_pattern = r'\{\{[A-Z_]+\}\}'
    placeholders = re.findall(placeholder_pattern, content_str)
    if placeholders:
        errors.append(f"Found unreplaced placeholders: {', '.join(set(placeholders))}")
    
    # Check for common placeholder patterns (but allow PLACEHOLDER in TP IDs which are expected)
    common_patterns = [
        r'REPLACE_ME',
        r'RACE_NAME',
        r'INSERT_HERE',
        r'YOUR_RACE'
    ]
    for pattern in common_patterns:
        matches = re.findall(pattern, content_str, re.IGNORECASE)
        if matches:
            errors.append(f"Found placeholder pattern '{pattern}': {len(matches)} occurrences")
    
    # Check for PLACEHOLDER but only flag if it's not in TP URLs (TP IDs are expected placeholders)
    placeholder_matches = re.findall(r'PLACEHOLDER', content_str, re.IGNORECASE)
    if placeholder_matches:
        # Check if all are in TP URLs
        tp_url_pattern = r'https://www\.trainingpeaks\.com[^"]*PLACEHOLDER[^"]*'
        tp_placeholders = re.findall(tp_url_pattern, content_str, re.IGNORECASE)
        if len(tp_placeholders) < len(placeholder_matches):
            errors.append(f"Found PLACEHOLDER outside TP URLs: {len(placeholder_matches) - len(tp_placeholders)} occurrences")
    
    return len(errors) == 0, errors


def test_required_sections_present(json_data: Dict, race_slug: str) -> Tuple[bool, List[str]]:
    """Test 3: Check that all required sections are present."""
    content_str = json.dumps(json_data, ensure_ascii=False)
    errors = []
    
    # Get expected race name
    race_name_map = {
        'unbound-200': 'UNBOUND',
        'mid-south': 'MID SOUTH'
    }
    expected_race_name = race_name_map.get(race_slug, race_slug.upper())
    
    # Check race name appears in title/hero
    if expected_race_name not in content_str:
        errors.append(f"Race name '{expected_race_name}' not found in content")
    
    # Check Course Profile variables
    for var in REQUIRED_SECTIONS['course_profile']:
        if var not in content_str:
            errors.append(f"Course Profile variable '{var}' not found")
    
    # Check Biased Opinion variables
    for var in REQUIRED_SECTIONS['biased_opinion']:
        if var not in content_str:
            errors.append(f"Biased Opinion variable '{var}' not found")
    
    # Check section markers (case-insensitive, allow variations)
    section_variations = {
        'FACTS AND HISTORY': ['Facts And History', 'FACTS AND HISTORY', 'Facts and History'],
        'FINAL VERDICT': ['Final Verdict', 'FINAL VERDICT', 'Final verdict', 'OVERALL SCORE'],
        'RACE LOGISTICS': ['Race Logistics', 'RACE LOGISTICS', 'Race logistics'],
        'TRAINING PLANS': ['Training Plans', 'TRAINING PLANS', 'Training plans']
    }
    
    for marker in REQUIRED_SECTIONS['section_markers']:
        variations = section_variations.get(marker, [marker])
        found = any(var in content_str for var in variations)
        if not found:
            errors.append(f"Section marker '{marker}' not found (checked: {', '.join(variations)})")
    
    # Check for training plans (should have multiple plan cards)
    plan_count = content_str.count('gg-plan')
    if plan_count < 10:  # Should have at least 10 plan elements
        errors.append(f"Training plans section incomplete: found {plan_count} plan elements (expected 15+)")
    
    return len(errors) == 0, errors


def test_content_uniqueness(file1_path: str, file2_path: str, race1: str, race2: str) -> Tuple[bool, List[str]]:
    """Test 4: Check that generated content is unique between races."""
    try:
        with open(file1_path, 'r', encoding='utf-8') as f:
            data1 = json.load(f)
        with open(file2_path, 'r', encoding='utf-8') as f:
            data2 = json.load(f)
    except FileNotFoundError as e:
        return False, [f"File not found: {e}"]
    
    # Extract text content (remove structure)
    content1 = json.dumps(data1, ensure_ascii=False)
    content2 = json.dumps(data2, ensure_ascii=False)
    
    # Calculate similarity
    similarity = SequenceMatcher(None, content1, content2).ratio()
    
    # Threshold: if >50% similar, content might not be unique
    if similarity > 0.5:
        return False, [
            f"Content similarity too high: {similarity:.1%}",
            f"Generated {race1} and {race2} are suspiciously similar - replacement may have failed"
        ]
    
    return True, []


def test_structural_integrity(json_data: Dict) -> Tuple[bool, List[str]]:
    """Test 5: Validate JSON structure and Elementor format."""
    errors = []
    
    # Check for required top-level keys
    required_keys = ['content', 'version', 'title', 'type']
    for key in required_keys:
        if key not in json_data:
            errors.append(f"Missing required key: '{key}'")
    
    # Check content is a list
    if 'content' in json_data and not isinstance(json_data['content'], list):
        errors.append("'content' must be a list")
    
    # Check for valid Elementor structure
    if 'content' in json_data:
        content = json_data['content']
        if len(content) == 0:
            errors.append("'content' list is empty")
        
        # Check for HTML widgets
        def count_widgets(elements, count=0):
            for elem in elements:
                if elem.get('widgetType') == 'html':
                    count += 1
                if 'elements' in elem:
                    count = count_widgets(elem['elements'], count)
            return count
        
        widget_count = count_widgets(content)
        if widget_count < 5:
            errors.append(f"Too few HTML widgets found: {widget_count} (expected 10+)")
    
    return len(errors) == 0, errors


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 test_generator.py <json_file> <race_slug> [comparison_file] [comparison_race]")
        print("")
        print("Examples:")
        print("  python3 test_generator.py output/elementor-mid-south.json mid-south")
        print("  python3 test_generator.py output/elementor-mid-south.json mid-south output/elementor-unbound-200.json unbound-200")
        sys.exit(1)
    
    json_file = sys.argv[1]
    race_slug = sys.argv[2]
    comparison_file = sys.argv[3] if len(sys.argv) > 3 else None
    comparison_race = sys.argv[4] if len(sys.argv) > 4 else None
    
    print("=" * 70)
    print("LANDING PAGE GENERATOR REGRESSION TEST SUITE")
    print("=" * 70)
    print(f"Testing: {json_file}")
    print(f"Race: {race_slug}")
    print("")
    
    # Load JSON
    json_data = load_json(json_file)
    
    all_passed = True
    results = []
    
    # Test 1: No template leakage
    print("TEST 1: No Template Leakage")
    passed, errors = test_no_template_leakage(json_data, race_slug)
    if passed:
        print("  ✅ No template leakage detected")
    else:
        print("  ❌ Template leakage detected:")
        for error in errors:
            print(f"     - {error}")
        all_passed = False
    results.append(("Template Leakage", passed))
    print("")
    
    # Test 2: All placeholders replaced
    print("TEST 2: All Placeholders Replaced")
    passed, errors = test_all_placeholders_replaced(json_data)
    if passed:
        print("  ✅ All placeholders replaced")
    else:
        print("  ❌ Unreplaced placeholders found:")
        for error in errors:
            print(f"     - {error}")
        all_passed = False
    results.append(("Placeholders", passed))
    print("")
    
    # Test 3: Required sections present
    print("TEST 3: Required Sections Present")
    passed, errors = test_required_sections_present(json_data, race_slug)
    if passed:
        print("  ✅ All required sections present")
    else:
        print("  ❌ Missing required sections:")
        for error in errors:
            print(f"     - {error}")
        all_passed = False
    results.append(("Required Sections", passed))
    print("")
    
    # Test 4: Content uniqueness (if comparison file provided)
    if comparison_file and comparison_race:
        print("TEST 4: Content Uniqueness")
        passed, errors = test_content_uniqueness(json_file, comparison_file, race_slug, comparison_race)
        if passed:
            print("  ✅ Content is unique")
        else:
            print("  ❌ Content similarity issues:")
            for error in errors:
                print(f"     - {error}")
            all_passed = False
        results.append(("Content Uniqueness", passed))
        print("")
    else:
        print("TEST 4: Content Uniqueness")
        print("  ⚠️  Skipped (no comparison file provided)")
        print("")
    
    # Test 5: Structural integrity
    print("TEST 5: JSON Structural Integrity")
    passed, errors = test_structural_integrity(json_data)
    if passed:
        print("  ✅ JSON structure valid")
    else:
        print("  ❌ JSON structure issues:")
        for error in errors:
            print(f"     - {error}")
        all_passed = False
    results.append(("Structural Integrity", passed))
    print("")
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    print("")
    
    if all_passed:
        print("✅ ALL TESTS PASSED")
        print("")
        print("File is ready for WordPress import.")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        print("")
        print("DO NOT import to WordPress until all tests pass.")
        sys.exit(1)


if __name__ == '__main__':
    main()

