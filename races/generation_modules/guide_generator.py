#!/usr/bin/env python3
"""
Training Guide Generator
Reads the HTML template and substitutes race-specific data.
"""

import argparse
import html
import json
import markdown
from pathlib import Path


def convert_markdown_to_html(text):
    """Convert markdown syntax to HTML"""
    if not text:
        return ""
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'nl2br', 'sane_lists'])
    return md.convert(str(text))


def load_race_data(race_json_path):
    """Load race data from JSON file"""
    with open(race_json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_template():
    """Load the HTML template"""
    # Get path relative to this script's location
    script_dir = Path(__file__).parent
    # Template is in the same directory as the generator
    template_path = script_dir / 'guide_template_full.html'
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_non_negotiables(race_data, index):
    """Extract non-negotiable data, handling both dict and string formats"""
    # Check multiple possible locations for non_negotiables
    non_negs = (race_data.get('non_negotiables', []) or
                race_data.get('race_metadata', {}).get('non_negotiables', []) or
                race_data.get('guide_variables', {}).get('non_negotiables', []))
    if index < len(non_negs):
        nn = non_negs[index]
        if isinstance(nn, dict):
            return {
                'requirement': nn.get('requirement', ''),
                'by_when': nn.get('by_when', ''),
                'why': nn.get('why', '')
            }
        else:
            # String format - use as requirement
            return {
                'requirement': str(nn),
                'by_when': '',
                'why': ''
            }
    # Defaults
    defaults = [
        {'requirement': 'Power meter or heart rate monitor', 'by_when': 'Week 1', 'why': 'Precise power data ensures correct training zones and optimal adaptation'},
        {'requirement': 'Heart rate monitor', 'by_when': 'Week 1', 'why': 'Heart rate provides backup data and helps gauge recovery status'},
        {'requirement': 'Professional bike fit', 'by_when': 'Week 2-3', 'why': 'Proper position prevents injury and maximizes power transfer'},
        {'requirement': 'Consistent training', 'by_when': 'Ongoing', 'why': 'Consistency is the foundation of adaptation - skip weeks, lose gains'},
        {'requirement': 'Follow the plan', 'by_when': 'Ongoing', 'why': 'The plan works if you work it - modifications undermine the system'}
    ]
    return defaults[index] if index < len(defaults) else {'requirement': '', 'by_when': '', 'why': ''}


def generate_guide(race_data, tier_name, ability_level, output_path):
    """
    Generate a training guide for a specific race, tier, and ability level.
    
    Args:
        race_data: Dict containing race information
        tier_name: str - "TIME CRUNCHED", "FINISHER", "COMPETE", or "PODIUM"
        ability_level: str - "Beginner", "Intermediate", or "Advanced"
        output_path: str - Where to save the generated HTML
    """
    
    # Load template
    template = load_template()
    
    # Extract race data from proper JSON structure
    metadata = race_data.get('race_metadata', {})
    characteristics = race_data.get('race_characteristics', {})
    hooks = race_data.get('race_hooks', {})
    guide_vars = race_data.get('guide_variables', {})
    
    # Get elevation gain (try multiple fields - note: JSON uses 'elevation_feet' in metadata for total gain)
    # Also check guide_variables which may have formatted string
    elevation_gain = 0
    elevation_gain_str = guide_vars.get('race_elevation', '')
    if elevation_gain_str:
        # Extract number from string like "11,000 feet"
        import re
        match = re.search(r'([\d,]+)', str(elevation_gain_str))
        if match:
            elevation_gain = int(match.group(1).replace(',', ''))
    
    # If not found in guide_vars, try metadata (elevation_feet is the total gain)
    if not elevation_gain:
        elevation_gain = (metadata.get('elevation_feet', 0) or
                          characteristics.get('elevation_gain_feet', 0) or 
                          metadata.get('elevation_gain_feet', 0) or
                          race_data.get('elevation_gain_feet', 0) or
                          race_data.get('elevation_feet', 0))
    
    try:
        elevation_gain = int(elevation_gain) if elevation_gain else 0
        elevation_str = f"{elevation_gain:,} feet of elevation gain" if elevation_gain else "XXX feet of elevation gain"
    except (ValueError, TypeError):
        elevation_str = "XXX feet of elevation gain"
    
    # Get distance
    distance = metadata.get('distance_miles', 0) or race_data.get('distance_miles', 0)
    try:
        distance = int(distance) if distance else 0
        distance_str = f"{distance} miles" if distance else 'XXX miles'
    except (ValueError, TypeError):
        distance_str = 'XXX miles'
    
    # Get terrain description
    terrain_desc = (guide_vars.get('race_terrain', '') or
                   guide_vars.get('terrain_description', '') or
                   characteristics.get('terrain_description', '') or
                   'varied terrain')
    
    # Calculate duration estimate if not provided (rough: 200 miles ≈ 10-15 hours for most)
    duration_estimate = guide_vars.get('duration_estimate', '')
    if not duration_estimate and distance:
        if distance >= 200:
            duration_estimate = '10-15 hours'
        elif distance >= 100:
            duration_estimate = '5-8 hours'
        elif distance >= 50:
            duration_estimate = '2-4 hours'
        else:
            duration_estimate = '1-2 hours'
    if not duration_estimate:
        duration_estimate = 'X-X hours'
    
    # Get weather strategy (expand if too short)
    weather_strategy = guide_vars.get('weather_strategy', '')
    if not weather_strategy or len(weather_strategy) < 100:
        # Build comprehensive weather strategy from race data
        typical_weather = characteristics.get('typical_weather', '')
        climate = characteristics.get('climate', '')
        race_date = metadata.get('date', '')
        
        weather_strategy = ""
        
        if typical_weather:
            weather_strategy += f"**Typical Conditions:** {typical_weather}. "
        elif climate:
            weather_strategy += f"**Typical Conditions:** Expect {climate} conditions. "
        
        if 'hot' in str(typical_weather).lower() or 'hot' in str(climate).lower():
            weather_strategy += "Heat management is critical. Start hydrated. Pre-cool if possible (cold water, ice). Wear light, breathable layers. Sun protection is mandatory (sunscreen, hat, sunglasses). Monitor forecast daily starting 5 days out. If extreme heat is forecast, adjust pacing strategy---start slower, fuel more aggressively. "
        elif 'cold' in str(typical_weather).lower() or 'cold' in str(climate).lower():
            weather_strategy += "Cold weather requires careful layering. Start warm, remove layers as you heat up. Protect extremities (toes, fingers, ears). Pack extra layers in case conditions worsen. Monitor forecast for precipitation. "
        else:
            weather_strategy += "Monitor forecast daily starting 5 days out. Pack layers for variable conditions. "
        
        weather_strategy += "Check forecast again 24 hours before race and adjust gear accordingly. "
        
        # Add wind considerations if applicable
        if 'kansas' in str(metadata.get('location', '')).lower() or 'wind' in str(typical_weather).lower():
            weather_strategy += "Wind can be a major factor---plan for crosswinds and headwinds. "
        
        if not weather_strategy:
            weather_strategy = "Check forecast week of race. Pack appropriate layers. Start hydrated if hot conditions expected. Monitor conditions daily starting 5 days out."
    
    # Build substitution dictionary
    substitutions = {
        '{{RACE_NAME}}': metadata.get('name', race_data.get('name', 'Race Name')),
        '{{DISTANCE}}': distance_str,
        '{{TERRAIN_DESCRIPTION}}': terrain_desc,
        '{{ELEVATION_GAIN}}': elevation_str,
        '{{DURATION_ESTIMATE}}': duration_estimate,
        '{{RACE_DESCRIPTION}}': convert_markdown_to_html(hooks.get('detail', metadata.get('description', 'Race description here'))),
        '{{ABILITY_LEVEL}}': ability_level,
        '{{TIER_NAME}}': tier_name,
        '{{WEEKLY_HOURS}}': get_weekly_hours(tier_name),
        '{{plan_weeks}}': '12',  # Default to 12 weeks, can be made dynamic
        '{{RACE_KEY_CHALLENGES}}': ', '.join(guide_vars.get('race_challenges', [])) if isinstance(guide_vars.get('race_challenges'), list) else guide_vars.get('race_challenges', 'technical terrain, elevation, and endurance'),
        '{{WEEKLY_STRUCTURE_DESCRIPTION}}': get_weekly_structure(tier_name),
        '{{RACE_INTRO_PARAGRAPH}}': generate_race_intro_paragraph(race_data),
        '{{COURSE_DESCRIPTION_PARAGRAPH}}': generate_course_description_paragraph(race_data),
        '{{RACE_SIGNIFICANCE_PARAGRAPH}}': generate_race_significance_paragraph(race_data),
        '{{WHAT_IT_TAKES_TO_FINISH}}': generate_what_it_takes_to_finish(race_data),
        '{{PLAN_PREPARATION_SUMMARY}}': generate_plan_preparation_summary(race_data),
        '{{PLAN_TITLE}}': get_plan_title(tier_name, ability_level),
        '{{ABILITY_LEVEL_EXPLANATION}}': get_ability_level_explanation(ability_level, tier_name),
        '{{TIER_VOLUME_EXPLANATION}}': get_tier_volume_explanation(tier_name),
        '{{PERFORMANCE_EXPECTATIONS}}': get_performance_expectations(tier_name),
        '{{RACE_ELEVATION}}': str(elevation_gain) if elevation_gain and isinstance(elevation_gain, (int, float)) else 'XXX',
        '{{RACE_SPECIFIC_SKILL_NOTES}}': convert_markdown_to_html(guide_vars.get('specific_skill_notes', 'Practice descending, cornering, and rough terrain handling.')),
        '{{RACE_SPECIFIC_TACTICS}}': convert_markdown_to_html(guide_vars.get('specific_tactics', 'Start conservatively. Fuel early and often. Be patient on climbs.')),
        '{{WEATHER_STRATEGY}}': convert_markdown_to_html(weather_strategy),
        '{{AID_STATION_STRATEGY}}': convert_markdown_to_html(guide_vars.get('aid_station_strategy', 'Use aid stations for quick refills. Don\'t linger.')),
        '{{ALTITUDE_POWER_LOSS}}': guide_vars.get('altitude_power_loss', '5-10% power loss expected above 8,000 feet'),
        '{{RECOMMENDED_TIRE_WIDTH}}': characteristics.get('recommended_tire_width', guide_vars.get('recommended_tire_width', '38-42mm')),
        '{{EQUIPMENT_CHECKLIST}}': generate_equipment_checklist(race_data),
        '{{RACE_SUPPORT_URL}}': metadata.get('website', race_data.get('website', 'https://example.com')),
        
        # Infographic placeholders (now all generated as HTML tables/diagrams)
        '{{INFOGRAPHIC_PHASE_BARS}}': '[Phase progression infographic]',  # Could be enhanced later
        '{{INFOGRAPHIC_RATING_HEX}}': generate_rating_hex(race_data),
        '{{INFOGRAPHIC_DIFFICULTY_TABLE}}': generate_difficulty_table(race_data),
        '{{INFOGRAPHIC_FUELING_TABLE}}': generate_fueling_table(race_data),
        '{{INFOGRAPHIC_MENTAL_MAP}}': generate_mental_map(race_data),
        '{{INFOGRAPHIC_THREE_ACTS}}': generate_three_acts(race_data),
        '{{INFOGRAPHIC_INDOOR_OUTDOOR_DECISION}}': generate_indoor_outdoor_decision(race_data),
        '{{INFOGRAPHIC_TIRE_DECISION}}': generate_tire_decision(race_data),
        '{{INFOGRAPHIC_KEY_WORKOUT_SUMMARY}}': generate_key_workout_summary(race_data),
        
        # Non-negotiables (extract from race_data)
        '{{NON_NEG_1_REQUIREMENT}}': convert_markdown_to_html(extract_non_negotiables(race_data, 0)['requirement']),
        '{{NON_NEG_1_BY_WHEN}}': extract_non_negotiables(race_data, 0)['by_when'],
        '{{NON_NEG_1_WHY}}': convert_markdown_to_html(extract_non_negotiables(race_data, 0)['why']),
        '{{NON_NEG_2_REQUIREMENT}}': convert_markdown_to_html(extract_non_negotiables(race_data, 1)['requirement']),
        '{{NON_NEG_2_BY_WHEN}}': extract_non_negotiables(race_data, 1)['by_when'],
        '{{NON_NEG_2_WHY}}': convert_markdown_to_html(extract_non_negotiables(race_data, 1)['why']),
        '{{NON_NEG_3_REQUIREMENT}}': convert_markdown_to_html(extract_non_negotiables(race_data, 2)['requirement']),
        '{{NON_NEG_3_BY_WHEN}}': extract_non_negotiables(race_data, 2)['by_when'],
        '{{NON_NEG_3_WHY}}': convert_markdown_to_html(extract_non_negotiables(race_data, 2)['why']),
        '{{NON_NEG_4_REQUIREMENT}}': convert_markdown_to_html(extract_non_negotiables(race_data, 3)['requirement']),
        '{{NON_NEG_4_BY_WHEN}}': extract_non_negotiables(race_data, 3)['by_when'],
        '{{NON_NEG_4_WHY}}': convert_markdown_to_html(extract_non_negotiables(race_data, 3)['why']),
        '{{NON_NEG_5_REQUIREMENT}}': convert_markdown_to_html(extract_non_negotiables(race_data, 4)['requirement']),
        '{{NON_NEG_5_BY_WHEN}}': extract_non_negotiables(race_data, 4)['by_when'],
        '{{NON_NEG_5_WHY}}': convert_markdown_to_html(extract_non_negotiables(race_data, 4)['why']),
        
        # Skill placeholder examples (would be race-specific)
        '{{SKILL_5_NAME}}': 'Emergency Repairs',
        '{{SKILL_5_WHY}}': convert_markdown_to_html('Mechanical issues will happen. Knowing how to fix them keeps you racing. A flat tire at mile 150 doesn\'t have to end your day---if you can fix it quickly. A dropped chain doesn\'t have to cost you 10 minutes---if you\'ve practiced the fix. The difference between finishing and DNF often comes down to mechanical competence. You can\'t control when mechanicals happen, but you can control how prepared you are to handle them.'),
        '{{SKILL_5_HOW}}': convert_markdown_to_html('Practice changing tubes under time pressure: set a timer, change a tube, aim to beat your previous time. Practice fixing dropped chains: intentionally drop your chain, then fix it quickly. Learn to use tire plugs: practice inserting plugs into a punctured tire. Know your quick-link: practice breaking and rejoining your chain. Test your multi-tool: make sure every tool works before race day. Practice in conditions similar to race day: cold hands, tired, stressed. Build a troubleshooting decision tree: flat = tube or plug? Chain break = quick-link. Derailleur hanger bent = straighten or replace? Spoke break = true wheel or ride carefully? The goal isn\'t perfection---it\'s competence under pressure.'),
        '{{SKILL_5_CUE}}': convert_markdown_to_html('Carry tools. Know your bike. Practice fixes. Mechanicals are when, not if.'),
    }
    
    # Perform all substitutions
    output = template
    for placeholder, value in substitutions.items():
        output = output.replace(placeholder, str(value))
    
    # Conditionally remove Masters section if not a Masters plan
    import re
    if ability_level != 'Masters':
        # Remove Masters section from TOC
        masters_toc_pattern = r'<!-- START MASTERS SECTION TOC -->.*?<!-- END MASTERS SECTION TOC -->'
        output = re.sub(masters_toc_pattern, '', output, flags=re.DOTALL)
        # Remove Masters section content
        masters_section_pattern = r'<!-- START MASTERS SECTION -->.*?<!-- END MASTERS SECTION -->'
        output = re.sub(masters_section_pattern, '', output, flags=re.DOTALL)
        # Renumber Women-Specific from section 14 to section 13
        output = output.replace('id="section-14-women-specific-considerations"', 'id="section-13-women-specific-considerations"')
        output = output.replace('14 · Women-Specific Considerations', '13 · Women-Specific Considerations')
        output = output.replace('href="#section-14-women-specific-considerations"', 'href="#section-13-women-specific-considerations"')
        # Renumber FAQ from section 15 to section 14
        output = output.replace('id="section-15-faq"', 'id="section-14-faq"')
        output = output.replace('15 · Frequently Asked Questions', '14 · Frequently Asked Questions')
        output = output.replace('href="#section-15-faq"', 'href="#section-14-faq"')
        print(f"  → Removed Masters section (not a Masters plan)")
        print(f"  → Renumbered Women-Specific to section 13, FAQ to section 14")
    else:
        print(f"  → Included Masters section (Masters plan)")
        print(f"  → Women-Specific is section 14, FAQ is section 15")
    
    # Wire in race-specific modules
    race_specific = race_data.get("race_specific") or {}
    output = output.replace("{{FLINT_MODULE}}", build_flint_module(race_specific))
    output = output.replace("{{TIRE_PRESSURE_MODULE}}", build_tire_pressure_module(race_specific))
    output = output.replace("{{WIND_MODULE}}", build_wind_module(race_specific))
    output = output.replace("{{TIME_DRIFT_MODULE}}", build_time_drift_module(race_specific))
    output = output.replace("{{DECISION_TREE_MODULE}}", build_decision_tree_module(race_specific))
    output = output.replace("{{PSYCH_LANDMARKS_MODULE}}", build_psych_landmarks_module(race_specific))
    
    # Validate no unreplaced placeholders remain
    import re
    unreplaced = re.findall(r'\{\{[A-Z_]+\}\}', output)
    if unreplaced:
        # Filter out known placeholders that are intentionally left (like INFOGRAPHIC placeholders that are handled)
        critical_unreplaced = [p for p in unreplaced if 'XXX' not in p and 'INFOGRAPHIC' not in p and 'PHASE' not in p]
        if critical_unreplaced:
            print(f"  Warning: Unreplaced placeholders found: {set(critical_unreplaced)}")
    
    # Conditionally remove altitude section if elevation < 5000 feet
    # Check multiple possible field names for elevation (avg_elevation_feet is the race location elevation)
    race_elevation = 0
    if isinstance(race_data, dict):
        race_elevation = (metadata.get('avg_elevation_feet', 0) or
                         characteristics.get('altitude_feet', 0) or
                         metadata.get('altitude_feet', 0) or
                         race_data.get('elevation_feet', 0) or
                         race_data.get('avg_elevation_feet', 0) or
                         race_data.get('altitude_feet', 0))
    
    try:
        race_elevation = int(race_elevation) if race_elevation else 0
    except (ValueError, TypeError):
        race_elevation = 0
    
    if race_elevation < 5000:
        # Remove altitude section (between START and END comments - match both instances)
        import re
        # Remove first altitude section marker (ONLY SHOW IF >= 3000)
        altitude_pattern1 = r'<!-- START ALTITUDE SECTION - ONLY SHOW IF RACE_ELEVATION >= 3000 -->.*?<!-- END ALTITUDE SECTION -->'
        output = re.sub(altitude_pattern1, '', output, flags=re.DOTALL)
        # Remove second altitude section (the detailed one - REMOVE IF < 5000)
        altitude_pattern2 = r'<!-- START ALTITUDE SECTION - REMOVE IF.*?<!-- END ALTITUDE SECTION -->'
        output = re.sub(altitude_pattern2, '', output, flags=re.DOTALL)
        print(f"  → Removed altitude section (race elevation: {race_elevation} feet < 5000)")
    else:
        # Remove only the "REMOVE IF < 5000" section, keep the main one
        import re
        altitude_pattern2 = r'<!-- START ALTITUDE SECTION - REMOVE IF.*?<!-- END ALTITUDE SECTION -->'
        output = re.sub(altitude_pattern2, '', output, flags=re.DOTALL)
        print(f"  → Included altitude section (race elevation: {race_elevation} feet >= 5000)")
    
    # Convert any remaining markdown syntax to HTML in the body
    import re
    body_start = output.find('<body>')
    body_end = output.find('</body>')
    
    if body_start != -1 and body_end != -1:
        body_content = output[body_start + 6:body_end]
        
        # Convert markdown to HTML (handles **bold**, *italic*, # headings, etc.)
        md = markdown.Markdown(extensions=['tables', 'fenced_code', 'nl2br'])
        html_body = md.convert(body_content)
        
        # Reconstruct output with converted HTML
        output = output[:body_start + 6] + html_body + output[body_end:]
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"✓ Generated: {output_path}")
    return output_path


def get_weekly_hours(tier_name):
    """Return weekly hours for each tier"""
    hours = {
        'TIME CRUNCHED': '0-5',
        'FINISHER': '8-10',
        'COMPETE': '12-17',
        'PODIUM': '18-25',
        # Legacy support
        'AYAHUASCA': '0-5',
    }
    return hours.get(tier_name, '12-17')


def get_weekly_structure(tier_name):
    """Return weekly structure description for each tier"""
    structures = {
        'TIME CRUNCHED': '3-4 sessions per week: 2 high-intensity intervals, 1-2 endurance rides',
        'FINISHER': '4-5 sessions per week: 1-2 intervals, 2-3 endurance rides, 1 long weekend ride',
        'COMPETE': '5-6 sessions per week: 2-3 intervals, 2-3 endurance rides, 1 long ride, 1 recovery',
        'PODIUM': '6-7 sessions per week: 3 intervals, 2-3 endurance rides, 1 long ride, 1-2 recovery',
        # Legacy support
        'AYAHUASCA': '3-4 sessions per week: 2 high-intensity intervals, 1-2 endurance rides',
    }
    return structures.get(tier_name, structures['FINISHER'])


def generate_equipment_checklist(race_data):
    """Generate race-specific equipment checklist with checkboxes"""
    items = [
        'Power meter (calibrated)',
        'Heart rate monitor',
        'GPS bike computer',
        f'Tires: {race_data.get("recommended_tire_width", "38-42mm")}',
        'Spare tubes/plugs',
        'Multi-tool',
        'Pump/CO2',
        'Nutrition for race duration',
        'Water bottles (2-3)',
        'Race number',
        'ID and emergency contact'
    ]
    
    # Add race-specific items
    if race_data.get('elevation_gain_feet', 0) > 5000:
        items.append('Gear range for climbing')
    
    if 'hot' in str(race_data.get('weather_strategy', '')).lower():
        items.append('Extra electrolytes')
        items.append('Sun protection')
    
    # Generate HTML with checkboxes
    checklist_html = '<div class="equipment-checklist-items">\n'
    for item in items:
        checklist_html += f'  <label class="checklist-item">\n'
        checklist_html += f'    <input type="checkbox">\n'
        checklist_html += f'    <span>{item}</span>\n'
        checklist_html += f'  </label>\n'
    checklist_html += '</div>\n'
    checklist_html += '<p class="checklist-download"><a href="#" onclick="downloadChecklistPDF()" class="download-link">📥 Download Printable Checklist (PDF)</a></p>'
    
    return checklist_html


def generate_fueling_table(race_data):
    """Generate fueling and hydration calculator table"""
    distance = race_data.get('distance_miles', 200)
    duration_hours = distance / 15  # Rough estimate: 15 mph average
    
    # Base scenarios
    scenarios = [
        {
            'scenario': 'Training Ride < 2 hours',
            'carbs': '30-45g/hour',
            'fluid': '500-750ml/hour',
            'notes': 'Water + electrolytes. Start fueling after 60 min if needed.'
        },
        {
            'scenario': 'Training Ride 2-4 hours',
            'carbs': '45-60g/hour',
            'fluid': '500-750ml/hour',
            'notes': 'Mix of gels, bars, and real food. Practice your race nutrition.'
        },
        {
            'scenario': 'Long Training Ride 4-6 hours',
            'carbs': '60-75g/hour',
            'fluid': '500-750ml/hour',
            'notes': 'Aggressive gut training. Test race-day nutrition strategy.'
        },
        {
            'scenario': f'Race Day ({distance} miles, ~{int(duration_hours)} hours)',
            'carbs': '60-90g/hour',
            'fluid': '500-750ml/hour',
            'notes': 'Start fueling in first 30 min. Mix multiple carb sources (glucose + fructose).'
        },
        {
            'scenario': 'Hot Conditions (>80°F)',
            'carbs': '60-90g/hour',
            'fluid': '750-1000ml/hour',
            'notes': 'Increase sodium to 500-700mg/hour. Pre-cool if possible.'
        },
        {
            'scenario': 'Cold Conditions (<50°F)',
            'carbs': '60-90g/hour',
            'fluid': '400-600ml/hour',
            'notes': 'Lower fluid needs, but still fuel aggressively. Warm fluids help.'
        }
    ]
    
    # Build HTML table
    html = '<table class="fueling-table">\n'
    html += '  <thead>\n'
    html += '    <tr>\n'
    html += '      <th>Scenario</th>\n'
    html += '      <th>Carbohydrate Intake</th>\n'
    html += '      <th>Fluid Intake</th>\n'
    html += '      <th>Notes</th>\n'
    html += '    </tr>\n'
    html += '  </thead>\n'
    html += '  <tbody>\n'
    
    for scenario in scenarios:
        html += '    <tr>\n'
        html += f'      <td><strong>{scenario["scenario"]}</strong></td>\n'
        html += f'      <td>{scenario["carbs"]}</td>\n'
        html += f'      <td>{scenario["fluid"]}</td>\n'
        html += f'      <td>{scenario["notes"]}</td>\n'
        html += '    </tr>\n'
    
    html += '  </tbody>\n'
    html += '</table>'
    
    return html


def generate_difficulty_table(race_data):
    """Generate difficulty rating table"""
    metadata = race_data.get('race_metadata', {})
    characteristics = race_data.get('race_characteristics', {})
    guide_vars = race_data.get('guide_variables', {})
    
    # Extract distance (same logic as main generator)
    distance = metadata.get('distance_miles', 0) or race_data.get('distance_miles', 0)
    try:
        distance = int(distance) if distance else 0
        distance_str = f"{distance} miles" if distance else 'N/A miles'
    except (ValueError, TypeError):
        distance_str = 'N/A miles'
    
    # Extract elevation gain (same logic as main generator)
    elevation_gain = 0
    elevation_gain_str = guide_vars.get('race_elevation', '')
    if elevation_gain_str:
        import re
        match = re.search(r'([\d,]+)', str(elevation_gain_str))
        if match:
            elevation_gain = int(match.group(1).replace(',', ''))
    
    if not elevation_gain:
        elevation_gain = (metadata.get('elevation_feet', 0) or
                         characteristics.get('elevation_gain_feet', 0) or
                         race_data.get('elevation_gain_feet', 0) or 0)
    
    try:
        elevation_gain = int(elevation_gain) if elevation_gain else 0
        elevation_str = f"{elevation_gain:,} feet" if elevation_gain else 'N/A feet'
    except (ValueError, TypeError):
        elevation_str = 'N/A feet'
    
    # Get technical difficulty
    technical = characteristics.get('technical_difficulty', 'Moderate')
    if technical:
        technical = technical.title()
    else:
        technical = 'Moderate'
    
    return f'''
    <table class="difficulty-table">
        <thead>
            <tr>
                <th>Category</th>
                <th>Rating</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Distance</strong></td>
                <td>{distance_str}</td>
            </tr>
            <tr>
                <td><strong>Elevation Gain</strong></td>
                <td>{elevation_str}</td>
            </tr>
            <tr>
                <td><strong>Technical Difficulty</strong></td>
                <td>{technical}</td>
            </tr>
            <tr>
                <td><strong>Time Cutoff</strong></td>
                <td>{race_data.get('time_cutoff', 'None')}</td>
            </tr>
        </tbody>
    </table>
    '''


def generate_rating_hex(race_data):
    """Generate race difficulty rating hex (radar chart as HTML table)"""
    # Calculate ratings (1-5 scale) based on race characteristics
    distance = race_data.get('distance_miles', 200)
    elevation = race_data.get('elevation_gain_feet', 0)
    terrain = race_data.get('terrain', 'rolling')
    altitude = race_data.get('altitude_feet', 0)
    
    # Distance rating (1-5)
    if distance >= 200:
        dist_rating = 5
    elif distance >= 150:
        dist_rating = 4
    elif distance >= 100:
        dist_rating = 3
    elif distance >= 50:
        dist_rating = 2
    else:
        dist_rating = 1
    
    # Elevation rating
    if elevation >= 15000:
        elev_rating = 5
    elif elevation >= 10000:
        elev_rating = 4
    elif elevation >= 5000:
        elev_rating = 3
    elif elevation >= 2000:
        elev_rating = 2
    else:
        elev_rating = 1
    
    # Technicality rating
    tech_map = {
        'mountain': 5,
        'flint_hills': 4,
        'rolling': 3,
        'flat': 2
    }
    tech_rating = tech_map.get(terrain, 3)
    
    # Climate rating (default moderate)
    climate_rating = 3
    
    # Altitude rating
    if altitude >= 8000:
        alt_rating = 5
    elif altitude >= 5000:
        alt_rating = 4
    elif altitude >= 3000:
        alt_rating = 3
    elif altitude >= 1000:
        alt_rating = 2
    else:
        alt_rating = 1
    
    # Adventure rating (combination of factors)
    adventure_rating = min(5, max(1, (dist_rating + elev_rating + tech_rating) // 3))
    
    html = '<div class="rating-hex">\n'
    html += '  <table class="rating-table">\n'
    html += '    <thead>\n'
    html += '      <tr>\n'
    html += '        <th>Dimension</th>\n'
    html += '        <th>Rating (1-5)</th>\n'
    html += '        <th>Visual</th>\n'
    html += '      </tr>\n'
    html += '    </thead>\n'
    html += '    <tbody>\n'
    
    ratings = [
        ('Elevation', elev_rating),
        ('Length', dist_rating),
        ('Technicality', tech_rating),
        ('Climate', climate_rating),
        ('Altitude', alt_rating),
        ('Adventure', adventure_rating)
    ]
    
    for name, rating in ratings:
        bars = '█' * rating + '░' * (5 - rating)
        html += f'      <tr>\n'
        html += f'        <td><strong>{name}</strong></td>\n'
        html += f'        <td>{rating}/5</td>\n'
        html += f'        <td class="rating-bars">{bars}</td>\n'
        html += f'      </tr>\n'
    
    html += '    </tbody>\n'
    html += '  </table>\n'
    html += '</div>'
    
    return html


def generate_indoor_outdoor_decision(race_data):
    """Generate indoor vs outdoor decision tree/table"""
    html = '<table class="decision-table">\n'
    html += '  <thead>\n'
    html += '    <tr>\n'
    html += '      <th>Condition</th>\n'
    html += '      <th>Ride Indoors</th>\n'
    html += '      <th>Ride Outdoors</th>\n'
    html += '    </tr>\n'
    html += '  </thead>\n'
    html += '  <tbody>\n'
    
    decisions = [
        {
            'condition': 'Temperature < 20°F or > 100°F',
            'indoors': 'Yes - Safety risk',
            'outdoors': 'No - Dangerous conditions'
        },
        {
            'condition': 'Ice, snow, or dangerous road conditions',
            'indoors': 'Yes - Crash risk too high',
            'outdoors': 'No - Unsafe'
        },
        {
            'condition': 'Structured intervals (VO2max, Threshold)',
            'indoors': 'Yes - Better control, no traffic',
            'outdoors': 'Maybe - If safe route available'
        },
        {
            'condition': 'Endurance ride (Z1-Z2)',
            'indoors': 'Avoid - Too boring',
            'outdoors': 'Yes - Mental training, skills practice'
        },
        {
            'condition': 'Time-crunched (< 60 min)',
            'indoors': 'Yes - No travel time, immediate start',
            'outdoors': 'No - Travel time wastes workout'
        },
        {
            'condition': 'Long ride (4+ hours)',
            'indoors': 'No - Mental torture',
            'outdoors': 'Yes - Essential for race prep'
        },
        {
            'condition': 'Recovery ride',
            'indoors': 'Maybe - If weather is terrible',
            'outdoors': 'Yes - Fresh air aids recovery'
        }
    ]
    
    for item in decisions:
        html += '    <tr>\n'
        html += f'      <td><strong>{item["condition"]}</strong></td>\n'
        html += f'      <td>{item["indoors"]}</td>\n'
        html += f'      <td>{item["outdoors"]}</td>\n'
        html += '    </tr>\n'
    
    html += '  </tbody>\n'
    html += '</table>'
    
    return html


def generate_mental_map(race_data):
    """Generate mental framework diagram as structured content"""
    html = '<div class="mental-map">\n'
    html += '  <div class="mental-framework">\n'
    html += '    <h3>Mental Training Framework</h3>\n'
    html += '    <div class="mental-layers">\n'
    html += '      <div class="mental-layer">\n'
    html += '        <h4>1. Foundation: Breathing & Presence</h4>\n'
    html += '        <p><strong>6-2-7 Technique:</strong> Inhale 6 counts, hold 2, exhale 7. Calms nervous system, brings focus to present moment.</p>\n'
    html += '      </div>\n'
    html += '      <div class="mental-layer">\n'
    html += '        <h4>2. Reframing: Change Your Story</h4>\n'
    html += '        <p><strong>Instead of:</strong> <q>This hurts</q> → <strong>Say:</strong> <q>This is my body adapting. I\'m getting stronger.</q></p>\n'
    html += '        <p><strong>Instead of:</strong> <q>I can\'t do this</q> → <strong>Say:</strong> <q>I\'m doing it right now. One pedal stroke at a time.</q></p>\n'
    html += '      </div>\n'
    html += '      <div class="mental-layer">\n'
    html += '        <h4>3. Anchoring: Physical Cues</h4>\n'
    html += '        <p><strong>Power position:</strong> Hands in drops, core engaged, smooth pedal stroke. This is your <q>race mode</q> trigger.</p>\n'
    html += '        <p><strong>Breathing rhythm:</strong> Match cadence to breath (e.g., 2 pedal strokes per breath). Creates flow state.</p>\n'
    html += '      </div>\n'
    html += '      <div class="mental-layer">\n'
    html += '        <h4>4. Acceptance: The Suffering Contract</h4>\n'
    html += '        <p><strong>You signed up for this.</strong> Discomfort is part of the deal. Accept it. Don\'t fight it. Work with it.</p>\n'
    html += '        <p><strong>Pain is temporary. Quitting lasts forever.</strong></p>\n'
    html += '      </div>\n'
    html += '      <div class="mental-layer">\n'
    html += '        <h4>5. Purpose: Remember Your Why</h4>\n'
    html += '        <p><strong>Why are you here?</strong> Connect to your deeper motivation. This race matters because you chose it.</p>\n'
    html += '      </div>\n'
    html += '    </div>\n'
    html += '  </div>\n'
    html += '</div>'
    
    return html


def generate_three_acts(race_data):
    """Generate three-act race structure table"""
    distance = race_data.get('distance_miles', 200)
    duration_hours = distance / 15
    
    html = '<table class="three-acts-table">\n'
    html += '  <thead>\n'
    html += '    <tr>\n'
    html += '      <th>Phase</th>\n'
    html += '      <th>When</th>\n'
    html += '      <th>What\'s Happening</th>\n'
    html += '      <th>Your Job</th>\n'
    html += '    </tr>\n'
    html += '  </thead>\n'
    html += '  <tbody>\n'
    
    acts = [
        {
            'phase': 'Act 1: The Start',
            'when': f'0 - {int(duration_hours * 0.2)} hours',
            'happening': 'High energy, adrenaline, everyone goes too hard. Groups form. Positioning matters.',
            'job': 'Stay calm. Don\'t chase. Fuel early (first 30 min). Find your rhythm. Let the race come to you.'
        },
        {
            'phase': 'Act 2: The Grind',
            'when': f'{int(duration_hours * 0.2)} - {int(duration_hours * 0.8)} hours',
            'happening': 'The real race. Fatigue sets in. Groups break up. Mental game begins. This is where races are won or lost.',
            'job': 'Stay consistent. Fuel every 20-30 min. Manage effort (don\'t redline). Use mental techniques. One section at a time.'
        },
        {
            'phase': 'Act 3: The Finish',
            'when': f'{int(duration_hours * 0.8)} hours - Finish',
            'happening': 'Everything hurts. Decision fatigue. Final push. This is where training pays off.',
            'job': 'Empty the tank. Use everything you\'ve got. Remember your why. Push through the pain. Finish strong.'
        }
    ]
    
    for act in acts:
        html += '    <tr>\n'
        html += f'      <td><strong>{act["phase"]}</strong></td>\n'
        html += f'      <td>{act["when"]}</td>\n'
        html += f'      <td>{act["happening"]}</td>\n'
        html += f'      <td>{act["job"]}</td>\n'
        html += '    </tr>\n'
    
    html += '  </tbody>\n'
    html += '</table>'
    
    return html


def generate_tire_decision(race_data):
    """Generate tire selection decision tree/table"""
    terrain = race_data.get('terrain', 'rolling')
    distance = race_data.get('distance_miles', 200)
    
    html = '<div class="tire-decision">\n'
    html += '  <table class="tire-table">\n'
    html += '    <thead>\n'
    html += '      <tr>\n'
    html += '        <th>Condition</th>\n'
    html += '        <th>Tire Width</th>\n'
    html += '        <th>Tread</th>\n'
    html += '        <th>Pressure</th>\n'
    html += '        <th>Why</th>\n'
    html += '      </tr>\n'
    html += '    </thead>\n'
    html += '    <tbody>\n'
    
    tire_scenarios = [
        {
            'condition': 'Smooth gravel, dry',
            'width': '38-40mm',
            'tread': 'Semi-slick or light file tread',
            'pressure': '35-40 PSI',
            'why': 'Low rolling resistance. Speed matters more than grip.'
        },
        {
            'condition': 'Rough/loose gravel',
            'width': '40-42mm',
            'tread': 'Moderate knobs (2-3mm)',
            'pressure': '30-35 PSI',
            'why': 'Need grip and comfort. Wider = lower pressure = better traction.'
        },
        {
            'condition': 'Mud or wet conditions',
            'width': '42-45mm',
            'tread': 'Aggressive knobs (4-5mm)',
            'pressure': '28-32 PSI',
            'why': 'Maximum grip. Lower pressure helps mud clear from tread.'
        },
        {
            'condition': 'Mixed terrain (your race)',
            'width': '40-42mm',
            'tread': 'Moderate knobs (2-3mm)',
            'pressure': '32-36 PSI',
            'why': 'Versatile. Handles most conditions. Good balance of speed and grip.'
        },
        {
            'condition': 'Long distance (6+ hours)',
            'width': '40-42mm',
            'tread': 'Moderate knobs',
            'pressure': '32-35 PSI',
            'why': 'Comfort matters. Lower pressure reduces fatigue. Still fast enough.'
        }
    ]
    
    for scenario in tire_scenarios:
        html += '      <tr>\n'
        html += f'        <td><strong>{scenario["condition"]}</strong></td>\n'
        html += f'        <td>{scenario["width"]}</td>\n'
        html += f'        <td>{scenario["tread"]}</td>\n'
        html += f'        <td>{scenario["pressure"]}</td>\n'
        html += f'        <td>{scenario["why"]}</td>\n'
        html += '      </tr>\n'
    
    html += '    </tbody>\n'
    html += '  </table>\n'
    html += '  <p class="tire-note"><strong>Rule of thumb:</strong> When in doubt, go wider and lower pressure. Comfort and grip beat marginal speed gains on rough terrain.</p>\n'
    html += '</div>'
    
    return html


def generate_key_workout_summary(race_data):
    """Generate key workout types overview table"""
    html = '<table class="workout-summary-table">\n'
    html += '  <thead>\n'
    html += '    <tr>\n'
    html += '      <th>Workout Type</th>\n'
    html += '      <th>Zone</th>\n'
    html += '      <th>Duration</th>\n'
    html += '      <th>Purpose</th>\n'
    html += '      <th>Key Focus</th>\n'
    html += '    </tr>\n'
    html += '  </thead>\n'
    html += '  <tbody>\n'
    
    workouts = [
        {
            'type': 'Endurance',
            'zone': 'Z1-Z2',
            'duration': '2-6 hours',
            'purpose': 'Aerobic base, fat adaptation',
            'focus': 'Easy pace. Conversational. Builds durability.'
        },
        {
            'type': 'G-Spot Intervals',
            'zone': '87-92% FTP',
            'duration': '15-60 min blocks',
            'purpose': 'Race-specific power',
            'focus': 'Sustained gravel race pace. Practice position.'
        },
        {
            'type': 'Threshold',
            'zone': 'Z4 (93-105% FTP)',
            'duration': '10-30 min blocks',
            'purpose': 'Lactate clearance, sustained power',
            'focus': 'Hard but controlled. Can say a few words.'
        },
        {
            'type': 'VO2max',
            'zone': 'Z5 (106-120% FTP)',
            'duration': '2-8 min intervals',
            'purpose': 'Max aerobic capacity',
            'focus': 'Very hard. Near max. Single words only.'
        },
        {
            'type': 'Anaerobic',
            'zone': 'Z6 (121-150% FTP)',
            'duration': '30 sec - 3 min',
            'purpose': 'Power, lactate tolerance',
            'focus': 'All-out efforts. Sharp, explosive.'
        },
        {
            'type': 'Neuromuscular',
            'zone': 'Z7 (>150% FTP)',
            'duration': '5-15 seconds',
            'purpose': 'Max power, sprint',
            'focus': 'Pure explosive. All-out sprints.'
        },
        {
            'type': 'Tempo',
            'zone': 'Z3 (76-90% FTP)',
            'duration': '20-60 min',
            'purpose': 'Moderate intensity (limited use)',
            'focus': 'Comfortably hard. Used sparingly in polarized plans.'
        }
    ]
    
    for workout in workouts:
        html += '    <tr>\n'
        html += f'      <td><strong>{workout["type"]}</strong></td>\n'
        html += f'      <td>{workout["zone"]}</td>\n'
        html += f'      <td>{workout["duration"]}</td>\n'
        html += f'      <td>{workout["purpose"]}</td>\n'
        html += f'      <td>{workout["focus"]}</td>\n'
        html += '    </tr>\n'
    
    html += '  </tbody>\n'
    html += '</table>'
    
    return html


def _html_escape(value):
    """Simple HTML escape that tolerates None."""
    if value is None:
        return ""
    return html.escape(str(value))


def build_flint_module(race_specific):
    surface = race_specific.get("surface") or {}
    terrain_type = surface.get("terrain_type")
    description = surface.get("description")
    hazard_sectors = surface.get("hazard_sectors") or []

    # Only render if we actually have something meaningful
    if not (terrain_type and description and hazard_sectors):
        return ""

    rows = []
    for sector in hazard_sectors:
        name = _html_escape(sector.get("name"))
        mile_marker = _html_escape(sector.get("mile_marker"))
        risk_level = _html_escape(str(sector.get("risk_level", "")).replace("_", " ").title())
        tactics = convert_markdown_to_html(sector.get("tactics", ""))
        rows.append(
            f"<tr>"
            f"<td><strong>{name}</strong></td>"
            f"<td>{mile_marker}</td>"
            f"<td>{risk_level}</td>"
            f"<td>{tactics}</td>"
            f"</tr>"
        )

    rows_html = "\n".join(rows)

    return f"""
<div class="gg-alert">
  <h3>Flint Rock Hazard Protocol</h3>
  <p>{convert_markdown_to_html(description) if description else ''}</p>

  <table class="gg">
    <thead>
      <tr>
        <th>Sector</th>
        <th>Miles</th>
        <th>Risk Level</th>
        <th>Tactics</th>
      </tr>
    </thead>
    <tbody>
      {rows_html}
    </tbody>
  </table>

  <h4>Protection Strategy:</h4>
  <ul>
    <li><strong>Line choice:</strong> Avoid the crown where sharp rock concentrates.</li>
    <li><strong>Body position:</strong> Stay relaxed to reduce pinch-flat risk.</li>
    <li><strong>Speed:</strong> Maintain momentum over sharp sections instead of panic braking.</li>
    <li><strong>If wet:</strong> Mud + flint is the worst combo – consider dropping pressure slightly.</li>
  </ul>
</div>
""".strip()


def build_tire_pressure_module(race_specific):
    mechanicals = race_specific.get("mechanicals") or {}
    recommended_tires = mechanicals.get("recommended_tires") or []
    pressure_by_weight = mechanicals.get("pressure_by_weight") or {}

    if not (recommended_tires and pressure_by_weight):
        return ""

    # Build table rows
    rows = []
    for weight_class, pressures in pressure_by_weight.items():
        label = str(weight_class)
        label = label.replace("_", "-").replace("lbs", " lbs").replace("plus", "+")
        dry = _html_escape(pressures.get("dry"))
        mixed = _html_escape(pressures.get("mixed"))
        mud = _html_escape(pressures.get("mud"))
        rows.append(
            f"<tr>"
            f"<td><strong>{_html_escape(label)}</strong></td>"
            f"<td>{dry}</td>"
            f"<td>{mixed}</td>"
            f"<td>{mud}</td>"
            f"</tr>"
        )

    rows_html = "\n".join(rows)

    tires_html = "\n".join(f"<li>{_html_escape(t)}</li>" for t in recommended_tires)
    headline_tire = _html_escape(recommended_tires[0]) if recommended_tires else "this course"

    return f"""
<div class="gg-tactical">
  <h3>Tire Pressure Recommendations for {headline_tire}</h3>
  <table class="gg">
    <thead>
      <tr>
        <th>Rider Weight</th>
        <th>Dry Conditions</th>
        <th>Mixed Conditions</th>
        <th>Mud/Wet</th>
      </tr>
    </thead>
    <tbody>
      {rows_html}
    </tbody>
  </table>
  <p><strong>Recommended Tires:</strong></p>
  <ul>
    {tires_html}
  </ul>
  <p><strong>Note:</strong> These are starting points. Adjust based on tire casing, rim width, and your own feel. When in doubt, err slightly lower for comfort and grip, not vanity PSI.</p>
</div>
""".strip()


def build_wind_module(race_specific):
    wind = race_specific.get("wind_protocol") or {}
    prevailing_direction = wind.get("prevailing_direction")
    when_it_matters = wind.get("when_it_matters")
    group_tactics = wind.get("group_tactics")
    solo_tactics = wind.get("solo_tactics")

    if not (prevailing_direction or when_it_matters or group_tactics or solo_tactics):
        return ""

    return f"""
<div class="gg-tactical">
  <h3>Wind Protocol</h3>
  <p><strong>Prevailing Pattern:</strong> {_html_escape(prevailing_direction or '')}</p>

  <h4>When It Matters:</h4>
  <p>{convert_markdown_to_html(when_it_matters) if when_it_matters else ''}</p>

  <h4>Group Tactics:</h4>
  <p>{convert_markdown_to_html(group_tactics) if group_tactics else ''}</p>

  <h4>Solo Tactics:</h4>
  <p>{convert_markdown_to_html(solo_tactics) if solo_tactics else ''}</p>

  <div class="gg-blackpill">
    <span class="label">Reality Check</span>
    <p>The wind will be harder than you expect. Lower your power targets 5–10% into sustained headwinds and protect your head. Ego burns more matches than the course.</p>
  </div>
</div>
""".strip()


def build_time_drift_module(race_specific):
    environment = race_specific.get("environment") or {}
    time_drift = environment.get("time_drift") or {}

    neutral = time_drift.get("neutral")
    mild_mud = time_drift.get("mild_mud")
    heavy_mud = time_drift.get("heavy_mud")
    note = time_drift.get("note")

    if not (neutral or mild_mud or heavy_mud or note):
        return ""

    return f"""
<div class="gg-info">
  <h3>Expected Time Drift</h3>
  <p><strong>{convert_markdown_to_html(note) if note else ''}</strong></p>

  <table class="gg">
    <thead>
      <tr>
        <th>Conditions</th>
        <th>Time Addition</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Neutral (normal wind & conditions)</td>
        <td><strong>{_html_escape(neutral or "")}</strong></td>
      </tr>
      <tr>
        <td>Mild mud or heavy wind</td>
        <td><strong>{_html_escape(mild_mud or "")}</strong></td>
      </tr>
      <tr>
        <td>Heavy mud (peanut butter)</td>
        <td><strong>{_html_escape(heavy_mud or "")}</strong></td>
      </tr>
    </tbody>
  </table>

  <p><strong>Plan accordingly:</strong> Bring more food, fluids, and mental patience than your best-case scenario assumes. Most people underestimate how long they'll be out there.</p>
</div>
""".strip()


def build_decision_tree_module(race_specific):
    tree = race_specific.get("in_race_decision_tree") or {}

    # If there's nothing, return empty
    if not tree:
        return ""

    def _render_steps(label, key):
        steps = tree.get(key) or []
        if not steps:
            return ""
        items = "\n".join(f"<li>{convert_markdown_to_html(step)}</li>" for step in steps)
        return f"""
  <h4>{label}</h4>
  <ol>
    {items}
  </ol>
""".rstrip()

    sections = [
        _render_steps("Flat Tire", "flat_tire"),
        _render_steps("Dropped from Group", "dropped_from_group"),
        _render_steps("Bonking", "bonking"),
        _render_steps("Cramping", "cramping"),
    ]
    sections_html = "\n\n".join(s for s in sections if s)

    if not sections_html:
        return ""

    return f"""
<div class="gg-decision-tree">
  <h3>In-Race Decision Tree</h3>
  <p>When things go sideways (and at some point they will), follow protocol instead of panic.</p>
{sections_html}
</div>
""".strip()


def build_psych_landmarks_module(race_specific):
    psych = race_specific.get("psychological_landmarks") or {}
    if not psych:
        return ""

    dark = psych.get("dark_patch") or {}
    shatter = psych.get("where_field_shatters") or {}
    relief = psych.get("late_relief") or {}
    honeymoon = psych.get("the_honeymoon") or {}
    second_wind = psych.get("second_wind") or {}

    # If all are completely empty, bail
    if not (dark or shatter or relief or honeymoon or second_wind):
        return ""

    def _render_block(title, node):
        miles = _html_escape(node.get("miles"))
        desc = convert_markdown_to_html(node.get("description", ""))
        if not (miles or desc):
            return ""
        return f"""
  <h4>{title} (Miles {miles})</h4>
  <p>{desc}</p>
""".rstrip()

    blocks = [
        _render_block("The Honeymoon", honeymoon),
        _render_block("Where the Field Shatters", shatter),
        _render_block("The Dark Patch", dark),
        _render_block("Second Wind", second_wind),
        _render_block("Late-Race Relief", relief),
    ]
    blocks_html = "\n\n".join(b for b in blocks if b)

    if not blocks_html:
        return ""

    return f"""
<div class="gg-info">
  <h3>Mental Landmarks</h3>
  <p>Long races have predictable psychological phases. Knowing when they tend to show up makes them easier to handle.</p>
{blocks_html}
  <p><strong>Your job:</strong> Recognize these moments as part of the script, not proof that you're failing. Stay on task, solve the next problem, and let the course come back to you.</p>
</div>
""".strip()


def main():
    """CLI entry point for guide generator"""
    parser = argparse.ArgumentParser(description='Generate training plan guide HTML')
    parser.add_argument('--race', required=True, help='Path to race JSON file')
    parser.add_argument('--plan', required=True, help='Path to plan JSON file')
    parser.add_argument('--output-dir', required=True, help='Directory to save generated guide')
    
    args = parser.parse_args()
    
    # Load race and plan data
    race_data = load_race_data(args.race)
    plan_data = load_race_data(args.plan) if args.plan else None
    
    # Extract tier and level from plan data or filename
    tier_name = 'FINISHER'  # Default
    ability_level = 'Intermediate'  # Default
    
    # Try to extract from filename first (more reliable)
    plan_path = Path(args.plan)
    plan_name = plan_path.stem.lower()
    
    if 'ayahuasca' in plan_name or 'time crunched' in plan_name or 'time_crunched' in plan_name:
        tier_name = 'TIME CRUNCHED'  # Updated from AYAHUASCA
    elif 'finisher' in plan_name:
        tier_name = 'FINISHER'
    elif 'compete' in plan_name:
        tier_name = 'COMPETE'
    elif 'podium' in plan_name:
        tier_name = 'PODIUM'
    
    if 'beginner' in plan_name:
        ability_level = 'Beginner'
    elif 'intermediate' in plan_name:
        ability_level = 'Intermediate'
    elif 'advanced' in plan_name:
        ability_level = 'Advanced'
        # Note: GOAT removed - no longer used
    elif 'masters' in plan_name:
        ability_level = 'Masters'
    elif 'save_my_race' in plan_name:
        ability_level = 'Save My Race'
    
    # Override with plan_data if available
    if plan_data:
        if 'tier' in plan_data:
            tier_name = plan_data.get('tier', tier_name).upper()
        if 'level' in plan_data:
            ability_level = plan_data.get('level', ability_level).title()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    race_name_slug = race_data.get('race_metadata', {}).get('name', 'race').lower().replace(' ', '_')
    plan_slug = f"{tier_name.lower()}_{ability_level.lower().replace(' ', '_')}"
    output_filename = f"{race_name_slug}_{plan_slug}_guide.html"
    output_path = output_dir / output_filename
    
    # Generate guide
    generate_guide(
        race_data=race_data,
        tier_name=tier_name,
        ability_level=ability_level,
        output_path=str(output_path)
    )
    
    print(f"✓ Generated: {output_path}")


def generate_race_intro_paragraph(race_data):
    """Generate the introductory paragraph for Section 1"""
    metadata = race_data.get('race_metadata', {})
    race_name = metadata.get('name', 'Race Name')
    distance = metadata.get('distance_miles', 0) or race_data.get('distance_miles', 0)
    elevation_gain = metadata.get('elevation_feet', 0) or race_data.get('elevation_gain_feet', 0) or race_data.get('elevation_feet', 0)
    location = metadata.get('location', '')
    
    try:
        distance = int(distance) if distance else 0
        elevation_gain = int(elevation_gain) if elevation_gain else 0
    except (ValueError, TypeError):
        distance = 0
        elevation_gain = 0
    
    # Build intro based on race characteristics
    intro = f"Welcome to your <strong>{race_name}</strong> training plan."
    
    if distance:
        intro += f" {distance} miles"
    if elevation_gain:
        intro += f" with {elevation_gain:,} feet of climbing"
    if location:
        intro += f" through {location}"
    
    # Add race-specific hook
    hooks = race_data.get('race_hooks', {})
    hook_text = hooks.get('hook', '')
    if hook_text:
        intro += f". {hook_text}"
    else:
        intro += ". This isn't a race you survive by accident. It's a race you prepare for—or it prepares you for a very long day."
    
    return intro


def generate_course_description_paragraph(race_data):
    """Generate detailed course description from 7 variables"""
    metadata = race_data.get('race_metadata', {})
    characteristics = race_data.get('race_characteristics', {})
    guide_vars = race_data.get('guide_variables', {})
    
    distance = metadata.get('distance_miles', 0) or race_data.get('distance_miles', 0)
    elevation_gain = metadata.get('elevation_feet', 0) or race_data.get('elevation_gain_feet', 0) or race_data.get('elevation_feet', 0)
    terrain_desc = characteristics.get('terrain_description', '') or guide_vars.get('terrain_description', 'varied terrain')
    climate = characteristics.get('climate', '') or guide_vars.get('climate', '')
    starting_elevation = metadata.get('avg_elevation_feet', 0) or characteristics.get('altitude_feet', 0) or 0
    support_level = characteristics.get('support_level', 'well-supported')
    adventure_factor = characteristics.get('adventure_factor', 'moderate')
    
    try:
        distance = int(distance) if distance else 0
        elevation_gain = int(elevation_gain) if elevation_gain else 0
        starting_elevation = int(starting_elevation) if starting_elevation else 0
    except (ValueError, TypeError):
        distance = 0
        elevation_gain = 0
        starting_elevation = 0
    
    desc = f"The {metadata.get('name', 'Race')} covers"
    if distance:
        desc += f" {distance} miles"
    if elevation_gain:
        desc += f" with {elevation_gain:,} feet of cumulative elevation gain"
    if terrain_desc:
        desc += f" through {terrain_desc}"
    
    # Handling demands
    if 'flint' in terrain_desc.lower() or 'rock' in terrain_desc.lower():
        desc += "—this is a moderate handling challenge"
    else:
        desc += "—this is a moderate handling challenge"
    
    # Climate
    if climate:
        desc += f". Climate is the silent killer—{climate}"
    elif 'hot' in str(guide_vars.get('weather_strategy', '')).lower():
        desc += ". Climate is the silent killer—Hot and humid, 85-95°F"
    else:
        desc += ". Climate varies"
    
    # Altitude
    if starting_elevation >= 5000:
        desc += f". Starting elevation is around {starting_elevation:,} feet, so altitude is a factor"
    else:
        desc += f". Starting elevation is around {starting_elevation:,} feet, so altitude isn't a factor"
    
    # Support
    if support_level:
        if 'well' in support_level.lower():
            desc += ". The race is well-supported with aid stations"
        else:
            desc += f". The race is {support_level}"
    
    # Adventure
    if adventure_factor:
        desc += f". The adventure factor is {adventure_factor}"
    
    return desc


def generate_race_significance_paragraph(race_data):
    """Generate paragraph on why the race matters"""
    metadata = race_data.get('race_metadata', {})
    hooks = race_data.get('race_hooks', {})
    race_name = metadata.get('name', 'Race Name')
    
    # Build from hooks and metadata
    significance = f"{race_name} is"
    
    # Check for iconic status
    if 'iconic' in str(hooks.get('detail', '')).lower() or 'iconic' in str(metadata.get('description', '')).lower():
        significance += " the most iconic gravel race in the world"
    else:
        significance += " a significant gravel race"
    
    significance += f"—{race_name} is gravel cycling. "
    
    # Organization
    significance += "The organization is flawless, the course is legendary, and the event execution sets the industry standard. "
    
    # Energy and community
    significance += "The energy, the field, the community—this is what gravel racing aspires to be. "
    
    # Field depth
    significance += "Thousands of riders create incredible camaraderie, and the volunteers make it unforgettable. The field depth is unmatched—the pros, the weekend warriors, and everyone in between. "
    
    # Cost
    location = metadata.get('location', '')
    if location:
        significance += f"Entry fees are premium, but you get what you pay for. Travel and lodging in {location} aren't cheap, but manageable with planning."
    else:
        significance += "Entry fees are premium, but you get what you pay for."
    
    return significance


def generate_what_it_takes_to_finish(race_data):
    """Generate content for 'What It Takes to Finish'"""
    metadata = race_data.get('race_metadata', {})
    distance = metadata.get('distance_miles', 0) or race_data.get('distance_miles', 0)
    
    try:
        distance = int(distance) if distance else 0
    except (ValueError, TypeError):
        distance = 0
    
    # Estimate duration
    if distance >= 200:
        duration = "10-15 hours"
    elif distance >= 100:
        duration = "5-8 hours"
    elif distance >= 50:
        duration = "2-4 hours"
    else:
        duration = "1-2 hours"
    
    requirements = f"You'll be out there {duration}. "
    requirements += "Base fitness alone won't cut it—you need specific preparation for sustained output. "
    requirements += "Heat acclimatization isn't optional. "
    requirements += "Endurance pacing is critical—smooth power wins over surges. "
    requirements += "Bike handling confidence at speed, especially in groups. "
    requirements += "Equipment reliability—mechanical issues end races."
    
    return requirements


def generate_plan_preparation_summary(race_data):
    """Generate content for 'This Plan Prepares You for All of It'"""
    metadata = race_data.get('race_metadata', {})
    race_name = metadata.get('name', 'Race Name')
    characteristics = race_data.get('race_characteristics', {})
    terrain_desc = characteristics.get('terrain_description', '') or 'varied terrain'
    
    summary = f"Every workout, long ride, and recovery week is designed around {race_name}'s specific demands. "
    summary += "Heat adaptation protocols. "
    summary += "Endurance pacing for race distance. "
    summary += f"Technical handling for {terrain_desc}. "
    summary += "Mental training for when it all falls apart."
    
    return summary


def get_plan_title(tier_name, ability_level):
    """Return descriptive title for each plan combination"""
    titles = {
        ('TIME CRUNCHED', 'Beginner'): 'Time Crunched Plan',
        ('TIME CRUNCHED', 'Intermediate'): 'Time Crunched Plan',
        ('TIME CRUNCHED', 'Masters'): 'Time Crunched Plan',
        ('TIME CRUNCHED', 'Save My Race'): 'Time Crunched Plan',
        # Legacy support
        ('AYAHUASCA', 'Beginner'): 'Time Crunched Plan',
        ('AYAHUASCA', 'Intermediate'): 'Time Crunched Plan',
        ('AYAHUASCA', 'Masters'): 'Time Crunched Plan',
        ('AYAHUASCA', 'Save My Race'): 'Time Crunched Plan',
        ('FINISHER', 'Beginner'): 'First Timer Plan',
        ('FINISHER', 'Intermediate'): 'Solid Finisher Plan',
        ('FINISHER', 'Advanced'): 'Strong Finish Plan',
        ('COMPETE', 'Intermediate'): 'Competitive Plan',
        ('COMPETE', 'Advanced'): 'Podium Contender Plan',
        ('COMPETE', 'Masters'): '50+ Performance Plan',
        ('COMPETE', 'Save My Race'): 'Emergency Plan',
        ('PODIUM', 'Advanced'): 'Elite Preparation',
    }
    return titles.get((tier_name, ability_level), f'{ability_level} Plan')


def get_ability_level_explanation(ability_level, tier_name):
    """Provide detailed explanation for ability level"""
    weekly_hours = get_weekly_hours(tier_name)
    
    if ability_level == 'Beginner':
        return f'<strong>Your ability level (Beginner)</strong> reflects your training experience and current fitness—not one or the other, but both. You\'re a beginner if you\'ve never trained systematically for endurance sports, you\'re currently out of shape or returning after significant time off (2+ years), you don\'t know your FTP, and long rides for you are 1-2 hours. Beginner plans build base fitness first. They assume you need to develop aerobic capacity, muscular endurance, and durability before you can handle intensity.'
    elif ability_level == 'Intermediate':
        return f'<strong>Your ability level (Intermediate)</strong> reflects your training experience and current fitness—not one or the other, but both. You\'re intermediate if you\'ve got endurance sports background—cycling, running, triathlon, or other aerobic training, you\'re currently fit enough to ride 3-4 hours without falling apart, you understand pacing, you\'ve practiced fueling on long rides, and you know what "sustainable discomfort" feels like. Intermediate plans assume you can handle two quality sessions per week plus endurance volume. They use polarized training (80% easy, 20% hard) because your body can absorb that stress without breaking.'
    elif ability_level == 'Advanced':
        return f'<strong>Your ability level (Advanced)</strong> reflects your training experience and current fitness—not one or the other, but both. You\'re advanced if you\'re already fast, you\'ve raced seriously (road, gravel, MTB, triathlon—doesn\'t matter), you know your FTP, you understand interval structure, and you\'ve trained with power or heart rate zones for years. Advanced plans use block periodization—concentrated periods of specific intensity (threshold blocks, VO2 blocks) followed by recovery. They assume you know your body well enough to execute hard sessions without burying yourself.'
    elif ability_level == 'Masters':
        return f'<strong>Your ability level (Masters)</strong> reflects your training experience and current fitness—not one or the other, but both. You\'re 50+ (or 40+ with significant recovery needs) with intermediate experience. Masters plans use moderate volume, emphasize recovery, and integrate HRV monitoring for autoregulation. They acknowledge that recovery takes longer as you age.'
    else:
        return f'<strong>Your ability level ({ability_level})</strong> reflects your training experience and current fitness—not one or the other, but both.'


def get_tier_volume_explanation(tier_name):
    """Provide detailed explanation for volume category"""
    weekly_hours = get_weekly_hours(tier_name)
    
    if tier_name == 'TIME CRUNCHED' or tier_name == 'AYAHUASCA':
        return f'<strong>Your volume category (TIME CRUNCHED)</strong> is based on the hours you\'ll actually spend riding each week, week after week, for the full training block. Be honest. Don\'t count the time you wish you had—count the time you\'ll realistically ride. Life will interfere. Plan for 80% completion and you\'ll hit closer to 100%. At <strong>~{weekly_hours} hours per week</strong>, you\'re in the TIME CRUNCHED category. Time Crunched plans use high-intensity interval training (HIIT) to maximize fitness from minimal time. Two to three hard sessions per week, short endurance rides, and minimal long rides (capped at 2-3 hours). Critical caveat: These plans assume you already have fitness and experience. HIIT doesn\'t build base fitness—it sharpens existing fitness.'
    elif tier_name == 'FINISHER':
        return f'<strong>Your volume category (FINISHER)</strong> is based on the hours you\'ll actually spend riding each week, week after week, for the full training block. Be honest. Don\'t count the time you wish you had—count the time you\'ll realistically ride. Life will interfere. Plan for 80% completion and you\'ll hit closer to 100%. At <strong>~{weekly_hours} hours per week</strong>, you\'re in the FINISHER category. This is the sweet spot for most gravel racers. You\'ve got enough time to build a real aerobic base, practice race-specific intensity, and complete long rides that prepare you for race distance. Finisher plans include two quality sessions per week (threshold, tempo, climbing work), several endurance rides, and one long ride that builds to 4-5 hours by peak weeks.'
    elif tier_name == 'COMPETE':
        return f'<strong>Your volume category (COMPETE)</strong> is based on the hours you\'ll actually spend riding each week, week after week, for the full training block. Be honest. Don\'t count the time you wish you had—count the time you\'ll realistically ride. Life will interfere. Plan for 80% completion and you\'ll hit closer to 100%. At <strong>~{weekly_hours} hours per week</strong>, you\'re in the COMPETE category. You\'re training to race properly. Not just participate—compete. Compete plans include three to four quality sessions per week, multiple endurance rides, and long rides that hit 5-6 hours with race-specific intensity. You\'re building threshold power, repeatability (surge and recover repeatedly), and the ability to hold race pace for hours.'
    elif tier_name == 'PODIUM':
        return f'<strong>Your volume category (PODIUM)</strong> is based on the hours you\'ll actually spend riding each week, week after week, for the full training block. Be honest. Don\'t count the time you wish you had—count the time you\'ll realistically ride. Life will interfere. Plan for 80% completion and you\'ll hit closer to 100%. At <strong>~{weekly_hours} hours per week</strong>, you\'re in the PODIUM category. Professional-level commitment. At this volume, you need coaching, not a pre-made plan. You\'re managing recovery protocols, tracking performance metrics closely, and adjusting week-to-week based on how your body responds.'
    else:
        return f'<strong>Your volume category ({tier_name})</strong> is based on the hours you\'ll actually spend riding each week, week after week, for the full training block.'


def get_performance_expectations(tier_name):
    """Provide performance expectations based on tier"""
    weekly_hours = get_weekly_hours(tier_name)
    
    if tier_name == 'TIME CRUNCHED' or tier_name == 'AYAHUASCA':
        return f"With {weekly_hours} hours per week, you're building minimal viable fitness. This is survival mode training. Realistic expectations: You'll finish the race, but it will be hard. You won't be competitive, but you'll complete the distance. If you're a true beginner on a Time Crunched plan, adjust expectations further—you're showing up underprepared and should prioritize finishing over performance."
    elif tier_name == 'FINISHER':
        return f"With {weekly_hours} hours per week, you're building solid aerobic base fitness. Realistic expectations: You'll finish strong at most gravel races. You won't be competing for podiums at Tier 1 events, but you'll complete the distance at a moderate pace without heroics."
    elif tier_name == 'COMPETE':
        return f"With {weekly_hours} hours per week, you're building race fitness. Realistic expectations: This volume typically places riders in the top third of the field at most gravel races. You're training to compete, not just participate."
    elif tier_name == 'PODIUM':
        return f"With {weekly_hours} hours per week, you're training at professional-level volume. Realistic expectations: At this volume, you should be competing for top positions. However, if you're training 20+ hours per week, consider getting coaching rather than following a pre-made plan."
    else:
        return "Performance expectations vary based on your training consistency, natural ability, and race-day execution."


if __name__ == '__main__':
    main()
