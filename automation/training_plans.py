#!/usr/bin/env python3
"""
Training Plans HTML Generator
=============================
Generates the EXACT training plans section HTML structure with:
- Links always present on workout cards
- Style tag AFTER </section> (not inside)
- Card CSS in base file (validated separately)
- Exact indentation and structure matching template

This module ensures consistency and prevents the back-and-forth
we've been having with template structure.
"""

from typing import Dict, List


def generate_training_plans_html(tiers_data: Dict, race_name: str = "") -> str:
    """
    Generate training plans section HTML with exact template structure.
    
    Args:
        tiers_data: Dict with keys 'Ayahuasca', 'Finisher', 'Compete', 'Podium'
                   Each tier has: 'hours', 'footer', 'plans' (list of dicts)
                   Each plan has: 'display', 'weeks', 'url'
        race_name: Optional race name for context (not used in output)
    
    Returns:
        Complete HTML string with section, cards, and style tag AFTER section
    """
    tier_cards = []
    
    for tier_name, tier_info in tiers_data.items():
        if not tier_info.get('plans'):  # Skip tiers with no plans
            continue
        
        plans_html = []
        for plan in tier_info['plans']:
            plan_url = plan.get('url', '#')
            plan_display = plan.get('display', '')
            plan_weeks = plan.get('weeks', 0)
            
            plan_html = f"""        <div class="gg-plan">
          <div class="gg-plan-name">
            {plan_display} <span>({plan_weeks} weeks)</span>
          </div>
          <a href="{plan_url}" class="gg-plan-cta" target="_blank">View Plan</a>
        </div>"""
            plans_html.append(plan_html)
        
        card_html = f"""    <!-- ================= {tier_name.upper()} ================= -->
    <article class="gg-volume-card">
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
    
    # EXACT template structure - style tag AFTER </section>
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
  background: #f4d03f; /* Yellow */
  color: #000;
  padding: 12px 24px;
  border: 3px solid #000;
  border-radius: 50px; /* Pill shape */
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
  background: #40E0D0; /* Turquoise */
  color: #000 !important; /* Black for maximum visibility - !important to override inheritance */
  border: 3px solid #000;
  text-decoration: none !important;
  font-family: 'Sometype Mono', monospace;
  font-size: 13px;
  font-weight: 700; /* Bolder */
  text-transform: uppercase;
  letter-spacing: 0.08em;
  box-shadow: 4px 4px 0 #000;
  transition: all 0.15s ease;
  cursor: pointer;
}}

.gg-plan-cta:hover {{
  background: #f4d03f; /* Yellow */
  color: #000 !important; /* Black text for contrast - !important to override */
  transform: translate(2px, 2px);
  box-shadow: 2px 2px 0 #000;
}}

.gg-plan-cta:active {{
  transform: translate(4px, 4px);
  box-shadow: 0 0 0 #000;
}}
</style>"""
    
    return template.format(tier_cards='\n\n'.join(tier_cards))


def build_training_plans_data(tp_data: Dict) -> Dict:
    """
    Build tiers_data structure from training plans JSON data.
    
    Args:
        tp_data: Training plans data from race JSON with 'plans' list
    
    Returns:
        tiers_data dict ready for generate_training_plans_html()
    """
    tp = tp_data.get('training_plans', {})
    
    # Initialize tier structure
    tiers_data = {
        'Ayahuasca': {
            'hours': '0–5 hrs / week',
            'footer': 'For chaos schedules and stubborn goals. You train when you can, not when you "should".',
            'plans': []
        },
        'Finisher': {
            'hours': '8–12 hrs / week',
            'footer': 'For grown-ups with real lives who want to cross the line proud, not shattered.',
            'plans': []
        },
        'Compete': {
            'hours': '12–18 hrs / week',
            'footer': 'For hitters who want to be in the moves, not just in the photo dump.',
            'plans': []
        },
        'Podium': {
            'hours': '18–25+ hrs / week',
            'footer': 'For psychos who plan vacations around watts, weather, and start lists.',
            'plans': []
        }
    }
    
    # Organize plans by tier
    for plan in tp.get('plans', []):
        tier = plan.get('tier')
        level = plan.get('level')
        level_display = level if level != 'Emergency' else 'Save My Race'
        name_display = plan.get('name')
        weeks = plan.get('weeks', 0)
        
        # Format display name to match template exactly
        if tier == 'Ayahuasca':
            if level == 'Masters 50+':
                display_name = "Master's 50+ Plan"
            elif level == 'Emergency':
                display_name = "Save My Race – Emergency Plan"
            else:
                display_name = f"{level_display} – {name_display}"
        elif tier == 'Finisher':
            if level == 'Beginner':
                display_name = f"Beginner – {name_display}"
            elif level == 'Masters 50+':
                display_name = f"Finisher Master's – 50+ Plan"
            elif level == 'Emergency':
                display_name = f"Finisher – Save My Race"
            else:
                display_name = f"Finisher {level_display} – {name_display}"
        elif tier == 'Compete':
            if level == 'Masters 50+':
                display_name = f"Compete Master's – 50+ Performance"
            elif level == 'Emergency':
                display_name = f"Compete – Save My Race"
            else:
                display_name = f"Compete {level_display} – {name_display}"
        elif tier == 'Podium':
            display_name = f"Podium {level_display} – {name_display}"
        else:
            display_name = f"{level_display} – {name_display}"
        
        # Build TrainingPeaks URL
        tp_id = plan.get('tp_id', 'PLACEHOLDER_NEEDS_RESEARCH')
        tp_slug = plan.get('tp_slug', '')
        category = plan.get('category', 'gran-fondo-century')
        marketplace_base = tp.get('marketplace_base_url', 'https://www.trainingpeaks.com/training-plans/cycling')
        
        if tp_id and tp_id != 'PLACEHOLDER_NEEDS_RESEARCH' and tp_slug:
            plan_url = f"{marketplace_base}/{category}/tp-{tp_id}/{tp_slug}"
        else:
            plan_url = "#"  # Placeholder if URL not ready
        
        if tier in tiers_data:
            tiers_data[tier]['plans'].append({
                'display': display_name,
                'weeks': weeks,
                'url': plan_url
            })
    
    return tiers_data
