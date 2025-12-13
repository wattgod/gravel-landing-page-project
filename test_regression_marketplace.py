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
5. No duplicate openings (fixed 2024-12-11)
6. No duplicate stories (fixed 2024-12-11)
7. No duplicate closings (fixed 2024-12-11)
8. No duplicate alternatives (fixed 2024-12-11)
9. No within-tier duplicates (fixed 2024-12-11)
10. SMR positioning isolation (fixed 2024-12-XX - SMR plans must use salvage/urgency, not performance/progression)

Exit codes:
    0 = All regression tests passed
    1 = Regression detected (previously-fixed bug returned)
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

# ============================================================================
# REGRESSION TEST SUITE
# ============================================================================

class RegressionTestFailure(Exception):
    """Raised when a regression test fails"""
    pass

# ============================================================================
# CONTENT EXTRACTION (reused from validate_descriptions.py)
# ============================================================================

def extract_opening(content):
    """Extract opening paragraph from HTML."""
    match = re.search(r'<p style="margin:0;font-size:24px;font-weight:700;line-height:1.3">([^<]+)</p>', content)
    return match.group(1).strip() if match else ""

def extract_story(content):
    """Extract story justification paragraph from HTML."""
    match = re.search(r'<div style="margin-bottom:14px">\s*<p style="margin:0;font-size:16px">([^<]+)</p>', content)
    return match.group(1).strip() if match else ""

def extract_closing(content):
    """Extract closing statement from HTML."""
    footer_match = re.search(r'<div style="border-top:2px', content)
    if footer_match:
        before_footer = content[:footer_match.start()]
        matches = list(re.finditer(r'<p style="margin:0;font-size:16px">([^<]+)</p>', before_footer))
        if matches:
            return matches[-1].group(1).strip()
    match = re.search(r'<p style="margin:0;font-size:16px">([^<]*(?:This is |Built for |Designed for |Unbound)[^<]+)</p>', content)
    return match.group(1).strip() if match else ""

def extract_alternative(content):
    """Extract alternative hook paragraph from HTML."""
    match = re.search(r'<h3[^>]*>Alternative\?</h3>\s*<p style="margin:0;font-size:16px">([^<]+)</p>', content)
    return match.group(1).strip() if match else ""

def get_tier_from_filename(filename):
    """Extract tier from filename (e.g., 'finisher_advanced.html' -> 'finisher')."""
    parts = filename.split('_')
    if parts:
        return parts[0]
    return "unknown"

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
    """
    REGRESSION: Masters-specific content must ONLY appear in Masters plans
    
    CHECKS ALL SECTIONS:
    - Opening
    - Story
    - Features
    - Guide topics
    - Alternative section (CRITICAL - was missing)
    - Value prop box
    - Closing
    """
    output_dir = Path("output/html_descriptions")
    if not output_dir.exists():
        return
    
    masters_keywords = [
        'age 45+', 
        'age 50+', 
        'recovery protocols for 50+', 
        'masters-specific',
        'recovery timelines from your 30s',
        'age-related',
        'younger athletes',
        "train like you're 25",
        'at 50+',
        'at your age',
        'as you age',
        'age-appropriate',
        'recovery isn\'t optional',
        'recovery becomes the primary',
        'recovery architecture',
        'recovery-first',
        'longer recovery',
        'adaptation timeline',
        'adaptation windows'
    ]
    errors = []
    
    for html_file in output_dir.rglob("*.html"):
        # Skip Masters plans
        if 'masters' in html_file.name.lower():
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        # Extract alternative section specifically (was missing before)
        alternative_match = re.search(r'<h3[^>]*>Alternative\?</h3>\s*<p[^>]*>([^<]+)</p>', content, re.IGNORECASE)
        alternative_text = alternative_match.group(1) if alternative_match else ""
        
        # Check alternative section for Masters language
        for keyword in masters_keywords:
            if keyword in alternative_text:
                errors.append(
                    f"{html_file.name}: Alternative section contains Masters language '{keyword}' "
                    f"in non-Masters plan (Masters content only for Masters plans)"
                )
        
        # Count Masters keyword mentions in full content
        masters_mentions = sum(1 for keyword in masters_keywords if keyword in content)
        
        # Allow 1-2 mentions (might be in general context), but flag 3+
        if masters_mentions >= 3:
            errors.append(
                f"{html_file.name}: {masters_mentions} Masters-specific mentions in non-Masters plan "
                f"(Masters content only for Masters plans)"
            )
    
    if errors:
        raise RegressionTestFailure("Masters content isolation regression:\n" + "\n".join(errors))

def test_no_duplicate_openings():
    """REGRESSION: No two plans should have identical opening paragraphs (fixed 2024-12-11)"""
    output_dir = Path("output/html_descriptions")
    if not output_dir.exists():
        return
    
    openings = {}  # opening_text -> [list of filenames]
    errors = []
    
    for html_file in output_dir.rglob("*.html"):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        opening = extract_opening(content)
        if opening:
            if opening in openings:
                openings[opening].append(html_file.name)
            else:
                openings[opening] = [html_file.name]
    
    # Find duplicates
    for opening_text, filenames in openings.items():
        if len(filenames) > 1:
            errors.append(f"DUPLICATE OPENING: {', '.join(filenames)}")
    
    if errors:
        raise RegressionTestFailure("Duplicate openings regression:\n" + "\n".join(errors))

def test_no_duplicate_stories():
    """REGRESSION: No two plans should have identical story paragraphs (fixed 2024-12-11)"""
    output_dir = Path("output/html_descriptions")
    if not output_dir.exists():
        return
    
    stories = {}  # story_text -> [list of filenames]
    errors = []
    
    for html_file in output_dir.rglob("*.html"):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        story = extract_story(content)
        if story:
            if story in stories:
                stories[story].append(html_file.name)
            else:
                stories[story] = [html_file.name]
    
    # Find duplicates
    for story_text, filenames in stories.items():
        if len(filenames) > 1:
            errors.append(f"DUPLICATE STORY: {', '.join(filenames)}")
    
    if errors:
        raise RegressionTestFailure("Duplicate stories regression:\n" + "\n".join(errors))

def test_no_duplicate_closings():
    """REGRESSION: No two plans should have identical closing paragraphs (fixed 2024-12-11)"""
    output_dir = Path("output/html_descriptions")
    if not output_dir.exists():
        return
    
    closings = {}  # closing_text -> [list of filenames]
    errors = []
    
    for html_file in output_dir.rglob("*.html"):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        closing = extract_closing(content)
        if closing:
            if closing in closings:
                closings[closing].append(html_file.name)
            else:
                closings[closing] = [html_file.name]
    
    # Find duplicates
    for closing_text, filenames in closings.items():
        if len(filenames) > 1:
            errors.append(f"DUPLICATE CLOSING: {', '.join(filenames)}")
    
    if errors:
        raise RegressionTestFailure("Duplicate closings regression:\n" + "\n".join(errors))

def test_no_duplicate_alternative_hooks():
    """REGRESSION: No two plans should have identical alternative sections (fixed 2024-12-11)"""
    output_dir = Path("output/html_descriptions")
    if not output_dir.exists():
        return
    
    alternatives = {}  # alternative_text -> [list of filenames]
    errors = []
    
    for html_file in output_dir.rglob("*.html"):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        alternative = extract_alternative(content)
        if alternative:
            if alternative in alternatives:
                alternatives[alternative].append(html_file.name)
            else:
                alternatives[alternative] = [html_file.name]
    
    # Find duplicates
    for alternative_text, filenames in alternatives.items():
        if len(filenames) > 1:
            errors.append(f"DUPLICATE ALTERNATIVE: {', '.join(filenames)}")
    
    if errors:
        raise RegressionTestFailure("Duplicate alternatives regression:\n" + "\n".join(errors))

def test_no_repeated_phrases():
    """
    TEST: No identical phrases repeated within same description
    
    WHY: Sounds lazy/robotic, breaks flow
    EXAMPLE: "Everything here is calibrated..." twice = bad
    """
    descriptions = find_descriptions()
    errors = []
    
    # Common phrases to check for repetition
    phrases_to_check = [
        'everything here is calibrated',
        'this plan delivers',
        'built for',
        'designed for',
        'race-day capacity'
    ]
    
    for plan_name, filepath in descriptions:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        for phrase in phrases_to_check:
            count = content.count(phrase)
            if count > 1:
                errors.append(
                    f"{plan_name}: Phrase '{phrase}' repeated {count} times "
                    f"(should appear once maximum)"
                )
    
    return errors

def test_within_tier_duplicates():
    """REGRESSION: No duplicate content within same tier (critical for positioning, fixed 2024-12-11)"""
    output_dir = Path("output/html_descriptions")
    if not output_dir.exists():
        return
    
    # Group by tier
    tier_content = defaultdict(lambda: {
        'openings': {},
        'stories': {},
        'closings': {},
        'alternatives': {}
    })
    errors = []
    
    for html_file in output_dir.rglob("*.html"):
        tier = get_tier_from_filename(html_file.name)
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        opening = extract_opening(content)
        story = extract_story(content)
        closing = extract_closing(content)
        alternative = extract_alternative(content)
        
        # Track content within tier
        if opening:
            if opening in tier_content[tier]['openings']:
                tier_content[tier]['openings'][opening].append(html_file.name)
            else:
                tier_content[tier]['openings'][opening] = [html_file.name]
        
        if story:
            if story in tier_content[tier]['stories']:
                tier_content[tier]['stories'][story].append(html_file.name)
            else:
                tier_content[tier]['stories'][story] = [html_file.name]
        
        if closing:
            if closing in tier_content[tier]['closings']:
                tier_content[tier]['closings'][closing].append(html_file.name)
            else:
                tier_content[tier]['closings'][closing] = [html_file.name]
        
        if alternative:
            if alternative in tier_content[tier]['alternatives']:
                tier_content[tier]['alternatives'][alternative].append(html_file.name)
            else:
                tier_content[tier]['alternatives'][alternative] = [html_file.name]
    
    # Check for duplicates within each tier
    for tier, content_dict in tier_content.items():
        for content_type, content_map in content_dict.items():
            for content_text, filenames in content_map.items():
                if len(filenames) > 1:
                    errors.append(f"DUPLICATE {content_type.upper()} IN {tier.upper()}: {', '.join(filenames)}")
    
    if errors:
        raise RegressionTestFailure("Within-tier duplicates regression:\n" + "\n".join(errors))

def test_smr_positioning_isolation():
    """
    REGRESSION: Save My Race plans must use SMR-specific positioning (salvage/urgency/6-weeks)
    NOT regular plan positioning (performance/progression/12-weeks)
    
    CRITICAL: SMR is different product with different positioning. This test prevents
    the generator from accidentally using regular variations for SMR plans.
    
    Fixed: 2024-12-XX (SMR positioning completely wrong - using regular plan variations)
    """
    output_dir = Path("output/html_descriptions")
    if not output_dir.exists():
        return
    
    errors = []
    
    # SMR-specific language (REQUIRED in SMR plans)
    smr_required = [
        '6 weeks',
        '6-week',
        'six weeks',
        'life got in the way',
        "don't defer",
        'salvage',
        'triage',
        'minimum viable',
        'sufficient preparation',
        'emergency',
        'cram the training',
        'cram some training',
        'cram the work',
        'haven\'t been training'
    ]
    
    # Regular plan language (FORBIDDEN in SMR plans)
    regular_forbidden = [
        '12-week',
        '12 week',
        'progressive overload',
        'unlock another gear',
        'your fitness will show up predictably',
        'performance arrives',
        'full race-distance simulation',
        'weekly practice building competence',
        'your 12-week arc'
    ]
    
    for html_file in output_dir.rglob("*.html"):
        is_save_my_race = 'save_my_race' in html_file.name.lower() or 'save my race' in html_file.name.lower()
        
        if not is_save_my_race:
            continue  # Only check SMR plans
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        # SMR plans MUST have SMR language (6 weeks should be prominent)
        smr_found = any(indicator in content for indicator in smr_required)
        if not smr_found:
            errors.append(
                f"{html_file.name}: Save My Race plan missing SMR-specific language "
                f"(should mention 6 weeks, salvage, triage, don't defer)"
            )
        
        # SMR plans MUST NOT have regular language
        for indicator in regular_forbidden:
            if indicator in content:
                errors.append(
                    f"{html_file.name}: Save My Race plan contains regular plan language '{indicator}'. "
                    f"SMR plans should use salvage/urgency positioning, not performance/progression."
                )
    
    if errors:
        raise RegressionTestFailure("SMR positioning isolation regression:\n" + "\n".join(errors))

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
        ("No Duplicate Openings", test_no_duplicate_openings),
        ("No Duplicate Stories", test_no_duplicate_stories),
        ("No Duplicate Closings", test_no_duplicate_closings),
        ("No Duplicate Alternative Hooks", test_no_duplicate_alternative_hooks),
        ("No Within-Tier Duplicates", test_within_tier_duplicates),
        ("SMR Positioning Isolation", test_smr_positioning_isolation),
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

