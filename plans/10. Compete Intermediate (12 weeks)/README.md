# COMPETE INTERMEDIATE - COMPETITIVE PLAN (12 weeks)

## Template Status

✅ **COMPLETE** - All 12 weeks with 84 workouts

## Plan Overview

**Training Philosophy:** Polarized (80/20)  
**Target Athlete:** Intermediate competitive racer, solid cycling background, top-third finish goal  
**Weekly Hours:** 12-15 hours  
**Goal:** Competitive performance through proven polarized distribution

## JSON Template

The `template.json` file contains:
- ✅ Plan metadata
- ✅ All 12 weeks (84 workouts total)
- ✅ Default modifications (polarized philosophy, cadence work, rhythm/loaded intervals)

## Key Features

### Polarized 80/20 Philosophy
- **80% Easy:** Z1-Z2 (55-75% FTP) - conversational pace
- **20% Hard:** Z4-Z5+ (95%+ FTP) - truly hard efforts
- **Almost nothing in the middle (Z3)** - this is the key to polarized training
- **Discipline:** Easy days stay TRULY easy for recovery, hard days can be TRULY hard because you're recovered

### Changing Pace Philosophy
- **Base Period (Weeks 1-4):**
  - High cadence work (100+ rpm seated) on intervals
  - Low cadence/torque work (40-60 rpm seated, big gear) on intervals
  - Alternates to teach power production in different ways

- **Build Period (Weeks 5-8):**
  - Mix of high/low cadence work
  - **Rhythm Intervals** introduced (Weeks 6, 7):
    - Pattern: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 4-6, continuous
    - Simulates race variability

- **Peak Period (Weeks 9-12):**
  - **Loaded Intervals** introduced (Weeks 7, 10):
    - Pattern: 1 min Z5/Z6 (high cadence, seated) → settle into 11-19 min Z3 (self-selected cadence)
    - Simulates race starts and surges
  - Rhythm intervals continue
  - Mix of cadence work throughout

### Strength Training
- Removed from workout blocks
- Notes added suggesting athlete performs own strength program
- Suggested on lighter training days

### Monday Week Previews
- All Monday rest days include:
  - Week overview with polarization reminders
  - Key workouts highlighted
  - Important reminders (zone discipline, fueling, recovery, etc.)
  - Countdown to race
  - Competitive performance guidance

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

1. ✅ Strength removed from blocks, notes added
2. ✅ Monday week previews added to all rest days
3. ✅ Rest day TSS limits added (30 TSS max, 1 hour max)
4. ✅ Cadence work integrated into all hard sessions
5. ✅ Rhythm intervals added in Build/Peak phases
6. ✅ Loaded intervals added in Peak phase

## Usage with Cursor AI

To generate a race-specific plan:

1. **Load template:**
   ```
   Load: current/plans/10. Compete Intermediate (12 weeks)/template.json
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

## Polarized Training Principles

### Zone Distribution
- **Z1-Z2 (55-75% FTP):** Easy days - conversational pace
- **Z3 (76-94% FTP):** Avoided except in short transitions
- **Z4-Z5+ (95%+ FTP):** Hard days - truly hard efforts

### Discipline Requirements
- Easy days stay TRULY easy (feels painfully slow - that's correct)
- Hard days can be TRULY hard (because you're recovered)
- No "no man's land" (Z3) - this violates polarization
- Calculate weekly distribution: ~80% Z1-Z2, ~20% Z4-Z5+

### Recovery Principle
- Easy days enable hard days
- Polarized training makes recovery weeks especially effective
- Fatigue is more specific and easier to recover from

## Changing Pace Philosophy Details

### Base Period Cadence Work
- All intervals alternate between:
  - **High cadence (100+ rpm):** Seated, fast leg speed
  - **Low cadence (40-60 rpm):** Seated, big gear, torque work
- Teaches neuromuscular skill to produce power in different ways
- Foundation for changing pace later

### Rhythm Intervals (Build/Peak)
- **Pattern:** 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 4-6, continuous
- **Weeks:** 6, 7, 9, 10
- Simulates race variability (surges, climbs, wind)
- All continuous, no recovery between pattern repeats

### Loaded Intervals (Peak)
- **Pattern:** 1 min Z5/Z6 (high cadence, seated) → settle into 11-19 min Z3 (self-selected cadence)
- **Weeks:** 7, 10
- Simulates race starts and surges
- Teaches ability to settle into sustainable pace after hard start

## Next Steps

Once complete (all 12 weeks), this template can be used like other Compete plans:
- Load template.json
- Load nutrition_hydration_guidelines.json
- Apply race-specific modifications
- Generate race-specific plan

