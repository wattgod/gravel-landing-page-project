#!/usr/bin/env python3
"""
JSON SCHEMA REGRESSION TEST
============================
Ensures all race data JSON files follow the exact same schema structure.
Prevents import failures on the website by catching schema mismatches.

Exit codes:
    0 = All schema tests passed
    1 = Schema mismatches detected
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Any

# ============================================================================
# SCHEMA VALIDATION
# ============================================================================

def get_all_keys(data: Any, path: str = "") -> Set[str]:
    """Recursively get all keys from a nested dictionary."""
    keys = set()
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            keys.add(current_path)
            if isinstance(value, dict):
                keys.update(get_all_keys(value, current_path))
    return keys

def get_required_fields(data: Any, path: str = "") -> Dict[str, Any]:
    """Get required fields structure (non-optional fields)."""
    required = {}
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            if isinstance(value, dict):
                required[current_path] = get_required_fields(value, current_path)
            else:
                required[current_path] = type(value).__name__
    return required

def compare_schemas(reference: Dict, test: Dict, path: str = "") -> List[str]:
    """
    Compare two schemas and return list of mismatches.
    Returns critical mismatches (missing required fields, extra unexpected fields in core sections).
    """
    errors = []
    
    # Core sections that must match exactly
    critical_sections = [
        'final_verdict',
        'biased_opinion',
        'black_pill',
        'training_plans',
    ]
    
    def check_section(ref_data: Any, test_data: Any, section_path: str):
        """Check if a section matches the reference schema."""
        section_errors = []
        
        if not isinstance(ref_data, dict) or not isinstance(test_data, dict):
            return section_errors
        
        # Get all keys from both
        ref_keys = set(ref_data.keys())
        test_keys = set(test_data.keys())
        
        # Check for missing required fields
        missing = ref_keys - test_keys
        for key in missing:
            section_errors.append(f"Missing required field: {section_path}.{key}")
        
        # Check for unexpected fields in critical sections
        if any(critical in section_path for critical in critical_sections):
            unexpected = test_keys - ref_keys
            for key in unexpected:
                section_errors.append(f"Unexpected field in {section_path}: {key} (not in reference schema)")
        
        # Recursively check nested dictionaries
        for key in ref_keys & test_keys:
            if isinstance(ref_data[key], dict) and isinstance(test_data[key], dict):
                # Only recurse if both are dicts
                nested_errors = check_section(ref_data[key], test_data[key], f"{section_path}.{key}" if section_path else key)
                section_errors.extend(nested_errors)
        
        return section_errors
    
    errors.extend(check_section(reference, test, path))
    return errors

def test_race_data_schema(file_path: Path, reference_file: Path) -> List[str]:
    """
    Test a race data JSON file against the reference schema.
    Returns list of error messages.
    """
    errors = []
    
    try:
        with open(reference_file, 'r', encoding='utf-8') as f:
            reference = json.load(f)
        with open(file_path, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
    except Exception as e:
        return [f"Failed to parse files: {e}"]
    
    # Extract race objects
    ref_race = reference.get('race', {})
    test_race = test_data.get('race', {})
    
    if not ref_race:
        return [f"Reference file {reference_file.name} missing 'race' key"]
    if not test_race:
        return [f"Test file {file_path.name} missing 'race' key"]
    
    # CRITICAL: Check top-level race keys match exactly
    # Extra top-level fields cause "Invalid Content In File" upload errors
    ref_race_keys = set(ref_race.keys())
    test_race_keys = set(test_race.keys())
    
    missing_top_level = ref_race_keys - test_race_keys
    unexpected_top_level = test_race_keys - ref_race_keys
    
    if missing_top_level:
        errors.append(f"{file_path.name}: Missing top-level race fields: {', '.join(sorted(missing_top_level))}")
    if unexpected_top_level:
        errors.append(f"{file_path.name}: EXTRA top-level race fields (will cause upload failure): {', '.join(sorted(unexpected_top_level))}")
    
    # Compare critical sections directly
    # Check final_verdict, biased_opinion, training_plans match exactly
    critical_sections_to_check = ['final_verdict', 'biased_opinion', 'training_plans']
    
    for section in critical_sections_to_check:
        ref_section = ref_race.get(section, {})
        test_section = test_race.get(section, {})
        
        if not ref_section and test_section:
            errors.append(f"{file_path.name}: Has unexpected section '{section}' (not in reference)")
        elif ref_section and not test_section:
            errors.append(f"{file_path.name}: Missing required section '{section}'")
        elif ref_section and test_section:
            # Check keys match exactly for these critical sections
            ref_keys = set(ref_section.keys())
            test_keys = set(test_section.keys())
            
            missing = ref_keys - test_keys
            unexpected = test_keys - ref_keys
            
            if missing:
                errors.append(f"{file_path.name}: {section} missing fields: {', '.join(missing)}")
            if unexpected:
                errors.append(f"{file_path.name}: {section} has unexpected fields: {', '.join(unexpected)}")
            
            # For training_plans, also check plans array structure
            if section == 'training_plans':
                ref_plans = ref_section.get('plans', [])
                test_plans = test_section.get('plans', [])
                
                if ref_plans and test_plans:
                    ref_plan_keys = set(ref_plans[0].keys())
                    test_plan_keys = set(test_plans[0].keys())
                    
                    missing_plan = ref_plan_keys - test_plan_keys
                    unexpected_plan = test_plan_keys - ref_plan_keys
                    
                    if missing_plan:
                        errors.append(f"{file_path.name}: training_plans.plans[0] missing fields: {', '.join(missing_plan)}")
                    if unexpected_plan:
                        errors.append(f"{file_path.name}: training_plans.plans[0] has unexpected fields: {', '.join(unexpected_plan)}")
    
    # Check final_verdict structure specifically (common failure point)
    ref_fv = ref_race.get('final_verdict', {})
    test_fv = test_race.get('final_verdict', {})
    
    if ref_fv and test_fv:
        ref_fv_keys = set(ref_fv.keys())
        test_fv_keys = set(test_fv.keys())
        
        missing_fv = ref_fv_keys - test_fv_keys
        unexpected_fv = test_fv_keys - ref_fv_keys
        
        if missing_fv:
            errors.append(f"{file_path.name}: final_verdict missing fields: {', '.join(missing_fv)}")
        if unexpected_fv:
            errors.append(f"{file_path.name}: final_verdict has unexpected fields: {', '.join(unexpected_fv)}")
    
    # Check biased_opinion structure specifically
    ref_bo = ref_race.get('biased_opinion', {})
    test_bo = test_race.get('biased_opinion', {})
    
    if ref_bo and test_bo:
        ref_bo_keys = set(ref_bo.keys())
        test_bo_keys = set(test_bo.keys())
        
        missing_bo = ref_bo_keys - test_bo_keys
        unexpected_bo = test_bo_keys - ref_bo_keys
        
        if missing_bo:
            errors.append(f"{file_path.name}: biased_opinion missing fields: {', '.join(missing_bo)}")
        if unexpected_bo:
            errors.append(f"{file_path.name}: biased_opinion has unexpected fields: {', '.join(unexpected_bo)}")
    
    # Check training_plans structure
    ref_tp = ref_race.get('training_plans', {})
    test_tp = test_race.get('training_plans', {})
    
    if ref_tp and test_tp:
        # Check plans array structure
        ref_plans = ref_tp.get('plans', [])
        test_plans = test_tp.get('plans', [])
        
        if ref_plans and test_plans:
            # Check first plan structure
            if len(ref_plans) > 0 and len(test_plans) > 0:
                ref_plan_keys = set(ref_plans[0].keys())
                test_plan_keys = set(test_plans[0].keys())
                
                missing_plan = ref_plan_keys - test_plan_keys
                unexpected_plan = test_plan_keys - ref_plan_keys
                
                if missing_plan:
                    errors.append(f"{file_path.name}: training_plans.plans[0] missing fields: {', '.join(missing_plan)}")
                if unexpected_plan:
                    errors.append(f"{file_path.name}: training_plans.plans[0] has unexpected fields: {', '.join(unexpected_plan)}")
    
    # Check for HTML tags in content (may cause "Invalid Content In File" errors)
    import re
    def check_html_tags(obj, path=''):
        html_errors = []
        if isinstance(obj, str):
            # Check for HTML tags
            if re.search(r'<[^>]+>', obj):
                html_errors.append(f"HTML tags found at {path}")
        elif isinstance(obj, dict):
            for k, v in obj.items():
                html_errors.extend(check_html_tags(v, f"{path}.{k}" if path else k))
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                html_errors.extend(check_html_tags(item, f"{path}[{i}]"))
        return html_errors
    
    html_issues = check_html_tags(test_race)
    if html_issues:
        errors.extend([f"{file_path.name}: {issue} (may cause upload failure)" for issue in html_issues])
    
    return errors

def main():
    """Run all JSON schema regression tests."""
    data_dir = Path('data')
    
    if not data_dir.exists():
        print("ERROR: data/ directory not found")
        return 1
    
    # Use mid-south-data.json as the reference schema
    reference_file = data_dir / 'mid-south-data.json'
    
    if not reference_file.exists():
        print(f"ERROR: Reference file {reference_file} not found")
        return 1
    
    all_errors = []
    
    # Test all race data files against the reference
    for json_file in data_dir.glob('*-data.json'):
        if json_file.name == reference_file.name:
            continue  # Skip reference file itself
        
        print(f"Testing {json_file.name} against {reference_file.name}...")
        errors = test_race_data_schema(json_file, reference_file)
        all_errors.extend(errors)
    
    # Report results
    if all_errors:
        print("\n" + "="*70)
        print("JSON SCHEMA VIOLATIONS DETECTED")
        print("="*70)
        for error in all_errors:
            print(f"  ❌ {error}")
        print("\n" + "="*70)
        print(f"Total violations: {len(all_errors)}")
        print("\nThese schema mismatches will cause website import failures.")
        print("Fix the schema to match the reference (mid-south-data.json) exactly.")
        return 1
    else:
        print("\n" + "="*70)
        print("✅ ALL JSON SCHEMA TESTS PASSED")
        print("="*70)
        print("All race data files match the reference schema structure.")
        return 0

if __name__ == '__main__':
    sys.exit(main())

