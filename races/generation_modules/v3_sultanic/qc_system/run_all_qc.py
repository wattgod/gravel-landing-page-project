#!/usr/bin/env python3
"""
Master QC script - runs all validations.

Usage:
    python run_all_qc.py

Returns:
    0 if all validations pass
    1 if any validation fails
"""

import sys
import subprocess
from pathlib import Path

def run_validation(script_name: str) -> bool:
    """Run a validation script and return True if it passes."""
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        print(f"ERROR: Validation script not found: {script_path}")
        return False
    
    print(f"\n{'=' * 80}")
    print(f"Running: {script_name}")
    print('=' * 80)
    
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=False
    )
    
    return result.returncode == 0


def main():
    """Run all QC validations."""
    print("\n" + "=" * 80)
    print("RUNNING ALL QC VALIDATIONS")
    print("=" * 80)
    
    # Run pool validation
    pools_ok = run_validation('validate_variation_pools.py')
    
    # Run description validation
    descriptions_ok = run_validation('validate_descriptions.py')
    
    # Summary
    print("\n" + "=" * 80)
    print("QC SUMMARY")
    print("=" * 80)
    print(f"Variation Pools: {'✓ PASSED' if pools_ok else '✗ FAILED'}")
    print(f"Descriptions: {'✓ PASSED' if descriptions_ok else '✗ FAILED'}")
    print("=" * 80)
    
    if pools_ok and descriptions_ok:
        print("\n✓ ALL VALIDATIONS PASSED")
        print("Safe to show Matti.")
        sys.exit(0)
    else:
        print("\n✗ VALIDATION FAILED")
        print("DO NOT show Matti until fixed.")
        sys.exit(1)


if __name__ == '__main__':
    main()


