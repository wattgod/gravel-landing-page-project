# Race-Specific Modules Implementation

**Date:** December 5, 2024  
**Status:** ✅ Complete

## Overview

Added 6 race-specific modules to the guide generator that dynamically insert race-specific content into Sections 10 and 11 of the training guides.

---

## ✅ What Was Implemented

### 1. Python Functions (guide_generator.py)

Added 6 builder functions that generate HTML modules from `race_specific` JSON data:

1. **`build_flint_module()`** - Flint rock hazard protocol with sector table
2. **`build_tire_pressure_module()`** - Tire pressure recommendations by rider weight
3. **`build_wind_module()`** - Wind protocol with group/solo tactics
4. **`build_time_drift_module()`** - Expected time drift by conditions
5. **`build_decision_tree_module()`** - In-race decision tree for common problems
6. **`build_psych_landmarks_module()`** - Mental landmarks (dark patch, field shatters, relief)

**Helper Function:**
- `_html_escape()` - Safe HTML escaping that tolerates None values

**Wiring Code:**
Added after all existing template.replace() calls:
```python
race_specific = race_data.get("race_specific") or {}
output = output.replace("{{FLINT_MODULE}}", build_flint_module(race_specific))
output = output.replace("{{TIRE_PRESSURE_MODULE}}", build_tire_pressure_module(race_specific))
output = output.replace("{{WIND_MODULE}}", build_wind_module(race_specific))
output = output.replace("{{TIME_DRIFT_MODULE}}", build_time_drift_module(race_specific))
output = output.replace("{{DECISION_TREE_MODULE}}", build_decision_tree_module(race_specific))
output = output.replace("{{PSYCH_LANDMARKS_MODULE}}", build_psych_landmarks_module(race_specific))
```

### 2. Template Tokens (guide_template_full.html)

**Section 10 - Race Tactics:**
- `{{DECISION_TREE_MODULE}}` - Before "The bottom line on tactics"
- `{{PSYCH_LANDMARKS_MODULE}}` - Before "The bottom line on tactics"

**Section 11 - Race-Specific Preparation:**
- `{{FLINT_MODULE}}` - After intro paragraph, before "Non-Negotiables"
- `{{TIRE_PRESSURE_MODULE}}` - After Non-Negotiables table
- `{{WIND_MODULE}}` - After Non-Negotiables table
- `{{TIME_DRIFT_MODULE}}` - After Weather Strategy paragraph

---

## 📋 JSON Structure Required

To activate these modules, add a `race_specific` object to your race JSON:

```json
{
  "race_specific": {
    "surface": {
      "terrain_type": "flint_rock",
      "description": "The Flint Hills contain sharp, angular rocks that can cause flats...",
      "hazard_sectors": [
        {
          "name": "Sector 1",
          "mile_marker": "15-25",
          "risk_level": "high",
          "tactics": "Drop pressure 2-3 PSI, avoid crown"
        }
      ]
    },
    "mechanicals": {
      "recommended_tires": ["Vittoria Terreno Dry", "Schwalbe G-One RS"],
      "pressure_by_weight": {
        "150_lbs": {
          "dry": "28-32 PSI",
          "mixed": "26-30 PSI",
          "mud": "24-28 PSI"
        },
        "180_lbs": {
          "dry": "32-36 PSI",
          "mixed": "30-34 PSI",
          "mud": "28-32 PSI"
        }
      }
    },
    "wind_protocol": {
      "prevailing_direction": "Southwest, 15-25 mph sustained",
      "when_it_matters": "Miles 50-120 are exposed with no shelter...",
      "group_tactics": "Form echelons, rotate every 30 seconds...",
      "solo_tactics": "Stay aero, lower power targets 5-10%..."
    },
    "environment": {
      "time_drift": {
        "note": "Unbound typically runs 1-2 hours longer than best-case estimates.",
        "neutral": "+1 hour",
        "mild_mud": "+1.5 hours",
        "heavy_mud": "+2.5 hours"
      }
    },
    "in_race_decision_tree": {
      "flat_tire": [
        "Stop immediately, assess damage",
        "If sidewall cut: use boot + tube",
        "If small puncture: use plug",
        "Check tire pressure after repair"
      ],
      "dropped_from_group": [
        "Don't panic",
        "Assess: Can you bridge?",
        "If yes: 2-3 min hard effort",
        "If no: Settle into sustainable pace"
      ],
      "bonking": [
        "Immediate: 2 gels + water",
        "Reduce power 20% for 10 min",
        "Focus on fueling every 15 min",
        "Don't try to make up lost time"
      ],
      "cramping": [
        "Reduce intensity immediately",
        "Take electrolyte tab",
        "Stretch on bike if possible",
        "Accept slower pace for 20-30 min"
      ]
    },
    "psychological_landmarks": {
      "dark_patch": {
        "miles": "80-100",
        "description": "This is where the novelty wears off and the reality sets in..."
      },
      "where_field_shatters": {
        "miles": "120-140",
        "description": "The field will split here. Don't chase every move..."
      },
      "late_relief": {
        "miles": "160-180",
        "description": "If you've paced correctly, you'll start feeling better here..."
      }
    }
  }
}
```

---

## 🎯 Behavior

- **Graceful Degradation:** If `race_specific` is missing or incomplete, modules return empty strings (no errors, no broken HTML)
- **Self-Contained:** Each function is ~30-50 lines, no external dependencies
- **CSS Ready:** Uses existing `.gg-*` classes from the template
- **HTML Safe:** All user input is escaped via `_html_escape()`

---

## 🧪 Testing

To test:

1. Add `race_specific` data to a race JSON file (e.g., `unbound_gravel_200.json`)
2. Generate a guide: `python3 generate_race_plans.py unbound_gravel_200.json`
3. Open the generated guide HTML
4. Check Sections 10 and 11 for the modules

**Expected Result:**
- If data exists: Modules appear with formatted content
- If data missing: Modules are absent (no placeholders, no errors)

---

## 📝 Files Modified

1. **`races/generation_modules/guide_generator.py`**
   - Added `import html`
   - Added `_html_escape()` helper
   - Added 6 builder functions (~300 lines)
   - Added wiring code (6 lines)

2. **`races/generation_modules/guide_template_full.html`**
   - Added 6 tokens in Sections 10 and 11

---

## ✅ Status

**Implementation:** Complete  
**Testing:** Ready (requires race JSON with `race_specific` data)  
**Documentation:** This file

---

## 🔄 Next Steps

1. Add `race_specific` data to existing race JSON files
2. Regenerate guides to see modules in action
3. Adjust module content/styling as needed
4. Scale to all 140+ races

---

**All code committed to GitHub.**

