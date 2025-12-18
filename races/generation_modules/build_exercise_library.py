#!/usr/bin/env python3
"""
Build Master Exercise Video Library
Converts PN CSV + YouTube fallbacks into structured JSON library
"""

import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Set

# YouTube fallbacks for exercises not in PN library
YOUTUBE_FALLBACKS = {
    "Good Morning": "https://www.youtube.com/watch?v=Daq-wJMUnes",
    "Hip Hinge w/ Dowel": "https://www.youtube.com/watch?v=ctMrDzw8LYQ",
    "KB Swing": "https://www.youtube.com/watch?v=YGnS0QVLcyQ",
    "Kettlebell Swing": "https://www.youtube.com/watch?v=YGnS0QVLcyQ",
    "Pike Push-Up": "https://www.youtube.com/watch?v=XckEEwa1BPI",
    "Clamshell": "https://www.youtube.com/watch?v=V_AnVxKPFlY",
    "Fire Hydrant": "https://www.youtube.com/watch?v=IRkRgk2Gc1E",
    "World's Greatest Stretch": "https://www.youtube.com/watch?v=-CiWQ2IvY34",
    "Hollow Body Hold": "https://www.youtube.com/watch?v=YaXPRqUwItQ",
    "Hollow Body Rock": "https://www.youtube.com/watch?v=mqnf9n0SPU0",
    "Broad Jump": "https://www.youtube.com/watch?v=7s8iH3mJzhk",
    "Suitcase Deadlift": "https://www.youtube.com/watch?v=PdEy1pNcbdA",
    "Heavy DB Row": "https://www.youtube.com/watch?v=pYcpY20QaE8",
}

def normalize_exercise_name(name: str) -> str:
    """Normalize exercise name for ID generation"""
    # Convert to lowercase
    normalized = name.lower()
    # Replace common variations
    normalized = normalized.replace('push-up', 'push_up').replace('pushup', 'push_up')
    normalized = normalized.replace(' ', '_')
    normalized = normalized.replace('-', '_')
    normalized = normalized.replace('/', '_')
    normalized = normalized.replace("'", '')
    normalized = re.sub(r'[^a-z0-9_]', '', normalized)
    # Remove duplicate underscores
    normalized = re.sub(r'_+', '_', normalized)
    return normalized.strip('_')

def generate_aliases(name: str) -> List[str]:
    """Generate common aliases for an exercise name"""
    aliases = []
    
    # Common variations
    variations = {
        'push-up': ['pushup', 'push up', 'press-up'],
        'pushup': ['push-up', 'push up', 'press-up'],
        'dumbbell': ['db', 'dumbell'],
        'db': ['dumbbell', 'dumbell'],
        'kettlebell': ['kb', 'kettle bell'],
        'kb': ['kettlebell', 'kettle bell'],
        'single-leg': ['sl', 'single leg'],
        'single leg': ['sl', 'single-leg'],
        'rdl': ['romanian deadlift'],
        'romanian deadlift': ['rdl'],
        'glute bridge': ['hip bridge'],
        'hip bridge': ['glute bridge'],
    }
    
    name_lower = name.lower()
    for key, variants in variations.items():
        if key in name_lower:
            for variant in variants:
                alias = name_lower.replace(key, variant)
                aliases.append(alias.title())
    
    return aliases

def classify_category(name: str) -> tuple:
    """
    Classify exercise into category and subcategory
    
    Returns: (category, subcategory)
    """
    name_lower = name.lower()
    
    # Squat variations
    if any(word in name_lower for word in ['squat', 'lunge', 'pistol', 'split squat', 'bulgarian']):
        if 'front' in name_lower:
            return ('squat', 'front_squat')
        elif 'back' in name_lower or 'barbell' in name_lower:
            return ('squat', 'back_squat')
        elif 'goblet' in name_lower:
            return ('squat', 'goblet_squat')
        elif 'split' in name_lower or 'bulgarian' in name_lower:
            return ('squat', 'split_squat')
        elif 'lunge' in name_lower:
            return ('squat', 'lunge')
        else:
            return ('squat', 'bodyweight_squat')
    
    # Hinge variations
    if any(word in name_lower for word in ['deadlift', 'rdl', 'romanian', 'hinge', 'good morning', 'swing']):
        if 'swing' in name_lower:
            return ('hinge', 'swing')
        elif 'rdl' in name_lower or 'romanian' in name_lower:
            return ('hinge', 'rdl')
        elif 'deadlift' in name_lower:
            if 'sumo' in name_lower:
                return ('hinge', 'sumo_deadlift')
            elif 'trap' in name_lower:
                return ('hinge', 'trap_bar_deadlift')
            else:
                return ('hinge', 'conventional_deadlift')
        elif 'hinge' in name_lower:
            return ('hinge', 'hip_hinge')
        elif 'good morning' in name_lower:
            return ('hinge', 'good_morning')
        else:
            return ('hinge', 'hinge_pattern')
    
    # Push variations
    if any(word in name_lower for word in ['push', 'press', 'bench', 'chest']):
        if 'overhead' in name_lower or 'shoulder press' in name_lower:
            return ('push', 'vertical_push')
        elif 'bench' in name_lower or 'chest' in name_lower:
            return ('push', 'horizontal_push')
        elif 'push' in name_lower:
            if 'incline' in name_lower or 'hands elevated' in name_lower:
                return ('push', 'incline_push')
            elif 'decline' in name_lower or 'feet elevated' in name_lower:
                return ('push', 'decline_push')
            else:
                return ('push', 'horizontal_push')
        else:
            return ('push', 'horizontal_push')
    
    # Pull variations
    if any(word in name_lower for word in ['row', 'pull', 'chin', 'lat', 'face pull']):
        if 'pull' in name_lower or 'chin' in name_lower:
            return ('pull', 'vertical_pull')
        elif 'row' in name_lower:
            if 'inverted' in name_lower:
                return ('pull', 'inverted_row')
            elif 'bent' in name_lower or 'bent-over' in name_lower:
                return ('pull', 'bent_over_row')
            else:
                return ('pull', 'horizontal_pull')
        else:
            return ('pull', 'horizontal_pull')
    
    # Core variations
    if any(word in name_lower for word in ['plank', 'dead bug', 'hollow', 'bird dog', 'pallof', 'side plank', 'ab wheel', 'russian twist', 'wood chop']):
        if 'plank' in name_lower:
            return ('core', 'anti_extension')
        elif 'dead bug' in name_lower:
            return ('core', 'anti_extension')
        elif 'hollow' in name_lower:
            return ('core', 'anti_extension')
        elif 'pallof' in name_lower or 'chop' in name_lower:
            return ('core', 'anti_rotation')
        elif 'side plank' in name_lower:
            return ('core', 'anti_lateral_flexion')
        elif 'russian twist' in name_lower or 'rotation' in name_lower:
            return ('core', 'rotation')
        else:
            return ('core', 'anti_extension')
    
    # Carry variations
    if 'carry' in name_lower or 'walk' in name_lower and ('farmer' in name_lower or 'suitcase' in name_lower):
        if 'farmer' in name_lower:
            return ('carry', 'farmer_carry')
        elif 'suitcase' in name_lower:
            return ('carry', 'suitcase_carry')
        else:
            return ('carry', 'loaded_carry')
    
    # Glute variations
    if any(word in name_lower for word in ['glute bridge', 'hip bridge', 'hip thrust', 'clamshell', 'fire hydrant', 'monster walk', 'band walk']):
        if 'bridge' in name_lower or 'thrust' in name_lower:
            return ('glute', 'bridge')
        elif 'clamshell' in name_lower:
            return ('glute', 'activation')
        elif 'fire hydrant' in name_lower:
            return ('glute', 'activation')
        elif 'walk' in name_lower:
            return ('glute', 'activation')
        else:
            return ('glute', 'activation')
    
    # Plyometric/Power
    if any(word in name_lower for word in ['jump', 'hop', 'bound', 'explosive', 'plyo', 'clapping']):
        return ('plyometric', 'jump')
    
    # Mobility
    if any(word in name_lower for word in ['stretch', 'mobilization', 'activation', 'warmup', 'mobility', 'world\'s greatest']):
        return ('mobility', 'stretch')
    
    # Default
    return ('other', 'general')

def extract_equipment(name: str) -> List[str]:
    """Extract equipment requirements from exercise name"""
    equipment = []
    name_lower = name.lower()
    
    if 'bodyweight' in name_lower or ('push' in name_lower and 'up' in name_lower) or 'squat' in name_lower and 'barbell' not in name_lower and 'dumbbell' not in name_lower:
        equipment.append('bodyweight')
    
    if 'dumbbell' in name_lower or ' db ' in name_lower or name_lower.startswith('db '):
        equipment.append('dumbbell')
    
    if 'kettlebell' in name_lower or ' kb ' in name_lower or name_lower.startswith('kb '):
        equipment.append('kettlebell')
    
    if 'barbell' in name_lower or 'bb ' in name_lower:
        equipment.append('barbell')
    
    if 'band' in name_lower:
        equipment.append('band')
    
    if 'cable' in name_lower:
        equipment.append('cable')
    
    if 'trx' in name_lower:
        equipment.append('trx')
    
    if 'box' in name_lower:
        equipment.append('box')
    
    if 'bench' in name_lower:
        equipment.append('bench')
    
    if 'miniband' in name_lower or 'mini band' in name_lower:
        equipment.append('miniband')
    
    if 'dowel' in name_lower or 'broomstick' in name_lower:
        equipment.append('dowel')
    
    if not equipment:
        equipment.append('bodyweight')  # Default
    
    return list(set(equipment))  # Remove duplicates

def estimate_difficulty(name: str, category: str) -> str:
    """Estimate difficulty level"""
    name_lower = name.lower()
    
    # Advanced indicators
    if any(word in name_lower for word in ['single-leg', 'single arm', 'pistol', 'one-arm', 'weighted', 'explosive', 'plyo', 'clapping']):
        return 'advanced'
    
    # Beginner indicators
    if any(word in name_lower for word in ['assisted', 'band-assisted', 'hands elevated', 'knees', 'beginner', 'partial']):
        return 'beginner'
    
    # Equipment-based
    if 'barbell' in name_lower:
        return 'intermediate'
    if 'dumbbell' in name_lower or 'kettlebell' in name_lower:
        return 'intermediate'
    
    # Category-based defaults
    if category == 'carry':
        return 'intermediate'
    if category == 'plyometric':
        return 'advanced'
    if category == 'mobility':
        return 'beginner'
    
    return 'intermediate'

def build_exercise_library(pn_csv_path: str, output_json_path: str):
    """Build complete exercise library from PN CSV + YouTube fallbacks"""
    
    exercises = []
    exercise_ids = set()
    
    # Load PN exercises
    print(f"Loading PN exercises from: {pn_csv_path}")
    with open(pn_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['Exercise Name'].strip()
            url = row['Video URL'].strip()
            
            if not name or not url:
                continue
            
            ex_id = normalize_exercise_name(name)
            # Ensure unique IDs
            original_id = ex_id
            counter = 1
            while ex_id in exercise_ids:
                ex_id = f"{original_id}_{counter}"
                counter += 1
            exercise_ids.add(ex_id)
            
            category, subcategory = classify_category(name)
            equipment = extract_equipment(name)
            difficulty = estimate_difficulty(name, category)
            
            exercise = {
                "id": ex_id,
                "name": name,
                "aliases": generate_aliases(name),
                "video_url": url,
                "video_source": "precision_nutrition",
                "category": category,
                "subcategory": subcategory,
                "equipment": equipment,
                "movement_pattern": category,  # Simplified
                "difficulty": difficulty,
                "muscles_primary": [],  # Could be enhanced later
                "muscles_secondary": [],
                "gravel_god_approved": True
            }
            
            exercises.append(exercise)
    
    # Add YouTube fallbacks
    print(f"Adding {len(YOUTUBE_FALLBACKS)} YouTube fallbacks...")
    for name, url in YOUTUBE_FALLBACKS.items():
        ex_id = normalize_exercise_name(name)
        # Ensure unique IDs
        original_id = ex_id
        counter = 1
        while ex_id in exercise_ids:
            ex_id = f"{original_id}_{counter}"
            counter += 1
        exercise_ids.add(ex_id)
        
        category, subcategory = classify_category(name)
        equipment = extract_equipment(name)
        difficulty = estimate_difficulty(name, category)
        
        exercise = {
            "id": ex_id,
            "name": name,
            "aliases": generate_aliases(name),
            "video_url": url,
            "video_source": "youtube",
            "category": category,
            "subcategory": subcategory,
            "equipment": equipment,
            "movement_pattern": category,
            "difficulty": difficulty,
            "muscles_primary": [],
            "muscles_secondary": [],
            "gravel_god_approved": True
        }
        
        exercises.append(exercise)
    
    # Create library structure
    library = {
        "metadata": {
            "version": "1.0",
            "total_exercises": len(exercises),
            "sources": {
                "precision_nutrition": len([e for e in exercises if e["video_source"] == "precision_nutrition"]),
                "youtube": len([e for e in exercises if e["video_source"] == "youtube"])
            },
            "categories": {}
        },
        "exercises": exercises
    }
    
    # Count by category
    for exercise in exercises:
        cat = exercise["category"]
        if cat not in library["metadata"]["categories"]:
            library["metadata"]["categories"][cat] = 0
        library["metadata"]["categories"][cat] += 1
    
    # Save JSON
    print(f"Saving library to: {output_json_path}")
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(library, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Library created: {len(exercises)} exercises")
    print(f"   Categories: {library['metadata']['categories']}")
    
    return library

if __name__ == "__main__":
    import sys
    
    pn_csv = sys.argv[1] if len(sys.argv) > 1 else "/Users/mattirowe/Downloads/pn_exercises_full.csv"
    output_json = sys.argv[2] if len(sys.argv) > 2 else "/Users/mattirowe/gravel-landing-page-project/races/generation_modules/exercise_video_library.json"
    
    library = build_exercise_library(pn_csv, output_json)
    print(f"\n✅ Exercise library built successfully!")

