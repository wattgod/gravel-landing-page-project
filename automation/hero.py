"""
Gravel God Hero Section Generator

SINGLE SOURCE OF TRUTH for Hero section HTML.
This module enforces correct badge colors and score card structure.

CRITICAL RULES:
- Badge colors: Turquoise (#4ECDC4) per design system
- Tier badge: Tag-shaped with angled clip-path
- Location badge: State-shaped (user provides shape)
- Score card: Proper progress bar widths (percentage of 50)
- All colors from approved palette

Usage:
    from hero import generate_hero_html
    
    html = generate_hero_html(race_data)
"""

from typing import Dict, List


# Gravel God Color Palette (Hero-specific)
COLOR_PALETTE = {
    'turquoise': '#4ECDC4',           # Badge backgrounds
    'yellow': '#F4D03F',              # Text shadows, accents
    'cream': '#F5F5DC',               # Light text
    'brown_dark': '#59473C',          # Primary text
    'brown_medium': '#8C7568',        # Secondary elements
    'black': '#2C2C2C',               # Borders, shadows
    'white': '#FFFFFF',               # Backgrounds
    'light_gray': '#F0F0F0'           # Progress bar tracks
}


def calculate_percentage(score: int, max_score: int = 50) -> int:
    """
    Calculate percentage for progress bars.
    
    Args:
        score: Actual score (0-50)
        max_score: Maximum possible score (default 50)
        
    Returns:
        Percentage as integer (0-100)
    """
    if max_score == 0:
        return 0
    return int((score / max_score) * 100)


def validate_hero_data(data: Dict) -> List[str]:
    """
    Validate hero section data structure.
    
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Check top-level structure
    if 'race' not in data:
        errors.append("Missing 'race' key in data")
        return errors
    
    race = data['race']
    
    # Check required race fields
    required_race_fields = ['display_name', 'tagline', 'vitals', 'gravel_god_rating']
    for field in required_race_fields:
        if field not in race:
            errors.append(f"Missing required race field: '{field}'")
    
    # Check vitals
    if 'vitals' in race:
        if 'location_badge' not in race['vitals']:
            errors.append("Missing 'location_badge' in vitals")
    
    # Check rating structure
    if 'gravel_god_rating' in race:
        rating = race['gravel_god_rating']
        required_rating_fields = {
            'tier_label': str,
            'overall_score': int,
            'course_profile': int,
            'biased_opinion': int
        }
        
        for field, expected_type in required_rating_fields.items():
            if field not in rating:
                errors.append(f"Missing rating field: '{field}'")
            elif not isinstance(rating[field], expected_type):
                errors.append(f"Rating field '{field}' should be {expected_type.__name__}")
        
        # Validate score ranges
        if 'overall_score' in rating:
            if not (0 <= rating['overall_score'] <= 100):
                errors.append("overall_score must be between 0 and 100")
        
        if 'course_profile' in rating:
            if not (0 <= rating['course_profile'] <= 50):
                errors.append("course_profile must be between 0 and 50")
        
        if 'biased_opinion' in rating:
            if not (0 <= rating['biased_opinion'] <= 50):
                errors.append("biased_opinion must be between 0 and 50")
    
    return errors


def generate_hero_html(data: Dict) -> str:
    """
    Generate hero section HTML with validated colors and structure.
    
    The hero section shows race name, location, tier, and overall score with breakdown.
    
    Args:
        data: Race data dict with 'race' key containing all hero data
        
    Returns:
        Complete HTML string with <div> and <style> tags
        
    Raises:
        KeyError: If required data structure is missing
        
    Example:
        >>> race_data = {
        ...     'race': {
        ...         'display_name': 'Unbound 200',
        ...         'tagline': 'The Flint Hills will break you',
        ...         'vitals': {'location_badge': 'EMPORIA, KANSAS'},
        ...         'gravel_god_rating': {
        ...             'tier_label': 'TIER 1',
        ...             'overall_score': 87,
        ...             'course_profile': 44,
        ...             'biased_opinion': 43
        ...         }
        ...     }
        ... }
        >>> html = generate_hero_html(race_data)
    """
    # Extract hero data
    race = data['race']
    rating = race['gravel_god_rating']
    
    # Validate required fields
    errors = validate_hero_data(data)
    if errors:
        raise KeyError(f"Hero data validation failed:\n" + "\n".join(f"  - {e}" for e in errors))
    
    # Calculate percentages for progress bars
    course_pct = calculate_percentage(rating['course_profile'], 50)
    opinion_pct = calculate_percentage(rating['biased_opinion'], 50)
    
    # Hero HTML structure
    hero_html = f"""<div class="gg-hero-inner">
  <div class="gg-hero-left">
    <div class="gg-hero-badges">
      <span class="gg-hero-badge gg-hero-badge-tier">{rating['tier_label']}</span>
      <span class="gg-hero-badge gg-hero-badge-loc">{race['vitals']['location_badge']}</span>
    </div>
    <div class="gg-hero-title">{race['display_name']}</div>
    <div class="gg-hero-quote">{race['tagline']}</div>
  </div>
  
  <div class="gg-hero-right">
    <div class="gg-hero-score-card">
      <div class="gg-hero-score-label">Gravel God Rating</div>
      <div class="gg-hero-score-main">{rating['overall_score']}<span>/100</span></div>
      <div class="gg-hero-score-sub">{rating['tier_label']} · Iconic · High Consequence</div>
      
      <div class="gg-hero-score-breakdown">
        <div class="gg-hero-score-break-row">
          <span class="gg-hero-break-label">Course Profile</span>
          <div class="gg-hero-break-bar">
            <div class="gg-hero-break-fill" style="width: {course_pct}%;"></div>
          </div>
          <span class="gg-hero-break-score">{rating['course_profile']} / 50</span>
        </div>
        
        <div class="gg-hero-score-break-row">
          <span class="gg-hero-break-label">Biased Opinion</span>
          <div class="gg-hero-break-bar">
            <div class="gg-hero-break-fill" style="width: {opinion_pct}%;"></div>
          </div>
          <span class="gg-hero-break-score">{rating['biased_opinion']} / 50</span>
        </div>
        
        <div class="gg-hero-final-row">
          <span>Final Score</span>
          <span class="gg-hero-final-score">{rating['overall_score']} / 100</span>
        </div>
      </div>
      
      <div class="gg-hero-score-caption">
        Score based on Gravel God radar + editorial bias.
      </div>
    </div>
  </div>
</div>"""
    
    # Style block with enforced colors
    style_html = f"""<style>
/* Hero Section */
.gg-hero-inner {{
  display: flex;
  flex-wrap: wrap;
  gap: 48px;
  padding: 48px 24px;
}}

.gg-hero-left {{
  flex: 1;
  min-width: 300px;
}}

.gg-hero-right {{
  flex: 0 0 400px;
  min-width: 300px;
}}

/* Badges */
.gg-hero-badges {{
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}}

.gg-hero-badge {{
  display: inline-block;
  background: {COLOR_PALETTE['turquoise']};  /* ENFORCED: Turquoise per design system */
  color: {COLOR_PALETTE['black']};
  padding: 12px 20px;
  border: 3px solid {COLOR_PALETTE['black']};
  font-family: 'Sometype Mono', monospace;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  box-shadow: 4px 4px 0 {COLOR_PALETTE['black']};
}}

.gg-hero-badge-tier {{
  clip-path: polygon(0% 0%, 85% 0%, 100% 100%, 0% 100%);  /* Tag shape */
}}

/* Title and Quote */
.gg-hero-title {{
  font-family: 'Sometype Mono', monospace;
  font-size: 48px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: {COLOR_PALETTE['brown_dark']};
  margin: 0 0 16px 0;
  line-height: 1.1;
}}

.gg-hero-quote {{
  font-family: 'Sometype Mono', monospace;
  font-size: 18px;
  line-height: 1.6;
  color: {COLOR_PALETTE['brown_medium']};
  font-style: italic;
}}

/* Score Card */
.gg-hero-score-card {{
  background: {COLOR_PALETTE['white']};
  border: 3px solid {COLOR_PALETTE['black']};
  border-radius: 8px;
  padding: 32px;
  box-shadow: 8px 8px 0 {COLOR_PALETTE['black']};
}}

.gg-hero-score-label {{
  font-family: 'Sometype Mono', monospace;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: {COLOR_PALETTE['brown_medium']};
  margin-bottom: 8px;
}}

.gg-hero-score-main {{
  font-family: 'Sometype Mono', monospace;
  font-size: 64px;
  font-weight: 700;
  color: {COLOR_PALETTE['brown_dark']};
  line-height: 1;
  margin-bottom: 8px;
}}

.gg-hero-score-main span {{
  font-size: 32px;
  color: {COLOR_PALETTE['brown_medium']};
}}

.gg-hero-score-sub {{
  font-family: 'Sometype Mono', monospace;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: {COLOR_PALETTE['brown_medium']};
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 2px solid {COLOR_PALETTE['brown_medium']};
}}

/* Score Breakdown */
.gg-hero-score-breakdown {{
  margin-bottom: 16px;
}}

.gg-hero-score-break-row {{
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}}

.gg-hero-break-label {{
  flex: 0 0 120px;
  font-family: 'Sometype Mono', monospace;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: {COLOR_PALETTE['brown_dark']};
}}

.gg-hero-break-bar {{
  flex: 1;
  height: 24px;
  background: {COLOR_PALETTE['light_gray']};
  border: 2px solid {COLOR_PALETTE['black']};
  border-radius: 4px;
  overflow: hidden;
}}

.gg-hero-break-fill {{
  height: 100%;
  background: {COLOR_PALETTE['turquoise']};  /* ENFORCED: Turquoise */
  transition: width 0.3s ease;
}}

.gg-hero-break-score {{
  flex: 0 0 60px;
  font-family: 'Sometype Mono', monospace;
  font-size: 14px;
  font-weight: 700;
  color: {COLOR_PALETTE['brown_dark']};
  text-align: right;
}}

.gg-hero-final-row {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  margin-top: 16px;
  border-top: 2px solid {COLOR_PALETTE['black']};
  font-family: 'Sometype Mono', monospace;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}}

.gg-hero-final-score {{
  font-size: 18px;
  color: {COLOR_PALETTE['brown_dark']};
}}

.gg-hero-score-caption {{
  font-family: 'Sometype Mono', monospace;
  font-size: 11px;
  color: {COLOR_PALETTE['brown_medium']};
  font-style: italic;
  text-align: center;
}}

/* Responsive */
@media (max-width: 768px) {{
  .gg-hero-inner {{
    flex-direction: column;
    gap: 32px;
    padding: 32px 16px;
  }}
  
  .gg-hero-right {{
    flex: 1;
  }}
  
  .gg-hero-title {{
    font-size: 32px;
  }}
  
  .gg-hero-quote {{
    font-size: 16px;
  }}
  
  .gg-hero-score-main {{
    font-size: 48px;
  }}
  
  .gg-hero-break-label {{
    flex: 0 0 80px;
    font-size: 10px;
  }}
}}
</style>"""
    
    # Return combined HTML
    return hero_html + "\n" + style_html
