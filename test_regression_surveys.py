#!/usr/bin/env python3
"""
Regression test for survey generation
Ensures surveys are created for all plans with correct content and URLs
"""

import json
import re
from pathlib import Path
import sys

# Add races directory to path
sys.path.insert(0, str(Path(__file__).parent / "races" / "generation_modules"))

def test_survey_exists(race_folder):
    """Test that survey exists for each plan"""
    race_folder = Path(race_folder)
    errors = []
    
    # Find all plan folders
    plan_folders = [d for d in race_folder.iterdir() if d.is_dir() and d.name[0].isdigit()]
    
    if not plan_folders:
        return [f"❌ No plan folders found in {race_folder}"]
    
    for plan_folder in sorted(plan_folders):
        surveys_dir = plan_folder / "surveys"
        if not surveys_dir.exists():
            errors.append(f"❌ {plan_folder.name}: surveys directory missing")
            continue
        
        # Look for survey file
        survey_files = list(surveys_dir.glob("survey-*.html"))
        if not survey_files:
            errors.append(f"❌ {plan_folder.name}: Survey file missing")
            continue
        
        if len(survey_files) > 1:
            errors.append(f"⚠️  {plan_folder.name}: Multiple survey files found: {[f.name for f in survey_files]}")
    
    return errors

def test_survey_filename_format(race_folder):
    """Test that survey filenames are URL-friendly (no spaces, proper format)"""
    race_folder = Path(race_folder)
    errors = []
    
    plan_folders = [d for d in race_folder.iterdir() if d.is_dir() and d.name[0].isdigit()]
    
    for plan_folder in sorted(plan_folders):
        surveys_dir = plan_folder / "surveys"
        if not surveys_dir.exists():
            continue
        
        survey_files = list(surveys_dir.glob("survey-*.html"))
        for survey_file in survey_files:
            filename = survey_file.name
            
            # Check for spaces in filename
            if " " in filename:
                errors.append(f"❌ {plan_folder.name}: Survey filename contains spaces: {filename}")
            
            # Check format: survey-{race}-{tier}-{level}.html
            if not re.match(r'^survey-[a-z0-9-]+-[a-z0-9-]+-[a-z0-9-]+\.html$', filename):
                errors.append(f"⚠️  {plan_folder.name}: Survey filename format unexpected: {filename}")
            
            # Check for double hyphens (should be single)
            if "--" in filename:
                errors.append(f"⚠️  {plan_folder.name}: Survey filename has double hyphens: {filename}")
    
    return errors

def test_survey_content_structure(race_folder, race_json_path):
    """Test that survey files have correct HTML structure and required content"""
    race_folder = Path(race_folder)
    race_data = json.load(open(race_json_path))
    race_name = race_data.get("race_metadata", {}).get("name", "Race")
    
    errors = []
    plan_folders = [d for d in race_folder.iterdir() if d.is_dir() and d.name[0].isdigit()]
    
    for plan_folder in sorted(plan_folders):
        surveys_dir = plan_folder / "surveys"
        if not surveys_dir.exists():
            continue
        
        survey_files = list(surveys_dir.glob("survey-*.html"))
        if not survey_files:
            continue
        
        survey_file = survey_files[0]
        content = survey_file.read_text(encoding='utf-8')
        
        # Required HTML structure
        checks = [
            ("<!DOCTYPE html>", "DOCTYPE declaration"),
            ("<html lang=\"en\">", "HTML tag"),
            ("<head>", "Head section"),
            ("<title>", "Title tag"),
            ("Training Plan Survey", "Survey title"),
            ("<form id=\"surveyForm\"", "Survey form"),
            ("name=\"completed\"", "Race completion question"),
            ("name=\"effectiveness\"", "Effectiveness rating"),
            ("name=\"adherence\"", "Adherence question"),
            ("name=\"hours\"", "Training hours question"),
            ("name=\"worked_best\"", "What worked best question"),
            ("name=\"didnt_work\"", "What didn't work question"),
            ("name=\"difficulty\"", "Difficulty rating"),
            ("name=\"recommend\"", "Recommendation question"),
            ("name=\"improvements\"", "Improvements textarea"),
            ("type=\"submit\"", "Submit button"),
            ("github.com", "GitHub Issue link"),
        ]
        
        for check_text, check_name in checks:
            if check_text not in content:
                errors.append(f"❌ {plan_folder.name}: Missing '{check_name}' in survey")
        
        # Check that plan name is embedded (not just from URL params)
        # Extract tier and level from folder name
        tier_match = re.search(r'(Ayahuasca|Finisher|Compete|Podium)', plan_folder.name, re.I)
        if tier_match:
            tier = tier_match.group(1)
            if tier.title() not in content:
                errors.append(f"⚠️  {plan_folder.name}: Plan tier '{tier}' not found in survey content")
        
        # Check for race name
        if race_name not in content:
            errors.append(f"❌ {plan_folder.name}: Race name '{race_name}' not found in survey")
        
        # Check for proper CSS styling (Gravel God style)
        if "Sometype Mono" not in content and "Courier New" not in content:
            errors.append(f"⚠️  {plan_folder.name}: Missing monospace font in survey")
        
        # Check that survey has JavaScript for form handling
        if "addEventListener('submit'" not in content and "form.addEventListener" not in content:
            errors.append(f"❌ {plan_folder.name}: Missing form submission handler")
        
        # Check for GitHub Issue URL generation
        if "github.com" in content and "issues/new" not in content:
            errors.append(f"⚠️  {plan_folder.name}: GitHub link may not be to Issues page")
    
    return errors

def test_survey_url_in_workout(race_folder, race_json_path):
    """Test that survey URLs are embedded in final workouts"""
    race_folder = Path(race_folder)
    race_data = json.load(open(race_json_path))
    race_name = race_data.get("race_metadata", {}).get("name", "Race")
    race_slug = race_name.lower().replace(' ', '-').replace('the ', '')
    
    errors = []
    plan_folders = [d for d in race_folder.iterdir() if d.is_dir() and d.name[0].isdigit()]
    
    for plan_folder in sorted(plan_folders):
        workouts_dir = plan_folder / "workouts"
        if not workouts_dir.exists():
            continue
        
        # Find final Sunday workout (W12_Sun or W06_Sun)
        final_sunday_files = list(workouts_dir.glob("*Sun*.zwo"))
        if not final_sunday_files:
            errors.append(f"⚠️  {plan_folder.name}: No Sunday workout found to check survey link")
            continue
        
        # Get the last week Sunday workout
        final_sunday = None
        for f in sorted(final_sunday_files):
            if "W12" in f.name or "W06" in f.name:
                final_sunday = f
        
        if not final_sunday:
            # Try to find any Sunday workout as fallback
            final_sunday = sorted(final_sunday_files)[-1]
        
        content = final_sunday.read_text(encoding='utf-8')
        
        # Check for survey link
        if "TRAINING PLAN SURVEY" not in content:
            errors.append(f"❌ {plan_folder.name}: Survey link missing in final Sunday workout ({final_sunday.name})")
            continue
        
        # Check for correct survey URL format
        survey_url_pattern = rf'https://wattgod\.github\.io/gravel-landing-page-project/guides/{re.escape(race_slug)}/surveys/survey-{re.escape(race_slug)}-[a-z0-9-]+\.html'
        if not re.search(survey_url_pattern, content):
            errors.append(f"❌ {plan_folder.name}: Survey URL format incorrect in workout")
        
        # Check that URL points to correct survey file
        surveys_dir = plan_folder / "surveys"
        if surveys_dir.exists():
            survey_files = list(surveys_dir.glob("survey-*.html"))
            if survey_files:
                expected_filename = survey_files[0].name
                if expected_filename not in content:
                    errors.append(f"⚠️  {plan_folder.name}: Survey URL in workout doesn't match survey filename")
    
    return errors

def test_survey_only_on_final_sunday(race_folder):
    """Test that survey is ONLY added to final Sunday workout, not other workouts"""
    race_folder = Path(race_folder)
    errors = []
    
    plan_folders = [d for d in race_folder.iterdir() if d.is_dir() and d.name[0].isdigit()]
    
    for plan_folder in sorted(plan_folders):
        workouts_dir = plan_folder / "workouts"
        if not workouts_dir.exists():
            continue
        
        # Get plan weeks from folder name
        weeks_match = re.search(r'(\d+)\s*weeks?', plan_folder.name, re.I)
        final_week = int(weeks_match.group(1)) if weeks_match else 12
        
        for workout_file in workouts_dir.glob("*.zwo"):
            filename = workout_file.name
            content = workout_file.read_text(encoding='utf-8')
            
            # Extract week number from filename (e.g., W06_Sun -> 6)
            week_match = re.search(r'W(\d+)_', filename)
            if not week_match:
                continue
            week_num = int(week_match.group(1))
            
            # Check if this is the actual day indicator (not just "Sunday" in the name)
            # Pattern: W##_Sun_- is Sunday, W##_Fri_- is Friday even if "Sunday" is in the name
            is_sunday_workout = "_Sun_-" in filename or "_Sun_" in filename
            is_final_week = week_num == final_week
            
            has_survey = "TRAINING PLAN SURVEY" in content
            has_survey_name = "<name>Training Plan Survey</name>" in content
            
            # Survey should ONLY be on final week Sunday
            if is_final_week and is_sunday_workout:
                # Should have survey
                if not has_survey:
                    errors.append(f"❌ {plan_folder.name}: Survey missing from final Sunday ({filename})")
            else:
                # Should NOT have survey
                if has_survey or has_survey_name:
                    errors.append(f"❌ {plan_folder.name}: Survey incorrectly added to {filename} (week {week_num}, not final Sunday)")
    
    return errors


def test_survey_github_pages_deployment(race_json_path):
    """Test that surveys are deployed to GitHub Pages docs structure"""
    race_data = json.load(open(race_json_path))
    race_name = race_data.get("race_metadata", {}).get("name", "Race")
    race_slug = race_name.lower().replace(' ', '-').replace('the ', '')
    
    errors = []
    
    # Check docs/guides/{race}/surveys/ directory
    docs_surveys_dir = Path(__file__).parent / "docs" / "guides" / race_slug / "surveys"
    
    if not docs_surveys_dir.exists():
        errors.append(f"❌ GitHub Pages surveys directory missing: {docs_surveys_dir}")
        return errors
    
    survey_files = list(docs_surveys_dir.glob("survey-*.html"))
    if not survey_files:
        errors.append(f"❌ No survey files found in GitHub Pages directory")
        return errors
    
    # Check for spaces in filenames (should be none)
    for survey_file in survey_files:
        if " " in survey_file.name:
            errors.append(f"❌ GitHub Pages survey has spaces in filename: {survey_file.name}")
    
    # Check that all surveys are valid HTML
    for survey_file in survey_files:
        content = survey_file.read_text(encoding='utf-8')
        if "<!DOCTYPE html>" not in content:
            errors.append(f"❌ GitHub Pages survey not valid HTML: {survey_file.name}")
        if "Training Plan Survey" not in content:
            errors.append(f"❌ GitHub Pages survey missing title: {survey_file.name}")
    
    return errors

if __name__ == "__main__":
    print("=" * 80)
    print("SURVEY REGRESSION TEST SUITE")
    print("=" * 80)
    
    all_errors = []
    
    # Test Mid South
    print("\n🔍 Testing Mid South surveys...")
    mid_south_folder = Path(__file__).parent / "races" / "Mid South"
    mid_south_json = Path(__file__).parent / "races" / "mid_south.json"
    
    if mid_south_folder.exists() and mid_south_json.exists():
        # Test 1: Survey files exist
        print("  Testing survey file existence...")
        errors = test_survey_exists(mid_south_folder)
        all_errors.extend(errors)
        if not errors:
            print("    ✓ All surveys exist")
        else:
            for error in errors:
                print(f"    {error}")
        
        # Test 2: Filename format
        print("  Testing survey filename format...")
        errors = test_survey_filename_format(mid_south_folder)
        all_errors.extend(errors)
        if not errors:
            print("    ✓ All survey filenames are URL-friendly")
        else:
            for error in errors:
                print(f"    {error}")
        
        # Test 3: Content structure
        print("  Testing survey content structure...")
        errors = test_survey_content_structure(mid_south_folder, mid_south_json)
        all_errors.extend(errors)
        if not errors:
            print("    ✓ All surveys have correct structure")
        else:
            for error in errors:
                print(f"    {error}")
        
        # Test 4: Survey URLs in workouts
        print("  Testing survey URLs in final workouts...")
        errors = test_survey_url_in_workout(mid_south_folder, mid_south_json)
        all_errors.extend(errors)
        if not errors:
            print("    ✓ All final workouts have survey links")
        else:
            for error in errors:
                print(f"    {error}")
        
        # Test 5: Survey ONLY on final Sunday (regression for bug where "Sunday" in name triggered survey)
        print("  Testing survey only on final Sunday (not Fri/other days)...")
        errors = test_survey_only_on_final_sunday(mid_south_folder)
        all_errors.extend(errors)
        if not errors:
            print("    ✓ Survey correctly placed only on final Sunday workouts")
        else:
            for error in errors:
                print(f"    {error}")
        
        # Test 6: GitHub Pages deployment
        print("  Testing GitHub Pages deployment...")
        errors = test_survey_github_pages_deployment(mid_south_json)
        all_errors.extend(errors)
        if not errors:
            print("    ✓ All surveys deployed to GitHub Pages")
        else:
            for error in errors:
                print(f"    {error}")
    else:
        print("  ⚠️  Mid South folder or JSON not found")
    
    # Summary
    print("\n" + "=" * 80)
    if all_errors:
        print(f"❌ FAILED: {len(all_errors)} error(s) found")
        for error in all_errors:
            print(f"  {error}")
        sys.exit(1)
    else:
        print("✅ All survey tests passed")
        sys.exit(0)
