#!/usr/bin/env python3
"""
COLOR PALETTE REGRESSION TEST
==============================
Ensures all content follows Gravel God neobrutalist color palette:
- Brand yellow (#F4D03F) allowed for backgrounds and accents (use judiciously)
- Forbidden: Neon yellow (#FFFF00) - never use, replace with brand yellow (#F4D03F)
- Forbidden: Muted cream (#FFF5E6) - replace with brand yellow (#F4D03F) or earth tones

Exit codes:
    0 = All color palette tests passed
    1 = Color palette violations detected
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Tuple

# ============================================================================
# COLOR PALETTE RULES
# ============================================================================

# Forbidden yellows (neon yellow - never use)
FORBIDDEN_YELLOWS = [
    '#FFFF00',
    '#ffff00',
    'FFFF00',
]

# Brand yellow (allowed, but use judiciously - not excessively)
BRAND_YELLOW = [
    '#F4D03F',
    '#f4d03f',
    'F4D03F',
]

# Muted earth tones that SHOULD be used for backgrounds
CORRECT_BACKGROUND_COLORS = [
    '#FFF5E6',  # Muted cream
    '#fff5e6',
    '#F5E5D3',  # Cream
    '#f5e5d3',
    '#BFA595',  # Sand
    '#bfa595',
    '#E8DDD0',  # Light sand
    '#e8ddd0',
    '#FFF9E3',  # Pale yellow-cream
    '#fff9e3',
]

# Selectors that indicate LARGE background areas (forbidden for bright yellow)
LARGE_BACKGROUND_SELECTORS = [
    r'\.gg-vitals-table\s+tr[^}]*background',
    r'\.gg-vitals-table\s+td[^}]*background',
    r'\.gg-zone-card[^}]*background',
    r'\.gg-fact-card[^}]*background',
    r'\.gg-course-breakdown-note[^}]*background',
    r'tr:nth-child\([^)]+\)[^}]*background',
    r'td:nth-child\([^)]+\)[^}]*background',
    r'\.gg-plan-card[^}]*background',
    r'\.gg-overall-card[^}]*background',
]

# Selectors that indicate SMALL accents (bright yellow acceptable)
# NOTE: Bright yellow is FORBIDDEN everywhere - NO yellow in backgrounds, NO yellow in box-shadows
# Only text-shadow is acceptable (but even that should be minimal)
SMALL_ACCENT_SELECTORS = [
    r'text-shadow',  # Text shadow - ONLY acceptable use of bright yellow (and even this should be minimal)
]

# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def check_css_file(css_path: Path) -> List[str]:
    """Check CSS file for color palette violations."""
    errors = []
    
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css = f.read()
    except Exception as e:
        return [f"Failed to read CSS file: {e}"]
    
    # Find all background declarations with forbidden yellow (neon yellow)
    background_pattern = r'background[^:]*:\s*([^;]+);'
    background_matches = re.finditer(background_pattern, css, re.IGNORECASE)
    
    for match in background_matches:
        background_value = match.group(1).strip()
        line_num = css[:match.start()].count('\n') + 1
        
        # Check if this background uses forbidden neon yellow (#FFFF00)
        for yellow in FORBIDDEN_YELLOWS:
            if yellow in background_value:
                # Extract selector for better error message
                context_before = css[max(0, match.start() - 200):match.start()]
                selector_match = re.search(r'([^{]+)\{', context_before[-100:])
                selector = selector_match.group(1).strip() if selector_match else "unknown"
                errors.append(
                    f"Line {line_num}: Forbidden neon yellow ({yellow}) used in '{selector}'. "
                    f"Use brand yellow (#F4D03F) instead."
                )
    
    # Check for forbidden neon yellow in box-shadows
    boxshadow_pattern = r'box-shadow[^:]*:\s*([^;]+);'
    boxshadow_matches = re.finditer(boxshadow_pattern, css, re.IGNORECASE)
    
    for match in boxshadow_matches:
        boxshadow_value = match.group(1).strip()
        line_num = css[:match.start()].count('\n') + 1
        
        # Check if this box-shadow uses forbidden neon yellow
        for yellow in FORBIDDEN_YELLOWS:
            if yellow in boxshadow_value:
                # Extract selector for better error message
                context_before = css[max(0, match.start() - 200):match.start()]
                selector_match = re.search(r'([^{]+)\{', context_before[-100:])
                selector = selector_match.group(1).strip() if selector_match else "unknown"
                errors.append(
                    f"Line {line_num}: Forbidden neon yellow ({yellow}) used in box-shadow for '{selector}'. "
                    f"Use brand yellow (#F4D03F) or brown (#59473C) instead."
                )
    
    return errors

def check_elementor_file(elementor_path: Path) -> List[str]:
    """Check Elementor JSON for color palette violations."""
    errors = []
    
    try:
        with open(elementor_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return [f"Failed to parse Elementor file: {e}"]
    
    # Convert to string for searching
    content_str = json.dumps(data)
    
    # Check custom_css in page_settings
    custom_css = data.get('page_settings', {}).get('custom_css', '')
    if custom_css:
        css_errors = check_css_content(custom_css, f"{elementor_path.name} (custom_css)")
        errors.extend(css_errors)
    
    # Check HTML content for inline styles
    html_pattern = r'"html"\s*:\s*"([^"]+)"'
    html_matches = re.finditer(html_pattern, content_str)
    
    for match in html_matches:
        html_content = match.group(1)
        # Unescape JSON string
        html_content = html_content.replace('\\n', '\n').replace('\\"', '"').replace('\\/', '/')
        
        # Check for bright yellow in style tags
        style_pattern = r'<style[^>]*>([^<]+)</style>'
        style_matches = re.finditer(style_pattern, html_content, re.IGNORECASE | re.DOTALL)
        
        for style_match in style_matches:
            style_content = style_match.group(1)
            css_errors = check_css_content(style_content, f"{elementor_path.name} (inline styles)")
            errors.extend(css_errors)
    
    return errors

def check_css_content(css: str, context: str) -> List[str]:
    """Check CSS content string for violations."""
    errors = []
    
    # Find all background declarations with forbidden neon yellow
    background_pattern = r'background[^:]*:\s*([^;]+);'
    background_matches = re.finditer(background_pattern, css, re.IGNORECASE)
    
    for match in background_matches:
        background_value = match.group(1).strip()
        
        # Check if this background uses forbidden neon yellow (#FFFF00)
        for yellow in FORBIDDEN_YELLOWS:
            if yellow in background_value:
                # Extract selector for better error message
                context_before = css[max(0, match.start() - 200):match.start()]
                selector_match = re.search(r'([^{]+)\{', context_before[-100:])
                selector = selector_match.group(1).strip() if selector_match else "unknown"
                errors.append(
                    f"{context}: Forbidden neon yellow ({yellow}) used for background in '{selector}'. "
                    f"Use brand yellow (#F4D03F) instead."
                )
    
    # Check for forbidden neon yellow in box-shadows
    boxshadow_pattern = r'box-shadow[^:]*:\s*([^;]+);'
    boxshadow_matches = re.finditer(boxshadow_pattern, css, re.IGNORECASE)
    
    for match in boxshadow_matches:
        boxshadow_value = match.group(1).strip()
        
        # Check if this box-shadow uses forbidden neon yellow
        for yellow in FORBIDDEN_YELLOWS:
            if yellow in boxshadow_value:
                # Extract selector for better error message
                context_before = css[max(0, match.start() - 200):match.start()]
                selector_match = re.search(r'([^{]+)\{', context_before[-100:])
                selector = selector_match.group(1).strip() if selector_match else "unknown"
                errors.append(
                    f"{context}: Forbidden neon yellow ({yellow}) used in box-shadow for '{selector}'. "
                    f"Use brand yellow (#F4D03F) or brown (#59473C) instead."
                )
    
    return errors

def check_generation_script(script_path: Path) -> List[str]:
    """Check generation script for color palette violations."""
    errors = []
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            script = f.read()
    except Exception as e:
        return [f"Failed to read script file: {e}"]
    
    # Find all background declarations with forbidden neon yellow
    background_pattern = r'background[^:]*:\s*([^;]+)'
    background_matches = re.finditer(background_pattern, script, re.IGNORECASE)
    
    for match in background_matches:
        background_value = match.group(1).strip()
        line_num = script[:match.start()].count('\n') + 1
        
        # Check if this background uses forbidden neon yellow
        for yellow in FORBIDDEN_YELLOWS:
            if yellow in background_value:
                errors.append(
                    f"Line {line_num}: Forbidden neon yellow ({yellow}) used for background. "
                    f"Use brand yellow (#F4D03F) instead."
                )
    
    return errors

# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def main():
    """Run all color palette regression tests."""
    css_file = Path('assets/css/landing-page.css')
    script_file = Path('scripts/generate_landing_page.py')
    output_dir = Path('output')
    
    all_errors = []
    
    # Test CSS file
    if css_file.exists():
        print(f"Testing {css_file.name}...")
        css_errors = check_css_file(css_file)
        all_errors.extend([f"CSS: {e}" for e in css_errors])
    else:
        all_errors.append("CSS file not found: assets/css/landing-page.css")
    
    # Test generation script
    if script_file.exists():
        print(f"Testing {script_file.name}...")
        script_errors = check_generation_script(script_file)
        all_errors.extend([f"Script: {e}" for e in script_errors])
    else:
        all_errors.append("Generation script not found: scripts/generate_landing_page.py")
    
    # Test Elementor JSON files (exclude backup/old files)
    for json_file in output_dir.glob('elementor-*.json'):
        # Skip backup/old files
        if any(skip in json_file.name.lower() for skip in ['fixed', 'old', 'backup', 'corrected']):
            continue
        print(f"Testing {json_file.name}...")
        elementor_errors = check_elementor_file(json_file)
        all_errors.extend([f"{json_file.name}: {e}" for e in elementor_errors])
    
    # Report results
    if all_errors:
        print("\n" + "="*70)
        print("COLOR PALETTE VIOLATIONS DETECTED")
        print("="*70)
        for error in all_errors:
            print(f"  ❌ {error}")
        print("\n" + "="*70)
        print(f"Total violations: {len(all_errors)}")
        print("\nColor palette rules:")
        print("  ✅ Brand yellow (#F4D03F) allowed for backgrounds and accents (use judiciously)")
        print("  ❌ Forbidden: Neon yellow (#FFFF00) - never use, replace with brand yellow")
        print("  ❌ Forbidden: Muted cream (#FFF5E6) - replace with brand yellow or earth tones")
        print("\nSee documentation/COLOR_PALETTE_RULES.md for details.")
        return 1
    else:
        print("\n" + "="*70)
        print("✅ ALL COLOR PALETTE TESTS PASSED")
        print("="*70)
        print("All files follow neobrutalist color palette:")
        print("  - Brand yellow (#F4D03F) used judiciously for backgrounds and accents")
        print("  - No forbidden neon yellow (#FFFF00) or muted cream (#FFF5E6)")
        return 0

if __name__ == '__main__':
    sys.exit(main())
