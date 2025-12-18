#!/usr/bin/env python3
"""
Workout Enhancement Functions
- Add URLs to all exercises (replace gravelgod.com/demos)
- Estimate workout duration
- Add workout context (previous/next workout connections)
"""

import re
from exercise_lookup import get_video_url

# Warmup/Cooldown exercise mappings
WARMUP_COOLDOWN_EXERCISES = {
    "Downward Dog Lunge + Rotation": "https://vimeo.com/111032509",  # Using split jump as closest match
    "Tripod Bridge": "https://vimeo.com/111033887",  # Glute Bridge
    "Curtsy Lunges": "https://vimeo.com/111043982",  # Split Squat
    "Lateral Lunges": "https://vimeo.com/111032894",  # Alternating Lateral Lunge Walk
    "Cat-Cow": "https://vimeo.com/111048715",  # Bird Dog (mobility)
    "World's Greatest Stretch": "https://www.youtube.com/watch?v=-CiWQ2IvY34",
    "Lying Windshield Wipers": "https://vimeo.com/111109110",  # Dead Bug (core mobility)
    "Bird Dog": "https://vimeo.com/111048715",
    "Hip Rails": "https://vimeo.com/111033887",  # Glute Bridge
    "MiniBand Marches": "https://vimeo.com/111033318",  # Band Stomp
    "Glute Activation (Clamshells)": "https://www.youtube.com/watch?v=V_AnVxKPFlY",
    "Monster Walk": "https://vimeo.com/111033318",  # Band Stomp
    "Hip Circles (quadruped)": "https://vimeo.com/111048715",  # Bird Dog
    "Hip Circles (standing)": "https://vimeo.com/111032509",  # Split Jump
    "Deep Squat Sit": "https://vimeo.com/111129796",  # Goblet Squat
    "Hip Flexor Stretch": "https://vimeo.com/111032509",  # Split Jump
    "Pigeon Pose": "https://vimeo.com/111032509",  # Split Jump
    "90-90 Hip Stretch": "https://vimeo.com/111032509",  # Split Jump
    "Supine Spinal Twist": "https://vimeo.com/111109110",  # Dead Bug
    "Child's Pose": "https://vimeo.com/111048715",  # Bird Dog
    "Light Jog in Place": "https://vimeo.com/111032509",  # Split Jump
    "Leg Swings": "https://vimeo.com/111032509",  # Split Jump
    "Air Squat": "https://vimeo.com/111129796",  # Goblet Squat
    "Dead Hang or Lat Stretch": "https://vimeo.com/111241988",  # Inverted Row
}

def add_urls_to_all_exercises(description):
    """
    Replace 'gravelgod.com/demos' references with actual video URLs
    
    Args:
        description: Workout description text
    
    Returns:
        Description with all exercises having URLs
    """
    # Remove the "→ All demos: gravelgod.com/demos" text from headers
    description = re.sub(
        r' → All demos: gravelgod\.com/demos',
        '',
        description
    )
    
    # Split into lines and process
    lines = description.split('\n')
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is an exercise line (starts with •)
        if line.strip().startswith('•'):
            result_lines.append(line)
            
            # Check if next line already has a URL
            if i + 1 < len(lines) and '→' in lines[i + 1] and 'http' in lines[i + 1]:
                # Already has URL, keep it
                result_lines.append(lines[i + 1])
                i += 2
                continue
            
            # Extract exercise name (handle leading spaces and bullet)
            # Pattern: optional whitespace, bullet, whitespace, exercise name, optional dash and rest
            exercise_match = re.search(r'•\s*([^─\n]+?)(?:\s*─|$)', line)
            if exercise_match:
                exercise_name = exercise_match.group(1).strip()
                # Remove parenthetical notes for matching
                exercise_name_clean = re.sub(r'\s*\([^)]+\)', '', exercise_name).strip()
                
                # Try to find URL - check exact match first
                url = None
                if exercise_name_clean in WARMUP_COOLDOWN_EXERCISES:
                    url = WARMUP_COOLDOWN_EXERCISES[exercise_name_clean]
                else:
                    # Try partial match (exercise name contains dictionary key)
                    for key, value in WARMUP_COOLDOWN_EXERCISES.items():
                        if key.lower() in exercise_name_clean.lower() or exercise_name_clean.lower() in key.lower():
                            url = value
                            break
                    
                    # If still no match, try fuzzy match via library
                    if not url:
                        try:
                            url = get_video_url(exercise_name_clean)
                        except:
                            pass
                
                if url:
                    # Add URL line
                    result_lines.append(f"     → {url}")
        
        else:
            result_lines.append(line)
        
        i += 1
    
    return '\n'.join(result_lines)

def add_urls_to_section(section_text):
    """Add URLs to exercises in a section (warmup/cooldown)"""
    lines = section_text.split('\n')
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        result_lines.append(line)
        
        # Check if this is an exercise line (starts with •)
        if line.strip().startswith('•'):
            # Check if next line has a URL
            if i + 1 < len(lines) and '→' in lines[i + 1] and 'http' in lines[i + 1]:
                # Already has URL, skip
                result_lines.append(lines[i + 1])
                i += 2
                continue
            
            # Extract exercise name
            exercise_match = re.match(r'•\s*([^─]+?)(?:\s*─|$)', line)
            if exercise_match:
                exercise_name = exercise_match.group(1).strip()
                # Remove parenthetical notes for matching
                exercise_name_clean = re.sub(r'\s*\([^)]+\)', '', exercise_name).strip()
                
                # Try to find URL
                url = None
                if exercise_name_clean in WARMUP_COOLDOWN_EXERCISES:
                    url = WARMUP_COOLDOWN_EXERCISES[exercise_name_clean]
                else:
                    # Try fuzzy match
                    url = get_video_url(exercise_name_clean)
                
                if url:
                    # Add URL line
                    result_lines.append(f"     → {url}")
        
        i += 1
    
    return '\n'.join(result_lines)

def estimate_workout_duration(description):
    """
    Estimate workout duration based on Main 1 and Main 2 exercises
    
    CONSERVATIVE ESTIMATION - accounts for:
    - Video watching (athletes checking form)
    - Setup/transition time between exercises
    - Form checks and rest periods
    
    Duration calculation:
    - Warmup: Fixed (8-10 min) + 2 min buffer for video watching
    - Prep: Fixed (5 min) + 1 min buffer
    - Main 1: Sets × (60s exercise time + rest) + 3 min setup/video buffer
    - Main 2: Sets × (60s exercise time + rest) + 3 min setup/video buffer
    - Core (if present): Sets × (rep time + rest) + 2 min buffer
    - Cooldown: Fixed (5 min)
    - Additional 5 min buffer for overall transitions
    
    Returns:
        Estimated duration in minutes (conservative)
    """
    duration = 0
    
    # Warmup (8-10 min) + buffer for video watching
    if '★ WARMUP' in description:
        warmup_match = re.search(r'★ WARMUP\s*\((\d+)\s*min\)', description)
        if warmup_match:
            duration += int(warmup_match.group(1))
        else:
            duration += 8  # Default
        duration += 2  # Buffer for video watching
    
    # Prep (5 min) + buffer
    if '★ PREP' in description:
        prep_match = re.search(r'★ PREP\s*\((\d+)\s*min\)', description)
        if prep_match:
            duration += int(prep_match.group(1))
        else:
            duration += 5  # Default
        duration += 1  # Buffer for setup
    
    # Main 1 - More conservative: 60s per set (includes video checks, form review)
    main1_match = re.search(r'★ MAIN 1:.*?│\s*(\d+)\s*sets.*?│\s*(\d+)s\s*rest', description)
    if main1_match:
        sets = int(main1_match.group(1))
        rest_sec = int(main1_match.group(2))
        # Conservative: 60s per set (exercise + form checks) + rest time
        main1_time = sets * (60 + rest_sec) / 60  # Convert to minutes
        duration += main1_time
        duration += 3  # Buffer for video watching and setup
    
    # Main 2 - More conservative: 60s per set
    main2_match = re.search(r'★ MAIN 2:.*?│\s*(\d+)\s*sets.*?│\s*(\d+)s\s*rest', description)
    if main2_match:
        sets = int(main2_match.group(1))
        rest_sec = int(main2_match.group(2))
        main2_time = sets * (60 + rest_sec) / 60
        duration += main2_time
        duration += 3  # Buffer for video watching and setup
    
    # Core (if present) + buffer
    core_match = re.search(r'★ CORE\s*\((\d+)\s*min\)', description)
    if core_match:
        duration += int(core_match.group(1))
        duration += 2  # Buffer
    
    # Cooldown (5 min)
    if '★ COOLDOWN' in description:
        cooldown_match = re.search(r'★ COOLDOWN\s*\((\d+)\s*min\)', description)
        if cooldown_match:
            duration += int(cooldown_match.group(1))
        else:
            duration += 5  # Default
    
    # Additional buffer for overall transitions and video watching
    duration += 5
    
    # Round UP to nearest 5 minutes, minimum 40 min
    duration_rounded = max(40, ((int(duration) + 4) // 5) * 5)
    
    return int(duration_rounded)

def get_workout_context(week, template_key, plan_weeks, get_pathway_name_func, strength_schedule):
    """
    Generate context about previous and next workouts
    
    Args:
        week: Current week number
        template_key: Current template key
        plan_weeks: Total plan weeks
        get_pathway_name_func: Function to get pathway name from template key
        strength_schedule: STRENGTH_SCHEDULE dictionary
    
    Returns:
        Context string about progression
    """
    pathway_name = get_pathway_name_func(template_key)
    
    # Extract session letter
    session = "A"
    if "_B_" in template_key or template_key.endswith("_B"):
        session = "B"
    
    context_parts = []
    
    # Previous workout context
    if week > 1:
        prev_week = week - 1
        # Find previous template
        if prev_week in strength_schedule:
            prev_sessions = strength_schedule[prev_week]
            # Find the other session from same week, or previous week's same session
            if session == "A":
                # Previous was B from previous week (most recent workout)
                # Look for session B in previous week
                prev_template = None
                for day, key in prev_sessions:
                    if "_B_" in key or key.endswith("_B"):
                        prev_template = key
                        break
                # If no B found, use A from previous week
                if not prev_template:
                    for day, key in prev_sessions:
                        if "_A_" in key or key.endswith("_A"):
                            prev_template = key
                            break
            else:
                # Previous was A from same week
                prev_template = None
                for day, key in prev_sessions:
                    if "_A_" in key or key.endswith("_A"):
                        prev_template = key
                        break
                
                if not prev_template and prev_week > 1:
                    # Look at previous week
                    if prev_week - 1 in strength_schedule:
                        for day, key in strength_schedule[prev_week - 1]:
                            if "_B_" in key or key.endswith("_B"):
                                prev_template = key
                                break
            
            if prev_template:
                prev_pathway = get_pathway_name_func(prev_template)
                if prev_pathway != pathway_name:
                    context_parts.append(f"Building on {prev_pathway} from last week.")
                else:
                    context_parts.append("Continuing this phase's progression.")
    
    # Next workout context
    if week < plan_weeks:
        next_week = week + 1
        if next_week in strength_schedule:
            next_sessions = strength_schedule[next_week]
            next_template = None
            for day, key in next_sessions:
                if (session == "A" and ("_B_" in key or key.endswith("_B"))) or \
                   (session == "B" and ("_A_" in key or key.endswith("_A"))):
                    next_template = key
                    break
            
            if next_template:
                next_pathway = get_pathway_name_func(next_template)
                if next_pathway != pathway_name:
                    context_parts.append(f"Next week transitions to {next_pathway}.")
                else:
                    context_parts.append("Next session continues this phase.")
    
    if context_parts:
        return " ".join(context_parts)
    
    return None

# Note: get_pathway_name and STRENGTH_SCHEDULE will be passed as parameters
# to avoid circular imports

