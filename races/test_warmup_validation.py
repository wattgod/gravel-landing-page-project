#!/usr/bin/env python3
"""
Regression tests for workout warmup structure.

Validates that all archetype workouts have proper warmup:
- 10min Z1/Z2 warmup (600 seconds, PowerLow 0.50, PowerHigh 0.65)
- 5min high cadence Z3 (300 seconds, Power 0.85, Cadence 100)
"""

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple

# Archetypes that might have different warmup structures
SPECIAL_WARMUP_ARCHETYPES = ["testing", "rest", "endurance"]  # These may have different structures

def parse_zwo_file(filepath: str) -> Dict:
    """Parse a ZWO file and extract warmup information."""
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        result = {
            "filepath": filepath,
            "has_warmup": False,
            "warmup_duration": None,
            "warmup_power_low": None,
            "warmup_power_high": None,
            "has_z3_warmup": False,
            "z3_duration": None,
            "z3_power": None,
            "z3_cadence": None,
            "description": "",
            "errors": [],
            "warnings": []
        }
        
        # Get description
        desc_elem = root.find("description")
        if desc_elem is not None and desc_elem.text:
            result["description"] = desc_elem.text
        
        # Find workout element (warmup is inside <workout>)
        workout = root.find("workout")
        if workout is None:
            return result
        
        # Find Warmup element
        warmup = workout.find("Warmup")
        if warmup is not None:
            result["has_warmup"] = True
            result["warmup_duration"] = int(warmup.get("Duration", 0))
            result["warmup_power_low"] = float(warmup.get("PowerLow", 0))
            result["warmup_power_high"] = float(warmup.get("PowerHigh", 0))
        
        # Find SteadyState blocks (look for Z3 warmup after Warmup)
        # We'll check all SteadyState blocks and identify the warmup Z3
        steady_states = workout.findall("SteadyState")
        for ss in steady_states:
            power = float(ss.get("Power", 0))
            duration = int(ss.get("Duration", 0))
            cadence = ss.get("Cadence")
            
            # Z3 warmup: Power 0.85, Duration 300, Cadence 100
            if power == 0.85 and duration == 300:
                if cadence and int(cadence) >= 100:
                    result["has_z3_warmup"] = True
                    result["z3_duration"] = duration
                    result["z3_power"] = power
                    result["z3_cadence"] = int(cadence) if cadence else None
        
        return result
    except Exception as e:
        return {
            "filepath": filepath,
            "errors": [f"Parse error: {str(e)}"],
            "has_warmup": False,
            "has_z3_warmup": False
        }

def validate_warmup_structure(parsed: Dict, filename: str) -> List[str]:
    """Validate warmup structure against requirements."""
    errors = []
    warnings = []
    
    # Check if this is a special archetype
    is_special = any(arch in filename.lower() for arch in SPECIAL_WARMUP_ARCHETYPES)
    
    # Standard warmup requirements
    if not is_special:
        # 1. Must have Warmup element
        if not parsed["has_warmup"]:
            errors.append("Missing <Warmup> element")
        else:
            # 2. Warmup should be 10min (600 seconds)
            if parsed["warmup_duration"] != 600:
                errors.append(f"Warmup duration should be 600s (10min), found {parsed['warmup_duration']}s")
            
            # 3. PowerLow should be 0.50
            if parsed["warmup_power_low"] != 0.50:
                errors.append(f"Warmup PowerLow should be 0.50, found {parsed['warmup_power_low']}")
            
            # 4. PowerHigh should be 0.65
            if parsed["warmup_power_high"] != 0.65:
                errors.append(f"Warmup PowerHigh should be 0.65, found {parsed['warmup_power_high']}")
        
        # 5. Must have Z3 warmup block (5min high cadence)
        if not parsed["has_z3_warmup"]:
            errors.append("Missing 5min high cadence Z3 warmup block (300s @ 0.85 power, 100+ cadence)")
        else:
            # 6. Z3 duration should be 300 seconds
            if parsed["z3_duration"] != 300:
                errors.append(f"Z3 warmup duration should be 300s (5min), found {parsed['z3_duration']}s")
            
            # 7. Z3 power should be 0.85
            if parsed["z3_power"] != 0.85:
                errors.append(f"Z3 warmup power should be 0.85, found {parsed['z3_power']}")
            
            # 8. Z3 cadence should be 100+
            if parsed["z3_cadence"] is None or parsed["z3_cadence"] < 100:
                warnings.append(f"Z3 warmup cadence should be 100+, found {parsed['z3_cadence']}")
    
    # Check description mentions warmup
    if parsed["description"]:
        desc_lower = parsed["description"].lower()
        if "warm-up" in desc_lower or "warmup" in desc_lower:
            # Check for 10min mention
            if "10min" not in desc_lower and "10 min" not in desc_lower:
                warnings.append("Description mentions warmup but not '10min'")
            
            # Check for high cadence Z3 mention
            if "high cadence" not in desc_lower and "z3" not in desc_lower:
                warnings.append("Description mentions warmup but not 'high cadence Z3'")
    
    return errors, warnings

def test_all_archetype_workouts():
    """Test all archetype workout files."""
    script_dir = Path(__file__).parent
    # Check both possible locations
    archetype_dir = script_dir / "archetype_examples"
    if not archetype_dir.exists():
        # Try Downloads folder
        downloads_dir = Path.home() / "Downloads" / "archetype_examples"
        if downloads_dir.exists():
            archetype_dir = downloads_dir
        else:
            print(f"❌ Archetype examples directory not found in:")
            print(f"   - {script_dir / 'archetype_examples'}")
            print(f"   - {downloads_dir}")
            return False
    
    # Find all ZWO files
    zwo_files = list(archetype_dir.rglob("*.zwo"))
    
    if not zwo_files:
        print(f"❌ No ZWO files found in {archetype_dir}")
        return False
    
    print(f"🔍 Testing {len(zwo_files)} workout files...")
    print("=" * 80)
    
    all_errors = []
    all_warnings = []
    passed = 0
    failed = 0
    
    for zwo_file in sorted(zwo_files):
        parsed = parse_zwo_file(str(zwo_file))
        errors, warnings = validate_warmup_structure(parsed, zwo_file.name)
        
        # Get relative path for display
        try:
            rel_path = str(zwo_file.relative_to(archetype_dir))
        except ValueError:
            rel_path = str(zwo_file)
        
        if errors:
            failed += 1
            all_errors.append({
                "file": zwo_file.name,
                "path": rel_path,
                "errors": errors,
                "warnings": warnings
            })
        else:
            passed += 1
            if warnings:
                all_warnings.append({
                    "file": zwo_file.name,
                    "path": rel_path,
                    "warnings": warnings
                })
    
    # Print results
    print(f"\n✅ PASSED: {passed}")
    print(f"❌ FAILED: {failed}")
    
    if all_errors:
        print(f"\n❌ ERRORS ({len(all_errors)} files):")
        for item in all_errors[:10]:  # Show first 10
            print(f"  • {item['path']}")
            for err in item["errors"]:
                print(f"    - {err}")
        if len(all_errors) > 10:
            print(f"  ... and {len(all_errors) - 10} more files with errors")
    
    if all_warnings:
        print(f"\n⚠️  WARNINGS ({len(all_warnings)} files):")
        for item in all_warnings[:5]:  # Show first 5
            print(f"  • {item['path']}")
            for warn in item["warnings"]:
                print(f"    - {warn}")
        if len(all_warnings) > 5:
            print(f"  ... and {len(all_warnings) - 5} more files with warnings")
    
    print("=" * 80)
    
    if failed > 0:
        print(f"❌ VALIDATION FAILED: {failed} file(s) have errors")
        return False
    else:
        print("✅ All warmup validations passed!")
        return True

def test_warmup_description_format():
    """Test that warmup descriptions are properly formatted."""
    script_dir = Path(__file__).parent
    archetype_dir = script_dir / "archetype_examples"
    if not archetype_dir.exists():
        downloads_dir = Path.home() / "Downloads" / "archetype_examples"
        if downloads_dir.exists():
            archetype_dir = downloads_dir
    
    zwo_files = list(archetype_dir.rglob("*.zwo"))
    
    print(f"\n🔍 Testing warmup description format in {len(zwo_files)} files...")
    
    missing_10min = []
    missing_z3_mention = []
    missing_rpe = []
    
    for zwo_file in zwo_files:
        parsed = parse_zwo_file(str(zwo_file))
        desc = parsed.get("description", "").lower()
        
        # Skip special archetypes
        if any(arch in zwo_file.name.lower() for arch in SPECIAL_WARMUP_ARCHETYPES):
            continue
        
        if "warm-up" in desc or "warmup" in desc:
            if "10min" not in desc and "10 min" not in desc:
                missing_10min.append(zwo_file.name)
            
            if "high cadence" not in desc and ("z3" not in desc or "cadence" not in desc):
                missing_z3_mention.append(zwo_file.name)
            
            if "rpe" not in desc:
                missing_rpe.append(zwo_file.name)
    
    issues = False
    
    if missing_10min:
        print(f"⚠️  {len(missing_10min)} files missing '10min' in warmup description")
        issues = True
    
    if missing_z3_mention:
        print(f"⚠️  {len(missing_z3_mention)} files missing 'high cadence Z3' in warmup description")
        issues = True
    
    if missing_rpe:
        print(f"⚠️  {len(missing_rpe)} files missing 'RPE' in warmup description")
        issues = True
    
    if not issues:
        print("✅ All warmup descriptions properly formatted")
    
    return not issues

if __name__ == "__main__":
    print("=" * 80)
    print("WARMUP VALIDATION TEST SUITE")
    print("=" * 80)
    
    test1_passed = test_all_archetype_workouts()
    test2_passed = test_warmup_description_format()
    
    print("\n" + "=" * 80)
    if test1_passed and test2_passed:
        print("✅ ALL TESTS PASSED")
        exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        exit(1)

