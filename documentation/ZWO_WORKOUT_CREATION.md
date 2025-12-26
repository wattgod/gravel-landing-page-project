# ZWO Workout Creation System

## Overview

This document provides comprehensive instructions for creating ZWO workout files using the archetype library system. This system generates 192 progressive workout archetypes across 32 categories with 6 progression levels each.

## Key Files

- **`create_archetype_library.py`** - Main script that generates all ZWO workout files
- **`test_cadence_resting.py`** - Regression tests for cadence functionality
- **`CADENCE_RESTING_BREAKTHROUGH.md`** - Critical documentation for CadenceResting feature

## Quick Start

```bash
cd /Users/mattirowe/nate_workout_processing
python3 create_archetype_library.py
```

This generates 192 ZWO files in `/Users/mattirowe/Downloads/Nate_Workouts_Archetypes/`

## Workout Structure

### XML Elements

ZWO workouts use the following XML structure:

```xml
<workout_file>
  <author>Gravel God Training</author>
  <name>Workout Name - Level</name>
  <description>Formatted workout description</description>
  <sportType>bike</sportType>
  <workout>
    <!-- WARM-UP -->
    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75" />
    <SteadyState Duration="600" Power="0.87" CadenceLow="100" CadenceHigh="120" />
    <!-- MAIN SET -->
    <IntervalsT Repeat="5" OnDuration="240" OnPower="0.85" OffDuration="180" OffPower="0.55" 
                CadenceLow="110" CadenceHigh="120" CadenceResting="65" />
    <!-- COOL-DOWN -->
    <Cooldown Duration="600" PowerLow="0.50" PowerHigh="0.65" />
  </workout>
</workout_file>
```

### Key XML Elements

- **`Warmup`** - Progressive warmup from Z1 to Z2
- **`SteadyState`** - Continuous effort at fixed power
- **`IntervalsT`** - Repeating intervals with ON/OFF phases
- **`Cooldown`** - Easy spin-down

## Critical Features

### 1. CadenceResting Attribute

**CRITICAL FOR FUTURE LLMs**: The system automatically adds `CadenceResting` attributes to `IntervalsT` elements when work cadence differs significantly from recovery cadence.

**When it's added:**
- High cadence intervals (≥100rpm work) → `CadenceResting="65"`
- SFR intervals (≤60rpm work) → `CadenceResting="65"`
- Normal cadence (70-95rpm) → No `CadenceResting` (defaults to same)

**See `CADENCE_RESTING_BREAKTHROUGH.md` for complete details.**

### 2. Cadence Ranges

The system supports multiple cadence input formats:

- **Single value**: `85` → `Cadence="85"`
- **Tuple range**: `(100, 120)` → `CadenceLow="100" CadenceHigh="120"`
- **String range**: `"100-120"` → `CadenceLow="100" CadenceHigh="120"`

### 3. Text Events (Disabled)

Text events (`<textevent>`) are **disabled by default** for all workouts. The workout descriptions provide sufficient context, making text events redundant.

## Workout Categories

### 1. VO2max
- 30/30 VO2
- Broken VO2 (40/20)
- Microbursts

### 2. TT/Threshold
- 3x10 Threshold
- Progressive Threshold
- TT Progressives

### 3. Tempo/G-Spot
- Tempo Intervals
- Tempo + Lift
- Climbing Over/Under

### 4. Cadence Work
- High Cadence Intervals
- SFR + Cadence Contrast

### 5. SFR/Muscle Force
- 5x4 SFR
- SFR + Cadence Contrast

### 6. Progressive Change of Rhythm
- Mixed Climbing

### 7. Durability
- Tired 30/30s
- Tired Threshold Repeats
- Full Simulation Combo

### 8. Endurance
- Long Endurance with Late Efforts
- Bookend Endurance

## Progression Levels

Each archetype has 6 progression levels (1-6):

- **Level 1**: Beginner-friendly, lower intensity/duration
- **Level 2-3**: Intermediate progression
- **Level 4-5**: Advanced progression
- **Level 6**: Maximum difficulty

Progression is achieved through:
- Increased duration
- Increased power targets
- More intervals/repeats
- Longer blocks

## Description Formatting

Workout descriptions follow the **Gravel God Description Format Standard**:

```
WARM-UP:
• 15min building from Z1 to Z2, then 10min Z3 @ 100-120rpm

MAIN SET:
• 5x4min @ 85% FTP with 3min recovery
• Cadence: 110-120rpm (high cadence work)
• Position: Seated, on the hoods

COOL-DOWN:
• 10 min @ Z1 (RPE 1-2)
• Spin out the legs

EXECUTION:
• HYDRATION: 1 bottle/hr with electrolytes mandatory...
• [Workout-specific guidance]
```

### Formatting Rules

- **ALL CAPS headers** with colons (`WARM-UP:`, `MAIN SET:`, `COOL-DOWN:`, `EXECUTION:`)
- **Bullet points** using `•` character
- **Dimensional prescriptions** (Cadence, Position, Timing) as bullet points in MAIN SET
- **No "Why This Matters"** section
- **No "Execution"** section (replaced by EXECUTION with dynamic guidance)

## Warmup Varieties

The system uses 4 warmup varieties (distributed via hash):

1. **Steady 10min Z3** high cadence
2. **Progressive Z3** (build from 85% to 92% FTP)
3. **2x5min Z3** with 1min Z2 between
4. **Ramp Z1-Z4** in 4 steps (3min per zone)

## Main Set Types

### IntervalsT Pattern

For alternating ON/OFF intervals:

```python
interval = ET.SubElement(workout, 'IntervalsT')
interval.set('Repeat', str(repeats))
interval.set('OnDuration', str(on_duration))
interval.set('OnPower', str(on_power))
interval.set('OffDuration', str(off_duration))
interval.set('OffPower', str(off_power))
add_cadence_to_element(interval, cadence_value_or_range)
# Text events are disabled: skip_text_events=True
```

### SteadyState Pattern

For continuous efforts:

```python
steady = ET.SubElement(workout, 'SteadyState')
steady.set('Duration', str(duration))
steady.set('Power', str(power))
add_cadence_to_element(steady, cadence_value_or_range)
```

## Key Functions

### `add_cadence_to_element(element, cadence_value_or_range, resting_cadence=None)`

Adds cadence attributes to XML elements. Automatically sets `CadenceResting` for `IntervalsT` when appropriate.

**Parameters:**
- `element`: XML element (IntervalsT or SteadyState)
- `cadence_value_or_range`: Single value, tuple `(low, high)`, or string `"100-120"`
- `resting_cadence`: Optional override for recovery cadence

**Auto-behavior:**
- High cadence (≥100rpm) → `CadenceResting="65"`
- Low cadence (≤60rpm) → `CadenceResting="65"`
- Normal cadence (70-95rpm) → No `CadenceResting`

### `add_interval_text_events(interval_element, on_power, off_power, on_duration, workout_type='generic', skip_text_events=False)`

**Note**: Text events are disabled by default (`skip_text_events=True` in all calls).

### `create_zwo_workout(category, archetype_name, level_num, level_data)`

Main function that creates a complete ZWO workout XML structure.

## Testing

Run regression tests:

```bash
cd /Users/mattirowe/nate_workout_processing
python3 test_cadence_resting.py
```

**Test Coverage:**
- High cadence auto-resting
- SFR cadence auto-resting
- Normal cadence no resting
- Explicit resting cadence override
- SteadyState no resting
- Cadence range string parsing
- Boundary conditions (60rpm, 100rpm)

## Common Patterns

### High Cadence Intervals

```python
interval = ET.SubElement(workout, 'IntervalsT')
interval.set('Repeat', '5')
interval.set('OnDuration', '240')
interval.set('OnPower', '0.85')
interval.set('OffDuration', '180')
interval.set('OffPower', '0.55')
add_cadence_to_element(interval, (110, 120))  # Auto-adds CadenceResting="65"
```

### SFR Intervals

```python
interval = ET.SubElement(workout, 'IntervalsT')
interval.set('Repeat', '4')
interval.set('OnDuration', '180')
interval.set('OnPower', '0.97')
interval.set('OffDuration', '180')
interval.set('OffPower', '0.55')
add_cadence_to_element(interval, 55)  # Auto-adds CadenceResting="65"
```

### Mixed Climbing

```python
# Alternating seated/standing within climb blocks
interval = ET.SubElement(workout, 'IntervalsT')
interval.set('Repeat', str(cycles_per_block))
interval.set('OnDuration', str(on_duration))  # Seated
interval.set('OnPower', str(level_data['on_power']))
interval.set('OffDuration', str(off_duration))  # Standing
interval.set('OffPower', str(level_data['off_power']))
# Text events disabled - description is clear enough
```

## Output Structure

Generated workouts are organized by category:

```
Nate_Workouts_Archetypes/
├── VO2max/
│   ├── 3030_VO2_1.zwo
│   ├── 3030_VO2_2.zwo
│   └── ...
├── TT_Threshold/
│   ├── 3x10_Threshold_1.zwo
│   └── ...
└── ...
```

## Important Notes for Future LLMs

1. **DO NOT REMOVE CadenceResting feature** - It's critical for proper workout execution
2. **Text events are disabled** - Don't re-enable them unless explicitly requested
3. **Description format is strict** - Follow the Gravel God Description Format Standard
4. **Warmup always includes high cadence Z3** - 10min @ 100-120rpm after initial warmup
5. **Cooldown is always 10min** - Easy spin at Z1-Z2
6. **Power values are %FTP** - 0.85 = 85% FTP, 1.15 = 115% FTP
7. **Duration is in seconds** - 240 = 4 minutes

## Troubleshooting

### Workouts showing wrong cadence in TrainingPeaks

- Verify `CadenceResting` is set for high/low cadence intervals
- Check that cadence ranges use `CadenceLow`/`CadenceHigh` (not single `Cadence`)

### Text events appearing in workouts

- Ensure all `add_interval_text_events()` calls have `skip_text_events=True`

### Progression not working

- Check that `level_data` includes proper duration/power increases
- Verify TSS calculations for meaningful progression

## References

- **`CADENCE_RESTING_BREAKTHROUGH.md`** - Complete CadenceResting documentation
- **`test_cadence_resting.py`** - Regression test suite
- **`create_archetype_library.py`** - Main generation script (3600+ lines)
