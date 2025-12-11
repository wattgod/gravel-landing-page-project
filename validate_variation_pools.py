#!/usr/bin/env python3
"""
VARIATION POOL QC VALIDATOR
============================
Validates variation pool files have correct structure and content.

Usage:
    python validate_variation_pools.py
    
Checks:
    - All tiers have required number of variations
    - Masters content exists where needed
    - No duplicate content
    - Content length appropriate
    - No placeholder text
"""

import sys
import re
from pathlib import Path

# Import all variation pools
try:
    from TIER_SPECIFIC_SOLUTION_STATE_V3 import SOLUTION_STATE_OPENINGS
    from TIER_SPECIFIC_CHOICE_FEATURES import CHOICE_FEATURES
    from TIER_SPECIFIC_GUIDE_TOPICS_FINAL import GUIDE_TOPICS
    from ALTERNATIVE_HOOKS_BEHAVIORAL import ALTERNATIVE_HOOKS
    from TIER_SPECIFIC_STORY_JUSTIFICATIONS import STORY_JUSTIFICATIONS
    from TIER_SPECIFIC_VALUE_PROP_BOXES import VALUE_PROP_BOXES
    from GUIDE_INTRIGUE_LINES import GUIDE_INTRIGUE_LINES
except ImportError as e:
    print(f"Error importing variation pools: {e}")
    sys.exit(1)

# ============================================================================
# VALIDATION RULES
# ============================================================================

TIERS = ['ayahuasca', 'finisher', 'compete', 'podium']

EXPECTED_COUNTS = {
    'SOLUTION_STATE_OPENINGS': 5,
    'CHOICE_FEATURES': 8,
    'GUIDE_TOPICS': 8,
    'ALTERNATIVE_HOOKS': 21,
    'STORY_JUSTIFICATIONS': 5,
    'VALUE_PROP_BOXES': 5,
}

MASTERS_REQUIREMENTS = {
    'finisher': 2,  # At least 2 Masters variations in Finisher tier
    'compete': 2,   # At least 2 Masters variations in Compete tier
}

PLACEHOLDER_PATTERNS = [
    r'\[.*?\]',  # [placeholder]
    r'TODO',
    r'FIXME',
    r'XXX',
    r'REPLACE',
]

FORBIDDEN_CONTENT = [
    'This isn\'t generic',  # Old closing pattern
    'You Should Buy',        # Old template
    'Pain / Problem',        # Old template
]

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_tier_pool(pool_name, pool_data, expected_count):
    """Validate a single variation pool."""
    errors = []
    warnings = []
    
    for tier in TIERS:
        if tier not in pool_data:
            errors.append(f"{pool_name}: Missing tier '{tier}'")
            continue
        
        variations = pool_data[tier]
        actual_count = len(variations)
        
        # Count check
        if actual_count < expected_count:
            errors.append(f"{pool_name}[{tier}]: Only {actual_count} variations (expected {expected_count})")
        elif actual_count > expected_count:
            warnings.append(f"{pool_name}[{tier}]: {actual_count} variations (expected {expected_count}, extras OK)")
        
        # Check each variation
        for i, variation in enumerate(variations):
            variation_id = f"{pool_name}[{tier}][{i}]"
            
            # Empty check
            if not variation or not variation.strip():
                errors.append(f"{variation_id}: Empty variation")
                continue
            
            # Length check
            if len(variation) < 20:
                warnings.append(f"{variation_id}: Very short ({len(variation)} chars)")
            
            # Placeholder check
            for pattern in PLACEHOLDER_PATTERNS:
                if re.search(pattern, variation):
                    errors.append(f"{variation_id}: Contains placeholder pattern: {pattern}")
            
            # Forbidden content check
            for forbidden in FORBIDDEN_CONTENT:
                if forbidden in variation:
                    errors.append(f"{variation_id}: Contains forbidden content: '{forbidden}'")
        
        # Duplicate check
        if len(variations) != len(set(variations)):
            errors.append(f"{pool_name}[{tier}]: Contains duplicate variations")
        
        # Masters content check
        if tier in MASTERS_REQUIREMENTS:
            min_masters = MASTERS_REQUIREMENTS[tier]
            masters_count = sum(
                1 for v in variations 
                if any(kw in v.lower() for kw in ['recovery', 'age', '40', '45', '50', 'masters'])
            )
            if masters_count < min_masters:
                warnings.append(
                    f"{pool_name}[{tier}]: Only {masters_count} Masters variations "
                    f"(recommended: {min_masters}+)"
                )
    
    return errors, warnings

def validate_guide_intrigue():
    """Validate guide intrigue lines."""
    errors = []
    warnings = []
    
    if len(GUIDE_INTRIGUE_LINES) < 20:
        errors.append(f"GUIDE_INTRIGUE_LINES: Only {len(GUIDE_INTRIGUE_LINES)} variations (expected 20+)")
    
    for i, line in enumerate(GUIDE_INTRIGUE_LINES):
        if not line or not line.strip():
            errors.append(f"GUIDE_INTRIGUE_LINES[{i}]: Empty line")
            continue
        
        if len(line) < 30:
            warnings.append(f"GUIDE_INTRIGUE_LINES[{i}]: Very short ({len(line)} chars)")
        
        if len(line) > 120:
            warnings.append(f"GUIDE_INTRIGUE_LINES[{i}]: Very long ({len(line)} chars)")
        
        for pattern in PLACEHOLDER_PATTERNS:
            if re.search(pattern, line):
                errors.append(f"GUIDE_INTRIGUE_LINES[{i}]: Contains placeholder: {pattern}")
    
    # Duplicate check
    if len(GUIDE_INTRIGUE_LINES) != len(set(GUIDE_INTRIGUE_LINES)):
        errors.append("GUIDE_INTRIGUE_LINES: Contains duplicates")
    
    return errors, warnings

def validate_value_prop_boxes():
    """Special validation for value prop boxes (dict structure)."""
    errors = []
    warnings = []
    
    for tier in TIERS:
        if tier not in VALUE_PROP_BOXES:
            errors.append(f"VALUE_PROP_BOXES: Missing tier '{tier}'")
            continue
        
        variations = VALUE_PROP_BOXES[tier]
        
        for i, var_dict in enumerate(variations):
            var_id = f"VALUE_PROP_BOXES[{tier}][{i}]"
            
            # Structure check
            if 'philosophy' not in var_dict:
                errors.append(f"{var_id}: Missing 'philosophy' key")
            if 'props' not in var_dict:
                errors.append(f"{var_id}: Missing 'props' key")
            
            # Philosophy check
            if var_dict.get('philosophy'):
                phil = var_dict['philosophy']
                if len(phil) < 20:
                    warnings.append(f"{var_id}: Philosophy very short")
            
            # Props check
            props = var_dict.get('props', [])
            if len(props) != 4:
                errors.append(f"{var_id}: Expected 4 props, got {len(props)}")
    
    return errors, warnings

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "="*80)
    print("VARIATION POOL VALIDATION")
    print("="*80 + "\n")
    
    all_errors = []
    all_warnings = []
    
    # Validate each pool
    pools_to_check = [
        ('SOLUTION_STATE_OPENINGS', SOLUTION_STATE_OPENINGS, EXPECTED_COUNTS['SOLUTION_STATE_OPENINGS']),
        ('CHOICE_FEATURES', CHOICE_FEATURES, EXPECTED_COUNTS['CHOICE_FEATURES']),
        ('GUIDE_TOPICS', GUIDE_TOPICS, EXPECTED_COUNTS['GUIDE_TOPICS']),
        ('ALTERNATIVE_HOOKS', ALTERNATIVE_HOOKS, EXPECTED_COUNTS['ALTERNATIVE_HOOKS']),
        ('STORY_JUSTIFICATIONS', STORY_JUSTIFICATIONS, EXPECTED_COUNTS['STORY_JUSTIFICATIONS']),
    ]
    
    for pool_name, pool_data, expected_count in pools_to_check:
        print(f"Checking {pool_name}...")
        errors, warnings = validate_tier_pool(pool_name, pool_data, expected_count)
        all_errors.extend(errors)
        all_warnings.extend(warnings)
    
    # Validate value prop boxes (special structure)
    print("Checking VALUE_PROP_BOXES...")
    errors, warnings = validate_value_prop_boxes()
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Validate guide intrigue lines
    print("Checking GUIDE_INTRIGUE_LINES...")
    errors, warnings = validate_guide_intrigue()
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    print()
    
    # Report results
    if all_errors:
        print("="*80)
        print("ERRORS:")
        print("="*80)
        for error in all_errors:
            print(f"✗ {error}")
        print()
    
    if all_warnings:
        print("="*80)
        print("WARNINGS:")
        print("="*80)
        for warning in all_warnings:
            print(f"⚠ {warning}")
        print()
    
    if not all_errors and not all_warnings:
        print("="*80)
        print("✓ ALL VALIDATION CHECKS PASSED")
        print("="*80)
        print("\nVariation pools are ready for generation.\n")
        return 0
    elif not all_errors:
        print("="*80)
        print("✓ VALIDATION PASSED (with warnings)")
        print("="*80)
        print(f"\n{len(all_warnings)} warnings found. Review recommended.\n")
        return 0
    else:
        print("="*80)
        print("✗ VALIDATION FAILED")
        print("="*80)
        print(f"\n{len(all_errors)} errors found. Fix before generating.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
