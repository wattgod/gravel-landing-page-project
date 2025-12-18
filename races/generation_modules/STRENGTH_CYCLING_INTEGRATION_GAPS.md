# Strength-Cycling Integration Gap Analysis

## Executive Summary

**Current State**: Two parallel systems generate ZWO files independently with minimal coordination.

**Key Finding**: Strength and cycling workouts are **not integrated** at the calendar/schedule level. They generate separate files with no coordination on:
- Day placement
- Phase alignment
- Recovery/load management
- Race-specific customization

---

## 1. Phase Alignment

### Cycling Phases

**Location**: `guide_template_full.html` (lines 464-470), `guide_generator.py` (implicit)

**12-Week Plan Phases**:
- **Base Phase**: Weeks 1-3 — Building aerobic foundation
- **Build Phase**: Weeks 4-7 — Adding intensity, race-specific fitness
- **Peak Phase**: Weeks 8-10 — Maximum training load
- **Taper Phase**: Weeks 11-12 — Reducing volume, maintaining intensity

**6-Week Plan Phases**:
- **Assessment**: Week 1
- **Build & Peak**: Weeks 2-4
- **Sharpening**: Week 5
- **Taper**: Week 6

**Code Reference**: `guide_template_full.html:464-470`, `guide_generator.py:718-757`

### Strength Phases

**Location**: `strength_generator.py:52-94` (`STRENGTH_PHASES` dictionary)

**20-Week Plan Phases**:
- **Learn to Lift** (RED): Weeks 1-6 — Anatomical Adaptation, RPE 5-6
- **Lift Heavy Sh*t** (YELLOW): Weeks 7-12 — Hypertrophy/Max Strength, RPE 6-8
- **Lift Fast** (GREEN): Weeks 13-18 — Power/Conversion, RPE 7-9
- **Don't Lose It** (GREEN_MAINT): Weeks 19-20 — Maintenance/Taper, RPE 5-6

**12-Week Plan Mapping** (compressed):
- Weeks 1-3 → YELLOW_HYPER (Lift Heavy Sh*t)
- Weeks 4-6 → YELLOW_MAX (Lift Heavy Sh*t)
- Weeks 7-10 → GREEN_POWER (Lift Fast)
- Weeks 11-12 → GREEN_CONV (Lift Fast)

**Code Reference**: `strength_generator.py:379-402`

### Alignment Analysis

**❌ MISALIGNED**

| Cycling Phase | Weeks | Strength Phase | Weeks | Conflict |
|---------------|-------|----------------|-------|----------|
| Base | 1-3 | Learn to Lift | 1-6 | Strength starts at RED (foundation), cycling starts at Base (aerobic) |
| Build | 4-7 | Learn to Lift (cont.) | 1-6 | Strength still in foundation phase while cycling adds intensity |
| Peak | 8-10 | Lift Heavy Sh*t | 7-12 | Strength peaks during cycling peak (double load) |
| Taper | 11-12 | Lift Heavy Sh*t (cont.) | 7-12 | Strength still heavy during cycling taper |

**12-Week Plan**:
| Cycling Phase | Weeks | Strength Phase | Weeks | Conflict |
|---------------|-------|----------------|-------|----------|
| Base | 1-3 | Lift Heavy Sh*t | 1-3 | Strength starts heavy during cycling base |
| Build | 4-7 | Lift Heavy Sh*t → Lift Fast | 4-10 | Strength transitions during cycling build |
| Peak | 8-10 | Lift Fast | 7-10 | Both peak simultaneously (double load) |
| Taper | 11-12 | Lift Fast | 11-12 | Strength still intense during taper |

**Gap**: No coordination between cycling and strength phase transitions. Strength phases are fixed to calendar weeks, not cycling phases.

---

## 2. Day/Week Assignment

### Cycling Workout Assignment

**Location**: `zwo_generator.py:240-282` (`generate_all_zwo_files`)

**Current Implementation**:
- Workouts are generated from `plan_template["weeks"]` array
- Each week has `workouts` array or `workouts_by_block` dict
- **No explicit day assignment** in template structure
- Filenames don't include day information
- Workouts are generated sequentially, not assigned to specific days

**Code Reference**: `zwo_generator.py:248-280`

**Example Structure** (inferred from code):
```json
{
  "weeks": [
    {
      "week_number": 1,
      "workouts": [
        {"name": "Endurance Ride", "blocks": "...", "description": "..."},
        {"name": "Threshold Intervals", "blocks": "...", "description": "..."}
      ]
    }
  ]
}
```

**Gap**: Cycling workouts have **no day assignment**. They're just a list of workouts per week.

### Strength Workout Assignment

**Location**: `strength_generator.py:96-118` (`STRENGTH_SCHEDULE`)

**Current Implementation**:
- Explicit day assignment: `("Mon", "RED_A_PHASE1")`, `("Thu", "RED_B_PHASE1")`
- Fixed schedule: Monday and Thursday for all weeks (except weeks 19-20 which are Mon only)
- Schedule is hardcoded, not configurable

**Code Reference**: `strength_generator.py:97-118`

**Example**:
```python
STRENGTH_SCHEDULE = {
    1: [("Mon", "RED_A_PHASE1"), ("Thu", "RED_B_PHASE1")],
    2: [("Mon", "RED_A_PHASE1"), ("Thu", "RED_B_PHASE1")],
    # ...
}
```

**Gap**: Strength has fixed Mon/Thu schedule, but cycling has no day assignment. **No coordination** between the two.

### Recovery/Conflict Prevention

**Current State**: ❌ **NO LOGIC EXISTS**

- No check to prevent strength on days before key bike sessions
- No check to prevent strength on recovery days
- No load management between cycling and strength
- No coordination on weekly TSS/stress

**Example Problem**:
- Week 8: Cycling Peak phase (high load)
- Week 8: Strength Lift Heavy Sh*t (high load)
- **Result**: Double peak load, no recovery coordination

**Code Reference**: None found. No conflict prevention logic exists.

---

## 3. Race-Specific Customization

### Cycling Race Customization

**Location**: `unbound_gravel_200.json`, `zwo_generator.py:164-214` (`enhance_workout_description`)

**Current Implementation**:
- Race JSON includes `workout_modifications`:
  - `heat_training`: Weeks 6-10 (tier-based)
  - `dress_rehearsal`: Week 9, tier-specific duration
  - `aggressive_fueling`: Target carbs/hour
  - `robust_taper`: Weeks 11-12
  - `gravel_grit`: Week 12
- Modifications applied to cycling workout descriptions
- Tier-specific adjustments (dress rehearsal duration)

**Code Reference**: `unbound_gravel_200.json:63-109`, `zwo_generator.py:164-214`

**Example**:
```json
{
  "workout_modifications": {
    "heat_training": {
      "enabled": true,
      "tier_3_weeks": [6, 7, 8, 9, 10]
    },
    "dress_rehearsal": {
      "enabled": true,
      "week": 9,
      "duration_hours": {
        "ayahuasca": 5,
        "finisher": 7,
        "compete": 9,
        "podium": 10
      }
    }
  }
}
```

### Strength Race Customization

**Location**: `strength_generator.py` (no race-specific logic found)

**Current Implementation**:
- ❌ **NO RACE-SPECIFIC CUSTOMIZATION**
- Strength templates are identical for all races
- No exercise selection based on race demands
- No phase adjustments based on race characteristics

**Code Reference**: `strength_generator.py:361-447` (`generate_strength_files`)

**Gap**: Strength system doesn't read race JSON or apply race-specific modifications.

### What SHOULD Vary by Race (Not Currently Implemented)

**Unbound 200** (Endurance focus):
- Hip stability exercises for long saddle time
- Core endurance (long holds)
- Shoulder/upper back for aero position
- **Current**: Generic strength program

**Leadville** (Climbing focus):
- Single-leg power exercises
- Altitude considerations (if applicable)
- Explosive power for steep climbs
- **Current**: Generic strength program

**BWR** (Technical/punchy):
- Explosive power for punchy climbs
- Core for technical sections
- Upper body for bike handling
- **Current**: Generic strength program

**Code Reference**: None. Race-specific strength customization doesn't exist.

---

## 4. Tier Variation

### Cycling Tier Variation

**Location**: `generate_race_plans.py:32-48` (`PLAN_MAPPING`), `unbound_gravel_200.json:136-153` (`tier_overrides`)

**Current Implementation**:
- Tier affects plan template selection (15 different plans)
- Tier affects dress rehearsal duration (5-10 hours)
- Tier affects weekly hours (0-5, 8-12, 12-18, 18+)
- Tier affects workout volume/intensity in templates

**Code Reference**: 
- `generate_race_plans.py:32-48`
- `unbound_gravel_200.json:136-153`
- `zwo_generator.py:104-109` (dress rehearsal tier logic)

**Example**:
```python
PLAN_MAPPING = {
    "1. Ayahuasca Beginner (12 weeks)": {"tier": "ayahuasca", "level": "beginner", "weeks": 12},
    "5. Finisher Beginner (12 weeks)": {"tier": "finisher", "level": "beginner", "weeks": 12},
    # ...
}
```

### Strength Tier Variation

**Location**: `strength_generator.py:361-447`

**Current Implementation**:
- ❌ **NO TIER VARIATION**
- Same strength program for all tiers
- Same volume (2x/week) for all tiers
- Same exercises for all tiers
- Only variation: 6-week plans skip strength (too short)

**Code Reference**: `strength_generator.py:376-378` (6-week skip logic)

**Gap**: Strength doesn't adapt to tier. Ayahuasca (0-5 hrs/week) gets same strength as Podium (18+ hrs/week).

### What SHOULD Vary by Tier (Not Currently Implemented)

**Ayahuasca** (0-5 hrs/week cycling):
- Minimal strength (1x/week maintenance)
- Bodyweight focus (time-efficient)
- **Current**: 2x/week, same as everyone

**Finisher** (8-12 hrs/week):
- Standard 2x/week strength
- Mix of bodyweight and weights
- **Current**: ✅ Correct (2x/week)

**Compete** (12-18 hrs/week):
- 2x/week strength, but lighter during peak weeks
- More recovery-focused
- **Current**: 2x/week, no reduction during peak

**Podium** (18+ hrs/week):
- 2x/week strength, but very light during peak
- Maintenance focus, not building
- **Current**: 2x/week, same intensity as everyone

**Code Reference**: None. Tier-based strength variation doesn't exist.

---

## 5. Calendar Integration

### Current Calendar Structure

**Location**: Generated ZWO files in `workouts/` folder

**Current Implementation**:
- Cycling ZWOs: `{workout_name}.zwo` (no day/week in filename)
- Strength ZWOs: `W{week}_STR_{phase}_{session}.zwo` (week in filename)
- **No unified calendar** showing both
- **No day assignment** for cycling workouts
- Athletes must manually organize workouts in TrainingPeaks

**Code Reference**: 
- `zwo_generator.py:261-277` (cycling filenames)
- `strength_generator.py:293` (strength filenames)

**Example Files**:
```
workouts/
  Endurance_Ride.zwo                    # Cycling (no week/day)
  Threshold_Intervals.zwo               # Cycling (no week/day)
  W01_STR_Learn_to_Lift_A.zwo          # Strength (week 1, Mon)
  W01_STR_Learn_to_Lift_B.zwo          # Strength (week 1, Thu)
```

**Gap**: No unified schedule. Athletes don't know:
- "Monday = Strength, Tuesday = VO2max intervals"
- Which cycling workouts pair with which strength days
- Weekly structure/rhythm

### Training Plan Delivery Format

**Location**: `guide_generator.py`, `guide_template_full.html`

**Current Implementation**:
- HTML training guide (35+ pages)
- Mentions cycling phases (Base/Build/Peak/Taper)
- Mentions strength exists but **no detailed schedule**
- No weekly calendar showing both cycling and strength
- No day-by-day breakdown

**Code Reference**: `guide_template_full.html:464-470` (phase overview), `guide_generator.py:932` (strength section)

**Gap**: Guide doesn't show integrated weekly schedule. Athletes must infer from separate ZWO files.

---

## Integration Gaps Summary

### Critical Gaps

1. **❌ No Phase Alignment**
   - Strength phases don't align with cycling phases
   - Double peaks (both systems peak simultaneously)
   - No coordination on taper

2. **❌ No Day Assignment for Cycling**
   - Cycling workouts have no day assignment
   - Strength has fixed Mon/Thu
   - No way to coordinate schedules

3. **❌ No Recovery/Conflict Prevention**
   - No logic to prevent strength before key bike sessions
   - No load management between systems
   - No weekly TSS coordination

4. **❌ No Race-Specific Strength Customization**
   - Same strength program for all races
   - No exercise selection based on race demands
   - No phase adjustments for race characteristics

5. **❌ No Tier Variation for Strength**
   - Same strength volume/intensity for all tiers
   - Ayahuasca gets same program as Podium
   - No reduction during peak weeks for high-volume tiers

6. **❌ No Unified Calendar**
   - No integrated weekly schedule
   - Athletes must manually organize workouts
   - No day-by-day breakdown in guide

### Medium Priority Gaps

7. **⚠️ No Load Management**
   - No TSS tracking across cycling + strength
   - No weekly stress coordination
   - No recovery week coordination

8. **⚠️ No Exercise Selection Logic**
   - Same exercises for all races
   - No race-specific exercise pools
   - No substitution logic based on equipment/limitations

### Low Priority Gaps

9. **ℹ️ Filename Inconsistency**
   - Cycling: `{workout_name}.zwo` (no week/day)
   - Strength: `W{week}_STR_{phase}_{session}.zwo` (week included)
   - Makes organization harder

10. **ℹ️ No Strength in Guide**
    - Guide mentions strength exists
    - No detailed strength schedule in guide
    - No exercise descriptions

---

## Recommendations

### Priority 1: Day Assignment System

**Create unified day assignment**:
- Add day field to cycling workout templates
- Create `WEEKLY_SCHEDULE` structure showing both cycling and strength
- Generate unified calendar view

**Example Structure**:
```python
WEEKLY_SCHEDULE = {
    1: {
        "Mon": {"cycling": "Endurance Ride", "strength": "RED_A_PHASE1"},
        "Tue": {"cycling": "Threshold Intervals", "strength": None},
        "Wed": {"cycling": "Recovery Spin", "strength": None},
        "Thu": {"cycling": "Tempo Ride", "strength": "RED_B_PHASE1"},
        # ...
    }
}
```

### Priority 2: Phase Alignment

**Align strength phases with cycling phases**:
- Base phase → Light strength (Learn to Lift)
- Build phase → Moderate strength (transition to Lift Heavy Sh*t)
- Peak phase → Reduce strength volume (maintenance)
- Taper phase → Minimal strength (Don't Lose It)

**Code Changes**:
- Modify `generate_strength_files()` to accept cycling phase info
- Adjust strength schedule based on cycling phase, not fixed weeks

### Priority 3: Race-Specific Strength

**Add race-specific strength customization**:
- Create `race_strength_modifications` in race JSON
- Exercise selection pools by race type
- Phase adjustments based on race demands

**Example**:
```json
{
  "strength_modifications": {
    "focus": "endurance",  // or "power", "technical"
    "exercise_pool": "unbound_200",  // race-specific pool
    "phase_adjustments": {
      "peak_weeks_reduce": true,
      "taper_weeks_minimal": true
    }
  }
}
```

### Priority 4: Tier Variation

**Add tier-based strength adjustments**:
- Ayahuasca: 1x/week maintenance
- Finisher: 2x/week standard
- Compete: 2x/week, reduce during peak
- Podium: 2x/week, very light during peak

**Code Changes**:
- Modify `generate_strength_files()` to accept tier info
- Adjust volume/frequency based on tier

---

## Implementation Priority

1. **Day Assignment System** (High) — Unlocks all other integrations
2. **Phase Alignment** (High) — Prevents double peaks, coordinates taper
3. **Race-Specific Strength** (Medium) — Adds value differentiation
4. **Tier Variation** (Medium) — Better matches athlete needs
5. **Unified Calendar** (Low) — Nice-to-have, improves UX

---

## Files Requiring Changes

### High Priority
- `zwo_generator.py` — Add day assignment logic
- `strength_generator.py` — Accept cycling phase info, add tier/race customization
- Plan templates (`plans/*/template.json`) — Add day fields to workouts

### Medium Priority
- `generate_race_plans.py` — Pass phase/tier/race info to strength generator
- Race JSON files — Add `strength_modifications` section
- `guide_generator.py` — Add unified weekly calendar to guide

### Low Priority
- `guide_template_full.html` — Add weekly schedule section
- Filename generation — Standardize format

---

## Next Steps

1. **Audit plan templates** — Understand current workout structure
2. **Design unified schedule structure** — Define data model
3. **Implement day assignment** — Add to cycling generator
4. **Add phase coordination** — Modify strength generator
5. **Add race/tier customization** — Extend both systems
6. **Generate unified calendar** — Update guide generator

---

**Document Version**: 1.0  
**Date**: 2024-12-15  
**Status**: Audit Complete — Ready for Architecture Design

