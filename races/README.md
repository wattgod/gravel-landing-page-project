# Race Plan Generation System

## Overview

This system generates all 15 training plan variants for any race, producing:
- **84 ZWO workout files** (per plan)
- **35-page training plan guide** (PDF per plan)
- **Marketplace description** (HTML per plan)

## Structure

```
races/
├── race_schema_template.json    # Template for creating new race JSON
├── unbound_gravel_200.json      # Example race data
├── generate_race_plans.py       # Main generator script
└── [Race Name]/
    ├── race_data.json           # Race-specific data (saved copy)
    ├── 1. Ayahuasca Beginner (12 weeks)/
    │   ├── training_plan_guide.pdf
    │   ├── marketplace_description.html
    │   └── workouts/
    │       ├── W01_Mon_Rest.zwo
    │       ├── W01_Tue_HIIT_Introduction.zwo
    │       └── ... (84 total)
    ├── 2. Ayahuasca Intermediate (12 weeks)/
    │   └── ...
    └── ... (15 total plan folders)
```

## Usage

### 1. Create Race JSON

Copy `race_schema_template.json` and populate with race-specific data:

```bash
cp race_schema_template.json my_race.json
# Edit my_race.json with race details
```

### 2. Generate All Plans

```bash
python generate_race_plans.py my_race.json
```

This will:
- Create folder structure for the race
- Generate all 15 plan variants
- Output: 1,260 ZWO files (15 × 84) + 15 guides + 15 marketplace descriptions

### 3. Review & Upload

- Review outputs in `[Race Name]/` folder
- Upload ZWO files to TrainingPeaks
- Upload guides and descriptions to marketplace

## Race JSON Schema

See `race_schema_template.json` for complete structure. Key sections:

- **race_metadata**: Name, distance, elevation, date, location
- **race_characteristics**: Climate, altitude, terrain, technical difficulty
- **race_hooks**: Marketing copy for marketplace
- **non_negotiables**: 3 race-specific challenges
- **masterclass_topics**: Guide topics ordered by race relevance
- **workout_modifications**: Heat training, dress rehearsal, fueling, etc.
- **guide_variables**: Variables for 35-page guide
- **marketplace_variables**: Variables for HTML description
- **tier_overrides**: Tier-specific adjustments (dress rehearsal hours, etc.)

## Plan Mapping

The system automatically maps to 15 plan variants:

1. Ayahuasca Beginner (12 weeks)
2. Ayahuasca Intermediate (12 weeks)
3. Ayahuasca Masters (12 weeks)
4. Ayahuasca Save My Race (6 weeks)
5. Finisher Beginner (12 weeks)
6. Finisher Intermediate (12 weeks)
7. Finisher Advanced (12 weeks)
8. Finisher Masters (12 weeks)
9. Finisher Save My Race (6 weeks)
10. Compete Intermediate (12 weeks)
11. Compete Advanced (12 weeks)
12. Compete Masters (12 weeks)
13. Compete Save My Race (6 weeks)
14. Podium Advanced (12 weeks)
15. Podium Advanced GOAT (12 weeks)

## Automation Features

- **Editable**: Modify `race_data.json` → regenerate all 15 plans
- **Consistent**: Same structure across all races
- **Scalable**: Add new race → generate all 15 automatically
- **Versioned**: Integrates with existing versioning system

## Next Steps

1. ✅ Schema created
2. ✅ Folder structure template created
3. ✅ Generator script skeleton created
4. ⏳ Implement ZWO generation
5. ⏳ Implement guide generation
6. ⏳ Implement marketplace HTML generation
7. ⏳ Test with Unbound 200

