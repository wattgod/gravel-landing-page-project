#!/usr/bin/env python3
"""
ZWO File Generator
Generates TrainingPeaks-compatible ZWO workout files from plan templates

V2 Integration: Now uses Nate archetype library with training methodology support
"""

import os
import html
import re
from pathlib import Path

# Import the workout description generator - prefer V2 Nate integration
try:
    from workout_description_generator_v2_nate import (
        generate_nate_workout_description,
        detect_archetype,
        select_archetype_for_methodology,
        generate_zwo_blocks_from_archetype,
        NATE_ARCHETYPES_AVAILABLE,
        TRAINING_METHODOLOGIES
    )
    DESCRIPTION_GENERATOR_V2 = True
    DESCRIPTION_GENERATOR_AVAILABLE = True
except ImportError:
    DESCRIPTION_GENERATOR_V2 = False
    # Fall back to V1 legacy generator
    try:
        from workout_description_generator import generate_workout_description, detect_archetype
        DESCRIPTION_GENERATOR_AVAILABLE = True
    except ImportError:
        DESCRIPTION_GENERATOR_AVAILABLE = False
        print("⚠️  No workout description generator available - using legacy descriptions")

# Methodology mapping from plan philosophy to v2 generator
PHILOSOPHY_TO_METHODOLOGY = {
    "hiit": "HIT",
    "hiit-focused": "HIT",
    "survival": "HIT",
    "pyramidal": "PYRAMIDAL",
    "traditional pyramidal": "PYRAMIDAL",
    "polarized": "POLARIZED",
    "polarized training": "POLARIZED",
    "masters-optimized": "POLARIZED",
    "high-volume": "POLARIZED",
    "race-specific": "POLARIZED"
}

def get_methodology_from_plan(plan_info):
    """Extract training methodology from plan_info."""
    # Check for explicit methodology field first
    if "methodology" in plan_info:
        return plan_info["methodology"]

    # Fall back to parsing philosophy field
    philosophy = plan_info.get("philosophy", "").lower()

    for key, methodology in PHILOSOPHY_TO_METHODOLOGY.items():
        if key in philosophy:
            return methodology

    # Default to POLARIZED (Gravel God default)
    return "POLARIZED"

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

def generate_standardized_filename(workout_name, week_num, blocks=""):
    """
    Generate standardized filename for drag-and-drop compatibility across all plans.
    Format: W{week:02d}_{day}_{archetype}.zwo
    
    This ensures the same workout type has the same filename across all plans,
    allowing drag-and-drop once and reuse across thousands of training plans.
    """
    # Extract day of week from workout name
    day_map = {
        "Mon": ["Mon", "Monday"],
        "Tue": ["Tue", "Tuesday", "Tues"],
        "Wed": ["Wed", "Wednesday"],
        "Thu": ["Thu", "Thursday", "Thurs"],
        "Fri": ["Fri", "Friday"],
        "Sat": ["Sat", "Saturday"],
        "Sun": ["Sun", "Sunday"]
    }
    
    day = None
    for day_code, patterns in day_map.items():
        for pattern in patterns:
            if pattern in workout_name:
                day = day_code
                break
        if day:
            break
    
    if not day:
        # Fallback: try to extract from name pattern
        day_match = re.search(r'([A-Z][a-z]{2,3})\s*-', workout_name)
        if day_match:
            day_str = day_match.group(1)
            for day_code, patterns in day_map.items():
                if day_str in patterns:
                    day = day_code
                    break
    
    # Default to Mon if no day found
    if not day:
        day = "Mon"
    
    # Detect archetype for standardized naming
    try:
        # Use detect_archetype from whichever generator is available (already imported)
        archetype = detect_archetype(workout_name)
    except:
        archetype = "general"
    
    # Map archetypes to standardized names
    archetype_map = {
        "vo2_steady": "VO2max",
        "vo2_30_30": "VO2max_30_30",
        "vo2_40_20": "VO2max_40_20",
        "vo2_extended": "VO2max_Extended",
        "threshold_steady": "Threshold",
        "threshold_progressive": "Threshold_Progressive",
        "threshold_touch": "Threshold_Touch",
        "mixed_climbing": "Mixed_Climbing",
        "mixed_intervals": "Mixed_Intervals",
        "sfr": "SFR",
        "tempo": "Tempo",
        "g_spot": "G_Spot",
        "stomps": "Stomps",
        "microbursts": "Microbursts",
        "race_simulation": "Race_Simulation",
        "endurance": "Endurance",
        "testing": "FTP_Test",
        "rest": "Rest",
        "general": "General"
    }
    
    # Special handling for specific workout types
    name_upper = workout_name.upper()
    if "FTP TEST" in name_upper or "FTP_TEST" in name_upper:
        archetype_name = "FTP_Test"
    elif "DURABILITY" in name_upper:
        archetype_name = "Durability_Test"
    elif "RACE DAY" in name_upper or "RACE_DAY" in name_upper:
        archetype_name = "Race_Day"
    elif "LONG" in name_upper and ("ENDURANCE" in name_upper or "EASY" in name_upper):
        archetype_name = "Long_Endurance"
    elif "EASY" in name_upper or "RECOVERY" in name_upper or "SPIN" in name_upper:
        archetype_name = "Easy_Recovery"
    elif "REST" in name_upper:
        archetype_name = "Rest"
    else:
        archetype_name = archetype_map.get(archetype, "General")
    
    # Generate standardized filename
    filename = f"W{week_num:02d}_{day}_{archetype_name}.zwo"
    
    return filename

def get_heat_protocol_tier(week_num, race_data):
    """Determine heat/weather training tier based on week type and race data"""
    # Check for weather_training (Mid South) or heat_training (Unbound)
    weather_config = race_data.get("workout_modifications", {}).get("weather_training", {})
    heat_config = race_data.get("workout_modifications", {}).get("heat_training", {})
    
    # Use weather_training if available, otherwise fall back to heat_training
    config = weather_config if weather_config.get("enabled") else heat_config
    
    if not config.get("enabled"):
        return None
    
    if week_num in config.get("tier_1_weeks", []):
        return "tier1"
    elif week_num in config.get("tier_2_weeks", []):
        return "tier2"
    elif week_num in config.get("tier_3_weeks", []):
        return "tier3"
    return None

def add_heat_training_note(week_num, race_data, heat_tier, is_endurance):
    """Add heat/weather training note based on tier and workout type"""
    if not heat_tier:
        return ""
    
    # Check if this is weather training (Mid South) or heat training (Unbound)
    weather_config = race_data.get("workout_modifications", {}).get("weather_training", {})
    heat_config = race_data.get("workout_modifications", {}).get("heat_training", {})
    is_weather_training = weather_config.get("enabled", False)
    
    # Get training weeks from race data
    if is_weather_training:
        training_weeks = weather_config.get("tier_3_weeks", [4, 5, 6, 7, 8, 9, 10])
        training_type = "WEATHER ADAPTATION"
        training_desc = "unpredictable conditions (cold, heat, wind)"
    else:
        training_weeks = heat_config.get("tier_3_weeks", [6, 7, 8, 9, 10])
        training_type = "HEAT ACCLIMATIZATION"
        training_desc = "hot conditions"
    
    week_range = f"{min(training_weeks)}-{max(training_weeks)}" if training_weeks else "6-10"
    
    # Training protocol period
    if week_num in training_weeks:
        if is_weather_training:
            # Weather adaptation (cold, heat, wind)
            if is_endurance:
                return f"\n\n• {training_type} PROTOCOL (Weeks {week_range}):\nThis endurance ride is ideal for weather adaptation training. Race day weather can be unpredictable—you could face 40°F freezing rain or 75°F heat. Train in varied conditions:\n\nOPTION 1 - COLD WEATHER TRAINING:\n• Ride in cold conditions (40-50°F) with appropriate clothing\n• Practice fueling and hydration in cold (harder to drink when cold)\n• Test clothing layers and wind protection\n\nOPTION 2 - HEAT TRAINING (if available):\n• Ride in warm conditions (70-75°F) if weather permits\n• Practice hydration and cooling strategies\n• Test clothing for heat\n\nOPTION 3 - WIND TRAINING:\n• Ride on exposed roads/ridgelines when windy\n• Practice aero positioning and pacing in wind\n• Build strength and tactics for windy conditions\n\nEFFECT: Adapting to varied conditions prevents race-day shock. Weather unpredictability is THE defining feature—be ready for anything.\n\nSAFETY: Don't train in dangerous conditions (ice, extreme cold, severe weather). Safety first."
            else:
                # Quality sessions: Complete in normal conditions, note weather prep
                return f"\n\n• {training_type} (Weeks {week_range}):\nComplete this quality session in normal conditions (preserve workout quality). Weather adaptation happens on endurance rides. Prepare for unpredictable conditions—cold, heat, wind, or mud. Practice your race-day clothing and nutrition strategies during long rides."
        else:
            # Heat acclimatization
            if is_endurance:
                return f"\n\n• {training_type} PROTOCOL (Weeks {week_range}):\nThis endurance ride is ideal for heat training. Choose ONE option:\n\nOPTION 1 - INDOOR TRAINER (Cool Climate):\n• Turn OFF all fans\n• Close windows/doors\n• Wear: thermal base + rain jacket + leg warmers + gloves + beanie\n• Target core temp: 38.5-39.0°C for 45-60 min\n• If temp >39.5°C: reduce power 10% or stop\n\nOPTION 2 - POST-EXERCISE HOT WATER IMMERSION:\n• Complete ride in normal conditions\n• Immediately after: 30-40 min hot bath at 40°C (104°F)\n• Submerged to shoulders, head exposed\n• Relief breaks: sit up 2 min every 10 min if needed\n\nOPTION 3 - SAUNA (Maintenance):\n• Complete ride in normal conditions\n• Post-ride: 25-30 min sauna at 80-100°C\n• 3-4 sessions per week for adaptation\n\nEFFECT: 5-8% performance improvement in hot conditions. Plasma volume expansion, enhanced sweating, reduced cardiovascular strain.\n\nSAFETY: Never exceed 39.5°C core temp. Stop if confused, dizzy, or nauseous. Skip if ill, dehydrated, or poorly recovered."
            else:
                return f"\n\n• {training_type} (Weeks {week_range}):\nComplete this quality session in COOL conditions (preserve workout quality). After workout, add heat exposure:\n\nPOST-EXERCISE OPTION:\n• 30-40 min hot bath at 40°C (104°F) OR\n• 25-30 min sauna at 80-100°C\n\nEFFECT: Heat adaptation without compromising interval quality. Research shows post-exercise heat exposure produces adaptations comparable to active heat training.\n\nNOTE: Heat training should NOT compromise workout quality. Reserve active heat training for easy endurance rides."
    
    # Outside training weeks: Maintenance protocol
    if is_weather_training:
        return f"\n\n• WEATHER MAINTENANCE:\nContinue training in varied conditions when possible. Race day weather can be unpredictable—stay adaptable."
    else:
        return f"\n\n• HEAT MAINTENANCE:\nAdaptations decay 2.5% per day without exposure. Maintenance: One 60-90 min heat session every 3-5 days OR 30 min sauna 3x/week OR 30-40 min hot bath every 3 days."

def add_hydration_note(duration_minutes, is_quality_session, race_data):
    """Add hydration note based on duration and intensity"""
    if duration_minutes < 90:
        return f"\n\n• HYDRATION:\n<90 min (any intensity): 1 bottle/hr with electrolytes mandatory. Before hard efforts, take 1 gel. Light urine color (not clear) = well hydrated."
    elif duration_minutes >= 90 and not is_quality_session:
        return f"\n\n• HYDRATION:\n>90 min low intensity: 60g carbs/hr. 1-1.5 bottles/hr. 600-1200 mg sodium/hr depending on heat. Monitor sweat rate—if losing >1-1.5% bodyweight, increase sodium."
    else:  # >90 min high intensity/intervals/heat
        return f"\n\n• HYDRATION:\n>90 min high intensity/intervals/heat: 90g carbs/hr. 1.5 bottles/hr minimum. 1000-1500 mg sodium/hr. Aggressive cooling: ice sock, dump water, shade stops when practical. Replace ~75% of losses within 2 hours post-ride."

def add_aggressive_fueling_note(is_long_ride, race_data):
    """Add aggressive fueling note for long rides"""
    if not is_long_ride:
        return ""
    
    target_carbs = race_data.get("workout_modifications", {}).get("aggressive_fueling", {}).get("target_carbs_per_hour", 60)
    
    return f"\n\n• AGGRESSIVE FUELING:\nTarget {target_carbs}-90g carbs/hour (up to 100g on dress rehearsal). Train your gut aggressively. This is critical for long race days. Competitors need aggressive fueling—race day isn't the time to discover your stomach can't handle 80g carbs/hour. Practice your race-day nutrition products. Start fueling from mile 1."

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
    
    return f"\n\n• DRESS REHEARSAL:\nTHIS IS YOUR {duration_hours}-HOUR 'BLOW OUT DAY.' CLEAR YOUR SCHEDULE. This is logistics practice, fueling practice, heat practice, and mental preparation all in one. Test EVERYTHING: nutrition products, hydration system, clothing, bike setup, tire pressure. Practice eating while riding. Practice bottle handoffs. Practice pacing. For Competitors, this {duration_hours}-hour ride is worth 15 shorter rides for race prep. This is the difference between finishing and performing at your best."

def add_robust_taper_note(week_num, race_data):
    """Add robust taper note if applicable"""
    taper_config = race_data.get("workout_modifications", {}).get("robust_taper", {})
    
    if not taper_config.get("enabled"):
        return ""
    
    if week_num not in taper_config.get("weeks", []):
        return ""
    
    race_distance = race_data["race_metadata"].get("distance_miles", 100)
    return f"\n\n• ROBUST TAPER:\nFreshness/form counts for A LOT in this race. You don't want to show up half-cooked when you're going to go so deep in the well. Volume is low, but maintain sharpness. For competitive athletes, freshness is everything for a {race_distance}-mile day."

def add_survey_link(week_num, workout_name, race_data, plan_info):
    """Add survey link to the final workout (last week, Sunday)
    Returns tuple: (new_workout_name, description_addition)
    """
    # Get plan duration from plan_info
    plan_weeks = plan_info.get("weeks", 12)
    
    # Check if this is the final week and Sunday workout
    # Pattern: "W## Sun - ..." where Sun is the day indicator (not a substring like "Sunday")
    is_final_week = week_num == plan_weeks
    # Check for Sunday day indicator pattern: " Sun - " or starts with "W## Sun"
    is_sunday = " Sun - " in workout_name or re.match(r'^W\d+\s+Sun\s+-', workout_name) is not None
    
    if is_final_week and is_sunday:
        race_name = race_data.get("race_metadata", {}).get("name", "Race")
        tier = plan_info.get("tier", "").lower()
        level = plan_info.get("level", "").lower()
        
        # Generate plan-specific survey URL
        race_slug = race_name.lower().replace(' ', '-').replace('the ', '')
        # Map tier to survey slug (use "time-crunched" instead of "ayahuasca")
        tier_slug_map = {
            "ayahuasca": "time-crunched",
            "finisher": "finisher",
            "compete": "compete",
            "podium": "podium"
        }
        tier_slug = tier_slug_map.get(tier.lower(), tier.lower())
        level_slug = level.lower().replace('_', '-')
        survey_filename = f"survey-{race_slug}-{tier_slug}-{level_slug}.html"
        survey_url = f"https://wattgod.github.io/gravel-landing-page-project/guides/{race_slug}/surveys/{survey_filename}"
        
        # GG brand tone congratulations
        # Map tier names to display names
        tier = plan_info.get("tier", "").lower()
        tier_display_map = {
            "ayahuasca": "Time Crunched",
            "finisher": "Finisher",
            "compete": "Compete",
            "podium": "Podium"
        }
        tier_display = tier_display_map.get(tier, tier.title())
        
        level_display = plan_info.get("level", "").replace("_", " ").title()
        if level_display == "Save My Race":
            level_display = "Save My Race"
        # Note: GOAT removed - no longer used
        
        description_addition = f"""

🎉 CONGRATULATIONS - YOU DID IT! 🎉

You've completed the {tier_display} {level_display} training plan. That's not easy. You showed up. You put in the work. You built the fitness. Now it's time to race—or you already did.

• TRAINING PLAN SURVEY (POST-COMPLETION):
Your experience matters. Share what worked, what didn't, and what we can improve. This feedback directly shapes future plans. Takes 3-4 minutes.

Survey: {survey_url}

Your honest feedback helps us make each plan better. Thank you for trusting the process. Now go execute. 🚴"""
        
        # Return new workout name and description addition
        return ("Training Plan Survey", description_addition)
    
    return (None, "")

def add_gravel_grit_note(week_num, workout_name, race_data):
    """Add Gravel Grit note if applicable"""
    grit_config = race_data.get("workout_modifications", {}).get("gravel_grit", {})
    
    if not grit_config.get("enabled"):
        return ""
    
    if week_num != grit_config.get("week"):
        return ""
    
    if "RACE" not in workout_name.upper():
        return ""
    
    dark_mile = race_data.get('race_hooks', {}).get('dark_mile', 150)
    return f"\n\n• GRAVEL GRIT:\nMental preparation is as important as physical. When mile {dark_mile} hits and everything hurts, mental toughness gets you through. Visualize success. Break the race into manageable chunks. You've trained for this. You're ready."

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
    # Weather/heat training applies to specified weeks
    heat_tier = get_heat_protocol_tier(week_num, race_data)
    weather_config = race_data.get("workout_modifications", {}).get("weather_training", {})
    heat_config = race_data.get("workout_modifications", {}).get("heat_training", {})
    training_weeks = weather_config.get("tier_3_weeks", []) if weather_config.get("enabled") else heat_config.get("tier_3_weeks", [])
    is_training_week = week_num in training_weeks
    
    if is_training_week and "REST" not in workout_name.upper():
        # Use tier3 for weather/heat training weeks if enabled
        if heat_tier:
            description += add_heat_training_note(week_num, race_data, heat_tier, is_endurance)
        elif weather_config.get("enabled") or heat_config.get("enabled"):
            # Default: assume training is enabled
            description += add_heat_training_note(week_num, race_data, "tier3", is_endurance)
    
    if duration_minutes > 0:
        description += add_hydration_note(duration_minutes, is_quality_session, race_data)
        description += f"\n\n• DAILY BASELINE HYDRATION:\nStart day hydrated: ~500 ml water + 500-1000 mg sodium with breakfast. Pre-ride (60 min before): 500 ml fluid + 300-600 mg sodium. Aim for light urine color (not clear)."
    
    if is_long_ride:
        description += add_aggressive_fueling_note(is_long_ride, race_data)
    
    # Add position alternation note for endurance and long rides
    description += add_position_alternation_note(workout_name, description, duration_minutes, is_long_ride, is_endurance)
    
    description += add_dress_rehearsal_note(week_num, workout_name, race_data, plan_info)
    description += add_robust_taper_note(week_num, race_data)
    description += add_gravel_grit_note(week_num, workout_name, race_data)
    
    # Add survey link to final workout (last week, Sunday)
    new_name, survey_description = add_survey_link(week_num, workout_name, race_data, plan_info)
    description += survey_description
    
    # Return description and potentially new name
    return description, new_name

def create_zwo_file(workout, output_path, race_data, plan_info):
    """Create a single ZWO workout file"""
    name = workout.get("name", "")
    week_num = workout.get("week_number", 1)
    blocks = workout.get("blocks", "    <FreeRide Duration=\"60\"/>\n")
    original_description = workout.get("description", "")

    # Generate proper description using generator
    if DESCRIPTION_GENERATOR_AVAILABLE:
        # Get methodology from plan
        methodology = get_methodology_from_plan(plan_info)
        total_weeks = plan_info.get("weeks", 12)

        # Calculate progression level (1-6) based on week position
        progress = week_num / total_weeks
        if progress < 0.17:
            level = 1
        elif progress < 0.33:
            level = 2
        elif progress < 0.50:
            level = 3
        elif progress < 0.67:
            level = 4
        elif progress < 0.83:
            level = 5
        else:
            level = 6

        # Use V2 Nate generator if available
        if DESCRIPTION_GENERATOR_V2 and NATE_ARCHETYPES_AVAILABLE:
            # Detect workout type and get matching archetype
            workout_type = detect_archetype(name)
            archetype, rec_level = select_archetype_for_methodology(
                workout_type,
                methodology=methodology,
                week_num=week_num,
                total_weeks=total_weeks
            )

            if archetype:
                # Generate description from Nate archetype
                description = generate_nate_workout_description(
                    archetype,
                    level,
                    methodology=methodology,
                    include_dimensions=True
                )
            else:
                # Fall back to V1 generator for non-Nate archetypes
                try:
                    from workout_description_generator import generate_workout_description as v1_generate
                    description = v1_generate(
                        workout_name=name,
                        blocks=blocks,
                        week_num=week_num,
                        level=level,
                        existing_description=original_description
                    )
                except:
                    description = original_description
        else:
            # Use V1 legacy generator
            description = generate_workout_description(
                workout_name=name,
                blocks=blocks,
                week_num=week_num,
                level=level,
                existing_description=original_description
            )
    else:
        # Fall back to original description
        description = original_description

    # Add race-specific enhancements (hydration, heat, etc.)
    description, new_name = enhance_workout_description(
        {"name": name, "description": description, "blocks": blocks, "week_number": week_num},
        week_num,
        race_data,
        plan_info
    )

    # Use new name if provided (for survey workout)
    if new_name:
        name = new_name

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
                    
                    # Use standardized filename for drag-and-drop compatibility
                    filename = generate_standardized_filename(
                        workout_copy['name'], 
                        week_num, 
                        workout_copy.get('blocks', '')
                    )
                    # Add block suffix if multiple blocks
                    if len(week_data["workouts_by_block"]) > 1:
                        base_name = filename.replace('.zwo', '')
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
                
                # Use standardized filename for drag-and-drop compatibility
                filename = generate_standardized_filename(
                    workout_copy['name'], 
                    week_num, 
                    workout_copy.get('blocks', '')
                )
                
                output_path = workouts_dir / filename
                
                create_zwo_file(workout_copy, output_path, race_data, plan_info)
                total_workouts += 1
    
    return total_workouts

def estimate_race_time_hours(race_data, tier_key, level_key):
    """Estimate race completion time in hours based on tier, level, and race distance"""
    distance = race_data.get("race_metadata", {}).get("distance_miles", 100)
    elevation = race_data.get("race_metadata", {}).get("elevation_feet", 0)
    
    # Base average speeds (mph) by tier and level
    # These are conservative estimates for typical athletes
    # Adjusted for realistic gravel race speeds (slower than road)
    speed_map = {
        ("ayahuasca", "beginner"): 11.0,
        ("ayahuasca", "intermediate"): 12.0,
        ("ayahuasca", "masters"): 11.5,
        ("ayahuasca", "save_my_race"): 10.5,
        ("finisher", "beginner"): 14.5,
        ("finisher", "intermediate"): 14.5,
        ("finisher", "advanced"): 16.0,
        ("finisher", "masters"): 13.5,
        ("finisher", "save_my_race"): 12.5,
        ("compete", "intermediate"): 15.5,
        ("compete", "advanced"): 17.5,
        ("compete", "masters"): 15.0,
        ("compete", "save_my_race"): 14.0,
        ("podium", "advanced"): 19.0,
        ("podium", "advanced_goat"): 20.5,
    }
    
    # Get base speed
    base_speed = speed_map.get((tier_key, level_key), 12.0)
    
    # Adjust for elevation (more elevation = slower)
    # For longer races, elevation penalty is less impactful (spread over more distance)
    # Rough adjustment: -0.3 mph per 1000ft over 5000ft for races >150 miles
    # -0.5 mph per 1000ft over 5000ft for shorter races
    if distance > 150:
        elevation_penalty_multiplier = 0.3
    else:
        elevation_penalty_multiplier = 0.5
    
    elevation_penalty = max(0, (elevation - 5000) / 1000) * elevation_penalty_multiplier
    adjusted_speed = base_speed - elevation_penalty
    
    # Calculate time
    time_hours = distance / adjusted_speed
    
    # Round to nearest 0.5 hours
    time_hours = round(time_hours * 2) / 2
    
    return max(4.0, time_hours)  # Minimum 4 hours

def generate_race_workout_blocks(total_minutes, tier_key, level_key, distance, elevation):
    """Generate structured workout blocks for race day based on Three-Act pacing framework"""
    
    # Define intensity zones by tier (as % of FTP)
    # These represent sustainable race pace for each tier
    intensity_map = {
        ("ayahuasca", "beginner"): {"steady": 0.65, "build": 0.70, "strong": 0.72},
        ("ayahuasca", "intermediate"): {"steady": 0.68, "build": 0.73, "strong": 0.75},
        ("ayahuasca", "masters"): {"steady": 0.66, "build": 0.71, "strong": 0.73},
        ("ayahuasca", "save_my_race"): {"steady": 0.63, "build": 0.68, "strong": 0.70},
        ("finisher", "beginner"): {"steady": 0.70, "build": 0.75, "strong": 0.78},
        ("finisher", "intermediate"): {"steady": 0.73, "build": 0.78, "strong": 0.80},
        ("finisher", "advanced"): {"steady": 0.76, "build": 0.81, "strong": 0.83},
        ("finisher", "masters"): {"steady": 0.72, "build": 0.77, "strong": 0.79},
        ("finisher", "save_my_race"): {"steady": 0.68, "build": 0.73, "strong": 0.75},
        ("compete", "intermediate"): {"steady": 0.78, "build": 0.83, "strong": 0.85},
        ("compete", "advanced"): {"steady": 0.82, "build": 0.87, "strong": 0.90},
        ("compete", "masters"): {"steady": 0.76, "build": 0.81, "strong": 0.83},
        ("compete", "save_my_race"): {"steady": 0.74, "build": 0.79, "strong": 0.81},
        ("podium", "advanced"): {"steady": 0.85, "build": 0.90, "strong": 0.93},
        ("podium", "advanced_goat"): {"steady": 0.88, "build": 0.93, "strong": 0.96},
    }
    
    intensities = intensity_map.get((tier_key, level_key), {"steady": 0.70, "build": 0.75, "strong": 0.78})
    
    # Warmup: 10-15 minutes (in seconds)
    warmup_duration = min(900, max(600, total_minutes * 60 // 20))  # 10-15 min or 5% of total
    
    # Cooldown: 5-10 minutes (in seconds)
    cooldown_duration = min(600, max(300, total_minutes * 60 // 30))  # 5-10 min or 3% of total
    
    # Three-Act framework breakdown (remaining time after warmup/cooldown)
    total_seconds = total_minutes * 60
    race_seconds = total_seconds - warmup_duration - cooldown_duration
    
    # Split race time into three acts
    act1_seconds = int(race_seconds * 0.33)  # First third
    act2_seconds = int(race_seconds * 0.34)  # Middle third
    act3_seconds = race_seconds - act1_seconds - act2_seconds  # Final third (gets remainder)
    
    # Build workout blocks
    blocks = []
    
    # Warmup
    blocks.append(f'    <Warmup Duration="{warmup_duration}" PowerLow="0.50" PowerHigh="0.65"/>\n')
    
    # Act 1: Build into race (conservative start, building intensity)
    # Split into segments to show progression if long enough
    if act1_seconds > 1800:  # If >30 min, split into segments
        act1_part1 = act1_seconds // 2
        act1_part2 = act1_seconds - act1_part1
        blocks.append(f'    <SteadyState Duration="{act1_part1}" Power="{intensities["steady"]:.2f}" Cadence="85"/>\n')
        blocks.append(f'    <SteadyState Duration="{act1_part2}" Power="{intensities["build"]:.2f}" Cadence="85"/>\n')
    else:
        blocks.append(f'    <SteadyState Duration="{act1_seconds}" Power="{intensities["steady"]:.2f}" Cadence="85"/>\n')
    
    # Act 2: Sustainable pace (main race effort)
    blocks.append(f'    <SteadyState Duration="{act2_seconds}" Power="{intensities["build"]:.2f}" Cadence="85"/>\n')
    
    # Act 3: Stay strong (maintain or slightly increase)
    blocks.append(f'    <SteadyState Duration="{act3_seconds}" Power="{intensities["strong"]:.2f}" Cadence="85"/>\n')
    
    # Cooldown
    blocks.append(f'    <Cooldown Duration="{cooldown_duration}" PowerLow="{intensities["strong"]:.2f}" PowerHigh="0.55"/>\n')
    
    return "".join(blocks)

def generate_race_workout(race_data, plan_info, output_dir):
    """Generate a race day workout file"""
    tier_key = plan_info.get("tier", "").lower()
    level_key = plan_info.get("level", "").lower()
    race_name = race_data.get("race_metadata", {}).get("name", "Race")
    race_name_upper = race_name.upper()
    distance = race_data.get("race_metadata", {}).get("distance_miles", 100)
    elevation = race_data.get("race_metadata", {}).get("elevation_feet", 0)
    
    # Estimate race time
    estimated_hours = estimate_race_time_hours(race_data, tier_key, level_key)
    estimated_minutes = int(estimated_hours * 60)
    
    # Get race-specific tactics from guide variables
    guide_vars = race_data.get("guide_variables", {})
    race_challenges = guide_vars.get("race_challenges", [])
    race_terrain = guide_vars.get("race_terrain", "")
    race_weather = guide_vars.get("race_weather", "")
    
    # Format challenges
    challenges_text = ""
    if race_challenges:
        challenges_text = "\n".join([f"• {challenge}" for challenge in race_challenges[:3]])
    
    # Build description with race tactics and checklists
    description = f"""• RACE DAY - {race_name_upper}
Estimated completion time: {estimated_hours:.1f} hours ({estimated_minutes} minutes)
Distance: {distance} miles | Elevation: {elevation:,} feet

• PRE-RACE CHECKLIST (Review 1-2 weeks before race):
✓ Review your training guide's equipment checklist
✓ Test all race-day nutrition products
✓ Practice race-day fueling strategy (60-90g carbs/hour)
✓ Check weather forecast 5 days out, then daily
✓ Pack layers for variable conditions
✓ Test bike setup and tire pressure
✓ Review race route and aid station locations
✓ Plan pacing strategy (Three-Act framework)
✓ Review mental protocols for when it gets hard
✓ Prepare emergency repair kit

• RACE TACTICS & STRATEGY:
{challenges_text if challenges_text else f"• {race_terrain}" if race_terrain else ""}

PACING - Three-Act Framework:
• Act 1 (First 1/3): Start conservatively. Build into the race. Don't go too hard early.
• Act 2 (Middle 1/3): Settle into sustainable pace. Focus on nutrition and hydration.
• Act 3 (Final 1/3): This is where training pays off. Stay strong when others fade.

FUELING:
• Start fueling from mile 1 - don't wait until you're hungry
• Target 60-90g carbs/hour (up to 100g if trained)
• Practice your race-day products - no experiments on race day
• Hydration: 1-1.5 bottles/hour, 600-1500mg sodium/hour depending on conditions
• Monitor urine color - light yellow (not clear) = well hydrated

RACE-SPECIFIC NOTES:
{race_weather if race_weather else "Check weather forecast and adjust gear accordingly."}

• RESOURCES IN YOUR GUIDE:
Before race day, review these sections in your training guide:
• Equipment Checklist (download and use)
• Race Strategy & Tactics section
• Nutrition & Hydration protocols
• Technical Skills section
• Mental Training protocols
• Race Week preparation

• RACE DAY MINDSET:
You've done the work. Trust your training. Execute your plan. When it gets hard (and it will), remember: this is what you trained for. Stay patient, stay fueled, stay strong.

Good luck! You've got this. 🚴"""
    
    # Create workout name
    plan_title = plan_info.get("tier", "").title() + " " + plan_info.get("level", "").replace("_", " ").title()
    workout_name = f"RACE DAY - {race_name}"
    
    # Create structured workout blocks based on tier and estimated time
    # Three-Act pacing framework with appropriate intensities
    blocks = generate_race_workout_blocks(estimated_minutes, tier_key, level_key, distance, elevation)
    
    # Create ZWO file
    workouts_dir = Path(output_dir) / "workouts"
    workouts_dir.mkdir(parents=True, exist_ok=True)
    
    # Standardized filename (no race name for drag-and-drop compatibility)
    filename = "RACE_DAY.zwo"
    output_path = workouts_dir / filename
    
    # Escape XML
    name_escaped = html.escape(workout_name, quote=False)
    description_escaped = html.escape(description, quote=False)
    
    zwo_content = ZWO_TEMPLATE.format(
        name=name_escaped,
        description=description_escaped,
        blocks=blocks
    )
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(zwo_content)
    
    return output_path

