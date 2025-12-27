# Plan Expansion Roadmap - Unbound 200

## Overview

Expanding the 5 simplified plans to support:
- **3 Durations**: 12, 16, and 20 weeks
- **3-5 Variations**: Per plan type
- **FTP Test Integration**: Every ~6 weeks in 20-week plans
- **Enhanced Guides**: With infographics and visual elements
- **TrainingPeaks Export**: For easy copy/paste workflow

---

## Plan Structure

### Base Plans (5 Types)
1. **Time Crunched** - HIIT-Focused (0-5 hrs/week)
2. **Finisher** - Traditional Pyramidal (5-8 hrs/week)
3. **Compete** - Polarized Training (8-12 hrs/week)
4. **Compete Masters** - Masters-optimized (8-12 hrs/week)
5. **Podium** - High-volume (12+ hrs/week)

### Durations
- **12 weeks**: Standard plan length
- **16 weeks**: Extended build phase
- **20 weeks**: Maximum preparation with FTP tests

### Variations (3-5 per plan)
1. **Standard** - Default progression
2. **Volume Focus** - Slightly higher volume emphasis
3. **Intensity Focus** - Slightly higher intensity emphasis
4. **Balanced** - Balanced volume and intensity
5. **Conservative** - More conservative progression

### Total Plans Generated
**5 plan types × 3 durations × 5 variations = 75 total plans**

---

## FTP Test Integration

### Test Schedule
- **12-week plans**: Weeks 1, 7
- **16-week plans**: Weeks 1, 7, 13
- **20-week plans**: Weeks 1, 7, 13, 19

### FTP Test Workout
Using: `2026-01-30_TheAssessm.zwo`
- **Structure**: 12min warmup → 5min RPE 6 → 5min RPE 2 → 5min ALL OUT → 5min RPE 2 → 20min ALL OUT → 10min cooldown
- **Purpose**: Sets training zones for next 6 weeks
- **Placement**: Typically replaces Tuesday workout

### Conversion to GG Format
- Convert FreeRide + textevents to proper SteadyState blocks
- Add GG-style description with WARM-UP, MAIN SET, COOL-DOWN, PURPOSE
- Include Unbound 200-specific notes

---

## Plan Extension Logic

### 12 → 16 Weeks
- Add 4 weeks using pattern from weeks 9-12
- Weeks 13-14: Extended build (volume +5%)
- Weeks 15-16: Peak build (maintain volume)

### 12 → 20 Weeks
- Add 8 weeks using pattern from weeks 9-12
- Weeks 13-16: Extended build phase
- Weeks 17-18: Peak build phase
- Weeks 19-20: Final build/taper prep
- Insert FTP tests at weeks 1, 7, 13, 19

### Variation Logic
- **Volume Focus**: Increase volume_percent by 5-10%
- **Intensity Focus**: Add more interval work, reduce recovery
- **Balanced**: Maintain standard ratios
- **Conservative**: Reduce volume_percent by 5-10%

---

## Guide Enhancements

### From Athlete Profiles (Infographic Elements)

#### 1. Philosophy Diagrams
- Visual representation of training approach
- Bar charts showing 80/20 split (polarized)
- Volume vs intensity visualization

#### 2. Quick Stats Boxes
- Grid layout with key metrics
- Plan duration, target hours, goal
- Visual stat boxes with large numbers

#### 3. Phase Cards
- Border-styled cards for each phase
- Header with phase name
- Body with phase details

#### 4. Weekly Structure Tables
- Day-by-day breakdown
- Key session indicators (🔑)
- Priority order when life gets in the way

#### 5. Neo-Brutalist Styling
- Bold borders, uppercase text
- Monospace font (Sometype Mono)
- High contrast, clean layout

### Guide Content by Duration

#### 12-Week Guides
- Standard progression
- 3-4 phases
- Standard taper

#### 16-Week Guides
- Extended build phase
- 4-5 phases
- Longer base building
- Extended taper

#### 20-Week Guides
- Maximum preparation
- 5-6 phases
- FTP test schedule highlighted
- Extended base + build phases
- Comprehensive taper

---

## TrainingPeaks Workflow

### First Time Setup (Drag & Drop)
1. Open TrainingPeaks calendar
2. Navigate to plan folder (e.g., "1. Time Crunched Standard (12 weeks)")
3. Drag workouts from `workouts/` folder into TrainingPeaks
4. Organize by week
5. Save as template plan

### Subsequent Plans (Copy/Paste)
1. Open saved template plan in TrainingPeaks
2. Copy entire plan structure
3. Paste into new calendar
4. Replace workouts with new variation's workouts
5. Much faster than drag/drop

### Export Structure
```
trainingpeaks_export/
├── PLAN_EXPORT_SUMMARY.md
├── variation_1_plans/  (Standard)
├── variation_2_plans/  (Volume Focus)
├── variation_3_plans/  (Intensity Focus)
└── ...
```

---

## Implementation Status

### ✅ Completed
- Base 5-plan structure
- 12-week plan generation
- Nate's workout dimensions (cadence, position, durability)
- Race-specific text (heat, fueling, hydration)

### 🚧 In Progress
- Expanded generator script (`generate_expanded_race_plans.py`)
- FTP test integration
- Plan extension logic (12→16→20 weeks)
- Variation system

### ⏭️ Next Steps
1. **Test FTP test conversion** - Verify FreeRide→SteadyState conversion
2. **Test plan extension** - Verify 16/20 week plans work correctly
3. **Test variations** - Verify variation logic creates distinct plans
4. **Enhance guide generator** - Add infographic elements
5. **Create TrainingPeaks export** - Structure for copy/paste workflow
6. **Generate all 75 plans** - Full expansion for Unbound 200

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
    └── [export structure]
```

---

## Guide Enhancements to Add

### From Athlete Profiles:

1. **Philosophy Diagram**
   ```html
   <div class="philosophy-diagram">
     <!-- Visual bar chart showing 80/20 split -->
   </div>
   ```

2. **Quick Stats Grid**
   ```html
   <div class="quick-stats">
     <div class="stat-box">
       <span class="stat-value">12</span>
       <span class="stat-label">Weeks</span>
     </div>
     <!-- More stats -->
   </div>
   ```

3. **Phase Cards**
   ```html
   <div class="phase-card">
     <div class="phase-card-header">Phase 1: Base Building</div>
     <div class="phase-card-body">...</div>
   </div>
   ```

4. **Weekly Structure Table**
   ```html
   <table>
     <tr>
       <th>Day</th>
       <th>Workout</th>
       <th>Notes</th>
     </tr>
     <!-- Key session indicators -->
   </table>
   ```

---

## Testing Checklist

- [ ] FTP test converts correctly (FreeRide → SteadyState)
- [ ] FTP test inserted at correct weeks (1, 7, 13, 19 for 20-week)
- [ ] 16-week plans extend correctly from 12-week base
- [ ] 20-week plans extend correctly with FTP tests
- [ ] Variations create distinct plans
- [ ] Guides match plan durations
- [ ] TrainingPeaks export structure works
- [ ] All 75 plans generate successfully

---

*Created: December 26, 2025*  
*For: Unbound Gravel 200 Plan Expansion*

