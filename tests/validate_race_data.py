#!/usr/bin/env python3
"""
Race Data Validation Tests

Validates race data JSON files against research markdown files to catch:
- Missing research files
- Fabricated/contradictory data
- Score/explanation mismatches
- Placeholder text
- Numeric field discrepancies

Usage:
    python tests/validate_race_data.py              # Run all validations
    python tests/validate_race_data.py mid-south    # Validate specific race
    python tests/validate_race_data.py --report     # Generate full report
"""

import json
import os
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RESEARCH_DIR = PROJECT_ROOT / "research"

# Validation thresholds
ELEVATION_TOLERANCE_PCT = 0.30  # 30% tolerance for elevation differences
DISTANCE_TOLERANCE_PCT = 0.10   # 10% tolerance for distance differences


@dataclass
class ValidationIssue:
    race: str
    severity: str  # "ERROR", "WARNING", "INFO"
    category: str
    message: str
    data_value: Optional[str] = None
    research_value: Optional[str] = None


@dataclass
class ValidationResult:
    race: str
    has_research: bool = False
    has_data: bool = False
    validation_tier: str = "bronze"  # gold, silver, bronze
    issues: list = field(default_factory=list)

    @property
    def is_valid(self):
        # Gold tier: no errors allowed
        # Silver tier: errors become warnings (more lenient)
        # Bronze tier: always valid (stub, needs research)
        if self.validation_tier == "bronze":
            return True
        elif self.validation_tier == "silver":
            return not any(i.severity == "ERROR" and i.category not in ["missing_file"] for i in self.issues)
        else:  # gold
            return not any(i.severity == "ERROR" for i in self.issues)

    @property
    def error_count(self):
        return sum(1 for i in self.issues if i.severity == "ERROR")

    @property
    def warning_count(self):
        return sum(1 for i in self.issues if i.severity == "WARNING")

    @property
    def info_count(self):
        return sum(1 for i in self.issues if i.severity == "INFO")


def extract_numbers_from_text(text: str) -> list[float]:
    """Extract all numbers from text, handling commas and units."""
    # Find patterns like "10,000", "119.7", "2,900-3,700"
    numbers = []
    patterns = [
        r'(\d{1,3}(?:,\d{3})+(?:\.\d+)?)',  # Numbers with commas: 10,000
        r'(\d+(?:\.\d+)?)',                   # Regular numbers: 119.7
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            num_str = match.group(1).replace(',', '')
            try:
                numbers.append(float(num_str))
            except ValueError:
                pass
    return numbers


def parse_research_file(filepath: Path) -> dict:
    """Parse research markdown file and extract key facts."""
    if not filepath.exists():
        return {}

    content = filepath.read_text(encoding='utf-8')
    facts = {
        'raw_content': content,
        'distances': [],
        'elevations': [],
        'locations': [],
        'dates': [],
        'field_sizes': [],
        'cutoffs': [],
        'terrain_percentages': [],
    }

    # Extract from OFFICIAL DATA table if present
    lines = content.split('\n')
    in_table = False

    for i, line in enumerate(lines):
        line_lower = line.lower()

        # Distance extraction
        if 'distance' in line_lower:
            numbers = extract_numbers_from_text(line)
            facts['distances'].extend(numbers)

        # Elevation extraction
        if any(term in line_lower for term in ['elevation', 'climbing', 'gain', 'vert']):
            numbers = extract_numbers_from_text(line)
            # Filter to reasonable elevation values (100-50000 ft or 30-15000 m)
            # Exclude likely year values (2015-2030)
            for n in numbers:
                if 100 <= n <= 50000 and not (2015 <= n <= 2030):
                    facts['elevations'].append(n)

        # Location extraction
        if 'location' in line_lower or 'venue' in line_lower:
            # Look for city, state/country patterns
            location_match = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z][a-z]+)', line)
            if location_match:
                facts['locations'].append(location_match.group(1))

        # Terrain percentage extraction
        if 'unroad' in line_lower or 'gravel' in line_lower or 'terrain' in line_lower:
            pct_matches = re.findall(r'(\d+)%', line)
            for pct in pct_matches:
                facts['terrain_percentages'].append(int(pct))

        # Cutoff time extraction
        if 'cutoff' in line_lower or 'time limit' in line_lower:
            numbers = extract_numbers_from_text(line)
            for n in numbers:
                if 5 <= n <= 48:  # Reasonable hour range
                    facts['cutoffs'].append(n)

    return facts


def load_data_file(filepath: Path) -> dict:
    """Load and parse race data JSON file."""
    if not filepath.exists():
        return {}

    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def check_placeholders(data: dict, race: str) -> list[ValidationIssue]:
    """Check for placeholder text in data."""
    issues = []
    placeholders = ['TBD', 'PLACEHOLDER', 'TODO', 'FIXME', 'XXX', 'NEEDS_RESEARCH']

    def search_dict(d, path=""):
        if isinstance(d, dict):
            for k, v in d.items():
                search_dict(v, f"{path}.{k}" if path else k)
        elif isinstance(d, list):
            for i, item in enumerate(d):
                search_dict(item, f"{path}[{i}]")
        elif isinstance(d, str):
            for ph in placeholders:
                if ph in d.upper():
                    issues.append(ValidationIssue(
                        race=race,
                        severity="WARNING",
                        category="placeholder",
                        message=f"Placeholder text '{ph}' found at {path}",
                        data_value=d[:100]
                    ))

    search_dict(data)
    return issues


def check_score_explanation_consistency(data: dict, race: str) -> list[ValidationIssue]:
    """Check that scores match their explanations."""
    issues = []

    ratings = data.get('race', {}).get('ratings_breakdown', {})

    # Altitude score check
    altitude = ratings.get('altitude', {})
    if altitude:
        score = altitude.get('score', 0)
        explanation = altitude.get('explanation', '').lower()

        # High score (4-5) should NOT say altitude is irrelevant/zero/none
        # But it SHOULD mention altitude challenges - that's correct!
        # Only flag if explanation explicitly dismisses altitude as a non-factor
        dismissive_terms = ['irrelevant', 'non-factor', 'doesn\'t matter', 'not a factor', 'altitude is not']
        if score >= 4 and any(term in explanation for term in dismissive_terms):
            issues.append(ValidationIssue(
                race=race,
                severity="ERROR",
                category="score_mismatch",
                message=f"Altitude score={score} contradicts explanation dismissing altitude",
                data_value=f"Score: {score}, Explanation: {explanation[:100]}"
            ))

        # Low score (1-2) shouldn't mention high altitude challenges requiring acclimatization
        if score <= 2 and 'acclimat' in explanation and 'required' in explanation:
            issues.append(ValidationIssue(
                race=race,
                severity="WARNING",
                category="score_mismatch",
                message=f"Altitude score={score} may be too low given explanation mentions acclimatization required",
                data_value=f"Score: {score}, Explanation: {explanation[:100]}"
            ))

    # Prestige score check
    prestige = ratings.get('prestige', {})
    if prestige:
        score = prestige.get('score', 0)
        explanation = prestige.get('explanation', '').lower()

        # Score 5 should mention Lifetime Grand Prix, major purse, or iconic status
        if score == 5:
            prestige_markers = ['lifetime', 'grand prix', 'lgp', 'iconic', '$100k', '$50k', 'uci', 'world']
            if not any(marker in explanation for marker in prestige_markers):
                issues.append(ValidationIssue(
                    race=race,
                    severity="WARNING",
                    category="score_mismatch",
                    message=f"Prestige score=5 but explanation doesn't mention major prestige markers",
                    data_value=explanation[:150]
                ))

    return issues


def check_numeric_fields(data: dict, research: dict, race: str) -> list[ValidationIssue]:
    """Compare numeric fields between data and research."""
    issues = []

    vitals = data.get('race', {}).get('vitals', {})

    # Check elevation
    data_elevation = vitals.get('elevation_ft', 0)
    research_elevations = research.get('elevations', [])

    if data_elevation and research_elevations:
        # Find the closest research elevation (considering unit conversion m->ft)
        min_diff = float('inf')
        closest = None
        closest_unit = "ft"
        for re in research_elevations:
            # Try direct comparison (both in feet)
            diff_ft = abs(data_elevation - re) / max(data_elevation, re)
            # Try m->ft conversion (research might be in meters)
            re_as_ft = re * 3.281
            diff_m = abs(data_elevation - re_as_ft) / max(data_elevation, re_as_ft)

            if diff_ft < min_diff:
                min_diff = diff_ft
                closest = re
                closest_unit = "ft"
            if diff_m < min_diff:
                min_diff = diff_m
                closest = re
                closest_unit = "m"

        if min_diff > ELEVATION_TOLERANCE_PCT:
            unit_note = f" ({closest * 3.281:.0f} ft)" if closest_unit == "m" else ""
            issues.append(ValidationIssue(
                race=race,
                severity="ERROR",
                category="elevation_mismatch",
                message=f"Elevation differs by {min_diff*100:.0f}% from research",
                data_value=f"{data_elevation:,} ft",
                research_value=f"{closest:,.0f} {closest_unit}{unit_note} (closest found)"
            ))

    # Check distance
    data_distance = vitals.get('distance_mi', 0)
    research_distances = research.get('distances', [])

    if data_distance and research_distances:
        min_diff = float('inf')
        closest = None
        for rd in research_distances:
            diff = abs(data_distance - rd) / max(data_distance, rd)
            if diff < min_diff:
                min_diff = diff
                closest = rd

        if min_diff > DISTANCE_TOLERANCE_PCT:
            issues.append(ValidationIssue(
                race=race,
                severity="WARNING",
                category="distance_mismatch",
                message=f"Distance differs by {min_diff*100:.0f}% from research",
                data_value=f"{data_distance} mi",
                research_value=f"{closest:.1f} mi (closest found)"
            ))

    return issues


def check_tier_consistency(data: dict, race: str) -> list[ValidationIssue]:
    """Check that tier matches overall score."""
    issues = []

    rating = data.get('race', {}).get('gravel_god_rating', {})
    score = rating.get('overall_score', 0)
    tier = rating.get('tier', 0)
    tier_note = rating.get('tier_note', '')

    # Expected tier based on score
    if score >= 85:
        expected_tier = 1
    elif score >= 75:
        expected_tier = 2
    else:
        expected_tier = 3

    if tier != expected_tier and not tier_note:
        issues.append(ValidationIssue(
            race=race,
            severity="WARNING",
            category="tier_mismatch",
            message=f"Tier {tier} doesn't match score {score} (expected Tier {expected_tier}). Add tier_note if prestige override.",
            data_value=f"Score: {score}, Tier: {tier}"
        ))

    return issues


def check_gravel_god_math(data: dict, race: str) -> list[ValidationIssue]:
    """Verify the 14-variable scoring math adds up."""
    issues = []

    rating = data.get('race', {}).get('gravel_god_rating', {})

    # If score_note exists, math overrides are intentional - use INFO instead of ERROR
    has_score_note = bool(rating.get('score_note'))
    severity = "INFO" if has_score_note else "ERROR"

    # Course profile (7 variables)
    course_vars = ['length', 'technicality', 'elevation', 'climate', 'altitude', 'adventure', 'logistics']
    course_sum = sum(rating.get(v, 0) for v in course_vars)
    stated_course = rating.get('course_profile', 0)

    if course_sum != stated_course:
        note = f" (explained in score_note)" if has_score_note else ""
        issues.append(ValidationIssue(
            race=race,
            severity=severity,
            category="math_override" if has_score_note else "math_error",
            message=f"Course profile: sum = {course_sum}, stated = {stated_course}{note}",
            data_value=f"Variables sum: {course_sum}"
        ))

    # Editorial (7 variables)
    editorial_vars = ['prestige', 'race_quality', 'experience', 'community', 'field_depth', 'value', 'expenses']
    editorial_sum = sum(rating.get(v, 0) for v in editorial_vars)
    stated_editorial = rating.get('biased_opinion', 0)

    if editorial_sum != stated_editorial:
        note = f" (explained in score_note)" if has_score_note else ""
        issues.append(ValidationIssue(
            race=race,
            severity=severity,
            category="math_override" if has_score_note else "math_error",
            message=f"Editorial: sum = {editorial_sum}, stated = {stated_editorial}{note}",
            data_value=f"Variables sum: {editorial_sum}"
        ))

    # Overall score
    total = course_sum + editorial_sum
    expected_overall = round((total / 70) * 100)
    stated_overall = rating.get('overall_score', 0)

    if abs(expected_overall - stated_overall) > 2:  # Allow 2 point rounding tolerance
        note = f" (explained in score_note)" if has_score_note else ""
        issues.append(ValidationIssue(
            race=race,
            severity="INFO" if has_score_note else "WARNING",
            category="math_override" if has_score_note else "math_error",
            message=f"Overall score: expected ~{expected_overall}, stated {stated_overall}{note}",
            data_value=f"({course_sum}+{editorial_sum})/70*100 = {expected_overall}"
        ))

    return issues


def validate_race(race_slug: str) -> ValidationResult:
    """Run all validations for a single race."""
    result = ValidationResult(race=race_slug)

    # Find files
    data_file = DATA_DIR / f"{race_slug}-data.json"

    # Handle research file naming variations
    research_file = RESEARCH_DIR / f"{race_slug}.md"
    if not research_file.exists():
        # Try alternate names
        alternates = [
            f"bwr-california.md" if race_slug == "belgian-waffle-ride" else None,
        ]
        for alt in alternates:
            if alt:
                alt_path = RESEARCH_DIR / alt
                if alt_path.exists():
                    research_file = alt_path
                    break

    result.has_data = data_file.exists()
    result.has_research = research_file.exists()

    if not result.has_data:
        result.issues.append(ValidationIssue(
            race=race_slug,
            severity="ERROR",
            category="missing_file",
            message="Data file not found"
        ))
        return result

    if not result.has_research:
        result.issues.append(ValidationIssue(
            race=race_slug,
            severity="WARNING",
            category="missing_file",
            message="Research file not found - data may be unvalidated"
        ))

    # Load files
    data = load_data_file(data_file)
    research = parse_research_file(research_file) if result.has_research else {}

    # Get validation tier from data
    result.validation_tier = data.get('race', {}).get('validation_tier', 'bronze')

    # Run checks based on tier
    # Bronze tier: minimal checks (stub data)
    # Silver tier: standard checks
    # Gold tier: strict checks
    result.issues.extend(check_placeholders(data, race_slug))

    if result.validation_tier in ['silver', 'gold']:
        result.issues.extend(check_score_explanation_consistency(data, race_slug))
        result.issues.extend(check_tier_consistency(data, race_slug))
        result.issues.extend(check_gravel_god_math(data, race_slug))

        if research:
            result.issues.extend(check_numeric_fields(data, research, race_slug))

    return result


def get_all_races() -> list[str]:
    """Get list of all race slugs from data files."""
    races = []
    for f in DATA_DIR.glob("*-data.json"):
        slug = f.stem.replace("-data", "")
        if slug not in ['gravel_race_database', 'gravel_race_database_enhanced']:
            races.append(slug)
    return sorted(races)


def print_result(result: ValidationResult, verbose: bool = True):
    """Print validation result for a race."""
    status = "PASS" if result.is_valid else "FAIL"
    color = "\033[92m" if result.is_valid else "\033[91m"
    reset = "\033[0m"
    tier_color = {"gold": "\033[93m", "silver": "\033[37m", "bronze": "\033[33m"}.get(result.validation_tier, "")

    print(f"{color}[{status}]{reset} {result.race} {tier_color}[{result.validation_tier.upper()}]{reset}")

    if verbose or not result.is_valid:
        for issue in result.issues:
            if issue.severity == "ERROR":
                icon = "\033[91m  ERROR\033[0m"
            elif issue.severity == "WARNING":
                icon = "\033[93m  WARN \033[0m"
            else:
                icon = "\033[94m  INFO \033[0m"

            print(f"{icon} [{issue.category}] {issue.message}")
            if issue.data_value:
                print(f"         Data: {issue.data_value}")
            if issue.research_value:
                print(f"         Research: {issue.research_value}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate race data against research")
    parser.add_argument("race", nargs="?", help="Specific race to validate")
    parser.add_argument("--report", action="store_true", help="Generate full report")
    parser.add_argument("--quiet", "-q", action="store_true", help="Only show failures")
    args = parser.parse_args()

    if args.race:
        races = [args.race]
    else:
        races = get_all_races()

    results = []
    for race in races:
        result = validate_race(race)
        results.append(result)
        if not args.quiet or not result.is_valid:
            print_result(result, verbose=not args.quiet)
        if not args.quiet:
            print()

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r.is_valid)
    failed = total - passed
    total_errors = sum(r.error_count for r in results)
    total_warnings = sum(r.warning_count for r in results)
    total_infos = sum(r.info_count for r in results)

    # Tier breakdown
    gold_results = [r for r in results if r.validation_tier == "gold"]
    silver_results = [r for r in results if r.validation_tier == "silver"]
    bronze_results = [r for r in results if r.validation_tier == "bronze"]

    gold_passed = sum(1 for r in gold_results if r.is_valid)
    silver_passed = sum(1 for r in silver_results if r.is_valid)
    bronze_passed = sum(1 for r in bronze_results if r.is_valid)

    print("=" * 60)
    print(f"SUMMARY: {passed}/{total} passed, {failed} failed")
    print(f"         {total_errors} errors, {total_warnings} warnings, {total_infos} info (explained overrides)")
    print()
    print("BY TIER:")
    if gold_results:
        print(f"  🥇 Gold:   {gold_passed}/{len(gold_results)} passed (fully validated)")
    if silver_results:
        print(f"  🥈 Silver: {silver_passed}/{len(silver_results)} passed (partially validated)")
    if bronze_results:
        print(f"  🥉 Bronze: {bronze_passed}/{len(bronze_results)} passed (stubs, research pending)")
    print("=" * 60)

    # Exit with error code if any failures
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
