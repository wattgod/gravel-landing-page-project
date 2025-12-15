#!/usr/bin/env python3
"""
Regression Test Suite for Unified Cycling + Strength Training System

Tests phase alignment, tier variation, race customization, and calendar generation.
"""

import unittest
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "generation_modules"))

from config.phase_alignment import (
    get_strength_phase,
    get_strength_frequency,
    PHASE_ALIGNMENT,
    STRENGTH_FREQUENCY
)
from config.tier_config import get_tier, get_strength_sessions
from config.race_strength_profiles import get_race_profile, get_emphasized_exercises
from config.weekly_structure import get_weekly_template, get_strength_days
from unified_plan_generator import UnifiedPlanGenerator


class TestPhaseAlignment(unittest.TestCase):
    """Test phase alignment between cycling and strength."""
    
    def test_base_phase_alignment(self):
        """Base phases should map to Learn to Lift."""
        self.assertEqual(get_strength_phase("base_1"), "Learn to Lift")
        self.assertEqual(get_strength_phase("base_2"), "Learn to Lift")
    
    def test_build_phase_alignment(self):
        """Build phases should map to Lift Heavy Sh*t and Lift Fast."""
        self.assertEqual(get_strength_phase("build_1"), "Lift Heavy Sh*t")
        self.assertEqual(get_strength_phase("build_2"), "Lift Fast")
    
    def test_peak_phase_alignment(self):
        """Peak phase should map to Lift Fast (not heavy)."""
        self.assertEqual(get_strength_phase("peak"), "Lift Fast")
        # Critical: Should NOT be "Lift Heavy Sh*t" (no double-peaking)
        self.assertNotEqual(get_strength_phase("peak"), "Lift Heavy Sh*t")
    
    def test_taper_phase_alignment(self):
        """Taper phase should map to Don't Lose It."""
        self.assertEqual(get_strength_phase("taper"), "Don't Lose It")
    
    def test_no_double_peaking(self):
        """Verify no double-peaking: peak cycling phase should not have heavy strength."""
        peak_strength = get_strength_phase("peak")
        self.assertIn(peak_strength, ["Lift Fast", "Don't Lose It"])
        self.assertNotIn(peak_strength, ["Lift Heavy Sh*t", "Learn to Lift"])


class TestTierVariation(unittest.TestCase):
    """Test tier-based strength frequency variation."""
    
    def test_ayahuasca_frequency(self):
        """Ayahuasca should have highest frequency (strength priority)."""
        self.assertEqual(get_strength_frequency("ayahuasca", "base_1"), 3)
        self.assertEqual(get_strength_frequency("ayahuasca", "base_2"), 3)
        self.assertEqual(get_strength_frequency("ayahuasca", "build_1"), 2)
        self.assertEqual(get_strength_frequency("ayahuasca", "peak"), 2)
        self.assertEqual(get_strength_frequency("ayahuasca", "taper"), 1)
    
    def test_finisher_frequency(self):
        """Finisher should have moderate frequency."""
        self.assertEqual(get_strength_frequency("finisher", "base_1"), 2)
        self.assertEqual(get_strength_frequency("finisher", "build_1"), 2)
        self.assertEqual(get_strength_frequency("finisher", "peak"), 1)
        self.assertEqual(get_strength_frequency("finisher", "taper"), 1)
    
    def test_compete_frequency(self):
        """Compete should reduce frequency during peak cycling."""
        self.assertEqual(get_strength_frequency("compete", "base_1"), 2)
        self.assertEqual(get_strength_frequency("compete", "build_1"), 2)
        self.assertEqual(get_strength_frequency("compete", "build_2"), 1)  # Reduced
        self.assertEqual(get_strength_frequency("compete", "peak"), 1)
        self.assertEqual(get_strength_frequency("compete", "taper"), 1)
    
    def test_podium_frequency(self):
        """Podium should have lowest frequency (cycling priority)."""
        self.assertEqual(get_strength_frequency("podium", "base_1"), 2)
        self.assertEqual(get_strength_frequency("podium", "build_1"), 1)  # Early reduction
        self.assertEqual(get_strength_frequency("podium", "peak"), 1)
        self.assertEqual(get_strength_frequency("podium", "taper"), 0)  # Optional
    
    def test_frequency_scaling(self):
        """Frequency should scale: Ayahuasca >= Finisher >= Compete >= Podium."""
        phases = ["base_1", "build_1", "peak"]
        for phase in phases:
            ayahuasca = get_strength_frequency("ayahuasca", phase)
            finisher = get_strength_frequency("finisher", phase)
            compete = get_strength_frequency("compete", phase)
            podium = get_strength_frequency("podium", phase)
            
            self.assertGreaterEqual(ayahuasca, finisher, 
                f"Ayahuasca should have >= frequency than Finisher in {phase}")
            self.assertGreaterEqual(finisher, compete,
                f"Finisher should have >= frequency than Compete in {phase}")
            self.assertGreaterEqual(compete, podium,
                f"Compete should have >= frequency than Podium in {phase}")


class TestRaceProfiles(unittest.TestCase):
    """Test race-specific strength customization."""
    
    def test_unbound_200_profile(self):
        """Unbound 200 should emphasize endurance exercises."""
        profile = get_race_profile("unbound_gravel_200")
        self.assertEqual(profile["name"], "Unbound Gravel 200")
        self.assertIn("endurance", profile["primary_demands"])
        self.assertIn("hip_stability", profile["primary_demands"])
        self.assertIn("Single-Leg RDL", profile["emphasized_exercises"])
        self.assertIn("Pallof Press", profile["emphasized_exercises"])
    
    def test_leadville_profile(self):
        """Leadville should emphasize single-leg and climbing exercises."""
        profile = get_race_profile("leadville_100")
        self.assertIn("climbing_power", profile["primary_demands"])
        self.assertIn("single_leg_strength", profile["primary_demands"])
        self.assertIn("Bulgarian Split Squat", profile["emphasized_exercises"])
        self.assertIn("Heavy Deadlift", profile["de_emphasized_exercises"])
    
    def test_bwr_profile(self):
        """BWR should emphasize explosive power."""
        profile = get_race_profile("belgian_waffle_ride")
        self.assertIn("explosive_power", profile["primary_demands"])
        self.assertIn("Box Jump", profile["emphasized_exercises"])
        self.assertIn("KB Swing", profile["emphasized_exercises"])
    
    def test_default_profile(self):
        """Unknown race should return default profile."""
        profile = get_race_profile("unknown_race")
        self.assertEqual(profile["name"], "Generic Gravel")
        self.assertIn("endurance", profile["primary_demands"])
    
    def test_emphasized_exercises(self):
        """get_emphasized_exercises should return list."""
        exercises = get_emphasized_exercises("unbound_gravel_200")
        self.assertIsInstance(exercises, list)
        self.assertGreater(len(exercises), 0)


class TestWeeklyStructure(unittest.TestCase):
    """Test weekly structure and day assignments."""
    
    def test_standard_template(self):
        """Standard template should have Mon/Thu strength."""
        template = get_weekly_template("finisher", "base_1")
        self.assertEqual(template["description"], "Standard week with Tue/Sat key sessions")
        self.assertEqual(template["days"]["monday"]["am"], "strength")
        self.assertEqual(template["days"]["thursday"]["am"], "strength")
    
    def test_three_key_template(self):
        """Compete/Podium build should use three-key template."""
        template = get_weekly_template("compete", "build_1")
        self.assertIn("3 key sessions", template["description"])
        self.assertEqual(template["days"]["tuesday"]["is_key_day"], True)
        self.assertEqual(template["days"]["thursday"]["is_key_day"], True)
        self.assertEqual(template["days"]["saturday"]["is_key_day"], True)
    
    def test_strength_priority_template(self):
        """Ayahuasca should use strength-priority template."""
        template = get_weekly_template("ayahuasca", "base_1")
        self.assertEqual(template["description"], "Strength-focused week for Ayahuasca tier")
        self.assertEqual(template["days"]["monday"]["am"], "strength")
        self.assertEqual(template["days"]["wednesday"]["am"], "strength")
        self.assertEqual(template["days"]["friday"]["am"], "strength")
    
    def test_taper_template(self):
        """Taper phase should use taper template."""
        template = get_weekly_template("compete", "taper")
        self.assertEqual(template["description"], "Taper week with reduced volume")
        self.assertEqual(template["days"]["sunday"]["am"], "RACE")
    
    def test_strength_days_assignment(self):
        """Strength days should be assigned correctly."""
        # Ayahuasca base: 3x/week
        days = get_strength_days("ayahuasca", "base_1", 3)
        self.assertEqual(len(days), 3)
        self.assertIn("monday", days)
        self.assertIn("wednesday", days)
        self.assertIn("friday", days)
        
        # Finisher base: 2x/week
        days = get_strength_days("finisher", "base_1", 2)
        self.assertEqual(len(days), 2)
        self.assertIn("monday", days)
        self.assertIn("thursday", days)
        
        # Compete build: 2x/week
        days = get_strength_days("compete", "build_1", 2)
        self.assertEqual(len(days), 2)
        self.assertIn("monday", days)
        self.assertIn("thursday", days)
    
    def test_no_strength_before_key_sessions(self):
        """Strength should not be scheduled before key cycling sessions."""
        # Tuesday is key session - no strength Monday PM or Tuesday AM
        template = get_weekly_template("finisher", "base_1")
        self.assertNotEqual(template["days"]["monday"]["pm"], "strength")
        self.assertNotEqual(template["days"]["tuesday"]["am"], "strength")
        
        # Saturday is key session - no strength Friday PM or Saturday AM
        self.assertNotEqual(template["days"]["friday"]["pm"], "strength")
        self.assertNotEqual(template["days"]["saturday"]["am"], "strength")


class TestUnifiedGenerator(unittest.TestCase):
    """Test unified plan generator."""
    
    def setUp(self):
        """Set up test generator."""
        self.race_id = "unbound_gravel_200"
        self.tier_id = "compete"
        self.plan_weeks = 12
        self.race_date = "2025-06-07"
        self.race_data = {
            "race_metadata": {
                "name": "Unbound Gravel 200",
                "date": "June"
            }
        }
    
    def test_generator_initialization(self):
        """Generator should initialize correctly."""
        generator = UnifiedPlanGenerator(
            self.race_id,
            self.tier_id,
            self.plan_weeks,
            self.race_date,
            self.race_data
        )
        self.assertEqual(generator.race_id, self.race_id)
        self.assertEqual(generator.tier_id, self.tier_id)
        self.assertEqual(generator.plan_weeks, self.plan_weeks)
    
    def test_phase_schedule_building(self):
        """Phase schedule should be built correctly."""
        generator = UnifiedPlanGenerator(
            self.race_id,
            self.tier_id,
            self.plan_weeks,
            self.race_date,
            self.race_data
        )
        schedule = generator._build_phase_schedule()
        
        self.assertEqual(len(schedule), self.plan_weeks)
        
        # Check first week
        self.assertEqual(schedule[0]["week"], 1)
        self.assertEqual(schedule[0]["cycling_phase"], "base_1")
        self.assertEqual(schedule[0]["strength_phase"], "Learn to Lift")
        
        # Check last week
        self.assertEqual(schedule[-1]["week"], self.plan_weeks)
        self.assertEqual(schedule[-1]["cycling_phase"], "taper")
        self.assertEqual(schedule[-1]["strength_phase"], "Don't Lose It")
    
    def test_phase_distribution_12_week(self):
        """12-week plan should have correct phase distribution."""
        generator = UnifiedPlanGenerator(
            self.race_id,
            self.tier_id,
            12,
            self.race_date,
            self.race_data
        )
        schedule = generator._build_phase_schedule()
        
        # Count weeks per phase
        phase_counts = {}
        for week_info in schedule:
            phase = week_info["cycling_phase"]
            phase_counts[phase] = phase_counts.get(phase, 0) + 1
        
        # Expected distribution for 12-week plan
        self.assertEqual(phase_counts.get("base_1", 0), 2)
        self.assertEqual(phase_counts.get("base_2", 0), 2)
        self.assertEqual(phase_counts.get("build_1", 0), 3)
        self.assertEqual(phase_counts.get("build_2", 0), 2)
        self.assertEqual(phase_counts.get("peak", 0), 2)
        self.assertEqual(phase_counts.get("taper", 0), 1)
    
    def test_strength_phase_progression(self):
        """Strength phases should progress correctly."""
        generator = UnifiedPlanGenerator(
            self.race_id,
            self.tier_id,
            self.plan_weeks,
            self.race_date,
            self.race_data
        )
        schedule = generator._build_phase_schedule()
        
        # Track phase transitions
        phases_seen = []
        for week_info in schedule:
            strength_phase = week_info["strength_phase"]
            if strength_phase not in phases_seen:
                phases_seen.append(strength_phase)
        
        # Should see progression: Learn to Lift → Lift Heavy Sh*t → Lift Fast → Don't Lose It
        self.assertIn("Learn to Lift", phases_seen)
        self.assertIn("Lift Heavy Sh*t", phases_seen)
        self.assertIn("Lift Fast", phases_seen)
        self.assertIn("Don't Lose It", phases_seen)
        
        # Verify order (rough check - Learn to Lift should come before Lift Heavy Sh*t)
        learn_idx = phases_seen.index("Learn to Lift")
        heavy_idx = phases_seen.index("Lift Heavy Sh*t")
        fast_idx = phases_seen.index("Lift Fast")
        taper_idx = phases_seen.index("Don't Lose It")
        
        self.assertLess(learn_idx, heavy_idx)
        self.assertLess(heavy_idx, fast_idx)
        self.assertLess(fast_idx, taper_idx)
    
    def test_tier_frequency_application(self):
        """Tier-specific frequency should be applied."""
        # Test Ayahuasca (higher frequency)
        generator_aya = UnifiedPlanGenerator(
            self.race_id,
            "ayahuasca",
            self.plan_weeks,
            self.race_date,
            self.race_data
        )
        schedule_aya = generator_aya._build_phase_schedule()
        
        # Test Compete (lower frequency)
        generator_comp = UnifiedPlanGenerator(
            self.race_id,
            "compete",
            self.plan_weeks,
            self.race_date,
            self.race_data
        )
        schedule_comp = generator_comp._build_phase_schedule()
        
        # Count strength sessions
        aya_sessions = sum(w["strength_sessions"] for w in schedule_aya)
        comp_sessions = sum(w["strength_sessions"] for w in schedule_comp)
        
        # Ayahuasca should have more sessions
        self.assertGreater(aya_sessions, comp_sessions)


class TestCalendarGeneration(unittest.TestCase):
    """Test calendar generation."""
    
    def test_calendar_structure(self):
        """Calendar should have correct structure."""
        generator = UnifiedPlanGenerator(
            "unbound_gravel_200",
            "compete",
            12,
            "2025-06-07",
            {}
        )
        
        # Build a test week
        week_info = generator._build_phase_schedule()[0]
        calendar_entry = generator._build_calendar_week(week_info, [])
        
        self.assertEqual(calendar_entry["week"], 1)
        self.assertIn("cycling_phase", calendar_entry)
        self.assertIn("strength_phase", calendar_entry)
        self.assertIn("days", calendar_entry)
        self.assertEqual(len(calendar_entry["days"]), 7)  # 7 days
    
    def test_calendar_days(self):
        """Calendar should have all 7 days."""
        generator = UnifiedPlanGenerator(
            "unbound_gravel_200",
            "compete",
            12,
            "2025-06-07",
            {}
        )
        
        week_info = generator._build_phase_schedule()[0]
        calendar_entry = generator._build_calendar_week(week_info, [])
        
        day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for day in day_names:
            self.assertIn(day, calendar_entry["days"])
            self.assertIn("date", calendar_entry["days"][day])
            self.assertIn("am", calendar_entry["days"][day])
            self.assertIn("pm", calendar_entry["days"][day])


class TestIntegration(unittest.TestCase):
    """Integration tests for full system."""
    
    def test_end_to_end_generation(self):
        """Test full plan generation (without file I/O)."""
        generator = UnifiedPlanGenerator(
            "unbound_gravel_200",
            "compete",
            12,
            "2025-06-07",
            {
                "race_metadata": {
                    "name": "Unbound Gravel 200",
                    "date": "June"
                }
            }
        )
        
        schedule = generator._build_phase_schedule()
        
        # Verify schedule integrity
        self.assertEqual(len(schedule), 12)
        
        # Verify phase progression
        phases = [w["cycling_phase"] for w in schedule]
        self.assertEqual(phases[0], "base_1")
        self.assertEqual(phases[-1], "taper")
        
        # Verify strength alignment
        for week_info in schedule:
            cycling_phase = week_info["cycling_phase"]
            strength_phase = week_info["strength_phase"]
            expected_strength = get_strength_phase(cycling_phase)
            self.assertEqual(strength_phase, expected_strength,
                f"Week {week_info['week']}: {cycling_phase} should map to {expected_strength}")
        
        # Verify tier frequency
        for week_info in schedule:
            tier = generator.tier_id
            phase = week_info["cycling_phase"]
            expected_freq = get_strength_frequency(tier, phase)
            actual_freq = week_info["strength_sessions"]
            self.assertEqual(actual_freq, expected_freq,
                f"Week {week_info['week']}: {tier} {phase} should have {expected_freq} sessions")


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPhaseAlignment))
    suite.addTests(loader.loadTestsFromTestCase(TestTierVariation))
    suite.addTests(loader.loadTestsFromTestCase(TestRaceProfiles))
    suite.addTests(loader.loadTestsFromTestCase(TestWeeklyStructure))
    suite.addTests(loader.loadTestsFromTestCase(TestUnifiedGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestCalendarGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

