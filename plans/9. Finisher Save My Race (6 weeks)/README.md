# FINISHER SAVE MY RACE - 6 WEEK EMERGENCY PLAN

## Template Status

✅ **COMPLETE** - All 6 weeks with 3 assessment-based tracks

## Plan Overview

**Training Philosophy:** G-Spot/Threshold (Emergency Sharpening)  
**Target Athlete:** Emergency situation, already has base fitness, needs final sharpening  
**Weekly Hours:** 10-12 hours  
**Goal:** Convert existing base into race-ready fitness in compressed timeframe

## JSON Template

The `template.json` file contains:
- ✅ Plan metadata
- ✅ Week 1: Assessment week (7 workouts)
- ✅ Weeks 2-4: Three tracks (Aggressive, Balanced, Foundation) - 21 workouts each
- ✅ Week 5: Recovery & Final Sharpening (7 workouts)
- ✅ Week 6: Race Week (7 workouts)
- ✅ Default modifications (G-Spot/Threshold, cadence work, rhythm/loaded intervals)

## Key Features

### Emergency Plan Structure
- **Week 1:** Rapid assessment & threshold baseline
- **Weeks 2-4:** Concentrated sharpening block (choose track based on Week 1 assessment)
- **Week 5:** Recovery & final sharpening
- **Week 6:** Race week

### Three Assessment-Based Tracks

**Track Selection Based on Week 1 Performance:**

1. **Aggressive Track** (Strong Week 1 Performance)
   - FTP test good, G-Spot sustainable, Threshold intervals completed strong
   - Ready for aggressive sharpening
   - Higher volume/intensity in Weeks 2-4

2. **Balanced Track** (Moderate Week 1 Performance)
   - FTP test okay, G-Spot hard but manageable, Threshold intervals challenging
   - Balanced approach
   - Moderate volume/intensity in Weeks 2-4

3. **Foundation Track** (Weak Week 1 Performance)
   - FTP test disappointing, G-Spot very hard, Threshold intervals falling apart
   - Focus on foundation building
   - Lower volume/intensity, more G-Spot, less threshold in Weeks 2-4

### G-Spot/Threshold Philosophy
- **G-Spot (87-92% FTP):** "Uncomfortably sustainable" - time-efficient race preparation
- **Threshold (95-105% FTP):** Race pace - sustained near-max effort
- **Emergency Mode:** Not about building base (takes months), about sharpening what you have

### Changing Pace Philosophy
- **Base Period (Week 1):**
  - High cadence work (100+ rpm seated) on intervals
  - Low cadence/torque work (40-60 rpm seated, big gear) on intervals
  - Alternates to teach power production in different ways

- **Build Period (Weeks 2-4):**
  - Mix of high/low cadence work
  - **Rhythm Intervals** introduced (Weeks 3, 4):
    - Pattern: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 3-4, continuous
    - Simulates race variability

- **Peak Period (Week 4):**
  - **Loaded Intervals** introduced:
    - Pattern: 1 min Z5/Z6 (high cadence, seated) → settle into 11-19 min Z3 (self-selected cadence)
    - Simulates race starts and surges

### Strength Training
- Removed from workout blocks
- Notes added suggesting athlete performs own strength program
- Suggested on lighter training days

### Monday Week Previews
- All Monday rest days include:
  - Week overview with assessment reminders
  - Key workouts highlighted
  - Track-specific guidance (Weeks 2-4)
  - Important reminders (fueling, recovery, etc.)
  - Countdown to race

### Rest Day Limits
- All rest days (Monday, Friday):
  - Fine to ride if desired
  - Max 1 hour
  - Max 30 TSS

## Week Structure

**Week 1:** Assessment week (7 workouts)
- Tuesday: FTP test + G-Spot assessment
- Thursday: Threshold assessment
- Saturday: Moderate endurance with tempo

**Weeks 2-4:** Choose track based on Week 1 assessment
- Each track has 3 weeks of workouts (21 workouts total per track)
- Structure varies by track (Aggressive/Balanced/Foundation)

**Week 5:** Recovery & Final Sharpening (7 workouts)
- Reduced volume
- Race openers
- Final preparation

**Week 6:** Race Week (7 workouts)
- Final openers
- Pre-race shake-out
- Race day

## Conversions Applied

1. ✅ Sweet Spot → G-Spot (all references)
2. ✅ 88-93% FTP → 87-92% FTP (G-Spot range)
3. ✅ Strength removed from blocks, notes added
4. ✅ Monday week previews added to all rest days
5. ✅ Rest day TSS limits added (30 TSS max, 1 hour max)
6. ✅ Cadence work integrated into all hard sessions
7. ✅ Rhythm intervals added in Weeks 3-4
8. ✅ Loaded intervals added in Week 4

## Usage with Cursor AI

To generate a race-specific plan:

1. **Load template:**
   ```
   Load: current/plans/9. Finisher Save My Race (6 weeks)/template.json
   Load: current/guidelines/nutrition_hydration_guidelines.json
   ```

2. **Provide race-specific considerations:**
   ```
   Race: [RACE NAME]
   - Heat training needed
   - Aggressive fueling: 50-60g carbs/hour minimum
   - Dress rehearsal: [X]-hour ride Week [Y]
   - Robust taper: Week 6
   - Gravel Grit: Week 6 race day
   ```

3. **Cursor will generate:**
   - Modified Python script
   - ZWO files for selected track (or all tracks)
   - Modifications document

## Template Statistics

- **Total weeks:** 6
- **Base workouts:** 21 (Week 1: 7, Week 5: 7, Week 6: 7)
- **Track workouts:** 21 per track (Weeks 2-4: 7 workouts × 3 weeks)
- **Total possible workouts:** 84 (21 base + 21 × 3 tracks)
- **File size:** ~80KB JSON
- **Structure:** Complete with all workout descriptions and ZWO blocks

## Assessment-Based Training

### Week 1 Assessment
- **FTP Test:** Sets training zones (20-min avg × 0.95 = FTP)
- **G-Spot Sustainability Check:** 20 min @ 87-90% FTP
- **Threshold Assessment:** 2x15 min @ 100-105% FTP

### Track Selection Criteria
- **Aggressive:** All assessments strong → aggressive sharpening
- **Balanced:** Assessments moderate → balanced approach
- **Foundation:** Assessments weak → foundation building

### Critical Decision Point
After Week 1, athlete must honestly assess performance and choose appropriate track. This determines Weeks 2-4 training load.

## Changing Pace Philosophy Details

### Base Period Cadence Work
- All intervals alternate between:
  - **High cadence (100+ rpm):** Seated, fast leg speed
  - **Low cadence (40-60 rpm):** Seated, big gear, torque work
- Teaches neuromuscular skill to produce power in different ways
- Foundation for changing pace later

### Rhythm Intervals (Weeks 3-4)
- **Pattern:** 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 3-4, continuous
- Simulates race variability (surges, climbs, wind)
- All continuous, no recovery between pattern repeats

### Loaded Intervals (Week 4)
- **Pattern:** 1 min Z5/Z6 (high cadence, seated) → settle into 11-19 min Z3 (self-selected cadence)
- Simulates race starts and surges
- Teaches ability to settle into sustainable pace after hard start

## Emergency Plan Truths

### What This Plan Does
- ✅ Sharpens existing base fitness into race readiness
- ✅ Delivers maximum race readiness in minimum time
- ✅ Uses G-Spot/Threshold for time-efficient training
- ✅ Provides assessment-based tracks for individual needs

### What This Plan Doesn't Do
- ❌ Build base fitness (takes 8-12+ weeks minimum)
- ❌ Replace proper preparation
- ❌ Guarantee optimal performance

### Key Lessons
- 6 weeks works for SHARPENING existing fitness, not BUILDING fitness
- G-Spot + Threshold = maximum ROI for limited time
- Emergency prep requires honest self-assessment (Week 1 testing critical)
- Conservative race execution essential with compressed timeline
- Better option: don't emergency prep. Build fitness year-round.

## Next Steps

Once complete, this template can be used like other Finisher plans:
- Load template.json
- Load nutrition_hydration_guidelines.json
- Apply race-specific modifications
- Generate race-specific plan for selected track (or all tracks)

