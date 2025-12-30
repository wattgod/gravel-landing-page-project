#!/usr/bin/env python3
"""
EXPANDED PLAN GENERATOR FOR UNBOUND 200
Generates training plans with multiple durations and variations:
- 5 plan types (Time Crunched, Finisher, Compete, Compete Masters, Podium)
- 3 durations (12, 16, 20 weeks)
- 3-5 variations per plan
- FTP test integration for 20-week plans (every 6 weeks)
- Matching guides for each plan length

Usage:
    python generate_expanded_race_plans.py unbound_gravel_200.json
"""

import json
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET

# Import generation modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generation_modules'))
import subprocess
try:
    from zwo_generator import generate_all_zwo_files, create_zwo_file
    from marketplace_generator import generate_marketplace_html
except ImportError as e:
    print(f"ERROR: Could not import required generation modules: {e}")
    sys.exit(1)

# PLAN TYPES
PLAN_TYPES = {
    "1. Time Crunched": {
        "tier": "ayahuasca",
        "level": "beginner",
        "target_hours": "0-5 hrs/week",
        "goal": "Finish the race",
        "philosophy": "HIIT-Focused (Survival Mode)",
        "source_plans": [
            "1. Ayahuasca Beginner (12 weeks)",
            "2. Ayahuasca Intermediate (12 weeks)"
        ]
    },
    "2. Finisher": {
        "tier": "finisher",
        "level": "beginner",
        "target_hours": "8-10 hrs/week",
        "goal": "Finish confidently, learn proper training",
        "philosophy": "Traditional Pyramidal",
        "source_plans": [
            "5. Finisher Beginner (12 weeks)",
            "6. Finisher Intermediate (12 weeks)"
        ]
    },
    "3. Compete": {
        "tier": "compete",
        "level": "intermediate",
        "target_hours": "12-17 hrs/week",
        "goal": "Competitive finish, race for position",
        "philosophy": "Polarized Training",
        "source_plans": [
            "10. Compete Intermediate (12 weeks)",
            "11. Compete Advanced (12 weeks)"
        ]
    },
    "4. Compete Masters": {
        "tier": "compete",
        "level": "masters",
        "target_hours": "12-17 hrs/week",
        "goal": "Age-group competitive",
        "philosophy": "Masters-optimized Polarized Training",
        "source_plans": [
            "3. Ayahuasca Masters (12 weeks)",
            "8. Finisher Masters (12 weeks)",
            "12. Compete Masters (12 weeks)"
        ]
    },
    "5. Podium": {
        "tier": "podium",
        "level": "advanced",
        "target_hours": "18-25 hrs/week",
        "goal": "Race to win, podium finish",
        "philosophy": "High-volume, race-specific preparation",
        "source_plans": [
            "14. Podium Advanced (12 weeks)",
            "15. Podium Advanced GOAT (12 weeks)"
        ]
    }
}

# DURATIONS
DURATIONS = [12, 16, 20]

# VARIATIONS (Standard only - no variations)
VARIATIONS = {
    "variation_1": {"name": "Standard", "description": "Standard progression"}
}

# FTP TEST CONFIGURATION (for 20-week plans)
FTP_TEST_WEEKS_20 = [1, 7, 13, 19]  # Every ~6 weeks
FTP_TEST_WEEKS_16 = [1, 7, 13]  # Every ~6 weeks
FTP_TEST_WEEKS_12 = [1, 7]  # Every ~6 weeks

def load_ftp_test_template(ftp_test_path):
    """Load the FTP test workout template - return path for converter"""
    if not os.path.exists(ftp_test_path):
        print(f"⚠️  FTP test template not found: {ftp_test_path}")
        return None
    return ftp_test_path  # Return path, converter will handle parsing

def convert_ftp_test_to_gg_format(ftp_test_root, week_num):
    """Convert the FTP test workout to GG format"""
    # Extract description
    desc_elem = ftp_test_root.find('description')
    description = desc_elem.text if desc_elem is not None else ""
    
    # Extract workout blocks
    workout_elem = ftp_test_root.find('workout')
    blocks = []
    if workout_elem is not None:
        for child in workout_elem:
            # Convert FreeRide with textevents to proper structure
            if child.tag == 'FreeRide':
                duration = int(child.get('Duration', 0))
                # Check for textevents to determine power
                textevents = child.findall('textevent')
                if textevents:
                    rpe = textevents[0].get('message', '').replace('RPE ', '')
                    # Convert RPE to power zones (approximate)
                    rpe_power_map = {
                        '2': 0.50, '3': 0.55, '4': 0.60, '5': 0.65,
                        '6': 0.75, '7': 0.85, '8': 1.00, '9': 1.10, '10': 1.20
                    }
                    power = rpe_power_map.get(rpe, 0.60)
                    blocks.append(f'    <SteadyState Duration="{duration}" Power="{power:.2f}"/>\n')
                else:
                    blocks.append(f'    <FreeRide Duration="{duration}"/>\n')
            else:
                # Keep other elements as-is
                tag = child.tag
                attrs = ' '.join([f'{k}="{v}"' for k, v in child.attrib.items()])
                blocks.append(f'    <{tag} {attrs}/>\n')
    
    blocks_str = "".join(blocks)
    
    # Create GG-formatted description
    gg_description = f"""WARM-UP:
• 12min progressive warmup building from Z1 to Z2

MAIN SET:
• 5min @ RPE 6/10 (moderate effort)
• 5min @ RPE 2 (easy recovery)
• 5min ALL OUT (RPE 8-10). Go as hard as you can. Start firm but hard for first 2min, then adjust effort up or down.
• 5min @ RPE 2 (easy recovery)
• 20min ALL OUT. Start conservatively at RPE 8/10 - 20 minutes is a LONG time. This sets your FTP.

COOL-DOWN:
• 10min easy spin Z1-Z2

PURPOSE:
FTP Assessment. This test sets your training zones for the next 6 weeks. Accurate testing = accurate training zones. Write down your average power for the 20-minute effort, multiply by 0.95. That's your FTP.

• UNBOUND GRAVEL 200 - FTP TEST PROTOCOL:
You'll want the terrain to be unbroken flat or slightly uphill - you don't want to get caught at a stop light or intersection in the middle of your effort. Do this test when fresh (not after a hard week)."""
    
    return {
        "name": f"W{week_num:02d} - FTP Test",
        "description": gg_description,
        "blocks": blocks_str
    }

def should_insert_ftp_test(week_num, plan_weeks):
    """Determine if FTP test should be inserted this week"""
    if plan_weeks == 20:
        return week_num in FTP_TEST_WEEKS_20
    elif plan_weeks == 16:
        return week_num in FTP_TEST_WEEKS_16
    elif plan_weeks == 12:
        return week_num in FTP_TEST_WEEKS_12
    return False

def load_race_data(race_json_path):
    """Load race-specific data from JSON file"""
    with open(race_json_path, 'r') as f:
        return json.load(f)

def load_plan_template(plan_folder_name):
    """Load plan template JSON from old structure"""
    # Try multiple possible paths
    possible_paths = [
        Path(__file__).parent.parent / "plans" / plan_folder_name / "template.json",
        Path(__file__).parent / "plans" / plan_folder_name / "template.json",
        Path(__file__).parent.parent.parent / "plans" / plan_folder_name / "template.json"
    ]
    
    for template_path in possible_paths:
        if template_path.exists():
            with open(template_path, 'r') as f:
                return json.load(f)
    
    print(f"⚠️  Template not found: {plan_folder_name}")
    return None

def extend_plan_template(base_template, target_weeks, ftp_test_template=None):
    """Extend a 12-week plan template to 16 or 20 weeks"""
    if target_weeks == 12:
        return base_template
    
    # Deep copy the template to avoid modifying original
    import copy
    extended_template = copy.deepcopy(base_template)
    
    # Calculate how many additional weeks needed
    additional_weeks = target_weeks - 12
    
    # Get the last few weeks as a pattern (use weeks 9-12 for better progression)
    last_weeks = extended_template.get("weeks", [])[-4:]  # Last 4 weeks as pattern
    
    # Create new weeks by repeating and modifying the pattern
    new_weeks = extended_template.get("weeks", [])[:]
    
    for i in range(additional_weeks):
        # Use pattern from last weeks, cycling through
        pattern_week_idx = i % len(last_weeks)
        pattern_week = last_weeks[pattern_week_idx]
        
        # Deep copy the pattern week to avoid modifying original
        new_week = copy.deepcopy(pattern_week)
        new_week_number = 13 + i
        new_week["week_number"] = new_week_number
        new_week["focus"] = f"Extended Build - Week {new_week_number}"
        
        # Adjust volume percent slightly (build phase)
        if i < additional_weeks // 2:
            new_week["volume_percent"] = min(100, pattern_week.get("volume_percent", 100) + 5)
        else:
            new_week["volume_percent"] = pattern_week.get("volume_percent", 100)
        
        # Update workout week numbers - use regex to properly replace week numbers
        import re
        for workout in new_week.get("workouts", []):
            old_name = workout.get("name", "")
            # Replace week number pattern (W01, W02, W12, etc.) with new week number
            # Pattern: W followed by 1-2 digits at start of name
            new_name = re.sub(r'^W\d{1,2}_', f'W{new_week_number:02d}_', old_name)
            # Also handle cases like "W01" in middle of name (less common)
            new_name = re.sub(r'W(\d{1,2})(?=[^0-9])', f'W{new_week_number:02d}', new_name)
            workout["name"] = new_name
            workout["week_number"] = new_week_number
        
        new_weeks.append(new_week)
    
    extended_template["weeks"] = new_weeks
    extended_template["plan_metadata"]["duration_weeks"] = target_weeks
    
    return extended_template

def insert_ftp_tests(plan_template, ftp_test_path, plan_weeks, tier):
    """Insert FTP test and durability test workouts into plan template at appropriate weeks"""
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generation_modules'))
    from ftp_test_converter import convert_ftp_test
    from durability_test_converter import convert_durability_test, select_durability_test
    
    for week in plan_template.get("weeks", []):
        week_num = week.get("week_number", 1)
        workouts = week.get("workouts", [])
        
        # Check if this is an FTP test week
        if should_insert_ftp_test(week_num, plan_weeks) and ftp_test_path:
            # Week 1, 7, 13, 19: FTP test
            for i, workout in enumerate(workouts):
                if "Tue" in workout.get("name", "") or "Test" in workout.get("name", ""):
                    # Replace with FTP test
                    ftp_workout = convert_ftp_test(ftp_test_path, week_num)
                    if ftp_workout:
                        workouts[i] = ftp_workout
                    break
            else:
                # If no Tuesday workout, insert as first workout
                ftp_workout = convert_ftp_test(ftp_test_path, week_num)
                if ftp_workout:
                    workouts.insert(0, ftp_workout)
        
        # Check if this is a durability test week (week 7, 13, or 19)
        # Note: Week 7 and 19 also have FTP tests, so we do both
        if week_num in [7, 13, 19]:
            # Select appropriate durability test
            durability_path, test_name = select_durability_test(week_num, plan_weeks, tier)
            
            if durability_path and durability_path.exists():
                # Find Saturday workout (typically where long tests go)
                for i, workout in enumerate(workouts):
                    if "Sat" in workout.get("name", "") or "Long" in workout.get("name", ""):
                        # Replace with durability test
                        durability_workout = convert_durability_test(durability_path, week_num, test_name)
                        if durability_workout:
                            workouts[i] = durability_workout
                        break
                else:
                    # If no Saturday workout, find longest workout or insert
                    longest_idx = 0
                    longest_duration = 0
                    for i, workout in enumerate(workouts):
                        # Try to estimate duration from blocks
                        blocks = workout.get("blocks", "")
                        if "Duration" in blocks:
                            # Extract duration (rough estimate)
                            import re
                            durations = re.findall(r'Duration="(\d+)"', blocks)
                            if durations:
                                total = sum(int(d) for d in durations)
                                if total > longest_duration:
                                    longest_duration = total
                                    longest_idx = i
                    
                    # Replace longest workout with durability test
                    durability_workout = convert_durability_test(durability_path, week_num, test_name)
                    if durability_workout:
                        workouts[longest_idx] = durability_workout
    
    return plan_template

def create_plan_variation(base_template, variation_key, variation_info):
    """Create a variation of a plan template"""
    variation_template = json.loads(json.dumps(base_template))  # Deep copy
    
    # Modify based on variation type
    if "Volume" in variation_info["name"]:
        # Increase volume slightly
        for week in variation_template.get("weeks", []):
            week["volume_percent"] = min(110, week.get("volume_percent", 100) + 5)
    elif "Intensity" in variation_info["name"]:
        # Increase intensity slightly (reduce recovery, add intervals)
        pass  # Would need to modify workout structures
    elif "Conservative" in variation_info["name"]:
        # Reduce volume slightly
        for week in variation_template.get("weeks", []):
            week["volume_percent"] = max(70, week.get("volume_percent", 100) - 5)
    
    variation_template["variation"] = variation_info
    return variation_template

def generate_plan_set(race_data, plan_type_info, duration, variation_key, variation_info, race_folder, race_json_path, ftp_test_template):
    """Generate one complete plan (all workouts, marketplace, guide)"""
    # Get plan type number
    plan_type_num = None
    for i, (name, info) in enumerate(PLAN_TYPES.items(), 1):
        if info == plan_type_info:
            plan_type_num = i
            break
    
    plan_type_name = list(PLAN_TYPES.keys())[list(PLAN_TYPES.values()).index(plan_type_info)]
    plan_folder_name = f"{plan_type_num}. {plan_type_name} {variation_info['name']} ({duration} weeks)"
    
    print(f"\n📦 Generating: {plan_folder_name}")
    print(f"   Duration: {duration} weeks")
    print(f"   Variation: {variation_info['name']}")
    
    plan_output_dir = race_folder / plan_folder_name
    plan_output_dir.mkdir(exist_ok=True)
    (plan_output_dir / "workouts").mkdir(exist_ok=True)
    
    # Load base plan template
    source_plan = plan_type_info['source_plans'][0]
    base_template = load_plan_template(source_plan)
    if not base_template:
        print(f"  ❌ Could not load plan template: {source_plan}")
        return False
    
    # Extend to target duration
    extended_template = extend_plan_template(base_template, duration, ftp_test_template)
    
    # Insert FTP tests and durability tests
    tier = plan_type_info.get("tier", "finisher")
    if ftp_test_template:
        extended_template = insert_ftp_tests(extended_template, ftp_test_template, duration, tier)
    
    # Create variation
    variation_template = create_plan_variation(extended_template, variation_key, variation_info)
    
    # Create plan info with methodology mapping
    philosophy = plan_type_info["philosophy"]
    # Map philosophy to methodology for v2 generator
    philosophy_lower = philosophy.lower()
    if "hiit" in philosophy_lower or "survival" in philosophy_lower:
        methodology = "HIT"
    elif "pyramidal" in philosophy_lower:
        methodology = "PYRAMIDAL"
    else:
        methodology = "POLARIZED"  # Default for Gravel God

    plan_info = {
        "tier": plan_type_info["tier"],
        "level": plan_type_info["level"],
        "weeks": duration,
        "target_hours": plan_type_info["target_hours"],
        "goal": plan_type_info["goal"],
        "philosophy": philosophy,
        "methodology": methodology,  # V2 generator methodology
        "variation": variation_info["name"]
    }
    
    # Generate ZWO files
    print(f"  → Generating ZWO files...")
    zwo_count = generate_all_zwo_files(variation_template, race_data, plan_info, plan_output_dir)
    print(f"     ✓ Generated {zwo_count} ZWO workout files")
    
    # Generate marketplace description
    print(f"  → Generating marketplace description...")
    marketplace_file = generate_marketplace_html(race_data, variation_template, plan_info)
    if marketplace_file:
        print(f"     ✓ Generated marketplace description")
    
    # Generate training guide
    print(f"  → Generating training plan guide...")
    guide_file = generate_training_guide(race_data, variation_template, plan_info, plan_output_dir, race_json_path, duration)
    if guide_file:
        print(f"     ✓ Generated training plan guide")
    
    # Generate race day workout
    from zwo_generator import generate_race_workout
    race_workout_file = generate_race_workout(race_data, plan_info, plan_output_dir)
    print(f"     ✓ Generated race day workout")
    
    # Generate strength workouts based on plan duration
    # 12-week plans: Maintenance only (compressed progression)
    # 16 and 20-week plans: Full strength training
    try:
        from strength_generator import generate_strength_files
        import os
        
        # Find strength templates file
        templates_file = Path(__file__).parent / "generation_modules" / "MASTER_TEMPLATES_V2.md"
        if not templates_file.exists():
            # Try alternative locations
            alt_paths = [
                Path(__file__).parent.parent / "generation_modules" / "MASTER_TEMPLATES_V2.md",
                Path(__file__).parent / "MASTER_TEMPLATES_V2.md"
            ]
            for alt_path in alt_paths:
                if alt_path.exists():
                    templates_file = alt_path
                    break
        
        if templates_file.exists():
            strength_count = generate_strength_files(plan_info, plan_output_dir, str(templates_file))
            if strength_count > 0:
                print(f"     ✓ Generated {strength_count} strength workout files")
        else:
            print(f"     ⚠️  Strength templates not found, skipping strength generation")
    except ImportError as e:
        print(f"     ⚠️  Strength generator not available: {e}")
    except Exception as e:
        print(f"     ⚠️  Error generating strength workouts: {e}")
    
    return True

def generate_training_guide(race_data, plan_template, plan_info, plan_output_dir, race_json_path, duration):
    """Generate training plan guide with duration-specific content"""
    guide_generator_path = Path(__file__).parent / "generation_modules" / "guide_generator.py"
    
    plan_name_slug = plan_info['tier'] + '_' + plan_info['level']
    plan_json_path = plan_output_dir / f"{plan_name_slug}_temp.json"
    
    with open(plan_json_path, 'w') as f:
        json.dump(plan_template, f, indent=2)
    
    try:
        # Guide generator may not support --duration, so we'll handle it in the template
        result = subprocess.run([
            sys.executable,
            str(guide_generator_path),
            "--race", str(race_json_path),
            "--plan", str(plan_json_path),
            "--output-dir", str(plan_output_dir)
        ], capture_output=True, text=True, check=True)
        
        plan_json_path.unlink()
        
        guide_files = list(plan_output_dir.glob(f"*{plan_name_slug}*.html"))
        if guide_files:
            return guide_files[0]
    except subprocess.CalledProcessError as e:
        print(f"     ⚠️  Guide generation failed: {e.stderr}")
        if plan_json_path.exists():
            plan_json_path.unlink()
    except Exception as e:
        print(f"     ⚠️  Guide generation error: {e}")
        if plan_json_path.exists():
            plan_json_path.unlink()
    
    return None

def create_trainingpeaks_export(race_folder, race_name):
    """Create TrainingPeaks plan export structure for easy copy/paste"""
    tp_export_dir = race_folder / "trainingpeaks_export"
    tp_export_dir.mkdir(exist_ok=True)
    
    # Create a summary document
    summary_path = tp_export_dir / "PLAN_EXPORT_SUMMARY.md"
    with open(summary_path, 'w') as f:
        f.write(f"# TrainingPeaks Plan Export - {race_name}\n\n")
        f.write("## Instructions\n\n")
        f.write("1. **First Time Setup**: Drag and drop workouts from plan folders into TrainingPeaks\n")
        f.write("2. **Subsequent Races**: Copy/paste the entire plan structure\n\n")
        f.write("## Plan Structure\n\n")
        
        for plan_type_name, plan_type_info in PLAN_TYPES.items():
            f.write(f"### {plan_type_name}\n\n")
            for duration in DURATIONS:
                for var_key, var_info in list(VARIATIONS.items())[:3]:  # First 3 variations
                    plan_folder = f"{plan_type_name} {var_info['name']} ({duration} weeks)"
                    f.write(f"- {plan_folder}\n")
    
    print(f"\n📋 Created TrainingPeaks export structure: {tp_export_dir}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_expanded_race_plans.py <race_json_file> [ftp_test_path]")
        print("Example: python generate_expanded_race_plans.py races/unbound_gravel_200.json")
        sys.exit(1)
    
    race_json_path = Path(sys.argv[1])
    if not race_json_path.exists():
        print(f"ERROR: Race JSON file not found: {race_json_path}")
        sys.exit(1)
    
    # Load FTP test template if provided
    ftp_test_template = None
    if len(sys.argv) >= 3:
        ftp_test_path = Path(sys.argv[2])
        ftp_test_template = load_ftp_test_template(ftp_test_path)
    else:
        # Try default location
        default_ftp_path = Path("/Users/mattirowe/Downloads/2026-01-30_TheAssessm.zwo")
        if default_ftp_path.exists():
            ftp_test_template = load_ftp_test_template(default_ftp_path)
    
    # Load race data
    race_data = load_race_data(race_json_path)
    race_name = race_data["race_metadata"]["name"]
    
    print(f"\n🚀 Generating Plans for: {race_name}")
    print(f"   Tiers: {len(PLAN_TYPES)}")
    print(f"   Durations: {', '.join(map(str, DURATIONS))} weeks")
    print(f"   Variation: Standard only")
    print(f"   Total Plans: {len(PLAN_TYPES)} tiers × {len(DURATIONS)} durations = {len(PLAN_TYPES) * len(DURATIONS)}")
    
    if ftp_test_template:
        print(f"   ✓ FTP test template loaded - will be inserted in 20-week plans")
    else:
        print(f"   ⚠️  No FTP test template - 20-week plans will not include FTP tests")
    
    # Create output structure
    base_path = Path(__file__).parent
    race_folder = base_path / race_name
    race_folder.mkdir(exist_ok=True)
    
    # Generate all plans
    success_count = 0
    total_plans = len(PLAN_TYPES) * len(DURATIONS) * len(VARIATIONS)
    
    for plan_type_name, plan_type_info in PLAN_TYPES.items():
        for duration in DURATIONS:
            for var_key, var_info in VARIATIONS.items():
                if generate_plan_set(race_data, plan_type_info, duration, var_key, var_info, 
                                   race_folder, race_json_path, ftp_test_template):
                    success_count += 1
    
    # Create TrainingPeaks export structure
    create_trainingpeaks_export(race_folder, race_name)
    
    print(f"\n✅ Successfully generated {success_count}/{total_plans} plans")
    print(f"   Output directory: {race_folder}")
    print(f"\n📋 Next Steps:")
    print(f"   1. Review plans in: {race_folder}")
    print(f"   2. Use TrainingPeaks export guide: {race_folder}/trainingpeaks_export/PLAN_EXPORT_SUMMARY.md")
    print(f"   3. Drag/drop workouts into TrainingPeaks for first plan")
    print(f"   4. Copy/paste plan structure for subsequent plans")

if __name__ == "__main__":
    main()

