#!/usr/bin/env python3
"""
Regression Tests for Strength Generator
Tests all functionality to catch bugs before production use
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import xml.etree.ElementTree as ET
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from strength_generator import (
    load_strength_templates,
    get_pathway_name,
    get_session_letter,
    create_strength_zwo_file,
    generate_strength_workout,
    generate_strength_workout_for_plan_week,
    generate_strength_files,
    generate_all_strength_workouts,
    PATHWAY_NAMES,
    STRENGTH_SCHEDULE
)


class TestStrengthGenerator(unittest.TestCase):
    """Test suite for strength generator"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests"""
        # Use the actual templates file
        cls.templates_file = Path("generation_modules/MASTER_TEMPLATES_V2.md")
        if not cls.templates_file.exists():
            raise FileNotFoundError(f"Templates file not found: {cls.templates_file}")
        
        # Load templates once
        cls.templates = load_strength_templates(str(cls.templates_file))
        
        # Create temporary directory for test outputs
        cls.test_output_dir = Path(tempfile.mkdtemp(prefix="strength_test_"))
        print(f"\nTest output directory: {cls.test_output_dir}")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures"""
        if cls.test_output_dir.exists():
            shutil.rmtree(cls.test_output_dir)
            print(f"\nCleaned up test directory: {cls.test_output_dir}")
    
    def test_01_template_loading(self):
        """Test that all 16 templates are loaded correctly"""
        self.assertGreater(len(self.templates), 0, "No templates loaded")
        
        expected_templates = [
            "RED_A_PHASE1", "RED_A_PHASE2", "RED_A_PHASE3",
            "RED_B_PHASE1", "RED_B_PHASE2", "RED_B_PHASE3",
            "YELLOW_A_HYPER", "YELLOW_A_MAX",
            "YELLOW_B_HYPER", "YELLOW_B_MAX",
            "GREEN_A_POWER", "GREEN_A_CONV", "GREEN_A_MAINT",
            "GREEN_B_POWER", "GREEN_B_CONV", "GREEN_B_MAINT"
        ]
        
        missing = [t for t in expected_templates if t not in self.templates]
        self.assertEqual(len(missing), 0, 
                         f"Missing templates: {missing}")
        
        # Verify each template has content
        for key in expected_templates:
            content = self.templates[key]
            self.assertGreater(len(content), 100, 
                             f"Template {key} too short ({len(content)} chars)")
            self.assertIn("STRENGTH:", content,
                         f"Template {key} missing 'STRENGTH:' marker")
    
    def test_02_pathway_name_mapping(self):
        """Test pathway name extraction"""
        test_cases = [
            ("RED_A_PHASE1", "Learn to Lift"),
            ("RED_B_PHASE2", "Learn to Lift"),
            ("YELLOW_A_HYPER", "Lift Heavy Sh*t"),
            ("YELLOW_B_MAX", "Lift Heavy Sh*t"),
            ("GREEN_A_POWER", "Lift Fast"),
            ("GREEN_B_CONV", "Lift Fast"),
            ("GREEN_A_MAINT", "Don't Lose It"),  # Critical: maintenance weeks
            ("GREEN_B_MAINT", "Don't Lose It"),  # Critical: maintenance weeks
        ]
        
        for template_key, expected_name in test_cases:
            actual = get_pathway_name(template_key)
            self.assertEqual(actual, expected_name,
                           f"Pathway name mismatch for {template_key}: "
                           f"expected '{expected_name}', got '{actual}'")
    
    def test_03_session_letter_extraction(self):
        """Test session letter (A/B) extraction"""
        test_cases = [
            ("RED_A_PHASE1", "A"),
            ("RED_B_PHASE1", "B"),
            ("YELLOW_A_HYPER", "A"),
            ("YELLOW_B_HYPER", "B"),
            ("GREEN_A_MAINT", "A"),
            ("GREEN_B_MAINT", "B"),
        ]
        
        for template_key, expected_session in test_cases:
            actual = get_session_letter(template_key)
            self.assertEqual(actual, expected_session,
                           f"Session letter mismatch for {template_key}: "
                           f"expected '{expected_session}', got '{actual}'")
    
    def test_04_zwo_file_structure(self):
        """Test that generated ZWO files have correct XML structure"""
        output_file = self.test_output_dir / "test_structure.zwo"
        
        create_strength_zwo_file(
            week=1,
            template_key="RED_A_PHASE1",
            description=self.templates["RED_A_PHASE1"],
            output_path=output_file,
            plan_weeks=20
        )
        
        self.assertTrue(output_file.exists(), "ZWO file not created")
        
        # Parse XML
        tree = ET.parse(output_file)
        root = tree.getroot()
        
        # Verify structure
        self.assertEqual(root.tag, "workout_file", "Root tag incorrect")
        self.assertIsNotNone(root.find('author'), "Missing author")
        self.assertIsNotNone(root.find('name'), "Missing name")
        self.assertIsNotNone(root.find('description'), "Missing description")
        
        sport_type = root.find('sportType')
        self.assertIsNotNone(sport_type, "Missing sportType")
        self.assertEqual(sport_type.text, "bike", "sportType must be 'bike'")
        
        workout = root.find('workout')
        self.assertIsNotNone(workout, "Missing workout block")
        
        free_ride = workout.find('FreeRide')
        self.assertIsNotNone(free_ride, "Missing FreeRide block")
        # Duration should be conservative estimate (40-60 min = 2400-3600 seconds)
        duration = int(free_ride.get('Duration'))
        self.assertGreaterEqual(duration, 2400, "Duration too short (should be >= 40 min)")
        self.assertLessEqual(duration, 3600, "Duration too long (should be <= 60 min)")
        self.assertEqual(free_ride.get('Power'), "0.0", "FreeRide Power incorrect")
    
    def test_05_zwo_file_content(self):
        """Test that ZWO file content is correct"""
        output_file = self.test_output_dir / "test_content.zwo"
        
        create_strength_zwo_file(
            week=1,
            template_key="RED_A_PHASE1",
            description=self.templates["RED_A_PHASE1"],
            output_path=output_file,
            plan_weeks=20
        )
        
        tree = ET.parse(output_file)
        root = tree.getroot()
        
        # Check title
        name = root.find('name').text
        self.assertIn("W01 STR:", name, "Title missing week prefix")
        self.assertIn("Learn to Lift", name, "Title missing pathway name")
        self.assertIn("(A)", name, "Title missing session letter")
        
        # Check description
        description = root.find('description').text
        self.assertIn("STRENGTH:", description, "Description missing STRENGTH marker")
        self.assertIn("Learn to Lift", description, "Description missing pathway")
        # Check for URLs (can be vimeo.com or youtube.com)
        self.assertIn("https://", description, "Description missing URLs")
        # Check for duration in description
        self.assertIn("Duration:", description, "Description missing duration")
        
        # Check Unicode characters are preserved
        self.assertIn("★", description, "Unicode star (★) not preserved")
        self.assertIn("→", description, "Unicode arrow (→) not preserved")
        self.assertIn("│", description, "Unicode pipe (│) not preserved")
    
    def test_06_12_week_plan_mapping(self):
        """
        Test 12-week plan week mapping logic
        
        CRITICAL: This test verifies the compressed mapping, NOT the 20-week schedule.
        
        Expected mapping (compressed, starts at Yellow):
        | Plan Week | Template        | Pathway        |
        |-----------|-----------------|----------------|
        | 1-3       | YELLOW_A/B_HYPER| Lift Heavy Sh*t|
        | 4-6       | YELLOW_A/B_MAX | Lift Heavy Sh*t|
        | 7-10      | GREEN_A/B_POWER | Lift Fast |
        | 11-12     | GREEN_A/B_CONV  | Lift Fast |
        
        This is NOT pulling weeks 7-12 from the 20-week schedule (which would be
        YELLOW → GREEN_POWER only). Instead, it compresses the full progression
        starting at Yellow for week 1.
        """
        # This is the critical bug fix - verify weeks 1-12 all get templates
        plan_info = {"weeks": 12}
        output_dir = self.test_output_dir / "12week_test"
        
        count = generate_strength_files(
            plan_info,
            output_dir,
            str(self.templates_file)
        )
        
        # Should generate 24 files (12 weeks × 2 sessions)
        self.assertEqual(count, 24, 
                         f"Expected 24 files for 12-week plan, got {count}")
        
        # Verify week mapping
        workouts_dir = output_dir / "workouts"
        self.assertTrue(workouts_dir.exists(), "Workouts directory not created")
        
        # Check specific weeks - verify compressed mapping
        week_checks = {
            1: ("YELLOW_A_HYPER", "Lift Heavy Sh*t"),  # Weeks 1-3: YELLOW_HYPER
            3: ("YELLOW_A_HYPER", "Lift Heavy Sh*t"),  # Weeks 1-3: YELLOW_HYPER
            4: ("YELLOW_A_MAX", "Lift Heavy Sh*t"),    # Weeks 4-6: YELLOW_MAX
            6: ("YELLOW_A_MAX", "Lift Heavy Sh*t"),    # Weeks 4-6: YELLOW_MAX
            7: ("GREEN_A_POWER", "Lift Fast"),     # Weeks 7-10: GREEN_POWER
            10: ("GREEN_A_POWER", "Lift Fast"),    # Weeks 7-10: GREEN_POWER
            11: ("GREEN_A_CONV", "Lift Fast"),     # Weeks 11-12: GREEN_CONV
            12: ("GREEN_A_CONV", "Lift Fast"),     # Weeks 11-12: GREEN_CONV
        }
        
        for week, (expected_template, expected_pathway) in week_checks.items():
            file_a = workouts_dir / f"W{week:02d}_STR_{expected_pathway.replace(' ', '_')}_A.zwo"
            self.assertTrue(file_a.exists(), 
                          f"Week {week} Session A file missing: {file_a.name}")
            
            # Verify content
            tree = ET.parse(file_a)
            root = tree.getroot()
            desc = root.find('description').text
            
            # Check template content
            if "HYPER" in expected_template:
                self.assertIn("Hypertrophy", desc, 
                             f"Week {week} should use HYPER template")
            elif "MAX" in expected_template:
                self.assertIn("Max Strength", desc,
                             f"Week {week} should use MAX template")
            elif "POWER" in expected_template:
                self.assertIn("Power", desc,
                             f"Week {week} should use POWER template")
            elif "CONV" in expected_template:
                self.assertIn("Conversion", desc,
                             f"Week {week} should use CONV template")
    
    def test_07_20_week_plan_generation(self):
        """Test 20-week plan generates all weeks correctly"""
        plan_info = {"weeks": 20}
        output_dir = self.test_output_dir / "20week_test"
        
        count = generate_strength_files(
            plan_info,
            output_dir,
            str(self.templates_file)
        )
        
        # Should generate 38 files (weeks 1-18 have 2 sessions, weeks 19-20 have 1 each)
        self.assertEqual(count, 38,
                         f"Expected 38 files for 20-week plan, got {count}")
        
        workouts_dir = output_dir / "workouts"
        
        # Verify week 1 (RED -> Learn to Lift)
        week1_file = workouts_dir / "W01_STR_Learn_to_Lift_A.zwo"
        self.assertTrue(week1_file.exists(), "Week 1 file missing")
        
        tree = ET.parse(week1_file)
        desc = tree.getroot().find('description').text
        self.assertIn("Learn to Lift", desc, "Week 1 should be Learn to Lift")
        
        # Verify week 7 (YELLOW -> Lift Heavy Sh*t)
        week7_file = workouts_dir / "W07_STR_Lift_Heavy_Sh*t_A.zwo"
        self.assertTrue(week7_file.exists(), "Week 7 file missing")
        
        tree = ET.parse(week7_file)
        desc = tree.getroot().find('description').text
        self.assertIn("Lift Heavy Sh*t", desc, "Week 7 should be Lift Heavy Sh*t")
        
        # Verify week 19 (GREEN_MAINT -> Don't Lose It)
        week19_file = workouts_dir / "W19_STR_Don't_Lose_It_A.zwo"
        self.assertTrue(week19_file.exists(), "Week 19 file missing")
        
        tree = ET.parse(week19_file)
        name = tree.getroot().find('name').text
        self.assertIn("Don't Lose It", name, "Week 19 should be 'Don't Lose It'")
        
        # Verify week 20 (GREEN_MAINT -> Don't Lose It)
        week20_file = workouts_dir / "W20_STR_Don't_Lose_It_B.zwo"
        self.assertTrue(week20_file.exists(), "Week 20 file missing")
        
        tree = ET.parse(week20_file)
        name = tree.getroot().find('name').text
        self.assertIn("Don't Lose It", name, "Week 20 should be 'Don't Lose It'")
    
    def test_08_6_week_plan_skips_strength(self):
        """Test that 6-week plans skip strength generation"""
        plan_info = {"weeks": 6}
        output_dir = self.test_output_dir / "6week_test"
        
        count = generate_strength_files(
            plan_info,
            output_dir,
            str(self.templates_file)
        )
        
        self.assertEqual(count, 0,
                         f"6-week plan should skip strength, but generated {count} files")
    
    def test_09_filename_format(self):
        """Test that filenames follow correct format"""
        # Use generate_strength_workout which creates the filename automatically
        output_file = generate_strength_workout(
            week=8,
            day="Mon",
            template_key="YELLOW_A_HYPER",
            templates_dict=self.templates,
            output_dir=self.test_output_dir
        )
        
        # Filename should be: W08_STR_Lift_Heavy_Sh*t_A.zwo
        expected_name = "W08_STR_Lift_Heavy_Sh*t_A.zwo"
        self.assertEqual(output_file.name, expected_name,
                        f"Filename incorrect: expected '{expected_name}', got '{output_file.name}'")
        
        # Also verify the title inside matches
        tree = ET.parse(output_file)
        name = tree.getroot().find('name').text
        self.assertIn("W08 STR:", name, "Title should include week number")
        self.assertIn("Lift Heavy Sh*t", name, "Title should include pathway name")
        self.assertIn("(A)", name, "Title should include session letter")
    
    def test_10_url_preservation(self):
        """Test that URLs are preserved in descriptions"""
        output_file = self.test_output_dir / "test_urls.zwo"
        
        create_strength_zwo_file(
            week=1,
            template_key="RED_A_PHASE1",
            description=self.templates["RED_A_PHASE1"],
            output_path=output_file,
            plan_weeks=20
        )
        
        tree = ET.parse(output_file)
        description = tree.getroot().find('description').text
        
        # Check for YouTube URLs
        self.assertIn("https://www.youtube.com", description,
                     "YouTube URLs not preserved")
        
        # Check URLs are not HTML-escaped (they should be clickable)
        # URLs should appear as plain text in the description
        url_count = description.count("https://www.youtube.com")
        self.assertGreater(url_count, 0,
                          f"Expected at least 1 YouTube URL, found {url_count}")
    
    def test_11_unicode_preservation(self):
        """Test that Unicode characters are preserved correctly"""
        output_file = self.test_output_dir / "test_unicode.zwo"
        
        create_strength_zwo_file(
            week=1,
            template_key="RED_A_PHASE1",
            description=self.templates["RED_A_PHASE1"],
            output_path=output_file,
            plan_weeks=20
        )
        
        # Read raw file to check encoding
        with open(output_file, 'rb') as f:
            raw_content = f.read()
        
        # Should be UTF-8
        self.assertIn(b'UTF-8', raw_content, "File should declare UTF-8 encoding")
        
        # Parse and check Unicode characters
        tree = ET.parse(output_file)
        description = tree.getroot().find('description').text
        
        unicode_chars = {
            "★": "star",
            "→": "arrow",
            "│": "pipe",
            "─": "em dash"
        }
        
        for char, name in unicode_chars.items():
            self.assertIn(char, description,
                         f"Unicode character {name} ({char}) not preserved")
    
    def test_12_all_weeks_have_files_12week(self):
        """Regression test: Ensure all 12 weeks generate files"""
        plan_info = {"weeks": 12}
        output_dir = self.test_output_dir / "12week_complete"
        
        count = generate_strength_files(
            plan_info,
            output_dir,
            str(self.templates_file)
        )
        
        workouts_dir = output_dir / "workouts"
        
        # Check every week has both A and B sessions
        for week in range(1, 13):
            # Find files for this week
            week_files = list(workouts_dir.glob(f"W{week:02d}_STR_*.zwo"))
            self.assertEqual(len(week_files), 2,
                           f"Week {week} should have 2 files (A and B), found {len(week_files)}")
            
            # Verify one is A and one is B
            has_a = any("_A.zwo" in f.name for f in week_files)
            has_b = any("_B.zwo" in f.name for f in week_files)
            self.assertTrue(has_a, f"Week {week} missing Session A file")
            self.assertTrue(has_b, f"Week {week} missing Session B file")
    
    def test_13_duration_estimation(self):
        """Test that duration is estimated conservatively"""
        output_file = self.test_output_dir / "test_duration.zwo"
        
        create_strength_zwo_file(
            week=1,
            template_key="RED_A_PHASE1",
            description=self.templates["RED_A_PHASE1"],
            output_path=output_file,
            plan_weeks=20
        )
        
        tree = ET.parse(output_file)
        free_ride = tree.getroot().find('workout/FreeRide')
        duration_sec = int(free_ride.get('Duration'))
        duration_min = duration_sec // 60
        
        # Should be conservative (40-60 min)
        self.assertGreaterEqual(duration_min, 40, "Duration too short")
        self.assertLessEqual(duration_min, 60, "Duration too long")
        
        # Check description has duration
        desc = tree.getroot().find('description').text
        self.assertIn("Duration:", desc, "Description missing duration")
        self.assertIn(f"~{duration_min} min", desc, "Description duration doesn't match FreeRide")
    
    def test_14_urls_in_all_exercises(self):
        """Test that all exercises have video URLs"""
        output_file = self.test_output_dir / "test_urls.zwo"
        
        create_strength_zwo_file(
            week=1,
            template_key="RED_A_PHASE1",
            description=self.templates["RED_A_PHASE1"],
            output_path=output_file,
            plan_weeks=20
        )
        
        tree = ET.parse(output_file)
        desc = tree.getroot().find('description').text
        
        # Count exercise lines with URLs
        import re
        exercise_pattern = r'•\s*[^→\n]+?─\s*[^\n]*\n\s*→\s*(https://[^\s\n]+)'
        url_matches = re.findall(exercise_pattern, desc)
        
        # Should have URLs for warmup/cooldown exercises
        self.assertGreater(len(url_matches), 5, "Not enough exercise URLs found")
        
        # All URLs should be valid
        for url in url_matches:
            self.assertTrue(url.startswith("https://"), f"Invalid URL: {url}")
            self.assertTrue("vimeo.com" in url or "youtube.com" in url, f"Unknown video host: {url}")
    
    def test_15_workout_context(self):
        """Test that workout context is added when appropriate"""
        # Week 7 should have context (transition from RED to YELLOW)
        output_file = self.test_output_dir / "test_context.zwo"
        
        create_strength_zwo_file(
            week=7,
            template_key="YELLOW_A_HYPER",
            description=self.templates["YELLOW_A_HYPER"],
            output_path=output_file,
            plan_weeks=20
        )
        
        tree = ET.parse(output_file)
        desc = tree.getroot().find('description').text
        
        # Should have context about previous workout
        has_context = ("Building on" in desc or "Continuing" in desc or "Next week" in desc)
        self.assertTrue(has_context, "Workout context missing")


def run_tests():
    """Run all tests and print summary"""
    print("=" * 70)
    print("STRENGTH GENERATOR REGRESSION TESTS")
    print("=" * 70)
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestStrengthGenerator)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED")
    else:
        print(f"❌ TESTS FAILED: {len(result.failures)} failures, {len(result.errors)} errors")
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}")
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

