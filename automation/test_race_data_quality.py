"""
Regression tests for race data JSON files.
Ensures all race data files meet quality standards.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

def load_race_data(filepath: str) -> Dict:
    """Load and parse a race data JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def test_required_fields(data: Dict, race_name: str) -> List[Tuple[str, bool, str]]:
    """Test that all required fields are present."""
    results = []
    race = data.get('race', {})
    
    required_fields = [
        ('name', 'Race name'),
        ('slug', 'Race slug'),
        ('display_name', 'Display name'),
        ('tagline', 'Tagline'),
        ('race_challenge_tagline', 'Race challenge tagline'),
        ('vitals', 'Vitals section'),
        ('vitals.distance_mi', 'Distance in miles'),
        ('vitals.elevation_ft', 'Elevation in feet'),
        ('vitals.location', 'Location'),
        ('vitals.location_badge', 'Location badge'),
        ('vitals.date', 'Date'),
        ('climate', 'Climate section'),
        ('climate.primary', 'Climate primary'),
        ('climate.description', 'Climate description'),
        ('terrain', 'Terrain section'),
        ('terrain.primary', 'Terrain primary'),
        ('terrain.technical_rating', 'Technical rating'),
        ('altitude', 'Altitude section'),
        ('altitude.altitude_impact', 'Altitude impact'),
        ('gravel_god_rating', 'Gravel God rating'),
        ('gravel_god_rating.overall_score', 'Overall score'),
        ('gravel_god_rating.tier', 'Tier'),
        ('history', 'History section'),
        ('history.founded', 'Founded year'),
        ('history.origin_story', 'Origin story'),
        ('course_description', 'Course description'),
        ('course_description.character', 'Course character'),
        ('course_description.signature_challenge', 'Signature challenge'),
        ('ratings_breakdown', 'Ratings breakdown'),
        ('biased_opinion', 'Biased opinion'),
        ('biased_opinion.verdict', 'Verdict'),
        ('biased_opinion.summary', 'Summary'),
        ('black_pill', 'Black pill'),
        ('black_pill.reality', 'Black pill reality'),
        ('final_verdict', 'Final verdict'),
        ('final_verdict.score', 'Final verdict score'),
        ('logistics', 'Logistics'),
        ('logistics.airport', 'Airport'),
        ('logistics.official_site', 'Official site'),
        ('seo', 'SEO section'),
        ('seo.title', 'SEO title'),
        ('seo.meta_description', 'Meta description'),
        ('seo.focus_keyword', 'Focus keyword'),
    ]
    
    for field_path, field_name in required_fields:
        parts = field_path.split('.')
        value = race
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                value = None
                break
        
        passed = value is not None and value != ""
        results.append((f"{race_name}: {field_name}", passed, 
                       f"Missing or empty: {field_path}" if not passed else "OK"))
    
    return results

def test_suffering_zones_quality(data: Dict, race_name: str) -> List[Tuple[str, bool, str]]:
    """Test that suffering zones are detailed enough."""
    results = []
    race = data.get('race', {})
    course = race.get('course_description', {})
    zones = course.get('suffering_zones', [])
    
    if not zones:
        results.append((f"{race_name}: Suffering zones exist", False, "No suffering zones defined"))
        return results
    
    results.append((f"{race_name}: Suffering zones exist", True, f"{len(zones)} zones defined"))
    
    # Check each zone has required fields
    for i, zone in enumerate(zones):
        zone_num = i + 1
        has_mile = 'mile' in zone or 'stage' in zone
        has_label = 'label' in zone and zone['label']
        has_desc = 'desc' in zone and zone['desc'] and len(zone['desc']) > 20
        
        results.append((f"{race_name}: Zone {zone_num} has location", has_mile, 
                       "Missing mile/stage" if not has_mile else "OK"))
        results.append((f"{race_name}: Zone {zone_num} has label", has_label,
                       "Missing label" if not has_label else "OK"))
        results.append((f"{race_name}: Zone {zone_num} description detailed", has_desc,
                       f"Description too short ({len(zone.get('desc', ''))} chars)" if not has_desc else "OK"))
    
    return results

def test_ratings_completeness(data: Dict, race_name: str) -> List[Tuple[str, bool, str]]:
    """Test that ratings breakdown is complete."""
    results = []
    race = data.get('race', {})
    ratings = race.get('ratings_breakdown', {})
    
    required_ratings = [
        'prestige', 'length', 'technicality', 'elevation', 
        'climate', 'altitude', 'adventure'
    ]
    
    for rating in required_ratings:
        if rating not in ratings:
            results.append((f"{race_name}: {rating} rating", False, "Missing"))
            continue
        
        rating_data = ratings[rating]
        has_score = 'score' in rating_data
        has_explanation = 'explanation' in rating_data and len(rating_data['explanation']) > 30
        
        results.append((f"{race_name}: {rating} has score", has_score, 
                       "Missing score" if not has_score else "OK"))
        results.append((f"{race_name}: {rating} has explanation", has_explanation,
                       f"Explanation too short ({len(rating_data.get('explanation', ''))} chars)" if not has_explanation else "OK"))
    
    return results

def test_content_quality(data: Dict, race_name: str) -> List[Tuple[str, bool, str]]:
    """Test content quality - length, detail, etc."""
    results = []
    race = data.get('race', {})
    
    # Check origin story length
    origin = race.get('history', {}).get('origin_story', '')
    results.append((f"{race_name}: Origin story detailed", len(origin) > 100,
                   f"Too short ({len(origin)} chars)" if len(origin) <= 100 else "OK"))
    
    # Check biased opinion summary length
    summary = race.get('biased_opinion', {}).get('summary', '')
    results.append((f"{race_name}: Biased opinion summary detailed", len(summary) > 150,
                   f"Too short ({len(summary)} chars)" if len(summary) <= 150 else "OK"))
    
    # Check black pill reality length
    reality = race.get('black_pill', {}).get('reality', '')
    results.append((f"{race_name}: Black pill reality detailed", len(reality) > 100,
                   f"Too short ({len(reality)} chars)" if len(reality) <= 100 else "OK"))
    
    # Check signature challenge length
    challenge = race.get('course_description', {}).get('signature_challenge', '')
    results.append((f"{race_name}: Signature challenge detailed", len(challenge) > 50,
                   f"Too short ({len(challenge)} chars)" if len(challenge) <= 50 else "OK"))
    
    # Check notable moments exist
    moments = race.get('history', {}).get('notable_moments', [])
    results.append((f"{race_name}: Notable moments exist", len(moments) >= 3,
                   f"Only {len(moments)} moments (need 3+)" if len(moments) < 3 else "OK"))
    
    return results

def test_distance_flagship(data: Dict, race_name: str) -> List[Tuple[str, bool, str]]:
    """Test that distance matches flagship/premier course."""
    results = []
    race = data.get('race', {})
    vitals = race.get('vitals', {})
    distance = vitals.get('distance_mi')
    
    # Known premier course distances (will need to be updated as we find issues)
    premier_distances = {
        'Ned Gravel': 70,  # Tungsten course
        'Barry Roubaix': 62,  # The Killer
        'SBT GRVL': 108,  # Black course
        'Unbound': 200,  # 200-mile
        'Belgian Waffle Ride': 131,  # Waffle course
    }
    
    if race_name in premier_distances:
        expected = premier_distances[race_name]
        passed = distance == expected
        results.append((f"{race_name}: Distance matches premier course", passed,
                       f"Expected {expected} mi, got {distance} mi" if not passed else "OK"))
    
    return results

def test_seo_quality(data: Dict, race_name: str) -> List[Tuple[str, bool, str]]:
    """Test SEO metadata quality."""
    results = []
    race = data.get('race', {})
    seo = race.get('seo', {})
    
    title = seo.get('title', '')
    meta_desc = seo.get('meta_description', '')
    keyword = seo.get('focus_keyword', '')
    
    results.append((f"{race_name}: SEO title exists", len(title) > 20,
                   f"Too short ({len(title)} chars)" if len(title) <= 20 else "OK"))
    results.append((f"{race_name}: Meta description length", 120 <= len(meta_desc) <= 160,
                   f"Length {len(meta_desc)} (should be 120-160)" if not (120 <= len(meta_desc) <= 160) else "OK"))
    results.append((f"{race_name}: Focus keyword exists", len(keyword) > 0,
                   "Missing" if len(keyword) == 0 else "OK"))
    
    return results

def run_all_tests():
    """Run all tests on all race data files."""
    data_dir = Path(__file__).parent.parent / 'data'
    all_results = []
    
    for json_file in sorted(data_dir.glob('*-data.json')):
        race_name = json_file.stem.replace('-data', '').replace('-', ' ').title()
        try:
            data = load_race_data(str(json_file))
            actual_race_name = data.get('race', {}).get('display_name', race_name)
            
            print(f"\n{'='*60}")
            print(f"Testing: {actual_race_name}")
            print(f"{'='*60}")
            
            # Run all test suites
            all_results.extend(test_required_fields(data, actual_race_name))
            all_results.extend(test_suffering_zones_quality(data, actual_race_name))
            all_results.extend(test_ratings_completeness(data, actual_race_name))
            all_results.extend(test_content_quality(data, actual_race_name))
            all_results.extend(test_distance_flagship(data, actual_race_name))
            all_results.extend(test_seo_quality(data, actual_race_name))
            
        except Exception as e:
            print(f"ERROR loading {json_file}: {e}")
            all_results.append((f"{race_name}: File loads", False, str(e)))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
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
