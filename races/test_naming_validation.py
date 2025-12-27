#!/usr/bin/env python3
"""
Validation Test: Naming Conventions
Ensures no "Ayahuasca" or "GOAT" references in generated files
"""

import os
import sys
from pathlib import Path
import re

# Forbidden terms
FORBIDDEN_TERMS = {
    "Ayahuasca": "Should be 'Time Crunched'",
    "ayahuasca": "Should be 'time crunched' or 'Time Crunched'",
    "AYAHUASCA": "Should be 'TIME CRUNCHED'",
    "GOAT": "Should be removed - no longer used",
    "goat": "Should be removed - no longer used",
    "Goat": "Should be removed - no longer used"
}

# Allowed contexts (where these terms might appear in comments or old files)
ALLOWED_CONTEXTS = [
    "source_plans",  # Old plan names in source references
    "comment",  # Code comments
    "template",  # Template files
]

def check_file_for_forbidden_terms(file_path):
    """Check a single file for forbidden terms"""
    errors = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for term, message in FORBIDDEN_TERMS.items():
                    if term in line:
                        # Check if it's in an allowed context
                        is_allowed = any(context in str(file_path).lower() for context in ALLOWED_CONTEXTS)
                        
                        if not is_allowed:
                            errors.append({
                                'file': str(file_path),
                                'line': line_num,
                                'term': term,
                                'message': message,
                                'context': line.strip()[:100]
                            })
    except Exception as e:
        errors.append({
            'file': str(file_path),
            'line': 0,
            'term': 'ERROR',
            'message': f"Could not read file: {e}",
            'context': ''
        })
    
    return errors

def validate_plan_directory(plan_dir):
    """Validate all files in a plan directory"""
    all_errors = []
    
    # Check guide files
    for guide_file in plan_dir.glob("*guide.html"):
        errors = check_file_for_forbidden_terms(guide_file)
        all_errors.extend(errors)
    
    # Check ZWO files
    workouts_dir = plan_dir / "workouts"
    if workouts_dir.exists():
        for zwo_file in workouts_dir.glob("*.zwo"):
            errors = check_file_for_forbidden_terms(zwo_file)
            all_errors.extend(errors)
    
    # Check marketplace description
    for marketplace_file in plan_dir.glob("marketplace*.html"):
        errors = check_file_for_forbidden_terms(marketplace_file)
        all_errors.extend(errors)
    
    return all_errors

def main():
    """Run naming validation tests"""
    base_path = Path(__file__).parent
    unbound_dir = base_path / "Unbound Gravel 200"
    
    if not unbound_dir.exists():
        print(f"❌ Unbound Gravel 200 directory not found: {unbound_dir}")
        return 1
    
    print("🔍 Validating naming conventions...")
    print(f"   Checking for: {', '.join(FORBIDDEN_TERMS.keys())}\n")
    
    all_errors = []
    plan_dirs = [d for d in unbound_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    for plan_dir in plan_dirs:
        errors = validate_plan_directory(plan_dir)
        if errors:
            all_errors.extend(errors)
            print(f"❌ {plan_dir.name}: {len(errors)} violations found")
        else:
            print(f"✅ {plan_dir.name}: No violations")
    
    if all_errors:
        print(f"\n❌ Found {len(all_errors)} naming violations:\n")
        
        # Group by term
        by_term = {}
        for error in all_errors:
            term = error['term']
            if term not in by_term:
                by_term[term] = []
            by_term[term].append(error)
        
        for term, errors in by_term.items():
            print(f"\n{term} ({len(errors)} occurrences):")
            for error in errors[:10]:  # Show first 10
                print(f"  {error['file']}:{error['line']} - {error['context']}")
            if len(errors) > 10:
                print(f"  ... and {len(errors) - 10} more")
        
        return 1
    else:
        print("\n✅ All naming conventions validated!")
        return 0

if __name__ == "__main__":
    sys.exit(main())

