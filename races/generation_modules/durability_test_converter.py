#!/usr/bin/env python3
"""
Durability Test Converter
Converts durability test workouts to GG format
Tests: 2hr, 3hr, 4hr @ 0.8 FTP (top of Z2/bottom of Z3)
"""

import xml.etree.ElementTree as ET
from pathlib import Path

def convert_durability_test(durability_test_path, week_num, test_name="Durability Test"):
    """
    Convert durability test from TrainingPeaks format to GG format
    
    Args:
        durability_test_path: Path to durability test ZWO file
        week_num: Week number for naming
        test_name: Name of the test (e.g., "Metabolism 1", "Aerobic Endurance")
    
    Returns:
        dict with 'name', 'description', 'blocks' for GG format
    """
    try:
        tree = ET.parse(durability_test_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Error loading durability test: {e}")
        return None
    
    # Extract workout blocks
    workout_elem = root.find('workout')
    if workout_elem is None:
        return None
    
    blocks = []
    main_duration = 0
    
    # Convert to GG format
    for child in workout_elem:
        if child.tag == 'Warmup':
            duration = int(child.get('Duration', 0))
            power_low = child.get('PowerLow', '0.55')
            power_high = child.get('PowerHigh', '0.75')
            blocks.append(f'    <Warmup Duration="{duration}" PowerLow="{power_low}" PowerHigh="{power_high}"/>\n')
        elif child.tag == 'SteadyState':
            duration = int(child.get('Duration', 0))
            power = child.get('Power', '0.80')
            main_duration = duration
            # Add cadence for steady state
            blocks.append(f'    <SteadyState Duration="{duration}" Power="{power}" CadenceLow="85" CadenceHigh="95"/>\n')
        elif child.tag == 'Cooldown':
            duration = int(child.get('Duration', 0))
            power_low = child.get('PowerLow', '0.50')
            power_high = child.get('PowerHigh', '0.70')
            blocks.append(f'    <Cooldown Duration="{duration}" PowerLow="{power_low}" PowerHigh="{power_high}"/>\n')
        else:
            # Keep other elements as-is
            tag = child.tag
            attrs = ' '.join([f'{k}="{v}"' for k, v in child.attrib.items()])
            blocks.append(f'    <{tag} {attrs}/>\n')
    
    blocks_str = "".join(blocks)
    
    # Calculate hours from duration (seconds)
    hours = main_duration / 3600
    
    # Create GG-formatted description
    description = f"""WARM-UP:
• 10-15min building from Z1 to top of Z2/bottom of Z3. Get the legs moving - don't just jump into it.

MAIN SET:
• {hours:.0f} hours @ 0.80 FTP (top of Z2/bottom of Z3). Steady on the gas. This is NOT an all-out time trial. You should feel at the top end of endurance and the bottom end of tempo - mentally you have to stay engaged but RPE should be 6/10 to start and grow towards the end.

COOL-DOWN:
• 10min easy spin Z1-Z2

PURPOSE:
Durability Assessment - HR Decoupling Test. Looking for where HR decouples so we can see where aerobic fitness is. This test measures your ability to sustain steady power over extended duration. The goal is to hold steady power while monitoring heart rate drift.

EXECUTION:
• PACING: Start at RPE 6/10. Power should feel sustainable but require mental engagement. RPE will grow toward the end - that's expected.
• FUELING: You MUST eat and drink every 30 minutes - you're burning LOTS of calories. This is non-negotiable. Practice your race fueling strategy.
• MINIMIZE STOPS: Rest invalidates the decoupling data. Plan your route to avoid stoplights and intersections.
• HR MONITORING: Watch for HR drift. If HR climbs significantly while power stays steady, that's decoupling - it shows your aerobic fitness limit.
• TERRAIN: Flat or rolling terrain preferred. Avoid big climbs that would force power changes."""
    
    return {
        "name": f"W{week_num:02d} - {test_name}",
        "description": description,
        "blocks": blocks_str,
        "week_number": week_num,
        "duration_hours": hours
    }

def select_durability_test(week_num, plan_weeks, tier):
    """
    Select appropriate durability test based on progression and tier
    
    Args:
        week_num: Current week number
        plan_weeks: Total weeks in plan (12, 16, 20)
        tier: Plan tier (ayahuasca, finisher, compete, podium)
    
    Returns:
        tuple: (test_path, test_name) or (None, None) if no test
    """
    # Test schedule: Later weeks get longer tests
    # Week 1: FTP test (handled separately)
    # Week 7: 2hr test (Metabolism 1)
    # Week 13: 3hr test (Aerobic Endurance) 
    # Week 19: 4hr test (Metabolism 3) - only for 20-week plans
    
    # Base paths
    base_path = Path("/Users/mattirowe/Downloads")
    
    # Determine test based on week and tier
    if week_num == 7:
        # Early progression: 2hr test for all tiers
        test_path = base_path / "2026-01-05_TheAssessm.zwo"  # Metabolism 1 (2hr)
        test_name = "Durability Test - Metabolism 1"
        return test_path, test_name
    
    elif week_num == 13:
        # Mid progression: 3hr test for most, 4hr for higher tiers
        if tier in ["compete", "podium"]:
            test_path = base_path / "2026-01-07_TheAssessm.zwo"  # Metabolism 3 (4hr)
            test_name = "Durability Test - Metabolism 3"
        else:
            test_path = base_path / "2026-01-06_TheAssessm.zwo"  # Aerobic Endurance (3hr)
            test_name = "Durability Test - Aerobic Endurance"
        return test_path, test_name
    
    elif week_num == 19:
        # Late progression: 4hr test for all (only 20-week plans)
        if plan_weeks == 20:
            test_path = base_path / "2026-01-07_TheAssessm.zwo"  # Metabolism 3 (4hr)
            test_name = "Durability Test - Metabolism 3"
            return test_path, test_name
    
    return None, None

if __name__ == "__main__":
    # Test conversion
    test_path = Path("/Users/mattirowe/Downloads/2026-01-06_TheAssessm.zwo")
    if test_path.exists():
        result = convert_durability_test(test_path, 13, "Aerobic Endurance")
        if result:
            print("✅ Durability Test Conversion Successful")
            print(f"Name: {result['name']}")
            print(f"Duration: {result['duration_hours']} hours")
            print(f"Blocks length: {len(result['blocks'])} chars")
        else:
            print("❌ Conversion failed")
    else:
        print(f"⚠️  Test file not found: {test_path}")

