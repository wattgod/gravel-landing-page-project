#!/usr/bin/env python3
"""
Validate race data schema before generation.
"""

import json
import sys
from typing import Dict, Any, List


def validate_race_data(data: Dict) -> List[str]:
    """Validate race data schema completeness."""
    errors = []
    
    required_fields = [
        'race.name',
        'race.slug',
        'race.display_name',
        'race.tagline',
        'race.vitals',
        'race.gravel_god_rating',
        'race.ratings_breakdown',
        'race.training_plans'
    ]
    
    for field_path in required_fields:
        parts = field_path.split('.')
        current = data
        for part in parts:
            if part not in current:
                errors.append(f"Missing required field: {field_path}")
                break
            current = current[part]
    
    # Validate TrainingPeaks plan count
    if 'race' in data and 'training_plans' in data['race']:
        expected_count = data['race']['training_plans'].get('total_count', 0)
        actual_count = len(data['race']['training_plans'].get('plans', []))
        if expected_count != actual_count:
            errors.append(f"Plan count mismatch: expected {expected_count}, got {actual_count}")
    
    # Validate TP URLs
    if 'race' in data and 'training_plans' in data['race']:
        for plan in data['race']['training_plans'].get('plans', []):
            if not plan.get('tp_id') or not plan.get('tp_slug'):
                tier = plan.get('tier', 'Unknown')
                level = plan.get('level', 'Unknown')
                errors.append(f"Missing TP ID or slug for {tier} {level}")
    
    # Validate ratings breakdown has all 7 categories
    if 'race' in data and 'ratings_breakdown' in data['race']:
        required_ratings = ['prestige', 'length', 'technicality', 'elevation', 'climate', 'altitude', 'adventure']
        ratings = data['race']['ratings_breakdown']
        for rating in required_ratings:
            if rating not in ratings:
                errors.append(f"Missing rating category: {rating}")
            elif 'score' not in ratings[rating] or 'explanation' not in ratings[rating]:
                errors.append(f"Rating category '{rating}' missing score or explanation")
    
    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_race_data.py <race_data.json>")
        sys.exit(1)
    
    json_path = sys.argv[1]
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {json_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}")
        sys.exit(1)
    
    errors = validate_race_data(data)
    
    if errors:
        print("VALIDATION FAILED:")
        for error in errors:
            print(f"  ✗ {error}")
        sys.exit(1)
    else:
        print("✓ Valid")
        sys.exit(0)


if __name__ == '__main__':
    main()


