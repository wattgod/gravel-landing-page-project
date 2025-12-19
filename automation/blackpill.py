"""
Gravel God Black Pill Section Generator

SINGLE SOURCE OF TRUTH for Black Pill section HTML.
This module fixes the color violation found in the original implementation.

CRITICAL FIX:
- Original violation: #F4D03F on large background areas
- Fixed: Using #FFF5E6 (muted cream) for large backgrounds
- #F4D03F only for small accents (badges, hover states)

Usage:
    from blackpill import generate_blackpill_html
    
    html = generate_blackpill_html(race_data)
"""

from typing import Dict, List


# Gravel God Color Palette
COLOR_PALETTE = {
    'yellow_accent': '#F4D03F',      # ONLY for small elements (badges, hovers)
    'cream_background': '#FFF5E6',    # For large background areas
    'cream_soft': '#F5E5D3',          # Alternative muted cream
    'turquoise': '#40E0D0',           # Accent color
    'brown_dark': '#59473C',          # Text
    'brown_medium': '#8C7568',        # Borders
    'brown_light': '#BFA595',         # Subtle elements
    'black': '#000000'                # Borders, shadows
}


def validate_background_color(element_type: str) -> str:
    """
    Return appropriate background color based on element size.
    
    RULE: Large backgrounds use muted earth tones, NOT bright yellow.
    """
    if element_type in ['large_background', 'quote_block', 'section_bg']:
        return COLOR_PALETTE['cream_background']
    elif element_type in ['badge', 'small_accent']:
        return COLOR_PALETTE['yellow_accent']
    else:
        return COLOR_PALETTE['cream_background']  # Default to safe choice


def generate_blackpill_html(data: Dict) -> str:
    """
    Generate Black Pill section HTML with validated colors.
    
    The Black Pill section provides a reality check about race difficulty.
    
    Args:
        data: Race data dict with 'race' key containing 'black_pill' object
        
    Returns:
        Complete HTML string with <section> and <style> tags
        
    Raises:
        KeyError: If required data structure is missing
        
    Example:
        >>> race_data = {
        ...     'race': {
        ...         'black_pill': {
        ...             'title': 'This Race Will Hurt',
        ...             'reality': 'Most people underestimate...',
        ...             'consequences': ['Sleep deprivation', 'Equipment failures'],
        ...             'expectation_reset': 'Finishing is the real victory'
        ...         }
        ...     }
        ... }
        >>> html = generate_blackpill_html(race_data)
    """
    # Extract black pill data
    race = data['race']
    bp = race['black_pill']
    
    # Validate required fields
    required_fields = ['title', 'reality', 'consequences', 'expectation_reset']
    missing = [f for f in required_fields if f not in bp]
    if missing:
        raise KeyError(f"Black pill data missing required fields: {missing}")
    
    # Build consequences list - compacted
    consequences_items = ''.join([f'<li>{c}</li>' for c in bp['consequences']])
    
    # Get quote from black_pill.quote, final_verdict.one_liner, or use a default
    quote = bp.get('quote') or data['race'].get('final_verdict', {}).get('one_liner', 'This race will test every assumption you have about your durability.')
    
    # Section HTML - compacted
    section_html = f"""<section class="gg-blackpill-section">
  <div class="gg-blackpill-badge"><span class="gg-blackpill-badge-icon">◆</span> THE BLACK PILL</div>
  <h2 class="gg-blackpill-title">{bp['title']}</h2>
  <div class="gg-blackpill-body">
    <p><strong>{bp['reality']}</strong></p>
    <p><strong>Here's what it actually costs:</strong></p>
    <ul>{consequences_items}</ul>
    <p><strong>{bp['expectation_reset']}</strong></p>
  </div>
  <div class="gg-blackpill-quote">{quote}</div>
</section>"""
    
    # Style block with FIXED colors
    style_html = f"""<style>
/* Black Pill Section */
.gg-blackpill-section {{
  max-width: 1000px;
  margin: 48px auto;
  padding: 48px 24px;
  background: {validate_background_color('section_bg')};  /* FIXED: Was #F4D03F */
  border: 3px solid {COLOR_PALETTE['black']};
  border-radius: 8px;
  box-shadow: 8px 8px 0 {COLOR_PALETTE['black']};
}}

.gg-blackpill-badge {{
  display: inline-block;
  background: {COLOR_PALETTE['yellow_accent']};  /* OK: Small badge */
  color: {COLOR_PALETTE['black']};
  padding: 12px 24px;
  border: 3px solid {COLOR_PALETTE['black']};
  border-radius: 50px;
  box-shadow: 6px 6px 0 {COLOR_PALETTE['black']};
  font-family: 'Sometype Mono', monospace;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: 24px;
}}

.gg-blackpill-badge-icon {{
  margin-right: 8px;
  font-size: 11px;
}}

.gg-blackpill-title {{
  font-family: 'Sometype Mono', monospace;
  font-size: 28px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: {COLOR_PALETTE['brown_dark']};
  margin: 0 0 24px 0;
  line-height: 1.2;
}}

.gg-blackpill-body {{
  font-family: 'Sometype Mono', monospace;
  font-size: 15px;
  line-height: 1.8;
  color: {COLOR_PALETTE['brown_dark']};
}}

.gg-blackpill-body p {{
  margin: 0 0 20px 0;
}}

.gg-blackpill-body ul {{
  list-style: none;
  padding: 0;
  margin: 20px 0;
}}

.gg-blackpill-body li {{
  padding: 12px 0 12px 32px;
  position: relative;
  border-bottom: 1px solid {COLOR_PALETTE['brown_medium']};
}}

.gg-blackpill-body li:before {{
  content: '◆';
  position: absolute;
  left: 0;
  color: {COLOR_PALETTE['brown_dark']};
  font-weight: 700;
}}

.gg-blackpill-body li:last-child {{
  border-bottom: none;
}}

.gg-blackpill-quote {{
  font-family: 'Sometype Mono', monospace;
  font-size: 18px;
  font-weight: 700;
  font-style: italic;
  color: {COLOR_PALETTE['brown_dark']};
  text-align: center;
  margin-top: 2rem;
  padding: 1.5rem;
  border-left: 4px solid {COLOR_PALETTE['brown_dark']};
  background: {validate_background_color('quote_block')};  /* FIXED: Was #F4D03F */
}}

/* Responsive */
@media (max-width: 768px) {{
  .gg-blackpill-section {{
    padding: 32px 16px;
    margin: 32px 0;
  }}
  
  .gg-blackpill-title {{
    font-size: 22px;
  }}
  
  .gg-blackpill-body {{
    font-size: 14px;
  }}
}}
</style>"""
    
    # CRITICAL: Style tag comes AFTER section
    return section_html + "\n" + style_html


def validate_blackpill_data(data: Dict) -> List[str]:
    """
    Validate Black Pill data structure.
    
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Check top-level structure
    if 'race' not in data:
        errors.append("Missing 'race' key in data")
        return errors
    
    if 'black_pill' not in data['race']:
        errors.append("Missing 'black_pill' key in race data")
        return errors
    
    bp = data['race']['black_pill']
    
    # Check required fields
    required_fields = {
        'title': str,
        'reality': str,
        'consequences': list,
        'expectation_reset': str
    }
    
    for field, expected_type in required_fields.items():
        if field not in bp:
            errors.append(f"Missing required field: '{field}'")
        elif not isinstance(bp[field], expected_type):
            errors.append(f"Field '{field}' should be {expected_type.__name__}, got {type(bp[field]).__name__}")
    
    # Check consequences list
    if 'consequences' in bp:
        if not bp['consequences']:
            errors.append("Consequences list is empty")
        elif not all(isinstance(c, str) for c in bp['consequences']):
            errors.append("All consequences must be strings")
    
    return errors
