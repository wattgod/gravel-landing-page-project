#!/usr/bin/env python3
"""
Validation Tests for Expanded Unbound 200 Plans
Tests FTP test integration, durability tests, plan structure
"""

import os
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

# Add generation modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generation_modules'))

def test_ftp_test_presence(plan_dir, expected_weeks):
    """Test that FTP tests are present at expected weeks"""
    workouts_dir = plan_dir / "workouts"
    if not workouts_dir.exists():
        return False, f"Workouts directory not found: {workouts_dir}"
    
    errors = []
    for week in expected_weeks:
        ftp_files = list(workouts_dir.glob(f"W{week:02d}*FTP*.zwo"))
        if not ftp_files:
            errors.append(f"Missing FTP test for week {week}")
    
    if errors:
        return False, "; ".join(errors)
    return True, "All FTP tests present"

def test_durability_test_presence(plan_dir, expected_weeks, tier):
    """Test that durability tests are present at expected weeks"""
    workouts_dir = plan_dir / "workouts"
    if not workouts_dir.exists():
        return False, f"Workouts directory not found: {workouts_dir}"
    
    errors = []
    for week in expected_weeks:
        durability_files = list(workouts_dir.glob(f"W{week:02d}*Durability*.zwo"))
        if not durability_files:
            errors.append(f"Missing durability test for week {week}")
    
    if errors:
        return False, "; ".join(errors)
    return True, "All durability tests present"

def test_workout_count(plan_dir, expected_count):
    """Test that workout count matches expected duration"""
    workouts_dir = plan_dir / "workouts"
    if not workouts_dir.exists():
        return False, f"Workouts directory not found: {workouts_dir}"
    
    zwo_files = list(workouts_dir.glob("*.zwo"))
    actual_count = len(zwo_files)
    
    # Allow some variance (race day workout, etc.)
    if abs(actual_count - expected_count) > 5:
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
        
        # Check required elements
        if root.tag != 'workout_file':
            return False, f"Invalid root tag: {root.tag}"
        
        name_elem = root.find('name')
        if name_elem is None:
            return False, "Missing <name> element"
        
        workout_elem = root.find('workout')
        if workout_elem is None:
            return False, "Missing <workout> element"
        
        return True, "Valid ZWO structure"
    except ET.ParseError as e:
        return False, f"XML parse error: {e}"

def validate_plan(plan_dir, duration, tier):
    """Validate a single plan"""
    plan_name = plan_dir.name
    print(f"\n📋 Validating: {plan_name}")
    
    results = []
    
    # Determine expected test weeks
    if duration == 12:
        ftp_weeks = [1, 7]
        durability_weeks = [7]
    elif duration == 16:
        ftp_weeks = [1, 7, 13]
        durability_weeks = [7, 13]
    else:  # 20 weeks
        ftp_weeks = [1, 7, 13, 19]
        durability_weeks = [7, 13, 19]
    
    # Expected workout count (7 workouts/week * duration)
    expected_workouts = 7 * duration
    
    # Test FTP tests
    passed, msg = test_ftp_test_presence(plan_dir, ftp_weeks)
    results.append(("FTP Tests", passed, msg))
    
    # Test durability tests
    passed, msg = test_durability_test_presence(plan_dir, durability_weeks, tier)
    results.append(("Durability Tests", passed, msg))
    
    # Test workout count
    passed, msg = test_workout_count(plan_dir, expected_workouts)
    results.append(("Workout Count", passed, msg))
    
    # Test guide
    passed, msg = test_guide_exists(plan_dir)
    results.append(("Training Guide", passed, msg))
    
    # Test sample ZWO file
    workouts_dir = plan_dir / "workouts"
    if workouts_dir.exists():
        zwo_files = list(workouts_dir.glob("*.zwo"))
        if zwo_files:
            passed, msg = test_zwo_structure(zwo_files[0])
            results.append(("ZWO Structure", passed, msg))
    
    # Print results
    all_passed = all(r[1] for r in results)
    for test_name, passed, msg in results:
        status = "✅" if passed else "❌"
        print(f"  {status} {test_name}: {msg}")
    
    return all_passed

def main():
    """Run validation tests on Unbound 200 plans"""
    base_path = Path(__file__).parent
    unbound_dir = base_path / "Unbound Gravel 200"
    
    if not unbound_dir.exists():
        print(f"❌ Unbound Gravel 200 directory not found: {unbound_dir}")
        return 1
    
    # Find all plan directories
    plan_dirs = [d for d in unbound_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    print(f"🔍 Found {len(plan_dirs)} plans to validate")
    
    # Validate a sample of plans
    sample_plans = [
        ("1. 1. Time Crunched Standard (12 weeks)", 12, "ayahuasca"),
        ("1. 1. Time Crunched Standard (20 weeks)", 20, "ayahuasca"),
        ("3. Compete Standard (16 weeks)", 16, "compete"),
        ("5. 5. Podium Standard (20 weeks)", 20, "podium"),
    ]
    
    all_passed = True
    for plan_name, duration, tier in sample_plans:
        plan_dir = unbound_dir / plan_name
        if plan_dir.exists():
            passed = validate_plan(plan_dir, duration, tier)
            all_passed = all_passed and passed
        else:
            print(f"⚠️  Plan not found: {plan_name}")
    
    if all_passed:
        print("\n✅ All validation tests passed!")
        return 0
    else:
        print("\n❌ Some validation tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())

