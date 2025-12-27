# Plan Regeneration Needed

## Status

✅ **Code committed to GitHub**  
⚠️ **Plans need regeneration** to include durability tests

---

## What Was Generated

### Initial Generation (Before Durability Tests)
- ✅ 75 plans generated (5 types × 3 durations × 5 variations)
- ✅ 8,545 ZWO workout files
- ✅ 97 training guides
- ✅ FTP tests integrated (but only in some plans)
- ❌ Durability tests NOT integrated (code added after generation)

### Validation Results
- ❌ FTP tests missing in 12-week plans
- ❌ Durability tests missing in all plans
- ❌ 20-week plans only have 85 workouts (should have 140)
- ✅ Guides present
- ✅ ZWO structure valid

---

## What Needs Regeneration

### To Include:
1. **FTP Tests** at weeks 1, 7, 13, 19 (all plans)
2. **Durability Tests** at weeks 7, 13, 19 (tier-scaled)
3. **Proper plan extension** for 16 and 20-week plans

### Command to Regenerate:
```bash
cd /Users/mattirowe/Documents/GravelGod/project/gravel-landing-page-project
python3 races/generate_expanded_race_plans.py \
    races/unbound_gravel_200.json \
    /Users/mattirowe/Downloads/2026-01-30_TheAssessm.zwo
```

---

## What's Committed to GitHub

✅ **Code Files:**
- `generate_expanded_race_plans.py` - Main generator
- `ftp_test_converter.py` - FTP test converter
- `durability_test_converter.py` - Durability test converter
- `test_expanded_plans_validation.py` - Validation tests

✅ **Documentation:**
- `PLAN_EXPANSION_ROADMAP.md`
- `EXPANSION_SUMMARY.md`
- `GUIDE_ENHANCEMENTS_FROM_ATHLETE_PROFILES.md`
- `DURABILITY_TEST_INTEGRATION.md`
- `DURABILITY_TEST_SUMMARY.md`
- `GENERATION_STATUS.md`

✅ **Modified:**
- `workout_description_generator.py` - Updated with Nate's dimensions

---

## Next Steps

1. **Regenerate plans** with durability test integration
2. **Run validation tests** to verify
3. **Commit generated plans** (if desired, or keep local only)

---

*Status: December 26, 2025*  
*Code: Committed ✅*  
*Plans: Need Regeneration ⚠️*

