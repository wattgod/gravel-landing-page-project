#!/usr/bin/env python3
"""
MARKETPLACE DESCRIPTION QC VALIDATOR
====================================
Run after generating HTML descriptions to catch issues BEFORE review.

Usage:
    python validate_descriptions.py [output_dir]
    
Exit codes:
    0 = All checks passed
    1 = Validation failures found
"""

import os
import sys
import re
from pathlib import Path
from collections import defaultdict

# ============================================================================
# VALIDATION RULES
# ============================================================================

REQUIRED_ELEMENTS = {
    'opening': r'<p style="margin:0;font-size:24px;font-weight:700',
    'story': r'<p style="margin:0;font-size:16px">(?!This is |Built for |Designed for |Unbound)',  # Not a closing
    'plan_name_header': r'What the .+ plan Includes',
    'guide_header': r'18,000\+ Word Guide',
    'guide_intrigue': r'<p style="margin:0 0 6px;font-size:14px;font-style:italic;color:#555">',
    'guide_topics': r'— ',  # Em dash indicating topic format
    'alternative_header': r'Alternative\?',
    'alternative_content': r'Or you could',
    'value_prop_header': r'What This Plan Delivers',
    'value_prop_philosophy': r'<p style="margin:0 0 8px;font-size:14px;font-weight:700">',
    'closing': r'<p style="margin:0;font-size:16px">(This is |Built for |Designed for |Unbound)',
    'footer_url': r'gravelgodcycling\.com',
    'footer_brand': r'GRAVEL GOD CYCLING',
}

MASTERS_KEYWORDS = [
    'recovery',
    'age',
    '40',
    '45',
    '50',
    'masters',
    'older',
    'veteran'
]

FORBIDDEN_PATTERNS = {
    'bullets_in_main': r'<ul style=',  # Should only be in guide box
    'old_header_format': r'<div style="border-bottom:2px solid #000;padding-bottom:10px;margin-bottom:14px">',
    'pain_problem_box': r'Pain / Problem',
    'you_should_buy': r'You Should Buy This If',
    'race_header': r'<p style="margin:0;font-size:30px',
    'generic_closing_start': r'This isn\'t generic\.',
}

MAX_CHAR_LIMIT = 3700  # Warning threshold
HARD_CHAR_LIMIT = 4000  # TrainingPeaks limit

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_file(filepath):
    """Run all validation checks on a single HTML file."""
    errors = []
    warnings = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    is_masters = 'masters' in filename
    
    # 1. CHARACTER COUNT
    char_count = len(content)
    if char_count > HARD_CHAR_LIMIT:
        errors.append(f"HARD LIMIT EXCEEDED: {char_count} chars (limit: {HARD_CHAR_LIMIT})")
    elif char_count > MAX_CHAR_LIMIT:
        warnings.append(f"Near limit: {char_count} chars (warning at {MAX_CHAR_LIMIT})")
    
    # 2. REQUIRED ELEMENTS
    for element, pattern in REQUIRED_ELEMENTS.items():
        if not re.search(pattern, content):
            errors.append(f"Missing required element: {element}")
    
    # 3. FORBIDDEN PATTERNS (old template artifacts)
    for pattern_name, pattern in FORBIDDEN_PATTERNS.items():
        if re.search(pattern, content):
            errors.append(f"Found forbidden pattern: {pattern_name}")
    
    # 4. MASTERS-SPECIFIC VALIDATION
    if is_masters:
        # Masters plans MUST have Masters content
        masters_content_found = any(
            keyword in content.lower() 
            for keyword in MASTERS_KEYWORDS
        )
        # Check for multiple Masters keywords (not just one mention)
        masters_keyword_count = sum(
            content.lower().count(keyword) 
            for keyword in MASTERS_KEYWORDS
        )
        # Need at least 2 instances of Masters keywords (beyond just plan name)
        if not masters_content_found or masters_keyword_count < 2:
            errors.append(
                f"Masters plan missing Masters-specific content. "
                f"Need keywords like: {', '.join(MASTERS_KEYWORDS[:5])}"
            )
    else:
        # NON-Masters plans MUST NOT have Masters content
        masters_mentions = sum(
            content.lower().count(keyword) 
            for keyword in ['45+', '50+', 'age', 'masters', 'older', 'veteran']
        )
        if masters_mentions > 2:  # Allow 1-2 incidental mentions
            errors.append(
                f"Non-Masters plan contains Masters-specific content "
                f"({masters_mentions} age-related mentions found)"
            )
    
    # 5. CLOSING REPETITION CHECK
    # Only check the last paragraph before the footer (actual closing)
    # Other paragraphs may contain "Unbound" but aren't the closing
    footer_match = re.search(r'<div style="border-top:2px', content)
    if footer_match:
        before_footer = content[:footer_match.start()]
        # Find all paragraphs before footer
        all_paragraphs = list(re.finditer(
            r'<p style="margin:0;font-size:16px">([^<]+)</p>',
            before_footer
        ))
        # Check only the last paragraph (the actual closing)
        if all_paragraphs:
            last_paragraph_text = all_paragraphs[-1].group(1)
            # Check if it matches closing pattern
            closing_pattern = r'^(This is |Built for |Designed for |Unbound)'
            if not re.search(closing_pattern, last_paragraph_text, re.IGNORECASE):
                # Last paragraph doesn't match closing pattern - might be missing
                errors.append("Last paragraph before footer doesn't match closing pattern")
    else:
        # No footer found - check for any closing-style paragraphs (fallback)
        closing_matches = re.findall(
            r'<p style="margin:0;font-size:16px">([^<]*(?:This is |Built for |Designed for |Unbound)[^<]+)</p>',
            content
        )
        if len(closing_matches) > 1:
            errors.append(f"Multiple closing-style paragraphs found: {len(closing_matches)}")
    
    # 6. GUIDE INTRIGUE LINE FORMAT
    intrigue_matches = re.findall(
        r'<p style="margin:0 0 6px;font-size:14px;font-style:italic;color:#555">([^<]+)</p>',
        content
    )
    if intrigue_matches:
        intrigue_text = intrigue_matches[0]
        if len(intrigue_text) < 20:
            warnings.append(f"Guide intrigue line very short: '{intrigue_text[:50]}'")
        if len(intrigue_text) > 120:
            warnings.append(f"Guide intrigue line very long: {len(intrigue_text)} chars")
    
    # 7. PLAN NAME CONSISTENCY
    plan_name_matches = re.findall(r'What the (.+?) plan Includes', content)
    if plan_name_matches:
        plan_name = plan_name_matches[0]
        if len(plan_name.split()) > 4:
            warnings.append(f"Plan name very long: '{plan_name}'")
    
    # 8. EM DASH CHECK (proper formatting)
    if ' — ' not in content and ' - ' in content:
        warnings.append("Found hyphens (-) where em dashes (—) expected")
    
    return {
        'filepath': filepath,
        'filename': filename,
        'char_count': char_count,
        'errors': errors,
        'warnings': warnings,
        'passed': len(errors) == 0
    }

def validate_directory(output_dir):
    """Validate all HTML files in output directory."""
    results = []
    
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                result = validate_file(filepath)
                results.append(result)
    
    return results

def extract_opening(content):
    """Extract opening paragraph from HTML."""
    match = re.search(r'<p style="margin:0;font-size:24px;font-weight:700;line-height:1.3">([^<]+)</p>', content)
    return match.group(1).strip() if match else ""

def extract_story(content):
    """Extract story justification paragraph from HTML."""
    # First paragraph after opening (before "What the" header)
    match = re.search(r'<div style="margin-bottom:14px">\s*<p style="margin:0;font-size:16px">([^<]+)</p>', content)
    return match.group(1).strip() if match else ""

def extract_closing(content):
    """Extract closing statement from HTML."""
    # Find the last paragraph before the footer (which has border-top:2px)
    # This is the closing statement
    footer_match = re.search(r'<div style="border-top:2px', content)
    if footer_match:
        before_footer = content[:footer_match.start()]
        # Find the last <p> tag with the closing style before the footer
        matches = list(re.finditer(r'<p style="margin:0;font-size:16px">([^<]+)</p>', before_footer))
        if matches:
            return matches[-1].group(1).strip()
    # Fallback: look for closing patterns
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

def validate_cross_plan_duplicates(results):
    """Check that no content is duplicated across any plans (within or across tiers)."""
    from collections import defaultdict
    
    # Track content by variation type across ALL plans
    content_tracker = defaultdict(dict)  # content -> (filepath, tier)
    
    errors = []
    
    for result in results:
        filepath = result['filepath']
        filename = result['filename']
        tier = get_tier_from_filename(filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract each variation type
        opening = extract_opening(content)
        story = extract_story(content)
        closing = extract_closing(content)
        alternative = extract_alternative(content)
        
        # Check for duplicates (within or across tiers)
        variations = [
            ('opening', opening),
            ('story', story),
            ('closing', closing),
            ('alternative', alternative)
        ]
        
        for content_type, variation_content in variations:
            if variation_content:  # Only check non-empty content
                if variation_content in content_tracker[content_type]:
                    # Found duplicate
                    original_file, original_tier = content_tracker[content_type][variation_content]
                    errors.append(
                        f"DUPLICATE {content_type}: {os.path.basename(filepath)} "
                        f"and {os.path.basename(original_file)} have identical content"
                    )
                else:
                    content_tracker[content_type][variation_content] = (filepath, tier)
    
    return errors

def print_results(results):
    """Print validation results in readable format."""
    total = len(results)
    passed = sum(1 for r in results if r['passed'])
    failed = total - passed
    
    # Check for cross-plan duplicates
    duplicate_errors = validate_cross_plan_duplicates(results)
    if duplicate_errors:
        # Add duplicate errors to all results that have them
        for error in duplicate_errors:
            # Find which files are involved
            for result in results:
                if any(os.path.basename(result['filepath']) in error for _ in [1]):
                    result['errors'].append(error)
                    result['passed'] = False
        failed += len(duplicate_errors)
    
    print("\n" + "="*80)
    print("MARKETPLACE DESCRIPTION VALIDATION REPORT")
    print("="*80)
    
    # Summary
    print(f"\nTotal files: {total}")
    print(f"✓ Passed: {passed}")
    if failed > 0:
        print(f"✗ Failed: {failed}")
    print()
    
    # Character count summary
    char_counts = [r['char_count'] for r in results]
    print("CHARACTER COUNTS:")
    print(f"  Min: {min(char_counts)}")
    print(f"  Max: {max(char_counts)}")
    print(f"  Avg: {sum(char_counts) // len(char_counts)}")
    print()
    
    # Detailed results for failures
    if failed > 0:
        print("="*80)
        print("FAILURES:")
        print("="*80)
        for result in results:
            if not result['passed']:
                print(f"\n✗ {result['filename']} ({result['char_count']} chars)")
                for error in result['errors']:
                    print(f"  ERROR: {error}")
                for warning in result['warnings']:
                    print(f"  WARN:  {warning}")
    
    # Warnings (even for passing files)
    warnings_found = [r for r in results if r['warnings']]
    if warnings_found:
        print("\n" + "="*80)
        print("WARNINGS:")
        print("="*80)
        for result in warnings_found:
            if result['passed']:  # Only show warnings for passing files
                print(f"\n⚠ {result['filename']}")
                for warning in result['warnings']:
                    print(f"  {warning}")
    
    # Success message
    if failed == 0:
        print("\n" + "="*80)
        print("✓ ALL VALIDATIONS PASSED")
        print("="*80)
        print("\nDescriptions ready for TrainingPeaks upload.")
    else:
        print("\n" + "="*80)
        print("✗ VALIDATION FAILED")
        print("="*80)
        print("\nFix errors before uploading to TrainingPeaks.")
    
    print()
    return failed == 0

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    else:
        output_dir = "output/html_descriptions"
    
    if not os.path.exists(output_dir):
        print(f"Error: Directory not found: {output_dir}")
        sys.exit(1)
    
    results = validate_directory(output_dir)
    
    if not results:
        print(f"Error: No HTML files found in {output_dir}")
        sys.exit(1)
    
    success = print_results(results)
    sys.exit(0 if success else 1)
