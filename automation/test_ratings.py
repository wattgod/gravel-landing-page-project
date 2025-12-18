#!/usr/bin/env python3
"""
Regression tests for ratings.py module.

Run: python3 automation/test_ratings.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from automation.ratings import generate_ratings_html


# Sample test data matching expected schema
SAMPLE_DATA = {
    "race": {
        "display_name": "Mid South",
        "ratings_breakdown": {
            "length": {"score": 4, "explanation": "103 miles is substantial but not extreme."},
            "technicality": {"score": 3, "explanation": "Red dirt gets technical when wet."},
            "elevation": {"score": 2, "explanation": "Rolling terrain, no major climbs."},
            "climate": {"score": 4, "explanation": "March weather is unpredictable."},
            "altitude": {"score": 1, "explanation": "Low altitude, no acclimatization needed."},
            "adventure": {"score": 3, "explanation": "Rural Oklahoma has its own character."},
            "logistics": {"score": 4, "explanation": "Well-organized event with good support."}
        },
        "gravel_god_rating": {
            "logistics": 4
        },
        "black_pill": {
            "quote": "The weather will test your resolve."
        },
        "final_verdict": {
            "one_liner": "Where training meets chaos."
        }
    }
}


def test_generates_valid_html():
    """Test that function returns valid HTML string."""
    html = generate_ratings_html(SAMPLE_DATA)
    assert isinstance(html, str), "Should return string"
    assert len(html) > 500, "Should return substantial HTML"
    print("✓ Generates valid HTML")


def test_contains_section_structure():
    """Test that HTML contains required section structure."""
    html = generate_ratings_html(SAMPLE_DATA)
    assert 'id="course-ratings"' in html, "Missing section ID"
    assert 'gg-ratings-section' in html, "Missing section class"
    assert 'gg-ratings-grid' in html, "Missing ratings grid"
    print("✓ Contains section structure")


def test_contains_header_elements():
    """Test that HTML contains header pill and heading."""
    html = generate_ratings_html(SAMPLE_DATA)
    assert 'WHAT THE COURSE IS LIKE' in html, "Missing header text"
    assert 'COURSE BREAKDOWN' in html, "Missing section title"
    assert 'gg-pill' in html, "Missing pill element"
    print("✓ Contains header elements")


def test_radar_chart_present():
    """Test that radar chart SVG is present."""
    html = generate_ratings_html(SAMPLE_DATA)
    assert 'gg-course-radar-svg' in html, "Missing radar SVG"
    assert 'viewBox="0 0 320 320"' in html, "Missing SVG viewBox"
    assert 'gg-radar-card' in html, "Missing radar card"
    print("✓ Radar chart present")


def test_profile_card_present():
    """Test that course profile card is present."""
    html = generate_ratings_html(SAMPLE_DATA)
    assert 'gg-course-profile-card' in html, "Missing profile card"
    assert 'Course Profile' in html, "Missing profile title"
    assert '/ 35' in html, "Missing raw score denominator"
    print("✓ Profile card present")


def test_rating_bars_rendered():
    """Test that rating bars are rendered for each category."""
    html = generate_ratings_html(SAMPLE_DATA)
    assert 'gg-rating-bar' in html, "Missing rating bars"
    assert 'gg-rating-bar-fill' in html, "Missing rating bar fills"
    assert 'width:' in html, "Missing width styles"
    print("✓ Rating bars rendered")


def test_all_categories_present():
    """Test that all 7 course categories are rendered."""
    html = generate_ratings_html(SAMPLE_DATA)
    categories = ['Length', 'Technicality', 'Elevation', 'Climate', 'Altitude', 'Adventure', 'Logistics']
    for cat in categories:
        assert cat in html, f"Missing category: {cat}"
    print("✓ All categories present")


def test_explanations_rendered():
    """Test that explanations are rendered."""
    html = generate_ratings_html(SAMPLE_DATA)
    assert '103 miles is substantial' in html, "Missing length explanation"
    assert 'Red dirt gets technical' in html, "Missing technicality explanation"
    print("✓ Explanations rendered")


def test_raw_score_calculated():
    """Test that raw course score is calculated correctly."""
    html = generate_ratings_html(SAMPLE_DATA)
    # Sum of scores: 4+3+2+4+1+3+4 = 21
    assert '21 / 35' in html, "Raw score should be 21/35"
    print("✓ Raw score calculated correctly")


def test_javascript_present():
    """Test that radar chart JavaScript is present."""
    html = generate_ratings_html(SAMPLE_DATA)
    assert '<script>' in html, "Missing script tag"
    assert 'document.querySelector' in html, "Missing DOM query"
    assert 'gg-radar-data-fill' in html, "Missing data polygon class"
    print("✓ JavaScript present")


def test_quote_rendered():
    """Test that pull quote is rendered."""
    html = generate_ratings_html(SAMPLE_DATA)
    assert 'gg-course-quote-big' in html, "Missing quote container"
    # Should use black_pill quote
    assert 'weather will test' in html, "Missing quote text"
    print("✓ Quote rendered")


def test_race_name_in_radar():
    """Test that race name appears in radar card."""
    html = generate_ratings_html(SAMPLE_DATA)
    assert 'Mid South' in html, "Missing race name"
    assert 'gg-radar-pill' in html, "Missing radar pill"
    print("✓ Race name in radar")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_generates_valid_html,
        test_contains_section_structure,
        test_contains_header_elements,
        test_radar_chart_present,
        test_profile_card_present,
        test_rating_bars_rendered,
        test_all_categories_present,
        test_explanations_rendered,
        test_raw_score_calculated,
        test_javascript_present,
        test_quote_rendered,
        test_race_name_in_radar,
    ]
    
    passed = 0
    failed = 0
    
    print("\n" + "=" * 50)
    print("RATINGS MODULE TESTS")
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
