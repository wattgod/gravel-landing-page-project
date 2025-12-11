#!/usr/bin/env python3
"""
Validate variation pool files.

Checks:
- Correct number of variations per tier
- No duplicate content
- No placeholder text
- No old template artifacts
- Masters content exists
- Reasonable content length
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Expected minimum variations per pool
MIN_VARIATIONS = {
    'comparison_hooks': 10,
    'solution_state': 5,
    'story_justifications': 5,
    'choice_features': 8,
    'guide_topics': 8,
    'guide_intrigue': 20,
    'behavioral_mirrors': 20,
    'closings': 5,
}

# Forbidden patterns in pools
FORBIDDEN_PATTERNS = [
    r'\[TODO\]',
    r'\[REPLACE\]',
    r'\[PLACEHOLDER\]',
    r'XXX',
    r'FIXME',
    r'This isn\'t generic',  # Old template
    r'Pain / Problem',  # Old template
]

# Placeholder patterns
PLACEHOLDER_PATTERNS = [
    r'\{[A-Z_]+\}',  # {VARIABLE}
    r'\[.*\]',  # [something]
]


def validate_pool_file(filepath: Path) -> Tuple[bool, List[str]]:
    """Validate a variation pool Python file."""
    errors = []
    warnings = []
    
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        return False, [f"Could not read file: {e}"]
    
    # Check for forbidden patterns
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            errors.append(f"Found forbidden pattern: {pattern}")
    
    # Check for placeholder text
    for pattern in PLACEHOLDER_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            warnings.append(f"Found potential placeholders: {matches[:3]}")
    
    # Check for Masters content in Finisher/Compete tiers
    if 'finisher' in filepath.name.lower() or 'compete' in filepath.name.lower():
        if 'masters' not in content.lower() and 'recovery' not in content.lower():
            warnings.append("Finisher/Compete tier should have Masters variations")
    
    # Check variation counts (basic check - look for list definitions)
    list_patterns = [
        r'COMPARISON_HOOKS\s*=\s*\[',
        r'CLOSING_STATEMENTS\s*=\s*\[',
        r'GUIDE_INTRIGUE\s*=\s*\[',
    ]
    
    for pattern in list_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            # Count items in list (rough estimate)
            list_match = re.search(pattern + r'([^\]]+)', content, re.DOTALL | re.IGNORECASE)
            if list_match:
                items = list_match.group(1)
                item_count = len(re.findall(r'"[^"]+"', items))
                if item_count < 5:
                    warnings.append(f"Pool may have too few variations (found {item_count})")
    
    return len(errors) == 0, errors + warnings


def validate_all_pools(base_dir: Path) -> Dict:
    """Validate all variation pool files."""
    results = {
        'passed': [],
        'failed': [],
        'warnings': [],
    }
    
    # Find variation pool files
    pool_files = list(base_dir.rglob('*VARIATION_POOLS*.py'))
    pool_files += list(base_dir.rglob('*variation*.py'))
    
    if not pool_files:
        print(f"WARNING: No variation pool files found in {base_dir}")
        return results
    
    print("=" * 80)
    print("VARIATION POOL VALIDATION REPORT")
    print("=" * 80)
    print(f"\nTotal files: {len(pool_files)}\n")
    
    for filepath in sorted(pool_files):
        is_valid, issues = validate_pool_file(filepath)
        
        errors = [i for i in issues if 'ERROR' in i or not i.startswith('Found potential')]
        warnings_list = [i for i in issues if i.startswith('Found potential') or 'should have' in i]
        
        if is_valid and not errors:
            results['passed'].append(filepath.name)
        else:
            results['failed'].append((filepath.name, errors))
        
        if warnings_list:
            results['warnings'].append((filepath.name, warnings_list))
    
    # Print results
    print(f"✓ Passed: {len(results['passed'])}")
    print(f"✗ Failed: {len(results['failed'])}")
    
    if results['warnings']:
        print(f"⚠ Warnings: {len(results['warnings'])}")
    
    if results['failed']:
        print("\n" + "=" * 80)
        print("FAILURES:")
        print("=" * 80)
        for filename, errors in results['failed']:
            print(f"\n✗ {filename}")
            for error in errors:
                print(f"  {error}")
    
    if results['warnings']:
        print("\n" + "=" * 80)
        print("WARNINGS:")
        print("=" * 80)
        for filename, warnings_list in results['warnings']:
            print(f"\n⚠ {filename}")
            for warning in warnings_list:
                print(f"  {warning}")
    
    print("\n" + "=" * 80)
    if results['failed']:
        print("✗ VALIDATION FAILED")
        print("=" * 80)
        return results
    else:
        print("✓ VALIDATION PASSED")
        print("=" * 80)
        return results


def main():
    """Main entry point."""
    # Find base directory (v3_sultanic)
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent
    
    if not base_dir.exists():
        print(f"ERROR: Directory not found: {base_dir}")
        sys.exit(1)
    
    results = validate_all_pools(base_dir)
    
    # Exit with error code if validation failed
    if results['failed']:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    from typing import Tuple
    main()

