"""
Gravel God Biased Opinion Section Generator

Generates the biased opinion section with editorial radar chart and explanations.

Usage:
    from automation.biased_opinion import generate_biased_opinion_html
    
    html = generate_biased_opinion_html(race_data)
"""

from typing import Dict


def generate_biased_opinion_html(data: Dict) -> str:
    """Generate biased opinion section - EXACTLY matches Course Profile structure."""
    race = data['race']
    ratings = race['ratings_breakdown']
    biased = race['biased_opinion']
    race_name = race['display_name']
    
    # These are the 7 biased opinion ratings
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
    words = opinion_quote.split()
    if len(words) > 30:
        sentences = opinion_quote.split('. ')
        if sentences and len(sentences[0].split()) <= 30:
            opinion_quote = sentences[0] + '.'
        else:
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
