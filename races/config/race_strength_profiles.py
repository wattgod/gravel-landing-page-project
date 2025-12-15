"""
Race-specific strength customization.

Different races demand different physical qualities.
"""

RACE_STRENGTH_PROFILES = {
    "unbound_gravel_200": {
        "name": "Unbound Gravel 200",
        "primary_demands": ["endurance", "hip_stability", "core_endurance"],
        "secondary_demands": ["single_leg_power", "grip_strength"],
        "emphasized_patterns": ["hinge", "core", "single_leg"],
        "emphasized_exercises": [
            "Single-Leg RDL",
            "Pallof Press",
            "Side Plank",
            "Hip Thrust",
            "Farmer Carry",
            "Dead Bug"
        ],
        "de_emphasized_exercises": [
            "Heavy Back Squat",  # Less relevant for steady-state
            "Bench Press"        # Upper body less critical
        ],
        "notes": "200 miles demands hip endurance and core stability for 10+ hours in the saddle. Single-leg work prevents imbalances. Avoid heavy bilateral squats that create unnecessary fatigue."
    },
    "unbound_gravel_100": {
        "name": "Unbound Gravel 100",
        "primary_demands": ["power_endurance", "hip_stability"],
        "secondary_demands": ["acceleration", "core_stability"],
        "emphasized_patterns": ["hinge", "core", "power"],
        "emphasized_exercises": [
            "KB Swing",
            "Bulgarian Split Squat",
            "Pallof Press",
            "Box Jump"
        ],
        "de_emphasized_exercises": [],
        "notes": "100 miles is faster and punchier than the 200. More power work, but still need hip endurance."
    },
    "leadville_100": {
        "name": "Leadville Trail 100",
        "primary_demands": ["climbing_power", "altitude_resilience", "single_leg_strength"],
        "secondary_demands": ["core_stability", "hip_endurance"],
        "emphasized_patterns": ["squat", "single_leg", "core"],
        "emphasized_exercises": [
            "Bulgarian Split Squat",
            "Step-Up",
            "Single-Leg Squat",
            "Goblet Squat",
            "Plank variations"
        ],
        "de_emphasized_exercises": [
            "Heavy Deadlift"  # Low back fatigue problematic at altitude
        ],
        "notes": "12,000+ ft of climbing at altitude. Single-leg strength is king. Avoid exercises that tax the low back excessively—altitude already compromises recovery."
    },
    "belgian_waffle_ride": {
        "name": "Belgian Waffle Ride",
        "primary_demands": ["explosive_power", "technical_handling", "repeated_efforts"],
        "secondary_demands": ["core_stability", "upper_body_endurance"],
        "emphasized_patterns": ["power", "core", "push"],
        "emphasized_exercises": [
            "Box Jump",
            "Plyo Push-Up",
            "KB Swing",
            "Split Squat Jump",
            "Pallof Press"
        ],
        "de_emphasized_exercises": [],
        "notes": "Punchy climbs, technical descents, repeated accelerations. Power and core are critical. Some upper body work helps with bike handling fatigue."
    },
    "mid_south": {
        "name": "Mid South",
        "primary_demands": ["mud_power", "hip_stability", "grip_endurance"],
        "secondary_demands": ["core_stability", "single_leg_power"],
        "emphasized_patterns": ["hinge", "core", "grip"],
        "emphasized_exercises": [
            "KB Swing",
            "Farmer Carry",
            "Suitcase Carry",
            "Dead Bug",
            "Single-Leg RDL"
        ],
        "de_emphasized_exercises": [],
        "notes": "Mud demands constant power application and core stability. Grip work helps with wet bar control. Hip hinge power for punching through soft surfaces."
    },
    "sbt_grvl": {
        "name": "SBT GRVL",
        "primary_demands": ["altitude_power", "climbing_endurance", "technical_descending"],
        "secondary_demands": ["core_stability", "hip_endurance"],
        "emphasized_patterns": ["squat", "core", "single_leg"],
        "emphasized_exercises": [
            "Bulgarian Split Squat",
            "Goblet Squat",
            "Side Plank",
            "Bird Dog",
            "Step-Up"
        ],
        "de_emphasized_exercises": [],
        "notes": "Steamboat altitude + climbing. Similar to Leadville profile but less extreme. Technical descents need core stability."
    },
    "gravel_worlds": {
        "name": "Gravel Worlds",
        "primary_demands": ["endurance", "hip_stability", "steady_power"],
        "secondary_demands": ["core_endurance", "single_leg_balance"],
        "emphasized_patterns": ["hinge", "core", "carry"],
        "emphasized_exercises": [
            "Hip Thrust",
            "Single-Leg RDL", 
            "Farmer Carry",
            "Dead Bug",
            "Pallof Press"
        ],
        "de_emphasized_exercises": [],
        "notes": "Long, steady grind in Nebraska. Hip endurance and core stability for endless miles of similar terrain."
    },
    "crusher_in_the_tushar": {
        "name": "Crusher in the Tushar",
        "primary_demands": ["climbing_power", "altitude_resilience", "pacing"],
        "secondary_demands": ["core_stability", "single_leg_strength"],
        "emphasized_patterns": ["squat", "single_leg", "core"],
        "emphasized_exercises": [
            "Bulgarian Split Squat",
            "Step-Up",
            "Goblet Squat",
            "Plank",
            "Single-Leg Glute Bridge"
        ],
        "de_emphasized_exercises": [
            "Heavy Deadlift"
        ],
        "notes": "10,000+ ft of climbing at altitude. Very similar profile to Leadville. Single-leg dominance, protect the low back."
    },
    "rebeccas_private_idaho": {
        "name": "Rebecca's Private Idaho",
        "primary_demands": ["sustained_power", "hip_endurance", "technical_handling"],
        "secondary_demands": ["core_stability", "upper_body_endurance"],
        "emphasized_patterns": ["hinge", "core", "single_leg"],
        "emphasized_exercises": [
            "KB Swing",
            "Single-Leg RDL",
            "Pallof Press",
            "Push-Up",
            "Bird Dog"
        ],
        "de_emphasized_exercises": [],
        "notes": "Mix of gravel and pavement with technical sections. Balanced profile with slight emphasis on hip power and handling stability."
    }
}

# Default profile for races not specifically defined
DEFAULT_PROFILE = {
    "name": "Generic Gravel",
    "primary_demands": ["endurance", "hip_stability", "core_stability"],
    "secondary_demands": ["single_leg_power", "grip_strength"],
    "emphasized_patterns": ["hinge", "core", "single_leg"],
    "emphasized_exercises": [
        "Single-Leg RDL",
        "Pallof Press", 
        "Dead Bug",
        "Hip Thrust",
        "Farmer Carry"
    ],
    "de_emphasized_exercises": [],
    "notes": "Balanced gravel-focused strength program."
}

def get_race_profile(race_id: str) -> dict:
    """Get strength profile for a race."""
    return RACE_STRENGTH_PROFILES.get(race_id.lower(), DEFAULT_PROFILE)

def get_emphasized_exercises(race_id: str) -> list:
    """Get list of emphasized exercises for a race."""
    profile = get_race_profile(race_id)
    return profile.get("emphasized_exercises", [])

