#!/usr/bin/env python3
"""
Pre-push validation for landing page templates.

Run this BEFORE pushing to WordPress to catch:
1. Unreplaced placeholders
2. Missing required sections
3. Invalid JSON structure
4. Missing images/media

Usage:
    python validate_template.py templates/template-master-fixed.json
    python validate_template.py --check-live https://gravelgodcycling.com/page-url/
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


class TemplateValidator:
    """Validates Elementor templates before push."""

    # Placeholders that are OK (Elementor internal)
    ALLOWED_PLACEHOLDERS = {
        '{{_CSS_CLASSES}}',
        '{{_ELEMENT_ID}}',
        '{{_ELEMENT_WIDTH}}',
        '{{ID}}',  # Elementor auto-generates
    }

    # Required CSS classes for a complete page
    REQUIRED_CSS_CLASSES = [
        'gg-hero',           # Hero section
        'gg-tier-overview',  # Tier overview
        'gg-blackpill',      # Black pill section
        'gg-plans-grid',     # Training plans grid
        'gg-plan-card',      # Plan cards
    ]

    # Required content patterns (must appear in rendered content)
    REQUIRED_CONTENT_PATTERNS = [
        (r'gg-plan-card', 'Training plan cards'),
        (r'gg-tier-cta', 'Tier CTA buttons'),
    ]

    def __init__(self, strict: bool = True):
        """
        Initialize validator.

        Args:
            strict: If True, treat warnings as errors
        """
        self.strict = strict
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_json_file(self, filepath: str) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a template JSON file.

        Args:
            filepath: Path to JSON file

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []

        # Check file exists
        if not Path(filepath).exists():
            self.errors.append(f"File not found: {filepath}")
            return False, self.errors, self.warnings

        # Load and validate JSON
        try:
            with open(filepath, 'r') as f:
                template = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return False, self.errors, self.warnings

        # Run all validations
        self._validate_structure(template)
        self._validate_placeholders(template)
        self._validate_required_sections(template)
        self._validate_links(template)

        is_valid = len(self.errors) == 0
        if self.strict and len(self.warnings) > 0:
            is_valid = False

        return is_valid, self.errors, self.warnings

    def validate_content_string(self, content: str, context: str = "content") -> Tuple[bool, List[str], List[str]]:
        """
        Validate a content string (e.g., Elementor data).

        Args:
            content: JSON string or HTML content
            context: Description for error messages

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []

        self._check_placeholders_in_string(content, context)
        self._check_required_patterns_in_string(content)

        is_valid = len(self.errors) == 0
        if self.strict and len(self.warnings) > 0:
            is_valid = False

        return is_valid, self.errors, self.warnings

    def _validate_structure(self, template: Dict[str, Any]):
        """Validate basic template structure."""
        if 'content' not in template:
            self.errors.append("Template missing 'content' array")
            return

        if not isinstance(template['content'], list):
            self.errors.append("Template 'content' must be an array")
            return

        if len(template['content']) == 0:
            self.errors.append("Template 'content' array is empty")

    def _validate_placeholders(self, template: Dict[str, Any]):
        """Check for unreplaced placeholders."""
        content_str = json.dumps(template)
        self._check_placeholders_in_string(content_str, "template")

    def _check_placeholders_in_string(self, content: str, context: str):
        """Find unreplaced placeholders in a string."""
        # Find all {{PLACEHOLDER}} patterns
        placeholders = re.findall(r'\{\{[A-Z][A-Z0-9_]*\}\}', content)

        # Filter out allowed placeholders
        bad_placeholders = [p for p in placeholders if p not in self.ALLOWED_PLACEHOLDERS]

        if bad_placeholders:
            unique = list(set(bad_placeholders))
            self.errors.append(
                f"Unreplaced placeholders in {context}: {', '.join(unique)}"
            )

    def _validate_required_sections(self, template: Dict[str, Any]):
        """Check that required CSS classes exist."""
        content_str = json.dumps(template)

        missing = []
        for css_class in self.REQUIRED_CSS_CLASSES:
            if css_class not in content_str:
                missing.append(css_class)

        if missing:
            self.warnings.append(
                f"Missing required CSS classes: {', '.join(missing)}"
            )

    def _check_required_patterns_in_string(self, content: str):
        """Check for required content patterns."""
        for pattern, description in self.REQUIRED_CONTENT_PATTERNS:
            if not re.search(pattern, content):
                self.warnings.append(f"Missing {description} (pattern: {pattern})")

    def _validate_links(self, template: Dict[str, Any]):
        """Validate that links don't contain placeholders."""
        content_str = json.dumps(template)

        # Find href attributes with placeholders
        href_placeholders = re.findall(r'href[^>]*\{\{[A-Z_]+\}\}', content_str)
        if href_placeholders:
            self.errors.append(
                f"Links contain unreplaced placeholders: {len(href_placeholders)} found"
            )


def validate_before_push(template: Dict[str, Any], race_data: Dict[str, Any] = None) -> bool:
    """
    Validate template before pushing to WordPress.

    Call this in push scripts before create_page().

    Args:
        template: Template dictionary (after placeholder replacement if applicable)
        race_data: Optional race data for context in error messages

    Returns:
        True if valid, raises ValidationError if not
    """
    validator = TemplateValidator(strict=True)

    # Convert to string for validation
    content_str = json.dumps(template)

    is_valid, errors, warnings = validator.validate_content_string(content_str)

    if not is_valid:
        race_name = ""
        if race_data:
            race = race_data.get('race', race_data)
            race_name = race.get('name', race_data.get('race_name', ''))

        error_msg = f"Validation failed{f' for {race_name}' if race_name else ''}:\n"
        for err in errors:
            error_msg += f"  ERROR: {err}\n"
        for warn in warnings:
            error_msg += f"  WARNING: {warn}\n"

        raise ValidationError(error_msg)

    return True


def validate_live_page(url: str) -> Tuple[bool, List[str], List[str]]:
    """
    Validate a live WordPress page.

    Args:
        url: Full URL to the page

    Returns:
        Tuple of (is_valid, errors, warnings)
    """
    try:
        import requests
    except ImportError:
        return False, ["requests library not installed"], []

    headers = {
        'User-Agent': 'Mozilla/5.0 GravelGod/1.0 Validator'
    }

    try:
        response = requests.get(url, timeout=30, headers=headers)
        response.raise_for_status()
    except Exception as e:
        return False, [f"Failed to fetch page: {e}"], []

    validator = TemplateValidator(strict=False)
    return validator.validate_content_string(response.text, f"live page {url}")


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Validate landing page templates')
    parser.add_argument('file', nargs='?', help='Template JSON file to validate')
    parser.add_argument('--check-live', metavar='URL', help='Validate a live page URL')
    parser.add_argument('--strict', action='store_true', help='Treat warnings as errors')

    args = parser.parse_args()

    if args.check_live:
        print(f"Validating live page: {args.check_live}")
        is_valid, errors, warnings = validate_live_page(args.check_live)
    elif args.file:
        print(f"Validating template: {args.file}")
        validator = TemplateValidator(strict=args.strict)
        is_valid, errors, warnings = validator.validate_json_file(args.file)
    else:
        parser.print_help()
        sys.exit(1)

    # Print results
    if errors:
        print("\nERRORS:")
        for err in errors:
            print(f"  ✗ {err}")

    if warnings:
        print("\nWARNINGS:")
        for warn in warnings:
            print(f"  ⚠ {warn}")

    if is_valid:
        print("\n✓ Validation passed")
        sys.exit(0)
    else:
        print("\n✗ Validation failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
