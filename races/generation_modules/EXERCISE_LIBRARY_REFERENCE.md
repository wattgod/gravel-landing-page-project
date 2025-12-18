# Exercise Video Library Reference

## Overview

**Total Exercises:** 404  
**Sources:**
- Precision Nutrition: 391 exercises (Vimeo)
- YouTube Fallbacks: 13 exercises

---

## Category Breakdown

| Category | Count | Description |
|----------|-------|-------------|
| **Squat** | 90 | Squat variations, lunges, split squats |
| **Push** | 79 | Push-ups, bench press, overhead press |
| **Pull** | 55 | Rows, pull-ups, face pulls |
| **Hinge** | 20 | Deadlifts, RDLs, swings, good mornings |
| **Core** | 20 | Planks, dead bugs, pallof press, rotations |
| **Carry** | 9 | Farmer carry, suitcase carry |
| **Glute** | 10 | Bridges, hip thrusts, activation |
| **Plyometric** | 8 | Jumps, explosive movements |
| **Mobility** | 16 | Stretches, mobilizations |
| **Other** | 97 | Accessory, corrective, metabolic |

---

## Equipment Requirements

| Equipment | Count | Exercises |
|-----------|-------|-----------|
| Bodyweight | 150+ | Most exercises can be done bodyweight-only |
| Dumbbell | 80+ | DB variations of major movements |
| Kettlebell | 20+ | KB swings, goblet squats, carries |
| Barbell | 40+ | Heavy compound lifts |
| Band | 60+ | Resistance band exercises |
| TRX | 10+ | Suspension training |
| Box | 15+ | Box jumps, step-ups |
| Bench | 20+ | Bench press variations |

---

## Difficulty Levels

| Level | Count | Description |
|-------|-------|-------------|
| Beginner | ~80 | Assisted, partial range, bodyweight basics |
| Intermediate | ~200 | Loaded movements, full range |
| Advanced | ~120 | Single-leg, explosive, complex movements |

---

## Common Exercise Patterns

### Squat Pattern
- Bodyweight Squat
- Goblet Squat
- Front Squat
- Back Squat
- Split Squat
- Bulgarian Split Squat
- Single-Leg Squat

### Hinge Pattern
- Deadlift
- Romanian Deadlift (RDL)
- Single-Leg RDL
- Good Morning
- Kettlebell Swing

### Push Pattern
- Push-Up (various angles)
- Bench Press
- Overhead Press
- Floor Press

### Pull Pattern
- Inverted Row
- Bent-Over Row
- Pull-Up/Chin-Up
- Face Pull

### Core Pattern
- Plank (various)
- Dead Bug
- Side Plank
- Pallof Press
- Bird Dog

### Carry Pattern
- Farmer Carry
- Suitcase Carry
- Overhead Carry

---

## Usage

### Python API

```python
from exercise_lookup import get_video_url, get_exercises_by_category

# Get video URL for an exercise
url = get_video_url("Push-Up")
# Returns: https://vimeo.com/111473394

# Get all exercises in a category
squats = get_exercises_by_category("squat")
# Returns: List of exercise dictionaries

# Search exercises
results = search_exercises("push", limit=10)
```

### Validation

```python
from exercise_lookup import validate_exercise_urls

exercises = ["Push-Up", "Deadlift", "Squat"]
results = validate_exercise_urls(exercises)
print(f"Coverage: {results['coverage']*100}%")
```

---

## Files

- **Library JSON:** `exercise_video_library.json`
- **Lookup Module:** `exercise_lookup.py`
- **Validation Script:** `validate_template_exercises.py`

---

## Notes

- All URLs are verified and working
- YouTube fallbacks are for exercises not in PN library
- Fuzzy matching handles common name variations
- Library is automatically loaded when module is imported

