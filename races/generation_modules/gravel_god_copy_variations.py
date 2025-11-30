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

    }

    

    if category == 'topic' and subcategory:

        variations = TOPIC_VARIATIONS.get(subcategory, [])

    elif category == 'tier_description' and subcategory:

        variations = TIER_DESCRIPTIONS.get(subcategory, [])

    elif category == 'level_modifier' and subcategory:

        variations = LEVEL_MODIFIERS.get(subcategory, [])

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

    }

    

    return copy

