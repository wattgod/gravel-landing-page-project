#!/usr/bin/env python3
"""
Validation tests for RPE (Rate of Perceived Exertion) integration in workout descriptions.
Ensures RPE 1-10 is properly included in all workout sections (WARM-UP, MAIN SET, COOL-DOWN).
"""

import sys
import re
from pathlib import Path
from xml.etree import ElementTree as ET

# Add generation_modules to path
sys.path.insert(0, str(Path(__file__).parent / "generation_modules"))

from workout_description_generator import (
    generate_workout_description,
    get_rpe_for_power,
    get_rpe_for_archetype,
    detect_archetype
)

def test_rpe_function_power_mapping():
    """Test that RPE function correctly maps power percentages to RPE ranges."""
    test_cases = [
        (0.50, "1-2"),   # Z1
        (0.65, "3-4"),   # Z2
        (0.80, "5-6"),   # Z3
        (0.90, "6-7"),   # G Spot
        (0.98, "7-8"),   # Z4
        (1.10, "9"),     # Z5
        (1.30, "10"),    # Z6
        (1.60, "10"),    # Z7
    ]
    
    failures = []
    for power_pct, expected_rpe in test_cases:
        actual_rpe = get_rpe_for_power(power_pct)
        if actual_rpe != expected_rpe:
            failures.append(f"Power {power_pct*100}% FTP: expected RPE {expected_rpe}, got {actual_rpe}")
    
    return failures

def test_rpe_in_warmup_section():
    """Test that WARM-UP section includes RPE."""
    test_blocks = """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>"""
    
    description = generate_workout_description(
        workout_name="W01 Tue - VO2max Intervals",
        blocks=test_blocks,
        week_num=1,
        level=1
    )
    
    if "WARM-UP:" not in description:
        return ["WARM-UP section missing"]
    
    if "RPE" not in description.split("WARM-UP:")[1].split("MAIN SET:")[0]:
        return ["RPE missing in WARM-UP section"]
    
    return []

def test_rpe_in_main_set_section():
    """Test that MAIN SET section includes RPE for intervals."""
    test_blocks = """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="5" OnDuration="180" OnPower="1.10" OffDuration="180" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.50" PowerHigh="0.65"/>"""
    
    description = generate_workout_description(
        workout_name="W01 Tue - VO2max Intervals",
        blocks=test_blocks,
        week_num=1,
        level=1
    )
    
    if "MAIN SET:" not in description:
        return ["MAIN SET section missing"]
    
    main_set_text = description.split("MAIN SET:")[1].split("COOL-DOWN:")[0]
    
    # Check for RPE in interval description
    if "RPE" not in main_set_text:
        return ["RPE missing in MAIN SET section"]
    
    # Check that RPE is appropriate for VO2max (should be 9)
    if "RPE 9" not in main_set_text:
        return [f"Expected RPE 9 for VO2max (110% FTP), found: {main_set_text}"]
    
    return []

def test_rpe_in_cooldown_section():
    """Test that COOL-DOWN section includes RPE."""
    test_blocks = """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <SteadyState Duration="600" Power="0.87"/>
    <Cooldown Duration="600" PowerLow="0.50" PowerHigh="0.65"/>"""
    
    description = generate_workout_description(
        workout_name="W01 Tue - Tempo",
        blocks=test_blocks,
        week_num=1,
        level=1
    )
    
    if "COOL-DOWN:" not in description:
        return ["COOL-DOWN section missing"]
    
    if "RPE" not in description.split("COOL-DOWN:")[1]:
        return ["RPE missing in COOL-DOWN section"]
    
    return []

def test_rpe_for_different_archetypes():
    """Test that different archetypes get appropriate RPE values."""
    test_cases = [
        ("W01 Tue - VO2max Intervals", "9", 1.10),  # VO2max should be RPE 9
        ("W01 Thu - Threshold Intervals", "7-8", 1.00),  # Threshold should be RPE 7-8
        ("W01 Sat - Long Endurance", "3-4", 0.70),  # Endurance should be RPE 3-4
        ("W01 Tue - G-Spot", "6-7", 0.90),  # G-Spot should be RPE 6-7
    ]
    
    failures = []
    for workout_name, expected_rpe, power_pct in test_cases:
        archetype = detect_archetype(workout_name)
        actual_rpe = get_rpe_for_archetype(archetype, power_pct)
        
        if expected_rpe not in actual_rpe and actual_rpe not in expected_rpe:
            failures.append(f"{workout_name}: expected RPE {expected_rpe}, got {actual_rpe}")
    
    return failures

def test_rpe_in_durability_workouts():
    """Test that durability workouts include RPE for Z2 and intervals."""
    # Durability workout: Z2 for 60min, then intervals
    test_blocks = """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <SteadyState Duration="3600" Power="0.70"/>
    <IntervalsT Repeat="4" OnDuration="300" OnPower="1.00" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.50" PowerHigh="0.65"/>"""
    
    description = generate_workout_description(
        workout_name="W05 Sat - Long Endurance with Intervals",
        blocks=test_blocks,
        week_num=5,
        level=3
    )
    
    failures = []
    
    # Check for Z2 RPE (should be 3-4)
    if "Z2" in description and "RPE 3-4" not in description:
        failures.append("Z2 section missing RPE 3-4 in durability workout")
    
    # Check for interval RPE (should be 7-8 for threshold)
    if "RPE" not in description:
        failures.append("RPE missing in durability workout description")
    
    return failures

def test_rpe_in_normalized_power_workouts():
    """Test that normalized power workouts include RPE."""
    test_blocks = """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <FreeRide Duration="10800" Power="0.85"/>
    <Cooldown Duration="600" PowerLow="0.50" PowerHigh="0.65"/>"""
    
    description = generate_workout_description(
        workout_name="W05 Sat - Normalized Power IF Target",
        blocks=test_blocks,
        week_num=5,
        level=3
    )
    
    if "RPE" not in description:
        return ["RPE missing in normalized power workout"]
    
    if "RPE 6-7" not in description and "RPE: 6-7" not in description:
        return ["Expected RPE 6-7 for normalized power (IF 0.85), not found"]
    
    return []

def test_rpe_in_over_under_workouts():
    """Test that over/under workouts include RPE for both under and over segments."""
    test_blocks = """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <SteadyState Duration="180" Power="0.88"/>
    <SteadyState Duration="60" Power="0.98"/>
    <SteadyState Duration="180" Power="0.88"/>
    <SteadyState Duration="60" Power="0.98"/>
    <SteadyState Duration="180" Power="0.55"/>
    <Cooldown Duration="600" PowerLow="0.50" PowerHigh="0.65"/>"""
    
    description = generate_workout_description(
        workout_name="W03 Thu - Mixed Climbing",
        blocks=test_blocks,
        week_num=3,
        level=2
    )
    
    failures = []
    
    if "RPE" not in description:
        failures.append("RPE missing in over/under workout")
    
    # Check for both under (5-6) and over (7-8) RPE
    if "RPE 5-6" not in description and "RPE 6-7" not in description:
        failures.append("Under segment RPE missing or incorrect")
    
    if "RPE 7-8" not in description:
        failures.append("Over segment RPE missing or incorrect")
    
    return failures

def test_rpe_format_consistency():
    """Test that RPE is formatted consistently across all workout types."""
    test_workouts = [
        ("W01 Tue - VO2max Intervals", """<Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="5" OnDuration="180" OnPower="1.10" OffDuration="180" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.50" PowerHigh="0.65"/>"""),
        ("W01 Thu - Threshold", """<Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <SteadyState Duration="600" Power="1.00"/>
    <Cooldown Duration="600" PowerLow="0.50" PowerHigh="0.65"/>"""),
        ("W01 Sat - Endurance", """<Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <SteadyState Duration="3600" Power="0.70"/>
    <Cooldown Duration="600" PowerLow="0.50" PowerHigh="0.65"/>"""),
    ]
    
    failures = []
    for workout_name, blocks in test_workouts:
        description = generate_workout_description(
            workout_name=workout_name,
            blocks=blocks,
            week_num=1,
            level=1
        )
        
        # Check that RPE appears in all three sections
        sections = ["WARM-UP:", "MAIN SET:", "COOL-DOWN:"]
        for section in sections:
            if section in description:
                section_text = description.split(section)[1].split("\n\n")[0]
                if "RPE" not in section_text:
                    failures.append(f"{workout_name}: RPE missing in {section}")
    
    return failures

def run_all_tests():
    """Run all RPE validation tests."""
    print("🧪 Running RPE Validation Tests...\n")
    
    tests = [
        ("RPE Power Mapping", test_rpe_function_power_mapping),
        ("RPE in WARM-UP", test_rpe_in_warmup_section),
        ("RPE in MAIN SET", test_rpe_in_main_set_section),
        ("RPE in COOL-DOWN", test_rpe_in_cooldown_section),
        ("RPE for Different Archetypes", test_rpe_for_different_archetypes),
        ("RPE in Durability Workouts", test_rpe_in_durability_workouts),
        ("RPE in Normalized Power", test_rpe_in_normalized_power_workouts),
        ("RPE in Over/Under", test_rpe_in_over_under_workouts),
        ("RPE Format Consistency", test_rpe_format_consistency),
    ]
    
    total_tests = len(tests)
    passed = 0
    failed = 0
    all_failures = []
    
    for test_name, test_func in tests:
        try:
            failures = test_func()
            if failures:
                print(f"❌ {test_name}: {len(failures)} failure(s)")
                for failure in failures:
                    print(f"   - {failure}")
                    all_failures.append(f"{test_name}: {failure}")
                failed += 1
            else:
                print(f"✅ {test_name}: PASSED")
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            all_failures.append(f"{test_name}: {e}")
            failed += 1
    
    print(f"\n📊 Results: {passed}/{total_tests} tests passed")
    
    if all_failures:
        print(f"\n❌ {len(all_failures)} failure(s) detected:")
        for failure in all_failures[:10]:  # Show first 10
            print(f"   - {failure}")
        if len(all_failures) > 10:
            print(f"   ... and {len(all_failures) - 10} more")
        return False
    
    print("\n✅ All RPE validation tests passed!")
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

