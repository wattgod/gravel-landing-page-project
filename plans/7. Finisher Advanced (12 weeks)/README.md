# FINISHER ADVANCED - STRONG FINISH PLAN (12 weeks)

## Template Status

✅ **COMPLETE** - All 12 weeks with 84 workouts

## Plan Overview

**Training Philosophy:** GOAT Method (Gravel Optimized Adaptive Training)  
**Target Athlete:** Strong cyclist, wants top-third finish, can monitor/adjust training  
**Weekly Hours:** 10-12 hours  
**Goal:** Strong finish in top third of field, adaptive multi-method approach

## JSON Template

The `template.json` file contains:
- ✅ Plan metadata
- ✅ All 12 weeks (84 workouts total)
- ✅ Default modifications (GOAT Method, cadence work, rhythm/loaded intervals)

## Key Features

### GOAT Method Philosophy
The GOAT Method adapts to the athlete's limiters by combining:
- **Pyramidal base weeks** (Weeks 1-3): Traditional base building
- **Limiter-focused blocks** (Weeks 5-7): Concentrated loading on biggest weakness
- **Polarized transmutation** (Weeks 9-10): Convert threshold gains to race performance
- **G-Spot when time-crunched**: Efficient training for busy weeks
- **All guided by athlete signals**: HRV, HR drift, performance markers

### Training Phases

1. **Weeks 1-3: Pyramidal Base Building**
   - Build aerobic foundation
   - Identify limiters through testing
   - Max strength work

2. **Week 4: Recovery + Limiter Assessment**
   - Recover from base phase
   - Plan limiter block based on testing
   - Explosive strength prep

3. **Weeks 5-7: Limiter Block (Threshold Endurance Focus)**
   - Concentrated threshold work
   - Block periodization principles
   - Peak threshold volume

4. **Week 8: Recovery + Transmutation Planning**
   - Absorb threshold block
   - Prepare for polarized conversion
   - Stability strength

5. **Weeks 9-10: Transmutation & Realization**
   - Polarized training (80/20)
   - Convert threshold to race performance
   - Race-specific work
   - Durability strength

6. **Weeks 11-12: Taper & Race Week**
   - Maintain sharpness, gain freshness
   - Final race prep
   - Light maintenance strength

### Changing Pace Philosophy
- **Base Period (Weeks 1-4):**
  - High cadence work (100+ rpm seated) on intervals
  - Low cadence/torque work (40-60 rpm seated, big gear) on intervals
  - Alternates to teach power production in different ways

- **Build Period (Weeks 5-8):**
  - Mix of high/low cadence work
  - **Rhythm Intervals** introduced (Weeks 6, 7):
    - Pattern: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 4-8, continuous
    - Simulates race variability

- **Peak Period (Weeks 9-12):**
  - **Loaded Intervals** introduced (Weeks 7, 10):
    - Pattern: 1 min Z5/Z6 (high cadence, seated) → settle into 11-29 min Z3 (self-selected cadence)
    - Simulates race starts and surges
  - Rhythm intervals continue
  - Mix of cadence work throughout

### Strength Training Phases
- **Base (Weeks 1-3):** Max strength (4x5-6 heavy)
- **Explosive (Week 4):** Explosive power (3x6-8, light loads)
- **Stability (Weeks 7-8):** Stability/injury prevention (3x10-12)
- **Durability (Weeks 9-10):** Muscular endurance (3x15-20, higher reps)
- **Maintenance (Weeks 11-12):** Light maintenance (2x8-10)

Strength is removed from workout blocks, notes added suggesting athlete performs own program.

### Monday Week Previews
- All Monday rest days include:
  - Week overview with GOAT Method principles
  - Key workouts highlighted
  - Important reminders (HRV monitoring, fueling, recovery, etc.)
  - Countdown to race

### Rest Day Limits
- All rest days (Monday, Friday):
  - Fine to ride if desired
  - Max 1 hour
  - Max 30 TSS

## Week Structure

Each week follows this pattern:
- **Monday:** Rest with week preview + rest day note
- **Tuesday-Sunday:** 6 workouts (mix of easy endurance, hard sessions, long rides, strength notes)

## Conversions Applied

1. ✅ Sweet Spot → G-Spot (all references)
2. ✅ 88-92% FTP → 87-92% FTP (G-Spot range)
3. ✅ Strength removed from blocks, notes added with phase-specific guidance
4. ✅ Monday week previews added to all rest days
5. ✅ Rest day TSS limits added (30 TSS max, 1 hour max)
6. ✅ Cadence work integrated into all hard sessions
7. ✅ Rhythm intervals added in Build/Peak phases
8. ✅ Loaded intervals added in Peak phase

## Usage with Cursor AI

To generate a race-specific plan:

1. **Load template:**
   ```
   Load: current/plans/7. Finisher Advanced (12 weeks)/template.json
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
- **File size:** ~60KB JSON
- **Structure:** Complete with all workout descriptions and ZWO blocks

## GOAT Method Principles

1. **Adaptive:** Training adapts to athlete's limiters (threshold, VO2max, durability)
2. **Multi-Method:** Combines best of pyramidal, polarized, block periodization
3. **Signal-Guided:** Uses HRV, HR drift, performance markers to adjust
4. **Limiter-Focused:** Concentrated blocks target biggest weakness
5. **Transmutation:** Converts raw fitness to race performance via polarized work

## Changing Pace Philosophy Details

### Base Period Cadence Work
- All intervals alternate between:
  - **High cadence (100+ rpm):** Seated, fast leg speed
  - **Low cadence (40-60 rpm):** Seated, big gear, torque work
- Teaches neuromuscular skill to produce power in different ways
- Foundation for changing pace later

### Rhythm Intervals (Build/Peak)
- **Pattern:** 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 4-8, continuous
- **Weeks:** 6, 7, 9, 10
- Simulates race variability (surges, climbs, wind)
- All continuous, no recovery between pattern repeats

### Loaded Intervals (Peak)
- **Pattern:** 1 min Z5/Z6 (high cadence, seated) → settle into 11-29 min Z3 (self-selected cadence)
- **Weeks:** 7, 10
- Simulates race starts and surges
- Teaches ability to settle into sustainable pace after hard start

## Next Steps

Once complete (all 12 weeks), this template can be used like FINISHER BEGINNER and FINISHER INTERMEDIATE:
- Load template.json
- Load nutrition_hydration_guidelines.json
- Apply race-specific modifications
- Generate race-specific plan

