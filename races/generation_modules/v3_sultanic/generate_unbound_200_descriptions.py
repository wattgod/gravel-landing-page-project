#!/usr/bin/env python3
"""
Generate V3 Sultanic Marketplace Descriptions for all Unbound 200 plans
"""

import os
import sys
import re
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import race and tier variables
from race_variables import unbound_200
from tier_variables import ayahuasca, finisher, compete, podium

# Plan mapping: plan_name -> (tier_module, level_key, weeks)
PLAN_MAPPING = {
    "1. Ayahuasca Beginner (12 weeks)": (ayahuasca, "beginner", 12),
    "2. Ayahuasca Intermediate (12 weeks)": (ayahuasca, "intermediate", 12),
    "3. Ayahuasca Masters (12 weeks)": (ayahuasca, "masters", 12),
    "4. Ayahuasca Save My Race (6 weeks)": (ayahuasca, "save_my_race", 6),
    "5. Finisher Beginner (12 weeks)": (finisher, "beginner", 12),
    "6. Finisher Intermediate (12 weeks)": (finisher, "intermediate", 12),
    "7. Finisher Advanced (12 weeks)": (finisher, "advanced", 12),
    "8. Finisher Masters (12 weeks)": (finisher, "masters", 12),
    "9. Finisher Save My Race (6 weeks)": (finisher, "save_my_race", 6),
    "10. Compete Intermediate (12 weeks)": (compete, "intermediate", 12),
    "11. Compete Advanced (12 weeks)": (compete, "advanced", 12),
    "12. Compete Masters (12 weeks)": (compete, "masters", 12),
    "13. Compete Save My Race (6 weeks)": (compete, "save_my_race", 6),
    "14. Podium Advanced (12 weeks)": (podium, "advanced", 12),
    "15. Podium Advanced GOAT (12 weeks)": (podium, "advanced_goat", 12),
}

def load_template():
    """Load the V3 Sultanic HTML template"""
    template_path = Path(__file__).parent / "templates" / "tp_description_template.html"
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def calculate_workouts(weeks, tier, level):
    """Calculate number of workouts based on plan parameters"""
    if weeks == 6:
        return 42  # 6 weeks * 7 days
    elif tier == "compete" and level == "advanced":
        return 168  # Block options create more workouts
    elif tier == "podium" and level == "advanced_goat":
        return 112  # Block options
    else:
        return weeks * 7  # Standard calculation

def generate_description(plan_name, tier_module, level_key, weeks):
    """Generate a single marketplace description"""
    
    # Load template
    template = load_template()
    
    # Get tier name from module
    tier_name = tier_module.__name__.split('.')[-1]
    
    # Calculate workouts
    num_workouts = calculate_workouts(weeks, tier_name, level_key)
    
    # Replace all variables
    html = template.replace('{{COMPARISON_HOOK}}', unbound_200.COMPARISON_HOOK)
    html = html.replace('{{PAIN_STAT}}', unbound_200.PAIN_STAT)
    html = html.replace('{{SOLUTION_STATE_LANGUAGE}}', unbound_200.SOLUTION_STATE_LANGUAGE)
    html = html.replace('{{RACE_NAME}}', unbound_200.RACE_NAME)
    html = html.replace('{{PLAN_COUNT}}', unbound_200.PLAN_COUNT)
    html = html.replace('{{LANDING_URL}}', unbound_200.LANDING_URL)
    html = html.replace('{{STORY_JUSTIFICATION}}', unbound_200.STORY_JUSTIFICATION)
    html = html.replace('{{RACE_SPECIFIC_1}}', unbound_200.RACE_SPECIFIC_1)
    html = html.replace('{{RACE_SPECIFIC_2}}', unbound_200.RACE_SPECIFIC_2)
    html = html.replace('{{RACE_SPECIFIC_3}}', unbound_200.RACE_SPECIFIC_3)
    
    # Use appropriate functionally free positioning based on weeks
    if weeks == 6:
        html = html.replace('{{FUNCTIONALLY_FREE_POSITIONING}}', unbound_200.FUNCTIONALLY_FREE_POSITIONING_6)
    else:
        html = html.replace('{{FUNCTIONALLY_FREE_POSITIONING}}', unbound_200.FUNCTIONALLY_FREE_POSITIONING_12)
    
    # Tier-specific variables
    html = html.replace('{{CHOICE_FEATURE_1}}', tier_module.CHOICE_FEATURE_1)
    html = html.replace('{{CHOICE_FEATURE_2}}', tier_module.CHOICE_FEATURE_2)
    html = html.replace('{{CHOICE_FEATURE_3}}', tier_module.CHOICE_FEATURE_3)
    html = html.replace('{{CHOICE_FEATURE_4}}', tier_module.CHOICE_FEATURE_4)
    html = html.replace('{{EXPECTATION_GUIDE_1}}', tier_module.EXPECTATION_GUIDE_1)
    html = html.replace('{{EXPECTATION_GUIDE_2}}', tier_module.EXPECTATION_GUIDE_2)
    html = html.replace('{{EXPECTATION_GUIDE_3}}', tier_module.EXPECTATION_GUIDE_3)
    html = html.replace('{{EXPECTATION_GUIDE_4}}', tier_module.EXPECTATION_GUIDE_4)
    # Only include 5th guide if it exists (saves ~70 chars if removed)
    if tier_module.EXPECTATION_GUIDE_5:
        html = html.replace('{{EXPECTATION_GUIDE_5_HTML}}', f'<li>{tier_module.EXPECTATION_GUIDE_5}</li>')
    else:
        html = html.replace('{{EXPECTATION_GUIDE_5_HTML}}', '')
    html = html.replace('{{PATTERN_FOR_1}}', tier_module.PATTERN_FOR_1)
    html = html.replace('{{PATTERN_FOR_2}}', tier_module.PATTERN_FOR_2)
    html = html.replace('{{PATTERN_FOR_3}}', tier_module.PATTERN_FOR_3)
    html = html.replace('{{PATTERN_FOR_4}}', tier_module.PATTERN_FOR_4)
    html = html.replace('{{PATTERN_NOT_FOR}}', tier_module.PATTERN_NOT_FOR)
    
    # Plan-specific variables
    html = html.replace('{{PLAN_WEEKS}}', str(weeks))
    html = html.replace('{{NUM_WORKOUTS}}', str(num_workouts))
    
    return html

def validate_character_count(html, max_chars=4000):
    """Validate character count - TrainingPeaks counts ALL characters including HTML"""
    total_chars = len(html)  # TrainingPeaks counts everything
    
    if total_chars <= 3950:
        status = "✓ SAFE"
    elif total_chars <= 4000:
        status = "⚠ TIGHT"
    else:
        status = "✗ OVER"
    
    return {
        'count': total_chars,
        'remaining': 4000 - total_chars,
        'status': status
    }

def quality_check(html):
    """Run quality checks on generated description"""
    checks = {
        'char_count': len(re.sub(r'<[^>]+>', '', html)) <= 4000,
        'no_variables': '{{' not in html,
        'comparison_hook': 'style="margin:0;font-size:30px' in html,
        'email_present': 'gravelgodcoaching@gmail.com' in html,
        'motto_present': 'Become what you are.' in html,
        'cross_link': 'gravelgodcycling.com' in html,
        'comparison_ignition': 'Two versions of' in html,
        'solution_state': 'You had' in html or 'You could' in html,
        'choice_economics': ('knowing exactly' in html or 'no guessing' in html or 
                           'certainty' in html.lower() or 'automaticity' in html.lower() or
                           'Maximal fitness' in html or 'Race-ready' in html or
                           'Race fitness' in html or 'Tactical advantage' in html or
                           'Elite-level' in html or 'sophisticated' in html.lower()),
        'expectation_building': 'Week 6' in html or 'mile' in html.lower(),
        'story_engineering': 'Training for' in html or 'without a plan' in html,
        'pattern_matching': 'You Should Buy This If' in html,
        'functionally_free': "You're spending that" in html or 'with or without' in html,
    }
    
    passed = all(checks.values())
    
    return {
        'passed': passed,
        'checks': checks
    }

def main():
    """Generate all Unbound 200 marketplace descriptions"""
    
    base_dir = Path(__file__).parent.parent.parent.parent / "races" / "Unbound Gravel 200"
    
    if not base_dir.exists():
        print(f"Error: Directory not found: {base_dir}")
        sys.exit(1)
    
    results = []
    
    print("Generating V3 Sultanic marketplace descriptions for Unbound 200...")
    print("=" * 70)
    
    for plan_name, (tier_module, level_key, weeks) in PLAN_MAPPING.items():
        print(f"\n{plan_name}...")
        
        try:
            # Generate description
            html = generate_description(plan_name, tier_module, level_key, weeks)
            
            # Validate character count
            validation = validate_character_count(html)
            
            # Quality check
            qc = quality_check(html)
            
            # Save to file
            plan_dir = base_dir / plan_name
            if not plan_dir.exists():
                print(f"  ⚠️  Warning: Plan directory not found: {plan_dir}")
                continue
            
            output_path = plan_dir / "marketplace_description.html"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            
            # Print status
            status_icon = "✓" if qc['passed'] else "✗"
            print(f"  {status_icon} {validation['count']} chars - {validation['status']}")
            
            if not qc['passed']:
                failed_checks = [k for k, v in qc['checks'].items() if not v]
                print(f"  ⚠️  Failed checks: {', '.join(failed_checks)}")
            
            results.append({
                'plan': plan_name,
                'chars': validation['count'],
                'status': validation['status'],
                'qc_passed': qc['passed'],
                'path': str(output_path)
            })
            
        except Exception as e:
            print(f"  ✗ ERROR: {str(e)}")
            results.append({
                'plan': plan_name,
                'error': str(e)
            })
    
    # Summary
    print("\n" + "=" * 70)
    print("GENERATION SUMMARY")
    print("=" * 70)
    
    total = len(results)
    passed = sum(1 for r in results if r.get('qc_passed', False))
    over_limit = sum(1 for r in results if r.get('status') == '✗ OVER')
    
    print(f"Total descriptions: {total}")
    print(f"Passed QC: {passed}")
    print(f"Over limit: {over_limit}")
    print(f"Success rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n✅ All descriptions generated successfully!")
    else:
        print(f"\n⚠️  {total - passed} descriptions need attention")

if __name__ == '__main__':
    main()

