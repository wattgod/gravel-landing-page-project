#!/usr/bin/env python3
"""
Workout Description Generator V2 - Nate Integration
=====================================================
Integrates the comprehensive Nate archetype library with training methodology support.

Key Features:
- 22 workout archetypes with 6 progression levels each (132 variations)
- Training methodology support: POLARIZED, PYRAMIDAL, HIT
- Full dimensional prescriptions: cadence, position, timing, fueling
- Durability workouts for ultra-distance events
- Race simulation workouts

Training Methodologies:
- POLARIZED (80/20): 75-80% Z1-Z2, 15-20% Z4-Z5+, <5% Z3 (Gravel God default)
- PYRAMIDAL: 75-80% Z1-Z2, 10-15% Z3 (G-Spot), 5-10% Z4-Z5+
- HIT (High Intensity Training): Reduced volume, increased intensity frequency

Version: 2.0 (Nate Integration)
"""

import re
import sys
import os
from typing import Dict, Tuple, Optional, List, Any
from pathlib import Path

# =============================================================================
# IMPORT NATE ARCHETYPES
# =============================================================================

# Try to import from archive location
# Path: /Users/mattirowe/Documents/GravelGod/archive/nate_workout_processing
NATE_ARCHIVE_PATH = Path("/Users/mattirowe/Documents/GravelGod/archive/nate_workout_processing")
sys.path.insert(0, str(NATE_ARCHIVE_PATH))

try:
    from new_archetypes import NEW_ARCHETYPES, VO2MAX_NEW, THRESHOLD_NEW, SPRINT_NEW, ANAEROBIC_CAPACITY, DURABILITY_NEW, ENDURANCE_NEW, RACE_SIMULATION
    NATE_ARCHETYPES_AVAILABLE = True
except ImportError:
    print(f"WARNING: Nate archetypes not found at {NATE_ARCHIVE_PATH}")
    NATE_ARCHETYPES_AVAILABLE = False
    NEW_ARCHETYPES = {}

# =============================================================================
# TRAINING METHODOLOGY DEFINITIONS
# =============================================================================

TRAINING_METHODOLOGIES = {
    "POLARIZED": {
        "name": "Polarized (80/20)",
        "description": "75-80% low intensity (Z1-Z2), 15-20% high intensity (Z4-Z5+), <5% threshold (Z3)",
        "intensity_distribution": {
            "low": (0.75, 0.80),      # Z1-Z2
            "moderate": (0.00, 0.05),  # Z3 (minimize)
            "high": (0.15, 0.20)       # Z4-Z5+
        },
        "workout_selection": {
            "primary_quality": ["VO2max", "Sprint_Neuromuscular", "Anaerobic_Capacity"],
            "secondary_quality": ["TT_Threshold"],  # Use sparingly
            "avoid": [],  # No Sweet Spot (uses G-Spot sparingly in durability only)
            "durability_allowed": True,
            "race_simulation_allowed": True
        },
        "recovery_emphasis": "high",
        "g_spot_usage": "durability_only"  # G-Spot (87-92%) only in durability context
    },
    "PYRAMIDAL": {
        "name": "Pyramidal",
        "description": "75-80% low intensity (Z1-Z2), 10-15% tempo/threshold (Z3), 5-10% high intensity (Z4-Z5+)",
        "intensity_distribution": {
            "low": (0.75, 0.80),       # Z1-Z2
            "moderate": (0.10, 0.15),  # Z3 (G-Spot, Tempo)
            "high": (0.05, 0.10)       # Z4-Z5+
        },
        "workout_selection": {
            "primary_quality": ["TT_Threshold"],
            "secondary_quality": ["VO2max", "Anaerobic_Capacity"],
            "avoid": [],
            "durability_allowed": True,
            "race_simulation_allowed": True
        },
        "recovery_emphasis": "moderate",
        "g_spot_usage": "regular"  # G-Spot used more freely
    },
    "HIT": {
        "name": "High Intensity Training",
        "description": "Reduced total volume, increased high-intensity frequency. Time-crunched athletes.",
        "intensity_distribution": {
            "low": (0.60, 0.70),       # Z1-Z2 (reduced)
            "moderate": (0.05, 0.10),  # Z3
            "high": (0.20, 0.30)       # Z4-Z5+ (increased)
        },
        "workout_selection": {
            "primary_quality": ["VO2max", "Anaerobic_Capacity", "Sprint_Neuromuscular"],
            "secondary_quality": ["TT_Threshold"],
            "avoid": ["Durability"],  # Skip long durability for time-crunched
            "durability_allowed": False,
            "race_simulation_allowed": True
        },
        "recovery_emphasis": "critical",  # Recovery even more important with HIT
        "g_spot_usage": "minimal"
    }
}

# Default methodology for Gravel God
DEFAULT_METHODOLOGY = "POLARIZED"


# =============================================================================
# ARCHETYPE LOOKUP AND SELECTION
# =============================================================================

def get_archetype_by_name(name: str, category: str = None) -> Optional[Dict]:
    """Look up an archetype by name, optionally filtering by category."""
    if not NATE_ARCHETYPES_AVAILABLE:
        return None

    search_categories = [category] if category else NEW_ARCHETYPES.keys()

    for cat in search_categories:
        if cat not in NEW_ARCHETYPES:
            continue
        for archetype in NEW_ARCHETYPES[cat]:
            if archetype['name'].lower() == name.lower():
                return archetype
            # Also check for partial matches
            if name.lower() in archetype['name'].lower():
                return archetype

    return None


def get_level_data(archetype: Dict, level: int) -> Optional[Dict]:
    """Get the data for a specific level of an archetype."""
    if not archetype or 'levels' not in archetype:
        return None

    level_key = str(level)
    if level_key not in archetype['levels']:
        # Fall back to closest available level
        available = sorted([int(k) for k in archetype['levels'].keys()])
        if not available:
            return None
        level_key = str(min(available, key=lambda x: abs(x - level)))

    return archetype['levels'].get(level_key)


def select_archetype_for_methodology(
    workout_type: str,
    methodology: str = DEFAULT_METHODOLOGY,
    week_num: int = 1,
    total_weeks: int = 12
) -> Tuple[Optional[Dict], int]:
    """
    Select an appropriate archetype based on workout type and training methodology.

    Returns: (archetype, recommended_level)
    """
    if not NATE_ARCHETYPES_AVAILABLE:
        return None, 1

    method_config = TRAINING_METHODOLOGIES.get(methodology, TRAINING_METHODOLOGIES[DEFAULT_METHODOLOGY])

    # Calculate progression level based on week position (1-6 scale)
    progress = week_num / total_weeks
    if progress < 0.17:
        level = 1
    elif progress < 0.33:
        level = 2
    elif progress < 0.50:
        level = 3
    elif progress < 0.67:
        level = 4
    elif progress < 0.83:
        level = 5
    else:
        level = 6

    # Map workout type to category
    type_to_category = {
        "vo2max": "VO2max",
        "vo2": "VO2max",
        "threshold": "TT_Threshold",
        "tt": "TT_Threshold",
        "sprint": "Sprint_Neuromuscular",
        "neuromuscular": "Sprint_Neuromuscular",
        "anaerobic": "Anaerobic_Capacity",
        "durability": "Durability",
        "endurance": "Endurance",
        "race_sim": "Race_Simulation",
        "race_simulation": "Race_Simulation"
    }

    category = type_to_category.get(workout_type.lower())
    if not category or category not in NEW_ARCHETYPES:
        return None, level

    # Check if this category is allowed by methodology
    if category in method_config["workout_selection"].get("avoid", []):
        return None, level

    # Select first archetype from category (can be enhanced with smarter selection)
    archetypes = NEW_ARCHETYPES.get(category, [])
    if not archetypes:
        return None, level

    return archetypes[0], level


# =============================================================================
# WORKOUT DESCRIPTION GENERATION
# =============================================================================

def generate_nate_workout_description(
    archetype: Dict,
    level: int,
    methodology: str = DEFAULT_METHODOLOGY,
    include_dimensions: bool = True
) -> str:
    """
    Generate a workout description from a Nate archetype.

    Returns formatted description with:
    - WARM-UP
    - MAIN SET (with dimensions)
    - COOL-DOWN
    - PURPOSE
    - METHODOLOGY note
    """
    if not archetype:
        return ""

    level_data = get_level_data(archetype, level)
    if not level_data:
        return ""

    lines = []

    # WARM-UP
    lines.append("WARM-UP:")
    lines.append("• 15min building from Z1 to Z2")
    lines.append("")

    # MAIN SET
    lines.append("MAIN SET:")
    lines.append(f"• {level_data.get('structure', 'See workout structure')}")

    # Dimensions
    if include_dimensions:
        cadence = level_data.get('cadence_prescription')
        position = level_data.get('position_prescription')

        if cadence:
            lines.append(f"• Cadence: {cadence}")
        if position:
            lines.append(f"• Position: {position}")

    lines.append("")

    # COOL-DOWN
    lines.append("COOL-DOWN:")
    lines.append("• 10min easy spin Z1-Z2")
    lines.append("")

    # PURPOSE
    lines.append("PURPOSE:")
    execution = level_data.get('execution', '')
    category_purpose = get_category_purpose(archetype['name'])
    lines.append(f"{category_purpose}")
    lines.append("")
    lines.append(f"Level {level}: {execution}")

    # Methodology note
    method_config = TRAINING_METHODOLOGIES.get(methodology, TRAINING_METHODOLOGIES[DEFAULT_METHODOLOGY])
    if methodology != DEFAULT_METHODOLOGY:
        lines.append("")
        lines.append(f"• TRAINING APPROACH: {method_config['name']}")

    # Fueling (if specified)
    fueling = level_data.get('fueling')
    if fueling:
        lines.append("")
        lines.append(f"• FUELING: {fueling}")

    return "\n".join(lines)


def get_category_purpose(archetype_name: str) -> str:
    """Get the purpose description for a workout category."""
    purposes = {
        "VO2": "VO2max development. Maximum aerobic power—the engine that drives race-winning attacks and sustained high-intensity efforts.",
        "Threshold": "Threshold development. Raising the power you can sustain for 20-60 minutes—the foundation of race-pace performance.",
        "Sprint": "Neuromuscular power. Building the explosive capacity for attacks, steep pitches, and race-winning moves.",
        "Anaerobic": "Anaerobic capacity. Lactate tolerance and the ability to produce race-breaking power repeatedly.",
        "Durability": "Durability training. The ability to produce quality efforts when fatigued—exactly what ultra-distance racing demands.",
        "Endurance": "Aerobic base building. The foundation everything else rests on.",
        "Breakaway": "Race simulation. Practicing the attack-and-hold pattern that wins breakaways.",
        "Sector": "Gravel sector simulation. Hard efforts followed by recovery—the rhythm of gravel racing.",
        "Chaos": "Variable pace training. Unpredictable power changes that mirror real race dynamics."
    }

    for key, purpose in purposes.items():
        if key.lower() in archetype_name.lower():
            return purpose

    return "Quality training. Building race-specific fitness through structured work."


# =============================================================================
# ZWO BLOCK GENERATION
# =============================================================================

def generate_zwo_blocks_from_archetype(archetype: Dict, level: int) -> str:
    """
    Generate ZWO XML blocks from a Nate archetype level.
    """
    if not archetype:
        return ""

    level_data = get_level_data(archetype, level)
    if not level_data:
        return ""

    blocks = []

    # Warmup
    blocks.append('    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>\n')

    # Check for durability workouts (tired_vo2, base_duration, etc.)
    if 'tired_vo2' in level_data or 'base_duration' in level_data:
        base_duration = level_data.get('base_duration', 7200)
        base_power = level_data.get('base_power', 0.70)

        # Long Z2 base
        blocks.append(f'    <SteadyState Duration="{base_duration}" Power="{base_power:.2f}"/>\n')

        # Quality at end
        if 'intervals' in level_data and isinstance(level_data['intervals'], tuple):
            repeats, duration = level_data['intervals']
            on_power = level_data.get('on_power', 1.10)
            off_duration = level_data.get('off_duration', 240)
            cadence = level_data.get('cadence', 90)
            blocks.append(
                f'    <IntervalsT Repeat="{repeats}" OnDuration="{duration}" '
                f'OnPower="{on_power:.2f}" Cadence="{cadence}" OffDuration="{off_duration}" OffPower="0.55"/>\n'
            )

    # Standard intervals
    elif 'intervals' in level_data and isinstance(level_data['intervals'], tuple):
        repeats, duration = level_data['intervals']
        on_power = level_data.get('on_power', 1.0)
        off_power = level_data.get('off_power', 0.55)
        off_duration = level_data.get('off_duration', level_data.get('duration', 180))
        actual_duration = level_data.get('duration', duration)
        cadence = level_data.get('cadence', 90)

        blocks.append(
            f'    <IntervalsT Repeat="{repeats}" OnDuration="{actual_duration}" '
            f'OnPower="{on_power:.2f}" Cadence="{cadence}" OffDuration="{off_duration}" OffPower="{off_power:.2f}"/>\n'
        )

    # Complex efforts (pyramids, descending, etc.)
    elif 'efforts' in level_data and isinstance(level_data['efforts'], list):
        recovery_duration = level_data.get('recovery_duration', 300)

        for i, effort in enumerate(level_data['efforts']):
            if isinstance(effort, dict):
                duration = effort.get('duration', 300)
                power = effort.get('power', 1.0)
                blocks.append(f'    <SteadyState Duration="{duration}" Power="{power:.2f}"/>\n')

                if i < len(level_data['efforts']) - 1:
                    blocks.append(f'    <SteadyState Duration="{recovery_duration}" Power="0.55"/>\n')

    # Single sustained effort
    elif 'single_effort' in level_data:
        duration = level_data.get('duration', 1200)
        power = level_data.get('power', 1.0)
        blocks.append(f'    <SteadyState Duration="{duration}" Power="{power:.2f}"/>\n')

    # Loaded recovery (VO2 + tempo)
    elif 'loaded_recovery' in level_data:
        repeats = level_data['intervals'][0] if isinstance(level_data.get('intervals'), tuple) else 3
        on_duration = level_data.get('duration', 180)
        on_power = level_data.get('on_power', 1.15)
        loaded_duration = level_data.get('loaded_duration', 120)
        loaded_power = level_data.get('loaded_power', 0.85)
        off_duration = level_data.get('off_duration', 180)

        for rep in range(repeats):
            blocks.append(f'    <SteadyState Duration="{on_duration}" Power="{on_power:.2f}"/>\n')
            blocks.append(f'    <SteadyState Duration="{loaded_duration}" Power="{loaded_power:.2f}"/>\n')
            if rep < repeats - 1:
                blocks.append(f'    <SteadyState Duration="{off_duration}" Power="0.50"/>\n')

    # Ramp intervals
    elif 'ramp' in level_data:
        repeats = level_data['intervals'][0] if isinstance(level_data.get('intervals'), tuple) else 2
        ramp_duration = level_data['intervals'][1] if isinstance(level_data.get('intervals'), tuple) else 720
        start_power = level_data.get('start_power', 0.88)
        end_power = level_data.get('end_power', 1.00)
        off_duration = level_data.get('off_duration', 300)

        for rep in range(repeats):
            blocks.append(
                f'    <Ramp Duration="{ramp_duration}" PowerLow="{start_power:.2f}" PowerHigh="{end_power:.2f}"/>\n'
            )
            if rep < repeats - 1:
                blocks.append(f'    <SteadyState Duration="{off_duration}" Power="0.55"/>\n')

    # Peak and fade
    elif 'peak_fade' in level_data:
        repeats = level_data['intervals'][0] if isinstance(level_data.get('intervals'), tuple) else 4
        peak_duration = level_data.get('peak_duration', 10)
        peak_power = level_data.get('peak_power', 2.0)
        fade_duration = level_data.get('fade_duration', 20)
        fade_power = level_data.get('fade_power', 1.2)
        off_duration = level_data.get('off_duration', 180)

        for rep in range(repeats):
            blocks.append(f'    <SteadyState Duration="{peak_duration}" Power="{peak_power:.2f}"/>\n')
            blocks.append(f'    <SteadyState Duration="{fade_duration}" Power="{fade_power:.2f}"/>\n')
            if rep < repeats - 1:
                blocks.append(f'    <SteadyState Duration="{off_duration}" Power="0.50"/>\n')

    # Breakaway simulation
    elif 'breakaway' in level_data:
        repeats = level_data.get('intervals', 2)
        attack_duration = level_data.get('attack_duration', 300)
        attack_power = level_data.get('attack_power', 1.10)
        hold_duration = level_data.get('hold_duration', 600)
        hold_power = level_data.get('hold_power', 0.88)
        recovery_duration = level_data.get('recovery_duration', 300)

        for rep in range(repeats):
            blocks.append(f'    <SteadyState Duration="{attack_duration}" Power="{attack_power:.2f}"/>\n')
            blocks.append(f'    <SteadyState Duration="{hold_duration}" Power="{hold_power:.2f}"/>\n')
            if rep < repeats - 1:
                blocks.append(f'    <SteadyState Duration="{recovery_duration}" Power="0.55"/>\n')

    # Openers
    elif 'openers' in level_data:
        warmup_duration = level_data.get('warmup_duration', 1200)
        warmup_power = level_data.get('warmup_power', 0.65)
        effort_count, effort_duration = level_data.get('efforts', (3, 30))
        effort_power = level_data.get('effort_power', 1.10)
        effort_recovery = level_data.get('effort_recovery', 120)
        cooldown_duration = level_data.get('cooldown_duration', 300)

        # Replace warmup with opener-specific warmup
        blocks = []  # Clear default warmup
        blocks.append(f'    <SteadyState Duration="{warmup_duration}" Power="{warmup_power:.2f}"/>\n')

        for i in range(effort_count):
            blocks.append(f'    <SteadyState Duration="{effort_duration}" Power="{effort_power:.2f}"/>\n')
            if i < effort_count - 1:
                blocks.append(f'    <SteadyState Duration="{effort_recovery}" Power="0.55"/>\n')

        blocks.append(f'    <SteadyState Duration="{cooldown_duration}" Power="0.50"/>\n')
        return ''.join(blocks)

    # Progressive fatigue
    elif 'progressive_fatigue' in level_data:
        num_intervals = level_data.get('intervals', 3)
        effort_duration = level_data.get('effort_duration', 600)
        on_power = level_data.get('on_power', 0.98)
        recovery_sequence = level_data.get('recovery_sequence', [300, 240, 180])

        for i in range(num_intervals):
            blocks.append(f'    <SteadyState Duration="{effort_duration}" Power="{on_power:.2f}"/>\n')
            if i < len(recovery_sequence):
                blocks.append(f'    <SteadyState Duration="{recovery_sequence[i]}" Power="0.55"/>\n')

    # Default fallback
    elif 'on_power' in level_data:
        duration = level_data.get('duration', 300)
        on_power = level_data.get('on_power', 1.0)
        blocks.append(f'    <SteadyState Duration="{duration}" Power="{on_power:.2f}"/>\n')

    # Cooldown
    blocks.append('    <Cooldown Duration="600" PowerLow="0.70" PowerHigh="0.50"/>\n')

    return ''.join(blocks)


# =============================================================================
# METHODOLOGY-AWARE WEEK PLANNING
# =============================================================================

def get_weekly_workout_distribution(
    methodology: str = DEFAULT_METHODOLOGY,
    week_type: str = "normal"  # normal, build, recovery, peak, taper
) -> Dict[str, int]:
    """
    Get the recommended workout distribution for a week based on methodology.

    Returns dict with counts: {workout_type: count_per_week}
    """
    method_config = TRAINING_METHODOLOGIES.get(methodology, TRAINING_METHODOLOGIES[DEFAULT_METHODOLOGY])

    # Base distributions by methodology
    if methodology == "POLARIZED":
        base = {
            "endurance": 4,  # Long Z2 rides
            "vo2max": 1,     # One VO2 session
            "threshold": 0,  # Minimal threshold in polarized
            "sprint": 1,     # Neuromuscular maintenance
            "rest": 1
        }
    elif methodology == "PYRAMIDAL":
        base = {
            "endurance": 3,
            "threshold": 1,  # More threshold work
            "vo2max": 1,
            "sprint": 1,
            "rest": 1
        }
    elif methodology == "HIT":
        base = {
            "endurance": 2,  # Reduced volume
            "vo2max": 2,     # More HIT sessions
            "sprint": 1,
            "rest": 2        # More rest for recovery
        }
    else:
        base = {"endurance": 4, "vo2max": 1, "rest": 2}

    # Modify for week type
    if week_type == "recovery":
        return {k: max(0, v - 1) if k != "rest" else v + 1 for k, v in base.items()}
    elif week_type == "build":
        return {k: v + 1 if k in ["vo2max", "threshold"] else v for k, v in base.items()}
    elif week_type == "taper":
        return {k: v // 2 if k == "endurance" else v for k, v in base.items()}

    return base


# =============================================================================
# EXPORTS AND COMPATIBILITY
# =============================================================================

# Make this module compatible with the legacy v1 interface
def detect_archetype(workout_name: str) -> str:
    """Legacy compatibility: detect archetype from workout name."""
    name_lower = workout_name.lower()

    if "vo2" in name_lower:
        return "vo2max"
    elif "threshold" in name_lower or "tt" in name_lower:
        return "threshold"
    elif "sprint" in name_lower or "stomp" in name_lower:
        return "sprint"
    elif "durability" in name_lower or "tired" in name_lower:
        return "durability"
    elif "endurance" in name_lower or "z2" in name_lower or "easy" in name_lower:
        return "endurance"
    elif "race" in name_lower and "sim" in name_lower:
        return "race_simulation"
    elif "rest" in name_lower:
        return "rest"

    return "general"


def generate_workout_description(workout_name: str, workout_xml: str, plan_info: dict = None) -> str:
    """
    Legacy compatibility: generate description from workout name.
    Enhanced to use Nate archetypes when available.
    """
    archetype_type = detect_archetype(workout_name)

    if NATE_ARCHETYPES_AVAILABLE:
        archetype, level = select_archetype_for_methodology(
            archetype_type,
            methodology=plan_info.get("methodology", DEFAULT_METHODOLOGY) if plan_info else DEFAULT_METHODOLOGY,
            week_num=plan_info.get("week_num", 6) if plan_info else 6,
            total_weeks=plan_info.get("total_weeks", 12) if plan_info else 12
        )

        if archetype:
            return generate_nate_workout_description(
                archetype,
                level,
                methodology=plan_info.get("methodology", DEFAULT_METHODOLOGY) if plan_info else DEFAULT_METHODOLOGY
            )

    # Fall back to basic description
    return f"Quality training session: {workout_name}"


# =============================================================================
# MAIN / TESTING
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("WORKOUT DESCRIPTION GENERATOR V2 - NATE INTEGRATION")
    print("=" * 70)

    if not NATE_ARCHETYPES_AVAILABLE:
        print("\nERROR: Nate archetypes not available!")
        print(f"Expected location: {NATE_ARCHIVE_PATH}")
        sys.exit(1)

    print(f"\n✓ Nate archetypes loaded successfully")
    print(f"  Categories: {list(NEW_ARCHETYPES.keys())}")

    total = sum(len(archetypes) for archetypes in NEW_ARCHETYPES.values())
    print(f"  Total archetypes: {total}")
    print(f"  Total variations: {total * 6}")

    print("\n" + "-" * 70)
    print("TRAINING METHODOLOGIES:")
    print("-" * 70)

    for method_name, config in TRAINING_METHODOLOGIES.items():
        print(f"\n{method_name}: {config['description']}")

    print("\n" + "-" * 70)
    print("SAMPLE WORKOUT GENERATION:")
    print("-" * 70)

    # Generate a sample VO2max workout
    archetype, level = select_archetype_for_methodology("vo2max", "POLARIZED", week_num=8, total_weeks=12)
    if archetype:
        print(f"\nArchetype: {archetype['name']}, Level: {level}")
        print("\nDescription:")
        print("-" * 40)
        description = generate_nate_workout_description(archetype, level, "POLARIZED")
        print(description)

        print("\n" + "-" * 40)
        print("ZWO Blocks:")
        print("-" * 40)
        blocks = generate_zwo_blocks_from_archetype(archetype, level)
        print(blocks)
