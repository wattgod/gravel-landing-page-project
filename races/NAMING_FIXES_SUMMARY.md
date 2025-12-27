# Naming Convention Fixes

## Issues Found

1. **Guide Generator**: Still using "AYAHUASCA" instead of "TIME CRUNCHED"
2. **Guide Template**: References "Ayahuasca" in tier list
3. **GOAT References**: Still present in guide generator
4. **ZWO Files**: May contain "Ayahuasca" in descriptions

## Fixes Applied

### Guide Generator (`guide_generator.py`)
- ✅ Updated tier detection to map "time crunched" → "TIME CRUNCHED"
- ✅ Updated `get_weekly_hours()` to include "TIME CRUNCHED"
- ✅ Updated `get_weekly_structure()` to include "TIME CRUNCHED"
- ✅ Updated volume category description to use "TIME CRUNCHED"
- ✅ Removed GOAT references from Advanced level description
- ✅ Updated plan titles to use "Time Crunched Plan"
- ✅ Updated docstring to reflect new tier names

### Guide Template (`guide_template_full.html`)
- ✅ Updated tier list from "Ayahuasca" to "Time Crunched"

### Validation Test
- ✅ Created `test_naming_validation.py` to catch naming violations

## Still Need to Fix

1. **ZWO Generator**: Check `tier_display` mapping
2. **Regenerate Plans**: All plans need regeneration with fixed naming
3. **Marketplace Generator**: May need updates

## Next Steps

1. Fix ZWO generator tier display
2. Regenerate all 15 plans
3. Run validation test to verify
4. Commit fixes

---

*Status: In Progress*

