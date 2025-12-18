#!/usr/bin/env python3
"""
Master test runner for all landing page automation modules.

Run: python3 automation/run_all_tests.py
"""

import subprocess
import sys
from pathlib import Path

# Get the automation directory
AUTOMATION_DIR = Path(__file__).parent

# All test files
TEST_FILES = [
    'test_blackpill.py',
    'test_hero.py',
    'test_vitals.py',
    'test_ratings.py',
    'test_course_map.py',
    'test_overview_hero.py',
    'test_tldr.py',
    'test_history.py',
    'test_biased_opinion.py',
    'test_final_verdict.py',
    'test_logistics.py',
    'test_ctas.py',
    'test_training_plans_section.py',
]


def run_all_tests():
    """Run all test files and collect results."""
    print("\n" + "=" * 60)
    print("  GRAVEL GOD LANDING PAGE - FULL TEST SUITE")
    print("=" * 60 + "\n")
    
    results = []
    total_passed = 0
    total_failed = 0
    
    for test_file in TEST_FILES:
        test_path = AUTOMATION_DIR / test_file
        if not test_path.exists():
            print(f"⚠️  {test_file} not found, skipping...")
            continue
        
        print(f"Running {test_file}...")
        result = subprocess.run(
            [sys.executable, str(test_path)],
            capture_output=True,
            text=True,
            cwd=str(AUTOMATION_DIR.parent)
        )
        
        # Parse results from output
        output = result.stdout + result.stderr
        
        if result.returncode == 0:
            # Extract pass count from output
            lines = output.strip().split('\n')
            for line in lines:
                if 'passed' in line and 'failed' in line:
                    parts = line.split()
                    for i, p in enumerate(parts):
                        if p == 'passed,':
                            passed = int(parts[i-1])
                            total_passed += passed
                        if p == 'failed':
                            failed = int(parts[i-1])
                            total_failed += failed
            results.append((test_file, 'PASSED', None))
            print(f"  ✅ {test_file}")
        else:
            results.append((test_file, 'FAILED', output))
            print(f"  ❌ {test_file}")
            total_failed += 1
    
    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    print(f"\n  Total tests: {total_passed + total_failed}")
    print(f"  ✅ Passed: {total_passed}")
    print(f"  ❌ Failed: {total_failed}")
    print(f"\n  Modules tested: {len(TEST_FILES)}")
    
    # Show failures if any
    failures = [r for r in results if r[1] == 'FAILED']
    if failures:
        print("\n" + "-" * 60)
        print("  FAILURES:")
        print("-" * 60)
        for name, status, output in failures:
            print(f"\n  {name}:")
            if output:
                for line in output.split('\n')[-20:]:  # Last 20 lines
                    print(f"    {line}")
    
    print("\n" + "=" * 60)
    
    if total_failed == 0:
        print("\n  🎉 ALL TESTS PASSED - SAFE TO DEPLOY\n")
        return 0
    else:
        print(f"\n  ⚠️  {total_failed} FAILURE(S) - FIX BEFORE DEPLOY\n")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
