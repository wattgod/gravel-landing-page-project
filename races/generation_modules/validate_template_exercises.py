#!/usr/bin/env python3
"""
Validate that all exercises in templates have video URLs
"""

import re
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from exercise_lookup import get_video_url, validate_exercise_urls

def extract_exercises_from_templates(template_file: str) -> list:
    """Extract all exercise names from template file"""
    with open(template_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern: Exercise name followed by URL
    pattern = r'([A-Z][^→\n]+?)\s*─\s*[^\n]*\n\s*→\s*(https://[^\s\n]+)'
    
    exercises = set()
    matches = re.findall(pattern, content)
    
    for exercise_line, url in matches:
        # Clean exercise name
        ex_name = exercise_line.strip()
        # Remove set markers
        ex_name = re.sub(r'^[A-Z]\d+\s+', '', ex_name)
        # Remove parenthetical notes
        ex_name = re.sub(r'\s*\([^)]+\)', '', ex_name).strip()
        
        if ex_name and len(ex_name) > 3:
            exercises.add(ex_name)
    
    return sorted(exercises)

def main():
    template_file = sys.argv[1] if len(sys.argv) > 1 else "generation_modules/MASTER_TEMPLATES_V2_PN_FINAL.md"
    
    print("=" * 70)
    print("TEMPLATE EXERCISE VALIDATION")
    print("=" * 70)
    
    # Extract exercises from templates
    print(f"\n📥 Extracting exercises from: {template_file}")
    template_exercises = extract_exercises_from_templates(template_file)
    print(f"   Found {len(template_exercises)} unique exercises")
    
    # Validate URLs
    print(f"\n🔍 Validating exercise URLs...")
    results = validate_exercise_urls(template_exercises)
    
    print(f"\n📊 Results:")
    print(f"   Total exercises: {results['total']}")
    print(f"   Found URLs: {results['found']}")
    print(f"   Missing URLs: {len(results['missing'])}")
    print(f"   Coverage: {results['coverage']*100:.1f}%")
    
    if results['missing']:
        print(f"\n⚠️  Missing URLs ({len(results['missing'])}):")
        for ex in results['missing']:
            print(f"   - {ex}")
    else:
        print(f"\n✅ All exercises have video URLs!")
    
    # Show sample matches
    print(f"\n📝 Sample matches (first 10):")
    for i, ex in enumerate(template_exercises[:10]):
        url = get_video_url(ex)
        status = "✓" if url else "✗"
        source = "PN" if url and "vimeo.com" in url else "YT" if url else "NONE"
        print(f"   {status} [{source}] {ex:40s} -> {url[:50] if url else 'NOT FOUND'}")

if __name__ == "__main__":
    main()

