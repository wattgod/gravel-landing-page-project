#!/usr/bin/env python3
"""
Verification script for training guide structure.
Checks:
1. TOC links match section IDs
2. All required sections are present
3. No duplicate section IDs
4. Women-Specific section has actual content
5. No unreplaced placeholder variables
6. No old content (QUICK REFERENCE, glossary, etc.)
7. Section numbering is sequential
8. CSS is embedded (not external link)
9. File size is reasonable
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


# Required sections that must be present in all guides
REQUIRED_SECTIONS = [
    "section-1-training-plan-brief",
    "section-2-before-you-start",
    "section-3",
    "section-4",
    "section-5",
    "section-6",
    "section-7",
    "section-8-fueling-hydration",
    "section-9",
    "section-10",
    "section-11",
    "section-12-race-week-protocol",
    "section-13-women-specific-considerations",  # Will be renumbered to 13 or 14
    "section-14-women-specific-considerations",  # For Masters plans
    "section-14-faq",  # Will be renumbered to 14 or 15
    "section-15-faq",  # For Masters plans
]

# Conditional sections (only in Masters plans)
CONDITIONAL_SECTIONS = [
    "section-13-masters-specific-considerations",
]


def extract_toc_links(html: str) -> Set[str]:
    """Extract all TOC links from HTML"""
    pattern = r'href="#([^"]+)"'
    matches = re.findall(pattern, html)
    # Filter to only section links
    section_links = {m for m in matches if m.startswith('section-')}
    return section_links


def extract_section_ids(html: str) -> Dict[str, List[str]]:
    """Extract all section IDs from HTML, grouped by type"""
    # Find all id attributes
    pattern = r'id="([^"]+)"'
    all_ids = re.findall(pattern, html)
    
    # Separate section IDs from other IDs
    section_ids = {}
    other_ids = []
    
    for id_val in all_ids:
        if id_val.startswith('section-'):
            if id_val not in section_ids:
                section_ids[id_val] = []
            section_ids[id_val].append(id_val)
        else:
            other_ids.append(id_val)
    
    return section_ids


def check_toc_matches(html: str) -> Tuple[bool, List[str]]:
    """Check if all TOC links have matching section IDs"""
    toc_links = extract_toc_links(html)
    section_ids = set(extract_section_ids(html).keys())
    
    mismatches = []
    for link in toc_links:
        if link not in section_ids:
            mismatches.append(f"TOC links to '{link}' but no matching section ID found")
    
    return len(mismatches) == 0, mismatches


def check_required_sections(html: str, is_masters: bool = False) -> Tuple[bool, List[str]]:
    """Check if all required sections are present"""
    section_ids = set(extract_section_ids(html).keys())
    missing = []
    
    # Check required sections
    for req_section in REQUIRED_SECTIONS:
        # For non-Masters plans, check section-13-women and section-14-faq
        # For Masters plans, check section-14-women and section-15-faq
        if not is_masters:
            if req_section in ["section-14-women-specific-considerations", "section-15-faq"]:
                continue  # Skip Masters-specific numbering
            if req_section == "section-13-women-specific-considerations":
                if req_section not in section_ids:
                    missing.append(f"Missing required section: {req_section}")
            elif req_section == "section-14-faq":
                if req_section not in section_ids:
                    missing.append(f"Missing required section: {req_section}")
            else:
                if req_section not in section_ids:
                    missing.append(f"Missing required section: {req_section}")
        else:
            # Masters plans should have section-14-women and section-15-faq
            if req_section in ["section-13-women-specific-considerations", "section-14-faq"]:
                continue  # Skip non-Masters numbering
            if req_section not in section_ids:
                missing.append(f"Missing required section: {req_section}")
    
    # Check conditional sections
    if is_masters:
        for cond_section in CONDITIONAL_SECTIONS:
            if cond_section not in section_ids:
                missing.append(f"Missing conditional section (Masters): {cond_section}")
    else:
        # Non-Masters plans should NOT have Masters section
        for cond_section in CONDITIONAL_SECTIONS:
            if cond_section in section_ids:
                missing.append(f"Unexpected section found (not a Masters plan): {cond_section}")
    
    return len(missing) == 0, missing


def check_duplicate_ids(html: str) -> Tuple[bool, List[str]]:
    """Check for duplicate section IDs (allowing 2 occurrences: section tag + h2 tag)"""
    section_ids = extract_section_ids(html)
    duplicates = []
    
    for section_id, occurrences in section_ids.items():
        # It's normal for sections to have IDs on both <section> and <h2> tags (2 occurrences)
        # More than 2 is a problem
        if len(occurrences) > 2:
            duplicates.append(f"Duplicate section ID '{section_id}' found {len(occurrences)} times (expected max 2)")
    
    return len(duplicates) == 0, duplicates


def check_women_specific_content(html: str) -> Tuple[bool, List[str]]:
    """Check if Women-Specific section has actual content"""
    issues = []
    
    # Check if section exists
    if "section-13-women-specific-considerations" not in html and "section-14-women-specific-considerations" not in html:
        issues.append("Women-Specific section not found")
        return False, issues
    
    # Check for key content markers
    required_content = [
        "Women aren't small men",
        "Menstrual Cycle and Training",
        "Iron: The Critical Difference",
    ]
    
    for content in required_content:
        if content not in html:
            issues.append(f"Women-Specific section missing key content: '{content}'")
    
    return len(issues) == 0, issues


def check_placeholders(html: str) -> Tuple[bool, List[str]]:
    """Check for unreplaced placeholder variables"""
    pattern = r'\{\{[A-Z_]+(?:\s+\|\s+[^}]+)?\}\}'
    placeholders = re.findall(pattern, html)
    
    # Filter out known safe placeholders that might be in comments or examples
    unsafe_placeholders = []
    for placeholder in placeholders:
        # Skip if it's in a comment
        if '<!--' in html[:html.find(placeholder)]:
            continue
        unsafe_placeholders.append(placeholder)
    
    return len(unsafe_placeholders) == 0, unsafe_placeholders


def check_old_content(html: str) -> Tuple[bool, List[str]]:
    """Check for content that should be removed"""
    forbidden_patterns = [
        (r'id="section-\d+">\d+: QUICK REFERENCE', "QUICK REFERENCE section (old content)"),
        (r'<h1[^>]*>.*QUICK REFERENCE', "QUICK REFERENCE section heading (old content)"),
        (r'id="section-\d+">\d+: GLOSSARY', "GLOSSARY section (should be FAQ)"),
        (r'<h1[^>]*>.*GLOSSARY', "GLOSSARY section heading (should be FAQ)"),
        (r'FTP \(Functional Threshold Power\)', "Glossary term (old content)"),
        (r'LTHR \(Lactate Threshold Heart Rate\)', "Glossary term (old content)"),
        (r'INFOGRAPHIC_RATING_HEX', "Unreplaced placeholder"),
        (r'INFOGRAPHIC_DIFFICULTY_TABLE', "Unreplaced placeholder"),
    ]
    
    issues = []
    for pattern, description in forbidden_patterns:
        if re.search(pattern, html, re.IGNORECASE):
            issues.append(description)
    
    return len(issues) == 0, issues


def check_section_sequence(html: str, is_masters: bool) -> Tuple[bool, List[str]]:
    """Check section numbers are sequential without gaps"""
    # Extract section numbers from IDs
    section_pattern = r'id="section-(\d+)'
    matches = re.findall(section_pattern, html)
    
    if not matches:
        return False, ["No section IDs found"]
    
    # Convert to integers and get unique values
    section_numbers = sorted(set(int(m) for m in matches))
    
    # Expected sequence depends on plan type
    if is_masters:
        expected = list(range(1, 16))  # 1-15 for Masters
    else:
        expected = list(range(1, 15))  # 1-14 for non-Masters
    
    issues = []
    
    # Check for missing sections
    missing = [n for n in expected if n not in section_numbers]
    if missing:
        issues.append(f"Missing section numbers: {missing}")
    
    # Check for unexpected sections
    unexpected = [n for n in section_numbers if n not in expected]
    if unexpected:
        issues.append(f"Unexpected section numbers: {unexpected}")
    
    # Check for gaps in sequence
    if section_numbers:
        gaps = []
        for i in range(len(section_numbers) - 1):
            if section_numbers[i+1] - section_numbers[i] > 1:
                gaps.append(f"{section_numbers[i]}-{section_numbers[i+1]}")
        if gaps:
            issues.append(f"Gaps in section sequence: {', '.join(gaps)}")
    
    return len(issues) == 0, issues


def check_css_embedding(html: str) -> Tuple[bool, List[str]]:
    """Check CSS is embedded, not external link"""
    issues = []
    
    # Check for external CSS links (should not exist, except Google Fonts)
    css_links = re.findall(r'<link[^>]*rel=["\']stylesheet["\']', html, re.IGNORECASE)
    for link_match in css_links:
        # Allow Google Fonts links
        if 'fonts.googleapis.com' not in link_match and 'fonts.gstatic.com' not in link_match:
            issues.append(f"External CSS link found (should be embedded): {link_match[:50]}...")
    
    # Check for embedded CSS (should exist)
    if '<style>' not in html:
        issues.append("No embedded CSS found (should have <style> tags)")
    
    return len(issues) == 0, issues


def check_file_size(file_path: Path) -> Tuple[bool, List[str]]:
    """Check file size is reasonable"""
    size_kb = file_path.stat().st_size / 1024
    
    issues = []
    if size_kb < 50:
        issues.append(f"File too small: {size_kb:.1f}KB (possible incomplete generation, expected >50KB)")
    elif size_kb > 500:
        issues.append(f"File too large: {size_kb:.1f}KB (possible corruption, expected <500KB)")
    
    return len(issues) == 0, issues


def verify_guide(guide_path: Path) -> Dict:
    """Verify a single guide file"""
    with open(guide_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Detect if this is a Masters plan
    is_masters = "section-13-masters-specific-considerations" in html or "masters" in guide_path.name.lower()
    
    results = {
        'file': str(guide_path),
        'is_masters': is_masters,
        'toc_matches': check_toc_matches(html),
        'required_sections': check_required_sections(html, is_masters),
        'duplicate_ids': check_duplicate_ids(html),
        'women_content': check_women_specific_content(html),
        'placeholders': check_placeholders(html),
        'old_content': check_old_content(html),
        'section_sequence': check_section_sequence(html, is_masters),
        'css_embedding': check_css_embedding(html),
        'file_size': check_file_size(guide_path),
    }
    
    return results


def main():
    """Main verification function"""
    if len(sys.argv) < 2:
        print("Usage: python verify_guide_structure.py <guide_file_or_directory> [--skip-index]")
        print("  --skip-index: Skip verification of index.html files")
        sys.exit(1)
    
    skip_index = "--skip-index" in sys.argv
    input_path = Path(sys.argv[1])
    
    # Collect guide files
    if input_path.is_file():
        guide_files = [input_path]
    elif input_path.is_dir():
        guide_files = [f for f in input_path.glob("*.html") if not (skip_index and f.name == "index.html")]
    else:
        print(f"Error: {input_path} is not a file or directory")
        sys.exit(1)
    
    if not guide_files:
        print(f"No HTML files found in {input_path}")
        sys.exit(1)
    
    print(f"🔍 Verifying {len(guide_files)} guide file(s)...\n")
    
    all_passed = True
    results = []
    
    for guide_file in sorted(guide_files):
        result = verify_guide(guide_file)
        results.append(result)
        
        # Check all conditions
        toc_ok, toc_issues = result['toc_matches']
        sections_ok, section_issues = result['required_sections']
        dup_ok, dup_issues = result['duplicate_ids']
        women_ok, women_issues = result['women_content']
        placeholders_ok, placeholder_issues = result['placeholders']
        old_content_ok, old_content_issues = result['old_content']
        sequence_ok, sequence_issues = result['section_sequence']
        css_ok, css_issues = result['css_embedding']
        size_ok, size_issues = result['file_size']
        
        file_passed = (toc_ok and sections_ok and dup_ok and women_ok and 
                      placeholders_ok and old_content_ok and sequence_ok and 
                      css_ok and size_ok)
        
        if not file_passed:
            all_passed = False
            print(f"❌ {guide_file.name}")
            if not toc_ok:
                print(f"   TOC Mismatches:")
                for issue in toc_issues:
                    print(f"     - {issue}")
            if not sections_ok:
                print(f"   Missing Sections:")
                for issue in section_issues:
                    print(f"     - {issue}")
            if not dup_ok:
                print(f"   Duplicate IDs:")
                for issue in dup_issues:
                    print(f"     - {issue}")
            if not women_ok:
                print(f"   Women-Specific Issues:")
                for issue in women_issues:
                    print(f"     - {issue}")
            if not placeholders_ok:
                print(f"   Placeholder Variables:")
                for issue in placeholder_issues[:5]:  # Limit to first 5
                    print(f"     - {issue}")
                if len(placeholder_issues) > 5:
                    print(f"     ... and {len(placeholder_issues) - 5} more")
            if not old_content_ok:
                print(f"   Old Content Found:")
                for issue in old_content_issues:
                    print(f"     - {issue}")
            if not sequence_ok:
                print(f"   Section Sequence Issues:")
                for issue in sequence_issues:
                    print(f"     - {issue}")
            if not css_ok:
                print(f"   CSS Embedding Issues:")
                for issue in css_issues:
                    print(f"     - {issue}")
            if not size_ok:
                print(f"   File Size Issues:")
                for issue in size_issues:
                    print(f"     - {issue}")
        else:
            print(f"✓ {guide_file.name} ({'Masters' if result['is_masters'] else 'Standard'})")
    
    print(f"\n{'='*60}")
    if all_passed:
        print("✅ All guides passed verification!")
        sys.exit(0)
    else:
        print("❌ Some guides failed verification")
        sys.exit(1)


if __name__ == "__main__":
    main()

