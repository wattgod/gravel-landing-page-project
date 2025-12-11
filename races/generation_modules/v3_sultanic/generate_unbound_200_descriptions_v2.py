#!/usr/bin/env python3
"""
Generate V3 Sultanic Marketplace Descriptions V2 - Using Variation Pools
Zero repetition, reality-grounded claims
"""

import os
import sys
import re
import random
import hashlib
from pathlib import Path
from collections import Counter

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import variation pools
from UNBOUND_200_VARIATION_POOLS_V2 import (
    COMPARISON_HOOKS,
    COMPARISON_HOOKS_MASTERS,
    COMPARISON_HOOKS_BEGINNER,
    COMPARISON_HOOKS_AYAHUASCA,
    COMPARISON_HOOKS_PODIUM,
    SOLUTION_STATE_LANGUAGE,
    STORY_JUSTIFICATIONS,
    FUNCTIONALLY_FREE_12WK,
    FUNCTIONALLY_FREE_6WK,
    PATTERN_MATCHING_SETS,
    LONG_RIDE_AGENCY,
    FUELING_AGENCY,
    PACING_AGENCY,
    TECHNICAL_AGENCY,
    MENTAL_AGENCY,
    HEAT_AGENCY,
    RACE_TACTICS_AGENCY,
    MASTERS_AGENCY,
    FUELING_GUIDE_VARIATIONS,
    TECHNICAL_GUIDE_VARIATIONS,
    RACE_TACTICS_GUIDE_VARIATIONS,
    MENTAL_GUIDE_VARIATIONS,
    PACING_GUIDE_VARIATIONS,
    WOMEN_SPECIFIC_GUIDE_VARIATIONS,
    RACE_SPECIFIC_LONG_RIDES,
    RACE_SPECIFIC_TECHNICAL,
    RACE_SPECIFIC_PACING,
)

# Import race variables for static data
from race_variables import unbound_200

# ==============================================================================
# PLAN CONFIGURATIONS WITH REALITY ANCHORS
# Based on CLAIMS_REFERENCE.md
# ==============================================================================

PLANS = {
    "1. Ayahuasca Beginner (12 weeks)": {
        'id': 'unbound_200_ayahuasca_beginner',
        'race': 'Unbound Gravel 200',
        'tier': 'ayahuasca',
        'level': 'beginner',
        'weeks': 12,
        'reality_anchors': {
            'has_long_rides': True,
            'max_ride_hours': 2.1,
            'dress_rehearsal_hours': 5,
            'has_fueling_practice': True,
            'has_technical_skills': True,
            'has_mental_section': True,
            'has_heat_protocols': True,  # All Unbound plans have heat protocols
            'has_power_based_training': False,  # Ayahuasca may not use power
            'has_race_tactics': True,
        }
    },
    "2. Ayahuasca Intermediate (12 weeks)": {
        'id': 'unbound_200_ayahuasca_intermediate',
        'race': 'Unbound Gravel 200',
        'tier': 'ayahuasca',
        'level': 'intermediate',
        'weeks': 12,
        'reality_anchors': {
            'has_long_rides': True,
            'max_ride_hours': 2.1,
            'dress_rehearsal_hours': 5,
            'has_fueling_practice': True,
            'has_technical_skills': True,
            'has_mental_section': True,
            'has_heat_protocols': True,
            'has_power_based_training': False,
            'has_race_tactics': True,
        }
    },
    "3. Ayahuasca Masters (12 weeks)": {
        'id': 'unbound_200_ayahuasca_masters',
        'race': 'Unbound Gravel 200',
        'tier': 'ayahuasca',
        'level': 'masters',
        'weeks': 12,
        'reality_anchors': {
            'has_long_rides': True,
            'max_ride_hours': 2.1,
            'dress_rehearsal_hours': 5,
            'has_fueling_practice': True,
            'has_technical_skills': True,
            'has_mental_section': True,
            'has_heat_protocols': True,
            'has_power_based_training': False,
            'has_race_tactics': True,
        }
    },
    "4. Ayahuasca Save My Race (6 weeks)": {
        'id': 'unbound_200_ayahuasca_save_my_race',
        'race': 'Unbound Gravel 200',
        'tier': 'ayahuasca',
        'level': 'save_my_race',
        'weeks': 6,
        'reality_anchors': {
            'has_long_rides': True,
            'max_ride_hours': 2.1,
            'dress_rehearsal_hours': 5,
            'has_fueling_practice': True,
            'has_technical_skills': True,
            'has_mental_section': True,
            'has_heat_protocols': True,  # Weeks 3-5 for 6-week plans
            'has_power_based_training': False,
            'has_race_tactics': True,
        }
    },
    "5. Finisher Beginner (12 weeks)": {
        'id': 'unbound_200_finisher_beginner',
        'race': 'Unbound Gravel 200',
        'tier': 'finisher',
        'level': 'beginner',
        'weeks': 12,
        'reality_anchors': {
            'has_long_rides': True,
            'max_ride_hours': 3.3,
            'dress_rehearsal_hours': 7,
            'has_fueling_practice': True,
            'has_technical_skills': True,
            'has_mental_section': True,
            'has_heat_protocols': True,
            'has_power_based_training': True,
            'has_race_tactics': True,
        }
    },
    "6. Finisher Intermediate (12 weeks)": {
        'id': 'unbound_200_finisher_intermediate',
        'race': 'Unbound Gravel 200',
        'tier': 'finisher',
        'level': 'intermediate',
        'weeks': 12,
        'reality_anchors': {
            'has_long_rides': True,
            'max_ride_hours': 3.3,
            'dress_rehearsal_hours': 7,
            'has_fueling_practice': True,
            'has_technical_skills': True,
            'has_mental_section': True,
            'has_heat_protocols': True,
            'has_power_based_training': True,
            'has_race_tactics': True,
        }
    },
    "7. Finisher Advanced (12 weeks)": {
        'id': 'unbound_200_finisher_advanced',
        'race': 'Unbound Gravel 200',
        'tier': 'finisher',
        'level': 'advanced',
        'weeks': 12,
        'reality_anchors': {
            'has_long_rides': True,
            'max_ride_hours': 3.3,
            'dress_rehearsal_hours': 7,
            'has_fueling_practice': True,
            'has_technical_skills': True,
            'has_mental_section': True,
            'has_heat_protocols': True,
            'has_power_based_training': True,
            'has_race_tactics': True,
        }
    },
    "8. Finisher Masters (12 weeks)": {
        'id': 'unbound_200_finisher_masters',
        'race': 'Unbound Gravel 200',
        'tier': 'finisher',
        'level': 'masters',
        'weeks': 12,
        'reality_anchors': {
            'has_long_rides': True,
            'max_ride_hours': 3.3,
            'dress_rehearsal_hours': 7,
            'has_fueling_practice': True,
            'has_technical_skills': True,
            'has_mental_section': True,
            'has_heat_protocols': True,
            'has_power_based_training': True,
            'has_race_tactics': True,
        }
    },
    "9. Finisher Save My Race (6 weeks)": {
        'id': 'unbound_200_finisher_save_my_race',
        'race': 'Unbound Gravel 200',
        'tier': 'finisher',
        'level': 'save_my_race',
        'weeks': 6,
        'reality_anchors': {
            'has_long_rides': True,
            'max_ride_hours': 3.3,
            'dress_rehearsal_hours': 7,
            'has_fueling_practice': True,
            'has_technical_skills': True,
            'has_mental_section': True,
            'has_heat_protocols': True,
            'has_power_based_training': True,
            'has_race_tactics': True,
        }
    },
    "10. Compete Intermediate (12 weeks)": {
        'id': 'unbound_200_compete_intermediate',
        'race': 'Unbound Gravel 200',
        'tier': 'compete',
        'level': 'intermediate',
        'weeks': 12,
        'reality_anchors': {
            'has_long_rides': True,
            'max_ride_hours': 5.3,
            'dress_rehearsal_hours': 9,
            'has_fueling_practice': True,
            'has_technical_skills': True,
            'has_mental_section': True,
            'has_heat_protocols': True,
            'has_power_based_training': True,
            'has_race_tactics': True,
        }
    },
    "11. Compete Advanced (12 weeks)": {
        'id': 'unbound_200_compete_advanced',
        'race': 'Unbound Gravel 200',
        'tier': 'compete',
        'level': 'advanced',
        'weeks': 12,
        'reality_anchors': {
            'has_long_rides': True,
            'max_ride_hours': 5.3,
            'dress_rehearsal_hours': 9,
            'has_fueling_practice': True,
            'has_technical_skills': True,
            'has_mental_section': True,
            'has_heat_protocols': True,
            'has_power_based_training': True,
            'has_race_tactics': True,
        }
    },
    "12. Compete Masters (12 weeks)": {
        'id': 'unbound_200_compete_masters',
        'race': 'Unbound Gravel 200',
        'tier': 'compete',
        'level': 'masters',
        'weeks': 12,
        'reality_anchors': {
            'has_long_rides': True,
            'max_ride_hours': 5.3,
            'dress_rehearsal_hours': 9,
            'has_fueling_practice': True,
            'has_technical_skills': True,
            'has_mental_section': True,
            'has_heat_protocols': True,
            'has_power_based_training': True,
            'has_race_tactics': True,
        }
    },
    "13. Compete Save My Race (6 weeks)": {
        'id': 'unbound_200_compete_save_my_race',
        'race': 'Unbound Gravel 200',
        'tier': 'compete',
        'level': 'save_my_race',
        'weeks': 6,
        'reality_anchors': {
            'has_long_rides': True,
            'max_ride_hours': 5.3,
            'dress_rehearsal_hours': 9,
            'has_fueling_practice': True,
            'has_technical_skills': True,
            'has_mental_section': True,
            'has_heat_protocols': True,
            'has_power_based_training': True,
            'has_race_tactics': True,
        }
    },
    "14. Podium Advanced (12 weeks)": {
        'id': 'unbound_200_podium_advanced',
        'race': 'Unbound Gravel 200',
        'tier': 'podium',
        'level': 'advanced',
        'weeks': 12,
        'reality_anchors': {
            'has_long_rides': True,
            'max_ride_hours': 6.5,
            'dress_rehearsal_hours': 10,
            'has_fueling_practice': True,
            'has_technical_skills': True,
            'has_mental_section': True,
            'has_heat_protocols': True,
            'has_power_based_training': True,
            'has_race_tactics': True,
        }
    },
    "15. Podium Advanced GOAT (12 weeks)": {
        'id': 'unbound_200_podium_advanced_goat',
        'race': 'Unbound Gravel 200',
        'tier': 'podium',
        'level': 'advanced_goat',
        'weeks': 12,
        'reality_anchors': {
            'has_long_rides': True,
            'max_ride_hours': 6.5,
            'dress_rehearsal_hours': 10,
            'has_fueling_practice': True,
            'has_technical_skills': True,
            'has_mental_section': True,
            'has_heat_protocols': True,
            'has_power_based_training': True,
            'has_race_tactics': True,
        }
    },
}

# ==============================================================================
# VARIATION SELECTION FUNCTIONS
# ==============================================================================

def select_choice_features(plan_config):
    """Select 4 choice features based on plan reality"""
    anchors = plan_config['reality_anchors']
    available_pools = []
    
    # For Masters plans, prioritize Masters-specific features
    if plan_config.get('level') == 'masters':
        available_pools.append(('masters', MASTERS_AGENCY))
    
    if anchors.get('has_long_rides', False):
        available_pools.append(('long_ride', LONG_RIDE_AGENCY))
    
    if anchors.get('has_fueling_practice', False):
        available_pools.append(('fueling', FUELING_AGENCY))
    
    if anchors.get('has_power_based_training', False):
        available_pools.append(('pacing', PACING_AGENCY))
    
    if anchors.get('has_technical_skills', False):
        available_pools.append(('technical', TECHNICAL_AGENCY))
    
    if anchors.get('has_mental_section', False):
        available_pools.append(('mental', MENTAL_AGENCY))
    
    if anchors.get('has_heat_protocols', False):
        available_pools.append(('heat', HEAT_AGENCY))
    
    if anchors.get('has_race_tactics', False):
        available_pools.append(('tactics', RACE_TACTICS_AGENCY))
    
    # Select 4 pools (or fewer if plan is simple)
    # Use plan_id in selection to ensure uniqueness
    plan_id = plan_config['id']
    pool_seed = int(hashlib.md5(f"{plan_id}_choice".encode()).hexdigest(), 16)
    random.seed(pool_seed)
    
    # For Masters plans, ensure at least one Masters feature is included
    if plan_config.get('level') == 'masters' and len(available_pools) >= 4:
        # Force include one Masters feature, then select 3 more
        masters_pool = [p for p in available_pools if p[0] == 'masters'][0]
        other_pools = [p for p in available_pools if p[0] != 'masters']
        if len(other_pools) >= 3:
            selected_others = random.sample(other_pools, 3)
            selected_pools = [masters_pool] + selected_others
        else:
            selected_pools = [masters_pool] + other_pools
    elif len(available_pools) >= 4:
        selected_pools = random.sample(available_pools, 4)
    else:
        selected_pools = available_pools
    
    # Pick one variation from each selected pool
    # Use different seed offset for each pool to ensure uniqueness
    features = []
    for i, (pool_name, pool) in enumerate(selected_pools):
        feature_seed = int(hashlib.md5(f"{plan_id}_choice_{pool_name}_{i}".encode()).hexdigest(), 16)
        random.seed(feature_seed)
        features.append(random.choice(pool))
    
    # Pad to 4 if needed
    while len(features) < 4:
        pad_seed = int(hashlib.md5(f"{plan_id}_choice_pad_{len(features)}".encode()).hexdigest(), 16)
        random.seed(pad_seed)
        features.append(random.choice(LONG_RIDE_AGENCY))
    
    return features

def select_guide_topics(plan_config):
    """Select 4 guide topics based on guide reality - always includes women-specific section"""
    anchors = plan_config['reality_anchors']
    available_pools = []
    
    # Always include women-specific guide topic
    available_pools.append(('women', WOMEN_SPECIFIC_GUIDE_VARIATIONS))
    
    if anchors.get('has_fueling_practice', False):
        available_pools.append(('fueling', FUELING_GUIDE_VARIATIONS))
    
    if anchors.get('has_technical_skills', False):
        available_pools.append(('technical', TECHNICAL_GUIDE_VARIATIONS))
    
    if anchors.get('has_race_tactics', False):
        available_pools.append(('tactics', RACE_TACTICS_GUIDE_VARIATIONS))
    
    if anchors.get('has_mental_section', False):
        available_pools.append(('mental', MENTAL_GUIDE_VARIATIONS))
    
    if anchors.get('has_power_based_training', False):
        available_pools.append(('pacing', PACING_GUIDE_VARIATIONS))
    
    if anchors.get('has_heat_protocols', False):
        # Heat guide topic - expand pool to reduce repetition
        heat_topics = [
            "Heat: 10-14 day acclimatization weeks 6-10 — 5-8% gain",
            "Heat: Progressive adaptation weeks 6-10 — 5-8% gain",
            "Heat: Indoor trainer, hot water immersion, sauna protocols",
            "Heat: Thermal adaptation weeks 6-10 — 5-8% improvement",
            "Heat: Weeks 6-10 acclimatization — 5-8% performance improvement",
            "Heat: Progressive heat adaptation protocols weeks 6-10",
            "Heat: 10-14 day protocols weeks 6-10 — indoor trainer, hot water, sauna",
            "Heat: Thermal adaptation weeks 6-10 — 5-8% gain in hot conditions",
        ]
        available_pools.append(('heat', heat_topics))
    
    # Use plan_id in selection to ensure uniqueness
    plan_id = plan_config['id']
    guide_seed = int(hashlib.md5(f"{plan_id}_guide".encode()).hexdigest(), 16)
    random.seed(guide_seed)
    
    # Always include women-specific, then select 3 more
    women_pool = [p for p in available_pools if p[0] == 'women'][0]
    other_pools = [p for p in available_pools if p[0] != 'women']
    
    if len(other_pools) >= 3:
        selected_others = random.sample(other_pools, 3)
        selected_pools = [women_pool] + selected_others
    else:
        selected_pools = [women_pool] + other_pools
    
    topics = []
    for i, (pool_name, pool) in enumerate(selected_pools):
        topic_seed = int(hashlib.md5(f"{plan_id}_guide_{pool_name}_{i}".encode()).hexdigest(), 16)
        random.seed(topic_seed)
        topics.append(random.choice(pool))
    
    # Pad if needed (shouldn't happen since we always include women)
    while len(topics) < 4:
        pad_seed = int(hashlib.md5(f"{plan_id}_guide_pad_{len(topics)}".encode()).hexdigest(), 16)
        random.seed(pad_seed)
        topics.append(random.choice(FUELING_GUIDE_VARIATIONS))
    
    return topics

def select_race_specific_features(plan_config):
    """Select 3 race-specific features based on plan structure"""
    anchors = plan_config['reality_anchors']
    race_feature_pools = []
    
    if anchors.get('has_long_rides', False):
        race_feature_pools.append(('long_ride', RACE_SPECIFIC_LONG_RIDES))
    
    if anchors.get('has_technical_skills', False):
        race_feature_pools.append(('technical', RACE_SPECIFIC_TECHNICAL))
    
    if anchors.get('has_power_based_training', False):
        race_feature_pools.append(('pacing', RACE_SPECIFIC_PACING))
    
    # Use plan_id in selection to ensure uniqueness
    plan_id = plan_config['id']
    race_seed = int(hashlib.md5(f"{plan_id}_race".encode()).hexdigest(), 16)
    random.seed(race_seed)
    
    # Select 3 race-specific features
    race_specific = []
    for i, (pool_name, pool) in enumerate(race_feature_pools[:3]):
        feature_seed = int(hashlib.md5(f"{plan_id}_race_{pool_name}_{i}".encode()).hexdigest(), 16)
        random.seed(feature_seed)
        race_specific.append(random.choice(pool))
    
    # Pad if needed
    while len(race_specific) < 3:
        pad_seed = int(hashlib.md5(f"{plan_id}_race_pad_{len(race_specific)}".encode()).hexdigest(), 16)
        random.seed(pad_seed)
        race_specific.append(random.choice(RACE_SPECIFIC_LONG_RIDES))
    
    return race_specific

# ==============================================================================
# GENERATION FUNCTION
# ==============================================================================

def load_template():
    """Load the V3 Sultanic HTML template"""
    template_path = Path(__file__).parent / "templates" / "tp_description_template.html"
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def calculate_workouts(weeks):
    """Calculate number of workouts"""
    if weeks == 6:
        return 42
    else:
        return 84  # Standard 12-week plan

def generate_description(plan_config):
    """
    Generate unique marketplace description using variation pools
    """
    
    # CRITICAL: Use plan_id as seed for consistency
    plan_id = plan_config['id']
    # Create deterministic seed from plan_id
    # Use a more robust seeding that ensures different plans get different variations
    seed_str = f"{plan_id}_{plan_config['tier']}_{plan_config['level']}"
    seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16) % (2**32)
    random.seed(seed)
    
    # 1. Select core variations (always needed)
    # Select comparison hook based on plan level/tier
    hook_seed = int(hashlib.md5(f"{plan_id}_hook".encode()).hexdigest(), 16)
    random.seed(hook_seed)
    
    # Choose hook pool based on plan characteristics
    if plan_config.get('level') == 'masters':
        hook_pool = COMPARISON_HOOKS_MASTERS
    elif plan_config.get('level') == 'beginner':
        hook_pool = COMPARISON_HOOKS_BEGINNER
    elif plan_config.get('tier') == 'ayahuasca':
        hook_pool = COMPARISON_HOOKS_AYAHUASCA
    elif plan_config.get('tier') == 'podium':
        hook_pool = COMPARISON_HOOKS_PODIUM
    else:
        hook_pool = COMPARISON_HOOKS
    
    comparison_hook = random.choice(hook_pool)
    
    solution_seed = int(hashlib.md5(f"{plan_id}_solution".encode()).hexdigest(), 16)
    random.seed(solution_seed)
    solution_state = random.choice(SOLUTION_STATE_LANGUAGE)
    
    story_seed = int(hashlib.md5(f"{plan_id}_story".encode()).hexdigest(), 16)
    random.seed(story_seed)
    story_justification = random.choice(STORY_JUSTIFICATIONS)
    
    pattern_seed = int(hashlib.md5(f"{plan_id}_pattern".encode()).hexdigest(), 16)
    random.seed(pattern_seed)
    pattern_set = random.choice(PATTERN_MATCHING_SETS)
    
    # 2. Select functionally free based on plan duration
    free_seed = int(hashlib.md5(f"{plan_id}_free".encode()).hexdigest(), 16)
    random.seed(free_seed)
    if plan_config['weeks'] == 12:
        functionally_free = random.choice(FUNCTIONALLY_FREE_12WK)
    else:
        functionally_free = random.choice(FUNCTIONALLY_FREE_6WK)
    
    # 3. Select choice features based on reality
    choice_features = select_choice_features(plan_config)
    
    # 4. Select guide topics based on reality
    guide_topics = select_guide_topics(plan_config)
    
    # 5. Select race-specific features
    race_specific = select_race_specific_features(plan_config)
    
    # 6. Calculate workouts
    num_workouts = calculate_workouts(plan_config['weeks'])
    
    # 7. Build variable dictionary
    variables = {
        'COMPARISON_HOOK': comparison_hook,
        'PAIN_STAT': unbound_200.PAIN_STAT,
        'SOLUTION_STATE_LANGUAGE': solution_state,
        'STORY_JUSTIFICATION': story_justification,
        'FUNCTIONALLY_FREE_POSITIONING': functionally_free,
        
        'CHOICE_FEATURE_1': choice_features[0],
        'CHOICE_FEATURE_2': choice_features[1],
        'CHOICE_FEATURE_3': choice_features[2],
        'CHOICE_FEATURE_4': choice_features[3],
        
        'EXPECTATION_GUIDE_1': guide_topics[0],
        'EXPECTATION_GUIDE_2': guide_topics[1],
        'EXPECTATION_GUIDE_3': guide_topics[2],
        'EXPECTATION_GUIDE_4': guide_topics[3],
        'EXPECTATION_GUIDE_5_HTML': '',  # Removed to save chars
        
        'RACE_SPECIFIC_1': race_specific[0],
        'RACE_SPECIFIC_2': race_specific[1],
        'RACE_SPECIFIC_3': race_specific[2],
        
        'PATTERN_FOR_1': pattern_set['for'][0],
        'PATTERN_FOR_2': pattern_set['for'][1],
        'PATTERN_FOR_3': pattern_set['for'][2],
        'PATTERN_FOR_4': pattern_set['for'][3],
        'PATTERN_NOT_FOR': pattern_set['not_for'],
        
        'RACE_NAME': unbound_200.RACE_NAME,
        'PLAN_WEEKS': str(plan_config['weeks']),
        'NUM_WORKOUTS': str(num_workouts),
        'PLAN_COUNT': unbound_200.PLAN_COUNT,
        'LANDING_URL': unbound_200.LANDING_URL,
    }
    
    # 8. Load template and substitute
    template = load_template()
    html = template
    for placeholder, value in variables.items():
        html = html.replace(f'{{{{{placeholder}}}}}', str(value))
    
    return html, variables

# ==============================================================================
# VALIDATION FUNCTIONS
# ==============================================================================

def validate_character_count(html, max_chars=4000):
    """Validate character count - TrainingPeaks counts ALL characters including HTML"""
    total_chars = len(html)
    
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

def check_for_repetition(all_descriptions):
    """Check if any phrases are repeated word-for-word across descriptions"""
    all_text = []
    for desc in all_descriptions:
        vars = desc['variables']
        all_text.extend([
            vars['COMPARISON_HOOK'],
            vars['SOLUTION_STATE_LANGUAGE'],
            vars['CHOICE_FEATURE_1'],
            vars['CHOICE_FEATURE_2'],
            vars['CHOICE_FEATURE_3'],
            vars['CHOICE_FEATURE_4'],
            vars['EXPECTATION_GUIDE_1'],
            vars['EXPECTATION_GUIDE_2'],
            vars['EXPECTATION_GUIDE_3'],
            vars['EXPECTATION_GUIDE_4'],
        ])
    
    # Count occurrences
    counts = Counter(all_text)
    
    # Find duplicates
    duplicates = {text: count for text, count in counts.items() if count > 1}
    
    if duplicates:
        print("\n⚠️  REPETITION DETECTED:")
        for text, count in list(duplicates.items())[:10]:  # Show first 10
            print(f"  [{count}x] {text[:80]}...")
        return False
    else:
        print("\n✓ ZERO REPETITION - All variations unique")
        return True

def quality_check(html):
    """Run quality checks on generated description"""
    checks = {
        'no_variables': '{{' not in html,
        'comparison_hook': 'style="margin:0;font-size:30px' in html,
        'email_present': 'gravelgodcoaching@gmail.com' in html,
        'motto_present': 'Become what you are.' in html,
        'cross_link': 'gravelgodcycling.com' in html,
        'comparison_ignition': len(re.findall(r'Two versions|chaos|executing|plan|ready|guessing|winging', html, re.I)) > 0,
        'solution_state': len(re.findall(r'You had|You could|fitness but not|fueling|went too hard|mile \d+', html, re.I)) > 0,
        'choice_economics': len(re.findall(r'knowing|no guessing|certainty|automaticity|protocols|practiced|FTP|zones|discipline', html, re.I)) > 0,
        'expectation_building': len(re.findall(r'Week|mile|Section|guide|protocol', html, re.I)) > 0,
        'story_engineering': len(re.findall(r'Training for|without a plan|Wing it|exam|studying|ready|preparation', html, re.I)) > 0,
        'pattern_matching': 'You Should Buy This If' in html,
        'functionally_free': len(re.findall(r"You're spending|with or without|entry|travel|plan or|ready or|investing|Worth it|Plan or|hope", html, re.I)) > 0,
    }
    
    passed = all(checks.values())
    
    return {
        'passed': passed,
        'checks': checks
    }

# ==============================================================================
# MAIN GENERATION
# ==============================================================================

def main():
    """Generate all Unbound 200 marketplace descriptions"""
    
    base_dir = Path(__file__).parent.parent.parent.parent / "races" / "Unbound Gravel 200"
    
    if not base_dir.exists():
        print(f"Error: Directory not found: {base_dir}")
        sys.exit(1)
    
    results = []
    all_descriptions = []
    
    print("Generating V3 Sultanic V2 marketplace descriptions (variation pools)...")
    print("=" * 70)
    
    for plan_name, plan_config in PLANS.items():
        print(f"\n{plan_name}...")
        
        try:
            # Generate description
            html, variables = generate_description(plan_config)
            
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
            status_icon = "✓" if qc['passed'] and validation['status'] != "✗ OVER" else "✗"
            print(f"  {status_icon} {validation['count']} chars - {validation['status']}")
            print(f"     Hook: {variables['COMPARISON_HOOK'][:60]}...")
            
            if not qc['passed']:
                failed_checks = [k for k, v in qc['checks'].items() if not v]
                print(f"  ⚠️  Failed checks: {', '.join(failed_checks)}")
            
            results.append({
                'plan': plan_name,
                'chars': validation['count'],
                'status': validation['status'],
                'qc_passed': qc['passed'],
                'path': str(output_path),
                'variables': variables
            })
            
            all_descriptions.append({
                'plan': plan_name,
                'variables': variables
            })
            
        except Exception as e:
            print(f"  ✗ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append({
                'plan': plan_name,
                'error': str(e)
            })
    
    # Check for repetition
    print("\n" + "=" * 70)
    print("REPETITION CHECK")
    print("=" * 70)
    slop_free = check_for_repetition(all_descriptions)
    
    # Summary
    print("\n" + "=" * 70)
    print("GENERATION SUMMARY")
    print("=" * 70)
    
    total = len(results)
    passed = sum(1 for r in results if r.get('qc_passed', False) and r.get('status') != '✗ OVER')
    over_limit = sum(1 for r in results if r.get('status') == '✗ OVER')
    
    print(f"Total descriptions: {total}")
    print(f"Passed QC: {passed}")
    print(f"Over limit: {over_limit}")
    print(f"Repetition: {'✓ ZERO' if slop_free else '✗ DETECTED'}")
    print(f"Success rate: {passed/total*100:.1f}%")
    
    if passed == total and slop_free:
        print("\n✅ All descriptions generated successfully with zero repetition!")
    else:
        print(f"\n⚠️  {total - passed} descriptions need attention")

if __name__ == '__main__':
    main()

