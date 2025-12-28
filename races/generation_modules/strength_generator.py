#!/usr/bin/env python3
"""
Strength ZWO Generator
Generates TrainingPeaks-compatible strength workout ZWO files
"""

import os
import html
import re
from pathlib import Path

# Import exercise lookup (optional - will validate exercises if available)
try:
    from exercise_lookup import get_video_url, validate_exercise_urls
    EXERCISE_LIBRARY_AVAILABLE = True
except ImportError:
    EXERCISE_LIBRARY_AVAILABLE = False
    print("⚠️  Exercise library not available - URLs will not be validated")

# Import workout enhancements
try:
    from workout_enhancements import (
        add_urls_to_all_exercises,
        estimate_workout_duration,
        get_workout_context
    )
    WORKOUT_ENHANCEMENTS_AVAILABLE = True
except ImportError:
    WORKOUT_ENHANCEMENTS_AVAILABLE = False
    print("⚠️  Workout enhancements not available - some features disabled")

# ZWO Template structure (same as zwo_generator.py)
ZWO_TEMPLATE = """<?xml version='1.0' encoding='UTF-8'?>
<workout_file>
  <author>Gravel God Training</author>
  <name>{name}</name>
  <description>{description}</description>
  <sportType>bike</sportType>
  <tags/>
  <workout>
{blocks}  </workout>
</workout_file>"""

# Pathway name mapping
PATHWAY_NAMES = {
    "RED": "Learn to Lift",
    "YELLOW": "Lift Heavy Sh*t",
    "GREEN": "Lift Fast",
    "GREEN_MAINT": "Don't Lose It"
}

# Strength phase definitions with taglines
STRENGTH_PHASES = {
    "Learn to Lift": {
        "weeks": "1-6",
        "code": "AA",
        "focus": "Anatomical Adaptation",
        "rpe": "5-6",
        "tagline_short": "Movement quality before load.",
        "tagline_one_liner": "Get the patterns right.",
        "tagline_full": "Yes, you need this. Build the movement patterns that keep you injury-free and make the heavy stuff possible. Nobody's impressed by your deadlift if you're doing it wrong.",
        "equipment": "Bodyweight, bands, light DB/KB"
    },
    "Lift Heavy Sh*t": {
        "weeks": "7-12",
        "code": "MT/MS",
        "focus": "Hypertrophy/Max Strength",
        "rpe": "6-8",
        "tagline_short": "Progressive overload. Real weight.",
        "tagline_one_liner": "Get strong.",
        "tagline_full": "This is where strength actually happens. Progressive overload, compound movements, real weight. Your legs already know how to spin circles — teach them to produce force.",
        "equipment": "Barbell, DB, bench"
    },
    "Lift Fast": {
        "weeks": "13-18",
        "code": "SM",
        "focus": "Power/Conversion",
        "rpe": "5-7",
        "tagline_short": "Power you can actually use.",
        "tagline_one_liner": "Get explosive.",
        "tagline_full": "Strength you can't access quickly is useless at hour six. Convert your gym gains into explosive power that actually shows up when you need to punch over a climb or close a gap.",
        "equipment": "DB, KB, bands, bodyweight"
    },
    "Don't Lose It": {
        "weeks": "19-20",
        "code": "Maint",
        "focus": "Maintenance/Taper",
        "rpe": "5-6",
        "tagline_short": "Maintain. Don't detrain.",
        "tagline_one_liner": "Stay ready.",
        "tagline_full": "Two weeks out isn't the time to PR your squat. Minimum effective dose to hold your adaptations while your legs freshen up for race day. Touch it, don't crush it.",
        "equipment": "Bodyweight, bands, light DB"
    }
}

# Strength schedule mapping (week → [(day, template_key), ...])
STRENGTH_SCHEDULE = {
    1: [("Mon", "RED_A_PHASE1"), ("Thu", "RED_B_PHASE1")],
    2: [("Mon", "RED_A_PHASE1"), ("Thu", "RED_B_PHASE1")],
    3: [("Mon", "RED_A_PHASE2"), ("Thu", "RED_B_PHASE2")],
    4: [("Mon", "RED_A_PHASE2"), ("Thu", "RED_B_PHASE2")],
    5: [("Mon", "RED_A_PHASE3"), ("Thu", "RED_B_PHASE3")],
    6: [("Mon", "RED_A_PHASE3"), ("Thu", "RED_B_PHASE3")],
    7: [("Mon", "YELLOW_A_HYPER"), ("Thu", "YELLOW_B_HYPER")],
    8: [("Mon", "YELLOW_A_HYPER"), ("Thu", "YELLOW_B_HYPER")],
    9: [("Mon", "YELLOW_A_HYPER"), ("Thu", "YELLOW_B_HYPER")],
    10: [("Mon", "YELLOW_A_MAX"), ("Thu", "YELLOW_B_MAX")],
    11: [("Mon", "YELLOW_A_MAX"), ("Thu", "YELLOW_B_MAX")],
    12: [("Mon", "YELLOW_A_MAX"), ("Thu", "YELLOW_B_MAX")],
    13: [("Mon", "GREEN_A_POWER"), ("Thu", "GREEN_B_POWER")],
    14: [("Mon", "GREEN_A_POWER"), ("Thu", "GREEN_B_POWER")],
    15: [("Mon", "GREEN_A_POWER"), ("Thu", "GREEN_B_POWER")],
    16: [("Mon", "GREEN_A_POWER"), ("Thu", "GREEN_B_POWER")],
    17: [("Mon", "GREEN_A_CONV"), ("Thu", "GREEN_B_CONV")],
    18: [("Mon", "GREEN_A_CONV"), ("Thu", "GREEN_B_CONV")],
    19: [("Mon", "GREEN_A_MAINT")],
    20: [("Mon", "GREEN_B_MAINT")]
}

def load_strength_templates(templates_file_path):
    """
    Load strength templates from MASTER_TEMPLATES_V2.md
    
    Returns dict mapping template_key -> description_text
    """
    import re
    
    with open(templates_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    templates = {}
    
    # Find all template sections: ## KEY followed by ``` on next line
    # Capture everything until the closing ```
    # Pattern: ## KEY (can include numbers) newline, ``` newline, content, newline ```
    # Use [A-Z0-9_] to include numbers in the key
    pattern = r'##\s*([A-Z0-9_]+)\s*\n```\s*\n(.*?)\n```'
    
    # Find all matches with DOTALL flag to match across newlines
    matches = re.finditer(pattern, content, re.DOTALL | re.MULTILINE)
    
    for match in matches:
        key = match.group(1).strip()
        template_text = match.group(2).strip()
        
        # Only process valid template keys (must have underscore and be > 3 chars)
        # Filter out single letters like "P" or "M" that might match
        # Must match expected pattern: PATHWAY_SESSION_PHASE or PATHWAY_SESSION_TYPE
        if (len(key) > 3 and '_' in key and template_text and len(template_text) > 50 and
            any(pathway in key for pathway in ['RED', 'YELLOW', 'GREEN'])):
            templates[key] = template_text
    
    return templates

def get_pathway_name(template_key):
    """Extract pathway name from template key"""
    # Check for maintenance first (more specific)
    if "MAINT" in template_key:
        return PATHWAY_NAMES["GREEN_MAINT"]
    elif "RED" in template_key:
        return PATHWAY_NAMES["RED"]
    elif "YELLOW" in template_key:
        return PATHWAY_NAMES["YELLOW"]
    elif "GREEN" in template_key:
        return PATHWAY_NAMES["GREEN"]
    return "Unknown"

def get_session_letter(template_key):
    """Extract session letter (A or B) from template key"""
    if "_A_" in template_key or template_key.endswith("_A"):
        return "A"
    elif "_B_" in template_key or template_key.endswith("_B"):
        return "B"
    return "A"  # Default

def format_description_with_tagline(description, template_key, week, plan_weeks=20):
    """
    Format description with updated header including tagline, duration, and context
    
    Args:
        description: Original template description
        template_key: Template key (e.g., "RED_A_PHASE1")
        week: Week number
        plan_weeks: Total plan weeks (for context)
    
    Returns:
        Formatted description with tagline header, duration, and context
    """
    pathway_name = get_pathway_name(template_key)
    session = get_session_letter(template_key)
    
    # Get phase info
    phase_info = STRENGTH_PHASES.get(pathway_name, {})
    tagline_short = phase_info.get("tagline_short", "")
    rpe = phase_info.get("rpe", "")
    equipment = phase_info.get("equipment", "")
    
    # Estimate duration
    duration_min = estimate_workout_duration(description) if WORKOUT_ENHANCEMENTS_AVAILABLE else 40
    
    # Get workout context
    context = None
    if WORKOUT_ENHANCEMENTS_AVAILABLE:
        context = get_workout_context(week, template_key, plan_weeks, get_pathway_name, STRENGTH_SCHEDULE)
    
    # Add URLs to all exercises
    if WORKOUT_ENHANCEMENTS_AVAILABLE:
        description = add_urls_to_all_exercises(description)
    
    # Build new header
    new_header = f"★ STRENGTH: {pathway_name} │ Session {session} │ Week {week}\n\n"
    new_header += f"  {tagline_short}\n\n"
    new_header += f"  RPE Target: {rpe} │ Equipment: {equipment} │ Duration: ~{duration_min} min\n"
    
    if context:
        new_header += f"\n  {context}\n"
    
    new_header += "\n"
    
    # Find the old header pattern and replace it
    # More flexible: match from ★ STRENGTH to the first exercise section
    header_match = re.search(r'★\s*STRENGTH:.*?\n.*?(?=\n★\s*(?:WARMUP|WORKOUT|COOLDOWN|PREP|MAIN|CORE))', description, re.DOTALL)
    
    if header_match:
        # Replace old header with new one
        description = description[:header_match.start()] + new_header + description[header_match.end():]
    else:
        # If no match, prepend new header
        description = new_header + description
    
    return description, duration_min

def create_strength_zwo_file(week, template_key, description, output_path, plan_weeks=20):
    """
    Create a single strength workout ZWO file
    
    Args:
        week: Week number (1-20)
        template_key: Template key (e.g., "RED_A_PHASE1")
        description: Full formatted strength session description
        output_path: Path to save the ZWO file
        plan_weeks: Total plan weeks (for context)
    """
    # Generate title
    pathway_name = get_pathway_name(template_key)
    session = get_session_letter(template_key)
    name = f"W{week:02d} STR: {pathway_name} ({session})"
    
    # Format description with tagline header, duration, and context
    description, duration_min = format_description_with_tagline(description, template_key, week, plan_weeks)
    
    # Validate exercises in description if library is available
    missing_exercises = []
    if EXERCISE_LIBRARY_AVAILABLE:
        # Extract exercise names from description
        exercise_pattern = r'([A-Z][^→\n]+?)\s*─\s*[^\n]*\n\s*→\s*(https://[^\s\n]+)'
        exercises_in_desc = re.findall(exercise_pattern, description)
        
        for exercise_line, existing_url in exercises_in_desc:
            # Clean exercise name
            ex_name = exercise_line.strip()
            ex_name = re.sub(r'^[A-Z]\d+\s+', '', ex_name)
            ex_name = re.sub(r'\s*\([^)]+\)', '', ex_name).strip()
            
            if ex_name and len(ex_name) > 3:
                # Check if URL exists in library (validation only)
                library_url = get_video_url(ex_name)
                if not library_url and existing_url:
                    # URL exists in template but not in library - this is OK
                    pass
                elif not library_url and not existing_url:
                    # Missing URL - flag for review
                    missing_exercises.append(ex_name)
        
        if missing_exercises:
            print(f"     ⚠️  Week {week}: {len(missing_exercises)} exercises missing URLs: {missing_exercises[:3]}")
    
    # Escape XML special characters
    name_escaped = html.escape(name, quote=False)
    description_escaped = html.escape(description, quote=False)
    
    # Workout block with estimated duration (convert minutes to seconds)
    duration_seconds = duration_min * 60
    workout_blocks = f"    <FreeRide Duration=\"{duration_seconds}\" Power=\"0.0\"/>\n"
    
    # Generate ZWO content
    zwo_content = ZWO_TEMPLATE.format(
        name=name_escaped,
        description=description_escaped,
        blocks=workout_blocks
    )
    
    # Write file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(zwo_content)
    
    return output_path

def generate_strength_workout(week, day, template_key, templates_dict, output_dir, plan_weeks=20):
    """
    Generate a single strength workout
    
    Args:
        week: Week number
        day: Day name ("Mon", "Thu", etc.)
        template_key: Template key from schedule
        templates_dict: Dictionary of all templates
        output_dir: Output directory for ZWO files
        plan_weeks: Total plan weeks (default 20 for full plan)
    
    Returns:
        Path to generated file
    """
    # Get description from templates
    if template_key not in templates_dict:
        raise ValueError(f"Template key '{template_key}' not found in templates")
    
    description = templates_dict[template_key]
    
    # Generate filename with day: W{week:02d}_{day}_STR_{pathway}_{session}.zwo
    pathway_name = get_pathway_name(template_key)
    session = get_session_letter(template_key)
    pathway_slug = pathway_name.replace(' ', '_').replace("'", "").replace("*", "")
    filename = f"W{week:02d}_{day}_STR_{pathway_slug}_{session}.zwo"
    output_path = Path(output_dir) / filename
    
    # Create ZWO file with plan_weeks for context generation
    create_strength_zwo_file(week, template_key, description, output_path, plan_weeks=plan_weeks)
    
    return output_path

def generate_strength_workout_for_plan_week(plan_week, plan_weeks, template_key, templates_dict, output_dir, day=None):
    """
    Generate a single strength workout for a specific plan week
    
    For 12-week plans, maps plan weeks to compressed strength progression:
    - Plan weeks 1-3 → YELLOW_A/B_HYPER (strength weeks 7-9)
    - Plan weeks 4-6 → YELLOW_A/B_MAX (strength weeks 10-12)
    - Plan weeks 7-10 → GREEN_A/B_POWER (strength weeks 13-16)
    - Plan weeks 11-12 → GREEN_A/B_CONV (strength weeks 17-18)
    
    Args:
        plan_week: Plan week number
        plan_weeks: Total plan weeks
        template_key: Template key (e.g., "GREEN_A_MAINT")
        templates_dict: Dictionary of templates
        output_dir: Output directory
        day: Day of week ("Mon", "Thu", etc.) - defaults based on session A/B
    """
    # Get description from templates
    if template_key not in templates_dict:
        raise ValueError(f"Template key '{template_key}' not found in templates")
    
    description = templates_dict[template_key]
    
    # Determine day if not provided (A = Mon, B = Thu)
    if day is None:
        session = get_session_letter(template_key)
        day = "Mon" if session == "A" else "Thu"
    
    # Generate title using plan week, not strength week
    pathway_name = get_pathway_name(template_key)
    session = get_session_letter(template_key)
    name = f"W{plan_week:02d} STR: {pathway_name} ({session})"
    
    # Generate filename with day: W{week:02d}_{day}_STR_{pathway}_{session}.zwo
    pathway_slug = pathway_name.replace(' ', '_').replace("'", "").replace("*", "")
    filename = f"W{plan_week:02d}_{day}_STR_{pathway_slug}_{session}.zwo"
    output_path = Path(output_dir) / filename
    
    # Create ZWO file (using plan_week for title, but template_key for content)
    create_strength_zwo_file(plan_week, template_key, description, output_path, plan_weeks=plan_weeks)
    
    return output_path

def generate_strength_files(plan_info, output_dir, templates_file_path):
    """Generate strength workout ZWO files based on plan duration"""
    from pathlib import Path
    
    print(f"  → Generating strength workouts...")
    
    plan_weeks = plan_info.get("weeks", 12)
    workouts_dir = Path(output_dir) / "workouts"
    workouts_dir.mkdir(parents=True, exist_ok=True)
    
    # Load templates
    templates = load_strength_templates(templates_file_path)
    
    generated_files = []
    
    if plan_weeks == 6:
        print(f"     ⏭️  Skipping strength (6-week plan too short)")
        return 0
    elif plan_weeks == 12:
        # 12-week plans: Maintenance only (compressed progression)
        # Plan weeks 1-3 → GREEN_MAINT (maintenance phase)
        # Plan weeks 4-6 → GREEN_MAINT (maintenance phase)
        # Plan weeks 7-10 → GREEN_MAINT (maintenance phase)
        # Plan weeks 11-12 → GREEN_MAINT (maintenance phase)
        
        for plan_week in range(1, plan_weeks + 1):
            # 12-week plans: Maintenance only (GREEN_MAINT)
            # Alternate between A and B sessions
            if plan_week % 2 == 1:
                template_a = "GREEN_A_MAINT"
                template_b = "GREEN_B_MAINT"
            else:
                template_a = "GREEN_A_MAINT"
                template_b = "GREEN_B_MAINT"
            
            # Generate both sessions (Mon and Thu)
            for day, template_key in [("Mon", template_a), ("Thu", template_b)]:
                try:
                    filepath = generate_strength_workout_for_plan_week(
                        plan_week, plan_weeks, template_key, templates, workouts_dir, day=day
                    )
                    generated_files.append(filepath)
                except Exception as e:
                    print(f"     ⚠️  Error generating week {plan_week}, {day}: {e}")
        
    elif plan_weeks == 16 or plan_weeks == 20:
        # 16 and 20-week plans: Full strength training progression
        # Full progression: RED (weeks 1-6) → YELLOW (weeks 7-12) → GREEN (weeks 13-18) → GREEN_MAINT (weeks 19-20)
        files = generate_all_strength_workouts(
            templates_file_path,
            str(workouts_dir),
            start_week=1,
            end_week=plan_weeks
        )
        generated_files = files
    else:
        # Default: assume 12-week plan logic (maintenance only)
        print(f"     ⚠️  Unknown plan duration ({plan_weeks} weeks), using 12-week maintenance logic")
        # Use same logic as 12-week plans (maintenance only)
        for plan_week in range(1, min(plan_weeks, 12) + 1):
            template_a = "GREEN_A_MAINT"
            template_b = "GREEN_B_MAINT"
            
            for day, template_key in [("Mon", template_a), ("Thu", template_b)]:
                try:
                    filepath = generate_strength_workout_for_plan_week(
                        plan_week, plan_weeks, template_key, templates, workouts_dir, day=day
                    )
                    generated_files.append(filepath)
                except Exception as e:
                    print(f"     ⚠️  Error generating week {plan_week}, {day}: {e}")
    
    print(f"     ✓ Generated {len(generated_files)} strength workout files")
    return len(generated_files)

def generate_all_strength_workouts(templates_file_path, output_dir, start_week=1, end_week=20):
    """
    Generate all strength workouts for specified weeks
    
    Args:
        templates_file_path: Path to MASTER_TEMPLATES_V2.md
        output_dir: Directory to save ZWO files
        start_week: First week to generate (default 1)
        end_week: Last week to generate (default 20)
    
    Returns:
        List of generated file paths
    """
    # Load templates
    templates = load_strength_templates(templates_file_path)
    
    generated_files = []
    plan_weeks = end_week  # Use end_week as total plan duration for context
    
    # Generate workouts for each week
    for week in range(start_week, end_week + 1):
        if week not in STRENGTH_SCHEDULE:
            continue
        
        for day, template_key in STRENGTH_SCHEDULE[week]:
            try:
                filepath = generate_strength_workout(
                    week, day, template_key, templates, output_dir, plan_weeks=plan_weeks
                )
                generated_files.append(filepath)
                print(f"Generated: {filepath.name}")
            except Exception as e:
                print(f"Error generating week {week}, {day}, {template_key}: {e}")
    
    return generated_files

if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description="Generate strength workout ZWO files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all workouts with validation
  python strength_generator.py --validate --output ../strength_workouts_validated/
  
  # Generate specific plan (12-week)
  python strength_generator.py --weeks 12 --output ./output/
  
  # Legacy: positional arguments still work
  python strength_generator.py templates.md output_dir
        """
    )
    
    parser.add_argument(
        'templates_file',
        nargs='?',
        default=str(Path(__file__).parent / "MASTER_TEMPLATES_V2_PN_FINAL.md"),
        help='Path to MASTER_TEMPLATES_V2.md file'
    )
    
    parser.add_argument(
        '--output', '-o',
        dest='output_dir',
        default="./test_strength_output",
        help='Output directory for ZWO files'
    )
    
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate all exercises have video URLs (requires exercise_lookup module)'
    )
    
    parser.add_argument(
        '--weeks',
        type=int,
        choices=[6, 12, 20],
        default=20,
        help='Plan duration in weeks (6, 12, or 20)'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Generate single test file (W01_STR_Rebuild_Frame_A.zwo)'
    )
    
    args = parser.parse_args()
    
    # Handle legacy positional arguments
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        # First positional arg is templates_file
        if len(sys.argv) > 1:
            args.templates_file = sys.argv[1]
        if len(sys.argv) > 2:
            args.output_dir = sys.argv[2]
    
    print("=" * 70)
    print("STRENGTH WORKOUT GENERATOR")
    print("=" * 70)
    print(f"Templates: {args.templates_file}")
    print(f"Output: {args.output_dir}")
    print(f"Plan: {args.weeks} weeks")
    print(f"Validation: {'Enabled' if args.validate else 'Disabled'}")
    print("=" * 70)
    
    # Validate templates file exists
    if not Path(args.templates_file).exists():
        print(f"❌ Error: Templates file not found: {args.templates_file}")
        sys.exit(1)
    
    # Run validation if requested
    if args.validate and EXERCISE_LIBRARY_AVAILABLE:
        print("\n🔍 Validating exercises in templates...")
        from validate_template_exercises import extract_exercises_from_templates, validate_exercise_urls
        
        template_exercises = extract_exercises_from_templates(args.templates_file)
        results = validate_exercise_urls(template_exercises)
        
        print(f"\n📊 Validation Results:")
        print(f"   Total exercises: {results['total']}")
        print(f"   Found URLs: {results['found']}")
        print(f"   Missing URLs: {len(results['missing'])}")
        print(f"   Coverage: {results['coverage']*100:.1f}%")
        
        if results['missing']:
            print(f"\n⚠️  Missing URLs ({len(results['missing'])}):")
            for ex in results['missing'][:10]:  # Show first 10
                print(f"   - {ex}")
            if len(results['missing']) > 10:
                print(f"   ... and {len(results['missing']) - 10} more")
            
            response = input("\nContinue anyway? (y/n): ")
            if response.lower() != 'y':
                print("Aborted.")
                sys.exit(1)
        else:
            print(f"\n✅ All exercises have video URLs!")
    elif args.validate and not EXERCISE_LIBRARY_AVAILABLE:
        print("\n⚠️  --validate flag requires exercise_lookup module")
        print("   Continuing without validation...")
    
    # Generate workouts
    if args.test:
        # Test mode: Generate single file
        print("\n🧪 Test Mode: Generating W01_STR_Rebuild_Frame_A.zwo")
        templates = load_strength_templates(args.templates_file)
        
        test_file = generate_strength_workout(
            week=1,
            day="Mon",
            template_key="RED_A_PHASE1",
            templates_dict=templates,
            output_dir=args.output_dir
        )
        
        print(f"\n✓ Generated test file: {test_file}")
        print(f"\nFile contents preview:")
        with open(test_file, 'r') as f:
            content = f.read()
            print(content[:500] + "...")
    else:
        # Full generation mode
        print(f"\n🚀 Generating {args.weeks}-week plan...")
        
        plan_info = {"weeks": args.weeks}
        count = generate_strength_files(
            plan_info=plan_info,
            output_dir=args.output_dir,
            templates_file_path=args.templates_file
        )
        
        print(f"\n✅ Generation complete!")
        print(f"   Generated {count} strength workout files")
        print(f"   Output directory: {args.output_dir}")

