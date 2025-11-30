# COMPETE SAVE MY RACE - 6 WEEK EMERGENCY PLAN

## Template Files

This folder contains the **generalized template** for the COMPETE SAVE MY RACE plan:

- **`GENERATE_COMPETE_SAVEMYRACE.py`** - Base generation script (creates ZWO files from workout data)
- **`ALL_WORKOUTS_DATA_SAVEMYRACE.py`** - All workout definitions (42 base workouts + 3 block options for Weeks 2-3)

## Plan Overview

**Training Philosophy:** Block Periodization (Compressed)  
**Target Athlete:** Emergency situation, already race-fit, needs final sharpening for competitive performance  
**Weekly Hours:** 15-18 hours  
**Duration:** 6 weeks  
**Goal:** Convert existing race fitness into peak competitive performance in compressed timeframe

## Plan Structure

- **Week 1:** Rapid Assessment & Block Planning (7 workouts)
- **Weeks 2-3:** Concentrated Loading Block - Choose ONE:
  - Option A: VO2max Block (7 workouts each week)
  - Option B: Threshold Block (7 workouts each week)
  - Option C: Durability Block (7 workouts each week)
- **Week 4:** Recovery & Transmutation (7 workouts)
- **Week 5:** Race Sharpening - Mixed Intensity (7 workouts)
- **Week 6:** Race Week - Taper & Compete (7 workouts)

**Total:** 42 base workouts + 3 block path options for Weeks 2-3

## Key Features

- **Block Periodization:** Concentrated loading on single limiter (VO2max, Threshold, or Durability)
- **Autoregulation:** Athlete chooses block path based on Week 1 assessment
- **Compressed Format:** 6 weeks for race-fit athletes needing final sharpening
- **High Volume:** 15-18 hours/week

## How to Generate Race-Specific Plans

### For Cursor AI:

1. **Provide the template plan** (this folder's contents)
2. **Provide race-specific considerations** (heat, fueling, dress rehearsal, taper, etc.)
3. **Request modifications:**
   - Cadence work (high/low cadence variations)
   - Rhythm/Loaded intervals (Week 5)
   - Race-specific modifications (heat training, aggressive fueling, dress rehearsal, robust taper, Gravel Grit)
   - G-Spot terminology (87-92% FTP) replaces Sweet Spot (88-93% FTP)

### Example Prompt for Cursor:

```
I need to generate a race-specific version of the COMPETE SAVE MY RACE plan for [RACE NAME].

Race-Specific Considerations:
1. Heat training needed
2. Aggressive carbohydrate fueling (60-90g carbs/hour)
3. Dress rehearsal: [X]-hour ride in Week 3 Saturday (~3 weeks before race)
4. Robust taper in Week 6
5. Gravel Grit integration

Also apply:
- Cadence work (high 100+ rpm, low 40-60 rpm) on all intervals
- Rhythm/Loaded intervals in Week 5
- Replace Sweet Spot with G-Spot (87-92% FTP)

Generate the modified script and create a modifications document.
```

## Race-Specific Folders

Each race-specific version should be in its own folder:
- `13. [RACE NAME] - Compete Save My Race (6 weeks)/`
  - Modified generation script
  - Generated ZWO files
  - Modifications document (explaining what changed and why)

## Files Required for Generation

1. **Template ZWO file:** `W01_Tue_-_FTP_Test.zwo` (must be in same directory as script)
2. **Workout data:** `ALL_WORKOUTS_DATA_SAVEMYRACE.py`
3. **Generation script:** `GENERATE_COMPETE_SAVEMYRACE.py` (base) or modified version

## Notes

- The base script generates all three block options for Weeks 2-3
- Athletes choose ONE block path based on Week 1 assessment
- Race-specific scripts should maintain this structure but add race-specific modifications

