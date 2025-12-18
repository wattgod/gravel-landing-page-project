"""
Gravel God Logistics Section Generator

Generates the logistics section with travel, lodging, and race info.

Usage:
    from automation.logistics import generate_logistics_html
    
    html = generate_logistics_html(race_data)
"""

from typing import Dict


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
