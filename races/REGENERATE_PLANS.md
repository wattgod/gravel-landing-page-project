# Regenerate Plans - Naming Fixes Applied

## Status

✅ **Naming fixes committed to GitHub**  
⚠️ **Plans need regeneration** to apply fixes

## Fixes Applied

1. ✅ Guide generator uses "TIME CRUNCHED" instead of "AYAHUASCA"
2. ✅ Removed GOAT references
3. ✅ Updated guide template tier list
4. ✅ Fixed ZWO generator tier display mapping
5. ✅ Added validation test

## Regeneration Command

```bash
cd /Users/mattirowe/Documents/GravelGod/project/gravel-landing-page-project
python3 races/generate_expanded_race_plans.py \
    races/unbound_gravel_200.json \
    /Users/mattirowe/Downloads/2026-01-30_TheAssessm.zwo
```

## Validation After Regeneration

```bash
cd /Users/mattirowe/Documents/GravelGod/project/gravel-landing-page-project/races
python3 test_naming_validation.py
```

Should show: ✅ All naming conventions validated!

---

*Status: Ready for regeneration*

