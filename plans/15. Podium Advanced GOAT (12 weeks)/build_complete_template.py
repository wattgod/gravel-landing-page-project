#!/usr/bin/env python3
"""
Build complete JSON template for PODIUM ADVANCED GOAT (12 weeks)
GOAT (Gravel Optimized Adaptive Training) - Integrated system
All workouts (12 weeks, with block options for Weeks 2-3 and Weeks 5-8)
"""
import json
import re
import os

def clean_description(desc):
    """Clean and convert workout descriptions"""
    if not desc:
        return ""
    desc = desc.replace("Sweet Spot", "G-Spot")
    desc = desc.replace("sweet spot", "G-Spot")
    desc = re.sub(r'88-93% FTP', '87-92% FTP', desc)
    desc = re.sub(r'88-92% FTP', '87-92% FTP', desc)
    return desc

def create_workout(name, description, blocks=None):
    """Create workout JSON object"""
    if blocks is None:
        blocks = "    <FreeRide Duration=\"60\"/>\n"
    return {
        "name": name,
        "description": clean_description(description),
        "blocks": blocks
    }

# Plan metadata
plan_metadata = {
    "name": "PODIUM ADVANCED GOAT",
    "duration_weeks": 12,
    "philosophy": "GOAT (Gravel Optimized Adaptive Training)",
    "target_hours": "20-25",
    "target_athlete": "Elite preparation, sophisticated monitoring capacity, coaching-level discipline",
    "goal": "Elite performance through integrated pyramidal base, polarized weeks, limiter-focused blocks, and multi-signal autoregulation"
}

weeks = []

# WEEK 1: Assessment, Baseline, Signal Establishment
weeks.append({
    "week_number": 1,
    "focus": "Assessment, Baseline, Signal Establishment",
    "volume_percent": 70,
    "volume_hours": "14-17.5",
    "workouts": [
        create_workout("W01 Mon - Rest", """• Week 1 is comprehensive assessment to establish YOUR baseline across all relevant signals: FTP, CP (critical power), LT1 (aerobic threshold), VO2max, HR drift, HRV baseline, CTL (chronic training load), and limiter identification. GOAT is adaptive—it needs data to adapt TO. Establish monitoring protocols: HRV measured every morning (same conditions—upon waking, still in bed, 5-min reading). Track: sleep quality/duration, RPE from workouts, resting HR, subjective readiness (1-10 scale). Use TrainingPeaks or similar to track CTL/ATL/TSB. Week 1 creates the dashboard.

• WEEK PREVIEW: Comprehensive assessment week. Tuesday has FTP + critical power testing (power profile). Thursday has LT1 + durability assessment. Saturday is long pyramidal base ride (6-7 hours). Sunday includes max strength work. This week establishes your baseline and identifies primary limiters for Block 1.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W01 Tue - FTP + Critical Power Testing", """• STRUCTURE:
30 min warmup → 5 min all-out → 10 min recovery → 20 min max effort → 15 min easy → 3 min all-out → 15 min easy → 1 min all-out → 15 min cooldown

• FTP (20-min avg × 0.95), plus 5-min/3-min/1-min max efforts for power profile. This reveals VO2max power (5-min), anaerobic capacity (3-min), neuromuscular power (1-min). Record everything. Compare ratios: 5-min should be ~120% FTP, 1-min ~150%+ FTP. Deficiencies = limiters for block periodization later. Monitoring Note: Record morning HRV before test, RPE immediately after, sleep quality last night, subjective readiness pre-test (1-10).""", """    <Warmup Duration="1800" PowerLow="0.50" PowerHigh="0.75"/>
    <SteadyState Duration="300" Power="1.20"/>
    <SteadyState Duration="600" Power="0.55"/>
    <SteadyState Duration="1200" Power="1.05"/>
    <SteadyState Duration="900" Power="0.55"/>
    <SteadyState Duration="180" Power="1.25"/>
    <SteadyState Duration="900" Power="0.55"/>
    <SteadyState Duration="60" Power="1.50"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W01 Wed - Easy Endurance (Pyramidal Base)", """• Pyramidal base principle—most volume at Z2. Easy conversational pace. Monitoring: Morning HRV, post-ride RPE, HR drift during ride (compare avg HR first 30 min vs last 30 min—should be minimal <5%).""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="7200" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W01 Thu - LT1 + Durability Assessment", """• STRUCTURE:
20 min warmup → 30 min @ 70-75% FTP (monitor HR to establish LT1) → 15 min easy → 3x20 min @ 85-90% FTP (monitor power/HR stability, 8 min easy between) → 30 min cooldown

• LT1 (aerobic threshold) = highest power you can sustain with stable HR and nasal breathing only. Usually ~70-75% FTP. Then durability check—can you hold 85-90% for sustained efforts? Power decay >5% or HR drift >8 bpm = durability limiter. Monitoring: Morning HRV, HR drift within 30-min block and across 3x20 intervals, power decay percentage, RPE evolution across intervals.

• CADENCE WORK: Mix cadences on durability blocks.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <SteadyState Duration="1800" Power="0.73"/>
    <SteadyState Duration="900" Power="0.55"/>
    <IntervalsT Repeat="3" OnDuration="1200" OnPower="0.875" Cadence="100" OffDuration="480" OffPower="0.55"/>
    <Cooldown Duration="1800" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W01 Fri - Easy Endurance", """• Duration: 2-2.5 hours | Zones: Z2

• Monitoring: Morning HRV, subjective readiness, accumulated fatigue from week.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W01 Sat - Long Pyramidal Base Ride", """• STRUCTURE:
Pyramidal—80% Z2, 15% Z3 (tempo touches), 5% Z4 (brief surges)
Example: First 3 hours Z2 → 4x15 min @ 80-85% FTP (6 min easy between) → Final 2-2.5 hours Z2

• Pyramidal distribution—MOST time Z2, moderate time Z3, small time Z4+. This is sustainable high-volume distribution. Eat 70-90g carbs/hour. Monitoring: HR drift over 6-7 hours, power decay in final hours, fueling tolerance, subjective difficulty (1-10).

• CADENCE WORK: Mix cadences on tempo blocks.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="10800" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="4" OnDuration="900" OnPower="0.825" Cadence="100" OffDuration="360" OffPower="0.55"/>
    <SteadyState Duration="8100" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W01 Sun - Long Easy Endurance + Max Strength (Base Phase)", """• Long easy ride maintains volume. Max strength during base phase builds force production foundation—critical for gravel. GOAT integrates strength year-round: max strength in base, explosive in VO2 phases, stability in threshold phases, durability in volume blocks. Monitoring: Morning HRV, recovery from Saturday's long ride, strength performance (bar speed, RPE).

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Heavy back squats, trap bar deadlifts, weighted planks, Bulgarian splits, single-leg RDLs (5x5 @ 85-90% 1RM, rest 4-5 min between sets). Max strength phase for elite athletes. Perfect form always. This is injury prevention AND performance. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="18000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# Weeks 2-3: Block 1 - Concentrated Loading (Pyramidal Base Maintained)
# Structure similar to COMPETE ADVANCED with workouts_by_block

weeks.append({
    "week_number": 2,
    "focus": "Block 1 - Concentrated Loading (Pyramidal Base Maintained)",
    "volume_percent": 85,
    "volume_hours": "17-21",
    "critical_decision_point": "Based on Week 1 assessment, choose VO2max, Threshold, or Durability Block.",
    "workouts_by_block": {
        "VO2max": [
            create_workout("W02 Mon - Rest VO2MAX BLOCK", """• Weeks 2-3 implement YOUR chosen limiter block while maintaining pyramidal base volume. This is GOAT's power: MOST training stays pyramidal (sustainable), but we ADD concentrated stimulus on your limiter. You're not abandoning base—you're sharpening one capacity within base framework. VO2max block selected.

• WEEK PREVIEW: VO2max concentrated loading. Tuesday, Thursday, Saturday have VO2max sessions (embedded in volume). Everything else pyramidal easy. This is peak VO2max stimulus—lungs will burn, legs will scream. That's adaptation.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
            create_workout("W02 Tue - VO2max Session #1 (Block Focus)", """• STRUCTURE:
30 min Z2 warmup → 6x5 min @ 110-120% FTP (5 min Z1 recovery) → 30 min Z2 cooldown

• Monitoring: Morning HRV before session. GREEN (normal/high)? Proceed. YELLOW (slightly low)? Reduce to 5x5 min. RED (significantly low)? Skip intervals, ride 2 hours Z2 instead. KPI: Can you complete all intervals with <5% power decay? Record avg power each interval.

• CADENCE WORK: Alternate high cadence (100+ rpm seated) and low cadence (40-60 rpm seated, big gear) on intervals.""", """    <Warmup Duration="1800" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1800" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="6" OnDuration="300" OnPower="1.15" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="1800" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
            create_workout("W02 Wed - Pyramidal Easy", """• Duration: 2.5-3 hours | Zones: Z2 (maintaining pyramidal base)

• Monitoring: Post-VO2 recovery—HRV should drop after hard session, should rebound toward baseline today.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="9000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
            create_workout("W02 Thu - VO2max Session #2 (Block Focus)", """• STRUCTURE:
30 min warmup → 8x4 min @ 110-120% FTP (4 min easy) → 30 min cooldown

• Monitoring: Morning HRV check. Adjust volume based on readiness. KPI: Repeatability—can you hit similar power across all 8 intervals?

• CADENCE WORK: Mix cadences—intervals 1, 3, 5, 7 at high cadence (100+ rpm), intervals 2, 4, 6, 8 at low cadence (40-60 rpm).""", """    <Warmup Duration="1800" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="8" OnDuration="240" OnPower="1.15" Cadence="100" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="1800" PowerLow="0.70" PowerHigh="0.50"/>
"""),
            create_workout("W02 Fri - Pyramidal Easy", """• Duration: 2-2.5 hours | Zones: Z2

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
            create_workout("W02 Sat - Long Pyramidal Ride with VO2 Touch", """• STRUCTURE:
First 3 hours Z2 → 5x5 min @ 110-120% FTP (5 min easy) embedded in hours 4-5 → Final 1-2 hours Z2

• GOAT Integration: VO2 work within long ride maintains block focus while accumulating volume (pyramidal principle). KPI: Can you hit VO2 power when fatigued deep in ride?

• CADENCE WORK: Mix cadences on VO2 intervals.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="10800" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="5" OnDuration="300" OnPower="1.15" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
            create_workout("W02 Sun - Long Pyramidal Easy + Explosive Strength", """• Duration: 5-6 hours Z2 + 50-60 min strength

• Strength: Box jumps, med ball slams, jump squats, power cleans (4x6-8 explosive)

• Notes: Explosive strength during VO2 block supports power development.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Box jumps, med ball slams, jump squats, power cleans (4x6-8 explosive). Explosive strength supports power development. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="18000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
        ],
        "Threshold": [
            create_workout("W02 Mon - Rest THRESHOLD BLOCK", """• Weeks 2-3 implement YOUR chosen limiter block while maintaining pyramidal base volume. This is GOAT's power: MOST training stays pyramidal (sustainable), but we ADD concentrated stimulus on your limiter. You're not abandoning base—you're sharpening one capacity within base framework. Threshold block selected.

• WEEK PREVIEW: Threshold concentrated loading. Tuesday, Thursday, Saturday have threshold sessions (embedded in volume). Everything else pyramidal easy. This is peak threshold stimulus—race pace will feel harder, but that's adaptation.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
            create_workout("W02 Tue - Threshold Session #1 (Block Focus)", """• STRUCTURE:
30 min Z2 warmup → 3x20 min @ 100-105% FTP (10 min Z1 recovery) → 30 min Z2 cooldown

• Monitoring: Morning HRV. GREEN? Full 3x20. YELLOW? 3x15 min. RED? Z2 ride only. KPI: Power stability—are you holding steady watts across all 20-min blocks?

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected.""", """    <Warmup Duration="1800" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1800" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="1200" OnPower="1.02" Cadence="100" OffDuration="600" OffPower="0.55"/>
    <SteadyState Duration="1800" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
            create_workout("W02 Wed - Pyramidal Easy", """• Duration: 2.5-3 hours Z2""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="9000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
            create_workout("W02 Thu - Threshold Session #2 (Block Focus)", """• STRUCTURE:
30 min warmup → 2x30 min @ 100-105% FTP (10 min easy) → 30 min cooldown

• KPI: Can you extend interval duration while maintaining power?

• CADENCE WORK: First interval at high cadence (100+ rpm), second at low cadence (40-60 rpm).""", """    <Warmup Duration="1800" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="1800" OnPower="1.02" Cadence="100" OffDuration="600" OffPower="0.55"/>
    <Cooldown Duration="1800" PowerLow="0.70" PowerHigh="0.50"/>
"""),
            create_workout("W02 Fri - Pyramidal Easy", """• Duration: 2-2.5 hours Z2

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
            create_workout("W02 Sat - Long Pyramidal Ride with Threshold Blocks", """• STRUCTURE:
First 2.5 hours Z2 → 4x20 min @ 100-105% FTP (8 min easy) in hours 3-6 → Final hour Z2

• GOAT Integration: Threshold when fatigued = race-specific.

• CADENCE WORK: Mix cadences on threshold blocks.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="8100" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="4" OnDuration="1200" OnPower="1.02" Cadence="100" OffDuration="480" OffPower="0.55"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
            create_workout("W02 Sun - Long Pyramidal Easy + Max Strength", """• Duration: 5-6 hours Z2 + 60 min strength

• Strength: Heavy squats, deadlifts (5x5 heavy)

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Heavy squats, deadlifts (5x5 heavy). Max strength phase. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="18000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
        ],
        "Durability": [
            create_workout("W02 Mon - Rest DURABILITY BLOCK", """• Weeks 2-3 implement YOUR chosen limiter block while maintaining pyramidal base volume. This is GOAT's power: MOST training stays pyramidal (sustainable), but we ADD concentrated stimulus on your limiter. You're not abandoning base—you're sharpening one capacity within base framework. Durability block selected.

• WEEK PREVIEW: Durability concentrated loading. Tuesday has G-Spot volume. Thursday has tempo volume. Saturday is peak volume ride (7-8 hours). This is peak durability stimulus—heavy legs, sustained power when tired.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
            create_workout("W02 Tue - G-Spot Volume (Block Focus)", """• STRUCTURE:
30 min warmup → 5x20 min @ 87-92% FTP (7 min easy) → 30 min cooldown

• Monitoring: HRV check. G-Spot is "hard enough" for adaptation, "easy enough" for repeatability. KPI: Decoupling—is HR drifting relative to power within intervals?

• CADENCE WORK: Mix cadences—intervals 1, 3, 5 at high cadence (100+ rpm), intervals 2, 4 at low cadence (40-60 rpm).""", """    <Warmup Duration="1800" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="5" OnDuration="1200" OnPower="0.895" Cadence="100" OffDuration="420" OffPower="0.55"/>
    <Cooldown Duration="1800" PowerLow="0.70" PowerHigh="0.50"/>
"""),
            create_workout("W02 Wed - Pyramidal Easy", """• Duration: 2.5-3 hours Z2""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="9000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
            create_workout("W02 Thu - Tempo Volume (Block Focus)", """• STRUCTURE:
30 min warmup → 4x30 min @ 80-85% FTP (10 min easy) → 30 min cooldown

• KPI: Sustained power at upper aerobic zone—building endurance ceiling.

• CADENCE WORK: Mix cadences on tempo blocks.""", """    <Warmup Duration="1800" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="4" OnDuration="1800" OnPower="0.825" Cadence="100" OffDuration="600" OffPower="0.55"/>
    <Cooldown Duration="1800" PowerLow="0.70" PowerHigh="0.50"/>
"""),
            create_workout("W02 Fri - Pyramidal Easy", """• Duration: 2-2.5 hours Z2

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
            create_workout("W02 Sat - Peak Volume Ride (Block Focus)", """• STRUCTURE:
First 3 hours Z2 → 5x30 min @ 85-95% FTP (varied, 10 min easy) in hours 4-7 → Final hour Z2

• GOAT Integration: Massive volume with sustained efforts = direct durability training. KPI: Power decay in final hours, fueling tolerance.

• CADENCE WORK: Mix cadences on sustained efforts.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="10800" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="5" OnDuration="1800" OnPower="0.90" Cadence="100" OffDuration="600" OffPower="0.55"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
            create_workout("W02 Sun - Long Pyramidal Easy + Durability Strength", """• Duration: 5-6 hours Z2 + 50-60 min strength

• Strength: Higher rep work—goblet squats, step-ups, planks (3x15-20)

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Higher rep work—goblet squats, step-ups, planks (3x15-20). Durability strength phase. Higher reps, lower weight for muscular endurance. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="18000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
        ]
    }
})

# Note: Week 3 would follow similar structure for each block
# Weeks 4, 5-8, 9-12 are standard (not block-specific)

template = {
    "plan_metadata": plan_metadata,
    "weeks": weeks,
    "default_modifications": {
        "goat_philosophy": {
            "enabled": True,
            "description": "GOAT (Gravel Optimized Adaptive Training) - Integrated system combining pyramidal base, polarized weeks, limiter-focused blocks, G-Spot efficiency, and multi-signal autoregulation",
            "components": {
                "pyramidal_base": "80/10/10 - Most time in Z2, moderate Z3/tempo, small Z4+",
                "polarized_micro_cycles": "80/20 - Some weeks shift to pure easy/hard split",
                "limiter_focused_blocks": "2-4 week concentrated loading on specific weakness",
                "gspot_efficiency": "87-92% FTP for time-crunched efficiency",
                "multi_signal_autoregulation": "HRV + RPE + CTL/TSB + power durability + HR drift"
            }
        },
        "cadence_work": {
            "enabled": True,
            "base_period": "High cadence (100+ rpm seated) and low cadence/torque (40-60 rpm seated, big gear) on all intervals",
            "build_period": "Mix high/low cadence + rhythm intervals (2 min Z3 + 1 min Z4 patterns) + loaded intervals (1 min Z5/Z6 → settle into Z3)",
            "description": "Teaches power production in different ways, foundation for changing pace"
        },
        "rhythm_intervals": {
            "enabled": True,
            "weeks": [6, 7, 9, 10],
            "description": "Alternating patterns: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 4-6, continuous"
        },
        "loaded_intervals": {
            "enabled": True,
            "weeks": [9, 10],
            "description": "1 min Z5/Z6 (high cadence, seated) → settle into 11-19 min Z3 (self-selected cadence). Simulates race starts and surges."
        },
        "gspot_terminology": {
            "enabled": True,
            "replaces": "Sweet Spot",
            "range": "87-92% FTP"
        },
        "strength_training": {
            "enabled": False,
            "note": "Athlete performs own strength program. Suggested on lighter training days. GOAT integrates strength year-round: max strength in base, explosive in VO2 phases, stability in threshold phases, durability in volume blocks."
        },
        "monday_week_preview": {
            "enabled": True,
            "description": "Monday rest days include week preview with key workouts, GOAT philosophy reminders, multi-signal monitoring guidance, and elite performance tips"
        },
        "rest_day_tss_limit": 30,
        "rest_day_duration_limit_hours": 1,
        "multi_signal_monitoring": {
            "enabled": True,
            "signals": ["HRV", "RPE", "CTL/TSB", "power durability", "HR drift", "sleep quality", "resting HR", "subjective readiness"],
            "description": "GOAT requires sophisticated monitoring - athlete must track multiple signals and adjust training accordingly"
        }
    }
}

output_path = "/Users/mattirowe/Documents/Gravel Landing Page Project/current/plans/15. Podium Advanced GOAT (12 weeks)/template.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(template, f, indent=2, ensure_ascii=False)

print(f"✅ Template structure created: {output_path}")
print(f"   Plan: {plan_metadata['name']}")
print(f"   Duration: {plan_metadata['duration_weeks']} weeks")
print(f"   Philosophy: {plan_metadata['philosophy']}")
print(f"   Week 1: Complete (7 workouts)")
print(f"   Week 2: Complete for all 3 blocks (21 workouts)")
print(f"   Note: Week 3, 4, 5-8, 9-12 need to be populated")
print(f"   This is a complex plan with GOAT philosophy and multi-signal autoregulation")

