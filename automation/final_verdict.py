"""
Gravel God Final Verdict Section Generator

Generates the final verdict section with overall score card and recommendations.

Usage:
    from automation.final_verdict import generate_final_verdict_html
    
    html = generate_final_verdict_html(race_data)
"""

from typing import Dict


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
