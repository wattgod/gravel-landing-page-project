#!/usr/bin/env python3
"""
REGRESSION TEST: POSITIONING QUALITY
Semi-automated checks for tier-appropriate positioning
"""

import os
import re
from pathlib import Path
from collections import defaultdict

DESC_DIR = "races/Unbound Gravel 200"

def find_descriptions():
    """Find all marketplace_description.html files"""
    descriptions = []
    for root, dirs, files in os.walk(DESC_DIR):
        if "marketplace_description.html" in files:
            plan_name = os.path.basename(root)
            descriptions.append((plan_name, os.path.join(root, "marketplace_description.html")))
    return sorted(descriptions)

def extract_tier_level_from_filename(plan_name):
    """Extract tier and level from plan filename"""
    # Examples: "1. Ayahuasca Beginner (12 weeks)", "5. Finisher Beginner (12 weeks)"
    plan_lower = plan_name.lower()
    
    # Tier
    if 'ayahuasca' in plan_lower:
        tier = 'ayahuasca'
    elif 'finisher' in plan_lower:
        tier = 'finisher'
    elif 'compete' in plan_lower:
        tier = 'compete'
    elif 'podium' in plan_lower:
        tier = 'podium'
    else:
        tier = 'unknown'
    
    # Level
    if 'beginner' in plan_lower:
        level = 'beginner'
    elif 'intermediate' in plan_lower:
        level = 'intermediate'
    elif 'advanced' in plan_lower:
        level = 'advanced'
    elif 'elite' in plan_lower or 'goat' in plan_lower:
        level = 'elite'
    elif 'save my race' in plan_lower or 'save_my_race' in plan_lower:
        level = 'save my race'
    else:
        level = None
    
    # Masters flag
    is_masters = 'masters' in plan_lower
    
    return tier, level, is_masters

def test_tier_mentioned_in_body():
    """
    TEST: Tier name must appear at least once in body copy (not just header)
    
    WHY: Ensures copy maintains tier-specific positioning throughout
    EXAMPLE: "The Finisher Beginner plan..." or "At 8-12 hours per week..."
    """
    descriptions = find_descriptions()
    errors = []
    
    tier_keywords = {
        'ayahuasca': ['ayahuasca', '0-5 hours', '4 hours'],
        'finisher': ['finisher', '8-12 hours'],
        'compete': ['compete', '12-18 hours'],
        'podium': ['podium', '18+ hours', '18 hours']
    }
    
    for plan_name, filepath in descriptions:
        tier, level, is_masters = extract_tier_level_from_filename(plan_name)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove header/title (first 500 chars) to check body only
        body_content = content[500:].lower()
        
        # Check if tier is mentioned
        tier_found = any(keyword in body_content for keyword in tier_keywords.get(tier, []))
        
        if not tier_found:
            errors.append(
                f"{plan_name}: Tier '{tier}' not mentioned in body copy "
                f"(should mention 'finisher', '8-12 hours', etc.)"
            )
    
    return errors

def test_race_name_frequency():
    """
    TEST: Race name must appear 2-3 times in description
    
    WHY: Ensures race-specific positioning (not generic)
    EXAMPLE: "Unbound Gravel 200" should appear multiple times
    """
    descriptions = find_descriptions()
    errors = []
    warnings = []
    
    # Extract race name from directory path
    # Assumes format: "races/Unbound Gravel 200/plan_name/"
    race_name = "Unbound Gravel 200"  # Could extract from path
    
    for plan_name, filepath in descriptions:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count mentions of race name (case insensitive)
        mentions = content.lower().count(race_name.lower())
        
        if mentions < 2:
            errors.append(
                f"{plan_name}: Race name mentioned only {mentions} time(s) "
                f"(should be 2-3 for race-specific positioning)"
            )
        elif mentions > 4:
            warnings.append(
                f"{plan_name}: Race name mentioned {mentions} times "
                f"(might be repetitive, verify manually)"
            )
    
    return errors, warnings

def test_beat_contrast_patterns():
    """
    TEST: Opening should contain beat/contrast psychology patterns
    
    WHY: Ensures Sultanic positioning (not generic coach-speak)
    PATTERNS: "Most...", "You...", contrast words
    
    NOTE: This is a SOFT CHECK - requires manual verification
    """
    descriptions = find_descriptions()
    warnings = []
    
    # Beat indicators (what others do wrong)
    beat_patterns = [
        r'most (people|riders|athletes|plans)',
        r'generic plans',
        r'traditional training',
        r'random(ly)?'
    ]
    
    # Contrast indicators (how this is different)
    contrast_patterns = [
        r'this plan',
        r'this (breaks|fixes|delivers)',
        r'not (just|merely|simply)',
        r'instead'
    ]
    
    for plan_name, filepath in descriptions:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract opening (first 500 chars)
        opening = content[:500].lower()
        
        # Check for beat
        has_beat = any(re.search(pattern, opening) for pattern in beat_patterns)
        
        # Check for contrast
        has_contrast = any(re.search(pattern, opening) for pattern in contrast_patterns)
        
        if not has_beat and not has_contrast:
            warnings.append(
                f"{plan_name}: Opening may lack beat/contrast psychology "
                f"(manual verification recommended)"
            )
    
    return warnings

def test_generic_coach_speak():
    """
    TEST: Forbid generic coach-speak phrases
    
    WHY: Maintains Matti voice (direct, reality-grounded)
    FORBIDDEN: "Unlock your potential", "train smarter", etc.
    """
    descriptions = find_descriptions()
    errors = []
    
    forbidden_phrases = [
        'unlock your potential',
        'train smarter not harder',
        'take your training to the next level',
        'are you ready to',
        'transform your',
        'achieve your dreams',
        'reach your goals',
        'become the athlete you',
        'unleash your'
    ]
    
    for plan_name, filepath in descriptions:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        for phrase in forbidden_phrases:
            if phrase in content:
                errors.append(
                    f"{plan_name}: Contains generic coach-speak: '{phrase}'"
                )
    
    return errors

def run_positioning_tests():
    """Run all positioning quality tests"""
    print("\n" + "="*80)
    print("POSITIONING QUALITY TESTS")
    print("Semi-automated checks for tier-appropriate positioning")
    print("="*80)
    
    all_errors = []
    all_warnings = []
    
    # Test 1: Tier Mentions
    print("\nTest 1: Tier Mentioned in Body Copy")
    errors = test_tier_mentioned_in_body()
    if errors:
        print("  ❌ FAILED")
        for error in errors:
            print(f"    {error}")
        all_errors.extend(errors)
    else:
        print("  ✅ PASSED - All plans mention tier in body copy")
    
    # Test 2: Race Name Frequency
    print("\nTest 2: Race Name Frequency")
    errors, warnings = test_race_name_frequency()
    if errors:
        print("  ❌ FAILED")
        for error in errors:
            print(f"    {error}")
        all_errors.extend(errors)
    elif warnings:
        print("  ⚠️  WARNINGS")
        for warning in warnings:
            print(f"    {warning}")
        all_warnings.extend(warnings)
    else:
        print("  ✅ PASSED - All plans mention race name 2-3 times")
    
    # Test 3: Beat/Contrast Patterns (Soft Check)
    print("\nTest 3: Beat/Contrast Psychology (Soft Check)")
    warnings = test_beat_contrast_patterns()
    if warnings:
        print("  ⚠️  WARNINGS (Manual Verification Recommended)")
        for warning in warnings:
            print(f"    {warning}")
        all_warnings.extend(warnings)
    else:
        print("  ✅ PASSED - All openings show beat/contrast patterns")
    
    # Test 4: Generic Coach-Speak
    print("\nTest 4: No Generic Coach-Speak")
    errors = test_generic_coach_speak()
    if errors:
        print("  ❌ FAILED")
        for error in errors:
            print(f"    {error}")
        all_errors.extend(errors)
    else:
        print("  ✅ PASSED - No forbidden generic phrases found")
    
    # Summary
    print("\n" + "="*80)
    print("POSITIONING TEST SUMMARY")
    print("="*80)
    
    if all_errors:
        print(f"❌ {len(all_errors)} ERROR(S) - Fix required")
        return False
    elif all_warnings:
        print(f"⚠️  {len(all_warnings)} WARNING(S) - Manual review recommended")
        print("Positioning may need refinement, but not blocking")
        return True
    else:
        print("✅ ALL POSITIONING TESTS PASSED")
        return True

if __name__ == "__main__":
    success = run_positioning_tests()
    exit(0 if success else 1)
