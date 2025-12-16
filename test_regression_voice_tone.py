#!/usr/bin/env python3
"""
VOICE AND TONE REGRESSION TESTS
================================
Ensures all content adheres to Matti voice guidelines:
- Dry, matter-of-fact tone
- No theatrical language
- No motivational-speech energy
- Correct altitude vs. elevation usage

Exit codes:
    0 = All voice/tone tests passed
    1 = Voice/tone violations detected
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Tuple

# ============================================================================
# VOICE VIOLATION PATTERNS
# ============================================================================

THEATRICAL_PATTERNS = [
    r'\bterminal\s+(?:climb|exam|test|challenge)\b',
    r'\bexistential\s+(?:questions?|dilemma|journey)\b',
    r'\btransformation\s+disguised\s+as\b',
    r'\btransformative\s+(?:journey|experience|suffering)\b',
    r'\bcharacter-building\s+experience\b',
    r'\bultimate\s+test\b',
    r'\bbrutal\s+(?:suffering|test|challenge)\b',
    r'\bsavage\s+(?:course|climb|terrain)\b',
    r'\bmerciless\s+(?:gradient|climb|course)\b',
    r'\bsoul-crushing\b',
    r'\bspirit-breaking\b',
    r'\blegendary\s+(?:suffering|challenge|test)\b',
    r'\bepic\s+(?:journey|suffering|test)\b',
    r'\bmonumental\s+(?:achievement|suffering)\b',
    r'\bincredible\s+(?:suffering|challenge)\b',
    r'\bamazing\s+(?:suffering|journey)\b',
    r'\bunbelievable\s+(?:suffering|challenge)\b',
    r'\blife-changing\s+transformation\b',
]

MOTIVATIONAL_PATTERNS = [
    r'\bchampions?\s+(?:are\s+)?made\b',
    r'\bpush\s+through\s+the\s+pain\b',
    r'\bdiscover\s+what\s+you\'?re\s+truly\s+capable\s+of\b',
    r'\bunlock\s+your\s+potential\b',
    r'\breach\s+new\s+heights?\b',
    r'\bconquer\s+the\s+(?:course|climb|challenge)\b',
    r'\bembrace\s+the\s+(?:suffering|pain|challenge)\b',
    r'\bprove\s+to\s+yourself\b',
    r'\bdig\s+deep\b',
    r'\bfind\s+your\s+inner\s+(?:strength|warrior|champion)\b',
]

DRAMATIC_BUILDUP_PATTERNS = [
    r'\bwhere\s+(?:riders|athletes)\s+face\s+existential\b',
    r'\bthis\s+is\s+where\s+(?:champions|legends)\s+are\s+made\b',
    r'\bthe\s+moment\s+of\s+truth\b',
    r'\bthe\s+ultimate\s+challenge\s+awaits\b',
]

# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def check_text_for_violations(text: str, file_path: str) -> List[Tuple[str, str]]:
    """
    Check text for voice/tone violations.
    Returns list of (pattern_type, matched_text) tuples.
    """
    violations = []
    
    if not text:
        return violations
    
    # Check theatrical patterns
    for pattern in THEATRICAL_PATTERNS:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            violations.append(('theatrical', match.group()))
    
    # Check motivational patterns
    for pattern in MOTIVATIONAL_PATTERNS:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            violations.append(('motivational', match.group()))
    
    # Check dramatic buildup
    for pattern in DRAMATIC_BUILDUP_PATTERNS:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            violations.append(('dramatic_buildup', match.group()))
    
    return violations

def check_altitude_usage(text: str, race_data: dict) -> List[str]:
    """
    Check for incorrect altitude vs. elevation usage.
    Returns list of error messages.
    """
    errors = []
    
    # Get altitude rating
    altitude_score = race_data.get('gravel_god_rating', {}).get('altitude', 0)
    
    # If altitude score is 5/5, race should be at low altitude
    if altitude_score == 5:
        # Check for incorrect "high altitude" references
        if re.search(r'\bhigh\s+altitude\b', text, re.IGNORECASE):
            errors.append("Race scored 5/5 for altitude (low altitude) but contains 'high altitude' reference")
        
        # Check for altitude concerns when there shouldn't be (but allow "zero altitude concerns" or "no altitude concerns")
        if re.search(r'\baltitude\s+(?:challenge|issue|problem)\b', text, re.IGNORECASE):
            errors.append("Race scored 5/5 for altitude but mentions altitude challenges/issues/problems")
        # Check for "altitude concerns" but allow negations like "zero altitude concerns" or "no altitude concerns"
        if re.search(r'\baltitude\s+concerns?\b', text, re.IGNORECASE):
            # Check if it's negated
            if not re.search(r'\b(?:zero|no|without)\s+altitude\s+concerns?\b', text, re.IGNORECASE):
                errors.append("Race scored 5/5 for altitude but mentions altitude concerns (without negation)")
    
    # Check for confusion between elevation gain and altitude
    if re.search(r'\baltitude.*elevation\s+gain\b', text, re.IGNORECASE) or \
       re.search(r'\belevation\s+gain.*altitude\b', text, re.IGNORECASE):
        errors.append("Text may be confusing altitude (elevation above sea level) with elevation gain (total climbing)")
    
    return errors

def test_race_data_file(file_path: Path) -> List[str]:
    """
    Test a race data JSON file for voice/tone violations.
    Returns list of error messages.
    """
    errors = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return [f"Failed to parse {file_path}: {e}"]
    
    race = data.get('race', {})
    
    # Fields to check for voice violations
    text_fields = [
        ('ratings_breakdown', lambda r: [
            r.get('ratings_breakdown', {}).get(k, {}).get('explanation', '')
            for k in ['length', 'technicality', 'elevation', 'climate', 'altitude', 
                      'logistics', 'adventure', 'prestige', 'race_quality', 
                      'experience', 'community', 'field_depth', 'value', 'expenses']
        ]),
        ('history.origin_story', lambda r: [r.get('history', {}).get('origin_story', '')]),
        ('history.reputation', lambda r: [r.get('history', {}).get('reputation', '')]),
        ('course_description.character', lambda r: [r.get('course_description', {}).get('character', '')]),
        ('course_description.suffering_zones', lambda r: [
            zone.get('desc', '') 
            for zone in r.get('course_description', {}).get('suffering_zones', [])
        ]),
        ('biased_opinion.summary', lambda r: [r.get('biased_opinion', {}).get('summary', '')]),
        ('black_pill.reality', lambda r: [r.get('black_pill', {}).get('reality', '')]),
        ('final_verdict.should_you_race', lambda r: [r.get('final_verdict', {}).get('should_you_race', '')]),
        ('final_verdict.alternatives', lambda r: [r.get('final_verdict', {}).get('alternatives', '')]),
        ('tldr.should_race_if', lambda r: [r.get('tldr', {}).get('should_race_if', '')]),
        ('tldr.skip_if', lambda r: [r.get('tldr', {}).get('skip_if', '')]),
    ]
    
    # Check all text fields
    for field_name, get_texts in text_fields:
        texts = get_texts(race)
        for text in texts:
            if not text:
                continue
            
            violations = check_text_for_violations(text, str(file_path))
            for violation_type, matched_text in violations:
                errors.append(
                    f"{file_path.name} - {field_name}: {violation_type} violation: '{matched_text}'"
                )
            
            # Check altitude usage
            altitude_errors = check_altitude_usage(text, race)
            for error in altitude_errors:
                errors.append(f"{file_path.name} - {field_name}: {error}")
    
    return errors

def main():
    """Run all voice/tone regression tests."""
    data_dir = Path('data')
    
    if not data_dir.exists():
        print("ERROR: data/ directory not found")
        return 1
    
    all_errors = []
    
    # Test all race data files
    for json_file in data_dir.glob('*-data.json'):
        print(f"Testing {json_file.name}...")
        errors = test_race_data_file(json_file)
        all_errors.extend(errors)
    
    # Report results
    if all_errors:
        print("\n" + "="*70)
        print("VOICE/TONE VIOLATIONS DETECTED")
        print("="*70)
        for error in all_errors:
            print(f"  ❌ {error}")
        print("\n" + "="*70)
        print(f"Total violations: {len(all_errors)}")
        print("\nSee documentation/VOICE_AND_TONE_GUIDELINES.md for guidance.")
        return 1
    else:
        print("\n" + "="*70)
        print("✅ ALL VOICE/TONE TESTS PASSED")
        print("="*70)
        return 0

if __name__ == '__main__':
    sys.exit(main())

