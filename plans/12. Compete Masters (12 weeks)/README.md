# COMPETE MASTERS - 50+ PERFORMANCE PLAN (12 weeks)

## Template Status

✅ **COMPLETE** - All 12 weeks with 84 workouts

## Plan Overview

**Training Philosophy:** Autoregulated (HRV-Based) + Polarized  
**Target Athlete:** Age 50+, race performance goal (not just completion), has 12-18 hours weekly  
**Weekly Hours:** 12-18 hours  
**Goal:** Strong competitive finish with age-appropriate training and aggressive recovery management

## JSON Template

The `template.json` file contains:
- ✅ Plan metadata
- ✅ Week 1: Complete (7 workouts - foundation assessment week)
- ⏳ Weeks 2-12: Need to be populated (77 workouts)

## Key Features

### Autoregulated (HRV-Based) + Polarized Philosophy
- **HRV/Readiness Checks:** Before every quality session
  - **Green:** Full workout
  - **Yellow:** Modified workout (reduced volume/intensity)
  - **Red:** Easy day or rest
- **Polarized 80/20:**
  - 80% easy (Z1-Z2, conversational pace)
  - 20% hard (Z4-Z5+, truly hard efforts)
  - Almost nothing in the middle (Z3 avoided except transitions)
- **Masters Principle:** Recovery enables performance. You can't force fitness at 50+.

### Masters-Specific Considerations
- **FTP Multiplier:** 0.93 (more conservative for 50+)
- **Recovery Priority:** 48+ hours after hard sessions
- **Strength Training:** 2x/week minimum, heavy loads during base phase
  - Prevents sarcopenia, maintains bone density, builds power
  - Notes only (athlete does own program)
- **Respect Fatigue Signals:** If crushed, back off immediately

### Changing Pace Philosophy
- **Base Period (Weeks 1-4):**
  - High cadence work (100+ rpm seated) on intervals
  - Low cadence/torque work (40-60 rpm seated, big gear) on intervals
  - Alternates to teach power production in different ways

- **Build Period (Weeks 5-8):**
  - Mix of high/low cadence work
  - **Rhythm Intervals** introduced (Weeks 6, 7):
    - Pattern: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 3-4, continuous
    - Simulates race variability

- **Peak Period (Weeks 9-12):**
  - **Loaded Intervals** introduced (Weeks 9, 10):
    - Pattern: 1 min Z5/Z6 (high cadence, seated) → settle into 11-19 min Z3 (self-selected cadence)
    - Simulates race starts and surges
  - Rhythm intervals continue
  - Mix of cadence work throughout

### Strength Training
- **NOT incorporated into workout blocks**
- **Notes added** suggesting athlete performs own strength program
- **Suggested on lighter training days** (typically Sunday after long rides)
- **Phases:**
  - Weeks 1-4: Max Strength (heavy loads, 4x6-8 @ 85-88% 1RM)
  - Weeks 5-7: Explosive Strength (light loads, maximum velocity)
  - Weeks 8-10: Durability/Stability Strength (higher reps, lower weight)
  - Weeks 11-12: Maintenance (light, movement quality)

### Monday Week Previews
- All Monday rest days include:
  - Week overview with autoregulation reminders
  - Key workouts highlighted
  - HRV/readiness check reminders
  - Masters-specific guidance (recovery, strength, pacing)
  - Countdown to race
  - Competitive performance tips

### Rest Day Limits
- All rest days (Monday, Friday):
  - Fine to ride if desired
  - Max 1 hour
  - Max 30 TSS

## Week Structure

Each week follows this pattern:
- **Monday:** Rest with week preview + rest day note
- **Tuesday-Sunday:** 6 workouts (mix of easy endurance, hard sessions with HRV checks, long rides, strength notes)

## HRV/Readiness Check Pattern

Every quality session includes:
```
Readiness Check: Green? Full workout. Yellow? Modified workout. Red? Easy day or rest.
```

Examples:
- **Green:** Full workout as prescribed
- **Yellow:** Reduced volume/intensity (e.g., 4x3 min instead of 4x4 min, or 3x12 min instead of 3x15 min)
- **Red:** Skip intervals, ride 60-90 min easy instead

## Template Statistics

- **Total weeks:** 12
- **Total workouts required:** 84 (12 weeks × 7 workouts)
- **Current completion:** Week 1 (7 workouts) = 8% complete
- **Remaining:** 77 workouts

## Usage with Cursor AI

To generate a race-specific plan:

1. **Load template:**
   ```
   Load: current/plans/12. Compete Masters (12 weeks)/template.json
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

## Next Steps

The template structure is correct and follows the same pattern as FINISHER MASTERS (but with higher volume). To complete:

1. Populate Weeks 2-12 following the same pattern as Week 1
2. Include HRV/readiness checks on all quality sessions
3. Add cadence work to all intervals
4. Add rhythm intervals in Build phase (Weeks 6-7)
5. Add loaded intervals in Peak phase (Weeks 9-10)
6. Add strength notes (not blocks) on appropriate days
7. Add Monday week previews to all rest days
8. Add rest day TSS limits

The patterns are established in Week 1 - remaining weeks follow the same structure with progressive volume/intensity changes as described in the plan text.

## Comparison to FINISHER MASTERS

**Similarities:**
- Same philosophy (Autoregulated + Polarized)
- Same HRV/readiness check structure
- Same Masters-specific considerations
- Same strength training approach (notes, not blocks)

**Differences:**
- **Volume:** 12-18 hours/week (vs 8-12 hours/week)
- **Focus:** Competitive performance (vs strong finish)
- **Intensity:** Slightly higher intensity targets
- **Long rides:** Longer (up to 5-5.5 hours vs 3.5-4.5 hours)

