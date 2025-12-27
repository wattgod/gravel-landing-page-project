# Durability Test Integration - Summary

## ✅ Implementation Complete

Added benchmark durability tests to testing weeks, scaling by progression and plan tier.

---

## Test Schedule by Week

### Week 1
- **FTP Test** (20min all out) - All plans, all tiers
- Sets baseline training zones

### Week 7
- **FTP Test** (20min all out) - All plans
- **Durability Test - Metabolism 1** (2hr @ 0.8 FTP) - All tiers
- Early progression benchmark

### Week 13
- **FTP Test** (20min all out) - 16 & 20-week plans
- **Durability Test**:
  - **Time Crunched, Finisher**: 3hr @ 0.8 FTP (Aerobic Endurance)
  - **Compete, Compete Masters, Podium**: 4hr @ 0.8 FTP (Metabolism 3)
- Mid progression benchmark, tier-scaled

### Week 19
- **FTP Test** (20min all out) - 20-week plans only
- **Durability Test - Metabolism 3** (4hr @ 0.8 FTP) - All tiers
- Maximum durability benchmark before taper

---

## Test Files Used

1. **FTP Test**: `2026-01-30_TheAssessm.zwo`
   - 20min all out effort
   - Sets training zones

2. **Metabolism 1**: `2026-01-05_TheAssessm.zwo`
   - 2 hours @ 0.8 FTP
   - Week 7 test

3. **Aerobic Endurance**: `2026-01-06_TheAssessm.zwo`
   - 3 hours @ 0.8 FTP
   - Week 13 test (lower tiers)

4. **Metabolism 3**: `2026-01-07_TheAssessm.zwo`
   - 4 hours @ 0.8 FTP
   - Week 13 test (higher tiers), Week 19 test (all tiers)

---

## Test Logic

### Tier-Based Scaling
- **Lower tiers** (Time Crunched, Finisher): Progress from 2hr → 3hr
- **Higher tiers** (Compete, Compete Masters, Podium): Progress from 2hr → 4hr

### Week-Based Progression
- **Week 7**: 2hr test (all tiers) - Early benchmark
- **Week 13**: 3hr (lower) or 4hr (higher) - Mid benchmark
- **Week 19**: 4hr test (all tiers, 20-week only) - Max benchmark

---

## Test Purpose

### HR Decoupling Assessment
- Measures where HR decouples from power
- Shows aerobic fitness limit
- Indicates ability to sustain steady power

### Fueling Practice
- Must eat/drink every 30 minutes
- Practice race fueling strategy
- Tests metabolic efficiency

### Mental Engagement
- RPE 6/10 to start, grows toward end
- Tests mental fortitude
- Simulates race conditions

---

## Implementation Details

### Converter Module
- `durability_test_converter.py`
- Converts Warmup, SteadyState, Cooldown elements
- Adds proper cadence ranges (85-95rpm)
- Creates GG-style descriptions with:
  - WARM-UP section
  - MAIN SET section
  - COOL-DOWN section
  - PURPOSE section
  - EXECUTION section

### Integration
- Tests inserted into plan templates
- Replaces Saturday long rides in test weeks
- Tier-based selection via `select_durability_test()`
- Week-based progression automatically handled

---

## Example Test Descriptions

### Week 7 - Metabolism 1 (2hr)
```
WARM-UP:
• 10-15min building from Z1 to top of Z2/bottom of Z3

MAIN SET:
• 2 hours @ 0.80 FTP (top of Z2/bottom of Z3)

PURPOSE:
Durability Assessment - HR Decoupling Test
```

### Week 13 - Aerobic Endurance (3hr)
```
WARM-UP:
• 10-15min building from Z1 to top of Z2/bottom of Z3

MAIN SET:
• 3 hours @ 0.80 FTP (top of Z2/bottom of Z3)

PURPOSE:
Durability Assessment - HR Decoupling Test
```

### Week 13/19 - Metabolism 3 (4hr)
```
WARM-UP:
• 10-15min building from Z1 to top of Z2/bottom of Z3

MAIN SET:
• 4 hours @ 0.80 FTP (top of Z2/bottom of Z3)

PURPOSE:
Durability Assessment - HR Decoupling Test
```

---

## Verification

✅ Test selection logic verified for all tiers and weeks
✅ Converter tested and working
✅ Integration into expanded generator complete
✅ Ready for plan regeneration

---

*Created: December 26, 2025*  
*Status: Ready for use*

