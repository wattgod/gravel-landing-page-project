#!/usr/bin/env python3
"""
Push Unbound 200 Landing Page to WordPress

CORRECT USAGE:
    python push_unbound_200.py          # Update existing page
    python push_unbound_200.py create   # Create new page

This script demonstrates the CORRECT way to push a race page:
1. Load template
2. Define race data
3. Call replace_placeholders() to fill in race-specific content
4. Call create_page() which validates before pushing
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from push_pages import WordPressPagePusher, WP_CONFIG

# Page ID for updates (set after first creation)
# NOTE: Updating existing Elementor pages via REST API is unreliable.
# For major changes, delete and recreate the page instead.
PAGE_ID = 4840
PAGE_URL = "https://gravelgodcycling.com/unbound-gravel-200-race-guide/"

# Template path - using the race-specific template
TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'Unbound/landing-page/elementor-unbound-200.json'
)

# Unbound 200 race data for placeholder replacement
RACE_DATA = {
    'race_name': 'Unbound Gravel 200',
    'location': 'Emporia, Kansas',
    'city': 'Emporia',
    'distance': '200',
    'race_tagline': "You don't race Unbound. You survive it.",
    'race_slug': 'unbound-gravel-200',
    'map_embed_url': 'https://ridewithgps.com/embeds?type=route&id=46551378&title=Unbound%20200&sampleGraph=true&distanceMarkers=true',
}


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'update'

    # Load template
    with open(TEMPLATE_PATH, 'r') as f:
        template = json.load(f)

    # Initialize pusher
    pusher = WordPressPagePusher(
        wordpress_url=WP_CONFIG['site_url'],
        username=WP_CONFIG['username'],
        password=WP_CONFIG['app_password']
    )

    # IMPORTANT: Replace placeholders before pushing
    # This ensures all {{PLACEHOLDER}} values are filled in
    page_content = pusher.replace_placeholders(template, RACE_DATA)

    # Set page metadata
    page_content['title'] = 'Unbound Gravel 200 Race Guide'
    page_content['slug'] = 'unbound-gravel-200-race-guide'
    page_content['status'] = 'publish'

    print("Unbound 200 Landing Page Push")
    print(f"Template: {TEMPLATE_PATH}")
    print(f"Mode: {mode}")

    try:
        if mode == 'update' and PAGE_ID:
            # Update existing page
            print(f"\nUpdating page {PAGE_ID}...")

            # Validate before push (create_page does this, but update needs manual call)
            pusher.validate_before_push(page_content)

            # Format and push
            elementor_content = page_content.get('content', [])
            page_settings = page_content.get('page_settings', {})
            elementor_data_str = json.dumps(elementor_content, ensure_ascii=False)

            payload = {
                'title': page_content['title'],
                'meta': {
                    '_elementor_edit_mode': 'builder',
                    '_elementor_template_type': 'wp-page',
                    '_elementor_data': elementor_data_str,
                    '_elementor_version': '3.25.10',
                    '_elementor_page_settings': page_settings
                }
            }

            url = f'{pusher.api_url}/pages/{PAGE_ID}'
            response = pusher.session.post(url, json=payload)

            if response.status_code in [200, 201]:
                result = response.json()
                print(f"✓ Page updated: ID {result.get('id')}")
                print(f"✓ URL: {result.get('link')}")

                # Regenerate CSS
                pusher.regenerate_elementor_css(PAGE_ID)
            else:
                print(f"✗ Error: {response.status_code}")
                print(response.text[:500])
        else:
            # Create new page - validation happens automatically in create_page()
            print("\nCreating new page...")
            result = pusher.create_page(page_content, regenerate_css=True)

            print(f"✓ Page created: ID {result.get('id')}")
            print(f"✓ URL: {result.get('link')}")
            print(f"\nUpdate PAGE_ID in this script to: {result.get('id')}")

    except ValueError as e:
        # Validation failed
        print(f"\n✗ VALIDATION ERROR:\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise


if __name__ == '__main__':
    main()
