#!/usr/bin/env python3
"""
Push Unbound 200 Landing Page to WordPress

Usage:
    python push_unbound_200.py          # Create new page
    python push_unbound_200.py update   # Update existing page (ID 4825)
"""
import json
import sys
import os
import requests

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from push_pages import WordPressPagePusher, WP_CONFIG

# Page ID for updates
PAGE_ID = 4825
PAGE_URL = "https://gravelgodcycling.com/unbound-gravel-200-race-guide/"

# Load the Unbound 200 Elementor template
TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'Unbound/landing-page/elementor-unbound-200.json'
)

with open(TEMPLATE_PATH, 'r') as f:
    template = json.load(f)

# Initialize pusher
pusher = WordPressPagePusher(
    wordpress_url=WP_CONFIG['site_url'],
    username=WP_CONFIG['username'],
    password=WP_CONFIG['app_password']
)

# Extract Elementor content and settings
elementor_content = template.get('content', [])
page_settings = template.get('page_settings', {})
elementor_data_str = json.dumps(elementor_content, ensure_ascii=False)

print("Unbound 200 Landing Page Push")
print(f"Template: {TEMPLATE_PATH}")
print(f"Elementor data: {len(elementor_data_str):,} chars")

# Prepare payload with explicit Elementor meta
payload = {
    'title': 'Unbound Gravel 200 Race Guide',
    'slug': 'unbound-gravel-200-race-guide',
    'status': 'publish',
    'meta': {
        '_elementor_edit_mode': 'builder',
        '_elementor_template_type': 'wp-page',
        '_elementor_data': elementor_data_str,
        '_elementor_version': '0.4',
        '_elementor_pro_version': '',
        '_elementor_page_settings': page_settings
    }
}

try:
    mode = sys.argv[1] if len(sys.argv) > 1 else 'update'

    if mode == 'update':
        print(f"\nUpdating page {PAGE_ID}...")
        url = f'{pusher.api_url}/pages/{PAGE_ID}'
        response = pusher.session.post(url, json=payload)
    else:
        print("\nCreating new page...")
        url = f'{pusher.api_url}/pages'
        response = pusher.session.post(url, json=payload)

    if response.status_code in [200, 201]:
        result = response.json()
        page_id = result.get('id')
        page_url = result.get('link')

        print(f"✓ Page {'updated' if mode == 'update' else 'created'}: ID {page_id}")
        print(f"✓ URL: {page_url}")

        # Regenerate CSS
        print("\nRegenerating Elementor CSS...")
        css_result = pusher.regenerate_elementor_css(page_id)
        if css_result and css_result.get('success'):
            print(f"✓ CSS regenerated")
        else:
            print("⚠ CSS regeneration may have failed")

        # Verify content
        print("\nContent verification:")
        verify_response = requests.get(page_url)
        checks = [
            ('gg-hero', 'Hero section'),
            ('gg-vitals', 'Race vitals'),
            ('gg-blackpill', 'Black pill section'),
            ('gg-volume-section', 'Training plans'),
        ]
        for css_class, name in checks:
            if css_class in verify_response.text:
                print(f"  ✓ {name}")
            else:
                print(f"  ✗ {name} NOT found")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text[:500])

except Exception as e:
    print(f"\n✗ Error: {e}")
    raise
