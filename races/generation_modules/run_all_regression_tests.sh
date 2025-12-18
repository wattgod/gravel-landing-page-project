#!/bin/bash
# Run all regression tests for strength system

echo "======================================================================"
echo "STRENGTH SYSTEM REGRESSION TEST SUITE"
echo "======================================================================"
echo ""

cd "$(dirname "$0")"

# Test 1: Exercise Library
echo "📚 Test 1: Exercise Library"
echo "----------------------------------------------------------------------"
python3 -m unittest test_exercise_library -v
LIBRARY_EXIT=$?

echo ""
echo "🔍 Test 2: Exercise Lookup"
echo "----------------------------------------------------------------------"
python3 -m unittest test_exercise_lookup -v
LOOKUP_EXIT=$?

echo ""
echo "📄 Test 3: ZWO Generation"
echo "----------------------------------------------------------------------"
python3 -m unittest test_zwo_generation -v
ZWO_EXIT=$?

echo ""
echo "💪 Test 4: Strength Generator"
echo "----------------------------------------------------------------------"
python3 -m unittest test_strength_generator -v
STRENGTH_EXIT=$?

echo ""
echo "======================================================================"
echo "SUMMARY"
echo "======================================================================"

if [ $LIBRARY_EXIT -eq 0 ] && [ $LOOKUP_EXIT -eq 0 ] && [ $ZWO_EXIT -eq 0 ] && [ $STRENGTH_EXIT -eq 0 ]; then
    echo "✅ ALL TESTS PASSED"
    exit 0
else
    echo "❌ SOME TESTS FAILED"
    echo "   Library: $([ $LIBRARY_EXIT -eq 0 ] && echo '✅' || echo '❌')"
    echo "   Lookup:  $([ $LOOKUP_EXIT -eq 0 ] && echo '✅' || echo '❌')"
    echo "   ZWO:     $([ $ZWO_EXIT -eq 0 ] && echo '✅' || echo '❌')"
    echo "   Strength: $([ $STRENGTH_EXIT -eq 0 ] && echo '✅' || echo '❌')"
    exit 1
fi

