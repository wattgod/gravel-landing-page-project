#!/usr/bin/env python3
"""
Build complete JSON template for FINISHER MASTERS (12 weeks)
Autoregulated (HRV-Based) + Polarized with Changing Pace philosophy
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
    "name": "FINISHER MASTERS",
    "duration_weeks": 12,
    "philosophy": "Autoregulated (HRV-Based) + Polarized",
    "target_hours": "8-12",
    "target_athlete": "Age 50+, performance-minded finisher, has 8-12 hours weekly",
    "goal": "Strong competitive finish with age-appropriate training and smart recovery"
}

weeks = []

# WEEK 1: Foundation Assessment & Dual Philosophy Introduction
weeks.append({
    "week_number": 1,
    "focus": "Foundation Assessment & Dual Philosophy Introduction",
    "volume_percent": 70,
    "volume_hours": "5.5-8.5",
    "workouts": [
        create_workout("W01 Mon - Rest", """• Welcome to Masters Performance training with DUAL safeguards. You're 50+ pursuing strong finishes (not just completion). You have 8-12 hours weekly—enough for performance IF trained intelligently. This plan combines TWO proven approaches: (1) Autoregulation via HRV monitoring, and (2) Polarized distribution (80% easy, 20% hard). Check HRV daily if possible. High/normal = green light for quality. Low = easy day or rest. No HRV tracker? Use perceived recovery: good sleep + fresh legs = go. Poor sleep + heavy legs = back off. Polarized = easy days TRULY easy (Z1-Z2), hard days TRULY hard (Z4-Z5+), almost nothing in middle. Masters principle: recovery IS training at 50+.

• WEEK PREVIEW: Foundation week. Tuesday has FTP test (if HRV green). Saturday is first long easy ride (2-2.5 hours). Sunday includes critical strength work—non-negotiable for 50+ athletes. Track HRV daily to establish baseline.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W01 Tue - FTP Test (if HRV green)", """• STRUCTURE:
15 min warmup → 3 min moderate → 5 min easy → 20 min sustained effort (not all-out, controlled max) → 10 min cooldown

• HRV Check: Green? Do test. Yellow? Ride 45 min easy, try tomorrow. Red? Skip, test next week. Masters FTP testing: sustained 20-min at "hard but controlled" pace. Multiply avg power × 0.93 (conservative for 50+). This sets zones for polarized training: Z1-Z2 = 55-75% FTP (easy), Z4-Z5+ = 95%+ FTP (hard). Write everything down.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <SteadyState Duration="180" Power="0.85"/>
    <SteadyState Duration="300" Power="0.55"/>
    <SteadyState Duration="1200" Power="1.00"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W01 Wed - Easy Endurance (Polarized Easy)", """• First polarized easy day after testing. CONVERSATIONAL PACE. If you can't speak full sentences, you're going too hard. This is the "80" in 80/20. Masters athletes MUST keep easy days easy—this is where you recover for hard sessions. Feels slow? Perfect.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2700" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W01 Thu - Easy Endurance (if recovered from test)", """• Readiness Check: Feeling good after Tuesday test? Ride easy today. Still tired? Take rest day. Masters athletes often need 48+ hours recovery after maximal efforts. Easy means EASY—conversational entire time.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2700" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W01 Fri - Rest", """• Scheduled rest day. Non-negotiable for Masters. Your body needs this before weekend.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W01 Sat - Long Easy Endurance (Polarized Volume)", """• Readiness Check: Slept well + legs feel fresh? Do 2-2.5 hours. Poor sleep or tired? Do 90 min. Longest ride of week. CONVERSATIONAL PACE entire time. This is polarized foundation—long, easy, aerobic. Builds mitochondrial density and durability without crushing Masters bodies. Eat 50-60g carbs/hour. Practice race fueling.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="7200" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W01 Sun - Easy Endurance + Max Strength (Priority)", """• Easy ride then CRITICAL strength work. Strength training 2x/week is NON-NEGOTIABLE for 50+ athletes—prevents sarcopenia (muscle loss), maintains bone density, builds power-to-weight ratio. Masters athletes lift HEAVY (perfect form) during base phase. This is injury prevention AND performance. Rest 3-4 min between heavy sets. This matters as much as cycling.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Heavy back squats, trap bar deadlifts, weighted planks, Bulgarian split squats, single-leg RDLs (4x6-8 heavy @ 85-88% estimated 1RM, rest 3-4 min between sets). Max strength phase for Masters. Perfect form always. This is injury prevention AND performance. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2700" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 2: Polarized Base Building with Autoregulation
weeks.append({
    "week_number": 2,
    "focus": "Polarized Base Building with Autoregulation",
    "volume_percent": 80,
    "volume_hours": "6.5-9.5",
    "workouts": [
        create_workout("W02 Mon - Rest", """• Week 2 builds polarized structure: ONE hard session, EVERYTHING else easy. This is 80/20—most time spent easy (building aerobic base), small amount hard (building top-end fitness). HRV determines IF you do hard session. This dual approach (polarized + autoregulated) is perfect for Masters: easy days stay easy for recovery, hard days can be truly hard because you're recovered.

• WEEK PREVIEW: Polarized structure week. Wednesday introduces first hard session (VO2max intervals—if HRV green). Saturday is longest ride yet (2.5-3 hours). Sunday continues max strength work. Remember: easy days easy, hard days hard.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W02 Tue - Easy Endurance", """• Easy day before first hard session. Conversational pace. Save energy for tomorrow.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2700" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W02 Wed - HARD Session #1: VO2max Introduction (if HRV green)", """• STRUCTURE:
15 min warmup → 4x3 min @ 110-115% FTP (3 min easy recovery between) → 15 min cooldown

• Readiness Check: HRV green + slept well? Full workout. HRV yellow? 4x2 min @ 108% instead. HRV red? Ride 45 min easy, skip intervals. First HARD day—this is the "20" in 80/20. Lungs burning, legs screaming by end of each interval. But FULL RECOVERY between reps—Masters athletes need this. Don't cheat rest intervals. Quality over quantity at 50+.

• CADENCE WORK: Alternate high cadence (100+ rpm seated) and low cadence (40-60 rpm seated, big gear) on intervals. This teaches power production in different ways.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="4" OnDuration="180" OnPower="1.12" Cadence="100" OffDuration="180" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W02 Thu - Easy Endurance", """• Day after hard session. SUPER easy. Active recovery only. This enables next quality session. Masters rule: easy days enable hard days.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2700" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W02 Fri - Easy Endurance (if feeling good)", """• Readiness Check: Easy ride if recovered. Still tired from Wednesday? Take rest day instead. No penalty for extra rest at 50+.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W02 Sat - Long Easy Endurance", """• Readiness Check: Green light + good sleep? Do 2.5-3 hours. Yellow? Do 2 hours. Red? 90 min easy. Longest ride yet. Day after hard session = tired legs possible, but keep power LOW. Conversational pace. Pure aerobic volume. Eat 60g carbs/hour.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="9000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W02 Sun - Easy Endurance + Max Strength", """• Easy ride then progressive strength. If last week felt manageable, add 2-5% weight today. Perfect form always. This builds durability for gravel racing. Rest fully between sets—this is max strength work, not cardio.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Heavy front squats, Romanian deadlifts, weighted step-ups, Copenhagen planks, pallof press (4x6-8 heavy, rest 3-4 min). Max strength phase. Progressive overload—add 2-5% if last week felt good. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2700" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 3: Volume Progression with Polarized Discipline
weeks.append({
    "week_number": 3,
    "focus": "Volume Progression with Polarized Discipline",
    "volume_percent": 90,
    "volume_hours": "7-11",
    "workouts": [
        create_workout("W03 Mon - Rest", """• Week 3 adds SECOND hard session (still only ~20% of weekly time). By Sunday you should feel accumulated fatigue IF recovering well. Masters checkpoint: good sleep (7-8+ hours), adequate protein (1.6-2g/kg bodyweight), stress managed. If crushed by Wednesday, you're pushing too hard or life stress is high. Back off immediately.

• WEEK PREVIEW: Volume progression week. Wednesday introduces threshold intervals (if HRV green). Saturday has VO2max progression (5x3 min). Sunday is longest ride (2.5-3.5 hours). Two hard sessions this week, everything else easy.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W03 Tue - Easy Endurance", """• Easy day before quality. Building aerobic volume. Conversational pace.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W03 Wed - HARD Session #1: Threshold Introduction (if HRV green)", """• STRUCTURE:
15 min warmup → 3x10 min @ 100-105% FTP (5 min easy recovery between) → 15 min cooldown

• Readiness Check: Green? Full workout. Yellow? 3x8 min @ 98-100%. Red? 60 min easy, skip intervals. Just above FTP. Hard but controllable. Breathing labored but rhythmic. This is race pace for Masters. Should finish thinking "maybe one more." Long warmup/cooldown maintains polarization—only intervals are hard.

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="600" OnPower="1.02" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W03 Thu - Easy Endurance", """• Recovery between hard sessions. Keep it truly easy.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2700" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W03 Fri - Easy Endurance", """• Another easy day. Building volume before weekend hard session.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W03 Sat - HARD Session #2: VO2max Progression (if HRV green)", """• STRUCTURE:
15 min warmup → 5x3 min @ 110-115% FTP (3 min easy recovery between) → 15 min cooldown

• Readiness Check: Green + slept well? Full 5 intervals. Yellow? 4x3 min. Red? 60 min easy ride. One more interval than Week 2. These hurt—that's adaptation. Full recovery between reps mandatory for Masters. Don't push through compromised form.

• CADENCE WORK: Alternate high and low cadence. Intervals 1, 3, 5 at high cadence (100+ rpm), intervals 2, 4 at low cadence (40-60 rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="5" OnDuration="180" OnPower="1.12" Cadence="100" OffDuration="180" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W03 Sun - Long Easy Endurance + Max Strength", """• Readiness Check: Long ride only if feeling recovered. Otherwise 2 hours. Day after VO2max = tired legs possible. Keep it EASY—conversational pace. Eat 60-70g carbs/hour. Heavy strength maintains max force production. Progressive overload continues—add weight if last week felt good.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Heavy back squats, trap bar deadlifts, weighted carries, heavy single-leg work (4x6-8 heavy, rest 3-4 min). Max strength phase. Progressive overload. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="10800" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 4: Recovery & Adaptation
weeks.append({
    "week_number": 4,
    "focus": "Recovery & Adaptation",
    "volume_percent": 60,
    "volume_hours": "5-7",
    "workouts": [
        create_workout("W04 Mon - Rest", """• Recovery week. Masters athletes NEED this more than younger athletes. You should feel tired Monday, fresh by Friday. This is when adaptation happens—your body gets stronger during rest. If not recovered by Sunday, you pushed too hard in Week 3 or have life stress/sleep issues to address. One light quality session this week, everything else easy.

• WEEK PREVIEW: Recovery week. Wednesday has light quality touch (if HRV good). Rest of week is easy endurance. Strength transitions to explosive work (prepares for Build phase). This is when adaptation happens.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W04 Tue - Easy Endurance", """• Truly easy. Enjoy low stress riding. Just moving legs.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2700" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W04 Wed - Light Quality Touch (if HRV good)", """• STRUCTURE:
10 min warmup → 3x6 min @ 98-102% FTP (4 min easy between) → 10 min cooldown

• Readiness Check: Feeling recovered? Do light intervals. Still tired? Skip, ride 45 min easy instead. Reduced volume, maintained intensity. Should feel controlled. This reminds body what hard feels like without crushing it.

• CADENCE WORK: Mix cadences—one high, one low, one self-selected.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="3" OnDuration="360" OnPower="1.00" Cadence="90" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W04 Thu - Easy Endurance", """• Easy day. Your body is adapting during rest.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1800" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W04 Fri - Easy Endurance", """• Easy day. Fitness increasing while resting. Trust it.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2700" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W04 Sat - Moderate Easy Endurance", """• No intensity. Just aerobic time. Practice skills—bike handling, cornering. Check equipment. Ensure bike fit is perfect for Masters body—comfort prevents injury.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W04 Sun - Optional Easy Spin + Explosive Strength Transition", """• Skip ride if tired. Strength transitions to explosive work—preparing for Build phase intensity. Light loads, maximum velocity. This bridges max strength to power production for 50+ athletes. Masters-specific: lower jump heights, focus on movement quality over height/distance.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Box jumps (lower height for Masters), medicine ball slams, jump squats (bodyweight or light load), power cleans (light) (3x6-8 explosive). Explosive strength phase. Light loads, maximum velocity. Masters-specific: lower jump heights, focus on movement quality. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2700" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 5: Build Phase - Intensity Introduction
weeks.append({
    "week_number": 5,
    "focus": "Build Phase - Intensity Introduction",
    "volume_percent": 85,
    "volume_hours": "7-10",
    "workouts": [
        create_workout("W05 Mon - Rest", """• Build phase begins. Weeks 5-8 increase both volume and intensity based on YOUR recovery. Two quality sessions per week, everything else easy—that's polarization. Autoregulation determines execution. HRV/readiness green = push. Yellow = modify. Red = back off. Masters athletes work WITH bodies, not against them.

• WEEK PREVIEW: Build phase begins. Wednesday has extended threshold (3x12 min). Saturday has VO2max development (5x4 min). Intensity increases, but easy days stay easy. Strength shifts to explosive work.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W05 Tue - Easy Endurance", """• Long easy ride before quality. Building base while fresh.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W05 Wed - HARD Session #1: Threshold Development (if HRV green)", """• STRUCTURE:
15 min warmup → 3x12 min @ 100-105% FTP (6 min easy between) → 15 min cooldown

• Readiness Check: Green? Full workout. Yellow? 3x10 min @ 98-100%. Red? 60 min easy. Longer threshold than Week 4. Race pace training. Stay smooth, breathe rhythmically. Masters execution: controlled starts, steady power, strong finishes.

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="720" OnPower="1.02" Cadence="100" OffDuration="360" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W05 Thu - Easy Endurance", """• Recovery from threshold. Keep it genuinely easy.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2700" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W05 Fri - Easy Endurance", """• Another easy day before weekend quality.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W05 Sat - HARD Session #2: VO2max Development (if HRV green)", """• STRUCTURE:
15 min warmup → 5x4 min @ 110-115% FTP (4 min easy between) → 15 min cooldown

• Readiness Check: Green + slept well? Full 5x4. Yellow? 5x3 min. Red? 60 min easy. Longer intervals than Week 3. Building VO2max capacity. Full recovery between reps—don't cheat rest intervals at 50+.

• CADENCE WORK: Alternate high and low cadence. Intervals 1, 3, 5 at high cadence (100+ rpm), intervals 2, 4 at low cadence (40-60 rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="5" OnDuration="240" OnPower="1.12" Cadence="100" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W05 Sun - Long Easy Endurance + Explosive Strength", """• Readiness Check: Long ride if recovered. Otherwise 2 hours. Day after VO2max = tired legs. Keep power LOW. Conversational pace. Fuel: 60-70g carbs/hour. Explosive strength supports power production.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Jump squats, box jumps, med ball work, explosive step-ups (3x6-8 explosive). Explosive strength supports power production. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="10800" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 6: Build Phase - Volume + Intensity Progression
weeks.append({
    "week_number": 6,
    "focus": "Build Phase - Volume + Intensity Progression",
    "volume_percent": 95,
    "volume_hours": "7.5-11.5",
    "workouts": [
        create_workout("W06 Mon - Rest", """• Volume and intensity both increase IF readiness stays green. By Saturday you should feel accumulated fatigue but not destroyed. If exhausted by Wednesday, you're violating polarization—easy days creeping into Z3. Masters discipline: keep easy EASY so hard can be HARD.

• WEEK PREVIEW: Volume + intensity progression. Wednesday has long threshold (2x20 min). Saturday combines VO2max + threshold (big workout). Sunday is longest ride yet (3-4 hours). This week builds race-specific fitness.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W06 Tue - Easy Endurance", """• Long easy ride. Building base.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4500" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W06 Wed - HARD Session #1: Long Threshold (if HRV green)", """• STRUCTURE:
15 min warmup → 2x20 min @ 100-105% FTP (8 min easy between) → 15 min cooldown

• Readiness Check: Green? Full 2x20. Yellow? 2x15 min. Red? 60 min easy. Classic threshold work for Masters. 40 cumulative minutes at race pace. Break 20-min blocks into 5-min segments mentally. Stay smooth, controlled breathing.

• CADENCE WORK: First interval at high cadence (100+ rpm), second at low cadence (40-60 rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="1200" OnPower="1.02" Cadence="100" OffDuration="480" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W06 Thu - Easy Endurance", """• Recovery between quality sessions. Super easy.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2700" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W06 Fri - Easy Endurance", """• Easy day before weekend.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W06 Sat - HARD Session #2: Mixed Intervals (if HRV green)", """• STRUCTURE:
15 min warmup → 5x4 min @ 110-115% FTP (4 min easy between) → 15 min easy → 2x10 min @ 100-105% FTP (5 min easy between) → 10 min cooldown

• Readiness Check: Green + good sleep? Full workout. Yellow? 4x3 min VO2 + 2x8 min threshold. Red? 60 min easy. Combined stimulus. VO2 when fresh, threshold when fatigued. Take rest intervals seriously—stay Z1-Z2, not Z3.

• RHYTHM INTERVALS: For threshold blocks, try rhythm pattern: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 3, continuous. This simulates race variability.

• CADENCE WORK: VO2 intervals—alternate high and low cadence. Threshold blocks—use rhythm pattern or mix cadences.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="5" OnDuration="240" OnPower="1.12" Cadence="100" OffDuration="240" OffPower="0.55"/>
    <SteadyState Duration="900" Power="0.65" Cadence="85"/>
    <IntervalsT Repeat="2" OnDuration="600" OnPower="1.02" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W06 Sun - Long Easy Endurance + Explosive Strength", """• Readiness Check: Longest ride yet. Only if recovered. Day after big quality. Keep it EASY. Conversational pace. Eat 70g carbs/hour. Test race gear. Explosive strength maintains power.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Explosive movements—jump squats, box jumps, med ball (3x6-8). Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="10800" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 7: Build Phase - Peak Training Load
weeks.append({
    "week_number": 7,
    "focus": "Build Phase - Peak Training Load",
    "volume_percent": 100,
    "volume_hours": "8-12",
    "workouts": [
        create_workout("W07 Mon - Rest", """• Biggest week. By Sunday you should feel significant accumulated fatigue—that's expected IF recovering well (good sleep, nutrition, stress management). If crushed by Wednesday, STOP and rest. Masters athletes must respect fatigue. Week 8 is recovery. Push through IF readiness stays green or yellow.

• WEEK PREVIEW: Peak training load week. Wednesday has peak threshold (3x15 min). Saturday combines VO2max + threshold (big workout). Sunday is longest ride (3.5-4.5 hours). This is your "A" week.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W07 Tue - Easy Endurance", """• Long easy ride. Save energy for tomorrow.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4500" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W07 Wed - HARD Session #1: Peak Threshold (if HRV green)", """• STRUCTURE:
15 min warmup → 3x15 min @ 100-105% FTP (7 min easy between) → 15 min cooldown

• Readiness Check: Green? Full 3x15. Yellow? 3x12 min. Red? 60 min easy. Three 15-minute blocks—45 cumulative minutes at race pace. Hard for Masters. Pace yourself—controlled execution. One interval at a time.

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected or rhythm pattern.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="900" OnPower="1.02" Cadence="100" OffDuration="420" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W07 Thu - Easy Endurance", """• Truly easy after yesterday's threshold.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2700" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W07 Fri - Easy Endurance", """• Easy day. Building volume before Saturday.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4500" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W07 Sat - HARD Session #2: VO2max + Threshold (if HRV green)", """• STRUCTURE:
15 min warmup → 5x3 min @ 110-115% FTP (3 min easy) → 15 min easy → 2x12 min @ 100-105% FTP (6 min easy) → 10 min cooldown

• Readiness Check: Green + slept well? Full workout. Yellow? 4x3 min VO2 + 2x10 min threshold. Red? 60 min easy. Big quality day. VO2 efforts then threshold. Break down mentally—one interval at a time.

• LOADED INTERVALS: For threshold blocks, try loaded pattern: 1 min Z5/Z6 (high cadence, seated) → settle into 11 min Z3 (self-selected cadence). This simulates race starts.

• CADENCE WORK: VO2 intervals—alternate high and low cadence. Threshold blocks—use loaded pattern or rhythm pattern.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="5" OnDuration="180" OnPower="1.12" Cadence="100" OffDuration="180" OffPower="0.55"/>
    <SteadyState Duration="900" Power="0.65" Cadence="85"/>
    <IntervalsT Repeat="2" OnDuration="720" OnPower="1.02" Cadence="100" OffDuration="360" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W07 Sun - Long Easy Endurance + Stability Strength", """• Readiness Check: Longest ride of plan. Only if recovered. Day after big quality. Keep EASY. Conversational pace. Fuel properly: 70-80g carbs/hour. Test everything. Strength shifts to stability—injury prevention for Masters at peak load.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Single-leg stability, planks, anti-rotation, core endurance (3x12-15). Stability strength phase. Injury prevention for Masters at peak load. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="14400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 8: Recovery & Absorption
weeks.append({
    "week_number": 8,
    "focus": "Recovery & Absorption",
    "volume_percent": 60,
    "volume_hours": "5-7",
    "workouts": [
        create_workout("W08 Mon - Rest", """• Recovery week after biggest block. Masters especially need this. Tired Monday, fresh by Friday. This is when adaptation happens—fitness increases during rest. If not recovered by Sunday, address sleep, nutrition, or life stress.

• WEEK PREVIEW: Recovery week. Wednesday has light quality (if HRV good). Rest of week is easy endurance. Strength transitions to durability (higher reps, lower weight). This is when adaptation happens.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W08 Tue - Easy", """• Truly easy. Enjoy the break from intensity.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2700" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W08 Wed - Light Quality (if HRV good)", """• STRUCTURE:
10 min warmup → 3x8 min @ 98-102% FTP (4 min easy) → 10 min cooldown

• Readiness Check: HRV good? Do light intervals. Still tired? Skip, ride easy instead. Maintaining fitness without adding fatigue.

• CADENCE WORK: Mix cadences—one high, one low, one self-selected.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="3" OnDuration="480" OnPower="1.00" Cadence="90" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W08 Thu - Easy", """• Easy day. Your body is adapting.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1800" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W08 Fri - Easy", """• Easy day. Fitness increasing while resting.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2700" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W08 Sat - Moderate Easy", """• No intensity. Just aerobic time. Practice skills. Check equipment.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W08 Sun - Optional Spin + Durability Strength", """• Skip ride if tired. Strength transitions to durability—higher reps, lower weight for muscular endurance supporting long gravel races.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Higher reps—goblet squats, step-ups, planks (3x15-20). Durability strength phase. Higher reps, lower weight for muscular endurance. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2700" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 9: Peak Phase - Race Specificity
weeks.append({
    "week_number": 9,
    "focus": "Peak Phase - Race Specificity",
    "volume_percent": 90,
    "volume_hours": "7-11",
    "workouts": [
        create_workout("W09 Mon - Rest", """• Peak phase begins. Final four weeks before race day. Training becomes race-specific now—long sustained efforts, race-pace blocks, gravel simulation. You've built the engine. Now we tune it for race day performance. Maintain strict polarization and autoregulation. Two quality sessions per week, everything else easy.

• WEEK PREVIEW: Peak phase begins. Wednesday has VO2max intervals (sharpens top end). Saturday has race-pace threshold (2x25 min). Sunday is long easy ride. Practice race nutrition aggressively (70-80g carbs/hour on long rides).

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W09 Tue - Easy Endurance", """• Long easy ride. Pure aerobic work. Keep it conversational. This is the "80" in polarized 80/20.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="6000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W09 Wed - HARD Session #1: VO2max (if HRV green)", """• STRUCTURE:
15 min warmup with openers → 6x4 min @ 110-115% FTP (4 min easy between) → 15 min cooldown

• Readiness Check: Green? Full workout. Yellow? 5x4 min. Red? 60 min easy. VO2max work sharpens your top end. These should feel hard but doable—your threshold fitness makes these easier. Embrace the burn.

• CADENCE WORK: Alternate high and low cadence. Intervals 1, 3, 5 at high cadence (100+ rpm), intervals 2, 4, 6 at low cadence (40-60 rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <SteadyState Duration="30" Power="1.10"/>
    <SteadyState Duration="30" Power="0.55"/>
    <SteadyState Duration="30" Power="1.10"/>
    <SteadyState Duration="30" Power="0.55"/>
    <SteadyState Duration="30" Power="1.10"/>
    <SteadyState Duration="30" Power="0.55"/>
    <IntervalsT Repeat="6" OnDuration="240" OnPower="1.12" Cadence="100" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W09 Thu - Easy Endurance", """• Recovery between quality sessions. Keep it truly easy.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W09 Fri - Easy Endurance", """• Building easy volume. Aerobic base maintenance.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="6000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W09 Sat - HARD Session #2: Race-Pace Threshold (if HRV green)", """• STRUCTURE:
15 min warmup → 2x25 min @ 100-105% FTP (10 min easy between) → 15 min cooldown

• Readiness Check: Green? Full workout. Yellow? 2x20 min. Red? 60 min easy. Threshold work should feel easier after recovery week. This is your race pace—sustainable, controlled, strong. Practice drinking while holding power.

• RHYTHM INTERVALS: For one interval, try rhythm pattern: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 8, continuous. This simulates race variability.

• CADENCE WORK: Mix cadences or use rhythm pattern.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="1500" OnPower="1.02" Cadence="100" OffDuration="600" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W09 Sun - Long Easy + Durability Strength", """• Long easy ride. Pure durability training. Strength shifts to higher reps, lower weight—muscular endurance for long gravel races. Eat 70-80g carbs/hour.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Higher rep work—goblet squats, step-ups, planks (3x15-20). Durability strength phase. Higher reps, lower weight for muscular endurance. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="14400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 10: Peak Phase - Race Specificity
weeks.append({
    "week_number": 10,
    "focus": "Peak Phase - Race Specificity",
    "volume_percent": 95,
    "volume_hours": "7.5-11.5",
    "workouts": [
        create_workout("W10 Mon - Rest", """• Realization phase. Final push before taper. Training is race-specific now—long sustained efforts, variability simulation, race-pace blocks. You've built the engine, sharpened it, now we tune it precisely for race day. Two more weeks of quality, then taper.

• WEEK PREVIEW: Race specificity week. Wednesday has mixed race efforts (VO2max + threshold). Saturday has long race-pace blocks (3x20 min). Sunday is final long race simulation (dress rehearsal). Test ALL race-day equipment, nutrition, hydration.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W10 Tue - Easy Endurance", """• Long easy ride. Keep it conversational. Build aerobic volume.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="6000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W10 Wed - HARD Session #1: Race Simulation (if HRV green)", """• STRUCTURE:
15 min warmup → 4x6 min @ 110% FTP + 2x15 min @ 100-105% FTP (5-7 min easy between) → 15 min cooldown

• Readiness Check: Green? Full workout. Yellow? 3x5 min VO2 + 2x12 min threshold. Red? 60 min easy. Race simulation. VO2max efforts = hard climbs or surges. Threshold blocks = sustained race pace. This is exactly what gravel racing feels like. Variable power, constant effort.

• RHYTHM INTERVALS: For threshold blocks, use rhythm pattern: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 5, continuous.

• CADENCE WORK: VO2 intervals—alternate high and low cadence. Threshold blocks—use rhythm pattern.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="4" OnDuration="360" OnPower="1.10" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <IntervalsT Repeat="2" OnDuration="900" OnPower="1.02" Cadence="100" OffDuration="420" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W10 Thu - Easy Endurance", """• Recovery day. Your legs need this between quality sessions.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W10 Fri - Easy Endurance", """• Building volume without fatigue. Easy aerobic work.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="6000" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W10 Sat - HARD Session #2: Long Race-Pace Blocks (if HRV green)", """• STRUCTURE:
15 min warmup → 3x20 min @ 100-105% FTP (8 min easy between) → 15 min cooldown

• Readiness Check: Green? Full workout. Yellow? 3x15 min. Red? 60 min easy. Three 20-minute threshold blocks. This is your race pace for extended periods. You should feel strong and controlled here—weeks of training paying off. Execute cleanly.

• LOADED INTERVALS: For one interval, try loaded pattern: 1 min Z5/Z6 (high cadence, seated) → settle into 19 min Z3 (self-selected cadence). This simulates race starts.

• CADENCE WORK: Mix cadences or use loaded/rhythm patterns.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="1200" OnPower="1.02" Cadence="100" OffDuration="480" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W10 Sun - Long Race Simulation + Maintenance Strength", """• STRUCTURE:
First 2 hours Z2 → 2x30 min @ 90-95% FTP (10 min easy between) in hours 2-4 → Final hour Z2

• Readiness Check: Final long race simulation. Only if recovered. Sustained efforts when already tired = race day. Eat 70-90g carbs/hour. Test ALL race-day gear, nutrition, hydration. This is dress rehearsal.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Maintenance only—light loads, movement quality (2x8-10). Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="6000" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="2" OnDuration="1800" OnPower="0.93" Cadence="88" OffDuration="600" OffPower="0.55"/>
    <SteadyState Duration="3600" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 11: Taper Week
weeks.append({
    "week_number": 11,
    "focus": "Taper Week",
    "volume_percent": 70,
    "volume_hours": "5.5-8.5",
    "workouts": [
        create_workout("W11 Mon - Rest", """• Taper begins. Volume drops 30%, intensity stays sharp but reduced. You should feel increasingly fresh each day while maintaining sharpness. Check HRV—should trend up toward or above baseline. Masters athletes respond well to taper—recovery capacity means freshness returns quickly. Legs should feel snappy. Power should come easy. That's fitness + freshness = form.

• WEEK PREVIEW: Taper begins. Wednesday has race openers (reduced volume, maintained intensity). Saturday has moderate endurance with openers (final reminder workout). Volume drops, intensity stays sharp.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W11 Tue - Easy Endurance", """• Easy ride. You're tapering now. Enjoy the lower volume.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4500" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W11 Wed - Taper Quality (if HRV green)", """• STRUCTURE:
15 min warmup → 3x10 min @ 95-100% FTP + 3x90sec @ 110% FTP (5 min easy between all) → 15 min cooldown

• Readiness Check: Green? Full workout. Yellow? 3x8 min threshold + 3x60sec VO2. Red? 60 min easy. Reduced volume, maintained intensity. Threshold reminds body of race pace. VO2 openers keep top-end sharp. Should feel powerful and controlled.

• CADENCE WORK: High cadence on all efforts (100+ rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="3" OnDuration="600" OnPower="0.98" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <IntervalsT Repeat="3" OnDuration="90" OnPower="1.10" Cadence="100" OffDuration="210" OffPower="0.55"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
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

• Readiness Check: Shorter long ride but maintains race-intensity efforts. Should feel strong and controlled. This is your final "reminder" workout before race week.

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
    "volume_hours": "3-6",
    "workouts": [
        create_workout("W12 Mon - Rest", """• Race week. Volume drops dramatically. Intensity stays sharp but brief. Check HRV—should be at or above baseline. You should feel fresh, powerful, ready. Nervous energy is normal—channel it into final prep. Check bike. Pack bags. Review race plan. Trust your training—autoregulation + polarization got you here.

• WEEK PREVIEW: Race week! Wednesday has final sharpness session (race openers). Thursday is easy spin or rest. Friday is pre-race shake-out. Saturday/Sunday: RACE DAY!

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W12 Tue - Easy", """• Easy spin. Just moving legs. No stress. Stay off your feet when not riding.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1800" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W12 Wed - Race Openers (if HRV green)", """• STRUCTURE:
15 min easy → 3x4 min @ 95-100% FTP (3 min easy) → 3x90sec @ 110% FTP (2 min easy) → 3x30sec @ 115% FTP (90sec easy) → 10 min easy

• Readiness Check: Green? Full workout. Yellow? 3x3 min threshold + 3x60sec VO2. Red? 45 min easy. Final intensity before race. Should feel powerful, snappy, explosive. If legs feel dead, add another rest day. This is your sharpness check—power should come easily.

• CADENCE WORK: High cadence on all efforts (100+ rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="3" OnDuration="240" OnPower="0.98" Cadence="100" OffDuration="180" OffPower="0.55"/>
    <IntervalsT Repeat="3" OnDuration="90" OnPower="1.10" Cadence="100" OffDuration="120" OffPower="0.55"/>
    <IntervalsT Repeat="3" OnDuration="30" OnPower="1.15" Cadence="100" OffDuration="90" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W12 Thu - Easy or Rest", """• Optional: 30-45 min Z2

• If race is Sunday, easy spin today. If race is Saturday, consider rest. Listen to your body. Trust your fitness.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W12 Fri - Pre-Race Shake-Out", """• STRUCTURE:
15 min easy → 3x3 min @ race pace (2 min easy) → 3x1 min @ 110% FTP (2 min easy) → 2x30sec @ 115% FTP (90sec easy) → 10 min easy

• Final ride before race. Legs should feel fresh and powerful. Check bike one last time. Test race-day tire pressure. Visualize race execution. You're ready.

• CADENCE WORK: High cadence on all efforts (100+ rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="3" OnDuration="180" OnPower="0.98" Cadence="100" OffDuration="120" OffPower="0.55"/>
    <IntervalsT Repeat="3" OnDuration="60" OnPower="1.10" Cadence="100" OffDuration="120" OffPower="0.55"/>
    <IntervalsT Repeat="2" OnDuration="30" OnPower="1.15" Cadence="100" OffDuration="90" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W12 Sat - Race Day or Rest", """• If racing Saturday: EXECUTE YOUR PLAN

• If racing Sunday: Complete rest or 20-30 min easy spin with 3x30sec openers

• Notes: If racing today—start conservatively (50+ bodies warm up slower), fuel from the start (50-60g carbs/hour MINIMUM), pace smart (you can accelerate in final third if feeling good), strong finish (durability training pays off late). Autoregulation + Polarization prepared you for this. Trust it.""", """    <FreeRide Duration="60"/>
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
        "autoregulation": {
            "enabled": True,
            "description": "HRV-based autoregulation (green/yellow/red system) or perceived recovery (good sleep + fresh legs = go, poor sleep + heavy legs = back off)",
            "hrv_system": {
                "green": "Full workout",
                "yellow": "Modified workout (reduced volume/intensity)",
                "red": "Easy ride or rest"
            }
        },
        "polarized_philosophy": {
            "enabled": True,
            "description": "80% easy (Z1-Z2), 20% hard (Z4-Z5+), almost nothing in the middle"
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
            "description": "Alternating patterns: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 3-8, continuous"
        },
        "loaded_intervals": {
            "enabled": True,
            "weeks": [7, 10],
            "description": "1 min Z5/Z6 (high cadence, seated) → settle into 11-19 min Z3 (self-selected cadence). Simulates race starts and surges."
        },
        "strength_training": {
            "enabled": False,
            "phases": {
                "base": "Max strength (4x6-8 heavy @ 85-88% 1RM, rest 3-4 min)",
                "explosive": "Explosive power (3x6-8, light loads, maximum velocity)",
                "stability": "Stability/injury prevention (3x12-15)",
                "durability": "Muscular endurance (3x15-20, higher reps, lower weight)",
                "maintenance": "Light maintenance (2x8-10)"
            },
            "note": "Athlete performs own strength program. Phases adapt to training block focus. NON-NEGOTIABLE for 50+ athletes."
        },
        "monday_week_preview": {
            "enabled": True,
            "description": "Monday rest days include week preview with key workouts, HRV monitoring reminders, and Masters-specific guidance"
        },
        "rest_day_tss_limit": 30,
        "rest_day_duration_limit_hours": 1,
        "masters_specific": {
            "ftp_multiplier": 0.93,
            "recovery_principle": "Recovery IS training at 50+",
            "strength_priority": "NON-NEGOTIABLE for 50+ athletes—prevents sarcopenia, maintains bone density"
        }
    }
}

# Save complete template
output_path = "/Users/mattirowe/Documents/Gravel Landing Page Project/current/plans/8. Finisher Masters (12 weeks)/template.json"
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
print(f"   ✅ Autoregulation + Polarized philosophy applied")
print(f"   ✅ Changing Pace philosophy integrated (cadence work, rhythm/loaded intervals)")
print(f"   ✅ Masters-specific considerations included")

