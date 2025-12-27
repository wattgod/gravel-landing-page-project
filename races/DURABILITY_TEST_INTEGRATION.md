# Durability Test Integration

## Overview

Added benchmark durability tests to testing weeks, scaling by progression and plan tier.

---

## Test Schedule

### FTP Tests (Week 1, 7, 13, 19)
- **Week 1**: FTP Test (20min all out) - All plans
- **Week 7**: FTP Test (20min all out) - All plans
- **Week 13**: FTP Test (20min all out) - 16 & 20-week plans
- **Week 19**: FTP Test (20min all out) - 20-week plans only

### Durability Tests (Week 7, 13, 19)
- **Week 7**: 2hr @ 0.8 FTP (Metabolism 1) - All tiers
- **Week 13**: 
  - 3hr @ 0.8 FTP (Aerobic Endurance) - Time Crunched, Finisher
  - 4hr @ 0.8 FTP (Metabolism 3) - Compete, Compete Masters, Podium
- **Week 19**: 4hr @ 0.8 FTP (Metabolism 3) - All tiers (20-week plans only)

---

## Test Files

1. **FTP Test** (`2026-01-30_TheAssessm.zwo`)
   - 20min all out effort
   - Sets training zones for next 6 weeks

2. **Metabolism 1** (`2026-01-05_TheAssessm.zwo`)
   - 2 hours @ 0.8 FTP
   - Early progression test

3. **Aerobic Endurance** (`2026-01-06_TheAssessm.zwo`)
   - 3 hours @ 0.8 FTP
   - Mid progression test (lower tiers)

4. **Metabolism 3** (`2026-01-07_TheAssessm.zwo`)
   - 4 hours @ 0.8 FTP
   - Advanced progression test (higher tiers, late weeks)

---

## Test Logic

### Week 7 (Early Progression)
- **All tiers**: 2hr test
- Tests basic durability and aerobic fitness
- Replaces Saturday long ride

### Week 13 (Mid Progression)
- **Time Crunched, Finisher**: 3hr test
- **Compete, Compete Masters, Podium**: 4hr test
- Tests extended durability
- Tier-based scaling for appropriate challenge

### Week 19 (Late Progression)
- **All tiers**: 4hr test (20-week plans only)
- Maximum durability test
- Final benchmark before taper

---

## Test Purpose

### HR Decoupling Assessment
- Measures where HR decouples from power
- Shows aerobic fitness limit
- Indicates ability to sustain steady power over extended duration

### Fueling Practice
- Must eat/drink every 30 minutes
- Practice race fueling strategy
- Tests metabolic efficiency

### Mental Engagement
- RPE 6/10 to start, grows toward end
- Tests mental fortitude
- Simulates race conditions

---

## Implementation

### Converter
- `durability_test_converter.py` - Converts tests to GG format
- Handles Warmup, SteadyState, Cooldown elements
- Adds proper cadence ranges
- Creates GG-style descriptions

### Integration
- Tests inserted into plan templates
- Replaces Saturday long rides in test weeks
- Tier-based selection for appropriate challenge
- Week-based progression (2hr → 3hr → 4hr)

---

## Test Descriptions

Each test includes:
- **WARM-UP**: 10-15min building to top of Z2/bottom of Z3
- **MAIN SET**: Steady power @ 0.8 FTP for duration
- **COOL-DOWN**: 10min easy spin
- **PURPOSE**: HR decoupling assessment
- **EXECUTION**: Pacing, fueling, monitoring instructions

---

## Example Week Structure

### Week 7 (12-week plan)
- **Monday**: Rest
- **Tuesday**: FTP Test (20min all out)
- **Wednesday**: Easy ride
- **Thursday**: Intervals
- **Friday**: Rest
- **Saturday**: Durability Test - Metabolism 1 (2hr)
- **Sunday**: Rest

### Week 13 (16-week plan, Compete tier)
- **Monday**: Rest
- **Tuesday**: FTP Test (20min all out)
- **Wednesday**: Easy ride
- **Thursday**: Intervals
- **Friday**: Rest
- **Saturday**: Durability Test - Metabolism 3 (4hr)
- **Sunday**: Rest

---

*Created: December 26, 2025*  
*Status: Integrated into expanded plan generator*

