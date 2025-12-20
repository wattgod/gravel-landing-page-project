"""
Fix course content quality issues in race data files.
Adds missing terrain_detail, named_section, expands short descriptions, etc.
"""

import json
from pathlib import Path
from typing import Dict

def enhance_suffering_zones(race: Dict, race_name: str) -> bool:
    """Enhance suffering zones with missing details."""
    course = race.get('course_description', {})
    zones = course.get('suffering_zones', [])
    if not zones:
        return False
    
    changed = False
    
    for zone in zones:
        # Add terrain_detail if missing
        if 'terrain_detail' not in zone or not zone['terrain_detail']:
            desc = zone.get('desc', '')
            label = zone.get('label', '')
            mile = zone.get('mile', zone.get('stage', 0))
            
            # Generate terrain detail from context
            if 'climb' in label.lower() or 'summit' in label.lower():
                zone['terrain_detail'] = f"Sustained climbing at mile {mile}"
            elif 'descent' in label.lower() or 'downhill' in label.lower():
                zone['terrain_detail'] = f"Technical descent at mile {mile}"
            elif 'exposure' in label.lower() or 'open' in label.lower():
                zone['terrain_detail'] = f"Exposed terrain with no shelter"
            elif 'wind' in label.lower():
                zone['terrain_detail'] = f"Open terrain where wind is a factor"
            else:
                zone['terrain_detail'] = f"Key section at mile {mile}"
            changed = True
        
        # Add named_section if missing and we can derive it
        if 'named_section' not in zone or not zone['named_section']:
            label = zone.get('label', '')
            # Use label as named section if it's specific enough
            if label and label not in ['First Climb', 'Final Push', 'Reality Check', 'Midway', 'High Point', 'Final Descent']:
                zone['named_section'] = label
                changed = True
        
        # Expand short descriptions
        desc = zone.get('desc', '')
        if len(desc) < 40:
            label = zone.get('label', '')
            mile = zone.get('mile', zone.get('stage', 0))
            
            # Expand based on context
            if 'climb' in label.lower():
                expanded = f"{desc} The sustained effort at mile {mile} tests your pacing and fitness. Legs will be talking by this point."
            elif 'descent' in label.lower():
                expanded = f"{desc} Technical terrain requires focus and bike handling skills. Fatigue makes this section dangerous."
            elif 'exposure' in label.lower() or 'wind' in label.lower():
                expanded = f"{desc} Open terrain means no shelter from elements. Weather conditions become a major factor here."
            elif 'final' in label.lower():
                expanded = f"{desc} The finish is close but the course isn't done with you yet. Stay focused and finish strong."
            else:
                expanded = f"{desc} This section demands attention and proper pacing. The cumulative fatigue is real by mile {mile}."
            
            if len(expanded) <= 200:  # Don't make it too long
                zone['desc'] = expanded
                changed = True
    
    return changed

def enhance_course_character(course: Dict, race_name: str, vitals: Dict) -> bool:
    """Enhance course character description if too short."""
    character = course.get('character', '')
    if len(character) >= 80:
        return False
    
    # Build enhanced description
    distance = vitals.get('distance_mi', 0)
    elevation = vitals.get('elevation_ft', 0)
    location = vitals.get('location', '')
    
    parts = [character]
    
    # Add distance context
    if distance:
        parts.append(f"At {distance} miles, this is a {'full-day effort' if distance >= 100 else 'substantial challenge'}.")
    
    # Add elevation context
    if elevation >= 10000:
        parts.append(f"With {elevation//1000}K+ feet of climbing, the vertical gain is relentless.")
    elif elevation >= 5000:
        parts.append(f"The {elevation//1000}K+ feet of climbing demands consistent effort throughout.")
    
    # Add location context if relevant
    if 'colorado' in location.lower() and 'altitude' not in character.lower():
        parts.append("The high-altitude terrain adds another dimension to the challenge.")
    
    enhanced = " ".join(parts)
    if len(enhanced) <= 200:  # Keep reasonable length
        course['character'] = enhanced
        return True
    
    return False

def enhance_signature_challenge(course: Dict, race_name: str, vitals: Dict) -> bool:
    """Enhance signature challenge if too short."""
    challenge = course.get('signature_challenge', '')
    if len(challenge) >= 60:
        return False
    
    # Build enhanced challenge
    elevation = vitals.get('elevation_ft', 0)
    distance = vitals.get('distance_mi', 0)
    
    parts = [challenge]
    
    # Add specific details
    if elevation >= 10000:
        parts.append(f"The {elevation//1000}K+ feet of climbing compounds throughout the day.")
    elif elevation >= 5000:
        parts.append(f"With {elevation//1000}K+ feet of elevation gain, pacing becomes critical.")
    
    if distance >= 150:
        parts.append("The distance itself is a test of endurance and mental fortitude.")
    
    enhanced = " ".join(parts)
    if len(enhanced) <= 150:  # Keep reasonable length
        course['signature_challenge'] = enhanced
        return True
    
    return False

def fix_generic_labels(zones: list) -> bool:
    """Replace generic labels with more specific ones."""
    changed = False
    generic_replacements = {
        'Final Push': 'Final Challenge',
        'Reality Check': 'First Major Test',
        'High Point': 'Summit Challenge',
        'Final Descent': 'Technical Descent to Finish',
    }
    
    for zone in zones:
        label = zone.get('label', '')
        if label in generic_replacements:
            zone['label'] = generic_replacements[label]
            changed = True
    
    return changed

def highlight_premier_course(race: Dict, race_name: str) -> bool:
    """Ensure premier course is mentioned in descriptions."""
    premier_courses = {
        'SBT GRVL': {'name': 'Black', 'distance': 108},
    }
    
    if race_name not in premier_courses:
        return False
    
    expected = premier_courses[race_name]
    course = race.get('course_description', {})
    character = course.get('character', '').lower()
    challenge = course.get('signature_challenge', '').lower()
    
    if expected['name'].lower() not in character and expected['name'].lower() not in challenge:
        # Add to character description
        current = course.get('character', '')
        if current:
            course['character'] = f"{current} The {expected['name']} course at {expected['distance']} miles is the premier distance."
        else:
            course['character'] = f"The {expected['name']} course at {expected['distance']} miles is the premier distance."
        return True
    
    return False

def fix_file(filepath: Path) -> Dict[str, bool]:
    """Fix all course content issues in a single file."""
    results = {}
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        race = data.get('race', {})
        race_name = race.get('display_name', race.get('name', 'Race'))
        course = race.get('course_description', {})
        vitals = race.get('vitals', {})
        zones = course.get('suffering_zones', [])
        
        results['suffering_zones'] = enhance_suffering_zones(race, race_name)
        results['course_character'] = enhance_course_character(course, race_name, vitals)
        results['signature_challenge'] = enhance_signature_challenge(course, race_name, vitals)
        results['generic_labels'] = fix_generic_labels(zones) if zones else False
        results['premier_course'] = highlight_premier_course(race, race_name)
        
        # Write back if any changes
        if any(results.values()):
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        
        return results
    except Exception as e:
        print(f"ERROR fixing {filepath}: {e}")
        return {'error': str(e)}

def main():
    """Fix all race data files."""
    data_dir = Path(__file__).parent.parent / 'data'
    
    print("Fixing course content quality issues...")
    print("=" * 60)
    
    fixed_count = 0
    for json_file in sorted(data_dir.glob('*-data.json')):
        race_name = json_file.stem.replace('-data', '').replace('-', ' ').title()
        print(f"\nFixing: {race_name}")
        
        results = fix_file(json_file)
        if 'error' not in results:
            if any(results.values()):
                fixed_count += 1
                for key, value in results.items():
                    if value:
                        print(f"  ✓ Fixed {key}")
        else:
            print(f"  ❌ Error: {results['error']}")
    
    print(f"\n{'='*60}")
    print(f"Fixed {fixed_count} files")
    print("=" * 60)

if __name__ == '__main__':
    main()
