#!/usr/bin/env python3
"""
RACE-AGNOSTIC DESCRIPTIONS REGRESSION TEST
===========================================
Ensures workout descriptions remain race-agnostic for scalability.

Race names should NOT appear in regular workout descriptions.
Only RACE_DAY.zwo files may contain race names (intentional).

This enables the same workout library to be used across 400+ race plans
without race-specific text embedded in each workout file.

Fixed: 2024-12-29 - Removed race name prefixes from all note functions

Exit codes:
    0 = All regression tests passed
    1 = Regression detected (race names found in workout descriptions)
"""

import os
import re
import sys
from pathlib import Path

# Known race names to check for (add new races here)
RACE_NAMES = [
    "UNBOUND GRAVEL 200",
    "UNBOUND GRAVEL",
    "MID SOUTH",
    "MIDSOUTH",
    "BELGIAN WAFFLE RIDE",
    "BWR",
    "LEADVILLE",
    "DIRTY KANZA",  # Old name for Unbound
    "GRAVEL WORLDS",
    "SBT GRVL",
    "STEAMBOAT GRAVEL",
]

# Patterns that should NOT appear in regular workout descriptions
# These are the old race-specific prefixes
FORBIDDEN_PATTERNS = [
    r"• [A-Z\s]+ - HYDRATION:",  # e.g., "• UNBOUND GRAVEL 200 - HYDRATION:"
    r"• [A-Z\s]+ - DAILY BASELINE HYDRATION:",
    r"• [A-Z\s]+ - HEAT TRAINING",
    r"• [A-Z\s]+ - WEATHER",
    r"• [A-Z\s]+ - AGGRESSIVE FUELING:",
    r"• [A-Z\s]+ - DRESS REHEARSAL:",
    r"• [A-Z\s]+ - ROBUST TAPER:",
    r"• [A-Z\s]+ - GRAVEL GRIT:",
    r"• [A-Z\s]+ - HEAT MAINTENANCE:",
    r"• [A-Z\s]+ - WEATHER MAINTENANCE:",
]

# Files that ARE allowed to contain race names
ALLOWED_FILES = [
    "RACE_DAY.zwo",
    "race_data.json",
]


def check_file_for_race_names(filepath: Path) -> list:
    """Check a single file for race names in descriptions."""
    issues = []

    # Skip allowed files
    if filepath.name in ALLOWED_FILES:
        return []

    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        return [f"Could not read file: {e}"]

    # Only check ZWO files
    if filepath.suffix.lower() != '.zwo':
        return []

    # Extract description content
    desc_match = re.search(r'<description>(.*?)</description>', content, re.DOTALL)
    if not desc_match:
        return []

    description = desc_match.group(1)

    # Check for forbidden patterns (race-specific prefixes)
    for pattern in FORBIDDEN_PATTERNS:
        matches = re.findall(pattern, description)
        for match in matches:
            # Make sure it's actually a race name, not just the generic format
            for race_name in RACE_NAMES:
                if race_name in match.upper():
                    issues.append(f"Found race-specific prefix: '{match}'")
                    break

    # Check for race names in bullet points (but allow in general prose)
    for race_name in RACE_NAMES:
        # Look for race name in bullet point format
        pattern = rf"• {re.escape(race_name)}\s*-"
        if re.search(pattern, description, re.IGNORECASE):
            issues.append(f"Found race name in bullet prefix: '{race_name}'")

    return issues


def run_regression_test():
    """Run the race-agnostic regression test."""
    print("=" * 80)
    print("RACE-AGNOSTIC DESCRIPTIONS REGRESSION TEST")
    print("=" * 80)
    print()

    # Find races directory
    script_dir = Path(__file__).parent
    races_dir = script_dir / "races"

    if not races_dir.exists():
        print(f"❌ Races directory not found: {races_dir}")
        return 1

    total_files = 0
    files_with_issues = 0
    all_issues = []

    # Find all ZWO files in race plan folders
    for zwo_file in races_dir.rglob("*.zwo"):
        # Skip strength workout library (not race-specific)
        if "strength_workouts" in str(zwo_file):
            continue

        total_files += 1
        issues = check_file_for_race_names(zwo_file)

        if issues:
            files_with_issues += 1
            rel_path = zwo_file.relative_to(script_dir)
            all_issues.append((rel_path, issues))

    # Report results
    if all_issues:
        print(f"❌ REGRESSION DETECTED: {files_with_issues} files contain race-specific descriptions")
        print()
        for filepath, issues in all_issues[:10]:  # Show first 10
            print(f"  {filepath}:")
            for issue in issues:
                print(f"    - {issue}")
        if len(all_issues) > 10:
            print(f"  ... and {len(all_issues) - 10} more files")
        print()
        print("FIX: Workout descriptions should use generic prefixes like:")
        print("  • HYDRATION:")
        print("  • DAILY BASELINE HYDRATION:")
        print("  • HEAT TRAINING PROTOCOL:")
        print("  NOT race-specific prefixes like:")
        print("  • UNBOUND GRAVEL 200 - HYDRATION:")
        print()
        return 1

    print(f"✓ Race-Agnostic Descriptions")
    print(f"  Checked {total_files} ZWO files - no race-specific prefixes found")
    print()
    print("=" * 80)
    print(f"RESULTS: All tests passed")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(run_regression_test())
