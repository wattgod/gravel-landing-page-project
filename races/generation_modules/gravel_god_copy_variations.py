#!/usr/bin/env python3

"""

Gravel God Copy Variation Library v1.0

======================================

Randomizable copy blocks to prevent canned-looking marketplace descriptions.

Each category has 30+ variations that get randomly selected during generation.

Usage:

    from gravel_god_copy_variations import get_variation, get_non_negotiable_phrasing

    

    intro = get_variation('fifteen_plans_intro')

    check = get_non_negotiable_phrasing("Heat adaptation protocol built into weeks 6-10")

"""

import random

from typing import List, Dict, Optional

# ============================================================================

# ENCODING FIX: Use these Unicode characters consistently

# ============================================================================

CHECKMARK = "✓"  # U+2713

ARROW = "→"      # U+2192

STAR = "☆"       # U+2606

BULLET = "•"     # U+2022

MDASH = "—"      # U+2014

# ============================================================================

# 15 PLANS SECTION VARIATIONS

# ============================================================================

FIFTEEN_PLANS_HEADLINES = [

    "15 PLANS. ONE RACE. ZERO GENERIC BULLSHIT.",

    "15 PLANS. YOUR RACE. NO COOKIE-CUTTER GARBAGE.",

    "15 WAYS TO TRAIN. ONE FINISH LINE. ZERO EXCUSES.",

    "ONE RACE. 15 APPROACHES. FINALLY, A PLAN THAT FITS.",

    "15 PLANS BECAUSE ONE-SIZE-FITS-ALL IS LAZY.",

    "YOUR LIFE. YOUR HOURS. YOUR PLAN. 15 OPTIONS.",

    "NOT ONE PLAN. FIFTEEN. BECAUSE YOU'RE NOT GENERIC.",

    "15 PLANS. BECAUSE 'JUST TRAIN MORE' ISN'T ADVICE.",

    "FIFTEEN PLANS. ONE OBSESSION. ZERO FLUFF.",

    "15 PLANS FOR 15 DIFFERENT LIVES. PICK YOURS.",

]

FIFTEEN_PLANS_BODY = [

    "Most plans give you one approach for everyone. That's lazy. A 50-year-old with 6 hrs/week needs <strong>fundamentally different training</strong> than a 28-year-old with 15.",

    "Generic plans assume you're generic. You're not. A parent with 5 hours needs different structure than a single 25-year-old with 20.",

    "One plan for everyone is coach malpractice. Your 8 hours/week demands completely different periodization than someone's 18.",

    "Cookie-cutter plans are for cookie-cutter athletes. You didn't sign up for a generic race—why train with a generic plan?",

    "The 'one plan fits all' approach is how coaches avoid actual coaching. We built 15 because your constraints deserve respect.",

    "Most training plans are lazy. One size, take it or leave it. We built 15 because a Masters athlete and a 25-year-old shouldn't train identically.",

    "You're not a template. A time-crunched parent needs different training than a full-time athlete. That's why there are 15 options, not 1.",

    "Generic plans are easy to sell and hard to execute. We did the work—15 plans matched to 15 real-life situations.",

    "Your schedule isn't average, so why train with an average plan? 15 options because real life comes in more than one flavor.",

    "One-size-fits-all is a lie coaches tell to avoid work. We built 15 plans because your 6 hours isn't the same as someone else's 18.",

]

PHILOSOPHY_TAGLINES = [

    "<span style=\"color:#40E0D0;font-weight:bold;\">5-8 hrs?</span> Polarized · <span style=\"color:#40E0D0;font-weight:bold;\">8-12?</span> Pyramidal · <span style=\"color:#40E0D0;font-weight:bold;\">12-18?</span> Block · <span style=\"color:#40E0D0;font-weight:bold;\">18+?</span> GOAT",

    "<span style=\"color:#40E0D0;font-weight:bold;\">Limited time?</span> Polarized intensity · <span style=\"color:#40E0D0;font-weight:bold;\">Moderate?</span> Pyramidal balance · <span style=\"color:#40E0D0;font-weight:bold;\">Serious?</span> Block periodization · <span style=\"color:#40E0D0;font-weight:bold;\">All-in?</span> GOAT protocol",

    "<span style=\"color:#40E0D0;font-weight:bold;\">5-8 hrs:</span> Max stimulus, min time · <span style=\"color:#40E0D0;font-weight:bold;\">8-12:</span> Build the base · <span style=\"color:#40E0D0;font-weight:bold;\">12-18:</span> Race to compete · <span style=\"color:#40E0D0;font-weight:bold;\">18+:</span> Leave nothing",

    "Polarized for the time-crunched. Pyramidal for the balanced. Block for the serious. GOAT for the obsessed.",

    "Different hours = different science. We matched the methodology to your reality.",

]

# ============================================================================

# MASTERCLASS SECTION VARIATIONS

# ============================================================================

MASTERCLASS_HEADLINES = [

    "THE 35-PAGE MASTERCLASS",

    "THE 35-PAGE DEEP DIVE",

    "35 PAGES OF WHAT ACTUALLY WORKS",

    "THE GUIDE: 35 PAGES, ZERO FILLER",

    "35 PAGES OF RACE-SPECIFIC INTEL",

    "THE MASTERCLASS: EVERYTHING THAT MATTERS",

    "35 PAGES. META-ANALYZED. RACE-SPECIFIC.",

    "YOUR 35-PAGE UNFAIR ADVANTAGE",

]

MASTERCLASS_INTROS = [

    "Meta-analysis on everything that matters:",

    "The research, distilled. The BS, removed:",

    "What the science says. What the pros do. What you need:",

    "Everything you need to know, nothing you don't:",

    "Research-backed. Field-tested. Race-specific:",

    "The honest breakdown on what actually moves the needle:",

    "Cut through the noise. Here's what works:",

    "No fluff. No filler. Just what matters:",

]

# Topic descriptions with variations

TOPIC_VARIATIONS = {

    "heat_training": [

        "The protocol that works—when to start, how to adapt",

        "When to start, how hard to push, what actually works",

        "The adaptation timeline and protocols that matter",

        "Start date, session structure, adaptation markers",

        "What the research says, what the pros do, what you need",

    ],

    "fueling": [

        "Calories, hydration, timing for {distance}+ miles",

        "The math on calories, the science on timing",

        "How much, how often, and what happens when you mess up",

        "{distance} miles of fuel strategy, dialed",

        "Carbs per hour, hydration math, gut training",

    ],

    "race_tactics": [

        "When to sit in, when to push, when to survive",

        "Pacing strategy for the long game",

        "The first 50 miles. The middle. The end. Different games.",

        "Group dynamics, solo strategy, checkpoint math",

        "How to not blow up and how to recover when you do",

    ],

    "mental_training": [

        "What to do when mile {dark_mile} hurts",

        "The dark place and how to get through it",

        "Mantras, segments, and suffering management",

        "When your legs quit, your brain takes over. Here's how.",

        "The psychology of ultra-distance suffering",

    ],

    "workout_execution": [

        "Why most athletes fail intervals",

        "How to actually execute the workouts",

        "The difference between completing and nailing it",

        "RPE, pacing, and why your 'hard' isn't hard enough",

        "Execution details that separate finishers from DNFs",

    ],

    "recovery": [

        "The honest takes",

        "What actually matters, what doesn't",

        "Sleep, nutrition, and the stuff most plans skip",

        "The unglamorous work that makes the glamorous work possible",

        "Recovery isn't rest. Here's what it actually is.",

    ],

    "altitude": [

        "The 5 strategies—which one matches your schedule",

        "Live high, train low, and 3 other options",

        "What to do if you can't pre-acclimatize",

        "Altitude prep when you live at sea level",

        "The research, the options, and what's realistic",

    ],

    "tires": [

        "Width, pressure, compound for race conditions",

        "The setup that matches the course",

        "What the fast riders run and why",

        "Tire strategy isn't sexy but it matters",

        "The 10-minute decision that changes your race",

    ],

    "strength": [

        "What to do in the gym, what to skip",

        "Cycling-specific strength that transfers",

        "The minimum effective dose for injury prevention",

        "Gym work that helps vs gym work that hurts",

        "Strength training for endurance—the honest version",

    ],

}

# ============================================================================

# NON-NEGOTIABLE PHRASING VARIATIONS

# ============================================================================

NON_NEGOTIABLE_TEMPLATES = {

    "heat_adaptation": [

        "{checkmark} Heat adaptation protocol starting {weeks} weeks out",

        "{checkmark} Heat training built into weeks {start}-{end}",

        "{checkmark} {sessions}+ heat adaptation sessions before race day",

        "{checkmark} Systematic heat prep—not just 'drink more water'",

        "{checkmark} Heat protocol matched to Kansas June conditions",

    ],

    "long_rides": [

        "{checkmark} Two {hours}+ hour rides minimum before race day",

        "{checkmark} {hours}-hour dress rehearsal in week {week}",

        "{checkmark} Long ride progression building to {hours} hours",

        "{checkmark} Race simulation rides with full nutrition protocol",

        "{checkmark} Time-in-saddle that actually prepares you",

    ],

    "nutrition": [

        "{checkmark} Race-day nutrition dialed: {carbs}g carbs/hour",

        "{checkmark} Fueling strategy tested on training rides",

        "{checkmark} {carbs}g/hour carb protocol, practiced and proven",

        "{checkmark} Gut training built into long ride progression",

        "{checkmark} Nutrition execution—not just 'eat more'",

    ],

    "tire_strategy": [

        "{checkmark} Tire strategy: {width}mm+ with chunk protection",

        "{checkmark} Tire setup matched to course conditions",

        "{checkmark} Equipment dialed for {surface} surfaces",

        "{checkmark} Tire pressure and width optimized for the course",

        "{checkmark} Rubber that matches the terrain",

    ],

    "mental_prep": [

        "{checkmark} Mental prep for hours {start}-{end} when legs stop working",

        "{checkmark} Psychological strategies for mile {dark_mile}",

        "{checkmark} Suffering management for the dark miles",

        "{checkmark} Mental training for when fitness isn't enough",

        "{checkmark} The brain work that gets you to the finish",

    ],

    "climbing": [

        "{checkmark} Climbing-specific power development for {elevation}+ feet",

        "{checkmark} Hill repeats building to race-day demands",

        "{checkmark} Sustained climbing intervals throughout build phase",

        "{checkmark} Vertical preparation matched to {elevation} ft gain",

        "{checkmark} Power-to-weight work that transfers to race day",

    ],

    "altitude": [

        "{checkmark} Altitude strategy matched to your schedule and access",

        "{checkmark} High-altitude preparation protocol",

        "{checkmark} {altitude}+ ft elevation—specific adaptations built in",

        "{checkmark} Altitude prep options based on your reality",

        "{checkmark} Thin-air protocols for sea-level athletes",

    ],

    "skills": [

        "{checkmark} Technical skills training for {terrain} terrain",

        "{checkmark} Cornering and line selection practice built in",

        "{checkmark} Bike handling for race-specific conditions",

        "{checkmark} Skills work that prevents race-day mistakes",

        "{checkmark} Technical confidence for {surface} surfaces",

    ],

    "dress_rehearsal": [

        "{checkmark} {hours}-hour dress rehearsal in week {week}",

        "{checkmark} Full race simulation with race nutrition",

        "{checkmark} Dress rehearsal mimicking race conditions",

        "{checkmark} Practice run covering {percent}% of race distance",

        "{checkmark} Simulation ride with everything dialed",

    ],

}

# ============================================================================

# TIER DESCRIPTION VARIATIONS

# ============================================================================

TIER_DESCRIPTIONS = {

    "ayahuasca": [

        "You're underprepared by conventional standards. These plans are damage control—getting you to the finish line when time isn't on your side.",

        "Limited hours, maximum focus. Every session counts when you're working with constraints.",

        "The desperate tier, honestly. But desperate doesn't mean impossible—it means efficient.",

        "You don't have the hours. We get it. This plan squeezes maximum adaptation from minimum time.",

        "Time-crunched reality meets smart training. Not ideal, but effective.",

    ],

    "finisher": [

        "This plan maximizes your 8-12 hours with focused quality over junk volume. The goal: cross the line strong, not crawl.",

        "Enough hours to prepare properly. This plan builds the base you need and the fitness to finish confident.",

        "The realistic tier. You've got time to train right—this plan makes sure you do.",

        "8-12 hours is workable. This plan turns those hours into a finish you'll be proud of.",

        "Quality over quantity, but enough quantity to matter. Built for reliable finishes.",

    ],

    "compete": [

        "You're not just finishing—you're racing. This plan builds the engine and the tactics to compete for your category.",

        "Serious structure for serious athletes. You've got the time—now build the fitness to use it.",

        "Category placement isn't luck. It's preparation. This is that preparation.",

        "12-18 hours means you can build real race fitness. This plan does exactly that.",

        "The competitor tier. You're not here to survive—you're here to race.",

    ],

    "podium": [

        "Elite tier. Full commitment required. If you're reading this, you probably need coaching, not a plan.",

        "Maximum hours, maximum structure, maximum results. This is the all-in option.",

        "The serious-serious tier. Most athletes here benefit from personalized coaching.",

        "18+ hours is a full-time commitment. This plan respects that with full-time structure.",

        "You've got the hours and the drive. This plan has the structure to match.",

    ],

}

LEVEL_MODIFIERS = {

    "beginner": [

        "Conservative progression. Fundamentals first. Built for athletes new to structured training.",

        "Learning the ropes while building fitness. Sustainable progression over aggressive gains.",

        "First-time structured training? Start here. We'll build the foundation right.",

        "Beginner-friendly progression—but don't confuse beginner with easy.",

    ],

    "intermediate": [

        "You know the basics. This plan assumes competence and builds on it.",

        "Some background, looking to level up. Moderate progression with room to push.",

        "Not your first rodeo, but not your hundredth either. Balanced approach.",

        "Experience meets ambition. Solid structure for solid athletes.",

    ],

    "advanced": [

        "Aggressive progression for experienced athletes. You know your body—this plan pushes it.",

        "High intensity, high volume, high expectations. Built for athletes who can handle it.",

        "You've done the work before. This plan assumes that and builds accordingly.",

        "Advanced means advanced. Don't pick this if you're not ready for it.",

    ],

    "masters": [

        "Fast After 50 methodology. Recovery emphasis without sacrificing intensity.",

        "Age-appropriate periodization. Your experience is an asset—train like it.",

        "Masters athletes need different structure. This plan delivers it.",

        "Recovery isn't weakness—it's wisdom. Built for athletes who know the difference.",

    ],

    "save_my_race": [

        "Six weeks. Emergency protocol. Compressed intensity because that's what you've got.",

        "The Hail Mary tier. Not ideal, but better than showing up unprepared.",

        "Race is soon, training is behind. This plan does damage control.",

        "Six weeks of focused work beats six weeks of panic. Start here.",

    ],

}

# ============================================================================

# SIMPLIFIED TEMPLATE VARIATIONS

# ============================================================================

TIER_PHILOSOPHY_VARIATIONS = {
    "ayahuasca": [
        "High-intensity interval training works for time-crunched athletes. You get maximum fitness from minimal time, enough intensity to sharpen performance, and enough recovery to absorb the stress. No junk miles. No hero intervals. Just systematic progression toward finishing the distance.",
        "Minimal time demands maximum efficiency. HIIT delivers fitness when volume isn't possible. You get intensity that sharpens, recovery that enables, and progression that gets you to the finish. No wasted sessions. No filler. Just results.",
        "Time-crunched doesn't mean unprepared. High-intensity training works when every minute counts. You get the stimulus you need, the recovery you require, and the progression that finishes the distance.",
    ],
    "finisher": [
        "Polarized training principles work for athletes with moderate time. You get enough volume to build durability, enough intensity to sharpen performance, and enough recovery to absorb both. No junk miles. No hero intervals. Just systematic progression toward a strong finish.",
        "Moderate hours demand smart structure. Polarized training builds the base and sharpens the edge. You get volume that builds durability, intensity that creates fitness, and recovery that enables both. Systematic progression toward finishing strong.",
        "8-12 hours is enough to prepare properly. Polarized training maximizes those hours. You get the base you need, the intensity that sharpens, and the recovery that enables. No wasted time. Just progression toward a strong finish.",
    ],
    "compete": [
        "Polarized training principles work for time-crunched competitive athletes. You get enough volume to build durability, enough intensity to sharpen performance, and enough recovery to absorb both. No junk miles. No hero intervals. Just systematic progression toward a specific performance target.",
        "Competitive athletes need competitive training. Polarized structure delivers. You get volume that builds race fitness, intensity that sharpens performance, and recovery that enables progression. Systematic training toward competitive results.",
        "12-18 hours demands smart periodization. Polarized training builds the engine and sharpens the edge. You get the volume for durability, the intensity for performance, and the recovery for progression. No wasted sessions. Just competitive preparation.",
    ],
    "podium": [
        "Block periodization and high-volume training work for serious athletes. You get massive aerobic volume to build extreme durability, concentrated intensity blocks to target limiters, and systematic recovery to absorb the load. No junk miles. No wasted time. Just elite-level preparation.",
        "Elite preparation demands elite structure. Block periodization targets limiters. High volume builds durability. Systematic recovery enables progression. You get the volume for extreme fitness, the intensity for performance, and the structure for results.",
        "18+ hours requires professional-level structure. Block periodization concentrates intensity. High volume builds extreme durability. Systematic recovery enables progression. No wasted time. Just elite-level preparation.",
    ],
}

TRAINING_APPROACH_VARIATIONS = {
    "ayahuasca": [
        "Minimal-volume training without fueling precision breaks athletes. 60-80g carbs/hour—not theory, practiced at race intensity until automatic when you're suffering. The {plan_title} builds systems that work under load. {weather_adaptation}Three-Act pacing framework maps tactics to the race timeline. Technical skills and mental protocols are practiced under load. Training at {weekly_hours} hours requires systems, not just discipline.",
        "Time-crunched training demands precision. Fueling at 60-80g carbs/hour—practiced until automatic. The {plan_title} builds systems that function under stress. {weather_adaptation}Three-Act pacing maps strategy to race timeline. Skills and mental protocols practiced under load. {weekly_hours} hours requires systems, not hope.",
    ],
    "finisher": [
        "Moderate-volume training without fueling precision breaks athletes. 60-80g carbs/hour—not theory, practiced at race intensity until automatic when you're suffering. The {plan_title} builds systems that work under load. {weather_adaptation}Three-Act pacing framework maps tactics to the race timeline. Technical skills and mental protocols are practiced under load. Training at {weekly_hours} hours requires systems, not just discipline.",
        "8-12 hours demands smart structure. Fueling at 60-80g carbs/hour—practiced until automatic. The {plan_title} builds systems that function under stress. {weather_adaptation}Three-Act pacing maps strategy to race timeline. Skills and mental protocols practiced under load. {weekly_hours} hours requires systems, not hope.",
    ],
    "compete": [
        "High-volume training without fueling precision breaks athletes. 60-80g carbs/hour—not theory, practiced at race intensity until automatic when you're suffering. The {plan_title} builds systems that work under load. {weather_adaptation}Three-Act pacing framework maps tactics to the race timeline. Technical skills and mental protocols are practiced under load. Training at {weekly_hours} hours requires systems, not just discipline.",
        "Competitive training demands competitive systems. Fueling at 60-80g carbs/hour—practiced until automatic. The {plan_title} builds systems that function under stress. {weather_adaptation}Three-Act pacing maps strategy to race timeline. Skills and mental protocols practiced under load. {weekly_hours} hours requires systems, not hope.",
    ],
    "podium": [
        "Elite-level training without fueling precision breaks athletes. 60-80g carbs/hour—not theory, practiced at race intensity until automatic when you're suffering. The {plan_title} builds systems that work under load. {weather_adaptation}Three-Act pacing framework maps tactics to the race timeline. Technical skills and mental protocols are practiced under load. Training at {weekly_hours} hours requires systems, not just discipline.",
        "Elite preparation demands elite systems. Fueling at 60-80g carbs/hour—practiced until automatic. The {plan_title} builds systems that function under stress. {weather_adaptation}Three-Act pacing maps strategy to race timeline. Skills and mental protocols practiced under load. {weekly_hours} hours requires systems, not hope.",
    ],
}

PLAN_FEATURES_VARIATIONS = {
    "ayahuasca": [
        "Precision taper protocol with deload timing proven for {level} athletes. Distance-specific fueling for the {distance} miles: 60-80g carbs/hour protocol tested for extended efforts. {weather_adaptation}",
        "Taper protocol optimized for {level} athletes. Fueling strategy for {distance} miles: 60-80g carbs/hour tested under load. {weather_adaptation}",
    ],
    "finisher": [
        "Precision taper protocol with deload timing proven for {level} athletes. Distance-specific fueling for the {distance} miles: 60-80g carbs/hour protocol tested for extended efforts. {weather_adaptation}",
        "Taper protocol optimized for {level} athletes. Fueling strategy for {distance} miles: 60-80g carbs/hour tested under load. {weather_adaptation}",
    ],
    "compete": [
        "Precision taper protocol with deload timing proven for {level} athletes. Distance-specific fueling for the {distance} miles: 60-80g carbs/hour protocol tested for extended efforts. {weather_adaptation}",
        "Taper protocol optimized for {level} athletes. Fueling strategy for {distance} miles: 60-80g carbs/hour tested under load. {weather_adaptation}",
    ],
    "podium": [
        "Precision taper protocol with deload timing proven for {level} athletes. Distance-specific fueling for the {distance} miles: 60-80g carbs/hour protocol tested for extended efforts. {weather_adaptation}",
        "Taper protocol optimized for {level} athletes. Fueling strategy for {distance} miles: 60-80g carbs/hour tested under load. {weather_adaptation}",
    ],
}

ALTERNATIVE_WARNING_VARIATIONS = {
    "ayahuasca": [
        "Or you could keep doing random intensity without structure. Minimal volume without periodization. Fitness doesn't peak when needed.",
        "Or you could wing it with random training. No structure, no periodization, no peak when it matters.",
    ],
    "finisher": [
        "Or you could keep doing big volume without periodization. Random intensity distribution. Fitness doesn't peak when needed.",
        "Or you could just ride more without structure. Random intensity, no periodization, no peak when it matters.",
    ],
    "compete": [
        "Or you could keep doing big volume without periodization. Random intensity distribution. Fitness doesn't peak when needed.",
        "Or you could just ride more without structure. Random intensity, no periodization, no peak when it matters.",
    ],
    "podium": [
        "Or you could keep doing massive volume without structure. Random intensity distribution. Fitness doesn't peak when needed.",
        "Or you could just ride more without structure. Random intensity, no periodization, no peak when it matters.",
    ],
}

DELIVERY_HEADLINE_VARIATIONS = [
    "Systematic progression eliminates guesswork. Training becomes results.",
    "Structured training creates predictable results. No guesswork, just progression.",
    "Systematic preparation delivers systematic results. Training becomes performance.",
]

DELIVERY_DETAILS_VARIATIONS = [
    "Power distribution for {distance} miles • Race execution protocols • Fueling and hydration at intensity • Technical skills under fatigue",
    "Power management for {distance} miles • Race execution systems • Fueling protocols under load • Technical skills when tired",
]

# ============================================================================
# RACE-SPECIFIC CONTENT POOLS
# ============================================================================

# ============================================================================
# RACE-SPECIFIC CONTENT POOL GENERATOR
# ============================================================================

from pathlib import Path
import re

def extract_race_specific_content(race_data, research_doc_path=None):
    """
    Automatically extract race-specific content from race JSON and research docs.
    Generates content pools for terrain, weather, location, character, and challenges.
    
    Args:
        race_data: Race JSON data
        research_doc_path: Optional path to research document (e.g., COURSE_BREAKDOWN_RESEARCH.md)
    
    Returns:
        Dictionary with race-specific content pools by category
    """
    race_metadata = race_data.get("race_metadata", {})
    race_characteristics = race_data.get("race_characteristics", {})
    race_hooks = race_data.get("race_hooks", {})
    non_negotiables = race_data.get("non_negotiables", [])
    
    race_name = race_metadata.get("name", "")
    location = race_metadata.get("location", "")
    distance = race_metadata.get("distance_miles", 0)
    terrain_type = race_characteristics.get("terrain", "")
    typical_weather = race_characteristics.get("typical_weather", "")
    climate = race_characteristics.get("climate", "")
    
    # Extract from race hooks
    punchy_hook = race_hooks.get("punchy", "")
    detail_hook = race_hooks.get("detail", "")
    
    # Build terrain references
    terrain_refs = []
    if terrain_type:
        # Convert terrain type to readable format
        terrain_readable = terrain_type.replace("_", " ").title()
        terrain_refs.append(f"{terrain_readable}")
        if location:
            terrain_refs.append(f"{location} {terrain_readable.lower()}")
        terrain_refs.append(f"{terrain_readable.lower()} terrain")
    
    # Extract terrain details from non-negotiables
    for nn in non_negotiables:
        requirement = nn.get("requirement", "").lower()
        why = nn.get("why", "").lower()
        if "clay" in requirement or "clay" in why:
            if "red clay" in why:
                terrain_refs.append("red clay that becomes unrideable mud when wet")
                terrain_refs.append("red clay that turns to peanut butter mud")
        if "flint" in requirement or "flint" in why:
            terrain_refs.append("Flint Hills terrain")
            terrain_refs.append("Flint-specific cornering")
    
    # Build weather references
    weather_refs = []
    if "unpredictable" in climate.lower() or "unpredictable" in typical_weather.lower():
        weather_refs.append("weather lottery")
        weather_refs.append("weather lottery that decides your race")
        weather_refs.append("unpredictable weather")
        weather_refs.append("unpredictable conditions")
        if "40-75" in typical_weather or "swing" in typical_weather.lower():
            weather_refs.append("40-75°F temperature swings")
        if "freezing" in typical_weather.lower() or "heat" in typical_weather.lower():
            weather_refs.append("weather lottery: freezing rain or heat")
    elif "hot" in climate.lower() or "hot" in typical_weather.lower():
        weather_refs.append("June heat")
        weather_refs.append("85-95°F conditions")
        weather_refs.append("hot and humid conditions")
        weather_refs.append("heat that breaks people")
    
    # Build location references
    location_refs = []
    if location:
        location_refs.append(location)
        if distance:
            location_refs.append(f"{distance} miles of {location.split(',')[0]}")
        location_refs.append(f"{location.split(',')[0]} gravel")
    
    # Build character references from hooks
    character_refs = []
    if punchy_hook:
        # Extract key phrases from punchy hook
        if "Bobby Wintle" in punchy_hook or "hugs" in punchy_hook:
            character_refs.append("Bobby Wintle hugs every finisher")
        if "hospitality" in detail_hook.lower():
            character_refs.append("unreasonable hospitality instead of unreasonable suffering")
    
    # Extract from non-negotiables for character
    for nn in non_negotiables:
        why = nn.get("why", "").lower()
        if "tactical" in why or "pack" in why:
            character_refs.append("tactical pack racing")
        if "exposed" in why or "ridgeline" in why:
            character_refs.append("exposed ridgelines amplify wind")
            character_refs.append("exposed terrain")
    
    # Build challenge references from non-negotiables
    challenge_refs = []
    for nn in non_negotiables:
        requirement = nn.get("requirement", "").lower()
        why = nn.get("why", "").lower()
        
        if "clay" in why and "mud" in why:
            challenge_refs.append("red clay becomes unrideable peanut butter mud when wet")
        if "exposed" in why and "wind" in why:
            challenge_refs.append("exposed ridgelines amplify wind")
        if "tactical" in why:
            challenge_refs.append("tactical pack racing on exposed sections")
        if "weather" in why and "turn" in why:
            challenge_refs.append("weather turns mid-race")
            challenge_refs.append("conditions change mid-race")
        if "heat" in why:
            challenge_refs.append("heat that breaks people")
        if "flint" in requirement.lower():
            challenge_refs.append("Flint-specific cornering and line selection")
    
    # Read research document if provided
    research_content = ""
    if research_doc_path and Path(research_doc_path).exists():
        try:
            with open(research_doc_path, 'r', encoding='utf-8') as f:
                research_content = f.read()
        except:
            pass
    
    # Extract additional references from research doc
    if research_content:
        research_lower = research_content.lower()
        race_name_lower = race_name.lower()
        
        # Look for race-specific mentions in research doc
        if race_name_lower in research_lower:
            # Extract sentences mentioning the race
            sentences = re.findall(rf'[^.!?]*{re.escape(race_name_lower)}[^.!?]*[.!?]', research_content, re.IGNORECASE)
            for sentence in sentences[:3]:  # Limit to 3 sentences
                sentence_clean = sentence.strip()
                if len(sentence_clean) < 150:  # Only short, usable phrases
                    if "terrain" in sentence_clean.lower() or "clay" in sentence_clean.lower() or "flint" in sentence_clean.lower():
                        terrain_refs.append(sentence_clean)
                    elif "weather" in sentence_clean.lower() or "heat" in sentence_clean.lower():
                        weather_refs.append(sentence_clean)
    
    # Remove duplicates and empty strings
    def clean_refs(ref_list):
        return list(dict.fromkeys([r.strip() for r in ref_list if r.strip()]))
    
    return {
        "terrain": clean_refs(terrain_refs),
        "weather": clean_refs(weather_refs),
        "location": clean_refs(location_refs),
        "character": clean_refs(character_refs),
        "challenges": clean_refs(challenge_refs),
    }

# Legacy Mid South references (kept for backward compatibility)
MID_SOUTH_REFERENCES = {
    "terrain": [
        "Oklahoma red clay",
        "red clay terrain",
        "red clay roads",
        "red clay that becomes unrideable mud when wet",
        "red clay that turns to peanut butter mud",
    ],
    "weather": [
        "weather lottery",
        "weather lottery that decides your race",
        "unpredictable weather",
        "40-75°F temperature swings",
        "weather lottery: freezing rain or heat",
        "unpredictable conditions",
    ],
    "location": [
        "Stillwater, Oklahoma",
        "Oklahoma gravel",
        "100 miles of Oklahoma",
    ],
    "character": [
        "Bobby Wintle hugs every finisher",
        "unreasonable hospitality instead of unreasonable suffering",
        "tactical pack racing",
        "exposed ridgelines amplify wind",
        "exposed terrain",
    ],
    "challenges": [
        "red clay becomes unrideable peanut butter mud when wet",
        "exposed ridgelines amplify wind",
        "tactical pack racing on exposed sections",
        "weather turns mid-race",
        "conditions change mid-race",
    ],
}

def get_race_specific_reference(race_data, category, tier_key, level_key, used_refs=None):
    """
    Get a race-specific reference that's unique to this plan.
    Automatically extracts content from race JSON and research docs.
    
    Args:
        race_data: Race JSON data
        category: Reference category (terrain, weather, location, character, challenges)
        tier_key: Tier key for uniqueness
        level_key: Level key for uniqueness
        used_refs: Set of already-used references to avoid duplicates
    
    Returns:
        Race-specific reference string, or empty string if not applicable
    """
    race_name = race_data.get("race_metadata", {}).get("name", "").lower()
    
    if used_refs is None:
        used_refs = set()
    
    # Try to find research document
    base_path = Path(__file__).parent.parent.parent
    research_doc = base_path / "docs" / "COURSE_BREAKDOWN_RESEARCH.md"
    
    # Extract race-specific content automatically
    race_content = extract_race_specific_content(race_data, research_doc if research_doc.exists() else None)
    
    # Get pool for this category
    pool = race_content.get(category, [])
    
    # Fall back to legacy Mid South references if pool is empty and it's Mid South
    if not pool and "mid south" in race_name:
        pool = MID_SOUTH_REFERENCES.get(category, [])
    
    if not pool:
        return ""
    
    # Use tier+level as seed to get consistent but varied references
    import random
    seed_value = hash(f"{tier_key}_{level_key}_{category}")
    random.seed(seed_value)
    
    # Filter out already-used references
    available = [ref for ref in pool if ref not in used_refs]
    if not available:
        available = pool  # Fall back to all if all used
    
    selected = random.choice(available)
    used_refs.add(selected)
    
    return selected

# ============================================================================

# UTILITY FUNCTIONS

# ============================================================================

def get_variation(category: str, subcategory: str = None, **kwargs) -> str:

    """

    Get a random variation from a category.

    

    Args:

        category: Main category ('fifteen_plans_headline', 'masterclass_intro', etc.)

        subcategory: For nested categories like topic variations

        **kwargs: Variables to format into the string (e.g., distance=200)

    

    Returns:

        Randomly selected variation with variables filled in

    """

    

    variation_map = {

        'fifteen_plans_headline': FIFTEEN_PLANS_HEADLINES,

        'fifteen_plans_body': FIFTEEN_PLANS_BODY,

        'philosophy_tagline': PHILOSOPHY_TAGLINES,

        'masterclass_headline': MASTERCLASS_HEADLINES,

        'masterclass_intro': MASTERCLASS_INTROS,

        'tier_philosophy': TIER_PHILOSOPHY_VARIATIONS.get(subcategory, []) if subcategory else [],

        'training_approach': TRAINING_APPROACH_VARIATIONS.get(subcategory, []) if subcategory else [],

        'plan_features': PLAN_FEATURES_VARIATIONS.get(subcategory, []) if subcategory else [],

        'alternative_warning': ALTERNATIVE_WARNING_VARIATIONS.get(subcategory, []) if subcategory else [],

        'delivery_headline': DELIVERY_HEADLINE_VARIATIONS,

        'delivery_details': DELIVERY_DETAILS_VARIATIONS,

    }

    

    if category == 'topic' and subcategory:

        variations = TOPIC_VARIATIONS.get(subcategory, [])

    elif category == 'tier_description' and subcategory:

        variations = TIER_DESCRIPTIONS.get(subcategory, [])

    elif category == 'level_modifier' and subcategory:

        variations = LEVEL_MODIFIERS.get(subcategory, [])

    elif category == 'tier_philosophy' and subcategory:

        variations = TIER_PHILOSOPHY_VARIATIONS.get(subcategory, [])

    elif category == 'training_approach' and subcategory:

        variations = TRAINING_APPROACH_VARIATIONS.get(subcategory, [])

    elif category == 'plan_features' and subcategory:

        variations = PLAN_FEATURES_VARIATIONS.get(subcategory, [])

    elif category == 'alternative_warning' and subcategory:

        variations = ALTERNATIVE_WARNING_VARIATIONS.get(subcategory, [])

    else:

        variations = variation_map.get(category, [])

    

    if not variations:

        return f"[MISSING: {category}/{subcategory}]"

    

    selected = random.choice(variations)

    

    # Format with provided kwargs

    if kwargs:

        try:

            selected = selected.format(**kwargs, checkmark=CHECKMARK, arrow=ARROW)

        except KeyError:

            pass  # Leave unformatted if missing kwargs

    

    return selected

def get_non_negotiable_phrasing(raw_text: str, race_data: dict = None) -> str:

    """

    Convert a raw non-negotiable into varied phrasing.

    

    Args:

        raw_text: Original non-negotiable text

        race_data: Race JSON data for variable substitution

    

    Returns:

        Rephrased non-negotiable with checkmark

    """

    # Handle both string and dict formats
    if isinstance(raw_text, dict):
        raw_text = raw_text.get('requirement', '')

    # Extract key information from raw text

    raw_lower = raw_text.lower()

    

    # Determine category and select appropriate template

    if 'heat' in raw_lower:

        templates = NON_NEGOTIABLE_TEMPLATES['heat_adaptation']

        kwargs = {'weeks': '4-6', 'start': 6, 'end': 10, 'sessions': 10}

    elif 'hour' in raw_lower and ('ride' in raw_lower or 'rehearsal' in raw_lower):

        templates = NON_NEGOTIABLE_TEMPLATES['long_rides']

        kwargs = {'hours': 6, 'week': 9}

    elif 'carb' in raw_lower or 'nutrition' in raw_lower or 'fuel' in raw_lower:

        templates = NON_NEGOTIABLE_TEMPLATES['nutrition']

        kwargs = {'carbs': '80-100'}

    elif 'tire' in raw_lower:

        templates = NON_NEGOTIABLE_TEMPLATES['tire_strategy']

        kwargs = {'width': 40, 'surface': 'mixed gravel'}

    elif 'mental' in raw_lower or 'hour' in raw_lower and 'when' in raw_lower:

        templates = NON_NEGOTIABLE_TEMPLATES['mental_prep']

        kwargs = {'start': 8, 'end': 12, 'dark_mile': 150}

    elif 'climb' in raw_lower or 'elevation' in raw_lower:

        templates = NON_NEGOTIABLE_TEMPLATES['climbing']

        kwargs = {'elevation': '10,000'}

    elif 'altitude' in raw_lower:

        templates = NON_NEGOTIABLE_TEMPLATES['altitude']

        kwargs = {'altitude': 8000}

    elif 'skill' in raw_lower or 'corner' in raw_lower or 'technical' in raw_lower:

        templates = NON_NEGOTIABLE_TEMPLATES['skills']

        kwargs = {'terrain': 'technical', 'surface': 'loose gravel'}

    elif 'dress' in raw_lower or 'simulation' in raw_lower:

        templates = NON_NEGOTIABLE_TEMPLATES['dress_rehearsal']

        kwargs = {'hours': 6, 'week': 9, 'percent': 50}

    else:

        # Default: just add checkmark to original

        return f"{CHECKMARK} {raw_text}"

    

    # Override with race data if provided

    if race_data:

        race_metadata = race_data.get('race_metadata', {})

        race_characteristics = race_data.get('race_characteristics', {})

        guide_variables = race_data.get('guide_variables', {})

        

        if 'distance_miles' in race_metadata:

            kwargs['distance'] = race_metadata['distance_miles']

        if 'elevation_feet' in race_metadata:

            kwargs['elevation'] = f"{race_metadata['elevation_feet']:,}"

        if 'DARK_MILE' in guide_variables:

            kwargs['dark_mile'] = guide_variables['DARK_MILE']

    

    selected = random.choice(templates)

    return selected.format(**kwargs, checkmark=CHECKMARK)

def generate_varied_marketplace_copy(race_data: dict, tier: str, level: str, seed: int = None) -> dict:

    """

    Generate a complete set of varied copy for marketplace description.

    

    Args:

        race_data: Race JSON data

        tier: Tier key (ayahuasca, finisher, compete, podium)

        level: Level key (beginner, intermediate, advanced, masters, save_my_race)

        seed: Random seed for reproducibility (optional)

    

    Returns:

        Dictionary with all varied copy blocks

    """

    

    if seed:

        random.seed(seed)

    

    race_metadata = race_data.get('race_metadata', {})

    race_hooks = race_data.get('race_hooks', {})

    guide_variables = race_data.get('guide_variables', {})

    

    # Build varied copy
    copy = {
        'fifteen_plans_headline': get_variation('fifteen_plans_headline'),
        'fifteen_plans_body': get_variation('fifteen_plans_body'),
        'philosophy_tagline': get_variation('philosophy_tagline'),
        'masterclass_headline': get_variation('masterclass_headline'),
        'masterclass_intro': get_variation('masterclass_intro'),
        'tier_description': get_variation('tier_description', tier),
        'level_modifier': get_variation('level_modifier', level),
        
        # Topic descriptions with race-specific values
        'topic_heat': get_variation('topic', 'heat_training'),
        'topic_fueling': get_variation('topic', 'fueling', distance=race_metadata.get('distance_miles', 100)),
        'topic_tactics': get_variation('topic', 'race_tactics'),
        'topic_mental': get_variation('topic', 'mental_training', dark_mile=guide_variables.get('DARK_MILE', 100)),
        'topic_execution': get_variation('topic', 'workout_execution'),
        'topic_recovery': get_variation('topic', 'recovery'),
        'topic_altitude': get_variation('topic', 'altitude'),
        
        # Non-negotiables (rephrased)
        'non_negotiables': [
            get_non_negotiable_phrasing(nn, race_data) 
            for nn in race_data.get('non_negotiables', [])[:3]
        ],
        
        # Simplified template fields (will be formatted with race-specific data)
        'tier_philosophy': get_variation('tier_philosophy', tier),
        'training_approach': get_variation('training_approach', tier),
        'plan_features': get_variation('plan_features', tier),
        'alternative_warning': get_variation('alternative_warning', tier),
        'delivery_headline': get_variation('delivery_headline'),
        'delivery_details': get_variation('delivery_details'),
    }

    

    return copy

