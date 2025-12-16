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
        <span>"Something will break out there. Hopefully not you."</span>
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
        js_metrics=js_metrics_str
    )


def generate_blackpill_html(data: Dict) -> str:
    """Generate Black Pill section HTML."""
    race = data['race']
    bp = race['black_pill']
    
    consequences_items = '\n      '.join([f'<li>{c}</li>' for c in bp['consequences']])
    
    template = """<section class="gg-blackpill-section">

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
    Unbound doesn't fit inside a season. It defines it.
  </div>

</section>"""
    
    return template.format(
        title=bp['title'],
        reality=bp['reality'],
        consequences=consequences_items,
        expectation_reset=bp['expectation_reset']
    )


def generate_course_map_html(data: Dict) -> str:
    """Generate course map section with RideWithGPS embed and suffering zones."""
    race = data['race']
    course = race['course_description']
    rwgps_id = course['ridewithgps_id']
    rwgps_name = course['ridewithgps_name']
    
    # Build suffering zones HTML
    zones_html = []
    for zone in course['suffering_zones']:
        zones_html.append(f"""        <div class="gg-zone-card">
          <div class="gg-zone-mile">Mile {zone['mile']}</div>
          <div class="gg-zone-label">{zone['label']}</div>
          <div class="gg-zone-desc">{zone['desc']}</div>
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

      <footer class="gg-route-caption">
        Elevation + route courtesy of RideWithGPS. Suffering courtesy of you.
      </footer>

    </div>
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

