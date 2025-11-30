# FINISHER MASTERS - FAST AFTER 50 PERFORMANCE PLAN (12 weeks)

## Template Status

✅ **COMPLETE** - All 12 weeks with 84 workouts

## Plan Overview

**Training Philosophy:** Autoregulated (HRV-Based) + Polarized  
**Target Athlete:** Age 50+, performance-minded finisher, has 8-12 hours weekly  
**Weekly Hours:** 8-12 hours  
**Goal:** Strong competitive finish with age-appropriate training and smart recovery

## JSON Template

The `template.json` file contains:
- ✅ Plan metadata
- ✅ All 12 weeks (84 workouts total)
- ✅ Default modifications (autoregulation, polarized, cadence work, rhythm/loaded intervals, Masters-specific)

## Key Features

### Dual Philosophy: Autoregulation + Polarized

**Autoregulation (HRV-Based):**
- **Green (HRV high/normal):** Full workout
- **Yellow (HRV moderate):** Modified workout (reduced volume/intensity)
- **Red (HRV low):** Easy ride or rest
- **No HRV tracker?** Use perceived recovery: good sleep + fresh legs = go, poor sleep + heavy legs = back off

**Polarized 80/20:**
- **80% Easy:** Z1-Z2 (55-75% FTP) - conversational pace
- **20% Hard:** Z4-Z5+ (95%+ FTP) - truly hard efforts
- **Almost nothing in the middle** - this is the key to polarized training

### Masters-Specific Considerations

- **FTP Multiplier:** 0.93 (conservative for 50+)
- **Recovery Principle:** Recovery IS training at 50+
- **Strength Priority:** NON-NEGOTIABLE for 50+ athletes—prevents sarcopenia, maintains bone density
- **Extended Recovery:** Masters athletes often need 48+ hours recovery after maximal efforts
- **Readiness Checks:** Every workout includes readiness check (HRV or perceived recovery)

### Changing Pace Philosophy
- **Base Period (Weeks 1-4):**
  - High cadence work (100+ rpm seated) on intervals
  - Low cadence/torque work (40-60 rpm seated, big gear) on intervals
  - Alternates to teach power production in different ways

- **Build Period (Weeks 5-8):**
  - Mix of high/low cadence work
  - **Rhythm Intervals** introduced (Weeks 6, 7):
    - Pattern: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 3-8, continuous
    - Simulates race variability

- **Peak Period (Weeks 9-12):**
  - **Loaded Intervals** introduced (Weeks 7, 10):
    - Pattern: 1 min Z5/Z6 (high cadence, seated) → settle into 11-19 min Z3 (self-selected cadence)
    - Simulates race starts and surges
  - Rhythm intervals continue
  - Mix of cadence work throughout

### Strength Training Phases
- **Base (Weeks 1-3):** Max strength (4x6-8 heavy @ 85-88% 1RM, rest 3-4 min)
- **Explosive (Week 4):** Explosive power (3x6-8, light loads, maximum velocity)
- **Stability (Weeks 7-8):** Stability/injury prevention (3x12-15)
- **Durability (Weeks 9-10):** Muscular endurance (3x15-20, higher reps, lower weight)
- **Maintenance (Weeks 11-12):** Light maintenance (2x8-10)

Strength is removed from workout blocks, notes added suggesting athlete performs own program. **NON-NEGOTIABLE for 50+ athletes.**

### Monday Week Previews
- All Monday rest days include:
  - Week overview with autoregulation reminders
  - Key workouts highlighted with HRV/readiness checks
  - Important reminders (sleep, nutrition, stress management)
  - Countdown to race
  - Masters-specific guidance

### Rest Day Limits
- All rest days (Monday, Friday):
  - Fine to ride if desired
  - Max 1 hour
  - Max 30 TSS

## Week Structure

Each week follows this pattern:
- **Monday:** Rest with week preview + rest day note
- **Tuesday-Sunday:** 6 workouts (mix of easy endurance, hard sessions with readiness checks, long rides, strength notes)

## Conversions Applied

1. ✅ Strength removed from blocks, phase-specific notes added
2. ✅ Monday week previews added to all rest days
3. ✅ Rest day TSS limits added (30 TSS max, 1 hour max)
4. ✅ Cadence work integrated into all hard sessions
5. ✅ Rhythm intervals added in Build/Peak phases
6. ✅ Loaded intervals added in Peak phase
7. ✅ HRV/readiness checks added to all hard sessions
8. ✅ Masters-specific considerations throughout

## Usage with Cursor AI

To generate a race-specific plan:

1. **Load template:**
   ```
   Load: current/plans/8. Finisher Masters (12 weeks)/template.json
   Load: current/guidelines/nutrition_hydration_guidelines.json
   ```

2. **Provide race-specific considerations:**
   ```
   Race: [RACE NAME]
   - Heat training needed
   - Aggressive fueling: 50-60g carbs/hour minimum
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

## Autoregulation System

### HRV-Based (if tracking)
- **Green (High/Normal):** Full workout as prescribed
- **Yellow (Moderate):** Modified workout (reduced volume/intensity)
- **Red (Low):** Easy ride or rest day

### Perceived Recovery (if no HRV tracker)
- **Go:** Good sleep + fresh legs
- **Back Off:** Poor sleep + heavy legs

### Readiness Checks
Every hard session includes readiness check:
- Green: Full workout
- Yellow: Modified workout
- Red: Easy ride or rest

## Changing Pace Philosophy Details

### Base Period Cadence Work
- All intervals alternate between:
  - **High cadence (100+ rpm):** Seated, fast leg speed
  - **Low cadence (40-60 rpm):** Seated, big gear, torque work
- Teaches neuromuscular skill to produce power in different ways
- Foundation for changing pace later

### Rhythm Intervals (Build/Peak)
- **Pattern:** 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 3-8, continuous
- **Weeks:** 6, 7, 9, 10
- Simulates race variability (surges, climbs, wind)
- All continuous, no recovery between pattern repeats

### Loaded Intervals (Peak)
- **Pattern:** 1 min Z5/Z6 (high cadence, seated) → settle into 11-19 min Z3 (self-selected cadence)
- **Weeks:** 7, 10
- Simulates race starts and surges
- Teaches ability to settle into sustainable pace after hard start

## Next Steps

Once complete (all 12 weeks), this template can be used like other Finisher plans:
- Load template.json
- Load nutrition_hydration_guidelines.json
- Apply race-specific modifications
- Generate race-specific plan

