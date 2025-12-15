# Regression Test Suite - Quick Start

## Run All Tests

```bash
cd races/
./run_regression_tests.sh
```

## Test Results

✅ **29/29 tests passing**

### Test Coverage
- Phase Alignment: 5 tests ✅
- Tier Variation: 5 tests ✅
- Race Profiles: 5 tests ✅
- Weekly Structure: 5 tests ✅
- Unified Generator: 5 tests ✅
- Calendar Generation: 2 tests ✅
- Integration: 1 test ✅

## Key Tests

### Critical: No Double-Peaking
```python
# Peak cycling phase should NOT have heavy strength
assert get_strength_phase("peak") == "Lift Fast"  # Not "Lift Heavy Sh*t"
```

### Critical: Recovery Rules
```python
# No strength within 48 hours before key cycling sessions
assert "tuesday" not in strength_days  # Before Tuesday intervals
assert "friday" not in strength_days   # Before Saturday long ride
```

### Critical: Frequency Scaling
```python
# Frequency should scale: Ayahuasca >= Finisher >= Compete >= Podium
assert get_strength_frequency("ayahuasca", "base_1") >= get_strength_frequency("finisher", "base_1")
```

## Before Committing

Run tests to ensure nothing broke:
```bash
./run_regression_tests.sh
```

---

**Status**: ✅ All tests passing  
**Last Updated**: 2024-12-15

