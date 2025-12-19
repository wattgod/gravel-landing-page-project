"""
Landing Page Index Generator

Generates a structured JSON index file for each landing page containing
all searchable/filterable data. This enables building a searchable database
later without re-parsing HTML.

Usage:
    from automation.generate_landing_page_index import generate_index
    
    index = generate_index(race_data)
    # Save to race_index.json
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


def extract_ratings(data: Dict) -> Dict[str, Any]:
    """Extract course ratings for search/filtering."""
    race = data.get('race', {})
    ratings_breakdown = race.get('ratings_breakdown', {})
    gravel_god_rating = race.get('gravel_god_rating', {})
    
    return {
        'overall_score': gravel_god_rating.get('overall_score'),
        'tier': gravel_god_rating.get('tier'),
        'tier_label': gravel_god_rating.get('tier_label'),
        'length_score': ratings_breakdown.get('length', {}).get('score'),
        'technicality_score': ratings_breakdown.get('technicality', {}).get('score'),
        'elevation_score': ratings_breakdown.get('elevation', {}).get('score'),
        'climate_score': ratings_breakdown.get('climate', {}).get('score'),
        'altitude_score': ratings_breakdown.get('altitude', {}).get('score'),
        'adventure_score': ratings_breakdown.get('adventure', {}).get('score'),
        'logistics_score': ratings_breakdown.get('logistics', {}).get('score'),
        'prestige_score': gravel_god_rating.get('prestige')
    }


def extract_biased_opinion(data: Dict) -> Dict[str, Any]:
    """Extract biased opinion ratings."""
    race = data.get('race', {})
    opinion = race.get('biased_opinion', {})
    gravel_god_rating = race.get('gravel_god_rating', {})
    
    return {
        'overall_score': gravel_god_rating.get('biased_opinion'),
        'course_quality': opinion.get('course_quality'),
        'organization': opinion.get('organization'),
        'value': opinion.get('value'),
        'atmosphere': opinion.get('atmosphere'),
        'summary': opinion.get('summary')
    }


def extract_course_characteristics(data: Dict) -> Dict[str, Any]:
    """Extract course characteristics for filtering."""
    race = data.get('race', {})
    course = race.get('course_description', {})
    vitals = race.get('vitals', {})
    terrain = race.get('terrain', {})
    climate = race.get('climate', {})
    
    return {
        'distance_miles': vitals.get('distance_mi'),
        'elevation_gain_feet': vitals.get('elevation_ft'),
        'terrain_type': terrain.get('primary'),
        'terrain_surface': terrain.get('surface'),
        'technical_rating': terrain.get('technical_rating'),
        'signature_challenge': course.get('signature_challenge'),
        'character': course.get('character'),
        'key_features': terrain.get('features', []),
        'suffering_zones': course.get('suffering_zones', []),
        'location': vitals.get('location'),
        'climate_primary': climate.get('primary'),
        'climate_description': climate.get('description'),
        'climate_challenges': climate.get('challenges', [])
    }


def extract_tldr(data: Dict) -> Dict[str, Any]:
    """Extract TLDR decision grid data."""
    tldr = data.get('tldr', {})
    return {
        'best_for': tldr.get('best_for'),
        'not_for': tldr.get('not_for'),
        'key_considerations': tldr.get('key_considerations', [])
    }


def extract_logistics(data: Dict) -> Dict[str, Any]:
    """Extract logistics information."""
    race = data.get('race', {})
    vitals = race.get('vitals', {})
    logistics = race.get('logistics', {})
    
    location = vitals.get('location', '')
    location_parts = location.split(',') if location else []
    
    return {
        'location': location,
        'location_badge': vitals.get('location_badge'),
        'county': vitals.get('county'),
        'city': location_parts[0].strip() if len(location_parts) > 0 else None,
        'state': location_parts[1].strip() if len(location_parts) > 1 else None,
        'country': 'USA',
        'date': vitals.get('date'),
        'date_specific': vitals.get('date_specific'),
        'venue': logistics.get('venue'),
        'parking': logistics.get('parking'),
        'lodging': logistics.get('lodging'),
        'travel_tips': logistics.get('travel_tips'),
        'registration': vitals.get('registration'),
        'start_time': vitals.get('start_time'),
        'field_size': vitals.get('field_size')
    }


def extract_final_verdict(data: Dict) -> Dict[str, Any]:
    """Extract final verdict and recommendations."""
    race = data.get('race', {})
    verdict = race.get('final_verdict', {})
    gravel_god_rating = race.get('gravel_god_rating', {})
    
    return {
        'overall_score': gravel_god_rating.get('overall_score'),
        'recommendation': verdict.get('recommendation'),
        'best_for_riders': verdict.get('best_for_riders', []),
        'key_strengths': verdict.get('key_strengths', []),
        'considerations': verdict.get('considerations', []),
        'summary': verdict.get('summary')
    }


def extract_history(data: Dict) -> Dict[str, Any]:
    """Extract race history and facts."""
    race = data.get('race', {})
    history = race.get('history', {})
    return {
        'founded': history.get('founded'),
        'editions': history.get('editions'),
        'notable_facts': history.get('notable_facts', []),
        'random_facts': history.get('random_facts', []),
        'timeline': history.get('timeline', [])
    }


def generate_index(race_data: Dict, output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate a structured index JSON for a landing page.
    
    Args:
        race_data: Full race data dictionary
        output_path: Optional path to save the index file
    
    Returns:
        Structured index dictionary
    """
    race = race_data.get('race', {})
    
    index = {
        # Core identifiers
        'race_id': race.get('slug'),
        'race_name': race.get('display_name') or race.get('name'),
        'race_slug': race.get('slug'),
        'tier': race.get('gravel_god_rating', {}).get('tier'),
        'tier_label': race.get('gravel_god_rating', {}).get('tier_label'),
        'tagline': race.get('tagline'),
        
        # Dates
        'race_date': race.get('vitals', {}).get('date_specific') or race.get('vitals', {}).get('date'),
        'year': race.get('year'),
        
        # Course characteristics (for filtering)
        'course': extract_course_characteristics(race_data),
        
        # Ratings (for filtering by difficulty, etc.)
        'ratings': extract_ratings(race_data),
        
        # Biased opinion (for filtering by quality/value)
        'biased_opinion': extract_biased_opinion(race_data),
        
        # TLDR (for "best for" searches)
        'tldr': extract_tldr(race_data),
        
        # Logistics (for location-based search)
        'logistics': extract_logistics(race_data),
        
        # Final verdict (for overall recommendations)
        'final_verdict': extract_final_verdict(race_data),
        
        # History
        'history': extract_history(race_data),
        
        # Training plans
        'training_plans': {
            'available': True,
            'model': 'on-demand',
            'questionnaire_url': f"https://wattgod.github.io/training-plans-component/training-plan-questionnaire.html?race={race.get('slug')}",
            'race_challenge_tagline': race.get('race_challenge_tagline')
        },
        
        # SEO and metadata
        'seo': race.get('seo', {}),
        
        # Generated metadata
        'index_generated_at': datetime.now().isoformat(),
        'landing_page_url': race.get('seo', {}).get('canonical_url') or f"/races/{race.get('slug')}",
        
        # Additional metadata
        'ridewithgps_id': race.get('course_description', {}).get('ridewithgps_id'),
        'prize_purse': race.get('vitals', {}).get('prize_purse'),
        'field_size': race.get('vitals', {}).get('field_size')
    }
    
    # Add searchable text fields (for full-text search)
    searchable_text = []
    searchable_text.append(race.get('display_name') or race.get('name'))
    searchable_text.append(race.get('tagline', ''))
    searchable_text.append(race.get('course_description', {}).get('character', ''))
    searchable_text.append(race.get('course_description', {}).get('signature_challenge', ''))
    searchable_text.append(' '.join(race.get('terrain', {}).get('features', [])))
    searchable_text.append(race.get('vitals', {}).get('location', ''))
    searchable_text.append(race.get('vitals', {}).get('county', ''))
    searchable_text.append(' '.join(race.get('tldr', {}).get('key_considerations', [])))
    searchable_text.append(' '.join(race.get('final_verdict', {}).get('best_for_riders', [])))
    searchable_text.append(race.get('climate', {}).get('primary', ''))
    searchable_text.append(race.get('terrain', {}).get('primary', ''))
    
    index['searchable_text'] = ' '.join(filter(None, searchable_text))
    
    # Add filter tags (for quick filtering UI)
    filter_tags = []
    
    # Tier
    tier = race.get('gravel_god_rating', {}).get('tier')
    if tier:
        filter_tags.append(f"tier-{tier}")
    
    # Distance
    distance = race.get('vitals', {}).get('distance_mi')
    if distance:
        if distance < 50:
            filter_tags.append('distance-short')
        elif distance < 100:
            filter_tags.append('distance-medium')
        elif distance < 150:
            filter_tags.append('distance-long')
        else:
            filter_tags.append('distance-ultra')
    
    # Elevation
    elevation = race.get('vitals', {}).get('elevation_ft')
    if elevation:
        if elevation < 5000:
            filter_tags.append('elevation-moderate')
        elif elevation < 10000:
            filter_tags.append('elevation-high')
        else:
            filter_tags.append('elevation-extreme')
    
    # Terrain tags
    terrain_surface = race.get('terrain', {}).get('surface', '')
    terrain_primary = race.get('terrain', {}).get('primary', '')
    terrain_text = f"{terrain_surface} {terrain_primary}".lower()
    
    if 'gravel' in terrain_text:
        filter_tags.append('terrain-gravel')
    if 'pavement' in terrain_text or 'road' in terrain_text:
        filter_tags.append('terrain-pavement')
    if 'single-track' in terrain_text or 'singletrack' in terrain_text:
        filter_tags.append('terrain-singletrack')
    if 'sand' in terrain_text:
        filter_tags.append('terrain-sand')
    if 'water' in terrain_text:
        filter_tags.append('terrain-water-crossings')
    
    # Technical rating
    technical_rating = race.get('terrain', {}).get('technical_rating')
    if technical_rating:
        if technical_rating <= 2:
            filter_tags.append('technical-easy')
        elif technical_rating <= 4:
            filter_tags.append('technical-moderate')
        else:
            filter_tags.append('technical-hard')
    
    # Overall score tags
    overall_score = race.get('gravel_god_rating', {}).get('overall_score')
    if overall_score:
        if overall_score >= 90:
            filter_tags.append('score-excellent')
        elif overall_score >= 80:
            filter_tags.append('score-very-good')
        elif overall_score >= 70:
            filter_tags.append('score-good')
        else:
            filter_tags.append('score-fair')
    
    index['filter_tags'] = filter_tags
    
    # Save if path provided
    if output_path:
        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
    
    return index


def generate_all_indexes(data_dir: str = "data", output_dir: str = "indexes"):
    """
    Generate index files for all race data files.
    
    Args:
        data_dir: Directory containing race data JSON files
        output_dir: Directory to save index files
    """
    from pathlib import Path
    import json
    
    data_path = Path(data_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    race_files = list(data_path.glob("*data.json"))
    
    print(f"Generating indexes for {len(race_files)} races...")
    
    for race_file in race_files:
        with open(race_file, 'r', encoding='utf-8') as f:
            race_data = json.load(f)
        
        race_slug = race_data.get('race', {}).get('slug', race_file.stem.replace('-data', ''))
        index_file = output_path / f"{race_slug}-index.json"
        
        index = generate_index(race_data, str(index_file))
        print(f"  ✓ {race_slug}: {index_file.name}")
    
    print(f"\n✓ Generated {len(race_files)} index files in {output_dir}/")


if __name__ == '__main__':
    import sys
    from pathlib import Path
    
    if len(sys.argv) > 1:
        # Generate index for specific race file
        race_file = sys.argv[1]
        with open(race_file, 'r', encoding='utf-8') as f:
            import json
            race_data = json.load(f)
        
        race_slug = race_data.get('race', {}).get('slug', Path(race_file).stem.replace('-data', ''))
        output_file = f"indexes/{race_slug}-index.json"
        
        index = generate_index(race_data, output_file)
        print(f"✓ Generated index: {output_file}")
    else:
        # Generate all indexes
        generate_all_indexes()
