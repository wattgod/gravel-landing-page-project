# Orchestrator Reference - Complete System Overview

This document provides everything needed to build an orchestrator that integrates with the existing system.

---

## 1. Repository Structure

```
~/Documents/Gravel Landing Page Project/current/
├── .git/
├── .gitignore
├── README.md
├── WORKFLOW_DOCUMENTATION.md
├── GITHUB_PUSH_INSTRUCTIONS.md
│
├── races/
│   ├── generate_race_plans.py          # Main orchestrator (current)
│   ├── race_schema_template.json       # Race JSON schema
│   ├── unbound_gravel_200.json         # Example race data
│   │
│   ├── generation_modules/
│   │   ├── zwo_generator.py            # Generates ZWO workout files
│   │   ├── marketplace_generator.py    # Generates marketplace HTML
│   │   ├── guide_generator.py           # Placeholder for guide generation
│   │   └── gravel_god_copy_variations.py # Copy variation library
│   │
│   └── [Race Name]/                    # Generated outputs (excluded from git)
│       ├── race_data.json
│       └── [15 Plan Folders]/
│           ├── workouts/               # 84-168 ZWO files
│           ├── marketplace_description.html
│           └── training_plan_guide.pdf
│
└── plans/                               # 15 plan templates
    ├── 1. Ayahuasca Beginner (12 weeks)/
    │   └── template.json
    ├── 2. Ayahuasca Intermediate (12 weeks)/
    │   └── template.json
    ├── 3. Ayahuasca Masters (12 weeks)/
    │   └── template.json
    ├── 4. Ayahuasca Save My Race (6 weeks)/
    │   └── template.json
    ├── 5. Finisher Beginner (12 weeks)/
    │   └── template.json
    ├── 6. Finisher Intermediate (12 weeks)/
    │   └── template.json
    ├── 7. Finisher Advanced (12 weeks)/
    │   └── template.json
    ├── 8. Finisher Masters (12 weeks)/
    │   └── template.json
    ├── 9. Finisher Save My Race (6 weeks)/
    │   └── template.json
    ├── 10. Compete Intermediate (12 weeks)/
    │   └── template.json
    ├── 11. Compete Advanced (12 weeks)/
    │   └── template.json
    ├── 12. Compete Masters (12 weeks)/
    │   └── template.json
    ├── 13. Compete Save My Race (6 weeks)/
    │   └── template.json
    ├── 14. Podium Advanced (12 weeks)/
    │   └── template.json
    └── 15. Podium Advanced GOAT (12 weeks)/
        └── template.json
```

---

## 2. Plan Template JSON Structure

### Simple Template (e.g., Ayahuasca Beginner)

```json
{
  "plan_metadata": {
    "name": "AYAHUASCA BEGINNER",
    "duration_weeks": 12,
    "philosophy": "HIIT-Focused (Survival Mode)",
    "target_hours": "0-5",
    "target_athlete": "Complete beginner, severely time-limited...",
    "goal": "Build minimum fitness to survive race day..."
  },
  "weeks": [
    {
      "week_number": 1,
      "focus": "Foundation & Reality Check",
      "volume_percent": 70,
      "volume_hours": "0-3.5",
      "workouts": [
        {
          "name": "W01 Mon - Rest",
          "description": "• Welcome to survival mode training...",
          "blocks": "    <FreeRide Duration=\"60\"/>\n"
        },
        {
          "name": "W01 Tue - HIIT Introduction",
          "description": "• STRUCTURE:\n10 min easy warmup → 6x30sec HARD...",
          "blocks": "    <Warmup Duration=\"600\" PowerLow=\"0.50\" PowerHigh=\"0.70\"/>\n    <IntervalsT Repeat=\"6\" OnDuration=\"30\" OnPower=\"1.50\" Cadence=\"100\" OffDuration=\"120\" OffPower=\"0.55\"/>\n    <Cooldown Duration=\"600\" PowerLow=\"0.70\" PowerHigh=\"0.50\"/>\n"
        }
        // ... 5 more workouts per week
      ]
    }
    // ... 12 weeks total
  ]
}
```

### Complex Template (e.g., Compete Advanced with Block Options)

```json
{
  "plan_metadata": {
    "name": "COMPETE ADVANCED",
    "duration_weeks": 12,
    "philosophy": "Block Periodization",
    "target_hours": "15-18"
  },
  "weeks": [
    {
      "week_number": 1,
      "focus": "Comprehensive Assessment",
      "workouts": [
        // Standard workouts array
      ]
    },
    {
      "week_number": 2,
      "focus": "Block 1 - Concentrated Loading",
      "critical_decision_point": "Based on Week 1 assessment, choose VO2max, Threshold, Durability, or Neuromuscular Block.",
      "workouts_by_block": {
        "VO2max": [
          {
            "name": "W02 Mon - Rest VO2MAX BLOCK",
            "description": "...",
            "blocks": "..."
          },
          // ... more workouts for VO2max block
        ],
        "Threshold": [
          {
            "name": "W02 Mon - Rest THRESHOLD BLOCK",
            "description": "...",
            "blocks": "..."
          },
          // ... more workouts for Threshold block
        ],
        "Durability": [
          // ... workouts for Durability block
        ],
        "Neuromuscular": [
          // ... workouts for Neuromuscular block
        ]
      }
    }
    // ... more weeks
  ]
}
```

**Key Differences:**
- **Simple plans:** Use `workouts` array (7 workouts per week × 12 weeks = 84 workouts)
- **Complex plans:** Use `workouts_by_block` dict (generates multiple variants, e.g., 168 workouts for Compete Advanced)
- **6-week plans:** Same structure but only 6 weeks (42 workouts typically)

---

## 3. ZWO Generator Code

**File:** `races/generation_modules/zwo_generator.py`

**Main Function:**
```python
def generate_all_zwo_files(plan_template, race_data, plan_info, output_dir):
    """
    Generate all ZWO files for a plan.
    
    Args:
        plan_template: Loaded JSON from plans/[Plan Name]/template.json
        race_data: Loaded JSON from races/[race_name].json
        plan_info: Dict with {"tier": "ayahuasca", "level": "beginner", "weeks": 12}
        output_dir: Path to output directory (e.g., races/[Race Name]/[Plan Folder]/)
    
    Returns:
        int: Number of ZWO files generated
    """
```

**Key Functions:**
- `enhance_workout_description()` - Adds race-specific notes to workout descriptions
- `add_position_alternation_note()` - Adds drops/hoods guidance
- `add_heat_training_note()` - Adds heat protocol notes
- `add_hydration_note()` - Adds hydration guidance
- `add_aggressive_fueling_note()` - Adds fueling strategy
- `add_dress_rehearsal_note()` - Adds dress rehearsal guidance
- `add_robust_taper_note()` - Adds taper guidance
- `add_gravel_grit_note()` - Adds mental prep notes
- `create_zwo_file()` - Creates single ZWO file
- `generate_all_zwo_files()` - Main function, processes all weeks/workouts

**Handles:**
- Standard weeks with `workouts` array
- Block-based weeks with `workouts_by_block` dict
- Track-based weeks with `workouts_by_track` dict (for Save My Race plans)

---

## 4. Current Orchestrator

**File:** `races/generate_race_plans.py`

**Structure:**
```python
PLAN_MAPPING = {
    "1. Ayahuasca Beginner (12 weeks)": {"tier": "ayahuasca", "level": "beginner", "weeks": 12},
    "2. Ayahuasca Intermediate (12 weeks)": {"tier": "ayahuasca", "level": "intermediate", "weeks": 12},
    # ... 15 total plans
}

def generate_all_plan_variants(race_data_file):
    """Generates all 15 plan variants for a given race."""
    # 1. Load race data
    # 2. Create folder structure
    # 3. For each plan:
    #    - Load plan template
    #    - Generate ZWO files
    #    - Generate marketplace HTML
    #    - Generate training guide (placeholder)
```

**Usage:**
```bash
python3 races/generate_race_plans.py unbound_gravel_200.json
```

---

## 5. Plan Template Locations

All 15 templates are in `plans/` directory:

1. `plans/1. Ayahuasca Beginner (12 weeks)/template.json`
2. `plans/2. Ayahuasca Intermediate (12 weeks)/template.json`
3. `plans/3. Ayahuasca Masters (12 weeks)/template.json`
4. `plans/4. Ayahuasca Save My Race (6 weeks)/template.json`
5. `plans/5. Finisher Beginner (12 weeks)/template.json`
6. `plans/6. Finisher Intermediate (12 weeks)/template.json`
7. `plans/7. Finisher Advanced (12 weeks)/template.json`
8. `plans/8. Finisher Masters (12 weeks)/template.json`
9. `plans/9. Finisher Save My Race (6 weeks)/template.json`
10. `plans/10. Compete Intermediate (12 weeks)/template.json`
11. `plans/11. Compete Advanced (12 weeks)/template.json` (has block options)
12. `plans/12. Compete Masters (12 weeks)/template.json`
13. `plans/13. Compete Save My Race (6 weeks)/template.json`
14. `plans/14. Podium Advanced (12 weeks)/template.json`
15. `plans/15. Podium Advanced GOAT (12 weeks)/template.json` (has block options)

---

## 6. Integration Points

### To Generate ZWO Files:
```python
from generation_modules.zwo_generator import generate_all_zwo_files

plan_template = load_json("plans/[Plan Name]/template.json")
race_data = load_json("races/[race_name].json")
plan_info = {"tier": "ayahuasca", "level": "beginner", "weeks": 12}

num_files = generate_all_zwo_files(plan_template, race_data, plan_info, output_dir)
```

### To Generate Marketplace HTML:
```python
from generation_modules.marketplace_generator import generate_marketplace_html

html = generate_marketplace_html(race_data, plan_template, plan_info)
```

### To Generate Guide (when implemented):
```python
from generation_modules.guide_generator import generate_training_guide

generate_training_guide(race_data, plan_template, plan_info, output_path)
```

---

## 7. Output Structure

For each race, generates:

```
races/[Race Name]/
├── race_data.json                    # Copy of input race JSON
│
├── 1. Ayahuasca Beginner (12 weeks)/
│   ├── workouts/
│   │   ├── W01_Mon_-_Rest.zwo
│   │   ├── W01_Tue_-_HIIT_Introduction.zwo
│   │   └── ... (84 total for 12-week plans)
│   ├── marketplace_description.html
│   └── training_plan_guide.pdf
│
└── ... (15 plan folders total)
```

**Workout Counts:**
- 12-week plans: 84 workouts (7 per week)
- 6-week plans: 42 workouts (7 per week)
- Compete Advanced: 168 workouts (block options create variants)
- Podium Advanced GOAT: 112 workouts (block options)

---

## 8. Key Data Structures

### Race JSON Structure:
See `races/unbound_gravel_200.json` for complete example.

**Sections:**
- `race_metadata` - Basic race info
- `race_characteristics` - Conditions, terrain, climate
- `race_hooks` - Marketing copy
- `non_negotiables` - Critical requirements
- `masterclass_topics` - Guide content structure
- `workout_modifications` - Training adjustments
- `guide_variables` - Pre-formatted guide text
- `marketplace_variables` - Marketplace-specific
- `tier_overrides` - Tier-specific values

### Plan Template Structure:
**Required:**
- `plan_metadata` - Plan info (name, philosophy, target hours)
- `weeks[]` - Array of week objects

**Week Object:**
- `week_number` - Week number (1-12)
- `focus` - Week focus description
- `workouts[]` OR `workouts_by_block{}` OR `workouts_by_track{}`

**Workout Object:**
- `name` - Workout name (e.g., "W01 Tue - HIIT Introduction")
- `description` - Workout description (markdown-style)
- `blocks` - XML workout blocks (TrainingPeaks format)

---

## 9. File Paths

**Absolute paths:**
```
~/Documents/Gravel Landing Page Project/current/
```

**Relative paths (from current directory):**
- Race JSON: `races/[race_name].json`
- Plan templates: `plans/[Plan Name]/template.json`
- Output: `races/[Race Name]/[Plan Folder]/`
- Generation modules: `races/generation_modules/`

---

## 10. Dependencies

**Python 3.7+** with standard library only:
- `json` - Loading/saving JSON files
- `os` - File operations
- `re` - Regular expressions
- `html` - XML/HTML escaping
- `pathlib` - Path handling

**No external packages required.**

---

*This document provides everything needed to build an orchestrator that integrates with the existing system.*

