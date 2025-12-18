#!/usr/bin/env python3
"""
Precision Nutrition Exercise Library Mapper
Maps exercises from strength templates to PN library video URLs
"""

import re
from pathlib import Path
from typing import Dict, Optional

# Exercise name normalization patterns
EXERCISE_ALIASES = {
    # Squat variations
    "Split Squat": ["Split Squat", "Bulgarian Split Squat", "Lateral Lunge"],
    "Goblet Squat": ["Goblet Squat", "Goblet Split Squat"],
    "Bulgarian Split Squat": ["Bulgarian Split Squat", "BSS", "Split Squat"],
    "Front Squat": ["Front Squat"],
    "Jump Squat": ["Jump Squat", "Squat Jump"],
    "Single-Leg Squat to Box": ["Single-Leg Squat to Box", "Pistol Squat"],
    "Split Squat Jump": ["Split Squat Jump"],
    
    # Hinge variations
    "Hip Hinge": ["Hip Hinge", "Hip Hinge w/ Dowel", "Good Morning"],
    "KB/DB RDL": ["KB/DB RDL", "RDL", "Romanian Deadlift", "Single-Leg RDL"],
    "Trap Bar Deadlift": ["Trap Bar Deadlift", "Trap Bar DL"],
    "KB/DB Deadlift": ["KB/DB Deadlift", "Deadlift"],
    "Single-Leg RDL": ["Single-Leg RDL", "SL RDL"],
    "Single-Leg DL to Hop": ["Single-Leg DL to Hop"],
    
    # Push variations
    "Push-Up": ["Push-Up", "Push-Up (floor)", "Pushup"],
    "Incline Push-Up": ["Incline Push-Up", "Incline Pushup", "Push-Up (hands elevated)"],
    "Push-Up + Shoulder Tap": ["Push-Up + Shoulder Tap", "Push-Up Shoulder Tap"],
    "Plyo Push-Up": ["Plyo Push-Up", "Plyometric Push-Up"],
    "DB Bench Press": ["DB Bench Press", "Dumbbell Bench Press"],
    "DB Floor Press": ["DB Floor Press", "Floor Press"],
    "Incline DB Press": ["Incline DB Press", "Incline Dumbbell Press"],
    "Med Ball Chest Pass": ["Med Ball Chest Pass", "Medicine Ball Chest Pass"],
    
    # Pull variations
    "Inverted Row": ["Inverted Row", "Bodyweight Row"],
    "Band Row": ["Band Row", "Resistance Band Row"],
    "Bent-Over DB Row": ["Bent-Over DB Row", "Bent-Over Dumbbell Row"],
    "Single-Arm DB Row": ["Single-Arm DB Row", "Single-Arm Dumbbell Row"],
    "TRX Row": ["TRX Row", "Suspension Row"],
    "Pull-Up": ["Pull-Up", "Pullup", "Chin-Up"],
    
    # Core variations
    "Dead Bug": ["Dead Bug", "Deadbug"],
    "Weighted Dead Bug": ["Weighted Dead Bug"],
    "Hollow Body Hold": ["Hollow Body Hold", "Hollow Hold"],
    "Hollow Body Rock": ["Hollow Body Rock"],
    "Plank": ["Plank"],
    "Ab Wheel Rollout": ["Ab Wheel Rollout", "Ab Wheel"],
    "Bird Dog": ["Bird Dog", "Birddog"],
    "Side Plank": ["Side Plank"],
    "Side Plank w/ Hip Dip": ["Side Plank w/ Hip Dip", "Side Plank Hip Dip"],
    "Pallof Press": ["Pallof Press"],
    "Band Chop": ["Band Chop"],
    "Med Ball Rotational Throw": ["Med Ball Rotational Throw", "Medicine Ball Rotational Throw"],
    "Russian Twist": ["Russian Twist"],
    
    # Carry variations
    "Farmer Carry": ["Farmer Carry", "Farmer's Walk"],
    "Suitcase Carry": ["Suitcase Carry"],
    "Suitcase Deadlift": ["Suitcase Deadlift"],
    
    # Glute variations
    "Glute Bridge": ["Glute Bridge", "Hip Bridge"],
    "Single-Leg Glute Bridge": ["Single-Leg Glute Bridge", "Single Leg Hip Bridge"],
    
    # Power/plyometric
    "Box Jump": ["Box Jump"],
    "Broad Jump": ["Broad Jump"],
    "KB Swing": ["KB Swing", "Kettlebell Swing"],
    "Med Ball Slam": ["Med Ball Slam", "Medicine Ball Slam"],
    
    # Accessory
    "Band Pull-Apart": ["Band Pull-Apart", "Band Pull Apart"],
    "Good Morning": ["Good Morning"],
}

def normalize_exercise_name(exercise_name: str) -> str:
    """
    Normalize exercise name for matching
    
    Removes:
    - Parenthetical notes: "(bodyweight)", "(light DB/KB)", etc.
    - Variations: "w/ Dowel", "hands elevated", etc.
    - Extra whitespace
    """
    # Remove parenthetical notes
    normalized = re.sub(r'\s*\([^)]+\)', '', exercise_name)
    
    # Remove common variation markers
    normalized = re.sub(r'\s*w/\s*[^─\n]+', '', normalized)
    normalized = re.sub(r'\s*\(hands[^)]*\)', '', normalized)
    
    # Clean whitespace
    normalized = ' '.join(normalized.split())
    
    return normalized.strip()

def find_pn_exercise_match(exercise_name: str, pn_library: Dict[str, str]) -> Optional[str]:
    """
    Find matching exercise in PN library
    
    Args:
        exercise_name: Exercise name from template
        pn_library: Dict mapping PN exercise names to video URLs
    
    Returns:
        PN video URL if match found, None otherwise
    """
    normalized = normalize_exercise_name(exercise_name)
    
    # Direct match
    if normalized in pn_library:
        return pn_library[normalized]
    
    # Check aliases
    for canonical_name, aliases in EXERCISE_ALIASES.items():
        if normalized in aliases or any(alias.lower() in normalized.lower() for alias in aliases):
            if canonical_name in pn_library:
                return pn_library[canonical_name]
    
    # Fuzzy match - check if any PN exercise name contains key words
    normalized_words = set(normalized.lower().split())
    for pn_exercise, url in pn_library.items():
        pn_words = set(pn_exercise.lower().split())
        # If 2+ words match, consider it a match
        if len(normalized_words & pn_words) >= 2:
            return url
    
    return None

def load_pn_library(library_path: str) -> Dict[str, str]:
    """
    Load PN exercise library from spreadsheet/CSV
    
    Expected format:
    - CSV or Excel file
    - Columns: Exercise Name, Video URL (or similar)
    
    Returns:
        Dict mapping exercise names to video URLs
    """
    import csv
    
    pn_library = {}
    
    # Try CSV first
    if library_path.endswith('.csv'):
        with open(library_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Try common column names
                ex_name = row.get('Exercise Name') or row.get('Exercise') or row.get('Name')
                url = row.get('Video URL') or row.get('URL') or row.get('Link')
                
                if ex_name and url:
                    pn_library[ex_name.strip()] = url.strip()
    
    # TODO: Add Excel support if needed
    # elif library_path.endswith(('.xlsx', '.xls')):
    #     import pandas as pd
    #     df = pd.read_excel(library_path)
    #     ...
    
    return pn_library

def replace_youtube_urls_in_template(template_text: str, pn_library: Dict[str, str]) -> str:
    """
    Replace YouTube URLs with PN library URLs in template text
    
    Args:
        template_text: Template description text
        pn_library: Dict mapping exercise names to PN video URLs
    
    Returns:
        Updated template text with PN URLs
    """
    # Pattern: Exercise name followed by URL on next line
    pattern = r'([A-Z][^→\n]+?)\s*─\s*[^\n]*\n\s*→\s*(https://www\.youtube\.com/watch\?v=[^\s\n]+)'
    
    def replace_match(match):
        exercise_line = match.group(1).strip()
        youtube_url = match.group(2)
        
        # Extract exercise name (remove parenthetical notes)
        exercise_name = re.sub(r'\s*\([^)]+\)', '', exercise_line).strip()
        
        # Find PN match
        pn_url = find_pn_exercise_match(exercise_name, pn_library)
        
        if pn_url:
            # Replace with PN URL
            return f"{exercise_line} ─ [same reps/sets]\n     → {pn_url}"
        else:
            # Keep YouTube URL but add comment
            return f"{exercise_line} ─ [same reps/sets]\n     → {youtube_url}  # TODO: Find PN equivalent"
    
    return re.sub(pattern, replace_match, template_text)

if __name__ == "__main__":
    print("PN Exercise Library Mapper")
    print("=" * 70)
    print("\nThis script maps exercises from strength templates to PN library videos.")
    print("\nUsage:")
    print("  1. Download PN exercise library spreadsheet")
    print("  2. Save as CSV or provide path to library file")
    print("  3. Run: python pn_exercise_mapper.py <library_file> <template_file>")
    print("\nExample:")
    print("  python pn_exercise_mapper.py pn_library.csv MASTER_TEMPLATES_V2.md")

