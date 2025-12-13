# POSITIONING QUALITY TESTS
# Semi-automated checks for tier-appropriate positioning
# These tests ensure marketplace descriptions maintain strong positioning

import os
import re
from pathlib import Path

def find_descriptions():
    """Find all marketplace description HTML files"""
    base_dir = Path("races/Unbound Gravel 200")
    descriptions = []
    
    for plan_dir in sorted(base_dir.iterdir()):
        if plan_dir.is_dir():
            desc_file = plan_dir / "marketplace_description.html"
            if desc_file.exists():
                plan_name = plan_dir.name
                descriptions.append((plan_name, str(desc_file)))
    
    return descriptions

def extract_tier_level_from_filename(plan_name):
    """Extract tier and level from plan filename"""
    plan_lower = plan_name.lower()
    
    # Extract tier
    tier = None
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
    
    # Extract level
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

def test_no_repeated_phrases():
    """
    TEST: No identical phrases repeated within same description
    
    WHY: Sounds lazy/robotic, breaks flow
    EXAMPLE: "Everything here is calibrated..." twice = bad
    CRITICAL: "Life got in the way" appearing twice (opening + story) = bad
    """
    descriptions = find_descriptions()
    errors = []
    
    # Common phrases to check for repetition
    phrases_to_check = [
        'everything here is calibrated',
        'this plan delivers',
        'built for',
        'designed for',
        'race-day capacity',
        'life got in the way',  # Critical for SMR plans - should not repeat
    ]
    
    for plan_name, filepath in descriptions:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        for phrase in phrases_to_check:
            count = content.count(phrase)
            if count > 1:
                errors.append(
                    f"{plan_name}: Phrase '{phrase}' repeated {count} times "
                    f"(should appear once maximum)"
                )
    
    return errors

def test_save_my_race_variations_isolated():
    """
    TEST: Bidirectional isolation - SMR and regular plans use correct variations
    
    WHY: SMR is different product with different positioning (salvage/urgency vs performance)
    
    BIDIRECTIONAL CHECK:
    1. SMR plans MUST have SMR language (6 weeks, salvage, triage, don't defer)
    2. SMR plans MUST NOT have regular language (12-week, progressive overload, unlock gear)
    3. Regular plans MUST NOT have SMR language (emergency, 6 weeks, salvage)
    """
    descriptions = find_descriptions()
    errors = []
    
    # SMR-specific language (REQUIRED in SMR, FORBIDDEN in regular)
    # Note: "cramming" in regular plans (e.g., "cramming high-volume training") is different
    # from SMR "cram the training" - test checks for SMR-specific phrases
    smr_indicators = [
        '6 weeks',
        '6-week',
        'six weeks',
        'life got in the way',
        "don't defer",
        'salvage',
        'triage',
        'minimum viable',
        'sufficient preparation',
        'emergency',
        'cram the training',  # SMR-specific, not "cramming high-volume"
        'cram some training',  # SMR-specific
        'cram the work',  # SMR-specific
        'haven\'t been training'
    ]
    
    # Regular plan language (FORBIDDEN in SMR, OK in regular)
    regular_indicators = [
        '12-week',
        '12 week',
        'twelve week',
        'progressive overload',
        'unlock another gear',
        'your fitness will show up predictably',
        'shows up predictably',  # Regular plan confidence
        'structured progression',  # Regular plan language (long-term development)
        'systematic development',  # Regular plan language
        'performance arrives',
        'full race-distance simulation',  # No time for this in 6 weeks
        'weekly practice building competence',  # Implies many weeks
    ]
    
    for plan_name, filepath in descriptions:
        is_save_my_race = 'save_my_race' in plan_name.lower() or 'save my race' in plan_name.lower()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        if is_save_my_race:
            # SMR plan: MUST have SMR language, MUST NOT have regular language
            
            # Check for missing SMR language (6 weeks should be prominent)
            smr_found = any(indicator in content for indicator in smr_indicators)
            if not smr_found:
                errors.append(
                    f"{plan_name}: Save My Race plan missing SMR-specific language "
                    f"(should mention 6 weeks, salvage, triage, don't defer)"
                )
            
            # Check for forbidden regular language
            for indicator in regular_indicators:
                if indicator in content:
                    errors.append(
                        f"{plan_name}: Save My Race plan contains regular plan language '{indicator}'. "
                        f"SMR plans should use salvage/urgency positioning, not performance/progression."
                    )
        else:
            # Regular plan: MUST NOT have SMR language
            for indicator in smr_indicators:
                if indicator in content:
                    errors.append(
                        f"{plan_name}: Contains SMR language '{indicator}' but is NOT "
                        f"Save My Race plan (SMR language only for 6-week emergency plans)"
                    )
    
    return errors

def test_race_name_natural_references():
    """
    TEST: Race name uses natural language (not keyword stuffing)
    
    RULE: 
    - First mention: Full formal name
    - Subsequent: Shorthand ("Unbound", "the race", etc.)
    
    FAIL: 3+ mentions of full formal name (keyword stuffing)
    """
    descriptions = find_descriptions()
    errors = []
    
    race_name = "Unbound Gravel 200"
    
    for plan_name, filepath in descriptions:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count formal name mentions
        formal_mentions = content.count(race_name)
        
        if formal_mentions > 2:
            errors.append(
                f"{plan_name}: Full race name '{race_name}' appears "
                f"{formal_mentions} times (sounds like keyword stuffing). "
                f"Use shorthand after first mention ('Unbound', 'the race')."
            )
    
    return errors

def test_full_plan_designation_in_body():
    """
    TEST: Full plan designation (tier + level OR tier + masters) must appear in body copy
    
    WHY: Ensures reader identifies with THEIR SPECIFIC PLAN, not just tier
    EXAMPLE: "The Finisher Beginner plan..." or "The Finisher Masters plan..."
    
    CRITICAL: This is about self-identification. Reader should see:
    - "Finisher Beginner" (if that's their plan - non-Masters with level)
    - "Finisher Masters" (if that's their plan - Masters without level)
    - Not just "finisher" or "8-12 hours" generically
    
    PLAN STRUCTURE:
    - Non-Masters: tier + level (e.g., "Finisher Intermediate")
    - Masters: tier + masters (e.g., "Finisher Masters") - NO level needed
    """
    descriptions = find_descriptions()
    errors = []
    warnings = []
    
    for plan_name, filepath in descriptions:
        tier, level, is_masters = extract_tier_level_from_filename(plan_name)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove header/title (first 500 chars) to check body only
        body_content = content[500:].lower()
        
        # Build expected plan designation based on plan structure
        # Masters plans: tier + masters (no level)
        # Non-Masters plans: tier + level
        
        if is_masters and not level:
            # Masters without level (correct structure: "Finisher Masters")
            expected_designation = f"{tier} masters"
            if expected_designation in body_content:
                continue  # PASS - found "tier masters"
            else:
                errors.append(
                    f"{plan_name}: Full plan designation not found in body. "
                    f"Should mention '{expected_designation.title()}' (Masters plans use tier + masters, no level)"
                )
        elif is_masters and level:
            # Masters WITH level (unusual - might be old structure)
            # Accept either "tier level masters" or "tier masters"
            expected_full = f"{tier} {level} masters"
            expected_short = f"{tier} masters"
            if expected_full in body_content or expected_short in body_content:
                warnings.append(
                    f"{plan_name}: Has level in filename but Masters plans typically use tier only. "
                    f"Consider 'Finisher Masters' not 'Finisher Intermediate Masters'"
                )
                continue  # PASS with warning
            else:
                errors.append(
                    f"{plan_name}: Full plan designation not found. "
                    f"Should mention '{expected_short.title()}' (Masters plans use tier + masters)"
                )
        elif level and not is_masters:
            # Non-Masters with level (correct structure: "Finisher Intermediate")
            expected_designation = f"{tier} {level}"
            if expected_designation in body_content:
                continue  # PASS - found "tier level"
            else:
                # Check if at least tier is mentioned (downgraded to warning)
                if tier in body_content:
                    warnings.append(
                        f"{plan_name}: Tier mentioned but not full designation. "
                        f"Should mention '{expected_designation.title()}' (tier + level together)"
                    )
                else:
                    errors.append(
                        f"{plan_name}: Full plan designation not found. "
                        f"Should mention '{expected_designation.title()}'"
                    )
        else:
            # No level, no Masters (unusual structure)
            if tier in body_content:
                warnings.append(
                    f"{plan_name}: Only tier mentioned (unusual structure - no level or Masters flag)"
                )
            else:
                errors.append(
                    f"{plan_name}: Tier '{tier}' not mentioned in body"
                )
    
    return errors, warnings

def test_no_weak_verbs_in_stories():
    """
    TEST: Story justifications avoid generic/weak coach-speak verbs
    
    WHY: These verbs make copy sound generic, not distinctively Matti
    FORBIDDEN: "refines", "emphasizes", "delivers", "provides", 
               "helps", "allows", "enables"
    BETTER: "builds", "breaks", "creates", "requires", direct statements
    """
    descriptions = find_descriptions()
    errors = []
    
    weak_verbs = [
        'refines consistency',
        'emphasizes',
        'delivers precision',
        'provides structure',
        'helps you',
        'allows you to',
        'enables you to',
        'breaks through plateaus'  # cliché
    ]
    
    for plan_name, filepath in descriptions:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        # Check story section (approximate - between opening and features)
        # This is rough but catches most issues
        story_section = content[500:1500]  # Middle section typically story
        
        for weak_pattern in weak_verbs:
            if weak_pattern in story_section:
                errors.append(
                    f"{plan_name}: Story contains weak verb pattern '{weak_pattern}' "
                    f"(sounds generic, not Matti voice)"
                )
    
    return errors

def test_matti_voice_indicators():
    """
    TEST: Description includes distinctive Matti voice phrases
    
    WHY: Ensures voice consistency, not generic coach copy
    REQUIREMENT: Each description should have 1-2 distinctive Matti phrases
    
    Distinctive Matti phrases:
    - "predictably, not accidentally"
    - "when suffering" / "when you're getting rattled"
    - "race-day capacity, not training-day heroics"
    - "practiced protocols, not theory"
    - "race rewards [X], not [Y]"
    - "making this work around a life"
    """
    descriptions = find_descriptions()
    warnings = []
    
    matti_indicators = [
        'predictably, not accidentally',
        'predictably, not',  # Allow slight variation
        'when suffering',
        'when you\'re getting rattled',
        'when rattled',
        'race-day capacity',
        'training-day heroics',
        'practiced protocols',
        'not theory',
        'not just theory',
        'race rewards',
        'unbound rewards',
        'making this work around a life',
        'work around a life',
        'different engine',
        'this plan breaks that pattern',
        'breaks that pattern'
    ]
    
    for plan_name, filepath in descriptions:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        # Count how many Matti indicators present
        indicators_found = [ind for ind in matti_indicators if ind in content]
        
        if len(indicators_found) == 0:
            warnings.append(
                f"{plan_name}: No distinctive Matti phrases found "
                f"(copy may sound too generic - manual review recommended)"
            )
        elif len(indicators_found) == 1:
            # One is borderline - warning but not error
            warnings.append(
                f"{plan_name}: Only 1 Matti phrase found ('{indicators_found[0]}') "
                f"- consider adding more distinctive voice markers"
            )
        # 2+ indicators = good, no warning
    
    return warnings

def test_no_forbidden_jargon():
    """
    TEST: Descriptions don't contain jargon or false claims explicitly removed by user
    
    BUG FIXED: 2024-12-12
    ISSUE: G Spot, 6-2-7 breathing, GOAT Method appearing despite removal
    USER INSTRUCTION: "Don't mention G Spot - no one knows what that is"
    
    FALSE CLAIM FIXED: 2024-12-12
    ISSUE: "Four hours beats eight hours" - unrealistic claim
    USER INSTRUCTION: "I don't want to promise that training for 4 hours a week 
    makes you better than 8 hours a week that's not realistic"
    
    WHY FORBIDDEN:
    JARGON:
    - G Spot zone (88-92% FTP): Requires explanation, confuses buyers
    - 6-2-7 breathing: Too specific/nerdy, not compelling
    - GOAT Method: Proprietary but needs explanation
    - HRV protocols: Too technical for marketplace copy
    
    FALSE CLAIMS:
    - "4 hours beats 8 hours": Unrealistic - 4 structured hours don't beat 8 hours total
    
    These were replaced with:
    - 60-80g carbs/hour (trending, understandable)
    - Three-Act pacing (clear framework)
    - Heat adaptation (proven strategy)
    - Dress rehearsal ride (obvious benefit)
    - Reality-grounded alternatives: "You won't build the fitness of someone training 15 hours. But you'll build enough—if every workout counts."
    """
    descriptions = find_descriptions()
    errors = []
    
    # Jargon explicitly forbidden by user (2024-12-12)
    forbidden_jargon = [
        ('G Spot', 'Use "race pace" or "sustainable power" instead'),
        ('88-92% FTP', 'Mention this only if explaining race pace, not as feature'),
        ('6-2-7 breathing', 'Too nerdy - use "breathing technique" or "mental training"'),
        ('GOAT Method', 'Requires explanation - use specific protocols instead'),
        ('HRV protocol', 'Too technical - use "recovery monitoring" or "readiness data"'),
        ('HRV-guided', 'Too technical - use "recovery-based" or "data-guided"'),
    ]
    
    # False claims explicitly forbidden by user (2024-12-12)
    forbidden_claims = [
        ('four hours.*beats.*eight', 'Unrealistic - 4 structured hours don\'t beat 8 hours total'),
        ('4 hours.*beats.*8 hours', 'Unrealistic - 4 structured hours don\'t beat 8 hours total'),
        ('beats eight hours', 'Unrealistic claim - remove'),
        ('beats 8 hours', 'Unrealistic claim - remove'),
    ]
    
    for plan_name, filepath in descriptions:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for forbidden jargon
        for jargon, suggestion in forbidden_jargon:
            if jargon in content:
                errors.append(
                    f"{plan_name}: Contains forbidden jargon '{jargon}'. "
                    f"{suggestion}"
                )
        
        # Check for false claims (using regex for pattern matching)
        import re
        for pattern, suggestion in forbidden_claims:
            if re.search(pattern, content, re.IGNORECASE):
                errors.append(
                    f"{plan_name}: Contains '{pattern}'. {suggestion}"
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
    
    # Test 1: Full Plan Designation
    print("\nTest 1: Full Plan Designation in Body Copy")
    errors, warnings = test_full_plan_designation_in_body()
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
        print("  ✅ PASSED - All plans include full designation in body copy")
    
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
    
    # Test 5: No Repeated Phrases
    print("\nTest 5: No Repeated Phrases")
    errors = test_no_repeated_phrases()
    if errors:
        print("  ❌ FAILED")
        for error in errors:
            print(f"    {error}")
        all_errors.extend(errors)
    else:
        print("  ✅ PASSED - No repeated phrases found")
    
    # Test 6: Save My Race Variations Isolated
    print("\nTest 6: Save My Race Variations Isolated")
    errors = test_save_my_race_variations_isolated()
    if errors:
        print("  ❌ FAILED")
        for error in errors:
            print(f"    {error}")
        all_errors.extend(errors)
    else:
        print("  ✅ PASSED - Emergency language only in SMR plans")
    
    # Test 7: Race Name Natural References
    print("\nTest 7: Race Name Natural References")
    errors = test_race_name_natural_references()
    if errors:
        print("  ❌ FAILED")
        for error in errors:
            print(f"    {error}")
        all_errors.extend(errors)
    else:
        print("  ✅ PASSED - Race name used naturally (not keyword stuffing)")
    
    # Test 8: No Weak Verbs in Story Justifications
    print("\nTest 8: No Weak Verbs in Story Justifications")
    errors = test_no_weak_verbs_in_stories()
    if errors:
        print("  ❌ FAILED")
        for error in errors:
            print(f"    {error}")
        all_errors.extend(errors)
    else:
        print("  ✅ PASSED - No generic coach-speak verbs found")
    
    # Test 9: Matti Voice Indicators Present
    print("\nTest 9: Matti Voice Indicators Present")
    warnings = test_matti_voice_indicators()
    if warnings:
        print("  ⚠️  WARNINGS (Manual Review Recommended)")
        for warning in warnings:
            print(f"    {warning}")
        all_warnings.extend(warnings)
    else:
        print("  ✅ PASSED - Distinctive Matti phrases present (2+ per description)")
    
    # Test 10: No Forbidden Jargon/Claims
    print("\nTest 10: No Forbidden Jargon/Claims")
    errors = test_no_forbidden_jargon()
    if errors:
        print("  ❌ FAILED")
        for error in errors:
            print(f"    {error}")
        all_errors.extend(errors)
    else:
        print("  ✅ PASSED - No forbidden jargon or false claims found")
    
    # Summary
    print("\n" + "="*80)
    print("POSITIONING TEST SUMMARY")
    print("="*80)
    
    if all_errors:
        print(f"❌ {len(all_errors)} ERROR(S) - Fix required")
    else:
        print("✅ All positioning tests passed")
    
    if all_warnings:
        print(f"⚠️  {len(all_warnings)} WARNING(S) - Manual verification recommended")
    
    return len(all_errors) == 0

if __name__ == "__main__":
    success = run_positioning_tests()
    exit(0 if success else 1)
