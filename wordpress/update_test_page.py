#!/usr/bin/env python3
"""
Update existing test page with new template - Debug version
"""
import json
from push_pages import WordPressPagePusher, WP_CONFIG

# Page ID from previous test
PAGE_ID = 4814

# Load template
with open('templates/template-master-fixed.json', 'r') as f:
    template = json.load(f)

# Race data for Mid South (same as before)
race_data = {
    "race_name": "Mid South",
    "location": "Stillwater, Oklahoma",
    "distance": "100",
    "city": "Stillwater",
    "race_tagline": "Oklahoma's weather lottery with a $100K prize purse and a guaranteed Bobby hug.",
    "map_embed_url": "https://ridewithgps.com/embeds?type=route&id=48969927&title=Mid%20South%202026%20100%20Mile&sampleGraph=true&distanceMarkers=true"
}

# Initialize pusher
pusher = WordPressPagePusher(
    wordpress_url=WP_CONFIG['site_url'],
    username=WP_CONFIG['username'],
    password=WP_CONFIG['app_password']
)

# Replace placeholders
page_content = pusher.replace_placeholders(template, race_data)

# Check if the new content has our changes
elementor_data = page_content.get('meta', {}).get('_elementor_data', '')
if 'gg-stat-row' in elementor_data:
    print("✓ Template contains stat row")
else:
    print("✗ Template missing stat row!")

if 'gg-topnav-toggle' in elementor_data:
    print("✓ Template contains mobile nav toggle")
else:
    print("✗ Template missing mobile nav toggle!")

if 'gg-inline-quote' in elementor_data:
    print("✓ Template contains inline quote")
else:
    print("✗ Template missing inline quote!")

# Format for WordPress REST API
formatted = pusher._format_page_data(page_content)

# Debug: Show what we're sending
print(f"\nMeta fields being sent:")
for key in formatted.get('meta', {}).keys():
    value = formatted['meta'][key]
    if isinstance(value, str) and len(value) > 100:
        print(f"  {key}: [{len(value)} chars]")
    else:
        print(f"  {key}: {value}")

print(f"\nUpdating page {PAGE_ID}...")

# Update the page
import requests
url = f"{pusher.api_url}/pages/{PAGE_ID}"
response = pusher.session.post(url, json=formatted)

print(f"Response status: {response.status_code}")
if response.status_code != 200:
    print(f"Error: {response.text[:500]}")
else:
    result = response.json()
    print(f"✓ Page updated: {result.get('link', 'unknown')}")

    # Check what meta was actually saved
    print("\nVerifying saved meta...")
    get_response = pusher.session.get(f"{url}?context=edit")
    if get_response.status_code == 200:
        saved = get_response.json()
        saved_meta = saved.get('meta', {})
        if '_elementor_data' in saved_meta:
            data = saved_meta['_elementor_data']
            if 'gg-stat-row' in str(data):
                print("✓ Stat row saved to WordPress")
            else:
                print("✗ Stat row NOT in saved data")
            if 'gg-topnav-toggle' in str(data):
                print("✓ Mobile nav toggle saved to WordPress")
            else:
                print("✗ Mobile nav toggle NOT in saved data")

# Regenerate CSS
print("\nRegenerating Elementor CSS...")
css_result = pusher.regenerate_elementor_css(PAGE_ID)
if css_result:
    print(f"✓ CSS regenerated successfully")
else:
    print("⚠ CSS regeneration may have failed")

print(f"\nView page: https://gravelgodcycling.com/the-mid-south-gravel-race-guide-4/")
