#!/usr/bin/env python3
"""
Regression tests for biased_opinion.py module.

Run: python3 automation/test_biased_opinion.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from automation.biased_opinion import generate_biased_opinion_html


# Sample test data matching expected schema
SAMPLE_DATA = {
    "race": {
        "display_name": "Mid South",
        "ratings_breakdown": {
            "prestige": {"score": 4, "explanation": "Growing reputation in the gravel world."},
            "race_quality": {"score": 5, "explanation": "Excellent organization and execution."},
            "experience": {"score": 4, "explanation": "Memorable for the right reasons."},
            "community": {"score": 5, "explanation": "Oklahoma hospitality is legendary."},
            "field_depth": {"score": 3, "explanation": "Mix of pros and enthusiasts."},
            "value": {"score": 4, "explanation": "Good bang for your buck."},
            "expenses": {"score": 3, "explanation": "Travel costs add up."}
        },
        "biased_opinion": {
            "verdict": "A GRAVEL RITE OF PASSAGE",
            "quote": "You'll remember this one forever, for better or worse.",
            "summary": "The race that proves weather is the ultimate equalizer."
        }
    }
}


def test_generates_valid_html():
    """Test that function returns valid HTML string."""
    html = generate_biased_opinion_html(SAMPLE_DATA)
    assert isinstance(html, str), "Should return string"
    assert len(html) > 500, "Should return substantial HTML"
    print("✓ Generates valid HTML")


def test_contains_section_structure():
    """Test that HTML contains required section structure."""
    html = generate_biased_opinion_html(SAMPLE_DATA)
    assert 'id="biased-opinion"' in html, "Missing section ID"
    assert 'gg-ratings-section' in html, "Missing section class"
    assert 'gg-ratings-grid' in html, "Missing ratings grid"
    print("✓ Contains section structure")


def test_contains_header_elements():
    """Test that HTML contains header pill and heading."""
    html = generate_biased_opinion_html(SAMPLE_DATA)
    assert 'BIASED OPINION' in html, "Missing header text"
    assert 'A GRAVEL RITE OF PASSAGE' in html, "Missing verdict"
    assert 'gg-pill' in html, "Missing pill element"
    print("✓ Contains header elements")


def test_editorial_radar_present():
    """Test that editorial radar chart is present."""
    html = generate_biased_opinion_html(SAMPLE_DATA)
    assert 'Editorial Radar' in html, "Missing 'Editorial Radar' title"
    assert 'gg-course-radar-svg' in html, "Missing radar SVG"
    assert 'gg-radar-card' in html, "Missing radar card"
    print("✓ Editorial radar present")


def test_editorial_profile_card():
    """Test that editorial profile card is present."""
    html = generate_biased_opinion_html(SAMPLE_DATA)
    assert 'Editorial Profile' in html, "Missing profile title"
    assert 'gg-course-profile-card' in html, "Missing profile card"
    assert '/ 35' in html, "Missing raw score denominator"
    print("✓ Editorial profile card present")


def test_all_opinion_categories():
    """Test that all 7 opinion categories are rendered."""
    html = generate_biased_opinion_html(SAMPLE_DATA)
    categories = ['Prestige', 'Race Quality', 'Experience', 'Community', 'Field Depth', 'Value', 'Expenses']
    for cat in categories:
        assert cat in html, f"Missing category: {cat}"
    print("✓ All opinion categories present")


def test_raw_score_calculated():
    """Test that raw editorial score is calculated correctly."""
    html = generate_biased_opinion_html(SAMPLE_DATA)
    # Sum of scores: 4+5+4+5+3+4+3 = 28
    assert '28 / 35' in html, "Raw score should be 28/35"
    print("✓ Raw score calculated correctly")


def test_explanations_rendered():
    """Test that explanations are rendered."""
    html = generate_biased_opinion_html(SAMPLE_DATA)
    assert 'Growing reputation' in html, "Missing prestige explanation"
    assert 'Oklahoma hospitality' in html, "Missing community explanation"
    print("✓ Explanations rendered")


def test_quote_rendered():
    """Test that pull quote is rendered."""
    html = generate_biased_opinion_html(SAMPLE_DATA)
    assert 'gg-course-quote-big' in html, "Missing quote container"
    assert 'remember this one forever' in html, "Missing quote text"
    print("✓ Quote rendered")


def test_javascript_present():
    """Test that radar chart JavaScript is present."""
    html = generate_biased_opinion_html(SAMPLE_DATA)
    assert '<script>' in html, "Missing script tag"
    assert '#biased-opinion' in html, "Missing section selector in JS"
    assert 'gg-radar-data-fill' in html, "Missing data polygon class"
    print("✓ JavaScript present")


def test_race_name_in_radar():
    """Test that race name appears in radar card."""
    html = generate_biased_opinion_html(SAMPLE_DATA)
    assert 'Mid South' in html, "Missing race name"
    print("✓ Race name in radar")


def test_rating_bars_rendered():
    """Test that rating bars are rendered."""
    html = generate_biased_opinion_html(SAMPLE_DATA)
    assert 'gg-rating-bar' in html, "Missing rating bars"
    assert 'gg-rating-bar-fill' in html, "Missing rating bar fills"
    print("✓ Rating bars rendered")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_generates_valid_html,
        test_contains_section_structure,
        test_contains_header_elements,
        test_editorial_radar_present,
        test_editorial_profile_card,
        test_all_opinion_categories,
        test_raw_score_calculated,
        test_explanations_rendered,
        test_quote_rendered,
        test_javascript_present,
        test_race_name_in_radar,
        test_rating_bars_rendered,
    ]
    
    passed = 0
    failed = 0
    
    print("\n" + "=" * 50)
    print("BIASED OPINION MODULE TESTS")
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
