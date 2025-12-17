#!/usr/bin/env python3
"""
REGRESSION TEST: Simplified Marketplace Description Structure
============================================================
Ensures marketplace descriptions use the new simplified template structure:
- Uses simplified template (not old neo-brutalist template)
- Has correct HTML structure with Courier New font, max-width:800px
- Contains required sections: tier philosophy, training approach, plan features, etc.
- No old template placeholders or sections

Exit codes:
    0 = All tests passed
    1 = Structure violations detected
"""

import re
import sys
from pathlib import Path


def check_simplified_structure(marketplace_path):
    """Check if marketplace description uses simplified template structure"""
    with open(marketplace_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    errors = []
    
    # Check for simplified template structure
    if 'font-family:\'Courier New\'' not in content:
        errors.append("Missing Courier New font family")
    
    if 'max-width:800px' not in content:
        errors.append("Missing max-width:800px")
    
    if 'color:#111' not in content:
        errors.append("Missing color:#111")
    
    # Check for required sections
    if 'TIER_PHILOSOPHY' in content or '{{TIER_PHILOSOPHY}}' in content:
        errors.append("Unreplaced placeholder: TIER_PHILOSOPHY")
    
    if 'What the' not in content or 'Includes' not in content:
        errors.append("Missing 'What the [Plan] Includes' section")
    
    if '18,000+ Word Guide' not in content:
        errors.append("Missing guide content summary section")
    
    if 'Alternative?' not in content:
        errors.append("Missing 'Alternative?' section")
    
    if 'What This Plan Delivers' not in content:
        errors.append("Missing 'What This Plan Delivers' section")
    
    # Check for old template remnants (should NOT be present)
    if 'background:#F5F5DC' in content:
        errors.append("Contains old template background color")
    
    if 'GRAVEL GOD CYCLING' in content and '---' in content and content.count('GRAVEL GOD CYCLING') > 1:
        # Old template had GRAVEL GOD CYCLING header, new one only in footer
        if content.find('GRAVEL GOD CYCLING') < content.find('What the'):
            errors.append("Contains old template header structure")
    
    if 'border:4px solid #000;box-shadow:8px 8px 0' in content:
        errors.append("Contains old template box-shadow styling")
    
    # Check for race-specific content
    if 'This is' not in content or 'For people whose fitness' not in content:
        errors.append("Missing race-specific closing statement")
    
    # Check for footer
    if 'GRAVEL GOD CYCLING' not in content:
        errors.append("Missing footer")
    
    if 'gravelgodcoaching@gmail.com' not in content:
        errors.append("Missing contact email")
    
    # Check for simplified styling elements
    if 'background:#f5f5f5' not in content:
        errors.append("Missing simplified template gray background boxes")
    
    if 'border-left:5px solid #777' not in content:
        errors.append("Missing simplified template left border accent")
    
    return errors


def main():
    """Run regression tests on all Mid South marketplace descriptions"""
    base_path = Path(__file__).parent
    mid_south_path = base_path / "races" / "Mid South"
    
    if not mid_south_path.exists():
        print("❌ ERROR: Mid South race folder not found")
        sys.exit(1)
    
    # Find all marketplace description files in plan folders
    marketplace_files = list(mid_south_path.glob("*/marketplace_description.html"))
    
    if not marketplace_files:
        print("❌ ERROR: No marketplace description files found in plan folders")
        sys.exit(1)
    
    print(f"🔍 Testing {len(marketplace_files)} marketplace description files...\n")
    
    all_passed = True
    for marketplace_file in sorted(marketplace_files):
        errors = check_simplified_structure(marketplace_file)
        
        if errors:
            print(f"❌ {marketplace_file.parent.name}")
            for error in errors:
                print(f"   • {error}")
            all_passed = False
        else:
            print(f"✓ {marketplace_file.parent.name}")
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ All marketplace descriptions passed simplified structure tests")
        return 0
    else:
        print("❌ Some marketplace descriptions failed simplified structure tests")
        return 1


if __name__ == '__main__':
    sys.exit(main())
