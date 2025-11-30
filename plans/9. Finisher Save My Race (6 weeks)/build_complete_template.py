#!/usr/bin/env python3
"""
Build complete JSON template for FINISHER SAVE MY RACE (6 weeks)
Sweet Spot/Threshold with Changing Pace philosophy
Three tracks based on Week 1 assessment: Aggressive, Balanced, Foundation
All workouts (6 weeks, with 3 track options for Weeks 2-4)
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
    desc = re.sub(r'88-90% FTP', '87-90% FTP', desc)
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
    "name": "FINISHER SAVE MY RACE",
    "duration_weeks": 6,
    "philosophy": "G-Spot/Threshold (Emergency Sharpening)",
    "target_hours": "10-12",
    "target_athlete": "Emergency situation, already has base fitness, needs final sharpening",
    "goal": "Convert existing base into race-ready fitness in compressed timeframe"
}

weeks = []

# WEEK 1: Rapid Assessment & Threshold Baseline
weeks.append({
    "week_number": 1,
    "focus": "Rapid Assessment & Threshold Baseline",
    "volume_percent": 70,
    "volume_hours": "7-8.5",
    "workouts": [
        create_workout("W01 Mon - Rest", """• Welcome to emergency mode with compressed timeline. You have 6 weeks and 10-12 hours weekly. Unlike true beginners, you already have base fitness—you've been riding consistently but need race-specific sharpening. G-Spot (87-92% FTP) and Threshold (95-105% FTP) are your weapons—they deliver maximum race readiness in minimum time. This isn't about building base—that takes months. This is about sharpening what you have. Week 1: assessment. Weeks 2-4: concentrated G-Spot/Threshold loading. Week 5: light recovery/sharpening. Week 6: taper/race.

• WEEK PREVIEW: Assessment week. Tuesday has FTP test + G-Spot sustainability check. Thursday has threshold assessment (race pace check). This week determines which track you follow in Weeks 2-4: Aggressive (strong performance), Balanced (moderate performance), or Foundation (weak performance). Be honest with yourself.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W01 Tue - FTP Test + G-Spot Assessment", """• STRUCTURE:
20 min warmup → 5 min all-out → 10 min recovery → 20 min max sustained effort → 15 min easy → 20 min @ 87-90% FTP (assess sustainability, monitor RPE) → 10 min cooldown

• FTP test sets your zones (20-min avg × 0.95 = FTP). Then G-Spot sustainability check—does 87-90% feel manageable for 20 minutes? If yes, your base is solid. If it feels unsustainably hard, you might be less prepared than you think. Write down FTP and G-Spot feel. This determines training approach for next 5 weeks.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <SteadyState Duration="300" Power="1.20"/>
    <SteadyState Duration="600" Power="0.55"/>
    <SteadyState Duration="1200" Power="1.05"/>
    <SteadyState Duration="900" Power="0.55"/>
    <SteadyState Duration="1200" Power="0.89"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W01 Wed - Easy Endurance", """• Full recovery from testing. Easy conversational pace. Your body is processing yesterday's maximal effort.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W01 Thu - Threshold Assessment", """• STRUCTURE:
20 min warmup → 2x15 min @ 100-105% FTP (7 min easy between) → 15 min cooldown

• Can you hold race pace (just above FTP) for two 15-minute blocks? This reveals your current race readiness. If power is stable + RPE manageable = good fitness foundation. If power fades >5% or feels unsustainably hard = need more foundational work than 6 weeks allows (but we'll do our best). Record power consistency, HR response, and perceived effort.

• CADENCE WORK: First interval at high cadence (100+ rpm seated), second at low cadence (40-60 rpm seated, big gear).""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="900" OnPower="1.02" Cadence="100" OffDuration="420" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W01 Fri - Rest or Easy Spin", """• Optional: 30-45 min Z1 (50-60% FTP)

• Rest or very easy spin. Two hard tests this week. Your body needs recovery.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W01 Sat - Moderate Endurance Ride", """• STRUCTURE:
60 min easy → 3x10 min @ 80-85% FTP (4 min easy between) → Final 30 min easy

• Building weekly volume. Tempo touches assess your upper aerobic zone without crushing you. This is maintenance volume—keeping base while we sharpen threshold. Eat 50-60g carbs per hour.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3000" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="600" OnPower="0.82" Cadence="88" OffDuration="240" OffPower="0.55"/>
    <SteadyState Duration="1500" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W01 Sun - Easy Endurance", """• Easy recovery. End of assessment week. You should have clear picture of current fitness.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 2-4: Three Tracks
# AGGRESSIVE TRACK
aggressive_track = {
    "track_name": "Aggressive Track",
    "description": "Strong Week 1 Performance - Ready for aggressive sharpening",
    "weeks": []
}

# Week 2 Aggressive
aggressive_track["weeks"].append({
    "week_number": 2,
    "focus": "Concentrated Sharpening - Aggressive",
    "volume_percent": 85,
    "volume_hours": "8.5-10",
    "workouts": [
        create_workout("W02 Mon - Rest", """• Weeks 2-4 are your concentrated sharpening block. THREE weeks of focused G-Spot and Threshold work. This is where race fitness comes from in compressed timeline. You'll do 2-3 quality sessions per week. By end of Week 4 you should feel threshold-specific fatigue (race pace feels harder). That's adaptation. Week 5 recovery allows conversion to performance.

• WEEK PREVIEW: Aggressive track selected (strong Week 1 performance). Tuesday has G-Spot intervals (4x15 min). Thursday has threshold intervals (3x12 min). Saturday has long G-Spot ride (3x20 min). This is aggressive loading—you're ready for it.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W02 Tue - G-Spot Intervals", """• STRUCTURE:
15 min warmup → 4x15 min @ 87-92% FTP (5 min easy between) → 15 min cooldown

• 60 cumulative minutes at G-Spot. "Uncomfortably sustainable"—harder than tempo, easier than threshold. This is time-efficient race preparation. Control breathing, stay smooth.

• CADENCE WORK: Alternate high cadence (100+ rpm seated) and low cadence (40-60 rpm seated, big gear) on intervals.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="4" OnDuration="900" OnPower="0.90" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W02 Wed - Easy Endurance", """• Easy day. Recovery between quality sessions.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W02 Thu - Threshold Intervals", """• STRUCTURE:
15 min warmup → 3x12 min @ 100-105% FTP (6 min easy between) → 15 min cooldown

• Race pace work. Breathing labored but rhythmic. This is what gravel racing feels like—sustained near-max effort.

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="720" OnPower="1.02" Cadence="100" OffDuration="360" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W02 Fri - Rest or Easy Spin", """• Optional: 30-45 min Z1

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W02 Sat - Long G-Spot Ride", """• STRUCTURE:
30 min easy → 3x20 min @ 87-92% FTP (7 min easy between) → Final 30-45 min easy

• G-Spot embedded in longer ride. Building race-specific endurance. Eat 60g carbs/hour.

• CADENCE WORK: Mix cadences on G-Spot efforts—some high, some low.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1500" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="1200" OnPower="0.90" Cadence="100" OffDuration="420" OffPower="0.55"/>
    <SteadyState Duration="1800" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W02 Sun - Easy Endurance", """• Easy recovery. Building volume without intensity.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# Week 3 Aggressive
aggressive_track["weeks"].append({
    "week_number": 3,
    "focus": "Peak Loading - Aggressive",
    "volume_percent": 100,
    "volume_hours": "10-12",
    "workouts": [
        create_workout("W03 Mon - Rest", """• Peak loading week. Biggest volume and intensity. By Sunday you should feel accumulated fatigue—that's expected. Week 4 sustains this load, then Week 5 recovery.

• WEEK PREVIEW: Peak loading week. Tuesday has extended G-Spot (5x15 min—75 minutes cumulative). Thursday has extended threshold (2x20 min). Saturday has long race simulation (4x15 min varied intensity). This is your biggest week.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W03 Tue - Extended G-Spot", """• STRUCTURE:
15 min warmup → 5x15 min @ 87-92% FTP (5 min easy between) → 15 min cooldown

• 75 cumulative minutes at G-Spot. Peak volume. Break into 5-min segments mentally.

• CADENCE WORK: Alternate high and low cadence. Intervals 1, 3, 5 at high cadence (100+ rpm), intervals 2, 4 at low cadence (40-60 rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="5" OnDuration="900" OnPower="0.90" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W03 Wed - Easy Endurance", """• Easy day. Recovery between quality sessions.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W03 Thu - Extended Threshold", """• STRUCTURE:
15 min warmup → 2x20 min @ 100-105% FTP (8 min easy between) → 15 min cooldown

• Classic 2x20 at threshold. Hard but sustainable. This is race pace for 40 cumulative minutes.

• CADENCE WORK: First interval at high cadence (100+ rpm), second at low cadence (40-60 rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="1200" OnPower="1.02" Cadence="100" OffDuration="480" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W03 Fri - Rest or Easy Spin", """• Optional: 30-45 min Z1

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W03 Sat - Long Race Simulation", """• STRUCTURE:
45 min easy → 4x15 min @ 90-100% FTP (varied, 6 min easy between) → Final 45-60 min easy

• Peak long ride. Variable race-intensity efforts when tired. Eat 70g carbs/hour. Practice race fueling.

• RHYTHM INTERVALS: For some efforts, try rhythm pattern: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 4, continuous.

• CADENCE WORK: Mix cadences and use rhythm patterns.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2400" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="4" OnDuration="900" OnPower="0.95" Cadence="100" OffDuration="360" OffPower="0.55"/>
    <SteadyState Duration="2700" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W03 Sun - Easy Endurance", """• Easy recovery. End of peak week.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# Week 4 Aggressive
aggressive_track["weeks"].append({
    "week_number": 4,
    "focus": "Sustained Loading - Aggressive",
    "volume_percent": 95,
    "volume_hours": "9.5-11.5",
    "workouts": [
        create_workout("W04 Mon - Rest", """• Sustained loading week. Maintaining high volume and intensity. By Sunday you should feel threshold-specific fatigue. Week 5 recovery allows conversion to performance.

• WEEK PREVIEW: Sustained loading week. Tuesday has G-Spot + openers. Thursday has threshold progression (3x15 min). Saturday has final long ride (3x20 min race-pace efforts). One more week of loading, then recovery.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W04 Tue - G-Spot + Openers", """• STRUCTURE:
15 min warmup → 3x15 min @ 87-92% FTP (5 min easy between) → 10 min easy → 4x1 min @ 105-110% FTP (2 min easy between) → 10 min cooldown

• G-Spot maintains base, openers add sharpness. The 1-min efforts keep neuromuscular system responsive.

• CADENCE WORK: Mix cadences on G-Spot intervals. Openers at high cadence (100+ rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="3" OnDuration="900" OnPower="0.90" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="600" Power="0.65" Cadence="85"/>
    <IntervalsT Repeat="4" OnDuration="60" OnPower="1.08" Cadence="100" OffDuration="120" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W04 Wed - Easy Endurance", """• Easy day. Recovery between quality sessions.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W04 Thu - Threshold Progression", """• STRUCTURE:
15 min warmup → 3x15 min @ 100-105% FTP (7 min easy between) → 15 min cooldown

• Longer threshold blocks. 45 cumulative minutes at race pace. Should feel controlled—you've built this fitness.

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected or rhythm pattern.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="900" OnPower="1.02" Cadence="100" OffDuration="420" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W04 Fri - Rest", """• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W04 Sat - Final Long Ride", """• STRUCTURE:
30 min easy → 3x20 min @ 90-100% FTP (8 min easy between) → Final 30-45 min easy

• Final big ride before taper/recovery week. Race-pace efforts. Eat 60-70g carbs/hour.

• LOADED INTERVALS: For one interval, try loaded pattern: 1 min Z5/Z6 (high cadence, seated) → settle into 19 min Z3 (self-selected cadence). This simulates race starts.

• CADENCE WORK: Mix cadences or use loaded/rhythm patterns.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1500" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="1200" OnPower="0.95" Cadence="100" OffDuration="480" OffPower="0.55"/>
    <SteadyState Duration="1800" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W04 Sun - Easy Endurance", """• Easy recovery. End of loading block.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# BALANCED TRACK
balanced_track = {
    "track_name": "Balanced Track",
    "description": "Moderate Week 1 Performance - Balanced approach",
    "weeks": []
}

# Week 2 Balanced
balanced_track["weeks"].append({
    "week_number": 2,
    "focus": "Concentrated Sharpening - Balanced",
    "volume_percent": 85,
    "volume_hours": "8.5-10",
    "workouts": [
        create_workout("W02 Mon - Rest", """• Weeks 2-4 are your concentrated sharpening block. THREE weeks of focused G-Spot and Threshold work. This is where race fitness comes from in compressed timeline. You'll do 2-3 quality sessions per week. By end of Week 4 you should feel threshold-specific fatigue (race pace feels harder). That's adaptation. Week 5 recovery allows conversion to performance.

• WEEK PREVIEW: Balanced track selected (moderate Week 1 performance). Tuesday has G-Spot foundation (4x12 min). Thursday has threshold introduction (3x10 min). Saturday has G-Spot endurance (3x15 min). Progressive loading approach.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W02 Tue - G-Spot Foundation", """• STRUCTURE:
15 min warmup → 4x12 min @ 87-92% FTP (5 min easy between) → 15 min cooldown

• Building G-Spot tolerance. 48 minutes cumulative. If intervals feel hard, this is appropriate load.

• CADENCE WORK: Alternate high cadence (100+ rpm seated) and low cadence (40-60 rpm seated, big gear) on intervals.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="4" OnDuration="720" OnPower="0.90" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W02 Wed - Easy Endurance", """• Easy day. Recovery between quality sessions.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W02 Thu - Threshold Introduction", """• STRUCTURE:
15 min warmup → 3x10 min @ 100-105% FTP (6 min easy between) → 15 min cooldown

• Shorter threshold blocks. Building race pace tolerance progressively.

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="600" OnPower="1.02" Cadence="100" OffDuration="360" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W02 Fri - Rest or Easy Spin", """• Optional: 30-45 min Z1

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W02 Sat - G-Spot Endurance", """• STRUCTURE:
30 min easy → 3x15 min @ 87-92% FTP (6 min easy between) → Final 60 min easy

• G-Spot in longer ride. Building endurance at sustainable intensity.

• CADENCE WORK: Mix cadences on G-Spot efforts—some high, some low.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1500" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="900" OnPower="0.90" Cadence="100" OffDuration="360" OffPower="0.55"/>
    <SteadyState Duration="3000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W02 Sun - Easy Endurance", """• Easy recovery. Building volume without intensity.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# Week 3 Balanced
balanced_track["weeks"].append({
    "week_number": 3,
    "focus": "Progressive Loading - Balanced",
    "volume_percent": 100,
    "volume_hours": "10-12",
    "workouts": [
        create_workout("W03 Mon - Rest", """• Progressive loading week. Building on Week 2 foundation. By Sunday you should feel accumulated fatigue—that's expected. Week 4 consolidates, then Week 5 recovery.

• WEEK PREVIEW: Progressive loading week. Tuesday has extended G-Spot (4x15 min). Thursday has threshold progression (3x12 min). Saturday has long ride with mixed efforts (G-Spot + threshold). Building toward peak.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W03 Tue - Extended G-Spot", """• STRUCTURE:
15 min warmup → 4x15 min @ 87-92% FTP (5 min easy between) → 15 min cooldown

• 60 minutes cumulative at G-Spot. Progression from Week 2.

• CADENCE WORK: Alternate high and low cadence. Intervals 1, 3 at high cadence (100+ rpm), intervals 2, 4 at low cadence (40-60 rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="4" OnDuration="900" OnPower="0.90" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W03 Wed - Easy Endurance", """• Easy day. Recovery between quality sessions.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W03 Thu - Threshold Progression", """• STRUCTURE:
15 min warmup → 3x12 min @ 100-105% FTP (6 min easy between) → 15 min cooldown

• Longer threshold blocks. Building toward race pace sustainability.

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="720" OnPower="1.02" Cadence="100" OffDuration="360" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W03 Fri - Rest", """• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W03 Sat - Long Ride with Mixed Efforts", """• STRUCTURE:
45 min easy → 2x20 min @ 87-92% FTP (8 min easy between) → 30 min easy → 2x10 min @ 95-100% FTP (5 min easy between) → Final 30 min easy

• G-Spot when fresh, threshold when fatigued. Race simulation. Eat 60-70g carbs/hour.

• RHYTHM INTERVALS: For threshold blocks, try rhythm pattern: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 3, continuous.

• CADENCE WORK: Mix cadences and use rhythm patterns.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2400" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="2" OnDuration="1200" OnPower="0.90" Cadence="100" OffDuration="480" OffPower="0.55"/>
    <SteadyState Duration="1500" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="2" OnDuration="600" OnPower="0.98" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="1500" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W03 Sun - Easy Endurance", """• Easy recovery. End of progressive loading week.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# Week 4 Balanced
balanced_track["weeks"].append({
    "week_number": 4,
    "focus": "Consolidation - Balanced",
    "volume_percent": 95,
    "volume_hours": "9.5-11.5",
    "workouts": [
        create_workout("W04 Mon - Rest", """• Consolidation week. Maintaining fitness while preparing for recovery. By Sunday you should feel threshold-specific fatigue. Week 5 recovery allows conversion to performance.

• WEEK PREVIEW: Consolidation week. Tuesday has G-Spot maintenance (4x12 min). Thursday has threshold development (2x15 min). Saturday has final long ride (3x15 min moderate race-pace efforts). One more week of loading, then recovery.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W04 Tue - G-Spot Maintenance", """• STRUCTURE:
15 min warmup → 4x12 min @ 87-92% FTP (5 min easy between) → 15 min cooldown

• Maintaining G-Spot fitness. Should feel controlled.

• CADENCE WORK: Mix cadences—intervals 1, 3 at high cadence (100+ rpm), intervals 2, 4 at low cadence (40-60 rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="4" OnDuration="720" OnPower="0.90" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W04 Wed - Easy Endurance", """• Easy day. Recovery between quality sessions.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W04 Thu - Threshold Development", """• STRUCTURE:
15 min warmup → 2x15 min @ 100-105% FTP (8 min easy between) → 15 min cooldown

• Two 15-minute blocks. 30 cumulative minutes at race pace.

• CADENCE WORK: First interval at high cadence (100+ rpm), second at low cadence (40-60 rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="900" OnPower="1.02" Cadence="100" OffDuration="480" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W04 Fri - Rest", """• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W04 Sat - Final Long Ride", """• STRUCTURE:
30 min easy → 3x15 min @ 90-95% FTP (6 min easy between) → Final 45 min easy

• Final preparation ride. Moderate race-pace efforts. Eat 60g carbs/hour.

• CADENCE WORK: Mix cadences on efforts.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1500" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="900" OnPower="0.93" Cadence="100" OffDuration="360" OffPower="0.55"/>
    <SteadyState Duration="2400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W04 Sun - Easy Endurance", """• Easy recovery. End of loading block.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# FOUNDATION TRACK
foundation_track = {
    "track_name": "Foundation Track",
    "description": "Weak Week 1 Performance - Focus on foundation building",
    "weeks": []
}

# Week 2 Foundation
foundation_track["weeks"].append({
    "week_number": 2,
    "focus": "Concentrated Sharpening - Foundation",
    "volume_percent": 85,
    "volume_hours": "8.5-10",
    "workouts": [
        create_workout("W02 Mon - Rest", """• Weeks 2-4 are your concentrated sharpening block. THREE weeks of focused G-Spot and Threshold work. This is where race fitness comes from in compressed timeline. You'll do 2-3 quality sessions per week. By end of Week 4 you should feel threshold-specific fatigue (race pace feels harder). That's adaptation. Week 5 recovery allows conversion to performance.

• WEEK PREVIEW: Foundation track selected (weak Week 1 performance). Tuesday has G-Spot building (4x10 min—shorter intervals). Thursday has tempo work (building foundation before threshold). Saturday has steady endurance (3x12 min sustainable intensity). Building foundation first.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W02 Tue - G-Spot Building", """• STRUCTURE:
15 min warmup → 4x10 min @ 87-92% FTP (5 min easy between) → 10 min cooldown

• Shorter G-Spot intervals. Building tolerance before pushing harder.

• CADENCE WORK: Alternate high cadence (100+ rpm seated) and low cadence (40-60 rpm seated, big gear) on intervals.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="4" OnDuration="600" OnPower="0.90" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W02 Wed - Easy Endurance", """• Easy day. Recovery between quality sessions.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W02 Thu - Tempo Work", """• STRUCTURE:
15 min warmup → 3x12 min @ 80-85% FTP (5 min easy between) → 15 min cooldown

• Upper aerobic work. Building foundation before true threshold work.

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="3" OnDuration="720" OnPower="0.82" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W02 Fri - Rest", """• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W02 Sat - Steady Endurance", """• STRUCTURE:
30 min easy → 3x12 min @ 80-88% FTP (5 min easy between) → Final 45 min easy

• Building aerobic endurance with sustainable intensity.

• CADENCE WORK: Mix cadences on efforts.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1500" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="720" OnPower="0.84" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="2400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W02 Sun - Easy Endurance", """• Easy recovery. Building volume without intensity.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# Week 3 Foundation
foundation_track["weeks"].append({
    "week_number": 3,
    "focus": "Progressive Building - Foundation",
    "volume_percent": 100,
    "volume_hours": "10-12",
    "workouts": [
        create_workout("W03 Mon - Rest", """• Progressive building week. Building on Week 2 foundation. By Sunday you should feel accumulated fatigue—that's expected. Week 4 builds readiness, then Week 5 recovery.

• WEEK PREVIEW: Progressive building week. Tuesday has G-Spot progression (4x12 min—longer than Week 2). Thursday has light threshold introduction (first true threshold work). Saturday has long endurance (3x15 min sustainable efforts). Building fitness progressively.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W03 Tue - G-Spot Progression", """• STRUCTURE:
15 min warmup → 4x12 min @ 87-92% FTP (5 min easy between) → 15 min cooldown

• Longer G-Spot intervals. Building fitness.

• CADENCE WORK: Alternate high and low cadence. Intervals 1, 3 at high cadence (100+ rpm), intervals 2, 4 at low cadence (40-60 rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="4" OnDuration="720" OnPower="0.90" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W03 Wed - Easy Endurance", """• Easy day. Recovery between quality sessions.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W03 Thu - Light Threshold Introduction", """• STRUCTURE:
15 min warmup → 3x10 min @ 95-100% FTP (6 min easy between) → 15 min cooldown

• First true threshold work. Lower end of zone if needed.

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="600" OnPower="0.98" Cadence="100" OffDuration="360" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W03 Fri - Rest", """• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W03 Sat - Long Endurance", """• STRUCTURE:
30 min easy → 3x15 min @ 85-90% FTP (5 min easy between) → Final 60 min easy

• Building durability with sustainable efforts.

• CADENCE WORK: Mix cadences on efforts.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1500" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="900" OnPower="0.88" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="3000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W03 Sun - Easy Endurance", """• Easy recovery. End of progressive building week.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# Week 4 Foundation
foundation_track["weeks"].append({
    "week_number": 4,
    "focus": "Readiness Building - Foundation",
    "volume_percent": 95,
    "volume_hours": "9.5-11.5",
    "workouts": [
        create_workout("W04 Mon - Rest", """• Readiness building week. Building toward race readiness. By Sunday you should feel threshold-specific fatigue. Week 5 recovery allows conversion to performance.

• WEEK PREVIEW: Readiness building week. Tuesday has G-Spot work (3x15 min). Thursday has threshold work (2x12 min). Saturday has long ride (2x20 min G-Spot). Building race readiness progressively.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W04 Tue - G-Spot Work", """• STRUCTURE:
15 min warmup → 3x15 min @ 87-92% FTP (5 min easy between) → 15 min cooldown

• Building G-Spot fitness. Should feel more manageable than Week 2.

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="3" OnDuration="900" OnPower="0.90" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W04 Wed - Easy Endurance", """• Easy day. Recovery between quality sessions.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W04 Thu - Threshold Work", """• STRUCTURE:
15 min warmup → 2x12 min @ 100-105% FTP (7 min easy between) → 15 min cooldown

• Race pace development. Two 12-minute blocks.

• CADENCE WORK: First interval at high cadence (100+ rpm), second at low cadence (40-60 rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="720" OnPower="1.02" Cadence="100" OffDuration="420" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W04 Fri - Rest", """• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W04 Sat - Long Ride", """• STRUCTURE:
30 min easy → 2x20 min @ 87-92% FTP (8 min easy between) → Final 45 min easy

• G-Spot in longer context. Building race readiness.

• CADENCE WORK: Mix cadences on efforts.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1500" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="2" OnDuration="1200" OnPower="0.90" Cadence="100" OffDuration="480" OffPower="0.55"/>
    <SteadyState Duration="2400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W04 Sun - Easy Endurance", """• Easy recovery. End of loading block.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 5: Recovery & Final Sharpening
weeks.append({
    "week_number": 5,
    "focus": "Recovery & Final Sharpening",
    "volume_percent": 70,
    "volume_hours": "7-8.5",
    "workouts": [
        create_workout("W05 Mon - Rest", """• Recovery week with sharpening. You just did 3 weeks of concentrated G-Spot/Threshold work. Week 5 reduces volume while adding race-specific openers. By Sunday you should feel fresh and sharp—ready for race week.

• WEEK PREVIEW: Recovery week. Wednesday has light G-Spot touch (maintaining fitness). Friday has race openers (race pace reminder + short bursts). Saturday has moderate endurance with touches (final preparation). Volume drops, intensity stays sharp.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W05 Tue - Easy Endurance", """• Easy recovery ride. Enjoying lower training stress.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W05 Wed - Light G-Spot Touch", """• STRUCTURE:
15 min warmup → 3x8 min @ 87-92% FTP (4 min easy between) → 10 min cooldown

• Reduced G-Spot volume. Maintaining fitness without fatigue.

• CADENCE WORK: Mix cadences—one high, one low, one self-selected.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="3" OnDuration="480" OnPower="0.90" Cadence="90" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W05 Thu - Easy Endurance", """• Easy day. Recovery continues.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W05 Fri - Race Openers", """• STRUCTURE:
15 min warmup → 2x10 min @ 95-100% FTP (5 min easy between) → 10 min easy → 4x1 min @ 105-110% FTP (2 min easy between) → 10 min cooldown

• Race pace reminder plus short bursts for sharpness. Should feel controlled and powerful.

• CADENCE WORK: High cadence on all efforts (100+ rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="2" OnDuration="600" OnPower="0.98" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="600" Power="0.65" Cadence="85"/>
    <IntervalsT Repeat="4" OnDuration="60" OnPower="1.08" Cadence="100" OffDuration="120" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W05 Sat - Moderate Endurance with Touches", """• STRUCTURE:
30 min easy → 3x10 min @ 90-95% FTP (5 min easy between) → Final 45 min easy

• Shorter ride with race-intensity touches. Final preparation before race week.

• CADENCE WORK: Mix cadences on efforts.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1500" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="600" OnPower="0.93" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="2400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W05 Sun - Easy Endurance", """• Easy recovery. You should feel increasingly fresh and ready.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4500" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 6: Race Week
weeks.append({
    "week_number": 6,
    "focus": "Race Week",
    "volume_percent": 40,
    "volume_hours": "4-6",
    "workouts": [
        create_workout("W06 Mon - Rest", """• Race week. Volume drops dramatically. You converted base fitness into race readiness in 5 weeks through concentrated G-Spot/Threshold work. You're not perfectly prepared—6 weeks isn't enough for that—but you're RACE READY. Now execute smart pacing and aggressive fueling.

• WEEK PREVIEW: Race week! Wednesday has final openers (sharpness check). Thursday is easy or rest. Friday is pre-race shake-out (if racing Sunday). Saturday/Sunday: RACE DAY!

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W06 Tue - Easy Endurance", """• Easy spin. Just moving legs. No stress.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2700" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W06 Wed - Final Openers", """• STRUCTURE:
15 min easy → 3x4 min @ 95-100% FTP (3 min easy between) → 5 min easy → 3x90sec @ 105-110% FTP (2 min easy between) → 3x30sec @ 115% FTP (90sec easy between) → 10 min easy

• Final sharpness check. Should feel powerful and snappy. If legs feel dead, skip the 30-second efforts and just do 4-min + 90-sec efforts.

• CADENCE WORK: High cadence on all efforts (100+ rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="3" OnDuration="240" OnPower="0.98" Cadence="100" OffDuration="180" OffPower="0.55"/>
    <SteadyState Duration="300" Power="0.65" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="90" OnPower="1.08" Cadence="100" OffDuration="120" OffPower="0.55"/>
    <IntervalsT Repeat="3" OnDuration="30" OnPower="1.15" Cadence="100" OffDuration="90" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W06 Thu - Easy Endurance or Rest", """• Optional: 30-45 min Z2

• If race is Sunday, easy spin. If race is Saturday, rest completely.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W06 Fri - Pre-Race Shake-Out (if racing Sunday)", """• STRUCTURE:
15 min easy → 2x3 min @ race pace (2 min easy between) → 2x90sec @ 105% FTP (2 min easy between) → 2x30sec @ 110% FTP (90sec easy between) → 10 min easy

• Final ride before race. Legs should feel fresh and powerful. Check bike one last time. Visualize race execution—conservative start, steady middle, finish strong.

• CADENCE WORK: High cadence on all efforts (100+ rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="2" OnDuration="180" OnPower="0.98" Cadence="100" OffDuration="120" OffPower="0.55"/>
    <IntervalsT Repeat="2" OnDuration="90" OnPower="1.05" Cadence="100" OffDuration="120" OffPower="0.55"/>
    <IntervalsT Repeat="2" OnDuration="30" OnPower="1.10" Cadence="100" OffDuration="90" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W06 Sat - Race Day or Rest", """• If racing Saturday: EXECUTE YOUR PLAN

• If racing Sunday: Rest or 30-45 min easy Z2 with 2x30sec openers

• Notes: If racing today—START CONSERVATIVELY (you only had 6 weeks of sharpening, not full preparation), fuel from mile 1 (50-60g carbs/hour minimum), pace yourself, finish strong. G-Spot/Threshold work built the fitness—now be smart with it.""", """    <FreeRide Duration="60"/>
"""),
        create_workout("W06 Sun - Race Day or Recovery", """• If racing Sunday: EXECUTE YOUR PLAN

• If raced Saturday: 30-45 min easy recovery spin, celebrate

• Notes: Race day. Conservative start is MANDATORY with compressed prep. Fuel aggressively. Pace conservatively. When it gets hard in final hours, you have the G-Spot/Threshold work—that's what gets you to the finish. Be smart, finish strong.""", """    <FreeRide Duration="60"/>
""")
    ]
})

# Create complete template
template = {
    "plan_metadata": plan_metadata,
    "weeks": weeks,
    "tracks": {
        "aggressive": aggressive_track,
        "balanced": balanced_track,
        "foundation": foundation_track
    },
    "default_modifications": {
        "emergency_plan": {
            "enabled": True,
            "description": "6-week emergency plan for athletes with existing base fitness needing race-specific sharpening",
            "assessment_based": True,
            "tracks": {
                "aggressive": "Strong Week 1 performance - Ready for aggressive sharpening",
                "balanced": "Moderate Week 1 performance - Balanced approach",
                "foundation": "Weak Week 1 performance - Focus on foundation building"
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
            "weeks": [3, 4],
            "description": "Alternating patterns: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 3-4, continuous"
        },
        "loaded_intervals": {
            "enabled": True,
            "weeks": [4],
            "description": "1 min Z5/Z6 (high cadence, seated) → settle into 11-19 min Z3 (self-selected cadence). Simulates race starts and surges."
        },
        "gspot_terminology": {
            "enabled": True,
            "replaces": "Sweet Spot",
            "range": "87-92% FTP"
        },
        "strength_training": {
            "enabled": False,
            "note": "Athlete performs own strength program. Suggested on lighter training days."
        },
        "monday_week_preview": {
            "enabled": True,
            "description": "Monday rest days include week preview with key workouts, assessment reminders, and track-specific guidance"
        },
        "rest_day_tss_limit": 30,
        "rest_day_duration_limit_hours": 1
    }
}

# Save complete template
output_path = "/Users/mattirowe/Documents/Gravel Landing Page Project/current/plans/9. Finisher Save My Race (6 weeks)/template.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(template, f, indent=2, ensure_ascii=False)

print(f"✅ Complete template created: {output_path}")
print(f"   Plan: {plan_metadata['name']}")
print(f"   Duration: {plan_metadata['duration_weeks']} weeks")
print(f"   Philosophy: {plan_metadata['philosophy']}")
print(f"   Total weeks: {len(weeks)}")
total_workouts = sum(len(w['workouts']) for w in weeks)
print(f"   Base workouts: {total_workouts}")
print(f"   Tracks: 3 (Aggressive, Balanced, Foundation)")
print(f"   ✅ All 6 weeks complete!")
print(f"   ✅ G-Spot/Threshold philosophy applied")
print(f"   ✅ Changing Pace philosophy integrated (cadence work, rhythm/loaded intervals)")
print(f"   ✅ Three assessment-based tracks included")

