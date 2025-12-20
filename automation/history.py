"""
Gravel God History Section Generator

Generates the history section with timeline, experience, and random facts.

Usage:
    from automation.history import generate_history_html
    
    html = generate_history_html(race_data)
"""

from typing import Dict


def generate_history_html(data: Dict) -> str:
    """Generate history section with timeline, experience, and random facts."""
    race = data['race']
    history = race['history']
    display_name = race['display_name']
    location = race['vitals']['location']
    
    # Build timeline events
    timeline_html = []
    for moment in history.get('notable_moments', []):
        # Handle both "Year: Description" format and plain string format
        if ':' in moment:
            year = moment.split(':')[0].strip()
            content = moment.split(':', 1)[1].strip()
        else:
            # No year specified - use founded year or current year
            year = str(history.get('founded', '')) if history.get('founded') else 'Recent'
            content = moment
        timeline_html.append(f"""    <div class="gg-timeline-event">
      <div class="gg-timeline-year">{year}</div>
      <div class="gg-timeline-content">
        {content}
      </div>
    </div>""")
    
    # Random facts
    if 'random_facts' in history and isinstance(history['random_facts'], list) and len(history['random_facts']) >= 3:
        facts = history['random_facts'][:5]
    else:
        facts = [
            f"{history['reputation']}",
            f"The course is {race['course_description']['character'].lower()}.",
            f"{race['vitals']['field_size']}",
            f"{race['black_pill']['reality'][:150]}..."
        ]
        facts = facts[:4]
    
    # Generate dynamic facts header
    race_name_short = display_name.split()[0] if display_name else "Race"
    facts_header_variations = [
        f"{race_name_short} Facts",
        f"Things You Should Know",
        f"What Makes {race_name_short} Different",
        f"The Details That Matter",
        f"{race_name_short} Reality Check"
    ]
    race_slug = race.get('slug', '')
    facts_header = facts_header_variations[hash(race_slug) % len(facts_header_variations)] if race_slug else "Random Facts"
    
    # Generate dynamic "Vision Quest" title
    vision_quest_variations = [
        f"{display_name} is a Vision Quest, not a race",
        f"{display_name} is what happens when ambition meets reality",
        f"{display_name} isn't a race—it's a character test",
        f"{display_name} is where training plans meet the truth",
        f"{display_name} separates riders from racers"
    ]
    vision_quest_title = vision_quest_variations[(hash(race_slug) + 1) % len(vision_quest_variations)] if race_slug else f"{display_name} is a Vision Quest, not a race"
    
    facts_html = []
    for i, fact in enumerate(facts[:5], 1):
        facts_html.append(f"""      <div class="gg-fact-card">
        <div class="gg-fact-number">{i}</div>
        <div class="gg-fact-text">
          {fact}
        </div>
      </div>""")
    
    template = f"""<section class="gg-tldr-grid">

  <!-- Vision Quest -->
  <div>
    <div class="gg-pill">Facts And History</div>
    <div class="gg-tldr-vision-header">
      <h2 class="gg-tldr-vision-title">{vision_quest_title}</h2>
    </div>
    <p>{history['origin_story']}</p>
  </div>

  <!-- The Experience -->
  <div>
    <h3 class="gg-subheading">The Experience</h3>
    <p>You roll out of {location.split(',')[0]} wedged into a nervous pack of riders, half of whom are over-biked and under-trained. The first hour feels almost polite. Then the field hits the first challenging sections and you start seeing people on the side of the road wrestling with mechanicals and broken spirits.</p>
    <p>The middle third is pure accounting: calories, bottles, chain lube, and bad decisions. The race doesn't "start" so much as it quietly removes options until you're either riding alone into a crosswind, clinging to a group that's too strong, or sitting in a folding chair at a checkpoint trying to decide if you're the kind of person who goes back out into the dark.</p>
  </div>

  <!-- Timeline History -->
  <div class="gg-timeline-section">
{chr(10).join(timeline_html)}
  </div>

  <!-- Random Facts Cards -->
  <div>
    <h3 class="gg-facts-header">{facts_header}</h3>
    <div class="gg-facts-grid">
{chr(10).join(facts_html)}
    </div>
  </div>

</section>"""
    
    return template
