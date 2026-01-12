# Warmup Logic Documentation

## Overview

Warmup structure varies by workout archetype. Most workouts require a structured warmup, but endurance workouts start easy and build naturally, so they don't need a formal warmup.

---

## Warmup Requirements by Archetype

### Workouts WITH Warmup

**Standard warmup structure:**
- 10min Z1-Z2 progression (50-65% FTP, RPE 3-4)
- 5min high cadence Z3 (85% FTP, 100+ rpm, RPE 5-6)

**Applies to:**
- All interval-based workouts (VO2, Threshold, SFR, Stomps, Microbursts)
- All tempo and sweet spot workouts
- All blended workouts
- All threshold workouts
- All climbing workouts
- Testing workouts (FTP tests)

**Rationale:** These workouts require priming the cardiovascular system and preparing for high-intensity efforts. The warmup ensures:
- Gradual heart rate increase
- Muscle temperature elevation
- Neuromuscular activation
- Mental preparation for hard efforts

---

### Workouts WITHOUT Warmup

**Endurance workouts start immediately at Z2:**

**Applies to:**
- `endurance` - Long Z2 rides with optional intervals
- `endurance_blocks` - Endurance with structured blocks
- `endurance_with_surges` - Ultra-long endurance with surges

**Rationale:** 
- Endurance workouts are already low-intensity (Z2)
- They naturally start easy and build
- No need to "prime" for Z2 work
- Starting immediately is more time-efficient for long rides
- The first 10-15 minutes naturally serve as a warmup

**Rest workouts:**
- `rest` - Minimal activity, no structured warmup needed

---

## Implementation

### Code Locations

1. **`generate_archetype_examples.py`**
   - `generate_workout_blocks()` function
   - Checks if archetype is in `endurance_archetypes` list
   - Skips warmup blocks for endurance workouts

2. **`workout_description_generator.py`**
   - `generate_description()` function
   - Skips WARM-UP section in description for endurance workouts

3. **`test_warmup_validation.py`**
   - `SPECIAL_WARMUP_ARCHETYPES` list includes endurance workouts
   - Validation tests skip endurance workouts

---

## Endurance Archetype List

```python
endurance_archetypes = [
    "endurance",
    "endurance_blocks", 
    "endurance_with_surges"
]
```

---

## Example: Endurance Workout Structure

**Before (incorrect):**
```xml
<Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
<SteadyState Duration="300" Power="0.85" Cadence="100"/>
<SteadyState Duration="3600" Power="0.70"/>
```

**After (correct):**
```xml
<SteadyState Duration="3600" Power="0.70"/>
```

The workout starts immediately at Z2. The first 10-15 minutes naturally serve as a warmup.

---

## Validation

The `test_warmup_validation.py` test suite:
- ✅ Validates warmup presence for non-endurance workouts
- ✅ Skips warmup validation for endurance workouts
- ✅ Ensures endurance workouts don't have warmup blocks

---

## Updated: 2026-01-12

