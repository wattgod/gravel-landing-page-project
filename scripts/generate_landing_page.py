#!/usr/bin/env python3
"""
Gravel God Landing Page Generator
Generates complete Elementor JSON from race data schema.
"""

import json
import re
from typing import Dict, Any, List, Optional


def load_race_data(json_path: str) -> Dict[str, Any]:
    """Load race data schema from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def calculate_percentage(score: int, max_score: int = 50) -> int:
    """Calculate percentage for progress bars."""
    return int((score / max_score) * 100)


def generate_hero_html(data: Dict) -> str:
    """Generate hero section HTML."""
    race = data['race']
    rating = race['gravel_god_rating']
    
    template = """<div class="gg-hero-inner">

  <!-- ===========================
       LEFT SIDE — TITLE + BADGES
       =========================== -->
  <div class="gg-hero-left">

    <div class="gg-hero-badges">
      <!-- Tier 1 diamond-style badge -->
      <span class="gg-hero-badge gg-hero-badge-tier">
        {tier_label}
      </span>

      <!-- Location pill -->
      <span class="gg-hero-badge gg-hero-badge-loc">
        {location_badge}
      </span>
    </div>

    <div class="gg-hero-title">
      {display_name}
    </div>

    <div class="gg-hero-quote">
      {tagline}
    </div>
  </div>

  <!-- ===========================
       RIGHT SIDE — SCORE CARD
       =========================== -->
  <div class="gg-hero-right">
    <div class="gg-hero-score-card">

      <!-- LABEL -->
      <div class="gg-hero-score-label">Gravel God Rating</div>

      <!-- MAIN SCORE -->
      <div class="gg-hero-score-main">
        {overall_score}<span>/100</span>
      </div>

      <!-- SUBTEXT -->
      <div class="gg-hero-score-sub">
        {tier_label} · Iconic · High Consequence
      </div>

      <!-- BREAKDOWN BARS -->
      <div class="gg-hero-score-breakdown">

        <!-- Course Profile -->
        <div class="gg-hero-score-break-row">
          <span class="gg-hero-break-label">Course Profile</span>
          <div class="gg-hero-break-bar">
            <div class="gg-hero-break-fill" style="width: {course_pct}%;"></div>
          </div>
          <span class="gg-hero-break-score">{course_profile} / 50</span>
        </div>

        <!-- Biased Opinion -->
        <div class="gg-hero-score-break-row">
          <span class="gg-hero-break-label">Biased Opinion</span>
          <div class="gg-hero-break-bar">
            <div class="gg-hero-break-fill" style="width: {opinion_pct}%;"></div>
          </div>
          <span class="gg-hero-break-score">{biased_opinion} / 50</span>
        </div>

        <!-- Final Score -->
        <div class="gg-hero-final-row">
          <span>Final Score</span>
          <span class="gg-hero-final-score">{overall_score} / 100</span>
        </div>

      </div>

      <div class="gg-hero-score-caption">
        Score based on Gravel God radar + editorial bias.
      </div>

    </div>
  </div>
</div>"""
    
    return template.format(
        tier_label=rating['tier_label'],
        location_badge=race['vitals']['location_badge'],
        display_name=race['display_name'],
        tagline=race['tagline'],
        overall_score=rating['overall_score'],
        course_profile=rating['course_profile'],
        biased_opinion=rating['biased_opinion'],
        course_pct=calculate_percentage(rating['course_profile']),
        opinion_pct=calculate_percentage(rating['biased_opinion'])
    )


def generate_vitals_html(data: Dict) -> str:
    """Generate race vitals section HTML."""
    race = data['race']
    vitals = race['vitals']
    
    # Note: The actual template in the JSON is more complex with dashboard cards
    # This simplified version matches the skill doc template
    terrain_desc = ', '.join(vitals['terrain_types'])
    
    template = """<section id="race-vitals" class="gg-guide-section js-guide-section">
  <div class="gg-vitals-grid">
    <div>
      <div class="gg-vitals-pill">Quick Facts</div>
      <h2 class="gg-vitals-heading">Race Vitals</h2>
      <p class="gg-vitals-lede">
        The numbers that matter. Everything else is commentary.
      </p>
    </div>
    
    <div class="gg-vitals-table-wrap">
      <table class="gg-vitals-table">
        <tbody>
          <tr><th>Location</th><td>{location}</td></tr>
          <tr><th>Date</th><td>{date}</td></tr>
          <tr><th>Distance</th><td>{distance_mi} miles</td></tr>
          <tr><th>Elevation Gain</th><td>~{elevation_ft} ft</td></tr>
          <tr><th>Terrain</th><td>{terrain}</td></tr>
          <tr><th>Field Size</th><td>{field_size}</td></tr>
          <tr><th>Start Time</th><td>{start_time}</td></tr>
          <tr><th>Registration</th><td>{registration}</td></tr>
          <tr><th>Prize Purse</th><td>{prize_purse}</td></tr>
          <tr><th>Aid Stations</th><td>{aid_stations}</td></tr>
          <tr><th>Cut-off Time</th><td>{cutoff_time}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>"""
    
    return template.format(
        location=f"{vitals['location']} ({vitals['county']})",
        date=vitals['date_specific'],
        distance_mi=vitals['distance_mi'],
        elevation_ft=f"{vitals['elevation_ft']:,}",
        terrain=terrain_desc,
        field_size=vitals['field_size'],
        start_time=vitals['start_time'],
        registration=vitals['registration'],
        prize_purse=vitals['prize_purse'],
        aid_stations=vitals['aid_stations'],
        cutoff_time=vitals['cutoff_time']
    )


def generate_ratings_html(data: Dict) -> str:
    """Generate ratings breakdown section HTML with radar chart and course profile."""
    race = data['race']
    ratings = race['ratings_breakdown']
    rating = race['gravel_god_rating']
    
    # Course profile variables (7 total, excluding prestige)
    # Note: logistics might be in gravel_god_rating, not ratings_breakdown
    course_categories = ['length', 'technicality', 'elevation', 'climate', 'altitude', 'adventure']
    
    # Add logistics if available (check both places)
    if 'logistics' in ratings:
        course_categories.append('logistics')
    elif 'logistics' in rating:
        # Create a logistics entry from gravel_god_rating
        logistics_score = rating.get('logistics', 4)
        ratings['logistics'] = {
            'score': logistics_score,
            'explanation': 'Logistics rating based on course accessibility, aid station quality, and race organization.'
        }
        course_categories.append('logistics')
    
    # Calculate raw course score (sum of all 7 variables)
    raw_course_score = sum(ratings[cat]['score'] for cat in course_categories)
    
    # Generate course profile card rows
    profile_rows = []
    for cat in course_categories:
        cat_data = ratings[cat]
        score = cat_data['score']
        width_pct = int((score / 5) * 100)
        profile_rows.append(f"""        <div class="gg-course-metric-row">
          <span class="gg-course-metric-label">{cat.title()}</span>
          <div class="gg-rating-bar">
            <div class="gg-rating-bar-fill" style="width: {width_pct}%;"></div>
          </div>
          <span class="gg-course-metric-score">{score}/5</span>
        </div>""")
    
    # Generate right-side explanations
    explanation_html = []
    for cat in course_categories:
        cat_data = ratings[cat]
        explanation_html.append(f"""      <h3 class="gg-subheading">{cat.title()}</h3>
      <p>
        {cat_data['explanation']}
      </p>""")
    
    # Build JavaScript metrics array for radar chart
    js_metrics = []
    for cat in course_categories:
        score = ratings[cat]['score']
        label = cat.title()
        js_metrics.append(f'        {{ label: "{label}",       value: {score} }}')
    js_metrics_str = ',\n'.join(js_metrics)
    
    # Get course quote from black_pill or final_verdict
    course_quote = race.get('black_pill', {}).get('quote') or race.get('final_verdict', {}).get('one_liner', 'Something will break out there. Hopefully not you.')
    
    template = """<section class="gg-section gg-ratings-section" id="course-ratings">
  <div class="gg-ratings-header">
    <div class="gg-pill">
      <span class="gg-pill-icon">◆</span>
      <span>WHAT THE COURSE IS LIKE</span>
    </div>
    <h2 class="gg-section-title">THE RATINGS</h2>
  </div>

  <div class="gg-ratings-grid">
    <!-- LEFT: RADAR + COURSE PROFILE CARD + QUOTE -->
    <div class="gg-ratings-left">

      <!-- Radar card -->
      <div class="gg-radar-card">
        <div class="gg-radar-header">
          <div class="gg-radar-title">Gravel God Radar</div>
          <div class="gg-radar-pill"><span>{race_name}</span></div>
        </div>

        <svg class="gg-course-radar-svg" viewBox="0 0 320 320"></svg>
      </div>

      <!-- Course profile / mini bars -->
      <div class="gg-course-profile-card">
        <div class="gg-course-profile-title">Course Profile</div>
        <div class="gg-course-profile-meta">
          Seven variables · 1–5 scale &nbsp;&nbsp;|&nbsp;&nbsp;
          Raw Course Score: <strong>{raw_course_score} / 35</strong>
        </div>

{profile_rows}
      </div>

      <!-- Big pull quote living in the LEFT column -->
      <div class="gg-course-quote-big">
        <span>"{course_quote}"</span>
      </div>
    </div>

    <!-- RIGHT: COPY FOR EACH VARIABLE -->
    <div class="gg-ratings-right">

{explanations}
    </div>
  </div>
</section>

<script>
  (function () {{
    const section = document.querySelector("#course-ratings");
    if (!section) return;

    const svg = section.querySelector(".gg-course-radar-svg");
    if (!svg) return;

    const ns = "http://www.w3.org/2000/svg";

    const config = {{
      center: 160,
      radius: 110,
      maxScore: 5,
      metrics: [
{js_metrics}
      ]
    }};

    const {{ center, radius, maxScore, metrics }} = config;
    const n = metrics.length;

    function polar(index, r) {{
      const angleDeg = (360 / n) * index - 90;
      const a = (angleDeg * Math.PI) / 180;
      return {{
        x: center + r * Math.cos(a),
        y: center + r * Math.sin(a),
        angleDeg
      }};
    }}

    // Grid rings
    const rings = 4;
    for (let i = 1; i <= rings; i++) {{
      const r = (radius * i) / rings;
      let d = "";
      for (let j = 0; j < n; j++) {{
        const {{ x, y }} = polar(j, r);
        d += (j === 0 ? "M" : "L") + x + "," + y + " ";
      }}
      d += "Z";
      const ring = document.createElementNS(ns, "path");
      ring.setAttribute("d", d);
      ring.setAttribute("class", "gg-radar-grid-ring");
      svg.appendChild(ring);
    }}

    // Axes + labels
    metrics.forEach((metric, i) => {{
      const {{ x: ex, y: ey, angleDeg }} = polar(i, radius);

      const axis = document.createElementNS(ns, "line");
      axis.setAttribute("x1", center);
      axis.setAttribute("y1", center);
      axis.setAttribute("x2", ex);
      axis.setAttribute("y2", ey);
      axis.setAttribute("class", "gg-radar-axis-line");
      svg.appendChild(axis);

      const labelPos = polar(i, radius + 24);
      const text = document.createElementNS(ns, "text");
      text.setAttribute("x", labelPos.x);
      text.setAttribute("y", labelPos.y);
      text.setAttribute(
        "text-anchor",
        angleDeg > 90 && angleDeg < 270 ? "end" : "start"
      );
      text.setAttribute("dominant-baseline", "middle");
      text.setAttribute("class", "gg-radar-label");
      text.textContent = metric.label.toUpperCase();
      svg.appendChild(text);
    }});

    // Data polygon
    let d = "";
    metrics.forEach((metric, i) => {{
      const r = (metric.value / maxScore) * radius;
      const {{ x, y }} = polar(i, r);
      d += (i === 0 ? "M" : "L") + x + "," + y + " ";
    }});
    d += "Z";

    const poly = document.createElementNS(ns, "path");
    poly.setAttribute("d", d);
    poly.setAttribute("class", "gg-radar-data-fill");
    svg.appendChild(poly);
  }})();
</script>"""
    
    return template.format(
        race_name=race['display_name'],
        raw_course_score=raw_course_score,
        profile_rows='\n'.join(profile_rows),
        explanations='\n\n'.join(explanation_html),
        js_metrics=js_metrics_str,
        course_quote=course_quote
    )


def generate_blackpill_html(data: Dict) -> str:
    """Generate Black Pill section HTML."""
    race = data['race']
    bp = race['black_pill']
    
    consequences_items = '\n      '.join([f'<li>{c}</li>' for c in bp['consequences']])
    
    template = """<style>
  .gg-blackpill-section {{
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }}
  
  .gg-blackpill-body {{
    max-width: 100%;
  }}
  
  .gg-blackpill-quote {{
    max-width: 100%;
  }}
</style>

<section class="gg-blackpill-section">

  <!-- BLACK PILL BADGE -->
  <div class="gg-blackpill-badge">
    <span class="gg-blackpill-badge-icon">◆</span>
    THE BLACK PILL
  </div>

  <!-- SECTION HEADING -->
  <h3 class="gg-blackpill-heading">
    {title}
  </h3>

  <!-- BODY COPY -->
  <div class="gg-blackpill-body">
    <p>
      <strong>{reality}</strong>
    </p>

    <p>
      <strong>Here's what it actually costs:</strong>
    </p>
    <ul>
      {consequences}
    </ul>

    <p>
      <strong>{expectation_reset}</strong>
    </p>
  </div>

  <!-- PULL QUOTE -->
  <div class="gg-blackpill-quote">
    {quote}
  </div>

</section>"""
    
    # Get quote from black_pill.quote, final_verdict.one_liner, or use a default
    quote = bp.get('quote') or data['race'].get('final_verdict', {}).get('one_liner', 'This race will test every assumption you have about your durability.')
    
    return template.format(
        title=bp['title'],
        reality=bp['reality'],
        consequences=consequences_items,
        expectation_reset=bp['expectation_reset'],
        quote=quote
    )


def generate_course_map_html(data: Dict) -> str:
    """Generate course map section with RideWithGPS embed and suffering zones."""
    race = data['race']
    course = race['course_description']
    rwgps_id = course['ridewithgps_id']
    rwgps_name = course['ridewithgps_name']
    
    # Build suffering zones HTML with enhanced details
    zones_html = []
    for zone in course['suffering_zones']:
        mile = zone['mile']
        label = zone['label']
        desc = zone['desc']
        
        # Enhanced details if available
        terrain_detail = zone.get('terrain_detail', '')
        named_section = zone.get('named_section', '')
        citation = zone.get('citation', '')
        weather_note = zone.get('weather_note', '')
        
        # Build description with enhanced details
        desc_parts = [desc]
        
        if named_section:
            desc_parts.append(f"<strong>{named_section}</strong>")
        
        if terrain_detail:
            desc_parts.append(terrain_detail)
        
        if weather_note:
            desc_parts.append(f"<em>{weather_note}</em>")
        
        full_desc = ' '.join(desc_parts)
        
        # Add citation if present
        citation_html = ''
        if citation:
            citation_html = f'<div class="gg-zone-citation">Source: {citation}</div>'
        
        zones_html.append(f"""        <div class="gg-zone-card">
          <div class="gg-zone-mile">Mile {mile}</div>
          <div class="gg-zone-label">{label}</div>
          <div class="gg-zone-desc">{full_desc}</div>
          {citation_html}
        </div>""")
    
    # Calculate distance for title
    distance = race['vitals']['distance_mi']
    location = race['vitals']['location'].split(',')[0]  # Just city name
    
    template = f"""<section class="gg-route-section js-guide-section" id="course-map">
  <div class="gg-route-card">
    <div class="gg-route-card-inner">

      <header class="gg-route-header">
        <span class="gg-pill gg-pill--small">Course Map</span>
        <h2 class="gg-route-title">
          WHAT {distance} MILES OF {location.upper()} ACTUALLY LOOKS LIKE
        </h2>
        <p class="gg-route-lede">
          Hover over the profile to see where the climbs, chaos, and
          "why did I sign up for this" moments actually are.
        </p>
      </header>

      <div class="gg-route-frame-wrap">
        <iframe
          src="https://ridewithgps.com/embeds?type=route&id={rwgps_id}&title={rwgps_name}&sampleGraph=true&distanceMarkers=true"
          style="width: 1px; min-width: 100%; height: 650px; border: none;"
          scrolling="no"
        ></iframe>
      </div>

      <!-- Suffering Zones -->
      <div class="gg-suffering-zones">
{chr(10).join(zones_html)}
      </div>

      <!-- Course Breakdown Research Note -->
      <div class="gg-course-breakdown-note" style="margin-top: 2rem; padding: 1rem; background: #F5F5DC; border: 2px solid #59473C; font-family: 'Sometype Mono', monospace; font-size: 0.85rem; color: #59473C; line-height: 1.6;">
        <strong>Course Breakdown:</strong> Suffering zones are based on race reports, Strava segments, and course analysis. Terrain details reflect typical conditions—weather can dramatically change difficulty.
      </div>

      <footer class="gg-route-caption">
        Elevation + route courtesy of RideWithGPS. Suffering courtesy of you.
      </footer>

    </div>
  </div>
</section>"""
    
    return template


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


def generate_tldr_html(data: Dict) -> str:
    """Generate TLDR/Decision section HTML - brief and scannable (2-3 sentences max, ~40-60 words)."""
    race = data['race']
    
    # Use tldr fields if available (preferred - already condensed)
    if 'tldr' in race:
        tldr = race['tldr']
        should_race_condensed = tldr.get('should_race_if', 'You value community and authentic hospitality over predictable conditions.')
        skip_if_text = tldr.get('skip_if', 'You need to know exactly what you\'re getting into before you commit.')
    else:
        # Fallback: extract from final_verdict and condense
        verdict = race.get('final_verdict', {})
        should_race_full = verdict.get('should_you_race', 'You like hurting yourself, surprises (not the good kind), and you\'re prepared to commit a month of salary and (hopefully) a shit load of training getting ready for one truly insane day.')
        
        # Condense to core message - extract key points
        should_race_condensed = should_race_full
        
        # If it's too long, extract the core message
        if len(should_race_full.split()) > 60:
            # Try to extract first 2-3 sentences or key phrases
            sentences = should_race_full.split('. ')
            if len(sentences) >= 2:
                # Take first 2 sentences, condense if needed
                should_race_condensed = '. '.join(sentences[:2]) + '.'
                # If still too long, take first sentence + key phrase
                if len(should_race_condensed.split()) > 60:
                    should_race_condensed = sentences[0] + '.'
            else:
                # Single long sentence - extract key phrases
                # Look for "if you value" or "if you need" patterns
                if 'value' in should_race_full.lower():
                    parts = should_race_full.split('—')
                    if len(parts) > 0:
                        should_race_condensed = parts[0].strip() + '.'
        
        # Get skip_if - extract from should_you_race or use alternatives
        skip_if_text = 'You\'re not ready to find out what\'s actually inside you.'
        if 'reconsider' in should_race_full.lower():
            # Extract the reconsider part
            parts = should_race_full.split('—')
            if len(parts) > 1:
                skip_part = parts[1].strip()
                # Condense to 2-3 sentences
                skip_sentences = skip_part.split('. ')
                if len(skip_sentences) >= 2:
                    skip_if_text = '. '.join(skip_sentences[:2]) + '.'
                else:
                    skip_if_text = skip_part
                # Ensure it's not too long
                if len(skip_if_text.split()) > 60:
                    skip_if_text = skip_sentences[0] + '.' if skip_sentences else skip_if_text
    
    template = f"""<div class="gg-decision-grid">
  <div class="gg-decision-card gg-decision-card--yes">
    <h3>You Should Race This If:</h3>
    <p>{should_race_condensed}</p>
    <a href="#training" class="gg-decision-cta">Get a Training Plan →</a>
  </div>

  <div class="gg-decision-card gg-decision-card--no">
    <h3>Skip This If:</h3>
    <p>{skip_if_text}</p>
    
  </div>
</div>"""
    
    return template


def generate_history_html(data: Dict) -> str:
    """Generate history section with timeline, experience, and random facts."""
    race = data['race']
    history = race['history']
    display_name = race['display_name']
    location = race['vitals']['location']
    
    # Build timeline events
    timeline_html = []
    for moment in history['notable_moments']:
        year = moment.split(':')[0]
        content = moment.split(':', 1)[1].strip()
        timeline_html.append(f"""    <div class="gg-timeline-event">
      <div class="gg-timeline-year">{year}</div>
      <div class="gg-timeline-content">
        {content}
      </div>
    </div>""")
    
    # Random facts - use quality facts from data if available, otherwise generate from key details
    if 'random_facts' in history and isinstance(history['random_facts'], list) and len(history['random_facts']) >= 3:
        facts = history['random_facts'][:5]  # Use provided quality facts
    else:
        # Fallback: generate from key details (but these should be replaced with quality facts)
        facts = [
            f"{history['reputation']}",
            f"The course is {race['course_description']['character'].lower()}.",
            f"{race['vitals']['field_size']}",
            f"{race['black_pill']['reality'][:150]}..."
        ]
        # Only use first 4 if we don't have quality facts
        facts = facts[:4]
    
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
      <h2 class="gg-tldr-vision-title">{display_name} is a Vision Quest, not a race</h2>
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
    <h3 class="gg-facts-header">Random Facts</h3>
    <div class="gg-facts-grid">
{chr(10).join(facts_html)}
    </div>
  </div>

</section>"""
    
    return template


def generate_biased_opinion_html(data: Dict) -> str:
    """Generate biased opinion section - EXACTLY matches Course Profile structure."""
    race = data['race']
    ratings = race['ratings_breakdown']
    biased = race['biased_opinion']
    race_name = race['display_name']
    
    # These are the 7 biased opinion ratings: prestige, race_quality, experience, community, field_depth, value, expenses
    opinion_ratings = ['prestige', 'race_quality', 'experience', 'community', 'field_depth', 'value', 'expenses']
    
    # Calculate raw opinion score (sum of all 7 variables)
    raw_opinion_score = sum(ratings[cat]['score'] for cat in opinion_ratings if cat in ratings)
    
    # Generate editorial profile card rows (left column, like course profile)
    profile_rows = []
    for rating_key in opinion_ratings:
        if rating_key in ratings:
            cat_data = ratings[rating_key]
            score = cat_data['score']
            width_pct = int((score / 5) * 100)
            label = rating_key.replace('_', ' ').title()
            profile_rows.append(f"""        <div class="gg-course-metric-row">
          <span class="gg-course-metric-label">{label}</span>
          <div class="gg-rating-bar">
            <div class="gg-rating-bar-fill" style="width: {width_pct}%;"></div>
          </div>
          <span class="gg-course-metric-score">{score}/5</span>
        </div>""")
    
    # Generate right-side explanations
    explanation_html = []
    for rating_key in opinion_ratings:
        if rating_key in ratings:
            cat_data = ratings[rating_key]
            label = rating_key.replace('_', ' ').title()
            explanation_html.append(f"""      <h3 class="gg-subheading">{label}</h3>
      <p>
        {cat_data['explanation']}
      </p>""")
    
    # Build JavaScript metrics array for radar chart
    js_metrics = []
    for rating_key in opinion_ratings:
        if rating_key in ratings:
            score = ratings[rating_key]['score']
            label = rating_key.replace('_', ' ').title()
            js_metrics.append(f'        {{ label: "{label}",       value: {score} }}')
    js_metrics_str = ',\n'.join(js_metrics)
    
    # Get quote from biased_opinion.quote (max 30 words, punchy and memorable)
    opinion_quote = biased.get('quote') or biased.get('summary', 'This race will test every assumption you have about your durability.')
    # If quote is too long, truncate to first sentence or 30 words max
    words = opinion_quote.split()
    if len(words) > 30:
        # Try to find first sentence
        sentences = opinion_quote.split('. ')
        if sentences and len(sentences[0].split()) <= 30:
            opinion_quote = sentences[0] + '.'
        else:
            # Fallback: take first 30 words
            opinion_quote = ' '.join(words[:30]) + '...'
    
    template = f"""<section class="gg-section gg-ratings-section" id="biased-opinion">
  <div class="gg-ratings-header">
    <div class="gg-pill">
      <span class="gg-pill-icon">◆</span>
      <span>BIASED OPINION</span>
    </div>
    <h2 class="gg-section-title">{biased['verdict']}</h2>
  </div>

  <div class="gg-ratings-grid">
    <!-- LEFT: RADAR + EDITORIAL PROFILE CARD + QUOTE -->
    <div class="gg-ratings-left">

      <!-- Radar card -->
      <div class="gg-radar-card">
        <div class="gg-radar-header">
          <div class="gg-radar-title">Editorial Radar</div>
          <div class="gg-radar-pill"><span>{race_name}</span></div>
        </div>

        <svg class="gg-course-radar-svg" viewBox="0 0 320 320"></svg>
      </div>

      <!-- Editorial profile / mini bars -->
      <div class="gg-course-profile-card">
        <div class="gg-course-profile-title">Editorial Profile</div>
        <div class="gg-course-profile-meta">
          Seven variables · 1–5 scale &nbsp;&nbsp;|&nbsp;&nbsp;
          Raw Editorial Score: <strong>{raw_opinion_score} / 35</strong>
        </div>

{chr(10).join(profile_rows)}
      </div>

      <!-- Big pull quote living in the LEFT column -->
      <div class="gg-course-quote-big">
        <span>"{opinion_quote}"</span>
      </div>
    </div>

    <!-- RIGHT: COPY FOR EACH VARIABLE -->
    <div class="gg-ratings-right">

{chr(10).join(explanation_html)}
    </div>
  </div>
</section>

<script>
  (function () {{
    const section = document.querySelector("#biased-opinion");
    if (!section) return;

    const svg = section.querySelector(".gg-course-radar-svg");
    if (!svg) return;

    const ns = "http://www.w3.org/2000/svg";

    const config = {{
      center: 160,
      radius: 110,
      maxScore: 5,
      metrics: [
{js_metrics_str}
      ]
    }};

    const {{ center, radius, maxScore, metrics }} = config;
    const n = metrics.length;

    function polar(index, r) {{
      const angleDeg = (360 / n) * index - 90;
      const a = (angleDeg * Math.PI) / 180;
      return {{
        x: center + r * Math.cos(a),
        y: center + r * Math.sin(a),
        angleDeg
      }};
    }}

    // Grid rings
    const rings = 4;
    for (let i = 1; i <= rings; i++) {{
      const r = (radius * i) / rings;
      let d = "";
      for (let j = 0; j < n; j++) {{
        const {{ x, y }} = polar(j, r);
        d += (j === 0 ? "M" : "L") + x + "," + y + " ";
      }}
      d += "Z";
      const ring = document.createElementNS(ns, "path");
      ring.setAttribute("d", d);
      ring.setAttribute("class", "gg-radar-grid-ring");
      svg.appendChild(ring);
    }}

    // Axes + labels
    metrics.forEach((metric, i) => {{
      const {{ x: ex, y: ey, angleDeg }} = polar(i, radius);

      const axis = document.createElementNS(ns, "line");
      axis.setAttribute("x1", center);
      axis.setAttribute("y1", center);
      axis.setAttribute("x2", ex);
      axis.setAttribute("y2", ey);
      axis.setAttribute("class", "gg-radar-axis-line");
      svg.appendChild(axis);

      const labelPos = polar(i, radius + 24);
      const text = document.createElementNS(ns, "text");
      text.setAttribute("x", labelPos.x);
      text.setAttribute("y", labelPos.y);
      text.setAttribute(
        "text-anchor",
        angleDeg > 90 && angleDeg < 270 ? "end" : "start"
      );
      text.setAttribute("dominant-baseline", "middle");
      text.setAttribute("class", "gg-radar-label");
      text.textContent = metric.label.toUpperCase();
      svg.appendChild(text);
    }});

    // Data polygon
    let d = "";
    metrics.forEach((metric, i) => {{
      const r = (metric.value / maxScore) * radius;
      const {{ x, y }} = polar(i, r);
      d += (i === 0 ? "M" : "L") + x + "," + y + " ";
    }});
    d += "Z";

    const poly = document.createElementNS(ns, "path");
    poly.setAttribute("d", d);
    poly.setAttribute("class", "gg-radar-data-fill");
    svg.appendChild(poly);
  }})();
</script>"""
    
    return template


def generate_final_verdict_html(data: Dict) -> str:
    """Generate final verdict section HTML."""
    race = data['race']
    verdict = race['final_verdict']
    rating = race['gravel_god_rating']
    
    course_profile = rating['course_profile']
    biased_opinion = rating['biased_opinion']
    
    template = f"""<style>
  /* ==============================
     SECTION 7 – OVERALL SCORE
     ============================== */

  .gg-overall-section {{
    padding: 3rem 0 4.5rem;
  }}

  .gg-overall-header {{
    margin-bottom: 2.5rem;
  }}

  .gg-overall-header .gg-section-title {{
    font-family: "Sometype Mono", monospace;
    font-size: 2rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #59473C;
    margin: 0 0 0.75rem;
  }}

  .gg-overall-kicker {{
    font-family: "Sometype Mono", monospace;
    font-size: 0.95rem;
    color: #7A6A5E;
    margin: 0;
  }}

  .gg-pill {{
    display: inline-flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.40rem 1.7rem 0.48rem;
    border-radius: 999px;
    background: #F4D03F;
    border: 3px solid #59473C;
    box-shadow: 4px 4px 0 #59473C;
    font-family: "Sometype Mono", monospace;
    font-size: 0.90rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    white-space: nowrap;
    user-select: none;
    margin-bottom: 0.5rem;
  }}

  .gg-pill-icon {{
    font-size: 1rem;
    line-height: 1;
    transform: translateY(-1px);
  }}

  .gg-pill-text {{
    margin-top: 1px;
  }}

  /* Overall card layout */

  .gg-overall-wrap {{
    display: grid;
    grid-template-columns: minmax(0, 480px) minmax(0, 1fr);
    gap: 3rem;
    align-items: flex-start;
  }}

  .gg-overall-left,
  .gg-overall-right {{
    min-width: 0;
  }}

  .gg-overall-card {{
    position: relative;
    background: #F5F5DC;
    border: 4px solid #59473C;
    box-shadow: 10px 10px 0 #2C2C2C;
    padding: 2rem 2.2rem 2.1rem;
    font-family: "Sometype Mono", monospace;
  }}

  .gg-overall-tier-badge {{
    position: absolute;
    top: -14px;
    right: -14px;
    width: 72px;
    height: 72px;
    background: #4ECDC4;
    border: 4px solid #59473C;
    box-shadow: 6px 6px 0 #2C2C2C;
    transform: rotate(45deg);
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .gg-overall-tier-badge span {{
    transform: rotate(-45deg);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #59473C;
    text-align: center;
  }}

  .gg-overall-label {{
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: #8C7568;
    margin-bottom: 0.4rem;
  }}

  .gg-overall-score-row {{
    display: flex;
    align-items: baseline;
    gap: 0.6rem;
    margin-bottom: 0.35rem;
  }}

  .gg-overall-score-main {{
    font-size: 3rem;
    line-height: 1;
    color: #59473C;
  }}

  .gg-overall-score-total {{
    font-size: 1.2rem;
    color: #8C7568;
  }}

  .gg-overall-tier-text {{
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: #59473C;
    margin-bottom: 0.9rem;
  }}

  .gg-overall-one-liner {{
    font-size: 0.98rem;
    line-height: 1.6;
    color: #59473C;
    margin-bottom: 1.5rem;
  }}

  .gg-overall-breakdown {{
    font-size: 0.9rem;
    color: #59473C;
  }}

  .gg-overall-breakdown-table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 0.9rem;
  }}

  .gg-overall-breakdown-table td {{
    padding: 0.16rem 0;
  }}

  .gg-overall-breakdown-table td:first-child {{
    text-transform: uppercase;
    letter-spacing: 0.11em;
    font-size: 0.78rem;
    color: #8C7568;
  }}

  .gg-overall-breakdown-table td:last-child {{
    text-align: right;
    font-size: 0.9rem;
  }}

  .gg-overall-note {{
    font-size: 0.9rem;
    line-height: 1.6;
    color: #59473C;
  }}

  /* Right-side explanation */

  .gg-overall-right .gg-subheading {{
    font-family: "Sometype Mono", monospace;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin: 0 0 0.4rem;
    color: #59473C;
  }}

  .gg-overall-right p {{
    font-family: "Sometype Mono", monospace;
    font-size: 0.98rem;
    line-height: 1.7;
    color: #59473C;
    margin: 0 0 1.1rem;
  }}

  .gg-overall-right p:last-child {{
    margin-bottom: 0;
  }}

  @media (max-width: 960px) {{
    .gg-overall-wrap {{
      grid-template-columns: minmax(0, 1fr);
      gap: 2.5rem;
    }}
  }}
</style>

<section id="overall-score" class="gg-section gg-overall-section">
  <div class="gg-overall-header">
    <div class="gg-pill">
      <span class="gg-pill-icon">◆</span>
      <span class="gg-pill-text">Final verdict</span>
    </div>
    <h2 class="gg-section-title">OVERALL SCORE</h2>
    <p class="gg-overall-kicker">
      The part where we stop pretending this is objective.
    </p>
  </div>

  <div class="gg-overall-wrap">
    <!-- LEFT: BIG SCORE CARD -->
    <div class="gg-overall-left">
      <div class="gg-overall-card">
        <div class="gg-overall-tier-badge">
          <span>{rating['tier_label']}</span>
        </div>

        <div class="gg-overall-label">{race['display_name']}</div>

        <div class="gg-overall-score-row">
          <div class="gg-overall-score-main">{verdict['score'].split()[0]}</div>
          <div class="gg-overall-score-total">/100</div>
        </div>

        <div class="gg-overall-tier-text">
          {rating['tier_label']} · Iconic · High Consequence
        </div>

        <p class="gg-overall-one-liner">
          {verdict['one_liner']}
        </p>

        <div class="gg-overall-breakdown">
          <table class="gg-overall-breakdown-table">
            <tr>
              <td>Course profile (Section 5)</td>
              <td>{course_profile} / 35</td>
            </tr>
            <tr>
              <td>Editorial profile (Section 6)</td>
              <td>{biased_opinion} / 35</td>
            </tr>
            <tr>
              <td><strong>Final score</strong></td>
              <td><strong>{verdict['score']}</strong></td>
            </tr>
          </table>
        </div>
      </div>
    </div>

    <!-- RIGHT: EXPLANATION COPY -->
    <div class="gg-overall-right">
      <h3 class="gg-subheading">Should You Race This?</h3>
      <p>
        {verdict['should_you_race']}
      </p>

      <h3 class="gg-subheading">Alternatives</h3>
      <p>
        {verdict['alternatives']}
      </p>
    </div>
  </div>
</section>"""
    
    return template


def generate_logistics_html(data: Dict) -> str:
    """Generate logistics section HTML."""
    race = data['race']
    logistics = race['logistics']
    
    template = f"""<section class="gg-logistics-section">
  <div class="gg-logistics-inner">
    <!-- LEFT: LOGISTICS COPY -->
    <div>
      <div class="gg-logistics-pill">Race Logistics</div>
      <h3 class="gg-logistics-heading">The unsexy details that decide your day</h3>

      <!-- Getting There -->
      <div>
        <div class="gg-logistics-list-title">Getting There</div>
        <ul class="gg-logistics-list">
          <li><strong>Closest major airport:</strong> {logistics['airport']}</li>
          <li><strong>Transportation:</strong> {logistics['lodging_strategy'].split('.')[0]}.</li>
          <li><strong>When to arrive:</strong> Plan to arrive 2-3 days early for travel, shakeout, and gear organization.</li>
        </ul>
      </div>

      <!-- Staying There -->
      <div>
        <div class="gg-logistics-list-title">Staying There</div>
        <ul class="gg-logistics-list">
          <li><strong>Lodging:</strong> {logistics['lodging_strategy']}</li>
          <li><strong>Food & groceries:</strong> {logistics['food']}</li>
          <li><strong>Packet pickup:</strong> {logistics['packet_pickup']}</li>
          <li><strong>Parking:</strong> {logistics['parking']}</li>
        </ul>
      </div>
    </div>

    <!-- RIGHT: SINGLE LINK CARD -->
    <aside>
      <div class="gg-logistics-links">
        <div class="gg-logistics-card">
          <div class="gg-logistics-card-title">Official race info</div>
          <a href="{logistics['official_site']}" target="_blank" rel="noopener">
            Course details, rules & latest updates →
          </a>
        </div>
      </div>

      <div class="gg-logistics-disclaimer">
        This guide is my opinion as a coach and racer, not the official word from the event
        organizers. Details change—rules, cutoffs, routes, and support policies. Always double-check
        the <strong>official race website</strong> and pre-race communication before you travel or
        make big decisions.
      </div>
    </aside>
  </div>
</section>"""
    
    return template


def generate_training_plans_html(data: Dict) -> str:
    """Generate training plans section with TP URLs."""
    race = data['race']
    tp = race['training_plans']
    
    # Group plans by tier
    tiers_data = {
        'Ayahuasca': {'hours': '0–5 hrs / week', 'footer': 'For chaos schedules and stubborn goals. You train when you can, not when you "should".', 'plans': []},
        'Finisher': {'hours': '8–12 hrs / week', 'footer': 'For grown-ups with real lives who want to cross the line proud, not shattered.', 'plans': []},
        'Compete': {'hours': '12–18 hrs / week', 'footer': 'For hitters who want to be in the moves, not just in the photo dump.', 'plans': []},
        'Podium': {'hours': '18–25+ hrs / week', 'footer': 'For psychos who plan vacations around watts, weather, and start lists.', 'plans': []}
    }
    
    # Organize plans by tier
    for plan in tp['plans']:
        tier = plan['tier']
        level_display = plan['level'] if plan['level'] != 'Emergency' else 'Save My Race'
        name_display = plan['name']
        weeks = plan['weeks']
        
        # Build full TP URL
        category = plan.get('category', 'gran-fondo-century')
        tp_url = f"{tp['marketplace_base_url']}/{category}/{plan['tp_id']}/{plan['tp_slug']}"
        
        display_name = f"{level_display} – {name_display}"
        
        tiers_data[tier]['plans'].append({
            'display': display_name,
            'weeks': weeks,
            'url': tp_url
        })
    
    # Generate tier cards HTML
    tier_cards = []
    for tier_name, tier_info in tiers_data.items():
        if not tier_info['plans']:  # Skip tiers with no plans
            continue
            
        plans_html = []
        for plan in tier_info['plans']:
            plan_html = f"""        <div class="gg-plan">
          <div class="gg-plan-name">
            {plan['display']} <span>({plan['weeks']} weeks)</span>
          </div>
          <a href="{plan['url']}" class="gg-plan-cta" target="_blank">View Plan</a>
        </div>"""
            plans_html.append(plan_html)
        
        card_html = f"""    <article class="gg-volume-card">
      <div class="gg-volume-tag">Volume Track</div>
      <h3 class="gg-volume-title">{tier_name}</h3>
      <div class="gg-volume-hours">{tier_info['hours']}</div>
      <div class="gg-volume-divider"></div>

      <div class="gg-plan-stack">
{chr(10).join(plans_html)}
      </div>

      <div class="gg-volume-footer">
        {tier_info['footer']}
      </div>
    </article>"""
        tier_cards.append(card_html)
    
    template = """<section class="gg-volume-section" id="volume-tracks">
  <!-- TRAINING PLANS BADGE -->
  <div class="gg-training-plans-badge">
    <span class="gg-training-plans-badge-icon">◆</span>
    TRAINING PLANS
  </div>

  <div class="gg-volume-grid">
{tier_cards}
  </div>
</section>

<style>
/* Training Plans Badge */
.gg-training-plans-badge {{
  display: inline-block;
  background: #f4d03f;
  color: #000;
  padding: 12px 24px;
  border: 3px solid #000;
  border-radius: 50px;
  box-shadow: 6px 6px 0 #000;
  font-family: 'Sometype Mono', monospace;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: 24px;
}}

.gg-training-plans-badge-icon {{
  margin-right: 8px;
  font-size: 11px;
}}

/* Fix for button text visibility */
.gg-plan-cta {{
  display: inline-block;
  padding: 8px 16px;
  background: #40E0D0;
  color: #000 !important;
  border: 3px solid #000;
  text-decoration: none !important;
  font-family: 'Sometype Mono', monospace;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  box-shadow: 4px 4px 0 #000;
  transition: all 0.15s ease;
  cursor: pointer;
}}

.gg-plan-cta:hover {{
  background: #f4d03f;
  color: #000 !important;
  transform: translate(2px, 2px);
  box-shadow: 2px 2px 0 #000;
}}

.gg-plan-cta:active {{
  transform: translate(4px, 4px);
  box-shadow: 0 0 0 #000;
}}
</style>"""
    
    return template.format(tier_cards='\n\n'.join(tier_cards))


def find_widget_by_content(elements: List[Dict], search_pattern: str) -> Optional[Dict]:
    """Find HTML widget by searching for content pattern in HTML."""
    for element in elements:
        if element.get('widgetType') == 'html':
            settings = element.get('settings', {})
            if isinstance(settings, dict):
                html = settings.get('html', '')
                if search_pattern in html:
                    return element
        if 'elements' in element:
            result = find_widget_by_content(element['elements'], search_pattern)
            if result:
                return result
    return None


def find_widget_by_element_id(elements: List[Dict], target_id: str) -> Optional[Dict]:
    """Find widget by _element_id in settings."""
    for element in elements:
        settings = element.get('settings', {})
        if isinstance(settings, dict) and settings.get('_element_id') == target_id:
            return element
        if 'elements' in element:
            result = find_widget_by_element_id(element['elements'], target_id)
            if result:
                return result
    return None


def replace_widget_html(elementor_json: Dict, search_pattern: str, new_html: str, element_id: Optional[str] = None) -> bool:
    """Find and replace HTML widget content. Returns True if found and replaced."""
    elements = elementor_json.get('content', [])
    
    # Try element ID first if provided
    if element_id:
        widget = find_widget_by_element_id(elements, element_id)
        if widget:
            settings = widget.get('settings', {})
            if isinstance(settings, dict):
                settings['html'] = new_html
                return True
    
    # Fall back to content pattern search
    widget = find_widget_by_content(elements, search_pattern)
    if widget:
        settings = widget.get('settings', {})
        if isinstance(settings, dict):
            settings['html'] = new_html
            return True
    
    return False


def build_elementor_json(data: Dict, base_json_path: str) -> Dict:
    """Build complete Elementor JSON with all sections."""
    # Load base JSON structure
    with open(base_json_path, 'r', encoding='utf-8') as f:
        elementor_data = json.load(f)
    
    # Generate all HTML sections
    print("  Generating hero section...")
    hero_html = generate_hero_html(data)
    
    print("  Generating vitals section...")
    vitals_html = generate_vitals_html(data)
    
    print("  Generating ratings section...")
    ratings_html = generate_ratings_html(data)
    
    print("  Generating black pill section...")
    blackpill_html = generate_blackpill_html(data)
    
    print("  Generating training plans section...")
    training_html = generate_training_plans_html(data)
    
    print("  Generating course map section...")
    course_map_html = generate_course_map_html(data)
    
    print("  Generating overview hero section...")
    overview_html = generate_overview_hero_html(data)
    
    print("  Generating TLDR section...")
    tldr_html = generate_tldr_html(data)
    
    print("  Generating history section...")
    history_html = generate_history_html(data)
    
    print("  Generating biased opinion section...")
    opinion_html = generate_biased_opinion_html(data)
    
    print("  Generating final verdict section...")
    verdict_html = generate_final_verdict_html(data)
    
    print("  Generating logistics section...")
    logistics_html = generate_logistics_html(data)
    
    # Find and replace widgets in Elementor JSON
    print("  Replacing hero widget...")
    if not replace_widget_html(elementor_data, 'gg-hero-inner', hero_html):
        print("  WARNING: Hero widget not found!")
    
    print("  Replacing vitals widget...")
    if not replace_widget_html(elementor_data, 'id="race-vitals"', vitals_html, element_id='vitals'):
        print("  WARNING: Vitals widget not found!")
    
    print("  Replacing ratings widget...")
    if not replace_widget_html(elementor_data, 'id="course-ratings"', ratings_html, element_id='course'):
        print("  WARNING: Ratings widget not found!")
    
    print("  Replacing black pill widget...")
    if not replace_widget_html(elementor_data, 'gg-blackpill-section', blackpill_html, element_id='blackpill'):
        print("  WARNING: Black pill widget not found!")
    
    print("  Replacing training plans widget...")
    if not replace_widget_html(elementor_data, 'gg-volume-section', training_html, element_id='training'):
        print("  WARNING: Training plans widget not found!")
    
    print("  Replacing course map widget...")
    if not replace_widget_html(elementor_data, 'gg-route-section', course_map_html, element_id='course-map'):
        print("  WARNING: Course map widget not found!")
    
    print("  Replacing overview hero widget...")
    if not replace_widget_html(elementor_data, 'gg-overview-hero-v2', overview_html):
        print("  WARNING: Overview hero widget not found!")
    
    print("  Replacing TLDR widget...")
    if not replace_widget_html(elementor_data, 'gg-decision-grid', tldr_html, element_id='tldr'):
        print("  WARNING: TLDR widget not found!")
    
    print("  Replacing history widget...")
    if not replace_widget_html(elementor_data, 'gg-tldr-grid', history_html, element_id='history'):
        print("  WARNING: History widget not found!")
    
    print("  Replacing biased opinion widget...")
    if not replace_widget_html(elementor_data, 'gg-opinion-section', opinion_html, element_id='opinion'):
        print("  WARNING: Biased opinion widget not found!")
    
    print("  Replacing final verdict widget...")
    if not replace_widget_html(elementor_data, 'gg-overall-section', verdict_html, element_id='verdict'):
        print("  WARNING: Final verdict widget not found!")
    
    print("  Replacing logistics widget...")
    if not replace_widget_html(elementor_data, 'gg-logistics-section', logistics_html, element_id='logistics'):
        print("  WARNING: Logistics widget not found!")
    
    # Update page title
    race_name = data['race']['display_name']
    elementor_data['title'] = f"{race_name} Landing Page"
    
    return elementor_data


def generate_landing_page(race_data_path: str, base_json_path: str, output_path: str):
    """Main generation function."""
    print(f"Loading race data from {race_data_path}...")
    data = load_race_data(race_data_path)
    
    print("Generating HTML sections...")
    elementor_json = build_elementor_json(data, base_json_path)
    
    print(f"Writing Elementor JSON to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(elementor_json, f, ensure_ascii=False, indent=2)
    
    race_name = data['race']['name']
    print(f"✓ Landing page generated for {race_name}")
    print(f"✓ Output: {output_path}")
    print(f"✓ Ready to import to Elementor")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python generate_landing_page.py <race_data.json> <base_template.json> <output.json>")
        sys.exit(1)
    
    race_data_path = sys.argv[1]
    base_json_path = sys.argv[2]
    output_path = sys.argv[3]
    
    generate_landing_page(race_data_path, base_json_path, output_path)

