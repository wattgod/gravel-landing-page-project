"""Fix remaining race data quality issues."""

import json
from pathlib import Path

data_dir = Path(__file__).parent.parent / 'data'

issues = {
    'Gravel Worlds': {'meta_desc_min': True},
    'Leadville Trail 100 MTB': {'challenge_tagline': True, 'meta_desc_min': True},
    'The Mid South': {'meta_desc_min': True},
    'Ned Gravel': {'challenge_tagline': True},
    'Oregon Trail Gravel Grinder': {'challenge_tagline': True},
    "Rebecca's Private Idaho": {'challenge_tagline': True, 'meta_desc_min': True},
    'Rooted Vermont': {'challenge_tagline': True, 'meta_desc_min': True},
    'Sea Otter Classic Gravel': {'challenge_tagline': True, 'meta_desc_min': True},
    'The Rad Dirt Fest': {'challenge_tagline': True, 'meta_desc_min': True},
    'Unbound Gravel 200': {'meta_desc_min': True},
}

for json_file in sorted(data_dir.glob('*-data.json')):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        race = data.get('race', {})
        race_name = race.get('display_name', race.get('name', 'Race'))
        
        if race_name not in issues:
            continue
        
        print(f'Fixing: {race_name}')
        
        # Fix challenge tagline
        if issues[race_name].get('challenge_tagline') and ('race_challenge_tagline' not in race or not race['race_challenge_tagline']):
            sig_challenge = race.get('course_description', {}).get('signature_challenge', '')
            if sig_challenge and len(sig_challenge) < 100:
                race['race_challenge_tagline'] = sig_challenge[:80]
            else:
                vitals = race.get('vitals', {})
                elevation = vitals.get('elevation_ft', 0)
                parts = []
                if elevation >= 10000:
                    parts.append(f'{elevation//1000}K+ feet of climbing')
                elif elevation >= 5000:
                    parts.append(f'{elevation//1000}K+ feet of climbing')
                if race.get('altitude', {}).get('max_elevation_ft', 0) >= 8000:
                    parts.append('at altitude')
                race['race_challenge_tagline'] = ' and '.join(parts) if parts else 'challenging gravel terrain'
            print(f'  ✓ Added challenge tagline')
        
        # Fix meta description length
        if issues[race_name].get('meta_desc_min') and 'seo' in race:
            desc = race['seo'].get('meta_description', '')
            if len(desc) < 120:
                location = race.get('vitals', {}).get('location', '')
                city = location.split(',')[0].strip() if ',' in location else location
                distance = race.get('vitals', {}).get('distance_mi', 0)
                distance_str = f'{distance}-mile' if isinstance(distance, (int, float)) else str(distance)
                challenge = race.get('race_challenge_tagline', '')
                base = f'{race_name} {city} guide: {distance_str} gravel race'
                if challenge and len(challenge) < 40:
                    base += f' at {challenge}'
                new_desc = f'{base}. Get training plans & course breakdown.'
                if len(new_desc) <= 160:
                    race['seo']['meta_description'] = new_desc
                    print(f'  ✓ Fixed meta description length ({len(new_desc)} chars)')
        
        # Write back
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f'Error with {json_file}: {e}')
