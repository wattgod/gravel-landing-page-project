#!/usr/bin/env python3
"""
Build complete JSON template for AYAHUASCA SAVE MY RACE (6 weeks)
Emergency plan for minimal time (3-5 hours/week)
All 6 weeks with 42 workouts total
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
    "name": "AYAHUASCA SAVE MY RACE",
    "duration_weeks": 6,
    "philosophy": "G-Spot/Threshold (Emergency Sharpening)",
    "target_hours": "3-5",
    "target_athlete": "Emergency situation, minimal time (3-5 hrs/week), needs to finish in 6 weeks",
    "goal": "Get race-ready FAST with time-efficient training, accept compromises"
}

weeks = []

# WEEK 1: Rapid Assessment & Foundation
weeks.append({
    "week_number": 1,
    "focus": "Rapid Assessment & Foundation",
    "volume_percent": 70,
    "volume_hours": "2-3.5",
    "workouts": [
        create_workout("W01 Mon - Rest", """• Welcome to emergency mode. You have 6 weeks to get ready for a gravel race with only 3-5 hours per week. This isn't ideal—but it's reality. We're using G-Spot and Threshold work because they give maximum bang-for-buck in minimal time. Accept this: you won't have perfect endurance. You won't have elite power. But you WILL be able to finish if you execute this plan and pace the race conservatively. Let's be honest about what we're working with.

• WEEK PREVIEW: Rapid assessment week. Tuesday has quick FTP test (20 min sustained effort). Thursday introduces G-Spot intervals (3x10 min). Saturday is longest ride of week (75-90 min with G-Spot blocks). This week establishes your baseline and introduces time-efficient intensity.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W01 Tue - Quick FTP Test", """• STRUCTURE:
15 min warmup → 20 min sustained effort (hard but not all-out) → 10 min cooldown

• No time for fancy testing. 20-minute sustained effort at "this really hurts but I can hold it." Average power × 0.95 = FTP. This is your training anchor. Write it down. If you can't complete 20 minutes, go as long as possible and use that. We work with what we have.

• CADENCE: Self-selected for test effort.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <SteadyState Duration="1200" Power="1.05"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W01 Wed - Rest", """• Full rest day. With only 3-5 hours weekly, every session must count. Recovery matters.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W01 Thu - G-Spot Introduction", """• STRUCTURE:
15 min warmup → 3x10 min @ 87-92% FTP (4 min easy between) → 10 min cooldown

• G-Spot is "uncomfortably sustainable." This is your bread and butter for the next 6 weeks. Builds threshold power without destroying you. Stay seated, control breathing. If you blow up, back off 3-5%.

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="600" OnPower="0.895" Cadence="100" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W01 Fri - Rest", """• Rest day. Don't be a hero. You have minimal volume—make it count.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W01 Sat - Longer Endurance + Intensity", """• STRUCTURE:
20 min easy → 3x12 min @ 85-90% FTP (5 min easy between) → 15 min easy

• Longest ride of the week. G-Spot blocks build both power and endurance in one session—time-efficient. Eat 40-50g carbs during ride. Practice fueling—you'll need it on race day.

• CADENCE WORK: Mix cadences—intervals 1, 3 at high cadence (100+ rpm), interval 2 at low cadence (40-60 rpm).""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1200" Power="0.68" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="720" OnPower="0.875" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="900" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W01 Sun - Rest or Optional Easy Spin", """• Optional: 30 min Z1 spin

• Default is rest. Only spin if you feel great AND energetic. Emergency plans require discipline on rest days.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS.""")
    ]
})

# WEEK 2: Building G-Spot Foundation
weeks.append({
    "week_number": 2,
    "focus": "Building G-Spot Foundation",
    "volume_percent": 85,
    "volume_hours": "2.5-4.25",
    "workouts": [
        create_workout("W02 Mon - Rest", """• Week 2 increases intensity duration slightly. You're building as much threshold power as possible with the time you have. G-Spot is king in emergency mode—87-92% FTP builds power without excessive fatigue. Every minute on the bike needs to count. No junk miles.

• WEEK PREVIEW: Building G-Spot foundation. Tuesday has extended G-Spot intervals (3x12 min). Thursday introduces threshold work (2x10 min). Saturday is biggest session of week (90-105 min with mixed intensity). This week builds threshold power efficiently.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W02 Tue - G-Spot Progression", """• STRUCTURE:
15 min warmup → 3x12 min @ 87-92% FTP (4 min easy between) → 10 min cooldown

• Longer intervals than Week 1. This should feel hard but sustainable. You're building the engine. Control your breathing, stay smooth. If form breaks, end the interval early—quality over quantity.

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm), interval 3 self-selected.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="720" OnPower="0.895" Cadence="100" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W02 Wed - Rest", """• Rest day. Non-negotiable. Your body needs this to absorb Tuesday's work.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W02 Thu - Threshold Introduction", """• STRUCTURE:
15 min warmup → 2x10 min @ 95-100% FTP (5 min easy between) → 10 min cooldown

• First threshold work. This is HARD—breathing labored but rhythmic. This is race pace intensity. Should finish thinking "maybe one more." If you can't hold power, back off to 90-93%. Better to finish strong than blow up.

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="600" OnPower="0.98" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W02 Fri - Rest", """• Rest day. You need recovery between quality sessions.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W02 Sat - Weekend Key Session", """• STRUCTURE:
20 min easy → 2x15 min @ 87-92% FTP (6 min easy between) → 10 min easy → 2x8 min @ 75-80% FTP (3 min easy between) → 15 min easy

• Biggest session of week. G-Spot first, then tempo when tired. This builds power AND durability in one ride. Eat 40-60g carbs during ride. You're training your body to fuel under stress.

• CADENCE WORK: Mix cadences on G-Spot blocks—one high cadence (100+ rpm), one low cadence (40-60 rpm).""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1200" Power="0.68" Cadence="85"/>
    <IntervalsT Repeat="2" OnDuration="900" OnPower="0.895" Cadence="100" OffDuration="360" OffPower="0.55"/>
    <SteadyState Duration="600" Power="0.68" Cadence="85"/>
    <IntervalsT Repeat="2" OnDuration="480" OnPower="0.78" Cadence="100" OffDuration="180" OffPower="0.55"/>
    <SteadyState Duration="900" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W02 Sun - Rest or Light Spin", """• Optional: 30-40 min Z1

• Default is rest. Light spin only if feeling recovered. Don't dig a hole.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS.""")
    ]
})

# WEEK 3: Peak G-Spot Volume
weeks.append({
    "week_number": 3,
    "focus": "Peak G-Spot Volume",
    "volume_percent": 100,
    "volume_hours": "3-5",
    "workouts": [
        create_workout("W03 Mon - Rest", """• Week 3 is your biggest training week. You'll do as much G-Spot and Threshold as your body can handle in 3-5 hours. By Saturday you should feel accumulated fatigue—that's the point. Week 4 backs off before final sharpening. This is your fitness-building week. Make it count.

• WEEK PREVIEW: Peak G-Spot volume week. Tuesday has maximum G-Spot volume (4x10 min). Thursday has extended threshold (2x12 min). Saturday is biggest session of plan (105-120 min with mixed intensity). This is your "A" week.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W03 Tue - Peak G-Spot", """• STRUCTURE:
15 min warmup → 4x10 min @ 87-92% FTP (4 min easy between) → 10 min cooldown

• Four intervals—most yet. This should be hard but doable. G-Spot builds threshold without crushing you. Stay controlled. If you fade on interval 4, that's fine—you pushed hard enough.

• CADENCE WORK: Mix cadences—intervals 1, 3 at high cadence (100+ rpm), intervals 2, 4 at low cadence (40-60 rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="4" OnDuration="600" OnPower="0.895" Cadence="100" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W03 Wed - Rest", """• Full rest after big session. Your body needs this.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W03 Thu - Threshold Progression", """• STRUCTURE:
15 min warmup → 2x12 min @ 95-100% FTP (6 min easy between) → 10 min cooldown

• Longer threshold blocks. This is race pace. Breathing hard but controlled. This is what gravel racing will feel like. Get comfortable being uncomfortable. If you can't hold full 12 min, do what you can—10 min is better than nothing.

• CADENCE WORK: Mix cadences—interval 1 high cadence (100+ rpm), interval 2 low cadence (40-60 rpm).""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="720" OnPower="0.98" Cadence="100" OffDuration="360" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W03 Fri - Rest", """• Rest day. Two hard days done. You need recovery.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W03 Sat - Biggest Session of Plan", """• STRUCTURE:
20 min easy → 3x15 min @ 87-92% FTP (5 min easy between) → 15 min easy → 3x8 min @ 75-80% FTP (3 min easy between) → 15 min easy

• Longest and hardest ride. Three G-Spot blocks, then three tempo blocks when tired. This is your "A" session—it builds power, endurance, and race simulation all in one. Eat 50-60g carbs during ride. This matters. You're teaching your body to fuel under stress—critical for race day survival.

• CADENCE WORK: Mix cadences on G-Spot blocks—intervals 1, 3 at high cadence (100+ rpm), interval 2 at low cadence (40-60 rpm).""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1200" Power="0.68" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="900" OnPower="0.895" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="900" Power="0.68" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="480" OnPower="0.78" Cadence="100" OffDuration="180" OffPower="0.55"/>
    <SteadyState Duration="900" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W03 Sun - Rest or Easy Spin", """• Optional: 30-45 min Z1

• Default is rest. You should feel tired after this week. That's good—you overloaded the system. Only spin if you feel surprisingly good.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS.""")
    ]
})

# WEEK 4: Recovery & Absorption
weeks.append({
    "week_number": 4,
    "focus": "Recovery & Absorption",
    "volume_percent": 60,
    "volume_hours": "1.75-3",
    "workouts": [
        create_workout("W04 Mon - Rest", """• Recovery week. Your body adapts during rest, not during work. By Friday you should feel fresh. If you're still tired by week's end, you pushed too hard in Week 3 or aren't sleeping enough. Emergency plans need emergency recovery discipline.

• WEEK PREVIEW: Recovery week. Tuesday has light G-Spot (2x10 min, easier). Thursday is easy endurance. Saturday is moderate ride with light tempo touch. This is when adaptation happens.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W04 Tue - Light G-Spot", """• STRUCTURE:
10 min warmup → 2x10 min @ 85-88% FTP (5 min easy between) → 10 min cooldown

• Lighter than Week 3. Maintains fitness without adding fatigue. Should feel controlled and relatively easy.

• CADENCE WORK: Mix cadences—one high cadence (100+ rpm), one low cadence (40-60 rpm).""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="600" OnPower="0.865" Cadence="90" OffDuration="300" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W04 Wed - Rest", """• Full rest day.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W04 Thu - Easy Endurance", """• Duration: 40-50 min

• Zones: Z2 (65-75% FTP)

• Notes: Easy pace. Conversational. Just moving legs. Active recovery helps.

• CADENCE: Self-selected (85-95 rpm).""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="2400" Power="0.70" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.55"/>
"""),
        create_workout("W04 Fri - Rest", """• Rest day. You should start feeling fresh and strong by now.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W04 Sat - Moderate Ride", """• STRUCTURE:
20 min easy → 2x10 min @ 80-85% FTP (5 min easy between) → 15 min easy

• No intensity stress. Light tempo touches maintain stimulus. This should feel comfortable. Check bike. Make sure everything works. Address any fit issues now.

• CADENCE WORK: Mix cadences on tempo blocks.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1200" Power="0.68" Cadence="85"/>
    <IntervalsT Repeat="2" OnDuration="600" OnPower="0.825" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="900" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W04 Sun - Rest", """• Full rest day. Preparing for final two weeks.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS.""")
    ]
})

# WEEK 5: Race Preparation - Specificity
weeks.append({
    "week_number": 5,
    "focus": "Race Preparation - Specificity",
    "volume_percent": 85,
    "volume_hours": "2.5-4.25",
    "workouts": [
        create_workout("W05 Mon - Rest", """• Two weeks to race. Training becomes race-specific now. You're practicing race pace, race duration (as much as possible), race fueling. Accept that your longest training ride is 2 hours but race might be 4-8+ hours. This means pacing and fueling are CRITICAL. You can't train your way out of this gap—you have to race smart.

• WEEK PREVIEW: Race preparation week. Tuesday has race pace intervals (3x10 min @ 90-95% FTP). Thursday has G-Spot + openers (sharpening session). Saturday is final long race prep (105-120 min). This week practices race-specific efforts.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W05 Tue - Race Pace Intervals", """• STRUCTURE:
15 min warmup → 3x10 min @ 90-95% FTP (4 min easy between) → 10 min cooldown

• Race pace intervals. This is what sustained gravel racing feels like. Should be hard but sustainable. Practice drinking while holding power—you'll need this skill on race day. If you can't hold 90-95%, drop to 85-90%. Finishing strong matters more than hitting exact numbers.

• RHYTHM INTERVALS: For one interval, try rhythm pattern: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 3, continuous. This simulates race variability.

• CADENCE WORK: Mix cadences or use rhythm pattern.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="3" OnDuration="600" OnPower="0.93" Cadence="100" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W05 Wed - Rest", """• Rest day after quality session.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W05 Thu - G-Spot + Openers", """• STRUCTURE:
15 min warmup → 2x12 min @ 87-92% FTP (5 min easy between) → 5 min easy → 3x1 min @ 100% FTP (2 min easy between) → 5 min cooldown

• G-Spot maintains power, openers keep legs sharp. The 1-min efforts should feel snappy. This is race preparation—keeping your top-end responsive.

• CADENCE WORK: Mix cadences on G-Spot blocks. High cadence (100+ rpm) on openers.""", """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="2" OnDuration="720" OnPower="0.895" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="300" Power="0.65" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="60" OnPower="1.00" Cadence="100" OffDuration="120" OffPower="0.55"/>
    <Cooldown Duration="300" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W05 Fri - Rest", """• Rest day before weekend key session.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W05 Sat - Final Long Race Prep", """• STRUCTURE:
30 min easy → 3x15 min @ 85-92% FTP (varied effort, 5 min easy between) → Final 30-45 min easy

• Final long ride before taper. Simulating race effort—sustained power when already tired. Eat 50-60g carbs during ride. Test ALL race day nutrition. This is dress rehearsal. Whatever you eat today, you can eat on race day. Test nothing new on race day.

• LOADED INTERVALS: For one interval, try loaded pattern: 1 min Z5/Z6 (high cadence, seated) → settle into 14 min Z3 (self-selected cadence). This simulates race starts.

• CADENCE WORK: Mix cadences or use loaded/rhythm patterns.""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1800" Power="0.68" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="900" OnPower="0.895" Cadence="100" OffDuration="300" OffPower="0.55"/>
    <SteadyState Duration="2400" Power="0.68" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.68" PowerHigh="0.55"/>
"""),
        create_workout("W05 Sun - Rest or Light Spin", """• Optional: 30 min Z1

• Default is rest. Light spin only if feeling good. You're one week from race week.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS.""")
    ]
})

# WEEK 6: Race Week - Final Prep
weeks.append({
    "week_number": 6,
    "focus": "Race Week - Final Prep",
    "volume_percent": 40,
    "volume_hours": "1.25-2.5",
    "workouts": [
        create_workout("W06 Mon - Rest", """• Race week. Volume drops dramatically. You should feel fresh and ready. Nervous energy is normal—you trained for 5 weeks in emergency mode. You did what you could with the time you had. Now execute the race plan: START CONSERVATIVELY. Fuel from mile 1 (50-60g carbs/hour minimum). Accept that final hours will be survival mode. You can do this.

• WEEK PREVIEW: Race week! Tuesday is easy spin (30 min). Wednesday has race openers (final sharpness). Thursday is rest or easy spin. Friday is pre-race shake-out (if racing Sunday). Saturday/Sunday: RACE DAY!

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W06 Tue - Easy Spin", """• Duration: 30 min

• Zones: Z1-Z2 (55-70% FTP)

• Notes: Easy spin. Just moving legs. No stress. Stay off your feet when not riding.

• CADENCE: Self-selected (85-95 rpm).""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="1200" Power="0.65" Cadence="85"/>
    <Cooldown Duration="600" PowerLow="0.65" PowerHigh="0.55"/>
"""),
        create_workout("W06 Wed - Race Openers", """• STRUCTURE:
10 min easy → 3x3 min @ 85-92% FTP (2 min easy between) → 3x30sec @ 100% FTP (90sec easy between) → 5 min easy

• Final intensity before race. Should feel controlled and strong. If legs feel dead, skip openers and just ride 30 min easy. This is your sharpness check.

• CADENCE WORK: High cadence on all efforts (100+ rpm).""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.70"/>
    <SteadyState Duration="600" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="3" OnDuration="180" OnPower="0.885" Cadence="100" OffDuration="120" OffPower="0.55"/>
    <IntervalsT Repeat="3" OnDuration="30" OnPower="1.00" Cadence="100" OffDuration="90" OffPower="0.55"/>
    <Cooldown Duration="300" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W06 Thu - Rest or Very Easy Spin", """• Optional: 20-30 min Z1

• Notes: If race is Sunday, easy spin. If race is Saturday, rest completely. Listen to your body.

• REST DAY NOTE: Fine to ride if you really want, but no longer than an hour and don't break 30 TSS."""),
        create_workout("W06 Fri - Pre-Race Shake-Out (if racing Sunday)", """• STRUCTURE:
10 min easy → 2x2 min @ 85-90% FTP (2 min easy between) → 2x30sec @ 100% FTP (90sec easy between) → 5 min easy

• Final ride before race. Legs should feel fresh. Check bike one last time. Visualize conservative race execution. You're ready to survive this.

• CADENCE WORK: High cadence on all efforts (100+ rpm).""", """    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.70"/>
    <SteadyState Duration="600" Power="0.70" Cadence="85"/>
    <IntervalsT Repeat="2" OnDuration="120" OnPower="0.875" Cadence="100" OffDuration="120" OffPower="0.55"/>
    <IntervalsT Repeat="2" OnDuration="30" OnPower="1.00" Cadence="100" OffDuration="90" OffPower="0.55"/>
    <Cooldown Duration="300" PowerLow="0.70" PowerHigh="0.50"/>
"""),
        create_workout("W06 Sat - Race Day or Rest", """• If racing Saturday: EXECUTE SURVIVAL PLAN

• If racing Sunday: Complete rest or 20 min easy spin

• Notes: If racing today—START EASY (seriously, way easier than you think), fuel from mile 1 (50-60g carbs/hour minimum, more if you can), accept that you're underprepared so ego has no place here, finish upright. You trained for 5 weeks. That's what you have. Race accordingly.""", """    <FreeRide Duration="60"/>
"""),
        create_workout("W06 Sun - Race Day or Recovery", """• If racing Sunday: EXECUTE SURVIVAL PLAN

• If raced Saturday: Easy 20-30 min recovery spin if legs allow, celebrate survival

• Notes: Race day. Conservative start is MANDATORY—you don't have endurance to recover from going out hard. Fuel aggressively—your tank is smaller than others due to limited training volume. Final hours will hurt—everyone's do, but yours will hurt more because you're underprepared. That's okay. Mental toughness gets you home. You can do this. Just keep moving forward.""", """    <FreeRide Duration="60"/>
""")
    ]
})

template = {
    "plan_metadata": plan_metadata,
    "weeks": weeks,
    "default_modifications": {
        "emergency_philosophy": {
            "enabled": True,
            "description": "Emergency plan for minimal time (3-5 hours/week) - time-efficient G-Spot/Threshold training",
            "volume_range": "3-5 hours/week",
            "reality_check": "Not optimal, but gets you to finish line with conservative pacing and aggressive fueling"
        },
        "cadence_work": {
            "enabled": True,
            "base_period": "High cadence (100+ rpm seated) and low cadence/torque (40-60 rpm seated, big gear) on all intervals",
            "build_period": "Mix high/low cadence + rhythm intervals (2 min Z3 + 1 min Z4 patterns) + loaded intervals (1 min Z5/Z6 → settle into Z3)",
            "description": "Teaches power production in different ways, foundation for changing pace"
        },
        "rhythm_intervals": {
            "enabled": True,
            "weeks": [5],
            "description": "Alternating patterns: 2 min Z3 (self-selected cadence) + 1 min Z4 (high cadence 100+ rpm) x 3, continuous"
        },
        "loaded_intervals": {
            "enabled": True,
            "weeks": [5],
            "description": "1 min Z5/Z6 (high cadence, seated) → settle into 14 min Z3 (self-selected cadence). Simulates race starts and surges."
        },
        "gspot_terminology": {
            "enabled": True,
            "replaces": "Sweet Spot",
            "range": "87-92% FTP"
        },
        "strength_training": {
            "enabled": False,
            "note": "Athlete performs own strength program. Suggested on lighter training days. Emergency plans prioritize time-efficient cycling work."
        },
        "monday_week_preview": {
            "enabled": True,
            "description": "Monday rest days include week preview with key workouts, emergency plan reminders, reality checks, and race execution guidance"
        },
        "rest_day_tss_limit": 30,
        "rest_day_duration_limit_hours": 1,
        "emergency_considerations": {
            "minimal_volume": "3-5 hours/week - every session must count",
            "reality_checks": "Longest ride is 2 hours, race might be 4-8+ hours - pacing and fueling are CRITICAL",
            "conservative_pacing": "START CONSERVATIVELY - you don't have endurance to recover from going out hard",
            "aggressive_fueling": "Fuel from mile 1 (50-60g carbs/hour minimum) - covers endurance gaps"
        }
    }
}

output_path = "/Users/mattirowe/Documents/Gravel Landing Page Project/current/plans/4. Ayahuasca Save My Race (6 weeks)/template.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(template, f, indent=2, ensure_ascii=False)

print(f"✅ Template created: {output_path}")
print(f"   Plan: {plan_metadata['name']}")
print(f"   Duration: {plan_metadata['duration_weeks']} weeks")
print(f"   Philosophy: {plan_metadata['philosophy']}")
print(f"   Total workouts: {sum(len(w['workouts']) for w in weeks)}")
print(f"   Volume: {plan_metadata['target_hours']} hours/week")
print(f"   Status: ✅ Complete and ready for race-specific generation")

