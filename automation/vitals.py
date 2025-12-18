"""
Gravel God Vitals Section Generator

Generates the race vitals table section with key facts.

Usage:
    from automation.vitals import generate_vitals_html
    
    html = generate_vitals_html(race_data)
"""

from typing import Dict


def generate_vitals_html(data: Dict) -> str:
    """Generate race vitals section HTML."""
    race = data['race']
    vitals = race['vitals']
    
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
