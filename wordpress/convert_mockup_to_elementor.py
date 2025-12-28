#!/usr/bin/env python3
"""
Convert Neo-Brutalist HTML mockup to Elementor JSON template.

This script:
1. Reads the HTML mockup
2. Extracts CSS and sections
3. Creates Elementor JSON structure
4. Saves as generic template with placeholders
"""

import json
import re
import uuid
from pathlib import Path
from bs4 import BeautifulSoup

def generate_id():
    """Generate Elementor-style ID (8 hex chars)."""
    return uuid.uuid4().hex[:8]

def extract_css_and_body(html_content):
    """Extract CSS from <style> tags and body content."""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract all CSS
    css_parts = []
    for style_tag in soup.find_all('style'):
        css_parts.append(style_tag.string or '')
        style_tag.decompose()

    css = '\n'.join(css_parts)

    # Get body content
    body = soup.find('body')
    body_html = ''.join(str(child) for child in body.children) if body else ''

    return css, body_html

def create_html_widget(html_content, css_classes=''):
    """Create an Elementor HTML widget."""
    return {
        "id": generate_id(),
        "settings": {
            "html": html_content,
            "_css_classes": css_classes
        },
        "elements": [],
        "isInner": False,
        "widgetType": "html",
        "elType": "widget"
    }

def create_section(elements, settings=None):
    """Create an Elementor section with a column."""
    section_settings = settings or {}
    section_settings.setdefault("layout", "full_width")

    return {
        "id": generate_id(),
        "settings": section_settings,
        "elements": [
            {
                "id": generate_id(),
                "settings": {
                    "_column_size": 100,
                    "_inline_size": None
                },
                "elements": elements,
                "isInner": False,
                "elType": "column"
            }
        ],
        "isInner": False,
        "elType": "section"
    }

def create_elementor_template(css, body_html):
    """Create full Elementor template structure."""

    content = []

    # 1. CSS Section (full width reset + custom styles)
    css_widget = create_html_widget(f"<style>\n{css}\n</style>")
    content.append(create_section([css_widget]))

    # 2. Main content as single HTML widget
    # Wrap in container for proper styling
    main_html = f"""<div class="gg-neo-brutalist-page">
{body_html}
</div>"""

    main_widget = create_html_widget(main_html, "gg-main-content")
    content.append(create_section([main_widget], {
        "layout": "full_width",
        "css_classes": "gg-page-wrapper"
    }))

    # Build full template
    template = {
        "content": content,
        "page_settings": {
            "hide_title": "yes",
            "template": "elementor_canvas"
        },
        "version": "0.4",
        "title": "Neo-Brutalist Landing Page Template",
        "type": "page"
    }

    return template

def add_placeholders(html_content):
    """Replace Unbound-specific content with placeholders."""

    replacements = [
        # Race basics
        (r'Unbound Gravel 200', '{{RACE_NAME}}'),
        (r'Unbound 200', '{{RACE_NAME}}'),
        (r'Unbound', '{{RACE_NAME_SHORT}}'),
        (r'Emporia, Kansas', '{{LOCATION}}'),
        (r'Emporia', '{{CITY}}'),
        (r'Kansas', '{{STATE}}'),

        # Scores (keep specific for now, parameterize later)
        (r'88<span>/100</span>', '{{OVERALL_SCORE}}<span>/100</span>'),
        (r'22 / 35', '{{COURSE_PROFILE_SCORE}} / 35'),
        (r'33 / 35', '{{BIASED_OPINION_SCORE}} / 35'),
        (r'22<span>/35</span>', '{{COURSE_PROFILE_SCORE}}<span>/35</span>'),
        (r'33<span>/35</span>', '{{BIASED_OPINION_SCORE}}<span>/35</span>'),

        # URLs
        (r'https://unboundgravel\.com', '{{OFFICIAL_RACE_URL}}'),
        (r'race=unbound-gravel-200', 'race={{RACE_SLUG}}'),

        # Specific content markers for batch replacement
        (r'TIER 1 / HIGH CONSEQUENCE', '{{TIER_LABEL}}'),
        (r'First Saturday in June', '{{RACE_DATE}}'),
        (r'202\.4 miles', '{{DISTANCE}} miles'),
        (r'200 miles', '{{DISTANCE}} miles'),
        (r'202 miles', '{{DISTANCE}} miles'),
    ]

    result = html_content
    for pattern, replacement in replacements:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

    return result

def main():
    # Paths
    mockup_path = Path(__file__).parent / 'mockups' / 'neo-brutalist-mockup.html'
    output_unbound = Path(__file__).parent.parent / 'Unbound' / 'landing-page' / 'elementor-unbound-200-neo.json'
    output_template = Path(__file__).parent / 'templates' / 'template-neo-brutalist.json'

    print(f"Reading mockup: {mockup_path}")

    # Read mockup
    with open(mockup_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Extract CSS and body
    css, body_html = extract_css_and_body(html_content)

    print(f"Extracted {len(css)} chars of CSS")
    print(f"Extracted {len(body_html)} chars of body HTML")

    # Create Unbound-specific template (no placeholders)
    unbound_template = create_elementor_template(css, body_html)

    # Save Unbound template
    output_unbound.parent.mkdir(parents=True, exist_ok=True)
    with open(output_unbound, 'w', encoding='utf-8') as f:
        json.dump(unbound_template, f, indent=2, ensure_ascii=False)
    print(f"Saved Unbound template: {output_unbound}")

    # Create generic template with placeholders
    body_with_placeholders = add_placeholders(body_html)
    css_with_placeholders = add_placeholders(css)
    generic_template = create_elementor_template(css_with_placeholders, body_with_placeholders)
    generic_template['title'] = 'Neo-Brutalist Landing Page Template (Generic)'

    # Save generic template
    output_template.parent.mkdir(parents=True, exist_ok=True)
    with open(output_template, 'w', encoding='utf-8') as f:
        json.dump(generic_template, f, indent=2, ensure_ascii=False)
    print(f"Saved generic template: {output_template}")

    print("\nDone! Templates created:")
    print(f"  1. Unbound-specific: {output_unbound}")
    print(f"  2. Generic template: {output_template}")

if __name__ == '__main__':
    main()
