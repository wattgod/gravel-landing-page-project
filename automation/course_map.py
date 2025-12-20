"""
Gravel God Course Map Section Generator

Generates the course map section with RideWithGPS embed and suffering zones.
Includes inline CSS for complete modularization.

Usage:
    from automation.course_map import generate_course_map_html
    
    html = generate_course_map_html(race_data)
"""

from typing import Dict


def generate_course_map_html(data: Dict) -> str:
    """Generate course map section with RideWithGPS embed and suffering zones."""
    race = data['race']
    course = race['course_description']
    rwgps_id = course.get('ridewithgps_id', '')
    rwgps_name = course.get('ridewithgps_name', race.get('display_name', 'Race Course'))
    
    # Build suffering zones HTML with enhanced details
    zones_html = []
    suffering_zones = course.get('suffering_zones', [])
    for zone in suffering_zones:
        # Handle both 'mile' and 'stage' formats
        mile = zone.get('mile') or zone.get('stage', '')
        mile_label = f"Mile {mile}" if zone.get('mile') else f"Stage {mile}" if zone.get('stage') else "Key Section"
        label = zone.get('label', '')
        desc = zone.get('desc', '')
        
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
          <div class="gg-zone-mile">{mile_label}</div>
          <div class="gg-zone-label">{label}</div>
          <div class="gg-zone-desc">{desc_html}</div>
          {citation_html}
        </div>""")
    
    # Calculate distance for title
    distance = race['vitals']['distance_mi']
    location = race['vitals']['location'].split(',')[0]  # Just city name
    
    # Use map_url if provided, otherwise use embed URL if rwgps_id exists
    map_url = course.get('map_url')
    map_note = course.get('map_note', 'Course map coming soon')
    
    if map_url:
        iframe_src = map_url
    elif rwgps_id:
        iframe_src = f"https://ridewithgps.com/embeds?type=route&id={rwgps_id}&title={rwgps_name}&sampleGraph=true&distanceMarkers=true"
    else:
        # No map available - return section without iframe
        iframe_src = None
    
    # Build map frame HTML
    if iframe_src:
        map_frame_html = f'<div class="gg-route-frame-wrap"><iframe src="{iframe_src}" style="width: 1px; min-width: 100%; height: 650px; border: none;" scrolling="no"></iframe></div>'
    else:
        map_frame_html = f'<div class="gg-route-frame-wrap"><p style="padding: 40px; text-align: center; color: #8C7568; font-family: \'Sometype Mono\', monospace; font-size: 16px;">{map_note}</p></div>'
    
    # Section HTML - compacted
    section_html = f"""<section class="gg-route-section" id="course-map">
  <div class="gg-route-card">
    <div class="gg-route-card-inner">
      <header class="gg-route-header">
        <span class="gg-pill">Course Map</span>
        <h2 class="gg-route-title">WHAT {distance} MILES OF {location.upper()} ACTUALLY LOOKS LIKE</h2>
        <p class="gg-route-lede">Hover over the profile to see where the climbs, chaos, and "why did I sign up for this" moments actually are.</p>
      </header>
      {map_frame_html}
      <div class="gg-suffering-zones">
{chr(10).join(zones_html)}
      </div>
      <div class="gg-course-breakdown-note">
        <strong>Course Breakdown:</strong> Suffering zones are based on race reports, Strava segments, and course analysis. Terrain details reflect typical conditions—weather can dramatically change difficulty.
      </div>
      <footer class="gg-route-caption">Elevation + route courtesy of RideWithGPS. Suffering courtesy of you.</footer>
    </div>
  </div>
</section>"""
    
    # Style block - complete CSS for course map section
    style_html = f"""<style>
/* Course Map Section */
.gg-route-section {{
  max-width: 1000px;
  margin: 48px auto;
  padding: 0 24px;
}}

.gg-route-card {{
  border: 4px solid #000000;
  background: #FFFFFF;
  box-shadow: 8px 8px 0px 0px #000000;
}}

.gg-route-card-inner {{
  padding: 32px;
}}

.gg-route-header {{
  text-align: center;
  margin-bottom: 32px;
}}

.gg-pill {{
  display: inline-block;
  background: #F4D03F;
  color: #000000;
  padding: 8px 20px;
  font-family: 'Sometype Mono', monospace;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  border: 3px solid #000000;
  box-shadow: 4px 4px 0 #000000;
  margin-bottom: 20px;
}}

.gg-route-title {{
  font-family: 'Sometype Mono', monospace;
  font-size: 32px;
  font-weight: 700;
  text-transform: uppercase;
  color: #000000;
  margin: 0 0 16px 0;
  line-height: 1.2;
  letter-spacing: 0.02em;
}}

.gg-route-lede {{
  font-family: 'Sometype Mono', monospace;
  font-size: 16px;
  color: #59473C;
  line-height: 1.6;
  max-width: 650px;
  margin: 0 auto;
}}

.gg-route-frame-wrap {{
  margin: 32px 0;
  border: 4px solid #000000;
  box-shadow: 6px 6px 0px 0px #000000;
  overflow: hidden;
}}

.gg-suffering-zones {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin: 32px 0;
}}

.gg-zone-card {{
  border: 4px solid #000000;
  background: #FFFFFF;
  padding: 0;
  position: relative;
  box-shadow: 8px 8px 0px 0px #000000;
  transition: transform 0.1s ease, box-shadow 0.1s ease;
  overflow: hidden;
}}

.gg-zone-card:hover {{
  transform: translate(-2px, -2px);
  box-shadow: 10px 10px 0px 0px #000000;
}}

.gg-zone-card:nth-child(odd) {{
  background: #4ECDC4;
}}

.gg-zone-card:nth-child(even) {{
  background: #FFFFFF;
}}

.gg-zone-mile {{
  position: absolute;
  top: -12px;
  left: 16px;
  background: #59473C;
  color: #FFFFFF;
  font-weight: 900;
  font-size: 14px;
  padding: 6px 12px;
  border: 3px solid #000000;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  z-index: 10;
  box-shadow: 4px 4px 0px 0px #000000;
  font-family: 'Sometype Mono', monospace;
}}

.gg-zone-label {{
  font-weight: 900;
  font-size: 20px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 24px 20px 16px 20px;
  border-bottom: 4px solid #000000;
  background: #59473C;
  color: #FFFFFF;
  line-height: 1.2;
  margin: 0;
  font-family: 'Sometype Mono', monospace;
}}

.gg-zone-desc {{
  padding: 20px;
  font-size: 15px;
  line-height: 1.6;
  color: #000000;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}}

.gg-zone-desc p {{
  margin: 0 0 12px 0;
}}

.gg-zone-desc strong {{
  font-weight: 900;
  text-transform: uppercase;
  display: block;
  margin-top: 16px;
  margin-bottom: 12px;
  padding: 10px 14px;
  background: #59473C;
  color: #FFFFFF;
  border: 3px solid #000000;
  box-shadow: 4px 4px 0px 0px #000000;
  font-family: 'Sometype Mono', monospace;
}}

.gg-zone-desc em {{
  font-style: normal;
  display: block;
  margin-top: 10px;
  padding: 10px 14px;
  background: #F0F0F0;
  border-left: 4px solid #000000;
  border-top: 2px solid #000000;
  border-right: 2px solid #000000;
  border-bottom: 2px solid #000000;
  font-weight: 600;
  color: #000000;
}}

.gg-zone-citation {{
  padding: 12px 20px;
  background: #F5F5F5;
  border-top: 3px solid #000000;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #666666;
  font-family: 'Sometype Mono', monospace;
}}

.gg-course-breakdown-note {{
  border: 4px solid #000000;
  background: #FFF5E6;
  padding: 16px 20px;
  margin-top: 32px;
  font-family: 'Sometype Mono', monospace;
  font-size: 13px;
  line-height: 1.6;
  color: #000000;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  box-shadow: 6px 6px 0px 0px #000000;
}}

.gg-course-breakdown-note strong {{
  font-weight: 900;
}}

.gg-route-caption {{
  text-align: center;
  margin-top: 24px;
  font-family: 'Sometype Mono', monospace;
  font-size: 13px;
  color: #8C7568;
  font-style: italic;
}}

/* Responsive */
@media (max-width: 768px) {{
  .gg-route-section {{
    padding: 0 16px;
  }}
  
  .gg-route-card-inner {{
    padding: 24px 16px;
  }}
  
  .gg-route-title {{
    font-size: 24px;
  }}
  
  .gg-suffering-zones {{
    grid-template-columns: 1fr;
  }}
}}
</style>"""
    
    # CRITICAL: Style tag comes AFTER section (like blackpill.py)
    return section_html + "\n" + style_html
