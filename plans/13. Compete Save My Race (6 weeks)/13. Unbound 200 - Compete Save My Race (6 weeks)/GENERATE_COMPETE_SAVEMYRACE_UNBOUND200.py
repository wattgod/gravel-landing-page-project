#!/usr/bin/env python3
"""
COMPETE SAVE MY RACE - 6 WEEK EMERGENCY PLAN (UNBOUND 200 MODIFIED)
ZWO Generation Script - Block Periodization with Cadence Work, Rhythm Intervals & Unbound 200 Modifications

Training Philosophy: Block Periodization (Compressed)
Target: 15-18 hours/week
Goal: Convert existing race fitness into peak competitive performance in compressed timeframe
Race: Unbound 200 (heat, long day, logistics-heavy)

UNBOUND 200 MODIFICATIONS:
- Heat training emphasis (Weeks 2-5)
- Aggressive fueling practice (60-90g carbs/hour on long rides)
- Dress rehearsal: 9-hour ride in Week 3 Saturday (~3 weeks before race)
- Robust taper (Week 6)
- Gravel Grit integration (Week 6 race day)
- Cadence work: High (100+ rpm) & Low (40-60 rpm) on all intervals
- Rhythm/Mixed intervals in Week 5 (sharpening)
- Loaded intervals in Week 5 (sharpening)
- G-Spot (87-92% FTP) replaces Sweet Spot (88-93% FTP)

Imports all workout data from ALL_WORKOUTS_DATA_SAVEMYRACE.py and enhances with Unbound-specific modifications.
"""
import sys
import os
import re

# Import all workout data
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from ALL_WORKOUTS_DATA_SAVEMYRACE import (
        week_1, week_2_vo2max, week_2_threshold, week_2_durability,
        week_3_vo2max, week_3_threshold, week_3_durability,
        week_4, week_5, week_6
    )
except ImportError as e:
    print(f"ERROR: Could not import workout data: {e}")
    print("Make sure ALL_WORKOUTS_DATA_SAVEMYRACE.py is in the same directory.")
    exit(1)

def get_heat_protocol_tier(week_num, is_recovery_week=False, is_load_week=False):
    """Determine heat training tier based on week type"""
    # Recovery week (4)
    if is_recovery_week:
        return "tier1"  # Better Than Nothing
    # Load weeks (2, 3)
    elif is_load_week:
        return "tier3"  # Ideal (for healthy, recovered athletes in emergency plan)
    # Medium weeks (5)
    else:
        return "tier2"  # Good

def add_unbound_notes_to_description(description, week_num, is_long_ride=False, is_quality_session=False, is_dress_rehearsal=False, duration_minutes=0, workout_name=""):
    """Add Unbound 200 specific notes to workout description"""
    unbound_notes = []
    
    # Determine week type for heat protocol
    is_recovery_week = week_num == 4
    is_load_week = week_num in [2, 3]
    heat_tier = get_heat_protocol_tier(week_num, is_recovery_week, is_load_week)
    
    # Heat training (Weeks 2-5, quality sessions)
    if week_num >= 2 and week_num <= 5 and is_quality_session and 'REST' not in description:
        if heat_tier == "tier1":
            heat_note = "\n\n★ UNBOUND 200 - HEAT TRAINING (Better Than Nothing):\nProtocol: Finish any normal ride, then shower hot (as hot as tolerated) for 10-12 minutes. Keep HR elevated minimally. Hydrate lightly after (don't chug immediately; small sips).\n\nEffect: Maintains heat adaptations, mild plasma-volume expansion, minimal additional stress.\n\nUse When: Fatigued, limited time, or already did the hard workout of the week."
        elif heat_tier == "tier2":
            heat_note = "\n\n★ UNBOUND 200 - HEAT TRAINING (Good):\nProtocol: Option 1: 20-40 min Z2 ride inside with reduced airflow. Option 2: 10-15 min sauna/hot bath immediately after training. Keep core temp elevated but manageable. Drink ~500-750 ml + 500-1000 mg sodium during exposure. Finish with only light cooling (no cold shower).\n\nEffect: Start of measurable heat adaptation, raises plasma volume. Training stress increases slightly but manageable.\n\nUse When: Medium weeks, early build phase, you want adaptation without deep fatigue."
        else:  # tier3
            heat_note = "\n\n★ UNBOUND 200 - HEAT TRAINING (Ideal - High Impact):\nProtocol: 1) Ride Outside or Indoors With Minimal Cooling: 45-75 min Z2 OR Intervals with fan on low. 2) Post-ride heat exposure: 15-25 min sauna or hot bath. 3) Hydration Target: 1-1.5 L/hr loss is OK. Replace 75% of losses within 2 hours. Sodium 1000-1500 mg/hr. 4) Avoid cooling for 20-30 min after.\n\nEffect: Maximal heat adaptation, big plasma volume gains, noticeable RPE reductions in hot races.\n\nUse When: Preparing for hot events (Unbound), you're healthy and recovered, you can afford temporary fatigue."
        unbound_notes.append(heat_note)
    
    # Hydration protocol based on duration and intensity
    if duration_minutes > 0:
        if duration_minutes < 90:
            hydration_note = "\n\n★ UNBOUND 200 - HYDRATION:\n<90 min (any intensity): 1 bottle/hr with electrolytes mandatory. Before hard efforts, take 1 gel. Light urine color (not clear) = well hydrated."
        elif duration_minutes >= 90 and not is_quality_session:
            hydration_note = "\n\n★ UNBOUND 200 - HYDRATION:\n>90 min low intensity: 60g carbs/hr. 1-1.5 bottles/hr. 600-1200 mg sodium/hr depending on heat. Monitor sweat rate—if losing >1-1.5% bodyweight, increase sodium."
        else:  # >90 min high intensity/intervals/heat
            hydration_note = "\n\n★ UNBOUND 200 - HYDRATION:\n>90 min high intensity/intervals/heat: 90g carbs/hr. 1.5 bottles/hr minimum. 1000-1500 mg sodium/hr. Aggressive cooling: ice sock, dump water, shade stops when practical. Replace ~75% of losses within 2 hours post-ride."
        unbound_notes.append(hydration_note)
    
    # Daily baseline hydration (for all workouts)
    if duration_minutes > 0:
        baseline_note = "\n\n★ UNBOUND 200 - DAILY BASELINE HYDRATION:\nStart day hydrated: ~500 ml water + 500-1000 mg sodium with breakfast. Pre-ride (60 min before): 500 ml fluid + 300-600 mg sodium. Aim for light urine color (not clear)."
        # Only add once per workout
        if 'DAILY BASELINE' not in ''.join(unbound_notes):
            unbound_notes.append(baseline_note)
    
    # Aggressive fueling (all long rides)
    if is_long_ride:
        unbound_notes.append("\n\n★ UNBOUND 200 - AGGRESSIVE FUELING:\nTarget 60-90g carbs/hour (up to 100g on dress rehearsal). Train your gut aggressively. This is critical for Unbound's long day. Competitors need aggressive fueling—race day isn't the time to discover your stomach can't handle 80g carbs/hour. Practice your race-day nutrition products. Start fueling from mile 1.")
    
    # Dress rehearsal (Week 3 Saturday)
    if is_dress_rehearsal:
        unbound_notes.append("\n\n★ UNBOUND 200 - DRESS REHEARSAL:\nTHIS IS YOUR 9-HOUR 'BLOW OUT DAY.' CLEAR YOUR SCHEDULE. This is logistics practice, fueling practice, heat practice, and mental preparation all in one. Test EVERYTHING: nutrition products, hydration system, clothing, bike setup, tire pressure. Practice eating while riding. Practice bottle handoffs. Practice pacing. For Competitors, this 9-hour ride is worth 15 shorter rides for race prep. This is the difference between finishing and performing at your best.")
    
    # Robust taper (Week 6)
    if week_num == 6:
        unbound_notes.append("\n\n★ UNBOUND 200 - ROBUST TAPER:\nFreshness/form counts for A LOT in this race. You don't want to show up half-cooked when you're going to go so deep in the well. Volume is low, but maintain sharpness. For competitive athletes, freshness is everything for a 200-mile day.")
    
    # Gravel Grit (Week 6 race day)
    name_upper = (workout_name + " " + description).upper()
    if week_num == 6 and ('RACE' in name_upper or 'RACE DAY' in name_upper):
        unbound_notes.append("\n\n★ UNBOUND 200 - GRAVEL GRIT:\nIf you've been following the Gravel Grit mental training program, this is when it pays off. You've trained your mind to push through discomfort. Trust that training. When it gets hard in the final hours, remember: everyone hurts. Who handles it better? That's you. Mental toughness is the difference between finishing and performing at your best.")
    
    return description + ''.join(unbound_notes)

def add_cadence_instructions_to_description(description, week_num, is_quality_session):
    """Add cadence work instructions to interval descriptions"""
    if not is_quality_session or week_num < 2:
        return description
    
    # Check if cadence note already exists
    if '★ CADENCE WORK:' in description or 'CADENCE WORK' in description:
        return description
    
    # Add cadence instructions for intervals
    if 'IntervalsT' in description or 'interval' in description.lower() or 'STRUCTURE:' in description:
        cadence_note = "\n\n★ CADENCE WORK (Changing Pace Foundation):\nAll intervals include cadence variation to teach your body to produce power in different ways—fundamental skill for changing pace in races. Base period: Alternate high cadence (100+ rpm, seated) and low cadence (40-60 rpm, seated). First interval: high cadence. Second: low cadence. Continue alternating. If odd number of intervals, last one is self-selected cadence. Build period: Rhythm intervals use self-selected cadence for Z3 portions, high cadence (100+ rpm) for Z4 portions. Loaded intervals: high cadence (100+ rpm) for Z5/Z6 surge, self-selected cadence for Z3 portion."
        
        # Insert before EXECUTION or READINESS CHECK if present
        if '★ EXECUTION:' in description:
            description = description.replace('★ EXECUTION:', cadence_note + '\n\n★ EXECUTION:')
        elif '• READINESS CHECK:' in description:
            description = description.replace('• READINESS CHECK:', cadence_note + '\n\n• READINESS CHECK:')
        elif '★ STRUCTURE:' in description:
            # Add after structure
            structure_end = description.find('\n\n', description.find('★ STRUCTURE:'))
            if structure_end != -1:
                description = description[:structure_end] + cadence_note + description[structure_end:]
            else:
                description = description + cadence_note
        else:
            # Add at end if no structure section
            description = description + cadence_note
    
    return description

def add_rhythm_loaded_notes(description, week_num, is_quality_session):
    """Add rhythm/loaded interval notes for Week 5 (sharpening)"""
    if week_num != 5 or not is_quality_session:
        return description
    
    if 'Rhythm' in description or 'Loaded' in description or 'Mixed' in description:
        return description  # Already has note
    
    # Add note about rhythm/loaded intervals
    rhythm_note = "\n\n★ RHYTHM/LOADED INTERVALS (SHARPENING WEEK - Changing Pace):\nSome intervals this week use Rhythm patterns (alternating 2 min Z3 + 1 min Z4, continuous) or Loaded intervals (1 min Z5/Z6 surge then settle into 14 min Z3). These train race-specific pacing—you're never jumping cleanly from Z2 to threshold in races. Rhythm intervals: 2 min Z3 (self-selected cadence, seated) + 1 min Z4 (high cadence 100+ rpm, seated), repeat × 4 reps = 1 set, do 3 sets with 5 min easy between sets. Loaded intervals: 1 min Z5/Z6 (high cadence 100+ rpm, seated) then settle into 14 min Z3 (self-selected cadence, seated). This teaches your body to change pace under load—exactly what happens in gravel races."
    
    if '★ CADENCE WORK' in description:
        # Add after cadence work
        description = description.replace('★ CADENCE WORK', '★ CADENCE WORK' + rhythm_note)
    elif '★ STRUCTURE:' in description:
        # Add after structure
        structure_end = description.find('\n\n', description.find('★ STRUCTURE:'))
        if structure_end != -1:
            description = description[:structure_end] + rhythm_note + description[structure_end:]
        else:
            description = description + rhythm_note
    else:
        description = description + rhythm_note
    
    return description

def add_cadence_to_blocks(blocks, week_num, is_quality_session):
    """Add cadence ranges to interval blocks where possible"""
    if not is_quality_session or week_num < 2:
        return blocks
    
    # For IntervalsT blocks, add cadence ranges
    # We'll add CadenceLow and CadenceHigh attributes
    def add_cadence_to_interval(match):
        full_match = match.group(0)
        # Check if cadence already specified
        if 'Cadence' in full_match:
            return full_match
        # Add cadence ranges: high cadence (100-110) and low cadence (40-60)
        # For simplicity, add both ranges in description, or add CadenceLow/CadenceHigh if ZWO supports it
        # ZWO format uses CadenceLow and CadenceHigh attributes
        if 'CadenceLow' not in full_match:
            cadence_attr = ' CadenceLow="40" CadenceHigh="110"'
            return full_match.replace(' />', cadence_attr + ' />').replace('/>', cadence_attr + ' />')
        return full_match
    
    blocks = re.sub(r'<IntervalsT[^>]*/>', add_cadence_to_interval, blocks)
    
    return blocks

def replace_sweet_spot_with_gspot(description):
    """Replace Sweet Spot references with G-Spot (87-92% FTP)"""
    description = description.replace('Sweet Spot', 'G-Spot')
    description = description.replace('sweet spot', 'G-Spot')
    description = description.replace('88-92% FTP', '87-92% FTP')
    description = description.replace('88-93% FTP', '87-92% FTP')
    return description

def estimate_workout_duration(blocks):
    """Estimate workout duration in minutes from blocks"""
    total_seconds = 0
    # Extract Duration values from blocks
    duration_matches = re.findall(r'Duration="(\d+)"', blocks)
    for duration_str in duration_matches:
        total_seconds += int(duration_str)
    return total_seconds // 60

def enhance_workout_for_unbound(workout, week_num, block_type=""):
    """Enhance workout with Unbound 200 specific modifications"""
    enhanced = workout.copy()
    
    # Skip actual rest days for modifications (but not "RACE or REST" type workouts)
    name_upper = workout['name'].upper()
    if 'RACE' in name_upper:
        pass
    elif 'REST' in name_upper and (' - REST' in name_upper or name_upper.startswith('REST') or name_upper.endswith('REST')):
        return enhanced
    
    # Replace Sweet Spot with G-Spot in both name and description
    enhanced['name'] = enhanced['name'].replace('Sweet Spot', 'G-Spot')
    enhanced['description'] = replace_sweet_spot_with_gspot(enhanced['description'])
    
    # Determine workout type
    is_long_ride = 'Long' in workout['name'] or ('hours' in workout['description'] and ('5' in workout['description'] or '6' in workout['description'] or '7' in workout['description'] or '8' in workout['description'] or '9' in workout['description']))
    is_quality_session = 'Hard Session' in workout['name'] or 'Quality' in workout['name'] or 'Threshold' in workout['name'] or 'VO2max' in workout['name'] or 'Mixed' in workout['name'] or 'Race' in workout['name'] or 'Simulation' in workout['name'] or 'G-Spot' in workout['name'] or 'Gspot' in workout['name'] or 'Sweet Spot' in workout['name'] or 'Tempo' in workout['name'] or 'Peak' in workout['name']
    is_dress_rehearsal = week_num == 3 and 'Sat' in workout['name'] and ('Long' in workout['name'] or 'Volume' in workout['name'] or 'Simulation' in workout['name'])
    
    # Estimate duration for hydration protocol
    duration_minutes = estimate_workout_duration(workout['blocks'])
    
    # Add cadence instructions to description
    enhanced['description'] = add_cadence_instructions_to_description(
        enhanced['description'],
        week_num,
        is_quality_session
    )
    
    # Add cadence ranges to blocks where possible
    enhanced['blocks'] = add_cadence_to_blocks(
        enhanced['blocks'],
        week_num,
        is_quality_session
    )
    
    # Add rhythm/loaded interval notes for Week 5
    enhanced['description'] = add_rhythm_loaded_notes(
        enhanced['description'],
        week_num,
        is_quality_session
    )
    
    # Add Unbound notes (with duration for hydration protocol and workout name for Gravel Grit)
    enhanced['description'] = add_unbound_notes_to_description(
        enhanced['description'],
        week_num,
        is_long_ride=is_long_ride,
        is_quality_session=is_quality_session,
        is_dress_rehearsal=is_dress_rehearsal,
        duration_minutes=duration_minutes,
        workout_name=workout['name']
    )
    
    # Week 3 Saturday: Modify to 9-hour dress rehearsal (for all block types)
    if is_dress_rehearsal:
        enhanced['name'] = 'W03 Sat - 9 Hour Dress Rehearsal'
        # Update description structure for 9-hour ride
        if '★ STRUCTURE:' in enhanced['description']:
            enhanced['description'] = enhanced['description'].replace(
                '★ STRUCTURE:',
                '★ STRUCTURE:\n9-HOUR DRESS REHEARSAL: First 3 hours Z2 (65-75% FTP) → Rhythm Interval Block in hour 4: (2 min Z3 + 1 min Z4) × 4 reps × 3 sets with 5 min easy between sets → Hours 5-6: Easy Z2, practice aggressive fueling (80-100g carbs/hour) → Hour 7: Loaded intervals (1 min Z5/Z6 surge then 14 min Z3) × 2 with 8 min easy between → Hours 8-9: Easy Z2 to finish.\n\nORIGINAL STRUCTURE:'
            )
        else:
            # Add structure if not present
            enhanced['description'] = '★ STRUCTURE:\n9-HOUR DRESS REHEARSAL: First 3 hours Z2 (65-75% FTP) → Rhythm Interval Block in hour 4: (2 min Z3 + 1 min Z4) × 4 reps × 3 sets with 5 min easy between sets → Hours 5-6: Easy Z2, practice aggressive fueling (80-100g carbs/hour) → Hour 7: Loaded intervals (1 min Z5/Z6 surge then 14 min Z3) × 2 with 8 min easy between → Hours 8-9: Easy Z2 to finish.\n\n' + enhanced['description']
        
        # Update blocks to 9-hour structure (32400 seconds = 9 hours)
        # Structure: 3h Z2 → Rhythm intervals → 2h Z2 → Loaded intervals → 2h Z2
        enhanced['blocks'] = '''    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="10800" Power="0.68" Cadence="85"/>
    <SteadyState Duration="180" Power="0.80" Cadence="90"/>
    <SteadyState Duration="120" Power="0.95" Cadence="100"/>
    <SteadyState Duration="180" Power="0.80" Cadence="90"/>
    <SteadyState Duration="120" Power="0.95" Cadence="100"/>
    <SteadyState Duration="180" Power="0.80" Cadence="90"/>
    <SteadyState Duration="120" Power="0.95" Cadence="100"/>
    <SteadyState Duration="180" Power="0.80" Cadence="90"/>
    <SteadyState Duration="120" Power="0.95" Cadence="100"/>
    <SteadyState Duration="300" Power="0.55"/>
    <SteadyState Duration="180" Power="0.80" Cadence="90"/>
    <SteadyState Duration="120" Power="0.95" Cadence="100"/>
    <SteadyState Duration="180" Power="0.80" Cadence="90"/>
    <SteadyState Duration="120" Power="0.95" Cadence="100"/>
    <SteadyState Duration="180" Power="0.80" Cadence="90"/>
    <SteadyState Duration="120" Power="0.95" Cadence="100"/>
    <SteadyState Duration="180" Power="0.80" Cadence="90"/>
    <SteadyState Duration="120" Power="0.95" Cadence="100"/>
    <SteadyState Duration="300" Power="0.55"/>
    <SteadyState Duration="180" Power="0.80" Cadence="90"/>
    <SteadyState Duration="120" Power="0.95" Cadence="100"/>
    <SteadyState Duration="180" Power="0.80" Cadence="90"/>
    <SteadyState Duration="120" Power="0.95" Cadence="100"/>
    <SteadyState Duration="180" Power="0.80" Cadence="90"/>
    <SteadyState Duration="120" Power="0.95" Cadence="100"/>
    <SteadyState Duration="180" Power="0.80" Cadence="90"/>
    <SteadyState Duration="120" Power="0.95" Cadence="100"/>
    <SteadyState Duration="7200" Power="0.68" Cadence="85"/>
    <SteadyState Duration="60" Power="1.20" Cadence="100"/>
    <SteadyState Duration="840" Power="0.80" Cadence="90"/>
    <SteadyState Duration="480" Power="0.55"/>
    <SteadyState Duration="60" Power="1.20" Cadence="100"/>
    <SteadyState Duration="840" Power="0.80" Cadence="90"/>
    <SteadyState Duration="7200" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
'''
    
    return enhanced

def create_workout(template_path, name, description, workout_blocks, output_path):
    """
    Create TrainingPeaks-compatible ZWO file
    """
    import html
    
    # Load template in binary mode
    with open(template_path, 'rb') as f:
        content = f.read()
    
    # Escape XML special characters
    name_escaped = html.escape(name, quote=False)
    description_escaped = html.escape(description, quote=False)
    
    # Replace NAME tag
    old_name = b'<name>W01 Tue - FTP Test</name>'
    new_name = f'<name>{name_escaped}</name>'.encode('utf-8')
    content = content.replace(old_name, new_name)
    
    # Replace description
    desc_start = content.find(b'<description>')
    desc_end = content.find(b'</description>')
    if desc_start != -1 and desc_end != -1:
        desc_end += len(b'</description>')
        old_desc = content[desc_start:desc_end]
        new_desc = f'<description>{description_escaped}</description>'.encode('utf-8')
        content = content.replace(old_desc, new_desc)
    
    # Replace workout section
    workout_start = content.find(b'<workout>')
    workout_end = content.find(b'</workout>')
    if workout_start != -1 and workout_end != -1:
        newline_pos = content.rfind(b'\n', max(0, workout_start - 20), workout_start)
        if newline_pos == -1:
            newline_pos = workout_start - 10
        workout_end += len(b'</workout>')
        old_workout = content[newline_pos + 1:workout_end]
        new_workout = f'      <workout>\n{workout_blocks}  </workout>'.encode('utf-8')
        content = content[:newline_pos + 1] + new_workout + content[workout_end:]
    
    # Write in binary mode
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(content)
    
    print(f"✓ Created: {name}")
    return True

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Configuration
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, 'W01_Tue_-_FTP_Test.zwo')
    output_dir = os.path.join(script_dir, 'generated_workouts_compete_savemyrace_unbound200')
    
    # Verify template exists
    if not os.path.exists(template_path):
        print(f"ERROR: Template not found at {template_path}")
        print("\nPlease update template_path in the script to point to your working template file.")
        exit(1)
    
    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("COMPETE SAVE MY RACE - 6 WEEK EMERGENCY PLAN")
    print("UNBOUND 200 MODIFIED")
    print("=" * 60)
    print("\nTraining Philosophy: Block Periodization (Compressed) + Cadence Work + Rhythm Intervals")
    print("Target: 15-18 hours/week")
    print("Goal: Convert existing race fitness into peak competitive performance")
    print("Race: Unbound 200 (heat, long day, logistics-heavy)")
    print("\nUNBOUND 200 ENHANCEMENTS:")
    print("  ✓ Heat training emphasis (Weeks 2-5, quality sessions)")
    print("  ✓ Aggressive fueling practice (60-90g carbs/hour on long rides)")
    print("  ✓ Dress rehearsal: 9-hour ride in Week 3 Saturday (~3 weeks before race)")
    print("  ✓ Robust taper (Week 6)")
    print("  ✓ Gravel Grit integration (Week 6 race day)")
    print("  ✓ Cadence work: High (100+ rpm) & Low (40-60 rpm) on all intervals")
    print("  ✓ Rhythm/Mixed intervals in Week 5 (sharpening)")
    print("  ✓ Loaded intervals in Week 5 (sharpening)")
    print("  ✓ G-Spot (87-92% FTP) replaces Sweet Spot")
    print("=" * 60)
    print("\nNOTE: Weeks 2-3 have 3 block options (VO2max, Threshold, Durability)")
    print("All three options will be generated. Choose the one matching your limiter.")
    print("=" * 60)
    
    total_workouts = 0
    
    # Week 1: Rapid Assessment (7 workouts)
    print("\n🔧 WEEK 1: Rapid Assessment & Block Planning")
    for workout in week_1:
        enhanced = enhance_workout_for_unbound(workout, 1)
        output_path = os.path.join(output_dir, f"{enhanced['name'].replace(' ', '_').replace('/', '_').replace('#', '')}.zwo")
        create_workout(
            template_path=template_path,
            name=enhanced['name'],
            description=enhanced['description'],
            workout_blocks=enhanced['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 1 complete: {len(week_1)} files generated")
    
    # Week 2: OPTION A - VO2max Block (7 workouts)
    print("\n🔧 WEEK 2: OPTION A - VO2max Block")
    for workout in week_2_vo2max:
        enhanced = enhance_workout_for_unbound(workout, 2, "VO2max")
        base_name = enhanced['name'].replace(' ', '_').replace('/', '_').replace('#', '')
        if '_VO2MAX' not in base_name:
            base_name += '_VO2max'
        output_path = os.path.join(output_dir, f"{base_name}.zwo")
        create_workout(
            template_path=template_path,
            name=enhanced['name'],
            description=enhanced['description'],
            workout_blocks=enhanced['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 2 VO2max complete: {len(week_2_vo2max)} files generated")
    
    # Week 2: OPTION B - Threshold Block (7 workouts)
    print("\n🔧 WEEK 2: OPTION B - Threshold Block")
    for workout in week_2_threshold:
        enhanced = enhance_workout_for_unbound(workout, 2, "Threshold")
        base_name = enhanced['name'].replace(' ', '_').replace('/', '_').replace('#', '')
        if '_THRESHOLD' not in base_name:
            base_name += '_Threshold'
        output_path = os.path.join(output_dir, f"{base_name}.zwo")
        create_workout(
            template_path=template_path,
            name=enhanced['name'],
            description=enhanced['description'],
            workout_blocks=enhanced['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 2 Threshold complete: {len(week_2_threshold)} files generated")
    
    # Week 2: OPTION C - Durability Block (7 workouts)
    print("\n🔧 WEEK 2: OPTION C - Durability Block")
    for workout in week_2_durability:
        enhanced = enhance_workout_for_unbound(workout, 2, "Durability")
        base_name = enhanced['name'].replace(' ', '_').replace('/', '_').replace('#', '')
        if '_DURABILITY' not in base_name:
            base_name += '_Durability'
        output_path = os.path.join(output_dir, f"{base_name}.zwo")
        create_workout(
            template_path=template_path,
            name=enhanced['name'],
            description=enhanced['description'],
            workout_blocks=enhanced['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 2 Durability complete: {len(week_2_durability)} files generated")
    
    # Week 3: OPTION A - VO2max Block Peak (7 workouts)
    print("\n🔧 WEEK 3: OPTION A - VO2max Block Peak Loading")
    print("  (Week 3 Saturday = 9-HOUR DRESS REHEARSAL)")
    for workout in week_3_vo2max:
        enhanced = enhance_workout_for_unbound(workout, 3, "VO2max")
        base_name = enhanced['name'].replace(' ', '_').replace('/', '_').replace('#', '')
        if '_VO2MAX' not in base_name:
            base_name += '_VO2max'
        output_path = os.path.join(output_dir, f"{base_name}.zwo")
        create_workout(
            template_path=template_path,
            name=enhanced['name'],
            description=enhanced['description'],
            workout_blocks=enhanced['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 3 VO2max complete: {len(week_3_vo2max)} files generated")
    
    # Week 3: OPTION B - Threshold Block Peak (7 workouts)
    print("\n🔧 WEEK 3: OPTION B - Threshold Block Peak Loading")
    print("  (Week 3 Saturday = 9-HOUR DRESS REHEARSAL)")
    for workout in week_3_threshold:
        enhanced = enhance_workout_for_unbound(workout, 3, "Threshold")
        base_name = enhanced['name'].replace(' ', '_').replace('/', '_').replace('#', '')
        if '_THRESHOLD' not in base_name:
            base_name += '_Threshold'
        output_path = os.path.join(output_dir, f"{base_name}.zwo")
        create_workout(
            template_path=template_path,
            name=enhanced['name'],
            description=enhanced['description'],
            workout_blocks=enhanced['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 3 Threshold complete: {len(week_3_threshold)} files generated")
    
    # Week 3: OPTION C - Durability Block Peak (7 workouts)
    print("\n🔧 WEEK 3: OPTION C - Durability Block Peak Loading")
    print("  (Week 3 Saturday = 9-HOUR DRESS REHEARSAL)")
    for workout in week_3_durability:
        enhanced = enhance_workout_for_unbound(workout, 3, "Durability")
        base_name = enhanced['name'].replace(' ', '_').replace('/', '_').replace('#', '')
        if '_DURABILITY' not in base_name:
            base_name += '_Durability'
        output_path = os.path.join(output_dir, f"{base_name}.zwo")
        create_workout(
            template_path=template_path,
            name=enhanced['name'],
            description=enhanced['description'],
            workout_blocks=enhanced['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 3 Durability complete: {len(week_3_durability)} files generated")
    
    # Week 4: Recovery & Transmutation (7 workouts)
    print("\n🔧 WEEK 4: Recovery & Transmutation")
    for workout in week_4:
        enhanced = enhance_workout_for_unbound(workout, 4)
        output_path = os.path.join(output_dir, f"{enhanced['name'].replace(' ', '_').replace('/', '_').replace('#', '')}.zwo")
        create_workout(
            template_path=template_path,
            name=enhanced['name'],
            description=enhanced['description'],
            workout_blocks=enhanced['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 4 complete: {len(week_4)} files generated")
    
    # Week 5: Race Sharpening (7 workouts)
    print("\n🔧 WEEK 5: Race Sharpening - Mixed Intensity (with Rhythm/Loaded Intervals)")
    for workout in week_5:
        enhanced = enhance_workout_for_unbound(workout, 5)
        output_path = os.path.join(output_dir, f"{enhanced['name'].replace(' ', '_').replace('/', '_').replace('#', '')}.zwo")
        create_workout(
            template_path=template_path,
            name=enhanced['name'],
            description=enhanced['description'],
            workout_blocks=enhanced['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 5 complete: {len(week_5)} files generated")
    
    # Week 6: Race Week (7 workouts)
    print("\n🔧 WEEK 6: Race Week - Taper & Compete (with Gravel Grit)")
    for workout in week_6:
        enhanced = enhance_workout_for_unbound(workout, 6)
        output_path = os.path.join(output_dir, f"{enhanced['name'].replace(' ', '_').replace('/', '_').replace('#', '')}.zwo")
        create_workout(
            template_path=template_path,
            name=enhanced['name'],
            description=enhanced['description'],
            workout_blocks=enhanced['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 6 complete: {len(week_6)} files generated")
    
    print("\n" + "=" * 60)
    print(f"🎉 GENERATION COMPLETE - UNBOUND 200 MODIFIED!")
    print(f"Total files generated: {total_workouts}")
    print(f"Output directory: {output_dir}")
    print("=" * 60)
    print("\nPLAN STRUCTURE:")
    print("  ✓ Week 1: Rapid Assessment & Block Planning")
    print("  ✓ Weeks 2-3: Concentrated Loading Block (choose ONE option)")
    print("    - Option A: VO2max Block")
    print("    - Option B: Threshold Block")
    print("    - Option C: Durability Block (G-Spot replaces Sweet Spot)")
    print("    - Week 3 Saturday: 9-HOUR DRESS REHEARSAL (all options)")
    print("  ✓ Week 4: Recovery & Transmutation")
    print("  ✓ Week 5: Race Sharpening (Rhythm/Loaded intervals)")
    print("  ✓ Week 6: Race Week - Robust Taper & Compete (Gravel Grit)")
    print("\nUNBOUND 200 MODIFICATIONS:")
    print("  ✓ Heat training: Weeks 2-5, all quality sessions (3-tier system)")
    print("  ✓ Aggressive fueling: 60-90g carbs/hour on all long rides")
    print("  ✓ Dress rehearsal: 9-hour ride Week 3 Saturday (~3 weeks before race)")
    print("  ✓ Robust taper: Week 6 volume reduced for freshness")
    print("  ✓ Gravel Grit: Mental toughness training referenced Week 6")
    print("\nKEY FEATURES:")
    print("  ✓ Block Periodization (compressed, 6 weeks)")
    print("  ✓ Cadence work: High (100+ rpm) & Low (40-60 rpm) on all intervals")
    print("  ✓ Rhythm/Mixed intervals in Week 5 (race simulation)")
    print("  ✓ Loaded intervals in Week 5 (Z5/Z6 surge into Z3)")
    print("  ✓ G-Spot (87-92% FTP) replaces Sweet Spot (88-93% FTP)")
    print("=" * 60)
    print("\nIMPORTANT: You have 3 block options for Weeks 2-3:")
    print("  - VO2max Block: Use files ending in '_VO2max'")
    print("  - Threshold Block: Use files ending in '_Threshold'")
    print("  - Durability Block: Use files ending in '_Durability'")
    print("\nChoose ONE block path based on your Week 1 assessment.")
    print("Delete the other two block options before uploading to TrainingPeaks.")
    print("\nNEXT STEPS:")
    print("1. Review Week 1 assessment results")
    print("2. Choose your block path (VO2max, Threshold, or Durability)")
    print("3. Delete the other two block options from generated files")
    print("4. Test upload ONE file to TrainingPeaks first")
    print("5. If successful, upload all files for your chosen path")
    print("6. Organize workouts into your plan")
    print("7. Publish your Compete Save My Race Unbound 200 plan!")

