"""
Gravel God Ratings Section Generator

Generates the course ratings breakdown section with radar chart and explanations.

Usage:
    from automation.ratings import generate_ratings_html
    
    html = generate_ratings_html(race_data)
"""

from typing import Dict


def generate_ratings_html(data: Dict) -> str:
    """Generate ratings breakdown section HTML with radar chart and course profile."""
    race = data['race']
    ratings = race['ratings_breakdown']
    rating = race['gravel_god_rating']
    
    # Course profile variables (7 total, excluding prestige)
    course_categories = ['length', 'technicality', 'elevation', 'climate', 'altitude', 'adventure']
    
    # Add logistics if available (check both places)
    if 'logistics' in ratings:
        course_categories.append('logistics')
    elif 'logistics' in rating:
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
    <h2 class="gg-section-title">COURSE BREAKDOWN</h2>
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
