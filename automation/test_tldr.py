#!/usr/bin/env python3
"""
Regression tests for tldr.py module.

Run: python3 automation/test_tldr.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from automation.tldr import generate_tldr_html


# Sample test data with tldr fields
SAMPLE_DATA_WITH_TLDR = {
    "race": {
        "tldr": {
            "should_race_if": "You thrive on unpredictability and want a true test of adaptability.",
            "skip_if": "You need perfect conditions and hate surprises."
        }
    }
}

# Sample test data without tldr fields (fallback mode)
SAMPLE_DATA_FALLBACK = {
    "race": {
        "final_verdict": {
            "should_you_race": "You like hurting yourself and surprises. Reconsider if you need certainty."
        }
    }
}


def test_generates_valid_html():
    """Test that function returns valid HTML string."""
    html = generate_tldr_html(SAMPLE_DATA_WITH_TLDR)
    assert isinstance(html, str), "Should return string"
    assert len(html) > 100, "Should return substantial HTML"
    print("✓ Generates valid HTML")


def test_contains_decision_grid():
    """Test that HTML contains decision grid structure."""
    html = generate_tldr_html(SAMPLE_DATA_WITH_TLDR)
    assert 'gg-decision-grid' in html, "Missing decision grid"
    print("✓ Contains decision grid")


def test_contains_both_cards():
    """Test that HTML contains both decision cards."""
    html = generate_tldr_html(SAMPLE_DATA_WITH_TLDR)
    assert 'gg-decision-card--yes' in html, "Missing 'yes' card"
    assert 'gg-decision-card--no' in html, "Missing 'no' card"
    print("✓ Contains both cards")


def test_should_race_header():
    """Test that 'Should Race' header is present."""
    html = generate_tldr_html(SAMPLE_DATA_WITH_TLDR)
    assert 'You Should Race This If:' in html, "Missing 'Should Race' header"
    print("✓ 'Should Race' header present")


def test_skip_if_header():
    """Test that 'Skip If' header is present."""
    html = generate_tldr_html(SAMPLE_DATA_WITH_TLDR)
    assert 'Skip This If:' in html, "Missing 'Skip If' header"
    print("✓ 'Skip If' header present")


def test_should_race_content_rendered():
    """Test that 'should race' content is rendered."""
    html = generate_tldr_html(SAMPLE_DATA_WITH_TLDR)
    assert 'unpredictability' in html, "Missing should_race content"
    assert 'adaptability' in html, "Missing should_race content"
    print("✓ 'Should race' content rendered")


def test_skip_if_content_rendered():
    """Test that 'skip if' content is rendered."""
    html = generate_tldr_html(SAMPLE_DATA_WITH_TLDR)
    assert 'perfect conditions' in html, "Missing skip_if content"
    assert 'hate surprises' in html, "Missing skip_if content"
    print("✓ 'Skip if' content rendered")


def test_training_cta_link():
    """Test that training CTA link is present."""
    html = generate_tldr_html(SAMPLE_DATA_WITH_TLDR)
    assert 'href="#training"' in html, "Missing training link"
    assert 'Get a Training Plan' in html, "Missing CTA text"
    assert 'gg-decision-cta' in html, "Missing CTA class"
    print("✓ Training CTA link present")


def test_fallback_mode():
    """Test that fallback mode works when tldr fields missing."""
    html = generate_tldr_html(SAMPLE_DATA_FALLBACK)
    assert 'gg-decision-grid' in html, "Should still generate grid in fallback"
    assert 'You Should Race This If:' in html, "Should have headers in fallback"
    print("✓ Fallback mode works")


def test_no_template_placeholders():
    """Test that no template placeholders remain."""
    html = generate_tldr_html(SAMPLE_DATA_WITH_TLDR)
    assert '{should' not in html, "Unresolved template placeholder"
    assert '{skip' not in html, "Unresolved template placeholder"
    print("✓ No template placeholders")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_generates_valid_html,
        test_contains_decision_grid,
        test_contains_both_cards,
        test_should_race_header,
        test_skip_if_header,
        test_should_race_content_rendered,
        test_skip_if_content_rendered,
        test_training_cta_link,
        test_fallback_mode,
        test_no_template_placeholders,
    ]
    
    passed = 0
    failed = 0
    
    print("\n" + "=" * 50)
    print("TLDR MODULE TESTS")
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
