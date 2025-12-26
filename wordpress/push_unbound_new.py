#!/usr/bin/env python3
"""
Push Unbound 200 Landing Page using template-master-fixed.json format
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from push_pages import WordPressPagePusher, WP_CONFIG

# Load the Unbound-specific template with race data from research brief
TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'templates/template-unbound-200.json'
)

with open(TEMPLATE_PATH, 'r') as f:
    template = json.load(f)

# Unbound 200 race data
race_data = {
    "race_name": "Unbound Gravel 200",
    "location": "Emporia, Kansas",
    "distance": "200",
    "city": "Emporia",
    "race_tagline": "You don't race Unbound. You survive it.",
    "map_embed_url": "https://ridewithgps.com/embeds?type=route&id=46551378&title=Unbound%20200&sampleGraph=true&distanceMarkers=true",
    "race_slug": "unbound-gravel-200"
}

# Initialize pusher
pusher = WordPressPagePusher(
    wordpress_url=WP_CONFIG['site_url'],
    username=WP_CONFIG['username'],
    password=WP_CONFIG['app_password']
)

# Replace placeholders
page_content = pusher.replace_placeholders(template, race_data)

# Set page details
page_content['title'] = 'Unbound Gravel 200 Race Guide - New Format'
page_content['slug'] = 'unbound-gravel-200-race-guide-new'
page_content['status'] = 'publish'

print("Creating Unbound 200 page with new template format...")
print(f"Template: {TEMPLATE_PATH}")

try:
    result = pusher.create_page(page_content, regenerate_css=True)

    page_id = result.get('id')
    page_url = result.get('link')

    print(f"\n✓ Page created: ID {page_id}")
    print(f"✓ URL: {page_url}")

    # Verify content
    import requests
    response = requests.get(page_url)

    checks = [
        ('gg-tier-overview', 'Tier overview'),
        ('gg-tier-section', 'Tier sections'),
        ('gg-plans-grid', 'Plans grid'),
        ('gg-training-section', 'Training section'),
    ]

    print("\nContent verification:")
    for css_class, name in checks:
        if css_class in response.text:
            print(f"  ✓ {name}")
        else:
            print(f"  ✗ {name} NOT found")

except Exception as e:
    print(f"\n✗ Error: {e}")
    raise
