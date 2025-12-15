"""
Tier definitions for Gravel God training plans.

Tiers determine volume, frequency, and periodization approach.
"""

TIERS = {
    "ayahuasca": {
        "name": "Ayahuasca",
        "tagline": "The journey is the destination.",
        "weekly_hours": {"min": 0, "max": 5, "target": 4},
        "description": "For athletes with minimal training time. Strength takes priority. Every session must count.",
        "cycling": {
            "sessions_per_week": {"base": 3, "build": 3, "peak": 3, "taper": 2},
            "long_ride_cap_hours": 2.5,
            "interval_sessions_per_week": 1
        },
        "strength": {
            "sessions_per_week": {"base": 3, "build": 2, "peak": 2, "taper": 1},
            "is_priority": True,
            "session_duration_min": 45
        },
        "weekly_structure": {
            "monday": "strength",
            "tuesday": "intervals",
            "wednesday": "strength", 
            "thursday": "easy_ride_or_rest",
            "friday": "strength",
            "saturday": "long_ride",
            "sunday": "rest"
        }
    },
    "finisher": {
        "name": "Finisher",
        "tagline": "Cross the line. That's the goal.",
        "weekly_hours": {"min": 8, "max": 12, "target": 10},
        "description": "For athletes targeting completion. Balanced approach to cycling and strength.",
        "cycling": {
            "sessions_per_week": {"base": 4, "build": 5, "peak": 4, "taper": 3},
            "long_ride_cap_hours": 4,
            "interval_sessions_per_week": 2
        },
        "strength": {
            "sessions_per_week": {"base": 2, "build": 2, "peak": 1, "taper": 1},
            "is_priority": False,
            "session_duration_min": 45
        },
        "weekly_structure": {
            "monday": "strength",
            "tuesday": "intervals",
            "wednesday": "easy_ride",
            "thursday": "strength",
            "friday": "rest_or_easy",
            "saturday": "long_ride",
            "sunday": "easy_ride"
        }
    },
    "compete": {
        "name": "Compete",
        "tagline": "You came to race.",
        "weekly_hours": {"min": 12, "max": 18, "target": 15},
        "description": "For athletes targeting performance goals. Cycling takes priority, strength supports.",
        "cycling": {
            "sessions_per_week": {"base": 5, "build": 6, "peak": 5, "taper": 4},
            "long_ride_cap_hours": 5,
            "interval_sessions_per_week": 3
        },
        "strength": {
            "sessions_per_week": {"base": 2, "build": 2, "peak": 1, "taper": 1},
            "is_priority": False,
            "session_duration_min": 40
        },
        "weekly_structure": {
            "monday": "strength_am_easy_pm",
            "tuesday": "intervals",
            "wednesday": "easy_ride",
            "thursday": "intervals_or_strength",
            "friday": "rest_or_easy",
            "saturday": "long_ride",
            "sunday": "easy_ride"
        }
    },
    "podium": {
        "name": "Podium",
        "tagline": "Second place is first loser.",
        "weekly_hours": {"min": 18, "max": 25, "target": 20},
        "description": "For athletes targeting podiums. High volume cycling, strength is maintenance only.",
        "cycling": {
            "sessions_per_week": {"base": 6, "build": 7, "peak": 6, "taper": 4},
            "long_ride_cap_hours": 6,
            "interval_sessions_per_week": 3
        },
        "strength": {
            "sessions_per_week": {"base": 2, "build": 1, "peak": 1, "taper": 0},
            "is_priority": False,
            "session_duration_min": 35
        },
        "weekly_structure": {
            "monday": "easy_ride_strength",
            "tuesday": "intervals",
            "wednesday": "easy_ride",
            "thursday": "intervals",
            "friday": "easy_ride_or_rest",
            "saturday": "long_ride",
            "sunday": "easy_ride"
        }
    }
}

def get_tier(tier_id: str) -> dict:
    """Get tier configuration by ID."""
    return TIERS.get(tier_id.lower(), TIERS["finisher"])

def get_strength_sessions(tier_id: str, phase: str) -> int:
    """Get strength sessions per week for tier and phase."""
    tier = get_tier(tier_id)
    phase_map = {"base_1": "base", "base_2": "base", "build_1": "build", 
                 "build_2": "build", "peak": "peak", "taper": "taper"}
    phase_key = phase_map.get(phase, "base")
    return tier["strength"]["sessions_per_week"].get(phase_key, 2)

