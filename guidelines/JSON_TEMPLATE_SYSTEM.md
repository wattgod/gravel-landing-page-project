# JSON Template System for Training Plan Generation

## Overview

This system uses JSON templates to speed up race-specific plan generation. Instead of parsing full plan text each time, we load structured JSON data and apply race-specific modifications.

## File Structure

```
Gravel Landing Page Project/
├── nutrition_hydration_guidelines.json (nutrition/fueling rules)
├── altitude_guidelines.json (altitude considerations)
├── technical_guidelines.json (technical/equipment guidelines)
└── [Plan Number]. [Plan Name]/
    └── template.json (plan structure)
```

## How It Works

### 1. Template JSON Structure

Each plan has a `template.json` with:
- **Plan metadata** (name, duration, philosophy, hours)
- **Weeks array** (each week's focus, volume, workouts)
- **Block options** (if applicable, e.g., Weeks 2-3 in Save My Race)
- **Default modifications** (cadence work, rhythm intervals, etc.)

### 2. Race-Specific Modifications

Race-specific changes are applied as overlays:
- Heat training protocol
- Aggressive fueling targets
- Dress rehearsal duration
- Robust taper adjustments
- Gravel Grit integration

### 3. Nutrition/Hydration Integration

The `nutrition_hydration_guidelines.json` provides:
- On-bike fueling guidelines by duration/intensity
- Daily baseline hydration
- Gut training principles
- Brief, operational workout notes

## Usage with Cursor AI

### Step 1: Load Template

Provide Cursor with:
```
Load the JSON template from: [Plan Number]. [Plan Name]/template.json
```

### Step 2: Provide Race-Specific Considerations

```
Race: [RACE NAME]
Race-Specific Considerations:
1. Heat training needed
2. Aggressive fueling (60-90g carbs/hour)
3. Dress rehearsal: [X]-hour ride Week [Y] Saturday
4. Robust taper in Week [Z]
5. Gravel Grit integration
```

### Step 3: Apply Modifications

Cursor will:
1. Load template JSON
2. Load nutrition_hydration_guidelines.json
3. Apply race-specific modifications
4. Generate modified Python script
5. Generate ZWO files
6. Create modifications document

## Example: Generating Unbound 200 Plan

```python
# Pseudo-code for how the system works:

# 1. Load template
template = load_json("13. Compete Save My Race (6 weeks)/template.json")

# 2. Load guidelines
nutrition = load_json("nutrition_hydration_guidelines.json")

# 3. Apply race-specific overlay
race_modifications = {
    "heat_training": {
        "weeks": [2, 3, 4, 5],
        "tier": "tier3"  # Ideal for load weeks
    },
    "dress_rehearsal": {
        "week": 3,
        "day": "Saturday",
        "duration_hours": 9
    },
    "aggressive_fueling": {
        "target": "60-90g carbs/hour",
        "dress_rehearsal": "up to 100g carbs/hour"
    }
}

# 4. Generate modified plan
modified_plan = apply_modifications(template, race_modifications, nutrition)

# 5. Generate Python script and ZWO files
generate_script(modified_plan)
generate_zwo_files(modified_plan)
```

## Benefits

1. **Faster Generation**: ~60-70% time savings
2. **Consistency**: No missed details
3. **Reusability**: Same template for multiple races
4. **Maintainability**: Update template once, affects all races
5. **Scalability**: Easy to add new races

## Nutrition Guidelines Integration

The nutrition guidelines are automatically applied to workouts based on:
- **Duration**: <60 min, 60-90 min, 90-180 min, 3-6+ hours
- **Intensity**: Easy, endurance/tempo, high intensity
- **Context**: Long rides, dress rehearsal, race day

Brief, operational notes are added to workout descriptions:
- "60-90 min: 20-40g carbs/hr if needed, 500-750ml fluid/hr"
- "3-6+ hours: 70-90g carbs/hr, 600-900ml fluid/hr, aggressive electrolytes"

## Adding New Plans

1. Create plan folder: `[Plan Number]. [Plan Name]/`
2. Convert plan to JSON template (use COMPETE SAVE MY RACE as example)
3. Save as `template.json` in plan folder
4. System is ready to use!

## Future Enhancements

- Altitude guidelines integration
- Technical guidelines integration
- Automated script generation from JSON
- Validation system for plan structure

