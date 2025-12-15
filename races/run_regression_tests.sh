#!/bin/bash
# Run all regression tests for the unified training system

set -e

echo "=========================================="
echo "Unified Training System - Regression Tests"
echo "=========================================="
echo ""

# Change to races directory
cd "$(dirname "$0")"

# Test 1: Unified system tests
echo "Test 1: Unified System Tests"
echo "----------------------------"
python3 test_unified_system.py -v
echo ""

# Test 2: Strength generator tests (if exists)
if [ -f "generation_modules/test_strength_generator.py" ]; then
    echo "Test 2: Strength Generator Tests"
    echo "-------------------------------"
    python3 -m unittest generation_modules.test_strength_generator -v
    echo ""
fi

# Test 3: Exercise library tests (if exists)
if [ -f "generation_modules/test_exercise_library.py" ]; then
    echo "Test 3: Exercise Library Tests"
    echo "------------------------------"
    python3 -m unittest generation_modules.test_exercise_library -v
    echo ""
fi

# Test 4: Exercise lookup tests (if exists)
if [ -f "generation_modules/test_exercise_lookup.py" ]; then
    echo "Test 4: Exercise Lookup Tests"
    echo "-----------------------------"
    python3 -m unittest generation_modules.test_exercise_lookup -v
    echo ""
fi

echo "=========================================="
echo "All regression tests complete!"
echo "=========================================="

