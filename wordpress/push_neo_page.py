#!/usr/bin/env python3
"""
Push a generated Neo-Brutalist page to WordPress

Usage:
    python push_neo_page.py ned-gravel           # Push specific race
    python push_neo_page.py --fix-hub-colors     # Fix gravel-races hub page colors
"""
import json
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from push_pages import WordPressPagePusher, WP_CONFIG

# Race page IDs mapping (for updates)
RACE_PAGE_IDS = {
    'ned-gravel': None,  # Will create if None
    # Add known page IDs here
}

# Gravel races hub page ID
HUB_PAGE_ID = 4871

def get_template_path(race_slug):
    """Get path to generated Neo-Brutalist template for a race."""
    # Convert slug to directory name (e.g., ned-gravel -> Ned-Gravel)
    parts = race_slug.split('-')
    dir_name = '-'.join(word.capitalize() for word in parts)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, dir_name, 'landing-page', f'elementor-{race_slug}-neo.json')


def push_race_page(race_slug, mode='replace'):
    """Push a race's Neo-Brutalist page to WordPress."""
    template_path = get_template_path(race_slug)

    if not os.path.exists(template_path):
        print(f"Template not found: {template_path}")
        print(f"Run: python wordpress/generate_neo_brutalist.py {race_slug}")
        sys.exit(1)

    print(f"Loading template: {template_path}")
    with open(template_path, 'r') as f:
        template = json.load(f)

    # Initialize pusher
    pusher = WordPressPagePusher(
        wordpress_url=WP_CONFIG['site_url'],
        username=WP_CONFIG['username'],
        password=WP_CONFIG['app_password']
    )

    # Build page slug and title
    display_name = template.get('page_settings', {}).get('race_display_name',
                     race_slug.replace('-', ' ').title())
    page_slug = f"{race_slug}-race-guide"
    page_title = f"{display_name} Race Guide"

    print("\n" + "="*60)
    print(f"PUSHING: {page_title}")
    print("="*60)

    # Format page data
    elementor_content = template.get('content', [])
    page_settings = template.get('page_settings', {})
    elementor_data_str = json.dumps(elementor_content, ensure_ascii=False)

    payload = {
        'title': page_title,
        'slug': page_slug,
        'status': 'publish',
        'template': 'elementor_canvas',
        'meta': {
            '_elementor_edit_mode': 'builder',
            '_elementor_template_type': 'wp-page',
            '_elementor_data': elementor_data_str,
            '_elementor_version': '3.25.10',
            '_elementor_page_settings': page_settings,
            '_wp_page_template': 'elementor_canvas'
        }
    }

    url = f'{pusher.api_url}/pages'
    response = pusher.session.post(url, json=payload)

    if response.status_code in [200, 201]:
        result = response.json()
        print(f"\n Page pushed successfully!")
        print(f"  ID: {result.get('id')}")
        print(f"  URL: {result.get('link')}")

        # Regenerate CSS
        pusher.regenerate_elementor_css(result.get('id'))
        print("  CSS regenerated")
        return result.get('id')
    else:
        print(f"\n Error: {response.status_code}")
        print(response.text[:500])
        sys.exit(1)


def fix_hub_colors():
    """Fix the gravel-races hub page to use correct brand colors."""
    print("\n" + "="*60)
    print("FIXING GRAVEL-RACES HUB PAGE COLORS")
    print("="*60)

    # Brand colors
    WRONG_TURQUOISE = '#5DADE2'
    CORRECT_TURQUOISE = '#4ECDC4'

    # Initialize pusher
    pusher = WordPressPagePusher(
        wordpress_url=WP_CONFIG['site_url'],
        username=WP_CONFIG['username'],
        password=WP_CONFIG['app_password']
    )

    # Fetch current page
    print(f"Fetching page {HUB_PAGE_ID}...")
    url = f'{pusher.api_url}/pages/{HUB_PAGE_ID}?context=edit'
    response = pusher.session.get(url)

    if response.status_code != 200:
        print(f"Error fetching page: {response.status_code}")
        sys.exit(1)

    page = response.json()
    meta = page.get('meta', {})
    elementor_data = meta.get('_elementor_data', '')

    if isinstance(elementor_data, str):
        # Check for wrong color
        if WRONG_TURQUOISE.lower() in elementor_data.lower():
            print(f"Found wrong color {WRONG_TURQUOISE}, replacing with {CORRECT_TURQUOISE}")
            # Replace color (case insensitive)
            elementor_data = re.sub(
                re.escape(WRONG_TURQUOISE),
                CORRECT_TURQUOISE,
                elementor_data,
                flags=re.IGNORECASE
            )

            # Update page
            update_payload = {
                'meta': {
                    '_elementor_data': elementor_data,
                    '_elementor_css': ''  # Force CSS regeneration
                }
            }

            update_url = f'{pusher.api_url}/pages/{HUB_PAGE_ID}'
            update_response = pusher.session.post(update_url, json=update_payload)

            if update_response.status_code in [200, 201]:
                print(f" Colors fixed!")
                pusher.regenerate_elementor_css(HUB_PAGE_ID)
                print("  CSS regenerated")
            else:
                print(f"Error updating: {update_response.status_code}")
                print(update_response.text[:500])
        else:
            print(f"Color {WRONG_TURQUOISE} not found in page data")
            # Check what colors ARE in the page
            colors_found = re.findall(r'#[0-9A-Fa-f]{6}', elementor_data[:5000])
            if colors_found:
                print(f"Colors found in page: {set(colors_found)}")
    else:
        print("Could not get Elementor data from page")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python push_neo_page.py <race-slug>    # Push a race page")
        print("  python push_neo_page.py --fix-hub-colors  # Fix hub page colors")
        sys.exit(1)

    arg = sys.argv[1]

    if arg == '--fix-hub-colors':
        fix_hub_colors()
    else:
        push_race_page(arg)

    print("\n" + "="*60)
    print("DONE")
    print("="*60)


if __name__ == '__main__':
    main()
