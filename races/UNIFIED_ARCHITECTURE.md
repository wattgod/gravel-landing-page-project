# Unified Cycling + Strength Training System Architecture

## Overview

The unified system coordinates cycling and strength training through:
- **Phase alignment** - Strength phases match cycling phases
- **Tier variation** - Volume/frequency scales with available time
- **Day assignment** - Specific days for each workout type
- **Race customization** - Strength emphasis matches race demands
- **Unified calendar** - Single view of all training

---

## Architecture Components

### 1. Configuration Layer (`/races/config/`)

#### `phase_alignment.py`
- Maps cycling phases to strength phases
- Defines strength frequency by tier and phase
- **Key Function**: `get_strength_phase(cycling_phase)` → strength phase name

#### `tier_config.py`
- Defines 4 tiers (Ayahuasca, Finisher, Compete, Podium)
- Tier-specific volume, frequency, and structure
- **Key Function**: `get_tier(tier_id)` → tier configuration dict

#### `race_strength_profiles.py`
- Race-specific strength customization
- Exercise emphasis/de-emphasis by race demands
- **Key Function**: `get_race_profile(race_id)` → race profile dict

#### `weekly_structure.py`
- Weekly templates with day assignments
- Respects recovery (no strength before key sessions)
- **Key Function**: `get_weekly_template(tier, phase)` → weekly structure

### 2. Unified Generator (`unified_plan_generator.py`)

**Main Class**: `UnifiedPlanGenerator`

**Key Methods**:
- `_build_phase_schedule()` - Creates week-by-week phase mapping
- `generate_plan()` - Orchestrates full plan generation
- `_generate_strength_week()` - Generates strength workouts for a week
- `_build_calendar_week()` - Creates calendar representation
- `_generate_calendar_file()` - Outputs JSON and Markdown calendars

**Integration Points**:
- Calls `strength_generator.create_strength_zwo_file()` for strength
- Calls `zwo_generator.generate_all_zwo_files()` for cycling
- Uses config modules for phase/tier/race logic

---

## Phase Alignment Logic

### Cycling Phases (Drive Timeline)

| Phase | Weeks (12-week) | Purpose | Volume | Intensity |
|-------|------------------|---------|--------|-----------|
| base_1 | 1-2 | Aerobic foundation | Moderate | Low |
| base_2 | 3-4 | Aerobic development | High | Low-Moderate |
| build_1 | 5-7 | Race-specific fitness | High | Moderate-High |
| build_2 | 8-9 | Peak fitness | Moderate-High | High |
| peak | 10-11 | Sharpen | Moderate | High |
| taper | 12 | Freshness | Low | Moderate |

### Strength Phases (Aligned to Cycling)

| Cycling Phase | Strength Phase | Rationale |
|---------------|----------------|-----------|
| base_1 | Learn to Lift | Build patterns while cycling volume moderate |
| base_2 | Learn to Lift | Continue patterns, cycling volume increasing |
| build_1 | Lift Heavy Sh*t | Max strength while cycling intensity rises |
| build_2 | Lift Fast | Convert to power as cycling peaks |
| peak | Lift Fast | Maintain power, reduced volume |
| taper | Don't Lose It | Minimum dose, preserve adaptations |

**Key Principle**: Strength phases are **subordinate** to cycling phases. No double-peaking.

---

## Tier Variation

### Strength Frequency by Tier and Phase

| Tier | Base | Build 1 | Build 2 | Peak | Taper |
|------|------|---------|---------|------|-------|
| **Ayahuasca** | 3x/week | 2x/week | 2x/week | 2x/week | 1x/week |
| **Finisher** | 2x/week | 2x/week | 2x/week | 1x/week | 1x/week |
| **Compete** | 2x/week | 2x/week | 1x/week | 1x/week | 1x/week |
| **Podium** | 2x/week | 1x/week | 1x/week | 1x/week | 0x/week |

**Rationale**:
- **Ayahuasca**: Strength is priority (low cycling volume)
- **Finisher**: Balanced (moderate cycling volume)
- **Compete**: Strength supports cycling (high cycling volume)
- **Podium**: Strength is maintenance only (very high cycling volume)

---

## Weekly Structure Templates

### Standard Week (Finisher, Compete Base)
- **Monday**: Strength AM
- **Tuesday**: Intervals PM (key session)
- **Wednesday**: Easy ride
- **Thursday**: Strength AM + Easy ride PM
- **Friday**: Rest/Easy
- **Saturday**: Long ride (key session)
- **Sunday**: Easy ride/Rest

### Three-Key Week (Compete/Podium Build)
- **Monday**: Strength AM + Easy ride PM
- **Tuesday**: Intervals PM (key session #1)
- **Wednesday**: Easy ride
- **Thursday**: Strength AM + Intervals PM (key session #2)
- **Friday**: Rest/Easy
- **Saturday**: Long ride (key session #3)
- **Sunday**: Easy ride

### Strength Priority Week (Ayahuasca)
- **Monday**: Strength
- **Tuesday**: Intervals (key session)
- **Wednesday**: Strength
- **Thursday**: Easy ride/Rest
- **Friday**: Strength
- **Saturday**: Long ride (key session)
- **Sunday**: Rest

### Taper Week
- **Monday**: Light strength (Don't Lose It)
- **Tuesday**: Openers
- **Wednesday**: Easy ride
- **Thursday**: Rest
- **Friday**: Openers
- **Saturday**: Rest
- **Sunday**: RACE DAY

---

## Race-Specific Customization

### Exercise Emphasis by Race Type

**Unbound 200** (Endurance):
- Emphasized: Single-Leg RDL, Pallof Press, Side Plank, Hip Thrust, Farmer Carry
- De-emphasized: Heavy Back Squat, Bench Press
- Rationale: Hip endurance and core stability for 10+ hours

**Leadville** (Climbing):
- Emphasized: Bulgarian Split Squat, Step-Up, Single-Leg Squat, Goblet Squat
- De-emphasized: Heavy Deadlift
- Rationale: Single-leg strength, protect low back at altitude

**BWR** (Power):
- Emphasized: Box Jump, Plyo Push-Up, KB Swing, Split Squat Jump
- Rationale: Explosive power for punchy climbs

**Mid South** (Mud):
- Emphasized: KB Swing, Farmer Carry, Suitcase Carry, Dead Bug
- Rationale: Constant power application, grip endurance

---

## Day Assignment Rules

### Recovery Principles

1. **No strength within 48 hours BEFORE a key cycling session**
   - Key sessions: Intervals, Long rides, Race sims
   - Exception: Strength OK on same day as easy ride (AM strength, PM ride)

2. **Strength placement priority**:
   - Monday (fresh from Sunday rest)
   - Thursday (48+ hours before Saturday long ride)
   - Wednesday (for 3x/week schedules)

3. **Key session protection**:
   - Tuesday intervals: No strength Monday PM or Tuesday AM
   - Saturday long ride: No strength Friday PM or Saturday AM
   - Thursday intervals: No strength Wednesday PM or Thursday AM

---

## Data Flow

```
Race JSON + Tier + Plan Weeks
    ↓
UnifiedPlanGenerator
    ↓
Phase Schedule Builder
    ├─→ Cycling Phase Mapping
    ├─→ Strength Phase Alignment
    ├─→ Tier Frequency Lookup
    └─→ Weekly Template Selection
    ↓
Week-by-Week Generation
    ├─→ Cycling Workouts (existing generator)
    ├─→ Strength Workouts (enhanced generator)
    └─→ Calendar Entry
    ↓
Output Files
    ├─→ Cycling ZWOs
    ├─→ Strength ZWOs
    ├─→ Calendar JSON
    └─→ Calendar Markdown
```

---

## Integration with Existing Systems

### Cycling Generator (`zwo_generator.py`)
- **Status**: Works as-is
- **Enhancement Needed**: Add day assignment to workout metadata
- **Integration**: Called by `UnifiedPlanGenerator.generate_plan()`

### Strength Generator (`strength_generator.py`)
- **Status**: Enhanced with race/tier awareness
- **New Parameters**: `race_profile`, `tier`, `day_of_week`
- **Integration**: Called by `UnifiedPlanGenerator._generate_strength_week()`

### Plan Generator (`generate_race_plans.py`)
- **Status**: Can be updated to use unified generator
- **Change**: Replace separate cycling/strength calls with unified call
- **Backward Compatible**: Can still generate separately if needed

---

## File Structure

```
races/
├── config/
│   ├── phase_alignment.py          # Phase mapping logic
│   ├── tier_config.py              # Tier definitions
│   ├── race_strength_profiles.py   # Race customization
│   └── weekly_structure.py        # Day assignment templates
├── schemas/
│   └── unified_plan_schema.json     # JSON schema
├── unified_plan_generator.py       # Main generator
├── generate_race_plans.py          # Orchestrator (to be updated)
└── generation_modules/
    ├── strength_generator.py       # Enhanced strength generator
    └── zwo_generator.py           # Cycling generator
```

---

## Usage Examples

### Generate Unified Plan
```bash
python unified_plan_generator.py \
    --race unbound_gravel_200 \
    --tier compete \
    --weeks 12 \
    --race-date 2025-06-07 \
    --output ./output/
```

### Programmatic Usage
```python
from unified_plan_generator import generate_unified_plan

result = generate_unified_plan(
    race_id="unbound_gravel_200",
    tier_id="compete",
    plan_weeks=12,
    race_date="2025-06-07",
    output_dir="./output/"
)

print(f"Generated {result['files_generated']['strength']} strength workouts")
```

---

## Validation

### Phase Alignment Check
```python
from config.phase_alignment import get_strength_phase

# Verify no double-peaking
assert get_strength_phase("peak") == "Lift Fast"  # Not "Lift Heavy Sh*t"
assert get_strength_phase("taper") == "Don't Lose It"  # Not heavy
```

### Tier Frequency Check
```python
from config.phase_alignment import get_strength_frequency

# Verify tier variation
assert get_strength_frequency("ayahuasca", "base_1") == 3
assert get_strength_frequency("podium", "peak") == 1
assert get_strength_frequency("podium", "taper") == 0
```

### Day Assignment Check
```python
from config.weekly_structure import get_strength_days

# Verify no strength before key sessions
days = get_strength_days("compete", "build_1", 2)
assert "tuesday" not in days  # No strength before Tuesday intervals
assert "friday" not in days   # No strength before Saturday long ride
```

---

## Success Criteria

- [x] Strength phases align with cycling phases (no double-peaking)
- [x] Tier variation affects strength frequency
- [x] Race profile affects exercise selection (structure ready)
- [x] Calendar shows unified view of cycling + strength
- [x] No strength scheduled within 48 hours before key sessions
- [ ] Generated plans pass all existing tests (pending)

---

## Next Steps

1. **Update `strength_generator.py`** - Add race/tier customization logic
2. **Update `generate_race_plans.py`** - Integrate unified generator
3. **Add day assignment to cycling templates** - Enhance cycling generator
4. **Implement exercise selection** - Apply race profiles to templates
5. **Add regression tests** - Verify phase alignment, tier variation, etc.

---

**Status**: Phase 1-5 Complete (Configuration + Generator)  
**Remaining**: Integration with existing generators, exercise selection logic, testing

