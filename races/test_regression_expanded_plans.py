#!/usr/bin/env python3
"""
Regression Tests for Expanded Plans
Validates:
- Plan structure (5 tiers × 3 durations = 15 plans)
- Tier hours are correct
- Naming conventions (no Ayahuasca, no GOAT)
- FTP test integration
- Durability test integration
- Workout counts match durations
- Guides exist
"""

import os
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

# Expected values
EXPECTED_TIERS = {
    "Time Crunched": "0-5 hrs/week",
    "Finisher": "8-10 hrs/week",
    "Compete": "12-17 hrs/week",
    "Compete Masters": "12-17 hrs/week",
    "Podium": "18-25 hrs/week"
}

EXPECTED_DURATIONS = [12, 16, 20]
EXPECTED_PLAN_COUNT = 15  # 5 tiers × 3 durations

FORBIDDEN_TERMS = ["Ayahuasca", "ayahuasca", "AYAHUASCA", "GOAT", "goat", "Goat"]

def test_plan_count(plan_dir):
    """Test that we have exactly 15 Standard plans"""
    standard_plans = list(plan_dir.glob("*Standard*"))
    count = len([p for p in standard_plans if p.is_dir()])
    
    if count == EXPECTED_PLAN_COUNT:
        return True, f"Correct plan count: {count}"
    else:
        return False, f"Expected {EXPECTED_PLAN_COUNT} plans, found {count}"

def test_tier_hours_in_guides(plan_dir):
    """Test that guides have correct tier hours"""
    errors = []
    
    for guide_file in plan_dir.rglob("*guide.html"):
        try:
            with open(guide_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check for correct hours - be flexible with format
                for tier, hours in EXPECTED_TIERS.items():
                    if tier in guide_file.name or tier.upper() in content:
                        # Extract hour range (e.g., "12-17" from "12-17 hrs/week" or "12-17 hours")
                        hour_range = hours.split()[0]  # Get "12-17" from "12-17 hrs/week"
                        # Check if hour range appears in content (flexible format)
                        if hour_range not in content:
                            errors.append(f"{guide_file.name}: Missing correct hours ({hour_range}) for {tier}")
        except Exception as e:
            errors.append(f"{guide_file.name}: Error reading - {e}")
    
    if errors:
        return False, f"Found {len(errors)} hour mismatches"
    return True, "All guides have correct tier hours"

def test_naming_conventions(plan_dir):
    """Test that no forbidden terms appear"""
    violations = []
    
    for file_path in plan_dir.rglob("*"):
        if file_path.is_file() and (file_path.suffix in ['.html', '.zwo', '.md']):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    for line_num, line in enumerate(lines, 1):
                        for term in FORBIDDEN_TERMS:
                            if term in line:
                                # Skip if in allowed context (comments, old file references)
                                if "source_plans" not in str(file_path) and "comment" not in str(file_path).lower():
                                    violations.append({
                                        'file': str(file_path.relative_to(plan_dir)),
                                        'line': line_num,
                                        'term': term
                                    })
            except Exception:
                pass  # Skip binary or unreadable files
    
    if violations:
        return False, f"Found {len(violations)} naming violations"
    return True, "All naming conventions validated"

def test_ftp_tests(plan_dir, duration):
    """Test that FTP tests are present at correct weeks"""
    if duration == 12:
        expected_weeks = [1, 7]
    elif duration == 16:
        expected_weeks = [1, 7, 13]
    else:  # 20 weeks
        expected_weeks = [1, 7, 13, 19]
    
    workouts_dir = plan_dir / "workouts"
    if not workouts_dir.exists():
        return False, "Workouts directory not found"
    
    errors = []
    for week in expected_weeks:
        ftp_files = list(workouts_dir.glob(f"W{week:02d}*FTP*.zwo"))
        if not ftp_files:
            errors.append(f"Missing FTP test for week {week}")
    
    if errors:
        return False, "; ".join(errors)
    return True, f"All FTP tests present for {duration}-week plan"

def test_durability_tests(plan_dir, duration, tier):
    """Test that durability tests are present at correct weeks"""
    if duration == 12:
        expected_weeks = [7]
    elif duration == 16:
        expected_weeks = [7, 13]
    else:  # 20 weeks
        expected_weeks = [7, 13, 19]
    
    workouts_dir = plan_dir / "workouts"
    if not workouts_dir.exists():
        return False, "Workouts directory not found"
    
    errors = []
    for week in expected_weeks:
        durability_files = list(workouts_dir.glob(f"W{week:02d}*Durability*.zwo"))
        if not durability_files:
            errors.append(f"Missing durability test for week {week}")
    
    if errors:
        return False, "; ".join(errors)
    return True, f"All durability tests present for {duration}-week {tier} plan"

def test_workout_count(plan_dir, duration):
    """Test that workout count matches duration"""
    workouts_dir = plan_dir / "workouts"
    if not workouts_dir.exists():
        return False, "Workouts directory not found"
    
    zwo_files = list(workouts_dir.glob("*.zwo"))
    actual_count = len(zwo_files)
    
    # Expected: ~7 workouts/week × duration + race day
    expected_count = 7 * duration + 1
    
    # Allow some variance (FTP tests, durability tests might add/subtract)
    if abs(actual_count - expected_count) > 10:
        return False, f"Expected ~{expected_count} workouts, found {actual_count}"
    return True, f"Workout count correct: {actual_count}"

def test_guide_exists(plan_dir):
    """Test that training guide exists"""
    guide_files = list(plan_dir.glob("*guide.html"))
    if not guide_files:
        return False, "Training guide not found"
    return True, f"Guide found: {guide_files[0].name}"

def test_zwo_structure(zwo_file):
    """Test that ZWO file has valid XML structure"""
    try:
        tree = ET.parse(zwo_file)
        root = tree.getroot()
        
        if root.tag != 'workout_file':
            return False, f"Invalid root tag: {root.tag}"
        
        if root.find('name') is None:
            return False, "Missing <name> element"
        
        if root.find('workout') is None:
            return False, "Missing <workout> element"
        
        return True, "Valid ZWO structure"
    except ET.ParseError as e:
        return False, f"XML parse error: {e}"

def main():
    """Run all regression tests"""
    base_path = Path(__file__).parent
    unbound_dir = base_path / "Unbound Gravel 200"
    
    if not unbound_dir.exists():
        print(f"❌ Unbound Gravel 200 directory not found: {unbound_dir}")
        return 1
    
    print("🔍 Running Regression Tests for Expanded Plans\n")
    
    all_passed = True
    results = []
    
    # Test 1: Plan count
    print("1. Testing plan count...")
    passed, msg = test_plan_count(unbound_dir)
    results.append(("Plan Count", passed, msg))
    print(f"   {'✅' if passed else '❌'} {msg}")
    all_passed = all_passed and passed
    
    # Test 2: Tier hours in guides
    print("\n2. Testing tier hours in guides...")
    passed, msg = test_tier_hours_in_guides(unbound_dir)
    results.append(("Tier Hours", passed, msg))
    print(f"   {'✅' if passed else '❌'} {msg}")
    all_passed = all_passed and passed
    
    # Test 3: Naming conventions
    print("\n3. Testing naming conventions...")
    passed, msg = test_naming_conventions(unbound_dir)
    results.append(("Naming Conventions", passed, msg))
    print(f"   {'✅' if passed else '❌'} {msg}")
    all_passed = all_passed and passed
    
    # Test 4-6: Sample plan validation
    print("\n4. Testing sample plans...")
    sample_plans = [
        ("1. 1. Time Crunched Standard (12 weeks)", 12, "time_crunched"),
        ("3. 3. Compete Standard (20 weeks)", 20, "compete"),
        ("5. 5. Podium Standard (16 weeks)", 16, "podium"),
    ]
    
    for plan_name, duration, tier in sample_plans:
        plan_dir = unbound_dir / plan_name
        if plan_dir.exists():
            print(f"\n   Testing: {plan_name}")
            
            # FTP tests
            passed, msg = test_ftp_tests(plan_dir, duration)
            results.append((f"{plan_name} - FTP Tests", passed, msg))
            print(f"     {'✅' if passed else '❌'} FTP Tests: {msg}")
            all_passed = all_passed and passed
            
            # Durability tests
            passed, msg = test_durability_tests(plan_dir, duration, tier)
            results.append((f"{plan_name} - Durability Tests", passed, msg))
            print(f"     {'✅' if passed else '❌'} Durability Tests: {msg}")
            all_passed = all_passed and passed
            
            # Workout count
            passed, msg = test_workout_count(plan_dir, duration)
            results.append((f"{plan_name} - Workout Count", passed, msg))
            print(f"     {'✅' if passed else '❌'} Workout Count: {msg}")
            all_passed = all_passed and passed
            
            # Guide
            passed, msg = test_guide_exists(plan_dir)
            results.append((f"{plan_name} - Guide", passed, msg))
            print(f"     {'✅' if passed else '❌'} Guide: {msg}")
            all_passed = all_passed and passed
    
    # Summary
    print("\n" + "="*60)
    passed_count = sum(1 for _, p, _ in results if p)
    total_count = len(results)
    print(f"Results: {passed_count}/{total_count} tests passed")
    
    if all_passed:
        print("✅ All regression tests passed!")
        return 0
    else:
        print("❌ Some regression tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())

