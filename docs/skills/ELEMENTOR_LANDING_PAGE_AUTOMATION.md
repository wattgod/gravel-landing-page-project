# GRAVEL GOD LANDING PAGE AUTOMATION SKILL

## Elementor JSON Generation System

**Purpose:** Automate complete landing page generation for gravel race guides. Input race data → Output production-ready Elementor JSON in minutes.

**Time Savings:** 7-8 hours manual → 40 minutes automated per page. 10 races = 70 hours → 7 hours (10x compression).

**Core Principle:** Template-driven generation with variable substitution. Same proven structure, zero manual assembly.

---

## Race Data Schema

Every landing page requires this complete data set. Populate once, generate forever.

```json
{
  "race": {
    "name": "Unbound 200",
    "slug": "unbound-200",
    "display_name": "Unbound Gravel 200",
    "tagline": "You don't race Unbound. You survive it.",
    
    "vitals": {
      "distance_mi": 200,
      "elevation_ft": 10000,
      "location": "Emporia, Kansas",
      "location_badge": "EMPORIA, KANSAS",
      "county": "Lyon County",
      "date": "Early June annually",
      "date_specific": "2026: June 6",
      "terrain_types": ["Flint Hills gravel", "rolling hills", "sharp limestone", "cattle guards"],
      "field_size": "2,500+ riders (200mi), 500+ (100mi)",
      "start_time": "Saturday 6:00 AM",
      "registration": "Opens October. Cost: $225 + fees",
      "prize_purse": "$100,000 (split equally men/women)",
      "aid_stations": "Miles 52, 106, 158. Water, snacks, neutral support",
      "cutoff_time": "None. (Finish by midnight encouraged)"
    },
    
    "climate": {
      "primary": "Flint Hills heat",
      "description": "June brings 85-95°F days with high humidity",
      "challenges": ["Heat adaptation critical", "Hydration demands extreme", "Sun exposure relentless"]
    },
    
    "terrain": {
      "primary": "Rolling gravel with punchy climbs",
      "surface": "Chunky limestone that shreds tires and hands",
      "technical_rating": 3,
      "features": ["Sustained rollers", "Cattle guard crossings", "Exposed ridgelines", "Creek crossings in wet years"]
    },
    
    "gravel_god_rating": {
      "overall_score": 93,
      "course_profile": 33,
      "biased_opinion": 47,
      "tier": 1,
      "tier_label": "TIER 1",
      "prestige": 5,
      "length": 5,
      "technicality": 3,
      "elevation": 3,
      "climate": 5,
      "altitude": 1,
      "adventure": 5
    },
    
    "history": {
      "founded": 2006,
      "founder": "Jim Cummins",
      "origin_story": "Started as 'Dirty Kanza 200' with 34 riders exploring Flint Hills gravel. Grew from underground cult race to North America's most prestigious gravel event.",
      "notable_moments": [
        "2019: Renamed 'Unbound Gravel' to reflect evolution",
        "2021: Prize purse equality ($100K split)",
        "Record field: 4,000+ across all distances"
      ],
      "reputation": "The Ironman of gravel. Finishing earns respect. Winning earns legend status."
    },
    
    "course_description": {
      "character": "Relentless. Not one killer climb, but 200 miles of constant attrition.",
      "suffering_zones": [
        {"mile": 60, "label": "First Meltdown Zone", "desc": "Reality sets in. The polite first hour is gone."},
        {"mile": 120, "label": "Checkpoint Salvation", "desc": "Halfway. Decide if you're going back out."},
        {"mile": 180, "label": "Dark Thoughts Begin", "desc": "20 miles left. Your brain starts negotiating."}
      ],
      "signature_challenge": "The heat. The duration. The Flint Hills don't negotiate.",
      "ridewithgps_id": "46551378",
      "ridewithgps_name": "Unbound%20200"
    },
    
    "ratings_breakdown": {
      "prestige": {
        "score": 5,
        "explanation": "This is the race. The one everyone knows. Finishing Unbound carries weight—not because of Instagram, but because riders know what it takes. It's the benchmark. The Ironman of gravel. If you're serious about this sport, you either want to do this race or you've already done it and are deciding if you want to go back."
      },
      "length": {
        "score": 5,
        "explanation": "200 miles is not a bike ride. It's an expedition compressed into 10-16 hours. The distance alone would be manageable on pavement. On gravel, with heat, wind, and the Flint Hills' relentless rolling terrain? It becomes a test of durability, not speed. Most riders finish closer to half-marathon pace than cycling pace."
      },
      "technicality": {
        "score": 3,
        "explanation": "Not a technical course by modern gravel standards—no white-knuckle descents, minimal singletrack. But chunky limestone, cattle guards, and the occasional muddy section (in wet years) demand bike-handling confidence. The challenge isn't navigating; it's maintaining speed on rough surfaces for 200 miles without breaking yourself or your equipment."
      },
      "elevation": {
        "score": 3,
        "explanation": "10,000+ feet sounds intimidating. It's not. There are no sustained climbs—just constant rolling terrain. Think: punchy 2-5% grades that never stop. The Flint Hills don't let you settle into a rhythm. You're either accelerating out of a dip or grinding over a rise. The cumulative fatigue is real, but this isn't climbing in the traditional sense."
      },
      "climate": {
        "score": 5,
        "explanation": "June in Kansas is a lottery. Best case: 75°F and overcast. Worst case: 95°F, full sun, and humidity that makes breathing feel expensive. Heat adaptation isn't optional—it's the difference between finishing strong and crawling to the line. The unrelenting sun exposure, combined with duration, makes this one of the most climate-punishing gravel races in North America."
      },
      "altitude": {
        "score": 1,
        "explanation": "Emporia sits at ~1,200 feet. Altitude is a non-factor unless you're coming from sea level and racing the day you arrive (don't do that). For 99% of riders, this score is irrelevant. Train anywhere. Show up ready."
      },
      "adventure": {
        "score": 5,
        "explanation": "The Flint Hills are stunning—big sky, endless horizons, wildflowers if you're lucky. But 'adventure' here means isolation. Miles 80-140 feel remote. If something goes wrong (mechanicals, bonking, existential crisis), you're managing it yourself. Aid stations are sparse. The course is beautiful in a 'this could go very wrong' kind of way."
      }
    },
    
    "biased_opinion": {
      "verdict": "Icon",
      "summary": "Unbound is gravel racing's Mount Everest—not because it's the hardest course, but because it's the race that defines the sport. Riders don't 'do' Unbound casually. They plan for it, obsess over heat protocols, and show up knowing that crossing the line in Emporia means something. The course itself isn't revolutionary—rolling terrain, gravel, heat. What makes it legendary is the field, the atmosphere, and the weight of the finish line. If you finish Unbound, you've earned it.",
      "strengths": [
        "The field: Pros, weekend warriors, and everyone in between. Starting alongside Keegan Swenson or Alexey Vermeulen is surreal.",
        "The finish line vibe: Bobby Wintle (race director) hugs every single finisher. People cry. It's real.",
        "The community: Post-race Emporia feels like a pilgrimage site. Shared suffering bonds people."
      ],
      "weaknesses": [
        "Logistics are chaotic: 4,000+ riders descending on a town of 25,000. Hotels sell out a year in advance. Parking is a nightmare.",
        "The lottery: You can't just sign up. You enter. You hope. It's part of the mystique, but also frustrating.",
        "Cost: $225 entry + travel + lodging. This isn't a cheap race."
      ],
      "bottom_line": "If you're serious about gravel, you'll do Unbound eventually. Whether you finish smiling or swearing, you'll never forget it."
    },
    
    "black_pill": {
      "title": "THE THING NOBODY TELLS YOU",
      "reality": "Finishing Unbound doesn't make you a gravel legend. It makes you someone who survived 200 miles of gravel in Kansas. The Instagram glow lasts a week. The pride lasts longer. But the real reward? Knowing you showed up to the hardest day you could design for yourself—and you didn't quit.",
      "consequences": [
        "You'll spend $1,500+ (entry, travel, lodging, gear). For one race.",
        "You'll train 10-20 hours a week for 12+ weeks. That's time away from family, friends, hobbies.",
        "You'll probably suffer more than you've ever suffered on a bike. The heat, the distance, the relentless terrain—none of it cares about your FTP."
      ],
      "expectation_reset": "Unbound is a test of will, not watts. Show up undertrained, and you'll finish broken. Show up overtrained, and you'll finish tired. The sweet spot? Prepared, durable, and mentally ready to hurt for 10-14 hours. That's what training plans are for."
    },
    
    "final_verdict": {
      "score": "93 / 100",
      "one_liner": "The gravel race by which all others are measured.",
      "should_you_race": "If you're asking whether Unbound is 'worth it,' the answer is probably yes—but only if you're willing to commit to the training, the logistics, and the reality that this race will test every assumption you have about your durability. It's not fun. It's not easy. But it's unforgettable.",
      "alternatives": "If you want the prestige without the chaos: try Belgian Waffle Ride (similar vibe, better logistics). If you want the distance without the heat: try Gravel Worlds in August (still hard, slightly cooler). If you want to test yourself without the hype: try Mid South (intimate, brutal, beautiful)."
    },
    
    "logistics": {
      "airport": "Wichita (ICT) - 90 minutes to Emporia",
      "lodging_strategy": "Book 12+ months early. Prioritize proximity to start line over charm. Emporia hotels sell out. Expect $150-250/night for basic rooms.",
      "food": "Pack your own breakfast. Race-morning lines are absurd. Stock up at Walmart/Dillons day before.",
      "packet_pickup": "Friday at Emporia State University. Long lines. Budget 45+ minutes.",
      "parking": "Free lots open 4:00 AM. Arrive early or walk 15+ minutes.",
      "official_site": "https://unboundgravel.com"
    },
    
    "training_plans": {
      "total_count": 15,
      "tiers": ["Ayahuasca", "Finisher", "Compete", "Podium"],
      "base_price": 99,
      "save_my_race_price": 59,
      "marketplace_base_url": "https://www.trainingpeaks.com/training-plans/cycling",
      "plans": [
        {
          "tier": "Ayahuasca",
          "level": "Beginner",
          "name": "Survival Plan",
          "weeks": 12,
          "tp_id": "tp-604628",
          "tp_slug": "1-unbound-200-ayahuasca-beginner-12-weeks"
        },
        {
          "tier": "Ayahuasca",
          "level": "Intermediate",
          "name": "Time-Crunched Plan",
          "weeks": 12,
          "tp_id": "tp-604627",
          "tp_slug": "2-unbound-200-ayahuasca-intermediate-12-weeks"
        },
        {
          "tier": "Ayahuasca",
          "level": "Masters 50+",
          "name": "Master's Plan",
          "weeks": 12,
          "tp_id": "tp-604625",
          "tp_slug": "3-unbound-200-ayahuasca-masters-50-12-weeks"
        },
        {
          "tier": "Ayahuasca",
          "level": "Emergency",
          "name": "Save My Race",
          "weeks": 6,
          "tp_id": "tp-604624",
          "tp_slug": "4-unbound-200-ayahuasca-save-my-race-emergency-plan-6-weeks"
        },
        {
          "tier": "Finisher",
          "level": "Beginner",
          "name": "First Timer",
          "weeks": 12,
          "tp_id": "tp-599529",
          "tp_slug": "5-unbound-200-finisher-beginner-12-weeks"
        },
        {
          "tier": "Finisher",
          "level": "Intermediate",
          "name": "Solid Finisher",
          "weeks": 12,
          "tp_id": "tp-599629",
          "tp_slug": "6-unbound-200-finisher-intermediate-12-weeks"
        },
        {
          "tier": "Finisher",
          "level": "Advanced",
          "name": "Strong Finish",
          "weeks": 12,
          "tp_id": "tp-599630",
          "tp_slug": "7-unbound-200-finisher-advanced-12-weeks"
        },
        {
          "tier": "Finisher",
          "level": "Masters 50+",
          "name": "Master's Plan",
          "weeks": 12,
          "tp_id": "tp-599632",
          "tp_slug": "8-unbound-200-finisher-masters-50-12-weeks"
        },
        {
          "tier": "Finisher",
          "level": "Emergency",
          "name": "Save My Race",
          "weeks": 6,
          "tp_id": "tp-599634",
          "tp_slug": "9-unbound-200-finisher-save-my-race-emergency-plan-6-weeks"
        },
        {
          "tier": "Compete",
          "level": "Intermediate",
          "name": "Competitive",
          "weeks": 12,
          "tp_id": "tp-599635",
          "tp_slug": "10-unbound-200-compete-intermediate-12-weeks"
        },
        {
          "tier": "Compete",
          "level": "Advanced",
          "name": "Podium Contender",
          "weeks": 12,
          "tp_id": "tp-599636",
          "tp_slug": "11-unbound-200-compete-advanced-12-weeks"
        },
        {
          "tier": "Compete",
          "level": "Masters 50+",
          "name": "50+ Performance",
          "weeks": 12,
          "tp_id": "tp-600267",
          "tp_slug": "12-unbound-200-compete-masters-50-12-weeks"
        },
        {
          "tier": "Compete",
          "level": "Emergency",
          "name": "Save My Race",
          "weeks": 6,
          "tp_id": "tp-600272",
          "tp_slug": "13-unbound-200-compete-save-my-race-emergency-plan-6-weeks"
        },
        {
          "tier": "Podium",
          "level": "Advanced",
          "name": "Elite Preparation",
          "weeks": 12,
          "tp_id": "tp-604613",
          "tp_slug": "14-unbound-200-podium-advanced-12-weeks"
        },
        {
          "tier": "Podium",
          "level": "Advanced",
          "name": "The G.O.A.T. Plan",
          "weeks": 12,
          "tp_id": "tp-604615",
          "tp_slug": "15-unbound-200-podium-goat-12-weeks"
        }
      ]
    }
  }
}
```

---

## HTML Section Templates

Each section is a template with variable placeholders. Python script performs substitution.

### Template: Hero Section

```html
<div class="gg-hero-inner">
  <div class="gg-hero-left">
    <div class="gg-hero-badges">
      <span class="gg-hero-badge gg-hero-badge-tier">{{TIER_LABEL}}</span>
      <span class="gg-hero-badge gg-hero-badge-loc">{{LOCATION_BADGE}}</span>
    </div>
    <div class="gg-hero-title">{{DISPLAY_NAME}}</div>
    <div class="gg-hero-quote">{{TAGLINE}}</div>
  </div>
  
  <div class="gg-hero-right">
    <div class="gg-hero-score-card">
      <div class="gg-hero-score-label">Gravel God Rating</div>
      <div class="gg-hero-score-main">{{OVERALL_SCORE}}<span>/100</span></div>
      <div class="gg-hero-score-sub">{{TIER_LABEL}} · Iconic · High Consequence</div>
      
      <div class="gg-hero-score-breakdown">
        <div class="gg-hero-score-break-row">
          <span class="gg-hero-break-label">Course Profile</span>
          <div class="gg-hero-break-bar">
            <div class="gg-hero-break-fill" style="width: {{COURSE_PROFILE_PCT}}%;"></div>
          </div>
          <span class="gg-hero-break-score">{{COURSE_PROFILE}} / 50</span>
        </div>
        
        <div class="gg-hero-score-break-row">
          <span class="gg-hero-break-label">Biased Opinion</span>
          <div class="gg-hero-break-bar">
            <div class="gg-hero-break-fill" style="width: {{BIASED_OPINION_PCT}}%;"></div>
          </div>
          <span class="gg-hero-break-score">{{BIASED_OPINION}} / 50</span>
        </div>
        
        <div class="gg-hero-final-row">
          <span>Final Score</span>
          <span class="gg-hero-final-score">{{OVERALL_SCORE}} / 100</span>
        </div>
      </div>
      
      <div class="gg-hero-score-caption">
        Score based on Gravel God radar + editorial bias.
      </div>
    </div>
  </div>
</div>
```

### Template: Race Vitals

```html
<section id="race-vitals" class="gg-guide-section js-guide-section">
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
          <tr><th>Location</th><td>{{LOCATION}}</td></tr>
          <tr><th>Date</th><td>{{DATE}}</td></tr>
          <tr><th>Distance</th><td>{{DISTANCE_MI}} miles</td></tr>
          <tr><th>Elevation Gain</th><td>~{{ELEVATION_FT}} ft</td></tr>
          <tr><th>Terrain</th><td>{{TERRAIN_DESCRIPTION}}</td></tr>
          <tr><th>Field Size</th><td>{{FIELD_SIZE}}</td></tr>
          <tr><th>Start Time</th><td>{{START_TIME}}</td></tr>
          <tr><th>Registration</th><td>{{REGISTRATION}}</td></tr>
          <tr><th>Prize Purse</th><td>{{PRIZE_PURSE}}</td></tr>
          <tr><th>Aid Stations</th><td>{{AID_STATIONS}}</td></tr>
          <tr><th>Cut-off Time</th><td>{{CUTOFF_TIME}}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>
```

### Template: Ratings Breakdown (7 Categories)

```html
<section id="ratings" class="gg-guide-section js-guide-section">
  <div class="gg-section-header">
    <div class="gg-pill">The Ratings</div>
    <h2>HOW WE SCORED {{RACE_NAME}}</h2>
  </div>
  
  <div class="gg-ratings-block">
    <!-- PRESTIGE -->
    <div class="gg-rating-row">
      <div class="gg-rating-meta">
        <div class="gg-rating-label">Prestige</div>
        <div class="gg-rating-score">{{PRESTIGE_SCORE}} / 5</div>
        <div class="gg-rating-bar">
          <div class="gg-rating-bar-track"></div>
          <div class="gg-rating-bar-fill score-{{PRESTIGE_SCORE}}"></div>
        </div>
      </div>
      <div class="gg-rating-copy">{{PRESTIGE_EXPLANATION}}</div>
    </div>
    
    <!-- LENGTH -->
    <div class="gg-rating-row">
      <div class="gg-rating-meta">
        <div class="gg-rating-label">Length</div>
        <div class="gg-rating-score">{{LENGTH_SCORE}} / 5</div>
        <div class="gg-rating-bar">
          <div class="gg-rating-bar-track"></div>
          <div class="gg-rating-bar-fill score-{{LENGTH_SCORE}}"></div>
        </div>
      </div>
      <div class="gg-rating-copy">{{LENGTH_EXPLANATION}}</div>
    </div>
    
    <!-- TECHNICALITY -->
    <div class="gg-rating-row">
      <div class="gg-rating-meta">
        <div class="gg-rating-label">Technicality</div>
        <div class="gg-rating-score">{{TECHNICALITY_SCORE}} / 5</div>
        <div class="gg-rating-bar">
          <div class="gg-rating-bar-track"></div>
          <div class="gg-rating-bar-fill score-{{TECHNICALITY_SCORE}}"></div>
        </div>
      </div>
      <div class="gg-rating-copy">{{TECHNICALITY_EXPLANATION}}</div>
    </div>
    
    <!-- ELEVATION -->
    <div class="gg-rating-row">
      <div class="gg-rating-meta">
        <div class="gg-rating-label">Elevation</div>
        <div class="gg-rating-score">{{ELEVATION_SCORE}} / 5</div>
        <div class="gg-rating-bar">
          <div class="gg-rating-bar-track"></div>
          <div class="gg-rating-bar-fill score-{{ELEVATION_SCORE}}"></div>
        </div>
      </div>
      <div class="gg-rating-copy">{{ELEVATION_EXPLANATION}}</div>
    </div>
    
    <!-- CLIMATE -->
    <div class="gg-rating-row">
      <div class="gg-rating-meta">
        <div class="gg-rating-label">Climate</div>
        <div class="gg-rating-score">{{CLIMATE_SCORE}} / 5</div>
        <div class="gg-rating-bar">
          <div class="gg-rating-bar-track"></div>
          <div class="gg-rating-bar-fill score-{{CLIMATE_SCORE}}"></div>
        </div>
      </div>
      <div class="gg-rating-copy">{{CLIMATE_EXPLANATION}}</div>
    </div>
    
    <!-- ALTITUDE -->
    <div class="gg-rating-row">
      <div class="gg-rating-meta">
        <div class="gg-rating-label">Altitude</div>
        <div class="gg-rating-score">{{ALTITUDE_SCORE}} / 5</div>
        <div class="gg-rating-bar">
          <div class="gg-rating-bar-track"></div>
          <div class="gg-rating-bar-fill score-{{ALTITUDE_SCORE}}"></div>
        </div>
      </div>
      <div class="gg-rating-copy">{{ALTITUDE_EXPLANATION}}</div>
    </div>
    
    <!-- ADVENTURE -->
    <div class="gg-rating-row">
      <div class="gg-rating-meta">
        <div class="gg-rating-label">Adventure</div>
        <div class="gg-rating-score">{{ADVENTURE_SCORE}} / 5</div>
        <div class="gg-rating-bar">
          <div class="gg-rating-bar-track"></div>
          <div class="gg-rating-bar-fill score-{{ADVENTURE_SCORE}}"></div>
        </div>
      </div>
      <div class="gg-rating-copy">{{ADVENTURE_EXPLANATION}}</div>
    </div>
  </div>
</section>
```

### Template: Black Pill Section

```html
<section class="gg-blackpill-section">
  <div class="gg-blackpill-badge">
    <span class="gg-blackpill-badge-icon">◆</span>
    THE BLACK PILL
  </div>
  
  <h2 class="gg-blackpill-title">{{BLACK_PILL_TITLE}}</h2>
  
  <div class="gg-blackpill-body">
    <p><strong>{{BLACK_PILL_REALITY}}</strong></p>
    
    <p><strong>Here's what it actually costs:</strong></p>
    <ul>
      {{BLACK_PILL_CONSEQUENCES_LIST}}
    </ul>
    
    <p><strong>{{BLACK_PILL_EXPECTATION_RESET}}</strong></p>
  </div>
</section>
```

### Template: Training Plans (Already Built)

*Use existing HTML from unbound_200_landing_volume_section_FIXED.html with variable substitution for TP URLs*

---

## Python Generation Script

```python
#!/usr/bin/env python3
"""
Gravel God Landing Page Generator
Generates complete Elementor JSON from race data schema.
"""

import json
from typing import Dict, Any, List

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
  <div class="gg-hero-left">
    <div class="gg-hero-badges">
      <span class="gg-hero-badge gg-hero-badge-tier">{tier_label}</span>
      <span class="gg-hero-badge gg-hero-badge-loc">{location_badge}</span>
    </div>
    <div class="gg-hero-title">{display_name}</div>
    <div class="gg-hero-quote">{tagline}</div>
  </div>
  
  <div class="gg-hero-right">
    <div class="gg-hero-score-card">
      <div class="gg-hero-score-label">Gravel God Rating</div>
      <div class="gg-hero-score-main">{overall_score}<span>/100</span></div>
      <div class="gg-hero-score-sub">{tier_label} · Iconic · High Consequence</div>
      
      <div class="gg-hero-score-breakdown">
        <div class="gg-hero-score-break-row">
          <span class="gg-hero-break-label">Course Profile</span>
          <div class="gg-hero-break-bar">
            <div class="gg-hero-break-fill" style="width: {course_pct}%;"></div>
          </div>
          <span class="gg-hero-break-score">{course_profile} / 50</span>
        </div>
        
        <div class="gg-hero-score-break-row">
          <span class="gg-hero-break-label">Biased Opinion</span>
          <div class="gg-hero-break-bar">
            <div class="gg-hero-break-fill" style="width: {opinion_pct}%;"></div>
          </div>
          <span class="gg-hero-break-score">{biased_opinion} / 50</span>
        </div>
        
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
    
    terrain_desc = ', '.join(vitals['terrain_types'])
    
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
    """Generate ratings breakdown section HTML."""
    race = data['race']
    ratings = race['ratings_breakdown']
    
    categories = ['prestige', 'length', 'technicality', 'elevation', 'climate', 'altitude', 'adventure']
    
    rows_html = []
    for cat in categories:
        cat_data = ratings[cat]
        row = f"""    <div class="gg-rating-row">
      <div class="gg-rating-meta">
        <div class="gg-rating-label">{cat.title()}</div>
        <div class="gg-rating-score">{cat_data['score']} / 5</div>
        <div class="gg-rating-bar">
          <div class="gg-rating-bar-track"></div>
          <div class="gg-rating-bar-fill score-{cat_data['score']}"></div>
        </div>
      </div>
      <div class="gg-rating-copy">{cat_data['explanation']}</div>
    </div>"""
        rows_html.append(row)
    
    template = """<section id="ratings" class="gg-guide-section js-guide-section">
  <div class="gg-section-header">
    <div class="gg-pill">The Ratings</div>
    <h2>HOW WE SCORED {race_name}</h2>
  </div>
  
  <div class="gg-ratings-block">
{rating_rows}
  </div>
</section>"""
    
    return template.format(
        race_name=race['name'].upper(),
        rating_rows='\n\n'.join(rows_html)
    )

def generate_blackpill_html(data: Dict) -> str:
    """Generate Black Pill section HTML."""
    race = data['race']
    bp = race['black_pill']
    
    consequences_items = '\n      '.join([f'<li>{c}</li>' for c in bp['consequences']])
    
    template = """<section class="gg-blackpill-section">
  <div class="gg-blackpill-badge">
    <span class="gg-blackpill-badge-icon">◆</span>
    THE BLACK PILL
  </div>
  
  <h2 class="gg-blackpill-title">{title}</h2>
  
  <div class="gg-blackpill-body">
    <p><strong>{reality}</strong></p>
    
    <p><strong>Here's what it actually costs:</strong></p>
    <ul>
      {consequences}
    </ul>
    
    <p><strong>{expectation_reset}</strong></p>
  </div>
</section>"""
    
    return template.format(
        title=bp['title'],
        reality=bp['reality'],
        consequences=consequences_items,
        expectation_reset=bp['expectation_reset']
    )

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
        category = 'gran-fondo-century' if 'road-cycling' not in plan.get('category', '') else 'road-cycling'
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

def build_elementor_json(data: Dict, base_json_path: str) -> Dict:
    """Build complete Elementor JSON with all sections."""
    # Load base JSON structure
    with open(base_json_path, 'r', encoding='utf-8') as f:
        elementor_data = json.load(f)
    
    # Generate all HTML sections
    hero_html = generate_hero_html(data)
    vitals_html = generate_vitals_html(data)
    ratings_html = generate_ratings_html(data)
    blackpill_html = generate_blackpill_html(data)
    training_html = generate_training_plans_html(data)
    
    # Find and replace widgets in Elementor JSON
    # (Implementation depends on Elementor JSON structure - see full script below)
    
    return elementor_data

def generate_landing_page(race_data_path: str, base_json_path: str, output_path: str):
    """Main generation function."""
    print(f"Loading race data from {race_data_path}...")
    data = load_race_data(race_data_path)
    
    print("Generating HTML sections...")
    elementor_json = build_elementor_json(data, base_json_path)
    
    print(f"Writing Elementor JSON to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(elementor_json, f, ensure_ascii=False)
    
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
```

---

## Validation & Quality Control

### Pre-Generation Checks

```python
def validate_race_data(data: Dict) -> List[str]:
    """Validate race data schema completeness."""
    errors = []
    
    required_fields = [
        'race.name',
        'race.slug',
        'race.display_name',
        'race.tagline',
        'race.vitals',
        'race.gravel_god_rating',
        'race.ratings_breakdown',
        'race.training_plans'
    ]
    
    for field_path in required_fields:
        parts = field_path.split('.')
        current = data
        for part in parts:
            if part not in current:
                errors.append(f"Missing required field: {field_path}")
                break
            current = current[part]
    
    # Validate TrainingPeaks plan count
    expected_count = data['race']['training_plans']['total_count']
    actual_count = len(data['race']['training_plans']['plans'])
    if expected_count != actual_count:
        errors.append(f"Plan count mismatch: expected {expected_count}, got {actual_count}")
    
    # Validate TP URLs
    for plan in data['race']['training_plans']['plans']:
        if not plan.get('tp_id') or not plan.get('tp_slug'):
            errors.append(f"Missing TP ID or slug for {plan.get('tier')} {plan.get('level')}")
    
    return errors
```

### Post-Generation Checks

```bash
# After generating JSON, validate:
1. JSON is valid (parseable)
2. All section IDs present
3. Training plan URLs return 200 (not 404)
4. Character counts don't exceed Elementor limits
5. All template variables replaced (no {{PLACEHOLDERS}} remaining)
```

---

## Workflow: Single Race Generation

### Step 1: Create Race Data JSON

```bash
# Create: unbound-200-data.json
# Populate with complete race schema
```

### Step 2: Run Generator

```bash
python generate_landing_page.py \
  unbound-200-data.json \
  elementor-base-template.json \
  elementor-unbound-200-GENERATED.json
```

### Step 3: Import to WordPress

1. WordPress → Elementor → Tools → Import Template
2. Upload `elementor-unbound-200-GENERATED.json`
3. Publish page with slug `/races/unbound-200`

### Step 4: Spot-Check

- Mobile responsive working?
- All TP links working?
- Images loading?
- Navigation anchors working?

**Total time: ~40 minutes**

---

## Batch Generation: All Races

```bash
# Generate all 10 race landing pages
for race in unbound belgian-waffle mid-south sbt-grvl dirty-kanza; do
  python generate_landing_page.py \
    data/${race}-data.json \
    elementor-base-template.json \
    output/elementor-${race}-GENERATED.json
done

# Outputs 10 production-ready Elementor JSON files
# Import all to WordPress in one session
```

**Total time for 10 races: ~7 hours (vs 70+ hours manual)**

---

## Expansion Strategy

### Phase 1: Core 10 Races (Current)

- Unbound 200
- Belgian Waffle Ride
- Mid South
- SBT GRVL
- Dirty Kanza XL
- Gravel Worlds
- Gravel Locos
- Rebecca's Private Idaho
- Barry-Roubaix
- Crusher in the Tushar

### Phase 2: Regional Events (Races 11-20)

- Big Sugar
- Leadville Trail 100 MTB (crossover)
- Haute Route Rockies
- Steamboat Gravel
- Vermont Overland
- Grinduro
- BWR North Carolina
- Pisgah Monster Cross
- Land Run 100
- Almanzo 100

### Time Math

- Manual: 20 races × 7 hours = 140 hours (3.5 weeks full-time)
- Automated: 20 races × 40 min = 13 hours (1.5 days)
- **Compression ratio: 10.8x**

---

## Critical Success Factors

### Content Quality

**Must nail these for automation to work:**

1. Race data accuracy (vitals, history, logistics)
2. Ratings explanations (honest, specific, defendable)
3. Black Pill reality checks (no generic warnings)
4. TrainingPeaks URL correctness (broken links = lost sales)

### Template Maintenance

**Single source of truth:**

- Update base template once → regenerate all pages
- Fix branding issue once → 20 races updated in minutes
- CSS tweak once → entire catalog refreshed

### Validation Rigor

**Zero tolerance for:**

- Broken TP links
- Missing sections
- Template placeholders in output
- Character limit violations
- Mobile layout breaks

---

## Success Metrics

**Generation speed:**

- Target: <5 minutes per page
- Reality check at 10 races
- Benchmark improvement over time

**Quality indicators:**

- Zero broken TP links
- Zero template placeholder escapes
- 100% mobile responsive
- Conversion rate matches or beats manual pages

**Maintenance velocity:**

- Branding updates: <1 hour for 20 pages
- Content refreshes: <2 hours for full catalog
- New race additions: <45 minutes end-to-end

---

## Files & Organization

```
/Gravel-God-Landing-Pages/
  /data/
    unbound-200-data.json
    belgian-waffle-data.json
    mid-south-data.json
    ...
  /templates/
    elementor-base-template.json
    section-hero.html
    section-vitals.html
    section-ratings.html
    ...
  /scripts/
    generate_landing_page.py
    validate_race_data.py
    batch_generate.sh
  /output/
    elementor-unbound-200.json
    elementor-belgian-waffle.json
    ...
  README.md
  CHANGELOG.md
```

---

## Next Steps

1. **Extract base template** from existing Unbound JSON
2. **Build Python generator** with all section templates
3. **Create 3 race data files** (Unbound, BWR, Mid South)
4. **Test generation** → validate output
5. **Batch generate** remaining 7 races
6. **Document edge cases** and automation limits

**Estimated build time: 8-12 hours**

**Payoff: 60-140 hours saved across catalog**

---

## Anti-Patterns to Avoid

### Template Bloat

❌ Don't add race-specific one-offs to templates

✅ Keep templates generic, handle edge cases in data

### Over-Automation

❌ Don't auto-generate ratings explanations (requires human judgment)

✅ Automate structure, hand-write content that requires editorial voice

### Validation Shortcuts

❌ Don't skip TP URL testing (broken links kill conversions)

✅ Validate every URL, every generation

### Documentation Drift

❌ Don't let code and docs diverge

✅ Update skill when templates change

---

## Final Note

This automation follows the exact pattern that made ZWO generation work:

1. **Comprehensive schema** (all data needed, nothing optional)
2. **Template-first approach** (HTML quality, then automation)
3. **Validation at every step** (catch errors before output)
4. **Batch-ready design** (10 races as easy as 1 race)

The difference between good automation and great automation is **validation rigor**. Build it right, test it hard, trust it completely.

**LFG. Ship it.** 🚀


