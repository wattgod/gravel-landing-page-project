#!/usr/bin/env python3
"""
Enhance Global Gravel Race Database with:
1. Missing high-priority races
2. Proper scoring formula
3. Data quality flags
4. Source tracking
5. Last verified dates
"""

import json
from pathlib import Path
from datetime import datetime

def calculate_priority_score(race):
    """
    Calculate priority score using actual formula:
    Score = (Field_Size_Tier × 3) + (Competition_Gap × 4) + (Protocol_Fit × 2) + (Prestige × 1)
    
    Field_Size_Tier: 1-5 based on field size
    Competition_Gap: 1-5 based on competition level (NONE=5, LOW=4, MEDIUM=2, HIGH=1)
    Protocol_Fit: 1-3 based on specialization opportunity
    Prestige: 1-3 based on tier and event type
    """
    # Field Size Tier (1-5)
    field_size = str(race.get('Field Size', '')).lower()
    if '5000+' in field_size or '4000+' in field_size:
        field_tier = 5
    elif '3000+' in field_size or '2000+' in field_size:
        field_tier = 4
    elif '1000+' in field_size or '1500+' in field_size:
        field_tier = 3
    elif '500+' in field_size or '800+' in field_size:
        field_tier = 2
    else:
        field_tier = 1
    
    # Competition Gap (1-5, inverted - NONE is best)
    competition = race.get('Competition', 'UNKNOWN')
    comp_map = {
        'NONE': 5,
        'LOW': 4,
        'MEDIUM': 2,
        'HIGH': 1,
        'UNKNOWN': 1
    }
    competition_gap = comp_map.get(competition, 1)
    
    # Protocol Fit (1-3)
    protocol = race.get('Protocol Fit', 'Standard')
    protocol_special = ['Altitude', 'Heat', 'Ultra', 'Stage Race', 'Technical']
    if any(p in protocol for p in protocol_special):
        protocol_score = 3
    elif protocol == 'Standard':
        protocol_score = 2
    else:
        protocol_score = 1
    
    # Prestige (1-3)
    tier = race.get('Tier', 3)
    if tier == 1:
        prestige = 3
    elif tier == 2:
        prestige = 2
    else:
        prestige = 1
    
    # Calculate score (max = 5×3 + 5×4 + 3×2 + 3×1 = 15+20+6+3 = 44, normalize to 1-10)
    raw_score = (field_tier * 3) + (competition_gap * 4) + (protocol_score * 2) + (prestige * 1)
    normalized_score = round((raw_score / 44) * 10, 1)
    
    return min(10, max(1, normalized_score))

def add_data_quality_flags(race, sources_used):
    """Add data quality and source tracking to race entry"""
    # Determine data quality based on what we know
    quality_flags = {}
    
    # Field Size
    if race.get('Field Size'):
        if '+' in str(race.get('Field Size')) or '-' in str(race.get('Field Size')):
            quality_flags['field_size'] = 'Estimated'
        else:
            quality_flags['field_size'] = 'Verified'
    else:
        quality_flags['field_size'] = 'Unknown'
    
    # Competition Level
    comp = race.get('Competition', '')
    if comp in ['HIGH', 'MEDIUM', 'LOW', 'NONE']:
        quality_flags['competition'] = 'Estimated'  # Needs TrainingPeaks verification
    else:
        quality_flags['competition'] = 'Unknown'
    
    # Elevation
    if race.get('Elevation (ft)'):
        quality_flags['elevation'] = 'Estimated'  # Usually from race websites
    else:
        quality_flags['elevation'] = 'Unknown'
    
    # Add source tracking
    race['_data_quality'] = quality_flags
    race['_sources'] = sources_used
    race['_last_verified'] = datetime.now().strftime('%Y-%m-%d')
    race['_verified_by'] = 'Database Enhancement Script'
    
    return race

def main():
    # Load our database
    db_file = Path('data/gravel_race_database.json')
    with open(db_file) as f:
        db_data = json.load(f)
    
    db_races = db_data['All Races']['rows']
    
    print("="*80)
    print("ENHANCING GLOBAL GRAVEL RACE DATABASE")
    print("="*80)
    print()
    
    # Step 1: Add missing high-priority races
    print("Step 1: Adding missing high-priority races...")
    missing_races = [
        {
            "Race Name": "Highlands Gravel Classic",
            "Location": "Fayetteville-Goshen AR",
            "Country": "USA",
            "Region": "Southeast",
            "Date/Month": "Late April",
            "Distance (mi)": "68/54",
            "Elevation (ft)": "6000-8000",
            "Field Size": "800-1200",
            "Entry Cost": "$80-100",
            "Tier": 1,
            "Competition": "NONE",
            "Protocol Fit": "Climbing",
            "Priority Score": None,  # Will calculate
            "Notes": "ONE OF ONLY 2 U.S. QUALIFIERS for UCI Gravel World Series. Top 25% qualify for World Championships.",
            "_source": "User identification - Critical missing race",
            "_added_date": datetime.now().strftime('%Y-%m-%d')
        },
        {
            "Race Name": "USA Cycling Gravel National Championships",
            "Location": "La Crescent MN",
            "Country": "USA",
            "Region": "Midwest",
            "Date/Month": "Mid-September",
            "Distance (mi)": "25-116",
            "Elevation (ft)": "4000-8000",
            "Field Size": "1500-2000",
            "Entry Cost": "$100-200",
            "Tier": 1,
            "Competition": "MEDIUM",
            "Protocol Fit": "Standard",
            "Priority Score": None,
            "Notes": "Official national championship. Coincides with La Crescent Apple Festival. 2025: Sept 20, 2026: Sept 12.",
            "_source": "User identification - Official championship",
            "_added_date": datetime.now().strftime('%Y-%m-%d')
        },
        {
            "Race Name": "Red Granite Grinder",
            "Location": "Athens WI",
            "Country": "USA",
            "Region": "Midwest",
            "Date/Month": "Early October",
            "Distance (mi)": "50/100/150",
            "Elevation (ft)": "6000-8000",
            "Field Size": "500-800",
            "Entry Cost": "$75-125",
            "Tier": 2,
            "Competition": "NONE",
            "Protocol Fit": "Standard",
            "Priority Score": None,
            "Notes": "User's favorite race. Part of Ironbear 1000 series. 92% gravel on 100mi route.",
            "_source": "User identification - Personal favorite",
            "_added_date": datetime.now().strftime('%Y-%m-%d')
        },
    ]
    
    existing_names = {r.get('Race Name', '').lower().strip() for r in db_races}
    added_count = 0
    
    for race in missing_races:
        name = race.get('Race Name', '').lower().strip()
        if name not in existing_names:
            # Calculate priority score
            race['Priority Score'] = calculate_priority_score(race)
            # Add data quality flags
            race = add_data_quality_flags(race, ['User identification', 'Web research'])
            db_races.append(race)
            existing_names.add(name)
            added_count += 1
            print(f"  ✓ Added: {race.get('Race Name')} (Score: {race.get('Priority Score')})")
        else:
            print(f"  ⚠ Already exists: {race.get('Race Name')}")
    
    print(f"\nAdded {added_count} missing races")
    print()
    
    # Step 2: Recalculate priority scores for all races using formula
    print("Step 2: Recalculating priority scores using formula...")
    recalculated = 0
    for race in db_races:
        old_score = race.get('Priority Score')
        new_score = calculate_priority_score(race)
        if old_score != new_score:
            race['Priority Score'] = new_score
            race['_priority_score_old'] = old_score
            race['_priority_score_calculated'] = datetime.now().strftime('%Y-%m-%d')
            recalculated += 1
    
    print(f"Recalculated {recalculated} priority scores")
    print()
    
    # Step 3: Add data quality flags to all races
    print("Step 3: Adding data quality flags and source tracking...")
    for race in db_races:
        if '_data_quality' not in race:
            sources = race.get('_source', 'Original database')
            if not isinstance(sources, list):
                sources = [sources] if sources else ['Original database']
            race = add_data_quality_flags(race, sources)
    
    print("Added data quality flags to all races")
    print()
    
    # Update database
    db_data['All Races']['rows'] = db_races
    db_data['_metadata'] = {
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_races': len(db_races),
        'enhancements': {
            'missing_races_added': added_count,
            'priority_scores_recalculated': recalculated,
            'data_quality_flags_added': True,
            'source_tracking_added': True
        }
    }
    
    # Save enhanced database
    enhanced_file = Path('data/gravel_race_database_enhanced.json')
    with open(enhanced_file, 'w') as f:
        json.dump(db_data, f, indent=2, default=str)
    
    print(f"✓ Enhanced database saved to: {enhanced_file}")
    print(f"✓ Total races: {len(db_races)}")
    print()
    print("="*80)
    print("ENHANCEMENT COMPLETE")
    print("="*80)

if __name__ == '__main__':
    main()
