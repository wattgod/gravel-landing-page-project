# Regression Test Suite Summary

## Test Coverage

**Total Tests**: 36 tests across 4 test modules

### 1. `test_exercise_library.py` (6 tests)
- ✅ Library loads and parses correctly
- ✅ All exercises have required fields (name, video_url, category)
- ✅ All URLs are valid format (vimeo.com or youtube.com)
- ✅ No duplicate exercise names
- ✅ All categories are valid (squat, hinge, push, pull, core, carry, glute, mobility, plyometric, power, other)

### 2. `test_exercise_lookup.py` (10 tests)
- ✅ Exact match returns URL
- ✅ Fuzzy match handles variations (Push-Up = Pushup)
- ✅ Compound names handled (Box Jump or Squat Jump)
- ✅ Category filtering works
- ✅ Equipment filtering works
- ✅ Substitute finder works
- ✅ URL validation returns correct coverage
- ✅ Search function returns relevant results
- ✅ Library statistics are accurate

### 3. `test_zwo_generation.py` (10 tests)
- ✅ ZWO XML structure is valid
- ✅ sportType is 'bike' (TrainingPeaks compatibility)
- ✅ FreeRide block exists with correct attributes
- ✅ Title format is correct (W## STR: [Phase] ([Session]))
- ✅ Description contains tagline
- ✅ Description contains RPE target
- ✅ Description contains equipment list
- ✅ All exercises have URLs
- ✅ Unicode characters preserved (★, →, │, ─)
- ✅ Filename format is correct

### 4. `test_strength_generator.py` (12 tests)
- ✅ Template loading (16 templates)
- ✅ Pathway name mapping (new phase names)
- ✅ Session letter extraction (A/B)
- ✅ ZWO file structure validation
- ✅ ZWO file content verification
- ✅ 12-week plan mapping logic
- ✅ 20-week plan generation
- ✅ 6-week plan skip logic
- ✅ Filename format validation
- ✅ URL preservation
- ✅ Unicode preservation
- ✅ All weeks generate files (12-week regression)

---

## Running Tests

### Run All Tests
```bash
cd races/generation_modules
./run_all_regression_tests.sh
```

### Run Individual Test Modules
```bash
python3 -m unittest test_exercise_library -v
python3 -m unittest test_exercise_lookup -v
python3 -m unittest test_zwo_generation -v
python3 -m unittest test_strength_generator -v
```

### Run Specific Test
```bash
python3 -m unittest test_exercise_library.TestExerciseLibrary.test_library_loads -v
```

---

## Test Files

- `test_exercise_library.py` - Library structure and data integrity
- `test_exercise_lookup.py` - Lookup module functionality
- `test_zwo_generation.py` - ZWO file generation and format
- `test_strength_generator.py` - Strength generator integration
- `run_all_regression_tests.sh` - Test runner script

---

## Status

✅ **All 36 tests passing** (after phase name updates)

The regression test suite validates:
- Exercise library integrity (404 exercises)
- Fuzzy matching accuracy
- ZWO file format compliance
- Strength generator correctness
- Phase name updates (Learn to Lift, Lift Heavy Sh*t, Lift Fast, Don't Lose It)

