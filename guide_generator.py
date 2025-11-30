#!/usr/bin/env python3
"""
Gravel God Training Guide Generator
Generates HTML training guides from race JSON + plan JSON templates.

Usage:
    python guide_generator.py --race unbound_200.json --plan compete_masters_complete.json
    python guide_generator.py --race-dir races/unbound-200/ --all-plans
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# =============================================================================
# CONSTANTS
# =============================================================================

# Neo-brutalist color palette
COLORS = {
    'cream': '#f5f5dc',
    'cream_dark': '#ede5d0',
    'turquoise': '#4ecdc4',
    'turquoise_light': 'rgba(78, 205, 196, 0.15)',
    'yellow': '#f4d03f',
    'yellow_light': '#fef9e7',
    'brown_dark': '#59473C',
    'text_dark': '#2c2c2c',
    'red': '#e74c3c',
    'red_light': '#fdedec',
    'green': '#27ae60',
    'green_light': '#e9f7ef',
}

# Plan tier metadata
TIER_INFO = {
    'ayahuasca': {'hours': '0-5', 'description': 'Minimal time, maximum efficiency'},
    'finisher': {'hours': '8-12', 'description': 'Finish strong with focused training'},
    'compete': {'hours': '12-18', 'description': 'Race competitively with serious training'},
    'podium': {'hours': '18+', 'description': 'Elite preparation for top performance'},
}

# =============================================================================
# DATA LOADING
# =============================================================================

def load_json(filepath: str) -> Dict[str, Any]:
    """Load JSON file with error handling."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {filepath}: {e}")
        sys.exit(1)


def extract_race_data(race_json: Dict[str, Any]) -> Dict[str, str]:
    """Extract and flatten race data for placeholder substitution."""
    race = race_json.get('race', race_json)
    vitals = race.get('vitals', {})
    radar = race.get('radar_scores', {})
    location = vitals.get('location', {})
    non_negs = race.get('non_negotiables', [])
    skills = race_json.get('skills', {})
    key_workouts = race_json.get('key_workouts', [])
    
    data = {
        # Basic race info
        'RACE_NAME': race.get('name', ''),
        'RACE_SLUG': race.get('slug', ''),
        'RACE_TAGLINE': race.get('tagline', ''),
        'RACE_DESCRIPTION': race.get('description', ''),
        'DISTANCE': str(vitals.get('distance_miles', '')),
        'ELEVATION_GAIN': f"{vitals.get('elevation_gain_ft', ''):,}" if vitals.get('elevation_gain_ft') else '',
        'RACE_ELEVATION': str(vitals.get('elevation_ft', '')),
        'TERRAIN_DESCRIPTION': race.get('terrain_description', ''),
        'DURATION_ESTIMATE': race.get('duration_estimate', ''),
        'RACE_KEY_CHALLENGES': race.get('key_challenges', ''),
        'LOCATION_CITY': location.get('city', ''),
        'LOCATION_STATE': location.get('state', ''),
        
        # Radar scores
        'RADAR_ELEVATION': str(radar.get('elevation', {}).get('score', 3)),
        'RADAR_LENGTH': str(radar.get('length', {}).get('score', 3)),
        'RADAR_TECHNICALITY': str(radar.get('technicality', {}).get('score', 3)),
        'RADAR_CLIMATE': str(radar.get('climate', {}).get('score', 3)),
        'RADAR_ALTITUDE': str(radar.get('altitude', {}).get('score', 1)),
        'RADAR_ADVENTURE': str(radar.get('adventure', {}).get('score', 3)),
        
        # Race-specific content
        'RACE_SUPPORT_URL': race.get('support_url', ''),
        'RECOMMENDED_TIRE_WIDTH': race.get('recommended_tire_width', '38-42mm'),
        'AID_STATION_STRATEGY': race.get('aid_station_strategy', ''),
        'WEATHER_STRATEGY': race.get('weather_strategy', ''),
        'RACE_SPECIFIC_SKILL_NOTES': race.get('skill_notes', ''),
        'RACE_SPECIFIC_TACTICS': race.get('tactics', ''),
        'EQUIPMENT_CHECKLIST': race.get('equipment_checklist', ''),
        
        # Tier/level from plan context (may be overridden)
        'ABILITY_LEVEL': race_json.get('ability_level', 'Intermediate'),
        'TIER_NAME': race_json.get('tier_name', 'Finisher'),
        'WEEKLY_HOURS': str(race_json.get('weekly_hours', 10)),
        'WEEKLY_STRUCTURE_DESCRIPTION': race_json.get('weekly_structure', ''),
        
        # Skill 5 (race-specific)
        'SKILL_5_NAME': skills.get('skill_5_name', 'Race-Specific Skill'),
        'SKILL_5_WHY': skills.get('skill_5_why', ''),
        'SKILL_5_HOW': skills.get('skill_5_how', ''),
        'SKILL_5_CUE': skills.get('skill_5_cue', ''),
    }
    
    # Non-negotiables (up to 5)
    for i, nn in enumerate(non_negs[:5], 1):
        data[f'NON_NEG_{i}_REQUIREMENT'] = nn.get('requirement', '')
        data[f'NON_NEG_{i}_BY_WHEN'] = nn.get('by_when', '')
        data[f'NON_NEG_{i}_WHY'] = nn.get('why', '')
    
    # Pad remaining non-negotiables if fewer than 5
    for i in range(len(non_negs) + 1, 6):
        data[f'NON_NEG_{i}_REQUIREMENT'] = ''
        data[f'NON_NEG_{i}_BY_WHEN'] = ''
        data[f'NON_NEG_{i}_WHY'] = ''
    
    # Key workouts (up to 4)
    for i, kw in enumerate(key_workouts[:4], 1):
        data[f'KEY_WORKOUT_{i}_NAME'] = kw.get('name', '')
        data[f'KEY_WORKOUT_{i}_PURPOSE'] = kw.get('purpose', '')
    
    # Pad remaining key workouts if fewer than 4
    for i in range(len(key_workouts) + 1, 5):
        data[f'KEY_WORKOUT_{i}_NAME'] = ''
        data[f'KEY_WORKOUT_{i}_PURPOSE'] = ''
    
    return data


def extract_plan_data(plan_json: Dict[str, Any]) -> Dict[str, str]:
    """Extract plan metadata for placeholder substitution."""
    meta = plan_json.get('plan_metadata', {})
    mods = plan_json.get('default_modifications', {})
    
    data = {
        'PLAN_NAME': meta.get('name', ''),
        'PLAN_DURATION_WEEKS': str(meta.get('duration_weeks', 12)),
        'PLAN_PHILOSOPHY': meta.get('philosophy', 'Traditional Pyramidal'),
        'PLAN_TARGET_HOURS': meta.get('target_hours', ''),
        'PLAN_TARGET_ATHLETE': meta.get('target_athlete', ''),
        'PLAN_GOAL': meta.get('goal', ''),
    }
    
    # Extract philosophy-specific guidance if present
    for key, value in mods.items():
        if isinstance(value, dict) and value.get('enabled'):
            data[f'MOD_{key.upper()}_ENABLED'] = 'true'
            if 'description' in value:
                data[f'MOD_{key.upper()}_DESC'] = value['description']
    
    return data


# =============================================================================
# RADAR CHART SVG GENERATION
# =============================================================================

def generate_radar_svg(scores: Dict[str, int], size: int = 400) -> str:
    """Generate SVG radar chart for race difficulty profile."""
    import math
    
    center = size // 2
    max_radius = center - 40
    
    # 6 axes: Elevation, Length, Technical, Climate, Altitude, Adventure
    labels = ['ELEVATION', 'LENGTH', 'TECHNICAL', 'CLIMATE', 'ALTITUDE', 'ADVENTURE']
    values = [
        scores.get('elevation', 3),
        scores.get('length', 3),
        scores.get('technicality', 3),
        scores.get('climate', 3),
        scores.get('altitude', 1),
        scores.get('adventure', 3),
    ]
    
    # Calculate polygon points
    angle_step = 2 * math.pi / 6
    polygon_points = []
    label_positions = []
    
    for i, val in enumerate(values):
        angle = -math.pi/2 + i * angle_step  # Start at top
        radius = (val / 5) * max_radius
        x = center + radius * math.cos(angle)
        y = center + radius * math.sin(angle)
        polygon_points.append(f"{x:.0f},{y:.0f}")
        
        # Label position (outside the chart)
        label_radius = max_radius + 30
        lx = center + label_radius * math.cos(angle)
        ly = center + label_radius * math.sin(angle)
        label_positions.append((lx, ly, labels[i], values[i]))
    
    # Generate SVG
    svg_parts = [
        f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}">',
        f'<rect x="0" y="0" width="{size}" height="{size}" fill="white"/>',
    ]
    
    # Draw concentric circles (5 levels)
    for level in range(1, 6):
        r = (level / 5) * max_radius
        svg_parts.append(f'<circle cx="{center}" cy="{center}" r="{r:.0f}" fill="none" stroke="#e0e0e0" stroke-width="1"/>')
    
    # Draw axis lines
    for i in range(6):
        angle = -math.pi/2 + i * angle_step
        x2 = center + max_radius * math.cos(angle)
        y2 = center + max_radius * math.sin(angle)
        svg_parts.append(f'<line x1="{center}" y1="{center}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#ccc" stroke-width="1"/>')
    
    # Draw data polygon
    polygon_str = ' '.join(polygon_points)
    svg_parts.append(f'<polygon points="{polygon_str}" fill="rgba(78, 205, 196, 0.3)" stroke="#4ecdc4" stroke-width="3"/>')
    
    # Draw data points
    for point in polygon_points:
        x, y = point.split(',')
        svg_parts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#4ecdc4" stroke="#2c2c2c" stroke-width="2"/>')
    
    # Draw labels
    for lx, ly, label, val in label_positions:
        anchor = "middle"
        if lx < center - 20:
            anchor = "end"
        elif lx > center + 20:
            anchor = "start"
        svg_parts.append(
            f'<text x="{lx:.0f}" y="{ly:.0f}" text-anchor="{anchor}" '
            f'font-family="Sometype Mono, monospace" font-size="12" font-weight="700">'
            f'{label} ({val}/5)</text>'
        )
    
    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


# =============================================================================
# PHASE BAR SVG GENERATION
# =============================================================================

def generate_phase_bar_svg() -> str:
    """Generate SVG showing 12-week training phases."""
    return '''<svg viewBox="0 0 600 120" width="600" height="120">
<text x="10" y="20" font-family="Sometype Mono, monospace" font-size="10" fill="#666">WEEK</text>
<text x="70" y="20" font-family="Sometype Mono, monospace" font-size="10" fill="#2c2c2c">1</text>
<text x="110" y="20" font-family="Sometype Mono, monospace" font-size="10" fill="#2c2c2c">2</text>
<text x="150" y="20" font-family="Sometype Mono, monospace" font-size="10" fill="#2c2c2c">3</text>
<text x="190" y="20" font-family="Sometype Mono, monospace" font-size="10" fill="#2c2c2c">4</text>
<text x="230" y="20" font-family="Sometype Mono, monospace" font-size="10" fill="#2c2c2c">5</text>
<text x="270" y="20" font-family="Sometype Mono, monospace" font-size="10" fill="#2c2c2c">6</text>
<text x="310" y="20" font-family="Sometype Mono, monospace" font-size="10" fill="#2c2c2c">7</text>
<text x="350" y="20" font-family="Sometype Mono, monospace" font-size="10" fill="#2c2c2c">8</text>
<text x="390" y="20" font-family="Sometype Mono, monospace" font-size="10" fill="#2c2c2c">9</text>
<text x="430" y="20" font-family="Sometype Mono, monospace" font-size="10" fill="#2c2c2c">10</text>
<text x="470" y="20" font-family="Sometype Mono, monospace" font-size="10" fill="#2c2c2c">11</text>
<text x="510" y="20" font-family="Sometype Mono, monospace" font-size="10" fill="#2c2c2c">12</text>
<text x="555" y="20" font-family="Sometype Mono, monospace" font-size="10" fill="#e74c3c" font-weight="700">RACE</text>
<rect x="55" y="35" width="120" height="40" fill="#4ecdc4" stroke="#2c2c2c" stroke-width="2"/>
<text x="115" y="60" text-anchor="middle" font-family="Sometype Mono, monospace" font-size="12" font-weight="700" fill="#2c2c2c">BASE</text>
<rect x="175" y="35" width="160" height="40" fill="#f4d03f" stroke="#2c2c2c" stroke-width="2"/>
<text x="255" y="60" text-anchor="middle" font-family="Sometype Mono, monospace" font-size="12" font-weight="700" fill="#2c2c2c">BUILD</text>
<rect x="335" y="35" width="120" height="40" fill="#e74c3c" stroke="#2c2c2c" stroke-width="2"/>
<text x="395" y="60" text-anchor="middle" font-family="Sometype Mono, monospace" font-size="12" font-weight="700" fill="white">PEAK</text>
<rect x="455" y="35" width="80" height="40" fill="#27ae60" stroke="#2c2c2c" stroke-width="2"/>
<text x="495" y="60" text-anchor="middle" font-family="Sometype Mono, monospace" font-size="12" font-weight="700" fill="white">TAPER</text>
<rect x="545" y="30" width="40" height="50" fill="none" stroke="#e74c3c" stroke-width="3" stroke-dasharray="5,3"/>
<text x="565" y="60" text-anchor="middle" font-family="Sometype Mono, monospace" font-size="10" font-weight="700" fill="#e74c3c">🏁</text>
<rect x="55" y="95" width="15" height="15" fill="#4ecdc4" stroke="#2c2c2c" stroke-width="1"/>
<text x="75" y="106" font-family="Sometype Mono, monospace" font-size="9" fill="#2c2c2c">Aerobic Foundation</text>
<rect x="180" y="95" width="15" height="15" fill="#f4d03f" stroke="#2c2c2c" stroke-width="1"/>
<text x="200" y="106" font-family="Sometype Mono, monospace" font-size="9" fill="#2c2c2c">Race-Specific Fitness</text>
<rect x="320" y="95" width="15" height="15" fill="#e74c3c" stroke="#2c2c2c" stroke-width="1"/>
<text x="340" y="106" font-family="Sometype Mono, monospace" font-size="9" fill="#2c2c2c">Maximum Load</text>
<rect x="440" y="95" width="15" height="15" fill="#27ae60" stroke="#2c2c2c" stroke-width="1"/>
<text x="460" y="106" font-family="Sometype Mono, monospace" font-size="9" fill="#2c2c2c">Fresh for Race Day</text>
</svg>'''


# =============================================================================
# HTML TEMPLATE
# =============================================================================

def get_css() -> str:
    """Return the complete neo-brutalist CSS."""
    return '''/* ============================================
   GRAVEL GOD NEO-BRUTALIST DESIGN SYSTEM
   ============================================ */

:root {
    --cream: #f5f5dc;
    --cream-dark: #ede5d0;
    --turquoise: #4ecdc4;
    --turquoise-light: rgba(78, 205, 196, 0.15);
    --yellow: #f4d03f;
    --yellow-light: #fef9e7;
    --brown-dark: #59473C;
    --text-dark: #2c2c2c;
    --red: #e74c3c;
    --red-light: #fdedec;
    --green: #27ae60;
    --green-light: #e9f7ef;
    --border-width: 3px;
    --shadow-offset: 6px;
    --shadow-color: rgba(0,0,0,0.2);
}

* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; scroll-padding-top: 80px; }

body {
    font-family: 'Sometype Mono', 'Courier New', Courier, monospace;
    font-size: 16px;
    line-height: 1.7;
    color: var(--text-dark);
    background: linear-gradient(135deg, var(--cream) 0%, var(--cream-dark) 100%);
    min-height: 100vh;
}

/* Navigation */
.sticky-nav {
    position: sticky;
    top: 0;
    z-index: 100;
    background: var(--brown-dark);
    border-bottom: var(--border-width) solid var(--text-dark);
    box-shadow: 0 var(--shadow-offset) 0 var(--shadow-color);
    padding: 0.75rem 1rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    justify-content: center;
}

.sticky-nav a {
    color: var(--cream);
    text-decoration: none;
    font-size: 0.75rem;
    font-weight: 500;
    padding: 0.35rem 0.6rem;
    border: 2px solid transparent;
    transition: all 0.2s ease;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.sticky-nav a:hover { color: var(--turquoise); border-color: var(--turquoise); }
.sticky-nav a.active { background: var(--turquoise); color: var(--text-dark); border-color: var(--text-dark); }

/* Header */
.header {
    background: var(--brown-dark);
    color: var(--cream);
    padding: 3rem 2rem;
    text-align: center;
    border-bottom: var(--border-width) solid var(--text-dark);
}

.header-brand { font-size: 0.9rem; text-transform: uppercase; letter-spacing: 3px; color: var(--turquoise); margin-bottom: 0.5rem; }
.header h1 { font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 2px; }
.header-subtitle { font-size: 1.1rem; opacity: 0.9; margin-bottom: 1rem; }
.header-meta { display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap; margin-top: 1.5rem; }
.header-meta-item { background: rgba(255,255,255,0.1); padding: 0.5rem 1rem; border: 2px solid var(--turquoise); }
.header-meta-item strong { color: var(--turquoise); }

/* Sections */
.section { padding: 3rem 2rem; max-width: 900px; margin: 0 auto; border-bottom: 2px dashed var(--brown-dark); }
.section:last-of-type { border-bottom: none; }
.section-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: var(--border-width) solid var(--text-dark); }
.section-number { background: var(--turquoise); color: var(--text-dark); width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: 700; border: var(--border-width) solid var(--text-dark); box-shadow: var(--shadow-offset) var(--shadow-offset) 0 var(--text-dark); }
.section-header h2 { font-size: 1.8rem; text-transform: uppercase; letter-spacing: 1px; }
.section-content h3 { font-size: 1.3rem; margin: 2rem 0 1rem; color: var(--brown-dark); border-left: 4px solid var(--turquoise); padding-left: 1rem; }
.section-content h4 { font-size: 1.1rem; margin: 1.5rem 0 0.75rem; color: var(--text-dark); }
.section-content p { margin-bottom: 1rem; }
.section-content ul, .section-content ol { margin: 1rem 0 1rem 1.5rem; }
.section-content li { margin-bottom: 0.5rem; }

/* Intro Box */
.intro-box { background: white; padding: 1.5rem; border: var(--border-width) solid var(--text-dark); box-shadow: var(--shadow-offset) var(--shadow-offset) 0 var(--text-dark); margin-bottom: 2rem; }

/* Tables */
.table-wrapper { overflow-x: auto; margin: 1.5rem 0; border: var(--border-width) solid var(--text-dark); box-shadow: var(--shadow-offset) var(--shadow-offset) 0 var(--text-dark); }
table { width: 100%; border-collapse: collapse; background: white; }
th { background: var(--brown-dark); color: var(--cream); padding: 1rem; text-align: left; font-weight: 700; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 0.5px; }
td { padding: 0.875rem 1rem; border-bottom: 1px solid var(--cream-dark); font-size: 0.9rem; }
tr:hover { background: var(--cream-dark); }
tr.g-spot-row { background: var(--turquoise-light); }
tr.g-spot-row:hover { background: rgba(78, 205, 196, 0.25); }

/* Callouts */
.callout { padding: 1.5rem; margin: 1.5rem 0; border: var(--border-width) solid var(--text-dark); box-shadow: var(--shadow-offset) var(--shadow-offset) 0 var(--text-dark); }
.callout-title { font-weight: 700; text-transform: uppercase; font-size: 0.9rem; letter-spacing: 0.5px; margin-bottom: 0.75rem; }
.callout-info { background: var(--turquoise-light); border-color: var(--turquoise); }
.callout-info .callout-title { color: var(--brown-dark); }
.callout-warning { background: var(--yellow-light); border-color: var(--yellow); }
.callout-warning .callout-title { color: var(--brown-dark); }
.callout-danger { background: var(--red-light); border-color: var(--red); }
.callout-danger .callout-title { color: var(--red); }
.callout-success { background: var(--green-light); border-color: var(--green); }
.callout-success .callout-title { color: var(--green); }

/* Cards */
.card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin: 1.5rem 0; }
.card { background: white; padding: 1.5rem; border: var(--border-width) solid var(--text-dark); box-shadow: var(--shadow-offset) var(--shadow-offset) 0 var(--text-dark); }
.card h4 { color: var(--brown-dark); margin-bottom: 0.75rem; font-size: 1rem; }
.card p { font-size: 0.9rem; margin: 0; }

/* Graphics */
.graphic-container { background: white; border: var(--border-width) solid var(--text-dark); box-shadow: var(--shadow-offset) var(--shadow-offset) 0 var(--text-dark); padding: 1.5rem; margin: 1.5rem 0; text-align: center; }
.graphic-title { font-weight: 700; text-transform: uppercase; font-size: 0.9rem; letter-spacing: 1px; margin-bottom: 1rem; color: var(--brown-dark); }
.graphic-container svg { max-width: 100%; height: auto; }

/* Skills Grid */
.skills-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin: 1.5rem 0; }
.skill-item { background: white; padding: 1.25rem; border: var(--border-width) solid var(--text-dark); box-shadow: 4px 4px 0 var(--text-dark); }
.skill-item h4 { color: var(--brown-dark); margin-bottom: 0.5rem; font-size: 1rem; border-bottom: 2px solid var(--turquoise); padding-bottom: 0.5rem; }
.skill-item p { font-size: 0.9rem; margin: 0; }
.skill-cue { font-style: italic; color: var(--turquoise); margin-top: 0.5rem; font-weight: 600; }

/* Glossary */
.glossary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin: 1.5rem 0; }
.glossary-item { background: white; padding: 1rem; border: 2px solid var(--cream-dark); }
.glossary-term { font-weight: 700; color: var(--turquoise); margin-bottom: 0.25rem; }
.glossary-def { font-size: 0.85rem; }

/* Phase List */
.phase-list { margin: 1.5rem 0; }
.phase-item { display: flex; align-items: center; gap: 1rem; padding: 0.75rem 1rem; margin-bottom: 0.5rem; background: white; border: 2px solid var(--text-dark); }
.phase-weeks { font-size: 0.85rem; font-weight: 600; min-width: 80px; }
.phase-name { font-weight: 700; min-width: 80px; }
.phase-desc { font-size: 0.9rem; }
.phase-base { border-left: 4px solid #4ecdc4; }
.phase-build { border-left: 4px solid #f4d03f; }
.phase-peak { border-left: 4px solid #e74c3c; }
.phase-taper { border-left: 4px solid #27ae60; }

/* Footer */
.footer { background: var(--brown-dark); color: var(--cream); text-align: center; padding: 4rem 2rem; border-top: var(--border-width) solid var(--text-dark); }
.footer-tagline { font-size: 2rem; font-weight: 700; color: var(--turquoise); margin-bottom: 2rem; text-transform: uppercase; letter-spacing: 2px; }
.footer-content { max-width: 700px; margin: 0 auto 2rem; }
.footer-content p { margin-bottom: 1.25rem; line-height: 1.8; }
.footer-emphasis { font-size: 1.1rem; font-weight: 700; color: var(--turquoise); }
.footer-contact { margin-top: 3rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.2); }
.footer-email { font-size: 0.95rem; margin-bottom: 0.5rem; }
.footer-email a { color: var(--turquoise); }
.footer-motto { font-size: 1rem; font-style: italic; color: var(--turquoise); margin-top: 1rem; }

/* Responsive */
@media (max-width: 768px) {
    .header h1 { font-size: 1.8rem; }
    .sticky-nav { padding: 0.5rem; }
    .sticky-nav a { font-size: 0.65rem; padding: 0.3rem 0.5rem; }
    .section { padding: 2rem 1rem; }
    .section-header h2 { font-size: 1.4rem; }
    th, td { padding: 0.5rem; font-size: 0.8rem; }
}

hr { border: none; border-top: 2px dashed var(--text-dark); margin: 2rem 0; opacity: 0.3; }'''


def get_nav_script() -> str:
    """Return the navigation highlight script."""
    return '''document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('.section');
    const navLinks = document.querySelectorAll('.sticky-nav a');
    
    function updateActiveLink() {
        let current = '';
        const scrollPos = window.scrollY + 100;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    }
    
    window.addEventListener('scroll', updateActiveLink);
    updateActiveLink();
});'''


# =============================================================================
# GUIDE GENERATION
# =============================================================================

def generate_guide_html(race_data: Dict[str, str], plan_data: Dict[str, str], 
                        radar_scores: Dict[str, int]) -> str:
    """Generate complete HTML training guide."""
    
    # Merge all data for placeholders
    data = {**race_data, **plan_data}
    
    # Generate SVG graphics
    radar_svg = generate_radar_svg(radar_scores)
    phase_svg = generate_phase_bar_svg()
    
    # Build HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow">
    <title>{data['RACE_NAME']} Training Guide | {data['TIER_NAME']} - {data['ABILITY_LEVEL']}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Sometype+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
{get_css()}
</style>
</head>
<body>

<nav class="sticky-nav">
    <a href="#welcome">Welcome</a>
    <a href="#structure">Structure</a>
    <a href="#before">Before</a>
    <a href="#how-training-works">Training</a>
    <a href="#zones">Zones</a>
    <a href="#execution">Execution</a>
    <a href="#recovery">Recovery</a>
    <a href="#strength">Strength</a>
    <a href="#skills">Skills</a>
    <a href="#fueling">Fueling</a>
    <a href="#mental">Mental</a>
    <a href="#race-day">Race Day</a>
    <a href="#tires">Tires</a>
    <a href="#glossary">Glossary</a>
</nav>

<header class="header">
    <div class="header-brand">Gravel God Coaching</div>
    <h1>{data['RACE_NAME']}</h1>
    <p class="header-subtitle">Training Guide</p>
    <div class="header-meta">
        <div class="header-meta-item"><strong>{data['TIER_NAME']}</strong> Tier</div>
        <div class="header-meta-item"><strong>{data['ABILITY_LEVEL']}</strong> Level</div>
        <div class="header-meta-item"><strong>{data['WEEKLY_HOURS']}</strong> hrs/week</div>
        <div class="header-meta-item"><strong>12</strong> weeks</div>
    </div>
</header>

<main>
<section class="section" id="welcome">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2>Welcome to Your Training</h2>
    </div>
    <div class="section-content">
        <div class="intro-box">
            <p>This plan isn't generic. It's built for <strong>{data['RACE_NAME']}</strong>—its {data['DISTANCE']} miles, {data['TERRAIN_DESCRIPTION']}, {data['ELEVATION_GAIN']} feet of elevation, and what it'll take to be out there for {data['DURATION_ESTIMATE']}.</p>
            <p>{data['RACE_DESCRIPTION']}</p>
            <p><strong>By the time you roll to the start, you'll know you're ready.</strong></p>
        </div>
        
        <div class="graphic-container">
            <div class="graphic-title">Race Difficulty Profile</div>
            {radar_svg}
        </div>
        
        <h3>What Makes This Plan Different</h3>
        <div class="card-grid">
            <div class="card">
                <h4>Built for Your Ability Level</h4>
                <p>You're on the <strong>{data['ABILITY_LEVEL']}</strong> version. The load and intensity match where you are right now.</p>
            </div>
            <div class="card">
                <h4>Built for Your Schedule</h4>
                <p>This is the <strong>{data['TIER_NAME']}</strong> tier, designed around <strong>{data['WEEKLY_HOURS']} hours/week</strong>. The week fits into your life so you can actually complete it.</p>
            </div>
            <div class="card">
                <h4>Built for This Race</h4>
                <p>The sessions target the key demands of {data['RACE_NAME']}: <strong>{data['RACE_KEY_CHALLENGES']}</strong>.</p>
            </div>
        </div>
    </div>
</section>

<section class="section" id="structure">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2>Plan Structure</h2>
    </div>
    <div class="section-content">
        <h3>12 Weeks, 4 Phases</h3>
        
        <div class="graphic-container">
            <div class="graphic-title">Training Phases</div>
            {phase_svg}
        </div>
        
        <div class="phase-list">
            <div class="phase-item phase-base">
                <span class="phase-weeks">Weeks 1-3</span>
                <span class="phase-name">BASE</span>
                <span class="phase-desc">Building aerobic foundation and endurance</span>
            </div>
            <div class="phase-item phase-build">
                <span class="phase-weeks">Weeks 4-7</span>
                <span class="phase-name">BUILD</span>
                <span class="phase-desc">Adding intensity, developing race-specific fitness</span>
            </div>
            <div class="phase-item phase-peak">
                <span class="phase-weeks">Weeks 8-10</span>
                <span class="phase-name">PEAK</span>
                <span class="phase-desc">Maximum training load and sharpening</span>
            </div>
            <div class="phase-item phase-taper">
                <span class="phase-weeks">Weeks 11-12</span>
                <span class="phase-name">TAPER</span>
                <span class="phase-desc">Reducing volume while maintaining intensity</span>
            </div>
        </div>
        
        <h3>Weekly Structure</h3>
        <div class="table-wrapper">
            <table>
                <thead><tr><th>Day</th><th>Session</th><th>Duration</th></tr></thead>
                <tbody>
{generate_weekly_structure_rows(data['WEEKLY_STRUCTURE_DESCRIPTION'])}
                </tbody>
            </table>
        </div>
        
        <div class="callout callout-info">
            <div class="callout-title">Recovery Weeks</div>
            <p>Every third or fourth week is a recovery week with 30-40% reduced volume. <strong>Recovery makes you fast.</strong> Don't skip these.</p>
        </div>
        
        <h3>A Note on Compliance vs. Perfection</h3>
        <p>You won't execute this plan perfectly. No one does.</p>
        <p>Life happens. Work intrudes. Illness strikes. Weather doesn't cooperate. Kids need attention. That's reality.</p>
        <p>The goal isn't perfection—it's <strong>consistency</strong>. Complete 85-90% of the prescribed workouts, and you'll arrive at {data['RACE_NAME']} prepared. Complete 95%+, and you'll be exceptionally prepared.</p>
        <p>Miss multiple weeks, skip the hard workouts, or constantly substitute 'easier' options, and the plan won't work. Not because the plan failed—because you didn't do it.</p>
        <p><strong>Be honest with yourself about compliance.</strong></p>
    </div>
</section>

{generate_before_you_start_section(data)}

{generate_training_fundamentals_section(data)}

{generate_zones_section()}

{generate_execution_section()}

{generate_recovery_section(data)}

{generate_strength_section(data)}

{generate_skills_section(data)}

{generate_fueling_section()}

{generate_mental_section()}

{generate_race_day_section(data)}

{generate_race_specific_section(data)}

{generate_tires_section()}

{generate_glossary_section()}

</main>

<footer class="footer">
    <div class="footer-tagline">See You at the Finish</div>
    <div class="footer-content">
        <p>You have the plan. You understand how training works, how to execute the workouts, how to fuel and hydrate, how to manage your mental game, and how to approach race day.</p>
        <p class="footer-emphasis">Now do the work.</p>
        <p><em>Not perfectly. Not heroically. Consistently. Intelligently. Over 12 weeks.</em></p>
        <p>On race morning, you'll stand at the start line knowing you did everything you could to prepare. That confidence—not hope, not optimism, but confidence based on completed work—is what this plan builds.</p>
        <p class="footer-emphasis">The race will be hard. You trained for hard.</p>
    </div>
    <div class="footer-contact">
        <p class="footer-email"><a href="mailto:gravelgodcoaching@gmail.com">gravelgodcoaching@gmail.com</a></p>
        <p class="footer-motto">Become what you could be.</p>
    </div>
</footer>

<script>
{get_nav_script()}
</script>

</body>
</html>'''
    
    return html


def generate_weekly_structure_rows(weekly_structure: str) -> str:
    """Parse weekly structure string into table rows."""
    if not weekly_structure:
        return '''<tr><td><strong>Monday</strong></td><td>Rest</td><td>—</td></tr>
<tr><td><strong>Tuesday</strong></td><td>Intensity</td><td>60-75 min</td></tr>
<tr><td><strong>Wednesday</strong></td><td>Endurance Z2</td><td>60-90 min</td></tr>
<tr class="g-spot-row"><td><strong>Thursday</strong></td><td>G Spot Work</td><td>60-75 min</td></tr>
<tr><td><strong>Friday</strong></td><td>Rest/Recovery</td><td>—</td></tr>
<tr><td><strong>Saturday</strong></td><td>Long Ride</td><td>2.5-4 hours</td></tr>
<tr><td><strong>Sunday</strong></td><td>Recovery/Skills</td><td>45-60 min</td></tr>'''
    
    rows = []
    # Parse format: "Monday: Rest | Tuesday: Intensity (60-75 min) | ..."
    days = weekly_structure.split('|')
    for day_str in days:
        day_str = day_str.strip()
        if ':' in day_str:
            day, rest = day_str.split(':', 1)
            rest = rest.strip()
            # Extract duration if in parentheses
            duration_match = re.search(r'\(([^)]+)\)', rest)
            if duration_match:
                duration = duration_match.group(1)
                session = rest.replace(f'({duration})', '').strip()
            else:
                session = rest
                duration = '—'
            
            row_class = ' class="g-spot-row"' if 'G Spot' in session else ''
            rows.append(f'<tr{row_class}><td><strong>{day.strip()}</strong></td><td>{session}</td><td>{duration}</td></tr>')
    
    return '\n'.join(rows) if rows else generate_weekly_structure_rows('')


# =============================================================================
# SECTION GENERATORS (Abbreviated for brevity - full content in production)
# =============================================================================

def generate_before_you_start_section(data: Dict[str, str]) -> str:
    """Generate Before You Start section."""
    return f'''<section class="section" id="before">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2>Before You Start</h2>
    </div>
    <div class="section-content">
        <h3>Health & Safety Check</h3>
        <div class="callout callout-danger">
            <div class="callout-title">You Need To Be Healthy Enough To Train</div>
            <p>Training puts considerable stress on your cardiovascular system, musculoskeletal system, and your body's ability to recover. Get a physical before starting this plan. Be confident you're healthy enough to handle the training load.</p>
        </div>
        
        <h3>Equipment Requirements</h3>
        <h4>Mandatory</h4>
        <ul>
            <li><strong>GPS bike computer</strong> — For tracking outdoor workouts and following routes</li>
            <li><strong>Power meter or heart rate monitor</strong> — You need objective data to execute workouts correctly</li>
            <li><strong>Bike fit</strong> — A poorly fitting bike will break you over 12 weeks and {data['DISTANCE']} miles</li>
            <li><strong>Indoor training setup</strong> — Smart trainer + fan at minimum</li>
            <li><strong>Reliable bike</strong> — Mechanically sound, appropriate tires for {data['RACE_NAME']}'s terrain</li>
        </ul>
        
        <h3>FTP Testing</h3>
        <p>Functional Threshold Power (FTP) is the cornerstone of this plan. All training zones are calculated as percentages of FTP. Wrong FTP = wrong zones = ineffective training.</p>
        <h4>When to test:</h4>
        <ul>
            <li><strong>Week 1:</strong> Establish baseline FTP</li>
            <li><strong>Week 6-7 (optional):</strong> Check progress</li>
            <li><strong>Week 11:</strong> Final test during taper</li>
        </ul>
    </div>
</section>'''


def generate_training_fundamentals_section(data: Dict[str, str]) -> str:
    """Generate Training Fundamentals section."""
    return '''<section class="section" id="how-training-works">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2>How Training Works</h2>
    </div>
    <div class="section-content">
        <h3>The Adaptation Cycle</h3>
        <p>All training follows the same basic cycle: <strong>Stress → Fatigue → Recovery → Adaptation</strong>.</p>
        
        <div class="card-grid">
            <div class="card">
                <h4>Step 1: Stress</h4>
                <p>You apply training stress—a hard workout that exceeds your current capacity. This creates disruption your body needs to solve.</p>
            </div>
            <div class="card">
                <h4>Step 2: Fatigue</h4>
                <p>Immediately after training, you're weaker than before. Fatigue is the signal that triggers adaptation.</p>
            </div>
            <div class="card">
                <h4>Step 3: Recovery</h4>
                <p>Given adequate rest, nutrition, and time, your body repairs and rebuilds stronger than before.</p>
            </div>
            <div class="card">
                <h4>Step 4: Adaptation</h4>
                <p>Supercompensation: your body builds more capacity than it had before to handle similar stress more easily next time.</p>
            </div>
        </div>
        
        <div class="callout callout-warning">
            <div class="callout-title">Where It Goes Wrong</div>
            <p><strong>Insufficient stress:</strong> Workout too easy, no adaptation triggered.<br>
            <strong>Insufficient recovery:</strong> New stress before recovery complete, accumulated fatigue without adaptation.<br>
            <strong>Inconsistent stress:</strong> Heroic efforts followed by weeks off—never compound adaptations.</p>
        </div>
    </div>
</section>'''


def generate_zones_section() -> str:
    """Generate Training Zones section."""
    return '''<section class="section" id="zones">
    <div class="section-header">
        <span class="section-number">05</span>
        <h2>Training Zones</h2>
    </div>
    <div class="section-content">
        <p>Zones exist to quantify intensity. But here's the paradox: <strong>the end goal is to develop a feeling for intensity.</strong></p>
        
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr><th>Zone</th><th>Name</th><th>% FTP</th><th>RPE</th><th>Feel</th></tr>
                </thead>
                <tbody>
                    <tr><td><strong>Z1</strong></td><td>Active Recovery</td><td>&lt;55%</td><td>1-2</td><td>Very easy, feels like nothing</td></tr>
                    <tr><td><strong>Z2</strong></td><td>Endurance</td><td>56-75%</td><td>3-4</td><td>All-day pace, can chat freely</td></tr>
                    <tr><td><strong>Z3</strong></td><td>Tempo</td><td>76-87%</td><td>5-6</td><td>Comfortably hard, short sentences</td></tr>
                    <tr class="g-spot-row"><td><strong>G SPOT</strong></td><td>Gravel Race Pace</td><td>88-92%</td><td>6-7</td><td>Uncomfortably sustainable</td></tr>
                    <tr><td><strong>Z4</strong></td><td>Threshold</td><td>93-105%</td><td>7-8</td><td>Hard, controlled, few words</td></tr>
                    <tr><td><strong>Z5</strong></td><td>VO2max</td><td>106-120%</td><td>9</td><td>Very hard, heavy breathing</td></tr>
                    <tr><td><strong>Z6</strong></td><td>Anaerobic</td><td>121-150%</td><td>10</td><td>All-out, 30 sec - 3 min max</td></tr>
                </tbody>
            </table>
        </div>
        
        <div class="callout callout-info">
            <div class="callout-title">Critical: Easy Means Easy</div>
            <p>Most people train too hard on easy days. Zone 2 should feel genuinely conversational. If you're breathing hard, you're in Z3. Fix this—it's the most common training mistake.</p>
        </div>
    </div>
</section>'''


def generate_execution_section() -> str:
    """Generate Workout Execution section."""
    return '''<section class="section" id="execution">
    <div class="section-header">
        <span class="section-number">06</span>
        <h2>Workout Execution</h2>
    </div>
    <div class="section-content">
        <h3>Universal Execution Rules</h3>
        <ol>
            <li><strong>Warm up properly</strong> — 15-20 minutes progressive before intensity</li>
            <li><strong>Do the actual workout</strong> — Not more, not less. Trust the plan.</li>
            <li><strong>Chase time-in-zone</strong> — Highest average across the set, not hero intervals</li>
            <li><strong>Stop if power drops >10%</strong> — Quality beats quantity</li>
        </ol>
        
        <h3>G Spot Execution (88-92% FTP)</h3>
        <p>This is gravel race pace—<em>uncomfortably sustainable</em>.</p>
        <ul>
            <li>Stay seated, control breathing</li>
            <li>Hard enough to hurt, easy enough to repeat</li>
            <li>Could talk in short phrases but wouldn't want to</li>
            <li>Fuel properly: 60-80g carbs/hour</li>
        </ul>
        
        <div class="callout callout-warning">
            <div class="callout-title">Common G Spot Mistake</div>
            <p>Starting at 95% FTP because "it doesn't feel that hard yet." By minute 30, you're dying. Start at 88% and build only if holding that feels too easy.</p>
        </div>
    </div>
</section>'''


def generate_recovery_section(data: Dict[str, str]) -> str:
    """Generate Recovery section."""
    return f'''<section class="section" id="recovery">
    <div class="section-header">
        <span class="section-number">07</span>
        <h2>Recovery</h2>
    </div>
    <div class="section-content">
        <h3>Recovery Makes You Fast</h3>
        <p>Training creates stress. Recovery creates adaptation. Skip recovery, skip adaptation.</p>
        
        <div class="card-grid">
            <div class="card">
                <h4>Sleep</h4>
                <p>7-9 hours minimum. This is when growth hormone peaks and muscles rebuild. Non-negotiable.</p>
            </div>
            <div class="card">
                <h4>Nutrition</h4>
                <p>Protein within 30 min post-workout. Carbs to replenish glycogen. Real food over supplements.</p>
            </div>
            <div class="card">
                <h4>Active Recovery</h4>
                <p>Easy spinning, walking, stretching. Movement promotes blood flow without adding stress.</p>
            </div>
            <div class="card">
                <h4>Recovery Weeks</h4>
                <p>Every 3-4 weeks, volume drops 30-40%. This is when adaptation consolidates. Don't skip.</p>
            </div>
        </div>
    </div>
</section>'''


def generate_strength_section(data: Dict[str, str]) -> str:
    """Generate Strength Training section."""
    return f'''<section class="section" id="strength">
    <div class="section-header">
        <span class="section-number">08</span>
        <h2>Strength Training</h2>
    </div>
    <div class="section-content">
        <h3>The Honest Take</h3>
        <p>Strength training makes you faster and keeps you healthy. But it's a long-term investment, not a quick fix.</p>
        
        <div class="callout callout-info">
            <div class="callout-title">During This 12-Week Block</div>
            <p><strong>Prioritize:</strong><br>
            • Mobility/stability work (non-negotiable)<br>
            • Basic core stability (highly recommended)<br>
            • Maintenance strength if you already lift</p>
        </div>
        
        <p>After {data['RACE_NAME']}, invest in a proper off-season strength block. Your future self—the one still racing at 50, 60, 70—will thank you.</p>
    </div>
</section>'''


def generate_skills_section(data: Dict[str, str]) -> str:
    """Generate Skills section with race-specific skill 5."""
    skill_5_html = ''
    if data.get('SKILL_5_NAME') and data['SKILL_5_NAME'] != 'Race-Specific Skill':
        skill_5_html = f'''
        <div class="skill-item">
            <h4>Skill 5: {data['SKILL_5_NAME']}</h4>
            <p><strong>Why:</strong> {data['SKILL_5_WHY']}</p>
            <p><strong>How:</strong> {data['SKILL_5_HOW']}</p>
            <p class="skill-cue">Cue: "{data['SKILL_5_CUE']}"</p>
        </div>'''
    
    skill_notes_html = ''
    if data.get('RACE_SPECIFIC_SKILL_NOTES'):
        skill_notes_html = f'''
        <h3>Race-Specific Skill Notes</h3>
        <p>{data['RACE_SPECIFIC_SKILL_NOTES']}</p>'''
    
    return f'''<section class="section" id="skills">
    <div class="section-header">
        <span class="section-number">09</span>
        <h2>Technical Skills for {data['RACE_NAME']}</h2>
    </div>
    <div class="section-content">
        <p>Fitness gets you to the race. Skills determine whether you use that fitness efficiently.</p>
        
        <div class="skills-grid">
            <div class="skill-item">
                <h4>Skill 1: Loose Surface Cornering</h4>
                <p>Look through the turn, weight your outside pedal, point inside knee toward the turn.</p>
                <p class="skill-cue">Cue: "Eyes through, weight down, knee out"</p>
            </div>
            <div class="skill-item">
                <h4>Skill 2: Eating While Riding</h4>
                <p>Practice on every long ride. Start flat, graduate to rough terrain.</p>
                <p class="skill-cue">Cue: "Flat road first, both hands work"</p>
            </div>
            <div class="skill-item">
                <h4>Skill 3: Group Riding</h4>
                <p>Smooth, predictable movements. No sudden braking or surging. Communicate.</p>
                <p class="skill-cue">Cue: "Smooth pulls, steady pace, speak up"</p>
            </div>
            <div class="skill-item">
                <h4>Skill 4: Descending on Loose Gravel</h4>
                <p>Weight back, elbows bent and loose, grip relaxed. Brake before turns, not during.</p>
                <p class="skill-cue">Cue: "Weight back, light hands, eyes up"</p>
            </div>
            {skill_5_html}
        </div>
        {skill_notes_html}
    </div>
</section>'''


def generate_fueling_section() -> str:
    """Generate Fueling & Hydration section."""
    return '''<section class="section" id="fueling">
    <div class="section-header">
        <span class="section-number">10</span>
        <h2>Fueling & Hydration</h2>
    </div>
    <div class="section-content">
        <h3>Quick Reference</h3>
        <div class="table-wrapper">
            <table>
                <thead><tr><th>Scenario</th><th>Carbs</th><th>Fluid</th><th>Notes</th></tr></thead>
                <tbody>
                    <tr><td>Pre-Ride (2-3hr before)</td><td>1-2g/kg</td><td>16-24 oz</td><td>Low fiber, familiar foods</td></tr>
                    <tr><td>Easy Ride (&lt;90 min)</td><td>0-30g/hr</td><td>16-24 oz/hr</td><td>Water usually sufficient</td></tr>
                    <tr><td>Long Ride (&gt;90 min)</td><td>60-80g/hr</td><td>24-32 oz/hr</td><td>Practice race products</td></tr>
                    <tr class="g-spot-row"><td><strong>Race Day</strong></td><td><strong>80-100g/hr</strong></td><td><strong>24-32 oz/hr</strong></td><td><strong>Nothing new!</strong></td></tr>
                    <tr><td>Hot Conditions (&gt;80°F)</td><td>Same</td><td>36-48 oz/hr</td><td>Add 500-1000mg sodium/hr</td></tr>
                </tbody>
            </table>
        </div>
        
        <h3>Training Your Gut</h3>
        <p>Your gut is trainable. Start at 40-50g/hr, increase by 10g every 2-3 weeks. By race day, you should handle 80-100g/hr comfortably.</p>
        
        <div class="callout callout-danger">
            <div class="callout-title">The Bonk is Real</div>
            <p>Under-fueling isn't grit—it's a guaranteed DNF around mile 120. Eat early, eat often, eat more than you think you need.</p>
        </div>
    </div>
</section>'''


def generate_mental_section() -> str:
    """Generate Mental Training section."""
    return '''<section class="section" id="mental">
    <div class="section-header">
        <span class="section-number">11</span>
        <h2>Mental Training</h2>
    </div>
    <div class="section-content">
        <h3>Three Tools That Work</h3>
        
        <div class="card-grid">
            <div class="card">
                <h4>6-2-7 Breathing</h4>
                <p>Inhale 6 seconds, hold 2, exhale 7. Triggers parasympathetic response, calms panic. Practice until automatic.</p>
            </div>
            <div class="card">
                <h4>Performance Statements</h4>
                <p>Pre-planned phrases that replace negative self-talk. "This is supposed to be hard." "Just get to the next aid station."</p>
            </div>
            <div class="card">
                <h4>Personal Highlight Reel</h4>
                <p>Mental movie of past success + race execution + crossing the finish. Triggers confident emotional state on demand.</p>
            </div>
        </div>
        
        <h3>Crisis Protocol</h3>
        <p>When things go wrong (they will): <strong>Breathe</strong> (3-5 cycles 6-2-7) → <strong>Statement</strong> (your most powerful one) → <strong>Action</strong> (smallest possible next step)</p>
    </div>
</section>'''


def generate_race_day_section(data: Dict[str, str]) -> str:
    """Generate Race Day section."""
    tactics_html = ''
    if data.get('RACE_SPECIFIC_TACTICS'):
        tactics_html = f'''
        <h3>{data['RACE_NAME']}-Specific Tactics</h3>
        <p>{data['RACE_SPECIFIC_TACTICS']}</p>'''
    
    aid_html = ''
    if data.get('AID_STATION_STRATEGY'):
        aid_html = f'''
        <h3>Aid Station Strategy</h3>
        <p>{data['AID_STATION_STRATEGY']}</p>'''
    
    return f'''<section class="section" id="race-day">
    <div class="section-header">
        <span class="section-number">12</span>
        <h2>Race Day</h2>
    </div>
    <div class="section-content">
        <h3>The Three-Act Structure</h3>
        <div class="table-wrapper">
            <table>
                <thead><tr><th>Phase</th><th>When</th><th>Your Job</th></tr></thead>
                <tbody>
                    <tr><td><strong>THE MADNESS</strong></td><td>0-90 min</td><td>Survive. Find sustainable group. Eat and drink while others forget.</td></tr>
                    <tr><td><strong>FALSE DAWN</strong></td><td>90 min - 3 hrs</td><td>Stay fueled. Contribute without overworking. Bank energy.</td></tr>
                    <tr><td><strong>THE PIPER</strong></td><td>3+ hrs to finish</td><td>Execute your plan while others fall apart. This is the race.</td></tr>
                </tbody>
            </table>
        </div>
        {tactics_html}
        {aid_html}
    </div>
</section>'''


def generate_race_specific_section(data: Dict[str, str]) -> str:
    """Generate Race-Specific Preparation section with non-negotiables."""
    # Build non-negotiables table rows
    nn_rows = []
    for i in range(1, 6):
        req = data.get(f'NON_NEG_{i}_REQUIREMENT', '')
        when = data.get(f'NON_NEG_{i}_BY_WHEN', '')
        why = data.get(f'NON_NEG_{i}_WHY', '')
        if req:
            nn_rows.append(f'<tr><td><strong>{req}</strong></td><td>{when}</td><td>{why}</td></tr>')
    
    nn_table = ''
    if nn_rows:
        nn_table = f'''<div class="table-wrapper">
            <table>
                <thead><tr><th>Requirement</th><th>By When</th><th>Why It Matters</th></tr></thead>
                <tbody>
{''.join(nn_rows)}
                </tbody>
            </table>
        </div>'''
    
    weather_html = ''
    if data.get('WEATHER_STRATEGY'):
        weather_html = f'''
        <h3>Weather Strategy</h3>
        <p>{data['WEATHER_STRATEGY']}</p>'''
    
    equipment_html = ''
    if data.get('EQUIPMENT_CHECKLIST'):
        equipment_html = f'''
        <h3>Equipment Checklist</h3>
        <p>{data['EQUIPMENT_CHECKLIST']}</p>'''
    
    return f'''<section class="section" id="race-specific">
    <div class="section-header">
        <span class="section-number">13</span>
        <h2>Race-Specific Preparation</h2>
    </div>
    <div class="section-content">
        <h3>The Non-Negotiables for {data['RACE_NAME']}</h3>
        <p>These aren't suggestions. Skip them and the course will expose the gap in your preparation.</p>
        {nn_table}
        {weather_html}
        {equipment_html}
    </div>
</section>'''


def generate_tires_section() -> str:
    """Generate Tires section."""
    return '''<section class="section" id="tires">
    <div class="section-header">
        <span class="section-number">14</span>
        <h2>Tires</h2>
    </div>
    <div class="section-content">
        <h3>The Decision Framework</h3>
        <p>Stop overthinking. Use this:</p>
        <ol>
            <li><strong>What width fits?</strong> When in doubt, go 38-42mm</li>
            <li><strong>What's durable?</strong> Ask people who've raced it</li>
            <li><strong>Can you test it?</strong> Mounted 2+ weeks before race day</li>
            <li><strong>Does it feel good?</strong> 3-4 hour test ride</li>
        </ol>
        
        <div class="callout callout-danger">
            <div class="callout-title">Common Mistakes</div>
            <p>• Buying new tires race week<br>
            • Chasing marginal gains over reliability<br>
            • Ignoring your own testing data</p>
        </div>
        
        <p><strong>The actual best tire</strong> is the one that gets you to the finish line without flatting and doesn't beat you up for 8 hours.</p>
    </div>
</section>'''


def generate_glossary_section() -> str:
    """Generate Glossary section."""
    return '''<section class="section" id="glossary">
    <div class="section-header">
        <span class="section-number">15</span>
        <h2>Glossary</h2>
    </div>
    <div class="section-content">
        <div class="glossary-grid">
            <div class="glossary-item">
                <div class="glossary-term">FTP (Functional Threshold Power)</div>
                <div class="glossary-def">Highest power you can sustain for ~1 hour. All zones calculated as % of FTP.</div>
            </div>
            <div class="glossary-item">
                <div class="glossary-term">TSS (Training Stress Score)</div>
                <div class="glossary-def">Training load based on duration × intensity. 100 TSS = 1 hour at FTP.</div>
            </div>
            <div class="glossary-item">
                <div class="glossary-term">G Spot (88-92% FTP)</div>
                <div class="glossary-def">Gravel race pace. Uncomfortably sustainable. Where you'll spend most of the race.</div>
            </div>
            <div class="glossary-item">
                <div class="glossary-term">RPE (Rate of Perceived Exertion)</div>
                <div class="glossary-def">1-10 scale of how hard effort feels. Trust RPE when devices conflict.</div>
            </div>
            <div class="glossary-item">
                <div class="glossary-term">Polarized Training</div>
                <div class="glossary-def">80% easy (Z1-Z2), 20% hard (Z4+), minimal middle zone.</div>
            </div>
            <div class="glossary-item">
                <div class="glossary-term">Taper</div>
                <div class="glossary-def">Volume drops 30-50% before race while intensity maintains. Arrive fresh.</div>
            </div>
            <div class="glossary-item">
                <div class="glossary-term">Bonk</div>
                <div class="glossary-def">Severe glycogen depletion. Prevention: eat early, eat often.</div>
            </div>
            <div class="glossary-item">
                <div class="glossary-term">Supercompensation</div>
                <div class="glossary-def">Body builds more capacity than before to handle similar stress more easily.</div>
            </div>
        </div>
    </div>
</section>'''


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def get_output_filename(race_name: str, plan_name: str, tier_name: str, ability: str) -> str:
    """Generate standardized output filename."""
    race_slug = re.sub(r'[^a-z0-9]+', '_', race_name.lower()).strip('_')
    plan_slug = re.sub(r'[^a-z0-9]+', '_', plan_name.lower()).strip('_')
    return f"{race_slug}_{plan_slug}_{tier_name.lower()}_{ability.lower()}_guide.html"


def main():
    parser = argparse.ArgumentParser(description='Generate Gravel God Training Guides')
    parser.add_argument('--race', required=True, help='Path to race JSON file')
    parser.add_argument('--plan', required=True, help='Path to plan JSON file')
    parser.add_argument('--output', help='Output HTML file path (auto-generated if not specified)')
    parser.add_argument('--output-dir', default='.', help='Output directory')
    
    args = parser.parse_args()
    
    # Load data
    print(f"Loading race data from: {args.race}")
    race_json = load_json(args.race)
    
    print(f"Loading plan data from: {args.plan}")
    plan_json = load_json(args.plan)
    
    # Extract data for placeholders
    race_data = extract_race_data(race_json)
    plan_data = extract_plan_data(plan_json)
    
    # Override tier/ability from plan if present
    if plan_data.get('PLAN_NAME'):
        # Infer tier from plan name
        plan_name = plan_data['PLAN_NAME'].upper()
        for tier in ['AYAHUASCA', 'FINISHER', 'COMPETE', 'PODIUM']:
            if tier in plan_name:
                race_data['TIER_NAME'] = tier.capitalize()
                break
        
        # Infer ability from plan name
        for ability in ['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'MASTERS']:
            if ability in plan_name:
                race_data['ABILITY_LEVEL'] = ability.capitalize()
                break
        
        # Get hours from plan metadata
        if plan_data.get('PLAN_TARGET_HOURS'):
            race_data['WEEKLY_HOURS'] = plan_data['PLAN_TARGET_HOURS']
    
    # Extract radar scores
    race = race_json.get('race', race_json)
    radar = race.get('radar_scores', {})
    radar_scores = {
        'elevation': radar.get('elevation', {}).get('score', 3),
        'length': radar.get('length', {}).get('score', 3),
        'technicality': radar.get('technicality', {}).get('score', 3),
        'climate': radar.get('climate', {}).get('score', 3),
        'altitude': radar.get('altitude', {}).get('score', 1),
        'adventure': radar.get('adventure', {}).get('score', 3),
    }
    
    # Generate HTML
    print("Generating HTML guide...")
    html = generate_guide_html(race_data, plan_data, radar_scores)
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        filename = get_output_filename(
            race_data['RACE_NAME'],
            plan_data.get('PLAN_NAME', 'plan'),
            race_data['TIER_NAME'],
            race_data['ABILITY_LEVEL']
        )
        output_path = os.path.join(args.output_dir, filename)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Guide generated: {output_path}")
    print(f"  Race: {race_data['RACE_NAME']}")
    print(f"  Plan: {plan_data.get('PLAN_NAME', 'Unknown')}")
    print(f"  Tier: {race_data['TIER_NAME']}")
    print(f"  Ability: {race_data['ABILITY_LEVEL']}")
    
    return output_path


if __name__ == '__main__':
    main()
