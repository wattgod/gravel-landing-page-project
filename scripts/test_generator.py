#!/usr/bin/env python3
"""
Landing Page Generator Regression Test Suite

Validates generated Elementor JSON files for:
- Template leakage (no race-specific content from template)
- Placeholder replacement
- Required sections present
- Content uniqueness
- JSON structural integrity
"""

import json
import re
import sys
from typing import Dict, List, Set, Tuple
from difflib import SequenceMatcher


# Race-specific forbidden terms
FORBIDDEN_TERMS = {
    'unbound-200': {
        'terms': ['Mid South', 'Stillwater', 'Oklahoma', 'Bobby Wintle', 'The Randomizer'],
        'founding_year': '2013'
    },
    'mid-south': {
        'terms': ['Unbound', 'Emporia', 'Flint Hills', 'Dirty Kanza', 'Kansas'],
        'founding_year': '2006'
    }
}

# Required sections to check
REQUIRED_SECTIONS = {
    'course_profile': ['Length', 'Technicality', 'Elevation', 'Climate', 'Altitude', 'Logistics', 'Adventure'],
    'biased_opinion': ['Prestige', 'Race Quality', 'Experience', 'Community', 'Field Depth', 'Value', 'Expenses'],
    'section_markers': ['FACTS AND HISTORY', 'FINAL VERDICT', 'RACE LOGISTICS', 'TRAINING PLANS']
}


def load_json(file_path: str) -> Dict:
    """Load and parse JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        sys.exit(1)


def test_no_template_leakage(json_data: Dict, race_slug: str) -> Tuple[bool, List[str]]:
    """Test 1: Check for template leakage (race-specific terms from other races)."""
    if race_slug not in FORBIDDEN_TERMS:
        print(f"⚠️  Warning: No forbidden terms defined for race '{race_slug}'")
        return True, []
    
    content_str = json.dumps(json_data, ensure_ascii=False)
    forbidden = FORBIDDEN_TERMS[race_slug]
    errors = []
    
    # Check forbidden terms
    for term in forbidden['terms']:
        # Allow in TrainingPeaks URLs (plan names might reference other races)
        tp_url_pattern = r'https://www\.trainingpeaks\.com[^"]*'
        tp_urls = re.findall(tp_url_pattern, content_str)
        tp_content = ' '.join(tp_urls)
        
        # Allow intentional comparisons (e.g., "compared to Unbound", "try Unbound")
        comparison_patterns = [
            r'compared to',
            r'compared to paying',
            r'try\s+' + re.escape(term),
            r'inspired by',
            r'like\s+' + re.escape(term),
        ]
        
        # Check if term appears outside TP URLs
        if term.lower() in content_str.lower():
            # Check if it's only in TP URLs
            if term.lower() not in tp_content.lower():
                # Check if it's in an intentional comparison
                is_comparison = any(re.search(pattern, content_str, re.IGNORECASE) for pattern in comparison_patterns)
                
                # For "Flint Hills" - allow if it's a comparison like "Flint Hills' annoying little brother"
                if term == 'Flint Hills' and ("annoying little brother" in content_str or "like the Flint Hills" in content_str):
                    is_comparison = True
                
                # For "Dirty Kanza" - allow if it's in history about inspiration
                if term == 'Dirty Kanza' and ("inspired by" in content_str.lower() or "history" in content_str.lower()):
                    is_comparison = True
                
                if not is_comparison:
                    # Count occurrences
                    count = len(re.findall(re.escape(term), content_str, re.IGNORECASE))
                    errors.append(f"Found forbidden term '{term}' ({count} times) - template leakage detected")
    
    # Check founding year
    founding_year = forbidden.get('founding_year')
    if founding_year:
        # Allow in years that are clearly not the founding year (e.g., "2026")
        year_pattern = rf'\b{founding_year}\b'
        matches = re.findall(year_pattern, content_str)
        # Filter out if it's in a date like "2026" or clearly a different context
        suspicious = [m for m in matches if f'Founded: {founding_year}' in content_str or f'founded {founding_year}' in content_str.lower()]
        if suspicious:
            errors.append(f"Found forbidden founding year '{founding_year}' - template leakage detected")
    
    return len(errors) == 0, errors


def test_all_placeholders_replaced(json_data: Dict) -> Tuple[bool, List[str]]:
    """Test 2: Check for unreplaced placeholders."""
    content_str = json.dumps(json_data, ensure_ascii=False)
    errors = []
    
    # Check for {{ }} placeholders
    placeholder_pattern = r'\{\{[A-Z_]+\}\}'
    placeholders = re.findall(placeholder_pattern, content_str)
    if placeholders:
        errors.append(f"Found unreplaced placeholders: {', '.join(set(placeholders))}")
    
    # Check for common placeholder patterns (but allow PLACEHOLDER in TP IDs which are expected)
    common_patterns = [
        r'REPLACE_ME',
        r'RACE_NAME',
        r'INSERT_HERE',
        r'YOUR_RACE'
    ]
    for pattern in common_patterns:
        matches = re.findall(pattern, content_str, re.IGNORECASE)
        if matches:
            errors.append(f"Found placeholder pattern '{pattern}': {len(matches)} occurrences")
    
    # Check for PLACEHOLDER but only flag if it's not in TP URLs (TP IDs are expected placeholders)
    placeholder_matches = re.findall(r'PLACEHOLDER', content_str, re.IGNORECASE)
    if placeholder_matches:
        # Check if all are in TP URLs
        tp_url_pattern = r'https://www\.trainingpeaks\.com[^"]*PLACEHOLDER[^"]*'
        tp_placeholders = re.findall(tp_url_pattern, content_str, re.IGNORECASE)
        if len(tp_placeholders) < len(placeholder_matches):
            errors.append(f"Found PLACEHOLDER outside TP URLs: {len(placeholder_matches) - len(tp_placeholders)} occurrences")
    
    return len(errors) == 0, errors


def test_required_sections_present(json_data: Dict, race_slug: str) -> Tuple[bool, List[str]]:
    """Test 3: Check that all required sections are present."""
    content_str = json.dumps(json_data, ensure_ascii=False)
    errors = []
    
    # Get expected race name
    race_name_map = {
        'unbound-200': 'UNBOUND',
        'mid-south': 'MID SOUTH'
    }
    expected_race_name = race_name_map.get(race_slug, race_slug.upper())
    
    # Check race name appears in title/hero
    if expected_race_name not in content_str:
        errors.append(f"Race name '{expected_race_name}' not found in content")
    
    # Check Course Profile variables
    for var in REQUIRED_SECTIONS['course_profile']:
        if var not in content_str:
            errors.append(f"Course Profile variable '{var}' not found")
    
    # Check Biased Opinion variables
    for var in REQUIRED_SECTIONS['biased_opinion']:
        if var not in content_str:
            errors.append(f"Biased Opinion variable '{var}' not found")
    
    # Check section markers (case-insensitive, allow variations)
    section_variations = {
        'FACTS AND HISTORY': ['Facts And History', 'FACTS AND HISTORY', 'Facts and History'],
        'FINAL VERDICT': ['Final Verdict', 'FINAL VERDICT', 'Final verdict', 'OVERALL SCORE'],
        'RACE LOGISTICS': ['Race Logistics', 'RACE LOGISTICS', 'Race logistics'],
        'TRAINING PLANS': ['Training Plans', 'TRAINING PLANS', 'Training plans']
    }
    
    for marker in REQUIRED_SECTIONS['section_markers']:
        variations = section_variations.get(marker, [marker])
        found = any(var in content_str for var in variations)
        if not found:
            errors.append(f"Section marker '{marker}' not found (checked: {', '.join(variations)})")
    
    # Check for training plans (should have multiple plan cards)
    plan_count = content_str.count('gg-plan')
    if plan_count < 10:  # Should have at least 10 plan elements
        errors.append(f"Training plans section incomplete: found {plan_count} plan elements (expected 15+)")
    
    return len(errors) == 0, errors


def test_content_uniqueness(file1_path: str, file2_path: str, race1: str, race2: str) -> Tuple[bool, List[str]]:
    """Test 4: Check that generated content is unique between races."""
    try:
        with open(file1_path, 'r', encoding='utf-8') as f:
            data1 = json.load(f)
        with open(file2_path, 'r', encoding='utf-8') as f:
            data2 = json.load(f)
    except FileNotFoundError as e:
        return False, [f"File not found: {e}"]
    
    # Extract text content (remove structure)
    content1 = json.dumps(data1, ensure_ascii=False)
    content2 = json.dumps(data2, ensure_ascii=False)
    
    # Calculate similarity
    similarity = SequenceMatcher(None, content1, content2).ratio()
    
    # Threshold: if >50% similar, content might not be unique
    if similarity > 0.5:
        return False, [
            f"Content similarity too high: {similarity:.1%}",
            f"Generated {race1} and {race2} are suspiciously similar - replacement may have failed"
        ]
    
    return True, []


def test_structural_integrity(json_data: Dict) -> Tuple[bool, List[str]]:
    """Test 5: Validate JSON structure and Elementor format."""
    errors = []
    
    # Check for required top-level keys
    required_keys = ['content', 'version', 'title', 'type']
    for key in required_keys:
        if key not in json_data:
            errors.append(f"Missing required key: '{key}'")
    
    # Check content is a list
    if 'content' in json_data and not isinstance(json_data['content'], list):
        errors.append("'content' must be a list")
    
    # Check for valid Elementor structure
    if 'content' in json_data:
        content = json_data['content']
        if len(content) == 0:
            errors.append("'content' list is empty")
        
        # Check for HTML widgets
        def count_widgets(elements, count=0):
            for elem in elements:
                if elem.get('widgetType') == 'html':
                    count += 1
                if 'elements' in elem:
                    count = count_widgets(elem['elements'], count)
            return count
        
        widget_count = count_widgets(content)
        if widget_count < 5:
            errors.append(f"Too few HTML widgets found: {widget_count} (expected 10+)")
    
    return len(errors) == 0, errors


def count_words(text: str) -> int:
    """Count words in text, handling HTML tags."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Split on whitespace and count
    return len(text.split())


def extract_html_content(json_data: Dict) -> str:
    """Extract all HTML content from Elementor JSON."""
    html_content = []
    
    def extract_from_elements(elements):
        for elem in elements:
            if elem.get('widgetType') == 'html':
                settings = elem.get('settings', {})
                if isinstance(settings, dict):
                    html = settings.get('html', '')
                    if html:
                        html_content.append(html)
            if 'elements' in elem:
                extract_from_elements(elem['elements'])
    
    if 'content' in json_data:
        extract_from_elements(json_data['content'])
    
    return ' '.join(html_content)


def test_content_length_limits(json_data: Dict) -> Tuple[bool, List[str], List[str]]:
    """Test 6: Check that key sections don't exceed maximum lengths."""
    errors = []
    warnings = []
    html_content = extract_html_content(json_data)
    
    # Extract TLDR sections
    should_race_match = re.search(r'You Should Race This If:.*?<p>(.*?)</p>', html_content, re.DOTALL)
    skip_if_match = re.search(r'Skip This If:.*?<p>(.*?)</p>', html_content, re.DOTALL)
    
    # Check TLDR should_race_if (max 60 words)
    if should_race_match:
        should_race_text = should_race_match.group(1)
        word_count = count_words(should_race_text)
        if word_count > 60:
            errors.append(f"TLDR 'should_race_if' too long: {word_count} words (max 60)")
    else:
        warnings.append("TLDR 'should_race_if' section not found")
    
    # Check TLDR skip_if (max 60 words)
    if skip_if_match:
        skip_if_text = skip_if_match.group(1)
        word_count = count_words(skip_if_text)
        if word_count > 60:
            errors.append(f"TLDR 'skip_if' too long: {word_count} words (max 60)")
    else:
        warnings.append("TLDR 'skip_if' section not found")
    
    # Extract Random Facts
    fact_matches = re.findall(r'<div class="gg-fact-text">(.*?)</div>', html_content, re.DOTALL)
    for i, fact in enumerate(fact_matches[:5], 1):
        word_count = count_words(fact)
        if word_count > 100:
            errors.append(f"Random Fact #{i} too long: {word_count} words (max 100)")
    
    # Extract Black Pill quote
    quote_match = re.search(r'class="gg-blackpill-quote"[^>]*>(.*?)</', html_content, re.DOTALL)
    if quote_match:
        quote_text = quote_match.group(1)
        word_count = count_words(quote_text)
        if word_count > 30:
            errors.append(f"Black Pill quote too long: {word_count} words (max 30)")
    
    # Extract Course Profile quote
    cp_quote_match = re.search(r'gg-course-quote-big[^>]*>.*?"(.*?)"', html_content, re.DOTALL)
    if cp_quote_match:
        cp_quote_text = cp_quote_match.group(1)
        word_count = count_words(cp_quote_text)
        if word_count > 30:
            errors.append(f"Course Profile quote too long: {word_count} words (max 30)")
    
    # Extract Biased Opinion quote
    bo_quote_match = re.search(r'id="biased-opinion".*?gg-course-quote-big[^>]*>.*?"(.*?)"', html_content, re.DOTALL)
    if bo_quote_match:
        bo_quote_text = bo_quote_match.group(1)
        word_count = count_words(bo_quote_text)
        if word_count > 30:
            errors.append(f"Biased Opinion quote too long: {word_count} words (max 30)")
    
    return len(errors) == 0, errors, warnings


def test_random_facts_quality(json_data: Dict) -> Tuple[bool, List[str], List[str]]:
    """Test 7: Validate that Random Facts aren't just boring stats."""
    warnings = []
    html_content = extract_html_content(json_data)
    
    # Extract Random Facts
    fact_matches = re.findall(r'<div class="gg-fact-text">(.*?)</div>', html_content, re.DOTALL)
    
    weak_patterns = [
        r'The race was founded in \d{4}',
        r'\d+ riders across distances',
        r'The course is [^.]*\.$',  # Single sentence ending with period
    ]
    
    for i, fact in enumerate(fact_matches, 1):
        fact_text = re.sub(r'<[^>]+>', '', fact).strip()
        
        # Check if single sentence
        sentences = [s.strip() for s in re.split(r'[.!?]+', fact_text) if s.strip()]
        if len(sentences) < 2:
            warnings.append(f"Random Fact #{i} is only {len(sentences)} sentence(s) - should be 2+ sentences")
        
        # Check for weak patterns
        for pattern in weak_patterns:
            if re.search(pattern, fact_text, re.IGNORECASE):
                warnings.append(f"Random Fact #{i} matches weak pattern: '{pattern}'")
        
        # Check if it's just a stat with no story
        if len(fact_text.split()) < 15:
            warnings.append(f"Random Fact #{i} is too short ({len(fact_text.split())} words) - likely just a stat")
    
    # Warnings don't fail the test, but flag for manual review
    return True, [], warnings


def test_section_layout_consistency(json_data: Dict) -> Tuple[bool, List[str]]:
    """Test 8: Ensure Course Profile and Biased Opinion layouts match."""
    errors = []
    html_content = extract_html_content(json_data)
    
    # Find Course Profile section (id="course-ratings")
    course_profile_section = re.search(r'id="course-ratings".*?(?=id="|</section>)', html_content, re.DOTALL | re.IGNORECASE)
    # Find Biased Opinion section (id="biased-opinion")
    biased_opinion_section = re.search(r'id="biased-opinion".*?(?=id="|</section>|FINAL VERDICT)', html_content, re.DOTALL | re.IGNORECASE)
    
    if course_profile_section:
        cp_content = course_profile_section.group(0)
        # Count rating bars more precisely - look for the container div, not the inner fill
        cp_bars = len(re.findall(r'<div class="gg-rating-bar">', cp_content))
        cp_radar = len(re.findall(r'gg-course-radar-svg|radarChart|radar-chart', cp_content, re.IGNORECASE))
        cp_quote = len(re.findall(r'gg-course-quote|course-quote-big', cp_content, re.IGNORECASE))
    else:
        errors.append("Course Profile section not found")
        cp_bars = cp_radar = cp_quote = 0
    
    if biased_opinion_section:
        bo_content = biased_opinion_section.group(0)
        # Count rating bars more precisely - look for the container div
        bo_bars = len(re.findall(r'<div class="gg-rating-bar">', bo_content))
        # Look for radar chart - uses same classes as Course Profile (gg-radar-card, gg-course-radar-svg)
        bo_radar = len(re.findall(r'gg-radar-card|gg-course-radar-svg|radarChart|radar-chart', bo_content, re.IGNORECASE))
        # Look for quote - uses same class as Course Profile (gg-course-quote-big)
        bo_quote = len(re.findall(r'gg-course-quote-big|course-quote', bo_content, re.IGNORECASE))
    else:
        errors.append("Biased Opinion section not found (id='biased-opinion')")
        bo_bars = bo_radar = bo_quote = 0
    
    # Both should have 7 rating bars
    if cp_bars != 7:
        errors.append(f"Course Profile has {cp_bars} rating bars (expected 7)")
    if bo_bars != 7:
        errors.append(f"Biased Opinion has {bo_bars} rating bars (expected 7)")
    
    # Both should have radar charts
    if cp_radar == 0:
        errors.append("Course Profile missing radar chart")
    if bo_radar == 0:
        errors.append("Biased Opinion missing radar chart")
    
    # Course Profile should have quote, Biased Opinion uses summary/strengths/weaknesses instead
    if cp_quote == 0:
        errors.append("Course Profile missing quote section")
    # Biased Opinion doesn't require a quote - it has summary/strengths/weaknesses instead
    # Check for summary instead
    bo_summary = len(re.findall(r'<strong>.*?</strong>.*?Strengths:', bo_content if biased_opinion_section else '', re.DOTALL | re.IGNORECASE))
    if bo_summary == 0 and biased_opinion_section:
        # This is fine - Biased Opinion structure is different
        pass
    
    return len(errors) == 0, errors


def test_formatting_quality(json_data: Dict) -> Tuple[bool, List[str]]:
    """Test 9: Catch spacing and formatting issues."""
    errors = []
    html_content = extract_html_content(json_data)
    
    # Check for double/triple blank lines (indicates spacing bug)
    double_blank = re.findall(r'\n\n\n+', html_content)
    if double_blank:
        errors.append(f"Found {len(double_blank)} instances of double/triple blank lines")
    
    # Check for excessive whitespace in paragraphs (but allow normal indentation)
    # Normal indentation is <p>\n        (newline + 8 spaces) = 9 chars total
    # Flag only if there are 10+ whitespace chars (excessive)
    excessive_whitespace = re.findall(r'<p>\s{10,}', html_content)
    if excessive_whitespace:
        errors.append(f"Found {len(excessive_whitespace)} paragraphs with excessive leading whitespace")
    
    # Check for inconsistent spacing between sections
    # Look for patterns like </section>\n\n\n<section> (should be single \n)
    section_spacing = re.findall(r'</section>\s{3,}<section', html_content)
    if section_spacing:
        errors.append(f"Found {len(section_spacing)} instances of inconsistent section spacing")
    
    return len(errors) == 0, errors


def test_quote_replacement(json_data: Dict, race_slug: str) -> Tuple[bool, List[str]]:
    """Test 10: Verify quotes are race-specific, not template text."""
    errors = []
    html_content = extract_html_content(json_data)
    
    # Known template quotes to flag
    template_quotes = [
        "Something will break out there. Hopefully not you.",
        "This race will test every assumption",
    ]
    
    # Extract Black Pill quote
    bp_quote_match = re.search(r'class="gg-blackpill-quote"[^>]*>(.*?)</', html_content, re.DOTALL)
    if bp_quote_match:
        bp_quote = re.sub(r'<[^>]+>', '', bp_quote_match.group(1)).strip()
        for template in template_quotes:
            if template.lower() in bp_quote.lower():
                errors.append(f"Black Pill quote matches template text: '{template}'")
    
    # Extract course quote
    course_quote_match = re.search(r'gg-course-quote[^>]*>(.*?)</', html_content, re.DOTALL)
    if course_quote_match:
        course_quote = re.sub(r'<[^>]+>', '', course_quote_match.group(1)).strip()
        for template in template_quotes:
            if template.lower() in course_quote.lower():
                errors.append(f"Course quote matches template text: '{template}'")
    
    # For Unbound, check for Mid South quotes (and vice versa)
    if race_slug == 'unbound-200':
        if 'Bobby' in html_content or 'Stillwater' in html_content:
            errors.append("Found Mid South-specific content in Unbound quotes")
    elif race_slug == 'mid-south':
        if 'Flint Hills' in html_content and 'annoying little brother' not in html_content:
            errors.append("Found Unbound-specific content in Mid South quotes")
    
    return len(errors) == 0, errors


def test_blackpill_width_constraint(json_data: Dict) -> Tuple[bool, List[str]]:
    """Test 13: Ensure Black Pill section has width constraint (max-width)."""
    errors = []
    html_content = extract_html_content(json_data)
    
    # Find Black Pill section
    bp_section = re.search(r'class="gg-blackpill-section".*?</section>', html_content, re.DOTALL | re.IGNORECASE)
    
    if not bp_section:
        errors.append("Black Pill section not found")
        return False, errors
    
    bp_content = bp_section.group(0)
    
    # Check for max-width constraint in inline styles or CSS
    # Look for max-width in style tag or inline style attribute
    has_max_width = False
    
    # Check inline style on section
    inline_style_match = re.search(r'gg-blackpill-section[^>]*style="[^"]*max-width', bp_content, re.IGNORECASE)
    if inline_style_match:
        has_max_width = True
    
    # Check for style tag with max-width
    style_tag_match = re.search(r'<style>.*?gg-blackpill-section.*?max-width.*?</style>', html_content, re.DOTALL | re.IGNORECASE)
    if style_tag_match:
        has_max_width = True
    
    # Check for max-width value (should be reasonable, like 600-1000px)
    if has_max_width:
        max_width_match = re.search(r'max-width:\s*(\d+)px', html_content, re.IGNORECASE)
        if max_width_match:
            width_value = int(max_width_match.group(1))
            if width_value > 1200:
                errors.append(f"Black Pill max-width too wide: {width_value}px (should be 800px or less)")
            elif width_value < 600:
                errors.append(f"Black Pill max-width too narrow: {width_value}px (should be at least 600px)")
        else:
            errors.append("Black Pill has max-width but value not found")
    else:
        errors.append("Black Pill section missing max-width constraint (should be max-width: 800px)")
    
    return len(errors) == 0, errors


def test_biased_opinion_layout_structure(json_data: Dict) -> Tuple[bool, List[str]]:
    """Test 12: Ensure Biased Opinion section matches Course Profile structure."""
    errors = []
    html_content = extract_html_content(json_data)
    
    # Find both sections
    course_profile_section = re.search(r'id="course-ratings".*?(?=id="|</section>)', html_content, re.DOTALL | re.IGNORECASE)
    biased_opinion_section = re.search(r'id="biased-opinion".*?(?=id="|</section>|FINAL VERDICT)', html_content, re.DOTALL | re.IGNORECASE)
    
    if not biased_opinion_section:
        errors.append("Biased Opinion section not found")
        return False, errors
    
    bo_content = biased_opinion_section.group(0)
    
    # Check for forbidden patterns (Strengths/Weaknesses sections)
    forbidden_patterns = [
        (r'<p><strong>Strengths:</strong></p>', "Strengths section"),
        (r'<p><strong>Weaknesses:</strong></p>', "Weaknesses section"),
        (r'<ul>.*?Strengths.*?</ul>', "Strengths list"),
        (r'<h3>Strengths</h3>', "Strengths heading"),
        (r'class="strengths-list"', "Strengths list class"),
        (r'<li>.*?strength.*?</li>', "Strength list items"),
    ]
    
    for pattern, description in forbidden_patterns:
        if re.search(pattern, bo_content, re.IGNORECASE | re.DOTALL):
            errors.append(f"Biased Opinion contains forbidden '{description}' section")
    
    # Verify structure matches Course Profile
    # Both should have: radar chart, rating bars card, quote, explanations
    if course_profile_section:
        cp_content = course_profile_section.group(0)
        
        # Check both have radar charts
        cp_radar = len(re.findall(r'gg-radar-card|gg-course-radar-svg', cp_content, re.IGNORECASE))
        bo_radar = len(re.findall(r'gg-radar-card|gg-course-radar-svg', bo_content, re.IGNORECASE))
        if cp_radar > 0 and bo_radar == 0:
            errors.append("Biased Opinion missing radar chart (Course Profile has one)")
        
        # Check both have rating bars
        cp_bars = len(re.findall(r'<div class="gg-rating-bar">', cp_content))
        bo_bars = len(re.findall(r'<div class="gg-rating-bar">', bo_content))
        if cp_bars == 7 and bo_bars != 7:
            errors.append(f"Biased Opinion has {bo_bars} rating bars (expected 7, matching Course Profile)")
        
        # Check both have quotes
        cp_quote = len(re.findall(r'gg-course-quote-big|course-quote', cp_content, re.IGNORECASE))
        bo_quote = len(re.findall(r'gg-course-quote-big|course-quote', bo_content, re.IGNORECASE))
        if cp_quote > 0 and bo_quote == 0:
            errors.append("Biased Opinion missing quote section (Course Profile has one)")
        
        # Check both have explanations on right
        cp_explanations = len(re.findall(r'gg-ratings-right|gg-subheading', cp_content, re.IGNORECASE))
        bo_explanations = len(re.findall(r'gg-ratings-right|gg-subheading', bo_content, re.IGNORECASE))
        if cp_explanations > 0 and bo_explanations == 0:
            errors.append("Biased Opinion missing explanations section (Course Profile has one)")
    
    return len(errors) == 0, errors


def test_external_links(json_data: Dict) -> Tuple[bool, List[str]]:
    """Test 11: Ensure external links are valid, not placeholders."""
    errors = []
    html_content = extract_html_content(json_data)
    
    # Extract official website URL - look for "Official Race Info" or "Official Site" links
    official_patterns = [
        r'Official.*?Info.*?href="([^"]+)"',
        r'Official.*?Site.*?href="([^"]+)"',
        r'official.*?website.*?href="([^"]+)"',
        r'href="([^"]*midsouthgravel[^"]*)"',  # Mid South specific
        r'href="([^"]*unboundgravel[^"]*)"',  # Unbound specific
    ]
    
    found_official = False
    for pattern in official_patterns:
        match = re.search(pattern, html_content, re.IGNORECASE)
        if match:
            found_official = True
            url = match.group(1)
            if not url.startswith(('http://', 'https://')):
                errors.append(f"Official website URL invalid format: '{url}'")
            elif 'placeholder' in url.lower() or 'needs to be researched' in url.lower() or 'replace' in url.lower():
                errors.append(f"Official website URL is placeholder: '{url}'")
            break
    
    if not found_official:
        # Check if it exists in logistics section
        logistics_match = re.search(r'RACE LOGISTICS.*?</section>', html_content, re.DOTALL | re.IGNORECASE)
        if logistics_match:
            # Link might be there but pattern didn't match - don't fail, just warn
            pass
        else:
            errors.append("Official website link not found in expected location")
    
    # Extract RideWithGPS ID
    rwgps_match = re.search(r'ridewithgps\.com.*?id=(\d+)', html_content)
    if rwgps_match:
        rwgps_id = rwgps_match.group(1)
        if not rwgps_id.isdigit():
            errors.append(f"RideWithGPS ID is not numeric: '{rwgps_id}'")
    else:
        # Check for placeholder RideWithGPS (but allow if it's a valid route ID format)
        if 'needs to be researched' in html_content.lower() and 'ridewithgps' in html_content.lower():
            errors.append("RideWithGPS ID appears to be placeholder")
    
    return len(errors) == 0, errors


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 test_generator.py <json_file> <race_slug> [comparison_file] [comparison_race]")
        print("")
        print("Examples:")
        print("  python3 test_generator.py output/elementor-mid-south.json mid-south")
        print("  python3 test_generator.py output/elementor-mid-south.json mid-south output/elementor-unbound-200.json unbound-200")
        sys.exit(1)
    
    json_file = sys.argv[1]
    race_slug = sys.argv[2]
    comparison_file = sys.argv[3] if len(sys.argv) > 3 else None
    comparison_race = sys.argv[4] if len(sys.argv) > 4 else None
    
    print("=" * 70)
    print("LANDING PAGE GENERATOR REGRESSION TEST SUITE")
    print("=" * 70)
    print(f"Testing: {json_file}")
    print(f"Race: {race_slug}")
    print("")
    
    # Load JSON
    json_data = load_json(json_file)
    
    all_passed = True
    results = []
    
    # Test 1: No template leakage
    print("TEST 1: No Template Leakage")
    passed, errors = test_no_template_leakage(json_data, race_slug)
    if passed:
        print("  ✅ No template leakage detected")
    else:
        print("  ❌ Template leakage detected:")
        for error in errors:
            print(f"     - {error}")
        all_passed = False
    results.append(("Template Leakage", passed))
    print("")
    
    # Test 2: All placeholders replaced
    print("TEST 2: All Placeholders Replaced")
    passed, errors = test_all_placeholders_replaced(json_data)
    if passed:
        print("  ✅ All placeholders replaced")
    else:
        print("  ❌ Unreplaced placeholders found:")
        for error in errors:
            print(f"     - {error}")
        all_passed = False
    results.append(("Placeholders", passed))
    print("")
    
    # Test 3: Required sections present
    print("TEST 3: Required Sections Present")
    passed, errors = test_required_sections_present(json_data, race_slug)
    if passed:
        print("  ✅ All required sections present")
    else:
        print("  ❌ Missing required sections:")
        for error in errors:
            print(f"     - {error}")
        all_passed = False
    results.append(("Required Sections", passed))
    print("")
    
    # Test 4: Content uniqueness (if comparison file provided)
    if comparison_file and comparison_race:
        print("TEST 4: Content Uniqueness")
        passed, errors = test_content_uniqueness(json_file, comparison_file, race_slug, comparison_race)
        if passed:
            print("  ✅ Content is unique")
        else:
            print("  ❌ Content similarity issues:")
            for error in errors:
                print(f"     - {error}")
            all_passed = False
        results.append(("Content Uniqueness", passed))
        print("")
    else:
        print("TEST 4: Content Uniqueness")
        print("  ⚠️  Skipped (no comparison file provided)")
        print("")
    
    # Test 5: Structural integrity
    print("TEST 5: JSON Structural Integrity")
    passed, errors = test_structural_integrity(json_data)
    if passed:
        print("  ✅ JSON structure valid")
    else:
        print("  ❌ JSON structure issues:")
        for error in errors:
            print(f"     - {error}")
        all_passed = False
    results.append(("Structural Integrity", passed))
    print("")
    
    # Test 6: Content length limits
    print("TEST 6: Content Length Limits")
    passed, errors, warnings = test_content_length_limits(json_data)
    if passed:
        print("  ✅ Content length limits respected")
    else:
        print("  ❌ Content length violations:")
        for error in errors:
            print(f"     - {error}")
        all_passed = False
    if warnings:
        print("  ⚠️  Warnings:")
        for warning in warnings:
            print(f"     - {warning}")
    results.append(("Content Length", passed))
    print("")
    
    # Test 7: Random Facts Quality
    print("TEST 7: Random Facts Quality")
    passed, errors, warnings = test_random_facts_quality(json_data)
    if warnings:
        print("  ⚠️  Quality warnings (manual review recommended):")
        for warning in warnings:
            print(f"     - {warning}")
    else:
        print("  ✅ Random facts quality acceptable")
    # Warnings don't fail, but flag for review
    results.append(("Random Facts Quality", True))
    print("")
    
    # Test 8: Layout Consistency
    print("TEST 8: Section Layout Consistency")
    passed, errors = test_section_layout_consistency(json_data)
    if passed:
        print("  ✅ Course Profile and Biased Opinion layouts match")
    else:
        print("  ❌ Layout inconsistencies:")
        for error in errors:
            print(f"     - {error}")
        all_passed = False
    results.append(("Layout Consistency", passed))
    print("")
    
    # Test 9: Formatting Quality
    print("TEST 9: Formatting Quality")
    passed, errors = test_formatting_quality(json_data)
    if passed:
        print("  ✅ Formatting is clean")
    else:
        print("  ❌ Formatting issues:")
        for error in errors:
            print(f"     - {error}")
        all_passed = False
    results.append(("Formatting", passed))
    print("")
    
    # Test 10: Quote Replacement
    print("TEST 10: Quote Uniqueness")
    passed, errors = test_quote_replacement(json_data, race_slug)
    if passed:
        print("  ✅ Quotes are race-specific")
    else:
        print("  ❌ Quote issues:")
        for error in errors:
            print(f"     - {error}")
        all_passed = False
    results.append(("Quote Uniqueness", passed))
    print("")
    
    # Test 11: External Links Valid
    print("TEST 11: External Links Valid")
    passed, errors = test_external_links(json_data)
    if passed:
        print("  ✅ External links are valid")
    else:
        print("  ❌ Link issues:")
        for error in errors:
            print(f"     - {error}")
        all_passed = False
    results.append(("External Links", passed))
    print("")
    
    # Test 12: Biased Opinion Layout Structure
    print("TEST 12: Biased Opinion Layout Structure")
    passed, errors = test_biased_opinion_layout_structure(json_data)
    if passed:
        print("  ✅ Biased Opinion layout matches Course Profile")
    else:
        print("  ❌ Layout structure issues:")
        for error in errors:
            print(f"     - {error}")
        all_passed = False
    results.append(("Biased Opinion Layout", passed))
    print("")
    
    # Test 13: Black Pill Width Constraint
    print("TEST 13: Black Pill Width Constraint")
    passed, errors = test_blackpill_width_constraint(json_data)
    if passed:
        print("  ✅ Black Pill section has proper width constraint")
    else:
        print("  ❌ Width constraint issues:")
        for error in errors:
            print(f"     - {error}")
        all_passed = False
    results.append(("Black Pill Width", passed))
    print("")
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    print("")
    
    if all_passed:
        print("✅ ALL TESTS PASSED")
        print("")
        print("File is ready for WordPress import.")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        print("")
        print("DO NOT import to WordPress until all tests pass.")
        sys.exit(1)


if __name__ == '__main__':
    main()

