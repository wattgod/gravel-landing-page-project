#!/usr/bin/env python3
"""
Regression tests for final_verdict.py module.

Run: python3 automation/test_final_verdict.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from automation.final_verdict import generate_final_verdict_html


# Sample test data matching expected schema
SAMPLE_DATA = {
    "race": {
        "display_name": "Mid South",
        "final_verdict": {
            "score": "82 / 100",
            "one_liner": "Where training meets chaos.",
            "should_you_race": "You should race this if you want to test yourself against unpredictable conditions and a supportive community.",
            "alternatives": "If you want similar vibes with less weather risk, consider SBT GRVL or Unbound."
        },
        "gravel_god_rating": {
            "tier_label": "TIER 1",
            "course_profile": 21,
            "biased_opinion": 28
        }
    }
}


def test_generates_valid_html():
    """Test that function returns valid HTML string."""
    html = generate_final_verdict_html(SAMPLE_DATA)
    assert isinstance(html, str), "Should return string"
    assert len(html) > 500, "Should return substantial HTML"
    print("✓ Generates valid HTML")


def test_contains_section_structure():
    """Test that HTML contains required section structure."""
    html = generate_final_verdict_html(SAMPLE_DATA)
    assert 'id="overall-score"' in html, "Missing section ID"
    assert 'gg-overall-section' in html, "Missing section class"
    print("✓ Contains section structure")


def test_contains_header_elements():
    """Test that HTML contains header elements."""
    html = generate_final_verdict_html(SAMPLE_DATA)
    assert 'Final verdict' in html, "Missing 'Final verdict' pill text"
    assert 'OVERALL SCORE' in html, "Missing section title"
    assert 'stop pretending this is objective' in html, "Missing kicker text"
    print("✓ Contains header elements")


def test_score_card_present():
    """Test that score card is present."""
    html = generate_final_verdict_html(SAMPLE_DATA)
    assert 'gg-overall-card' in html, "Missing score card"
    assert 'gg-overall-score-main' in html, "Missing main score element"
    assert '/100' in html, "Missing /100 denominator"
    print("✓ Score card present")


def test_score_displayed():
    """Test that score is displayed correctly."""
    html = generate_final_verdict_html(SAMPLE_DATA)
    assert '82' in html, "Missing score value"
    print("✓ Score displayed correctly")


def test_tier_badge_present():
    """Test that tier badge is present."""
    html = generate_final_verdict_html(SAMPLE_DATA)
    assert 'gg-overall-tier-badge' in html, "Missing tier badge"
    assert 'TIER 1' in html, "Missing tier label"
    print("✓ Tier badge present")


def test_race_name_displayed():
    """Test that race name is displayed."""
    html = generate_final_verdict_html(SAMPLE_DATA)
    assert 'Mid South' in html, "Missing race name"
    assert 'gg-overall-label' in html, "Missing label class"
    print("✓ Race name displayed")


def test_one_liner_rendered():
    """Test that one-liner is rendered."""
    html = generate_final_verdict_html(SAMPLE_DATA)
    assert 'training meets chaos' in html, "Missing one-liner"
    assert 'gg-overall-one-liner' in html, "Missing one-liner class"
    print("✓ One-liner rendered")


def test_breakdown_table():
    """Test that breakdown table is present."""
    html = generate_final_verdict_html(SAMPLE_DATA)
    assert 'gg-overall-breakdown-table' in html, "Missing breakdown table"
    assert 'Course profile' in html, "Missing course profile row"
    assert 'Editorial profile' in html, "Missing editorial profile row"
    assert '21 / 35' in html, "Missing course profile score"
    assert '28 / 35' in html, "Missing editorial profile score"
    print("✓ Breakdown table correct")


def test_should_you_race_section():
    """Test that 'Should You Race' section is rendered."""
    html = generate_final_verdict_html(SAMPLE_DATA)
    assert 'Should You Race This?' in html, "Missing Should You Race heading"
    assert 'unpredictable conditions' in html, "Missing should_you_race content"
    print("✓ 'Should You Race' section rendered")


def test_alternatives_section():
    """Test that alternatives section is rendered."""
    html = generate_final_verdict_html(SAMPLE_DATA)
    assert 'Alternatives' in html, "Missing Alternatives heading"
    assert 'SBT GRVL' in html, "Missing alternatives content"
    assert 'Unbound' in html, "Missing alternatives content"
    print("✓ Alternatives section rendered")


def test_inline_styles_present():
    """Test that inline styles are present."""
    html = generate_final_verdict_html(SAMPLE_DATA)
    assert '<style>' in html, "Missing style tag"
    assert '.gg-overall-section' in html, "Missing section styles"
    assert '#4ECDC4' in html, "Missing turquoise color"
    print("✓ Inline styles present")


def test_tier_styling():
    """Test that tier badge has correct styling."""
    html = generate_final_verdict_html(SAMPLE_DATA)
    assert 'rotate(45deg)' in html, "Missing rotation for tier badge"
    assert '#4ECDC4' in html, "Tier badge should be turquoise"
    print("✓ Tier styling correct")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_generates_valid_html,
        test_contains_section_structure,
        test_contains_header_elements,
        test_score_card_present,
        test_score_displayed,
        test_tier_badge_present,
        test_race_name_displayed,
        test_one_liner_rendered,
        test_breakdown_table,
        test_should_you_race_section,
        test_alternatives_section,
        test_inline_styles_present,
        test_tier_styling,
    ]
    
    passed = 0
    failed = 0
    
    print("\n" + "=" * 50)
    print("FINAL VERDICT MODULE TESTS")
    print("=" * 50 + "\n")
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: Unexpected error - {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    if failed == 0:
        print("\n✅ ALL TESTS PASSED")
    else:
        print(f"\n❌ {failed} TEST(S) FAILED")
        sys.exit(1)


if __name__ == '__main__':
    run_all_tests()
