# ZWO Generator Architecture Analysis

## Question 4: How is workout data currently structured?

### Answer: **Dict-based with sections array** - Multiple input methods supported

### Primary Structure (batch_workout_generator.py):

```python
workout_data = {
    "workout_name": str,           # Required
    "description": str,             # Required - can be very long (1000+ chars)
    "sections": [                   # Optional - array of workout sections
        {
            "type": str,            # "Warmup" | "Cooldown" | "Intervals" | "Tempo" | "SteadyState"
            "duration": int,        # seconds
            "power_low": float,     # FTP decimal (for Warmup/Cooldown)
            "power_high": float,    # FTP decimal (for Warmup/Cooldown)
            "power": float,         # FTP decimal (for SteadyState)
            "repeats": int,         # For Intervals
            "on_duration": int,     # seconds (for Intervals)
            "off_duration": int,    # seconds (for Intervals)
            "on_power": float,      # FTP decimal (for Intervals)
            "off_power": float,     # FTP decimal (for Intervals)
            "recovery_duration": int,    # Optional (for Tempo)
            "recovery_power": float      # Optional (for Tempo)
        }
    ]
}
```

### Input Methods:

1. **Hardcoded Python Lists** (batch_workout_generator.py):
   ```python
   example_workouts = [
       {
           "workout_name": "High-Intensity Power Blocks",
           "description": "...",
           "sections": [...]
       }
   ]
   generator.batch_generate(example_workouts)
   ```

2. **JSON Files** (process_workout_descriptions function):
   ```python
   # Load from JSON file
   workout_descriptions = json.load(open('workouts.json'))
   generator.batch_generate(workout_descriptions)
   ```

3. **Web API** (app.py):
   ```python
   # Single workout via POST request
   data = request.get_json()
   workout_name = data.get('name')
   description = data.get('description')
   # Generates single file
   ```

### For Strength Workouts - Easy Extension:

**Current structure easily supports strength workouts:**

```python
strength_workout = {
    "workout_name": "Strength - Upper Body Focus",
    "description": "Full strength workout instructions...",
    "sections": [
        {
            "type": "FreeRide",      # NEW TYPE - minimal power block
            "duration": 60,          # 1 minute
            "power": 0.0             # 0% FTP (rest day level)
        }
    ],
    "tags": ["Strength"],            # NEW FIELD - for categorization
    "sportType": "bike"              # Required (workaround)
}
```

**Minimal changes needed:**
- Add "FreeRide" section type handler
- Add optional "tags" field support
- Add optional "sportType" field (defaults to "bike")

---

## Question 5: Is there existing logic for "non-bike" or "rest day" workouts?

### Answer: **NO existing logic** - But easy to add

### Current State:

**No non-bike logic exists:**
- All workouts assume cycling power zones (Z1-Z6)
- All section types are power-based (Warmup, SteadyState, IntervalsT, Cooldown)
- No rest day handling
- No strength workout handling

### Extension Path - Very Easy:

**1. Add FreeRide section type:**
```python
# In generate_workout() method:
elif section["type"] == "FreeRide":
    ET.SubElement(workout_section, "FreeRide",
                Duration=str(section["duration"]),
                Power=str(section.get("power", 0.0)))
```

**2. Add workout type detection:**
```python
def is_strength_workout(workout_data):
    return "Strength" in workout_data.get("workout_name", "") or \
           "Strength" in workout_data.get("tags", [])

def is_rest_day(workout_data):
    return "Rest" in workout_data.get("workout_name", "") or \
           "Rest Day" in workout_data.get("workout_name", "")
```

**3. Add helper functions:**
```python
def create_strength_workout(name, description, tags=None):
    return {
        "workout_name": f"Strength - {name}",
        "description": description,
        "sections": [{
            "type": "FreeRide",
            "duration": 60,
            "power": 0.0
        }],
        "tags": tags or ["Strength"]
    }

def create_rest_day(description):
    return {
        "workout_name": "Rest Day",
        "description": description,
        "sections": [{
            "type": "FreeRide",
            "duration": 60,
            "power": 0.0
        }],
        "tags": ["Rest Day"]
    }
```

**Estimated effort:** 30-60 minutes to add support

---

## Question 6: How does batch generation handle workout sequencing/naming?

### Answer: **Simple iteration - No sequencing logic** - Easy to add

### Current Implementation:

**batch_generate() method:**
```python
def batch_generate(self, workout_descriptions: List[Dict]) -> List[str]:
    """Generate multiple workout files from a list of descriptions."""
    generated_files = []
    for workout_data in workout_descriptions:
        filename = self.generate_workout(workout_data)
        generated_files.append(filename)
    return generated_files
```

**Naming convention:**
```python
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{workout_name.replace(' ', '_')}_{timestamp}.zwo"
```

**Current limitations:**
- No interleaving logic (bike/strength/rest)
- No calendar/schedule structure
- No date-based naming
- No sequencing (just processes list in order)
- Timestamp-based naming (not date-based)

### For Auto-Interleaving Bike/Strength Days:

**Option 1: Schedule Structure (Recommended)**

```python
schedule = [
    {"day": 1, "type": "bike", "workout": "Endurance Ride"},
    {"day": 2, "type": "strength", "workout": "Upper Body"},
    {"day": 3, "bike": "Intervals"},
    {"day": 4, "type": "rest"},
    {"day": 5, "type": "bike", "workout": "Tempo"},
    {"day": 6, "type": "strength", "workout": "Lower Body"},
    {"day": 7, "type": "rest"}
]

def generate_scheduled_workouts(schedule, start_date, workout_templates):
    workouts = []
    for day_info in schedule:
        if day_info["type"] == "bike":
            workout = workout_templates["bike"][day_info["workout"]]
        elif day_info["type"] == "strength":
            workout = create_strength_workout(
                day_info["workout"],
                workout_templates["strength"][day_info["workout"]]
            )
        elif day_info["type"] == "rest":
            workout = create_rest_day(workout_templates["rest"])
        
        # Add date-based naming
        workout_date = start_date + timedelta(days=day_info["day"] - 1)
        workout["date"] = workout_date
        workouts.append(workout)
    
    return generator.batch_generate(workouts)
```

**Option 2: Pattern-Based Interleaving**

```python
def generate_weekly_pattern(pattern, weeks, workout_templates):
    """
    pattern: "BSSRBSS" (B=bike, S=strength, R=rest)
    weeks: number of weeks to generate
    """
    workouts = []
    day_num = 1
    
    for week in range(weeks):
        for day_char in pattern:
            if day_char == "B":
                workout = select_bike_workout(week, day_num, workout_templates)
            elif day_char == "S":
                workout = select_strength_workout(week, day_num, workout_templates)
            elif day_char == "R":
                workout = create_rest_day(workout_templates["rest"])
            
            workout["week"] = week + 1
            workout["day"] = day_num
            workouts.append(workout)
            day_num += 1
    
    return generator.batch_generate(workouts)
```

**Option 3: Date-Based Naming**

```python
def generate_workout(self, workout_data: Dict, date: datetime = None) -> str:
    # ... existing code ...
    
    if date:
        # Date-based naming: W01_Mon_Endurance_Ride.zwo
        week_num = (date - start_date).days // 7 + 1
        day_name = date.strftime("%a")
        filename = f"W{week_num:02d}_{day_name}_{workout_name.replace(' ', '_')}.zwo"
    else:
        # Timestamp-based (current behavior)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{workout_name.replace(' ', '_')}_{timestamp}.zwo"
```

### Estimated Effort:

- **Basic interleaving:** 2-4 hours
- **Schedule structure:** 4-8 hours
- **Date-based naming:** 1-2 hours
- **Full implementation:** 8-12 hours

---

## Summary

### Question 4: Data Structure
- **Answer:** Dict-based with sections array
- **Input:** Python lists, JSON files, or web API
- **Extension:** Very easy - just add new section types and optional fields

### Question 5: Non-Bike/Rest Day Logic
- **Answer:** No existing logic
- **Extension:** Very easy - add FreeRide section type and helper functions
- **Effort:** 30-60 minutes

### Question 6: Batch Sequencing/Naming
- **Answer:** Simple iteration, timestamp-based naming
- **Extension:** Easy - add schedule structure and date-based naming
- **Effort:** 2-12 hours depending on complexity

### Overall Assessment:

**Strength workouts slot in VERY EASILY:**
- ✅ Data structure already supports it (just add FreeRide section type)
- ✅ No major refactoring needed
- ✅ Can use existing batch generation infrastructure
- ✅ Tags and naming conventions work

**Auto-interleaving is straightforward:**
- ✅ Can add schedule structure
- ✅ Can implement pattern-based generation
- ✅ Can add date-based naming
- ✅ All fits within existing architecture

**Recommendation:** Start with adding FreeRide section type and strength/rest helpers (30-60 min), then add scheduling if needed (2-4 hours).

