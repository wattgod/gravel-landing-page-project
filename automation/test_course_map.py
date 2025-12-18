#!/usr/bin/env python3
"""
Regression tests for course_map.py module.

Run: python3 automation/test_course_map.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from automation.course_map import generate_course_map_html


# Sample test data matching expected schema
SAMPLE_DATA = {
    "race": {
        "vitals": {
            "location": "Stillwater, Oklahoma",
            "distance_mi": 103
        },
        "course_description": {
            "ridewithgps_id": "12345678",
            "ridewithgps_name": "Mid South 2025",
            "suffering_zones": [
                {
                    "mile": 15,
                    "label": "Red Dirt Reckoning",
                    "desc": "First taste of Oklahoma clay.",
                    "terrain_detail": "Loose gravel over hardpack",
                    "named_section": "The Gauntlet",
                    "weather_note": "Gets greasy when wet"
                },
                {
                    "mile": 45,
                    "label": "Crosswind Corridor",
                    "desc": "Exposed prairie with relentless wind.",
                    "citation": "2023 race reports"
                },
                {
                    "mile": 78,
                    "label": "The Grind",
                    "desc": "Where fatigue meets climbing."
                }
            ]
        }
    }
}


def test_generates_valid_html():
    """Test that function returns valid HTML string."""
    html = generate_course_map_html(SAMPLE_DATA)
    assert isinstance(html, str), "Should return string"
    assert len(html) > 500, "Should return substantial HTML"
    print("✓ Generates valid HTML")


def test_contains_section_structure():
    """Test that HTML contains required section structure."""
    html = generate_course_map_html(SAMPLE_DATA)
    assert 'id="course-map"' in html, "Missing section ID"
    assert 'gg-route-section' in html, "Missing section class"
    assert 'gg-route-card' in html, "Missing route card"
    print("✓ Contains section structure")


def test_contains_header_elements():
    """Test that HTML contains header elements."""
    html = generate_course_map_html(SAMPLE_DATA)
    assert 'Course Map' in html, "Missing Course Map pill"
    assert 'STILLWATER' in html, "Missing location in title"
    assert '103 MILES' in html, "Missing distance in title"
    print("✓ Contains header elements")


def test_rwgps_embed_present():
    """Test that RideWithGPS embed is present."""
    html = generate_course_map_html(SAMPLE_DATA)
    assert 'ridewithgps.com/embeds' in html, "Missing RWGPS embed URL"
    assert '12345678' in html, "Missing RWGPS route ID"
    assert 'Mid South 2025' in html, "Missing RWGPS route name"
    assert 'iframe' in html, "Missing iframe element"
    print("✓ RWGPS embed present")


def test_suffering_zones_rendered():
    """Test that suffering zones are rendered."""
    html = generate_course_map_html(SAMPLE_DATA)
    assert 'gg-suffering-zones' in html, "Missing suffering zones container"
    assert 'gg-zone-card' in html, "Missing zone cards"
    assert 'Mile 15' in html, "Missing mile marker"
    assert 'Mile 45' in html, "Missing mile marker"
    assert 'Mile 78' in html, "Missing mile marker"
    print("✓ Suffering zones rendered")


def test_zone_labels_rendered():
    """Test that zone labels are rendered."""
    html = generate_course_map_html(SAMPLE_DATA)
    assert 'Red Dirt Reckoning' in html, "Missing zone label"
    assert 'Crosswind Corridor' in html, "Missing zone label"
    assert 'The Grind' in html, "Missing zone label"
    print("✓ Zone labels rendered")


def test_zone_descriptions_rendered():
    """Test that zone descriptions are rendered."""
    html = generate_course_map_html(SAMPLE_DATA)
    assert 'Oklahoma clay' in html, "Missing zone description"
    assert 'relentless wind' in html, "Missing zone description"
    assert 'fatigue meets climbing' in html, "Missing zone description"
    print("✓ Zone descriptions rendered")


def test_enhanced_details_rendered():
    """Test that enhanced details (terrain, named section, weather) are rendered."""
    html = generate_course_map_html(SAMPLE_DATA)
    assert 'The Gauntlet' in html, "Missing named section"
    assert 'Loose gravel over hardpack' in html, "Missing terrain detail"
    assert 'Gets greasy when wet' in html, "Missing weather note"
    print("✓ Enhanced details rendered")


def test_citation_rendered():
    """Test that citations are rendered when present."""
    html = generate_course_map_html(SAMPLE_DATA)
    assert '2023 race reports' in html, "Missing citation"
    print("✓ Citation rendered")


def test_footer_caption_present():
    """Test that footer caption is present."""
    html = generate_course_map_html(SAMPLE_DATA)
    assert 'gg-route-caption' in html, "Missing caption container"
    assert 'RideWithGPS' in html, "Missing RWGPS credit"
    assert 'Suffering courtesy of you' in html, "Missing tagline"
    print("✓ Footer caption present")


def test_research_note_present():
    """Test that course breakdown research note is present."""
    html = generate_course_map_html(SAMPLE_DATA)
    assert 'gg-course-breakdown-note' in html, "Missing research note"
    assert 'race reports' in html.lower(), "Missing research note content"
    print("✓ Research note present")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_generates_valid_html,
        test_contains_section_structure,
        test_contains_header_elements,
        test_rwgps_embed_present,
        test_suffering_zones_rendered,
        test_zone_labels_rendered,
        test_zone_descriptions_rendered,
        test_enhanced_details_rendered,
        test_citation_rendered,
        test_footer_caption_present,
        test_research_note_present,
    ]
    
    passed = 0
    failed = 0
    
    print("\n" + "=" * 50)
    print("COURSE MAP MODULE TESTS")
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
