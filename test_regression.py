#!/usr/bin/env python3
"""
REGRESSION TEST SUITE
=====================
Prevents previously-fixed bugs from returning.

Tests critical fixes:
1. Guide structure (TOC, sections, CSS embedding)
2. Marketplace descriptions (character limits, required elements)
3. Content accuracy (no Section X references, Masters content isolation)
4. Validation logic (closing paragraph detection)

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

def test_guide_toc_positioning():
    """REGRESSION: TOC must be on left side, not top (fixed in commit)"""
    guides_dir = Path("docs/guides/unbound-gravel-200")
    if not guides_dir.exists():
        return  # Skip if guides not generated
    
    errors = []
    for guide_file in guides_dir.glob("*.html"):
        with open(guide_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for grid layout (TOC on left)
        if 'gg-guide-layout' not in content or 'gg-guide-toc' not in content:
            errors.append(f"{guide_file.name}: Missing grid layout for TOC positioning")
        
        # Check for old top-positioned TOC (should NOT exist)
        if 'toc-box' in content and 'gg-guide-toc' not in content:
            errors.append(f"{guide_file.name}: Old TOC structure detected (top positioning)")
    
    if errors:
        raise RegressionTestFailure("TOC positioning regression:\n" + "\n".join(errors))

def test_guide_css_embedding():
    """REGRESSION: CSS must be embedded, not external link (fixed to prevent GitHub Pages issues)"""
    guides_dir = Path("docs/guides/unbound-gravel-200")
    if not guides_dir.exists():
        return
    
    errors = []
    for guide_file in guides_dir.glob("*.html"):
        with open(guide_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for external CSS link (should NOT exist)
        if re.search(r'<link[^>]*href=["\']/gravel-landing-page-project/assets/css/guides\.css["\']', content):
            errors.append(f"{guide_file.name}: External CSS link detected (should be embedded)")
        
        # Check for embedded CSS (should exist)
        if '<style>' not in content or 'gg-guide-page' not in content:
            errors.append(f"{guide_file.name}: Missing embedded CSS")
    
    if errors:
        raise RegressionTestFailure("CSS embedding regression:\n" + "\n".join(errors))

def test_guide_no_ftp_hr_settings():
    """REGRESSION: Chapter 2 must NOT have FTP/HR settings (removed per user request)"""
    guides_dir = Path("docs/guides/unbound-gravel-200")
    if not guides_dir.exists():
        return
    
    errors = []
    for guide_file in guides_dir.glob("*.html"):
        with open(guide_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for FTP testing section (should NOT exist)
        if re.search(r'FTP\s+[Tt]esting|FTP\s+[Tt]est', content, re.IGNORECASE):
            # Allow in other sections, but not in Chapter 2
            section_2_match = re.search(r'section-2[^>]*>.*?FTP\s+[Tt]esting', content, re.DOTALL | re.IGNORECASE)
            if section_2_match:
                errors.append(f"{guide_file.name}: FTP Testing section in Chapter 2 (should be removed)")
        
        # Check for HR max testing in Chapter 2
        if re.search(r'section-2[^>]*>.*?[Hh]eart\s+[Rr]ate\s+[Mm]ax\s+[Tt]esting', content, re.DOTALL):
            errors.append(f"{guide_file.name}: Heart Rate Max Testing in Chapter 2 (should be removed)")
    
    if errors:
        raise RegressionTestFailure("FTP/HR settings regression:\n" + "\n".join(errors))

def test_guide_section_numbering():
    """REGRESSION: Sections must be sequentially numbered (fixed after Masters section addition)"""
    guides_dir = Path("docs/guides/unbound-gravel-200")
    if not guides_dir.exists():
        return
    
    errors = []
    for guide_file in guides_dir.glob("*.html"):
        with open(guide_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract all section IDs
        section_ids = re.findall(r'id="(section-\d+)', content)
        section_numbers = [int(s.split('-')[1]) for s in section_ids if s.split('-')[1].isdigit()]
        section_numbers.sort()
        
        # Check for gaps in numbering
        if section_numbers:
            expected = list(range(1, len(section_numbers) + 1))
            if section_numbers != expected:
                errors.append(f"{guide_file.name}: Non-sequential section numbering: {section_numbers}")
    
    if errors:
        raise RegressionTestFailure("Section numbering regression:\n" + "\n".join(errors))

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

def test_guide_women_specific_content():
    """REGRESSION: Women-Specific section must have actual content, not just a heading"""
    guides_dir = Path("docs/guides/unbound-gravel-200")
    if not guides_dir.exists():
        return
    
    errors = []
    for guide_file in guides_dir.glob("*.html"):
        with open(guide_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for Women-Specific section
        women_section_match = re.search(r'section-\d+-women-specific[^>]*>(.*?)</section>', content, re.DOTALL | re.IGNORECASE)
        if women_section_match:
            section_content = women_section_match.group(1)
            # Check for actual content (not just heading)
            text_content = re.sub(r'<[^>]+>', '', section_content).strip()
            if len(text_content) < 500:  # Should have substantial content
                errors.append(f"{guide_file.name}: Women-Specific section has insufficient content ({len(text_content)} chars)")
    
    if errors:
        raise RegressionTestFailure("Women-Specific content regression:\n" + "\n".join(errors))

def test_guide_faq_format():
    """REGRESSION: FAQ section must be Q&A format, not glossary (fixed after revert)"""
    guides_dir = Path("docs/guides/unbound-gravel-200")
    if not guides_dir.exists():
        return
    
    errors = []
    for guide_file in guides_dir.glob("*.html"):
        with open(guide_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for FAQ section
        faq_section_match = re.search(r'section-\d+-faq[^>]*>(.*?)</section>', content, re.DOTALL | re.IGNORECASE)
        if faq_section_match:
            section_content = faq_section_match.group(1)
            
            # Check for Q&A format (should have questions)
            question_count = len(re.findall(r'[?]', section_content))
            # Check for glossary format (should NOT have just term definitions)
            glossary_pattern = re.search(r'<dt>|<dd>|term.*definition', section_content, re.IGNORECASE)
            
            if question_count < 5 and glossary_pattern:
                errors.append(f"{guide_file.name}: FAQ section appears to be glossary format, not Q&A")
    
    if errors:
        raise RegressionTestFailure("FAQ format regression:\n" + "\n".join(errors))

# ============================================================================
# TEST RUNNER
# ============================================================================

def run_all_regression_tests():
    """Run all regression tests"""
    tests = [
        ("Guide TOC Positioning", test_guide_toc_positioning),
        ("Guide CSS Embedding", test_guide_css_embedding),
        ("Guide No FTP/HR Settings", test_guide_no_ftp_hr_settings),
        ("Guide Section Numbering", test_guide_section_numbering),
        ("Marketplace Character Limits", test_marketplace_character_limits),
        ("Marketplace No Section References", test_marketplace_no_section_references),
        ("Marketplace Closing Validation", test_marketplace_closing_validation),
        ("Masters Content Isolation", test_masters_content_isolation),
        ("Guide Women-Specific Content", test_guide_women_specific_content),
        ("Guide FAQ Format", test_guide_faq_format),
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 80)
    print("REGRESSION TEST SUITE")
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
    sys.exit(run_all_regression_tests())

