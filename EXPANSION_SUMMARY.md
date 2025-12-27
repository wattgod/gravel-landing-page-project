# Plan Expansion Summary - Unbound 200

## What We're Building

### Scope
- **5 Plan Types** × **3 Durations** × **5 Variations** = **75 Total Plans**
- Each plan includes: workouts, marketplace description, guide, race day workout
- FTP test integration for 20-week plans (every ~6 weeks)
- Enhanced guides with infographic elements

---

## Plan Types

1. **Time Crunched** - HIIT-Focused (0-5 hrs/week)
2. **Finisher** - Traditional Pyramidal (5-8 hrs/week)
3. **Compete** - Polarized Training (8-12 hrs/week)
4. **Compete Masters** - Masters-optimized (8-12 hrs/week)
5. **Podium** - High-volume (12+ hrs/week)

---

## Durations

### 12 Weeks (Standard)
- Standard progression
- FTP tests: Weeks 1, 7
- Standard taper

### 16 Weeks (Extended)
- Extended build phase
- FTP tests: Weeks 1, 7, 13
- Longer base building
- Extended taper

### 20 Weeks (Maximum)
- Maximum preparation time
- FTP tests: Weeks 1, 7, 13, 19 (every ~6 weeks)
- Extended base + build phases
- Comprehensive taper

---

## Variations

1. **Standard** - Default progression
2. **Volume Focus** - +5-10% volume emphasis
3. **Intensity Focus** - More interval work, less recovery
4. **Balanced** - Balanced volume and intensity
5. **Conservative** - -5-10% volume, more recovery

---

## FTP Test Integration

### Source
- File: `2026-01-30_TheAssessm.zwo`
- Structure: 12min warmup → 5min RPE 6 → 5min RPE 2 → 5min ALL OUT → 5min RPE 2 → 20min ALL OUT → 10min cooldown

### Conversion
- Convert FreeRide + textevents → SteadyState blocks
- Add GG-style description (WARM-UP, MAIN SET, COOL-DOWN, PURPOSE)
- Include Unbound 200-specific notes

### Placement
- Replaces Tuesday workout in test weeks
- Weeks: 1, 7 (12-week), 1, 7, 13 (16-week), 1, 7, 13, 19 (20-week)

---

## Guide Enhancements (From Athlete Profiles)

### 1. Philosophy Diagrams
- Visual bar chart showing 80/20 split (polarized)
- Easy vs Hard intensity distribution
- Plan-specific philosophy visualization

### 2. Quick Stats Grid
- Grid layout with key metrics
- Plan duration, target hours, goal
- Visual stat boxes

### 3. Phase Cards
- Border-styled cards for each training phase
- Header with phase name
- Body with phase details and tips

### 4. Weekly Structure Tables
- Day-by-day workout breakdown
- Key session indicators (🔑)
- Priority order when life gets in the way

### 5. Neo-Brutalist Styling
- Bold borders, uppercase text
- Monospace font (Sometype Mono)
- High contrast, clean layout

---

## TrainingPeaks Workflow

### First Time (Drag & Drop)
1. Open TrainingPeaks calendar
2. Navigate to plan folder
3. Drag workouts from `workouts/` folder
4. Organize by week
5. Save as template plan

### Subsequent Plans (Copy/Paste)
1. Open saved template plan
2. Copy entire plan structure
3. Paste into new calendar
4. Replace workouts with new variation's workouts
5. **Much faster than drag/drop**

### Export Structure
```
trainingpeaks_export/
├── PLAN_EXPORT_SUMMARY.md
├── variation_1_plans/  (Standard - use as template)
├── variation_2_plans/  (Volume Focus)
├── variation_3_plans/  (Intensity Focus)
└── ...
```

---

## Implementation Status

### ✅ Completed
- Base 5-plan structure (12 weeks)
- Nate's workout dimensions (cadence, position, durability)
- Race-specific text (heat, fueling, hydration)
- Expanded generator script framework

### 🚧 In Progress
- FTP test conversion (FreeRide → SteadyState)
- Plan extension logic (12→16→20 weeks)
- Variation system
- Guide enhancements

### ⏭️ Next Steps
1. Test FTP test conversion
2. Test plan extension (16/20 weeks)
3. Test variations
4. Add guide infographics
5. Generate all 75 plans
6. Create TrainingPeaks export structure

---

## File Structure

```
Unbound Gravel 200/
├── 1. Time Crunched Standard (12 weeks)/
│   ├── workouts/ (84 ZWO files)
│   ├── marketplace_description.html
│   ├── training_plan_guide.html
│   └── RACE_DAY_workout.zwo
├── 1. Time Crunched Standard (16 weeks)/
├── 1. Time Crunched Standard (20 weeks)/
├── 1. Time Crunched Volume Focus (12 weeks)/
├── ... (75 total plans)
└── trainingpeaks_export/
    ├── PLAN_EXPORT_SUMMARY.md
    └── [export structure for copy/paste]
```

---

## Key Features

### ✅ What's Working
- Base plan generation
- Workout dimensions (cadence, position, durability)
- Race-specific adaptations
- Clean XML structure

### 🔧 What Needs Work
- FTP test conversion (FreeRide → proper structure)
- Plan extension logic (needs testing)
- Variation system (needs refinement)
- Guide infographics (needs implementation)
- TrainingPeaks export structure

---

*Created: December 26, 2025*  
*Generator: `generate_expanded_race_plans.py`*

