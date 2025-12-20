"""
Script to fix common quality issues in race data JSON files.
Adds missing required fields with sensible defaults.
"""

import json
import os
from pathlib import Path
from typing import Dict

def ensure_seo_section(data: Dict) -> bool:
    """Ensure SEO section exists with all required fields."""
    race = data.get('race', {})
    
    if 'seo' not in race or not race['seo']:
        race['seo'] = {}
    
    seo = race['seo']
    race_name = race.get('display_name', race.get('name', 'Race'))
    location = race.get('vitals', {}).get('location', '')
    city = location.split(',')[0].strip() if ',' in location else location
    distance = race.get('vitals', {}).get('distance_mi', 0)
    distance_str = f"{distance}-mile" if isinstance(distance, (int, float)) else str(distance)
    slug = race.get('slug', race_name.lower().replace(' ', '-'))
    
    if 'title' not in seo or not seo['title']:
        seo['title'] = f"{race_name} Race Guide | Training Plans & {city} Course Intel"
    
    if 'meta_description' not in seo or not seo['meta_description']:
        challenge = race.get('race_challenge_tagline', '') or race.get('course_description', {}).get('signature_challenge', '')
        base = f"{race_name} {city} guide: {distance_str} gravel race"
        if challenge and len(challenge) < 40:
            base += f" at {challenge}"
        meta_desc = f"{base}. Get training plans & course breakdown."
        if len(meta_desc) > 160:
            meta_desc = meta_desc[:157] + "..."
        seo['meta_description'] = meta_desc
    
    if 'focus_keyword' not in seo or not seo['focus_keyword']:
        seo['focus_keyword'] = race_name.lower()
    
    if 'slug' not in seo or not seo['slug']:
        seo['slug'] = slug
    
    return True

def ensure_altitude_section(data: Dict) -> bool:
    """Ensure altitude section exists with all required fields."""
    race = data.get('race', {})
    
    if 'altitude' not in race or not race['altitude']:
        race['altitude'] = {}
    
    altitude = race['altitude']
    
    # Set defaults if missing
    if 'start_elevation_ft' not in altitude:
        altitude['start_elevation_ft'] = 0
    if 'max_elevation_ft' not in altitude:
        altitude['max_elevation_ft'] = 0
    if 'min_elevation_ft' not in altitude:
        altitude['min_elevation_ft'] = 0
    
    if 'altitude_impact' not in altitude or not altitude['altitude_impact']:
        max_elev = altitude.get('max_elevation_ft', 0)
        if max_elev >= 10000:
            altitude['altitude_impact'] = "SEVERE - Race elevation above 10,000 feet. Expect 15-20% power reduction from sea level."
            altitude['acclimatization_required'] = True
        elif max_elev >= 8000:
            altitude['altitude_impact'] = "SIGNIFICANT - Race elevation 8,000-10,000 feet. Expect 8-15% power reduction from sea level."
            altitude['acclimatization_required'] = True
        elif max_elev >= 6000:
            altitude['altitude_impact'] = "MODERATE - Race elevation 6,000-8,000 feet. Expect 5-10% power reduction from sea level."
            altitude['acclimatization_required'] = False
        elif max_elev >= 4000:
            altitude['altitude_impact'] = "MINOR - Race elevation 4,000-6,000 feet. Minor altitude consideration."
            altitude['acclimatization_required'] = False
        else:
            altitude['altitude_impact'] = "NONE - Race elevation below 4,000 feet. Altitude irrelevant."
            altitude['acclimatization_required'] = False
    
    if 'acclimatization_required' not in altitude:
        altitude['acclimatization_required'] = altitude.get('max_elevation_ft', 0) >= 8000
    
    return True

def ensure_race_challenge_tagline(data: Dict) -> bool:
    """Ensure race_challenge_tagline exists."""
    race = data.get('race', {})
    
    if 'race_challenge_tagline' not in race or not race['race_challenge_tagline']:
        # Try to derive from signature challenge or course description
        sig_challenge = race.get('course_description', {}).get('signature_challenge', '')
        if sig_challenge and len(sig_challenge) < 100:
            race['race_challenge_tagline'] = sig_challenge[:80]
        else:
            # Create from key features
            vitals = race.get('vitals', {})
            elevation = vitals.get('elevation_ft', 0)
            distance = vitals.get('distance_mi', 0)
            climate = race.get('climate', {}).get('primary', '')
            
            parts = []
            if elevation >= 10000:
                parts.append(f"{elevation//1000}K+ feet of climbing")
            elif elevation >= 5000:
                parts.append(f"{elevation//1000}K+ feet of climbing")
            
            if 'altitude' in climate.lower() or race.get('altitude', {}).get('max_elevation_ft', 0) >= 8000:
                parts.append("at altitude")
            
            if parts:
                race['race_challenge_tagline'] = " and ".join(parts)
            else:
                race['race_challenge_tagline'] = "challenging gravel terrain"
    
    return True

def fix_meta_description_length(data: Dict) -> bool:
    """Fix meta description to be 120-160 characters."""
    race = data.get('race', {})
    seo = race.get('seo', {})
    
    if 'meta_description' in seo and seo['meta_description']:
        desc = seo['meta_description']
        if len(desc) < 120:
            # Try to expand it
            race_name = race.get('display_name', race.get('name', 'Race'))
            location = race.get('vitals', {}).get('location', '')
            city = location.split(',')[0].strip() if ',' in location else location
            distance = race.get('vitals', {}).get('distance_mi', 0)
            distance_str = f"{distance}-mile" if isinstance(distance, (int, float)) else str(distance)
            
            base = f"{race_name} {city} guide: {distance_str} gravel race"
            challenge = race.get('race_challenge_tagline', '')
            if challenge and len(challenge) < 40:
                base += f" at {challenge}"
            new_desc = f"{base}. Get training plans & course breakdown."
            if len(new_desc) <= 160:
                seo['meta_description'] = new_desc
        elif len(desc) > 160:
            # Truncate intelligently
            seo['meta_description'] = desc[:157] + "..."
    
    return True

def fix_file(filepath: Path) -> Dict[str, bool]:
    """Fix all issues in a single file."""
    results = {}
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        results['seo'] = ensure_seo_section(data)
        results['altitude'] = ensure_altitude_section(data)
        results['challenge_tagline'] = ensure_race_challenge_tagline(data)
        results['meta_desc_length'] = fix_meta_description_length(data)
        
        # Write back
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return results
    except Exception as e:
        print(f"ERROR fixing {filepath}: {e}")
        return {'error': str(e)}

def main():
    """Fix all race data files."""
    data_dir = Path(__file__).parent.parent / 'data'
    
    print("Fixing race data quality issues...")
    print("=" * 60)
    
    fixed_count = 0
    for json_file in sorted(data_dir.glob('*-data.json')):
        race_name = json_file.stem.replace('-data', '').replace('-', ' ').title()
        print(f"\nFixing: {race_name}")
        
        results = fix_file(json_file)
        if 'error' not in results:
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
