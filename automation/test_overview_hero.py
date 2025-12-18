#!/usr/bin/env python3
"""
Regression tests for overview_hero.py module.

Run: python3 automation/test_overview_hero.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from automation.overview_hero import generate_overview_hero_html


# Sample test data matching expected schema
SAMPLE_DATA = {
    "race": {
        "display_name": "Mid South",
        "tagline": "Where the prairie tests your preparation.",
        "vitals": {
            "distance_mi": 103
        },
        "course_description": {
            "character": "Red dirt chaos and unpredictable weather"
        }
    }
}


def test_generates_valid_html():
    """Test that function returns valid HTML string."""
    html = generate_overview_hero_html(SAMPLE_DATA)
    assert isinstance(html, str), "Should return string"
    assert len(html) > 100, "Should return substantial HTML"
    print("✓ Generates valid HTML")


def test_contains_section_structure():
    """Test that HTML contains required section structure."""
    html = generate_overview_hero_html(SAMPLE_DATA)
    assert 'gg-overview-hero-v2' in html, "Missing section class"
    assert '<section' in html, "Missing section element"
    print("✓ Contains section structure")


def test_race_guide_badge_present():
    """Test that Race Guide badge is present."""
    html = generate_overview_hero_html(SAMPLE_DATA)
    assert 'gg-overview-badge' in html, "Missing badge container"
    assert 'Race Guide' in html, "Missing 'Race Guide' text"
    print("✓ Race Guide badge present")


def test_race_name_uppercase():
    """Test that race name is rendered in uppercase."""
    html = generate_overview_hero_html(SAMPLE_DATA)
    assert 'MID SOUTH' in html, "Race name should be uppercase"
    print("✓ Race name uppercase")


def test_title_includes_guide_text():
    """Test that title includes 'OVERVIEW & TRAINING GUIDE'."""
    html = generate_overview_hero_html(SAMPLE_DATA)
    assert 'OVERVIEW & TRAINING GUIDE' in html, "Missing guide text in title"
    print("✓ Title includes guide text")


def test_tagline_rendered():
    """Test that tagline is rendered."""
    html = generate_overview_hero_html(SAMPLE_DATA)
    assert 'prairie tests your preparation' in html, "Missing tagline"
    print("✓ Tagline rendered")


def test_body_includes_distance():
    """Test that body text includes distance."""
    html = generate_overview_hero_html(SAMPLE_DATA)
    assert '103 miles' in html, "Missing distance in body"
    print("✓ Body includes distance")


def test_body_includes_character():
    """Test that body text includes course character."""
    html = generate_overview_hero_html(SAMPLE_DATA)
    assert 'red dirt chaos' in html.lower(), "Missing course character in body"
    print("✓ Body includes course character")


def test_correct_css_classes():
    """Test that correct CSS classes are present."""
    html = generate_overview_hero_html(SAMPLE_DATA)
    assert 'gg-overview-title-v2' in html, "Missing title class"
    assert 'gg-overview-lede-v2' in html, "Missing lede class"
    assert 'gg-overview-body-v2' in html, "Missing body class"
    print("✓ Correct CSS classes present")


def test_no_template_placeholders():
    """Test that no template placeholders remain."""
    html = generate_overview_hero_html(SAMPLE_DATA)
    # f-strings use { } so we shouldn't have unresolved {var} patterns
    assert '{race' not in html, "Unresolved template placeholder"
    assert '{display' not in html, "Unresolved template placeholder"
    print("✓ No template placeholders")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_generates_valid_html,
        test_contains_section_structure,
        test_race_guide_badge_present,
        test_race_name_uppercase,
        test_title_includes_guide_text,
        test_tagline_rendered,
        test_body_includes_distance,
        test_body_includes_character,
        test_correct_css_classes,
        test_no_template_placeholders,
    ]
    
    passed = 0
    failed = 0
    
    print("\n" + "=" * 50)
    print("OVERVIEW HERO MODULE TESTS")
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
