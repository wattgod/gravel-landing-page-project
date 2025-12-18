#!/usr/bin/env python3
"""
GRAVEL GOD RACE PLAN GENERATOR
Generates all 15 plan variants for a given race:
- 84 ZWO workout files
- 35-page training plan guide (PDF)
- Marketplace description (HTML)

Usage:
    python generate_race_plans.py unbound_gravel_200.json
"""

import json
import os
import sys
import shutil
import tempfile
from pathlib import Path
from datetime import datetime

# Import generation modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generation_modules'))
import subprocess
try:
    from zwo_generator import generate_all_zwo_files
    from marketplace_generator import generate_marketplace_html
except ImportError as e:
    print(f"ERROR: Could not import required generation modules: {e}")
    print("Make sure generation_modules/ folder exists with zwo_generator.py and marketplace_generator.py")
    sys.exit(1)

# Optional: strength generator (may not exist)
try:
    from strength_generator import generate_all_strength_workouts
    STRENGTH_GENERATOR_AVAILABLE = True
except ImportError:
    STRENGTH_GENERATOR_AVAILABLE = False
    print("⚠️  Strength generator not available - strength workouts will be skipped")

# Import unified generator
try:
    sys.path.insert(0, os.path.dirname(__file__))
    from unified_plan_generator import generate_unified_plan
    UNIFIED_GENERATOR_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Unified generator not available: {e}")
    print("   Falling back to separate cycling + strength generation")
    UNIFIED_GENERATOR_AVAILABLE = False

# Plan mapping: folder name -> tier, level, weeks
PLAN_MAPPING = {
    "1. Ayahuasca Beginner (12 weeks)": {"tier": "ayahuasca", "level": "beginner", "weeks": 12},
    "2. Ayahuasca Intermediate (12 weeks)": {"tier": "ayahuasca", "level": "intermediate", "weeks": 12},
    "3. Ayahuasca Masters (12 weeks)": {"tier": "ayahuasca", "level": "masters", "weeks": 12},
    "4. Ayahuasca Save My Race (6 weeks)": {"tier": "ayahuasca", "level": "save_my_race", "weeks": 6},
    "5. Finisher Beginner (12 weeks)": {"tier": "finisher", "level": "beginner", "weeks": 12},
    "6. Finisher Intermediate (12 weeks)": {"tier": "finisher", "level": "intermediate", "weeks": 12},
    "7. Finisher Advanced (12 weeks)": {"tier": "finisher", "level": "advanced", "weeks": 12},
    "8. Finisher Masters (12 weeks)": {"tier": "finisher", "level": "masters", "weeks": 12},
    "9. Finisher Save My Race (6 weeks)": {"tier": "finisher", "level": "save_my_race", "weeks": 6},
    "10. Compete Intermediate (12 weeks)": {"tier": "compete", "level": "intermediate", "weeks": 12},
    "11. Compete Advanced (12 weeks)": {"tier": "compete", "level": "advanced", "weeks": 12},
    "12. Compete Masters (12 weeks)": {"tier": "compete", "level": "masters", "weeks": 12},
    "13. Compete Save My Race (6 weeks)": {"tier": "compete", "level": "save_my_race", "weeks": 6},
    "14. Podium Advanced (12 weeks)": {"tier": "podium", "level": "advanced", "weeks": 12},
    "15. Podium Advanced GOAT (12 weeks)": {"tier": "podium", "level": "advanced_goat", "weeks": 12}
}

def load_race_data(race_json_path):
    """Load race-specific data from JSON file"""
    with open(race_json_path, 'r') as f:
        return json.load(f)

def load_plan_template(plan_folder_name):
    """Load plan template JSON"""
    template_path = Path(__file__).parent.parent / "plans" / plan_folder_name / "template.json"
    with open(template_path, 'r') as f:
        return json.load(f)

def create_race_folder_structure(race_name, base_path):
    """Create folder structure for race"""
    race_folder = base_path / race_name
    race_folder.mkdir(exist_ok=True)
    
    # Create guides folder for all plan guides
    guides_folder = race_folder / "guides"
    guides_folder.mkdir(exist_ok=True)
    
    # Create folders for each of the 15 plans
    for plan_folder_name in PLAN_MAPPING.keys():
        plan_folder = race_folder / plan_folder_name
        plan_folder.mkdir(exist_ok=True)
        (plan_folder / "workouts").mkdir(exist_ok=True)
    
    return race_folder

def generate_zwo_files(plan_template, race_data, plan_info, output_dir):
    """Generate 84 ZWO workout files"""
    print(f"  → Generating ZWO files...")
    total_workouts = generate_all_zwo_files(plan_template, race_data, plan_info, output_dir)
    print(f"     ✓ Generated {total_workouts} ZWO files")
    return total_workouts

def generate_strength_files(plan_info, output_dir, templates_file_path):
    """Generate strength workout ZWO files based on plan duration"""
    if not STRENGTH_GENERATOR_AVAILABLE:
        return 0
    try:
        from strength_generator import generate_strength_files as generate_strength_files_impl
        return generate_strength_files_impl(plan_info, output_dir, templates_file_path)
    except ImportError:
        return 0

def generate_unified_plan_files(race_data, plan_info, plan_template, output_dir):
    """
    Generate unified cycling + strength plan using the unified generator.
    
    Returns tuple: (cycling_count, strength_count, calendar_path)
    """
    if not UNIFIED_GENERATOR_AVAILABLE:
        return None, None, None
    
    # Extract race ID from race data
    race_name = race_data["race_metadata"]["name"]
    race_id_map = {
        "Unbound Gravel 200": "unbound_gravel_200",
        "Unbound Gravel 100": "unbound_gravel_100",
        "Leadville Trail 100": "leadville_100",
        "Belgian Waffle Ride": "belgian_waffle_ride",
        "Mid South": "mid_south",
        "SBT GRVL": "sbt_grvl",
        "Gravel Worlds": "gravel_worlds",
        "Crusher in the Tushar": "crusher_in_the_tushar",
        "Rebecca's Private Idaho": "rebeccas_private_idaho"
    }
    race_id = race_id_map.get(race_name, "unbound_gravel_200")  # Default fallback
    
    # Extract race date from race data (default to June if not specified)
    race_date_str = race_data.get("race_metadata", {}).get("date", "June")
    # Convert month name to date (use first Saturday of month as default)
    from datetime import datetime
    try:
        if race_date_str == "June":
            race_date = "2025-06-07"  # Default Saturday
        elif race_date_str == "August":
            race_date = "2025-08-02"
        else:
            # Try to parse if it's already a date string
            datetime.strptime(race_date_str, "%Y-%m-%d")
            race_date = race_date_str
    except:
        race_date = "2025-06-07"  # Fallback
    
    tier_id = plan_info["tier"]
    plan_weeks = plan_info["weeks"]
    
    # Skip 6-week plans (too short for unified system)
    if plan_weeks < 8:
        return None, None, None
    
    try:
        print(f"  → Generating unified plan (cycling + strength)...")
        result = generate_unified_plan(
            race_id=race_id,
            tier_id=tier_id,
            plan_weeks=plan_weeks,
            race_date=race_date,
            output_dir=str(output_dir),
            race_data=race_data,
            plan_template=plan_template
        )
        
        cycling_count = result["files_generated"]["cycling"]
        strength_count = result["files_generated"]["strength"]
        calendar_path = Path(output_dir) / "calendar" / "training_calendar.md"
        
        print(f"     ✓ Generated {cycling_count} cycling + {strength_count} strength workouts")
        if calendar_path.exists():
            print(f"     ✓ Generated unified calendar: {calendar_path.name}")
        
        return cycling_count, strength_count, calendar_path
        
    except Exception as e:
        print(f"     ⚠️  Unified generation failed: {e}")
        print(f"     Falling back to separate generation...")
        return None, None, None

def generate_marketplace_description(race_data, plan_template, plan_info, output_dir):
    """Generate marketplace description HTML"""
    print(f"  → Generating marketplace description...")
    html_content = generate_marketplace_html(race_data, plan_template, plan_info)
    output_file = output_dir / "marketplace_description.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"     ✓ Generated marketplace description ({len(html_content)} chars)")
    return output_file

def generate_training_guide(race_data, plan_template, plan_info, plan_output_dir, race_json_path):
    """Generate HTML training guide using guide_generator.py"""
    print(f"  → Generating training plan guide...")
    
    # Output to plan folder: races/[race-slug]/[plan-folder]/
    # This keeps guides with their corresponding workouts and marketplace descriptions
    
    # Create plan JSON file path (temporary, for guide generator)
    plan_name_slug = plan_info['tier'] + '_' + plan_info['level']
    plan_json_path = plan_output_dir / f"{plan_name_slug}_temp.json"
    
    # Save plan template to temp JSON file for guide generator
    with open(plan_json_path, 'w') as f:
        json.dump(plan_template, f, indent=2)
    
    # Call guide generator (works as CLI: --race, --plan, --output-dir)
    guide_generator_path = Path(__file__).parent / "generation_modules" / "guide_generator.py"
    
    try:
        result = subprocess.run([
            sys.executable,
            str(guide_generator_path),
            "--race", str(race_json_path),
            "--plan", str(plan_json_path),
            "--output-dir", str(plan_output_dir)
        ], capture_output=True, text=True, check=True)
        
        # Clean up temp plan JSON
        plan_json_path.unlink()
        
        # Find the generated guide file
        guide_files = list(plan_output_dir.glob(f"*{plan_name_slug}*.html"))
        if guide_files:
            guide_file = guide_files[0]
        else:
            # Fallback: look for any HTML file with plan name
            guide_files = list(plan_output_dir.glob("*guide.html"))
            guide_file = guide_files[0] if guide_files else plan_output_dir / f"{plan_name_slug}_guide.html"
        
        print(f"     ✓ Generated training plan guide: {guide_file.name}")
        return guide_file
        
    except subprocess.CalledProcessError as e:
        print(f"     ⚠️  Guide generation failed: {e.stderr}")
        # Clean up temp file
        if plan_json_path.exists():
            plan_json_path.unlink()
        return None
    except Exception as e:
        print(f"     ⚠️  Guide generation error: {e}")
        if plan_json_path.exists():
            plan_json_path.unlink()
        return None

def generate_plan_variant(race_data, plan_folder_name, plan_info, race_folder, race_json_path):
    """Generate all outputs for one plan variant"""
    print(f"\n📦 Generating: {plan_folder_name}")
    
    plan_output_dir = race_folder / plan_folder_name
    
    # Load plan template
    plan_template = load_plan_template(plan_folder_name)
    
    # Try unified generation first (for 8+ week plans)
    unified_cycling, unified_strength, calendar_path = generate_unified_plan_files(
        race_data, plan_info, plan_template, plan_output_dir
    )
    
    if unified_cycling is not None:
        # Unified generation succeeded
        zwo_count = unified_cycling
        strength_count = unified_strength
    else:
        # Fall back to separate generation
        zwo_count = generate_zwo_files(plan_template, race_data, plan_info, plan_output_dir)
        
        # Generate strength workouts
        # Templates file path: Use PN version with updated phase names (relative to this file)
        base_path = Path(__file__).parent
        templates_file = base_path / "generation_modules" / "MASTER_TEMPLATES_V2_PN_FINAL.md"
        # Fallback: original templates
        if not templates_file.exists():
            templates_file = base_path / "generation_modules" / "MASTER_TEMPLATES_V2.md"
        
        strength_count = 0
        if templates_file.exists():
            strength_count = generate_strength_files(plan_info, plan_output_dir, templates_file)
        else:
            print(f"  ⚠️  Strength templates file not found: {templates_file}")
            print(f"     Skipping strength workout generation")
    
    marketplace_file = generate_marketplace_description(race_data, plan_template, plan_info, plan_output_dir)
    guide_file = generate_training_guide(race_data, plan_template, plan_info, plan_output_dir, race_json_path)
    
    # Generate race day workout
    from zwo_generator import generate_race_workout
    race_workout_file = generate_race_workout(race_data, plan_info, plan_output_dir)
    print(f"     ✓ Generated race day workout: {race_workout_file.name}")
    
    # Generate plan-specific survey
    from survey_generator import generate_plan_survey
    survey_file, survey_filename = generate_plan_survey(race_data, plan_info, plan_output_dir)
    print(f"     ✓ Generated survey: {survey_filename}")
    
    total_workouts = zwo_count + strength_count + 1  # +1 for race workout
    print(f"  ✅ Complete: {total_workouts} workouts ({zwo_count} cycling + {strength_count} strength + 1 race), guide, marketplace description, survey")
    
    return {
        "plan": plan_folder_name,
        "zwo_files": zwo_count,
        "strength_files": strength_count,
        "marketplace": marketplace_file,
        "guide": guide_file,
        "calendar": calendar_path if calendar_path and calendar_path.exists() else None
    }

def main():
    """Main generation function"""
    if len(sys.argv) < 2:
        print("Usage: python generate_race_plans.py <race_json_file>")
        print("Example: python generate_race_plans.py unbound_gravel_200.json")
        sys.exit(1)
    
    race_json_file = sys.argv[1]
    base_path = Path(__file__).parent
    
    # Load race data - handle both relative and absolute paths
    print(f"📥 Loading race data: {race_json_file}")
    race_json_path = Path(race_json_file)
    if not race_json_path.is_absolute():
        # If relative, try relative to base_path first, then current directory
        if (base_path / race_json_path).exists():
            race_json_path = base_path / race_json_path
        elif Path(race_json_path).exists():
            race_json_path = Path(race_json_path)
        else:
            # Try in races/ folder
            race_json_path = base_path.parent / "races" / race_json_path.name
    race_data = load_race_data(race_json_path)
    race_name = race_data["race_metadata"]["name"]
    
    # Create folder structure
    print(f"📁 Creating folder structure for: {race_name}")
    race_folder = create_race_folder_structure(race_name, base_path)
    
    # Save race data JSON to race folder (used by guide generator)
    race_data_file = race_folder / "race_data.json"
    with open(race_data_file, 'w') as f:
        json.dump(race_data, f, indent=2)
    
    # Generate all 15 plan variants
    print(f"\n🚀 Generating all 15 plan variants...")
    results = []
    
    for plan_folder_name, plan_info in PLAN_MAPPING.items():
        result = generate_plan_variant(race_data, plan_folder_name, plan_info, race_folder, race_data_file)
        results.append(result)
    
    # Verify generated guides (MANDATORY)
    # Guides are now in each plan folder, so collect them all
    print(f"\n{'='*60}")
    print(f"🔍 Verifying generated guides (MANDATORY)...")
    print(f"{'='*60}")
    verify_script = Path(__file__).parent / "generation_modules" / "verify_guide_structure.py"
    
    if not verify_script.exists():
        print("❌ ERROR: Verification script not found!")
        sys.exit(1)
    
    # Collect all guide files from plan folders
    guide_files = []
    for plan_folder_name in PLAN_MAPPING.keys():
        plan_dir = race_folder / plan_folder_name
        if plan_dir.exists():
            # Find guide HTML files in this plan folder
            plan_guides = list(plan_dir.glob("*guide.html"))
            guide_files.extend(plan_guides)
    
    if not guide_files:
        print("❌ ERROR: No guide files found in plan folders!")
        sys.exit(1)
    
    # Create temporary directory with all guides for verification
    temp_guides_dir = Path(tempfile.mkdtemp())
    try:
        for guide_file in guide_files:
            # Copy guide to temp directory for verification
            shutil.copy2(guide_file, temp_guides_dir / guide_file.name)
        
        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, str(verify_script), str(temp_guides_dir), "--skip-index"],
                capture_output=True,
                text=True
            )
            print(result.stdout)
            if result.returncode != 0:
                print("\n" + "="*60)
                print("❌ VERIFICATION FAILED - Generation aborted")
                print("="*60)
                print("Fix the issues above before proceeding.")
                print("Guides were generated but contain errors.")
                if result.stderr:
                    print("\nErrors:")
                    print(result.stderr)
                sys.exit(1)
            print("\n✅ All guides passed verification")
        except Exception as e:
            print(f"❌ ERROR: Could not run verification script: {e}")
            sys.exit(1)
    finally:
        # Clean up temp directory
        shutil.rmtree(temp_guides_dir, ignore_errors=True)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"✅ GENERATION COMPLETE: {race_name}")
    print(f"{'='*60}")
    print(f"📁 Output location: {race_folder}")
    print(f"📊 Generated:")
    print(f"   • 15 plan variants")
    print(f"   • {sum(r['zwo_files'] for r in results)} cycling ZWO files")
    print(f"   • {sum(r.get('strength_files', 0) for r in results)} strength ZWO files")
    print(f"   • {sum(r['zwo_files'] + r.get('strength_files', 0) for r in results)} total ZWO files")
    print(f"   • 15 training plan guides (HTML) in each plan folder")
    print(f"   • 15 marketplace descriptions")
    print(f"\n📝 Next steps:")
    print(f"   1. Review outputs in: {race_folder}")
    print(f"   2. Run verification: python3 races/generation_modules/verify_guide_structure.py {race_folder / 'guides'}")
    print(f"   3. Upload ZWO files to TrainingPeaks")
    print(f"   4. Upload guides and descriptions to marketplace")

if __name__ == "__main__":
    main()

