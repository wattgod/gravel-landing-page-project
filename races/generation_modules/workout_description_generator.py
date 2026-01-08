#!/usr/bin/env python3
"""
Workout Description Generator
Generates properly formatted ZWO descriptions with:
- WARM-UP section
- MAIN SET with accurate structure, cadence, and position
- COOL-DOWN section
- Archetype-specific PURPOSE that varies by progression level

Fixes the bug where descriptions don't match actual XML structure.
"""

import re
from typing import Dict, Tuple, Optional, List

# =============================================================================
# ARCHETYPE DETECTION
# =============================================================================

# Map workout name patterns to archetypes
ARCHETYPE_PATTERNS = {
    # VO2max archetypes
    "vo2_steady": [r"VO2max\s+Intervals?", r"VO2max\s+Development", r"\d+x\d+\s*min.*VO2"],
    "vo2_30_30": [r"30/30", r"30-30"],
    "vo2_40_20": [r"40/20", r"40-20", r"Broken\s+VO2"],
    "vo2_extended": [r"Extended\s+VO2max"],

    # Threshold archetypes
    "threshold_steady": [r"Threshold\s+Intervals?", r"Threshold\s+Development", r"Steady\s+Threshold", r"Threshold\s+Progression"],
    "threshold_progressive": [r"Progressive\s+Threshold"],
    "threshold_touch": [r"Threshold\s+Touch"],

    # Mixed/Climbing archetypes
    "mixed_climbing": [r"Mixed\s+Climbing", r"Climbing\s+O/U", r"Over.?Under.*Climb"],
    "mixed_intervals": [r"Mixed\s+Intervals?", r"Mixed.*VO2.*Threshold"],

    # SFR/Force archetypes
    "sfr": [r"SFR", r"Force\s+Development", r"Low\s+Cadence\s+Force"],

    # Tempo archetypes
    "tempo": [r"Tempo\s+", r"Steady\s+Tempo"],
    "g_spot": [r"G-?Spot", r"Sweet\s+Spot"],

    # Sprint/Neuromuscular
    "stomps": [r"Stomps?", r"Max\s+Torque"],
    "microbursts": [r"Microburst", r"15/15"],

    # Race simulation
    "race_simulation": [r"Race\s+Simulation", r"Race\s+Sim"],

    # Normalized Power / Intensity Factor
    "normalized_power": [r"Normalized\s+Power", r"NP\s+Workout", r"IF\s+Target", r"Intensity\s+Factor", r"NP.*IF", r"IF.*0\.85", r"NP.*0\.85"],

    # Endurance
    "endurance": [r"Endurance", r"Easy\s+Aerobic", r"Long\s+Aerobic", r"Z[12]\s+"],
    "endurance_blocks": [r"Endurance\s+\+", r"Endurance\s+Blocks", r"Structured\s+Endurance"],

    # Testing
    "testing": [r"FTP\s+Test", r"Assessment", r"Power\s+Profile", r"Testing"],

    # Rest
    "rest": [r"^Rest", r"Rest\s+Day", r"Recovery\s+Day"],
    
    # NEW ARCHETYPES
    "vo2_bookend": [r"VO2\s+Bookend", r"Bookend.*VO2"],
    "tempo_accelerations": [r"UnSteady", r"Tempo.*Acceleration", r"Tempo.*Surge"],
    "threshold_accumulation": [r"Fish\s+and\s+Chips", r"Threshold\s+Accumulation", r"\d+x\d+\s*min.*Z4"],
    "cadence_work": [r"Cadence\s+Clown", r"Cadence\s+Work", r"High\s+Cadence.*Acceleration"],
    "blended_vo2_gspot": [r"Buffers.*30/30", r"Blended.*VO2.*G\s*Spot", r"30/30.*Bookend.*SS"],
}

def detect_archetype(workout_name: str) -> str:
    """Detect workout archetype from workout name."""
    name_upper = workout_name.upper()

    # Check each archetype's patterns
    for archetype, patterns in ARCHETYPE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, workout_name, re.IGNORECASE):
                return archetype

    # Default fallback based on keywords
    if "EASY" in name_upper or "Z1" in name_upper or "Z2" in name_upper:
        return "endurance"
    if "HARD" in name_upper or "QUALITY" in name_upper:
        return "threshold_steady"  # Default hard session

    return "general"

# =============================================================================
# DIMENSIONAL PRESCRIPTIONS
# =============================================================================

# RPE prescriptions by power zone
# Based on Master Zone Chart: Z1=1-2, Z2=3-4, Z3=5-6, G Spot=6-7, Z4=7-8, Z5=9, Z6-Z7=10
RPE_BY_ZONE = {
    "Z1": "1-2",
    "Z2": "3-4",
    "Z3": "5-6",
    "G_Spot": "6-7",
    "Z4": "7-8",
    "Z5": "9",
    "Z6": "10",
    "Z7": "10",
}

def get_zone_range_for_power(power_pct: float) -> str:
    """Get zone range string matching Master Zone Chart for a given power percentage."""
    if power_pct < 0.55:
        return "<55%"  # Z1
    elif power_pct < 0.76:
        return "56-75%"  # Z2
    elif power_pct < 0.88:
        return "76-87%"  # Z3
    elif power_pct < 0.93:
        return "88-92%"  # G Spot
    elif power_pct < 1.06:
        return "93-105%"  # Z4
    elif power_pct < 1.21:
        return "106-120%"  # Z5
    elif power_pct < 1.51:
        return "121-150%"  # Z6
    else:
        return ">150%"  # Z7

def get_rpe_for_power(power_pct: float) -> str:
    """Get RPE range for a given power percentage of FTP."""
    if power_pct < 0.55:
        return "1-2"  # Z1
    elif power_pct < 0.76:
        return "3-4"  # Z2
    elif power_pct < 0.88:
        return "5-6"  # Z3
    elif power_pct < 0.93:
        return "6-7"  # G Spot
    elif power_pct < 1.06:
        return "7-8"  # Z4
    elif power_pct < 1.21:
        return "9"    # Z5
    else:
        return "10"   # Z6-Z7

def get_rpe_for_archetype(archetype: str, power_pct: float = None) -> str:
    """Get RPE range for an archetype, optionally using power percentage."""
    if power_pct:
        return get_rpe_for_power(power_pct)
    
    # Archetype-specific RPE defaults
    archetype_rpe = {
        "vo2_steady": "9",
        "vo2_30_30": "9",
        "vo2_40_20": "9",
        "vo2_extended": "9",
        "threshold_steady": "7-8",
        "threshold_progressive": "7-8",
        "threshold_touch": "7-8",
        "mixed_climbing": "6-7",
        "mixed_intervals": "7-9",
        "sfr": "7-8",
        "tempo": "5-6",
        "g_spot": "6-7",
        "stomps": "10",
        "microbursts": "9-10",
        "race_simulation": "6-9",
        "normalized_power": "6-7",
        "endurance": "3-4",
        "endurance_blocks": "3-4",
        "testing": "9-10",
        "rest": "1-2",
        "general": "5-6",
        
        # NEW ARCHETYPES
        "vo2_bookend": "9 (intervals), 3-4 (Z2)",
        "tempo_accelerations": "5-6 (tempo), 9 (accelerations)",
        "threshold_accumulation": "7-8",
        "cadence_work": "5-6",
        "blended_vo2_gspot": "9 (VO2), 6-7 (SS)",
    }
    return archetype_rpe.get(archetype, "5-6")

# Cadence prescriptions by archetype
CADENCE_PRESCRIPTIONS = {
    "vo2_steady": ("90-100rpm", "high turnover for VO2max efficiency"),
    "vo2_30_30": ("90-100rpm", "high turnover maintains power through fatigue"),
    "vo2_40_20": ("90-100rpm", "high turnover for repeated efforts"),
    "vo2_extended": ("90-100rpm", "high turnover sustains longer intervals"),

    "threshold_steady": ("85-95rpm", "race cadence"),
    "threshold_progressive": ("85-95rpm", "sustainable race cadence"),
    "threshold_touch": ("85-95rpm", "race pace feel"),

    "mixed_climbing": ("70-80rpm", "climbing simulation"),
    "mixed_intervals": ("85-95rpm", "variable as terrain demands"),

    "sfr": ("50-60rpm", "force development"),

    "tempo": ("85-95rpm", "sustainable rhythm"),
    "g_spot": ("85-95rpm", "sustainable sweet spot cadence"),

    "stomps": ("50-60rpm start, accelerate through", "max torque development"),
    "microbursts": ("100-110rpm", "high leg speed"),

    "race_simulation": ("variable", "match race demands"),

    "normalized_power": ("variable", "match terrain and strategy"),

    "endurance": ("self-selected", "comfortable endurance cadence"),
    "endurance_blocks": ("self-selected", "comfortable endurance cadence"),
    "testing": ("self-selected", "natural test cadence"),
    "rest": (None, None),
    "general": ("85-95rpm", "comfortable training cadence"),
    
    # NEW ARCHETYPES
    "vo2_bookend": ("90-100rpm (intervals), self-selected (Z2)", "high turnover for VO2, comfortable for endurance"),
    "tempo_accelerations": ("85-95rpm (tempo), 100+ rpm (accelerations)", "sustainable tempo with high-cadence bursts"),
    "threshold_accumulation": ("85-95rpm", "race cadence for threshold work"),
    "cadence_work": ("105-115rpm", "high cadence leg speed development"),
    "blended_vo2_gspot": ("90-100rpm (VO2), 85-95rpm (SS)", "high turnover for VO2, sustainable for SS"),
}

# Position prescriptions by archetype
POSITION_PRESCRIPTIONS = {
    "vo2_steady": ("Seated, hoods", "stable power platform"),
    "vo2_30_30": ("Seated, hoods", "quick recovery position"),
    "vo2_40_20": ("Seated, hoods", "power efficiency"),
    "vo2_extended": ("Seated, hoods", "sustained effort position"),

    "threshold_steady": ("Seated, drops or hoods", "race position"),
    "threshold_progressive": ("Seated, drops or hoods", "build into aero"),
    "threshold_touch": ("Seated, hoods", "controlled effort"),

    "mixed_climbing": ("Seated, hoods", "climbing efficiency"),
    "mixed_intervals": ("Seated, hoods or drops", "terrain-dependent"),

    "sfr": ("Seated, hoods", "torque focus"),

    "tempo": ("Alternating hoods/drops", "position practice"),
    "g_spot": ("Seated, hoods", "sustainable position"),

    "stomps": ("Seated to standing", "power development"),
    "microbursts": ("Seated, hoods", "quick turnover"),

    "race_simulation": ("Race position", "full race gear"),

    "normalized_power": ("Variable", "match terrain demands - hard on uphills, easier on downhills"),

    "endurance": ("Alternating", "comfort and position practice"),
    "endurance_blocks": ("Alternating", "comfort and position practice"),
    "testing": ("Seated, hoods", "consistent test position"),
    "rest": (None, None),
    "general": ("Seated, hoods", "training position"),
    
    # NEW ARCHETYPES
    "vo2_bookend": ("Seated, hoods (intervals), alternating (Z2)", "stable for VO2, varied for endurance"),
    "tempo_accelerations": ("Alternating in/out of saddle", "position changes during accelerations"),
    "threshold_accumulation": ("Seated, drops or hoods", "race position for threshold"),
    "cadence_work": ("Seated, hoods", "focus on leg speed, not position"),
    "blended_vo2_gspot": ("Seated, hoods", "sustainable position for both intensities"),
}

# =============================================================================
# PURPOSE TEMPLATES
# =============================================================================

# Purpose narratives by archetype (base version)
PURPOSE_TEMPLATES = {
    "vo2_steady": "VO2max development. Maximum aerobic power—the engine that drives race-winning attacks and sustained high-intensity efforts.",

    "vo2_30_30": "Broken VO2 accumulation. More time at max aerobic power than steady intervals allow. The short recovery keeps you in the productive zone longer.",

    "vo2_40_20": "Repeated high-intensity efforts. Builds the ability to attack, recover, and attack again—essential for racing dynamics.",

    "vo2_extended": "Extended VO2max intervals. Pushing deeper into the aerobic ceiling. These longer efforts build both power and mental toughness.",

    "threshold_steady": "Threshold development. Raising the power you can sustain for 20-60 minutes—the foundation of race-pace performance.",

    "threshold_progressive": "Progressive threshold work. Building into effort teaches pacing and race-day strategy.",

    "threshold_touch": "Threshold maintenance. Brief threshold work to maintain race-pace feel without excessive recovery cost.",

    "mixed_climbing": "Mixed climbing simulation. Tempo base with threshold surges—the pattern you'll feel on every rolling climb where the gradient keeps changing.",

    "mixed_intervals": "Mixed intensity intervals. VO2 to threshold transitions simulate race demands where efforts layer on each other.",

    "sfr": "Force development. Low cadence builds the torque for steep grades and tired legs late in the race.",

    "tempo": "Aerobic endurance. The bread and butter of sustainable race-day power. Building the engine that never quits.",

    "g_spot": "Sweet spot work. Maximum aerobic stimulus for minimum recovery cost. The most efficient zone for building race fitness.",

    "stomps": "Neuromuscular power. Max torque from a near-stop builds the explosive power for steep pitches and accelerations.",

    "microbursts": "Leg speed development. High-cadence bursts build the snap for attacks and pace changes.",

    "race_simulation": "Race simulation. Practicing race-day execution—pacing, fueling, mental strategies. This is dress rehearsal.",

    "normalized_power": "Normalized Power (NP) and Intensity Factor (IF) training. Target IF of 0.85 for the duration. How you achieve it is up to you—high average power, hard on uphills, easier on downhills. This teaches race-pace management and power distribution across variable terrain.",

    "endurance": "Aerobic base building. Easy riding builds mitochondrial density and fat oxidation—the foundation everything else rests on.",
    "endurance_blocks": "Structured aerobic endurance. Block intervals at high Z2/low Z3 build aerobic capacity while allowing brief recovery. This format tests and extends your aerobic limit—the power you can sustain for hours.",

    "testing": "Assessment and baseline. Accurate testing sets accurate training zones. Today's numbers guide tomorrow's training.",

    "rest": "Recovery. Adaptation happens during rest. Trust the process.",
    
    # NEW ARCHETYPES
    "vo2_bookend": "VO2 bookend training. VO2 intervals at the start and end maintain high-intensity stimulus while the long Z2 block in the middle builds endurance. This structure simulates race demands where you need power at the start and finish.",
    "tempo_accelerations": "Tempo with accelerations. Sustained tempo work with periodic short bursts builds the ability to maintain race pace while responding to attacks and terrain changes. Position alternation adds race-specific demands.",
    "threshold_accumulation": "Threshold accumulation. Many short threshold intervals with brief recovery build high-volume threshold work. This format accumulates more time at threshold than longer intervals allow, building race-pace endurance.",
    "cadence_work": "Cadence development. High-cadence accelerations (>105rpm) build leg speed and neuromuscular coordination. Power falls where it does, but maintain Z3 minimum—focus is on turnover, not power.",
    "blended_vo2_gspot": "Blended VO2max and G Spot. Combines 30/30 VO2 intervals with sweet spot work in the same session. This format builds both max aerobic power and sustainable race pace in one efficient workout.",

    "general": "Quality training. Building race-specific fitness through structured work.",
}

# Progression-specific PURPOSE additions
def get_progression_purpose(archetype: str, level: int) -> str:
    """Add level-specific context to PURPOSE."""
    base_purpose = PURPOSE_TEMPLATES.get(archetype, PURPOSE_TEMPLATES["general"])

    # Level-specific additions
    level_additions = {
        1: "Introduction to the pattern. Focus on execution quality over power targets.",
        2: "Building volume. Same pattern, more work. The fitness is in the accumulation.",
        3: "Cadence and position focus. Same structure—now refine the execution.",
        4: "Consolidation. Let the body absorb the previous weeks' work. Quality over ambition.",
        5: "Extended sets. More work per set. This is where real adaptations lock in.",
        6: "Peak volume. Maximum training load. You're building the capacity race day demands.",
    }
    
    # Special progression for normalized power workouts
    normalized_power_progressions = {
        1: "Introduction to NP/IF training. Target IF 0.85 for 2 hours. Focus on understanding how variable power affects NP.",
        2: "Building duration. Target IF 0.85 for 2.5 hours. Experiment with different strategies (high average vs. variable).",
        3: "Refining strategy. Target IF 0.85 for 2.5 hours. Focus on optimizing power distribution across terrain.",
        4: "Consolidation. Target IF 0.85 for 2 hours. Let the body absorb the previous weeks' work.",
        5: "Extended duration. Target IF 0.85 for 3 hours. This is where real race-pace management skills develop.",
        6: "Peak duration. Target IF 0.85 for 3 hours. Maximum training load for race-pace management.",
    }

    if archetype == "normalized_power" and level in normalized_power_progressions:
        return f"{base_purpose}\n\nLevel {level}: {normalized_power_progressions[level]}"

    if level in level_additions and archetype not in ["rest", "testing", "endurance"]:
        return f"{base_purpose}\n\nLevel {level}: {level_additions[level]}"

    return base_purpose

# =============================================================================
# XML BLOCK PARSING
# =============================================================================

def parse_xml_blocks(blocks: str) -> Dict:
    """Parse ZWO XML blocks to extract workout structure."""
    structure = {
        "warmup": None,
        "main_sets": [],
        "cooldown": None,
        "total_duration_minutes": 0,
        "pattern_type": None,  # 'intervals', 'over_under', 'steady', 'mixed', 'durability'
        "durability_structure": None,  # For durability workouts: Z2 blocks before/after intervals
    }

    # Parse warmup
    warmup_match = re.search(r'<Warmup\s+Duration="(\d+)"[^/]*/>', blocks)
    if warmup_match:
        duration_sec = int(warmup_match.group(1))
        structure["warmup"] = duration_sec // 60
        structure["total_duration_minutes"] += duration_sec // 60

    # Parse cooldown
    cooldown_match = re.search(r'<Cooldown\s+Duration="(\d+)"[^/]*/>', blocks)
    if cooldown_match:
        duration_sec = int(cooldown_match.group(1))
        structure["cooldown"] = duration_sec // 60
        structure["total_duration_minutes"] += duration_sec // 60

    # Parse FreeRide blocks (for normalized power workouts)
    freeride_match = re.search(r'<FreeRide\s+Duration="(\d+)"[^/]*Power="([0-9.]+)"[^/]*/>', blocks)
    if freeride_match:
        duration_sec = int(freeride_match.group(1))
        power = float(freeride_match.group(2))
        structure["total_duration_minutes"] += duration_sec // 60
        # Mark as normalized power structure
        structure["has_freeride"] = True
        structure["freeride_duration"] = duration_sec // 60
        structure["freeride_power"] = power

    # Parse intervals (IntervalsT)
    intervals_pattern = r'<IntervalsT\s+Repeat="(\d+)"\s+OnDuration="(\d+)"\s+OnPower="([0-9.]+)"[^/]*OffDuration="(\d+)"[^/]*/>'
    for match in re.finditer(intervals_pattern, blocks):
        reps = int(match.group(1))
        on_duration = int(match.group(2))
        on_power = float(match.group(3))
        off_duration = int(match.group(4))

        structure["main_sets"].append({
            "type": "intervals",
            "reps": reps,
            "on_duration_min": on_duration // 60,
            "on_duration_sec": on_duration % 60,
            "on_power_pct": int(on_power * 100),
            "off_duration_min": off_duration // 60,
        })
        structure["pattern_type"] = "intervals"

        total_interval_time = reps * (on_duration + off_duration)
        structure["total_duration_minutes"] += total_interval_time // 60

    # Parse steady state blocks for over/under pattern detection and durability detection
    steady_pattern = r'<SteadyState\s+Duration="(\d+)"\s+Power="([0-9.]+)"[^/]*/>'
    steady_matches = list(re.finditer(steady_pattern, blocks))

    # Collect all steady state blocks with power info
    steady_blocks = []
    for match in steady_matches:
        duration_sec = int(match.group(1))
        power = float(match.group(2))
        steady_blocks.append({
            "duration_sec": duration_sec,
            "duration_min": duration_sec // 60,
            "power": power,
            "power_pct": int(power * 100),
        })
    
    # Detect durability workout: Z2 blocks (0.65-0.72 power) BEFORE intervals
    # Pattern: Z2 endurance → intervals → possibly more Z2
    if structure["main_sets"] and any(s["type"] == "intervals" for s in structure["main_sets"]):
        # Check if there are Z2 blocks before the intervals
        z2_blocks = [b for b in steady_blocks if 0.65 <= b["power"] <= 0.72]
        if z2_blocks:
            # Find where intervals start in the block sequence
            # This is approximate - we'll detect based on structure
            structure["durability_structure"] = {
                "is_durability": True,
                "z2_blocks": z2_blocks,
                "has_intervals": True,
            }
            structure["pattern_type"] = "durability"

    # Detect over/under pattern (alternating tempo/threshold with recovery)
    if len(steady_blocks) >= 4:
        # Check for repeating pattern
        pattern = detect_over_under_pattern(steady_blocks)
        if pattern:
            structure["main_sets"].append(pattern)
            structure["pattern_type"] = "over_under"
            return structure

    # If no pattern detected, add individual blocks (excluding recovery)
    for block in steady_blocks:
        # Skip recovery blocks (power < 60%)
        if block["power"] < 0.60:
            continue
        structure["main_sets"].append({
            "type": "steady",
            "duration_min": block["duration_min"],
            "power_pct": block["power_pct"],
        })
        structure["total_duration_minutes"] += block["duration_min"]

    return structure


def detect_over_under_pattern(steady_blocks: List[Dict]) -> Optional[Dict]:
    """
    Detect over/under climbing pattern in steady state blocks.
    Pattern: (tempo @ 85-90% / threshold @ 93-100%) repeated, with recovery between sets.
    """
    # Filter out recovery blocks for pattern analysis
    work_blocks = [b for b in steady_blocks if b["power"] >= 0.80]
    recovery_blocks = [b for b in steady_blocks if b["power"] < 0.60]

    if len(work_blocks) < 4:
        return None

    # Check for alternating pattern (under/over)
    powers = [b["power_pct"] for b in work_blocks]
    durations = [b["duration_min"] for b in work_blocks]

    # Group into pairs (under, over)
    pairs = []
    i = 0
    while i < len(work_blocks) - 1:
        block1 = work_blocks[i]
        block2 = work_blocks[i + 1]

        # Check if this is an under/over pair (tempo then threshold)
        if block1["power"] < block2["power"] and block1["power"] < 0.92 and block2["power"] >= 0.92:
            pairs.append((block1, block2))
            i += 2
        else:
            i += 1

    if len(pairs) < 2:
        return None

    # Calculate set structure
    # Count how many pairs per set (before recovery)
    reps_per_set = len(pairs)
    num_sets = 1

    # Check for recovery blocks between sets
    if recovery_blocks:
        # Estimate number of sets based on recovery blocks
        num_sets = len(recovery_blocks) + 1
        reps_per_set = len(pairs) // num_sets

    # Use first pair as template
    under_block, over_block = pairs[0]

    return {
        "type": "over_under",
        "sets": num_sets,
        "reps_per_set": max(1, reps_per_set),
        "under_duration": under_block["duration_min"],
        "under_power": under_block["power_pct"],
        "over_duration": over_block["duration_min"],
        "over_power": over_block["power_pct"],
        "recovery_duration": recovery_blocks[0]["duration_min"] if recovery_blocks else 3,
    }

def format_main_set_description(structure: Dict, archetype: str) -> str:
    """Format the MAIN SET section based on parsed structure."""
    # Handle normalized power workouts specially (before checking main_sets)
    if archetype == "normalized_power" or structure.get("has_freeride"):
        duration_min = structure.get("freeride_duration") or structure.get("total_duration_minutes", 180)
        return f"• Target IF of 0.85 for {duration_min} minutes\n• Put Normalized Power (NP) field on your head unit\n• How you achieve it is up to you:\n  - High average power throughout\n  - Hard on uphills, easier on downhills\n  - Variable power matching terrain\n• Focus on managing NP to maintain IF of 0.85\n• RPE: 6-7 (uncomfortably sustainable)"
    
    if not structure or not structure.get("main_sets"):
        return "Unstructured session"

    # Handle durability workouts specially
    if structure.get("durability_structure") and structure["durability_structure"].get("is_durability"):
        return format_durability_workout(structure)

    lines = []

    for i, workout_set in enumerate(structure["main_sets"]):
        if workout_set["type"] == "intervals":
            reps = workout_set["reps"]
            on_min = workout_set["on_duration_min"]
            on_sec = workout_set["on_duration_sec"]
            on_power = workout_set["on_power_pct"]
            off_min = workout_set["off_duration_min"]

            # Format duration
            if on_sec > 0:
                duration_str = f"{on_min}:{on_sec:02d}"
            else:
                duration_str = f"{on_min}min"

            # Get RPE and zone range for this interval
            interval_rpe = get_rpe_for_power(on_power / 100.0)
            zone_range = get_zone_range_for_power(on_power / 100.0)
            lines.append(f"• {reps}x{duration_str} @ {zone_range} FTP, RPE {interval_rpe} ({off_min}min recovery)")

        elif workout_set["type"] == "over_under":
            # Format over/under climbing pattern
            sets = workout_set["sets"]
            reps = workout_set["reps_per_set"]
            under_dur = workout_set["under_duration"]
            under_pwr = workout_set["under_power"]
            over_dur = workout_set["over_duration"]
            over_pwr = workout_set["over_power"]
            recovery = workout_set["recovery_duration"]

            under_rpe = get_rpe_for_power(under_pwr / 100.0)
            over_rpe = get_rpe_for_power(over_pwr / 100.0)
            under_range = get_zone_range_for_power(under_pwr / 100.0)
            over_range = get_zone_range_for_power(over_pwr / 100.0)
            recovery_rpe = "1-2"  # Z1 recovery
            if sets > 1:
                lines.append(f"• {sets} sets of: ({under_dur}min @ {under_range} FTP, RPE {under_rpe} / {over_dur}min @ {over_range} FTP, RPE {over_rpe}) x{reps}")
                lines.append(f"• {recovery}min Z1 recovery between sets (RPE {recovery_rpe})")
            else:
                lines.append(f"• ({under_dur}min @ {under_range} FTP, RPE {under_rpe} / {over_dur}min @ {over_range} FTP, RPE {over_rpe}) x{reps}")

        elif workout_set["type"] == "steady":
            duration = workout_set["duration_min"]
            power = workout_set["power_pct"]
            steady_rpe = get_rpe_for_power(power / 100.0)
            zone_range = get_zone_range_for_power(power / 100.0)
            lines.append(f"• {duration}min @ {zone_range} FTP, RPE {steady_rpe}")

    return "\n".join(lines)

def format_durability_workout(structure: Dict) -> str:
    """Format durability workout: long Z2 ride → intervals → more Z2"""
    lines = []
    durability = structure.get("durability_structure", {})
    z2_blocks = durability.get("z2_blocks", [])
    
    # Get total Z2 time
    total_z2_min = sum(b["duration_min"] for b in z2_blocks)
    
    # Get intervals
    intervals = [s for s in structure["main_sets"] if s["type"] == "intervals"]
    
    if intervals and total_z2_min >= 60:
        # Format as durability workout
        first_z2_hours = total_z2_min // 60
        z2_rpe = get_rpe_for_power(0.70)  # Z2 RPE
        if first_z2_hours >= 1:
            lines.append(f"• First {first_z2_hours} hour{'s' if first_z2_hours > 1 else ''} Z2 (RPE {z2_rpe})")
        
        # Add intervals
        for interval in intervals:
            reps = interval["reps"]
            on_min = interval["on_duration_min"]
            on_power = interval["on_power_pct"]
            off_min = interval["off_duration_min"]
            interval_rpe = get_rpe_for_power(on_power / 100.0)
            zone_range = get_zone_range_for_power(on_power / 100.0)
            lines.append(f"→ {reps}x{on_min}min @ {zone_range} FTP, RPE {interval_rpe} ({off_min}min recovery, RPE 1-2)")
        
        # Check if there's more Z2 after (would need full block parsing)
        lines.append(f"→ Final Z2 to complete ride (RPE {z2_rpe})")
        
        return "\n".join(lines)
    
    # Fallback: format intervals normally
    interval_lines = []
    for interval in intervals:
        reps = interval["reps"]
        on_min = interval["on_duration_min"]
        on_power = interval["on_power_pct"]
        off_min = interval["off_duration_min"]
        interval_rpe = get_rpe_for_power(on_power / 100.0)
        zone_range = get_zone_range_for_power(on_power / 100.0)
        interval_lines.append(f"• {reps}x{on_min}min @ {zone_range} FTP, RPE {interval_rpe} ({off_min}min recovery, RPE 1-2)")
    return "\n".join(interval_lines) if interval_lines else "Durability workout structure"

# =============================================================================
# MAIN DESCRIPTION GENERATOR
# =============================================================================

def generate_workout_description(
    workout_name: str,
    blocks: str,
    week_num: int = 1,
    level: int = 1,
    existing_description: str = ""
) -> str:
    """
    Generate properly formatted workout description.

    Args:
        workout_name: Name of the workout
        blocks: XML blocks string
        week_num: Week number in plan
        level: Progression level (1-6)
        existing_description: Original description (for any notes to preserve)

    Returns:
        Formatted description string
    """
    # Detect archetype
    archetype = detect_archetype(workout_name)

    # Handle rest days
    if archetype == "rest":
        return "Complete rest day. Adaptation happens during rest. Light movement (walk, yoga) is fine."

    # Parse XML structure
    structure = parse_xml_blocks(blocks)

    # Get dimensional prescriptions
    cadence_rpm, cadence_why = CADENCE_PRESCRIPTIONS.get(archetype, CADENCE_PRESCRIPTIONS["general"])
    position, position_why = POSITION_PRESCRIPTIONS.get(archetype, POSITION_PRESCRIPTIONS["general"])

    # Build description sections
    sections = []

    # WARM-UP
    if structure["warmup"]:
        warmup_rpe = get_rpe_for_power(0.65)  # Z1-Z2 range
        sections.append(f"WARM-UP:\n• {structure['warmup']}min building from Z1 to Z2 (RPE {warmup_rpe})")

    # MAIN SET
    main_set_desc = format_main_set_description(structure, archetype)
    main_set_section = f"MAIN SET:\n{main_set_desc}"

    # Add cadence and position guidance
    # Check if this is a durability workout
    is_durability = False
    if structure and structure.get("durability_structure"):
        is_durability = structure["durability_structure"].get("is_durability", False)
    
    if is_durability:
        # Durability workouts: position alternation on Z2, specific guidance on intervals
        main_set_section += f"\n• Z2 sections: Position alternation every 30 min (drops ↔ hoods)"
        main_set_section += f"\n• Intervals: Position as specified for interval type"
        main_set_section += f"\n• Cadence: Z2 self-selected, intervals per archetype"
    elif archetype == "endurance":
        # For endurance/durability rides, add position alternation guidance
        if structure["total_duration_minutes"] >= 90:
            # Long endurance = durability workout
            main_set_section += f"\n• Position: {position} - Alternate every 30 min: 30 min drops (aero) → 30 min hoods (power)"
            main_set_section += f"\n• Cadence: {cadence_rpm if cadence_rpm else 'Self-selected'} - Comfortable endurance cadence"
        else:
            # Shorter endurance rides
            if position:
                main_set_section += f"\n• Position: {position}"
            if cadence_rpm:
                main_set_section += f"\n• Cadence: {cadence_rpm} ({cadence_why})"
    elif archetype == "normalized_power":
        # Normalized power workouts: variable cadence and position based on strategy
        main_set_section += f"\n• Cadence: {cadence_rpm} ({cadence_why})"
        main_set_section += f"\n• Position: {position}"
        main_set_section += f"\n• Strategy: Your choice—high average power, hard on uphills/easier on downhills, or variable matching terrain"
    elif archetype not in ["rest", "testing"]:
        # Quality sessions get specific cadence and position
        if cadence_rpm:
            main_set_section += f"\n• Cadence: {cadence_rpm} ({cadence_why})"
        if position:
            main_set_section += f"\n• Position: {position}"

    sections.append(main_set_section)

    # COOL-DOWN
    if structure["cooldown"]:
        cooldown_rpe = get_rpe_for_power(0.60)  # Z1-Z2 range
        sections.append(f"COOL-DOWN:\n• {structure['cooldown']}min easy spin Z1-Z2 (RPE {cooldown_rpe})")

    # PURPOSE
    # Special handling for durability workouts
    is_durability_purpose = False
    if structure and structure.get("durability_structure"):
        is_durability_purpose = structure["durability_structure"].get("is_durability", False)
    
    if is_durability_purpose:
        purpose = "Durability development. Building your ability to perform intervals when already fatigued—this is race simulation. The long Z2 ride first builds fatigue, then the intervals teach your body to sustain power when tired. This is exactly what you'll face in a 12-16 hour gravel race: needing to push hard after hours of riding."
        if level > 1:
            purpose += f"\n\nLevel {level}: {get_progression_purpose(archetype, level).split('Level')[1] if 'Level' in get_progression_purpose(archetype, level) else 'Building race-specific durability through accumulated fatigue.'}"
    else:
        purpose = get_progression_purpose(archetype, level)
    sections.append(f"PURPOSE:\n{purpose}")

    # Preserve HRV notes if present in original
    if existing_description and "HRV" in existing_description.upper():
        hrv_match = re.search(r'(HRV\s+CHECK:[^•\n]+)', existing_description, re.IGNORECASE)
        if hrv_match:
            sections.append(f"\n{hrv_match.group(1)}")

    # Preserve MASTERS notes if present
    if existing_description and "MASTERS" in existing_description.upper():
        masters_match = re.search(r'(MASTERS\s+NOTE:[^•\n]+)', existing_description, re.IGNORECASE)
        if masters_match:
            sections.append(f"\n{masters_match.group(1)}")

    return "\n\n".join(sections)

# =============================================================================
# TESTING
# =============================================================================

if __name__ == "__main__":
    # Test with sample workout
    test_name = "W02 Tue - VO2max Intervals"
    test_blocks = """    <Warmup Duration="1500" PowerLow="0.50" PowerHigh="0.75"/>
    <IntervalsT Repeat="5" OnDuration="240" OnPower="1.10" Cadence="100" OffDuration="240" OffPower="0.55"/>
    <Cooldown Duration="1200" PowerLow="0.70" PowerHigh="0.50"/>"""

    print("=== Test: VO2max Intervals ===")
    print(generate_workout_description(test_name, test_blocks, week_num=2, level=2))
    print()

    # Test mixed climbing
    test_name2 = "W05 Thu - Mixed Climbing"
    test_blocks2 = """    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>
    <SteadyState Duration="180" Power="0.88"/>
    <SteadyState Duration="120" Power="0.95"/>
    <SteadyState Duration="180" Power="0.88"/>
    <SteadyState Duration="120" Power="0.95"/>
    <SteadyState Duration="180" Power="0.55"/>
    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>"""

    print("=== Test: Mixed Climbing ===")
    print(generate_workout_description(test_name2, test_blocks2, week_num=5, level=3))
