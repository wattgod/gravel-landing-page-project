#!/usr/bin/env python3
"""
REGRESSION TEST: Simplified Guide Structure
============================================
Ensures guides use the new simplified template structure:
- Uses simplified template (not old full template)
- Has correct HTML structure with Courier New font
- Contains required sections: tier philosophy, training approach, plan features, etc.
- No old template placeholders or sections
- Guides are in plan folders (not central guides/ folder)

Exit codes:
    0 = All tests passed
    1 = Structure violations detected
"""

import re
import sys
from pathlib import Path


def check_simplified_structure(guide_path):
    """Check if guide uses simplified template structure"""
    with open(guide_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    errors = []
    
    # Check for simplified template structure
    if 'font-family:\'Courier New\'' not in content:
        errors.append("Missing Courier New font family")
    
    if 'max-width:800px' not in content:
        errors.append("Missing max-width:800px")
    
    # Check for required sections
    if 'TIER_PHILOSOPHY' in content or '{{TIER_PHILOSOPHY}}' in content:
        errors.append("Unreplaced placeholder: TIER_PHILOSOPHY")
    
    if 'TIER_PHILOSOPHY' not in content and 'High-intensity interval training works' not in content and 'Polarized training principles work' not in content and 'Block periodization' not in content:
        errors.append("Missing tier philosophy content")
    
    if 'What the' not in content or 'Includes' not in content:
        errors.append("Missing 'What the [Plan] Includes' section")
    
    if '18,000+ Word Guide' not in content:
        errors.append("Missing guide content summary section")
    
    if 'Alternative?' not in content:
        errors.append("Missing 'Alternative?' section")
    
    if 'What This Plan Delivers' not in content:
        errors.append("Missing 'What This Plan Delivers' section")
    
    # Check for old template remnants (should NOT be present)
    if 'section-1-training-plan-brief' in content:
        errors.append("Contains old template section markers")
    
    if 'GRAVEL GOD TRAINING GUIDE TEMPLATE' in content and 'REQUIRED VARIABLES' in content:
        errors.append("Contains old template comments")
    
    if '<!DOCTYPE html>' in content and '<html lang="en">' in content:
        # Old template had full HTML structure, simplified should just be a div
        if content.count('<!DOCTYPE html>') > 0:
            errors.append("Contains old template HTML structure (should be div-only)")
    
    # Check for race-specific content
    if 'This is' not in content or 'For people whose fitness' not in content:
        errors.append("Missing race-specific closing statement")
    
    # Check for footer
    if 'GRAVEL GOD CYCLING' not in content:
        errors.append("Missing footer")
    
    if 'gravelgodcoaching@gmail.com' not in content:
        errors.append("Missing contact email")
    
    return errors


def main():
    """Run regression tests on all Mid South guides"""
    base_path = Path(__file__).parent
    mid_south_path = base_path / "races" / "Mid South"
    
    if not mid_south_path.exists():
        print("❌ ERROR: Mid South race folder not found")
        sys.exit(1)
    
    # Find all guide files in plan folders
    guide_files = list(mid_south_path.glob("*/*guide.html"))
    
    if not guide_files:
        print("❌ ERROR: No guide files found in plan folders")
        sys.exit(1)
    
    print(f"🔍 Testing {len(guide_files)} guide files...\n")
    
    all_passed = True
    for guide_file in sorted(guide_files):
        errors = check_simplified_structure(guide_file)
        
        if errors:
            print(f"❌ {guide_file.name}")
            for error in errors:
                print(f"   • {error}")
            all_passed = False
        else:
            print(f"✓ {guide_file.name}")
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ All guides passed simplified structure tests")
        return 0
    else:
        print("❌ Some guides failed simplified structure tests")
        return 1


if __name__ == '__main__':
    sys.exit(main())
