#!/usr/bin/env python3
"""
Regression tests for the landing page pipeline.

Tests:
1. Template loading and structure
2. Placeholder replacement
3. Race data validation
4. WordPress push (if credentials available)
5. Content verification on live pages
"""
import json
import os
import sys
import unittest
from pathlib import Path

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from push_pages import WordPressPagePusher, WP_CONFIG
    HAS_WP_CONFIG = bool(WP_CONFIG.get('site_url'))
except (ImportError, Exception):
    HAS_WP_CONFIG = False


class TestTemplateStructure(unittest.TestCase):
    """Test template files are valid and have expected structure."""

    @classmethod
    def setUpClass(cls):
        cls.template_dir = Path(__file__).parent.parent / 'templates'
        cls.template_path = cls.template_dir / 'template-master-fixed.json'

    def test_template_exists(self):
        """Template file exists."""
        self.assertTrue(self.template_path.exists(),
                       f"Template not found: {self.template_path}")

    def test_template_valid_json(self):
        """Template is valid JSON."""
        with open(self.template_path, 'r') as f:
            template = json.load(f)
        self.assertIsInstance(template, dict)

    def test_template_has_content(self):
        """Template has content array."""
        with open(self.template_path, 'r') as f:
            template = json.load(f)
        self.assertIn('content', template)
        self.assertIsInstance(template['content'], list)
        self.assertGreater(len(template['content']), 0)

    def test_template_has_page_settings(self):
        """Template has page_settings."""
        with open(self.template_path, 'r') as f:
            template = json.load(f)
        self.assertIn('page_settings', template)

    def test_template_has_training_section(self):
        """Template contains training section classes."""
        with open(self.template_path, 'r') as f:
            content = f.read()

        required_classes = [
            'gg-plans-grid',
            'gg-plan-card',
            'gg-tier-cta',
        ]

        for cls in required_classes:
            self.assertIn(cls, content,
                         f"Template missing required class: {cls}")


class TestPlaceholderReplacement(unittest.TestCase):
    """Test placeholder replacement logic."""

    @classmethod
    def setUpClass(cls):
        cls.template_path = Path(__file__).parent.parent / 'templates' / 'template-master-fixed.json'
        with open(cls.template_path, 'r') as f:
            cls.template = json.load(f)

    def test_race_data_placeholders(self):
        """Race data placeholders are in template."""
        content_str = json.dumps(self.template)

        # These placeholders should exist in the template
        expected_placeholders = [
            '{{RACE_NAME}}',
            '{{LOCATION}}',
        ]

        for placeholder in expected_placeholders:
            self.assertIn(placeholder, content_str,
                         f"Template missing placeholder: {placeholder}")

    @unittest.skipUnless(HAS_WP_CONFIG, "No WordPress config")
    def test_placeholder_replacement(self):
        """Placeholders are correctly replaced."""
        pusher = WordPressPagePusher(
            wordpress_url=WP_CONFIG['site_url'],
            username=WP_CONFIG['username'],
            password=WP_CONFIG['app_password']
        )

        race_data = {
            "race_name": "Test Race",
            "location": "Test Location, State",
            "distance": "100",
            "city": "TestCity",
            "race_tagline": "Test tagline here.",
            "race_slug": "test-race"
        }

        result = pusher.replace_placeholders(self.template, race_data)
        result_str = json.dumps(result)

        # Placeholders should be replaced
        self.assertIn("Test Race", result_str)
        self.assertNotIn("{{RACE_NAME}}", result_str)


class TestRaceBriefs(unittest.TestCase):
    """Test race research briefs exist and are valid."""

    @classmethod
    def setUpClass(cls):
        cls.project_root = Path(__file__).parent.parent.parent
        cls.briefs_dir = cls.project_root / 'briefs'
        cls.unbound_dir = cls.project_root / 'Unbound'

    def test_unbound_brief_exists(self):
        """Unbound 200 brief exists."""
        brief_path = self.unbound_dir / 'unbound-200-brief.md'
        self.assertTrue(brief_path.exists(),
                       f"Unbound brief not found: {brief_path}")

    def test_unbound_brief_has_required_sections(self):
        """Unbound brief has required sections."""
        brief_path = self.unbound_dir / 'unbound-200-brief.md'

        if not brief_path.exists():
            self.skipTest("Brief not found")

        with open(brief_path, 'r') as f:
            content = f.read()

        required_sections = [
            'RADAR',
            'Prestige',
            'Training',
            'BLACK PILL',  # Case-sensitive match
        ]

        for section in required_sections:
            self.assertIn(section, content,
                         f"Brief missing section: {section}")


class TestLivePages(unittest.TestCase):
    """Test live WordPress pages (requires network)."""

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) GravelGod/1.0 TestSuite'
    }

    @classmethod
    def setUpClass(cls):
        try:
            import requests
            cls.requests = requests
            cls.has_network = True
        except ImportError:
            cls.has_network = False

    @unittest.skipUnless(HAS_WP_CONFIG, "No network/config")
    def test_mid_south_page_renders(self):
        """Mid South test page renders correctly."""
        url = "https://gravelgodcycling.com/the-mid-south-gravel-race-guide-4/"

        response = self.requests.get(url, timeout=30, headers=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        # Check for training section
        required_elements = [
            'gg-plans-grid',
            'gg-plan-card',
            'gg-tier-cta',
        ]

        for element in required_elements:
            self.assertIn(element, response.text,
                         f"Page missing element: {element}")

    @unittest.skipUnless(HAS_WP_CONFIG, "No network/config")
    def test_unbound_new_page_renders(self):
        """Unbound new format page renders correctly."""
        url = "https://gravelgodcycling.com/unbound-gravel-200-race-guide-new/"

        response = self.requests.get(url, timeout=30, headers=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        # Check for training section (same as Mid South)
        required_elements = [
            'gg-plans-grid',
            'gg-plan-card',
            'gg-tier-cta',
        ]

        for element in required_elements:
            self.assertIn(element, response.text,
                         f"Page missing element: {element}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
