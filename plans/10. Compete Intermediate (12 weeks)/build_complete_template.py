#!/usr/bin/env python3
"""
Build complete JSON template for COMPETE INTERMEDIATE (12 weeks)
Polarized (80/20) with Changing Pace philosophy
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
    "name": "COMPETE INTERMEDIATE",
    "duration_weeks": 12,
    "philosophy": "Polarized (80/20)",
    "target_hours": "12-15",
    "target_athlete": "Intermediate competitive racer, solid cycling background, top-third finish goal",
    "goal": "Competitive performance through proven polarized distribution"
}

weeks = []

# WEEK 1: Foundation & Polarized Philosophy Introduction
weeks.append({
    "week_number": 1,
    "focus": "Foundation & Polarized Philosophy Introduction",
    "volume_percent": 70,
    "volume_hours": "8.5-10.5",
    "workouts": [
        create_workout("W01 Mon - Rest", """• Welcome to Polarized Training for competitive performance. Polarized = 80% easy (Z1-Z2), 20% hard (Z4-Z5+), almost nothing in-between (Z3). This is counter-intuitive—most cyclists ride too hard on easy days and not hard enough on hard days, living in "no man's land" (Z3). Polarized training fixes this: easy days stay TRULY easy for recovery, hard days can be TRULY hard because you're recovered. This is proven for well-trained athletes pursuing competitive performance. The discipline? Staying easy on easy days. It feels slow. It feels like you're not training hard enough. Trust the science—polarized distribution produces superior fitness for athletes with solid background.

• WEEK PREVIEW: Foundation week. Tuesday has FTP test (sets training zones). Thursday introduces first hard session (VO2max intervals). Saturday is first long easy ride (3-4 hours). Notice: ONE hard session, EVERYTHING else easy. That's polarized.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W01 Tue - FTP Test", """• STRUCTURE:
20 min warmup with progressive intensity → 5 min all-out effort → 10 min recovery → 20 min max sustained effort → 10 min cooldown

• Classic FTP test. 5-min all-out primes the system. Then 20-min sustained max effort (not sprint, controlled). Average watts × 0.95 = FTP. This sets your training zones. CRITICAL: In polarized training, Z1-Z2 (55-75% FTP) is easy, Z4-Z5+ (95%+ FTP) is hard. Z3 (76-94% FTP) is avoided except in short transitions. Write down your FTP.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <SteadyState Duration="300" Power="1.20"/>
    <SteadyState Duration="600" Power="0.55"/>
    <SteadyState Duration="1200" Power="1.05"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W01 Wed - Easy Endurance (Pure Z2)", """• First polarized easy day. This is the "80" in 80/20. CONVERSATIONAL PACE ENTIRE TIME. If you can't speak in full sentences, you're going too hard. This feels painfully slow for competitive athletes—that's correct. You're building massive aerobic base without accumulating fatigue. Resist all urges to push harder. Easy means EASY.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W01 Thu - HARD Session #1: VO2max Introduction", """• STRUCTURE:
20 min easy warmup → 5x4 min @ 110-115% FTP (4 min easy recovery between) → 20 min easy cooldown

• First hard day. This is the "20" in 80/20. Hard means HARD. Each interval should hit 95%+ max HR by end. Lungs burning, legs screaming. But you only do this 2-3x per week—the easy days make these hard days possible. FULL RECOVERY between intervals—don't creep into Z3 during rest. Start controlled, finish strong. If you blow up on interval 1, you started too hard.

• CADENCE WORK: Alternate high cadence (100+ rpm seated) and low cadence (40-60 rpm seated, big gear) on intervals. This teaches power production in different ways.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="5" OnDuration="240" OnPower="1.12" Cadence="100" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="1200" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W01 Fri - Easy Endurance", """• Day after hard session. SUPER easy. Active recovery only. Spinning out legs, clearing lactate. This is critical recovery in polarized training—enables next hard session.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W01 Sat - Long Easy Endurance", """• Foundation of polarized training—long, steady, easy. CONVERSATIONAL ENTIRE TIME. This builds mitochondrial density, capillary density, fat oxidation, and durability without fatigue. Eat 60-70g carbs per hour. Practice race nutrition. This is "money in the bank" fitness. If breathing hard, SLOW DOWN.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="10800" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W01 Sun - Easy Endurance", """• Easy recovery after long day. Pure Z2. No intensity whatsoever. Building volume without fatigue.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 2: Polarized Volume Building
weeks.append({
    "week_number": 2,
    "focus": "Polarized Volume Building",
    "volume_percent": 80,
    "volume_hours": "9.5-12",
    "workouts": [
        create_workout("W02 Mon - Rest", """• Week 2 builds volume with strict polarization. TWO hard sessions this week (still only 20% of total time), everything else easy. Advanced riders struggle most with discipline on easy days—ego wants to push. Ignore ego. Easy pace builds aerobic engine that powers hard efforts.

• WEEK PREVIEW: Volume building week. Wednesday has threshold work (first threshold session). Saturday has VO2max progression (6x4 min—one more than Week 1). Sunday is longest ride yet (3.5-4.5 hours). Two hard sessions, everything else easy.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W02 Tue - Easy Endurance", """• Easy day before hard session. Conversational pace. Save energy for tomorrow. Pure aerobic base building.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W02 Wed - HARD Session #1: Threshold Work", """• STRUCTURE:
20 min easy warmup → 3x12 min @ 100-105% FTP (6 min easy recovery between) → 20 min easy cooldown

• Just above FTP. Hard but controllable. Breathing labored but rhythmic, not gasping. This is race pace for competitive gravel. Should finish thinking "I could maybe do one more." Long warmup/cooldown keeps total time in Z1-Z2 high (polarization principle—only intervals are hard).

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="720" OnPower="1.02" Cadence="100" OffDuration="360" OffPower="0.55"/>
    <Cooldown Duration="1200" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W02 Thu - Easy Endurance", """• Recovery between hard sessions. Truly easy. Resist temptation to ride Z3 "steady"—that violates polarization and prevents recovery.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W02 Fri - Easy Endurance", """• Another easy day. Building volume before weekend. Conversational pace.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W02 Sat - HARD Session #2: VO2max Progression", """• STRUCTURE:
20 min easy warmup → 6x4 min @ 110-115% FTP (4 min easy recovery between) → 20 min easy cooldown

• Second hard session. Six intervals (one more than Week 1). These HURT. Embrace the pain—this is where competitive fitness comes from. Full recovery between reps. Don't cheat rest intervals by staying in Z3.

• CADENCE WORK: Alternate high and low cadence. Intervals 1, 3, 5 at high cadence (100+ rpm), intervals 2, 4, 6 at low cadence (40-60 rpm).""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="6" OnDuration="240" OnPower="1.12" Cadence="100" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="1200" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W02 Sun - Long Easy Endurance", """• Long easy ride after hard day. This is polarized training—big volume, low intensity. Day after VO2max your legs are tired, but keep power LOW. Conversational pace entire time. Eat 60-70g carbs/hour.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="14400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 3: Peak Base Volume with Polarization
weeks.append({
    "week_number": 3,
    "focus": "Peak Base Volume with Polarization",
    "volume_percent": 90,
    "volume_hours": "11-13.5",
    "workouts": [
        create_workout("W03 Mon - Rest", """• Biggest week of base phase. By Sunday you should feel accumulated fatigue (tired but not destroyed). Easy days still EASY, hard days still HARD—that's polarization discipline. Week 4 is recovery, so push through this week while maintaining zone discipline.

• WEEK PREVIEW: Peak base week. Wednesday has mixed VO2max/threshold (big quality day). Saturday has threshold progression (2x20 min). Sunday is longest ride yet (4-5 hours). Two hard sessions, everything else easy.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W03 Tue - Easy Endurance", """• Long easy ride. Pure aerobic work. Conversational pace.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W03 Wed - HARD Session #1: Mixed VO2max/Threshold", """• STRUCTURE:
20 min easy warmup → 5x5 min @ 110-115% FTP (5 min easy between) → 15 min easy → 2x10 min @ 100-105% FTP (6 min easy between) → 15 min easy cooldown

• Big quality day. VO2max first while fresh, threshold when fatigued. This combines systems while maintaining polarization—intervals are hard, everything else easy. Total hard time = ~45 minutes. Total easy time = 65-75 minutes. That's 80/20 within the session.

• CADENCE WORK: VO2 intervals—alternate high and low cadence. Threshold blocks—mix cadences.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="5" OnDuration="300" OnPower="1.12" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="900" Power="0.65" Cadence="85"/>
    <IntervalsT Repeat="2" OnDuration="600" OnPower="1.02" Cadence="100" OffDuration="360" OffPower="0.55"/>
    <SteadyState Duration="900" Power="0.65" Cadence="85"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W03 Thu - Easy Endurance", """• Recovery from big session. Super easy. Active recovery without stress.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W03 Fri - Easy Endurance", """• Building volume before weekend. Easy pace.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W03 Sat - HARD Session #2: Threshold Progression", """• STRUCTURE:
20 min easy warmup → 2x20 min @ 100-105% FTP (10 min easy recovery between) → 20 min easy cooldown

• Classic 2x20 at threshold. Hard but sustainable. Breathing labored but controlled. This is race pace training. Break 20-min blocks into 5-min segments mentally. Stay smooth, stay seated, steady power.

• CADENCE WORK: First interval at high cadence (100+ rpm), second at low cadence (40-60 rpm).""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="1200" OnPower="1.02" Cadence="100" OffDuration="600" OffPower="0.55"/>
    <Cooldown Duration="1200" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W03 Sun - Long Easy Endurance", """• Longest ride yet. Day after threshold work = tired legs, but keep it EASY. Conversational pace. This teaches body to ride long on accumulated fatigue. Eat 70-80g carbs/hour. This is durability training through volume, not intensity.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="14400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 4: Recovery & Adaptation
weeks.append({
    "week_number": 4,
    "focus": "Recovery & Adaptation",
    "volume_percent": 60,
    "volume_hours": "7-9",
    "workouts": [
        create_workout("W04 Mon - Rest", """• Recovery week. Your body adapts during rest, not during work. By Friday you should feel fresh and strong. Polarized training makes recovery weeks especially effective—you haven't been grinding in Z3 all month, so fatigue is more specific and easier to recover from.

• WEEK PREVIEW: Recovery week. Wednesday has light quality touch (just maintaining fitness). Rest of week is easy endurance. This is when adaptation happens.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W04 Tue - Easy Endurance", """• Truly easy. Enjoy the ride. No power targets to stress about.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W04 Wed - Light Quality Touch", """• STRUCTURE:
15 min easy warmup → 3x8 min @ 98-102% FTP (5 min easy between) → 15 min easy cooldown

• Reduced volume threshold work. Maintains fitness without adding fatigue. Should feel controlled and comfortable. Still maintaining polarization—easy warmup/cooldown, hard intervals.

• CADENCE WORK: Mix cadences—one high, one low, one self-selected.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="3" OnDuration="480" OnPower="1.00" Cadence="90" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W04 Thu - Easy Endurance", """• Easy day. Your fitness is increasing during this rest.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W04 Fri - Easy Endurance", """• Easy day. Trust recovery process.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W04 Sat - Moderate Easy Endurance", """• No intensity. Just aerobic time. Practice skills—cornering, descending, bike handling. Check equipment for build phase.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="9000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W04 Sun - Easy Endurance", """• Easy recovery. End of recovery week feeling fresh.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 5: Build Phase - Intensity Increase
weeks.append({
    "week_number": 5,
    "focus": "Build Phase - Intensity Increase",
    "volume_percent": 85,
    "volume_hours": "10-12.5",
    "workouts": [
        create_workout("W05 Mon - Rest", """• Build phase begins. Weeks 5-8 progressively increase both volume and intensity while maintaining strict 80/20 distribution. Two hard sessions per week, everything else easy—that's the discipline.

• WEEK PREVIEW: Build phase begins. Wednesday has extended threshold (3x15 min). Saturday has VO2max development (6x5 min—longer intervals). Intensity increases, but easy days stay easy.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W05 Tue - Easy Endurance", """• Long easy ride before tomorrow's quality. Building aerobic base while fresh.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W05 Wed - HARD Session #1: Threshold Development", """• STRUCTURE:
20 min easy warmup → 3x15 min @ 100-105% FTP (7 min easy recovery between) → 20 min easy cooldown

• Longer threshold intervals than Week 4. 45 minutes cumulative at race pace. Hard but sustainable. Stay smooth, breathe rhythmically, don't spike power at starts. Long easy warmup/cooldown = polarization.

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="900" OnPower="1.02" Cadence="100" OffDuration="420" OffPower="0.55"/>
    <Cooldown Duration="1200" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W05 Thu - Easy Endurance", """• Recovery between hard sessions. Keep it truly easy.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W05 Fri - Easy Endurance", """• Building volume before weekend. Conversational pace.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W05 Sat - HARD Session #2: VO2max Development", """• STRUCTURE:
20 min easy warmup → 6x5 min @ 110-115% FTP (5 min easy recovery between) → 20 min easy cooldown

• Longer VO2max intervals. These are brutally hard. Embrace the suffering—this is where competitive performance comes from. Full recovery between reps mandatory.

• CADENCE WORK: Alternate high and low cadence. Intervals 1, 3, 5 at high cadence (100+ rpm), intervals 2, 4, 6 at low cadence (40-60 rpm).""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="6" OnDuration="300" OnPower="1.12" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="1200" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W05 Sun - Long Easy Endurance", """• Long ride after hard day. Keep it easy—this is durability training. Conversational pace. Fuel properly: 70-80g carbs/hour.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="14400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 6: Build Phase - Volume + Intensity Progression
weeks.append({
    "week_number": 6,
    "focus": "Build Phase - Volume + Intensity Progression",
    "volume_percent": 95,
    "volume_hours": "11.5-14",
    "workouts": [
        create_workout("W06 Mon - Rest", """• Volume and intensity both increase. By Saturday you should feel accumulated fatigue. Polarized discipline is critical—if easy days creep into Z3, you won't recover for hard sessions. Stay disciplined.

• WEEK PREVIEW: Volume + intensity progression. Wednesday has long threshold blocks (2x25 min). Saturday combines VO2max + threshold (big workout). Sunday is longest ride yet (4.5-5 hours). This week builds race-specific fitness.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W06 Tue - Easy Endurance", """• Long easy ride. Building base. Conversational pace.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="7200" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W06 Wed - HARD Session #1: Long Threshold Blocks", """• STRUCTURE:
20 min easy warmup → 2x25 min @ 100-105% FTP (10 min easy recovery between) → 20 min easy cooldown

• Long threshold blocks—50 cumulative minutes at race pace. This is hard. Break into 5-min segments mentally. Stay smooth, control breathing. This is competitive race pace training.

• CADENCE WORK: First interval at high cadence (100+ rpm), second at low cadence (40-60 rpm).""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="1500" OnPower="1.02" Cadence="100" OffDuration="600" OffPower="0.55"/>
    <Cooldown Duration="1200" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W06 Thu - Easy Endurance", """• Recovery between quality sessions. Super easy.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W06 Fri - Easy Endurance", """• Long easy day before weekend. Accumulating volume.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="7200" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W06 Sat - HARD Session #2: Mixed Intervals", """• STRUCTURE:
20 min easy warmup → 5x5 min @ 110-115% FTP (5 min easy between) → 15 min easy → 2x12 min @ 100-105% FTP (6 min easy between) → 15 min easy cooldown

• Combined stimulus. VO2max when fresh, threshold when fatigued. Big quality day. Take rest intervals seriously—stay in Z1-Z2, not Z3.

• RHYTHM INTERVALS: For threshold blocks, try rhythm pattern: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 4, continuous. This simulates race variability.

• CADENCE WORK: VO2 intervals—alternate high and low cadence. Threshold blocks—use rhythm pattern or mix cadences.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="5" OnDuration="300" OnPower="1.12" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="900" Power="0.65" Cadence="85"/>
    <IntervalsT Repeat="2" OnDuration="720" OnPower="1.02" Cadence="100" OffDuration="360" OffPower="0.55"/>
    <SteadyState Duration="900" Power="0.65" Cadence="85"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W06 Sun - Long Easy Endurance", """• Longest ride yet. Day after big quality. Keep it easy. This is volume-based durability training. Eat 70-80g carbs/hour. Test race-day gear and nutrition.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="16200" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 7: Build Phase - Peak Training Load
weeks.append({
    "week_number": 7,
    "focus": "Build Phase - Peak Training Load",
    "volume_percent": 100,
    "volume_hours": "12-15",
    "workouts": [
        create_workout("W07 Mon - Rest", """• Biggest week of plan. By Sunday you should feel significant accumulated fatigue—that's expected. Week 8 is recovery. Push through IF you're maintaining polarization discipline. If easy days have crept into Z3, you're breaking polarization and accumulating too much fatigue.

• WEEK PREVIEW: Peak training load week. Wednesday has peak threshold (3x20 min—60 minutes cumulative). Saturday combines VO2max + threshold (big workout). Sunday is longest ride (5-5.5 hours). This is your "A" week.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W07 Tue - Easy Endurance", """• Long easy ride. Save energy for tomorrow.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="7200" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W07 Wed - HARD Session #1: Peak Threshold Volume", """• STRUCTURE:
20 min easy warmup → 3x20 min @ 100-105% FTP (8 min easy recovery between) → 20 min easy cooldown

• Three 20-minute threshold blocks—60 cumulative minutes at race pace. This is HARD. Pace yourself—controlled start, steady middle, strong finish. This is race-specific training for competitive performance.

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected or rhythm pattern.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="1200" OnPower="1.02" Cadence="100" OffDuration="480" OffPower="0.55"/>
    <Cooldown Duration="1200" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W07 Thu - Easy Endurance", """• Truly easy after yesterday's threshold marathon. Active recovery only.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W07 Fri - Easy Endurance", """• Building volume. Conversational pace. Save energy for Saturday.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="7200" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W07 Sat - HARD Session #2: Peak Mixed Intensity", """• STRUCTURE:
20 min easy warmup → 6x4 min @ 110-115% FTP (4 min easy between) → 15 min easy → 2x12 min @ 100-105% FTP (7 min easy between) → 15 min easy cooldown

• Peak quality session. Six VO2 efforts then threshold work. Break it down—one interval at a time. Full recovery between efforts.

• LOADED INTERVALS: For threshold blocks, try loaded pattern: 1 min Z5/Z6 (high cadence, seated) → settle into 11 min Z3 (self-selected cadence). This simulates race starts.

• CADENCE WORK: VO2 intervals—alternate high and low cadence. Threshold blocks—use loaded pattern or rhythm pattern.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="6" OnDuration="240" OnPower="1.12" Cadence="100" OffDuration="240" OffPower="0.55"/>
    <SteadyState Duration="900" Power="0.65" Cadence="85"/>
    <IntervalsT Repeat="2" OnDuration="720" OnPower="1.02" Cadence="100" OffDuration="420" OffPower="0.55"/>
    <SteadyState Duration="900" Power="0.65" Cadence="85"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W07 Sun - Long Easy Endurance", """• Longest ride of plan. Day after big quality. Keep it easy. This is your "A" aerobic workout. Fuel like race day: 80-90g carbs/hour. Test everything.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="18000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 8: Recovery & Absorption
weeks.append({
    "week_number": 8,
    "focus": "Recovery & Absorption",
    "volume_percent": 60,
    "volume_hours": "7-9",
    "workouts": [
        create_workout("W08 Mon - Rest", """• Recovery week after peak training. You should feel tired Monday and fresh by Friday. This is when polarized training converts to performance—easy weeks don't accumulate fatigue, making recovery faster and more complete.

• WEEK PREVIEW: Recovery week. Wednesday has light quality touch (just maintaining fitness). Rest of week is easy endurance. This is when adaptation happens.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W08 Tue - Easy Endurance", """• Truly easy. Enjoy the break from intensity.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W08 Wed - Light Quality Touch", """• STRUCTURE:
15 min warmup → 3x10 min @ 98-102% FTP (5 min easy) → 15 min cooldown

• Maintaining fitness without fatigue. Still polarized—easy or hard, nothing in-between.

• CADENCE WORK: Mix cadences—one high, one low, one self-selected.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="3" OnDuration="600" OnPower="1.00" Cadence="90" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W08 Thu - Easy Endurance", """• Easy day. Your body is adapting.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W08 Fri - Easy Endurance", """• Easy day. Fitness increasing while resting.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W08 Sat - Moderate Easy Endurance", """• No intensity. Just aerobic time. Check equipment.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="9000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W08 Sun - Easy Endurance", """• Easy recovery. End of recovery week.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 9: Peak Phase - Race Specificity
weeks.append({
    "week_number": 9,
    "focus": "Peak Phase - Race Specificity",
    "volume_percent": 90,
    "volume_hours": "11-13.5",
    "workouts": [
        create_workout("W09 Mon - Rest", """• Peak phase. Final four weeks. Training becomes race-specific—longer sustained efforts, race-pace blocks, mixed intensities. Maintaining strict polarization: hard sessions truly hard, easy days truly easy.

• WEEK PREVIEW: Peak phase begins. Wednesday has race simulation (VO2max + threshold). Saturday has race-pace blocks (2x25 min). Sunday is long easy ride. Training becomes more race-specific now.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W09 Tue - Easy Endurance", """• Long easy ride. Pure aerobic work. Keep it conversational. This is the "80" in polarized 80/20.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="7200" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W09 Wed - HARD Session #1: Race Simulation", """• STRUCTURE:
20 min warmup → 4x6 min @ 110-115% FTP (6 min easy) → 15 min easy → 2x15 min @ 100-105% FTP (8 min easy) → 15 min cooldown

• Race simulation. VO2max = climbs/surges. Threshold = sustained race pace. This is competitive gravel racing for intermediate athletes.

• RHYTHM INTERVALS: For threshold blocks, use rhythm pattern: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 5, continuous. This simulates race variability.

• CADENCE WORK: VO2 intervals—alternate high and low cadence. Threshold blocks—use rhythm pattern.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="4" OnDuration="360" OnPower="1.12" Cadence="100" OffDuration="360" OffPower="0.55"/>
    <SteadyState Duration="900" Power="0.65" Cadence="85"/>
    <IntervalsT Repeat="2" OnDuration="900" OnPower="1.02" Cadence="100" OffDuration="480" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W09 Thu - Easy Endurance", """• Recovery between quality sessions. Keep it truly easy.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W09 Fri - Easy Endurance", """• Building easy volume. Aerobic base maintenance.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="7200" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W09 Sat - HARD Session #2: Race-Pace Blocks", """• STRUCTURE:
20 min warmup → 2x25 min @ 100-105% FTP (10 min easy) → 20 min cooldown

• Long threshold blocks. Race pace for extended periods. Should feel strong and controlled.

• CADENCE WORK: Mix cadences—first interval high cadence (100+ rpm), second low cadence (40-60 rpm) or use rhythm pattern.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="1500" OnPower="1.02" Cadence="100" OffDuration="600" OffPower="0.55"/>
    <Cooldown Duration="1200" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W09 Sun - Long Easy Endurance", """• Long easy ride after quality. Eat 80g carbs/hour. Dial in race nutrition.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="16200" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 10: Peak Phase - Final Quality
weeks.append({
    "week_number": 10,
    "focus": "Peak Phase - Final Quality",
    "volume_percent": 95,
    "volume_hours": "11.5-14",
    "workouts": [
        create_workout("W10 Mon - Rest", """• Final quality block. Second-to-last build week. You should feel fit and strong now. Two more weeks of quality, then taper. Focus on execution, recovery, and race logistics.

• WEEK PREVIEW: Final quality block. Wednesday has peak quality (VO2max + threshold). Saturday has race pace (3x20 min). Sunday is final long race simulation (dress rehearsal). Make these workouts count.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W10 Tue - Easy Endurance", """• Long easy ride. Keep it conversational. Build aerobic volume.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="7200" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W10 Wed - HARD Session #1: Peak Quality", """• STRUCTURE:
20 min warmup → 5x5 min @ 110-115% FTP (5 min easy) → 15 min easy → 2x20 min @ 100-105% FTP (8 min easy) → 15 min cooldown

• Final big quality before taper. Should feel powerful.

• RHYTHM INTERVALS: For threshold blocks, use rhythm pattern: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 6, continuous.

• CADENCE WORK: VO2 intervals—alternate high and low cadence. Threshold blocks—use rhythm pattern.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="5" OnDuration="300" OnPower="1.12" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="900" Power="0.65" Cadence="85"/>
    <IntervalsT Repeat="2" OnDuration="1200" OnPower="1.02" Cadence="100" OffDuration="480" OffPower="0.55"/>
    <SteadyState Duration="900" Power="0.65" Cadence="85"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W10 Thu - Easy Endurance", """• Recovery between quality sessions. Truly easy. Resist all urges to push.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W10 Fri - Easy Endurance", """• Building final aerobic volume. Easy pace. Conversational.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="7200" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W10 Sat - HARD Session #2: Race Pace", """• STRUCTURE:
20 min warmup → 3x20 min @ 100-105% FTP (8 min easy) → 20 min cooldown

• Three 20-minute threshold blocks. This is your race pace for extended periods. You should feel strong and controlled here—weeks of training paying off. Execute cleanly.

• LOADED INTERVALS: For one interval, try loaded pattern: 1 min Z5/Z6 (high cadence, seated) → settle into 19 min Z3 (self-selected cadence). This simulates race starts.

• CADENCE WORK: Mix cadences or use loaded/rhythm patterns.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="1200" OnPower="1.02" Cadence="100" OffDuration="480" OffPower="0.55"/>
    <Cooldown Duration="1200" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W10 Sun - Long Easy Simulation", """• STRUCTURE:
Z2 with 3x20 min @ 90-95% FTP scattered through hours 2-4 (8 min easy between)

• Final race rehearsal. Eat 80-90g carbs/hour.

• CADENCE WORK: Mix cadences on efforts.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="6000" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="1200" OnPower="0.93" Cadence="100" OffDuration="480" OffPower="0.55"/>
    <SteadyState Duration="6000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 11: Taper Week
weeks.append({
    "week_number": 11,
    "focus": "Taper Week",
    "volume_percent": 70,
    "volume_hours": "8.5-10.5",
    "workouts": [
        create_workout("W11 Mon - Rest", """• Taper begins. Volume drops 30%, intensity stays sharp but reduced. You should feel increasingly fresh each day while maintaining sharpness. Legs should feel snappy. Power should come easy. That's fitness + freshness = form.

• WEEK PREVIEW: Taper begins. Wednesday has race openers (reduced volume, maintained intensity). Saturday has moderate endurance with openers (final reminder workout). Volume drops, intensity stays sharp.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W11 Tue - Easy Endurance", """• Easy ride. You're tapering now. Enjoy the lower volume.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W11 Wed - Taper Quality", """• STRUCTURE:
15 min warmup → 3x10 min @ 100-105% FTP (5 min easy) → 3x2 min @ 110-115% FTP (2 min easy) → 15 min cooldown

• Reduced volume, maintained intensity. Still polarized.

• CADENCE WORK: High cadence on all efforts (100+ rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="3" OnDuration="600" OnPower="1.02" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <IntervalsT Repeat="3" OnDuration="120" OnPower="1.12" Cadence="100" OffDuration="120" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W11 Thu - Easy Endurance", """• Easy recovery. Your body is absorbing fitness and gaining freshness.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W11 Fri - Easy Endurance", """• Easy day. Just moving blood through legs. No stress.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W11 Sat - Taper Long Ride", """• STRUCTURE:
First 90 min Z2 → 3x10 min @ 95-100% FTP (5 min easy) → Final 60-90 min Z2

• Shorter long ride but maintains race-intensity efforts. Should feel strong and controlled. This is your final "reminder" workout before race week.

• CADENCE WORK: Mix cadences on threshold blocks.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4800" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="600" OnPower="0.98" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W11 Sun - Easy Endurance", """• Easy recovery. You're one week from race week now. Trust the process.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 12: Race Week
weeks.append({
    "week_number": 12,
    "focus": "Race Week",
    "volume_percent": 40,
    "volume_hours": "5-7.5",
    "workouts": [
        create_workout("W12 Mon - Rest", """• Race week. Volume drops dramatically. Intensity stays sharp but brief. You should feel fresh, powerful, ready. Nervous energy is normal—channel it into final prep. Check bike. Pack bags. Review race plan. Trust your training—polarized distribution got you here.

• WEEK PREVIEW: Race week! Wednesday has final openers (sharpness check). Thursday is easy or rest. Friday is pre-race shake-out. Saturday/Sunday: RACE DAY!

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W12 Tue - Easy", """• Easy spin. Just moving legs. No stress.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W12 Wed - Final Openers", """• STRUCTURE:
15 min easy → 3x5 min @ 95-100% FTP (3 min easy) → 3x2 min @ 110% FTP (2 min easy) → 4x30sec @ 115% FTP (90sec easy) → 10 min easy

• Final sharpness check. Should feel powerful, snappy, explosive. If legs feel dead, add another rest day. This is your sharpness check—power should come easily.

• CADENCE WORK: High cadence on all efforts (100+ rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="3" OnDuration="300" OnPower="0.98" Cadence="100" OffDuration="180" OffPower="0.55"/>
    <IntervalsT Repeat="3" OnDuration="120" OnPower="1.10" Cadence="100" OffDuration="120" OffPower="0.55"/>
    <IntervalsT Repeat="4" OnDuration="30" OnPower="1.15" Cadence="100" OffDuration="90" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W12 Thu - Easy or Rest", """• Optional: 60 min Z2

• If race is Sunday, easy spin today. If race is Saturday, consider rest. Listen to your body. Trust your fitness.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W12 Fri - Pre-Race Shake-Out", """• STRUCTURE:
15 min easy → 3x3 min @ race pace (2 min easy) → 3x90sec @ 110% FTP (2 min easy) → 3x30sec @ 115% FTP (90sec easy) → 10 min easy

• Final ride before race. Legs should feel fresh and powerful. Check bike one last time. Test race-day tire pressure. Visualize race execution. You're ready.

• CADENCE WORK: High cadence on all efforts (100+ rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="3" OnDuration="180" OnPower="0.98" Cadence="100" OffDuration="120" OffPower="0.55"/>
    <IntervalsT Repeat="3" OnDuration="90" OnPower="1.10" Cadence="100" OffDuration="120" OffPower="0.55"/>
    <IntervalsT Repeat="3" OnDuration="30" OnPower="1.15" Cadence="100" OffDuration="90" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W12 Sat - Race or Rest", """• If racing Saturday: EXECUTE YOUR PLAN

• If racing Sunday: Rest or 30-45 min easy Z2 with 2x30sec openers

• Notes: If racing today—trust your training, pace yourself early, fuel aggressively, stay mentally engaged. You've done the work. Now execute.""", """    <FreeRide Duration="60"/>
"""),
        create_workout("W12 Sun - Race or Recovery", """• If racing Sunday: EXECUTE YOUR PLAN

• If raced Saturday: Easy 30-60 min recovery spin, celebrate, eat everything

• Notes: Race day. Start conservatively. Fuel early and often. When it hurts, everyone hurts—who handles it better? That's you. You trained for this.""", """    <FreeRide Duration="60"/>
""")
    ]
})

# Create complete template
template = {
    "plan_metadata": plan_metadata,
    "weeks": weeks,
    "default_modifications": {
        "polarized_philosophy": {
            "enabled": True,
            "description": "80% easy (Z1-Z2), 20% hard (Z4-Z5+), almost nothing in the middle (Z3 avoided except transitions)"
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
            "weeks": [7, 10],
            "description": "1 min Z5/Z6 (high cadence, seated) → settle into 11-19 min Z3 (self-selected cadence). Simulates race starts and surges."
        },
        "strength_training": {
            "enabled": False,
            "note": "Athlete performs own strength program. Suggested on lighter training days."
        },
        "monday_week_preview": {
            "enabled": True,
            "description": "Monday rest days include week preview with key workouts, polarization reminders, and competitive performance guidance"
        },
        "rest_day_tss_limit": 30,
        "rest_day_duration_limit_hours": 1
    }
}

# Save complete template
output_path = "/Users/mattirowe/Documents/Gravel Landing Page Project/current/plans/10. Compete Intermediate (12 weeks)/template.json"
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
print(f"   ✅ Polarized 80/20 philosophy applied")
print(f"   ✅ Changing Pace philosophy integrated (cadence work, rhythm/loaded intervals)")

