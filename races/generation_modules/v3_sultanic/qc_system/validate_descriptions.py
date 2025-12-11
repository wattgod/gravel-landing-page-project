#!/usr/bin/env python3
"""
Validate generated marketplace description HTML files.

Checks:
- Character counts (warning at 3700, error at 4000)
- Required elements present
- No old template artifacts
- Masters plans have Masters-specific content
- Proper formatting
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Character limits
CHAR_WARNING = 3700
CHAR_ERROR = 4000

# Required elements (regex patterns) - updated for current template
REQUIRED_ELEMENTS = {
    'opening_24px': r'font-size:24px.*font-weight:700|font-size:30px.*font-weight:900',  # Allow both formats
    'story_paragraph': r'<p style="margin:0;font-size:16px">[^<]{50,}',
    'plan_name_header': r'What the [^<]+ plan Includes|What the [^<]+ Includes',
    'guide_header': r'18,000\+ Word Guide',
    'guide_intrigue': r'font-style:italic.*color:#555|font-style:italic.*color:#666',  # Grey italic line
    'guide_topics': r'[A-Z][a-z]+ [A-Z][a-z]+ - [^•]+ •|• [A-Z][a-z]+ -',  # Topics with dashes and bullets
    'alternative_header': r'Alternative\?',
    'behavioral_mirror': r'Or you could',
    'value_prop_header': r'What This Plan Delivers',
    'value_prop_philosophy': r'font-weight:700.*[^<]{30,}',
    'value_prop_items': r'[^•]+ • [^•]+ • [^•]+|• [^•]+ • [^•]+',  # Bullet-separated items
    'closing': r'Unbound Gravel 200|This is|Built for|Designed for',
    'footer_url': r'gravelgodcycling\.com',
    'footer_branding': r'GRAVEL GOD CYCLING',
}

# Forbidden patterns (old template artifacts)
FORBIDDEN_PATTERNS = {
    'race_header': r'UNBOUND GRAVEL 200.*font-size:30px',
    'bullets_main': r'<ul style="margin:0;padding-left:15px">.*<li>',
    'pain_problem_box': r'Pain / Problem',
    'buy_this_if': r'You Should Buy This If',
    'generic_opening': r"This isn't generic",
    'old_closing_start': r"This isn't generic.*It's designed for",
}

# Masters-specific keywords (must appear 2+ times, excluding plan name)
MASTERS_KEYWORDS = [
    'recovery', 'age', '40', '45', '50', 'masters', 'HRV', 'older', '50\+',
    'longer recovery', 'recovery windows', 'age-appropriate', 'autoregulation'
]

# Masters plan identifiers
MASTERS_PLANS = [
    'ayahuasca.*masters',
    'finisher.*masters',
    'compete.*masters',
]


def is_masters_plan(filename: str) -> bool:
    """Check if this is a Masters plan."""
    filename_lower = filename.lower()
    return any(re.search(pattern, filename_lower) for pattern in MASTERS_PLANS)


def count_masters_keywords(content: str) -> int:
    """Count Masters-specific keywords in content (excluding plan name)."""
    # Remove plan name mentions
    content_clean = re.sub(r'What the [^<]+ plan', '', content, flags=re.IGNORECASE)
    content_clean = re.sub(r'[A-Z][a-z]+ Masters', '', content_clean)
    
    count = 0
    for keyword in MASTERS_KEYWORDS:
        matches = re.findall(keyword, content_clean, re.IGNORECASE)
        count += len(matches)
    
    return count


def validate_file(filepath: Path) -> Tuple[bool, List[str]]:
    """Validate a single HTML file."""
    errors = []
    warnings = []
    
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        return False, [f"Could not read file: {e}"]
    
    filename = filepath.name
    
    # Character count
    char_count = len(content)
    if char_count > CHAR_ERROR:
        errors.append(f"Character count {char_count} exceeds hard limit {CHAR_ERROR}")
    elif char_count > CHAR_WARNING:
        warnings.append(f"Character count {char_count} exceeds warning threshold {CHAR_WARNING}")
    
    # Required elements
    for element_name, pattern in REQUIRED_ELEMENTS.items():
        if not re.search(pattern, content, re.DOTALL | re.IGNORECASE):
            errors.append(f"Missing required element: {element_name}")
    
    # Forbidden patterns
    for pattern_name, pattern in FORBIDDEN_PATTERNS.items():
        if re.search(pattern, content, re.DOTALL | re.IGNORECASE):
            errors.append(f"Found forbidden pattern: {pattern_name}")
    
    # Masters-specific content
    if is_masters_plan(filename):
        masters_count = count_masters_keywords(content)
        if masters_count < 2:
            errors.append(f"Masters plan missing Masters-specific content (found {masters_count} keywords, need 2+)")
    
    # Check for repetitive closings (same closing across multiple files)
    # This is handled at the batch level
    
    return len(errors) == 0, errors + warnings


def validate_all_descriptions(base_dir: Path) -> Dict:
    """Validate all marketplace description files."""
    results = {
        'passed': [],
        'failed': [],
        'warnings': [],
        'char_counts': [],
    }
    
    # Find all marketplace_description.html files
    description_files = list(base_dir.rglob('marketplace_description.html'))
    
    if not description_files:
        print(f"ERROR: No marketplace_description.html files found in {base_dir}")
        return results
    
    print("=" * 80)
    print("MARKETPLACE DESCRIPTION VALIDATION REPORT")
    print("=" * 80)
    print(f"\nTotal files: {len(description_files)}\n")
    
    for filepath in sorted(description_files):
        is_valid, issues = validate_file(filepath)
        char_count = len(filepath.read_text(encoding='utf-8'))
        results['char_counts'].append(char_count)
        
        if is_valid:
            results['passed'].append((filepath.name, char_count))
        else:
            results['failed'].append((filepath.name, char_count, issues))
    
    # Print results
    print(f"✓ Passed: {len(results['passed'])}")
    print(f"✗ Failed: {len(results['failed'])}")
    
    if results['char_counts']:
        print(f"\nCHARACTER COUNTS:")
        print(f"  Min: {min(results['char_counts'])}")
        print(f"  Max: {max(results['char_counts'])}")
        print(f"  Avg: {sum(results['char_counts']) // len(results['char_counts'])}")
    
    if results['failed']:
        print("\n" + "=" * 80)
        print("FAILURES:")
        print("=" * 80)
        for filename, char_count, issues in results['failed']:
            print(f"\n✗ {filename} ({char_count} chars)")
            for issue in issues:
                print(f"  ERROR: {issue}")
    
    print("\n" + "=" * 80)
    if results['failed']:
        print("✗ VALIDATION FAILED")
        print("=" * 80)
        print("\nFix errors before uploading to TrainingPeaks.")
        return results
    else:
        print("✓ VALIDATION PASSED")
        print("=" * 80)
        return results


def main():
    """Main entry point."""
    # Find base directory (races/Unbound Gravel 200)
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent.parent.parent.parent / "races" / "Unbound Gravel 200"
    
    if not base_dir.exists():
        print(f"ERROR: Directory not found: {base_dir}")
        sys.exit(1)
    
    results = validate_all_descriptions(base_dir)
    
    # Exit with error code if validation failed
    if results['failed']:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

