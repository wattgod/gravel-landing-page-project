# Git Commit Summary - Unified Training System

## Files to Commit

### Configuration Files (New)
- `races/config/phase_alignment.py` - Phase mapping logic
- `races/config/tier_config.py` - Tier definitions
- `races/config/race_strength_profiles.py` - Race-specific customization
- `races/config/weekly_structure.py` - Day assignment templates

### Generator Files (New)
- `races/unified_plan_generator.py` - Unified plan generator
- `races/schemas/unified_plan_schema.json` - JSON schema

### Test Files (New)
- `races/test_unified_system.py` - Regression test suite (29 tests)
- `races/run_regression_tests.sh` - Test runner script
- `races/REGRESSION_TESTS.md` - Test documentation

### Documentation Files (New)
- `races/UNIFIED_ARCHITECTURE.md` - Architecture documentation
- `races/UNIFIED_SYSTEM_SUMMARY.md` - System summary
- `races/INTEGRATION_COMPLETE.md` - Integration documentation
- `races/SESSION_SUMMARY.md` - Session summary
- `races/STRENGTH_CYCLING_INTEGRATION_GAPS.md` - Gap analysis

### Modified Files
- `races/generate_race_plans.py` - Integrated unified generator

### Generated Output (Should NOT commit)
- `races/Unbound Gravel 200/` - Generated plan outputs (exclude from commit)

---

## Recommended Commit Message

```
feat: Unified cycling + strength training system

- Add phase alignment configuration (cycling → strength mapping)
- Add tier variation (Ayahuasca 3x → Podium 1x frequency)
- Add race-specific strength profiles (9 races)
- Add weekly structure templates (day assignments)
- Add unified plan generator (coordinated cycling + strength)
- Integrate unified generator into generate_race_plans.py
- Add comprehensive regression test suite (29 tests, all passing)
- Add architecture documentation

Key features:
- Phase alignment prevents double-peaking
- Tier variation scales strength frequency
- Race profiles customize exercise emphasis
- Unified calendar shows day-by-day schedule
- One command generates all plans

Test coverage:
- Phase alignment: 5 tests
- Tier variation: 5 tests
- Race profiles: 5 tests
- Weekly structure: 5 tests
- Unified generator: 5 tests
- Calendar generation: 2 tests
- Integration: 1 test

Total: 29 tests, all passing ✅
```

---

## Git Commands

### Stage New Files
```bash
cd races/
git add config/
git add schemas/
git add unified_plan_generator.py
git add test_unified_system.py
git add run_regression_tests.sh
git add *.md
git add generate_race_plans.py
```

### Exclude Generated Output
```bash
# Add to .gitignore if not already there
echo "races/Unbound Gravel 200/" >> .gitignore
echo "races/*/calendar/" >> .gitignore
echo "races/*/plan_summary.json" >> .gitignore
```

### Commit
```bash
git commit -m "feat: Unified cycling + strength training system

- Add phase alignment configuration
- Add tier variation and race profiles
- Add unified plan generator
- Integrate into generate_race_plans.py
- Add regression test suite (29 tests)
- Add comprehensive documentation"
```

---

## Status Check

**Current Status**: 299 files modified/untracked

**Core System Files**: ~15 files (should commit)
**Generated Output**: ~284 files (should NOT commit)

**Recommendation**: 
1. Add generated output to .gitignore
2. Commit core system files
3. Push to GitHub

---

**Last Updated**: 2024-12-15

