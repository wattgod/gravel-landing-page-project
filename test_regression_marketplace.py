#!/usr/bin/env python3
"""
MARKETPLACE REGRESSION TEST SUITE
==================================
Prevents previously-fixed bugs in marketplace descriptions from returning.

Tests critical fixes:
1. Character limits (under 4,000)
2. No Section X references
3. Closing validation logic
4. Masters content isolation

Exit codes:
    0 = All regression tests passed
    1 = Regression detected (previously-fixed bug returned)
"""

import os
import re
import sys
from pathlib import Path

# ============================================================================
# REGRESSION TEST SUITE
# ============================================================================

class RegressionTestFailure(Exception):
    """Raised when a regression test fails"""
    pass

def test_marketplace_character_limits():
    """REGRESSION: All marketplace descriptions must be under 4,000 characters"""
    output_dir = Path("output/html_descriptions")
    if not output_dir.exists():
        return
    
    errors = []
    for html_file in output_dir.rglob("*.html"):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        char_count = len(content)
        if char_count > 4000:
            errors.append(f"{html_file.name}: {char_count:,} chars (exceeds 4,000 limit)")
    
    if errors:
        raise RegressionTestFailure("Character limit regression:\n" + "\n".join(errors))

def test_marketplace_no_section_references():
    """REGRESSION: Marketplace descriptions must NOT mention 'Section X' (user explicitly requested removal)"""
    output_dir = Path("output/html_descriptions")
    if not output_dir.exists():
        return
    
    errors = []
    section_pattern = re.compile(r'[Ss]ection\s+\d+', re.IGNORECASE)
    
    for html_file in output_dir.rglob("*.html"):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        matches = section_pattern.findall(content)
        if matches:
            errors.append(f"{html_file.name}: Contains 'Section X' references: {matches}")
    
    if errors:
        raise RegressionTestFailure("Section reference regression:\n" + "\n".join(errors))

def test_marketplace_closing_validation():
    """REGRESSION: Closing validation must only check last paragraph before footer (fixed podium_elite issue)"""
    output_dir = Path("output/html_descriptions")
    if not output_dir.exists():
        return
    
    # This test verifies the validation logic itself
    # We check that validate_descriptions.py uses the correct logic
    validate_file = Path("validate_descriptions.py")
    if not validate_file.exists():
        return
    
    with open(validate_file, 'r', encoding='utf-8') as f:
        validate_content = f.read()
    
    # Check that closing validation looks for footer first
    if 'border-top:2px' not in validate_content:
        raise RegressionTestFailure("Closing validation regression: Should check for footer before validating closing")
    
    # Check that it doesn't use the old pattern that caused false positives
    if re.search(r'closing_matches\s*=\s*re\.findall.*This is \|Built for \|Designed for \|Unbound', validate_content):
        # Old pattern that caused podium_elite false positive
        if 'before_footer' not in validate_content:
            raise RegressionTestFailure("Closing validation regression: Should use 'before_footer' logic, not global findall")

def test_masters_content_isolation():
    """REGRESSION: Masters-specific content must ONLY appear in Masters plans"""
    output_dir = Path("output/html_descriptions")
    if not output_dir.exists():
        return
    
    masters_keywords = ['age 45+', 'age 50+', 'recovery protocols for 50+', 'masters-specific']
    errors = []
    
    for html_file in output_dir.rglob("*.html"):
        # Skip Masters plans
        if 'masters' in html_file.name.lower():
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count Masters keyword mentions
        masters_mentions = sum(1 for keyword in masters_keywords if keyword.lower() in content.lower())
        
        # Allow 1-2 mentions (might be in general context), but flag 3+
        if masters_mentions >= 3:
            errors.append(f"{html_file.name}: {masters_mentions} Masters-specific mentions in non-Masters plan")
    
    if errors:
        raise RegressionTestFailure("Masters content isolation regression:\n" + "\n".join(errors))

# ============================================================================
# TEST RUNNER
# ============================================================================

def run_marketplace_regression_tests():
    """Run all marketplace regression tests"""
    tests = [
        ("Marketplace Character Limits", test_marketplace_character_limits),
        ("Marketplace No Section References", test_marketplace_no_section_references),
        ("Marketplace Closing Validation", test_marketplace_closing_validation),
        ("Masters Content Isolation", test_masters_content_isolation),
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 80)
    print("MARKETPLACE REGRESSION TEST SUITE")
    print("=" * 80)
    print()
    
    for test_name, test_func in tests:
        try:
            test_func()
            print(f"✓ {test_name}")
            passed += 1
        except RegressionTestFailure as e:
            print(f"✗ {test_name}")
            print(f"  {str(e)}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_name}")
            print(f"  Unexpected error: {str(e)}")
            failed += 1
    
    print()
    print("=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 80)
    
    if failed > 0:
        print()
        print("⚠️  REGRESSION DETECTED: Previously-fixed bugs have returned!")
        print("   Review the errors above and fix before proceeding.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(run_marketplace_regression_tests())

