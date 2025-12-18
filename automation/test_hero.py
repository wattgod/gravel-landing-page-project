"""
Regression tests for hero.py

Run these tests BEFORE deploying any changes to Hero generation.
These ensure badge colors, score calculations, and structure remain consistent.

Usage:
    python test_hero.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from automation.hero import (
    generate_hero_html,
    validate_hero_data,
    calculate_percentage,
    COLOR_PALETTE
)


def test_badge_colors_enforced():
    """
    CRITICAL: Test that badges use turquoise (#4ECDC4) per design system.
    """
    data = {
        'race': {
            'display_name': 'Test Race',
            'tagline': 'Test tagline',
            'vitals': {'location_badge': 'TEST, STATE'},
            'gravel_god_rating': {
                'tier_label': 'TIER 1',
                'overall_score': 85,
                'course_profile': 42,
                'biased_opinion': 43
            }
        }
    }
    
    html = generate_hero_html(data)
    
    # Badge backgrounds should be turquoise
    import re
    badge_bg_match = re.search(r'\.gg-hero-badge \{[^}]*background:\s*([^;]+);', html)
    
    assert badge_bg_match, "Could not find badge background color"
    badge_color = badge_bg_match.group(1).strip()
    
    assert badge_color == '#4ECDC4', f"Badge background should be #4ECDC4 (turquoise), got {badge_color}"
    
    print("✓ Badge colors enforced - turquoise (#4ECDC4) per design system")


def test_progress_bar_colors():
    """Test that progress bars use turquoise fill."""
    data = {
        'race': {
            'display_name': 'Test',
            'tagline': 'Test',
            'vitals': {'location_badge': 'TEST'},
            'gravel_god_rating': {
                'tier_label': 'TIER 1',
                'overall_score': 85,
                'course_profile': 40,
                'biased_opinion': 40
            }
        }
    }
    
    html = generate_hero_html(data)
    
    # Progress bar fill should be turquoise
    import re
    fill_match = re.search(r'\.gg-hero-break-fill \{[^}]*background:\s*([^;]+);', html)
    
    assert fill_match, "Could not find progress bar fill color"
    fill_color = fill_match.group(1).strip()
    
    assert fill_color == '#4ECDC4', f"Progress bar should be turquoise, got {fill_color}"
    
    print("✓ Progress bar colors correct (turquoise)")


def test_percentage_calculations():
    """Test that percentage calculations are correct."""
    # 44 out of 50 = 88%
    assert calculate_percentage(44, 50) == 88
    
    # 25 out of 50 = 50%
    assert calculate_percentage(25, 50) == 50
    
    # 50 out of 50 = 100%
    assert calculate_percentage(50, 50) == 100
    
    # 0 out of 50 = 0%
    assert calculate_percentage(0, 50) == 0
    
    # Edge case: 0 max_score
    assert calculate_percentage(10, 0) == 0
    
    print("✓ Percentage calculations correct")


def test_validation_catches_missing_fields():
    """Test that validation catches missing required fields."""
    bad_data = {
        'race': {
            'display_name': 'Test'
            # Missing: tagline, vitals, gravel_god_rating
        }
    }
    
    errors = validate_hero_data(bad_data)
    assert len(errors) > 0, "Should catch missing fields"
    assert any('tagline' in e for e in errors), "Should report missing tagline"
    assert any('vitals' in e for e in errors), "Should report missing vitals"
    assert any('gravel_god_rating' in e for e in errors), "Should report missing rating"
    
    print("✓ Validation catches missing fields")


def test_validation_catches_invalid_scores():
    """Test that validation catches out-of-range scores."""
    bad_data = {
        'race': {
            'display_name': 'Test',
            'tagline': 'Test',
            'vitals': {'location_badge': 'TEST'},
            'gravel_god_rating': {
                'tier_label': 'TIER 1',
                'overall_score': 150,  # Should be 0-100
                'course_profile': 60,   # Should be 0-50
                'biased_opinion': 43
            }
        }
    }
    
    errors = validate_hero_data(bad_data)
    assert len(errors) > 0, "Should catch invalid scores"
    assert any('overall_score' in e and '100' in e for e in errors), "Should report overall_score range"
    assert any('course_profile' in e and '50' in e for e in errors), "Should report course_profile range"
    
    print("✓ Validation catches invalid score ranges")


def test_all_data_renders():
    """Test that all provided data appears in output."""
    data = {
        'race': {
            'display_name': 'Unique Race Name',
            'tagline': 'Unique tagline text',
            'vitals': {'location_badge': 'UNIQUE, LOCATION'},
            'gravel_god_rating': {
                'tier_label': 'TIER 2',
                'overall_score': 75,
                'course_profile': 38,
                'biased_opinion': 37
            }
        }
    }
    
    html = generate_hero_html(data)
    
    # All data should appear
    assert 'Unique Race Name' in html
    assert 'Unique tagline text' in html
    assert 'UNIQUE, LOCATION' in html
    assert 'TIER 2' in html
    assert '75' in html
    assert '38' in html
    assert '37' in html
    
    print("✓ All data renders in output")


def test_score_breakdown_structure():
    """Test that score breakdown has correct structure."""
    data = {
        'race': {
            'display_name': 'Test',
            'tagline': 'Test',
            'vitals': {'location_badge': 'TEST'},
            'gravel_god_rating': {
                'tier_label': 'TIER 1',
                'overall_score': 85,
                'course_profile': 42,
                'biased_opinion': 43
            }
        }
    }
    
    html = generate_hero_html(data)
    
    # Should have breakdown section
    assert 'gg-hero-score-breakdown' in html
    
    # Should have both score rows
    assert 'Course Profile' in html
    assert 'Biased Opinion' in html
    
    # Should have final row
    assert 'gg-hero-final-row' in html
    assert 'Final Score' in html
    
    # Should have inline width styles for progress bars
    assert 'width: 84%;' in html  # 42/50 = 84%
    assert 'width: 86%;' in html  # 43/50 = 86%
    
    print("✓ Score breakdown structure correct")


def test_responsive_styles_present():
    """Test that responsive media query is present."""
    data = {
        'race': {
            'display_name': 'Test',
            'tagline': 'Test',
            'vitals': {'location_badge': 'TEST'},
            'gravel_god_rating': {
                'tier_label': 'TIER 1',
                'overall_score': 85,
                'course_profile': 40,
                'biased_opinion': 40
            }
        }
    }
    
    html = generate_hero_html(data)
    
    assert '@media (max-width: 768px)' in html, "Responsive media query missing!"
    
    print("✓ Responsive styles present")


def test_color_palette_consistency():
    """Test that all colors come from the palette constant."""
    data = {
        'race': {
            'display_name': 'Test',
            'tagline': 'Test',
            'vitals': {'location_badge': 'TEST'},
            'gravel_god_rating': {
                'tier_label': 'TIER 1',
                'overall_score': 85,
                'course_profile': 40,
                'biased_opinion': 40
            }
        }
    }
    
    html = generate_hero_html(data)
    
    # Extract all hex colors
    import re
    used_colors = set(re.findall(r'#[0-9A-Fa-f]{6}', html))
    
    # All colors should be in palette
    palette_colors = set(COLOR_PALETTE.values())
    
    for color in used_colors:
        assert color.upper() in {c.upper() for c in palette_colors}, \
            f"Color {color} not in COLOR_PALETTE! Add it or use approved color."
    
    print(f"✓ All {len(used_colors)} colors come from approved palette")


def test_tier_badge_has_clip_path():
    """Test that tier badge has tag-shaped clip-path."""
    data = {
        'race': {
            'display_name': 'Test',
            'tagline': 'Test',
            'vitals': {'location_badge': 'TEST'},
            'gravel_god_rating': {
                'tier_label': 'TIER 1',
                'overall_score': 85,
                'course_profile': 40,
                'biased_opinion': 40
            }
        }
    }
    
    html = generate_hero_html(data)
    
    # Tier badge should have clip-path for tag shape
    assert 'clip-path: polygon' in html, "Tier badge missing clip-path for tag shape!"
    assert 'gg-hero-badge-tier' in html
    
    print("✓ Tier badge has tag-shaped clip-path")


def run_all_tests():
    """Run all regression tests."""
    print("\n=== Running Hero Section Regression Tests ===\n")
    
    tests = [
        test_badge_colors_enforced,
        test_progress_bar_colors,
        test_percentage_calculations,
        test_validation_catches_missing_fields,
        test_validation_catches_invalid_scores,
        test_all_data_renders,
        test_score_breakdown_structure,
        test_responsive_styles_present,
        test_color_palette_consistency,
        test_tier_badge_has_clip_path
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} ERROR: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*50}\n")
    
    if failed > 0:
        print("⚠️  TESTS FAILED - DO NOT DEPLOY")
        sys.exit(1)
    else:
        print("✅ ALL TESTS PASSED - Safe to deploy")
        print("\nDesign system enforced:")
        print("  ✅ Badge colors: #4ECDC4 (turquoise)")
        print("  ✅ Progress bars: #4ECDC4 (turquoise)")
        print("  ✅ Score calculations: Correct percentages")
        print("  ✅ Structure: All elements present")
        sys.exit(0)


if __name__ == '__main__':
    run_all_tests()
