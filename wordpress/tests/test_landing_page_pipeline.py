#!/usr/bin/env python3
"""
Regression tests for the landing page pipeline.

Tests:
1. Template loading and structure
2. Placeholder replacement
3. Pre-push validation
4. Race data validation
5. WordPress push (if credentials available)
6. Content verification on live pages
"""
import json
import os
import re
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


class TestPrePushValidation(unittest.TestCase):
    """Test pre-push validation catches errors before they go live."""

    @classmethod
    def setUpClass(cls):
        cls.template_path = Path(__file__).parent.parent / 'templates' / 'template-master-fixed.json'
        with open(cls.template_path, 'r') as f:
            cls.template = json.load(f)

    def test_validation_catches_unreplaced_placeholders(self):
        """Validation fails when placeholders are not replaced."""
        pusher = WordPressPagePusher('https://dummy.com', 'dummy', 'dummy')

        # Template without replacement should fail validation
        with self.assertRaises(ValueError) as context:
            pusher.validate_before_push(self.template)

        self.assertIn('RACE_NAME', str(context.exception))

    def test_validation_passes_after_replacement(self):
        """Validation passes when placeholders are properly replaced."""
        pusher = WordPressPagePusher('https://dummy.com', 'dummy', 'dummy')

        race_data = {
            'race_name': 'Test Race',
            'location': 'Test City, State',
            'distance': '100',
            'city': 'TestCity',
            'race_tagline': 'Test tagline',
            'race_slug': 'test-race',
        }

        # Replace placeholders
        replaced = pusher.replace_placeholders(self.template, race_data)

        # Should pass validation
        result = pusher.validate_before_push(replaced)
        self.assertTrue(result)

    def test_validation_allows_elementor_internal_placeholders(self):
        """Elementor internal placeholders like {{ID}} are allowed."""
        pusher = WordPressPagePusher('https://dummy.com', 'dummy', 'dummy')

        # Content with only Elementor internal placeholders
        content = {
            'content': [{'id': '{{ID}}', 'settings': {'_css_classes': '{{_CSS_CLASSES}}'}}]
        }

        # Should pass (these are allowed)
        result = pusher.validate_before_push(content)
        self.assertTrue(result)

    def test_trainingpeaks_links_are_generated(self):
        """TrainingPeaks link placeholders are replaced."""
        pusher = WordPressPagePusher('https://dummy.com', 'dummy', 'dummy')

        race_data = {
            'race_name': 'Unbound 200',
            'race_slug': 'unbound-200',
        }

        replacements = pusher._build_replacements(race_data)

        self.assertIn('{{TP_LINK_TIME_CRUNCHED}}', replacements)
        self.assertIn('unbound-200', replacements['{{TP_LINK_TIME_CRUNCHED}}'])


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
    def test_unbound_page_renders(self):
        """Unbound 200 page renders correctly with proper content."""
        url = "https://gravelgodcycling.com/unbound-gravel-200-race-guide/"

        response = self.requests.get(url, timeout=30, headers=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        # Check for training section
        required_elements = [
            'gg-plans-grid',
            'gg-plan-card',
        ]

        for element in required_elements:
            self.assertIn(element, response.text,
                         f"Page missing element: {element}")

    @unittest.skipUnless(HAS_WP_CONFIG, "No network/config")
    def test_unbound_page_has_correct_content(self):
        """Unbound page has Unbound-specific content, no Mid South."""
        url = "https://gravelgodcycling.com/unbound-gravel-200-race-guide/"

        response = self.requests.get(url, timeout=30, headers=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        text = response.text.lower()

        # Must have Unbound-specific content
        self.assertIn('emporia', text, "Missing Emporia reference")
        self.assertIn('flint hills', text, "Missing Flint Hills reference")
        self.assertIn('unbound', text, "Missing Unbound reference")

        # Must NOT have Mid South content
        self.assertNotIn('stillwater', text, "Contains Stillwater (Mid South content)")
        self.assertNotIn('oklahoma', text, "Contains Oklahoma (Mid South content)")
        # Allow "mid south" only in alternatives section
        mid_south_count = text.count('mid south') + text.count('mid-south')
        self.assertLessEqual(mid_south_count, 2,
                            f"Too many Mid South references ({mid_south_count})")

    @unittest.skipUnless(HAS_WP_CONFIG, "No network/config")
    def test_unbound_page_no_unreplaced_placeholders(self):
        """Unbound page has no unreplaced template placeholders."""
        url = "https://gravelgodcycling.com/unbound-gravel-200-race-guide/"

        response = self.requests.get(url, timeout=30, headers=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        # Find placeholders like {{RACE_NAME}} but ignore Elementor internals
        placeholders = re.findall(r'\{\{[A-Z][A-Z_]*\}\}', response.text)
        # Filter out Elementor internal placeholders
        user_placeholders = [p for p in placeholders if not p.startswith('{{_')]

        self.assertEqual(user_placeholders, [],
                        f"Unreplaced placeholders found: {user_placeholders}")

    @unittest.skipUnless(HAS_WP_CONFIG, "No network/config")
    def test_unbound_page_score_matches_brief(self):
        """Unbound page score matches research brief (88/100)."""
        url = "https://gravelgodcycling.com/unbound-gravel-200-race-guide/"

        response = self.requests.get(url, timeout=30, headers=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        # Check for correct score
        self.assertIn('88<span>/100', response.text,
                     "Score should be 88/100 per research brief")

    @unittest.skipUnless(HAS_WP_CONFIG, "No network/config")
    def test_unbound_page_no_score_inconsistency(self):
        """Unbound page has no inconsistent score references (e.g., text saying 93 when score is 88)."""
        url = "https://gravelgodcycling.com/unbound-gravel-200-race-guide/"

        response = self.requests.get(url, timeout=30, headers=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        # Should NOT have 93/100 anywhere since the score is 88
        self.assertNotIn('93 / 100', response.text,
                        "Found '93 / 100' but score should be 88")
        self.assertNotIn('93/100', response.text,
                        "Found '93/100' but score should be 88")
        self.assertNotIn('A 93', response.text,
                        "Found 'A 93' reference but score should be 88")

    @unittest.skipUnless(HAS_WP_CONFIG, "No network/config")
    def test_unbound_page_suffering_zones_correct(self):
        """Unbound page has correct suffering zone mile markers."""
        url = "https://gravelgodcycling.com/unbound-gravel-200-race-guide/"

        response = self.requests.get(url, timeout=30, headers=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        # Check for correct suffering zones from research brief
        self.assertIn('Mile 28', response.text, "Missing Mile 28 (First Selection)")
        self.assertIn('Mile 40', response.text, "Missing Mile 40 (Divide Road)")
        self.assertIn('Mile 104', response.text, "Missing Mile 104 (Little Egypt)")

    @unittest.skipUnless(HAS_WP_CONFIG, "No network/config")
    def test_unbound_page_no_repeated_content(self):
        """Unbound page has no suspiciously repeated content blocks."""
        url = "https://gravelgodcycling.com/unbound-gravel-200-race-guide/"

        response = self.requests.get(url, timeout=30, headers=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        text = response.text.lower()

        # Check for repeated section headers
        # Allow up to 8: section header + TOC + mobile nav + footer + variations
        # Note: "course profile" appears in both section title AND score breakdown
        section_headers = [
            ('the black pill', 5),
            ('suffering zones', 5),
            ('training plans', 5),
            ('race vitals', 5),
            ('course profile', 8),  # Higher because it's in score breakdown too
        ]

        for header, max_count in section_headers:
            count = text.count(header)
            self.assertLessEqual(count, max_count,
                f"Section header '{header}' appears {count} times (max {max_count})")

        # Check for repeated key phrases that indicate copy-paste errors
        key_phrases = [
            'you don\'t race unbound',  # Tagline
            'super bowl of gravel',
            'derailleur destruction',
        ]

        for phrase in key_phrases:
            count = text.count(phrase)
            self.assertLessEqual(count, 2,
                f"Key phrase '{phrase}' appears {count} times (indicates repeated content)")

        # Check that suffering zone descriptions aren't duplicated
        # (e.g., "first selection" shouldn't appear more than twice)
        zone_names = [
            'first selection',
            'divide road',
            'little egypt',
            'cattle country',
        ]

        for zone in zone_names:
            count = text.count(zone)
            self.assertLessEqual(count, 3,
                f"Zone '{zone}' appears {count} times (max 3 - may indicate duplication)")


class TestTemplateNoDuplicateContent(unittest.TestCase):
    """Test templates don't have duplicate content blocks."""

    @classmethod
    def setUpClass(cls):
        cls.project_root = Path(__file__).parent.parent.parent
        cls.unbound_template = cls.project_root / 'Unbound/landing-page/elementor-unbound-200.json'

    def test_unbound_template_no_duplicate_sections(self):
        """Unbound template doesn't have duplicate section content."""
        if not self.unbound_template.exists():
            self.skipTest("Unbound template not found")

        with open(self.unbound_template, 'r') as f:
            content = f.read().lower()

        # Key content - allow up to 2 for section header + TOC reference
        unique_content = [
            ('the black pill', 3),  # Allow header + TOC + possibly nav
            ('you don\'t race unbound', 2),  # Tagline should be more unique
        ]

        for phrase, max_count in unique_content:
            count = content.count(phrase)
            self.assertLessEqual(count, max_count,
                f"'{phrase}' appears {count} times in template (max {max_count})")

    def test_template_no_duplicate_suffering_zones(self):
        """Template doesn't have duplicate suffering zone entries."""
        if not self.unbound_template.exists():
            self.skipTest("Unbound template not found")

        with open(self.unbound_template, 'r') as f:
            content = f.read()

        # Each mile marker should appear only once (plus maybe in TOC)
        mile_markers = ['Mile 28', 'Mile 40', 'Mile 104']

        for marker in mile_markers:
            count = content.count(marker)
            self.assertLessEqual(count, 2,
                f"'{marker}' appears {count} times in template (max 2 - section + TOC)")


if __name__ == '__main__':
    unittest.main(verbosity=2)
