#!/usr/bin/env python3
"""
Regression test: Verify that generated JSON files are copied to Downloads folder
with proper LATEST-YYYYMMDD labels after generation.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

DOWNLOADS_DIR = Path.home() / "Downloads"
PROJECT_DIR = Path(__file__).parent
OUTPUT_DIR = PROJECT_DIR / "output"

# Expected files to check (only files that should be in Downloads)
EXPECTED_FILES = {
    "mid-south": {
        "output": "elementor-mid-south.json",
        "downloads_pattern": "elementor-mid-south-LATEST-*.json"
    },
    "bwr-ca": {
        "output": "elementor-belgian-waffle-ride.json",
        "downloads_pattern": "elementor-belgian-waffle-ride-CA-LATEST-*.json"
    }
}


def find_latest_download_file(pattern: str) -> Path:
    """Find the most recent file matching pattern in Downloads."""
    matches = list(DOWNLOADS_DIR.glob(pattern))
    if not matches:
        return None
    
    # Sort by modification time, return most recent
    return max(matches, key=lambda p: p.stat().st_mtime)


def verify_downloads_files() -> list:
    """Verify that all expected files exist in Downloads with proper naming."""
    errors = []
    today = datetime.now().strftime("%Y%m%d")
    
    for race_name, file_info in EXPECTED_FILES.items():
        output_file = OUTPUT_DIR / file_info["output"]
        downloads_pattern = file_info["downloads_pattern"]
        
        # Check if output file exists
        if not output_file.exists():
            errors.append(f"Output file missing: {output_file}")
            continue
        
        # Find latest download file
        latest_download = find_latest_download_file(downloads_pattern)
        
        if not latest_download:
            errors.append(f"Download file missing for {race_name}: No file matching {downloads_pattern} in Downloads")
            continue
        
        # Verify filename format
        filename = latest_download.name
        if "LATEST-" not in filename:
            errors.append(f"Download file for {race_name} missing 'LATEST-' in filename: {filename}")
        
        # Verify it's from today or recent (within last 7 days)
        file_mtime = datetime.fromtimestamp(latest_download.stat().st_mtime)
        days_old = (datetime.now() - file_mtime).days
        if days_old > 7:
            errors.append(f"Download file for {race_name} is {days_old} days old (expected recent): {latest_download.name}")
        
        # Verify file sizes match (roughly - allow some variance)
        output_size = output_file.stat().st_size
        download_size = latest_download.stat().st_size
        size_diff = abs(output_size - download_size)
        if size_diff > 1000:  # Allow 1KB difference
            errors.append(f"Download file for {race_name} size mismatch: output={output_size}, download={download_size}")
    
    return errors


def main():
    """Run downloads regression test."""
    print("=" * 80)
    print("DOWNLOADS REGRESSION TEST")
    print("=" * 80)
    print(f"Checking Downloads folder: {DOWNLOADS_DIR}")
    print(f"Checking output folder: {OUTPUT_DIR}")
    print()
    
    errors = verify_downloads_files()
    
    if errors:
        print("✗ FAILED: Downloads regression test")
        print()
        for error in errors:
            print(f"  ERROR: {error}")
        print()
        return 1
    else:
        print("✓ PASSED: All expected files found in Downloads with proper LATEST- labels")
        print()
        # Show what we found
        for race_name, file_info in EXPECTED_FILES.items():
            latest = find_latest_download_file(file_info["downloads_pattern"])
            if latest:
                size_kb = latest.stat().st_size / 1024
                mtime = datetime.fromtimestamp(latest.stat().st_mtime)
                print(f"  ✓ {race_name}: {latest.name} ({size_kb:.1f}KB, {mtime.strftime('%Y-%m-%d %H:%M')})")
        print()
        return 0


if __name__ == "__main__":
    sys.exit(main())
