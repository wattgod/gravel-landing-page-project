"""
Regression tests for blackpill.py

Run these tests BEFORE deploying any changes to Black Pill generation.
These catch the color violation and other structure issues.

Usage:
    python test_blackpill.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from automation.blackpill import (
    generate_blackpill_html,
    validate_blackpill_data,
    validate_background_color,
    COLOR_PALETTE
)


def test_color_violation_fixed():
    """
    CRITICAL: Test that #F4D03F is NOT used on large backgrounds.
    This was the original violation that prompted modularization.
    """
    data = {
        'race': {
            'black_pill': {
                'title': 'Test Title',
                'reality': 'Test reality',
                'consequences': ['One', 'Two'],
                'expectation_reset': 'Test reset'
            }
        }
    }
    
    html = generate_blackpill_html(data)
    
    # Find the section background color
    # Should be in .gg-blackpill-section { background: COLOR }
    import re
    section_bg_match = re.search(r'\.gg-blackpill-section \{[^}]*background:\s*([^;]+);', html)
    
    assert section_bg_match, "Could not find section background color"
    bg_color = section_bg_match.group(1).strip()
    
    # CRITICAL: Background should be cream, NOT yellow
    assert bg_color == '#FFF5E6', f"Section background should be #FFF5E6 (cream), got {bg_color}"
    assert bg_color != '#F4D03F', "VIOLATION: #F4D03F should NOT be used on large backgrounds!"
    
    print("✓ Color violation FIXED - large backgrounds use cream, not yellow")


def test_yellow_allowed_for_small_elements():
    """Test that yellow (#F4D03F) IS allowed for small elements like badges."""
    data = {
        'race': {
            'black_pill': {
                'title': 'Test',
                'reality': 'Test',
                'consequences': ['One'],
                'expectation_reset': 'Test'
            }
        }
    }
    
    html = generate_blackpill_html(data)
    
    # Yellow should appear for badge
    assert '#F4D03F' in html, "Yellow should be present for badge"
    
    # But only in badge context
    import re
    badge_bg_match = re.search(r'\.gg-blackpill-badge \{[^}]*background:\s*([^;]+);', html)
    assert badge_bg_match, "Could not find badge background"
    badge_color = badge_bg_match.group(1).strip()
    assert badge_color == '#F4D03F', f"Badge should be yellow, got {badge_color}"
    
    print("✓ Yellow (#F4D03F) correctly used for small badge element")


def test_background_color_validator():
    """Test the background color validation function."""
    # Large elements should get cream
    assert validate_background_color('large_background') == '#FFF5E6'
    assert validate_background_color('quote_block') == '#FFF5E6'
    assert validate_background_color('section_bg') == '#FFF5E6'
    
    # Small elements can get yellow
    assert validate_background_color('badge') == '#F4D03F'
    assert validate_background_color('small_accent') == '#F4D03F'
    
    # Unknown types default to safe cream
    assert validate_background_color('unknown') == '#FFF5E6'
    
    print("✓ Background color validator working correctly")


def test_validation_catches_missing_fields():
    """Test that validation catches missing required fields."""
    bad_data = {
        'race': {
            'black_pill': {
                'title': 'Test'
                # Missing: reality, consequences, expectation_reset
            }
        }
    }
    
    errors = validate_blackpill_data(bad_data)
    assert len(errors) > 0, "Should catch missing fields"
    assert any('reality' in e for e in errors), "Should report missing reality"
    assert any('consequences' in e for e in errors), "Should report missing consequences"
    
    print("✓ Validation catches missing fields")


def test_validation_catches_wrong_types():
    """Test that validation catches wrong data types."""
    bad_data = {
        'race': {
            'black_pill': {
                'title': 'Test',
                'reality': 'Test',
                'consequences': 'Not a list',  # Should be list
                'expectation_reset': 'Test'
            }
        }
    }
    
    errors = validate_blackpill_data(bad_data)
    assert len(errors) > 0, "Should catch wrong types"
    assert any('consequences' in e and 'list' in e for e in errors), "Should report list type error"
    
    print("✓ Validation catches wrong data types")


def test_style_tag_position():
    """Test that style tag comes AFTER </section>, not inside."""
    data = {
        'race': {
            'black_pill': {
                'title': 'Test',
                'reality': 'Test',
                'consequences': ['One', 'Two'],
                'expectation_reset': 'Test'
            }
        }
    }
    
    html = generate_blackpill_html(data)
    
    section_close_pos = html.index('</section>')
    style_open_pos = html.index('<style>')
    
    assert style_open_pos > section_close_pos, "Style tag MUST come after </section>!"
    
    # Verify no style inside section
    section_html = html[:section_close_pos]
    assert '<style>' not in section_html, "Style tag must NOT be inside section!"
    
    print("✓ Style tag positioned correctly (after section)")


def test_consequences_list_rendering():
    """Test that consequences list renders correctly."""
    data = {
        'race': {
            'black_pill': {
                'title': 'Test',
                'reality': 'Test',
                'consequences': [
                    'First consequence',
                    'Second consequence',
                    'Third consequence'
                ],
                'expectation_reset': 'Test'
            }
        }
    }
    
    html = generate_blackpill_html(data)
    
    # All consequences should appear
    assert 'First consequence' in html
    assert 'Second consequence' in html
    assert 'Third consequence' in html
    
    # Should be in list items
    assert '<li>First consequence</li>' in html
    assert '<li>Second consequence</li>' in html
    
    print("✓ Consequences list renders correctly")


def test_color_palette_consistency():
    """Test that all colors come from the palette constant."""
    data = {
        'race': {
            'black_pill': {
                'title': 'Test',
                'reality': 'Test',
                'consequences': ['Test'],
                'expectation_reset': 'Test'
            }
        }
    }
    
    html = generate_blackpill_html(data)
    
    # All colors in HTML should be from COLOR_PALETTE
    used_colors = set()
    import re
    color_pattern = r'#[0-9A-Fa-f]{6}'
    used_colors = set(re.findall(color_pattern, html))
    
    palette_colors = set(COLOR_PALETTE.values())
    
    # Every color used should be in palette
    for color in used_colors:
        assert color.upper() in {c.upper() for c in palette_colors}, \
            f"Color {color} not in COLOR_PALETTE! Add it or use approved color."
    
    print(f"✓ All {len(used_colors)} colors come from approved palette")


def test_max_width_constraint():
    """Test that section has max-width constraint like other sections."""
    data = {
        'race': {
            'black_pill': {
                'title': 'Test',
                'reality': 'Test',
                'consequences': ['Test'],
                'expectation_reset': 'Test'
            }
        }
    }
    
    html = generate_blackpill_html(data)
    
    # Should have max-width: 1000px and margin: auto for centering
    assert 'max-width: 1000px' in html, "Missing max-width constraint!"
    assert 'margin:' in html and 'auto' in html, "Missing margin: auto for centering!"
    
    print("✓ Max-width constraint present (matches other sections)")


def test_responsive_styles_present():
    """Test that responsive media query is present."""
    data = {
        'race': {
            'black_pill': {
                'title': 'Test',
                'reality': 'Test',
                'consequences': ['Test'],
                'expectation_reset': 'Test'
            }
        }
    }
    
    html = generate_blackpill_html(data)
    
    assert '@media (max-width: 768px)' in html, "Responsive media query missing!"
    assert '@media' in html, "No media queries found"
    
    print("✓ Responsive styles present")


def test_no_template_placeholders():
    """Test that no template placeholders escape into output."""
    data = {
        'race': {
            'black_pill': {
                'title': 'Test Title',
                'reality': 'Test reality',
                'consequences': ['Test'],
                'expectation_reset': 'Test reset'
            }
        }
    }
    
    html = generate_blackpill_html(data)
    
    bad_patterns = ['{{', '}}', '${', 'PLACEHOLDER', 'TODO', 'FIXME', 'XXX']
    
    for pattern in bad_patterns:
        assert pattern not in html, f"Template placeholder escaped: {pattern}"
    
    print("✓ No template placeholders in output")


def run_all_tests():
    """Run all regression tests."""
    print("\n=== Running Black Pill Regression Tests ===\n")
    
    tests = [
        test_color_violation_fixed,
        test_yellow_allowed_for_small_elements,
        test_background_color_validator,
        test_validation_catches_missing_fields,
        test_validation_catches_wrong_types,
        test_style_tag_position,
        test_consequences_list_rendering,
        test_color_palette_consistency,
        test_max_width_constraint,
        test_responsive_styles_present,
        test_no_template_placeholders
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
        print("\nColor violation FIXED:")
        print("  ❌ Was: #F4D03F on large section background")
        print("  ✅ Now: #FFF5E6 on large section background")
        print("  ✅ Yellow only used for small badge")
        sys.exit(0)


if __name__ == '__main__':
    run_all_tests()
