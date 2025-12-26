# 🎯 MAJOR BREAKTHROUGH: CadenceResting Attribute Support

## What This Is

**CRITICAL FEATURE FOR FUTURE LLMs**: The ZWO workout generator now automatically adds `CadenceResting` attributes to `IntervalsT` elements when work cadence differs significantly from normal recovery cadence.

## Why This Matters

In Zwift/TrainingPeaks, when you have intervals with different cadence targets for work vs. recovery periods, you need to specify both:
- **Work cadence**: The cadence during the ON/effort phase
- **Recovery cadence**: The cadence during the OFF/recovery phase (via `CadenceResting`)

Without `CadenceResting`, platforms may default to the same cadence for both phases, which is incorrect for:
- **High cadence intervals** (100-120rpm work → should recover at ~65rpm)
- **SFR (Slow Force Reps)** intervals (50-60rpm work → should recover at ~65rpm)

## Implementation Details

### Function: `add_cadence_to_element()`

Located in `create_archetype_library.py` around line 2717.

**Key Logic:**
1. Accepts cadence as single value, range tuple `(low, high)`, or string `"100-120"`
2. Sets appropriate XML attributes:
   - Single value → `Cadence="85"`
   - Range → `CadenceLow="100" CadenceHigh="120"`
3. **AUTOMATICALLY adds `CadenceResting="65"`** for `IntervalsT` elements when:
   - Work cadence ≥ 100rpm (high cadence work)
   - Work cadence ≤ 60rpm (SFR/low cadence work)
4. Can also accept explicit `resting_cadence` parameter to override defaults

### Example Output

**High Cadence Intervals:**
```xml
<IntervalsT Repeat="5" OnDuration="240" OnPower="0.85" OffDuration="180" OffPower="0.55" 
            CadenceLow="110" CadenceHigh="120" CadenceResting="65">
  <textevent timeoffset="0" message="Tempo" />
  <textevent timeoffset="240" message="Recovery" />
</IntervalsT>
```

**SFR Intervals:**
```xml
<IntervalsT Repeat="4" OnDuration="180" OnPower="0.97" OffDuration="180" OffPower="0.55" 
            Cadence="55" CadenceResting="65">
  <textevent timeoffset="0" message="Threshold" />
  <textevent timeoffset="180" message="Recovery" />
</IntervalsT>
```

## Reference Implementation

This feature was inspired by the example file: `2026-01-23_Gravel-Tor.zwo`, which showed the pattern:
```xml
<IntervalsT Repeat="10" OnDuration="30" OnPower="0.82" OffDuration="30" OffPower="0.55" 
            Cadence="120" CadenceResting="65" />
```

## Testing

See `test_cadence_resting.py` for regression tests that verify:
1. High cadence intervals get `CadenceResting="65"`
2. SFR intervals get `CadenceResting="65"`
3. Normal cadence intervals (70-95rpm) do NOT get `CadenceResting` (defaults to same)
4. Explicit `resting_cadence` parameter overrides automatic behavior

## Impact

- **All 192 archetype workouts** now have proper cadence targets for both work and recovery phases
- **TrainingPeaks/Zwift** will correctly display and enforce different cadence targets during intervals
- **User experience** significantly improved - no more confusion about cadence targets during recovery

## Future Maintenance

**DO NOT REMOVE THIS FEATURE** - It's critical for proper workout execution in training platforms. If modifying `add_cadence_to_element()`, ensure:
1. `CadenceResting` is still automatically added for extreme cadences
2. Regression tests still pass
3. Example workouts (High Cadence, SFR) still generate correctly
