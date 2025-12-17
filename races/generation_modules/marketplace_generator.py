#!/usr/bin/env python3
"""
Marketplace Description Generator
Generates TrainingPeaks marketplace HTML descriptions from race + plan data
"""

import re
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generation_modules.gravel_god_copy_variations import (
    generate_varied_marketplace_copy,
    get_variation,
    get_non_negotiable_phrasing,
    get_race_specific_reference,
    CHECKMARK
)

def unicode_to_html_entities(text):
    """Convert Unicode characters to HTML entities to avoid encoding issues"""
    if not isinstance(text, str):
        return text
    
    # Map Unicode characters to HTML entities
    replacements = {
        '✓': '&#10004;',  # CHECKMARK
        '→': '&rarr;',    # ARROW
        '—': '&mdash;',   # EM DASH
        '•': '&bull;',    # BULLET
        '·': '&middot;',  # MIDDLE DOT
        '☆': '&#9734;',  # STAR
    }
    
    result = text
    for unicode_char, html_entity in replacements.items():
        result = result.replace(unicode_char, html_entity)
    
    return result

# Marketplace HTML Template (simplified design matching Unbound style)
# Uses varied copy from gravel_god_copy_variations.py
# Note: Uses HTML entities instead of Unicode to avoid encoding issues
MARKETPLACE_TEMPLATE = """<div style="font-family:'Courier New',monospace;color:#111;max-width:800px;margin:0 auto;line-height:1.5;font-size:16px">

<div style="margin-bottom:20px">
<p style="margin:0;font-size:24px;font-weight:700;line-height:1.3">{tier_philosophy}</p>
</div>

<div style="margin-bottom:14px">
<p style="margin:0;font-size:16px">{training_approach}</p>
</div>

<div style="margin-bottom:14px">
<h3 style="font-size:14px;text-transform:uppercase;border-bottom:1px solid #000;padding-bottom:5px;margin-bottom:8px">What the {plan_title} Includes</h3>
<p style="margin:0;font-size:16px">{plan_features}</p>
</div>

<div style="background:#f5f5f5;border:1px solid #ccc;border-left:5px solid #777;padding:12px;margin-bottom:14px">
<p style="margin:0 0 6px;font-size:14px"><strong>18,000+ Word Guide</strong></p>
<p style="margin:0 0 6px;font-size:14px;font-style:italic;color:#555">Everything you need in one manual. No gaps. No guesswork. All tested.</p>
<p style="margin:0;font-size:14px">{guide_content_summary}</p>
</div>

<div style="margin-bottom:14px">
<h3 style="font-size:14px;text-transform:uppercase;border-bottom:1px solid #000;padding-bottom:5px;margin-bottom:8px">Alternative?</h3>
<p style="margin:0;font-size:16px">{alternative_warning}</p>
</div>

<div style="background:#f5f5f5;border:1px solid #ccc;border-left:5px solid #777;padding:12px;margin-bottom:14px">
<h3 style="font-size:13px;text-transform:uppercase;margin:0 0 8px;color:#555">What This Plan Delivers</h3>
<p style="margin:0 0 8px;font-size:14px;font-weight:700">{delivery_headline}</p>
<p style="margin:0;font-size:14px">{delivery_details}</p>
</div>

<div style="margin-bottom:14px">
<p style="margin:0;font-size:16px">This is {race_name}. For people whose fitness needs to show up in results.</p>
</div>

<div style="border-top:2px solid #000;padding-top:10px">
<p style="margin:0;font-size:14px">Browse all plans: <a href="{race_url}" style="color:#111">{race_url}</a></p>
<p style="margin:8px 0 0;font-size:13px;color:#777">GRAVEL GOD CYCLING<br>gravelgodcoaching@gmail.com</p>
</div>

</div>"""

def get_masterclass_topics_html(race_data, copy_variations):
    """Generate masterclass topics HTML using varied copy"""
    topics_config = race_data.get("masterclass_topics", {})
    priority_order = topics_config.get("priority_order", [])
    
    # Map topic keys to copy variation keys
    topic_variation_map = {
        "heat": "topic_heat",
        "altitude": "topic_altitude",
        "fueling": "topic_fueling",
        "tactics": "topic_tactics",
        "mental": "topic_mental",
        "workout_execution": "topic_execution",
        "recovery_tires_strength": "topic_recovery",
    }
    
    # Map topic keys to display names
    topic_names = {
        "heat": "Heat Training",
        "altitude": "Altitude",
        "fueling": "Fueling",
        "tactics": "Race Tactics",
        "mental": "Mental Training",
        "workout_execution": "Workout Execution",
        "recovery_tires_strength": "Recovery, Tires, Strength"
    }
    
    html_lines = []
    for topic_key in priority_order[:6]:  # Limit to 6 topics
        variation_key = topic_variation_map.get(topic_key)
        if variation_key and variation_key in copy_variations:
            topic_name = topic_names.get(topic_key, topic_key.title())
            topic_desc = copy_variations[variation_key]
            # Convert Unicode to HTML entities
            topic_name = unicode_to_html_entities(topic_name)
            topic_desc = unicode_to_html_entities(topic_desc)
            html_lines.append(f'<p style="margin:4px 0;"><strong>&rarr; {topic_name}:</strong> {topic_desc}</p>')
    
    # Add recovery/tires/strength as combined line if not already included
    if "recovery_tires_strength" not in priority_order[:6] and "topic_recovery" in copy_variations:
        recovery_desc = unicode_to_html_entities(copy_variations["topic_recovery"])
        html_lines.append(f'<p style="margin-bottom:0;"><strong>&rarr; Recovery, Tires, Strength:</strong> {recovery_desc}</p>')
    
    if not html_lines:
        return '<p style="margin:4px 0;"><strong>&rarr; Training Guide:</strong> Comprehensive 35-page guide included</p>'
    
    return "\n".join(html_lines)

def get_tier_description(tier, level, plan_template):
    """Get tier description from plan template or defaults"""
    # Try to get from plan metadata first
    plan_metadata = plan_template.get("plan_metadata", {})
    target_athlete = plan_metadata.get("target_athlete", "")
    goal = plan_metadata.get("goal", "")
    
    # Build description
    tier_descriptions = {
        "ayahuasca": {
            "beginner": "You have almost no time but want to finish. This plan accepts that reality and maximizes every minute. Survival mode training that gets you across the line.",
            "intermediate": "You have 3-5 hours per week and want performance, not just completion. This plan uses G-Spot and Threshold because they deliver maximum fitness gains in minimum time.",
            "masters": "You're 50+ with minimal time (3-5 hrs/week) but want to finish strong. This plan combines autoregulation with time-efficient intensity. Recovery enables performance at 50+.",
            "save_my_race": "Emergency situation with minimal time. You already have base fitness—you just need race-specific sharpening. G-Spot and Threshold deliver maximum race readiness in minimum time."
        },
        "finisher": {
            "beginner": "You have a life outside cycling but want to do this right. This plan maximizes your 8-12 hours with focused quality over junk volume. The goal: cross the line strong, not crawl.",
            "intermediate": "You have 8-12 hours per week and want a solid finish. This plan uses polarized training (80% easy, 20% hard) to build durability and race-ready fitness.",
            "advanced": "You have 8-12 hours and want a strong finish. This plan uses the GOAT Method—pyramidal base, polarized weeks, limiter-focused blocks. Serious structure for serious athletes.",
            "masters": "You're 50+ with 8-12 hours per week. This plan combines autoregulation with polarized training. Recovery matters more than the workout at 50+.",
            "save_my_race": "Emergency situation, already has base fitness, needs final sharpening. G-Spot and Threshold deliver maximum race readiness in compressed timeframe."
        },
        "compete": {
            "intermediate": "You're not just finishing—you're racing. This plan builds the engine and the tactics to compete for your category. Polarized training for competitive performance.",
            "advanced": "You're racing for podium. This plan uses Block Periodization—concentrated loading on your biggest limiter, then race sharpening. Advanced training for advanced athletes.",
            "masters": "You're 50+ with performance goals. This plan combines autoregulation with polarized training. Recovery enables performance—you can't force fitness at 50+.",
            "save_my_race": "Emergency situation, already race-fit, needs final sharpening for competitive performance. Compressed Block Periodization delivers peak performance in 6 weeks."
        },
        "podium": {
            "advanced": "You're racing to win. This plan uses HVLI (High Volume, Low Intensity) or GOAT Method—massive aerobic volume builds extreme durability. Elite-level preparation.",
            "advanced_goat": "You're racing to win. This plan uses GOAT (Gravel Optimized Adaptive Training)—pyramidal base, polarized weeks, limiter-focused blocks, multi-signal autoregulation. Elite preparation."
        }
    }
    
    return tier_descriptions.get(tier, {}).get(level, f"{tier.title()} {level.title()} plan for {target_athlete}. {goal}")

def format_level_name(level):
    """Format level name for display"""
    level_map = {
        "beginner": "Beginner",
        "intermediate": "Intermediate",
        "advanced": "Advanced",
        "masters": "Masters (50+)",
        "save_my_race": "Save My Race (6 weeks)",
        "advanced_goat": "Advanced GOAT"
    }
    return level_map.get(level, level.title())

def generate_marketplace_html(race_data, plan_template, plan_info):
    """Generate marketplace description HTML with varied copy"""
    marketplace_vars = race_data.get("marketplace_variables", {})
    plan_metadata = plan_template.get("plan_metadata", {})
    
    # Get tier and level (lowercase for copy variations)
    tier_key = plan_info.get("tier", "").lower()
    level_key = plan_info.get("level", "").lower()
    
    # Generate varied copy for this variant
    copy = generate_varied_marketplace_copy(race_data, tier_key, level_key)
    
    # Get display names
    tier = plan_info.get("tier", "").title()
    level = format_level_name(plan_info.get("level", ""))
    weekly_hours = plan_info.get("weekly_hours", plan_metadata.get("target_hours", ""))
    plan_weeks = plan_info.get("weeks", plan_metadata.get("duration_weeks", 12))
    
    # Calculate number of workouts
    if plan_weeks == 6:
        num_workouts = 42  # 6 weeks * 7 days
    elif tier_key == "compete" and level_key == "advanced":
        num_workouts = 168  # Block options create more workouts
    elif tier_key == "podium" and level_key == "advanced_goat":
        num_workouts = 112  # Block options
    else:
        num_workouts = 84  # 12 weeks * 7 days
    
    # Get masterclass topics using varied copy
    masterclass_topics = get_masterclass_topics_html(race_data, copy)
    
    # Generate simplified content for new template using copy variations
    race_name = marketplace_vars.get("race_name", race_data["race_metadata"]["name"])
    plan_title = get_plan_title(tier_key, level_key)
    
    # Get race-specific data for formatting
    metadata = race_data.get('race_metadata', {})
    characteristics = race_data.get('race_characteristics', {})
    distance = metadata.get('distance_miles', 0)
    typical_weather = characteristics.get('typical_weather', '')
    climate = characteristics.get('climate', '')
    
    # Build weather adaptation text
    weather_adaptation = ""
    if 'unpredictable' in str(climate).lower() or 'unpredictable' in str(typical_weather).lower():
        weather_adaptation = "Weather adaptation training prepares you for variable conditions. "
    elif 'hot' in str(typical_weather).lower() or 'heat' in str(typical_weather).lower():
        weather_adaptation = "Heat adaptation in weeks 6-10 prepares you for race conditions. "
    elif 'cold' in str(typical_weather).lower() or 'cold' in str(climate).lower():
        weather_adaptation = "Weather adaptation training prepares you for variable conditions. "
    
    # Format copy variations with race-specific data
    level_display = level_key.replace('_', ' ').title()
    if level_key == 'save_my_race':
        level_display = 'Save My Race'
    
    # Get race-specific references (Mid South content) - ensures uniqueness per plan
    used_refs = set()
    race_terrain_ref = get_race_specific_reference(race_data, "terrain", tier_key, level_key, used_refs)
    race_weather_ref = get_race_specific_reference(race_data, "weather", tier_key, level_key, used_refs)
    race_location_ref = get_race_specific_reference(race_data, "location", tier_key, level_key, used_refs)
    race_character_ref = get_race_specific_reference(race_data, "character", tier_key, level_key, used_refs)
    race_challenge_ref = get_race_specific_reference(race_data, "challenges", tier_key, level_key, used_refs)
    
    tier_philosophy = copy.get('tier_philosophy', '')
    
    # Build training_approach with Mid South references integrated
    training_approach_base = copy.get('training_approach', '').format(
        plan_title=plan_title,
        weather_adaptation=weather_adaptation,
        weekly_hours=weekly_hours
    )
    
    # Inject Mid South-specific content naturally into training_approach
    # Strategy: Add 1-2 race references that make it clear this is for Mid South
    race_inserts = []
    if race_terrain_ref:
        race_inserts.append(race_terrain_ref)
    if race_weather_ref and len(race_inserts) < 2:
        race_inserts.append(race_weather_ref)
    
    if race_inserts:
        # Build natural race reference text with proper capitalization
        if len(race_inserts) == 2:
            # Capitalize first word of each reference
            ref1 = race_inserts[0][0].upper() + race_inserts[0][1:] if race_inserts[0] else ""
            ref2 = race_inserts[1][0].upper() + race_inserts[1][1:] if race_inserts[1] else ""
            race_text = f"{ref1} and {ref2}"
        else:
            race_text = race_inserts[0][0].upper() + race_inserts[0][1:] if race_inserts[0] else ""
        
        # Insert naturally into training_approach
        if f"The {plan_title} builds systems" in training_approach_base:
            # Insert as integrated phrase for natural grammar
            # "The Plan builds systems for Mid South's [reference]."
            # Make first word lowercase for natural flow, fix capitalization
            race_text_lower = race_text[0].lower() + race_text[1:] if race_text else ""
            # Capitalize proper nouns
            race_text_lower = race_text_lower.replace("oklahoma", "Oklahoma")
            race_text_lower = race_text_lower.replace("mid south", "Mid South")
            # Fix "weather lottery" capitalization (should be lowercase)
            race_text_lower = race_text_lower.replace("Weather lottery", "weather lottery")
            race_text_lower = race_text_lower.replace("Unpredictable", "unpredictable")
            race_text_lower = race_text_lower.replace("unpredictable conditions", "unpredictable conditions")
            
            # Insert as prepositional phrase - restructure sentence for better grammar
            # Original: "The Plan builds systems that work/function"
            # New: "The Plan builds systems for Mid South's [reference] that work/function"
            if f" that work" in training_approach_base and f"The {plan_title} builds systems that work" in training_approach_base:
                training_approach = training_approach_base.replace(
                    f"The {plan_title} builds systems that work",
                    f"The {plan_title} builds systems for Mid South's {race_text_lower} that work"
                )
            elif f" that function" in training_approach_base and f"The {plan_title} builds systems that function" in training_approach_base:
                training_approach = training_approach_base.replace(
                    f"The {plan_title} builds systems that function",
                    f"The {plan_title} builds systems for Mid South's {race_text_lower} that function"
                )
            else:
                # Fallback: insert after "builds systems" as separate clause
                training_approach = training_approach_base.replace(
                    f"The {plan_title} builds systems",
                    f"The {plan_title} builds systems for Mid South's {race_text_lower}"
                )
        elif weather_adaptation and weather_adaptation in training_approach_base:
            # Insert before weather adaptation as context
            training_approach = training_approach_base.replace(
                weather_adaptation,
                f"Mid South's {race_text.lower()}. {weather_adaptation}"
            )
        else:
            # Insert as new sentence after first sentence
            sentences = training_approach_base.split('. ')
            if len(sentences) > 1:
                training_approach = sentences[0] + '. ' + f"Mid South's {race_text.lower()}. " + '. '.join(sentences[1:])
            else:
                training_approach = training_approach_base + f" Mid South's {race_text.lower()}."
    else:
        training_approach = training_approach_base
    
    # Build plan_features with Mid South reference
    plan_features_base = copy.get('plan_features', '').format(
        level=level_display.lower(),
        distance=distance,
        weather_adaptation=weather_adaptation
    )
    
    # Add Mid South-specific challenge reference to plan_features
    if race_challenge_ref and race_challenge_ref not in plan_features_base:
        # Add at end if it fits naturally, with proper capitalization
        challenge_text = race_challenge_ref[0].lower() + race_challenge_ref[1:] if race_challenge_ref else ""
        plan_features = plan_features_base.rstrip('. ') + f". {challenge_text}."
    else:
        plan_features = plan_features_base
    # Build guide content summary with race-specific references
    guide_content_base = "Technical Skills Practice — Progressive drills for cornering, descending, rough terrain—weekly practice building competence. Race-Specific Preparation — Heat protocols, altitude adaptation (if needed), equipment choices. Training Fundamentals — Periodization principles that create predictable performance."
    
    # Add Mid South-specific content to guide summary if available
    if race_terrain_ref or race_challenge_ref:
        mid_south_note = ""
        if race_terrain_ref:
            mid_south_note = f"Mid South-specific: {race_terrain_ref.lower()}. "
        elif race_challenge_ref:
            mid_south_note = f"Mid South-specific: {race_challenge_ref.lower()}. "
        # Insert before "Heat protocols" for natural flow
        guide_content_summary = guide_content_base.replace(
            "Race-Specific Preparation — Heat protocols",
            f"Race-Specific Preparation — {mid_south_note}Heat protocols"
        ) if mid_south_note else guide_content_base
    else:
        guide_content_summary = guide_content_base
    alternative_warning = copy.get('alternative_warning', '')
    delivery_headline = copy.get('delivery_headline', 'Systematic progression eliminates guesswork. Training becomes results.')
    delivery_details = copy.get('delivery_details', '').format(distance=distance)
    
    # Get race URL - prioritize TrainingPeaks URL, then website, then generate
    race_url = marketplace_vars.get("trainingpeaks_url", "")
    if not race_url:
        race_url = race_data.get("race_metadata", {}).get("website", "")
    if not race_url:
        # Generate URL from race name slug
        race_slug = race_name.lower().replace(' ', '-').replace('the ', '').replace(' ', '-')
        race_url = f"https://gravelgodcycling.com/{race_slug}"
    
    # Fill template with simplified content
    html_content = MARKETPLACE_TEMPLATE.format(
        tier_philosophy=unicode_to_html_entities(tier_philosophy),
        training_approach=unicode_to_html_entities(training_approach),
        plan_title=unicode_to_html_entities(plan_title),
        plan_features=unicode_to_html_entities(plan_features),
        guide_content_summary=unicode_to_html_entities(guide_content_summary),
        alternative_warning=unicode_to_html_entities(alternative_warning),
        delivery_headline=unicode_to_html_entities(delivery_headline),
        delivery_details=unicode_to_html_entities(delivery_details),
        race_name=unicode_to_html_entities(race_name),
        race_url=race_url
    )
    
    # Validate character count (must be <4000)
    char_count = len(re.sub(r'<[^>]+>', '', html_content))  # Count text only
    if char_count > 4000:
        print(f"  ⚠️  Warning: Marketplace description is {char_count} characters (limit: 4000)")
        print(f"     Consider shortening race hook or reducing masterclass topics")
    
    return html_content


def get_plan_title(tier_key, level_key):
    """Get plan title from tier and level"""
    titles = {
        ('ayahuasca', 'beginner'): 'Survival Plan',
        ('ayahuasca', 'intermediate'): 'Time Crunched Plan',
        ('ayahuasca', 'masters'): '50+ Survival Plan',
        ('ayahuasca', 'save_my_race'): 'Emergency Plan',
        ('finisher', 'beginner'): 'First Timer Plan',
        ('finisher', 'intermediate'): 'Solid Finisher Plan',
        ('finisher', 'advanced'): 'Strong Finish Plan',
        ('finisher', 'masters'): 'Finisher Masters Plan',
        ('finisher', 'save_my_race'): 'Emergency Plan',
        ('compete', 'intermediate'): 'Competitive Plan',
        ('compete', 'advanced'): 'Podium Contender Plan',
        ('compete', 'masters'): '50+ Performance Plan',
        ('compete', 'save_my_race'): 'Emergency Plan',
        ('podium', 'advanced'): 'Elite Preparation',
        ('podium', 'advanced_goat'): 'The G.O.A.T. Plan',
    }
    return titles.get((tier_key, level_key), f'{level_key.title()} Plan')



