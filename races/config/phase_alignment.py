"""
Phase alignment between cycling and strength training.

Strength phases are subordinate to cycling phases.
"""

# Cycling phases drive the timeline
CYCLING_PHASES = {
    "base_1": {
        "purpose": "Aerobic foundation",
        "volume": "moderate",
        "intensity": "low",
        "key_sessions": ["endurance", "tempo"]
    },
    "base_2": {
        "purpose": "Aerobic development", 
        "volume": "high",
        "intensity": "low-moderate",
        "key_sessions": ["endurance", "sweet_spot"]
    },
    "build_1": {
        "purpose": "Race-specific fitness",
        "volume": "high",
        "intensity": "moderate-high",
        "key_sessions": ["threshold", "vo2max", "race_sim"]
    },
    "build_2": {
        "purpose": "Peak fitness",
        "volume": "moderate-high", 
        "intensity": "high",
        "key_sessions": ["vo2max", "race_sim", "over_unders"]
    },
    "peak": {
        "purpose": "Sharpen",
        "volume": "moderate",
        "intensity": "high",
        "key_sessions": ["openers", "race_sim"]
    },
    "taper": {
        "purpose": "Freshness",
        "volume": "low",
        "intensity": "moderate",
        "key_sessions": ["openers"]
    }
}

# Strength phases aligned to cycling phases
PHASE_ALIGNMENT = {
    # Cycling Phase → Strength Phase
    "base_1": "Learn to Lift",      # Build movement patterns while volume is moderate
    "base_2": "Learn to Lift",      # Continue patterns, cycling volume increasing
    "build_1": "Lift Heavy Sh*t",   # Max strength while cycling intensity rises
    "build_2": "Lift Fast",         # Convert to power as cycling peaks
    "peak": "Lift Fast",            # Maintain power, reduced volume
    "taper": "Don't Lose It"        # Minimum dose, preserve adaptations
}

# Strength frequency by tier and phase
STRENGTH_FREQUENCY = {
    # tier: {cycling_phase: sessions_per_week}
    "ayahuasca": {
        "base_1": 3,    # Strength priority for low-volume athletes
        "base_2": 3,
        "build_1": 2,
        "build_2": 2,
        "peak": 2,
        "taper": 1
    },
    "finisher": {
        "base_1": 2,
        "base_2": 2,
        "build_1": 2,
        "build_2": 2,
        "peak": 1,
        "taper": 1
    },
    "compete": {
        "base_1": 2,
        "base_2": 2,
        "build_1": 2,
        "build_2": 1,   # Reduce as cycling intensity peaks
        "peak": 1,
        "taper": 1
    },
    "podium": {
        "base_1": 2,
        "base_2": 2,
        "build_1": 1,   # Earlier reduction for high-volume athletes
        "build_2": 1,
        "peak": 1,
        "taper": 0      # Optional - athlete's choice
    }
}

def get_strength_phase(cycling_phase: str) -> str:
    """Get aligned strength phase for a cycling phase."""
    return PHASE_ALIGNMENT.get(cycling_phase, "Learn to Lift")

def get_strength_frequency(tier: str, cycling_phase: str) -> int:
    """Get strength sessions per week for tier and phase."""
    return STRENGTH_FREQUENCY.get(tier, {}).get(cycling_phase, 2)

