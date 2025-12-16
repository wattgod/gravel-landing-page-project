#!/usr/bin/env python3
"""
NEO BRUTALIST STYLING REGRESSION TEST
=====================================
Ensures all sections maintain consistent neo-brutalist styling:
- Bold borders (4px solid #000000)
- High contrast colors (black, white, yellow #FFFF00)
- Consistent box shadows (8px 8px 0px 0px #000000)
- No rounded corners
- Raw, geometric aesthetic

Exit codes:
    0 = All tests passed
    1 = Styling violations detected
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any

def check_css_file(css_path: Path) -> List[str]:
    """Check CSS file for neo-brutalist compliance."""
    errors = []
    
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css = f.read()
    except Exception as e:
        return [f"Failed to read CSS file: {e}"]
    
    # Check for neo-brutalist color palette
    if '#FFFF00' not in css and 'yellow' not in css.lower():
        errors.append("Missing bright yellow accent color (#FFFF00)")
    
    # Check for bold borders (should be 4px solid #000000)
    border_pattern = r'border:\s*(\d+)px\s*solid\s*#000000'
    border_matches = re.findall(border_pattern, css)
    if not border_matches:
        errors.append("No bold black borders found (4px solid #000000)")
    
    # Check for box shadows (neo-brutalist signature)
    shadow_pattern = r'box-shadow:\s*(\d+)px\s*(\d+)px\s*0px\s*0px'
    shadow_matches = re.findall(shadow_pattern, css)
    if not shadow_matches:
        errors.append("No neo-brutalist box shadows found (8px 8px 0px 0px)")
    
    # Check for rounded corners (should NOT exist in neo-brutalist)
    rounded_patterns = [
        r'border-radius:\s*[^0;]+',
        r'border-radius:\s*\d+',
    ]
    for pattern in rounded_patterns:
        matches = re.findall(pattern, css, re.IGNORECASE)
        if matches:
            # Allow border-radius: 0 or border-radius: 999px for pills (acceptable)
            for match in matches:
                if '999px' not in match and '0' not in match:
                    errors.append(f"Rounded corners found (not neo-brutalist): {match}")
    
    return errors

def check_elementor_file(elementor_path: Path) -> List[str]:
    """Check Elementor JSON for neo-brutalist class usage."""
    errors = []
    
    try:
        with open(elementor_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return [f"Failed to parse Elementor file: {e}"]
    
    # Convert to string for searching
    content_str = json.dumps(data)
    
    # Check for required neo-brutalist classes
    required_classes = [
        'gg-zone-card',
        'gg-vitals-table',
        'gg-timeline-section',
        'gg-timeline-event',
        'gg-timeline-year',
    ]
    
    missing_classes = []
    for cls in required_classes:
        if cls not in content_str:
            missing_classes.append(cls)
    
    if missing_classes:
        errors.append(f"Missing neo-brutalist classes: {', '.join(missing_classes)}")
    
    # Check for inline styles that might override neo-brutalist (bad practice)
    inline_style_pattern = r'style="[^"]*border-radius[^"]*"'
    inline_rounded = re.findall(inline_style_pattern, content_str, re.IGNORECASE)
    if inline_rounded:
        errors.append(f"Found inline styles with border-radius (not neo-brutalist): {len(inline_rounded)} instances")
    
    # Check for consistent zone card structure
    zone_card_pattern = r'gg-zone-card[^>]*>'
    zone_cards = re.findall(zone_card_pattern, content_str)
    if zone_cards:
        # Should have zone-mile, zone-label, zone-desc
        if 'gg-zone-mile' not in content_str:
            errors.append("Zone cards missing gg-zone-mile class")
        if 'gg-zone-label' not in content_str:
            errors.append("Zone cards missing gg-zone-label class")
        if 'gg-zone-desc' not in content_str:
            errors.append("Zone cards missing gg-zone-desc class")
    
    # Check vitals table structure
    if 'gg-vitals-table' in content_str:
        if '<th>' not in content_str or '<td>' not in content_str:
            errors.append("Vitals table missing proper th/td structure")
    
    # Check timeline structure
    if 'gg-timeline-section' in content_str:
        if 'gg-timeline-year' not in content_str:
            errors.append("Timeline missing gg-timeline-year class")
        if 'gg-timeline-content' not in content_str:
            errors.append("Timeline missing gg-timeline-content class")
    
    return errors

def check_css_in_page_settings(elementor_path: Path) -> List[str]:
    """Verify neo-brutalist CSS is included in page_settings."""
    errors = []
    
    try:
        with open(elementor_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return [f"Failed to parse Elementor file: {e}"]
    
    custom_css = data.get('page_settings', {}).get('custom_css', '')
    content_str = json.dumps(data)
    
    if not custom_css:
        errors.append("No custom_css in page_settings")
        return errors
    
    # Only check for styles if the file actually uses those sections
    uses_neo_brutalist = False
    
    if 'gg-zone-card' in content_str:
        uses_neo_brutalist = True
        if not re.search(r'\.gg-zone-card', custom_css):
            errors.append("Missing Zone card styles in page_settings.custom_css")
    
    if 'gg-vitals-table' in content_str:
        uses_neo_brutalist = True
        if not re.search(r'\.gg-vitals-table', custom_css):
            errors.append("Missing Vitals table styles in page_settings.custom_css")
    
    if 'gg-timeline-section' in content_str:
        uses_neo_brutalist = True
        if not re.search(r'\.gg-timeline-section', custom_css):
            errors.append("Missing Timeline section styles in page_settings.custom_css")
    
    # Only check for core neo-brutalist patterns if file uses neo-brutalist sections
    if uses_neo_brutalist:
        if not re.search(r'border:\s*4px\s*solid\s*#000000', custom_css):
            errors.append("Missing Bold black borders in page_settings.custom_css")
        if not re.search(r'box-shadow:\s*8px\s*8px\s*0px\s*0px\s*#000000', custom_css):
            errors.append("Missing Neo-brutalist box shadows in page_settings.custom_css")
        if not re.search(r'#FFFF00', custom_css):
            errors.append("Missing Bright yellow accent color in page_settings.custom_css")
    
    return errors

def main():
    """Run all neo-brutalist styling regression tests."""
    css_file = Path('assets/css/landing-page.css')
    output_dir = Path('output')
    
    all_errors = []
    
    # Test CSS file
    if css_file.exists():
        print(f"Testing {css_file.name}...")
        css_errors = check_css_file(css_file)
        all_errors.extend([f"CSS: {e}" for e in css_errors])
    else:
        all_errors.append("CSS file not found: assets/css/landing-page.css")
    
    # Test Elementor JSON files
    for json_file in output_dir.glob('elementor-*.json'):
        print(f"Testing {json_file.name}...")
        elementor_errors = check_elementor_file(json_file)
        all_errors.extend([f"{json_file.name}: {e}" for e in elementor_errors])
        
        # Check CSS in page_settings
        css_errors = check_css_in_page_settings(json_file)
        all_errors.extend([f"{json_file.name} (CSS): {e}" for e in css_errors])
    
    # Report results
    if all_errors:
        print("\n" + "="*70)
        print("NEO BRUTALIST STYLING VIOLATIONS DETECTED")
        print("="*70)
        for error in all_errors:
            print(f"  ❌ {error}")
        print("\n" + "="*70)
        print(f"Total violations: {len(all_errors)}")
        print("\nNeo-brutalist requirements:")
        print("  - Bold borders: 4px solid #000000")
        print("  - High contrast: black, white, yellow (#FFFF00)")
        print("  - Box shadows: 8px 8px 0px 0px #000000")
        print("  - No rounded corners (except pills)")
        print("  - Raw, geometric aesthetic")
        return 1
    else:
        print("\n" + "="*70)
        print("✅ ALL NEO BRUTALIST STYLING TESTS PASSED")
        print("="*70)
        print("All sections maintain consistent neo-brutalist styling.")
        return 0

if __name__ == '__main__':
    sys.exit(main())

