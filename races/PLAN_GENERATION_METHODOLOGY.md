# Plan Generation Methodology

## Structure: 5 Tiers × 3 Durations = 15 Plans

### Tiers
1. **Time Crunched** (0-5 hrs/week) - HIIT-Focused
2. **Finisher** (5-8 hrs/week) - Traditional Pyramidal
3. **Compete** (8-12 hrs/week) - Polarized Training
4. **Compete Masters** (8-12 hrs/week) - Masters-optimized Polarized
5. **Podium** (12+ hrs/week) - High-volume, race-specific

### Durations
- **12 weeks**: Standard progression
- **16 weeks**: Extended build phase
- **20 weeks**: Maximum preparation with FTP tests

---

## Generation Process

### Step 1: Load Base Template
- Each tier has a 12-week base template from `plans/` directory
- Templates contain workout structure, progression, and periodization

### Step 2: Extend to Target Duration
**For 16-week plans:**
- Take last 4 weeks of 12-week plan as pattern
- Add 4 weeks using pattern (weeks 13-16)
- Weeks 13-14: Extended build (+5% volume)
- Weeks 15-16: Peak build (maintain volume)

**For 20-week plans:**
- Take last 4 weeks of 12-week plan as pattern
- Add 8 weeks using pattern (weeks 13-20)
- Weeks 13-16: Extended build phase
- Weeks 17-18: Peak build phase
- Weeks 19-20: Final build/taper prep

### Step 3: Insert Testing
**FTP Tests:**
- Week 1: Initial FTP test (all plans)
- Week 7: Mid-plan recalibration (all plans)
- Week 13: Late-plan recalibration (16 & 20-week only)
- Week 19: Final test (20-week only)

**Durability Tests:**
- Week 7: 2hr @ 0.8 FTP (all tiers)
- Week 13: 
  - 3hr @ 0.8 FTP (Time Crunched, Finisher)
  - 4hr @ 0.8 FTP (Compete, Compete Masters, Podium)
- Week 19: 4hr @ 0.8 FTP (20-week only, all tiers)

### Step 4: Generate Workouts
- Each workout goes through `workout_description_generator.py`
- Applies Nate's dimensions (cadence, position, durability)
- Adds race-specific adaptations (heat, fueling, hydration)

### Step 5: Generate Guides
- Creates HTML training guide for each plan
- Includes phase-by-phase breakdown
- Race-specific tactics and equipment

---

## Nate's Dimensions - FULLY INCORPORATED ✅

### 1. Cadence Prescriptions by Archetype
**Implemented:**
- VO2max: 90-100rpm (high turnover)
- Threshold: 85-95rpm (race cadence)
- SFR/Force: 50-60rpm (force development)
- Endurance: Self-selected (comfortable)
- High cadence work: 100-120rpm (when specified)

**Example:**
```
• Cadence: 90-100rpm (high turnover for VO2max efficiency)
```

### 2. Position Prescriptions
**Implemented:**
- VO2max: Seated, hoods (quick recovery)
- Threshold: Seated, drops or hoods (race position)
- Endurance: Alternating hoods/drops (position practice)
- SFR: Seated (max torque development)
- Long rides: Alternating every 30min (aero efficiency)

**Example:**
```
• Position: Seated, drops or hoods (race position)
• Position: Alternating hoods/drops every 30 min (builds aero efficiency)
```

### 3. Durability Workouts
**FULLY IMPLEMENTED:**
- Detects durability structure: Long Z2 → Intervals → More Z2
- Formats as: "First Xmin Z2 (builds fatigue) → Then: intervals (performed while already tired)"
- Adds position alternation for durability rides
- Includes PURPOSE: "Building your ability to perform intervals when already fatigued—this is race simulation."

**Example:**
```
MAIN SET:
• First 60min Z2 (builds fatigue)
• Then: 4x8min @ Z4 with 2min recovery (performed while already tired)
• Final 30min Z2 (optional)

PURPOSE: Building your ability to perform intervals when already fatigued—this is race simulation.
```

### 4. In-Saddle vs Out-of-Saddle
**Partially Implemented:**
- Stomps: "Seated to standing (max torque development)"
- Need to add: Explicit alternating patterns for climbing/surges

### 5. Cadence in XML Attributes
**Implemented:**
- SFR: `Cadence="55" CadenceResting="65"`
- Z3 SteadyState: `CadenceLow="100" CadenceHigh="120"`
- IntervalsT: `Cadence="88"` (when specified)

### 6. Clean XML Structure
**FULLY IMPLEMENTED:**
- No text in step elements
- Proper element names (Warmup, SteadyState, IntervalsT, Cooldown)
- Valid durations
- Appropriate cadence attributes

---

## Training Methodologies by Tier

### Time Crunched (HIIT-Focused)
- **Philosophy**: Maximum fitness from minimal time
- **Structure**: 2-3 hard sessions/week, short endurance rides
- **Long rides**: Capped at 2-3 hours
- **Focus**: HIIT sharpens existing fitness (doesn't build base)

### Finisher (Traditional Pyramidal)
- **Philosophy**: Build durable aerobic base
- **Structure**: 4-5 sessions/week, balanced intensity distribution
- **Progression**: Base → Build → Peak → Taper
- **Focus**: Finish strong and comfortable

### Compete (Polarized Training)
- **Philosophy**: 80% easy / 20% hard
- **Structure**: 5-6 sessions/week, polarized intensity
- **Progression**: Extended base building, then sharpening
- **Focus**: Competitive finish, race for position

### Compete Masters (Masters-Optimized)
- **Philosophy**: Polarized with recovery emphasis
- **Structure**: Similar to Compete but with more recovery
- **Progression**: Slower build, more recovery days
- **Focus**: Age-group competitive

### Podium (High-Volume)
- **Philosophy**: Maximum volume with race-specific prep
- **Structure**: 6-7 sessions/week, high volume
- **Progression**: Extended base → build → peak → taper
- **Focus**: Race to win, podium finish

---

## Race-Specific Adaptations

### Heat Adaptation (Weeks 6-10)
- Added to workout descriptions
- Hydration protocols
- Heat management strategies

### Aggressive Fueling
- 60-90g carbs/hour targets
- Practice gut training
- Race-day nutrition protocols

### Dress Rehearsal
- Long ride (tier-specific duration)
- Test everything: nutrition, hydration, gear
- Mental preparation

### Robust Taper
- Freshness/form emphasis
- Volume reduction, maintain sharpness
- Race-week protocols

### Gravel Grit
- Mental toughness protocols
- Visualization techniques
- Breaking race into chunks

---

## Workout Description Structure

Every workout includes:

1. **WARM-UP**
   - Progressive building from Z1 to Z2
   - Duration-specific guidance

2. **MAIN SET**
   - Accurate structure matching XML
   - Cadence prescription (by archetype)
   - Position prescription (by archetype)
   - Durability structure (if applicable)

3. **COOL-DOWN**
   - Easy spin Z1-Z2
   - Recovery guidance

4. **PURPOSE**
   - Archetype-specific explanation
   - Progression context (level-based)
   - Why this workout matters

5. **EXECUTION** (when applicable)
   - Pacing guidance
   - Position instructions
   - Cadence targets
   - Race-specific notes

---

## Quality Assurance

### Validation Tests
1. **Naming Validation**: No "Ayahuasca" or "GOAT" references
2. **Architecture Validation**: Clean XML, proper elements
3. **FTP Test Validation**: Tests at correct weeks
4. **Durability Test Validation**: Tests at correct weeks, tier-scaled
5. **Workout Count Validation**: Matches duration (84/112/140 workouts)

### Regression Tests
- Marketplace descriptions
- Survey links
- Guide generation
- ZWO structure

---

## Output Per Plan

Each plan includes:
- **Workouts**: 84 (12w), 112 (16w), or 140 (20w) ZWO files
- **Training Guide**: HTML format with full plan details
- **Marketplace Description**: HTML for TrainingPeaks marketplace
- **Race Day Workout**: ZWO file with Three-Act pacing

---

*Methodology Status: Fully Implemented*  
*Nate's Dimensions: Fully Incorporated*  
*Ready for Generation: Yes*

