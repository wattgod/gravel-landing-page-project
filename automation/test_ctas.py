#!/usr/bin/env python3
"""
Regression tests for ctas.py module.

Run: python3 automation/test_ctas.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from automation.ctas import generate_coaching_cta_html, generate_gravel_races_cta_html


# ============================================================================
# COACHING CTA TESTS
# ============================================================================

def test_coaching_generates_valid_html():
    """Test that coaching CTA returns valid HTML string."""
    html = generate_coaching_cta_html()
    assert isinstance(html, str), "Should return string"
    assert len(html) > 200, "Should return substantial HTML"
    print("✓ Coaching CTA generates valid HTML")


def test_coaching_section_structure():
    """Test that coaching CTA has correct section structure."""
    html = generate_coaching_cta_html()
    assert 'gg-coaching-cta-section' in html, "Missing section class"
    assert 'gg-coaching-cta-card' in html, "Missing card class"
    assert '<section' in html, "Missing section element"
    print("✓ Coaching CTA section structure correct")


def test_coaching_title():
    """Test that coaching CTA has title."""
    html = generate_coaching_cta_html()
    assert 'Really Want to Train Right?' in html, "Missing title"
    assert 'gg-coaching-cta-title' in html, "Missing title class"
    print("✓ Coaching CTA title present")


def test_coaching_body_text():
    """Test that coaching CTA has body text."""
    html = generate_coaching_cta_html()
    assert 'Plans are templates' in html, "Missing body text"
    assert 'Coaching is personal' in html, "Missing body text"
    print("✓ Coaching CTA body text present")


def test_coaching_button():
    """Test that coaching CTA has button with correct link."""
    html = generate_coaching_cta_html()
    assert 'https://gravelgodcycling.com/coaching/' in html, "Missing coaching URL"
    assert 'Apply for Coaching' in html, "Missing button text"
    assert 'gg-coaching-cta-button' in html, "Missing button class"
    print("✓ Coaching CTA button present")


def test_coaching_colors():
    """Test that coaching CTA uses correct colors."""
    html = generate_coaching_cta_html()
    assert '#4ECDC4' in html, "Missing turquoise color"
    assert '#F4D03F' in html, "Missing yellow hover color"
    print("✓ Coaching CTA colors correct")


# ============================================================================
# GRAVEL RACES CTA TESTS
# ============================================================================

def test_races_generates_valid_html():
    """Test that gravel races CTA returns valid HTML string."""
    html = generate_gravel_races_cta_html()
    assert isinstance(html, str), "Should return string"
    assert len(html) > 200, "Should return substantial HTML"
    print("✓ Gravel races CTA generates valid HTML")


def test_races_section_structure():
    """Test that gravel races CTA has correct section structure."""
    html = generate_gravel_races_cta_html()
    assert 'gravel-races-cta' in html, "Missing section class"
    assert '<div class="gravel-races-cta">' in html, "Missing container"
    print("✓ Gravel races CTA section structure correct")


def test_races_title():
    """Test that gravel races CTA has title."""
    html = generate_gravel_races_cta_html()
    assert 'Ready to explore more suffering?' in html, "Missing title"
    assert '<h2>' in html, "Missing h2 element"
    print("✓ Gravel races CTA title present")


def test_races_button():
    """Test that gravel races CTA has button with correct link."""
    html = generate_gravel_races_cta_html()
    assert 'https://gravelgodcycling.com/gravel-races/' in html, "Missing races URL"
    assert 'ALL GRAVEL RACES' in html, "Missing button text"
    assert 'gravel-races-cta-button' in html, "Missing button class"
    print("✓ Gravel races CTA button present")


def test_races_colors():
    """Test that gravel races CTA uses correct colors."""
    html = generate_gravel_races_cta_html()
    assert '#4ECDC4' in html, "Missing turquoise color"
    assert '#F4D03F' in html, "Missing yellow hover color"
    assert '#F5E5D3' in html, "Missing cream background"
    print("✓ Gravel races CTA colors correct")


def test_races_font_import():
    """Test that gravel races CTA imports Sometype Mono font."""
    html = generate_gravel_races_cta_html()
    assert 'Sometype+Mono' in html or 'Sometype Mono' in html, "Missing font import"
    print("✓ Gravel races CTA font import present")


# ============================================================================
# SHARED DESIGN TESTS
# ============================================================================

def test_both_have_styles():
    """Test that both CTAs have inline styles."""
    coaching = generate_coaching_cta_html()
    races = generate_gravel_races_cta_html()
    assert '<style>' in coaching, "Coaching CTA missing style tag"
    assert '<style>' in races, "Races CTA missing style tag"
    print("✓ Both CTAs have inline styles")


def test_consistent_color_palette():
    """Test that both CTAs use consistent color palette."""
    coaching = generate_coaching_cta_html()
    races = generate_gravel_races_cta_html()
    # Both should use turquoise and yellow
    assert '#4ECDC4' in coaching and '#4ECDC4' in races, "Turquoise should be in both"
    assert '#F4D03F' in coaching and '#F4D03F' in races, "Yellow should be in both (hover)"
    print("✓ Consistent color palette across CTAs")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        # Coaching tests
        test_coaching_generates_valid_html,
        test_coaching_section_structure,
        test_coaching_title,
        test_coaching_body_text,
        test_coaching_button,
        test_coaching_colors,
        # Races tests
        test_races_generates_valid_html,
        test_races_section_structure,
        test_races_title,
        test_races_button,
        test_races_colors,
        test_races_font_import,
        # Shared tests
        test_both_have_styles,
        test_consistent_color_palette,
    ]
    
    passed = 0
    failed = 0
    
    print("\n" + "=" * 50)
    print("CTA MODULES TESTS")
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
