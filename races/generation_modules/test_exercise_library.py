#!/usr/bin/env python3
"""
Regression Tests for Exercise Video Library
Validates library structure, data integrity, and URL validity
"""

import json
import unittest
from pathlib import Path

def load_exercise_library():
    """Load exercise library JSON"""
    library_path = Path(__file__).parent / "exercise_video_library.json"
    if not library_path.exists():
        raise FileNotFoundError(f"Exercise library not found: {library_path}")
    
    with open(library_path, 'r', encoding='utf-8') as f:
        return json.load(f)


class TestExerciseLibrary(unittest.TestCase):
    """Test suite for exercise video library"""
    
    def setUp(self):
        """Load library before each test"""
        self.library = load_exercise_library()
    
    def test_library_loads(self):
        """Library JSON is valid and parseable"""
        assert self.library is not None, "Library failed to load"
        assert "exercises" in self.library, "Library missing 'exercises' key"
        assert len(self.library["exercises"]) >= 400, \
            f"Expected at least 400 exercises, got {len(self.library['exercises'])}"
    
    def test_all_exercises_have_required_fields(self):
        """Every exercise has minimum required fields"""
        required = ["name", "video_url", "category"]
        
        for ex in self.library["exercises"]:
            for field in required:
                assert field in ex, \
                    f"Missing {field} in {ex.get('name', 'UNKNOWN')}"
    
    def test_all_urls_are_valid_format(self):
        """URLs are properly formatted (vimeo or youtube)"""
        for ex in self.library["exercises"]:
            url = ex["video_url"]
            assert url.startswith("https://"), \
                f"Invalid URL format: {url} (must start with https://)"
            assert "vimeo.com" in url or "youtube.com" in url or "youtu.be" in url, \
                f"Unknown video host: {url} (must be vimeo.com or youtube.com/youtu.be)"
    
    def test_no_duplicate_exercise_names(self):
        """No exact duplicate names in library"""
        names = [ex["name"].lower() for ex in self.library["exercises"]]
        duplicates = [n for n in names if names.count(n) > 1]
        assert len(duplicates) == 0, \
            f"Duplicates found: {set(duplicates)}"
    
    def test_all_categories_are_valid(self):
        """Categories are from approved list"""
        valid_categories = {
            "squat", "hinge", "push", "pull", "core", 
            "carry", "glute", "mobility", "plyometric", "power", "other"
        }
        
        for ex in self.library["exercises"]:
            assert ex["category"] in valid_categories, \
                f"Invalid category '{ex['category']}' for {ex['name']}"


if __name__ == "__main__":
    unittest.main()

