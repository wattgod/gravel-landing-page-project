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
    
    race_name = race_data["race_metadata"]["name"]
    race_name_upper = race_name.upper()
    
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
            # Mid South: Weather adaptation (cold, heat, wind)
            if is_endurance:
                return f"\n\n• {race_name_upper} - {training_type} PROTOCOL (Weeks {week_range}):\nThis endurance ride is ideal for weather adaptation training. Mid South's weather lottery means you could face 40°F freezing rain or 75°F heat. Train in varied conditions:\n\nOPTION 1 - COLD WEATHER TRAINING:\n• Ride in cold conditions (40-50°F) with appropriate clothing\n• Practice fueling and hydration in cold (harder to drink when cold)\n• Test clothing layers and wind protection\n\nOPTION 2 - HEAT TRAINING (if available):\n• Ride in warm conditions (70-75°F) if weather permits\n• Practice hydration and cooling strategies\n• Test clothing for heat\n\nOPTION 3 - WIND TRAINING:\n• Ride on exposed roads/ridgelines when windy\n• Practice aero positioning and pacing in wind\n• Build strength and tactics for windy conditions\n\nEFFECT: Adapting to varied conditions prevents race-day shock. Mid South's weather unpredictability is THE defining feature—be ready for anything.\n\nSAFETY: Don't train in dangerous conditions (ice, extreme cold, severe weather). Safety first."
            else:
                # Quality sessions: Complete in normal conditions, note weather prep
                return f"\n\n• {race_name_upper} - {training_type} (Weeks {week_range}):\nComplete this quality session in normal conditions (preserve workout quality). Weather adaptation happens on endurance rides. For Mid South, prepare for unpredictable conditions—cold, heat, wind, or mud. Practice your race-day clothing and nutrition strategies during long rides."
        else:
            # Unbound: Heat acclimatization
            if is_endurance:
                return f"\n\n• {race_name_upper} - {training_type} PROTOCOL (Weeks {week_range}):\nThis endurance ride is ideal for heat training. Choose ONE option:\n\nOPTION 1 - INDOOR TRAINER (Cool Climate):\n• Turn OFF all fans\n• Close windows/doors\n• Wear: thermal base + rain jacket + leg warmers + gloves + beanie\n• Target core temp: 38.5-39.0°C for 45-60 min\n• If temp >39.5°C: reduce power 10% or stop\n\nOPTION 2 - POST-EXERCISE HOT WATER IMMERSION:\n• Complete ride in normal conditions\n• Immediately after: 30-40 min hot bath at 40°C (104°F)\n• Submerged to shoulders, head exposed\n• Relief breaks: sit up 2 min every 10 min if needed\n\nOPTION 3 - SAUNA (Maintenance):\n• Complete ride in normal conditions\n• Post-ride: 25-30 min sauna at 80-100°C\n• 3-4 sessions per week for adaptation\n\nEFFECT: 5-8% performance improvement in hot conditions. Plasma volume expansion, enhanced sweating, reduced cardiovascular strain.\n\nSAFETY: Never exceed 39.5°C core temp. Stop if confused, dizzy, or nauseous. Skip if ill, dehydrated, or poorly recovered."
            else:
                return f"\n\n• {race_name_upper} - {training_type} (Weeks {week_range}):\nComplete this quality session in COOL conditions (preserve workout quality). After workout, add heat exposure:\n\nPOST-EXERCISE OPTION:\n• 30-40 min hot bath at 40°C (104°F) OR\n• 25-30 min sauna at 80-100°C\n\nEFFECT: Heat adaptation without compromising interval quality. Research shows post-exercise heat exposure produces adaptations comparable to active heat training.\n\nNOTE: Heat training should NOT compromise workout quality. Reserve active heat training for easy endurance rides."
    
    # Outside training weeks: Maintenance protocol
    if is_weather_training:
        return f"\n\n• {race_name_upper} - WEATHER MAINTENANCE:\nContinue training in varied conditions when possible. Mid South's weather lottery means race day could be anything—stay adaptable."
    else:
        return f"\n\n• {race_name_upper} - HEAT MAINTENANCE:\nAdaptations decay 2.5% per day without exposure. Maintenance: One 60-90 min heat session every 3-5 days OR 30 min sauna 3x/week OR 30-40 min hot bath every 3 days."

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
    race_distance = race_data["race_metadata"].get("distance_miles", 100)
    return f"\n\n• {race_name_upper} - ROBUST TAPER:\nFreshness/form counts for A LOT in this race. You don't want to show up half-cooked when you're going to go so deep in the well. Volume is low, but maintain sharpness. For competitive athletes, freshness is everything for a {race_distance}-mile day."

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
        ("finisher", "beginner"): 13.0,
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
    
    # Create ZWO blocks - long free ride for the estimated duration
    blocks = f"    <FreeRide Duration=\"{estimated_minutes}\"/>\n"
    
    # Create ZWO file
    workouts_dir = Path(output_dir) / "workouts"
    workouts_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"RACE_DAY_-_{race_name.replace(' ', '_')}.zwo"
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

