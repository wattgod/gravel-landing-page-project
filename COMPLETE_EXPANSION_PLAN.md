# Complete Plan Expansion - Unbound 200

## Executive Summary

Expanding from **5 plans (12 weeks)** to **75 plans** with:
- **3 Durations**: 12, 16, 20 weeks
- **5 Variations**: Standard, Volume Focus, Intensity Focus, Balanced, Conservative
- **FTP Test Integration**: Every ~6 weeks (especially 20-week plans)
- **Enhanced Guides**: With infographics from athlete profiles
- **TrainingPeaks Workflow**: Drag/drop once, then copy/paste

---

## What We've Built

### ✅ Completed Components

1. **Base Generator** (`generate_expanded_race_plans.py`)
   - Supports multiple durations
   - Variation system
   - FTP test integration

2. **FTP Test Converter** (`ftp_test_converter.py`)
   - Converts TrainingPeaks format → GG format
   - FreeRide + textevents → SteadyState blocks
   - ✅ Tested and working

3. **Documentation**
   - `PLAN_EXPANSION_ROADMAP.md` - Full roadmap
   - `EXPANSION_SUMMARY.md` - Quick reference
   - `GUIDE_ENHANCEMENTS_FROM_ATHLETE_PROFILES.md` - Infographic guide

---

## Plan Matrix

| Plan Type | 12 Weeks | 16 Weeks | 20 Weeks | Variations | Total |
|-----------|----------|----------|----------|------------|-------|
| Time Crunched | ✓ | ✓ | ✓ | 5 | 15 |
| Finisher | ✓ | ✓ | ✓ | 5 | 15 |
| Compete | ✓ | ✓ | ✓ | 5 | 15 |
| Compete Masters | ✓ | ✓ | ✓ | 5 | 15 |
| Podium | ✓ | ✓ | ✓ | 5 | 15 |
| **TOTAL** | **25** | **25** | **25** | - | **75** |

---

## FTP Test Schedule

### 12-Week Plans
- **Week 1**: Initial FTP test (sets baseline)
- **Week 7**: Mid-plan FTP test (recalibrate zones)

### 16-Week Plans
- **Week 1**: Initial FTP test
- **Week 7**: Mid-plan FTP test
- **Week 13**: Late-plan FTP test (before final build)

### 20-Week Plans
- **Week 1**: Initial FTP test
- **Week 7**: First recalibration
- **Week 13**: Second recalibration
- **Week 19**: Final test before taper

**Rationale**: Every ~6 weeks ensures training zones stay accurate as fitness improves.

---

## Variations Explained

### 1. Standard
- Default progression from base plan
- Balanced volume and intensity
- Standard taper

### 2. Volume Focus
- +5-10% volume emphasis
- More endurance work
- Longer base building phase
- Good for: Athletes who respond well to volume

### 3. Intensity Focus
- More interval work
- Slightly less recovery
- Higher intensity density
- Good for: Time-crunched athletes, power-focused

### 4. Balanced
- Explicitly balanced approach
- Equal emphasis on volume and intensity
- Moderate progression
- Good for: Most athletes

### 5. Conservative
- -5-10% volume
- More recovery days
- Slower progression
- Good for: Injury-prone, older athletes, busy schedules

---

## Guide Enhancements (From Athlete Profiles)

### Visual Elements to Add:

1. **Philosophy Diagram**
   - Bar chart: 80% Easy / 20% Hard
   - Plan-specific visualization
   - Visual intensity distribution

2. **Quick Stats Grid**
   - Plan duration (12/16/20 weeks)
   - Target hours per week
   - Total workouts
   - FTP test frequency

3. **Phase Cards**
   - Base Building phase
   - Build phase
   - Peak phase
   - Taper phase
   - FTP test weeks (highlighted)

4. **Weekly Structure Table**
   - Day-by-day breakdown
   - Key session indicators (🔑)
   - Priority order

5. **Neo-Brutalist Styling**
   - Bold borders
   - Uppercase text
   - Monospace font
   - High contrast

---

## TrainingPeaks Workflow

### Step 1: First Plan (Drag & Drop)
1. Open TrainingPeaks calendar
2. Go to plan folder: `1. Time Crunched Standard (12 weeks)/workouts/`
3. Drag all 84 workouts into TrainingPeaks
4. Organize by week (Week 1, Week 2, etc.)
5. Save as template: "Time Crunched Standard 12w"

### Step 2: Subsequent Plans (Copy/Paste)
1. Open saved template plan
2. **Copy entire plan structure** (all weeks, all days)
3. Paste into new calendar
4. **Replace workouts** with new variation's workouts
5. Save as new plan

**Time Savings**: Copy/paste is 10x faster than drag/drop

### Export Structure
```
trainingpeaks_export/
├── PLAN_EXPORT_SUMMARY.md
├── templates/
│   ├── time_crunched_12w_template.tp
│   ├── finisher_12w_template.tp
│   └── ...
└── instructions.md
```

---

## Implementation Checklist

### Phase 1: Core Expansion ✅
- [x] Expanded generator script
- [x] FTP test converter
- [x] Plan extension logic (12→16→20)
- [x] Variation system framework

### Phase 2: Testing & Refinement 🚧
- [ ] Test FTP test insertion (20-week plans)
- [ ] Test plan extension (16/20 weeks)
- [ ] Test variations create distinct plans
- [ ] Verify workout counts match durations

### Phase 3: Guide Enhancements ⏭️
- [ ] Add philosophy diagrams
- [ ] Add quick stats grid
- [ ] Add phase cards
- [ ] Add weekly structure tables
- [ ] Update styling to neo-brutalist

### Phase 4: TrainingPeaks Export ⏭️
- [ ] Create export structure
- [ ] Generate template plans
- [ ] Create copy/paste instructions
- [ ] Test workflow

### Phase 5: Full Generation ⏭️
- [ ] Generate all 75 plans
- [ ] Verify all files created
- [ ] Test sample plans
- [ ] Create final documentation

---

## File Counts

### Per Plan:
- **12 weeks**: 84 workouts + marketplace + guide + race day = **87 files**
- **16 weeks**: 112 workouts + marketplace + guide + race day = **115 files**
- **20 weeks**: 140 workouts + marketplace + guide + race day = **143 files**

### Total Files:
- **12-week plans**: 25 plans × 87 files = **2,175 files**
- **16-week plans**: 25 plans × 115 files = **2,875 files**
- **20-week plans**: 25 plans × 143 files = **3,575 files**
- **TOTAL**: **8,625 files**

---

## Next Steps

1. **Test the expanded generator** with a single plan
2. **Verify FTP test integration** works correctly
3. **Test plan extension** (create a 16-week and 20-week plan)
4. **Add guide enhancements** (infographics)
5. **Generate all 75 plans** for Unbound 200
6. **Create TrainingPeaks export** structure

---

## Command to Run

```bash
# Generate all expanded plans
python3 races/generate_expanded_race_plans.py \
    races/unbound_gravel_200.json \
    /Users/mattirowe/Downloads/2026-01-30_TheAssessm.zwo
```

This will generate:
- 75 complete plans
- All workouts with Nate's dimensions
- FTP tests in 20-week plans
- Enhanced guides (once implemented)
- TrainingPeaks export structure

---

*Created: December 26, 2025*  
*Status: Framework Complete, Ready for Testing*

