# Unbound 200 Plan Expansion - COMPLETE ✅

## Summary

Successfully generated **75 complete training plans** for Unbound Gravel 200 with:
- **5 Plan Types** × **3 Durations** × **5 Variations** = **75 Plans**
- FTP test integration (every ~6 weeks)
- All workouts with Nate's dimensions (cadence, position, durability)
- Race-specific adaptations (heat, fueling, hydration)
- TrainingPeaks export structure

---

## Generated Plans

### Plan Types
1. **Time Crunched** - HIIT-Focused (0-5 hrs/week)
2. **Finisher** - Traditional Pyramidal (5-8 hrs/week)
3. **Compete** - Polarized Training (8-12 hrs/week)
4. **Compete Masters** - Masters-optimized (8-12 hrs/week)
5. **Podium** - High-volume (12+ hrs/week)

### Durations
- **12 weeks**: 25 plans (Standard progression)
- **16 weeks**: 25 plans (Extended build)
- **20 weeks**: 25 plans (Maximum preparation)

### Variations
- **Standard** - Default progression
- **Volume Focus** - +5-10% volume emphasis
- **Intensity Focus** - More interval work
- **Balanced** - Balanced approach
- **Conservative** - -5-10% volume, more recovery

---

## FTP Test Integration

### Schedule
- **12-week plans**: Weeks 1, 7
- **16-week plans**: Weeks 1, 7, 13
- **20-week plans**: Weeks 1, 7, 13, 19

### FTP Test Format
- Converted from TrainingPeaks format (`2026-01-30_TheAssessm.zwo`)
- Proper GG format with SteadyState blocks
- Full description with WARM-UP, MAIN SET, COOL-DOWN, PURPOSE
- Unbound 200-specific notes included

### Verification
✅ FTP tests found in 20-week plans (W01, W07, W13, W19)
✅ FTP tests found in 16-week plans (W01, W07, W13)
✅ FTP tests found in 12-week plans (W01, W07)

---

## File Structure

```
Unbound Gravel 200/
├── 1. 1. Time Crunched Standard (12 weeks)/
│   ├── workouts/ (84 ZWO files)
│   ├── marketplace_description.html
│   ├── training_plan_guide.html
│   └── RACE_DAY_workout.zwo
├── ... (75 total plans)
└── trainingpeaks_export/
    └── PLAN_EXPORT_SUMMARY.md
```

### File Counts
- **12-week plans**: 84 workouts + 3 files = **87 files per plan**
- **16-week plans**: 112 workouts + 3 files = **115 files per plan**
- **20-week plans**: 140 workouts + 3 files = **143 files per plan**

**Total**: ~8,625 files generated

---

## TrainingPeaks Workflow

### First Time (Drag & Drop)
1. Open TrainingPeaks calendar
2. Navigate to plan folder (e.g., `1. 1. Time Crunched Standard (12 weeks)/workouts/`)
3. Drag all workouts into TrainingPeaks
4. Organize by week
5. Save as template plan

### Subsequent Plans (Copy/Paste)
1. Open saved template plan
2. **Copy entire plan structure**
3. Paste into new calendar
4. **Replace workouts** with new variation's workouts
5. **Much faster than drag/drop**

See: `trainingpeaks_export/PLAN_EXPORT_SUMMARY.md` for full instructions

---

## What's Included in Each Plan

### Workouts
- ✅ All workouts with Nate's dimensions:
  - Cadence prescriptions by archetype
  - Position guidance (seated, hoods, drops, alternating)
  - Durability workouts (long Z2 → intervals while fatigued)
  - Clean XML structure (no weird text)
- ✅ FTP tests at appropriate weeks
- ✅ Race day workout with Three-Act pacing

### Marketplace Description
- HTML formatted
- Plan philosophy and approach
- Race-specific adaptations
- What's included summary

### Training Guide
- Plan overview
- Phase-by-phase breakdown
- Weekly structure
- Race-specific tactics
- Equipment & logistics

### Race Day Workout
- Three-Act pacing framework
- Race-specific power zones
- Terrain considerations
- Tactical notes

---

## Next Steps

### Immediate
1. ✅ Review sample plans
2. ✅ Verify FTP test formatting
3. ✅ Check workout counts match durations

### Future Enhancements
1. Add guide infographics (philosophy diagrams, stats grids)
2. Test plan variations create distinct plans
3. Generate TrainingPeaks template files
4. Create plan comparison tool

---

## Verification Checklist

- [x] All 75 plans generated
- [x] FTP tests inserted at correct weeks
- [x] Workout counts match durations (84/112/140)
- [x] All plans have marketplace descriptions
- [x] All plans have training guides
- [x] All plans have race day workouts
- [x] TrainingPeaks export structure created
- [x] FTP test format correct (GG format)

---

## Command Used

```bash
python3 races/generate_expanded_race_plans.py \
    races/unbound_gravel_200.json \
    /Users/mattirowe/Downloads/2026-01-30_TheAssessm.zwo
```

**Result**: ✅ Successfully generated 75/75 plans

---

*Generated: December 26, 2025*  
*Status: COMPLETE ✅*

