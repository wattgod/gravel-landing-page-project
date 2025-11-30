# AYAHUASCA MASTERS - FAST AFTER 50 PLAN (12 weeks)

## Template Status

✅ **COMPLETE** - All 12 weeks with 84 workouts

## Plan Overview

**Training Philosophy:** Autoregulated (HRV-Based)  
**Target Athlete:** Age 50+, minimal time available, recovery-focused, just finish goal  
**Weekly Hours:** 3-5 hours  
**Goal:** Finish confidently with age-appropriate training and recovery emphasis

## JSON Template

The `template.json` file contains:
- ✅ Plan metadata
- ✅ All 12 weeks (84 workouts total)
- ✅ Default modifications (autoregulation, cadence work, rhythm/loaded intervals, Masters-specific considerations)

## Key Features

### Autoregulated (HRV-Based) Philosophy
- **HRV/Readiness Checks:** Before every quality session
  - **Green (normal/high HRV):** Full workout
  - **Yellow (moderate readiness):** Modified workout (reduced volume/intensity)
  - **Red (low HRV/tired):** Easy day or rest
- **Perceived Recovery:** If no HRV tracker, use:
  - Good sleep + feeling fresh = quality okay
  - Poor sleep + heavy legs = back off
- **Your Body is the Best Coach:** Listen to it

### Masters-Specific Considerations
- **FTP Multiplier:** 0.93 (more conservative for Masters)
- **Recovery Priority:** 48+ hours after hard sessions
- **Strength Priority:** 2x/week minimum, focus on form over weight
- **Reality Check:** Better to undertrain slightly than overtrain significantly at 50+
- **Overtraining Risk:** Can sideline you for weeks at 50+
- **Undertraining:** You miss one good workout (acceptable risk)

### Volume Structure
- **Week 1:** Foundation & HRV Baseline (2-3.5 hours)
- **Week 2:** Building Routine (2.5-4 hours)
- **Week 3:** Progressive Loading (2.75-4.5 hours)
- **Week 4:** Recovery & Adaptation (1.75-3 hours)
- **Weeks 5-7:** Build Phase (2.5-5 hours)
- **Week 8:** Recovery & Absorption (1.75-3 hours)
- **Weeks 9-10:** Race Prep (2.75-4.75 hours)
- **Week 11:** Taper (2-3.5 hours)
- **Week 12:** Race Week (1.25-2.5 hours)

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
    - Pattern: 1 min Z5/Z6 (high cadence, seated) → settle into 9-14 min Z3 (self-selected cadence)
    - Simulates race starts and surges
  - Rhythm intervals continue
  - Mix of cadence work throughout

### G-Spot Terminology
- Replaces "Sweet Spot"
- Range: 87-92% FTP (1% lower than traditional Sweet Spot)
- Used throughout plan as primary intensity

### Strength Training
- **NOT incorporated into workout blocks**
- **Notes added** suggesting athlete performs own strength program
- **Suggested on lighter training days** (typically Sunday)
- **2x/week NON-NEGOTIABLE for 50+ athletes:**
  - Prevents sarcopenia (muscle loss)
  - Maintains bone density
  - Improves power-to-weight
  - Focus on FORM, not weight
- **Phases:**
  - Weeks 1-3: Progressive Strength (3x8-10, moderate weight)
  - Week 4: Light Strength Maintenance (2x10-12, bodyweight focus)
  - Weeks 5-7: Peak Strength (3x6-8 heavier, then 1x10-12 lighter)
  - Week 8: Light Strength Maintenance
  - Weeks 9-10: Strength Maintenance (2x8-10, moderate loads)
  - Weeks 11-12: Optional (light mobility work)

### Monday Week Previews
- All Monday rest days include:
  - Week overview with autoregulation reminders
  - Key workouts highlighted (especially long rides and quality sessions)
  - HRV/readiness check guidance
  - Masters-specific recovery reminders
  - Countdown to race
  - Race execution guidance

### Rest Day Limits
- All rest days (Monday, Wednesday, Friday, Sunday):
  - Fine to ride if desired
  - Max 1 hour
  - Max 30 TSS

## Week Structure

Each week follows this pattern:
- **Monday:** Rest with week preview + autoregulation reminders + rest day note
- **Tuesday:** Quality session (if HRV/readiness green) - G-Spot or Threshold
- **Wednesday:** Rest or very easy spin
- **Thursday:** Easy endurance (if recovered)
- **Friday:** Rest
- **Saturday:** Key session (longest ride of week, mixed intensity) - if feeling strong
- **Sunday:** Strength training (priority for Masters) or rest

## Autoregulation Decision Points

### Daily Checks:
- **Morning HRV:** Upon waking, still in bed, 5-min reading
- **Subjective Readiness:** Good sleep + fresh legs = go; Poor sleep + heavy legs = back off
- **Perceived Recovery:** 1-10 scale

### Workout Adjustments:
- **Green Light:** Full workout as prescribed
- **Yellow Light:** Modified workout (reduced volume/intensity)
- **Red Light:** Easy day or rest

### Masters-Specific Rules:
- **48+ hours after hard sessions:** Often need 48+ hours recovery
- **When in doubt, rest:** Better to miss one workout than overtrain
- **No shame in back-to-back rest days:** At 50+, this is strategic
- **If crushed by Wednesday:** Stop and take extra rest immediately

## Template Statistics

- **Total weeks:** 12
- **Total workouts:** 84 (12 weeks × 7 workouts)
- **File size:** ~50KB JSON
- **Structure:** Complete with all workout descriptions and ZWO blocks

## Usage with Cursor AI

To generate a race-specific plan:

1. **Load template:**
   ```
   Load: current/plans/3. Ayahuasca Masters (12 weeks)/template.json
   Load: current/guidelines/nutrition_hydration_guidelines.json
   ```

2. **Provide race-specific considerations:**
   ```
   Race: [RACE NAME]
   - Heat training needed (if applicable)
   - Aggressive fueling: 40-50g carbs/hour
   - Conservative pacing reminders
   - Mental toughness guidance
   ```

3. **Cursor will generate:**
   - Modified Python script
   - 84 ZWO files
   - Modifications document

## Autoregulation Principles

### Why Autoregulation Works for Masters:
- **Recovery Capacity:** Varies day-to-day at 50+
- **Life Stress:** Work, family, sleep quality all affect readiness
- **Injury Prevention:** Backing off when tired prevents overuse injuries
- **Quality Over Quantity:** One great workout beats three mediocre ones

### Key Principles:
- **Your body is the best coach:** Listen to it
- **Better to undertrain slightly than overtrain significantly:** At 50+, overtraining can sideline you for weeks
- **No medal for "toughest Masters athlete in training":** Be conservative
- **When in doubt, rest:** Masters rule

## Next Steps

Once complete (all 12 weeks), this template can be used like other Masters plans:
- Load template.json
- Load nutrition_hydration_guidelines.json
- Apply race-specific modifications
- Generate race-specific plan

**Remember:** Autoregulation respected your body. Smart training = successful finish. Celebrate your achievement.

