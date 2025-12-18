#!/usr/bin/env python3
"""
Regression Tests for ZWO File Generation
Validates XML structure, content, and TrainingPeaks compatibility
"""

import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
import tempfile
import shutil
from strength_generator import (
    create_strength_zwo_file,
    generate_strength_workout,
    load_strength_templates,
    get_pathway_name,
    get_session_letter
)


class TestZWOGeneration(unittest.TestCase):
    """Test suite for ZWO file generation"""
    
    def setUp(self):
        """Setup test environment"""
        self.test_output_dir = Path(tempfile.mkdtemp())
        self.templates_file = Path("generation_modules/MASTER_TEMPLATES_V2_PN_FINAL.md")
        
        if not self.templates_file.exists():
            self.skipTest(f"Templates file not found: {self.templates_file}")
        
        self.templates = load_strength_templates(str(self.templates_file))
    
    def tearDown(self):
        """Cleanup test files"""
        if self.test_output_dir.exists():
            shutil.rmtree(self.test_output_dir)
    
    def test_zwo_xml_structure(self):
        """ZWO files have valid XML structure"""
        output_file = self.test_output_dir / "test_structure.zwo"
        
        create_strength_zwo_file(
            week=1,
            template_key="RED_A_PHASE1",
            description=self.templates["RED_A_PHASE1"],
            output_path=output_file
        )
        
        # Parse XML
        tree = ET.parse(output_file)
        root = tree.getroot()
        
        # Verify required elements
        assert root.tag == "workout_file", "Root tag incorrect"
        assert root.find('author') is not None, "Missing author"
        assert root.find('name') is not None, "Missing name"
        assert root.find('description') is not None, "Missing description"
        assert root.find('sportType') is not None, "Missing sportType"
        assert root.find('workout') is not None, "Missing workout block"
    
    def test_sport_type_is_bike(self):
        """sportType must be 'bike' for TrainingPeaks compatibility"""
        output_file = self.test_output_dir / "test_sporttype.zwo"
        
        create_strength_zwo_file(
            week=1,
            template_key="RED_A_PHASE1",
            description=self.templates["RED_A_PHASE1"],
            output_path=output_file
        )
        
        tree = ET.parse(output_file)
        sport_type = tree.getroot().find('sportType')
        
        assert sport_type.text == "bike", \
            f"sportType must be 'bike', got '{sport_type.text}'"
    
    def test_free_ride_block_exists(self):
        """FreeRide block exists with correct attributes"""
        output_file = self.test_output_dir / "test_freeride.zwo"
        
        create_strength_zwo_file(
            week=1,
            template_key="RED_A_PHASE1",
            description=self.templates["RED_A_PHASE1"],
            output_path=output_file
        )
        
        tree = ET.parse(output_file)
        free_ride = tree.getroot().find('workout/FreeRide')
        
        assert free_ride is not None, "Missing FreeRide block"
        assert free_ride.get('Duration') == "60", "FreeRide Duration incorrect"
        assert free_ride.get('Power') == "0.0", "FreeRide Power incorrect"
    
    def test_title_format(self):
        """Title follows correct format: W## STR: [Phase] ([Session])"""
        output_file = self.test_output_dir / "test_title.zwo"
        
        create_strength_zwo_file(
            week=8,
            template_key="YELLOW_A_HYPER",
            description=self.templates["YELLOW_A_HYPER"],
            output_path=output_file
        )
        
        tree = ET.parse(output_file)
        name = tree.getroot().find('name').text
        
        assert name.startswith("W08 STR:"), "Title missing week prefix"
        assert "Lift Heavy Sh*t" in name, "Title missing phase name"
        assert "(A)" in name, "Title missing session letter"
    
    def test_description_contains_tagline(self):
        """Description includes phase tagline"""
        output_file = self.test_output_dir / "test_tagline.zwo"
        
        create_strength_zwo_file(
            week=1,
            template_key="RED_A_PHASE1",
            description=self.templates["RED_A_PHASE1"],
            output_path=output_file
        )
        
        tree = ET.parse(output_file)
        description = tree.getroot().find('description').text
        
        assert "Movement quality before load." in description, \
            "Description missing tagline"
    
    def test_description_contains_rpe(self):
        """Description includes RPE target"""
        output_file = self.test_output_dir / "test_rpe.zwo"
        
        create_strength_zwo_file(
            week=1,
            template_key="RED_A_PHASE1",
            description=self.templates["RED_A_PHASE1"],
            output_path=output_file
        )
        
        tree = ET.parse(output_file)
        description = tree.getroot().find('description').text
        
        assert "RPE Target:" in description, "Description missing RPE target"
        assert "5-6" in description, "RPE value not found"
    
    def test_description_contains_equipment(self):
        """Description includes equipment list"""
        output_file = self.test_output_dir / "test_equipment.zwo"
        
        create_strength_zwo_file(
            week=1,
            template_key="RED_A_PHASE1",
            description=self.templates["RED_A_PHASE1"],
            output_path=output_file
        )
        
        tree = ET.parse(output_file)
        description = tree.getroot().find('description').text
        
        assert "Equipment:" in description, "Description missing equipment"
    
    def test_all_exercises_have_urls(self):
        """All exercises in description have video URLs"""
        output_file = self.test_output_dir / "test_urls.zwo"
        
        create_strength_zwo_file(
            week=1,
            template_key="RED_A_PHASE1",
            description=self.templates["RED_A_PHASE1"],
            output_path=output_file
        )
        
        tree = ET.parse(output_file)
        description = tree.getroot().find('description').text
        
        # Count exercise lines (format: Exercise Name ─ ... → URL)
        import re
        exercise_pattern = r'([A-Z][^→\n]+?)\s*─\s*[^\n]*\n\s*→\s*(https://[^\s\n]+)'
        matches = re.findall(exercise_pattern, description)
        
        assert len(matches) > 0, "No exercises found in description"
        
        for exercise_line, url in matches:
            assert url.startswith("https://"), \
                f"Exercise '{exercise_line.strip()}' missing valid URL"
            assert "vimeo.com" in url or "youtube.com" in url, \
                f"Invalid URL format: {url}"
    
    def test_unicode_characters_preserved(self):
        """Unicode characters (★, →, │) are preserved"""
        output_file = self.test_output_dir / "test_unicode.zwo"
        
        create_strength_zwo_file(
            week=1,
            template_key="RED_A_PHASE1",
            description=self.templates["RED_A_PHASE1"],
            output_path=output_file
        )
        
        # Read raw file
        with open(output_file, 'rb') as f:
            raw_content = f.read()
        
        assert b'UTF-8' in raw_content, "File should declare UTF-8 encoding"
        
        # Parse and check Unicode
        tree = ET.parse(output_file)
        description = tree.getroot().find('description').text
        
        unicode_chars = ["★", "→", "│", "─"]
        for char in unicode_chars:
            assert char in description, \
                f"Unicode character '{char}' not preserved in description"
    
    def test_filename_format(self):
        """Filenames follow correct format: W##_STR_[Phase]_[Session].zwo"""
        output_file = generate_strength_workout(
            week=8,
            day="Mon",
            template_key="YELLOW_A_HYPER",
            templates_dict=self.templates,
            output_dir=self.test_output_dir
        )
        
        expected_pattern = r'W\d{2}_STR_.+_[AB]\.zwo'
        import re
        assert re.match(expected_pattern, output_file.name), \
            f"Filename format incorrect: {output_file.name}"


if __name__ == "__main__":
    unittest.main()

