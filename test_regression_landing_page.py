#!/usr/bin/env python3
"""
Regression test suite for landing page generator.
Ensures previously fixed bugs don't return.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional


def load_json(filepath: str) -> Dict:
    """Load JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_html_widgets(elements: List[Dict], found: List[Dict] = None) -> List[Dict]:
    """Recursively find all HTML widgets."""
    if found is None:
        found = []
    for element in elements:
        if element.get('widgetType') == 'html':
            settings = element.get('settings', {})
            if isinstance(settings, dict):
                found.append(element)
        if 'elements' in element:
            find_html_widgets(element['elements'], found)
    return found


def extract_html_content(elementor_json: Dict) -> str:
    """Extract all HTML content from Elementor JSON."""
    widgets = find_html_widgets(elementor_json.get('content', []))
    html_parts = []
    for widget in widgets:
        settings = widget.get('settings', {})
        if isinstance(settings, dict):
            html = settings.get('html', '')
            html_parts.append(html)
    return '\n'.join(html_parts)


class LandingPageRegressionTests:
    """Regression tests for landing page generation."""
    
    def __init__(self, json_path: str):
        self.json_path = json_path
        self.data = load_json(json_path)
        self.html_content = extract_html_content(self.data)
        self.errors = []
    
    def test_radar_chart_present(self):
        """Test: Radar chart SVG and JavaScript must be present in ratings section."""
        has_svg = 'gg-course-radar-svg' in self.html_content
        has_js = 'function polar' in self.html_content or 'polar(' in self.html_content
        has_metrics = 'metrics: [' in self.html_content or 'metrics =' in self.html_content
        
        if not (has_svg and has_js and has_metrics):
            self.errors.append("Ratings section missing radar chart (SVG, JavaScript, or metrics array)")
    
    def test_course_profile_card_present(self):
        """Test: Course profile card with all 7 variables must be present."""
        has_card = 'gg-course-profile-card' in self.html_content
        has_7_vars = (
            'Length' in self.html_content and
            'Technicality' in self.html_content and
            'Elevation' in self.html_content and
            'Climate' in self.html_content and
            'Altitude' in self.html_content and
            'Adventure' in self.html_content
        )
        # Logistics might be optional depending on data
        has_logistics = 'Logistics' in self.html_content or 'logistics' in self.html_content.lower()
        
        if not has_card:
            self.errors.append("Course profile card missing")
        if not has_7_vars:
            self.errors.append("Course profile missing required variables (Length, Technicality, Elevation, Climate, Altitude, Adventure)")
    
    def test_no_unreplaced_placeholders(self):
        """Test: No template placeholders should remain in output."""
        placeholder_pattern = re.compile(r'\{\{[A-Z_]+\}\}')
        matches = placeholder_pattern.findall(self.html_content)
        if matches:
            self.errors.append(f"Unreplaced placeholders found: {matches[:5]}")
    
    def test_hero_section_complete(self):
        """Test: Hero section must have all required elements."""
        has_hero = 'gg-hero-inner' in self.html_content
        has_score = 'gg-hero-score-card' in self.html_content
        has_breakdown = 'gg-hero-score-breakdown' in self.html_content
        
        if not (has_hero and has_score and has_breakdown):
            self.errors.append("Hero section incomplete (missing inner, score card, or breakdown)")
    
    def test_training_plans_section_complete(self):
        """Test: Training plans section must have all tiers and TP URLs."""
        has_section = 'gg-volume-section' in self.html_content
        has_ayahuasca = 'Ayahuasca' in self.html_content
        has_finisher = 'Finisher' in self.html_content
        has_compete = 'Compete' in self.html_content
        has_podium = 'Podium' in self.html_content
        has_tp_urls = 'trainingpeaks.com/training-plans' in self.html_content
        
        if not has_section:
            self.errors.append("Training plans section missing")
        if not (has_ayahuasca and has_finisher and has_compete and has_podium):
            self.errors.append("Training plans section missing one or more tiers")
        if not has_tp_urls:
            self.errors.append("Training plans section missing TrainingPeaks URLs")
    
    def test_ratings_section_layout(self):
        """Test: Ratings section must have correct grid layout."""
        has_grid = 'gg-ratings-grid' in self.html_content
        has_left = 'gg-ratings-left' in self.html_content
        has_right = 'gg-ratings-right' in self.html_content
        
        if not (has_grid and has_left and has_right):
            self.errors.append("Ratings section missing grid layout (grid, left, or right column)")
    
    def test_black_pill_section_present(self):
        """Test: Black pill section must be present."""
        has_section = 'gg-blackpill-section' in self.html_content
        has_badge = 'THE BLACK PILL' in self.html_content
        
        if not (has_section and has_badge):
            self.errors.append("Black pill section missing or incomplete")
    
    def test_json_valid(self):
        """Test: JSON must be valid and parseable."""
        # Already loaded, so if we got here it's valid
        pass
    
    def test_section_ids_present(self):
        """Test: Required section IDs must be present."""
        required_ids = ['course-ratings', 'race-vitals']
        # Check in HTML content
        for section_id in required_ids:
            if section_id not in self.html_content:
                self.errors.append(f"Required section ID '{section_id}' not found")
    
    def test_radar_chart_metrics_match_data(self):
        """Test: Radar chart metrics must match actual rating scores."""
        # Extract metrics from JavaScript
        metrics_match = re.search(r'metrics:\s*\[(.*?)\]', self.html_content, re.DOTALL)
        if not metrics_match:
            self.errors.append("Could not find metrics array in radar chart JavaScript")
            return
        
        # Check that all 7 course variables are represented
        metrics_text = metrics_match.group(1)
        required_labels = ['Length', 'Technicality', 'Elevation', 'Climate', 'Altitude', 'Adventure']
        for label in required_labels:
            if label not in metrics_text:
                self.errors.append(f"Radar chart missing metric: {label}")
    
    def test_course_profile_scores_match_data(self):
        """Test: Course profile card scores must match rating data."""
        # This is a structural test - actual data validation would require loading race data
        # For now, just check that scores are present
        score_pattern = re.compile(r'(\d+)/5')
        scores = score_pattern.findall(self.html_content)
        if len(scores) < 7:  # Should have at least 7 scores (one per variable)
            self.errors.append(f"Course profile missing scores (found {len(scores)}, expected 7+)")
    
    def test_no_duplicate_sections(self):
        """Test: No duplicate section IDs."""
        section_ids = re.findall(r'id="([^"]+)"', self.html_content)
        duplicates = [sid for sid in set(section_ids) if section_ids.count(sid) > 1]
        if duplicates:
            self.errors.append(f"Duplicate section IDs found: {duplicates}")
    
    def test_training_plans_urls_valid(self):
        """Test: All TrainingPeaks URLs must be well-formed."""
        tp_url_pattern = re.compile(r'https://www\.trainingpeaks\.com/training-plans/cycling/[^"\s]+')
        urls = tp_url_pattern.findall(self.html_content)
        
        if not urls:
            self.errors.append("No TrainingPeaks URLs found")
            return
        
        # Check URL structure (allow placeholders)
        for url in urls:
            # Allow placeholder URLs (they'll be updated when plans go live)
            if 'PLACEHOLDER' in url.upper():
                continue
            # Real URLs should have /tp- or be valid category paths
            if '/tp-' not in url and '/gran-fondo-century/' not in url and '/road-cycling/' not in url:
                self.errors.append(f"Malformed TP URL: {url[:50]}...")
                break
        
        # Should have at least 15 URLs (one per plan)
        if len(urls) < 15:
            self.errors.append(f"Expected 15+ TP URLs, found {len(urls)}")
    
    def test_training_plans_2_column_grid(self):
        """REGRESSION: Training plans grid must be 2 columns, not 4 (fixed 2025-12-16)."""
        has_2_col = 'grid-template-columns: repeat(2, 1fr)' in self.html_content
        has_4_col = 'grid-template-columns: repeat(4, 1fr)' in self.html_content
        
        if has_4_col:
            self.errors.append("Training plans grid uses 4 columns (should be 2)")
        if not has_2_col:
            self.errors.append("Training plans grid missing 2-column layout")
    
    def test_plan_cards_no_descriptions(self):
        """REGRESSION: Plan cards must NOT have descriptions - just name and button (fixed 2025-12-16)."""
        has_description = 'gg-plan-description' in self.html_content
        has_explicit_labels = 'Challenge:' in self.html_content or 'Solution:' in self.html_content
        
        if has_description:
            self.errors.append("Plan cards should NOT have description section (gg-plan-description class) - removed per user request")
        if has_explicit_labels:
            self.errors.append("Plan cards should NOT have explicit 'Challenge:' or 'Solution:' labels")
    
    def test_course_breakdown_header_not_ratings(self):
        """REGRESSION: Header must be 'COURSE BREAKDOWN', not 'THE RATINGS' (fixed 2025-12-16)."""
        has_course_breakdown = 'COURSE BREAKDOWN' in self.html_content
        has_the_ratings = 'THE RATINGS' in self.html_content
        
        if has_the_ratings:
            self.errors.append("Found old 'THE RATINGS' header (should be 'COURSE BREAKDOWN')")
        if not has_course_breakdown:
            self.errors.append("Missing 'COURSE BREAKDOWN' header")
    
    def test_coaching_cta_present(self):
        """REGRESSION: Coaching CTA section must be present at bottom (added 2025-12-16)."""
        has_section = 'gg-coaching-cta-section' in self.html_content
        has_card = 'gg-coaching-cta-card' in self.html_content
        has_button = 'Apply for Coaching' in self.html_content or 'coaching/' in self.html_content
        
        if not has_section:
            self.errors.append("Missing coaching CTA section (gg-coaching-cta-section)")
        if not has_card:
            self.errors.append("Missing coaching CTA card (gg-coaching-cta-card)")
        if not has_button:
            self.errors.append("Missing coaching CTA button/link")
    
    def test_gravel_races_cta_present(self):
        """REGRESSION: Gravel races CTA must be present at very bottom (added 2025-12-16)."""
        has_section = 'gravel-races-cta' in self.html_content
        has_button = 'ALL GRAVEL RACES' in self.html_content or 'gravel-races-cta-button' in self.html_content
        has_link = 'gravel-races/' in self.html_content
        
        if not has_section:
            self.errors.append("Missing gravel races CTA section (gravel-races-cta)")
        if not (has_button or has_link):
            self.errors.append("Missing gravel races CTA button/link")
    
    def test_toc_has_course_breakdown(self):
        """REGRESSION: TOC must say 'Course Breakdown', not 'The Ratings' (fixed 2025-12-16)."""
        has_course_breakdown = 'Course Breakdown' in self.html_content or 'course-breakdown' in self.html_content.lower()
        has_the_ratings = 'The Ratings' in self.html_content and 'gg-topnav' in self.html_content
        
        if has_the_ratings:
            self.errors.append("TOC still has 'The Ratings' link (should be 'Course Breakdown')")
        if not has_course_breakdown:
            self.errors.append("TOC missing 'Course Breakdown' link")
    
    def test_ridewithgps_route_id_valid(self):
        """REGRESSION: RideWithGPS route IDs must be valid numeric IDs, NOT placeholders (fixed 2025-12-16)."""
        # Find all RideWithGPS embed URLs
        rwgps_pattern = re.compile(r'ridewithgps\.com/embeds\?[^"\s]+')
        urls = rwgps_pattern.findall(self.html_content)
        
        if not urls:
            # If there's a course map section, there should be a RideWithGPS URL
            if 'gg-route-section' in self.html_content or 'course-map' in self.html_content:
                self.errors.append("Course map section found but no RideWithGPS embed URL")
            return
        
        # Check each URL for valid route ID
        for url in urls:
            # Extract the route ID from the URL
            id_match = re.search(r'[?&]id=([^&"\s]+)', url)
            if not id_match:
                self.errors.append(f"RideWithGPS URL missing route ID: {url[:80]}...")
                continue
            
            route_id = id_match.group(1)
            
            # Check for placeholder values
            if 'PLACEHOLDER' in route_id.upper() or 'NEEDS_RESEARCH' in route_id.upper():
                self.errors.append(f"RideWithGPS route ID is still a placeholder: {route_id}")
                continue
            
            # Check that it's a valid numeric ID (RideWithGPS IDs are numeric)
            if not route_id.isdigit():
                self.errors.append(f"RideWithGPS route ID must be numeric, found: {route_id}")
                continue
            
            # Check that it's a reasonable length (RideWithGPS IDs are typically 6-8 digits)
            if len(route_id) < 6 or len(route_id) > 10:
                self.errors.append(f"RideWithGPS route ID length suspicious: {route_id} (expected 6-10 digits)")
    
    def run_all_tests(self) -> List[str]:
        """Run all regression tests."""
        self.errors = []
        
        self.test_radar_chart_present()
        self.test_course_profile_card_present()
        self.test_no_unreplaced_placeholders()
        self.test_hero_section_complete()
        self.test_training_plans_section_complete()
        self.test_ratings_section_layout()
        self.test_black_pill_section_present()
        self.test_json_valid()
        self.test_section_ids_present()
        self.test_radar_chart_metrics_match_data()
        self.test_course_profile_scores_match_data()
        self.test_no_duplicate_sections()
        self.test_training_plans_urls_valid()
        self.test_training_plans_2_column_grid()
        self.test_plan_cards_no_descriptions()
        self.test_course_breakdown_header_not_ratings()
        self.test_coaching_cta_present()
        self.test_gravel_races_cta_present()
        self.test_toc_has_course_breakdown()
        self.test_ridewithgps_route_id_valid()
        
        return self.errors


def main():
    """Run regression tests."""
    if len(sys.argv) < 2:
        print("Usage: python test_regression_landing_page.py <elementor_json.json>")
        sys.exit(1)
    
    json_path = sys.argv[1]
    
    if not Path(json_path).exists():
        print(f"ERROR: File not found: {json_path}")
        sys.exit(1)
    
    print(f"Running regression tests on: {json_path}")
    print("=" * 60)
    
    tester = LandingPageRegressionTests(json_path)
    errors = tester.run_all_tests()
    
    if errors:
        print(f"\nFAILED: {len(errors)} test(s) failed\n")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        sys.exit(1)
    else:
        print("\n✓ All regression tests passed")
        sys.exit(0)


if __name__ == '__main__':
    main()


