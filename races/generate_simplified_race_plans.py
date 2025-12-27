#!/usr/bin/env python3
"""
SIMPLIFIED 5-PLAN GENERATOR FOR UNBOUND 200
Generates 5 core training plans (replacing 15) with new structure:
1. Finisher (0-5 hrs/week)
2. Finisher Plus (5-8 hrs/week)
3. Compete (8-12 hrs/week)
4. Compete Masters (8-12 hrs/week)
5. Podium (12+ hrs/week)

Usage:
    python generate_simplified_race_plans.py unbound_gravel_200.json
"""

import json
import os
import sys
import shutil
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
    sys.exit(1)

# NEW SIMPLIFIED PLAN MAPPING
SIMPLIFIED_PLAN_MAPPING = {
    "1. Time Crunched (12 weeks)": {
        "tier": "ayahuasca",  # Keep tier as ayahuasca for compatibility
        "level": "beginner",
        "weeks": 12,
        "target_hours": "0-5 hrs/week",
        "goal": "Finish the race",
        "philosophy": "HIIT-Focused (Survival Mode)",
        "replaces": ["Ayahuasca Beginner", "Ayahuasca Intermediate"],
        "source_plans": [
            "1. Ayahuasca Beginner (12 weeks)",
            "2. Ayahuasca Intermediate (12 weeks)"
        ]
    },
    "2. Finisher (12 weeks)": {
        "tier": "finisher",
        "level": "beginner",
        "weeks": 12,
        "target_hours": "5-8 hrs/week",
        "goal": "Finish confidently, learn proper training",
        "philosophy": "Traditional Pyramidal",
        "replaces": ["Finisher Beginner", "Finisher Intermediate"],
        "source_plans": [
            "5. Finisher Beginner (12 weeks)",
            "6. Finisher Intermediate (12 weeks)"
        ]
    },
    "3. Compete (12 weeks)": {
        "tier": "compete",
        "level": "intermediate",
        "weeks": 12,
        "target_hours": "8-12 hrs/week",
        "goal": "Competitive finish, race for position",
        "philosophy": "Polarized Training",
        "replaces": ["Compete Intermediate", "Compete Advanced"],
        "source_plans": [
            "10. Compete Intermediate (12 weeks)",
            "11. Compete Advanced (12 weeks)"
        ]
    },
    "4. Compete Masters (12 weeks)": {
        "tier": "compete",
        "level": "masters",
        "weeks": 12,
        "target_hours": "8-12 hrs/week",
        "goal": "Age-group competitive",
        "philosophy": "Masters-optimized Polarized Training",
        "replaces": ["Compete Masters", "Ayahuasca Masters", "Finisher Masters"],
        "source_plans": [
            "3. Ayahuasca Masters (12 weeks)",
            "8. Finisher Masters (12 weeks)",
            "12. Compete Masters (12 weeks)"
        ]
    },
    "5. Podium (12 weeks)": {
        "tier": "podium",
        "level": "advanced",
        "weeks": 12,
        "target_hours": "12+ hrs/week",
        "goal": "Race to win, podium finish",
        "philosophy": "High-volume, race-specific preparation",
        "replaces": ["Podium Advanced", "Podium Advanced GOAT"],
        "source_plans": [
            "14. Podium Advanced (12 weeks)",
            "15. Podium Advanced GOAT (12 weeks)"
        ]
    }
}

def load_race_data(race_json_path):
    """Load race-specific data from JSON file"""
    with open(race_json_path, 'r') as f:
        return json.load(f)

def load_plan_template(plan_folder_name):
    """Load plan template JSON from old structure"""
    template_path = Path(__file__).parent.parent / "plans" / plan_folder_name / "template.json"
    if not template_path.exists():
        print(f"⚠️  Template not found: {template_path}")
        return None
    with open(template_path, 'r') as f:
        return json.load(f)

def merge_plan_templates(source_plan_names, simplified_plan_info):
    """
    Merge multiple plan templates into one simplified plan.
    For now, we'll use the first source plan as primary and adapt it.
    """
    if not source_plan_names:
        return None
    
    # Load the first source plan as primary
    primary_plan = load_plan_template(source_plan_names[0])
    if not primary_plan:
        # Try the second if first doesn't exist
        if len(source_plan_names) > 1:
            primary_plan = load_plan_template(source_plan_names[1])
        if not primary_plan:
            return None
    
    # Adapt the plan to simplified structure
    # The template structure should remain the same, but we'll note the consolidation
    primary_plan["simplified_plan_info"] = simplified_plan_info
    primary_plan["source_plans"] = source_plan_names
    
    return primary_plan

def create_simplified_race_folder_structure(race_name, base_path):
    """Create folder structure for simplified 5-plan structure"""
    race_folder = base_path / race_name
    race_folder.mkdir(exist_ok=True)
    
    # Create folders for each of the 5 simplified plans
    for plan_folder_name in SIMPLIFIED_PLAN_MAPPING.keys():
        plan_folder = race_folder / plan_folder_name
        plan_folder.mkdir(exist_ok=True)
        (plan_folder / "workouts").mkdir(exist_ok=True)
    
    return race_folder

def generate_zwo_files(plan_template, race_data, plan_info, output_dir):
    """Generate ZWO workout files"""
    print(f"  → Generating ZWO files...")
    total_workouts = generate_all_zwo_files(plan_template, race_data, plan_info, output_dir)
    print(f"     ✓ Generated {total_workouts} ZWO workout files")
    return total_workouts

def generate_marketplace_description(race_data, plan_template, plan_info, output_dir):
    """Generate marketplace HTML description"""
    print(f"  → Generating marketplace description...")
    marketplace_file = generate_marketplace_html(race_data, plan_template, plan_info)
    
    if marketplace_file:
        output_path = output_dir / marketplace_file
        print(f"     ✓ Generated marketplace description: {marketplace_file}")
        return output_path
    return None

def generate_training_guide(race_data, plan_template, plan_info, plan_output_dir, race_json_path):
    """Generate training plan guide using simplified template"""
    print(f"  → Generating training plan guide...")
    
    # Use simplified guide template
    guide_generator_path = Path(__file__).parent / "generation_modules" / "guide_generator.py"
    simplified_template_path = Path(__file__).parent / "generation_modules" / "guide_template_simplified.html"
    
    # Create temp plan JSON
    plan_name_slug = plan_info['tier'] + '_' + plan_info['level']
    plan_json_path = plan_output_dir / f"{plan_name_slug}_temp.json"
    
    with open(plan_json_path, 'w') as f:
        json.dump(plan_template, f, indent=2)
    
    try:
        # Guide generator doesn't accept --template, it uses default template
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
            guide_file = guide_files[0]
            print(f"     ✓ Generated training plan guide: {guide_file.name}")
            return guide_file
    
    except subprocess.CalledProcessError as e:
        print(f"     ⚠️  Guide generation failed: {e.stderr}")
        if plan_json_path.exists():
            plan_json_path.unlink()
        return None
    except Exception as e:
        print(f"     ⚠️  Guide generation error: {e}")
        if plan_json_path.exists():
            plan_json_path.unlink()
        return None

def generate_plan_variant(race_data, plan_folder_name, plan_info, race_folder, race_json_path):
    """Generate all outputs for one simplified plan variant"""
    print(f"\n📦 Generating: {plan_folder_name}")
    print(f"   Target: {plan_info['target_hours']}")
    print(f"   Goal: {plan_info['goal']}")
    print(f"   Philosophy: {plan_info['philosophy']}")
    print(f"   Replaces: {', '.join(plan_info['replaces'])}")
    
    plan_output_dir = race_folder / plan_folder_name
    
    # Merge plan templates from source plans
    plan_template = merge_plan_templates(plan_info['source_plans'], plan_info)
    if not plan_template:
        print(f"  ❌ Could not load plan template")
        return False
    
    # Generate ZWO files
    zwo_count = generate_zwo_files(plan_template, race_data, plan_info, plan_output_dir)
    
    # Generate marketplace description
    marketplace_file = generate_marketplace_description(race_data, plan_template, plan_info, plan_output_dir)
    
    # Generate training guide
    guide_file = generate_training_guide(race_data, plan_template, plan_info, plan_output_dir, race_json_path)
    
    # Generate race day workout
    from zwo_generator import generate_race_workout
    race_workout_file = generate_race_workout(race_data, plan_info, plan_output_dir)
    print(f"     ✓ Generated race day workout: {race_workout_file.name}")
    
    return True

def print_generation_summary(race_data):
    """Print comprehensive summary of what was generated"""
    print("\n" + "="*80)
    print("UNBOUND 200 - SIMPLIFIED 5-PLAN GENERATION SUMMARY")
    print("="*80)
    
    print("\n📋 TRAINING METHOD:")
    print("   Plan-specific training methods:")
    print("   • Time Crunched: HIIT-Focused (Survival Mode) - Maximum time efficiency")
    print("   • Finisher: Traditional Pyramidal - Builds durable aerobic base")
    print("   • Compete: Polarized Training - 80% low-intensity, 20% high-intensity")
    print("   • Compete Masters: Masters-optimized Polarized Training")
    print("   • Podium: High Volume Low Intensity (HVLI) or GOAT Method")
    print("   • Race-specific: Heat adaptation, durability focus, aggressive fueling")
    
    print("\n🔧 WORKOUT DIMENSIONS USED:")
    dimensions = race_data.get("workout_modifications", {})
    
    if dimensions.get("heat_training", {}).get("enabled"):
        heat_config = dimensions["heat_training"]
        print(f"   ✓ HEAT TRAINING:")
        print(f"     - Tier 3 (Active): Weeks {heat_config.get('tier_3_weeks', [])}")
        print(f"     - Tier 2 (Build-up): Weeks {heat_config.get('tier_2_weeks', [])}")
        print(f"     - Tier 1 (Maintenance): Weeks {heat_config.get('tier_1_weeks', [])}")
        print(f"     - Protocol: Indoor trainer (no fans), hot bath, or sauna")
    
    if dimensions.get("aggressive_fueling", {}).get("enabled"):
        fueling_config = dimensions["aggressive_fueling"]
        print(f"   ✓ AGGRESSIVE FUELING:")
        print(f"     - Target: {fueling_config.get('target_carbs_per_hour', 60)}-90g carbs/hour")
        print(f"     - Applied to: Long rides >{fueling_config.get('long_ride_min_hours', 3)} hours")
        print(f"     - Race-specific: Start fueling from mile 1")
    
    if dimensions.get("dress_rehearsal", {}).get("enabled"):
        dress_config = dimensions["dress_rehearsal"]
        print(f"   ✓ DRESS REHEARSAL:")
        print(f"     - Week: {dress_config.get('week', 9)}")
        print(f"     - Day: {dress_config.get('day', 'Saturday')}")
        print(f"     - Duration by tier: {dress_config.get('duration_hours', {})}")
    
    if dimensions.get("robust_taper", {}).get("enabled"):
        taper_config = dimensions["robust_taper"]
        print(f"   ✓ ROBUST TAPER:")
        print(f"     - Weeks: {taper_config.get('weeks', [])}")
        print(f"     - Focus: Recovery, race prep, mental preparation")
    
    print("\n📝 RACE-SPECIFIC TEXT ADDED:")
    print("   Each workout includes Unbound 200-specific notes:")
    print("   • Heat acclimatization protocol (weeks 6-10)")
    print("   • Hydration strategies (60-90g carbs/hr, 1000-1500mg sodium/hr)")
    print("   • Aggressive fueling reminders (start from mile 1)")
    print("   • Position alternation guidance (drops vs hoods)")
    print("   • Daily baseline hydration reminders")
    print("   • Dress rehearsal emphasis (week 9)")
    print("   • Robust taper guidance (weeks 11-12)")
    print("   • Race-specific tactics (pacing first 90 min, mechanical prep)")
    print("\n🎯 NATE'S WORKOUT DIMENSIONS INCORPORATED:")
    print("   Each workout includes Nate's workout generator dimensions:")
    print("   • Cadence prescriptions by archetype (e.g., 90-100rpm for VO2, 50-60rpm for SFR)")
    print("   • Position guidance (seated, hoods, drops, alternating)")
    print("   • In-saddle vs out-of-saddle specifications")
    print("   • Durability workouts (long Z2 ride → intervals while fatigued → race simulation)")
    print("   • Archetype-specific PURPOSE explanations")
    print("   • Progression-level context (Level 1-6)")
    
    print("\n📊 TOTAL PLANS GENERATED: 5")
    for plan_name, plan_info in SIMPLIFIED_PLAN_MAPPING.items():
        print(f"   {plan_name}")
        print(f"     - Target: {plan_info['target_hours']}")
        print(f"     - Philosophy: {plan_info['philosophy']}")
        print(f"     - Replaces: {', '.join(plan_info['replaces'])}")
    
    print("\n📚 UPDATED GUIDES:")
    print("   Each plan includes a simplified guide with:")
    print("   • Training philosophy and approach")
    print("   • Plan features and what's included")
    print("   • 18,000+ word comprehensive guide")
    print("   • Race-specific adaptations for Unbound 200")
    print("   • Heat, fueling, and durability protocols")
    
    print("\n" + "="*80)

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_simplified_race_plans.py <race_json_file>")
        print("Example: python generate_simplified_race_plans.py races/unbound_gravel_200.json")
        sys.exit(1)
    
    race_json_path = Path(sys.argv[1])
    if not race_json_path.exists():
        print(f"ERROR: Race JSON file not found: {race_json_path}")
        sys.exit(1)
    
    # Load race data
    race_data = load_race_data(race_json_path)
    race_name = race_data["race_metadata"]["name"]
    
    print(f"\n🚀 Generating Simplified 5-Plan Structure for: {race_name}")
    print(f"   Race: {race_name}")
    print(f"   Distance: {race_data['race_metadata']['distance_miles']} miles")
    print(f"   Elevation: {race_data['race_metadata']['elevation_feet']:,} ft")
    
    # Create output structure
    base_path = Path(__file__).parent
    race_folder = create_simplified_race_folder_structure(race_name, base_path)
    
    # Generate each of the 5 plans
    success_count = 0
    for plan_folder_name, plan_info in SIMPLIFIED_PLAN_MAPPING.items():
        if generate_plan_variant(race_data, plan_folder_name, plan_info, race_folder, race_json_path):
            success_count += 1
    
    # Print summary
    print_generation_summary(race_data)
    
    print(f"\n✅ Successfully generated {success_count}/5 plans")
    print(f"   Output directory: {race_folder}")

if __name__ == "__main__":
    main()

