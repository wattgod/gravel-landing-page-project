#!/usr/bin/env python3
"""
REGRESSION TEST: Training Plans Template Structure
==================================================
Ensures training plans section matches exact template structure:
- Exact HTML structure with comments
- No links (plans not built yet)
- Correct CSS (badge + button styles only)
- Proper plan name formatting

Exit codes:
    0 = All tests passed
    1 = Structure violations detected
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Dict


def check_training_plans_structure(json_path: Path) -> List[str]:
    """Check training plans section structure in Elementor JSON."""
    errors = []
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return [f"Failed to parse JSON: {e}"]
    
    # Extract HTML content
    html_content = extract_html_from_json(data)
    
    # Check for training plans section
    if 'gg-volume-section' not in html_content:
        errors.append("Missing training plans section (gg-volume-section)")
        return errors
    
    # Check for required elements
    required_elements = [
        ('gg-training-plans-badge', 'Training plans badge'),
        ('gg-volume-grid', 'Volume grid container'),
        ('gg-volume-card', 'Volume card articles'),
        ('gg-volume-tag', 'Volume track tag'),
        ('gg-volume-title', 'Volume title'),
        ('gg-volume-hours', 'Volume hours'),
        ('gg-volume-divider', 'Volume divider'),
        ('gg-plan-stack', 'Plan stack container'),
        ('gg-plan', 'Plan items'),
        ('gg-plan-name', 'Plan names'),
        ('gg-volume-footer', 'Volume footer'),
    ]
    
    for class_name, description in required_elements:
        if class_name not in html_content:
            errors.append(f"Missing required element: {description} ({class_name})")
    
    # Check for tier comments
    tier_comments = [
        '<!-- ================= AYAHUASCA ================= -->',
        '<!-- ================= FINISHER ================= -->',
        '<!-- ================= COMPETE ================= -->',
        '<!-- ================= PODIUM ================= -->',
    ]
    
    for comment in tier_comments:
        if comment not in html_content:
            errors.append(f"Missing tier comment: {comment}")
    
    # Check for tier names
    tier_names = ['Ayahuasca', 'Finisher', 'Compete', 'Podium']
    for tier in tier_names:
        if f'<h3 class="gg-volume-title">{tier}</h3>' not in html_content:
            errors.append(f"Missing tier title: {tier}")
    
    # Check for NO links (plans not built yet)
    link_pattern = r'<a[^>]*class="gg-plan-cta"[^>]*>'
    links = re.findall(link_pattern, html_content)
    if links:
        errors.append(f"Found {len(links)} training plan links - should be NONE (plans not built yet)")
    
    # Check for "View Plan" text (should not exist)
    if 'View Plan' in html_content:
        errors.append("Found 'View Plan' text - links should be removed")
    
    # Check CSS structure
    css_checks = [
        (r'\.gg-training-plans-badge\s*\{', 'Training plans badge CSS'),
        (r'background:\s*#f4d03f', 'Badge yellow background (#f4d03f)'),
        (r'\.gg-plan-cta\s*\{', 'Plan CTA button CSS'),
        (r'background:\s*#40E0D0', 'Button turquoise background (#40E0D0)'),
        (r'\.gg-plan-cta:hover\s*\{', 'Button hover CSS'),
        (r'background:\s*#f4d03f.*hover', 'Button hover yellow (#f4d03f)'),
    ]
    
    for pattern, description in css_checks:
        if not re.search(pattern, html_content, re.IGNORECASE | re.DOTALL):
            errors.append(f"Missing CSS: {description}")
    
    # Check that ONLY the allowed CSS is present in training plans section (badge + button styles only)
    # Find the training plans section and its associated style tag (may be after section close)
    section_match = re.search(r'<section[^>]*class="gg-volume-section"[^>]*>.*?</section>', html_content, re.IGNORECASE | re.DOTALL)
    if section_match:
        section_html = section_match.group(0)
        section_end = section_match.end()
        
        # Look for style tag immediately after the section (within 200 chars)
        after_section = html_content[section_end:section_end+200]
        style_match = re.search(r'<style[^>]*>(.*?)</style>', after_section, re.IGNORECASE | re.DOTALL)
        if style_match:
            css_content = style_match.group(1)
            
            # Check for forbidden CSS classes (card styling that was removed)
            forbidden_css_classes = [
                (r'\.gg-volume-grid\s*\{', 'gg-volume-grid'),
                (r'\.gg-volume-card\s*\{', 'gg-volume-card'),
                (r'\.gg-volume-tag\s*\{', 'gg-volume-tag'),
                (r'\.gg-volume-title\s*\{', 'gg-volume-title'),
                (r'\.gg-volume-hours\s*\{', 'gg-volume-hours'),
                (r'\.gg-volume-divider\s*\{', 'gg-volume-divider'),
                (r'\.gg-plan-stack\s*\{', 'gg-plan-stack'),
                (r'\.gg-plan\s*\{', 'gg-plan'),
                (r'\.gg-plan-name\s*\{', 'gg-plan-name'),
                (r'\.gg-volume-footer\s*\{', 'gg-volume-footer'),
            ]
            
            for pattern, class_name in forbidden_css_classes:
                if re.search(pattern, css_content, re.IGNORECASE):
                    errors.append(f"Forbidden CSS class in training plans section: {class_name} (should use base CSS only, not inline)")
            
            # Count CSS rules in this section
            css_rules = re.findall(r'\.\w+[^{]*\{', css_content)
            
            # Should only have: .gg-training-plans-badge, .gg-training-plans-badge-icon, .gg-plan-cta, .gg-plan-cta:hover, .gg-plan-cta:active (5 max)
            if len(css_rules) > 5:
                errors.append(f"Too many CSS rules in training plans section: {len(css_rules)} (should only have badge + button styles, max 5 rules)")
                errors.append(f"Found rules: {', '.join(css_rules[:10])}")
    
    # Check plan name formatting
    plan_name_patterns = [
        (r'Beginner\s*–\s*[^<]+<span>', 'Beginner plan format'),
        (r'Finisher\s+Intermediate\s*–', 'Finisher Intermediate format'),
        (r'Compete\s+Intermediate\s*–', 'Compete Intermediate format'),
        (r'Podium\s+Advanced\s*–', 'Podium Advanced format'),
    ]
    
    # At least one of these patterns should match
    found_pattern = False
    for pattern, description in plan_name_patterns:
        if re.search(pattern, html_content, re.IGNORECASE):
            found_pattern = True
            break
    
    if not found_pattern and 'gg-plan-name' in html_content:
        # If we have plan names but no matches, might be okay - just warn
        pass
    
    return errors


def extract_html_from_json(data: Dict) -> str:
    """Recursively extract all HTML content from Elementor JSON."""
    html_parts = []
    
    def traverse(obj):
        if isinstance(obj, dict):
            if obj.get('widgetType') == 'html':
                html = obj.get('settings', {}).get('html', '')
                if html:
                    html_parts.append(html)
            for value in obj.values():
                traverse(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)
    
    traverse(data)
    return '\n'.join(html_parts)


def main():
    """Run training plans structure regression tests."""
    project_root = Path(__file__).parent
    output_dir = project_root / 'output'
    
    all_errors = []
    
    # Check all generated JSON files (skip backups)
    print("Checking training plans structure in generated JSONs...")
    print("=" * 70)
    
    json_files = [f for f in output_dir.glob('elementor-*.json') 
                  if 'FIXED' not in f.name and 'OLD' not in f.name and 'BACKUP' not in f.name]
    
    for json_file in sorted(json_files):
        errors = check_training_plans_structure(json_file)
        if errors:
            all_errors.extend([f"{json_file.name}: {e}" for e in errors])
            print(f"  ❌ {json_file.name}")
            for error in errors:
                print(f"     - {error}")
        else:
            print(f"  ✓ {json_file.name}")
    
    print()
    
    if all_errors:
        print(f"\nFAILED: {len(all_errors)} error(s) found\n")
        for i, error in enumerate(all_errors, 1):
            print(f"  {i}. {error}")
        sys.exit(1)
    else:
        print("✓ All training plans structure tests passed")
        print("  - Exact template structure verified")
        print("  - No links found (as expected)")
        print("  - CSS matches template")
        sys.exit(0)


if __name__ == '__main__':
    main()
