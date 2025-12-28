#!/usr/bin/env python3
"""
Push Neo-Brutalist Unbound 200 Landing Page to WordPress

Usage:
    python push_unbound_neo.py          # Update existing page
    python push_unbound_neo.py create   # Create new page for testing
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from push_pages import WordPressPagePusher, WP_CONFIG

# Page ID for the live Unbound page
PAGE_ID = 4846
PAGE_URL = "https://gravelgodcycling.com/unbound-gravel-200-race-guide/"

# Template path - Neo-Brutalist version
TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'Unbound/landing-page/elementor-unbound-200-neo.json'
)

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'update'

    # Load template
    print(f"Loading template: {TEMPLATE_PATH}")
    with open(TEMPLATE_PATH, 'r') as f:
        template = json.load(f)

    # Initialize pusher
    pusher = WordPressPagePusher(
        wordpress_url=WP_CONFIG['site_url'],
        username=WP_CONFIG['username'],
        password=WP_CONFIG['app_password']
    )

    # Set page metadata
    page_content = template.copy()
    page_content['title'] = 'Unbound Gravel 200 Race Guide'
    page_content['slug'] = 'unbound-gravel-200-race-guide'
    page_content['status'] = 'publish'

    print("\n" + "="*60)
    print("NEO-BRUTALIST UNBOUND 200 PUSH")
    print("="*60)
    print(f"Template: {TEMPLATE_PATH}")
    print(f"Mode: {mode}")
    print(f"Target: {PAGE_URL}")
    print("="*60)

    try:
        if mode == 'update' and PAGE_ID:
            print(f"\nUpdating page {PAGE_ID}...")

            # Build page data in the format expected by _format_page_data
            elementor_content = page_content.get('content', [])
            page_settings = page_content.get('page_settings', {})
            elementor_data_str = json.dumps(elementor_content, ensure_ascii=False)

            page_data = {
                'title': page_content['title'],
                'content': '',  # Empty content - Elementor renders from _elementor_data
                'template': 'elementor_canvas',
                'meta': {
                    '_elementor_edit_mode': 'builder',
                    '_elementor_template_type': 'wp-page',
                    '_elementor_data': elementor_data_str,
                    '_elementor_version': '3.25.10',
                    '_elementor_page_settings': page_settings,
                    '_wp_page_template': 'elementor_canvas',
                    '_elementor_css': ''  # Force CSS regeneration
                }
            }

            # Use the pusher's format function
            formatted = pusher._format_page_data(page_data)

            url = f'{pusher.api_url}/pages/{PAGE_ID}'
            response = pusher.session.post(url, json=formatted)

            if response.status_code in [200, 201]:
                result = response.json()
                print(f"\n✓ Page updated successfully!")
                print(f"  ID: {result.get('id')}")
                print(f"  URL: {result.get('link')}")

                # Verify the update took effect
                print("\nVerifying saved meta...")
                get_response = pusher.session.get(f"{url}?context=edit")
                if get_response.status_code == 200:
                    saved = get_response.json()
                    saved_meta = saved.get('meta', {})
                    if '_elementor_data' in saved_meta:
                        data = str(saved_meta['_elementor_data'])
                        if 'gg-neo-brutalist' in data:
                            print("  ✓ Neo-Brutalist content saved to WordPress")
                        else:
                            print("  ✗ Neo-Brutalist content NOT in saved data")
                            print("    Note: WordPress REST API may not allow _elementor_data updates")
                    else:
                        print("  ✗ _elementor_data not in response (not exposed to REST API)")

                # Regenerate CSS
                print("\nRegenerating Elementor CSS...")
                pusher.regenerate_elementor_css(PAGE_ID)
                print("✓ CSS regenerated")
            else:
                print(f"\n✗ Error: {response.status_code}")
                print(response.text[:500])
                sys.exit(1)

        elif mode == 'create':
            print("\nCreating new test page...")

            # Format properly like update mode
            elementor_content = page_content.get('content', [])
            page_settings = page_content.get('page_settings', {})
            elementor_data_str = json.dumps(elementor_content, ensure_ascii=False)

            payload = {
                'title': 'Unbound Gravel 200 Race Guide - Neo Test',
                'slug': 'unbound-gravel-200-race-guide-neo-test',
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
                print(f"\n✓ Test page created!")
                print(f"  ID: {result.get('id')}")
                print(f"  URL: {result.get('link')}")

                # Regenerate CSS
                print("\nRegenerating Elementor CSS...")
                pusher.regenerate_elementor_css(result.get('id'))
                print("✓ CSS regenerated")
            else:
                print(f"\n✗ Error: {response.status_code}")
                print(response.text[:500])
                sys.exit(1)

            print(f"\nTo update the live page, run:")
            print(f"  python push_unbound_neo.py update")

        elif mode == 'replace':
            # Delete old page and create new one with same slug to bypass cache
            print(f"\nReplacing page {PAGE_ID} (delete + create fresh)...")

            # First, get the old page info
            get_url = f'{pusher.api_url}/pages/{PAGE_ID}'
            get_response = pusher.session.get(get_url)
            if get_response.status_code == 200:
                old_page = get_response.json()
                old_slug = old_page.get('slug', 'unbound-gravel-200-race-guide')
                print(f"  Old page slug: {old_slug}")
            else:
                old_slug = 'unbound-gravel-200-race-guide'

            # Delete the old page
            print(f"\n  Deleting old page {PAGE_ID}...")
            delete_url = f'{pusher.api_url}/pages/{PAGE_ID}?force=true'
            delete_response = pusher.session.delete(delete_url)
            if delete_response.status_code in [200, 410]:
                print(f"  ✓ Old page deleted")
            else:
                print(f"  ⚠ Delete returned {delete_response.status_code}: {delete_response.text[:200]}")

            # Create new page with same slug
            print(f"\n  Creating new page with slug '{old_slug}'...")
            elementor_content = page_content.get('content', [])
            page_settings = page_content.get('page_settings', {})
            elementor_data_str = json.dumps(elementor_content, ensure_ascii=False)

            payload = {
                'title': 'Unbound Gravel 200 Race Guide',
                'slug': old_slug,
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
                new_page_id = result.get('id')
                print(f"\n✓ New page created!")
                print(f"  ID: {new_page_id}")
                print(f"  URL: {result.get('link')}")

                # Regenerate CSS
                print("\nRegenerating Elementor CSS...")
                pusher.regenerate_elementor_css(new_page_id)
                print("✓ CSS regenerated")

                print(f"\n⚠ NOTE: Update PAGE_ID in this script to {new_page_id} for future updates")
            else:
                print(f"\n✗ Error creating new page: {response.status_code}")
                print(response.text[:500])
                sys.exit(1)

        else:
            print(f"Unknown mode: {mode}")
            print("Usage: python push_unbound_neo.py [update|create|replace]")
            sys.exit(1)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise

    print("\n" + "="*60)
    print("DONE")
    print("="*60)

if __name__ == '__main__':
    main()
