# Unbound 200 - Simplified 5-Plan Generation Documentation

## Overview

This document explains the generation of **5 simplified training plans** for Unbound 200, replacing the previous 15-plan structure. Each plan is a 12-week program specifically tailored to the unique demands of Unbound Gravel 200.

---

## 1. TRAINING METHOD USED

### Core Philosophy: **Polarized Training Model**

All 5 plans follow a polarized training approach:

- **80% Low-Intensity Endurance (Z1-Z2)**
  - Builds aerobic base
  - Enhances fat oxidation
  - Develops durability for 12-16 hour efforts
  - Active recovery between hard sessions

- **20% High-Intensity Intervals**
  - VO2max intervals (30/30s, extended VO2)
  - Threshold work (steady state, progressive)
  - Mixed intervals (climbing simulations)
  - Race-specific efforts

### Plan-Specific Adaptations:

1. **Finisher (0-5 hrs/week)**
   - HIIT-focused survival mode
   - Maximum time efficiency
   - Minimal volume, maximum intensity
   - Focus: Finish the race

2. **Finisher Plus (5-8 hrs/week)**
   - Balanced HIIT + endurance
   - More volume than Finisher
   - Better durability development
   - Focus: Finish strong and comfortable

3. **Compete (8-12 hrs/week)**
   - Full periodization
   - Structured build phases
   - Race-specific work
   - Focus: Competitive finish, race for position

4. **Compete Masters (8-12 hrs/week)**
   - Masters-optimized recovery
   - Longer recovery between intervals
   - Age-group competitive focus
   - Focus: Age-group competitive

5. **Podium (12+ hrs/week)**
   - High-volume training
   - Elite preparation
   - Maximum race-specific work
   - Focus: Race to win, podium finish

---

## 2. WORKOUT DIMENSIONS USED

The generator uses **4 key workout dimensions** from the Unbound 200 race data:

### ✓ **HEAT TRAINING** (Enabled)

**Protocol Structure:**
- **Tier 3 (Active Training)**: Weeks 6-10
  - Endurance rides: Active heat training (indoor trainer with no fans, hot bath, or sauna)
  - Quality sessions: Post-exercise heat exposure (preserve workout quality)
  
- **Tier 2 (Build-up)**: Weeks 4-5
  - Introduction phase
  - Gradual adaptation

- **Tier 1 (Maintenance)**: Weeks 11-12
  - Maintenance protocol
  - Prevents adaptation decay

**Implementation:**
- **Endurance Rides (Weeks 6-10)**:
  - Option 1: Indoor trainer (no fans, overdress)
  - Option 2: Post-exercise hot bath (40°C, 30-40 min)
  - Option 3: Sauna (80-100°C, 25-30 min)
  - Target core temp: 38.5-39.0°C for 45-60 min

- **Quality Sessions (Weeks 6-10)**:
  - Complete in cool conditions (preserve workout quality)
  - Post-exercise: 30-40 min hot bath OR 25-30 min sauna

**Effect:** 5-8% performance improvement in hot conditions. Plasma volume expansion, enhanced sweating, reduced cardiovascular strain.

### ✓ **AGGRESSIVE FUELING** (Enabled)

**Configuration:**
- Target: **60-90g carbs/hour** (up to 100g on dress rehearsal)
- Applied to: Long rides **>3 hours**
- Race-specific emphasis: Start fueling from mile 1

**Workout Text Added:**
```
• UNBOUND GRAVEL 200 - AGGRESSIVE FUELING:
Target 60-90g carbs/hour (up to 100g on dress rehearsal). Train your gut aggressively. 
This is critical for Unbound Gravel 200's long day. Competitors need aggressive fueling—
race day isn't the time to discover your stomach can't handle 80g carbs/hour. 
Practice your race-day nutrition products. Start fueling from mile 1.
```

### ✓ **DRESS REHEARSAL** (Enabled)

**Configuration:**
- Week: **9** (Saturday)
- Duration by tier:
  - Finisher: 5 hours
  - Finisher Plus: 7 hours
  - Compete: 9 hours
  - Compete Masters: 9 hours
  - Podium: 10 hours

**Workout Text Added:**
```
• UNBOUND GRAVEL 200 - DRESS REHEARSAL:
THIS IS YOUR 9-HOUR 'BLOW OUT DAY.' CLEAR YOUR SCHEDULE. This is logistics practice, 
fueling practice, heat practice, and mental preparation all in one. Test EVERYTHING: 
nutrition products, hydration system, clothing, bike setup, tire pressure. Practice eating 
while riding. Practice bottle handoffs. Practice pacing. For Competitors, this 9-hour ride 
is worth 15 shorter rides for race prep. This is the difference between finishing and 
performing at your best.
```

### ✓ **ROBUST TAPER** (Enabled)

**Configuration:**
- Weeks: **11-12**
- Focus: Recovery, race prep, mental preparation

**Workout Text Added:**
- Reduced volume
- Maintained intensity (shorter intervals)
- Emphasis on recovery and race preparation
- Mental preparation guidance

### ✓ **HYDRATION PROTOCOLS** (Automatic)

**Applied to all workouts based on duration:**

- **<90 min (any intensity)**:
  - 1 bottle/hr with electrolytes mandatory
  - Before hard efforts: 1 gel
  - Light urine color (not clear) = well hydrated

- **>90 min low intensity**:
  - 60g carbs/hr
  - 1-1.5 bottles/hr
  - 600-1200 mg sodium/hr (depending on heat)
  - Monitor sweat rate

- **>90 min high intensity/intervals/heat**:
  - 90g carbs/hr
  - 1.5 bottles/hr minimum
  - 1000-1500 mg sodium/hr
  - Aggressive cooling: ice sock, dump water, shade stops

**Daily Baseline Hydration:**
- Start day hydrated: ~500 ml water + 500-1000 mg sodium with breakfast
- Pre-ride (60 min before): 500 ml fluid + 300-600 mg sodium
- Aim for light urine color (not clear)

### ✓ **POSITION ALTERNATION** (Automatic)

**Applied to endurance and long rides:**

- Alternate position every 30 minutes
- 30 min in drops (aero, race position)
- 30 min in hoods (power production, comfort)
- Builds both aero efficiency and power production

---

## 3. SPECIAL TEXT ADDED FOR UNBOUND 200

Each workout includes **race-specific text** tailored to Unbound 200's unique challenges:

### Heat Acclimatization Protocol
- **Weeks 6-10**: Active heat training instructions
- **Weeks 4-5**: Build-up phase guidance
- **Weeks 11-12**: Maintenance protocol
- Safety warnings (never exceed 39.5°C core temp)

### Aggressive Fueling Reminders
- Target 60-90g carbs/hour
- Start fueling from mile 1
- Train your gut aggressively
- Practice race-day nutrition products

### Hydration Strategies
- Duration-based hydration protocols
- Sodium intake recommendations (600-1500 mg/hr)
- Daily baseline hydration reminders
- Sweat rate monitoring guidance

### Position Alternation
- Drops vs hoods guidance
- 30-minute rotation schedule
- Aero efficiency + power production balance

### Dress Rehearsal Emphasis (Week 9)
- Clear your schedule
- Test everything: nutrition, hydration, clothing, bike setup
- Logistics practice
- Mental preparation

### Robust Taper Guidance (Weeks 11-12)
- Recovery focus
- Race prep emphasis
- Mental preparation
- Reduced volume, maintained intensity

### Race-Specific Tactics
- **Pacing first 90 minutes**: Critical for Unbound
- **Mechanical self-sufficiency**: Practice tire plugging, chain repair
- **Heat management**: Cooling strategies, shade stops
- **Mental preparation**: Dark patch at mile 120-150, second wind at mile 155-165

### Unbound-Specific Reminders
- "The fastest tire at Unbound is the one with air in it"
- Equipment survival > marginal gains
- Conservative equipment selection
- Mechanical self-sufficiency practice

---

## 4. TOTAL PLANS GENERATED: **5 PLANS**

### Plan 1: Finisher (12 weeks)
- **Target Hours**: 0-5 hrs/week
- **Goal**: Finish the race
- **Philosophy**: HIIT-focused survival mode
- **Replaces**: Ayahuasca Beginner, Finisher Beginner
- **Source Plans**: 
  - "1. Ayahuasca Beginner (12 weeks)"
  - "5. Finisher Beginner (12 weeks)"

### Plan 2: Finisher Plus (12 weeks)
- **Target Hours**: 5-8 hrs/week
- **Goal**: Finish strong and comfortable
- **Philosophy**: Balanced HIIT + endurance
- **Replaces**: Ayahuasca Intermediate, Finisher Intermediate
- **Source Plans**:
  - "2. Ayahuasca Intermediate (12 weeks)"
  - "6. Finisher Intermediate (12 weeks)"

### Plan 3: Compete (12 weeks)
- **Target Hours**: 8-12 hrs/week
- **Goal**: Competitive finish, race for position
- **Philosophy**: Structured periodization
- **Replaces**: Compete Intermediate, Compete Advanced
- **Source Plans**:
  - "10. Compete Intermediate (12 weeks)"
  - "11. Compete Advanced (12 weeks)"

### Plan 4: Compete Masters (12 weeks)
- **Target Hours**: 8-12 hrs/week
- **Goal**: Age-group competitive
- **Philosophy**: Masters-optimized recovery and intensity
- **Replaces**: Compete Masters, Ayahuasca Masters, Finisher Masters
- **Source Plans**:
  - "3. Ayahuasca Masters (12 weeks)"
  - "8. Finisher Masters (12 weeks)"
  - "12. Compete Masters (12 weeks)"

### Plan 5: Podium (12 weeks)
- **Target Hours**: 12+ hrs/week
- **Goal**: Race to win, podium finish
- **Philosophy**: High-volume, race-specific preparation
- **Replaces**: Podium Advanced, Podium Advanced GOAT
- **Source Plans**:
  - "14. Podium Advanced (12 weeks)"
  - "15. Podium Advanced GOAT (12 weeks)"

---

## 5. UPDATED GUIDES

Each plan includes a **simplified guide** with:

### Guide Structure (using `guide_template_simplified.html`):

1. **Tier Philosophy**
   - Training approach explanation
   - Plan-specific methodology

2. **What the Plan Includes**
   - Plan features
   - Workout types
   - Training structure

3. **18,000+ Word Comprehensive Guide**
   - Complete training manual
   - No gaps, no guesswork
   - All tested protocols

4. **Race-Specific Adaptations**
   - Heat acclimatization protocol
   - Aggressive fueling strategies
   - Hydration protocols
   - Dress rehearsal guidance
   - Robust taper instructions
   - Race-day tactics

5. **Alternative Warning**
   - What happens without proper preparation
   - Why this plan matters

6. **What This Plan Delivers**
   - Expected outcomes
   - Performance improvements
   - Race-day readiness

### Guide Content Summary:

- **Training Philosophy**: Polarized model explanation
- **Workout Structure**: Weekly progression
- **Heat Protocol**: Weeks 6-10 active training
- **Fueling Strategy**: 60-90g carbs/hour
- **Hydration**: Duration-based protocols
- **Dress Rehearsal**: Week 9 emphasis
- **Taper**: Weeks 11-12 robust taper
- **Race Tactics**: Pacing, mechanical prep, mental prep
- **Equipment**: Tire selection, pressure recommendations
- **Mental Preparation**: Dark patch, second wind, psychological landmarks

---

## GENERATION PROCESS

### Command:
```bash
python3 races/generate_simplified_race_plans.py races/unbound_gravel_200.json
```

### Output Structure:
```
Unbound Gravel 200/
├── 1. Finisher (12 weeks)/
│   ├── workouts/
│   │   ├── W01 Mon - Rest.zwo
│   │   ├── W01 Tue - FTP Test + Easy Spin.zwo
│   │   └── ... (84 total workouts)
│   ├── marketplace_description.html
│   ├── training_plan_guide.html
│   └── race_day_workout.zwo
├── 2. Finisher Plus (12 weeks)/
│   └── ...
├── 3. Compete (12 weeks)/
│   └── ...
├── 4. Compete Masters (12 weeks)/
│   └── ...
└── 5. Podium (12 weeks)/
    └── ...
```

### Files Generated Per Plan:
- **84 ZWO workout files** (12 weeks × 7 days/week)
- **1 Marketplace description** (HTML)
- **1 Training plan guide** (HTML, simplified template)
- **1 Race day workout** (ZWO)

**Total Files**: 5 plans × 87 files = **435 files**

---

## KEY DIFFERENCES FROM OLD 15-PLAN STRUCTURE

1. **Simplified Selection**: 5 clear options vs 15 confusing choices
2. **Better Positioning**: Each plan has distinct target athlete
3. **Consolidated Logic**: Merges best elements from multiple old plans
4. **Race-Specific**: All plans include Unbound 200-specific adaptations
5. **Updated Guides**: Simplified template, clearer structure
6. **Consistent Dimensions**: All plans use same workout dimensions (heat, fueling, etc.)

---

## VALIDATION

All generated workouts are validated against:
- ✅ Workout architecture standards (no text in XML elements)
- ✅ Correctly labeled intervals (IntervalsT, SteadyState, etc.)
- ✅ Cadence ranges provided where appropriate
- ✅ Power values as decimal percentages of FTP
- ✅ Race-specific text properly formatted
- ✅ Heat training protocol correctly applied
- ✅ Fueling and hydration notes included

---

*Generated: December 26, 2025*  
*For: Unbound Gravel 200 Training Plans*  
*Generator: `generate_simplified_race_plans.py`*

