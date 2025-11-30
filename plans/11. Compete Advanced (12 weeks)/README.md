# COMPETE ADVANCED - PODIUM CONTENDER PLAN (12 weeks)

## Template Status

✅ **COMPLETE** - All 12 weeks with 168 workouts

## Plan Overview

**Training Philosophy:** Block Periodization  
**Target Athlete:** Advanced racer, competitive performance goal, sophisticated training capacity  
**Weekly Hours:** 15-18 hours  
**Goal:** Podium-level performance through sequential limiter-focused training blocks

## JSON Template

The `template.json` file contains:
- ✅ Plan metadata
- ✅ Week 1: Complete (7 workouts - assessment week)
- ✅ Weeks 2-5: Complete for all 4 blocks (112 workouts total - 4 blocks × 4 weeks × 7 workouts)
- ✅ Weeks 6-7: Recovery & Transmutation (14 workouts)
- ✅ Weeks 8-10: Block 2 Race Sharpening (21 workouts)
- ✅ Weeks 11-12: Taper & Race (14 workouts)

## Block Periodization Structure

### Week 1: Assessment
- Comprehensive power profiling
- Identifies primary limiter
- Determines which block to follow (VO2max, Threshold, Durability, or Neuromuscular)

### Weeks 2-5: Block 1 - Concentrated Loading
Four block options based on Week 1 assessment:

1. **VO2max Block:** If 5-min power <118% FTP, or you get dropped on steep climbs/surges
2. **Threshold Block:** If threshold endurance weak, or you fade in sustained race pace efforts
3. **Durability Block:** If power decays significantly in final hours of long rides
4. **Neuromuscular Block:** If 1-min power <145% FTP and races have punchy technical sections

Each block has 4 weeks of concentrated loading on the identified limiter.

### Weeks 6-7: Recovery & Transmutation
- Convert concentrated loading into performance gains
- Light quality touch to maintain fitness
- Recovery allows adaptation

### Weeks 8-10: Block 2 - Race Sharpening
- Mixed intensity work
- Race simulation
- Maintains Block 1 gains while sharpening all systems

### Weeks 11-12: Taper & Race
- Volume drops, intensity stays sharp
- Final freshness for race day

## Key Features

### Block Periodization Philosophy
- Concentrated loading on ONE system at a time
- Creates deeper adaptation sequentially
- Requires discipline—temporarily neglect some capacities to overload others
- Advanced athletes understand this trade-off delivers superior results

### Changing Pace Philosophy
- **Base Period (Weeks 2-5):**
  - High cadence work (100+ rpm seated) on intervals
  - Low cadence/torque work (40-60 rpm seated, big gear) on intervals
  - Alternates to teach power production in different ways

- **Block 2 (Weeks 8-10):**
  - **Rhythm Intervals:**
    - Pattern: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 4-6, continuous
    - Simulates race variability
  - **Loaded Intervals:**
    - Pattern: 1 min Z5/Z6 (high cadence, seated) → settle into 11-19 min Z3 (self-selected cadence)
    - Simulates race starts and surges
  - Mix of cadence work throughout

### G-Spot Terminology
- Replaces "Sweet Spot"
- Range: 87-92% FTP (1% lower than traditional Sweet Spot)
- Used in Durability Block

### Strength Training
- Removed from workout blocks
- Notes added suggesting athlete performs own strength program
- Suggested on lighter training days

### Monday Week Previews
- All Monday rest days include:
  - Week overview with block periodization reminders
  - Key workouts highlighted
  - Important reminders (zone discipline, fueling, recovery, etc.)
  - Countdown to race
  - Competitive performance guidance

### Rest Day Limits
- All rest days (Monday, Friday):
  - Fine to ride if desired
  - Max 1 hour
  - Max 30 TSS

## Template Statistics

- **Total weeks:** 12
- **Total workouts:** 168
  - Week 1: 7 workouts (assessment)
  - Weeks 2-5: 112 workouts (4 blocks × 4 weeks × 7 workouts)
  - Weeks 6-7: 14 workouts (recovery)
  - Weeks 8-10: 21 workouts (Block 2)
  - Weeks 11-12: 14 workouts (taper & race)
- **Status:** ✅ Complete and ready for race-specific generation

## Usage with Cursor AI

To generate a race-specific plan:

1. **Load template:**
   ```
   Load: current/plans/11. Compete Advanced (12 weeks)/template.json
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
   - ZWO files for selected block (or all blocks)
   - Modifications document

## Next Steps

The template is complete and ready for:
1. Loading into Cursor AI
2. Applying race-specific modifications
3. Generating race-specific plans
4. Creating ZWO files

**Next:** Provide race-specific considerations to generate race-specific version!

