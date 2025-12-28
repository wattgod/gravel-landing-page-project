#!/usr/bin/env python3
"""
Content validation for landing pages.

Validates that page content matches the research brief.
Run BEFORE pushing to catch data inconsistencies.

Usage:
    python validate_content.py --template path/to/template.json --brief path/to/brief.md
    python validate_content.py --check-live https://gravelgodcycling.com/page-url/ --brief path/to/brief.md
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class ContentValidator:
    """Validates page content against research brief."""

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def parse_brief(self, brief_path: str) -> Dict:
        """Extract key data from research brief markdown."""
        with open(brief_path, 'r') as f:
            content = f.read()

        data = {}

        # Overall score
        match = re.search(r'\*\*Overall Score:\*\*\s*(\d+)/100', content)
        if match:
            data['overall_score'] = int(match.group(1))

        # Course profile score
        match = re.search(r'\*\*Course Profile:\*\*\s*(\d+)/(\d+)', content)
        if match:
            data['course_profile_score'] = f"{match.group(1)}/{match.group(2)}"

        # Prestige score
        match = re.search(r'\*\*Prestige:\*\*\s*(\d+)/(\d+)', content)
        if match:
            data['prestige_score'] = f"{match.group(1)}/{match.group(2)}"

        # Location
        match = re.search(r'\*\*Location:\*\*\s*([^\n]+)', content)
        if match:
            data['location'] = match.group(1).strip()

        # Distance
        match = re.search(r'\*\*Distance:\*\*\s*([^\n]+)', content)
        if match:
            data['distance'] = match.group(1).strip()

        # Suffering zones
        zones = []
        zone_matches = re.findall(r'\*\*Mile (\d+)(?:[^*]*)\*\*\s*-?\s*([^.\n]+)', content)
        for mile, name in zone_matches:
            zones.append({'mile': int(mile), 'name': name.strip()})
        if zones:
            data['suffering_zones'] = zones

        # RADAR scores
        radar_section = re.search(r'RADAR.*?(?=##|\Z)', content, re.DOTALL)
        if radar_section:
            radar_text = radar_section.group(0)
            radar = {}
            for metric in ['Length', 'Technicality', 'Elevation', 'Climate', 'Altitude', 'Adventure', 'Logistics']:
                match = re.search(rf'{metric}[:\s]+(\d+)/5', radar_text)
                if match:
                    radar[metric.lower()] = int(match.group(1))
            if radar:
                data['radar'] = radar

        return data

    def validate_template_against_brief(self, template_path: str, brief_path: str) -> Tuple[bool, List[str], List[str]]:
        """Validate template JSON against research brief."""
        self.errors = []
        self.warnings = []

        # Parse brief
        brief_data = self.parse_brief(brief_path)
        if not brief_data:
            self.errors.append("Could not parse research brief")
            return False, self.errors, self.warnings

        # Load template
        with open(template_path, 'r') as f:
            template = json.load(f)
        template_str = json.dumps(template)

        # Check overall score
        if 'overall_score' in brief_data:
            expected = brief_data['overall_score']
            # Look for score in template
            score_match = re.search(rf'{expected}<span>/100', template_str)
            if not score_match:
                # Check what score IS in the template
                actual_match = re.search(r'(\d+)<span>/100', template_str)
                if actual_match:
                    actual = int(actual_match.group(1))
                    if actual != expected:
                        self.errors.append(
                            f"Score mismatch: template has {actual}/100, brief says {expected}/100"
                        )

        # Check suffering zones
        if 'suffering_zones' in brief_data:
            for zone in brief_data['suffering_zones']:
                mile = zone['mile']
                name = zone['name']
                if f'Mile {mile}' not in template_str:
                    self.warnings.append(
                        f"Suffering zone Mile {mile} ({name}) not found in template"
                    )

        # Check location
        if 'location' in brief_data:
            location = brief_data['location']
            if location not in template_str:
                self.warnings.append(f"Location '{location}' not found in template")

        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings

    def validate_live_page_against_brief(self, url: str, brief_path: str) -> Tuple[bool, List[str], List[str]]:
        """Validate live page against research brief."""
        self.errors = []
        self.warnings = []

        try:
            import requests
        except ImportError:
            self.errors.append("requests library not installed")
            return False, self.errors, self.warnings

        # Fetch page
        headers = {'User-Agent': 'Mozilla/5.0 GravelGod/1.0 Validator'}
        try:
            response = requests.get(url, timeout=30, headers=headers)
            response.raise_for_status()
            page_content = response.text
        except Exception as e:
            self.errors.append(f"Failed to fetch page: {e}")
            return False, self.errors, self.warnings

        # Parse brief
        brief_data = self.parse_brief(brief_path)

        # Check overall score
        if 'overall_score' in brief_data:
            expected = brief_data['overall_score']
            score_match = re.search(rf'{expected}<span>/100', page_content)
            if not score_match:
                actual_match = re.search(r'(\d+)<span>/100', page_content)
                if actual_match:
                    actual = int(actual_match.group(1))
                    if actual != expected:
                        self.errors.append(
                            f"Score mismatch: page shows {actual}/100, brief says {expected}/100"
                        )

        # Check suffering zones
        if 'suffering_zones' in brief_data:
            for zone in brief_data['suffering_zones']:
                mile = zone['mile']
                name = zone['name']
                # Check if mile marker exists
                mile_pattern = rf'Mile\s*{mile}\b'
                if not re.search(mile_pattern, page_content):
                    self.warnings.append(
                        f"Suffering zone Mile {mile} ({name}) not found on page"
                    )

        # Check for required content sections
        required_sections = [
            ('gg-hero', 'Hero section'),
            ('gg-plans-grid', 'Training plans grid'),
            ('gg-blackpill', 'Black pill section'),
            ('gg-logistics', 'Logistics section'),
        ]
        for css_class, description in required_sections:
            if css_class not in page_content:
                self.warnings.append(f"Missing section: {description}")

        # Check for images (excluding logo)
        img_matches = re.findall(r'src="([^"]*\.(jpg|png|webp|gif))"', page_content)
        content_images = [img for img, _ in img_matches if 'logo' not in img.lower()]
        if len(content_images) == 0:
            self.warnings.append("No content images found (only logo)")

        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Validate content against research brief')
    parser.add_argument('--template', help='Template JSON file to validate')
    parser.add_argument('--check-live', metavar='URL', help='Live page URL to validate')
    parser.add_argument('--brief', required=True, help='Research brief markdown file')

    args = parser.parse_args()

    validator = ContentValidator()

    if args.check_live:
        print(f"Validating live page: {args.check_live}")
        print(f"Against brief: {args.brief}")
        is_valid, errors, warnings = validator.validate_live_page_against_brief(
            args.check_live, args.brief
        )
    elif args.template:
        print(f"Validating template: {args.template}")
        print(f"Against brief: {args.brief}")
        is_valid, errors, warnings = validator.validate_template_against_brief(
            args.template, args.brief
        )
    else:
        parser.print_help()
        sys.exit(1)

    print("")
    if errors:
        print("ERRORS:")
        for err in errors:
            print(f"  ✗ {err}")

    if warnings:
        print("WARNINGS:")
        for warn in warnings:
            print(f"  ⚠ {warn}")

    if is_valid and not warnings:
        print("✓ All validations passed")
    elif is_valid:
        print("\n✓ No critical errors (but warnings exist)")
    else:
        print("\n✗ Validation failed")

    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
