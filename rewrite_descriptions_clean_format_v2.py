#!/usr/bin/env python3
"""
Rewrite marketplace descriptions in clean prose format
Matching the Finisher Intermediate example format exactly
"""

from pathlib import Path
import re

def clean_text(text):
    """Remove section references and clean up"""
    text = re.sub(r'\(Section \d+\)', '', text)
    text = re.sub(r'Section \d+', '', text)
    text = re.sub(r'  +', ' ', text)
    return text.strip()

def extract_content_from_markdown(markdown_text):
    """Extract key content from markdown"""
    lines = markdown_text.split('\n')
    content = {
        'title': '',
        'intro': '',
        'what_you_get': '',
        'plan_includes': [],
        'guide_covers': [],
        'alternative': '',
        'numbers': {},
        'what_isnt': '',
        'purchase_includes': []
    }
    
    i = 0
    
    # Get title
    if lines[0].startswith('# '):
        content['title'] = lines[0][2:].strip()
        i = 1
    
    # Get intro (first paragraph after title, skip empty lines)
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].strip() and not lines[i].startswith('##'):
        content['intro'] = clean_text(lines[i])
        i += 1
    
    # Parse sections
    current_section = None
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('## '):
            section = line[3:].strip()
            if 'What You Get' in section:
                current_section = 'what_you_get'
            elif 'This Plan Includes' in section:
                current_section = 'plan_includes'
            elif 'Training Guide' in section or 'Guide Covers' in section:
                current_section = 'guide_covers'
            elif 'Alternative' in section:
                current_section = 'alternative'
            elif 'Real Numbers' in section:
                current_section = 'numbers'
            elif 'What This Isn' in section:
                current_section = 'what_isnt'
            elif 'Purchase includes' in section:
                current_section = 'purchase_includes'
            else:
                current_section = None
            i += 1
            continue
        
        if line.startswith('- '):
            item = clean_text(line[2:])
            # Remove bold markers but keep text
            item = re.sub(r'\*\*([^*]+)\*\*', r'\1', item)
            if current_section == 'plan_includes':
                content['plan_includes'].append(item)
            elif current_section == 'guide_covers':
                content['guide_covers'].append(item)
            elif current_section == 'purchase_includes':
                content['purchase_includes'].append(item)
            i += 1
            continue
        
        if line and current_section == 'alternative':
            content['alternative'] = clean_text(line)
            i += 1
            continue
        
        if line and current_section == 'what_isnt':
            if not content['what_isnt']:
                content['what_isnt'] = clean_text(line)
            else:
                content['what_isnt'] += ' ' + clean_text(line)
            i += 1
            continue
        
        if line and current_section == 'what_you_get':
            if not content['what_you_get']:
                content['what_you_get'] = clean_text(line)
            else:
                content['what_you_get'] += ' ' + clean_text(line)
            i += 1
            continue
        
        i += 1
    
    return content

def write_clean_prose_description(content, tier, weeks):
    """Write description in clean prose format matching example"""
    
    workouts = 84 if weeks == 12 else 42
    
    # Title
    desc = f"# {content['title']}\n\n"
    
    # Opening paragraph: tier-specific promise (use tier-specific openings from user's example)
    openings = {
        'ayahuasca': "You have 4 hours a week. Unbound takes 10-14 hours. The math doesn't work. You're doing it anyway. This plan makes it work—not through volume you don't have, but through structure that maximizes every hour.",
        'finisher': "You've finished events before. You know you can do the distance. But you also know there's another gear you're not finding. This plan unlocks it—not through more volume, but through better structure. The difference between finishing and competing isn't more hours. It's better hours.",
        'compete': "You're training 12-18 hours. You're doing the work. But something's not translating to race day. This plan fixes that—not through more volume, but through better distribution. The difference between training and racing isn't more hours. It's better hours.",
        'podium': "You've been your own coach long enough. You know self-coaching has blind spots. This plan removes them—not through more volume, but through better periodization. The difference between finishing strong and podiuming isn't more hours. It's better structure."
    }
    desc += f"{openings.get(tier, openings['finisher'])}\n\n"
    
    # Second paragraph: contrast (what they've been doing wrong)
    contrast = {
        'ayahuasca': "Most time-crunched riders try to cram high-volume training into low-volume weeks. It doesn't work. This plan uses high-intensity intervals and efficient structure to maximize adaptation from minimal time. Your fitness will show up predictably, not accidentally.",
        'finisher': "Most recreational riders train randomly: hard when they feel good, easy when they don't. This plan breaks that pattern. Your fitness will show up predictably, not accidentally. The training zones are scientific but simple. The workout progression is systematic but flexible. Performance arrives when you need it.",
        'compete': "You're training 12-18 hours but results aren't translating. Most riders at this volume train too much in the middle—not hard enough, not easy enough. This plan uses polarized training: 80% easy, 20% hard. The structure is systematic. The progression is clear. Race fitness arrives when you need it.",
        'podium': "You've been your own coach long enough. You know self-coaching has blind spots. This plan removes them. The periodization is precise. The intensity distribution is optimized. The taper is calculated. Performance peaks when you need it."
    }
    desc += f"{contrast.get(tier, contrast['finisher'])}\n\n"
    
    # Third paragraph: what the plan includes (prose, bold lead-in)
    includes_parts = []
    if content['plan_includes']:
        for item in content['plan_includes'][:5]:
            # Clean up item and add to prose
            clean_item = item.replace('—', '—').strip()
            if clean_item:
                includes_parts.append(clean_item)
    
    # If we don't have enough from markdown, use tier-specific defaults
    if not includes_parts:
        defaults = {
            'ayahuasca': [
                "Dress rehearsal rides at manageable duration (5 hours max) that still validate your race-day systems",
                "Outdoor options for every workout—no trainer required, just structured execution",
                "Skills-first approach that prevents mechanical failures and crashes from killing your race",
                "Race-pace power targets calibrated for your available training time, not fantasy watts",
                "High-efficiency workouts designed for maximum adaptation in minimal time—every session under 90 minutes"
            ],
            'finisher': [
                "Race-specific power zones calibrated from YOUR FTP, with RPE guidance when power isn't available",
                "Technical skills that keep you upright when others crash",
                "Structured taper in final 2 weeks that peaks fitness without losing form",
                "Progressive overload with clear weekly targets—intensity increases predictably, not randomly",
                "Pacing strategy for 10-14 hour efforts—how to start conservatively and finish strong"
            ],
            'compete': [
                "Polarized training structure: 80% easy, 20% hard—no middle zone",
                "Threshold and VO2max blocks that build race-specific power",
                "Long rides that test fueling, pacing, and mental strategies",
                "Technical skills for high-speed gravel racing",
                "Precision taper that peaks fitness without losing form"
            ],
            'podium': [
                "Block periodization: concentrated intensity blocks followed by recovery",
                "Precision intensity distribution optimized for your volume",
                "Race-specific power targets and pacing strategies",
                "Technical skills for podium-level racing",
                "Calculated taper that delivers peak performance"
            ]
        }
        includes_parts = defaults.get(tier, defaults['finisher'])
    
    includes_text = f"**{workouts} structured workouts across {weeks} weeks.** "
    # Clean up includes parts
    clean_includes_parts = []
    for part in includes_parts:
        clean_part = part.replace('—', '—').strip()
        # Remove any remaining section references
        clean_part = re.sub(r'\(Section \d+\)', '', clean_part)
        clean_part = re.sub(r'Section \d+', '', clean_part)
        clean_part = re.sub(r'  +', ' ', clean_part)
        if clean_part:
            clean_includes_parts.append(clean_part)
    includes_text += '. '.join(clean_includes_parts) + '.'
    desc += f"{includes_text}\n\n"
    
    # Fourth paragraph: guide highlights (prose)
    guide_parts = []
    if content['guide_covers']:
        for item in content['guide_covers'][:4]:
            # Extract topic and description
            clean_item = item.replace('—', '—').strip()
            if clean_item:
                guide_parts.append(clean_item)
    
    if not guide_parts:
        defaults = {
            'ayahuasca': [
                "Training fundamentals that work with limited hours, not against them",
                "Race week protocol that doesn't assume you have time for elaborate tapers",
                "Mental training for 10+ hour efforts when your body isn't fully trained",
                "Workout execution—how to nail each session type in under 90 minutes"
            ],
            'finisher': [
                "Polarized principles that build both endurance and speed",
                "How base, build, and peak phases stack together for race day",
                "Precise power targets and RPE guidance for structured progression",
                "Proven taper sequence"
            ],
            'compete': [
                "Polarized training principles: 80% easy, 20% hard",
                "How threshold and VO2max blocks build race-specific power",
                "Race tactics and pacing strategies for competitive racing",
                "Precision taper that peaks fitness"
            ],
            'podium': [
                "Block periodization principles",
                "Precision intensity distribution and recovery protocols",
                "Race tactics for podium-level competition",
                "Calculated taper that delivers peak performance"
            ]
        }
        guide_parts = defaults.get(tier, defaults['finisher'])
    
    guide_text = "**Your training guide delivers**: "
    # Clean up guide parts - remove section references and fix spacing
    clean_guide_parts = []
    for part in guide_parts:
        clean_part = part.replace(' — ', ' — ').replace('  ', ' ').strip()
        # Remove any remaining section references
        clean_part = re.sub(r'\(Section \d+\)', '', clean_part)
        clean_part = re.sub(r'Section \d+', '', clean_part)
        clean_part = re.sub(r'  +', ' ', clean_part)
        if clean_part:
            clean_guide_parts.append(clean_part)
    guide_text += '. '.join(clean_guide_parts) + '.'
    desc += f"{guide_text}\n\n"
    
    # Fifth paragraph: the alternative
    if content['alternative']:
        desc += f"**The alternative?** {content['alternative']}\n\n"
    else:
        alt_text = {
            'ayahuasca': "You try to train like someone with 12+ hours. You burn out by week 6. Or you train randomly and hope fitness appears.",
            'finisher': "You hire a coach who doesn't understand gravel racing. They give you road intervals and century training. You finish Unbound but never learn to race it. Or you keep training randomly and hope fitness appears.",
            'compete': "You keep training in the middle zone. You finish but never compete. Or you overtrain and arrive at race day exhausted.",
            'podium': "You keep self-coaching with blind spots. You finish strong but never podium. Or you hire a coach who doesn't understand gravel racing."
        }
        desc += f"**The alternative?** {alt_text.get(tier, alt_text['finisher'])}\n\n"
    
    # Sixth paragraph: real numbers
    hours_text = {
        'ayahuasca': '0-5 hours per week',
        'finisher': '8-12 hours per week',
        'compete': '12-18 hours per week',
        'podium': '18-25+ hours per week'
    }
    desc += f"**Real numbers:** {weeks} weeks, {workouts} workouts, {hours_text.get(tier, '8-12 hours per week')}. FTP-based zones with RPE guidance. 18,000+ word guide covering training, technical skills, race execution. $99.\n\n"
    
    # Closing paragraphs
    what_isnt_text = "This isn't a generic training plan with \"Unbound Gravel 200\" stuck on top. It's designed for the specific demands of this race—terrain, distance, conditions. Every workout, every rest day, every taper choice is built around getting you ready for this event."
    desc += f"{what_isnt_text}\n\n"
    
    desc += "If you're looking for magic bullets or shortcuts, this won't deliver. If you're looking for structured training that respects reality and builds race-ready fitness, this is it.\n\n"
    
    # Purchase includes
    desc += "**Purchase includes:** "
    if content['purchase_includes']:
        items = [item.replace('**', '').replace('- ', '') for item in content['purchase_includes']]
        desc += ', '.join(items) + '.\n\n'
    else:
        desc += f"{weeks}-week structured training plan ({workouts} workouts), complete training guide (18,000+ words), race-specific preparation protocols, lifetime access to all plan updates.\n\n"
    
    desc += "Train with purpose. Race with confidence.\n"
    
    return desc

# Plan mapping
plan_mapping = {
    "1. Ayahuasca Beginner (12 weeks)": {"file": "ayahuasca/ayahuasca_beginner.txt", "tier": "ayahuasca", "weeks": 12},
    "2. Ayahuasca Intermediate (12 weeks)": {"file": "ayahuasca/ayahuasca_intermediate.txt", "tier": "ayahuasca", "weeks": 12},
    "3. Ayahuasca Masters (12 weeks)": {"file": "ayahuasca/ayahuasca_beginner_masters.txt", "tier": "ayahuasca", "weeks": 12},
    "4. Ayahuasca Save My Race (6 weeks)": {"file": "ayahuasca/ayahuasca_save_my_race.txt", "tier": "ayahuasca", "weeks": 6},
    "5. Finisher Beginner (12 weeks)": {"file": "finisher/finisher_beginner.txt", "tier": "finisher", "weeks": 12},
    "6. Finisher Intermediate (12 weeks)": {"file": "finisher/finisher_intermediate.txt", "tier": "finisher", "weeks": 12},
    "7. Finisher Advanced (12 weeks)": {"file": "finisher/finisher_advanced.txt", "tier": "finisher", "weeks": 12},
    "8. Finisher Masters (12 weeks)": {"file": "finisher/finisher_intermediate_masters.txt", "tier": "finisher", "weeks": 12},
    "9. Finisher Save My Race (6 weeks)": {"file": "finisher/finisher_save_my_race.txt", "tier": "finisher", "weeks": 6},
    "10. Compete Intermediate (12 weeks)": {"file": "compete/compete_intermediate.txt", "tier": "compete", "weeks": 12},
    "11. Compete Advanced (12 weeks)": {"file": "compete/compete_advanced.txt", "tier": "compete", "weeks": 12},
    "12. Compete Masters (12 weeks)": {"file": "compete/compete_intermediate_masters.txt", "tier": "compete", "weeks": 12},
    "13. Compete Save My Race (6 weeks)": {"file": "compete/compete_save_my_race.txt", "tier": "compete", "weeks": 6},
    "14. Podium Advanced (12 weeks)": {"file": "podium/podium_advanced.txt", "tier": "podium", "weeks": 12},
    "15. Podium Advanced GOAT (12 weeks)": {"file": "podium/podium_elite.txt", "tier": "podium", "weeks": 12},
}

base_path = Path("races/Unbound Gravel 200")
desc_path = Path("marketplace_descriptions/unbound_200")

for plan_name, mapping in plan_mapping.items():
    plan_folder = base_path / plan_name
    dest_file = plan_folder / "marketplace_description.html"
    source_file = desc_path / mapping["file"]
    
    if source_file.exists():
        # Read markdown
        markdown = source_file.read_text()
        
        # Extract content
        content = extract_content_from_markdown(markdown)
        
        # Write clean prose format
        prose_desc = write_clean_prose_description(content, mapping["tier"], mapping["weeks"])
        
        # Write
        dest_file.write_text(prose_desc)
        
        char_count = len(prose_desc)
        status = "✓" if char_count <= 4000 else "⚠️"
        print(f"{status} {plan_name}: {char_count} chars")

