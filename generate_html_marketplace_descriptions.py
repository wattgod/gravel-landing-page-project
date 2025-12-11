#!/usr/bin/env python3
"""
TRAININGPEAKS MARKETPLACE DESCRIPTION GENERATOR - HTML VERSION
Uses tier-specific variation pools with proper HTML formatting
"""

import random
from TIER_SPECIFIC_SOLUTION_STATE_V3 import SOLUTION_STATE_OPENINGS
from TIER_SPECIFIC_CHOICE_FEATURES import CHOICE_FEATURES
from TIER_SPECIFIC_GUIDE_TOPICS_FINAL import GUIDE_TOPICS
from ALTERNATIVE_HOOKS_BEHAVIORAL import ALTERNATIVE_HOOKS
from TIER_SPECIFIC_STORY_JUSTIFICATIONS import STORY_JUSTIFICATIONS
from TIER_SPECIFIC_VALUE_PROP_BOXES import VALUE_PROP_BOXES
from GUIDE_INTRIGUE_LINES import GUIDE_INTRIGUE_LINES

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
        "Built for {race_name} demands. Designed for people making this work around a life, not building a life around this.",
        "{race_name}. For people who know the math doesn't work but show up regardless.",
        "This is for {race_name}. And for people with limited hours and unlimited determination.",
        "Designed for {race_name}. Built for people who need every single hour to count."
    ],
    
    "finisher": [
        "This is {race_name}. For people ready to stop surviving and start racing.",
        "Built for {race_name}. Designed for people who know there's another gear they're not finding.",
        "{race_name}. For people who want their fitness to show up predictably, not accidentally.",
        "This is for {race_name} demands. And for people ready to stop just finishing.",
        "Designed for {race_name}. Built for people who can commit 8-12 hours to structured progression."
    ],
    
    "compete": [
        "This is {race_name}. For people whose fitness needs to show up in results.",
        "Built for {race_name} demands. Designed for people training 12-18 hours who want precision, not just volume.",
        "{race_name}. For people done guessing why the next level won't arrive.",
        "This is for {race_name}. And for people ready to execute races, not just finish trained.",
        "Designed for {race_name}. Built for people who know the difference between training hard and training smart."
    ],
    
    "podium": [
        "This is {race_name}. For people who've been their own coach long enough.",
        "Built for {race_name}. Designed for people expecting to podium, not hoping to.",
        "{race_name}. For people who need structure to stay disciplined at 18+ hours per week.",
        "This is for {race_name} demands. And for people who know details separate podium from pack.",
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
# GENERATION LOGIC
# ============================================================================

def generate_html_description(tier, race_name, plan_seed, variation=""):
    """
    Generate HTML marketplace description with tier-specific variations
    
    Args:
        tier: One of ["ayahuasca", "finisher", "compete", "podium"]
        race_name: e.g., "Unbound Gravel 200"
        plan_seed: Unique seed for reproducible randomization
        variation: Optional plan variation (e.g., "intermediate", "beginner_masters")
    
    Returns:
        Complete HTML description string
    """
    
    # Validate tier
    if tier not in TIER_SPECS:
        raise ValueError(f"Invalid tier: {tier}. Must be one of {list(TIER_SPECS.keys())}")
    
    # Set seed for reproducible randomization
    random.seed(plan_seed)
    
    # Select components from variation pools (REDUCED for character limit)
    solution_state = random.choice(SOLUTION_STATE_OPENINGS[tier])
    choice_features_list = random.sample(CHOICE_FEATURES[tier], k=3)  # Down from 5
    guide_topics_list = random.sample(GUIDE_TOPICS[tier], k=3)  # Down from 5
    guide_intrigue = random.choice(GUIDE_INTRIGUE_LINES)  # Not tier-specific
    alternative_hook = random.choice(ALTERNATIVE_HOOKS[tier])
    story_justification = random.choice(STORY_JUSTIFICATIONS[tier])
    closing_statement = random.choice(CLOSING_STATEMENTS[tier])
    value_prop_box = random.choice(VALUE_PROP_BOXES[tier])
    
    # Get tier specs
    specs = TIER_SPECS[tier]
    
    # Generate clean plan name
    plan_name = generate_plan_name(tier, variation)
    
    # Format features and topics as flowing prose (not bullets)
    choice_features = format_as_prose(choice_features_list)
    guide_topics = format_as_prose(guide_topics_list)
    
    # Format closing statement with race name
    closing_statement = closing_statement.format(race_name=race_name)
    
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
    """Generate HTML descriptions for all 15 plans"""
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Plan variations (matches your 15 TrainingPeaks plans)
    plan_mapping = {
        "ayahuasca": ["beginner", "intermediate", "beginner_masters", "save_my_race"],
        "finisher": ["beginner", "intermediate", "advanced", "intermediate_masters", "save_my_race"],
        "compete": ["intermediate", "advanced", "intermediate_masters", "save_my_race"],
        "podium": ["advanced", "elite"]
    }
    
    generated = []
    
    for tier, variations in plan_mapping.items():
        tier_dir = os.path.join(output_dir, tier)
        os.makedirs(tier_dir, exist_ok=True)
        
        for variation in variations:
            seed = f"{race_name.lower().replace(' ', '_')}_{tier}_{variation}"
            html = generate_html_description(tier, race_name, seed, variation)
            
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
