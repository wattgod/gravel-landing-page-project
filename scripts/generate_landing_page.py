#!/usr/bin/env python3
"""
Gravel God Landing Page Generator
Generates complete Elementor JSON from race data schema.

All section generators are now imported from automation modules.
This file handles only:
- Loading race data
- Calling section generators
- Building Elementor JSON
- Widget replacement
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from html import unescape

# Add automation module to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import all section generators from automation modules
# NEW: On-demand training plans section (single CTA to questionnaire)
from automation.training_plans_section import generate_training_plans_html as generate_training_plans_section_html
from automation.blackpill import generate_blackpill_html
from automation.generate_landing_page_index import generate_index
from automation.hero import generate_hero_html
from automation.vitals import generate_vitals_html
from automation.ratings import generate_ratings_html
from automation.course_map import generate_course_map_html
from automation.overview_hero import generate_overview_hero_html
from automation.tldr import generate_tldr_html
from automation.history import generate_history_html
from automation.biased_opinion import generate_biased_opinion_html
from automation.final_verdict import generate_final_verdict_html
from automation.logistics import generate_logistics_html
from automation.ctas import generate_coaching_cta_html, generate_gravel_races_cta_html


def load_race_data(json_path: str) -> Dict[str, Any]:
    """Load race data schema from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_training_plans_html(data: Dict) -> str:
    """
    Generate training plans section using on-demand model.
    Single CTA pointing to questionnaire instead of 15 tier cards.
    """
    return generate_training_plans_section_html(data)


def find_widget_by_content(elements: List[Dict], search_pattern: str) -> Optional[Dict]:
    """Find HTML widget by searching for content pattern in HTML."""
    for element in elements:
        if element.get('widgetType') == 'html':
            settings = element.get('settings', {})
            if isinstance(settings, dict):
                html = settings.get('html', '')
                if search_pattern in html:
                    return element
        if 'elements' in element:
            result = find_widget_by_content(element['elements'], search_pattern)
            if result:
                return result
    return None


def find_widget_by_element_id(elements: List[Dict], target_id: str) -> Optional[Dict]:
    """Find widget by _element_id in settings."""
    for element in elements:
        settings = element.get('settings', {})
        if isinstance(settings, dict) and settings.get('_element_id') == target_id:
            return element
        if 'elements' in element:
            result = find_widget_by_element_id(element['elements'], target_id)
            if result:
                return result
    return None


def replace_widget_html(elementor_json: Dict, search_pattern: str, new_html: str, element_id: Optional[str] = None) -> bool:
    """Find and replace HTML widget content. Returns True if found and replaced."""
    elements = elementor_json.get('content', [])
    
    # Try element ID first if provided
    if element_id:
        widget = find_widget_by_element_id(elements, element_id)
        if widget:
            settings = widget.get('settings', {})
            if isinstance(settings, dict):
                settings['html'] = new_html
                return True
    
    # Fall back to content pattern search
    widget = find_widget_by_content(elements, search_pattern)
    if widget:
        settings = widget.get('settings', {})
        if isinstance(settings, dict):
            settings['html'] = new_html
            return True
    
    return False


def build_elementor_json(data: Dict, base_json_path: str) -> Dict:
    """Build complete Elementor JSON with all sections."""
    # Load base JSON structure
    with open(base_json_path, 'r', encoding='utf-8') as f:
        elementor_data = json.load(f)
    
    # Generate all HTML sections
    print("  Generating hero section...")
    hero_html = generate_hero_html(data)
    
    print("  Generating vitals section...")
    vitals_html = generate_vitals_html(data)
    
    print("  Generating ratings section...")
    ratings_html = generate_ratings_html(data)
    
    print("  Generating black pill section...")
    blackpill_html = generate_blackpill_html(data)
    
    print("  Generating training plans section...")
    training_html = generate_training_plans_html(data)
    
    print("  Generating course map section...")
    course_map_html = generate_course_map_html(data)
    
    print("  Generating overview hero section...")
    overview_html = generate_overview_hero_html(data)
    
    print("  Generating TLDR section...")
    tldr_html = generate_tldr_html(data)
    
    print("  Generating history section...")
    history_html = generate_history_html(data)
    
    print("  Generating biased opinion section...")
    opinion_html = generate_biased_opinion_html(data)
    
    print("  Generating final verdict section...")
    verdict_html = generate_final_verdict_html(data)
    
    print("  Generating logistics section...")
    logistics_html = generate_logistics_html(data)
    
    print("  Generating coaching CTA...")
    coaching_cta_html = generate_coaching_cta_html()
    
    print("  Generating gravel races CTA...")
    gravel_races_cta_html = generate_gravel_races_cta_html()
    
    # Find and replace widgets in Elementor JSON
    print("  Replacing hero widget...")
    if not replace_widget_html(elementor_data, 'gg-hero-inner', hero_html):
        print("  WARNING: Hero widget not found!")
    
    print("  Replacing vitals widget...")
    if not replace_widget_html(elementor_data, 'id="race-vitals"', vitals_html, element_id='vitals'):
        print("  WARNING: Vitals widget not found!")
    
    print("  Replacing ratings widget...")
    if not replace_widget_html(elementor_data, 'id="course-ratings"', ratings_html, element_id='course'):
        print("  WARNING: Ratings widget not found!")
    
    print("  Replacing black pill widget...")
    if not replace_widget_html(elementor_data, 'gg-blackpill-section', blackpill_html, element_id='blackpill'):
        print("  WARNING: Black pill widget not found!")
    
    print("  Replacing training plans widget...")
    if not replace_widget_html(elementor_data, 'gg-volume-section', training_html, element_id='training'):
        print("  WARNING: Training plans widget not found!")
    
    print("  Replacing course map widget...")
    if not replace_widget_html(elementor_data, 'gg-route-section', course_map_html, element_id='course-map'):
        print("  WARNING: Course map widget not found!")
    
    print("  Replacing overview hero widget...")
    if not replace_widget_html(elementor_data, 'gg-overview-hero-v2', overview_html):
        print("  WARNING: Overview hero widget not found!")
    
    print("  Replacing TLDR widget...")
    if not replace_widget_html(elementor_data, 'gg-decision-grid', tldr_html, element_id='tldr'):
        print("  WARNING: TLDR widget not found!")
    
    print("  Replacing history widget...")
    if not replace_widget_html(elementor_data, 'gg-tldr-grid', history_html, element_id='history'):
        print("  WARNING: History widget not found!")
    
    print("  Replacing biased opinion widget...")
    if not replace_widget_html(elementor_data, 'gg-opinion-section', opinion_html, element_id='opinion'):
        print("  WARNING: Biased opinion widget not found!")
    
    print("  Replacing final verdict widget...")
    if not replace_widget_html(elementor_data, 'gg-overall-section', verdict_html, element_id='verdict'):
        print("  WARNING: Final verdict widget not found!")
    
    print("  Replacing logistics widget...")
    # Append CTAs directly to logistics HTML (simpler approach)
    logistics_html += '\n\n' + coaching_cta_html + '\n\n' + gravel_races_cta_html
    
    if not replace_widget_html(elementor_data, 'gg-logistics-section', logistics_html, element_id='logistics'):
        print("  WARNING: Logistics widget not found!")
    
    # Update page title
    race_name = data['race']['display_name']
    elementor_data['title'] = f"{race_name} Landing Page"
    
    # Add neo brutalist CSS to page_settings.custom_css
    if 'page_settings' in elementor_data and 'custom_css' in elementor_data['page_settings']:
        with open('assets/css/landing-page.css', 'r', encoding='utf-8') as f:
            neo_brutalist_css = f.read()
        # Append to existing CSS
        elementor_data['page_settings']['custom_css'] += '\n\n' + neo_brutalist_css
    
    return elementor_data


def generate_wordpress_config(data: Dict) -> str:
    """
    Generate WordPress Quick Config block for easy copy-paste.
    
    RULE: After generating any landing page JSON, ALWAYS output this block.
    """
    race = data['race']
    race_name = race['display_name']
    race_slug = race.get('slug', race_name.lower().replace(' ', '-'))
    
    # Extract location info
    location_full = race['vitals']['location']
    city = location_full.split(',')[0].strip()
    state = location_full.split(',')[1].strip() if ',' in location_full else ''
    
    # Extract distance
    distance = race['vitals']['distance_mi']
    distance_str = f"{distance}-mile" if isinstance(distance, (int, float)) else str(distance)
    
    # Get defining challenge from race_challenge_tagline or signature_challenge
    challenge = race.get('race_challenge_tagline', '') or race.get('course_description', {}).get('signature_challenge', '')
    
    # Get hook from tagline or biased_opinion quote
    hook = race.get('tagline', '') or race.get('biased_opinion', {}).get('quote', '')
    
    # Build meta description (must be ≤160 chars)
    # Try to include hook if it's short enough
    base = f"{race_name} {city} guide: {distance_str} {state} gravel race"
    
    # Add challenge if short
    if challenge and len(challenge) < 40:
        base += f" at {challenge}"
    
    # Add hook if it fits
    if hook:
        hook_short = hook[:50] if len(hook) > 50 else hook
        test_desc = f"{base}. {hook_short}. Get training plans & course breakdown."
        if len(test_desc) <= 160:
            meta_desc = test_desc
        else:
            meta_desc = f"{base}. Get training plans & course breakdown."
    else:
        meta_desc = f"{base}. Get training plans & course breakdown."
    
    # Final safety truncation
    if len(meta_desc) > 160:
        meta_desc = meta_desc[:157] + "..."
    
    # Build SEO title (use from seo section if available, otherwise generate)
    seo = race.get('seo', {})
    seo_title = seo.get('title') or f"{race_name} Race Guide | Training Plans & {city} Course Intel | Gravel God"
    # Ensure "| Gravel God" suffix if not present
    if seo.get('title') and '| Gravel God' not in seo_title:
        seo_title += ' | Gravel God'
    
    # Use meta description from seo section if available and valid length
    if seo.get('meta_description') and len(seo.get('meta_description', '')) <= 160:
        meta_desc = seo.get('meta_description')
    # Otherwise use generated one
    
    # Get focus keyword from seo section, fallback to race name lowercase
    focus_keyword = seo.get('focus_keyword') or race_name.lower()
    
    config = f"""═══════════════════════════════════════════════════════════════
WORDPRESS QUICK CONFIG: {race_name}
═══════════════════════════════════════════════════════════════

PAGE SETUP (Right Sidebar)
─────────────────────────────────────────────────────────────
Page Title:     {race_name}
Slug:           {race_slug}
Parent:         Gravel Races
Template:       Elementor Full Width

─────────────────────────────────────────────────────────────
AIOSEO SETTINGS (Bottom Panel → General Tab)
─────────────────────────────────────────────────────────────
Page Title:
{seo_title}

Meta Description:
{meta_desc}

Focus Keyword:
{focus_keyword}
═══════════════════════════════════════════════════════════════"""
    
    return config


def generate_landing_page(race_data_path: str, base_json_path: str, output_path: str):
    """Main generation function."""
    print(f"Loading race data from {race_data_path}...")
    data = load_race_data(race_data_path)
    
    print("Generating HTML sections...")
    elementor_json = build_elementor_json(data, base_json_path)
    
    print(f"Writing Elementor JSON to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(elementor_json, f, ensure_ascii=False, indent=2)
    
    # Generate searchable index file
    print("Generating searchable index...")
    race_slug = data['race'].get('slug', Path(race_data_path).stem.replace('-data', ''))
    index_output = Path(output_path).parent / f"{race_slug}-index.json"
    generate_index(data, str(index_output))
    print(f"✓ Index saved: {index_output.name}")
    
    # Generate WordPress Quick Config
    print("\n" + generate_wordpress_config(data) + "\n")
    
    # Copy to Downloads with LATEST label if this is Mid South or BWR CA
    race_name_lower = data['race']['display_name'].lower()
    if 'mid south' in race_name_lower or 'belgian waffle' in race_name_lower or 'bwr' in race_name_lower:
        from datetime import datetime
        import shutil
        downloads_dir = Path.home() / "Downloads"
        date_str = datetime.now().strftime("%Y%m%d")
        
        if 'mid south' in race_name_lower:
            downloads_name = f"elementor-mid-south-LATEST-{date_str}.json"
        elif 'belgian waffle' in race_name_lower or 'bwr' in race_name_lower:
            downloads_name = f"elementor-belgian-waffle-ride-CA-LATEST-{date_str}.json"
        else:
            downloads_name = None
        
        if downloads_name:
            downloads_path = downloads_dir / downloads_name
            shutil.copy2(output_path, downloads_path)
            print(f"✓ Copied to Downloads: {downloads_path.name}")
    
    race_name = data['race']['name']
    print(f"✓ Landing page generated for {race_name}")
    print(f"✓ Output: {output_path}")
    print(f"✓ Ready to import to Elementor")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python generate_landing_page.py <race_data.json> <base_template.json> <output.json>")
        sys.exit(1)
    
    race_data_path = sys.argv[1]
    base_json_path = sys.argv[2]
    output_path = sys.argv[3]
    
    generate_landing_page(race_data_path, base_json_path, output_path)
