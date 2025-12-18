#!/usr/bin/env python3
"""
Regression tests for vitals.py module.

Run: python3 automation/test_vitals.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from automation.vitals import generate_vitals_html


# Sample test data matching expected schema
SAMPLE_DATA = {
    "race": {
        "vitals": {
            "location": "Stillwater, Oklahoma",
            "county": "Payne County",
            "date_specific": "March 21-22, 2025",
            "distance_mi": 103,
            "elevation_ft": 4200,
            "terrain_types": ["Gravel", "Red Dirt", "Pavement"],
            "field_size": "~2,500 riders",
            "start_time": "7:00 AM",
            "registration": "$185-$225",
            "prize_purse": "$30,000",
            "aid_stations": "4 fully stocked",
            "cutoff_time": "12 hours"
        }
    }
}


def test_generates_valid_html():
    """Test that function returns valid HTML string."""
    html = generate_vitals_html(SAMPLE_DATA)
    assert isinstance(html, str), "Should return string"
    assert len(html) > 100, "Should return substantial HTML"
    print("✓ Generates valid HTML")


def test_contains_section_structure():
    """Test that HTML contains required section structure."""
    html = generate_vitals_html(SAMPLE_DATA)
    assert 'id="race-vitals"' in html, "Missing section ID"
    assert 'gg-guide-section' in html, "Missing section class"
    assert 'gg-vitals-grid' in html, "Missing vitals grid"
    print("✓ Contains section structure")


def test_contains_header_elements():
    """Test that HTML contains header pill and heading."""
    html = generate_vitals_html(SAMPLE_DATA)
    assert 'Quick Facts' in html, "Missing 'Quick Facts' pill"
    assert 'Race Vitals' in html, "Missing heading"
    assert 'The numbers that matter' in html, "Missing lede text"
    print("✓ Contains header elements")


def test_location_rendered():
    """Test that location with county is rendered."""
    html = generate_vitals_html(SAMPLE_DATA)
    assert 'Stillwater, Oklahoma' in html, "Missing location"
    assert 'Payne County' in html, "Missing county"
    print("✓ Location rendered correctly")


def test_distance_rendered():
    """Test that distance is rendered with units."""
    html = generate_vitals_html(SAMPLE_DATA)
    assert '103 miles' in html, "Missing distance"
    print("✓ Distance rendered correctly")


def test_elevation_formatted():
    """Test that elevation is formatted with comma."""
    html = generate_vitals_html(SAMPLE_DATA)
    assert '4,200' in html, "Elevation should be formatted with comma"
    assert 'ft' in html, "Missing elevation unit"
    print("✓ Elevation formatted correctly")


def test_terrain_types_joined():
    """Test that terrain types are joined with commas."""
    html = generate_vitals_html(SAMPLE_DATA)
    assert 'Gravel, Red Dirt, Pavement' in html, "Terrain types should be comma-joined"
    print("✓ Terrain types joined correctly")


def test_all_vitals_present():
    """Test that all vital fields are rendered."""
    html = generate_vitals_html(SAMPLE_DATA)
    required_fields = [
        'Location', 'Date', 'Distance', 'Elevation', 'Terrain',
        'Field Size', 'Start Time', 'Registration', 'Prize Purse',
        'Aid Stations', 'Cut-off Time'
    ]
    for field in required_fields:
        assert field in html, f"Missing field: {field}"
    print("✓ All vitals present")


def test_table_structure():
    """Test that HTML contains proper table structure."""
    html = generate_vitals_html(SAMPLE_DATA)
    assert '<table' in html, "Missing table element"
    assert '<tbody>' in html, "Missing tbody"
    assert '<tr>' in html, "Missing table rows"
    assert '<th>' in html, "Missing table headers"
    assert '<td>' in html, "Missing table data cells"
    print("✓ Table structure correct")


def test_no_template_placeholders():
    """Test that no template placeholders remain."""
    html = generate_vitals_html(SAMPLE_DATA)
    assert '{' not in html or '{{' in html, "Unresolved template placeholder"
    assert '}' not in html or '}}' in html, "Unresolved template placeholder"
    print("✓ No template placeholders")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_generates_valid_html,
        test_contains_section_structure,
        test_contains_header_elements,
        test_location_rendered,
        test_distance_rendered,
        test_elevation_formatted,
        test_terrain_types_joined,
        test_all_vitals_present,
        test_table_structure,
        test_no_template_placeholders,
    ]
    
    passed = 0
    failed = 0
    
    print("\n" + "=" * 50)
    print("VITALS MODULE TESTS")
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
