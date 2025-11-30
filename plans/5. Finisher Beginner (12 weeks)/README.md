# FINISHER BEGINNER - FIRST-TIMER PLAN (12 weeks)

## Template Status

✅ **COMPLETE** - All 12 weeks with 84 workouts

## Plan Overview

**Training Philosophy:** Traditional Pyramidal  
**Target Athlete:** First big gravel race, building systematic base for first time, has done some recreational riding  
**Weekly Hours:** 8-10 hours  
**Goal:** Finish confidently, learn proper training, build durable aerobic base

## JSON Template

The `template.json` file contains:
- ✅ Plan metadata
- ✅ All 12 weeks (84 workouts total)
- ✅ Default modifications (cadence work, rhythm/loaded intervals, G-Spot terminology)

## Key Features

- **G-Spot terminology** (87-92% FTP) replaces Sweet Spot
- **Cadence work** on all intervals (high/low variations)
- **Rhythm/Loaded intervals** in Build/Peak phases (Weeks 5-10)
- **Strength training** removed from workouts (athlete's own program with notes)
- **Monday previews** week ahead with key workout highlights
- **Rest day limits** (30 TSS max, 1 hour max if riding)

## Week Structure

Each week follows this pattern:
- **Monday:** Rest with week preview + rest day note
- **Tuesday-Sunday:** 6 workouts (mix of intervals, endurance, long rides, strength notes)

## Conversions Applied

1. ✅ Sweet Spot → G-Spot (all references)
2. ✅ 88-92% FTP → 87-92% FTP (G-Spot range)
3. ✅ Strength removed from blocks, notes added
4. ✅ Monday week previews added to all rest days
5. ✅ Rest day TSS limits added (30 TSS max, 1 hour max)

## Usage with Cursor AI

To generate a race-specific plan:

1. **Load template:**
   ```
   Load: current/plans/5. Finisher Beginner (12 weeks)/template.json
   Load: current/guidelines/nutrition_hydration_guidelines.json
   ```

2. **Provide race-specific considerations:**
   ```
   Race: [RACE NAME]
   - Heat training needed
   - Aggressive fueling: 60-90g carbs/hour
   - Dress rehearsal: [X]-hour ride Week [Y]
   - Robust taper: Week [Z]
   - Gravel Grit: Week [Z] race day
   ```

3. **Cursor will generate:**
   - Modified Python script
   - 84 ZWO files (or modified count based on race)
   - Modifications document

## Template Statistics

- **Total weeks:** 12
- **Total workouts:** 84 (12 weeks × 7 workouts)
- **File size:** ~150KB JSON
- **Structure:** Complete with all workout descriptions and ZWO blocks

## Next Steps

This template is ready to use for generating race-specific plans. Follow the same pattern as COMPETE SAVE MY RACE for creating race-specific versions.
