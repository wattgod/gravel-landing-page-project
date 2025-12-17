#!/usr/bin/env python3
"""
Regression test for race workout generation
Ensures race workouts are created for all plans with correct content
"""

import json
from pathlib import Path
import sys

# Add races directory to path
sys.path.insert(0, str(Path(__file__).parent / "races" / "generation_modules"))

def test_race_workout_exists(race_folder):
    """Test that race workout exists for each plan"""
    race_folder = Path(race_folder)
    errors = []
    
    # Find all plan folders
    plan_folders = [d for d in race_folder.iterdir() if d.is_dir() and d.name[0].isdigit()]
    
    if not plan_folders:
        return [f"❌ No plan folders found in {race_folder}"]
    
    for plan_folder in sorted(plan_folders):
        workouts_dir = plan_folder / "workouts"
        if not workouts_dir.exists():
            errors.append(f"❌ {plan_folder.name}: workouts directory missing")
            continue
        
        # Look for race workout file
        race_files = list(workouts_dir.glob("RACE_DAY_*.zwo"))
        if not race_files:
            errors.append(f"❌ {plan_folder.name}: Race workout file missing")
            continue
        
        if len(race_files) > 1:
            errors.append(f"⚠️  {plan_folder.name}: Multiple race workout files found: {[f.name for f in race_files]}")
        
        # Check file content
        race_file = race_files[0]
        content = race_file.read_text(encoding='utf-8')
        
        # Must contain key elements
        checks = [
            ("RACE DAY", "Race day header"),
            ("PRE-RACE CHECKLIST", "Pre-race checklist"),
            ("RACE TACTICS", "Race tactics section"),
            ("PACING", "Pacing framework"),
            ("FUELING", "Fueling instructions"),
            ("RESOURCES IN YOUR GUIDE", "Guide resources reference"),
            ("Estimated completion time", "Time estimate"),
            ("Distance:", "Distance info"),
            ("Elevation:", "Elevation info"),
        ]
        
        # Must have structured workout blocks (not just FreeRide)
        if "<FreeRide" in content and "SteadyState" not in content:
            errors.append(f"❌ {plan_folder.name}: Race workout uses FreeRide instead of structured blocks")
        
        # Must have Warmup, SteadyState, and Cooldown blocks
        if "<Warmup" not in content:
            errors.append(f"❌ {plan_folder.name}: Missing Warmup block in race workout")
        if "<SteadyState" not in content:
            errors.append(f"❌ {plan_folder.name}: Missing SteadyState blocks in race workout")
        if "<Cooldown" not in content:
            errors.append(f"❌ {plan_folder.name}: Missing Cooldown block in race workout")
        
        for check_text, check_name in checks:
            if check_text not in content:
                errors.append(f"❌ {plan_folder.name}: Missing '{check_name}' in race workout")
    
    return errors

def test_race_workout_times(race_json_path):
    """Test that race time estimates are reasonable"""
    race_data = json.load(open(race_json_path))
    distance = race_data.get("race_metadata", {}).get("distance_miles", 100)
    
    from zwo_generator import estimate_race_time_hours
    
    # Test key combinations
    test_cases = [
        ("finisher", "beginner", distance * 0.06, distance * 0.10),  # 6-10 hours per 100 miles
        ("compete", "intermediate", distance * 0.05, distance * 0.08),  # 5-8 hours per 100 miles
        ("podium", "advanced", distance * 0.04, distance * 0.06),  # 4-6 hours per 100 miles
    ]
    
    errors = []
    for tier, level, min_hours, max_hours in test_cases:
        time_hours = estimate_race_time_hours(race_data, tier, level)
        if time_hours < min_hours or time_hours > max_hours:
            errors.append(
                f"❌ {tier} {level}: Time estimate {time_hours:.1f}h outside reasonable range "
                f"({min_hours:.1f}-{max_hours:.1f}h for {distance} miles)"
            )
    
    return errors

if __name__ == "__main__":
    print("=" * 80)
    print("RACE WORKOUT REGRESSION TEST")
    print("=" * 80)
    
    all_errors = []
    
    # Test Mid South
    print("\n🔍 Testing Mid South race workouts...")
    mid_south_folder = Path(__file__).parent / "races" / "Mid South"
    if mid_south_folder.exists():
        errors = test_race_workout_exists(mid_south_folder)
        all_errors.extend(errors)
        if not errors:
            print("  ✓ All Mid South race workouts present and valid")
    else:
        print("  ⚠️  Mid South folder not found")
    
    # Test time estimates
    print("\n🔍 Testing race time estimates...")
    mid_south_json = Path(__file__).parent / "races" / "mid_south.json"
    if mid_south_json.exists():
        errors = test_race_workout_times(mid_south_json)
        all_errors.extend(errors)
        if not errors:
            print("  ✓ Race time estimates are reasonable")
    
    # Summary
    print("\n" + "=" * 80)
    if all_errors:
        print(f"❌ FAILED: {len(all_errors)} error(s) found")
        for error in all_errors:
            print(f"  {error}")
        sys.exit(1)
    else:
        print("✅ All race workout tests passed")
        sys.exit(0)
