#!/usr/bin/env python3
"""
Generate Neo-Brutalist Landing Pages from Race Data

Takes race data JSON files and generates Elementor-ready Neo-Brutalist pages.

Usage:
    python generate_neo_brutalist.py mid-south      # Generate Mid-South page
    python generate_neo_brutalist.py --all          # Generate all races
    python generate_neo_brutalist.py mid-south --push  # Generate and push to WordPress
"""
import json
import sys
import os
import uuid
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from push_pages import WordPressPagePusher, WP_CONFIG


def generate_id():
    """Generate Elementor-style ID (8 hex chars)."""
    return uuid.uuid4().hex[:8]


def generate_neo_brutalist_html(race):
    """Generate Neo-Brutalist HTML from race data."""
    r = race['race']
    rating = r['gravel_god_rating']
    vitals = r['vitals']
    history = r['history']
    course = r['course_description']
    ratings = r.get('ratings_breakdown', {})
    opinion = r.get('biased_opinion', {})
    black_pill = r.get('black_pill', {})
    verdict = r.get('final_verdict', {})
    logistics = r.get('logistics', {})

    # Calculate bar widths
    course_profile_pct = int((rating['course_profile'] / 35) * 100)
    biased_opinion_pct = int((rating['biased_opinion'] / 35) * 100)

    # Get state from location
    location_parts = vitals['location'].split(', ')
    city = location_parts[0] if location_parts else vitals['location']
    state = location_parts[1] if len(location_parts) > 1 else ''

    # Format date
    race_date = vitals.get('date_specific', vitals.get('date', 'TBD'))
    if '2026' in race_date:
        race_date = race_date.split('2026:')[-1].strip() if '2026:' in race_date else race_date

    # Build suffering zones HTML
    suffering_zones_html = ""
    for i, zone in enumerate(course.get('suffering_zones', [])[:6]):
        highlight_class = ' course-card--highlight' if i == 1 else ''
        # Handle both 'mile' and 'stage' formats
        mile_label = zone.get('mile', zone.get('stage', i+1))
        mile_prefix = 'Stage' if 'stage' in zone else 'Mile'
        suffering_zones_html += f'''
            <div class="course-card{highlight_class}">
                <div class="course-mile">{mile_prefix} {mile_label}</div>
                <div class="course-name">{zone.get('label', zone.get('named_section', ''))}</div>
                <div class="course-desc">{zone.get('desc', '')}</div>
            </div>'''

    # Build ratings HTML (Course Profile)
    course_ratings_html = ""
    radar_vars = ['length', 'technicality', 'elevation', 'climate', 'altitude', 'adventure', 'logistics']
    for var in radar_vars:
        score = rating.get(var, 3)
        pct = score * 20
        danger_style = ' background: var(--danger);' if var == 'climate' and score >= 4 else ''
        course_ratings_html += f'''
            <div class="rating-metric">
                <span class="rating-metric-label">{var.title()}</span>
                <div class="rating-metric-bar">
                    <div class="rating-metric-fill" style="width: {pct}%;{danger_style}"></div>
                </div>
                <span class="rating-metric-value">{score}/5</span>
            </div>'''

    # Build course ratings explanation
    course_explanations_html = ""
    for var in radar_vars:
        if var in ratings:
            exp = ratings[var]
            course_explanations_html += f"<p><strong>{var.title()} ({exp['score']}/5):</strong> {exp['explanation']}</p>"

    # Build Editorial/Biased Opinion ratings - show ALL dimension scores with explanations
    opinion_ratings_html = ""
    opinion_explanations_html = ""

    # All dimensions we want to show in the editorial section
    all_dims = [
        ('prestige', 'Prestige'),
        ('length', 'Length'),
        ('technicality', 'Technicality'),
        ('elevation', 'Elevation'),
        ('climate', 'Climate'),
        ('altitude', 'Altitude'),
        ('adventure', 'Adventure'),
        ('logistics', 'Logistics')
    ]

    for key, label in all_dims:
        # Get score from gravel_god_rating
        score = rating.get(key, 0)
        if score > 0:
            pct = score * 20
            opinion_ratings_html += f'''
            <div class="rating-metric">
                <span class="rating-metric-label">{label}</span>
                <div class="rating-metric-bar">
                    <div class="rating-metric-fill" style="width: {pct}%;"></div>
                </div>
                <span class="rating-metric-value">{score}/5</span>
            </div>'''
            # Get explanation from ratings_breakdown if available
            if key in ratings and 'explanation' in ratings[key]:
                opinion_explanations_html += f"<p><strong>{label} ({score}/5):</strong> {ratings[key]['explanation']}</p>"

    # Build history timeline
    timeline_html = ""
    moments = history.get('notable_moments', [])[:5]
    for moment in moments:
        if ':' in moment:
            year, content = moment.split(':', 1)
            timeline_html += f'''
            <div class="timeline-item">
                <span class="timeline-year">{year.strip()}</span>
                <span class="timeline-content">{content.strip()}</span>
            </div>'''

    # Build strengths/weaknesses for verdict
    strengths_html = ""
    for s in opinion.get('strengths', [])[:6]:
        strengths_html += f"<li>{s}</li>"

    weaknesses_html = ""
    for w in opinion.get('weaknesses', [])[:6]:
        weaknesses_html += f"<li>{w}</li>"

    # Black pill consequences
    consequences_html = ""
    for c in black_pill.get('consequences', [])[:3]:
        consequences_html += f"<li>{c}</li>"

    # RideWithGPS embed
    rwgps_id = course.get('ridewithgps_id', '')
    rwgps_name = course.get('ridewithgps_name', r['name'].replace(' ', '%20'))
    map_embed = f'https://ridewithgps.com/embeds?type=route&amp;id={rwgps_id}&amp;title={rwgps_name}&amp;sampleGraph=true&amp;distanceMarkers=true' if rwgps_id else ''

    # Generate the full HTML
    html = f'''
<!-- HERO -->
<section class="hero" id="top">
    <div class="container">
        <div class="hero-grid">
            <div class="hero-content">
                <div class="hero-badges">
                    <span class="badge badge--tier">{rating['tier_label']} / ICONIC</span>
                    <span class="badge badge--location">{vitals['location_badge']}</span>
                    <span class="badge badge--date">{race_date}</span>
                    <span class="badge badge--distance">{vitals['distance_mi']} MI</span>
                </div>
                <h1 class="hero-title">{r['display_name']}</h1>
                <p class="hero-tagline">"{r['tagline']}"</p>
                <p class="hero-intro">{history.get('reputation', r['tagline'])}</p>
                <a class="btn" href="#training">GET YOUR TRAINING PLAN</a>
            </div>
            <div class="score-card">
                <div class="score-label">Gravel God Rating</div>
                <div class="score-main">{rating['overall_score']}<span>/100</span></div>
                <div class="tier-label">{rating['tier_label']} / HIGH CONSEQUENCE</div>
                <div class="score-breakdown">
                    <div class="breakdown-row">
                        <span class="breakdown-label">Course Profile</span>
                        <div class="breakdown-bar"><div class="breakdown-bar-fill" style="width: {course_profile_pct}%;"></div></div>
                        <span class="breakdown-score">{rating['course_profile']} / 35</span>
                    </div>
                    <div class="breakdown-row">
                        <span class="breakdown-label">Biased Opinion</span>
                        <div class="breakdown-bar"><div class="breakdown-bar-fill" style="width: {biased_opinion_pct}%;"></div></div>
                        <span class="breakdown-score">{rating['biased_opinion']} / 35</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- STICKY TOC -->
<nav class="toc">
    <div class="container">
        <div class="toc-inner">
            <a class="toc-link" href="#map">Course Map</a>
            <a class="toc-link" href="#vitals">Course Vitals</a>
            <a class="toc-link" href="#history">Facts &amp; History</a>
            <a class="toc-link" href="#course">The Course</a>
            <a class="toc-link" href="#ratings">The Ratings</a>
            <a class="toc-link" href="#opinion">Biased Opinion</a>
            <a class="toc-link" href="#blackpill">The Black Pill</a>
            <a class="toc-link" href="#verdict">Final Verdict</a>
            <a class="toc-link" href="#training">Training Plans</a>
            <a class="toc-link" href="#logistics">Race Logistics</a>
        </div>
    </div>
</nav>

<!-- COURSE MAP -->
<section class="section" id="map">
    <div class="container">
        <div class="section-header">
            <span class="section-kicker">[01] COURSE MAP</span>
            <h2 class="section-title">What {vitals['distance_mi']} Miles of {state} Gravel Looks Like</h2>
        </div>
        <div class="map-container">
            <div class="map-embed">
                <iframe class="lazyload" data-src="{map_embed}" style="width: 100%; height: 500px; border: none;"></iframe>
            </div>
            <div class="map-stats">
                <div class="stat-card"><div class="stat-value">{vitals['distance_mi']}</div><div class="stat-label">Miles</div></div>
                <div class="stat-card"><div class="stat-value">{vitals['elevation_ft']:,}</div><div class="stat-label">Feet Climbing</div></div>
                <div class="stat-card"><div class="stat-value">100%</div><div class="stat-label">Gravel</div></div>
                <div class="stat-card"><div class="stat-value">2</div><div class="stat-label">Aid Stations</div></div>
            </div>
        </div>
    </div>
</section>

<!-- COURSE VITALS -->
<section class="section" id="vitals">
    <div class="container">
        <div class="section-header">
            <span class="section-kicker">[02] COURSE VITALS</span>
            <h2 class="section-title">The Numbers That Matter</h2>
        </div>
        <div class="stats-grid--6 stats-grid">
            <div class="stat-card"><div class="stat-value stat-value--large">{vitals['distance_mi']}</div><div class="stat-label">Miles</div></div>
            <div class="stat-card"><div class="stat-value stat-value--large">{vitals['elevation_ft']//1000}K</div><div class="stat-label">Feet Elevation</div></div>
            <div class="stat-card"><div class="stat-value stat-value--large">{vitals.get('field_size', '2,500+').split()[0]}</div><div class="stat-label">Field Size</div></div>
            <div class="stat-card"><div class="stat-value stat-value--large">2</div><div class="stat-label">Aid Stations</div></div>
            <div class="stat-card"><div class="stat-value stat-value--large">N/A</div><div class="stat-label">Cutoff</div><div class="stat-sublabel">{vitals.get('cutoff_time', 'None')[:20]}</div></div>
            <div class="stat-card"><div class="stat-value stat-value--large">${vitals.get('prize_purse', '$100K').replace('$', '').split()[0]}</div><div class="stat-label">Prize Purse</div></div>
        </div>
    </div>
</section>

<!-- FACTS & HISTORY -->
<section class="section" id="history">
    <div class="container">
        <div class="section-header">
            <span class="section-kicker">[03] FACTS &amp; HISTORY</span>
            <h2 class="section-title">How It Became THE Race</h2>
        </div>
        <div class="two-col">
            <div>
                <p style="font-size: 14px; line-height: 1.8; margin-bottom: 16px;">{history.get('origin_story', '')}</p>
                <p style="font-size: 14px; line-height: 1.8;">{history.get('reputation', '')}</p>
            </div>
            <div>
                <div style="background: var(--white); border: var(--border); padding: 24px;">
                    <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 16px; font-weight: 700;">Key Moments</div>
                    <div class="timeline">{timeline_html}</div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- THE COURSE -->
<section class="section" id="course">
    <div class="container">
        <div class="section-header">
            <span class="section-kicker">[04] THE COURSE</span>
            <h2 class="section-title">Key Moments on the Route</h2>
            <p class="section-subtitle">{course.get('character', 'The locations that define this race.')}</p>
        </div>
        <div class="course-grid">{suffering_zones_html}</div>
    </div>
</section>

<!-- THE RATINGS -->
<section class="section" id="ratings">
    <div class="container">
        <div class="section-header">
            <span class="section-kicker">[05] THE RATINGS</span>
            <h2 class="section-title">Course Profile Analysis</h2>
        </div>
        <div class="rating-grid">
            <div class="rating-card">
                <div class="rating-title">Course Profile Score</div>
                <div class="rating-score">{rating['course_profile']}<span>/35</span></div>
                <div class="rating-label">RADAR BREAKDOWN</div>
                <div class="rating-metrics">{course_ratings_html}</div>
            </div>
            <div class="rating-card">
                <div class="rating-title">What Each Score Means</div>
                <div class="rating-explanation">{course_explanations_html}</div>
            </div>
        </div>
    </div>
</section>

<!-- BIASED OPINION -->
<section class="section" id="opinion">
    <div class="container">
        <div class="section-header">
            <span class="section-kicker">[06] BIASED OPINION</span>
            <h2 class="section-title">The Verdict</h2>
            <p class="section-subtitle">{opinion.get('summary', 'The course is one thing. What it means is something else entirely.')[:200]}</p>
        </div>
        <div class="rating-grid">
            <div class="rating-card">
                <div class="rating-title">Editorial Profile</div>
                <div class="rating-score">{rating['biased_opinion']}<span>/35</span></div>
                <div class="rating-label">OPINION SCORE</div>
                <div class="rating-metrics">{opinion_ratings_html}</div>
            </div>
            <div class="rating-card">
                <div class="rating-title">What Each Score Means</div>
                <div class="rating-explanation">{opinion_explanations_html}</div>
            </div>
        </div>
    </div>
</section>

<!-- THE BLACK PILL -->
<section class="blackpill" id="blackpill">
    <div class="container">
        <div class="blackpill-badge">[X] THE BLACK PILL</div>
        <h2 class="blackpill-title">{black_pill.get('title', 'The Hard Truth')}</h2>
        <p class="blackpill-body">{black_pill.get('reality', '')}</p>
        <ul class="blackpill-list">{consequences_html}</ul>
        <blockquote class="blackpill-quote">"{black_pill.get('expectation_reset', '')[:200]}"</blockquote>
    </div>
</section>

<!-- FINAL VERDICT -->
<section class="section" id="verdict">
    <div class="container">
        <div class="section-header">
            <span class="section-kicker">[07] FINAL VERDICT</span>
            <h2 class="section-title">Is This Race For You?</h2>
        </div>
        <div class="verdict-grid">
            <div class="verdict-card verdict-card--yes">
                <div class="verdict-header">[+] Race This If:</div>
                <ul class="verdict-list">{strengths_html}</ul>
            </div>
            <div class="verdict-card verdict-card--no">
                <div class="verdict-header">[-] Skip This If:</div>
                <ul class="verdict-list">{weaknesses_html}</ul>
            </div>
        </div>
    </div>
</section>

<!-- TRAINING PLANS -->
<section class="section" id="training">
    <div class="container">
        <div class="section-header">
            <span class="section-kicker">[08] TRAINING PLANS</span>
            <h2 class="section-title">Get Ready for {r['display_name']}</h2>
            <p class="section-subtitle">5 ways to prepare. Pick what fits your life.</p>
        </div>
        <div class="plans-grid">
            <div class="plan-card plan-card--1">
                <span class="plan-badge">Level 1</span>
                <div class="plan-title">Time Crunched</div>
                <div class="plan-desc">Minimal time, HIIT-focused</div>
                <div class="plan-hours">0-5 hrs/week</div>
                <a class="plan-cta" href="#">$100</a>
            </div>
            <div class="plan-card plan-card--2">
                <span class="plan-badge">Level 2</span>
                <div class="plan-title">Finisher</div>
                <div class="plan-desc">Traditional base building</div>
                <div class="plan-hours">8-10 hrs/week</div>
                <a class="plan-cta" href="#">$100</a>
            </div>
            <div class="plan-card plan-card--3">
                <span class="plan-badge">Level 3</span>
                <div class="plan-title">Compete</div>
                <div class="plan-desc">Polarized for performance</div>
                <div class="plan-hours">12-17 hrs/week</div>
                <a class="plan-cta" href="#">$100</a>
            </div>
            <div class="plan-card plan-card--4">
                <span class="plan-badge">Level 4</span>
                <div class="plan-title">Podium</div>
                <div class="plan-desc">Elite high volume</div>
                <div class="plan-hours">18-25 hrs/week</div>
                <a class="plan-cta" href="#">$100</a>
            </div>
            <div class="plan-card plan-card--masters">
                <span class="plan-badge">50+</span>
                <div class="plan-title">Masters 50+</div>
                <div class="plan-desc">Recovery-optimized</div>
                <div class="plan-hours">8-12 hrs/week</div>
                <a class="plan-cta" href="#">$100</a>
            </div>
        </div>
        <!-- TIER 2: CUSTOM PLAN CTA -->
        <div class="tier-cta-box" style="margin-top: 32px; border: 3px solid #000; padding: 24px; background: #fff; box-shadow: 6px 6px 0 #000;">
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 2rem; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 280px;">
                    <div style="font-size: 1.1rem; font-weight: 900; text-transform: uppercase; margin-bottom: 8px;">BUILT FOR YOU AND THIS RACE</div>
                    <p style="font-size: 0.85rem; color: #59473C; margin: 0;">Answer questions about your schedule, experience, and goals. Get a personalized plan for however many weeks you have.</p>
                </div>
                <a class="btn btn--accent" href="https://wattgod.github.io/training-plans-component/training-plan-questionnaire.html?race={r['slug']}" style="white-space: nowrap;">BUILD MY PLAN</a>
            </div>
        </div>
        <!-- TIER 3: COACHING CTA -->
        <div class="tier-cta-box" style="margin-top: 16px; border: 3px solid #000; padding: 24px; background: var(--accent); box-shadow: 6px 6px 0 #000;">
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 2rem; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 280px;">
                    <div style="font-size: 1.1rem; font-weight: 900; text-transform: uppercase; margin-bottom: 8px;">TRAINING THAT ADAPTS TO YOUR LIFE</div>
                    <p style="font-size: 0.85rem; color: #000; margin: 0;">Plans are templates. Coaching is personal. Get someone who adjusts your training week-to-week based on how you're actually responding.</p>
                </div>
                <a class="btn" href="https://gravelgodcycling.com/coaching/" style="background: #000; color: #fff; white-space: nowrap;">APPLY FOR COACHING</a>
            </div>
        </div>
    </div>
</section>

<!-- RACE LOGISTICS -->
<section class="section" id="logistics">
    <div class="container">
        <div class="section-header">
            <span class="section-kicker">[09] RACE LOGISTICS</span>
            <h2 class="section-title">Getting There and Staying There</h2>
        </div>
        <div class="logistics-grid">
            <div class="logistics-card">
                <div class="logistics-icon">[AIR]</div>
                <div class="logistics-title">Airport</div>
                <div class="logistics-value">{logistics.get('airport', 'TBD').split('-')[0].strip()[:20]}</div>
                <div class="logistics-detail">{logistics.get('airport', '')}</div>
            </div>
            <div class="logistics-card">
                <div class="logistics-icon">[BED]</div>
                <div class="logistics-title">Lodging</div>
                <div class="logistics-value">Book Early</div>
                <div class="logistics-detail">{logistics.get('lodging_strategy', 'Book early')[:80]}</div>
            </div>
            <div class="logistics-card">
                <div class="logistics-icon">[PIN]</div>
                <div class="logistics-title">Start/Finish</div>
                <div class="logistics-value">Downtown {city}</div>
                <div class="logistics-detail">{logistics.get('parking', 'Downtown start/finish')[:60]}</div>
            </div>
            <div class="logistics-card">
                <div class="logistics-icon">[BOX]</div>
                <div class="logistics-title">Packet Pickup</div>
                <div class="logistics-value">Friday Before</div>
                <div class="logistics-detail">{logistics.get('packet_pickup', 'Friday before race')[:60]}</div>
            </div>
            <div class="logistics-card">
                <div class="logistics-icon">[AID]</div>
                <div class="logistics-title">Aid Stations</div>
                <div class="logistics-value">{vitals.get('aid_stations', 'Multiple').split('.')[0][:20]}</div>
                <div class="logistics-detail">{vitals.get('aid_stations', '')[:60]}</div>
            </div>
            <div class="logistics-card">
                <div class="logistics-icon">[TIX]</div>
                <div class="logistics-title">Entry</div>
                <div class="logistics-value">{vitals.get('registration', 'TBD').split('.')[0][:20]}</div>
                <div class="logistics-detail">{vitals.get('registration', '')[:60]}</div>
            </div>
        </div>
    </div>
</section>

<!-- CTA -->
<section class="section section--black">
    <div class="container" style="text-align: center;">
        <h2 class="section-title" style="margin-bottom: 16px;">The Race Won't Wait</h2>
        <p class="section-subtitle" style="margin: 0 auto 32px; text-align: center; max-width: 500px;">
            {race_date}. {vitals['distance_mi']} miles. {state} doesn't care if you're ready.
        </p>
        <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap;">
            <a class="btn btn--accent" href="#training">GET A TRAINING PLAN</a>
            <a class="btn btn--outline" href="https://gravelgodcycling.com/coaching/" style="border-color: var(--white); color: var(--white);">APPLY FOR COACHING</a>
        </div>
        <div style="margin-top: 24px;">
            <a href="{logistics.get('official_site', '#')}" style="color: var(--accent); font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em;" target="_blank">Official Race Site</a>
        </div>
    </div>
</section>

<!-- FOOTER -->
<footer class="footer">
    <div class="container" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
        <div>[C] 2025 GRAVEL GOD CYCLING</div>
        <div style="font-size: 10px; opacity: 0.7;">Data sourced from race reports, forums, and official sources</div>
        <div><a href="#">ABOUT</a> / <a href="#">CONTACT</a> / <a href="#">ALL RACES</a></div>
    </div>
</footer>
'''
    return html


def get_neo_brutalist_css():
    """Return the Neo-Brutalist CSS."""
    # Read CSS from the Unbound mockup
    mockup_path = Path(__file__).parent / 'mockups' / 'neo-brutalist-mockup.html'
    if mockup_path.exists():
        with open(mockup_path, 'r') as f:
            content = f.read()
        # Extract CSS
        import re
        css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
        if css_match:
            return css_match.group(1)

    # Fallback minimal CSS
    return """
/* Neo-Brutalist Base Styles */
:root {
    --black: #000;
    --white: #fff;
    --accent: #F5B041;
    --danger: #E74C3C;
    --border: 3px solid #000;
}
body { font-family: 'Sometype Mono', monospace; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
"""


def create_elementor_template(race_data):
    """Create Elementor JSON template from race data."""
    html_content = generate_neo_brutalist_html(race_data)
    css = get_neo_brutalist_css()

    content = []

    # CSS Section
    css_widget = {
        "id": generate_id(),
        "settings": {"html": f"<style>\n{css}\n</style>"},
        "elements": [],
        "isInner": False,
        "widgetType": "html",
        "elType": "widget"
    }
    content.append({
        "id": generate_id(),
        "settings": {"layout": "full_width"},
        "elements": [{
            "id": generate_id(),
            "settings": {"_column_size": 100},
            "elements": [css_widget],
            "isInner": False,
            "elType": "column"
        }],
        "isInner": False,
        "elType": "section"
    })

    # Main content
    main_widget = {
        "id": generate_id(),
        "settings": {"html": f'<div class="gg-neo-brutalist-page">\n{html_content}\n</div>', "_css_classes": "gg-main-content"},
        "elements": [],
        "isInner": False,
        "widgetType": "html",
        "elType": "widget"
    }
    content.append({
        "id": generate_id(),
        "settings": {"layout": "full_width", "css_classes": "gg-page-wrapper"},
        "elements": [{
            "id": generate_id(),
            "settings": {"_column_size": 100},
            "elements": [main_widget],
            "isInner": False,
            "elType": "column"
        }],
        "isInner": False,
        "elType": "section"
    })

    return {
        "content": content,
        "page_settings": {"hide_title": "yes", "template": "elementor_canvas"},
        "version": "0.4",
        "title": f"{race_data['race']['display_name']} Race Guide",
        "type": "page"
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_neo_brutalist.py <race-slug> [--push]")
        print("       python generate_neo_brutalist.py --list")
        sys.exit(1)

    arg = sys.argv[1]
    push = '--push' in sys.argv

    # Find data files
    data_dir = Path(__file__).parent.parent / 'data'

    if arg == '--list':
        print("Available races:")
        for f in sorted(data_dir.glob('*-data.json')):
            print(f"  {f.stem.replace('-data', '')}")
        sys.exit(0)

    # Find the race data file
    race_slug = arg.lower().replace(' ', '-')
    data_file = data_dir / f"{race_slug}-data.json"

    if not data_file.exists():
        print(f"Data file not found: {data_file}")
        print("Use --list to see available races")
        sys.exit(1)

    print(f"Loading race data: {data_file}")
    with open(data_file, 'r') as f:
        race_data = json.load(f)

    # Generate template
    template = create_elementor_template(race_data)

    # Save to race folder
    race_name = race_data['race']['name'].replace(' ', '-')
    output_dir = Path(__file__).parent.parent / race_name / 'landing-page'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"elementor-{race_slug}-neo.json"

    with open(output_file, 'w') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    print(f"Saved: {output_file}")

    if push:
        print("\nPushing to WordPress...")
        pusher = WordPressPagePusher(
            wordpress_url=WP_CONFIG['site_url'],
            username=WP_CONFIG['username'],
            password=WP_CONFIG['app_password']
        )

        # Create the page
        elementor_data_str = json.dumps(template['content'], ensure_ascii=False)
        payload = {
            'title': template['title'],
            'slug': f"{race_slug}-race-guide",
            'status': 'publish',
            'template': 'elementor_canvas',
            'meta': {
                '_elementor_edit_mode': 'builder',
                '_elementor_template_type': 'wp-page',
                '_elementor_data': elementor_data_str,
                '_elementor_version': '3.25.10',
                '_elementor_page_settings': template['page_settings'],
                '_wp_page_template': 'elementor_canvas'
            }
        }

        url = f'{WP_CONFIG["site_url"]}/wp-json/wp/v2/pages'
        response = pusher.session.post(url, json=payload)

        if response.status_code in [200, 201]:
            result = response.json()
            page_id = result.get('id')
            print(f"Created page ID: {page_id}")
            print(f"URL: {result.get('link')}")
            pusher.regenerate_elementor_css(page_id)
        else:
            print(f"Error: {response.status_code}")
            print(response.text[:500])


if __name__ == '__main__':
    main()
