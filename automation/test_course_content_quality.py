"""
Regression tests for course content quality in race data files.
Checks for issues like sparse suffering zones, missing details, etc.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

def load_race_data(filepath: str) -> Dict:
    """Load and parse a race data JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def test_suffering_zones_detail(data: Dict, race_name: str) -> List[Tuple[str, bool, str]]:
    """Test that suffering zones have sufficient detail."""
    results = []
    race = data.get('race', {})
    course = race.get('course_description', {})
    zones = course.get('suffering_zones', [])
    
    if not zones:
        results.append((f"{race_name}: Suffering zones exist", False, "No suffering zones defined"))
        return results
    
    results.append((f"{race_name}: Suffering zones exist", True, f"{len(zones)} zones defined"))
    
    # Check each zone has sufficient detail
    for i, zone in enumerate(zones):
        zone_num = i + 1
        desc = zone.get('desc', '')
        label = zone.get('label', '')
        
        # Description should be at least 40 characters
        desc_length_ok = len(desc) >= 40
        results.append((f"{race_name}: Zone {zone_num} description detailed", desc_length_ok,
                       f"Description too short ({len(desc)} chars, need 40+)" if not desc_length_ok else f"OK ({len(desc)} chars)"))
        
        # Should have terrain_detail or named_section for context
        has_terrain_detail = 'terrain_detail' in zone and zone['terrain_detail']
        has_named_section = 'named_section' in zone and zone['named_section']
        has_context = has_terrain_detail or has_named_section
        results.append((f"{race_name}: Zone {zone_num} has context", has_context,
                       "Missing terrain_detail or named_section" if not has_context else "OK"))
        
        # Label should be descriptive (not just "First Climb", "Final Push", etc.)
        generic_labels = ['First Climb', 'Final Push', 'Reality Check', 'Midway', 'High Point', 'Final Descent']
        is_generic = label in generic_labels
        results.append((f"{race_name}: Zone {zone_num} label specific", not is_generic,
                       f"Generic label: '{label}'" if is_generic else f"OK: '{label}'"))
    
    return results

def test_course_character_detail(data: Dict, race_name: str) -> List[Tuple[str, bool, str]]:
    """Test that course character description is detailed enough."""
    results = []
    race = data.get('race', {})
    course = race.get('course_description', {})
    character = course.get('character', '')
    
    # Should be at least 80 characters
    length_ok = len(character) >= 80
    results.append((f"{race_name}: Course character detailed", length_ok,
                   f"Too short ({len(character)} chars, need 80+)" if not length_ok else f"OK ({len(character)} chars)"))
    
    return results

def test_signature_challenge_detail(data: Dict, race_name: str) -> List[Tuple[str, bool, str]]:
    """Test that signature challenge is detailed enough."""
    results = []
    race = data.get('race', {})
    course = race.get('course_description', {})
    challenge = course.get('signature_challenge', '')
    
    # Should be at least 60 characters
    length_ok = len(challenge) >= 60
    results.append((f"{race_name}: Signature challenge detailed", length_ok,
                   f"Too short ({len(challenge)} chars, need 60+)" if not length_ok else f"OK ({len(challenge)} chars)"))
    
    return results

def test_minimum_suffering_zones(data: Dict, race_name: str) -> List[Tuple[str, bool, str]]:
    """Test that there are enough suffering zones."""
    results = []
    race = data.get('race', {})
    course = race.get('course_description', {})
    zones = course.get('suffering_zones', [])
    
    # Should have at least 3 zones
    has_enough = len(zones) >= 3
    results.append((f"{race_name}: Minimum suffering zones", has_enough,
                   f"Only {len(zones)} zones (need 3+)" if not has_enough else f"OK ({len(zones)} zones)"))
    
    return results

def test_premier_course_highlighted(data: Dict, race_name: str) -> List[Tuple[str, bool, str]]:
    """Test that premier/flagship course distance is highlighted in descriptions."""
    results = []
    race = data.get('race', {})
    vitals = race.get('vitals', {})
    distance = vitals.get('distance_mi', 0)
    course = race.get('course_description', {})
    character = course.get('character', '').lower()
    challenge = course.get('signature_challenge', '').lower()
    
    # Known premier courses that should be mentioned
    premier_courses = {
        'Ned Gravel': {'distance': 70, 'name': 'Tungsten'},
        'Barry Roubaix': {'distance': 62, 'name': 'Killer'},
        'SBT GRVL': {'distance': 108, 'name': 'Black'},
        'Unbound': {'distance': 200, 'name': '200'},
        'Belgian Waffle Ride': {'distance': 131, 'name': 'Waffle'},
    }
    
    if race_name in premier_courses:
        expected = premier_courses[race_name]
        if distance != expected['distance']:
            results.append((f"{race_name}: Premier course distance", False,
                           f"Expected {expected['distance']} mi ({expected['name']} course), got {distance} mi"))
        else:
            # Check if premier course name is mentioned
            name_mentioned = expected['name'].lower() in character or expected['name'].lower() in challenge
            results.append((f"{race_name}: Premier course highlighted", name_mentioned,
                           f"Premier course '{expected['name']}' not mentioned in descriptions" if not name_mentioned else "OK"))
    
    return results

def run_all_tests():
    """Run all course content quality tests."""
    data_dir = Path(__file__).parent.parent / 'data'
    all_results = []
    
    for json_file in sorted(data_dir.glob('*-data.json')):
        race_name = json_file.stem.replace('-data', '').replace('-', ' ').title()
        try:
            data = load_race_data(str(json_file))
            actual_race_name = data.get('race', {}).get('display_name', race_name)
            
            print(f"\n{'='*60}")
            print(f"Testing Course Content: {actual_race_name}")
            print(f"{'='*60}")
            
            # Run all test suites
            all_results.extend(test_suffering_zones_detail(data, actual_race_name))
            all_results.extend(test_course_character_detail(data, actual_race_name))
            all_results.extend(test_signature_challenge_detail(data, actual_race_name))
            all_results.extend(test_minimum_suffering_zones(data, actual_race_name))
            all_results.extend(test_premier_course_highlighted(data, actual_race_name))
            
        except Exception as e:
            print(f"ERROR loading {json_file}: {e}")
            all_results.append((f"{race_name}: File loads", False, str(e)))
    
    # Summary
    print(f"\n{'='*60}")
    print("COURSE CONTENT QUALITY SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, p, _ in all_results if p)
    total = len(all_results)
    failed = total - passed
    
    print(f"Total tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success rate: {passed/total*100:.1f}%")
    
    if failed > 0:
        print(f"\n{'='*60}")
        print("FAILED TESTS:")
        print(f"{'='*60}")
        for test_name, passed, message in all_results:
            if not passed:
                print(f"❌ {test_name}")
                print(f"   {message}")
    
    return failed == 0

if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
