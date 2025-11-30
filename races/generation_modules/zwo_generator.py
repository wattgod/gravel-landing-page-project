#!/usr/bin/env python3
"""
ZWO File Generator
Generates TrainingPeaks-compatible ZWO workout files from plan templates
"""

import os
import html
import re
from pathlib import Path

# ZWO Template structure
ZWO_TEMPLATE = """<?xml version='1.0' encoding='UTF-8'?>
<workout_file>
  <author>Gravel God Training</author>
  <name>{name}</name>
  <description>{description}</description>
  <sportType>bike</sportType>
      <workout>
{blocks}  </workout>
</workout_file>"""

def estimate_workout_duration(blocks):
    """Estimate workout duration in minutes from XML blocks"""
    total_seconds = 0
    duration_matches = re.findall(r'Duration="(\d+)"', blocks)
    for duration_str in duration_matches:
        total_seconds += int(duration_str)
    return total_seconds // 60

def get_heat_protocol_tier(week_num, race_data):
    """Determine heat training tier based on week type and race data"""
    if not race_data.get("workout_modifications", {}).get("heat_training", {}).get("enabled"):
        return None
    
    heat_config = race_data["workout_modifications"]["heat_training"]
    
    if week_num in heat_config.get("tier_1_weeks", []):
        return "tier1"
    elif week_num in heat_config.get("tier_2_weeks", []):
        return "tier2"
    elif week_num in heat_config.get("tier_3_weeks", []):
        return "tier3"
    return None

def add_heat_training_note(week_num, race_data, heat_tier):
    """Add heat training note based on tier"""
    if not heat_tier:
        return ""
    
    heat_notes = {
        "tier1": "\n\n• {race_name_upper} - HEAT TRAINING (Better Than Nothing):\nProtocol: Finish any normal ride, then shower hot (as hot as tolerated) for 10-12 minutes. Keep HR elevated minimally. Hydrate lightly after (don't chug immediately; small sips).\n\nEffect: Maintains heat adaptations, mild plasma-volume expansion, minimal additional stress.\n\nUse When: Fatigued, limited time, or already did the hard workout of the week.",
        "tier2": "\n\n• {race_name_upper} - HEAT TRAINING (Good):\nProtocol: Option 1: 20-40 min Z2 ride inside with reduced airflow. Option 2: 10-15 min sauna/hot bath immediately after training. Keep core temp elevated but manageable. Drink ~500-750 ml + 500-1000 mg sodium during exposure. Finish with only light cooling (no cold shower).\n\nEffect: Start of measurable heat adaptation, raises plasma volume. Training stress increases slightly but manageable.\n\nUse When: Medium weeks, early build phase, you want adaptation without deep fatigue.",
        "tier3": "\n\n• {race_name_upper} - HEAT TRAINING (Ideal - High Impact):\nProtocol: 1) Ride Outside or Indoors With Minimal Cooling: 45-75 min Z2 OR Intervals with fan on low. 2) Post-ride heat exposure: 15-25 min sauna or hot bath. 3) Hydration Target: 1-1.5 L/hr loss is OK. Replace 75% of losses within 2 hours. Sodium 1000-1500 mg/hr. 4) Avoid cooling for 20-30 min after.\n\nEffect: Maximal heat adaptation, big plasma volume gains, noticeable RPE reductions in hot races.\n\nUse When: Preparing for hot events ({race_name}), you're healthy and recovered, you can afford temporary fatigue."
    }
    
    race_name = race_data["race_metadata"]["name"]
    race_name_upper = race_name.upper()
    return heat_notes.get(heat_tier, "").format(race_name=race_name, race_name_upper=race_name_upper)

def add_hydration_note(duration_minutes, is_quality_session, race_data):
    """Add hydration note based on duration and intensity"""
    race_name_upper = race_data["race_metadata"]["name"].upper()
    if duration_minutes < 90:
        return f"\n\n• {race_name_upper} - HYDRATION:\n<90 min (any intensity): 1 bottle/hr with electrolytes mandatory. Before hard efforts, take 1 gel. Light urine color (not clear) = well hydrated."
    elif duration_minutes >= 90 and not is_quality_session:
        return f"\n\n• {race_name_upper} - HYDRATION:\n>90 min low intensity: 60g carbs/hr. 1-1.5 bottles/hr. 600-1200 mg sodium/hr depending on heat. Monitor sweat rate—if losing >1-1.5% bodyweight, increase sodium."
    else:  # >90 min high intensity/intervals/heat
        return f"\n\n• {race_name_upper} - HYDRATION:\n>90 min high intensity/intervals/heat: 90g carbs/hr. 1.5 bottles/hr minimum. 1000-1500 mg sodium/hr. Aggressive cooling: ice sock, dump water, shade stops when practical. Replace ~75% of losses within 2 hours post-ride."

def add_aggressive_fueling_note(is_long_ride, race_data):
    """Add aggressive fueling note for long rides"""
    if not is_long_ride:
        return ""
    
    target_carbs = race_data.get("workout_modifications", {}).get("aggressive_fueling", {}).get("target_carbs_per_hour", 60)
    race_name = race_data["race_metadata"]["name"]
    race_name_upper = race_name.upper()
    
    return f"\n\n• {race_name_upper} - AGGRESSIVE FUELING:\nTarget {target_carbs}-90g carbs/hour (up to 100g on dress rehearsal). Train your gut aggressively. This is critical for {race_name}'s long day. Competitors need aggressive fueling—race day isn't the time to discover your stomach can't handle 80g carbs/hour. Practice your race-day nutrition products. Start fueling from mile 1."

def add_dress_rehearsal_note(week_num, workout_name, race_data, plan_info):
    """Add dress rehearsal note if applicable"""
    dress_config = race_data.get("workout_modifications", {}).get("dress_rehearsal", {})
    
    if not dress_config.get("enabled"):
        return ""
    
    if week_num != dress_config.get("week"):
        return ""
    
    if dress_config.get("day", "Saturday") not in workout_name:
        return ""
    
    tier = plan_info.get("tier", "compete")
    duration_hours = dress_config.get("duration_hours", {}).get(tier, 9)
    race_name = race_data["race_metadata"]["name"]
    race_name_upper = race_name.upper()
    
    return f"\n\n• {race_name_upper} - DRESS REHEARSAL:\nTHIS IS YOUR {duration_hours}-HOUR 'BLOW OUT DAY.' CLEAR YOUR SCHEDULE. This is logistics practice, fueling practice, heat practice, and mental preparation all in one. Test EVERYTHING: nutrition products, hydration system, clothing, bike setup, tire pressure. Practice eating while riding. Practice bottle handoffs. Practice pacing. For Competitors, this {duration_hours}-hour ride is worth 15 shorter rides for race prep. This is the difference between finishing and performing at your best."

def add_robust_taper_note(week_num, race_data):
    """Add robust taper note if applicable"""
    taper_config = race_data.get("workout_modifications", {}).get("robust_taper", {})
    
    if not taper_config.get("enabled"):
        return ""
    
    if week_num not in taper_config.get("weeks", []):
        return ""
    
    race_name_upper = race_data["race_metadata"]["name"].upper()
    return f"\n\n• {race_name_upper} - ROBUST TAPER:\nFreshness/form counts for A LOT in this race. You don't want to show up half-cooked when you're going to go so deep in the well. Volume is low, but maintain sharpness. For competitive athletes, freshness is everything for a 200-mile day."

def add_gravel_grit_note(week_num, workout_name, race_data):
    """Add Gravel Grit note if applicable"""
    grit_config = race_data.get("workout_modifications", {}).get("gravel_grit", {})
    
    if not grit_config.get("enabled"):
        return ""
    
    if week_num != grit_config.get("week"):
        return ""
    
    if "RACE" not in workout_name.upper():
        return ""
    
    race_name_upper = race_data["race_metadata"]["name"].upper()
    return f"\n\n• {race_name_upper} - GRAVEL GRIT:\nMental preparation is as important as physical. When mile {race_data.get('race_hooks', {}).get('dark_mile', 150)} hits and everything hurts, mental toughness gets you through. Visualize success. Break the race into manageable chunks. You've trained for this. You're ready."

def add_position_alternation_note(workout_name, description, duration_minutes, is_long_ride, is_endurance):
    """
    Add note about alternating drops/hoods position for endurance and long rides.
    
    Applies to:
    - Weekday endurance days
    - Long rides
    - Pattern: 30 min drops, 30 min hoods
    """
    # Check if this is an endurance or long ride
    if not (is_endurance or is_long_ride):
        return ""
    
    # Skip if it's a rest day or very short
    if "Rest" in workout_name or duration_minutes < 60:
        return ""
    
    # Calculate number of 30-minute blocks
    num_blocks = max(1, duration_minutes // 60)  # At least 1 block for 60+ min rides
    
    change_text = "position change" if num_blocks == 1 else "position changes"
    
    return f"\n\n• POSITION ALTERNATION:\nWhile racing you get as aero as possible (drops), but in training people often try to produce maximum power (hoods, out of saddle). These aren't the same thing. Alternate position every 30 minutes: 30 min in the drops (aero, race position) → 30 min in the hoods (power production, comfort). This builds both aero efficiency and power production. For {duration_minutes}-minute rides, aim for {num_blocks} {change_text}."

def enhance_workout_description(workout, week_num, race_data, plan_info):
    """Enhance workout description with race-specific modifications"""
    description = workout.get("description", "")
    workout_name = workout.get("name", "")
    
    # Determine workout characteristics
    is_long_ride = any(keyword in workout_name for keyword in ["Long", "Extended", "Dress Rehearsal"]) or \
                   ("hours" in description and any(h in description for h in ["5", "6", "7", "8", "9"]))
    
    is_quality_session = any(keyword in workout_name for keyword in [
        "Hard Session", "Quality", "Threshold", "VO2max", "Mixed", "Race", 
        "Simulation", "G-Spot", "Gspot", "Sweet Spot", "Tempo", "Peak", "HIIT"
    ])
    
    # Check if this is an endurance ride (Z2, easy, recovery, but not rest)
    is_endurance = any(keyword in workout_name.lower() for keyword in [
        "endurance", "easy", "z2", "recovery", "spin", "aerobic"
    ]) and not is_quality_session and "Rest" not in workout_name
    
    duration_minutes = estimate_workout_duration(workout.get("blocks", ""))
    
    # Add race-specific notes
    heat_tier = get_heat_protocol_tier(week_num, race_data)
    if heat_tier and is_quality_session and "REST" not in workout_name.upper():
        description += add_heat_training_note(week_num, race_data, heat_tier)
    
    if duration_minutes > 0:
        description += add_hydration_note(duration_minutes, is_quality_session, race_data)
        race_name_upper = race_data["race_metadata"]["name"].upper()
        description += f"\n\n• {race_name_upper} - DAILY BASELINE HYDRATION:\nStart day hydrated: ~500 ml water + 500-1000 mg sodium with breakfast. Pre-ride (60 min before): 500 ml fluid + 300-600 mg sodium. Aim for light urine color (not clear)."
    
    if is_long_ride:
        description += add_aggressive_fueling_note(is_long_ride, race_data)
    
    # Add position alternation note for endurance and long rides
    description += add_position_alternation_note(workout_name, description, duration_minutes, is_long_ride, is_endurance)
    
    description += add_dress_rehearsal_note(week_num, workout_name, race_data, plan_info)
    description += add_robust_taper_note(week_num, race_data)
    description += add_gravel_grit_note(week_num, workout_name, race_data)
    
    return description

def create_zwo_file(workout, output_path, race_data, plan_info):
    """Create a single ZWO workout file"""
    name = workout.get("name", "")
    description = enhance_workout_description(workout, workout.get("week_number", 1), race_data, plan_info)
    blocks = workout.get("blocks", "    <FreeRide Duration=\"60\"/>\n")
    
    # Escape XML special characters
    name_escaped = html.escape(name, quote=False)
    description_escaped = html.escape(description, quote=False)
    
    # Generate ZWO content
    zwo_content = ZWO_TEMPLATE.format(
        name=name_escaped,
        description=description_escaped,
        blocks=blocks
    )
    
    # Write file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(zwo_content)
    
    return True

def generate_all_zwo_files(plan_template, race_data, plan_info, output_dir):
    """Generate all ZWO files for a plan"""
    workouts_dir = Path(output_dir) / "workouts"
    workouts_dir.mkdir(parents=True, exist_ok=True)
    
    total_workouts = 0
    
    # Process all weeks
    for week_data in plan_template.get("weeks", []):
        week_num = week_data.get("week_number", 1)
        
        # Check if this week has block options
        if "workouts_by_block" in week_data:
            # This week has block options - generate all blocks
            for block_name, block_workouts in week_data["workouts_by_block"].items():
                for workout in block_workouts:
                    # Create a copy to avoid modifying original
                    workout_copy = workout.copy()
                    workout_copy["week_number"] = week_num
                    
                    # Clean filename
                    base_name = workout_copy['name'].replace(' ', '_').replace('/', '_').replace('#', '').replace('(', '').replace(')', '')
                    filename = f"{base_name}_{block_name}.zwo"
                    output_path = workouts_dir / filename
                    
                    create_zwo_file(workout_copy, output_path, race_data, plan_info)
                    total_workouts += 1
        elif "workouts" in week_data:
            # Regular week without blocks
            for workout in week_data["workouts"]:
                # Create a copy to avoid modifying original
                workout_copy = workout.copy()
                workout_copy["week_number"] = week_num
                
                # Clean filename
                base_name = workout_copy['name'].replace(' ', '_').replace('/', '_').replace('#', '').replace('(', '').replace(')', '')
                filename = f"{base_name}.zwo"
                output_path = workouts_dir / filename
                
                create_zwo_file(workout_copy, output_path, race_data, plan_info)
                total_workouts += 1
    
    return total_workouts

