# Unbound 200 Plan Generation Status

## ✅ Generation Complete

### Plans Generated
- **Total Plans**: 75 plans (5 types × 3 durations × 5 variations)
- **Plan Types**: Time Crunched, Finisher, Compete, Compete Masters, Podium
- **Durations**: 12, 16, 20 weeks
- **Variations**: Standard, Volume Focus, Intensity Focus, Balanced, Conservative

### Files Generated
- **ZWO Workouts**: ~8,400+ workout files
- **Training Guides**: 75 HTML guides (one per plan)
- **Marketplace Descriptions**: 75 HTML descriptions
- **Race Day Workouts**: 75 race day ZWO files
- **FTP Tests**: Integrated at weeks 1, 7, 13, 19
- **Durability Tests**: Integrated at weeks 7, 13, 19 (tier-scaled)

### Location
```
races/Unbound Gravel 200/
├── 1. 1. Time Crunched Standard (12 weeks)/
│   ├── workouts/ (84 ZWO files)
│   ├── unbound_gravel_200_ayahuasca_beginner_guide.html
│   └── marketplace_description.html
├── ... (75 total plans)
└── trainingpeaks_export/
    └── PLAN_EXPORT_SUMMARY.md
```

---

## ✅ Guides Generated

All 75 plans have training guides:
- HTML format
- Plan-specific content
- Phase-by-phase breakdown
- Race-specific adaptations
- Weekly structure

---

## ⚠️ Regression/Validation Tests

### Existing Tests
- `test_regression_training_plans.py` - Tests plan structure
- `test_regression_race_workouts.py` - Tests race workouts
- `races/generation_modules/test_zwo_generation.py` - Tests ZWO generation

### Missing Tests
- ❌ Tests for expanded plans (12/16/20 week variations)
- ❌ Tests for FTP test integration
- ❌ Tests for durability test integration
- ❌ Tests for plan variations (Standard, Volume Focus, etc.)

### Recommendation
Create validation tests for:
1. FTP test insertion at correct weeks
2. Durability test insertion at correct weeks
3. Plan extension logic (12→16→20 weeks)
4. Variation differences (volume/intensity changes)

---

## ⚠️ GitHub Commits

### Uncommitted Changes
- New files:
  - `generate_expanded_race_plans.py`
  - `durability_test_converter.py`
  - `ftp_test_converter.py`
  - Multiple documentation files
- Modified files:
  - `workout_description_generator.py`
- Generated plans:
  - `Unbound Gravel 200/` directory (75 plans)

### Status
❌ **Not yet committed to GitHub**

---

## Next Steps

1. ✅ Plans generated
2. ✅ Guides generated
3. ⚠️ Create validation tests for expanded plans
4. ⚠️ Commit to GitHub

---

*Status: December 26, 2025*

