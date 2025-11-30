#!/usr/bin/env python3
"""
Build complete JSON template for FINISHER BEGINNER (12 weeks)
All 84 workouts (12 weeks × 7 workouts)
"""
import json
import re

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
    "name": "FINISHER BEGINNER",
    "duration_weeks": 12,
    "philosophy": "Traditional Pyramidal",
    "target_hours": "8-10",
    "target_athlete": "First big gravel race, building systematic base for first time, has done some recreational riding",
    "goal": "Finish confidently, learn proper training, build durable aerobic base"
}

weeks = []

# WEEK 1
weeks.append({
    "week_number": 1,
    "focus": "Foundation & Assessment",
    "volume_percent": 70,
    "volume_hours": "5.5-7",
    "workouts": [
        create_workout("W01 Mon - Rest", """• Welcome to your first week. This week is about establishing your baseline fitness and learning the rhythm of structured training. Don't skip the FTP test on Tuesday—everything in this plan is built around that number. Keep all other rides conversational easy. Your body needs to learn consistency before we add intensity. You're building an aerobic engine first, then we'll sharpen it later.

• WEEK PREVIEW: This week focuses on establishing your baseline. Tuesday's FTP test sets your training zones for the entire plan. Thursday introduces your first G-Spot intervals—uncomfortably sustainable. Saturday is your first long ride (2.5-3 hours)—practice fueling here. Sunday includes strength work—don't skip it, it prevents injuries.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W01 Tue - FTP Test + Easy Spin", """• STRUCTURE:
15 min warmup → 5 min all-out → 10 min recovery → 20 min max effort → 15 min cooldown

• This sets your training zones for the entire plan. Go hard but not stupid—you need to sustain 20 minutes, not win it in the first 5. Write down your average power for the 20 minutes, multiply by 0.95. That's your FTP.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <SteadyState Duration="300" Power="1.20"/>
    <SteadyState Duration="600" Power="0.55"/>
    <SteadyState Duration="1200" Power="1.05"/>
    <Cooldown Duration="900" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W01 Wed - Endurance Foundation", """• Conversational pace. If you can't talk in full sentences, slow down. This is active recovery from yesterday's test. Your legs should feel looser by the end, not trashed.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W01 Thu - G-Spot Introduction", """• STRUCTURE:
15 min warmup Z2 → 3x10 min @ 87-90% FTP (5 min easy spin between intervals) → 10 min cooldown

• First taste of sustained discomfort. Should feel "uncomfortably sustainable." Stay seated, control your breathing. If you're gasping, back off 2-3%. This isn't a race.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="3" OnDuration="600" OnPower="0.89" Cadence="88" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W01 Fri - Rest or Active Recovery", """• Optional: 30-45 min Z1 spin (50-60% FTP)

• If you're tired, take the day off completely. If you feel good, easy spin only—no intensity. Walk the dog. Stretch. Foam roll.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W01 Sat - Long Endurance Foundation", """• Your bread and butter. Conversational pace the entire time. Eat 40-60g carbs every hour. Drink 500-750ml per hour. Practice race nutrition here—this is a dress rehearsal for race day fueling.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="9000" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W01 Sun - Easy Endurance + Strength", """• Recovery ride followed by foundational strength work. Strength prevents injuries and makes you more durable on the bike. Don't skip it—30 minutes twice a week is insurance against injury.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Goblet squats, single-leg deadlifts, planks, bird dogs, glute bridges (2x10-12 each). Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 2
weeks.append({
    "week_number": 2,
    "focus": "Volume Progression",
    "volume_percent": 80,
    "volume_hours": "6.5-8",
    "workouts": [
        create_workout("W02 Mon - Rest", """• Week 2 increases volume by 15-20%. Your body is still adapting to the training load, so recovery matters as much as the workouts. You should feel moderately tired by Friday—that's the point. If you're wrecked, you're going too hard on easy days. Most mistakes happen when athletes push Z2 into Z3 because their ego won't let them ride easy.

• WEEK PREVIEW: Volume increases this week. Tuesday introduces tempo intervals (comfortably hard). Thursday progresses G-Spot intervals (longer and slightly harder). Saturday is a progressive long ride with intensity in the final hour—simulates pushing on tired legs.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W02 Tue - Tempo Intervals", """• STRUCTURE:
15 min warmup → 3x12 min @ 80-85% FTP (4 min easy spin between) → 10 min cooldown

• Tempo is "comfortably hard"—harder than endurance, easier than threshold. You should be able to hold a conversation but prefer not to. This builds your ceiling for sustained efforts. Stay relaxed in your upper body.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="3" OnDuration="720" OnPower="0.82" Cadence="88" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W02 Wed - Endurance", """• Recovery ride. Keep it genuinely easy. Resist the urge to push. Today's job is moving blood through your legs to clear fatigue, not adding more fatigue.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4200" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W02 Thu - G-Spot Progression", """• STRUCTURE:
15 min warmup → 3x12 min @ 87-92% FTP (4 min easy between) → 10 min cooldown

• Slightly longer and slightly harder than last week. That's intentional progression. Control the start of each interval—don't spike power. Settle in at the right intensity and hold it steady.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="3" OnDuration="720" OnPower="0.90" Cadence="88" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W02 Fri - Rest", """• If you need this day, take it. Don't be a hero. Training is about absorbing the work, not just doing the work.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W02 Sat - Long Endurance Build", """• STRUCTURE:
Z2 first 2 hours, then 3x8 min @ 75-80% FTP in final hour (3 min easy between)

• Simulates what happens when you need to push on tired legs. Start easy, finish with some gas left in the tank. Eat 50-60g carbs per hour. Practice drinking on the bike without looking down.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="6600" Power="0.68" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="480" OnPower="0.78" Cadence="88" OffDuration="180" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W02 Sun - Easy Endurance + Strength", """• Another recovery ride. Do your strength work even if tired—it's only 30 minutes and prevents injuries. Progress your weights slightly from last week if movements felt easy.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Bulgarian split squats, Romanian deadlifts, side planks, dead bugs, single-leg glute bridges (2x10-12 each). Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4500" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 3
weeks.append({
    "week_number": 3,
    "focus": "Building the Base",
    "volume_percent": 90,
    "volume_hours": "7-9",
    "workouts": [
        create_workout("W03 Mon - Rest", """• This is your biggest week so far. By Saturday you should feel accumulated fatigue—that's normal and expected. Week 4 is a recovery week, so push through knowing rest is coming. Every workout counts this week. Sleep 8+ hours. Eat enough. Hydrate.

• WEEK PREVIEW: Biggest week yet. Tuesday introduces threshold intervals (hard but sustainable). Thursday is your first VO2max work (this will hurt—embrace it). Saturday is your longest ride with mixed intensity—simulates race-day efforts when tired.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W03 Tue - Threshold Development", """• STRUCTURE:
20 min warmup → 2x15 min @ 95-100% FTP (8 min easy between) → 10 min cooldown

• Classic threshold intervals. This is hard but not max effort. You should finish thinking "I could maybe do one more." Breathe rhythmically, stay smooth. This is where you build your sustainable race pace.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="900" OnPower="0.98" Cadence="90" OffDuration="480" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W03 Wed - Easy Endurance", """• Truly easy today. Resist all temptation to push. This is active recovery between hard sessions. Spin easy, clear your legs, save energy for tomorrow.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3000" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W03 Thu - VO2max Introduction", """• STRUCTURE:
20 min warmup with 3x30sec openers → 5x3 min @ 110-115% FTP (3 min easy between) → 10 min cooldown

• This will hurt. VO2max intervals are supposed to—you're training maximal oxygen processing. By the end of each interval your lungs should burn. Full recovery between intervals is NOT optional. If you blow up early, you started too hard.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <SteadyState Duration="30" Power="1.10"/>
    <SteadyState Duration="30" Power="0.55"/>
    <SteadyState Duration="30" Power="1.10"/>
    <SteadyState Duration="30" Power="0.55"/>
    <SteadyState Duration="30" Power="1.10"/>
    <SteadyState Duration="30" Power="0.55"/>
    <IntervalsT Repeat="5" OnDuration="180" OnPower="1.12" OffDuration="180" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W03 Fri - Rest", """• Take it. You've earned it. Two hard days back-to-back means you need real rest today.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W03 Sat - Longest Ride of Block", """• STRUCTURE:
First 90 min Z2, then 4x10 min @ 85-90% FTP (5 min easy between) in middle 90 min, final hour Z2

• This simulates race-day efforts when you're already tired. Eat 60-80g carbs per hour. Practice your fueling strategy—this matters more than you think. Try different foods. Figure out what works before race day.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4800" Power="0.68" Cadence="85"/>
    <IntervalsT Repeat="4" OnDuration="600" OnPower="0.88" Cadence="88" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="3600" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W03 Sun - Easy Endurance + Strength", """• You should feel tired today. That's fine. Keep the ride easy. Do the strength work anyway—build the habit. You're accumulating fatigue this week on purpose.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Front squats, step-ups, Copenhagen planks, pallof press, hip thrusts (3x8-10 each). Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4800" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 4
weeks.append({
    "week_number": 4,
    "focus": "Recovery & Adaptation",
    "volume_percent": 60,
    "volume_hours": "5-6",
    "workouts": [
        create_workout("W04 Mon - Rest", """• Recovery week. This is when your body actually gets stronger—adaptation happens during rest, not during work. You should feel fresh by the end of this week. If you don't, you're not recovering properly (check sleep, nutrition, life stress). Enjoy the lighter load.

• WEEK PREVIEW: Recovery week—lighter volume, easier intensity. Tuesday has light G-Spot work (just maintaining fitness). Rest of week is easy endurance. This is when your body adapts and gets stronger.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W04 Tue - Light G-Spot", """• STRUCTURE:
10 min warmup → 2x15 min @ 85-88% FTP (5 min easy between) → 10 min cooldown

• Easier than recent weeks. Keep power controlled, no heroics. This maintains fitness without adding fatigue. Think of it as "reminding" your body what hard feels like without crushing it.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="2" OnDuration="900" OnPower="0.86" Cadence="88" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W04 Wed - Easy Endurance", """• Truly easy. Spin the legs out. Think of this as moving meditation. Enjoy being on the bike without suffering.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2400" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W04 Thu - Rest or Easy Spin", """• Optional: 30-45 min Z1

• If you feel good, spin easy. If you're still tired, take the day completely off. Listen to your body.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W04 Fri - Easy Endurance", """• Yes, another easy day. Trust the process. Recovery weeks work by giving your body time to adapt.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3000" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W04 Sat - Moderate Endurance", """• No intensity today. Just time in the saddle at comfortable pace. Practice race nutrition even though effort is low. Work on bike handling—corners, descents, riding no-hands for 5 seconds to stretch.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="7200" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W04 Sun - Optional Easy Spin + Light Strength", """• If you're still tired, skip the ride completely. Do a lighter strength routine focusing on movement quality and mobility.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Bodyweight squats, lunges, planks, bird dogs—just movement quality, no heavy loads. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3000" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 5
weeks.append({
    "week_number": 5,
    "focus": "Build Phase Begins",
    "volume_percent": 85,
    "volume_hours": "7-8.5",
    "workouts": [
        create_workout("W05 Mon - Rest", """• Welcome to the Build phase. Weeks 5-8 progressively increase both volume and intensity. You should be feeling fresh after last week's recovery. Now we sharpen the base you've built. Threshold work increases—this is where you build your race pace.

• WEEK PREVIEW: Build phase begins. Tuesday has classic 2x20 threshold intervals (race pace training). Thursday increases G-Spot volume (4x12 min). Saturday combines long ride with G-Spot blocks—building ability to hit intensity when tired.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W05 Tue - Threshold Intervals", """• STRUCTURE:
20 min warmup → 2x20 min @ 95-100% FTP (10 min easy between) → 10 min cooldown

• Classic 2x20 threshold. This is hard but controlled. You should finish thinking "I could maybe squeeze out one more." Breathe rhythmically, stay smooth, keep pedal stroke circular. This builds your sustainable power.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="1200" OnPower="0.98" Cadence="90" OffDuration="600" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W05 Wed - Endurance", """• Keep it easy. Your job today is recovery, not fitness. Active recovery helps clear fatigue better than sitting on the couch.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4500" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W05 Thu - G-Spot Intervals", """• STRUCTURE:
15 min warmup → 4x12 min @ 87-92% FTP (4 min easy between) → 10 min cooldown

• More total time at G-Spot than previous weeks. Stay controlled—don't spike watts at the start. Settle into each interval and hold steady power.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="4" OnDuration="720" OnPower="0.90" Cadence="88" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W05 Fri - Rest or Recovery Ride", """• Optional: 45 min Z1 spin

• Day off if needed. Light spin if you feel good. No intensity.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W05 Sat - Long Endurance with Intensity", """• STRUCTURE:
First 90 min Z2 → 3x15 min @ 87-92% FTP (5 min easy between) → Final 60 min Z2

• Building your ability to hit intensity when already tired. This is race simulation. Fuel properly: 60-80g carbs/hour. Try race-day nutrition products today.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4800" Power="0.68" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="900" OnPower="0.90" Cadence="88" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="3600" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W05 Sun - Easy Endurance + Strength", """• Easy ride, solid strength work. You should be feeling accumulated fatigue by Sunday—that means the training is working.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Back to progressive loading—goblet squats, single-leg RDLs, planks with leg lifts, anti-rotation work (3x8-10). Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4500" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 6
weeks.append({
    "week_number": 6,
    "focus": "Intensity Progression",
    "volume_percent": 95,
    "volume_hours": "7.5-9.5",
    "workouts": [
        create_workout("W06 Mon - Rest", """• Volume and intensity both increase this week. You're building fitness through progressive overload. By Saturday you should feel tired but not destroyed. If you're consistently exhausted, back off 5-10% on power targets—better to finish workouts slightly easier than to blow up halfway through.

• WEEK PREVIEW: Intensity progression week. Tuesday increases VO2max volume (6x4 min). Thursday combines threshold + G-Spot (hard when tired). Saturday is a long mixed-terrain simulation—varied intensity like gravel racing.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W06 Tue - VO2max Intervals", """• STRUCTURE:
20 min warmup with openers → 6x4 min @ 110-115% FTP (4 min easy between) → 10 min cooldown

• Six intervals is a step up from last block. These hurt. Embrace the suck. Your breathing should be labored but controlled. If you can't complete an interval, stop and take extra rest. Quality > quantity.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <SteadyState Duration="30" Power="1.10"/>
    <SteadyState Duration="30" Power="0.55"/>
    <SteadyState Duration="30" Power="1.10"/>
    <SteadyState Duration="30" Power="0.55"/>
    <SteadyState Duration="30" Power="1.10"/>
    <SteadyState Duration="30" Power="0.55"/>
    <IntervalsT Repeat="6" OnDuration="240" OnPower="1.12" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W06 Wed - Endurance", """• Recovery day between hard sessions. Keep it conversational. Your ego will want to push—don't. Easy days make hard days possible.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4800" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W06 Thu - Threshold + G-Spot", """• STRUCTURE:
15 min warmup → 2x12 min @ 95-100% FTP + 2x10 min @ 87-92% FTP (5 min easy between all intervals) → 10 min cooldown

• Combined stimulus—threshold first while fresh, then G-Spot when fatigued. This teaches your body to sustain power when tired. Stay mentally engaged through all intervals.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="720" OnPower="0.98" Cadence="90" OffDuration="300" OffPower="0.55"/>
    <IntervalsT Repeat="2" OnDuration="600" OnPower="0.90" Cadence="88" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W06 Fri - Rest", """• You've earned it. Two hard days back-to-back. Rest today.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W06 Sat - Long Mixed Terrain Simulation", """• STRUCTURE:
First hour Z2 → 6x5 min @ 85-95% FTP (varied, 3 min easy between) scattered through hours 2-3 → Final hour Z2

• Simulates gravel race variability. Some efforts at tempo, some at threshold. Mimics surges on climbs or into wind. Fuel aggressively: 70-80g carbs/hour. Test race-day gear today.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3000" Power="0.68" Cadence="85"/>
    <IntervalsT Repeat="6" OnDuration="300" OnPower="0.90" Cadence="88" OffDuration="180" OffPower="0.55"/>
    <SteadyState Duration="3600" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W06 Sun - Easy Endurance + Strength", """• Long easy ride to build endurance without intensity. Strength work focuses on single-leg stability—this prevents compensation patterns that cause injury.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Bulgarian splits, single-leg deadlifts, side planks with rotation, dead bugs, hip thrusts (3x8-10). Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4800" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 7
weeks.append({
    "week_number": 7,
    "focus": "Peak Build Volume",
    "volume_percent": 100,
    "volume_hours": "8-10",
    "workouts": [
        create_workout("W07 Mon - Rest", """• This is your biggest week of the plan. By Saturday you should feel significant accumulated fatigue—that's intentional. Week 8 is recovery, so push through knowing rest is coming. Every workout this week counts. Prioritize sleep. Eat enough protein. Hydrate constantly.

• WEEK PREVIEW: Peak build week—biggest volume and intensity. Tuesday has 3x15 threshold (hardest threshold session). Thursday combines VO2max + G-Spot (big workout). Saturday is your longest ride with race simulation—this is your "A" workout.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W07 Tue - Threshold Progression", """• STRUCTURE:
20 min warmup → 3x15 min @ 95-100% FTP (7 min easy between) → 10 min cooldown

• Three threshold blocks. Hardest threshold session yet. Pace yourself—if you blow up on interval 1, you won't finish the workout. Controlled start, hold steady, finish strong. This is race pace training.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="900" OnPower="0.98" Cadence="90" OffDuration="420" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W07 Wed - Easy Endurance", """• Truly easy. Your legs need this. Don't push. Active recovery accelerates adaptation.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3600" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W07 Thu - VO2max + G-Spot", """• STRUCTURE:
20 min warmup → 5x4 min @ 110-115% FTP + 2x12 min @ 87-92% FTP (4-5 min easy between) → 10 min cooldown

• Big workout. VO2max first while fresh, then G-Spot when tired. This is hard but hugely effective. Break it into chunks mentally—5 VO2 efforts, then 2 G-Spot blocks. One at a time.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="5" OnDuration="240" OnPower="1.12" OffDuration="240" OffPower="0.55"/>
    <IntervalsT Repeat="2" OnDuration="720" OnPower="0.90" Cadence="88" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W07 Fri - Rest", """• Mandatory rest. Two massive days. You need this off day.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W07 Sat - Longest Ride of Plan", """• STRUCTURE:
First 90 min Z2 → 4x15 min @ 87-95% FTP (5 min easy between) in hours 2-3 → Final 90 min Z2

• This is your "A" workout of the week. Simulates race day: long duration + intensity when tired. Fuel like race day: 70-90g carbs/hour. Practice everything—bottle hand-ups, eating while riding hard, pacing. Mental toughness matters here.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4800" Power="0.68" Cadence="85"/>
    <IntervalsT Repeat="4" OnDuration="900" OnPower="0.91" Cadence="88" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="4800" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W07 Sun - Easy Endurance + Strength", """• Long easy ride. You should feel very tired today. That's good—it means you've done the work. Do strength anyway. Active recovery helps more than couch sitting.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Front squats, step-ups, Copenhagen planks, pallof press, single-leg hip thrusts (3x8-10). Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 8
weeks.append({
    "week_number": 8,
    "focus": "Recovery & Absorption",
    "volume_percent": 60,
    "volume_hours": "5-6",
    "workouts": [
        create_workout("W08 Mon - Rest", """• Recovery week after your biggest training block. You should feel tired at the start of this week and fresh by the end. This is when your body actually adapts and gets stronger. If you don't recover this week, you won't be able to hit the final peak phase properly.

• WEEK PREVIEW: Recovery week—lighter volume, easier intensity. Tuesday has light tempo (just maintaining fitness). Rest of week is easy endurance. This is when adaptation happens.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W08 Tue - Light Tempo", """• STRUCTURE:
10 min warmup → 2x12 min @ 80-85% FTP (5 min easy between) → 10 min cooldown

• Easier than recent weeks. Just maintaining fitness stimulus without adding fatigue. Should feel controlled and comfortable.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="2" OnDuration="720" OnPower="0.82" Cadence="88" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W08 Wed - Easy Endurance", """• Truly easy. Enjoy the ride. No power goals. Just move your legs.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2400" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W08 Thu - Rest or Easy Spin", """• Optional: 30-45 min Z1

• If tired, take it off. If fresh, spin easy. Listen to your body.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W08 Fri - Easy Endurance", """• Another easy day. Your body is adapting and getting stronger while you rest.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3000" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W08 Sat - Moderate Endurance", """• No intensity. Just aerobic time. Practice skills—cornering, descending, standing to stretch. Dial in bike fit. Check all equipment.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="9000" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W08 Sun - Optional Spin + Light Strength", """• Skip ride if still tired. Light strength focuses on movement quality and injury prevention.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Bodyweight movements, mobility work, core stability (light loads). Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3000" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 9
weeks.append({
    "week_number": 9,
    "focus": "Peak Phase - Specificity",
    "volume_percent": 90,
    "volume_hours": "7-9",
    "workouts": [
        create_workout("W09 Mon - Rest", """• Welcome to the Peak phase. Final four weeks before race day. Training becomes more race-specific now—longer sustained efforts, bigger gear work, gravel simulation. You've built the engine. Now we tune it for race day.

• WEEK PREVIEW: Peak phase begins. Tuesday has race-pace threshold (2x20 min). Thursday has long G-Spot intervals (3x20 min). Saturday is a big race simulation ride—long sustained efforts like gravel racing.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W09 Tue - Race-Pace Threshold", """• STRUCTURE:
20 min warmup → 2x20 min @ 95-100% FTP (8 min easy between) → 10 min cooldown

• Classic 2x20 at threshold. This is your race pace. You should be able to hold this power for extended periods on race day. Practice staying relaxed in your upper body even as legs burn.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="1200" OnPower="0.98" Cadence="90" OffDuration="480" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W09 Wed - Endurance", """• Recovery day. Keep it easy. Save energy for tomorrow's workout.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4500" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W09 Thu - G-Spot Progression", """• STRUCTURE:
20 min warmup → 3x20 min @ 87-92% FTP (5 min easy between) → 10 min cooldown

• Long G-Spot intervals. This is just below threshold—sustainable discomfort. Builds your ability to hold strong power for extended periods. Perfect for long gravel race efforts.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="3" OnDuration="1200" OnPower="0.90" Cadence="88" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W09 Fri - Rest or Easy Spin", """• Optional: 30-45 min Z1

• Day off if needed. Light spin if feeling good.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W09 Sat - Race Simulation Ride", """• STRUCTURE:
First hour Z2 → 3x30 min @ 85-92% FTP (10 min easy between) in hours 2-4 → Final 30 min Z2

• BIG workout. Simulates race-day pacing—long sustained efforts with short recoveries. This is exactly what gravel racing feels like. Fuel like race day: 70-80g carbs/hour. Test all race-day gear and nutrition.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3000" Power="0.68" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="1800" OnPower="0.88" Cadence="88" OffDuration="600" OffPower="0.55"/>
    <SteadyState Duration="1500" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W09 Sun - Easy Endurance + Strength", """• Easy ride. Strength work shifts to maintenance mode—keep the adaptations, don't add new stress.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Maintenance loading—goblet squats, RDLs, planks, anti-rotation (2x10). Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4800" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 10
weeks.append({
    "week_number": 10,
    "focus": "Final Build",
    "volume_percent": 95,
    "volume_hours": "7.5-9.5",
    "workouts": [
        create_workout("W10 Mon - Rest", """• Second-to-last hard week. You should be feeling fit and strong now. Two more weeks of quality work, then we taper. Focus on execution, recovery, and dialing in race-day logistics. Check your bike. Order any last nutrition products. Book travel.

• WEEK PREVIEW: Final build week. Tuesday combines threshold + VO2max (race pace + top-end). Thursday has long G-Spot (2x25 min). Saturday is your last big training day—race-like intensity with long sustained blocks.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W10 Tue - Threshold + VO2max", """• STRUCTURE:
20 min warmup → 2x15 min @ 95-100% FTP + 4x3 min @ 110% FTP (5-7 min easy between) → 10 min cooldown

• Combined stimulus. Threshold work builds race pace, VO2max keeps your top-end sharp. Quality execution on both. Don't blow up early.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="900" OnPower="0.98" Cadence="90" OffDuration="300" OffPower="0.55"/>
    <IntervalsT Repeat="4" OnDuration="180" OnPower="1.10" OffDuration="180" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W10 Wed - Endurance", """• Recovery between hard days. Keep it conversational. Your fitness is built—now you're maintaining and sharpening.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="4500" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W10 Thu - Long G-Spot", """• STRUCTURE:
20 min warmup → 2x25 min @ 87-92% FTP (7 min easy between) → 10 min cooldown

• Long sustained efforts just below threshold. This is bread-and-butter gravel racing power. Hold it steady, stay relaxed, control your breathing. You should feel strong here.""", """    <Warmup Duration="1200" PowerLow="0.50" PowerHigh="0.65"/>
    <IntervalsT Repeat="2" OnDuration="1500" OnPower="0.90" Cadence="88" OffDuration="420" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W10 Fri - Rest", """• Two hard days done. Rest today. You're close to peak fitness now.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W10 Sat - Long Race-Intensity Ride", """• STRUCTURE:
First hour Z2 → 2x45 min @ 85-90% FTP (15 min easy between) in hours 2-3 → Final hour Z2 with 4x5 min @ 90-95% FTP (3 min easy between)

• Last big training day before taper. Race-like intensity. Long sustained blocks early, then surges when tired late. THIS is gravel racing. Eat 70-90g carbs/hour. Test EVERYTHING—clothes, shoes, nutrition, hydration system.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3000" Power="0.68" Cadence="85"/>
    <IntervalsT Repeat="2" OnDuration="2700" OnPower="0.88" Cadence="88" OffDuration="900" OffPower="0.55"/>
    <SteadyState Duration="3000" Power="0.68" Cadence="85"/>
    <IntervalsT Repeat="4" OnDuration="300" OnPower="0.93" Cadence="88" OffDuration="180" OffPower="0.55"/>
    <SteadyState Duration="300" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W10 Sun - Easy Endurance + Light Strength", """• Long easy ride to build final endurance adaptations without fatigue. Light strength keeps you healthy going into taper.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Light maintenance—bodyweight movements, mobility, core (2x8-10). Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="5400" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 11
weeks.append({
    "week_number": 11,
    "focus": "Taper Begins",
    "volume_percent": 70,
    "volume_hours": "5.5-7",
    "workouts": [
        create_workout("W11 Mon - Rest", """• Taper week 1 of 2. Volume drops 30% but intensity stays high. This keeps you sharp while allowing freshness to return. You should start feeling "race ready" by the end of this week. Legs feel snappy, power comes easy. That's fitness + freshness.

• WEEK PREVIEW: Taper begins. Tuesday has race-pace openers (shorter threshold intervals). Thursday combines G-Spot + openers (maintained intensity, reduced volume). Saturday is a moderate endurance ride with race efforts—final reminder workout.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W11 Tue - Race-Pace Openers", """• STRUCTURE:
15 min warmup → 3x10 min @ 95-100% FTP (5 min easy between) → 10 min cooldown

• Shorter threshold intervals. Keep intensity high, reduce volume. Power should feel easy. If it doesn't, you need more rest—back off slightly.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="3" OnDuration="600" OnPower="0.98" Cadence="90" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W11 Wed - Easy Endurance", """• Easy day. Your body is absorbing the training and gaining freshness. Let it happen.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3000" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W11 Thu - Short G-Spot + Openers", """• STRUCTURE:
15 min warmup → 2x15 min @ 87-92% FTP + 3x1 min @ 105% FTP (5 min easy between all) → 10 min cooldown

• Reduced volume, maintained intensity. The 1-min openers keep your top-end sharp. Should feel snappy and strong.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="2" OnDuration="900" OnPower="0.90" Cadence="88" OffDuration="300" OffPower="0.55"/>
    <IntervalsT Repeat="3" OnDuration="60" OnPower="1.05" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W11 Fri - Rest", """• Rest day. You're tapering now. Less is more.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W11 Sat - Moderate Endurance with Race Efforts", """• STRUCTURE:
First hour Z2 → 3x10 min @ 88-95% FTP (5 min easy between) in hour 2 → Final 30-60 min Z2

• Shorter than recent weeks but still race-intensity efforts. You should feel strong. This is your final "reminder" workout before race week. Dial in final nutrition and equipment choices.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3000" Power="0.68" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="600" OnPower="0.91" Cadence="88" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="2400" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W11 Sun - Easy Spin + Optional Light Strength", """• Easy recovery spin. Skip strength if tired. You're one week out from race week now.

• STRENGTH TRAINING NOTE: Perform your own strength training program. Suggested focus: Light core/mobility only if feeling good. Strength work is best done on days with lighter training load.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="3000" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
""")
    ]
})

# WEEK 12
weeks.append({
    "week_number": 12,
    "focus": "Race Week",
    "volume_percent": 40,
    "volume_hours": "3-5",
    "workouts": [
        create_workout("W12 Mon - Rest", """• Race week. Volume drops dramatically. Intensity stays sharp but brief. You should feel increasingly fresh each day. Nervous energy is normal—channel it into final prep. Check your bike. Pack your bags. Review race plan. Trust your training.

• WEEK PREVIEW: Race week! Tuesday has race openers (final intensity check). Wednesday is easy spin. Thursday rest or shake-out. Friday pre-race shake-out. Saturday/Sunday: RACE DAY!

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W12 Tue - Race Openers", """• STRUCTURE:
15 min easy warmup → 3x3 min @ 90-100% FTP (3 min easy between) → 3x30 sec @ 110% FTP (2 min easy between) → 5 min cooldown

• Final intensity before race. Should feel powerful and snappy. If legs feel dead, add another day of rest before race. This is your "sharpness check." """, """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="3" OnDuration="180" OnPower="0.95" Cadence="90" OffDuration="180" OffPower="0.55"/>
    <IntervalsT Repeat="3" OnDuration="30" OnPower="1.10" OffDuration="120" OffPower="0.55"/>
    <Cooldown Duration="300" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W12 Wed - Easy Spin", """• Just moving legs. No intensity whatsoever. Spin out any lingering fatigue.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1800" Power="0.60" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.60" PowerHigh="0.55"/>
"""),
        create_workout("W12 Thu - Rest or 20-min Shake-Out", """• Optional: 20-30 min Z1 with 3x30 sec @ race pace

• If race is Sunday, consider total rest today. If race is Saturday, do a short shake-out ride. Listen to your body.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W12 Fri - Pre-Race Shake-Out", """• STRUCTURE:
15 min easy → 3x1 min @ race pace (2 min easy between) → 10 min easy

• Final ride before race. Legs should feel fresh and powerful. Check bike one last time. Test race-day tire pressure. Visualize race execution.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.70"/>
    <IntervalsT Repeat="3" OnDuration="60" OnPower="0.98" Cadence="90" OffDuration="120" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W12 Sat - Race Day or Rest", """• If racing Saturday: EXECUTE YOUR PLAN

• If racing Sunday: Complete rest or 20-min easy spin with 3x30sec openers

• Notes: If racing today—trust your training, pace yourself early, fuel aggressively, stay mentally engaged. You've done the work. Now execute.""", """    <FreeRide Duration="60"/>
"""),
        create_workout("W12 Sun - Race Day or Recovery", """• If racing Sunday: EXECUTE YOUR PLAN

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
        "cadence_work": {
            "enabled": True,
            "description": "High (100+ rpm) and low (40-60 rpm) cadence variations on all intervals",
            "base_period": "Alternate high and low cadence",
            "build_period": "Rhythm intervals use self-selected for Z3, high cadence for Z4"
        },
        "rhythm_intervals": {
            "enabled": True,
            "weeks": [5, 6, 7, 8, 9, 10],
            "description": "Alternating 2 min Z3 + 1 min Z4 patterns"
        },
        "loaded_intervals": {
            "enabled": True,
            "weeks": [5, 6, 7, 8, 9, 10],
            "description": "1 min Z5/Z6 surge then settle into 14 min Z3"
        },
        "gspot_terminology": {
            "enabled": True,
            "replaces": "Sweet Spot",
            "range": "87-92% FTP"
        },
        "strength_training": {
            "enabled": False,
            "note": "Athlete performs own strength program. Suggested on lighter training days."
        }
    }
}

# Save complete template
output_path = "/Users/mattirowe/Documents/Gravel Landing Page Project/current/plans/5. Finisher Beginner (12 weeks)/template.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(template, f, indent=2, ensure_ascii=False)

print(f"✅ Complete template created: {output_path}")
print(f"   Plan: {plan_metadata['name']}")
print(f"   Duration: {plan_metadata['duration_weeks']} weeks")
print(f"   Total weeks: {len(weeks)}")
total_workouts = sum(len(w['workouts']) for w in weeks)
print(f"   Total workouts: {total_workouts}")
print(f"   ✅ All 12 weeks complete!")

