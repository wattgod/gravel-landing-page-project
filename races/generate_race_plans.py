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
from pathlib import Path
from datetime import datetime

# Import generation modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generation_modules'))
try:
    from zwo_generator import generate_all_zwo_files
    from marketplace_generator import generate_marketplace_html
    from guide_generator import generate_guide_pdf
except ImportError as e:
    print(f"ERROR: Could not import generation modules: {e}")
    print("Make sure generation_modules/ folder exists with zwo_generator.py, marketplace_generator.py, and guide_generator.py")
    sys.exit(1)

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

def generate_marketplace_description(race_data, plan_template, plan_info, output_dir):
    """Generate marketplace description HTML"""
    print(f"  → Generating marketplace description...")
    html_content = generate_marketplace_html(race_data, plan_template, plan_info)
    output_file = output_dir / "marketplace_description.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"     ✓ Generated marketplace description ({len(html_content)} chars)")
    return output_file

def generate_training_guide(race_data, plan_template, plan_info, output_dir):
    """Generate 35-page training plan guide PDF"""
    print(f"  → Generating training plan guide...")
    output_file = output_dir / "training_plan_guide.pdf"
    guide_file = generate_guide_pdf(race_data, plan_template, plan_info, output_file)
    print(f"     ✓ Generated training plan guide")
    return guide_file

def generate_plan_variant(race_data, plan_folder_name, plan_info, race_folder):
    """Generate all outputs for one plan variant"""
    print(f"\n📦 Generating: {plan_folder_name}")
    
    plan_output_dir = race_folder / plan_folder_name
    
    # Load plan template
    plan_template = load_plan_template(plan_folder_name)
    
    # Generate outputs
    zwo_count = generate_zwo_files(plan_template, race_data, plan_info, plan_output_dir)
    marketplace_file = generate_marketplace_description(race_data, plan_template, plan_info, plan_output_dir)
    guide_file = generate_training_guide(race_data, plan_template, plan_info, plan_output_dir)
    
    print(f"  ✅ Complete: {zwo_count} workouts, guide, marketplace description")
    
    return {
        "plan": plan_folder_name,
        "zwo_files": zwo_count,
        "marketplace": marketplace_file,
        "guide": guide_file
    }

def main():
    """Main generation function"""
    if len(sys.argv) < 2:
        print("Usage: python generate_race_plans.py <race_json_file>")
        print("Example: python generate_race_plans.py unbound_gravel_200.json")
        sys.exit(1)
    
    race_json_file = sys.argv[1]
    base_path = Path(__file__).parent
    
    # Load race data
    print(f"📥 Loading race data: {race_json_file}")
    race_data = load_race_data(base_path / race_json_file)
    race_name = race_data["race_metadata"]["name"]
    
    # Create folder structure
    print(f"📁 Creating folder structure for: {race_name}")
    race_folder = create_race_folder_structure(race_name, base_path)
    
    # Save race data JSON to race folder
    race_data_file = race_folder / "race_data.json"
    with open(race_data_file, 'w') as f:
        json.dump(race_data, f, indent=2)
    
    # Generate all 15 plan variants
    print(f"\n🚀 Generating all 15 plan variants...")
    results = []
    
    for plan_folder_name, plan_info in PLAN_MAPPING.items():
        result = generate_plan_variant(race_data, plan_folder_name, plan_info, race_folder)
        results.append(result)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"✅ GENERATION COMPLETE: {race_name}")
    print(f"{'='*60}")
    print(f"📁 Output location: {race_folder}")
    print(f"📊 Generated:")
    print(f"   • 15 plan variants")
    print(f"   • {sum(r['zwo_files'] for r in results)} total ZWO files")
    print(f"   • 15 training plan guides")
    print(f"   • 15 marketplace descriptions")
    print(f"\n📝 Next steps:")
    print(f"   1. Review outputs in: {race_folder}")
    print(f"   2. Upload ZWO files to TrainingPeaks")
    print(f"   3. Upload guides and descriptions to marketplace")

if __name__ == "__main__":
    main()

