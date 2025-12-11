# Gravel God Strength ZWO Creation Skill v1.0

## Generating TrainingPeaks-Compatible Strength Workouts via ZWO Pipeline

**Version:** 1.0  

**Date:** December 2025  

**Purpose:** Systematic generation of strength training workouts using the existing ZWO infrastructure.

---

## CRITICAL DISCOVERY: The Strength Workaround

TrainingPeaks only accepts ZWO files with `sportType="bike"`. However, strength workouts can be deployed by:

1. Setting `sportType="bike"` (required)
2. Using a minimal power stub: `<FreeRide Duration="60" Power="0.0"/>`
3. Putting "Strength" or "STR" in the workout title
4. Writing the full strength session in the description field
5. Including clickable URLs for exercise demonstrations

**This is production-tested and confirmed working.**

---

## CONFIRMED TECHNICAL CAPABILITIES

| Feature | Status | Notes |
|---------|--------|-------|
| URLs | ✓ Clickable | Render as blue, underlined, clickable links |
| Character limit | ✓ 1700+ | No practical limit encountered |
| Unicode symbols | ✓ Full support | ★ • → │ ─ ☐ ☑ all render correctly |
| Line breaks | ✓ Preserved | Multi-line descriptions work |
| Indentation | ✓ Preserved | 2-space indent renders correctly |
| Tables (ASCII) | ✓ Work | Box-drawing characters render |

### What Does NOT Work
- Markdown (`**bold**`, `*italic*`) → shows raw asterisks
- HTML tags (`<b>`, `<br>`) → shows as plain text
- Color codes → not supported

---

## FORMATTING SYSTEM

### Unicode Toolkit

| Symbol | Unicode | Use Case |
|--------|---------|----------|
| ★ | U+2605 | Section headers |
| • | U+2022 | Bullet points (non-superset exercises) |
| → | U+2192 | Links, progressions, flow |
| │ | U+2502 | Metadata separators |
| ─ | U+2500 | Exercise-to-reps separator |
| ☐ | U+2610 | Unchecked box (optional tracking) |
| ☑ | U+2611 | Checked box (optional tracking) |

### Structural Conventions

**Section Headers:**
```
★ SECTION NAME (duration) │ rounds │ rest │ RPE
```

**Non-Superset Exercises (warmup, prep, cooldown):**
```
  • Exercise Name ─ reps or duration
```

**Superset Exercises (main lifts):**
```
  A1 Exercise Name ─ reps
  A2 Exercise Name ─ reps
  → https://video-link
```

**Exercise Notation:**
- `15/side` = 15 reps per side
- `30 sec` = 30 second hold
- `30m` = 30 meters (carries)
- `3x10` = 3 sets of 10 (alternative notation)

---

## TITLE NAMING CONVENTION

### Format
```
W## STR: [Pathway Name] ([Session Letter])
```

### Examples
```
W01 STR: Rebuild Frame (A)      ← Red Pathway, Session A
W01 STR: Rebuild Frame (B)      ← Red Pathway, Session B
W05 STR: Fortify Engine (A)     ← Yellow Pathway, Session A
W09 STR: Sharpen Sword (A)      ← Green Pathway, Session A
```

### Alternative (More Technical)
```
W01 STR - Red A                 ← Week 1, Red Pathway, Session A
W05 STR - Yellow B              ← Week 5, Yellow Pathway, Session B
```

---

## SESSION TEMPLATE STRUCTURE

### Header Block
```
★ STRENGTH: [Pathway] │ Session [A/B] │ Week [#]
  Phase: [Phase Name] │ RPE Target: [#-#]
  Equipment: [list]
  Duration: ~[##] min
```

### Warmup Block
```
★ WARMUP ([#] min)
  • Exercise 1 ─ reps
  • Exercise 2 ─ reps
  • Exercise 3 ─ reps
```

### Prep Block
```
★ PREP ([#] min) │ [#] rounds │ [#]s rest between
  • Exercise 1 ─ reps
  • Exercise 2 ─ reps
```

### Main Lift Blocks
```
★ MAIN 1: [Movement Pattern] │ [#] rounds │ [#]s rest
  A1 Exercise Name ─ reps
  A2 Exercise Name ─ reps
  → https://video-demo-link

★ MAIN 2: [Movement Pattern] │ [#] rounds │ [#]s rest
  B1 Exercise Name ─ reps
  B2 Exercise Name ─ reps
  → https://video-demo-link
```

### Core/Accessory Block
```
★ CORE/ACCESSORY ([#] min) │ [#] rounds │ [#]s rest
  C1 Exercise Name ─ reps
  C2 Exercise Name ─ reps
  C3 Exercise Name ─ reps
```

### Cooldown Block
```
★ COOLDOWN ([#] min)
  • Exercise 1 ─ duration
  • Exercise 2 ─ duration
```

### Notes Block
```
★ NOTES
  [Key coaching cue for this phase]
  [Form reminder or scaling option]
  → Full guide: https://gravelgod.com/strength-[pathway]
```

---

## COMPLETE SESSION EXAMPLE

### Red Pathway - Session A (Anatomical Adaptation)

**Title:** `W01 STR: Rebuild Frame (A)`

**Description:**
```
★ STRENGTH: Red Pathway │ Session A │ Week 1
  Phase: Anatomical Adaptation │ RPE Target: 5-6
  Equipment: Bodyweight, bands, light DB/KB
  Duration: ~40 min

★ WARMUP (10 min)
  • Downward Dog Lunge + Rotation ─ 5/side
  • Tripod Bridge ─ 5/side
  • Curtsy Lunges ─ 10/side
  • Lateral Lunges ─ 10/side

★ PREP (5 min) │ 2 rounds │ 60s rest between
  • Hip Rails ─ 10/side
  • MiniBand Marches ─ 10/side
  • Adductor Eccentrics ─ 15/side

★ MAIN 1: Glute Superset │ 3 rounds │ 90s rest
  A1 Glute Bridge (SL, Banded) ─ 15/side
  A2 TRX Row (or Band Row) ─ 10 reps
  → https://youtu.be/GLUTE_DEMO

★ MAIN 2: Hinge Superset │ 3 rounds │ 90s rest
  B1 Hip Hinge w/ Dowel ─ 12 reps
  B2 Push-Up (Incline if needed) ─ 10 reps
  → https://youtu.be/HINGE_DEMO

★ CORE/CARRY (10 min) │ 2-3 rounds │ 60s rest
  C1 Dead Bug ─ 30 sec
  C2 Side Plank ─ 30 sec/side
  C3 Farmer Carry ─ 30m

★ COOLDOWN (5 min)
  • Deep Squat Sit ─ 45 sec
  • Hip Flexor Stretch ─ 45 sec/side
  • T-Spine Rotation ─ 5/side

★ NOTES
  Quality > load. Every rep clean.
  If form breaks → reduce reps or take longer rest.
  → Full guide: https://gravelgod.com/strength-red
```

**Workout Blocks:**
```xml
    <FreeRide Duration="60" Power="0.0"/>
```

---

## ZWO FILE GENERATION

### Python Function (Extends Existing Generator)

```python
def create_strength_workout(template_path, week, pathway, session, description, output_path):
    """
    Create a strength workout ZWO file
    
    Args:
        template_path: Path to base ZWO template
        week: Week number (1-12)
        pathway: "Red", "Yellow", or "Green"
        session: "A" or "B"
        description: Full formatted strength session
        output_path: Where to save the file
    """
    # Map pathway to name
    pathway_names = {
        "Red": "Rebuild Frame",
        "Yellow": "Fortify Engine",
        "Green": "Sharpen Sword"
    }
    
    name = f"W{week:02d} STR: {pathway_names[pathway]} ({session})"
    
    # Minimal workout block (no actual bike work)
    workout_blocks = '''    <FreeRide Duration="60" Power="0.0"/>
'''
    
    # Use existing create_workout function
    create_workout(
        template_path=template_path,
        name=name,
        description=description,
        workout_blocks=workout_blocks,
        output_path=output_path
    )
```

### Batch Generation Example

```python
# Define strength sessions for 12-week plan
strength_sessions = [
    # Weeks 1-4: Red Pathway (Anatomical Adaptation)
    {"week": 1, "pathway": "Red", "session": "A", "description": RED_SESSION_A},
    {"week": 1, "pathway": "Red", "session": "B", "description": RED_SESSION_B},
    {"week": 2, "pathway": "Red", "session": "A", "description": RED_SESSION_A},
    # ... continues for all weeks
    
    # Weeks 5-8: Yellow Pathway (Hypertrophy/Max Strength)
    {"week": 5, "pathway": "Yellow", "session": "A", "description": YELLOW_SESSION_A},
    # ...
    
    # Weeks 9-12: Green Pathway (Power/Maintenance)
    {"week": 9, "pathway": "Green", "session": "A", "description": GREEN_SESSION_A},
    # ...
]

# Generate all strength workouts
for s in strength_sessions:
    create_strength_workout(
        template_path=TEMPLATE_PATH,
        week=s["week"],
        pathway=s["pathway"],
        session=s["session"],
        description=s["description"],
        output_path=f"/output/W{s['week']:02d}_STR_{s['pathway']}_{s['session']}.zwo"
    )
```

---

## PATHWAY PHASE MAPPING

| Weeks | Pathway | Phase Code | Focus | RPE |
|-------|---------|------------|-------|-----|
| 1-4 | 🟥 Red | AA | Anatomical Adaptation | 5-6 |
| 5-8 | 🟨 Yellow | MT/MS | Hypertrophy/Max Strength | 6-8 |
| 9-11 | 🟩 Green | SM | Power/Conversion | 5-7 |
| 12 | 🟩 Green | Maint | Maintenance/Taper | 5-6 |

**Note:** This is the default progression. Athletes may start on Yellow or Green based on assessment. Tier variations (Ayahuasca vs Podium) may modify frequency, not pathway.

---

## INTEGRATION WITH BIKE TRAINING

### Placement Rules
- Never place strength day before key bike session (VO2max, race simulation)
- Ideal: Strength on easy/rest days or after easy rides
- Minimum 48 hours before high-intensity bike work

### Typical Week Pattern
```
Mon: Rest or STR
Tue: Key Bike Session
Wed: Easy Ride
Thu: STR (if 2x/week)
Fri: Easy Ride
Sat: Key Bike Session (long)
Sun: Easy Ride or Rest
```

### Frequency by Tier

| Tier | Bike Hours | Strength Frequency |
|------|------------|-------------------|
| Ayahuasca | 0-5 hrs | 2x/week (prioritize strength) |
| Finisher | 8-12 hrs | 2x/week |
| Compete | 12-18 hrs | 2x/week (may reduce in Build) |
| Podium | 18+ hrs | 2x base, 1-2x build, 1x peak |

---

## VIDEO URL STRATEGY

### Options
1. **YouTube playlist per pathway** - Single link per session type
2. **Individual exercise links** - More URLs, more specific
3. **Hosted guide page** - One URL to comprehensive page with all demos

### Recommended Approach
- One link per main lift superset (2-3 URLs per session)
- Final link to full pathway guide on gravelgod.com
- Keep URLs short (use youtu.be format or custom shortlinks)

---

## QUALITY CHECKLIST

Before generating strength ZWO files:

☐ Title follows `W## STR: [Pathway Name] ([Session])` format
☐ Description uses ★ for section headers
☐ Main lifts use A1/A2 superset notation
☐ All exercises include reps/duration
☐ Rest periods specified for each block
☐ RPE target stated in header
☐ Equipment list included
☐ At least one video URL per main lift
☐ Notes section includes key coaching cue
☐ Workout block is `<FreeRide Duration="60" Power="0.0"/>`

---

## VERSION HISTORY

**v1.0 (December 2025):**
- Initial skill document
- Confirmed TrainingPeaks workaround (sportType=bike + FreeRide stub)
- Established formatting system (★ • → │ ─)
- Defined A1/A2 superset notation
- Created title naming convention
- Built complete session template
- Documented pathway phase mapping
- Added integration guidelines

---

## NEXT STEPS (Not Yet Defined)

1. **Pathway Exercise Libraries** - Define exact exercises for Red, Yellow, Green
2. **Progression Logic** - How sessions evolve week-to-week within pathway
3. **Assessment Integration** - How athletes self-select into pathways
4. **Tier Modifications** - Volume/frequency adjustments by tier
5. **Video Content** - Create or source exercise demonstration videos

