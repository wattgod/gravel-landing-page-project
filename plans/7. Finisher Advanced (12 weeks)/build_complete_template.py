#!/usr/bin/env python3
"""
Build complete JSON template for FINISHER ADVANCED (12 weeks)
GOAT Method (Gravel Optimized Adaptive Training) with Changing Pace philosophy
All 84 workouts (12 weeks × 7 workouts)
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
    desc = re.sub(r'88-92% FTP', '87-92% FTP', desc)
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
    "name": "FINISHER ADVANCED",
    "duration_weeks": 12,
    "philosophy": "GOAT Method (Gravel Optimized Adaptive Training)",
    "target_hours": "10-12",
    "target_athlete": "Strong cyclist, wants top-third finish, can monitor/adjust training",
    "goal": "Strong finish in top third of field, adaptive multi-method approach"
}

weeks = []

# WEEK 1: Assessment & GOAT Foundation
weeks.append({
    "week_number": 1,
    "focus": "Assessment & GOAT Foundation",
    "volume_percent": 70,
    "volume_hours": "7-8.5",
    "workouts": [
        create_workout("W01 Mon - Rest", """• Welcome to the GOAT Method. This isn't one training philosophy—it's the best of all of them, adapted to you. Pyramidal base weeks. Polarized quality weeks. Limiter-focused blocks. G-Spot when time-crunched. All guided by your signals. This week: baseline testing. FTP test Tuesday. Durability test Saturday. Monitor HRV daily if possible. Let's see what you're working with.

• WEEK PREVIEW: Baseline assessment week. Tuesday has FTP test + durability markers (HR drift check). Thursday introduces G-Spot intervals. Saturday is durability test ride (3.5-4 hours with power assessment). This week tells us your limiters.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W01 Tue - FTP Test + Durability Markers", """• STRUCTURE:
20 min warmup → 5 min all-out → 10 min recovery → 20 min max effort → 10 min easy → 10 min @ 85% of 20-min power (check HR drift) → 10 min cooldown

• FTP test first—pace it right, sustained 20 minutes. Then durability check: hold 85% of your 20-min power for 10 minutes and watch HR drift. If HR rises >5-8 bpm, you have durability limitations. Write everything down. FTP = 20-min avg × 0.95.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <SteadyState Duration="300" Power="1.20"/>
    <SteadyState Duration="600" Power="0.55"/>
    <SteadyState Duration="1200" Power="1.05"/>
    <SteadyState Duration="600" Power="0.55"/>
    <SteadyState Duration="600" Power="0.85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W01 Wed - Easy Endurance", """• Recovery from testing. Keep it conversational. Your body is still processing yesterday's efforts. Easy means easy.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4500" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W01 Thu - G-Spot Introduction", """• STRUCTURE:
15 min warmup → 3x12 min @ 87-92% FTP (5 min easy between) → 10 min cooldown

• First quality session. G-Spot is "uncomfortably sustainable"—harder than endurance, easier than threshold. This is efficient training for time-crunched weeks. Control your breathing, stay seated, keep it smooth.

• CADENCE WORK: Alternate high cadence (100+ rpm seated) and low cadence (40-60 rpm seated, big gear) on intervals. This teaches power production in different ways.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="3" OnDuration="720" OnPower="0.90" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W01 Fri - Rest or Active Recovery", """• Optional: 30-45 min Z1 spin (50-60% FTP)

• Day off if needed. Easy spin if feeling good. Listen to your body—this is GOAT Method principle #1.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W01 Sat - Durability Test Ride", """• STRUCTURE:
First hour Z2 → Hour 2-3: 2x30 min @ 75-80% FTP (10 min easy between), monitor HR drift → Final 30-60 min Z2

• Durability test. During the 30-min blocks, watch HR drift. If HR climbs >8-10 bpm while holding steady power, you need more aerobic base work. If HR stays stable, you have good durability. This tells us how to structure your training. Eat 60g carbs/hour.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3000" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="2" OnDuration="1800" OnPower="0.78" Cadence="88" OffDuration="600" OffPower="0.55"/>
    <SteadyState Duration="2400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W01 Sun - Easy Endurance + Strength", """• GOAT Method integrates year-round strength. Base phase = max strength work. Lift heavy, rest fully between sets. This builds force production that translates to watts on the bike.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Heavy goblet squats, trap bar deadlifts, planks, single-leg RDLs (4x5-6 heavy + 2x10 lighter). Max strength phase. Lift heavy, rest fully between sets (3-5 min). Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 2: Pyramidal Base Building
weeks.append({
    "week_number": 2,
    "focus": "Pyramidal Base Building",
    "volume_percent": 80,
    "volume_hours": "8-9.5",
    "workouts": [
        create_workout("W02 Mon - Rest", """• Based on your Week 1 testing, we're starting with pyramidal base building. Lots of Z2, some tempo, occasional G-Spot. This week follows traditional base principles—build the aerobic engine first. Check your HRV if you're tracking. If HRV is significantly down from baseline, take an extra rest day or make today's ride easier.

• WEEK PREVIEW: Pyramidal base week. Tuesday has tempo intervals (comfortably hard). Thursday progresses G-Spot (longer intervals). Saturday is long aerobic base with tempo work in final 90 minutes. Building the pyramid foundation.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W02 Tue - Tempo Intervals", """• STRUCTURE:
15 min warmup → 4x12 min @ 80-85% FTP (4 min easy between) → 10 min cooldown

• Tempo work—"comfortably hard." You should be able to hold a conversation but prefer not to. This builds your aerobic ceiling without excessive fatigue. Upper pyramidal distribution.

• CADENCE WORK: Mix cadences—intervals 1, 3 at high cadence (100+ rpm), intervals 2, 4 at low cadence (40-60 rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="4" OnDuration="720" OnPower="0.82" Cadence="100" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W02 Wed - Easy Endurance", """• Easy aerobic work. This is the base of your pyramid—massive Z2 volume. Keep it conversational. If you're breathing hard, slow down.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4500" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W02 Thu - G-Spot Progression", """• STRUCTURE:
15 min warmup → 3x15 min @ 87-92% FTP (5 min easy between) → 10 min cooldown

• Longer G-Spot than last week. Mid-pyramid intensity. This is time-efficient fitness building. Stay smooth, control power output, don't spike at interval starts.

• CADENCE WORK: Alternate cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="3" OnDuration="900" OnPower="0.90" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W02 Fri - Rest", """• Rest day. GOAT Method respects recovery. You're building, not destroying.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W02 Sat - Long Aerobic Base", """• STRUCTURE:
Z2 first 2+ hours → 3x10 min @ 75-80% FTP in final 90 minutes (5 min easy between) → Cooldown

• Foundation of pyramidal training—long Z2 with some tempo. Conversational pace first 2+ hours. Light tempo work when fatigued teaches your body to push on tired legs. Eat 60-70g carbs/hour. Practice race nutrition.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="7200" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="600" OnPower="0.78" Cadence="88" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W02 Sun - Easy Endurance + Max Strength", """• Easy ride, heavy strength work. Max strength phase continues. Progressive overload—add 2-5% load if last week felt easy. Full rest between sets (3-5 min).

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Heavy back squats, Romanian deadlifts, weighted planks, Bulgarian splits (4x5-6 heavy). Max strength phase. Full rest between sets (3-5 min). Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 3: Pyramidal Peak + Limiter Block Introduction
weeks.append({
    "week_number": 3,
    "focus": "Pyramidal Peak + Limiter Block Introduction",
    "volume_percent": 90,
    "volume_hours": "9-11",
    "workouts": [
        create_workout("W03 Mon - Rest", """• Biggest base week. By Saturday you should feel accumulated fatigue—that's the point. Week 4 we shift to a limiter block based on your testing and how this week feels. If you're crushing G-Spot but dying on long endurance, we'll target durability. If endurance feels easy but VO2max crushes you, we'll target that. GOAT Method adapts to YOUR limiters.

• WEEK PREVIEW: Biggest base week. Tuesday has classic 2x20 threshold (top of pyramid). Thursday has VO2max assessment (identifies limiters). Saturday is longest ride (4.5-5 hours) with G-Spot efforts when tired—durability test.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W03 Tue - Threshold Development", """• STRUCTURE:
20 min warmup → 2x20 min @ 95-100% FTP (10 min easy between) → 10 min cooldown

• Classic 2x20 threshold. Top of the pyramid—small amount of high intensity. Pace it right. Should finish thinking "I could maybe do one more." This builds your sustainable race pace power.

• CADENCE WORK: First interval at high cadence (100+ rpm seated), second at low cadence (40-60 rpm seated, big gear).""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="1200" OnPower="0.98" Cadence="100" OffDuration="600" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W03 Wed - Easy Endurance", """• Big pyramid base. Easy aerobic volume. Keep it truly conversational. This is where mitochondrial density and fat oxidation improve.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W03 Thu - VO2max Assessment", """• STRUCTURE:
20 min warmup with openers → 5x4 min @ 110-115% FTP (4 min easy between) → 10 min cooldown

• VO2max intervals—your "assessment" of top-end fitness. How hard are these? If you're dying by interval 3, VO2max is a limiter. If you're crushing all 5, your VO2 is strong. Take notes. This informs next week's block focus.

• CADENCE WORK: Alternate high and low cadence. Intervals 1, 3, 5 at high cadence (100+ rpm), intervals 2, 4 at low cadence (40-60 rpm).""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <SteadyState Duration="30" Power="1.10"/>
    <SteadyState Duration="30" Power="0.55"/>
    <SteadyState Duration="30" Power="1.10"/>
    <SteadyState Duration="30" Power="0.55"/>
    <SteadyState Duration="30" Power="1.10"/>
    <SteadyState Duration="30" Power="0.55"/>
    <IntervalsT Repeat="5" OnDuration="240" OnPower="1.12" Cadence="100" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W03 Fri - Rest", """• You've earned it. Two hard days back-to-back. Rest today.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W03 Sat - Biggest Aerobic Day", """• STRUCTURE:
First 2 hours Z2 → 4x12 min @ 85-90% FTP (5 min easy between) in hours 2-3 → Final hour Z2

• Longest ride yet. How do you feel during those 12-min efforts when already fatigued? Strong = good durability. Dying = durability is a limiter. This ride tells us a lot about your training needs. Eat 70-80g carbs/hour.

• CADENCE WORK: Mix cadences on G-Spot efforts—some high, some low.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="6000" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="4" OnDuration="720" OnPower="0.88" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W03 Sun - Easy Endurance + Max Strength", """• Long easy ride to cap volume week. Max strength work continues—this is base phase. Lift heavy, focus on quality movement.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Heavy front squats, step-ups with weight, Copenhagen planks, pallof press (4x5-6 heavy). Max strength phase. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="6000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 4: Recovery + Limiter Block Planning
weeks.append({
    "week_number": 4,
    "focus": "Recovery + Limiter Block Planning",
    "volume_percent": 60,
    "volume_hours": "6-7",
    "workouts": [
        create_workout("W04 Mon - Rest", """• Recovery week. Your body adapts during rest. Based on Weeks 1-3, we've identified your limiters. Next week begins a 3-week limiter block targeting your weakness. Could be threshold endurance, VO2max repeatability, durability, or sustained power. GOAT Method adapts to YOU. This week: recover and prepare.

• WEEK PREVIEW: Recovery week. Wednesday has light G-Spot work (just maintaining fitness). Rest of week is easy endurance. Strength shifts to explosive work (prepares for VO2max blocks). This is when adaptation happens.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W04 Tue - Easy Endurance", """• Truly easy. No metrics to hit. Just move your legs and recover.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W04 Wed - Light G-Spot", """• STRUCTURE:
10 min warmup → 2x12 min @ 85-88% FTP (5 min easy between) → 10 min cooldown

• Light quality work to maintain fitness without adding fatigue. Should feel controlled and easy. If it feels hard, you're not recovered yet—back off 5%.

• CADENCE WORK: Mix cadences—one high, one low.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="2" OnDuration="720" OnPower="0.86" Cadence="90" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W04 Thu - Rest or Easy Spin", """• Optional: 30-45 min Z1

• If tired, take it off. If fresh, easy spin only.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W04 Fri - Easy Endurance", """• Easy day. Absorbing training. Getting stronger during rest.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W04 Sat - Moderate Endurance", """• No intensity. Just aerobic time. Practice skills—cornering, bike handling, descending. Check equipment. Make sure everything is dialed.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="9000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W04 Sun - Optional Spin + Explosive Strength", """• Skip ride if tired. Strength shifts to explosive work—this prepares you for VO2max blocks coming. Light loads, maximum velocity.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Box jumps, medicine ball slams, jump squats, power cleans (light weight, explosive) (3x6-8). Explosive strength phase. Light loads, maximum velocity. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 5: Limiter Block 1 - Threshold Endurance Focus
weeks.append({
    "week_number": 5,
    "focus": "Limiter Block 1 - Threshold Endurance Focus",
    "volume_percent": 85,
    "volume_hours": "8.5-10",
    "workouts": [
        create_workout("W05 Mon - Rest", """• Limiter Block begins. Based on your testing and Week 3 performance, we're targeting threshold endurance—your ability to hold race pace for extended periods. Three weeks of focused threshold work. This is Block Periodization principles within GOAT Method. Single focus, maximum adaptation.

• WEEK PREVIEW: Threshold block begins. Wednesday has long threshold intervals (3x15 min). Saturday has extended threshold (2x25 min). This is concentrated loading on your biggest limiter. By Week 7 you'll feel threshold-specific fatigue—that's adaptation.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W05 Tue - Easy Endurance", """• Easy day before threshold block. Keep it conversational. Save energy.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W05 Wed - Threshold Block #1", """• STRUCTURE:
20 min warmup → 3x15 min @ 95-100% FTP (7 min easy between) → 10 min cooldown

• First threshold-focused session. Three 15-minute blocks at race pace. This builds your ability to sustain power. Pace yourself. Stay smooth. Controlled breathing.

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="900" OnPower="0.98" Cadence="100" OffDuration="420" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W05 Thu - Easy Endurance", """• Recovery between threshold sessions. Keep it genuinely easy. Active recovery only.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W05 Fri - Easy Endurance", """• Another easy day. Building volume without fatigue before weekend sessions.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W05 Sat - Threshold Block #2", """• STRUCTURE:
20 min warmup → 2x25 min @ 95-100% FTP (10 min easy between) → 10 min cooldown

• Longer threshold blocks. This is HARD. 25 minutes at threshold tests your mental toughness as much as physical. Break into 5-minute chunks mentally. Stay engaged. Don't drift.

• CADENCE WORK: First interval at high cadence (100+ rpm), second at low cadence (40-60 rpm).""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="1500" OnPower="0.98" Cadence="100" OffDuration="600" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W05 Sun - Long Endurance + Explosive Strength", """• Long easy ride after threshold day = building durability on tired legs. Explosive strength maintains power production during threshold-focused block. Eat 60-80g carbs/hour.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Jump squats, box jumps, med ball work, explosive step-ups (3x6-8 explosive). Explosive strength maintains power during threshold block. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="12600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 6: Limiter Block 2 - Threshold Overload
weeks.append({
    "week_number": 6,
    "focus": "Limiter Block 2 - Threshold Overload",
    "volume_percent": 95,
    "volume_hours": "9.5-11.5",
    "workouts": [
        create_workout("W06 Mon - Rest", """• Week 2 of threshold block. Volume and threshold duration both increase. This is concentrated loading—maximum stimulus in single capacity. By Saturday you should feel threshold-specific fatigue. That's adaptation happening. Week 8 is recovery, so push through this and next week.

• WEEK PREVIEW: Threshold overload week. Wednesday has extended threshold (2x30 min—longest yet). Saturday combines threshold + over-unders (teaches threshold sustainment when power varies). This is peak threshold volume.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W06 Tue - Easy Endurance", """• Long easy ride. Build aerobic base while threshold adaptations process. Keep it conversational.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="6000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W06 Wed - Threshold Block #1", """• STRUCTURE:
20 min warmup → 2x30 min @ 95-100% FTP (10 min easy between) → 10 min cooldown

• Two 30-minute threshold blocks. Longest yet. This is peak threshold volume. Mental game matters here. Stay present. Focus on each 5-minute segment. Breathing, pedaling, posture. One thing at a time.

• CADENCE WORK: First interval at high cadence (100+ rpm), second at low cadence (40-60 rpm).""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="1800" OnPower="0.98" Cadence="100" OffDuration="600" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W06 Thu - Easy Endurance", """• Recovery day. You need this after 60 minutes of threshold work. Truly easy.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4500" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W06 Fri - Easy Endurance", """• Building volume. Easy aerobic work. Save energy for tomorrow.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="6000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W06 Sat - Threshold Block #2 + Over-Unders", """• STRUCTURE:
20 min warmup → 2x20 min @ 95-100% FTP + 3x8 min (4 min @ 95%, 4 min @ 105%) [7 min easy between all] → 10 min cooldown

• Combined threshold stimulus. Classic 2x20, then over-unders to teach threshold sustainment when power varies. This mimics gravel racing—constant power variation around race pace.

• RHYTHM INTERVALS: For over-unders, try rhythm pattern: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 2, continuous. This simulates race variability.

• CADENCE WORK: Mix cadences on threshold blocks. Over-unders use rhythm pattern or mix cadences.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="1200" OnPower="0.98" Cadence="100" OffDuration="420" OffPower="0.55"/>
    <IntervalsT Repeat="3" OnDuration="480" OnPower="0.98" Cadence="100" OffDuration="420" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W06 Sun - Long Endurance + Explosive Strength", """• Long ride after big threshold day. Keep it truly easy—this is durability training. Fuel properly: 70-80g carbs/hour. Test race nutrition products.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Explosive movements—jump squats, box jumps, med ball (3x6-8). Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="14400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 7: Limiter Block 3 - Threshold Peak
weeks.append({
    "week_number": 7,
    "focus": "Limiter Block 3 - Threshold Peak",
    "volume_percent": 100,
    "volume_hours": "10-12",
    "workouts": [
        create_workout("W07 Mon - Rest", """• Final week of threshold block. Biggest threshold volume of the plan. By Sunday you should feel threshold-specific fatigue. That's good—you're overloading the system. Week 8 we shift to transmutation (polarized work to convert threshold gains to race performance). Push through this week knowing rest and variety are coming.

• WEEK PREVIEW: Peak threshold week. Wednesday has 3x20 threshold (most threshold volume in single session). Saturday has race-pace threshold endurance (70 minutes total at/near threshold). This is peak training stress.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W07 Tue - Easy Endurance", """• Long easy ride. Aerobic volume. Conversational pace.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="6000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W07 Wed - Threshold Block #1", """• STRUCTURE:
20 min warmup → 3x20 min @ 95-100% FTP (8 min easy between) → 10 min cooldown

• Three 20-minute blocks. Most threshold volume in single session. You should feel strong here—weeks 5-6 have prepared you. Controlled execution. Don't blow up early.

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected or rhythm pattern.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="1200" OnPower="0.98" Cadence="100" OffDuration="480" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W07 Thu - Easy Endurance", """• Recovery day. Your legs need this between big threshold sessions.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W07 Fri - Easy Endurance", """• Another easy day. Building volume. Save energy for Saturday's final threshold push.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="6000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W07 Sat - Threshold Block #2", """• STRUCTURE:
20 min warmup → 2x30 min @ 95-100% FTP + 10 min @ 90-95% FTP (8 min easy between) → 10 min cooldown

• Final big threshold day of block. 70 minutes total at/near threshold. This is peak training stress. You're teaching your body to sustain race pace indefinitely. Mental toughness required. Stay present.

• LOADED INTERVALS: For one interval, try loaded pattern: 1 min Z5/Z6 (high cadence, seated) → settle into 29 min Z3 (self-selected cadence). This simulates race starts.

• CADENCE WORK: Mix cadences or use loaded/rhythm patterns.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="1800" OnPower="0.98" Cadence="100" OffDuration="480" OffPower="0.55"/>
    <IntervalsT Repeat="1" OnDuration="600" OnPower="0.93" Cadence="100" OffDuration="480" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W07 Sun - Long Endurance + Stability Strength", """• Longest ride of block after big threshold day. This is gravel durability training—holding watts when exhausted. Keep it easy. Eat 70-90g carbs/hour. Strength shifts to stability during threshold overload—prevent injuries.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Single-leg stability work, planks, anti-rotation (3x10-12). Stability strength during threshold overload prevents injuries. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="16200" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 8: Recovery + Transmutation Planning
weeks.append({
    "week_number": 8,
    "focus": "Recovery + Transmutation Planning",
    "volume_percent": 60,
    "volume_hours": "6-7",
    "workouts": [
        create_workout("W08 Mon - Rest", """• Recovery week after threshold block. You should feel tired Monday, fresh by Sunday. This is when adaptation happens—your threshold power is increasing during rest. Next week begins transmutation phase: polarized training to convert threshold gains into race performance. Variety returns.

• WEEK PREVIEW: Recovery week. Wednesday has light threshold touch (just maintaining fitness). Rest of week is easy endurance. Strength shifts to stability work. This is when adaptation happens.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W08 Tue - Easy Endurance", """• Truly easy. Enjoy the break from threshold work. Just move your legs.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W08 Wed - Light Quality", """• STRUCTURE:
10 min warmup → 2x10 min @ 95-100% FTP (5 min easy between) → 10 min cooldown

• Maintaining threshold fitness without adding fatigue. Should feel strong and controlled. If it feels hard, you're not recovered—back off.

• CADENCE WORK: Mix cadences—one high, one low.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="2" OnDuration="600" OnPower="0.98" Cadence="90" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W08 Thu - Rest or Easy Spin", """• Optional: 30-45 min Z1

• If tired, take it off. If fresh, easy spin only.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W08 Fri - Easy Endurance", """• Easy day. Your body is adapting and getting stronger while you rest.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W08 Sat - Moderate Endurance", """• No intensity. Just aerobic time. Practice skills. Check equipment. Make sure everything is dialed for final four weeks.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="10800" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W08 Sun - Optional Spin + Stability Strength", """• Skip ride if tired. Light stability strength maintains adaptations without stress. Strength will shift to durability phase next week.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Core stability, single-leg balance work, mobility (light). Stability strength maintains adaptations. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 9: Transmutation - Polarized Conversion
weeks.append({
    "week_number": 9,
    "focus": "Transmutation - Polarized Conversion",
    "volume_percent": 90,
    "volume_hours": "9-11",
    "workouts": [
        create_workout("W09 Mon - Rest", """• Transmutation phase. You've built threshold endurance. Now we sharpen it with polarized distribution—lots of easy, targeted hard work at VO2max and race pace. This converts raw fitness into race performance. Check HRV if tracking—if significantly down, adjust intensity accordingly.

• WEEK PREVIEW: Transmutation begins. Wednesday has VO2max intervals (sharpens top end). Saturday has race-pace threshold (should feel easier after recovery). Training becomes polarized—80% easy, 20% hard.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W09 Tue - Easy Endurance", """• Long easy ride. Pure aerobic work. Keep it conversational. This is the "80" in polarized 80/20.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="6000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W09 Wed - Polarized Hard #1", """• STRUCTURE:
20 min warmup with openers → 6x4 min @ 110-115% FTP (4 min easy between) → 10 min cooldown

• VO2max work sharpens your top end after threshold block. These should feel hard but doable—your threshold fitness makes these easier. Embrace the burn.

• CADENCE WORK: Alternate high and low cadence. Intervals 1, 3, 5 at high cadence (100+ rpm), intervals 2, 4, 6 at low cadence (40-60 rpm).""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <SteadyState Duration="30" Power="1.10"/>
    <SteadyState Duration="30" Power="0.55"/>
    <SteadyState Duration="30" Power="1.10"/>
    <SteadyState Duration="30" Power="0.55"/>
    <SteadyState Duration="30" Power="1.10"/>
    <SteadyState Duration="30" Power="0.55"/>
    <IntervalsT Repeat="6" OnDuration="240" OnPower="1.12" Cadence="100" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W09 Thu - Easy Endurance", """• Recovery between quality sessions. Keep it truly easy.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W09 Fri - Easy Endurance", """• Building easy volume. Aerobic base maintenance.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="6000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W09 Sat - Polarized Hard #2", """• STRUCTURE:
20 min warmup → 2x25 min @ 95-100% FTP (10 min easy between) → 10 min cooldown

• Threshold work should feel easier after recovery week. This is your race pace—sustainable, controlled, strong. Practice drinking while holding power.

• RHYTHM INTERVALS: For one interval, try rhythm pattern: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 8, continuous. This simulates race variability.

• CADENCE WORK: Mix cadences or use rhythm pattern.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="1500" OnPower="0.98" Cadence="100" OffDuration="600" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W09 Sun - Long Easy + Durability Strength", """• Long easy ride. Pure durability training. Strength shifts to higher reps, lower weight—muscular endurance for long gravel races. Eat 70-80g carbs/hour.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Higher rep work—goblet squats, step-ups, planks (3x15-20). Durability strength phase. Higher reps, lower weight for muscular endurance. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="14400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 10: Realization - Race Specificity
weeks.append({
    "week_number": 10,
    "focus": "Realization - Race Specificity",
    "volume_percent": 95,
    "volume_hours": "9.5-11.5",
    "workouts": [
        create_workout("W10 Mon - Rest", """• Realization phase. Final push before taper. Training is race-specific now—long sustained efforts, variability simulation, race-pace blocks. You've built the engine, sharpened it, now we tune it precisely for race day. Two more weeks of quality, then taper.

• WEEK PREVIEW: Race specificity week. Wednesday has mixed race efforts (VO2max + threshold). Saturday has long race-pace blocks (3x20 min). Sunday is final long race simulation (dress rehearsal). This is peak race-specific fitness.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W10 Tue - Easy Endurance", """• Long easy ride. Keep it conversational. Build aerobic volume.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="6000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W10 Wed - Race Simulation #1", """• STRUCTURE:
20 min warmup → 4x6 min @ 110% FTP + 2x15 min @ 95-100% FTP (5-7 min easy between) → 10 min cooldown

• Race simulation. VO2max efforts = hard climbs or surges. Threshold blocks = sustained race pace. This is exactly what gravel racing feels like. Variable power, constant effort.

• RHYTHM INTERVALS: For threshold blocks, use rhythm pattern: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 5, continuous.

• CADENCE WORK: VO2 intervals—alternate high and low cadence. Threshold blocks—use rhythm pattern.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="4" OnDuration="360" OnPower="1.10" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <IntervalsT Repeat="2" OnDuration="900" OnPower="0.98" Cadence="100" OffDuration="420" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W10 Thu - Easy Endurance", """• Recovery day. Your legs need this between quality sessions.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W10 Fri - Easy Endurance", """• Building volume without fatigue. Easy aerobic work.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="6000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W10 Sat - Race Simulation #2", """• STRUCTURE:
20 min warmup → 3x20 min @ 95-100% FTP (8 min easy between) → 10 min cooldown

• Three 20-minute threshold blocks. This is your race pace for extended periods. You should feel strong and controlled here—weeks of training paying off. Execute cleanly.

• LOADED INTERVALS: For one interval, try loaded pattern: 1 min Z5/Z6 (high cadence, seated) → settle into 19 min Z3 (self-selected cadence). This simulates race starts.

• CADENCE WORK: Mix cadences or use loaded/rhythm patterns.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="1200" OnPower="0.98" Cadence="100" OffDuration="480" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W10 Sun - Long Race Simulation + Maintenance Strength", """• STRUCTURE:
First 2 hours Z2 → 2x30 min @ 90-95% FTP (10 min easy between) in hours 2-4 → Final hour Z2

• Final long race simulation. Sustained efforts when already tired = race day. Eat 70-90g carbs/hour. Test ALL race-day gear, nutrition, hydration. This is dress rehearsal.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Maintenance only—light loads, movement quality (2x8-10). Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="6000" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="2" OnDuration="1800" OnPower="0.93" Cadence="88" OffDuration="600" OffPower="0.55"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 11: Taper Week 1
weeks.append({
    "week_number": 11,
    "focus": "Taper Week 1",
    "volume_percent": 70,
    "volume_hours": "7-8.5",
    "workouts": [
        create_workout("W11 Mon - Rest", """• Taper begins. Volume drops 30%, intensity stays high. You should feel increasingly fresh each day while maintaining sharpness. Check HRV if tracking—should be trending up. Legs should feel snappy. Power should come easy. That's fitness + freshness = form.

• WEEK PREVIEW: Taper begins. Wednesday has race openers (reduced volume, maintained intensity). Saturday has moderate endurance with openers (final reminder workout). Volume drops, intensity stays sharp.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W11 Tue - Easy Endurance", """• Easy ride. You're tapering now. Enjoy the lower volume.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4500" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W11 Wed - Taper Quality", """• STRUCTURE:
15 min warmup → 3x10 min @ 95-100% FTP + 3x90sec @ 110% FTP (5 min easy between all) → 10 min cooldown

• Reduced volume, maintained intensity. Threshold reminds body of race pace. VO2 openers keep top-end sharp. Should feel powerful and controlled.

• CADENCE WORK: High cadence on all efforts (100+ rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="3" OnDuration="600" OnPower="0.98" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <IntervalsT Repeat="3" OnDuration="90" OnPower="1.10" Cadence="100" OffDuration="210" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W11 Thu - Easy Endurance", """• Easy recovery. Your body is absorbing fitness and gaining freshness.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W11 Fri - Easy Endurance", """• Easy day. Just moving blood through legs. No stress.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4500" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W11 Sat - Taper Long Ride", """• STRUCTURE:
First 90 min Z2 → 3x10 min @ 95-100% FTP (5 min easy between) → Final 30-60 min Z2

• Shorter long ride but maintains race-intensity efforts. Should feel strong and controlled. This is your final "reminder" workout before race week.

• CADENCE WORK: Mix cadences on threshold blocks.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4800" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="600" OnPower="0.98" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="2400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W11 Sun - Easy Spin + Optional Light Strength", """• Easy recovery spin. Skip strength if tired. You're one week from race week now. Trust the process.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Light core/mobility only if feeling good. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 12: Race Week
weeks.append({
    "week_number": 12,
    "focus": "Race Week",
    "volume_percent": 40,
    "volume_hours": "4-6",
    "workouts": [
        create_workout("W12 Mon - Rest", """• Race week. Volume drops dramatically. Intensity stays sharp but brief. Check HRV if tracking—should be at or above baseline. You should feel fresh, powerful, ready. Nervous energy is normal—channel it into final prep. Check bike. Pack bags. Review race plan. Trust your training—GOAT Method got you here.

• WEEK PREVIEW: Race week! Wednesday has final sharpness session (race openers). Thursday is easy spin or rest. Friday is pre-race shake-out. Saturday/Sunday: RACE DAY!

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W12 Tue - Easy Endurance", """• Easy spin. Just moving legs. No stress. Stay off your feet when not riding.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W12 Wed - Final Sharpness", """• STRUCTURE:
15 min easy → 3x4 min @ 95-100% FTP (3 min easy between) → 3x1 min @ 110% FTP (2 min easy between) → 3x30sec @ 115% FTP (90sec easy between) → 5 min cooldown

• Final intensity before race. Should feel powerful, snappy, explosive. If legs feel dead, add another rest day. This is your sharpness check—power should come easily.

• CADENCE WORK: High cadence on all efforts (100+ rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="3" OnDuration="240" OnPower="0.98" Cadence="100" OffDuration="180" OffPower="0.55"/>
    <IntervalsT Repeat="3" OnDuration="60" OnPower="1.10" Cadence="100" OffDuration="120" OffPower="0.55"/>
    <IntervalsT Repeat="3" OnDuration="30" OnPower="1.15" Cadence="100" OffDuration="90" OffPower="0.55"/>
    <Cooldown Duration="300" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W12 Thu - Easy Spin or Rest", """• Optional: 30-45 min Z1

• If race is Sunday, easy spin today. If race is Saturday, consider rest. Listen to your body. Trust your fitness.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W12 Fri - Pre-Race Shake-Out", """• STRUCTURE:
15 min easy → 3x2 min @ race pace (2 min easy between) → 3x30sec @ 110% FTP (90sec easy between) → 10 min easy

• Final ride before race. Legs should feel fresh and powerful. Check bike one last time. Test race-day tire pressure. Visualize race execution. You're ready.

• CADENCE WORK: High cadence on all efforts (100+ rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="3" OnDuration="120" OnPower="0.98" Cadence="100" OffDuration="120" OffPower="0.55"/>
    <IntervalsT Repeat="3" OnDuration="30" OnPower="1.10" Cadence="100" OffDuration="90" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W12 Sat - Race Day or Rest", """• If racing Saturday: EXECUTE YOUR PLAN

• If racing Sunday: Complete rest or 20-30 min easy spin with 3x30sec openers

• Notes: If racing today—start conservatively, fuel from the start (60-90g carbs/hour), pace yourself through first half, execute your race plan. GOAT Method prepared you for this. Trust it.""", """    <FreeRide Duration="60"/>
"""),
        create_workout("W12 Sun - Race Day or Recovery", """• If racing Sunday: EXECUTE YOUR PLAN

• If raced Saturday: Easy 30-60 min recovery spin, celebrate, refuel

• Notes: Race day. Stick to your pacing strategy. Fuel aggressively from mile 1. When it hurts, everyone hurts—who handles it better? You do. You trained adaptively, intelligently, and specifically for this. Execute.""", """    <FreeRide Duration="60"/>
""")
    ]
})

# Create complete template
template = {
    "plan_metadata": plan_metadata,
    "weeks": weeks,
    "default_modifications": {
        "goat_method": {
            "enabled": True,
            "description": "Gravel Optimized Adaptive Training - combines pyramidal, polarized, limiter-focused blocks, and G-Spot based on athlete signals"
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
            "description": "Alternating patterns: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 4-8, continuous"
        },
        "loaded_intervals": {
            "enabled": True,
            "weeks": [7, 10],
            "description": "1 min Z5/Z6 (high cadence, seated) → settle into 11-29 min Z3 (self-selected cadence). Simulates race starts and surges."
        },
        "gspot_terminology": {
            "enabled": True,
            "replaces": "Sweet Spot",
            "range": "87-92% FTP"
        },
        "strength_training": {
            "enabled": False,
            "phases": {
                "base": "Max strength (4x5-6 heavy)",
                "explosive": "Explosive power (3x6-8, light loads)",
                "stability": "Stability/injury prevention (3x10-12)",
                "durability": "Muscular endurance (3x15-20, higher reps)",
                "maintenance": "Light maintenance (2x8-10)"
            },
            "note": "Athlete performs own strength program. Phases adapt to training block focus."
        },
        "monday_week_preview": {
            "enabled": True,
            "description": "Monday rest days include week preview with key workouts, GOAT Method principles, and reminders"
        },
        "rest_day_tss_limit": 30,
        "rest_day_duration_limit_hours": 1
    }
}

# Save complete template
output_path = "/Users/mattirowe/Documents/Gravel Landing Page Project/current/plans/7. Finisher Advanced (12 weeks)/template.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(template, f, indent=2, ensure_ascii=False)

print(f"✅ Complete template created: {output_path}")
print(f"   Plan: {plan_metadata['name']}")
print(f"   Duration: {plan_metadata['duration_weeks']} weeks")
print(f"   Philosophy: {plan_metadata['philosophy']}")
print(f"   Total weeks: {len(weeks)}")
total_workouts = sum(len(w['workouts']) for w in weeks)
print(f"   Total workouts: {total_workouts}")
print(f"   ✅ All 12 weeks complete!")
print(f"   ✅ GOAT Method philosophy applied")
print(f"   ✅ Changing Pace philosophy integrated (cadence work, rhythm/loaded intervals)")
print(f"   ✅ G-Spot terminology applied")

