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

# Marketplace HTML Template (neo-brutalist styling)
# Uses varied copy from gravel_god_copy_variations.py
# Note: Uses HTML entities instead of Unicode to avoid encoding issues
MARKETPLACE_TEMPLATE = """<div style="font-family:'Courier New',monospace;background:#F5F5DC;padding:20px;">
<div style="background:#59473C;color:#F5F5DC;padding:12px 20px;display:inline-block;margin-bottom:16px;">
GRAVEL GOD CYCLING
---
</div>
<div style="border-left:4px solid #40E0D0;padding-left:16px;margin-bottom:20px;">
<p style="font-size:18px;color:#000;margin:0;"><strong>{race_hook}</strong></p>
<p style="font-size:14px;color:#59473C;margin-top:8px;">{race_hook_detail}</p>
</div>
<div style="border:4px solid #000;box-shadow:8px 8px 0 #000;padding:20px;margin:20px 0;background:#fff;">
<h2 style="margin-top:0;color:#000;">{fifteen_plans_headline}</h2>
<p>{fifteen_plans_body}</p>
<p style="margin-bottom:0;">{philosophy_tagline}</p>
</div>
<div style="border:4px solid #000;box-shadow:8px 8px 0 #40E0D0;padding:20px;margin:20px 0;background:#fff;">
<h2 style="margin-top:0;color:#000;">{masterclass_headline}</h2>
<p style="margin-bottom:12px;">{masterclass_intro}</p>
{masterclass_topics}
</div>
<div style="border:4px solid #000;box-shadow:8px 8px 0 #59473C;padding:20px;margin:20px 0;background:#fff;">
<h2 style="margin-top:0;color:#000;">BUILT FOR {race_name}</h2>
{non_negotiables_html}
<p style="margin-top:12px;margin-bottom:0;font-size:14px;">Plus: {plan_weeks} weeks, {num_workouts} workouts (Zwift/TrainerRoad/Wahoo/Garmin), race week protocol, gear checklist.</p>
</div>
<div style="background:#59473C;border:4px solid #000;padding:20px;margin:20px 0;color:#F5F5DC;">
---
<h2 style="margin-top:0;color:#40E0D0;">{tier} | {level} | {weekly_hours} HRS/WEEK</h2>
<p style="margin-bottom:0;">{tier_description}</p>
<p style="margin-top:8px;margin-bottom:0;font-size:12px;font-style:italic;">{level_modifier}</p>
</div>
<div style="background:#000;color:#F5F5DC;padding:20px;text-align:center;border:4px solid #000;">
<div style="font-size:24px;font-weight:bold;letter-spacing:4px;">GRAVEL GOD</div>
<div style="font-size:14px;color:#40E0D0;margin:8px 0;">gravelgodcycling.com</div>
<div style="font-size:13px;font-style:italic;">Become what you are.</div>
</div>
<p style="font-size:12px;color:#59473C;text-align:center;margin-top:12px;">gravelgodcoaching@gmail.com</p>
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
    
    # Build non-negotiables HTML from race-specific requirements
    # Use race_data non-negotiables directly to preserve race-specific content
    # Don't rephrase - the requirements are already race-specific and well-written
    non_negs = race_data.get("non_negotiables", [])[:3]
    non_negotiables = []
    for nn in non_negs:
        if isinstance(nn, dict):
            # Extract requirement text from dict - preserve race-specific wording exactly
            req_text = nn.get('requirement', str(nn))
        else:
            # Already a string
            req_text = str(nn)
        # Use original requirement text directly to preserve race-specific details
        # (get_non_negotiable_phrasing was losing race-specific content)
        non_negotiables.append(f"&#10004; {req_text}")  # Use HTML entity instead of Unicode
    
    # Convert any remaining Unicode characters to HTML entities
    non_negotiables_html = "\n".join([
        f'<p style="margin:4px 0;">{unicode_to_html_entities(nn)}</p>' 
        for nn in non_negotiables
    ])
    
    # Fill template with varied copy (convert Unicode to HTML entities)
    html_content = MARKETPLACE_TEMPLATE.format(
        race_hook=unicode_to_html_entities(race_data.get("race_hooks", {}).get("punchy", marketplace_vars.get("race_hook", ""))),
        race_hook_detail=unicode_to_html_entities(race_data.get("race_hooks", {}).get("detail", marketplace_vars.get("race_hook_detail", ""))),
        fifteen_plans_headline=unicode_to_html_entities(copy['fifteen_plans_headline']),
        fifteen_plans_body=unicode_to_html_entities(copy['fifteen_plans_body']),
        philosophy_tagline=unicode_to_html_entities(copy['philosophy_tagline']),
        masterclass_headline=unicode_to_html_entities(copy['masterclass_headline']),
        masterclass_intro=unicode_to_html_entities(copy['masterclass_intro']),
        masterclass_topics=masterclass_topics,  # Already converted in get_masterclass_topics_html
        race_name=unicode_to_html_entities(marketplace_vars.get("race_name", race_data["race_metadata"]["name"])),
        non_negotiables_html=non_negotiables_html,  # Already converted above
        plan_weeks=plan_weeks,
        num_workouts=num_workouts,
        tier=unicode_to_html_entities(tier),
        level=unicode_to_html_entities(level),
        weekly_hours=weekly_hours,
        tier_description=unicode_to_html_entities(copy['tier_description']),
        level_modifier=unicode_to_html_entities(copy['level_modifier'])
    )
    
    # Validate character count (must be <4000)
    char_count = len(re.sub(r'<[^>]+>', '', html_content))  # Count text only
    if char_count > 4000:
        print(f"  ⚠️  Warning: Marketplace description is {char_count} characters (limit: 4000)")
        print(f"     Consider shortening race hook or reducing masterclass topics")
    
    return html_content

