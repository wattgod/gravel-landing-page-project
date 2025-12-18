#!/usr/bin/env python3
"""
Regression tests for logistics.py module.

Run: python3 automation/test_logistics.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from automation.logistics import generate_logistics_html


# Sample test data matching expected schema
SAMPLE_DATA = {
    "race": {
        "logistics": {
            "airport": "Will Rogers World Airport (OKC) - 75 miles",
            "lodging_strategy": "Book 6+ months out. Stillwater hotels fill fast. Consider Tulsa or OKC as backups.",
            "food": "Eskimo Joe's is the local institution. Stock up at Walmart before race day.",
            "packet_pickup": "Friday afternoon at the expo venue. Saturday morning available but lines are long.",
            "parking": "Free parking at the start. Arrive by 5:30 AM to get a good spot.",
            "official_site": "https://midsouthgravel.com"
        }
    }
}


def test_generates_valid_html():
    """Test that function returns valid HTML string."""
    html = generate_logistics_html(SAMPLE_DATA)
    assert isinstance(html, str), "Should return string"
    assert len(html) > 300, "Should return substantial HTML"
    print("✓ Generates valid HTML")


def test_contains_section_structure():
    """Test that HTML contains required section structure."""
    html = generate_logistics_html(SAMPLE_DATA)
    assert 'gg-logistics-section' in html, "Missing section class"
    assert 'gg-logistics-inner' in html, "Missing inner container"
    print("✓ Contains section structure")


def test_header_elements():
    """Test that header elements are present."""
    html = generate_logistics_html(SAMPLE_DATA)
    assert 'Race Logistics' in html, "Missing 'Race Logistics' pill"
    assert 'unsexy details' in html, "Missing heading text"
    assert 'gg-logistics-pill' in html, "Missing pill class"
    print("✓ Header elements present")


def test_getting_there_section():
    """Test that 'Getting There' section is rendered."""
    html = generate_logistics_html(SAMPLE_DATA)
    assert 'Getting There' in html, "Missing 'Getting There' title"
    assert 'Will Rogers' in html, "Missing airport info"
    assert 'Closest major airport' in html, "Missing airport label"
    print("✓ 'Getting There' section rendered")


def test_staying_there_section():
    """Test that 'Staying There' section is rendered."""
    html = generate_logistics_html(SAMPLE_DATA)
    assert 'Staying There' in html, "Missing 'Staying There' title"
    assert 'Lodging' in html, "Missing lodging label"
    assert 'Food & groceries' in html, "Missing food label"
    print("✓ 'Staying There' section rendered")


def test_airport_info():
    """Test that airport info is rendered."""
    html = generate_logistics_html(SAMPLE_DATA)
    assert 'OKC' in html, "Missing airport code"
    assert '75 miles' in html, "Missing distance"
    print("✓ Airport info rendered")


def test_lodging_info():
    """Test that lodging info is rendered."""
    html = generate_logistics_html(SAMPLE_DATA)
    assert '6+ months' in html, "Missing booking timeframe"
    assert 'Stillwater' in html, "Missing location"
    print("✓ Lodging info rendered")


def test_food_info():
    """Test that food info is rendered."""
    html = generate_logistics_html(SAMPLE_DATA)
    assert "Eskimo Joe" in html, "Missing local food spot"
    print("✓ Food info rendered")


def test_packet_pickup_info():
    """Test that packet pickup info is rendered."""
    html = generate_logistics_html(SAMPLE_DATA)
    assert 'Packet pickup' in html, "Missing packet pickup label"
    assert 'Friday afternoon' in html, "Missing pickup day"
    print("✓ Packet pickup info rendered")


def test_parking_info():
    """Test that parking info is rendered."""
    html = generate_logistics_html(SAMPLE_DATA)
    assert 'Parking' in html, "Missing parking label"
    assert 'Free parking' in html, "Missing parking info"
    print("✓ Parking info rendered")


def test_official_site_link():
    """Test that official site link is present."""
    html = generate_logistics_html(SAMPLE_DATA)
    assert 'https://midsouthgravel.com' in html, "Missing official site URL"
    assert 'target="_blank"' in html, "Link should open in new tab"
    assert 'Official race info' in html, "Missing link title"
    print("✓ Official site link present")


def test_disclaimer_present():
    """Test that disclaimer is present."""
    html = generate_logistics_html(SAMPLE_DATA)
    assert 'gg-logistics-disclaimer' in html, "Missing disclaimer container"
    assert 'my opinion' in html.lower(), "Missing opinion disclaimer"
    assert 'official race website' in html.lower(), "Missing official site reference"
    print("✓ Disclaimer present")


def test_list_structure():
    """Test that HTML uses proper list structure."""
    html = generate_logistics_html(SAMPLE_DATA)
    assert '<ul' in html, "Missing unordered list"
    assert '<li>' in html, "Missing list items"
    assert 'gg-logistics-list' in html, "Missing list class"
    print("✓ List structure correct")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_generates_valid_html,
        test_contains_section_structure,
        test_header_elements,
        test_getting_there_section,
        test_staying_there_section,
        test_airport_info,
        test_lodging_info,
        test_food_info,
        test_packet_pickup_info,
        test_parking_info,
        test_official_site_link,
        test_disclaimer_present,
        test_list_structure,
    ]
    
    passed = 0
    failed = 0
    
    print("\n" + "=" * 50)
    print("LOGISTICS MODULE TESTS")
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
