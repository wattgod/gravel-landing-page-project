#!/usr/bin/env python3
"""
Create a NEW test page with the updated template
"""
import json
from push_pages import WordPressPagePusher, WP_CONFIG

# Load template
with open('templates/template-master-fixed.json', 'r') as f:
    template = json.load(f)

# Race data for Mid South
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

# Set page details - NEW SLUG to create fresh page
page_content['title'] = 'Mid South Gravel Race Guide - V2'
page_content['slug'] = 'mid-south-gravel-race-guide-v2'
page_content['status'] = 'publish'

print("Creating NEW page with updated template...")
result = pusher.create_page(page_content, regenerate_css=True)

page_id = result.get('id')
page_url = result.get('link')

print(f"✓ Page created: ID {page_id}")
print(f"✓ URL: {page_url}")

# Verify content
import requests
response = requests.get(page_url)
if 'gg-stat-row' in response.text:
    print("✓ Stat row is rendering!")
else:
    print("✗ Stat row NOT in rendered HTML")

if 'gg-topnav-toggle' in response.text:
    print("✓ Mobile nav toggle is rendering!")
else:
    print("✗ Mobile nav toggle NOT in rendered HTML")
