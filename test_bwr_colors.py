#!/usr/bin/env python3
"""
Regression test: Validate BWR uses only correct Gravel God brand yellow
"""
import json
import re
import sys

# Correct Gravel God brand yellow
BRAND_YELLOW = '#F4D03F'

# Wrong yellows that should NOT exist
FORBIDDEN_COLORS = [
    '#FFFF00',  # Pure neon yellow (too bright)
    '#FFF5E6',  # Muted cream (too pale)
]

def test_color_palette(json_file):
    """Test that BWR JSON uses correct brand colors"""
    
    with open(json_file, 'r') as f:
        content = f.read()
        data = json.loads(content)
    
    print(f"Testing color palette in: {json_file}")
    print("=" * 60)
    
    errors = []
    
    # Test 1: No forbidden colors
    print("\n[TEST 1] Checking for forbidden colors...")
    for forbidden in FORBIDDEN_COLORS:
        # Case-insensitive search
        pattern = re.compile(re.escape(forbidden), re.IGNORECASE)
        matches = pattern.findall(content)
        
        if matches:
            errors.append(f"FOUND FORBIDDEN COLOR: {forbidden} ({len(matches)} instances)")
            print(f"  ❌ FAIL: Found {len(matches)} instances of {forbidden}")
        else:
            print(f"  ✅ PASS: No instances of {forbidden}")
    
    # Test 2: Brand yellow is used
    print("\n[TEST 2] Checking for brand yellow usage...")
    brand_pattern = re.compile(re.escape(BRAND_YELLOW), re.IGNORECASE)
    brand_matches = brand_pattern.findall(content)
    
    if brand_matches:
        print(f"  ✅ PASS: Found {len(brand_matches)} instances of {BRAND_YELLOW}")
    else:
        errors.append(f"MISSING BRAND COLOR: {BRAND_YELLOW} not found")
        print(f"  ❌ FAIL: Brand yellow {BRAND_YELLOW} not found")
    
    # Test 3: Validate specific CSS rules
    print("\n[TEST 3] Checking specific CSS rules...")
    
    critical_rules = [
        ('.gg-pill', 'background', BRAND_YELLOW),
        ('.gg-training-plans-badge', 'background', BRAND_YELLOW),
        ('.gg-timeline-year', 'background', BRAND_YELLOW),
        ('.gg-timeline-event::before', 'background', BRAND_YELLOW),
    ]
    
    for selector, property, expected_color in critical_rules:
        # Search for the pattern in CSS
        pattern = rf'{re.escape(selector)}.*?{property}:\s*([#\w]+)'
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        
        if match:
            found_color = match.group(1).upper()
            if found_color == expected_color.upper():
                print(f"  ✅ PASS: {selector} {property} = {found_color}")
            else:
                errors.append(f"{selector} {property} uses {found_color}, expected {expected_color}")
                print(f"  ❌ FAIL: {selector} {property} = {found_color} (expected {expected_color})")
        else:
            print(f"  ⚠️  WARN: Could not find {selector} {property} rule")
    
    # Test 4: Check table alternating rows
    print("\n[TEST 4] Checking table/card alternating backgrounds...")
    
    alternating_patterns = [
        r'nth-child\(odd\).*?background:\s*#([A-Fa-f0-9]{6})',
        r'nth-child\(even\).*?background:\s*#([A-Fa-f0-9]{6})',
    ]
    
    for pattern in alternating_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for color in matches:
            color_hex = f'#{color.upper()}'
            if color_hex == BRAND_YELLOW:
                print(f"  ✅ PASS: Alternating row uses {color_hex}")
            elif color_hex in ['#FFFFFF', '#F5F5DC', '#F0F0F0']:
                print(f"  ✅ PASS: Alternating row uses neutral {color_hex}")
            elif color_hex.upper() in [c.upper() for c in FORBIDDEN_COLORS]:
                errors.append(f"Alternating row uses forbidden color {color_hex}")
                print(f"  ❌ FAIL: Alternating row uses forbidden {color_hex}")
    
    # Final summary
    print("\n" + "=" * 60)
    if errors:
        print(f"❌ TEST FAILED: {len(errors)} error(s) found")
        for error in errors:
            print(f"   - {error}")
        return False
    else:
        print("✅ ALL TESTS PASSED")
        print(f"Brand yellow ({BRAND_YELLOW}) is used consistently")
        print("No forbidden colors found")
        return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python test_bwr_colors.py <elementor-json-file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    success = test_color_palette(json_file)
    sys.exit(0 if success else 1)
