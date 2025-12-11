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
import subprocess
try:
    from zwo_generator import generate_all_zwo_files
    from marketplace_generator import generate_marketplace_html
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

def generate_marketplace_description(race_data, plan_template, plan_info, output_dir):
    """Generate marketplace description HTML"""
    print(f"  → Generating marketplace description...")
    html_content = generate_marketplace_html(race_data, plan_template, plan_info)
    output_file = output_dir / "marketplace_description.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"     ✓ Generated marketplace description ({len(html_content)} chars)")
    return output_file

def generate_training_guide(race_data, plan_template, plan_info, race_folder, race_json_path):
    """Generate HTML training guide using guide_generator.py"""
    print(f"  → Generating training plan guide...")
    
    # Output to guides folder: races/[race-slug]/guides/
    guides_folder = race_folder / "guides"
    guides_folder.mkdir(exist_ok=True)
    
    # Create plan JSON file path (temporary, for guide generator)
    plan_name_slug = plan_info['tier'] + '_' + plan_info['level']
    plan_json_path = guides_folder / f"{plan_name_slug}_temp.json"
    
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
            "--output-dir", str(guides_folder)
        ], capture_output=True, text=True, check=True)
        
        # Clean up temp plan JSON
        plan_json_path.unlink()
        
        # Find the generated guide file
        guide_files = list(guides_folder.glob(f"*{plan_name_slug}*.html"))
        if guide_files:
            guide_file = guide_files[0]
        else:
            # Fallback: look for any HTML file with plan name
            guide_files = list(guides_folder.glob("*.html"))
            guide_file = guide_files[0] if guide_files else guides_folder / f"{plan_name_slug}_guide.html"
        
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
    
    # Generate outputs
    zwo_count = generate_zwo_files(plan_template, race_data, plan_info, plan_output_dir)
    marketplace_file = generate_marketplace_description(race_data, plan_template, plan_info, plan_output_dir)
    guide_file = generate_training_guide(race_data, plan_template, plan_info, race_folder, race_json_path)
    
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
    
    # Verify generated guides
    print(f"\n{'='*60}")
    print(f"🔍 Verifying generated guides...")
    print(f"{'='*60}")
    try:
        verify_script = Path(__file__).parent / "generation_modules" / "verify_guide_structure.py"
        guides_dir = race_folder / "guides"
        if guides_dir.exists():
            import subprocess
            result = subprocess.run(
                [sys.executable, str(verify_script), str(guides_dir), "--skip-index"],
                capture_output=True,
                text=True
            )
            print(result.stdout)
            if result.returncode != 0:
                print("⚠️  Warning: Some guides failed verification. Review the output above.")
                print(result.stderr)
        else:
            print("⚠️  Warning: Guides directory not found, skipping verification")
    except Exception as e:
        print(f"⚠️  Warning: Could not run verification script: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"✅ GENERATION COMPLETE: {race_name}")
    print(f"{'='*60}")
    print(f"📁 Output location: {race_folder}")
    print(f"📊 Generated:")
    print(f"   • 15 plan variants")
    print(f"   • {sum(r['zwo_files'] for r in results)} total ZWO files")
    print(f"   • 15 training plan guides (HTML) in: {race_folder / 'guides'}")
    print(f"   • 15 marketplace descriptions")
    print(f"\n📝 Next steps:")
    print(f"   1. Review outputs in: {race_folder}")
    print(f"   2. Run verification: python3 races/generation_modules/verify_guide_structure.py {race_folder / 'guides'}")
    print(f"   3. Upload ZWO files to TrainingPeaks")
    print(f"   4. Upload guides and descriptions to marketplace")

if __name__ == "__main__":
    main()

