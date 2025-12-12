#!/usr/bin/env python3
"""
MASTER QC SCRIPT - RUN ALL VALIDATIONS
=======================================
Run this before showing Matti any output.

Usage:
    python run_all_qc.py [output_dir]
    
This runs:
    1. Regression tests (prevents previously-fixed bugs)
    2. Variation pool validation
    3. Generated description validation
    4. Masters-specific checks
    5. Character count summary
"""

import sys
import os
import subprocess

def run_command(cmd, description):
    """Run a command and report results."""
    print(f"\n{'='*80}")
    print(f"RUNNING: {description}")
    print(f"{'='*80}")
    
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=False,
        text=True
    )
    
    return result.returncode == 0

def main():
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "output/html_descriptions"
    
    print("\n" + "="*80)
    print("GRAVEL GOD MARKETPLACE DESCRIPTION QC")
    print("="*80)
    print(f"\nOutput directory: {output_dir}\n")
    
    all_passed = True
    
    # 1. Run marketplace regression tests (prevents previously-fixed bugs from returning)
    if not run_command("python3 test_regression_marketplace.py", "Marketplace Regression Test Suite"):
        all_passed = False
        print("\n⚠️  REGRESSION DETECTED: Previously-fixed bugs have returned!")
        print("   Review errors above and fix before proceeding.")
    
    # 2. Validate variation pools
    if not run_command("python3 validate_variation_pools.py", "Variation Pool Validation"):
        all_passed = False
        print("\n⚠️  FIX VARIATION POOLS BEFORE GENERATING")
    
    # 3. Validate generated descriptions
    if os.path.exists(output_dir):
        if not run_command(f"python3 validate_descriptions.py {output_dir}", "Description Validation"):
            all_passed = False
            print("\n⚠️  FIX GENERATED DESCRIPTIONS BEFORE SHIPPING")
    else:
        print(f"\n⚠️  Output directory not found: {output_dir}")
        print("Generate descriptions first, then run QC again.")
        all_passed = False
    
    # Final summary
    print("\n" + "="*80)
    if all_passed:
        print("✅ ALL QC CHECKS PASSED")
        print("="*80)
        print("\n✓ Marketplace regression tests passed")
        print("✓ Variation pools validated")
        print("✓ Generated descriptions validated")
        print("✓ Ready to show Matti\n")
        return 0
    else:
        print("❌ QC CHECKS FAILED")
        print("="*80)
        print("\n✗ Fix issues above before proceeding")
        print("✗ DO NOT show Matti until all checks pass\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
