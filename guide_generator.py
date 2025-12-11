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

{generate_skills_section(data)}

{generate_fueling_section(data)}

{generate_mental_section()}

{generate_race_tactics_section(data)}

{generate_race_specific_section(data)}

{generate_race_week_section(data)}

{generate_women_section()}

{generate_faq_section()}

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
    """Generate Recovery section - NOTE: This is now part of Workout Execution, kept for backwards compatibility."""
    return f'''<section class="section" id="recovery" style="display:none;">
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
    """Generate Strength Training section - NOTE: This is now part of Training Fundamentals, kept for backwards compatibility."""
    return f'''<section class="section" id="strength" style="display:none;">
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
        <span class="section-number">07</span>
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


def generate_fueling_section(data: Dict[str, str]) -> str:
    """Generate Fueling & Hydration section with improved comprehensive content."""
    race_distance = data.get('DISTANCE', '200')
    race_duration = data.get('DURATION_ESTIMATE', '~13 hours')
    
    return f'''<section class="section" id="fueling">
    <div class="section-header">
        <span class="section-number">08</span>
        <h2>Fueling & Hydration</h2>
    </div>
    <div class="section-content">
        <p>You can have perfect training, a dialed bike, and excellent pacing strategy. None of it matters if you run out of fuel halfway through your race.</p>
        <p>Nutrition determines roughly 8% of your race result. That's the difference between finishing strong and crawling to the line.</p>
        <p>This chapter covers what to eat, when to eat it, and how to execute nutrition under race stress when your stomach is rebelling and your brain is too stupid to remember to eat.</p>
        
        <h3>Quick Reference: Fueling & Hydration Guidelines</h3>
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>Scenario</th>
                        <th>Carbohydrate Intake</th>
                        <th>Fluid Intake</th>
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Training Ride &lt; 2 hours</strong></td>
                        <td>30-45g/hour</td>
                        <td>500-750ml/hour</td>
                        <td>Water + electrolytes. Start fueling after 60 min if needed.</td>
                    </tr>
                    <tr>
                        <td><strong>Training Ride 2-4 hours</strong></td>
                        <td>45-60g/hour</td>
                        <td>500-750ml/hour</td>
                        <td>Mix of gels, bars, and real food. Practice your race nutrition.</td>
                    </tr>
                    <tr>
                        <td><strong>Long Training Ride 4-6 hours</strong></td>
                        <td>60-75g/hour</td>
                        <td>500-750ml/hour</td>
                        <td>Aggressive gut training. Test race-day nutrition strategy.</td>
                    </tr>
                    <tr>
                        <td><strong>Race Day ({race_distance} miles, {race_duration})</strong></td>
                        <td>60-90g/hour</td>
                        <td>500-750ml/hour</td>
                        <td>Start fueling in first 30 min. Mix multiple carb sources (glucose + fructose).</td>
                    </tr>
                    <tr>
                        <td><strong>Hot Conditions (&gt;80°F)</strong></td>
                        <td>60-90g/hour</td>
                        <td>750-1000ml/hour</td>
                        <td>Increase sodium to 500-700mg/hour. Pre-cool if possible.</td>
                    </tr>
                    <tr>
                        <td><strong>Cold Conditions (&lt;50°F)</strong></td>
                        <td>60-90g/hour</td>
                        <td>400-600ml/hour</td>
                        <td>Lower fluid needs, but still fuel aggressively. Warm fluids help.</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <hr />
        
        <h3>The Nutrition Reality Check</h3>
        <p>The cycling nutrition industry wants you to believe you need seventeen different products, each with proprietary blend ratios and specific timing windows measured in seconds.</p>
        <p>You don't.</p>
        <p>You need carbohydrates during exercise. You need protein and carbs after exercise. You need reasonable daily nutrition that supports training.</p>
        <p>That's 95% of it.</p>
        <p>Everything else is optimization you can worry about after you've nailed the basics.</p>
        
        <hr />
        
        <h3>Daily Nutrition for Training</h3>
        <p>Your body is either recovering from the last workout or preparing for the next one. Daily nutrition supports both.</p>
        
        <h4>The Foundation</h4>
        <p><strong>Protein: 1.6-2.2g per kg bodyweight</strong></p>
        <p>If you weigh 70kg (154 lbs), that's 112-154g protein per day.</p>
        <p><strong>Why it matters:</strong> Protein rebuilds muscle tissue damaged during training. Skimp on protein and you're just breaking yourself down without rebuilding.</p>
        <p><strong>Sources:</strong> Meat, fish, eggs, dairy, legumes, protein powder if you're lazy or vegan.</p>
        <p><strong>The rule:</strong> Spread it across the day. Four meals with 25-40g each beats one massive 150g post-workout shake.</p>
        
        <hr />
        
        <p><strong>Carbohydrates: 3-7g per kg bodyweight</strong> (depends on training volume)</p>
        <ul>
            <li>Easy training days (Z2 endurance): 3-4g/kg</li>
            <li>Hard training days (intervals, long rides): 5-7g/kg</li>
            <li>Rest days: 2-3g/kg</li>
        </ul>
        <p>If you weigh 70kg:<br />
        - Easy day: 210-280g carbs<br />
        - Hard day: 350-490g carbs<br />
        - Rest day: 140-210g carbs</p>
        <p><strong>Why it matters:</strong> Carbs fuel high-intensity work and restock glycogen. Train hard without adequate carbs and your intervals will suck.</p>
        <p><strong>Sources:</strong> Rice, potatoes, oats, bread, pasta, fruit. Real food first, gels and bars during rides only.</p>
        <p><strong>The rule:</strong> Match carb intake to training load. Don't carb-load on rest days. Don't under-fuel hard training blocks.</p>
        
        <hr />
        
        <p><strong>Fat: 0.8-1.2g per kg bodyweight</strong></p>
        <p>If you weigh 70kg, that's 56-84g fat per day.</p>
        <p><strong>Why it matters:</strong> Hormones, cell membranes, vitamin absorption, satiety. Fat doesn't fuel hard efforts but it's essential for recovery and health.</p>
        <p><strong>Sources:</strong> Olive oil, nuts, avocados, fatty fish, whole eggs, butter.</p>
        <p><strong>The rule:</strong> Don't fear fat. Don't gorge on fat. Keep it moderate and consistent.</p>
        
        <hr />
        
        <h4>Timing That Actually Matters</h4>
        <p><strong>Pre-workout (2-3 hours before)</strong></p>
        <p>If training hard (threshold, VO2max):<br />
        - 1-2g carbs per kg bodyweight<br />
        - Low fiber, low fat, moderate protein<br />
        - Example: Oatmeal with banana and honey, or toast with peanut butter</p>
        <p>If training easy (Z2 endurance):<br />
        - Eat normally, don't stress timing<br />
        - Can even train fasted if under 90 minutes</p>
        <p><strong>The rule:</strong> Hard sessions need fuel. Easy sessions are flexible.</p>
        
        <hr />
        
        <p><strong>During workout</strong></p>
        <p>Covered in detail below. Short version: 60-80g carbs per hour for rides over 90 minutes at moderate-to-high intensity.</p>
        
        <hr />
        
        <p><strong>Post-workout (0-90 minutes after)</strong></p>
        <p>If workout was long (2.5+ hours) AND hard, AND you have another hard session within 24-36 hours:<br />
        - 20-30g protein<br />
        - 1-1.5g carbs per kg bodyweight<br />
        - Liquid is fine (protein shake, chocolate milk)</p>
        <p>If workout was easy, short, or your next hard session is 48+ hours away:<br />
        - Just eat your next meal normally<br />
        - Recovery nutrition is optional</p>
        <p><strong>The rule:</strong> The more frequently you train hard, the more critical recovery nutrition becomes. If you're training once per day with easy sessions, skip the fancy recovery protocols and just eat dinner.</p>
        
        <hr />
        
        <h3>What About Supplements?</h3>
        <p>Most supplements are placebo at best, actively harmful at worst.</p>
        
        <h4>Worth taking:</h4>
        <p><strong>Vitamin D (if deficient, most people are): 2000-4000 IU daily</strong><br />
        - Supports bone health, immune function, recovery<br />
        - Get your levels tested, supplement accordingly</p>
        <p><strong>Creatine monohydrate: 5g daily</strong><br />
        - Improves high-intensity repeatability<br />
        - Useful for VO2max and sprint work<br />
        - Cheap, well-researched, safe</p>
        <p><strong>Caffeine: 3-6mg per kg bodyweight before hard sessions</strong><br />
        - Proven performance enhancer<br />
        - Coffee works, pills work, gels work<br />
        - Tolerance builds, cycle off occasionally</p>
        
        <h4>Maybe worth taking:</h4>
        <p><strong>Beta-alanine: 3-5g daily</strong><br />
        - Buffers lactate, helps with threshold work<br />
        - Takes 4+ weeks to build up<br />
        - Makes your face tingle (harmless but weird)</p>
        <p><strong>Beetroot juice/nitrates: 2-3 hours before hard efforts</strong><br />
        - Improves oxygen efficiency<br />
        - Modest gains (2-3%)<br />
        - Tastes like dirt</p>
        
        <h4>Not worth taking:</h4>
        <p><strong>BCAAs (branch chain amino acids):</strong> Complete waste if you eat adequate protein<br />
        <strong>Testosterone boosters:</strong> Scams<br />
        <strong>Fat burners:</strong> Scams with side effects<br />
        <strong>Recovery drinks with proprietary blends:</strong> Overpriced protein+carbs</p>
        <p><strong>The rule:</strong> If you're deficient in something (Vitamin D, iron), fix it. If you're considering a supplement to "optimize," ask yourself if you've already nailed sleep, nutrition basics, and training consistency. If not, fix those first.</p>
        
        <hr />
        
        <h3>Fueling During Workouts</h3>
        <p>This is where races are won or lost.</p>
        
        <h4>The 60-80g Carbs Per Hour Rule</h4>
        <p>For any ride over 90 minutes at moderate-to-high intensity (Z3+), you need <strong>60-80g of carbohydrates per hour.</strong></p>
        <p>Not 30g. Not 100g. 60-80g.</p>
        <p><strong>Why this number?</strong></p>
        <p>Your gut can absorb approximately 60g of glucose per hour through SGLT1 transporters. Add fructose (which uses different transporters) and you can push to 90g total. The sweet spot for most athletes is 70-75g per hour—enough to fuel hard efforts without GI distress.</p>
        <p><strong>What 70g of carbs looks like:</strong></p>
        <ul>
            <li><strong>Option 1:</strong> 3 gels (24g each) = 72g</li>
            <li><strong>Option 2:</strong> 2 bottles of sports drink (35g each) = 70g</li>
            <li><strong>Option 3:</strong> 2 bars (40g each) = 80g</li>
            <li><strong>Option 4:</strong> Mix of real food + gels + drink</li>
        </ul>
        <p><strong>The rule:</strong> Pick what your stomach tolerates. Train your gut to handle race-day fueling. Don't experiment on race day.</p>
        
        <hr />
        
        <h4>Workout-Specific Fueling</h4>
        <p><strong>Z2 Endurance Rides (2-4 hours)</strong></p>
        <ul>
            <li><strong>Intensity:</strong> Low enough to burn primarily fat</li>
            <li><strong>Fueling:</strong> 40-60g carbs per hour</li>
        </ul>
        <p>You can get away with less because you're not depleting glycogen rapidly. Real food works great here—PB&J sandwiches, bananas, bars.</p>
        <p>Practice eating solid food on long easy rides. This builds GI tolerance for race day.</p>
        
        <hr />
        
        <p><strong>Tempo/G Spot Rides (2-3 hours with sustained efforts)</strong></p>
        <ul>
            <li><strong>Intensity:</strong> Moderate-high, significant glycogen use</li>
            <li><strong>Fueling:</strong> 60-80g carbs per hour</li>
        </ul>
        <p>Start fueling at 30-45 minutes, not 90 minutes. By the time you feel hungry, you're already behind.</p>
        <p>Mix of liquids (faster absorption) and solids (more satisfying, prevents flavor fatigue).</p>
        
        <hr />
        
        <p><strong>Threshold/VO2max Sessions (60-90 minutes)</strong></p>
        <ul>
            <li><strong>Intensity:</strong> Very high but short duration</li>
            <li><strong>Fueling:</strong> Pre-workout meal sufficient, maybe one gel mid-session</li>
        </ul>
        <p>You're not depleting glycogen in 60 minutes. Don't overthink this. Hydrate normally, maybe take a gel at 45 minutes if going long.</p>
        
        <hr />
        
        <p><strong>Race Simulation Rides (4-6 hours with race-pace efforts)</strong></p>
        <ul>
            <li><strong>Intensity:</strong> Variable, high average</li>
            <li><strong>Fueling:</strong> 70-80g carbs per hour, practice race-day nutrition</li>
        </ul>
        <p>This is where you dial in your race fueling. Test different products, timing, combinations. Figure out what your stomach tolerates at race pace.</p>
        <p><strong>The rule:</strong> The longer and harder the ride, the more critical fueling becomes. Easy rides are forgiving. Race-pace efforts are not.</p>
        
        <hr />
        
        <h3>Hydration Protocols</h3>
        <p>You lose 0.5-2 liters of fluid per hour depending on temperature, humidity, and effort.</p>
        <p>Dehydration of 2-3% bodyweight impairs performance. For a 70kg rider, that's 1.4-2.1 liters—easily achievable in 2-3 hours of hard riding in heat.</p>
        
        <h4>How much to drink:</h4>
        <p><strong>Aim for: 500-750ml per hour (16-25 oz)</strong></p>
        <p>More in heat, less in cold. More when sweating heavily, less when not.</p>
        <p><strong>The rule:</strong> Drink to thirst, but don't ignore thirst. By the time you're thirsty, you're already mildly dehydrated.</p>
        
        <h4>What to drink:</h4>
        <ul>
            <li><strong>Short rides (&lt;90 min):</strong> Water is fine</li>
            <li><strong>Long rides (2+ hours):</strong> Electrolyte drink with sodium</li>
        </ul>
        <p>Sodium matters on long rides. You lose 500-1000mg sodium per hour through sweat. Sports drinks provide 200-400mg per bottle. Add salt tabs if racing in heat or you're a heavy/salty sweater.</p>
        <p>Don't overthink potassium, magnesium, or trace minerals. Sodium is 90% of what matters for performance.</p>
        
        <h4>How to verify your hydration strategy works:</h4>
        <p>Weigh yourself before and after long training rides. Every pound lost represents roughly 16 ounces of fluid deficit. If you're losing more than 2-3% of body weight during rides, you need to drink more.</p>
        <p><strong>Example:</strong> 150-lb athlete loses 5 lbs during a 4-hour ride. That's 3.3% body weight loss and 80 oz of fluid deficit. At 4 hours, that's only 20 oz/hour consumption—too low. Target should be 32+ oz/hour to stay within 2-3% loss.</p>
        <p>Do this calculation during training. Adjust your hydration strategy based on real data from your body. Don't guess.</p>
        
        <h4>How to know if you're a salty sweater:</h4>
        <p>After long training rides, do you see visible salt crystals on your kit or face? Do you crave salty foods immediately after rides? That's information. You need more sodium than average.</p>
        
        <hr />
        
        <h3>Cramping</h3>
        <p>Cramps are <strong>not</strong> caused by electrolyte deficiency (despite what the supplement industry tells you).</p>
        <p>Cramps are caused by <strong>neuromuscular fatigue</strong>—your muscles are tired and misfiring.</p>
        <p>Salt tabs might help by changing neuromuscular excitability, but they're not addressing the root cause. The real fix is better pacing and better training.</p>
        
        <hr />
        
        <h3>Training Your Gut</h3>
        <p>Your gut is trainable just like your muscles.</p>
        <p>If you never eat during training rides, your gut won't tolerate eating during races. You'll get nauseous, crampy, or shut down completely.</p>
        <p>The ability to absorb large amounts of carbohydrates while exercising improves with practice. If you've never consumed 80+ grams of carbs per hour during a ride, your first attempt will probably end in GI distress—bloating, cramping, or worse.</p>
        <p>Your gut needs practice absorbing carbs while blood flow is diverted to working muscles. This is a learned adaptation.</p>
        
        <h4>How to build GI tolerance:</h4>
        <p><strong>Weeks 1-4 (Base Phase):</strong><br />
        - Practice eating real food on easy rides<br />
        - 40-50g carbs per hour, mostly solid<br />
        - Build tolerance gradually</p>
        <p><strong>Weeks 5-8 (Build Phase):</strong><br />
        - Increase to 60-70g carbs per hour<br />
        - Mix of liquids and solids<br />
        - Practice eating at tempo pace</p>
        <p><strong>Weeks 9-10 (Peak Training):</strong><br />
        - Hit 70-80g carbs per hour<br />
        - Race nutrition only (gels, drink, bars you'll use on race day)<br />
        - Practice at race pace</p>
        <p><strong>Race Week:</strong><br />
        - Stick with what worked in training<br />
        - No new products<br />
        - Trust your gut (literally)</p>
        <p><strong>The rule:</strong> Your gut adapts to what you consistently ask it to do. If you train it to handle 70g carbs per hour, it will. If you never practice, race day will be miserable.</p>
        
        <h4>One trick that helps: Mix glucose and fructose sources</h4>
        <p>Research shows that combining glucose and fructose (ideally in a 2:1 ratio) allows your gut to absorb more total carbohydrates per hour than either source alone. Different transporters in the intestine handle each sugar, so using both increases total capacity.</p>
        <p>Many sports nutrition products are already formulated this way. Check the labels. If you're making your own drink mix, consider combining sources—like maltodextrin (glucose) with table sugar (glucose + fructose).</p>
        
        <hr />
        
        <h3>Race-Day Nutrition Strategy</h3>
        <p>Everything you practiced in training gets executed under stress.</p>
        
        <h4>Pre-Race Meal (3-4 hours before start)</h4>
        <p><strong>Goal:</strong> Top off glycogen, don't experiment</p>
        <p><strong>What to eat:</strong><br />
        - 2-3g carbs per kg bodyweight<br />
        - Moderate protein<br />
        - Low fat, low fiber<br />
        - Familiar foods only</p>
        <p><strong>Example for 70kg rider:</strong><br />
        - 2 cups oatmeal with banana and honey (140g carbs)<br />
        - OR 3 pieces toast with jam and peanut butter (120g carbs)<br />
        - OR large bowl of rice with eggs (130g carbs)</p>
        <p>Drink 500ml water with your meal.</p>
        <p><strong>What not to do:</strong><br />
        - Try the complimentary breakfast burrito with hot sauce<br />
        - Drink coffee if you don't normally drink coffee<br />
        - Eat significantly more or less than you practiced</p>
        
        <hr />
        
        <h4>Starting Line (30-60 minutes before start)</h4>
        <p>Take one gel (24g carbs) with 200ml water.</p>
        <p>This tops off your tank right before the effort begins. You're not adding meaningful glycogen at this point—you're just making sure blood glucose is stable as the race starts.</p>
        
        <hr />
        
        <h4>During the Race: The Fueling Timeline</h4>
        <p><strong>The most common mistake:</strong> waiting until you're hungry to start eating.</p>
        <p>By the time you feel hungry, your glycogen is already depleted and your brain is glucose-starved. You're in a hole you can't climb out of.</p>
        <p><strong>The execution framework:</strong></p>
        <p><strong>0-30 minutes:</strong><br />
        - Focus on pacing, positioning, settling in<br />
        - Sip on drink, don't force nutrition yet<br />
        - Heart rate is spiking, gut blood flow is reduced</p>
        <p><strong>30-60 minutes:</strong><br />
        - First gel or equivalent (24g carbs)<br />
        - Start your fueling clock<br />
        - Hydrate consistently</p>
        <p><strong>Every 45-60 minutes after:</strong><br />
        - Consume 60-80g carbs per hour in consistent intervals<br />
        - <strong>Example:</strong> Gel every 45 minutes (24g × 4 = 96g per 3 hours, averaging 32g per hour—too low, need drink or bars too)<br />
        - <strong>Better example:</strong> Gel every 30 minutes (24g × 2 = 48g per hour) + drink with 30g per hour = 78g total</p>
        <p><strong>Set a timer.</strong> Seriously. Your brain will be stupid. It will forget to eat. It will lie to you and say "I'm fine, I'll eat at the next aid station." The timer removes decision-making.</p>
        <p><strong>At aid stations:</strong><br />
        - Top off bottles<br />
        - Grab food if needed<br />
        - Keep moving</p>
        <p>Don't stop for 5 minutes eating a ham sandwich. Grab and go. You're not on a picnic.</p>
        
        <hr />
        
        <h3>When Your Stomach Rebels</h3>
        <p>It will. At some point in a long race, your gut will protest.</p>
        <p><strong>Why it happens:</strong></p>
        <p>High-intensity exercise diverts blood from your GI system to working muscles. Your gut slows down. Food sits there, undigested, making you feel like shit.</p>
        <p><strong>What to do:</strong></p>
        <p><strong>1. Back off intensity for 5-10 minutes</strong><br />
        - Drop to Z2 pace<br />
        - Let gut blood flow recover<br />
        - Allow stomach to catch up</p>
        <p><strong>2. Switch to liquid calories temporarily</strong><br />
        - Easier to digest than solids<br />
        - Sports drink or cola at aid stations<br />
        - Gels if you can tolerate them</p>
        <p><strong>3. Small sips, not big gulps</strong><br />
        - Easier on the stomach<br />
        - Less sloshing</p>
        <p><strong>4. Don't panic and stop eating entirely</strong><br />
        - You'll bonk 30 minutes later<br />
        - Maintain some carb intake even if reduced</p>
        <p><strong>What not to do:</strong></p>
        <p>Hammer harder while nauseous. You'll either vomit or shut down completely.</p>
        <p><strong>The rule:</strong> Gut distress is your body telling you to back off intensity. Listen for 10 minutes, then resume pace once stomach settles.</p>
        
        <hr />
        
        <h3>The Reality Check on Fueling</h3>
        <p>Most athletes under-fuel during long events. Not because they don't know better—because it's hard.</p>
        <p>At mile 100, eating another gel might make you gag. Your stomach might feel full. You might not feel hungry. None of that changes the math: you're burning calories faster than you're consuming them, and eventually the tank will hit empty.</p>
        <p><strong>The solution:</strong> Treat fueling as a non-negotiable task, not an optional one based on hunger.</p>
        <p>Set a timer on your bike computer. Every 20 minutes: consume calories. Every 15 minutes: drink. Make it automatic. Don't wait until you feel hungry or thirsty—by then, you're already behind.</p>
        <p>This is why practice matters. By race day, eating and drinking on schedule should feel like shifting gears—just something you do without thinking about it.</p>
        
        <hr />
        
        <h3>Weight Management vs Performance</h3>
        <p>You want to be lean for racing. Lighter climbs easier. Lower body fat improves power-to-weight ratio.</p>
        <p>But chasing leanness during a training block is self-sabotage.</p>
        
        <h4>The Training Block Rule</h4>
        <p>During your 12-week build, your job is to train hard and recover well. Not cut weight.</p>
        <p><strong>Why?</strong></p>
        <p>Energy deficit impairs recovery. Under-fueled training produces inferior workouts. You're trying to build fitness, not starve yourself into a smaller body.</p>
        <p><strong>The hierarchy:</strong><br />
        1. Train consistently and well<br />
        2. Recover fully<br />
        3. Maintain current weight or gain slightly</p>
        <p>If you finish your 12 weeks 2kg heavier but significantly fitter, you did it right.</p>
        
        <h4>When to Cut Weight</h4>
        <p>After your race. During the off-season. When training volume is low and intensity is moderate.</p>
        <p>A 500-calorie daily deficit over 8-12 weeks can drop 4-6kg without destroying your fitness. Do this between racing seasons, not during them.</p>
        <p><strong>The rule:</strong> You can be lean or you can be fast. Pick one per season. Most of the time, pick fast.</p>
        
        <h4>Body Composition Reality Check</h4>
        <p>Optimal racing weight is highly individual. Some athletes race well at 8% body fat. Others race well at 14%.</p>
        <p>There is no universal "race weight."</p>
        <p><strong>What matters:</strong> power-to-weight ratio. If your FTP is 300W at 75kg (4.0 W/kg) and you cut to 70kg but your FTP drops to 280W (also 4.0 W/kg), you gained nothing and probably lost durability.</p>
        <p><strong>The rule:</strong> Chase performance metrics, not scale numbers. If your FTP and climbing times improve, your weight is fine. If they're declining, eat more.</p>
        
        <hr />
        
        <h3>The Bottom Line</h3>
        <p>Nutrition determines 8% of your race result. That's significant but not worth obsessing over.</p>
        <p><strong>Daily nutrition:</strong> Match carbs to training load. Get adequate protein. Don't fear fat. Eat real food.</p>
        <p><strong>Supplements:</strong> Vitamin D if deficient, creatine for high-intensity work, caffeine before hard sessions. Everything else is optional or snake oil.</p>
        <p><strong>During training:</strong> Practice eating 60-80g carbs per hour on long rides. Train your gut like you train your legs.</p>
        <p><strong>Race day:</strong> Eat a familiar pre-race meal 3-4 hours before. Start fueling at 30-45 minutes into the race. Hit 70g carbs per hour consistently. Set a timer so your stupid race brain doesn't forget.</p>
        <p><strong>When your stomach rebels:</strong> Back off intensity for 10 minutes and switch to liquids. Don't stop eating entirely.</p>
        <p><strong>Weight management:</strong> Happens in the off-season, not during training blocks. Chase performance, not scale numbers.</p>
        <p>Get the basics right. Execute consistently. That's 95% of nutrition.</p>
    </div>
</section>'''


def generate_mental_section() -> str:
    """Generate Mental Training section."""
    return '''<section class="section" id="mental">
    <div class="section-header">
        <span class="section-number">09</span>
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


def generate_race_tactics_section(data: Dict[str, str]) -> str:
    """Generate Race Tactics section."""
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
    
    return f'''<section class="section" id="race-tactics">
    <div class="section-header">
        <span class="section-number">10</span>
        <h2>Race Tactics</h2>
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
        <span class="section-number">11</span>
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


def generate_race_week_section(data: Dict[str, str]) -> str:
    """Generate Race Week Protocol section."""
    return f'''<section class="section" id="race-week">
    <div class="section-header">
        <span class="section-number">12</span>
        <h2>Race Week Protocol</h2>
    </div>
    <div class="section-content">
        <h3>The Taper</h3>
        <p>Volume drops 30-50% while intensity maintains. The goal: arrive fresh, not flat.</p>
        <p><strong>Week 11:</strong> 60-70% volume, maintain intensity, one hard session mid-week</p>
        <p><strong>Week 12:</strong> 40-50% volume, maintain intensity, one short hard session 3-4 days before race</p>
        <p><strong>Last 3 days:</strong> Easy spinning only, 30-60 minutes max. No intensity. No long rides.</p>
        
        <h3>Travel & Logistics</h3>
        <p>If traveling to the race:</p>
        <ul>
            <li>Arrive 2-3 days early if possible (time zone adjustment, course preview)</li>
            <li>Pack bike carefully—check it twice</li>
            <li>Bring backup equipment (tubes, chain, derailleur hanger)</li>
            <li>Test bike immediately upon arrival</li>
            <li>Stick to familiar foods—don't experiment with local cuisine</li>
        </ul>
        
        <h3>Final Preparation</h3>
        <p><strong>3-4 days before:</strong> Final equipment check, tire pressure test, nutrition plan finalized</p>
        <p><strong>2 days before:</strong> Easy 30-45 min spin, final bike check, pack race bag</p>
        <p><strong>1 day before:</strong> Course preview if possible (drive or easy spin), final nutrition prep, early dinner</p>
        <p><strong>Race morning:</strong> Familiar breakfast 3-4 hours before start, arrive 60-90 minutes early, warm up 15-20 minutes</p>
        
        <div class="callout callout-warning">
            <div class="callout-title">Race Week Mistakes</div>
            <p>• Trying to "make up" for missed training<br>
            • Testing new equipment or nutrition<br>
            • Overthinking everything<br>
            • Not sleeping enough<br>
            • Changing your routine</p>
        </div>
        
        <p><strong>The rule:</strong> Race week is about execution, not fitness. You've done the work. Now trust it.</p>
    </div>
</section>'''


def generate_women_section() -> str:
    """Generate Women-Specific Considerations section."""
    return '''<section class="section" id="women-specific">
    <div class="section-header">
        <span class="section-number">13</span>
        <h2>Women-Specific Considerations</h2>
    </div>
    <div class="section-content">
        <p>If you're a woman training for gravel racing, your physiology is different from men's in ways that actually affect training and performance. This isn't patronizing "girl power" bullshit—it's honest acknowledgment of real differences that matter.</p>
        <p>The good news: these differences are trainable and manageable. The bad news: if you ignore them, you're making things harder than they need to be.</p>
        
        <h3>Menstrual Cycle & Training</h3>
        <p>Your menstrual cycle affects training capacity. Not as an excuse to skip workouts, but as a variable to monitor and work with.</p>
        
        <h4>Follicular Phase (Days 1-14, from start of period to ovulation)</h4>
        <p><strong>What's happening:</strong> Estrogen rises, body temperature is lower, insulin sensitivity is higher.</p>
        <p><strong>Training impact:</strong> This is typically your power window. You'll recover faster, handle intensity better, and feel stronger. Days 5-14 are often your best training days of the month.</p>
        <p><strong>How to use it:</strong> Schedule your hardest interval sessions, longest rides, and FTP tests during this phase when possible. Your body is primed for high-quality work.</p>
        
        <h4>Luteal Phase (Days 15-28, from ovulation to next period)</h4>
        <p><strong>What's happening:</strong> Progesterone dominates, body temperature rises (~0.5°F), metabolism shifts toward fat burning, inflammation increases.</p>
        <p><strong>Training impact:</strong> Recovery takes longer. Interval quality might decline. You might feel flat even when doing everything right. Heart rate runs 5-10 bpm higher at same effort. Carb cravings increase (because your body actually needs more carbs—progesterone reduces glycogen storage efficiency).</p>
        <p><strong>How to use it:</strong> This is not the time to test FTP or push for breakthrough sessions. Focus on base miles, maintenance intervals, and recovery. Listen to your body more carefully. If Week 8 falls during late luteal phase and you feel like garbage despite perfect execution, that's normal—it's hormones, not fitness loss.</p>
        
        <h4>Iron Considerations</h4>
        <p><strong>Monthly blood loss means monthly iron loss.</strong> Women who menstruate need roughly 18mg of iron daily (vs. 8mg for men). Athletes need even more due to foot-strike hemolysis, GI losses, and increased red blood cell turnover.</p>
        <p><strong>Low iron = compromised training:</strong> Fatigue, inability to hit power targets, poor recovery, elevated heart rate, shortness of breath during efforts you should handle easily.</p>
        <p><strong>The fix:</strong></p>
        <ul>
            <li>Get bloodwork annually (ferritin, serum iron, hemoglobin, hematocrit)</li>
            <li>Target ferritin >50 ng/mL for athletes (many docs say >15 is "normal"—that's too low for performance)</li>
            <li>Iron-rich foods: red meat, dark leafy greens, lentils, fortified cereals</li>
            <li>Consider supplementation if levels are low (but get tested first—too much iron is also a problem)</li>
            <li>Take iron with vitamin C (aids absorption), avoid taking with calcium (blocks absorption)</li>
        </ul>
        <p><strong>Your period is not an excuse to skip workouts, but it IS a variable to monitor.</strong> Track your cycle. Notice patterns. Adjust expectations during luteal phase. Capitalize on follicular phase. This is performance optimization, not weakness.</p>
        
        <h3>Fueling Differences</h3>
        <p>Women's bodies process fuel differently than men's, especially during exercise.</p>
        
        <h4>Carbohydrate Needs</h4>
        <p><strong>Women need MORE carbs relative to body weight than men.</strong> Despite often being told to eat less, female athletes actually need aggressive carbohydrate intake to support training and maintain hormonal health.</p>
        <p><strong>Why:</strong> Women's bodies preferentially spare carbohydrate and burn more fat at rest. Sounds great, except during high-intensity efforts (which is most of gravel racing), you NEED carbs. If you're chronically under-fueling carbs, your body will:</p>
        <ul>
            <li>Downregulate thyroid function (slower metabolism, more fatigue)</li>
            <li>Disrupt menstrual cycle (late periods, missed periods, longer cycles)</li>
            <li>Compromise bone density</li>
            <li>Tank performance</li>
        </ul>
        <p><strong>The target for training:</strong> 5-7g carbs per kg body weight on training days. More on long ride days (7-10g/kg).</p>
        <p><strong>The target for racing:</strong> 60-90g carbs per hour minimum. Don't under-fuel trying to "stay lean"—that strategy kills performance AND health.</p>
        
        <h4>Fat Oxidation Reality</h4>
        <p>Women burn more fat than men at the same relative intensity. This is often presented as an advantage. It's not.</p>
        <p><strong>The problem:</strong> Fat oxidation rates are too slow to fuel high-intensity efforts. During threshold work, VO2max intervals, or surges in a gravel race, you're burning mostly carbs. If you've under-fueled carbs chronically, you don't have the glycogen stores to support these efforts.</p>
        <p><strong>The fix:</strong> Don't confuse "burns more fat at rest" with "can rely on fat during racing." Fuel your training with adequate carbs. Train your gut to absorb 80-90g carbs/hour. On race day, hit those targets aggressively.</p>
        
        <h4>The "Lean" Trap</h4>
        <p>There's enormous pressure on women to be lean. Social pressure, cultural pressure, sometimes even from coaches who should know better.</p>
        <p>Here's reality: <strong>chronic under-fueling destroys performance and health.</strong> Low energy availability (RED-S: Relative Energy Deficiency in Sport) causes:</p>
        <ul>
            <li>Hormonal disruption (irregular or absent periods)</li>
            <li>Bone density loss (stress fractures, long-term osteoporosis risk)</li>
            <li>Immune system suppression (sick all the time)</li>
            <li>Psychological issues (mood, anxiety, obsessive thoughts about food)</li>
            <li>Performance decline (despite "looking fit")</li>
        </ul>
        <p><strong>The rule:</strong> Fuel your training. Chase performance, not a number on the scale. If your periods stop or become irregular, you're under-fueling. Fix it immediately.</p>
        
        <h3>Bone Health</h3>
        <p>Women are at higher risk for stress fractures and osteoporosis, especially if under-fueling or over-training.</p>
        <p><strong>Protect your bones:</strong></p>
        <ul>
            <li>Adequate calcium (1000-1300mg daily from food, not just supplements)</li>
            <li>Vitamin D (2000-4000 IU daily if deficient)</li>
            <li>Weight-bearing exercise (strength training, not just cycling)</li>
            <li>Adequate energy availability (fuel your training)</li>
        </ul>
        <p>If you've had stress fractures or have a family history of osteoporosis, get a DEXA scan. Know your baseline. Monitor it.</p>
        
        <h3>The Bottom Line</h3>
        <p>Your physiology is different. That's not a weakness—it's a variable to work with.</p>
        <p>Track your cycle. Fuel aggressively. Monitor iron. Protect bone health. Adjust training expectations during luteal phase. Capitalize on follicular phase.</p>
        <p>This isn't about making excuses. It's about optimizing performance within the reality of your body.</p>
            </div>
</section>'''


def generate_faq_section() -> str:
    """Generate FAQ section."""
    return '''<section class="section" id="faq">
    <div class="section-header">
        <span class="section-number">14</span>
        <h2>Frequently Asked Questions</h2>
            </div>
    <div class="section-content">
        <h3>Q: What if I miss a week of training?</h3>
        <p><strong>A:</strong> One week won't kill you. Jump back in where the plan currently is—don't try to "make up" missed work. Forward progress only. If you missed two+ weeks due to illness or injury, reassess whether your race timeline is realistic.</p>
        
        <hr />
        
        <h3>Q: Can I do this plan entirely on Zwift/TrainerRoad/indoors?</h3>
        <p><strong>A:</strong> Technically yes, but you're missing critical skills development. Indoor training builds fitness, but outdoor riding builds handling, pacing, and mental resilience. Do at least 30-40% of your volume outside, especially long rides.</p>
        
        <hr />
        
        <h3>Q: What if my FTP changes mid-plan?</h3>
        <p><strong>A:</strong> Test again at Week 6-7 if you're curious, but only adjust zones if FTP changed by 5+ watts. Small fluctuations are noise. Major changes (10+ watts) mean you need to recalculate zones and adjust your workout targets accordingly.</p>
        
        <hr />
        
        <h3>Q: How do I know if I'm overtraining?</h3>
        <p><strong>A:</strong> Elevated resting heart rate, persistent fatigue, declining performance, irritability, poor sleep, loss of motivation. If you're hitting 3+ of these symptoms, take 2-3 days completely off, then return at reduced volume. Recovery makes you fast.</p>
        
        <hr />
        
        <h3>Q: What if I can't hit the prescribed watts?</h3>
        <p><strong>A:</strong> Either your FTP is set too high, or you're under-recovered. Take an extra rest day, retest FTP if needed. Don't grind through workouts at the wrong intensity—that's junk miles that compromise adaptation.</p>
        
        <hr />
        
        <h3>Q: Should I follow the plan exactly or can I move workouts around?</h3>
        <p><strong>A:</strong> Follow the plan as written. The order isn't random—it assumes a typical M-F work schedule with weekends for long rides. Hard days are spaced for optimal recovery. If you work nights or have a non-standard schedule, shift the entire week forward/backward as needed, but don't rearrange individual workouts.</p>
        
        <hr />
        
        <h3>Q: How much weight will I lose during this plan?</h3>
        <p><strong>A:</strong> Your mileage may vary. Know this: losing weight and fueling performance are often in conflict. Any meaningful, long-lasting attempt to lose weight should be undertaken in the off-season, NOT during build-up to an eating contest on a bike (which is what a gravel race is). Fuel your training properly or accept compromised results.</p>
        
        <hr />
        
        <h3>Q: Can I do other sports while following this plan?</h3>
        <p><strong>A:</strong> Light activity (yoga, walking, easy swimming) is fine. Running, CrossFit, or other high-intensity sports will compromise your cycling training. Pick one goal. You can't serve two masters and expect peak performance from either.</p>
        
        <hr />
        
        <h3>Q: What if I get sick during training?</h3>
        <p><strong>A:</strong> Above the neck (head cold): reduce intensity by one zone, monitor closely. Below the neck (chest, stomach): skip the workout entirely. Don't be a hero—training while sick extends recovery time and risks turning a minor illness into something serious.</p>
        
        <hr />
        
        <h3>Q: How do I taper if my race date changes?</h3>
        <p><strong>A:</strong> If race moves earlier: condense taper to 1 week, keep intensity but cut volume by 40%. If race moves later: add 1-2 weeks of maintenance (same intensity, 60-70% volume), then taper normally. Don't panic and overtrain.</p>
        
        <hr />
        
        <h3>Q: Is this plan suitable for [other race] instead of the target race?</h3>
        <p><strong>A:</strong> Maybe. If the race is similar duration (8-15 hours) and demands (sustained gravel endurance), yes. If it's significantly different (shorter, hillier, more technical), you'll need modifications. The fitness transfers, but race-specific skills don't.</p>
        
        <hr />
        
        <h3>Q: What if I don't have access to gravel roads for training?</h3>
        <p><strong>A:</strong> Use what you have. Road riding builds fitness. Fitness translates to gravel. You'll need at least a few gravel rides (weeks 6-10) to dial in handling and equipment, but the bulk of fitness work can be done on pavement. Don't use lack of gravel as an excuse to skip training.</p>
        
        <hr />
        
        <h3>Q: Should I train with a group or solo?</h3>
        <p><strong>A:</strong> Both. Solo for structured intervals (better execution, no distractions). Group for long rides (mental training, pacing practice, working with others). Mix it up based on the workout goal. Don't let your training partners dictate your training stress.</p>
        
        <hr />
        
        <h3>Q: What's the minimum equipment I need to start this plan today?</h3>
        <p><strong>A:</strong> A bike that fits and works. Power meter (required for this plan). Heart rate chest strap (required for backup). That's it. Everything else—fancy computers, carbon wheels, aero bars—can be figured out over 12 weeks. Stop shopping and start training.</p>
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
