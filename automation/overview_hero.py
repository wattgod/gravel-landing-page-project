"""
Gravel God Overview Hero Section Generator

Generates the overview hero section with race name and intro.

Usage:
    from automation.overview_hero import generate_overview_hero_html
    
    html = generate_overview_hero_html(race_data)
"""

from typing import Dict


def generate_overview_hero_html(data: Dict) -> str:
    """Generate overview hero section HTML."""
    race = data['race']
    display_name = race['display_name']
    tagline = race['tagline']
    course_char = race['course_description']['character']
    
    template = f"""<section class="gg-overview-hero-v2">

  <div class="gg-overview-badge">Race Guide</div>

  <h1 class="gg-overview-title-v2">
    {display_name.upper()}<br>
    OVERVIEW & TRAINING GUIDE
  </h1>

  <p class="gg-overview-lede-v2">
    {tagline}
  </p>

  <p class="gg-overview-body-v2">
    This page is your briefing: what the race actually is, how it breaks riders, and
    how to show up with a body and brain that can survive {race['vitals']['distance_mi']} miles of {course_char.lower()}.
  </p>

</section>"""
    
    return template
