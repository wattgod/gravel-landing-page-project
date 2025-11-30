# Race JSON to Guide Generator Mapping

This document shows how the existing race JSON structure maps to guide generator needs, avoiding data duplication.

## Current Race JSON Structure

### 1. `race_metadata` - Core Race Info
```json
{
  "name": "Unbound Gravel 200",
  "full_name": "Unbound Gravel 200",
  "distance_miles": 200,
  "elevation_feet": 11000,
  "date": "June",
  "location": "Emporia, Kansas",
  "start_elevation_feet": 1200,
  "max_elevation_feet": 1500,
  "avg_elevation_feet": 1200
}
```

**Guide Generator Mapping:**
- `name` → Guide title, headers
- `full_name` → Full race name in guide
- `distance_miles` → Fueling strategy, distance references
- `elevation_feet` → Climbing section, difficulty assessment
- `date` → Race timing context
- `location` → Race location in guide
- `start/max/avg_elevation_feet` → Altitude section (if needed)

---

### 2. `race_characteristics` - Race Conditions
```json
{
  "climate": "hot",
  "altitude_feet": 1200,
  "altitude_category": "low",
  "terrain": "flint_hills",
  "technical_difficulty": "moderate",
  "typical_weather": "Hot and humid, 85-95°F",
  "race_type": "ultra_distance"
}
```

**Guide Generator Mapping:**
- `climate` → Heat training section, hydration protocols
- `altitude_feet` → Altitude section (if >5000 ft)
- `altitude_category` → Altitude strategy selection
- `terrain` → Technical skills section, equipment recommendations
- `technical_difficulty` → Difficulty assessment, skills emphasis
- `typical_weather` → Weather preparation, clothing recommendations
- `race_type` → Training approach context

---

### 3. `race_hooks` - Marketing/Engagement
```json
{
  "punchy": "200 miles across the Flint Hills. 11,000 feet of climbing. June heat that breaks people.",
  "detail": "Unbound isn't a race you survive by accident. It's a race you prepare for—or it prepares you for a very long day.",
  "dark_mile": 150
}
```

**Guide Generator Mapping:**
- `punchy` → Guide introduction, opening hook
- `detail` → Race context section
- `dark_mile` → Mental training section, pacing strategy

---

### 4. `non_negotiables` - Critical Requirements
```json
[
  "Heat adaptation protocol built into weeks 6-10",
  "Flint-specific cornering and line selection skills",
  "9-hour dress rehearsal in week 9"
]
```

**Guide Generator Mapping:**
- Array of strings → "Non-Negotiables" callout box in guide
- Each item becomes a bullet point
- Used in both guide and marketplace description

---

### 5. `masterclass_topics` - Guide Content Structure
```json
{
  "priority_order": ["heat", "fueling", "tactics", "mental", "execution", "recovery"],
  "race_specific": true,
  "topics": {
    "heat": "The protocol that works—when to start, how to adapt",
    "fueling": "Calories, hydration, timing for 200+ miles",
    "tactics": "When to sit in, when to push, when to survive",
    "mental": "What to do when mile 150 hurts",
    "execution": "Why most athletes fail intervals",
    "recovery": "The honest takes"
  }
}
```

**Guide Generator Mapping:**
- `priority_order` → Section order in guide
- `race_specific` → Flag for custom vs generic content
- `topics` → Section descriptions/headings
- Each topic key maps to a guide section:
  - `heat` → Heat Training section
  - `fueling` → Fueling & Hydration section
  - `tactics` → Race Tactics section
  - `mental` → Mental Training section
  - `execution` → Workout Execution section
  - `recovery` → Recovery section

---

### 6. `workout_modifications` - Training Adjustments
```json
{
  "heat_training": {
    "enabled": true,
    "tier_3_weeks": [6, 7, 8, 9, 10],
    "tier_2_weeks": [4, 5],
    "tier_1_weeks": [11, 12]
  },
  "dress_rehearsal": {
    "enabled": true,
    "week": 9,
    "day": "Saturday",
    "duration_hours": {
      "ayahuasca": 5,
      "finisher": 7,
      "compete": 9,
      "podium": 10
    }
  },
  "aggressive_fueling": {
    "enabled": true,
    "target_carbs_per_hour": 60,
    "long_ride_min_hours": 3
  },
  "robust_taper": {
    "enabled": true,
    "weeks": [11, 12]
  },
  "gravel_grit": {
    "enabled": true,
    "week": 12
  }
}
```

**Guide Generator Mapping:**
- `heat_training` → Heat Training section details, protocol tiers
- `dress_rehearsal` → Dress Rehearsal section, tier-specific durations
- `aggressive_fueling` → Fueling section, carb targets
- `robust_taper` → Taper section, week references
- `gravel_grit` → Mental Training section, week reference

---

### 7. `guide_variables` - Pre-formatted Guide Text
```json
{
  "race_name": "Unbound Gravel 200",
  "race_distance": "200 miles",
  "race_elevation": "11,000 feet",
  "race_date": "June",
  "race_location": "Emporia, Kansas",
  "race_terrain": "Flint Hills gravel roads",
  "race_weather": "Hot and humid, typically 85-95°F",
  "race_challenges": [
    "Extreme heat and humidity",
    "Long distance requiring exceptional endurance",
    "Technical gravel sections requiring bike handling skills"
  ],
  "altitude_section": false,
  "altitude_feet": null
}
```

**Guide Generator Mapping:**
- `race_name` → Used throughout guide
- `race_distance` → Formatted for guide text
- `race_elevation` → Formatted for guide text
- `race_date` → Timing context
- `race_location` → Location references
- `race_terrain` → Terrain description
- `race_weather` → Weather section
- `race_challenges` → Key challenges section
- `altitude_section` → Boolean flag for including altitude section
- `altitude_feet` → Altitude value (if applicable)

**Note:** This section is specifically for guide generation - pre-formatted strings ready to drop into guide template.

---

### 8. `marketplace_variables` - Marketplace-Specific
```json
{
  "race_name": "Unbound Gravel 200",
  "race_hook": "200 miles across the Flint Hills...",
  "race_hook_detail": "Unbound isn't a race you survive...",
  "distance": "200",
  "dark_mile": "150",
  "non_negotiable_1": "Heat adaptation protocol...",
  "non_negotiable_2": "Flint-specific cornering...",
  "non_negotiable_3": "9-hour dress rehearsal..."
}
```

**Guide Generator Mapping:**
- Can reuse `race_name`, `distance`, `dark_mile` from here
- `non_negotiable_*` already covered in `non_negotiables` array
- `race_hook`/`race_hook_detail` can be used in guide intro

---

### 9. `tier_overrides` - Tier-Specific Values
```json
{
  "ayahuasca": {
    "dress_rehearsal_hours": 5,
    "weekly_hours": "0-5"
  },
  "finisher": {
    "dress_rehearsal_hours": 7,
    "weekly_hours": "8-12"
  },
  "compete": {
    "dress_rehearsal_hours": 9,
    "weekly_hours": "12-18"
  },
  "podium": {
    "dress_rehearsal_hours": 10,
    "weekly_hours": "18+"
  }
}
```

**Guide Generator Mapping:**
- `dress_rehearsal_hours` → Dress rehearsal section (tier-specific)
- `weekly_hours` → Weekly structure section (tier-specific)
- Used to customize guide content per tier

---

## Complete Mapping Summary

### Guide Sections → Race JSON Fields

| Guide Section | Race JSON Source |
|--------------|------------------|
| **Header/Title** | `race_metadata.name`, `race_metadata.full_name` |
| **Race Introduction** | `race_hooks.punchy`, `race_hooks.detail` |
| **Race Profile** | `race_metadata.*`, `race_characteristics.*` |
| **Distance/Elevation** | `race_metadata.distance_miles`, `race_metadata.elevation_feet` |
| **Location/Date** | `race_metadata.location`, `race_metadata.date` |
| **Weather/Climate** | `race_characteristics.climate`, `race_characteristics.typical_weather` |
| **Terrain** | `race_characteristics.terrain`, `race_characteristics.technical_difficulty` |
| **Non-Negotiables** | `non_negotiables[]` |
| **Heat Training** | `workout_modifications.heat_training`, `race_characteristics.climate` |
| **Fueling** | `workout_modifications.aggressive_fueling`, `race_metadata.distance_miles` |
| **Dress Rehearsal** | `workout_modifications.dress_rehearsal`, `tier_overrides.*.dress_rehearsal_hours` |
| **Taper** | `workout_modifications.robust_taper` |
| **Mental Training** | `race_hooks.dark_mile`, `workout_modifications.gravel_grit` |
| **Altitude** | `race_characteristics.altitude_feet`, `guide_variables.altitude_section` |
| **Masterclass Topics** | `masterclass_topics.priority_order`, `masterclass_topics.topics` |
| **Tier-Specific Content** | `tier_overrides.*` |

---

## Recommended Guide Generator Approach

**Use existing fields directly - no duplication needed:**

1. **Basic Info:** `race_metadata.*`
2. **Conditions:** `race_characteristics.*`
3. **Hooks:** `race_hooks.*`
4. **Non-Negotiables:** `non_negotiables[]`
5. **Masterclass:** `masterclass_topics.*`
6. **Modifications:** `workout_modifications.*`
7. **Tier Overrides:** `tier_overrides.*`
8. **Pre-formatted:** `guide_variables.*` (if you want ready-to-use strings)

**The `guide_variables` section is optional** - you can derive everything from other sections, or use it for pre-formatted strings to save processing.

---

## Example: Guide Generator Function Signature

```python
def generate_guide_html(race_data: dict, tier: str, level: str) -> str:
    """
    Generate guide from race JSON.
    
    Args:
        race_data: Complete race JSON (all sections above)
        tier: "ayahuasca", "finisher", "compete", "podium"
        level: "beginner", "intermediate", "advanced", "masters", "save_my_race"
    """
    
    # Access all data directly from race_data
    metadata = race_data['race_metadata']
    characteristics = race_data['race_characteristics']
    hooks = race_data['race_hooks']
    non_negs = race_data['non_negotiables']
    masterclass = race_data['masterclass_topics']
    modifications = race_data['workout_modifications']
    tier_overrides = race_data['tier_overrides'][tier]
    
    # Optional: use guide_variables for pre-formatted strings
    guide_vars = race_data.get('guide_variables', {})
    
    # Generate guide sections...
```

---

## No Additional Data Needed

The existing race JSON structure contains **everything needed** for guide generation:
- ✅ Race details (distance, elevation, location, date)
- ✅ Conditions (climate, altitude, terrain, weather)
- ✅ Training modifications (heat, fueling, dress rehearsal, taper)
- ✅ Content structure (masterclass topics, non-negotiables)
- ✅ Tier-specific values (dress rehearsal hours, weekly hours)
- ✅ Pre-formatted strings (optional, in `guide_variables`)

**You can generate complete guides using only the existing race JSON structure.**

