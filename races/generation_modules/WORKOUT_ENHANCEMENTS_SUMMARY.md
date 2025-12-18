# Workout Enhancements Summary

## Implemented Features

### 1. ✅ URLs for All Exercises
**Status**: Complete

- Replaced all `gravelgod.com/demos` references with direct video URLs
- Added URLs to warmup/cooldown exercises using exercise library
- All exercises now have clickable video links in TrainingPeaks

**Implementation**:
- `add_urls_to_all_exercises()` function in `workout_enhancements.py`
- Maps 24+ warmup/cooldown exercises to PN Vimeo URLs
- Falls back to fuzzy matching via exercise library for unmatched exercises

**Example**:
```
★ WARMUP (10 min)
  • Downward Dog Lunge + Rotation ─ 5/side
     → https://vimeo.com/111032509
  • Tripod Bridge ─ 5/side
     → https://vimeo.com/111033887
```

---

### 2. ✅ Workout Duration Estimation
**Status**: Complete

- Automatically calculates workout duration based on Main 1 and Main 2 exercises
- Includes warmup, prep, main work, core (if present), and cooldown
- Duration displayed in description header and ZWO file `<FreeRide>` block

**Calculation**:
- Warmup: Fixed (8-10 min, from template)
- Prep: Fixed (5 min, from template)
- Main 1: Sets × (45s exercise time + rest time) / 60
- Main 2: Sets × (45s exercise time + rest time) / 60
- Core: Fixed (from template, if present)
- Cooldown: Fixed (5 min, from template)
- **Rounded to nearest 5 minutes, minimum 30 min**

**Example**:
```
★ STRENGTH: Learn to Lift │ Session A │ Week 1

  Movement quality before load.

  RPE Target: 5-6 │ Equipment: Bodyweight, bands, light DB/KB │ Duration: ~35 min
```

**ZWO File**:
```xml
<FreeRide Duration="2100" Power="0.0"/>
```
(35 minutes × 60 = 2100 seconds)

---

### 3. ✅ Workout Context (Previous/Next Workout Connections)
**Status**: Complete

- Adds context about previous and next workouts to build athlete trust
- Shows progression between phases
- Indicates when continuing same phase vs. transitioning

**Implementation**:
- `get_workout_context()` function in `workout_enhancements.py`
- Analyzes `STRENGTH_SCHEDULE` to determine previous/next workouts
- Generates contextual messages based on phase transitions

**Example Messages**:
- "Building on Learn to Lift from last week."
- "Continuing this phase's progression."
- "Next week transitions to Lift Heavy Sh*t."

**Location**: Added to description header, below equipment/duration line

---

## Files Modified

1. **`workout_enhancements.py`** (NEW)
   - `add_urls_to_all_exercises()` - URL replacement
   - `estimate_workout_duration()` - Duration calculation
   - `get_workout_context()` - Context generation
   - `WARMUP_COOLDOWN_EXERCISES` dictionary - Exercise URL mappings

2. **`strength_generator.py`** (MODIFIED)
   - Imports workout enhancements module
   - `format_description_with_tagline()` - Now includes duration and context
   - `create_strength_zwo_file()` - Uses estimated duration in `<FreeRide>` block
   - Passes `plan_weeks` parameter for context generation

---

## Testing

### Manual Test
```bash
cd races/generation_modules
python3 strength_generator.py --test --output /tmp/test_enhanced
```

### Verify Output
1. Check description header includes duration
2. Check warmup/cooldown exercises have URLs
3. Check context message appears (if applicable)
4. Check ZWO file `<FreeRide>` has correct duration in seconds

---

## Next Steps

1. **Test TrainingPeaks Import**: Verify duration shows correctly in calendar
2. **Validate URLs**: Ensure all warmup/cooldown URLs are clickable
3. **Review Context Messages**: Ensure messages are helpful and accurate
4. **Update Regression Tests**: Add tests for new features

---

## Notes

- Duration estimation is conservative (rounded up to nearest 5 min)
- Context messages only appear when there's a meaningful transition
- URL matching uses exact match first, then partial match, then fuzzy match
- All enhancements are optional (module can be disabled if needed)

