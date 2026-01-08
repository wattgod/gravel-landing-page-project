#!/usr/bin/env python3
"""
Generate example ZWO files for all workout archetypes at all 6 progression levels.
Creates 19 archetypes × 6 levels = 114 example ZWO files.
"""

import os
import html
from pathlib import Path
from typing import Dict, List, Tuple

# ZWO Template
ZWO_TEMPLATE = """<?xml version='1.0' encoding='UTF-8'?>
<workout_file>
  <author>Gravel God Training</author>
  <name>{name}</name>
  <description>{description}</description>
  <sportType>bike</sportType>
  <workout>
{blocks}  </workout>
</workout_file>"""

# Archetype progression definitions
ARCHETYPE_PROGRESSIONS = {
    "vo2_steady": {
        "name": "VO2max Steady Intervals",
        "levels": {
            1: {"reps": 3, "on_duration": 180, "on_power": 1.10, "off_duration": 180, "off_power": 0.55},
            2: {"reps": 5, "on_duration": 180, "on_power": 1.10, "off_duration": 180, "off_power": 0.55},
            3: {"reps": 5, "on_duration": 180, "on_power": 1.10, "off_duration": 180, "off_power": 0.55, "cadence": (100, 110)},
            4: {"reps": 4, "on_duration": 180, "on_power": 1.10, "off_duration": 180, "off_power": 0.55},
            5: {"reps": 3, "on_duration": 240, "on_power": 1.10, "off_duration": 240, "off_power": 0.55},
            6: {"reps": 6, "on_duration": 180, "on_power": 1.10, "off_duration": 180, "off_power": 0.55},
        }
    },
    "vo2_30_30": {
        "name": "VO2max 30/30",
        "levels": {
            1: {"reps": 8, "on_duration": 30, "on_power": 1.25, "off_duration": 30, "off_power": 0.50},
            2: {"reps": 10, "on_duration": 30, "on_power": 1.25, "off_duration": 30, "off_power": 0.50},
            3: {"reps": 10, "on_duration": 30, "on_power": 1.25, "off_duration": 30, "off_power": 0.50, "cadence": (100, 110)},
            4: {"reps": 8, "on_duration": 30, "on_power": 1.25, "off_duration": 30, "off_power": 0.50},
            5: {"reps": 12, "on_duration": 30, "on_power": 1.25, "off_duration": 30, "off_power": 0.50},
            6: {"reps": 15, "on_duration": 30, "on_power": 1.25, "off_duration": 30, "off_power": 0.50},
        }
    },
    "vo2_40_20": {
        "name": "VO2max 40/20",
        "levels": {
            1: {"reps": 6, "on_duration": 40, "on_power": 1.20, "off_duration": 20, "off_power": 0.50},
            2: {"reps": 8, "on_duration": 40, "on_power": 1.20, "off_duration": 20, "off_power": 0.50},
            3: {"reps": 8, "on_duration": 40, "on_power": 1.20, "off_duration": 20, "off_power": 0.50, "cadence": (100, 110)},
            4: {"reps": 6, "on_duration": 40, "on_power": 1.20, "off_duration": 20, "off_power": 0.50},
            5: {"reps": 10, "on_duration": 40, "on_power": 1.20, "off_duration": 20, "off_power": 0.50},
            6: {"reps": 12, "on_duration": 40, "on_power": 1.20, "off_duration": 20, "off_power": 0.50},
        }
    },
    "vo2_extended": {
        "name": "VO2max Extended",
        "levels": {
            1: {"reps": 2, "on_duration": 300, "on_power": 1.10, "off_duration": 300, "off_power": 0.55},
            2: {"reps": 3, "on_duration": 300, "on_power": 1.10, "off_duration": 300, "off_power": 0.55},
            3: {"reps": 3, "on_duration": 300, "on_power": 1.10, "off_duration": 300, "off_power": 0.55, "cadence": (100, 110)},
            4: {"reps": 2, "on_duration": 360, "on_power": 1.10, "off_duration": 360, "off_power": 0.55},
            5: {"reps": 2, "on_duration": 480, "on_power": 1.10, "off_duration": 480, "off_power": 0.55},
            6: {"reps": 3, "on_duration": 360, "on_power": 1.10, "off_duration": 360, "off_power": 0.55},
        }
    },
    "threshold_steady": {
        "name": "Threshold Steady",
        "levels": {
            1: {"reps": 2, "on_duration": 600, "on_power": 1.00, "off_duration": 300, "off_power": 0.55},
            2: {"reps": 3, "on_duration": 600, "on_power": 1.00, "off_duration": 300, "off_power": 0.55},
            3: {"reps": 3, "on_duration": 600, "on_power": 1.00, "off_duration": 300, "off_power": 0.55, "position": "drops"},
            4: {"reps": 2, "on_duration": 720, "on_power": 1.00, "off_duration": 300, "off_power": 0.55},
            5: {"reps": 2, "on_duration": 900, "on_power": 1.00, "off_duration": 300, "off_power": 0.55},
            6: {"reps": 3, "on_duration": 720, "on_power": 1.00, "off_duration": 300, "off_power": 0.55},
        }
    },
    "threshold_progressive": {
        "name": "Threshold Progressive",
        "levels": {
            1: {"blocks": [(600, 0.95), (600, 1.00)]},  # 2x10min building 95%→100%
            2: {"blocks": [(720, 0.95), (720, 1.02)]},  # 2x12min building 95%→102%
            3: {"blocks": [(720, 0.95), (720, 1.02)], "position": "drops"},
            4: {"blocks": [(600, 0.95), (600, 1.00)]},  # Consolidation
            5: {"blocks": [(900, 0.95), (900, 1.02)]},  # Extended
            6: {"blocks": [(720, 0.95), (720, 1.02), (720, 0.95), (720, 1.02)]},  # Peak volume
        }
    },
    "threshold_touch": {
        "name": "Threshold Touch",
        "levels": {
            1: {"reps": 1, "on_duration": 300, "on_power": 1.00, "off_duration": 0, "off_power": 0},
            2: {"reps": 2, "on_duration": 300, "on_power": 1.00, "off_duration": 300, "off_power": 0.55},
            3: {"reps": 2, "on_duration": 300, "on_power": 1.00, "off_duration": 300, "off_power": 0.55, "position": "drops"},
            4: {"reps": 1, "on_duration": 360, "on_power": 1.00, "off_duration": 0, "off_power": 0},
            5: {"reps": 2, "on_duration": 360, "on_power": 1.00, "off_duration": 300, "off_power": 0.55},
            6: {"reps": 2, "on_duration": 480, "on_power": 1.00, "off_duration": 300, "off_power": 0.55},
        }
    },
    "mixed_climbing": {
        "name": "Mixed Climbing",
        "levels": {
            1: {"sets": 3, "reps_per_set": 1, "under_duration": 180, "under_power": 0.88, "over_duration": 60, "over_power": 0.98},
            2: {"sets": 4, "reps_per_set": 1, "under_duration": 180, "under_power": 0.88, "over_duration": 60, "over_power": 0.98},
            3: {"sets": 4, "reps_per_set": 1, "under_duration": 180, "under_power": 0.88, "over_duration": 60, "over_power": 0.98, "cadence": (70, 80)},
            4: {"sets": 3, "reps_per_set": 1, "under_duration": 180, "under_power": 0.88, "over_duration": 60, "over_power": 0.98},
            5: {"sets": 5, "reps_per_set": 1, "under_duration": 180, "under_power": 0.88, "over_duration": 60, "over_power": 0.98},
            6: {"sets": 6, "reps_per_set": 1, "under_duration": 180, "under_power": 0.88, "over_duration": 60, "over_power": 0.98},
        }
    },
    "mixed_intervals": {
        "name": "Mixed Intervals",
        "levels": {
            1: {"sets": 3, "vo2_duration": 120, "vo2_power": 1.10, "threshold_duration": 180, "threshold_power": 0.98},
            2: {"sets": 4, "vo2_duration": 120, "vo2_power": 1.10, "threshold_duration": 180, "threshold_power": 0.98},
            3: {"sets": 4, "vo2_duration": 120, "vo2_power": 1.10, "threshold_duration": 180, "threshold_power": 0.98, "position": "drops"},
            4: {"sets": 3, "vo2_duration": 120, "vo2_power": 1.10, "threshold_duration": 180, "threshold_power": 0.98},
            5: {"sets": 5, "vo2_duration": 120, "vo2_power": 1.10, "threshold_duration": 180, "threshold_power": 0.98},
            6: {"sets": 6, "vo2_duration": 120, "vo2_power": 1.10, "threshold_duration": 180, "threshold_power": 0.98},
        }
    },
    "sfr": {
        "name": "SFR - Sustained Force Repetitions",
        "levels": {
            1: {"reps": 3, "on_duration": 180, "on_power": 0.97, "off_duration": 180, "off_power": 0.55, "cadence": (50, 60)},
            2: {"reps": 4, "on_duration": 180, "on_power": 0.97, "off_duration": 180, "off_power": 0.55, "cadence": (50, 60)},
            3: {"reps": 4, "on_duration": 180, "on_power": 0.97, "off_duration": 180, "off_power": 0.55, "cadence": (50, 60)},
            4: {"reps": 3, "on_duration": 240, "on_power": 0.97, "off_duration": 240, "off_power": 0.55, "cadence": (50, 60)},
            5: {"reps": 4, "on_duration": 240, "on_power": 0.97, "off_duration": 240, "off_power": 0.55, "cadence": (50, 60)},
            6: {"reps": 5, "on_duration": 240, "on_power": 0.97, "off_duration": 240, "off_power": 0.55, "cadence": (50, 60)},
        }
    },
    "tempo": {
        "name": "Tempo",
        "levels": {
            1: {"blocks": [(900, 0.85)]},  # 2x15min
            2: {"blocks": [(900, 0.85), (900, 0.85), (900, 0.85)]},  # 3x15min
            3: {"blocks": [(900, 0.85), (900, 0.85), (900, 0.85)], "position": "alternating"},
            4: {"blocks": [(1200, 0.85), (1200, 0.85)]},  # 2x20min
            5: {"blocks": [(1500, 0.85), (1500, 0.85)]},  # 2x25min
            6: {"blocks": [(1200, 0.85), (1200, 0.85), (1200, 0.85)]},  # 3x20min
        }
    },
    "g_spot": {
        "name": "G-Spot / Sweet Spot",
        "levels": {
            1: {"blocks": [(600, 0.90)]},  # 2x10min
            2: {"blocks": [(600, 0.90), (600, 0.90), (600, 0.90)]},  # 3x10min
            3: {"blocks": [(600, 0.90), (600, 0.90), (600, 0.90)], "position": "drops"},
            4: {"blocks": [(720, 0.90), (720, 0.90)]},  # 2x12min
            5: {"blocks": [(900, 0.90), (900, 0.90)]},  # 2x15min
            6: {"blocks": [(720, 0.90), (720, 0.90), (720, 0.90)]},  # 3x12min
        }
    },
    "stomps": {
        "name": "Stomps",
        "levels": {
            1: {"reps": 4, "on_duration": 8, "on_power": 2.00, "off_duration": 120, "off_power": 0.50},
            2: {"reps": 6, "on_duration": 8, "on_power": 2.00, "off_duration": 120, "off_power": 0.50},
            3: {"reps": 6, "on_duration": 8, "on_power": 2.00, "off_duration": 120, "off_power": 0.50, "position": "standing"},
            4: {"reps": 4, "on_duration": 10, "on_power": 2.00, "off_duration": 120, "off_power": 0.50},
            5: {"reps": 6, "on_duration": 10, "on_power": 2.00, "off_duration": 120, "off_power": 0.50},
            6: {"reps": 8, "on_duration": 10, "on_power": 2.00, "off_duration": 120, "off_power": 0.50},
        }
    },
    "microbursts": {
        "name": "Microbursts",
        "levels": {
            1: {"reps": 10, "on_duration": 15, "on_power": 1.15, "off_duration": 15, "off_power": 0.50, "cadence": (100, 110)},
            2: {"reps": 15, "on_duration": 15, "on_power": 1.15, "off_duration": 15, "off_power": 0.50, "cadence": (100, 110)},
            3: {"reps": 15, "on_duration": 15, "on_power": 1.15, "off_duration": 15, "off_power": 0.50, "cadence": (100, 110)},
            4: {"reps": 12, "on_duration": 15, "on_power": 1.15, "off_duration": 15, "off_power": 0.50, "cadence": (100, 110)},
            5: {"reps": 18, "on_duration": 15, "on_power": 1.15, "off_duration": 15, "off_power": 0.50, "cadence": (100, 110)},
            6: {"reps": 20, "on_duration": 15, "on_power": 1.15, "off_duration": 15, "off_power": 0.50, "cadence": (100, 110)},
        }
    },
    "race_simulation": {
        "name": "Race Simulation",
        "levels": {
            1: {"pattern": "simple"},  # Tempo + 2-3 surges
            2: {"pattern": "extended"},  # Tempo + 4-5 surges
            3: {"pattern": "complex"},  # Tempo + threshold + VO2
            4: {"pattern": "simple"},  # Consolidation
            5: {"pattern": "extended_long"},  # Longer race sim
            6: {"pattern": "full"},  # Complete race demands
        }
    },
    "normalized_power": {
        "name": "Normalized Power / IF Target",
        "levels": {
            1: {"duration_minutes": 120, "if_target": 0.85},  # 2 hours
            2: {"duration_minutes": 150, "if_target": 0.85},  # 2.5 hours
            3: {"duration_minutes": 150, "if_target": 0.85},  # 2.5 hours
            4: {"duration_minutes": 120, "if_target": 0.85},  # 2 hours consolidation
            5: {"duration_minutes": 180, "if_target": 0.85},  # 3 hours
            6: {"duration_minutes": 180, "if_target": 0.85},  # 3 hours peak
        }
    },
    "endurance": {
        "name": "Endurance",
        "levels": {
            1: {"duration_minutes": 60, "power": 0.70},
            2: {"duration_minutes": 90, "power": 0.70},
            3: {"duration_minutes": 120, "power": 0.70},
            4: {"duration_minutes": 90, "power": 0.70},
            5: {"duration_minutes": 150, "power": 0.70},
            6: {"duration_minutes": 180, "power": 0.70},
        }
    },
    "testing": {
        "name": "FTP Test",
        "levels": {
            1: {"type": "ftp_20min"},
            2: {"type": "ftp_20min"},
            3: {"type": "ftp_20min"},
            4: {"type": "ftp_20min"},
            5: {"type": "ftp_20min"},
            6: {"type": "ftp_20min"},
        }
    },
    "rest": {
        "name": "Rest Day",
        "levels": {
            1: {"type": "rest"},
            2: {"type": "rest"},
            3: {"type": "rest"},
            4: {"type": "rest"},
            5: {"type": "rest"},
            6: {"type": "rest"},
        }
    },
}

def generate_workout_blocks(archetype: str, level: int) -> str:
    """Generate XML blocks for a workout based on archetype and level."""
    if archetype not in ARCHETYPE_PROGRESSIONS:
        return ""
    
    config = ARCHETYPE_PROGRESSIONS[archetype]["levels"][level]
    blocks = []
    
    # Warmup
    blocks.append('    <Warmup Duration="900" PowerLow="0.50" PowerHigh="0.75"/>')
    
    # Main set based on archetype
    if archetype in ["vo2_steady", "vo2_30_30", "vo2_40_20", "vo2_extended", "threshold_steady", "threshold_touch", "sfr", "stomps", "microbursts"]:
        # Interval-based workouts
        reps = config["reps"]
        on_dur = config["on_duration"]
        on_pwr = config["on_power"]
        off_dur = config.get("off_duration", 0)
        off_pwr = config.get("off_power", 0.50)
        
        cadence_attr = ""
        if "cadence" in config:
            cad_low, cad_high = config["cadence"]
            cadence_attr = f' Cadence="{cad_low}" CadenceResting="{cad_high}"'
        
        blocks.append(f'    <IntervalsT Repeat="{reps}" OnDuration="{on_dur}" OnPower="{on_pwr}" OffDuration="{off_dur}" OffPower="{off_pwr}"{cadence_attr}/>')
    
    elif archetype == "threshold_progressive":
        # Progressive threshold blocks
        for duration, power in config["blocks"]:
            blocks.append(f'    <SteadyState Duration="{duration}" Power="{power}"/>')
        if len(config["blocks"]) > 2:
            blocks.append('    <SteadyState Duration="300" Power="0.55"/>')  # Recovery between sets
    
    elif archetype == "mixed_climbing":
        # Over/under pattern
        sets = config["sets"]
        reps_per_set = config["reps_per_set"]
        under_dur = config["under_duration"]
        under_pwr = config["under_power"]
        over_dur = config["over_duration"]
        over_pwr = config["over_power"]
        
        for s in range(sets):
            for r in range(reps_per_set):
                blocks.append(f'    <SteadyState Duration="{under_dur}" Power="{under_pwr}"/>')
                blocks.append(f'    <SteadyState Duration="{over_dur}" Power="{over_pwr}"/>')
            if s < sets - 1:
                blocks.append('    <SteadyState Duration="180" Power="0.55"/>')  # Recovery
    
    elif archetype == "mixed_intervals":
        # VO2 to threshold transitions
        sets = config["sets"]
        vo2_dur = config["vo2_duration"]
        vo2_pwr = config["vo2_power"]
        thresh_dur = config["threshold_duration"]
        thresh_pwr = config["threshold_power"]
        
        for s in range(sets):
            blocks.append(f'    <SteadyState Duration="{vo2_dur}" Power="{vo2_pwr}"/>')
            blocks.append(f'    <SteadyState Duration="{thresh_dur}" Power="{thresh_pwr}"/>')
            if s < sets - 1:
                blocks.append('    <SteadyState Duration="180" Power="0.55"/>')  # Recovery
    
    elif archetype in ["tempo", "g_spot"]:
        # Steady state blocks
        for duration, power in config["blocks"]:
            blocks.append(f'    <SteadyState Duration="{duration}" Power="{power}"/>')
            if len(config["blocks"]) > 1:
                blocks.append('    <SteadyState Duration="180" Power="0.55"/>')  # Recovery
    
    elif archetype == "race_simulation":
        # Variable race pattern
        pattern = config["pattern"]
        if pattern == "simple":
            blocks.append('    <SteadyState Duration="1200" Power="0.85"/>')  # 20min tempo
            blocks.append('    <SteadyState Duration="60" Power="1.10"/>')  # Surge
            blocks.append('    <SteadyState Duration="300" Power="0.70"/>')  # Recovery
            blocks.append('    <SteadyState Duration="60" Power="1.10"/>')  # Surge
        elif pattern == "extended":
            blocks.append('    <SteadyState Duration="1200" Power="0.85"/>')  # 20min tempo
            for _ in range(4):
                blocks.append('    <SteadyState Duration="60" Power="1.10"/>')  # Surges
                blocks.append('    <SteadyState Duration="180" Power="0.70"/>')  # Recovery
        elif pattern == "complex":
            blocks.append('    <SteadyState Duration="900" Power="0.85"/>')  # Tempo
            blocks.append('    <SteadyState Duration="300" Power="1.00"/>')  # Threshold
            blocks.append('    <SteadyState Duration="120" Power="1.15"/>')  # VO2
            blocks.append('    <SteadyState Duration="300" Power="0.70"/>')  # Recovery
        elif pattern == "extended_long":
            blocks.append('    <SteadyState Duration="1800" Power="0.85"/>')  # 30min tempo
            for _ in range(5):
                blocks.append('    <SteadyState Duration="60" Power="1.10"/>')  # Surges
                blocks.append('    <SteadyState Duration="180" Power="0.70"/>')  # Recovery
        elif pattern == "full":
            blocks.append('    <SteadyState Duration="1800" Power="0.85"/>')  # 30min tempo
            blocks.append('    <SteadyState Duration="600" Power="1.00"/>')  # 10min threshold
            blocks.append('    <SteadyState Duration="180" Power="1.15"/>')  # VO2
            blocks.append('    <SteadyState Duration="300" Power="0.70"/>')  # Recovery
            blocks.append('    <SteadyState Duration="300" Power="1.00"/>')  # Threshold
            blocks.append('    <SteadyState Duration="120" Power="1.15"/>')  # VO2
    
    elif archetype == "normalized_power":
        # NP/IF target: Use SteadyState at G Spot (88-90% FTP) to simulate IF 0.85
        # This ensures proper TSS calculation in TrainingPeaks
        # IF 0.85 means NP should be 0.85 × FTP, which is achieved through variable power
        # Using steady G Spot power approximates the TSS correctly
        duration_sec = config["duration_minutes"] * 60
        blocks.append(f'    <SteadyState Duration="{duration_sec}" Power="0.90"/>')  # G Spot to approximate IF 0.85 TSS
    
    elif archetype == "endurance":
        # Long steady Z2
        duration_sec = config["duration_minutes"] * 60
        power = config["power"]
        blocks.append(f'    <SteadyState Duration="{duration_sec}" Power="{power}"/>')
    
    elif archetype == "testing":
        # FTP test structure
        blocks.append('    <SteadyState Duration="600" Power="0.70"/>')  # 10min warmup
        blocks.append('    <SteadyState Duration="300" Power="0.85"/>')  # 5min build
        blocks.append('    <SteadyState Duration="60" Power="1.20"/>')  # 1min open
        blocks.append('    <SteadyState Duration="300" Power="0.70"/>')  # 5min recovery
        blocks.append('    <SteadyState Duration="1200" Power="1.00"/>')  # 20min FTP test
    
    elif archetype == "rest":
        # Rest day - minimal activity
        blocks.append('    <SteadyState Duration="600" Power="0.50"/>')  # Optional easy spin
    
    # Cooldown
    blocks.append('    <Cooldown Duration="600" PowerLow="0.50" PowerHigh="0.65"/>')
    
    return "\n".join(blocks)

def generate_description(archetype: str, level: int) -> str:
    """Generate workout description using the workout_description_generator."""
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent / "generation_modules"))
        from workout_description_generator import generate_workout_description, detect_archetype
        
        workout_name = f"Level {level} - {ARCHETYPE_PROGRESSIONS[archetype]['name']}"
        blocks = generate_workout_blocks(archetype, level)
        
        description = generate_workout_description(
            workout_name=workout_name,
            blocks=blocks,
            week_num=level,
            level=level,
            existing_description=""
        )
        
        return description
    except Exception as e:
        print(f"  ⚠️  Error generating description for {archetype} Level {level}: {e}")
        # Fallback description
        return f"Level {level} progression of {ARCHETYPE_PROGRESSIONS[archetype]['name']}"

def create_zwo_file(archetype: str, level: int, output_dir: Path):
    """Create a ZWO file for a specific archetype and level."""
    archetype_name = ARCHETYPE_PROGRESSIONS[archetype]["name"]
    workout_name = f"Level {level} - {archetype_name}"
    
    blocks = generate_workout_blocks(archetype, level)
    description = generate_description(archetype, level)
    
    # Escape XML
    name_escaped = html.escape(workout_name, quote=False)
    desc_escaped = html.escape(description, quote=False)
    
    zwo_content = ZWO_TEMPLATE.format(
        name=name_escaped,
        description=desc_escaped,
        blocks=blocks
    )
    
    # Create filename
    archetype_slug = archetype.replace("_", "_").title().replace("_", "")
    filename = f"Level_{level}_{archetype_slug}.zwo"
    filepath = output_dir / filename
    
    filepath.write_text(zwo_content, encoding='utf-8')
    return filepath

def main():
    """Generate all archetype example files."""
    output_base = Path("/Users/mattirowe/Downloads/archetype_examples")
    output_base.mkdir(exist_ok=True)
    
    print(f"📦 Generating archetype examples...")
    print(f"   Output: {output_base}")
    
    total_files = 0
    
    for archetype in ARCHETYPE_PROGRESSIONS.keys():
        archetype_name = ARCHETYPE_PROGRESSIONS[archetype]["name"]
        archetype_dir = output_base / archetype_name.replace(" ", "_").replace("/", "_")
        archetype_dir.mkdir(exist_ok=True)
        
        print(f"\n  → {archetype_name}")
        
        for level in range(1, 7):
            try:
                filepath = create_zwo_file(archetype, level, archetype_dir)
                print(f"     ✓ Level {level}: {filepath.name}")
                total_files += 1
            except Exception as e:
                print(f"     ❌ Level {level}: Error - {e}")
    
    print(f"\n✅ Generated {total_files} archetype example files")
    print(f"   Location: {output_base}")

if __name__ == "__main__":
    main()

