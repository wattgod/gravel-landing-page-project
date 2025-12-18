#!/usr/bin/env python3
"""
Regression tests for history.py module.

Run: python3 automation/test_history.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from automation.history import generate_history_html


# Sample test data matching expected schema
SAMPLE_DATA = {
    "race": {
        "slug": "mid-south",
        "display_name": "Mid South",
        "vitals": {
            "location": "Stillwater, Oklahoma",
            "field_size": "~2,500 riders"
        },
        "course_description": {
            "character": "Red dirt chaos"
        },
        "history": {
            "origin_story": "What started as a small local ride has grown into one of gravel's most anticipated events.",
            "reputation": "Known for unpredictable weather and community spirit.",
            "notable_moments": [
                "2018: First edition draws 200 riders",
                "2020: Race cancelled due to pandemic",
                "2023: Field expands to 2,500 spots"
            ],
            "random_facts": [
                "The red dirt stains everything it touches.",
                "Local volunteers provide legendary aid station food.",
                "Wind direction changes the race completely.",
                "Some years it's dry, some years it's mud soup.",
                "Bobby Wintle created this as a community event."
            ]
        },
        "black_pill": {
            "reality": "The weather will humble you regardless of your FTP."
        }
    }
}


def test_generates_valid_html():
    """Test that function returns valid HTML string."""
    html = generate_history_html(SAMPLE_DATA)
    assert isinstance(html, str), "Should return string"
    assert len(html) > 500, "Should return substantial HTML"
    print("✓ Generates valid HTML")


def test_contains_section_structure():
    """Test that HTML contains required section structure."""
    html = generate_history_html(SAMPLE_DATA)
    assert 'gg-tldr-grid' in html, "Missing section class"
    assert '<section' in html, "Missing section element"
    print("✓ Contains section structure")


def test_contains_facts_header():
    """Test that Facts and History pill is present."""
    html = generate_history_html(SAMPLE_DATA)
    assert 'Facts And History' in html, "Missing Facts and History pill"
    print("✓ Facts and History pill present")


def test_vision_quest_title():
    """Test that vision quest title is rendered."""
    html = generate_history_html(SAMPLE_DATA)
    assert 'Mid South' in html, "Missing race name in title"
    assert 'gg-tldr-vision-title' in html, "Missing vision title class"
    print("✓ Vision quest title rendered")


def test_origin_story_rendered():
    """Test that origin story is rendered."""
    html = generate_history_html(SAMPLE_DATA)
    assert 'small local ride' in html, "Missing origin story content"
    print("✓ Origin story rendered")


def test_experience_section():
    """Test that 'The Experience' section is rendered."""
    html = generate_history_html(SAMPLE_DATA)
    assert 'The Experience' in html, "Missing Experience heading"
    assert 'gg-subheading' in html, "Missing subheading class"
    print("✓ Experience section rendered")


def test_timeline_rendered():
    """Test that timeline events are rendered."""
    html = generate_history_html(SAMPLE_DATA)
    assert 'gg-timeline-section' in html, "Missing timeline section"
    assert 'gg-timeline-event' in html, "Missing timeline events"
    assert '2018' in html, "Missing 2018 event"
    assert '2020' in html, "Missing 2020 event"
    assert '2023' in html, "Missing 2023 event"
    print("✓ Timeline rendered")


def test_timeline_content():
    """Test that timeline content is rendered correctly."""
    html = generate_history_html(SAMPLE_DATA)
    assert 'First edition draws 200 riders' in html, "Missing 2018 content"
    assert 'pandemic' in html, "Missing 2020 content"
    assert '2,500 spots' in html, "Missing 2023 content"
    print("✓ Timeline content correct")


def test_random_facts_rendered():
    """Test that random facts are rendered."""
    html = generate_history_html(SAMPLE_DATA)
    assert 'gg-facts-grid' in html, "Missing facts grid"
    assert 'gg-fact-card' in html, "Missing fact cards"
    assert 'red dirt stains' in html, "Missing fact content"
    print("✓ Random facts rendered")


def test_fact_numbers():
    """Test that facts have numbers."""
    html = generate_history_html(SAMPLE_DATA)
    assert 'gg-fact-number' in html, "Missing fact number class"
    print("✓ Fact numbers present")


def test_location_in_experience():
    """Test that location appears in experience text."""
    html = generate_history_html(SAMPLE_DATA)
    assert 'Stillwater' in html, "Missing location in experience"
    print("✓ Location in experience text")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_generates_valid_html,
        test_contains_section_structure,
        test_contains_facts_header,
        test_vision_quest_title,
        test_origin_story_rendered,
        test_experience_section,
        test_timeline_rendered,
        test_timeline_content,
        test_random_facts_rendered,
        test_fact_numbers,
        test_location_in_experience,
    ]
    
    passed = 0
    failed = 0
    
    print("\n" + "=" * 50)
    print("HISTORY MODULE TESTS")
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
