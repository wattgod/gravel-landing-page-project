"""
Weekly structure templates for unified training plans.

Assigns specific days to workout types while respecting recovery needs.
"""

# Key principle: No strength within 48 hours BEFORE a key cycling session
# Key principle: Strength OK on same day as easy ride (AM strength, PM ride)

WEEKLY_TEMPLATES = {
    "standard": {
        "description": "Standard week with Tue/Sat key sessions",
        "days": {
            "monday": {
                "am": "strength",
                "pm": None,
                "is_key_day": False,
                "notes": "Fresh from Sunday rest, ideal for strength"
            },
            "tuesday": {
                "am": None,
                "pm": "intervals",
                "is_key_day": True,
                "notes": "Key session #1 - intervals or threshold work"
            },
            "wednesday": {
                "am": None,
                "pm": "easy_ride",
                "is_key_day": False,
                "notes": "Recovery from Tuesday, prep for Thursday strength"
            },
            "thursday": {
                "am": "strength",
                "pm": "easy_ride",  # Optional
                "is_key_day": False,
                "notes": "Strength + optional easy spin"
            },
            "friday": {
                "am": None,
                "pm": "rest_or_easy",
                "is_key_day": False,
                "notes": "Pre-long-ride rest"
            },
            "saturday": {
                "am": "long_ride",
                "pm": None,
                "is_key_day": True,
                "notes": "Key session #2 - long ride or race sim"
            },
            "sunday": {
                "am": "easy_ride_or_rest",
                "pm": None,
                "is_key_day": False,
                "notes": "Recovery day"
            }
        }
    },
    "three_key": {
        "description": "High-volume week with 3 key sessions (Compete/Podium in Build)",
        "days": {
            "monday": {
                "am": "strength",
                "pm": "easy_ride",
                "is_key_day": False,
                "notes": "Strength AM, easy spin PM"
            },
            "tuesday": {
                "am": None,
                "pm": "intervals",
                "is_key_day": True,
                "notes": "Key session #1"
            },
            "wednesday": {
                "am": None,
                "pm": "easy_ride",
                "is_key_day": False,
                "notes": "Recovery"
            },
            "thursday": {
                "am": "strength",
                "pm": "intervals",
                "is_key_day": True,
                "notes": "Strength AM, intervals PM (key session #2)"
            },
            "friday": {
                "am": None,
                "pm": "rest_or_easy",
                "is_key_day": False,
                "notes": "Rest before weekend"
            },
            "saturday": {
                "am": "long_ride",
                "pm": None,
                "is_key_day": True,
                "notes": "Key session #3 - long ride"
            },
            "sunday": {
                "am": "easy_ride",
                "pm": None,
                "is_key_day": False,
                "notes": "Recovery ride"
            }
        }
    },
    "strength_priority": {
        "description": "Strength-focused week for Ayahuasca tier",
        "days": {
            "monday": {
                "am": "strength",
                "pm": None,
                "is_key_day": False,
                "notes": "Strength session #1"
            },
            "tuesday": {
                "am": None,
                "pm": "intervals",
                "is_key_day": True,
                "notes": "Key cycling session"
            },
            "wednesday": {
                "am": "strength",
                "pm": None,
                "is_key_day": False,
                "notes": "Strength session #2"
            },
            "thursday": {
                "am": None,
                "pm": "easy_ride_or_rest",
                "is_key_day": False,
                "notes": "Recovery"
            },
            "friday": {
                "am": "strength",
                "pm": None,
                "is_key_day": False,
                "notes": "Strength session #3"
            },
            "saturday": {
                "am": "long_ride",
                "pm": None,
                "is_key_day": True,
                "notes": "Long ride"
            },
            "sunday": {
                "am": None,
                "pm": None,
                "is_key_day": False,
                "notes": "Full rest"
            }
        }
    },
    "taper": {
        "description": "Taper week with reduced volume",
        "days": {
            "monday": {
                "am": "strength",
                "pm": None,
                "is_key_day": False,
                "notes": "Light strength - Don't Lose It"
            },
            "tuesday": {
                "am": None,
                "pm": "openers",
                "is_key_day": False,
                "notes": "Short, sharp openers"
            },
            "wednesday": {
                "am": None,
                "pm": "easy_ride",
                "is_key_day": False,
                "notes": "Easy spin"
            },
            "thursday": {
                "am": None,
                "pm": "rest",
                "is_key_day": False,
                "notes": "Rest"
            },
            "friday": {
                "am": None,
                "pm": "openers",
                "is_key_day": False,
                "notes": "Final openers"
            },
            "saturday": {
                "am": None,
                "pm": "rest",
                "is_key_day": False,
                "notes": "Rest before race"
            },
            "sunday": {
                "am": "RACE",
                "pm": None,
                "is_key_day": True,
                "notes": "RACE DAY"
            }
        }
    }
}

def get_weekly_template(tier: str, phase: str) -> dict:
    """Get appropriate weekly template for tier and phase."""
    if phase == "taper":
        return WEEKLY_TEMPLATES["taper"]
    if tier == "ayahuasca":
        return WEEKLY_TEMPLATES["strength_priority"]
    if tier in ["compete", "podium"] and phase in ["build_1", "build_2"]:
        return WEEKLY_TEMPLATES["three_key"]
    return WEEKLY_TEMPLATES["standard"]

def get_strength_days(tier: str, phase: str, sessions_per_week: int) -> list:
    """Get specific days for strength sessions."""
    template = get_weekly_template(tier, phase)
    strength_days = []
    
    for day, schedule in template["days"].items():
        if schedule.get("am") == "strength" or schedule.get("pm") == "strength":
            strength_days.append(day)
    
    # Limit to requested sessions per week
    return strength_days[:sessions_per_week]

