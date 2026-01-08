#!/usr/bin/env python3
"""
Generate example ZWO files for all workout archetypes at all 6 progression levels.
Creates 25 archetypes × 6 levels = 150 example ZWO files.
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
            2: {"reps": 4, "on_duration": 180, "on_power": 1.10, "off_duration": 150, "off_power": 0.55},  # Less recovery
            3: {"reps": 5, "on_duration": 180, "on_power": 1.10, "off_duration": 120, "off_power": 0.55, "cadence": (100, 110)},  # Less recovery, cadence focus
            4: {"reps": 5, "on_duration": 210, "on_power": 1.10, "off_duration": 120, "off_power": 0.55},  # Longer intervals, less recovery
            5: {"reps": 6, "on_duration": 180, "on_power": 1.10, "off_duration": 90, "off_power": 0.55},  # More reps, minimal recovery
            6: {"reps": 5, "on_duration": 240, "on_power": 1.10, "off_duration": 90, "off_power": 0.55},  # Extended duration, minimal recovery
        }
    },
    "vo2_30_30": {
        "name": "VO2max 30/30",
        "levels": {
            1: {"reps": 8, "on_duration": 30, "on_power": 1.25, "off_duration": 30, "off_power": 0.50},
            2: {"reps": 10, "on_duration": 30, "on_power": 1.25, "off_duration": 25, "off_power": 0.50},  # Less recovery
            3: {"reps": 12, "on_duration": 30, "on_power": 1.25, "off_duration": 20, "off_power": 0.50, "cadence": (100, 110)},  # More reps, less recovery
            4: {"reps": 12, "on_duration": 35, "on_power": 1.25, "off_duration": 20, "off_power": 0.50},  # Longer intervals
            5: {"reps": 15, "on_duration": 30, "on_power": 1.25, "off_duration": 15, "off_power": 0.50},  # More reps, minimal recovery
            6: {"reps": 18, "on_duration": 30, "on_power": 1.25, "off_duration": 15, "off_power": 0.50},  # Peak volume
        }
    },
    "vo2_40_20": {
        "name": "VO2max 40/20",
        "levels": {
            1: {"reps": 6, "on_duration": 40, "on_power": 1.20, "off_duration": 20, "off_power": 0.50},
            2: {"reps": 8, "on_duration": 40, "on_power": 1.20, "off_duration": 15, "off_power": 0.50},  # Less recovery
            3: {"reps": 10, "on_duration": 40, "on_power": 1.20, "off_duration": 15, "off_power": 0.50, "cadence": (100, 110)},  # More reps
            4: {"reps": 10, "on_duration": 45, "on_power": 1.20, "off_duration": 15, "off_power": 0.50},  # Longer intervals
            5: {"reps": 12, "on_duration": 40, "on_power": 1.20, "off_duration": 10, "off_power": 0.50},  # Minimal recovery
            6: {"reps": 15, "on_duration": 40, "on_power": 1.20, "off_duration": 10, "off_power": 0.50},  # Peak volume
        }
    },
    "vo2_extended": {
        "name": "VO2max Extended",
        "levels": {
            1: {"reps": 2, "on_duration": 300, "on_power": 1.10, "off_duration": 300, "off_power": 0.55},
            2: {"reps": 3, "on_duration": 300, "on_power": 1.10, "off_duration": 240, "off_power": 0.55},  # Less recovery
            3: {"reps": 3, "on_duration": 360, "on_power": 1.10, "off_duration": 240, "off_power": 0.55, "cadence": (100, 110)},  # Longer intervals
            4: {"reps": 3, "on_duration": 360, "on_power": 1.10, "off_duration": 180, "off_power": 0.55},  # Less recovery
            5: {"reps": 3, "on_duration": 420, "on_power": 1.10, "off_duration": 180, "off_power": 0.55},  # Extended duration
            6: {"reps": 4, "on_duration": 360, "on_power": 1.10, "off_duration": 180, "off_power": 0.55},  # More reps
        }
    },
    "threshold_steady": {
        "name": "Threshold Steady",
        "levels": {
            1: {"reps": 2, "on_duration": 600, "on_power": 1.00, "off_duration": 300, "off_power": 0.55},
            2: {"reps": 3, "on_duration": 600, "on_power": 1.00, "off_duration": 240, "off_power": 0.55},  # Less recovery
            3: {"reps": 3, "on_duration": 720, "on_power": 1.00, "off_duration": 240, "off_power": 0.55, "position": "drops"},  # Longer intervals
            4: {"reps": 3, "on_duration": 720, "on_power": 1.00, "off_duration": 180, "off_power": 0.55},  # Less recovery
            5: {"reps": 3, "on_duration": 900, "on_power": 1.00, "off_duration": 180, "off_power": 0.55},  # Extended duration
            6: {"reps": 4, "on_duration": 720, "on_power": 1.00, "off_duration": 180, "off_power": 0.55},  # More reps
        }
    },
    "threshold_progressive": {
        "name": "Threshold Progressive",
        "levels": {
            1: {"blocks": [(600, 0.95), (600, 1.00)]},  # 2x10min building 95%→100%
            2: {"blocks": [(720, 0.95), (720, 1.02)]},  # 2x12min building 95%→102%
            3: {"blocks": [(900, 0.95), (900, 1.02)], "position": "drops"},  # 2x15min, longer
            4: {"blocks": [(900, 0.95), (900, 1.02), (600, 0.95), (600, 1.00)]},  # 4 blocks total
            5: {"blocks": [(900, 0.95), (900, 1.02), (900, 0.95), (900, 1.02)]},  # 4x15min
            6: {"blocks": [(900, 0.95), (900, 1.02), (900, 0.95), (900, 1.02), (600, 0.95), (600, 1.00)]},  # 6 blocks peak
        }
    },
    "threshold_touch": {
        "name": "Threshold Touch",
        "levels": {
            1: {"reps": 1, "on_duration": 300, "on_power": 1.00, "off_duration": 0, "off_power": 0},
            2: {"reps": 2, "on_duration": 300, "on_power": 1.00, "off_duration": 240, "off_power": 0.55},  # Less recovery
            3: {"reps": 2, "on_duration": 360, "on_power": 1.00, "off_duration": 240, "off_power": 0.55, "position": "drops"},  # Longer intervals
            4: {"reps": 3, "on_duration": 300, "on_power": 1.00, "off_duration": 180, "off_power": 0.55},  # More reps, less recovery
            5: {"reps": 3, "on_duration": 360, "on_power": 1.00, "off_duration": 180, "off_power": 0.55},  # Longer intervals
            6: {"reps": 3, "on_duration": 480, "on_power": 1.00, "off_duration": 180, "off_power": 0.55},  # Extended duration
        }
    },
    "mixed_climbing": {
        "name": "Mixed Climbing",
        "levels": {
            1: {"sets": 3, "reps_per_set": 1, "under_duration": 180, "under_power": 0.88, "over_duration": 60, "over_power": 0.98},
            2: {"sets": 4, "reps_per_set": 1, "under_duration": 180, "under_power": 0.88, "over_duration": 60, "over_power": 0.98},
            3: {"sets": 4, "reps_per_set": 2, "under_duration": 180, "under_power": 0.88, "over_duration": 60, "over_power": 0.98, "cadence": (70, 80)},  # More reps per set
            4: {"sets": 5, "reps_per_set": 2, "under_duration": 180, "under_power": 0.88, "over_duration": 60, "over_power": 0.98},  # More sets with 2 reps
            5: {"sets": 5, "reps_per_set": 2, "under_duration": 210, "under_power": 0.88, "over_duration": 75, "over_power": 0.98},  # Longer intervals
            6: {"sets": 6, "reps_per_set": 2, "under_duration": 180, "under_power": 0.88, "over_duration": 60, "over_power": 0.98},  # Peak volume
        }
    },
    "mixed_intervals": {
        "name": "Mixed Intervals",
        "levels": {
            1: {"sets": 3, "vo2_duration": 120, "vo2_power": 1.10, "threshold_duration": 180, "threshold_power": 0.98},
            2: {"sets": 4, "vo2_duration": 120, "vo2_power": 1.10, "threshold_duration": 180, "threshold_power": 0.98},
            3: {"sets": 4, "vo2_duration": 150, "vo2_power": 1.10, "threshold_duration": 210, "threshold_power": 0.98, "position": "drops"},  # Longer intervals
            4: {"sets": 5, "vo2_duration": 120, "vo2_power": 1.10, "threshold_duration": 180, "threshold_power": 0.98},  # More sets
            5: {"sets": 5, "vo2_duration": 150, "vo2_power": 1.10, "threshold_duration": 210, "threshold_power": 0.98},  # Longer intervals
            6: {"sets": 6, "vo2_duration": 150, "vo2_power": 1.10, "threshold_duration": 210, "threshold_power": 0.98},  # Peak volume
        }
    },
    "sfr": {
        "name": "SFR - Sustained Force Repetitions",
        "levels": {
            1: {"reps": 3, "on_duration": 180, "on_power": 0.97, "off_duration": 180, "off_power": 0.55, "cadence": (50, 60)},
            2: {"reps": 4, "on_duration": 180, "on_power": 0.97, "off_duration": 150, "off_power": 0.55, "cadence": (50, 60)},  # Less recovery
            3: {"reps": 5, "on_duration": 180, "on_power": 0.97, "off_duration": 120, "off_power": 0.55, "cadence": (50, 60)},  # More reps, less recovery
            4: {"reps": 5, "on_duration": 240, "on_power": 0.97, "off_duration": 120, "off_power": 0.55, "cadence": (50, 60)},  # Longer intervals
            5: {"reps": 6, "on_duration": 240, "on_power": 0.97, "off_duration": 120, "off_power": 0.55, "cadence": (50, 60)},  # More reps
            6: {"reps": 7, "on_duration": 240, "on_power": 0.97, "off_duration": 90, "off_power": 0.55, "cadence": (50, 60)},  # Peak volume, minimal recovery
        }
    },
    "tempo": {
        "name": "Tempo",
        "levels": {
            1: {"blocks": [(900, 0.85)]},  # 1x15min
            2: {"blocks": [(900, 0.85), (900, 0.85)]},  # 2x15min
            3: {"blocks": [(900, 0.85), (900, 0.85), (900, 0.85)], "position": "alternating"},  # 3x15min
            4: {"blocks": [(1200, 0.85), (1200, 0.85), (900, 0.85)]},  # 2x20min + 1x15min
            5: {"blocks": [(1200, 0.85), (1200, 0.85), (1200, 0.85)]},  # 3x20min (more total time)
            6: {"blocks": [(1500, 0.85), (1500, 0.85), (900, 0.85)]},  # 2x25min + 1x15min (peak)
        }
    },
    "g_spot": {
        "name": "G-Spot / Sweet Spot",
        "levels": {
            1: {"blocks": [(600, 0.90)]},  # 1x10min
            2: {"blocks": [(600, 0.90), (600, 0.90)]},  # 2x10min
            3: {"blocks": [(600, 0.90), (600, 0.90), (600, 0.90)], "position": "drops"},  # 3x10min
            4: {"blocks": [(720, 0.90), (720, 0.90), (600, 0.90)]},  # 2x12min + 1x10min
            5: {"blocks": [(900, 0.90), (900, 0.90), (600, 0.90)]},  # 2x15min + 1x10min (more total time)
            6: {"blocks": [(900, 0.90), (900, 0.90), (720, 0.90)]},  # 2x15min + 1x12min (peak)
        }
    },
    "stomps": {
        "name": "Stomps",
        "levels": {
            1: {"reps": 4, "on_duration": 8, "on_power": 2.00, "off_duration": 120, "off_power": 0.50},
            2: {"reps": 6, "on_duration": 8, "on_power": 2.00, "off_duration": 90, "off_power": 0.50},  # Less recovery
            3: {"reps": 6, "on_duration": 10, "on_power": 2.00, "off_duration": 90, "off_power": 0.50, "position": "standing"},  # Longer intervals
            4: {"reps": 8, "on_duration": 8, "on_power": 2.00, "off_duration": 60, "off_power": 0.50},  # More reps, less recovery
            5: {"reps": 8, "on_duration": 10, "on_power": 2.00, "off_duration": 60, "off_power": 0.50},  # Longer intervals
            6: {"reps": 10, "on_duration": 10, "on_power": 2.00, "off_duration": 60, "off_power": 0.50},  # Peak volume
        }
    },
    "microbursts": {
        "name": "Microbursts",
        "levels": {
            1: {"reps": 10, "on_duration": 15, "on_power": 1.15, "off_duration": 15, "off_power": 0.50, "cadence": (100, 110)},
            2: {"reps": 15, "on_duration": 15, "on_power": 1.15, "off_duration": 12, "off_power": 0.50, "cadence": (100, 110)},  # Less recovery
            3: {"reps": 18, "on_duration": 15, "on_power": 1.15, "off_duration": 12, "off_power": 0.50, "cadence": (100, 110)},  # More reps
            4: {"reps": 20, "on_duration": 15, "on_power": 1.15, "off_duration": 10, "off_power": 0.50, "cadence": (100, 110)},  # More reps, less recovery
            5: {"reps": 24, "on_duration": 15, "on_power": 1.15, "off_duration": 10, "off_power": 0.50, "cadence": (100, 110)},  # More reps
            6: {"reps": 30, "on_duration": 15, "on_power": 1.15, "off_duration": 8, "off_power": 0.50, "cadence": (100, 110)},  # Peak volume, minimal recovery
        }
    },
    "race_simulation": {
        "name": "Race Simulation",
        "levels": {
            1: {"pattern": "simple"},  # Tempo + 2 surges
            2: {"pattern": "extended"},  # Tempo + 4 surges
            3: {"pattern": "complex"},  # Tempo + threshold + VO2 (higher intensity)
            4: {"pattern": "extended_long"},  # Longer tempo + 5 surges (more volume)
            5: {"pattern": "complex_long"},  # Extended complex pattern
            6: {"pattern": "full"},  # Complete race demands
        }
    },
    "normalized_power": {
        "name": "Normalized Power / IF Target",
        "levels": {
            1: {"duration_minutes": 120, "if_target": 0.85},  # 2 hours
            2: {"duration_minutes": 150, "if_target": 0.85},  # 2.5 hours
            3: {"duration_minutes": 180, "if_target": 0.85},  # 3 hours
            4: {"duration_minutes": 210, "if_target": 0.85},  # 3.5 hours
            5: {"duration_minutes": 240, "if_target": 0.85},  # 4 hours
            6: {"duration_minutes": 270, "if_target": 0.85},  # 4.5 hours peak
        }
    },
    "endurance": {
        "name": "Endurance",
        "levels": {
            1: {"duration_minutes": 60, "power": 0.70},
            2: {"duration_minutes": 90, "power": 0.70},
            3: {"duration_minutes": 120, "power": 0.70},
            4: {"duration_minutes": 150, "power": 0.70},  # Progressive, not consolidation
            5: {"duration_minutes": 180, "power": 0.70},
            6: {"duration_minutes": 240, "power": 0.70},  # Peak duration
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
    # NEW ARCHETYPES
    "vo2_bookend": {
        "name": "VO2 Bookend",
        "levels": {
            1: {"vo2_reps": 1, "vo2_duration": 240, "vo2_power": 1.10, "endurance_duration": 3600, "endurance_power": 0.70},  # 1x4min VO2, 1hr Z2
            2: {"vo2_reps": 1, "vo2_duration": 240, "vo2_power": 1.10, "endurance_duration": 4800, "endurance_power": 0.70},  # 1x4min VO2, 1.3hr Z2
            3: {"vo2_reps": 2, "vo2_duration": 240, "vo2_power": 1.10, "endurance_duration": 5400, "endurance_power": 0.70},  # 2x4min VO2, 1.5hr Z2
            4: {"vo2_reps": 2, "vo2_duration": 300, "vo2_power": 1.10, "endurance_duration": 6000, "endurance_power": 0.70},  # 2x5min VO2, 1.7hr Z2
            5: {"vo2_reps": 2, "vo2_duration": 300, "vo2_power": 1.10, "endurance_duration": 7200, "endurance_power": 0.70},  # 2x5min VO2, 2hr Z2
            6: {"vo2_reps": 3, "vo2_duration": 240, "vo2_power": 1.10, "endurance_duration": 7200, "endurance_power": 0.70},  # 3x4min VO2, 2hr Z2
        }
    },
    "tempo_accelerations": {
        "name": "Tempo with Accelerations",
        "levels": {
            1: {"tempo_duration": 1800, "tempo_power": 0.80, "accel_duration": 10, "accel_power": 1.15, "accel_frequency": 180},  # 30min tempo, 10sec accel every 3min
            2: {"tempo_duration": 2400, "tempo_power": 0.80, "accel_duration": 10, "accel_power": 1.15, "accel_frequency": 180},  # 40min tempo
            3: {"tempo_duration": 2400, "tempo_power": 0.82, "accel_duration": 15, "accel_power": 1.15, "accel_frequency": 180},  # 40min tempo, 15sec accel
            4: {"tempo_duration": 3000, "tempo_power": 0.80, "accel_duration": 10, "accel_power": 1.15, "accel_frequency": 150},  # 50min tempo, more frequent
            5: {"tempo_duration": 3000, "tempo_power": 0.82, "accel_duration": 15, "accel_power": 1.15, "accel_frequency": 150},  # 50min tempo, 15sec accel
            6: {"tempo_duration": 3600, "tempo_power": 0.82, "accel_duration": 15, "accel_power": 1.15, "accel_frequency": 120},  # 60min tempo, most frequent
        }
    },
    "threshold_accumulation": {
        "name": "Threshold Accumulation",
        "levels": {
            1: {"reps": 8, "on_duration": 180, "on_power": 1.00, "off_duration": 60, "off_power": 0.70},  # 8x3min Z4, 1min Z2
            2: {"reps": 10, "on_duration": 180, "on_power": 1.00, "off_duration": 60, "off_power": 0.70},  # 10x3min
            3: {"reps": 12, "on_duration": 180, "on_power": 1.00, "off_duration": 60, "off_power": 0.70},  # 12x3min
            4: {"reps": 12, "on_duration": 210, "on_power": 1.00, "off_duration": 60, "off_power": 0.70},  # 12x3.5min
            5: {"reps": 15, "on_duration": 180, "on_power": 1.00, "off_duration": 45, "off_power": 0.70},  # 15x3min, less recovery
            6: {"reps": 15, "on_duration": 210, "on_power": 1.00, "off_duration": 45, "off_power": 0.70},  # 15x3.5min, less recovery
        }
    },
    "cadence_work": {
        "name": "Cadence Work",
        "levels": {
            1: {"reps": 4, "on_duration": 30, "on_power": 0.88, "off_duration": 300, "off_power": 0.70, "cadence": (105, 115)},  # 4x30sec high cadence, Z3 min
            2: {"reps": 6, "on_duration": 30, "on_power": 0.88, "off_duration": 240, "off_power": 0.70, "cadence": (105, 115)},  # 6x30sec
            3: {"reps": 6, "on_duration": 30, "on_power": 0.90, "off_duration": 240, "off_power": 0.70, "cadence": (105, 115)},  # Higher power
            4: {"reps": 8, "on_duration": 30, "on_power": 0.88, "off_duration": 180, "off_power": 0.70, "cadence": (105, 115)},  # 8x30sec, less recovery
            5: {"reps": 8, "on_duration": 30, "on_power": 0.90, "off_duration": 180, "off_power": 0.70, "cadence": (105, 115)},  # Higher power
            6: {"reps": 10, "on_duration": 30, "on_power": 0.90, "off_duration": 150, "off_power": 0.70, "cadence": (105, 115)},  # 10x30sec, minimal recovery
        }
    },
    "endurance_blocks": {
        "name": "Endurance Blocks",
        "levels": {
            1: {"blocks": 3, "work_duration": 1800, "work_power": 0.75, "recovery_duration": 600, "recovery_power": 0.70},  # 3x30min High Z2/Low Z3, 10min Z2
            2: {"blocks": 4, "work_duration": 1800, "work_power": 0.75, "recovery_duration": 600, "recovery_power": 0.70},  # 4x30min
            3: {"blocks": 4, "work_duration": 2100, "work_power": 0.75, "recovery_duration": 600, "recovery_power": 0.70},  # 4x35min
            4: {"blocks": 5, "work_duration": 1800, "work_power": 0.75, "recovery_duration": 600, "recovery_power": 0.70},  # 5x30min
            5: {"blocks": 5, "work_duration": 2100, "work_power": 0.75, "recovery_duration": 600, "recovery_power": 0.70},  # 5x35min
            6: {"blocks": 6, "work_duration": 1800, "work_power": 0.75, "recovery_duration": 600, "recovery_power": 0.70},  # 6x30min
        }
    },
    "blended_vo2_gspot": {
        "name": "Blended VO2max and G Spot",
        "levels": {
            1: {"warmup_z3": 300, "sets": 2, "vo2_reps": 5, "vo2_on": 30, "vo2_off": 30, "vo2_power": 1.25, "ss_duration": 600, "ss_power": 0.90, "recovery": 300},  # 2 sets: 5x30/30 VO2, 10min SS
            2: {"warmup_z3": 300, "sets": 3, "vo2_reps": 5, "vo2_on": 30, "vo2_off": 30, "vo2_power": 1.25, "ss_duration": 600, "ss_power": 0.90, "recovery": 300},  # 3 sets
            3: {"warmup_z3": 300, "sets": 3, "vo2_reps": 6, "vo2_on": 30, "vo2_off": 30, "vo2_power": 1.25, "ss_duration": 600, "ss_power": 0.90, "recovery": 300},  # 3 sets, 6 reps
            4: {"warmup_z3": 300, "sets": 3, "vo2_reps": 6, "vo2_on": 30, "vo2_off": 30, "vo2_power": 1.25, "ss_duration": 720, "ss_power": 0.90, "recovery": 300},  # Longer SS
            5: {"warmup_z3": 300, "sets": 4, "vo2_reps": 5, "vo2_on": 30, "vo2_off": 30, "vo2_power": 1.25, "ss_duration": 600, "ss_power": 0.90, "recovery": 240},  # 4 sets, less recovery
            6: {"warmup_z3": 300, "sets": 4, "vo2_reps": 6, "vo2_on": 30, "vo2_off": 30, "vo2_power": 1.25, "ss_duration": 720, "ss_power": 0.90, "recovery": 240},  # Peak volume
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
            blocks.append('    <SteadyState Duration="1200" Power="0.85"/>')  # 20min tempo
            blocks.append('    <SteadyState Duration="600" Power="1.00"/>')  # 10min threshold (longer)
            blocks.append('    <SteadyState Duration="180" Power="1.15"/>')  # 3min VO2 (longer)
            blocks.append('    <SteadyState Duration="300" Power="0.70"/>')  # Recovery
        elif pattern == "extended_long":
            blocks.append('    <SteadyState Duration="1800" Power="0.85"/>')  # 30min tempo
            for _ in range(5):
                blocks.append('    <SteadyState Duration="60" Power="1.10"/>')  # Surges
                blocks.append('    <SteadyState Duration="180" Power="0.70"/>')  # Recovery
        elif pattern == "complex_long":
            blocks.append('    <SteadyState Duration="1800" Power="0.85"/>')  # 30min tempo
            blocks.append('    <SteadyState Duration="600" Power="1.00"/>')  # 10min threshold
            blocks.append('    <SteadyState Duration="180" Power="1.15"/>')  # VO2
            blocks.append('    <SteadyState Duration="300" Power="0.70"/>')  # Recovery
            blocks.append('    <SteadyState Duration="300" Power="1.00"/>')  # Threshold
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
    
    elif archetype == "vo2_bookend":
        # VO2 intervals at start and end with long Z2 in middle
        vo2_reps = config["vo2_reps"]
        vo2_dur = config["vo2_duration"]
        vo2_pwr = config["vo2_power"]
        end_dur = config["endurance_duration"]
        end_pwr = config["endurance_power"]
        
        # First VO2 set
        blocks.append(f'    <IntervalsT Repeat="{vo2_reps}" OnDuration="{vo2_dur}" OnPower="{vo2_pwr}" OffDuration="180" OffPower="0.55"/>')
        blocks.append('    <SteadyState Duration="300" Power="0.55"/>')  # Recovery
        # Long Z2 endurance block
        blocks.append(f'    <SteadyState Duration="{end_dur}" Power="{end_pwr}"/>')
        blocks.append('    <SteadyState Duration="300" Power="0.55"/>')  # Recovery
        # Second VO2 set (bookend)
        blocks.append(f'    <IntervalsT Repeat="{vo2_reps}" OnDuration="{vo2_dur}" OnPower="{vo2_pwr}" OffDuration="180" OffPower="0.55"/>')
    
    elif archetype == "tempo_accelerations":
        # Tempo work with periodic accelerations
        tempo_dur = config["tempo_duration"]
        tempo_pwr = config["tempo_power"]
        accel_dur = config["accel_duration"]
        accel_pwr = config["accel_power"]
        accel_freq = config["accel_frequency"]  # Seconds between accelerations
        
        # Break tempo into segments with accelerations
        segments = tempo_dur // accel_freq
        for i in range(segments):
            # Tempo block
            blocks.append(f'    <SteadyState Duration="{accel_freq - accel_dur}" Power="{tempo_pwr}"/>')
            # Acceleration
            blocks.append(f'    <SteadyState Duration="{accel_dur}" Power="{accel_pwr}"/>')
    
    elif archetype == "threshold_accumulation":
        # Many short threshold intervals
        reps = config["reps"]
        on_dur = config["on_duration"]
        on_pwr = config["on_power"]
        off_dur = config["off_duration"]
        off_pwr = config["off_power"]
        
        blocks.append(f'    <IntervalsT Repeat="{reps}" OnDuration="{on_dur}" OnPower="{on_pwr}" OffDuration="{off_dur}" OffPower="{off_pwr}"/>')
    
    elif archetype == "cadence_work":
        # High cadence accelerations
        reps = config["reps"]
        on_dur = config["on_duration"]
        on_pwr = config["on_power"]
        off_dur = config["off_duration"]
        off_pwr = config["off_power"]
        cad_low, cad_high = config["cadence"]
        
        blocks.append(f'    <IntervalsT Repeat="{reps}" OnDuration="{on_dur}" OnPower="{on_pwr}" OffDuration="{off_dur}" OffPower="{off_pwr}" Cadence="{cad_low}" CadenceResting="{cad_high}"/>')
    
    elif archetype == "endurance_blocks":
        # Structured endurance blocks
        num_blocks = config["blocks"]
        work_dur = config["work_duration"]
        work_pwr = config["work_power"]
        rec_dur = config["recovery_duration"]
        rec_pwr = config["recovery_power"]
        
        for i in range(num_blocks):
            blocks.append(f'    <SteadyState Duration="{work_dur}" Power="{work_pwr}"/>')
            if i < num_blocks - 1:
                blocks.append(f'    <SteadyState Duration="{rec_dur}" Power="{rec_pwr}"/>')
    
    elif archetype == "blended_vo2_gspot":
        # 30/30 VO2 intervals with sweet spot work
        warmup_z3 = config["warmup_z3"]
        sets = config["sets"]
        vo2_reps = config["vo2_reps"]
        vo2_on = config["vo2_on"]
        vo2_off = config["vo2_off"]
        vo2_pwr = config["vo2_power"]
        ss_dur = config["ss_duration"]
        ss_pwr = config["ss_power"]
        recovery = config["recovery"]
        
        # Warmup Z3
        blocks.append(f'    <SteadyState Duration="{warmup_z3}" Power="0.85"/>')
        
        for s in range(sets):
            # 30/30 VO2 intervals
            blocks.append(f'    <IntervalsT Repeat="{vo2_reps}" OnDuration="{vo2_on}" OnPower="{vo2_pwr}" OffDuration="{vo2_off}" OffPower="0.50"/>')
            # Sweet spot block
            blocks.append(f'    <SteadyState Duration="{ss_dur}" Power="{ss_pwr}"/>')
            if s < sets - 1:
                blocks.append(f'    <SteadyState Duration="{recovery}" Power="0.55"/>')  # Recovery between sets
    
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

