"""
Gravel God Course Map Section Generator

Generates the course map section with RideWithGPS embed and suffering zones.

Usage:
    from automation.course_map import generate_course_map_html
    
    html = generate_course_map_html(race_data)
"""

from typing import Dict


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
        
        # Build structured HTML with proper detail boxes
        desc_html = f'<p>{desc}</p>'
        
        if named_section:
            desc_html += f'<strong>{named_section}</strong>'
        
        detail_boxes = []
        if terrain_detail:
            detail_boxes.append(f'<em>{terrain_detail}</em>')
        if weather_note:
            detail_boxes.append(f'<em>{weather_note}</em>')
        
        if detail_boxes:
            desc_html += ''.join(detail_boxes)
        
        zones_html.append(f"""        <div class="gg-zone-card">
          <div class="gg-zone-mile">Mile {mile}</div>
          <div class="gg-zone-label">{label}</div>
          <div class="gg-zone-desc">{desc_html}</div>
          {citation_html}
        </div>""")
    
    # Calculate distance for title
    distance = race['vitals']['distance_mi']
    location = race['vitals']['location'].split(',')[0]  # Just city name
    
    # Use map_url if provided, otherwise use embed URL
    map_url = course.get('map_url')
    if map_url:
        iframe_src = map_url
    else:
        iframe_src = f"https://ridewithgps.com/embeds?type=route&id={rwgps_id}&title={rwgps_name}&sampleGraph=true&distanceMarkers=true"
    
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
          src="{iframe_src}"
          style="width: 1px; min-width: 100%; height: 650px; border: none;"
          scrolling="no"
        ></iframe>
      </div>

      <!-- Suffering Zones -->
      <div class="gg-suffering-zones">
{chr(10).join(zones_html)}
      </div>

      <!-- Course Breakdown Research Note -->
      <div class="gg-course-breakdown-note">
        <strong>Course Breakdown:</strong> Suffering zones are based on race reports, Strava segments, and course analysis. Terrain details reflect typical conditions—weather can dramatically change difficulty.
      </div>

      <footer class="gg-route-caption">
        Elevation + route courtesy of RideWithGPS. Suffering courtesy of you.
      </footer>

    </div>
  </div>
</section>"""
    
    return template
