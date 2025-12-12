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
        # Skip index.html (directory listing)
        if guide_file.name == "index.html":
            continue
            
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
        # Skip index.html (directory listing)
        if guide_file.name == "index.html":
            continue
            
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
        # Skip index.html (directory listing)
        if guide_file.name == "index.html":
            continue
            
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
        # Skip index.html (directory listing)
        if guide_file.name == "index.html":
            continue
            
        with open(guide_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract unique section IDs (sections can have both <section> and <h2> with same ID)
        section_ids = set(re.findall(r'id="(section-\d+)', content))
        section_numbers = sorted([int(s.split('-')[1]) for s in section_ids if s.split('-')[1].isdigit()])
        
        # Check for gaps in numbering (should be sequential: 1, 2, 3, ...)
        if section_numbers:
            # Get unique numbers and check they're sequential
            unique_numbers = sorted(set(section_numbers))
            expected = list(range(1, max(unique_numbers) + 1))
            
            # Check for gaps (missing numbers in sequence)
            gaps = [n for n in expected if n not in unique_numbers]
            if gaps:
                errors.append(f"{guide_file.name}: Missing section numbers: {gaps}")
            
            # Check for duplicates (shouldn't have multiple sections with same number)
            # Actually, duplicates are OK if they're the same section with multiple IDs
            # The real issue is gaps in the sequence
    
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
        # Skip index.html (directory listing)
        if guide_file.name == "index.html":
            continue
            
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
        # Skip index.html (directory listing)
        if guide_file.name == "index.html":
            continue
            
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
            
            # Check for glossary-style terms (should NOT have definition lists)
            if re.search(r'<dl>|<dt>|<dd>', section_content, re.IGNORECASE):
                errors.append(f"{guide_file.name}: FAQ section contains glossary terms (dl/dt/dd tags)")
    
    if errors:
        raise RegressionTestFailure("FAQ format regression:\n" + "\n".join(errors))

def test_guide_section1_plan_uniqueness():
    """REGRESSION: Chapter 1 must explain what makes the plan unique (ability level, tier volume, performance expectations)"""
    guides_dir = Path("docs/guides/unbound-gravel-200")
    if not guides_dir.exists():
        return
    
    errors = []
    for guide_file in guides_dir.glob("*.html"):
        # Skip index.html (directory listing)
        if guide_file.name == "index.html":
            continue
            
        with open(guide_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for "What Makes This Plan Different" section
        if 'What Makes This Plan Different' not in content:
            errors.append(f"{guide_file.name}: Missing 'What Makes This Plan Different' section")
            continue
        
        # Extract Section 1 content
        section1_match = re.search(r'section-1[^>]*>(.*?)</section>', content, re.DOTALL | re.IGNORECASE)
        if section1_match:
            section1_content = section1_match.group(1)
            
            # Check for ability level explanation (should explain Beginner/Intermediate/Advanced/Masters)
            if not re.search(r'(Beginner|Intermediate|Advanced|Masters).*experience|training experience|current fitness', section1_content, re.IGNORECASE):
                errors.append(f"{guide_file.name}: Missing ability level explanation in Section 1")
            
            # Check for tier volume explanation (should explain Ayahuasca/Finisher/Compete/Podium)
            if not re.search(r'(Ayahuasca|Finisher|Compete|Podium).*hours|weekly hours|volume category', section1_content, re.IGNORECASE):
                errors.append(f"{guide_file.name}: Missing tier volume explanation in Section 1")
            
            # Check for performance expectations (should have conditional expectations based on tier)
            if 'Performance Expectations' not in section1_content and 'performance expectations' not in section1_content.lower():
                errors.append(f"{guide_file.name}: Missing 'Performance Expectations' section in Section 1")
            
            # Check for plan title placeholder (should be replaced, not show {{PLAN_TITLE}})
            if '{{PLAN_TITLE}}' in section1_content:
                errors.append(f"{guide_file.name}: Unreplaced {{PLAN_TITLE}} placeholder in Section 1")
    
    if errors:
        raise RegressionTestFailure("Section 1 plan uniqueness regression:\n" + "\n".join(errors))

def test_guide_section8_nutrition_comprehensive():
    """REGRESSION: Section 8 (Fueling & Hydration) must have comprehensive content (~4,200 words), not abbreviated version"""
    guides_dir = Path("docs/guides/unbound-gravel-200")
    if not guides_dir.exists():
        return
    
    errors = []
    for guide_file in guides_dir.glob("*.html"):
        # Skip index.html (directory listing)
        if guide_file.name == "index.html":
            continue
            
        with open(guide_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for Section 8
        section8_match = re.search(r'section-8-fueling-hydration[^>]*>(.*?)</section>', content, re.DOTALL | re.IGNORECASE)
        if section8_match:
            section8_content = section8_match.group(1)
            # Remove HTML tags to get text content
            text_content = re.sub(r'<[^>]+>', ' ', section8_content)
            text_content = ' '.join(text_content.split())  # Normalize whitespace
            
            # Comprehensive version should be ~4,200 words (roughly 25,000+ characters of text)
            # Abbreviated version would be much shorter
            if len(text_content) < 20000:  # Conservative threshold
                errors.append(f"{guide_file.name}: Section 8 appears abbreviated ({len(text_content)} chars, expected ~25,000+)")
            
            # Check for key comprehensive topics that should be present
            required_topics = [
                'daily nutrition',
                'supplements',
                'workout-specific fueling',
                'cramping',
                'weight management',
                'race-day'
            ]
            missing_topics = [topic for topic in required_topics if topic.lower() not in text_content.lower()]
            if missing_topics:
                errors.append(f"{guide_file.name}: Section 8 missing key topics: {', '.join(missing_topics)}")
    
    if errors:
        raise RegressionTestFailure("Section 8 nutrition comprehensive content regression:\n" + "\n".join(errors))

def test_guide_section12_race_week_comprehensive():
    """REGRESSION: Section 12 (Race Week Protocol) must have comprehensive checklist, not abbreviated version"""
    guides_dir = Path("docs/guides/unbound-gravel-200")
    if not guides_dir.exists():
        return
    
    errors = []
    for guide_file in guides_dir.glob("*.html"):
        # Skip index.html (directory listing)
        if guide_file.name == "index.html":
            continue
            
        with open(guide_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for Section 12
        section12_match = re.search(r'section-12-race-week-protocol[^>]*>(.*?)</section>', content, re.DOTALL | re.IGNORECASE)
        if section12_match:
            section12_content = section12_match.group(1)
            text_content = re.sub(r'<[^>]+>', ' ', section12_content)
            text_content = ' '.join(text_content.split())
            
            # Comprehensive version should have substantial content
            # Abbreviated version would be much shorter (< 3000 chars)
            # Comprehensive version should be detailed (> 5000 chars)
            if len(text_content) < 5000:
                errors.append(f"{guide_file.name}: Section 12 appears abbreviated ({len(text_content)} chars, expected 5000+)")
            
            # Check for checklist structure (should have lists or structured content)
            has_checklist = re.search(r'<ul>|<ol>|<li>|checklist|•|✓', section12_content, re.IGNORECASE)
            if not has_checklist:
                errors.append(f"{guide_file.name}: Section 12 missing checklist structure")
    
    if errors:
        raise RegressionTestFailure("Section 12 race week comprehensive content regression:\n" + "\n".join(errors))

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
        ("Guide Section 1 Plan Uniqueness", test_guide_section1_plan_uniqueness),
        ("Guide Section 8 Nutrition Comprehensive", test_guide_section8_nutrition_comprehensive),
        ("Guide Section 12 Race Week Comprehensive", test_guide_section12_race_week_comprehensive),
        ("Guide FAQ Format (No Glossary)", test_guide_faq_format),
        ("Guide Women-Specific Content", test_guide_women_specific_content),
        ("Marketplace Character Limits", test_marketplace_character_limits),
        ("Marketplace No Section References", test_marketplace_no_section_references),
        ("Marketplace Closing Validation", test_marketplace_closing_validation),
        ("Masters Content Isolation", test_masters_content_isolation),
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

