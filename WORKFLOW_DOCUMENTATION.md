# Gravel God Training Plan Generation System - Complete Workflow

## System Overview

This system generates complete, race-specific training plans from a single race JSON file. It produces:
- **1,211 ZWO workout files** (varies by plan complexity)
- **15 marketplace HTML descriptions** (with randomized copy variations)
- **15 training plan guides** (placeholder for Google Docs integration)

All outputs are organized in a logical folder structure, ready for TrainingPeaks upload.

---

## Architecture

```
Race JSON (Single Source of Truth)
    ↓
generate_race_plans.py (Orchestrator)
    ↓
    ├──→ zwo_generator.py (Workout files)
    ├──→ marketplace_generator.py (HTML descriptions)
    └──→ guide_generator.py (Training guides - placeholder)
```

---

## File Structure

```
current/
├── races/
│   ├── generation_modules/
│   │   ├── zwo_generator.py          # Generates ZWO workout files
│   │   ├── marketplace_generator.py  # Generates marketplace HTML
│   │   ├── guide_generator.py        # Placeholder for guide generation
│   │   └── gravel_god_copy_variations.py  # Copy variation library
│   ├── generate_race_plans.py        # Main orchestrator script
│   ├── race_schema_template.json     # Schema for race JSON files
│   ├── unbound_gravel_200.json       # Example race data
│   └── [Race Name]/                  # Generated output folder
│       ├── race_data.json            # Copy of race JSON
│       └── [15 Plan Folders]/
│           ├── workouts/             # 84-168 ZWO files
│           ├── marketplace_description.html
│           └── training_plan_guide.pdf (placeholder)
│
└── plans/                            # Plan templates
    └── [15 Plan Templates]/
        └── template.json             # Plan structure and workouts
```

---

## Step-by-Step Workflow

### Step 1: Create Race JSON File

Create a JSON file following the `race_schema_template.json` structure:

```json
{
  "race_metadata": {
    "name": "Unbound Gravel 200",
    "distance_miles": 200,
    "elevation_feet": 11000,
    "date": "June",
    "location": "Emporia, KS"
  },
  "race_characteristics": {
    "climate": "hot",
    "altitude_feet": 1200,
    "terrain": "flint_hills",
    "technical_difficulty": "moderate"
  },
  "race_hooks": {
    "punchy": "200 miles across the Flint Hills. 11,000 feet of climbing. June heat that breaks people.",
    "detail": "Unbound isn't a race you survive by accident. It's a race you prepare for—or it prepares you for a very long day."
  },
  "non_negotiables": [
    "Heat adaptation protocol built into weeks 6-10",
    "Flint-specific cornering and line selection skills",
    "9-hour dress rehearsal in week 9"
  ],
  "masterclass_topics": {
    "priority_order": ["heat", "fueling", "tactics", "mental", "workout_execution", "recovery_tires_strength"],
    "race_specific": true
  },
  "workout_modifications": {
    "heat_training_enabled": true,
    "heat_training_weeks": [2, 3, 4, 5, 6, 7, 8, 9, 10],
    "aggressive_fueling_enabled": true,
    "dress_rehearsal_enabled": true,
    "dress_rehearsal_week": 9,
    "robust_taper_enabled": true,
    "robust_taper_weeks": [11, 12],
    "gravel_grit_enabled": true,
    "gravel_grit_weeks": [12]
  },
  "guide_variables": {
    "DISTANCE": "200",
    "DARK_MILE": "150"
  },
  "marketplace_variables": {
    "DISTANCE": "200",
    "DARK_MILE": "150"
  },
  "tier_overrides": {
    "finisher": {
      "dress_rehearsal_hours": 7
    },
    "compete": {
      "dress_rehearsal_hours": 9
    },
    "podium": {
      "dress_rehearsal_hours": 9
    }
  }
}
```

Save this file as `races/[race_name].json` (e.g., `races/unbound_gravel_200.json`)

---

### Step 2: Run Generation Script

```bash
cd ~/Documents/"Gravel Landing Page Project/current/races"
python3 generate_race_plans.py unbound_gravel_200.json
```

**What happens:**
1. Script loads race JSON
2. Creates folder structure: `races/[Race Name]/[15 Plan Folders]/`
3. For each of 15 plans:
   - Loads plan template JSON
   - Generates 84-168 ZWO workout files (varies by plan)
   - Generates marketplace HTML description (with varied copy)
   - Generates training guide placeholder
4. Saves all outputs to organized folders

---

### Step 3: Output Structure

For each race, you get:

```
races/[Race Name]/
├── race_data.json                    # Copy of input JSON
│
├── 1. Ayahuasca Beginner (12 weeks)/
│   ├── workouts/
│   │   ├── W01_Mon_-_Rest.zwo
│   │   ├── W01_Tue_-_HIIT_Introduction.zwo
│   │   └── ... (84 total)
│   ├── marketplace_description.html
│   └── training_plan_guide.pdf
│
├── 2. Ayahuasca Intermediate (12 weeks)/
│   └── ... (same structure)
│
└── ... (15 total plan folders)
```

---

## Key Features & Modifications

### 1. Copy Variations (Marketplace Descriptions)

**File:** `generation_modules/gravel_god_copy_variations.py`

**Purpose:** Prevents duplicate marketplace descriptions by randomizing copy blocks.

**How it works:**
- Each plan variant gets unique copy from 30+ variations
- Headlines, body text, topic descriptions all randomized
- Non-negotiables rephrased with variety
- Tier/level descriptions varied

**Usage:** Automatically called by `marketplace_generator.py` - no manual intervention needed.

---

### 2. Position Alternation (Workout Descriptions)

**File:** `generation_modules/zwo_generator.py` → `add_position_alternation_note()`

**Purpose:** Adds guidance about alternating drops/hoods position on endurance and long rides.

**Applies to:**
- Endurance rides (Z2, Easy, Recovery, Aerobic)
- Long rides (Saturday long rides, extended rides)
- Rides 60+ minutes

**Does NOT apply to:**
- Quality sessions (Threshold, VO2max, G-Spot, HIIT)
- Rest days
- Short rides (<60 minutes)

**Output example:**
```
• POSITION ALTERNATION:
While racing you get as aero as possible (drops), but in training people often try to produce maximum power (hoods, out of saddle). These aren't the same thing. Alternate position every 30 minutes: 30 min in the drops (aero, race position) → 30 min in the hoods (power production, comfort). This builds both aero efficiency and power production. For 120-minute rides, aim for 2 position changes.
```

---

### 3. Race-Specific Modifications

**Heat Training:**
- Automatically added to quality sessions in specified weeks
- Three tiers (Better Than Nothing, Good, Ideal)
- Protocol details in workout description

**Aggressive Fueling:**
- Added to all long rides when enabled
- Targets 60-90g carbs/hour
- Race-specific messaging

**Dress Rehearsal:**
- Replaces Saturday long ride in specified week
- Duration based on tier (7-9 hours)
- Full race simulation guidance

**Robust Taper:**
- Added to taper weeks
- Emphasizes freshness over volume

**Gravel Grit:**
- Mental preparation notes
- Added to race week workouts

---

### 4. Workout Description Enhancements

All workouts automatically receive:

1. **G-Spot Replacement:** "Sweet Spot" → "G-Spot (87-92% FTP)"
2. **Cadence Work:** High/low cadence variations based on plan modifications
3. **Rhythm/Loaded Intervals:** Notes for alternating zone/cadence patterns
4. **Strength Training Notes:** When enabled in plan
5. **Monday Week Preview:** Week overview on Monday rest days
6. **Rest Day TSS Limits:** Guidance on rest day riding
7. **Race-Specific Notes:** Heat, fueling, dress rehearsal, taper, grit

---

## Plan Templates Structure

Each plan template (`plans/[Plan Name]/template.json`) contains:

```json
{
  "plan_metadata": {
    "name": "Finisher Intermediate",
    "tier": "finisher",
    "level": "intermediate",
    "duration_weeks": 12,
    "philosophy": "Polarized (80/20)",
    "target_hours": "8-12",
    "goal": "Solid finish with confidence"
  },
  "default_modifications": {
    "cadence_work": {
      "enabled": true,
      "weeks": ["all"]
    },
    "rhythm_intervals": {
      "enabled": true,
      "weeks": ["week_8", "week_9", "week_10"]
    },
    "g_spot_replacement": true,
    "strength_training": {
      "enabled": false,
      "note": "Perform your own strength training program..."
    },
    "monday_week_preview": {
      "enabled": true
    },
    "rest_day_tss_limit": 30,
    "rest_day_duration_limit_hours": 1
  },
  "weeks": [
    {
      "week_number": 1,
      "focus": "Base building",
      "volume_hours": 8,
      "workouts": [
        {
          "name": "W01 Mon - Rest",
          "description": "Rest day...",
          "blocks": "<FreeRide Duration=\"3600\"/>"
        },
        // ... more workouts
      ]
    }
    // ... 12 weeks
  ]
}
```

---

## ZWO File Format

Generated ZWO files follow TrainingPeaks XML format:

```xml
<?xml version='1.0' encoding='UTF-8'?>
<workout_file>
  <author>Gravel God Training</author>
  <name>W01 Tue - HIIT Introduction</name>
  <description>• STRUCTURE:
10 min easy warmup → 6x30sec HARD / 2 min easy recovery → 10 min easy cooldown

• First HIIT session...

• POSITION ALTERNATION:
[If applicable]

• UNBOUND GRAVEL 200 - HYDRATION:
[Race-specific notes]
</description>
  <sportType>bike</sportType>
      <workout>
    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="6" OnDuration="30" OnPower="1.50" Cadence="100" OffDuration="120" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
  </workout>
</workout_file>
```

---

## Marketplace Description Format

Generated HTML follows neo-brutalist styling with:
- Brand colors (#59473C, #40E0D0, #F5F5DC)
- Varied headlines and body copy
- Masterclass topics (race-specific)
- Non-negotiables (rephrased with variety)
- Tier/level descriptions (varied)
- Character limit: <4000 chars

---

## Workflow Summary

1. **Create Race JSON** → Follow `race_schema_template.json`
2. **Run Generator** → `python3 generate_race_plans.py [race].json`
3. **Output** → `races/[Race Name]/[15 Plan Folders]/`
4. **Upload** → ZWO files to TrainingPeaks, HTML to marketplace

---

## Key Functions Reference

### `zwo_generator.py`

- `generate_all_zwo_files()` - Main function, generates all workouts
- `enhance_workout_description()` - Adds all modifications to descriptions
- `add_position_alternation_note()` - Adds drops/hoods guidance
- `add_heat_training_note()` - Adds heat protocol notes
- `add_hydration_note()` - Adds hydration guidance
- `add_aggressive_fueling_note()` - Adds fueling strategy
- `add_dress_rehearsal_note()` - Adds dress rehearsal guidance
- `add_robust_taper_note()` - Adds taper guidance
- `add_gravel_grit_note()` - Adds mental prep notes

### `marketplace_generator.py`

- `generate_marketplace_html()` - Main function, generates HTML
- `get_masterclass_topics_html()` - Builds masterclass section
- Uses `gravel_god_copy_variations.py` for varied copy

### `gravel_god_copy_variations.py`

- `generate_varied_marketplace_copy()` - Returns dict of varied copy blocks
- `get_variation()` - Gets single variation by category
- `get_non_negotiable_phrasing()` - Rephrases non-negotiables

---

## Important Notes

1. **Encoding:** All Unicode characters (✓, →, •) use constants from `gravel_god_copy_variations.py` to prevent encoding issues

2. **Formatting:**
   - Headers in ALL CAPS
   - Bullets (•) not stars (★)
   - Race names in ALL CAPS in headers

3. **Character Limits:**
   - Marketplace HTML: <4000 characters
   - ZWO descriptions: No hard limit, but kept reasonable

4. **Plan Variations:**
   - Some plans have block options (e.g., Compete Advanced: VO2max, Threshold, Durability, Neuromuscular)
   - These generate more workouts (168 vs 84)
   - Handled automatically by `zwo_generator.py`

---

## Testing

To verify generation worked:

```bash
cd races/[Race Name]/[Plan Folder]
ls workouts/*.zwo | wc -l  # Should be 84 (or 42 for 6-week plans, 168 for Compete Advanced)
cat marketplace_description.html | wc -c  # Should be <4000
grep "POSITION ALTERNATION" workouts/*.zwo | wc -l  # Count endurance/long rides
```

---

## Dependencies

- Python 3.7+
- Standard library only (json, os, re, html, pathlib)
- No external packages required

---

## Future Enhancements

1. **Guide Generator v2:** Integrate Google Docs API for automatic guide creation
2. **More Copy Variations:** Expand variation library
3. **Workout Block Variations:** More complex interval patterns
4. **Batch Processing:** Generate multiple races at once

---

*Last updated: November 2024*
*System version: 1.0*

