#!/usr/bin/env python3
"""
TRAININGPEAKS MARKETPLACE DESCRIPTION GENERATOR - HTML VERSION
Uses tier-specific variation pools with proper HTML formatting
"""

import random
import hashlib
import re
from TIER_SPECIFIC_SOLUTION_STATE_V3 import SOLUTION_STATE_OPENINGS
from TIER_SPECIFIC_CHOICE_FEATURES import CHOICE_FEATURES
from TIER_SPECIFIC_GUIDE_TOPICS_FINAL import GUIDE_TOPICS
from ALTERNATIVE_HOOKS_BEHAVIORAL import ALTERNATIVES, MASTERS_ALTERNATIVES
from TIER_SPECIFIC_STORY_JUSTIFICATIONS import STORY_JUSTIFICATIONS
from TIER_SPECIFIC_VALUE_PROP_BOXES import VALUE_PROP_BOXES
from GUIDE_INTRIGUE_LINES import GUIDE_INTRIGUE_LINES
from SMR_SPECIFIC_VARIATIONS import (
    SMR_OPENINGS, SMR_STORY_JUSTIFICATIONS, SMR_FEATURES, 
    SMR_GUIDE_TOPICS, SMR_ALTERNATIVES, SMR_CLOSINGS, SMR_VALUE_PROP_BOXES
)

# Helper functions to extract content from HTML (same as validate_descriptions.py)
def extract_opening_from_html(html):
    """Extract opening paragraph from HTML."""
    match = re.search(r'<p style="margin:0;font-size:24px;font-weight:700;line-height:1.3">([^<]+)</p>', html)
    return match.group(1) if match else ""

def extract_story_from_html(html):
    """Extract story justification paragraph from HTML."""
    match = re.search(r'<div style="margin-bottom:14px">\s*<p style="margin:0;font-size:16px">([^<]+)</p>', html)
    return match.group(1) if match else ""

def extract_closing_from_html(html):
    """Extract closing statement from HTML."""
    match = re.search(r'<p style="margin:0;font-size:16px">(This is |Built for |Designed for |Unbound)[^<]+</p>', html)
    return match.group(1) if match else ""

def extract_alternative_from_html(html):
    """Extract alternative hook paragraph from HTML."""
    match = re.search(r'<h3[^>]*>Alternative\?</h3>\s*<p style="margin:0;font-size:16px">([^<]+)</p>', html)
    return match.group(1) if match else ""

# ============================================================================
# TIER CONFIGURATION
# ============================================================================

TIER_SPECS = {
    "ayahuasca": {
        "display_name": "Ayahuasca",
        "hours": "0-5 hours/week",
        "duration": "12 weeks",
        "workouts": 84,
        "price": "$99"
    },
    "finisher": {
        "display_name": "Finisher",
        "hours": "8-12 hours/week",
        "duration": "12 weeks",
        "workouts": 84,
        "price": "$99"
    },
    "compete": {
        "display_name": "Compete",
        "hours": "12-18 hours/week",
        "duration": "12 weeks",
        "workouts": 84,
        "price": "$99"
    },
    "podium": {
        "display_name": "Podium",
        "hours": "18+ hours/week",
        "duration": "12 weeks",
        "workouts": 84,
        "price": "$99"
    }
}

# ============================================================================
# TIER-SPECIFIC CLOSING STATEMENTS (ONE-TWO PUNCH)
# ============================================================================

CLOSING_STATEMENTS = {
    "ayahuasca": [
        "This is {race_name}. For people with 4 hours a week who are doing it anyway.",
        "Built for the race demands. Designed for people making this work around a life, not building a life around this.",
        "Unbound. For people who know the math doesn't work but show up regardless.",
        "This is for {race_name}. And for people with limited hours and unlimited determination.",
        "Designed for the race. Built for people who need every single hour to count."
    ],
    
    "finisher": [
        "This is {race_name}. For people ready to stop surviving and start racing.",
        "Built for the race. Designed for people who know there's another gear they're not finding.",
        "Unbound. For people who want their fitness to show up predictably, not accidentally.",
        "This is for race demands. And for people ready to stop just finishing.",
        "Designed for {race_name}. Built for people who can commit 8-12 hours to structured progression."
    ],
    
    "compete": [
        "This is {race_name}. For people whose fitness needs to show up in results.",
        "Built for the race demands. Designed for people training 12-18 hours who want precision, not just volume.",
        "Unbound. For people done guessing why the next level won't arrive.",
        "This is for the race. And for people ready to execute races, not just finish trained.",
        "Designed for {race_name}. Built for people who know the difference between training hard and training smart."
    ],
    
    "podium": [
        "This is {race_name}. For people who've been their own coach long enough.",
        "Built for the race. Designed for people expecting to podium, not hoping to.",
        "Unbound. For people who need structure to stay disciplined at 18+ hours per week.",
        "This is for race demands. And for people who know details separate podium from pack.",
        "Designed for {race_name}. Built for people training at elite volume who want precision, not just more work."
    ]
}

# Race-specific context
RACE_CONTEXT = {
    "unbound_200": {
        "name": "Unbound Gravel 200",
        "distance": "200 miles",
        "elevation": "11,000 feet",
        "conditions": "95°F June heat",
        "dnf_rate": "40%"
    }
}

# ============================================================================
# HTML TEMPLATE
# ============================================================================

HTML_TEMPLATE = """<div style="font-family:'Courier New',monospace;color:#111;max-width:800px;margin:0 auto;line-height:1.5;font-size:16px">

<div style="margin-bottom:20px">
<p style="margin:0;font-size:24px;font-weight:700;line-height:1.3">{solution_state_opening}</p>
</div>

<div style="margin-bottom:14px">
<p style="margin:0;font-size:16px">{story_justification}</p>
</div>

<div style="margin-bottom:14px">
<h3 style="font-size:14px;text-transform:uppercase;border-bottom:1px solid #000;padding-bottom:5px;margin-bottom:8px">What the {plan_name} Includes</h3>
<p style="margin:0;font-size:16px">{choice_features}</p>
</div>

<div style="background:#f5f5f5;border:1px solid #ccc;border-left:5px solid #777;padding:12px;margin-bottom:14px">
<p style="margin:0 0 6px;font-size:14px"><strong>18,000+ Word Guide</strong></p>
<p style="margin:0 0 6px;font-size:14px;font-style:italic;color:#555">{guide_intrigue}</p>
<p style="margin:0;font-size:14px">{guide_topics}</p>
</div>

<div style="margin-bottom:14px">
<h3 style="font-size:14px;text-transform:uppercase;border-bottom:1px solid #000;padding-bottom:5px;margin-bottom:8px">Alternative?</h3>
<p style="margin:0;font-size:16px">{alternative_hook}</p>
</div>

<div style="background:#f5f5f5;border:1px solid #ccc;border-left:5px solid #777;padding:12px;margin-bottom:14px">
<h3 style="font-size:13px;text-transform:uppercase;margin:0 0 8px;color:#555">What This Plan Delivers</h3>
<p style="margin:0 0 8px;font-size:14px;font-weight:700">{value_prop_philosophy}</p>
<p style="margin:0;font-size:14px">{value_prop_items}</p>
</div>

<div style="margin-bottom:14px">
<p style="margin:0;font-size:16px">{closing_statement}</p>
</div>

<div style="border-top:2px solid #000;padding-top:10px">
<p style="margin:0;font-size:14px">Browse all plans: <a href="https://gravelgodcycling.com/unbound-200" style="color:#111">gravelgodcycling.com/unbound-200</a></p>
<p style="margin:8px 0 0;font-size:13px;color:#777">GRAVEL GOD CYCLING<br>gravelgodcoaching@gmail.com</p>
</div>

</div>"""

# ============================================================================
# MASTERS-AWARE SELECTION
# ============================================================================

def is_masters_content(item):
    """
    Check if a variation contains Masters-specific content.
    
    Masters content typically includes:
    - Age references: 45+, 50+, age, older, veteran
    - Age-specific training: recovery protocols, adaptation timelines
    - Age-related language: "at your age", "as you age"
    
    Args:
        item: Can be a string (for most variations) or dict (for value prop boxes)
    """
    if not item:
        return False
    
    # Handle dict (value prop boxes)
    if isinstance(item, dict):
        # Check both philosophy and props
        text = item.get('philosophy', '') + ' ' + ' '.join(item.get('props', []))
    else:
        # Handle string
        text = item
    
    if not text:
        return False
    
    text_lower = text.lower()
    
    # Direct age references
    age_keywords = ['45+', '50+', 'age', 'older', 'veteran', 'masters']
    if any(keyword in text_lower for keyword in age_keywords):
        return True
    
    # Age-specific training language
    age_training_patterns = [
        'recovery protocols for',
        'adaptation timeline',
        'adaptation windows',
        'longer recovery',
        'age-appropriate',
        'at your age',
        'as you age',
        'recovery isn\'t optional',
        'recovery becomes the primary',
        'recovery architecture',
        'recovery-first',
        'injury prevention',
        'hrv monitoring',
        'hrv-based'
    ]
    if any(pattern in text_lower for pattern in age_training_patterns):
        return True
    
    return False

def select_masters_aware(pool, is_masters_plan, k=1):
    """
    Select from variation pool with Masters-aware filtering.
    
    Args:
        pool: List of variations to select from
        is_masters_plan: True if this is a Masters plan, False otherwise
        k: Number of items to select (for random.sample)
    
    Returns:
        Selected item(s) - single item if k=1, list if k>1
    """
    if not pool:
        return None if k == 1 else []
    
    # Filter pool based on Masters status
    if is_masters_plan:
        # Masters plans: ONLY select from Masters variations
        filtered_pool = [item for item in pool if is_masters_content(item)]
        # If no Masters variations found, fall back to all (shouldn't happen)
        if not filtered_pool:
            filtered_pool = pool
    else:
        # Non-Masters plans: EXCLUDE Masters variations
        filtered_pool = [item for item in pool if not is_masters_content(item)]
        # If filtering removes everything, fall back to all (shouldn't happen)
        if not filtered_pool:
            filtered_pool = pool
    
    # Select from filtered pool
    if k == 1:
        return random.choice(filtered_pool) if filtered_pool else None
    else:
        # For sample, ensure we don't request more than available
        sample_size = min(k, len(filtered_pool))
        return random.sample(filtered_pool, sample_size) if filtered_pool else []

# ============================================================================
# GENERATION LOGIC
# ============================================================================

def generate_html_description(tier, race_name, plan_seed, variation="", forced_closing=None, used_content=None):
    """
    Generate HTML marketplace description with tier-specific variations
    
    Args:
        tier: One of ["ayahuasca", "finisher", "compete", "podium"]
        race_name: e.g., "Unbound Gravel 200"
        plan_seed: Unique seed for reproducible randomization
        variation: Optional plan variation (e.g., "intermediate", "beginner_masters")
        forced_closing: Optional closing statement template to force (for uniqueness)
        used_content: Optional dict of used content sets to exclude from selection
    
    Returns:
        Complete HTML description string
    """
    
    # Validate tier
    if tier not in TIER_SPECS:
        raise ValueError(f"Invalid tier: {tier}. Must be one of {list(TIER_SPECS.keys())}")
    
    # Set seed for reproducible randomization
    random.seed(plan_seed)
    
    # Determine if this is a Save My Race plan (CRITICAL: Different product, different positioning)
    is_save_my_race = "save_my_race" in variation.lower()
    
    # Determine if this is a Masters plan
    is_masters_plan = "masters" in variation.lower()
    
    # Helper to select from pool excluding used content
    def select_excluding_used(pool, is_masters, used_set, k=1):
        """Select from pool excluding items in used_set"""
        # First filter by Masters
        filtered = select_masters_aware(pool, is_masters, k=len(pool))
        if isinstance(filtered, list):
            available = [item for item in filtered if item not in used_set]
        else:
            available = [filtered] if filtered and filtered not in used_set else []
        
        if not available:
            # Fallback: use all filtered if nothing available
            available = filtered if isinstance(filtered, list) else [filtered]
        
        if k == 1:
            return random.choice(available) if available else None
        else:
            return random.sample(available, min(k, len(available))) if available else []
    
    # Helper to select variation with required placeholder (guaranteed positioning)
    def select_variation_with_placeholder(pool, is_masters, required_placeholder, used_set):
        """
        Select variation containing required placeholder.
        Guarantees critical positioning elements appear.
        Falls back to any available variation if none contain placeholder.
        """
        # First filter by Masters
        filtered = select_masters_aware(pool, is_masters, k=len(pool))
        if isinstance(filtered, list):
            available = [item for item in filtered if item not in used_set]
        else:
            available = [filtered] if filtered and filtered not in used_set else []
        
        if not available:
            # Fallback: use all filtered if nothing available
            available = filtered if isinstance(filtered, list) else [filtered]
        
        # Prioritize variations with required placeholder
        with_placeholder = [item for item in available if required_placeholder in item]
        
        if with_placeholder:
            return random.choice(with_placeholder)
        else:
            # Fallback: select any available variation
            return random.choice(available) if available else None
    
    # Get used content sets (default to empty if not provided)
    used_opening = used_content.get('opening', set()) if used_content else set()
    used_story = used_content.get('story', set()) if used_content else set()
    used_alternative = used_content.get('alternative', set()) if used_content else set()
    used_features = used_content.get('features', set()) if used_content else set()
    
    # ========================================================================
    # SAVE MY RACE: COMPLETELY DIFFERENT POSITIONING (salvage/urgency, not performance)
    # ========================================================================
    if is_save_my_race:
        # SMR plans use ONLY SMR-specific variations
        # NOT regular tier variations (different product, different positioning)
        
        # Select SMR opening (salvage/urgency, 6 weeks)
        available_openings = [op for op in SMR_OPENINGS if op not in used_opening]
        solution_state = random.choice(available_openings) if available_openings else random.choice(SMR_OPENINGS)
        used_opening.add(solution_state)
        
        # Select SMR story (tier-specific, triage, minimum viable, sufficient not perfect)
        smr_stories = SMR_STORY_JUSTIFICATIONS.get(tier, [])
        available_stories = [s for s in smr_stories if s not in used_story]
        story_justification = random.choice(available_stories) if available_stories else random.choice(smr_stories) if smr_stories else "The {plan_name} is built for this exact situation: compressed timeline, race-critical focus, emergency protocols."
        used_story.add(story_justification)
        
        # Format SMR placeholders immediately (before plan_name is generated)
        # We'll format again later, but this ensures placeholders are handled
        
        # Select SMR features (6-week timeline, race-critical focus, emergency protocols)
        available_features = [f for f in SMR_FEATURES if f not in used_features]
        choice_features_list = random.sample(available_features, min(3, len(available_features))) if len(available_features) >= 3 else available_features
        for f in choice_features_list:
            used_features.add(f)
        
        # Select SMR guide topics (6-week arc, triage, emergency)
        guide_topics_list = random.sample(SMR_GUIDE_TOPICS, min(3, len(SMR_GUIDE_TOPICS)))
        
        # Select SMR alternative (defer or cram)
        available_alternatives = [a for a in SMR_ALTERNATIVES if a not in used_alternative]
        alternative_hook = random.choice(available_alternatives) if available_alternatives else random.choice(SMR_ALTERNATIVES)
        used_alternative.add(alternative_hook)
        
        # Select SMR closing (haven't been training, don't defer, 6 weeks)
        if forced_closing:
            closing_statement = forced_closing
        else:
            available_closings = [c for c in SMR_CLOSINGS if c not in used_content.get('closing', set())]
            closing_statement = random.choice(available_closings) if available_closings else random.choice(SMR_CLOSINGS)
        
        guide_intrigue = random.choice(GUIDE_INTRIGUE_LINES)  # Not tier-specific
        
        # SMR value prop box (tier-specific, use SMR-specific, NOT regular tier variations)
        smr_value_props = SMR_VALUE_PROP_BOXES.get(tier, [])
        if smr_value_props:
            # Convert string to dict format for consistency
            value_prop_philosophy = random.choice(smr_value_props)
            value_prop_box = {
                "philosophy": value_prop_philosophy,
                "props": ["Emergency mental preparation protocols", "Triage system: what matters most", "Minimum viable fitness approach", "Six-week compressed timeline"]
            }
        else:
            # Fallback
            value_prop_box = {
                "philosophy": "Six weeks isn't enough for perfect preparation. But it's enough to finish.",
                "props": ["Emergency protocols", "Triage approach", "Minimum viable fitness", "Six-week timeline"]
            }
    
    # ========================================================================
    # REGULAR PLANS: Standard tier-specific positioning
    # ========================================================================
    else:
        # ========================================================================
        # PHASE 1: GUARANTEE CRITICAL POSITIONING (use FULL pools, no Masters filtering)
        # ========================================================================
        # Positioning requirements trump content filtering.
        # Tier-specific positioning > Masters content specificity
        
        # GUARANTEED POSITIONING: Story must contain {plan_name} for full designation
        # Use FULL pool (not Masters-filtered) to ensure placeholder variations exist
        story_justification = select_variation_with_placeholder(
            STORY_JUSTIFICATIONS[tier],  # Full pool, no Masters filtering
            False,  # Don't filter for Masters - we need positioning first
            '{plan_name}', 
            used_story
        )
        used_story.add(story_justification)
        
        # GUARANTEED POSITIONING: First feature must contain {race_name} for race-specificity
        # Use FULL pool (not Masters-filtered) to ensure placeholder variations exist
        first_feature = select_variation_with_placeholder(
            CHOICE_FEATURES[tier],  # Full pool, no Masters filtering
            False,  # Don't filter for Masters - we need positioning first
            '{race_name}',
            used_features
        )
        used_features.add(first_feature)
        choice_features_list = [first_feature]
        
        # ========================================================================
        # PHASE 2: REMAINING VARIATIONS (Masters-filtered for content appropriateness)
        # ========================================================================
        # Now that positioning is guaranteed, filter remaining selections for Masters content
        
        # Select other components with Masters filtering
        solution_state = select_excluding_used(SOLUTION_STATE_OPENINGS[tier], is_masters_plan, used_opening, k=1)
        guide_topics_list = select_masters_aware(GUIDE_TOPICS[tier], is_masters_plan, k=3)
        guide_intrigue = random.choice(GUIDE_INTRIGUE_LINES)  # Not tier-specific, no Masters filtering needed
        
        # Select alternative from correct pool (Masters vs non-Masters)
        # Build key: tier_level for non-Masters, tier_masters for Masters
        if is_masters_plan:
            alt_key = f"{tier}_masters"
            alt_pool = MASTERS_ALTERNATIVES.get(alt_key, [])
        else:
            # Non-Masters: use tier + level from variation
            # Handle special cases: elite -> advanced, save_my_race uses SMR_ALTERNATIVES (handled separately)
            if variation == "elite":
                alt_key = f"{tier}_advanced"  # Elite uses advanced pool
            elif variation in ["beginner", "intermediate", "advanced"]:
                alt_key = f"{tier}_{variation}"
            else:
                # Fallback based on tier defaults
                if tier == "ayahuasca":
                    alt_key = "ayahuasca_beginner"
                elif tier == "finisher":
                    alt_key = "finisher_intermediate"
                elif tier == "compete":
                    alt_key = "compete_intermediate"
                else:  # podium
                    alt_key = "podium_advanced"
            alt_pool = ALTERNATIVES.get(alt_key, [])
        
        # Select from pool excluding used
        if alt_pool:
            available_alternatives = [a for a in alt_pool if a not in used_alternative]
            alternative_hook = random.choice(available_alternatives) if available_alternatives else random.choice(alt_pool)
        else:
            # Fallback if key not found
            fallback_key = f"{tier}_intermediate" if tier != "podium" else "podium_advanced"
            fallback_pool = ALTERNATIVES.get(fallback_key, [])
            available_alternatives = [a for a in fallback_pool if a not in used_alternative]
            alternative_hook = random.choice(available_alternatives) if available_alternatives else (random.choice(fallback_pool) if fallback_pool else "Or you could keep training without structure.")
        used_alternative.add(alternative_hook)
        
        # Remaining features: Masters-filtered random selection
        for i in range(2):  # Need 2 more features (already have first one)
            available_features = select_masters_aware(CHOICE_FEATURES[tier], is_masters_plan, k=len(CHOICE_FEATURES[tier]))
            if isinstance(available_features, list):
                available = [f for f in available_features if f not in used_features]
                feature = random.choice(available) if available else random.choice(available_features)
            else:
                feature = available_features
            choice_features_list.append(feature)
            used_features.add(feature)
        
        # Use forced closing if provided, otherwise random
        if forced_closing:
            closing_statement = forced_closing
        else:
            closing_statement = random.choice(CLOSING_STATEMENTS[tier])  # No Masters variations in closings
        
        value_prop_box = select_masters_aware(VALUE_PROP_BOXES[tier], is_masters_plan, k=1)
    
    # Get tier specs
    specs = TIER_SPECS[tier]
    
    # Generate clean plan name
    plan_name = generate_plan_name(tier, variation)
    
    # Format placeholders in SMR content (must happen after plan_name is generated)
    if is_save_my_race:
        # Format SMR opening
        if '{race_name}' in solution_state:
            solution_state = solution_state.format(race_name=race_name)
        # Format SMR story
        if '{plan_name}' in story_justification or '{race_name}' in story_justification:
            story_justification = story_justification.format(plan_name=plan_name, race_name=race_name)
        # Format SMR closing
        if '{race_name}' in closing_statement:
            closing_statement = closing_statement.format(race_name=race_name)
    
    # Format story justification with plan_name and race_name (if placeholders exist)
    # This allows variations to include full plan designation and race name
    # Works for regular plans (SMR already formatted above)
    if not is_save_my_race:
        if '{plan_name}' in story_justification or '{race_name}' in story_justification:
            story_justification = story_justification.format(plan_name=plan_name, race_name=race_name)
    
    # Also format alternative_hook if it has placeholders (for both SMR and regular)
    if '{plan_name}' in alternative_hook or '{race_name}' in alternative_hook:
        alternative_hook = alternative_hook.format(plan_name=plan_name, race_name=race_name)
    
    # Format features and topics as flowing prose (not bullets)
    # CRITICAL: Format placeholders in features BEFORE formatting as prose
    formatted_features = []
    for feature in choice_features_list:
        if '{race_name}' in feature or '{plan_name}' in feature:
            feature = feature.format(race_name=race_name, plan_name=plan_name)
        formatted_features.append(feature)
    choice_features = format_as_prose(formatted_features)
    
    # Format placeholders in guide topics BEFORE formatting as prose
    formatted_topics = []
    for topic in guide_topics_list:
        if '{race_name}' in topic or '{plan_name}' in topic:
            topic = topic.format(race_name=race_name, plan_name=plan_name)
        formatted_topics.append(topic)
    guide_topics = format_as_prose(formatted_topics)
    
    # Format closing statement with race name (handle shorthand variations)
    # Works for both SMR and regular plans
    if '{race_name}' in closing_statement:
        closing_statement = closing_statement.format(race_name=race_name)
    # Shorthand variations use "the race", "Unbound", "race demands" - no formatting needed
    
    # Format value prop box
    value_prop_philosophy = value_prop_box['philosophy']
    value_prop_items = " • ".join(value_prop_box['props'])
    
    # Build HTML description
    html = HTML_TEMPLATE.format(
        plan_name=plan_name,
        race_name=race_name,
        solution_state_opening=solution_state,
        story_justification=story_justification,
        choice_features=choice_features,
        guide_topics=guide_topics,
        guide_intrigue=guide_intrigue,
        alternative_hook=alternative_hook,
        closing_statement=closing_statement,
        value_prop_philosophy=value_prop_philosophy,
        value_prop_items=value_prop_items,
        duration=specs['duration'],
        hours=specs['hours'],
        workouts=specs['workouts'],
        price=specs['price']
    )
    
    return html

# ============================================================================
# FORMATTING HELPERS
# ============================================================================

def generate_plan_name(tier, variation):
    """
    Generate clean plan name from tier and variation
    
    Examples:
        tier="finisher", variation="intermediate" → "Finisher Intermediate plan"
        tier="ayahuasca", variation="beginner_masters" → "Ayahuasca Masters plan"
        tier="podium", variation="elite" → "Podium Elite plan"
    """
    # Capitalize tier name
    tier_name = tier.capitalize()
    
    # Handle variation naming
    if not variation:
        return f"{tier_name} plan"
    
    # Special cases
    if "masters" in variation:
        return f"{tier_name} Masters plan"
    elif "save_my_race" in variation:
        return f"{tier_name} Save My Race plan"
    elif variation == "elite":
        return f"{tier_name} Elite plan"
    else:
        # Standard variations: beginner, intermediate, advanced
        var_name = variation.replace("_", " ").title()
        return f"{tier_name} {var_name} plan"

def format_as_prose(items):
    """
    Format list items as flowing prose instead of bullets
    Removes markdown bold markers and section references
    """
    # Clean up each item
    cleaned = []
    for item in items:
        # Remove markdown bold markers
        clean = item.replace('**', '')
        # Remove section references like (Section 7)
        import re
        clean = re.sub(r'\(Section \d+\)', '', clean)
        # Remove leading/trailing whitespace
        clean = clean.strip()
        cleaned.append(clean)
    
    # Join with periods and spaces
    return ". ".join(cleaned) + "."

# ============================================================================
# BATCH GENERATION
# ============================================================================

def generate_all_html_descriptions(race_name="Unbound Gravel 200", output_dir="output/html_descriptions"):
    """Generate HTML descriptions for all 15 plans with deduplication"""
    
    import os
    import hashlib
    os.makedirs(output_dir, exist_ok=True)
    
    # Plan variations (matches your 15 TrainingPeaks plans)
    plan_mapping = {
        "ayahuasca": ["beginner", "intermediate", "beginner_masters", "save_my_race"],
        "finisher": ["beginner", "intermediate", "advanced", "intermediate_masters", "save_my_race"],
        "compete": ["intermediate", "advanced", "intermediate_masters", "save_my_race"],
        "podium": ["advanced", "elite"]
    }
    
    # Track used content to prevent duplicates
    used_content = {
        'opening': set(),
        'story': set(),
        'closing': set(),
        'alternative': set()
    }
    
    # Track used closings globally (after formatting) to ensure uniqueness across all tiers
    used_closings_global = set()  # Track formatted closings across all tiers
    
    generated = []
    max_attempts = 200  # Maximum regeneration attempts per plan (increased for better uniqueness)
    plan_index = 0  # Global plan counter for deterministic selection
    
    for tier, variations in plan_mapping.items():
        tier_dir = os.path.join(output_dir, tier)
        os.makedirs(tier_dir, exist_ok=True)
        
        for variation in variations:
            plan_index += 1
            # Create unique seed using hash for better distribution
            plan_id = f"{race_name.lower().replace(' ', '_')}_{tier}_{variation}"
            seed_hash = hashlib.md5(plan_id.encode()).hexdigest()
            seed = f"{plan_id}_{seed_hash[:8]}"
            
            # Pre-select a unique closing for this plan
            # SMR plans use SMR_CLOSINGS, regular plans use CLOSING_STATEMENTS[tier]
            is_save_my_race = "save_my_race" in variation.lower()
            
            if is_save_my_race:
                # SMR plans: use tier-specific SMR closings
                closing_pool = SMR_CLOSINGS.get(tier, [])
                if not closing_pool:
                    # Fallback to first tier available
                    closing_pool = list(SMR_CLOSINGS.values())[0] if SMR_CLOSINGS else []
            else:
                # Regular plans: use tier-specific closings
                closing_pool = CLOSING_STATEMENTS[tier]
            
            selected_closing_template = None
            for closing_template in closing_pool:
                formatted_closing = closing_template.format(race_name=race_name)
                if formatted_closing not in used_closings_global:
                    selected_closing_template = closing_template
                    used_closings_global.add(formatted_closing)
                    break
            
            # If all closings for this tier are duplicates, use the first one anyway
            # (This shouldn't happen with diverse closing pools, but provides fallback)
            if not selected_closing_template:
                selected_closing_template = closing_pool[0]
                formatted_closing = selected_closing_template.format(race_name=race_name)
                used_closings_global.add(formatted_closing)
            
            # Generate with forced closing and active deduplication
            # Pass used_content to generator so it can exclude used items BEFORE selection
            attempt_seed = seed
            random.seed(attempt_seed)
            html = generate_html_description(tier, race_name, attempt_seed, variation, forced_closing=selected_closing_template, used_content=used_content)
            
            # Extract and track content (generator already excluded used items, so these should be unique)
            opening = extract_opening_from_html(html)
            story = extract_story_from_html(html)
            closing = extract_closing_from_html(html)
            alternative = extract_alternative_from_html(html)
            
            # Track used content (generator should have already excluded these, but verify)
            if opening:
                used_content['opening'].add(opening)
            if story:
                used_content['story'].add(story)
            if closing:
                used_content['closing'].add(closing)
            if alternative:
                used_content['alternative'].add(alternative)
            
            filename = f"{tier}_{variation}.html"
            filepath = os.path.join(tier_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            
            generated.append(filename)
            print(f"✓ Generated: {filename}")
    
    print(f"\n✓ Total generated: {len(generated)} HTML descriptions")
    print(f"✓ Output directory: {output_dir}")
    
    return generated

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    # Test single generation
    print("Testing HTML generation...\n")
    
    html = generate_html_description(
        tier="finisher",
        race_name="Unbound Gravel 200",
        plan_seed="unbound_200_finisher_intermediate",
        variation="intermediate"
    )
    
    print("SAMPLE OUTPUT (first 1000 chars):")
    print("=" * 80)
    print(html[:1000])
    print("..." if len(html) > 1000 else "")
    print("=" * 80)
    print(f"\nTotal length: {len(html)} characters")
    
    # Generate all 15
    print("\n\nGenerating all 15 HTML descriptions...")
    print("=" * 80)
    generate_all_html_descriptions()
