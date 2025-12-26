"""
Simplified Training Plans Section - 5 Core Plans

Replaces the 15-plan model with 5 core plans plus custom and coaching options.

Usage:
    from automation.simplified_training_plans_section import generate_simplified_plans_section
    
    html = generate_simplified_plans_section(
        race_name="SBT GRVL",
        race_slug="sbt-grvl"
    )
"""

from typing import Dict


def generate_simplified_plans_section(
    race_name: str,
    race_slug: str
) -> str:
    """
    Generate simplified Training Plans section with 5 core plans.
    
    Args:
        race_name: Display name of the race (e.g., "SBT GRVL")
        race_slug: URL-safe race identifier (e.g., "sbt-grvl")
    
    Returns:
        Complete HTML string for the Training Plans section
    """
    
    html = f"""<section class="training-plans-section" id="training-plans">
{get_simplified_plans_css()}
  <div class="section-header">
    <div class="section-badge">◆ Training Plans</div>
    <h2 class="section-title">Choose Your Plan</h2>
    <p class="section-subtitle">Five core plans covering every athlete, from first-time finisher to podium contender.</p>
  </div>
  
  <div class="plans-grid">
    {generate_plan_card(
        plan_number=1,
        plan_name="Finisher",
        duration="12 weeks",
        target_hours="0-5 hrs/week",
        target_athlete="Complete beginners, time-limited",
        goal="Finish the race",
        philosophy="HIIT-focused survival mode",
        replaces=["Ayahuasca Beginner", "Finisher Beginner"]
    )}
    
    {generate_plan_card(
        plan_number=2,
        plan_name="Finisher Plus",
        duration="12 weeks",
        target_hours="5-8 hrs/week",
        target_athlete="Intermediate riders, moderate time",
        goal="Finish strong and comfortable",
        philosophy="Balanced HIIT + endurance",
        replaces=["Ayahuasca Intermediate", "Finisher Intermediate"]
    )}
    
    {generate_plan_card(
        plan_number=3,
        plan_name="Compete",
        duration="12 weeks",
        target_hours="8-12 hrs/week",
        target_athlete="Advanced riders, committed training",
        goal="Competitive finish, race for position",
        philosophy="Structured periodization",
        replaces=["Compete Intermediate", "Compete Advanced"]
    )}
    
    {generate_plan_card(
        plan_number=4,
        plan_name="Compete Masters",
        duration="12 weeks",
        target_hours="8-12 hrs/week",
        target_athlete="Masters athletes (40+), experienced",
        goal="Age-group competitive",
        philosophy="Masters-optimized recovery and intensity",
        replaces=["Compete Masters", "Ayahuasca Masters", "Finisher Masters"]
    )}
    
    {generate_plan_card(
        plan_number=5,
        plan_name="Podium",
        duration="12 weeks",
        target_hours="12+ hrs/week",
        target_athlete="Elite/experienced athletes",
        goal="Race to win, podium finish",
        philosophy="High-volume, race-specific preparation",
        replaces=["Podium Advanced", "Podium Advanced GOAT"]
    )}
  </div>
  
  <div class="save-my-race-note">
    <strong>Running out of time?</strong> Add our <strong>Save My Race</strong> 6-week quick fix to any plan.
  </div>
</section>"""
    
    return html.strip()


def generate_plan_card(
    plan_number: int,
    plan_name: str,
    duration: str,
    target_hours: str,
    target_athlete: str,
    goal: str,
    philosophy: str,
    replaces: list = None
) -> str:
    """Generate HTML for a single plan card."""
    
    plan_slug = plan_name.lower().replace(" ", "-")
    
    card_html = f"""<div class="plan-card" data-plan="{plan_slug}">
      <div class="plan-header">
        <div class="plan-number">{plan_number}</div>
        <h3 class="plan-name">{plan_name}</h3>
        <div class="plan-duration">{duration}</div>
      </div>
      
      <div class="plan-details">
        <div class="plan-metric">
          <span class="metric-label">Time:</span>
          <span class="metric-value">{target_hours}</span>
        </div>
        <div class="plan-metric">
          <span class="metric-label">Target:</span>
          <span class="metric-value">{target_athlete}</span>
        </div>
        <div class="plan-metric">
          <span class="metric-label">Goal:</span>
          <span class="metric-value">{goal}</span>
        </div>
        <div class="plan-philosophy">
          <strong>Philosophy:</strong> {philosophy}
        </div>
      </div>
      
      <a href="#custom-plan" class="plan-cta">Get This Plan →</a>
    </div>"""
    
    return card_html


def get_simplified_plans_css() -> str:
    """Return the CSS for the simplified Training Plans section."""
    return """<style>
/* Simplified Training Plans Section */
.training-plans-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 48px 24px;
}

.section-header {
  text-align: center;
  margin-bottom: 48px;
}

.section-badge {
  display: inline-block;
  background: #F4D03F;
  color: #2c2c2c;
  padding: 8px 20px;
  font-family: 'Sometype Mono', monospace;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  border: 3px solid #2c2c2c;
  box-shadow: 4px 4px 0 #2c2c2c;
  margin-bottom: 20px;
}

.section-title {
  font-family: 'Sometype Mono', monospace;
  font-size: 36px;
  font-weight: 700;
  text-transform: uppercase;
  color: #2c2c2c;
  margin-bottom: 16px;
  letter-spacing: 0.02em;
}

.section-subtitle {
  font-family: 'Sometype Mono', monospace;
  font-size: 16px;
  color: #8C7568;
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Plans Grid */
.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.plan-card {
  background: #fff;
  border: 3px solid #2c2c2c;
  padding: 24px;
  box-shadow: 6px 6px 0 #2c2c2c;
  font-family: 'Sometype Mono', monospace;
  transition: transform 0.1s, box-shadow 0.1s;
}

.plan-card:hover {
  transform: translate(3px, 3px);
  box-shadow: 3px 3px 0 #2c2c2c;
}

.plan-header {
  text-align: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 2px solid #2c2c2c;
}

.plan-number {
  display: inline-block;
  background: #4ECDC4;
  color: #2c2c2c;
  width: 40px;
  height: 40px;
  border: 3px solid #2c2c2c;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 18px;
  margin: 0 auto 12px;
}

.plan-name {
  font-size: 20px;
  font-weight: 700;
  text-transform: uppercase;
  color: #2c2c2c;
  margin: 0 0 8px 0;
  letter-spacing: 0.03em;
}

.plan-duration {
  font-size: 13px;
  color: #8C7568;
  font-weight: 600;
}

.plan-details {
  margin-bottom: 20px;
}

.plan-metric {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  font-size: 13px;
}

.metric-label {
  color: #8C7568;
  font-weight: 600;
}

.metric-value {
  color: #2c2c2c;
  font-weight: 700;
  text-align: right;
  flex: 1;
  margin-left: 12px;
}

.plan-philosophy {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #E0E0E0;
  font-size: 12px;
  color: #59473C;
  line-height: 1.5;
}

.plan-philosophy strong {
  color: #2c2c2c;
}

.plan-cta {
  display: block;
  text-align: center;
  background: #2c2c2c;
  color: #F5F5DC !important;
  padding: 12px 24px;
  font-family: 'Sometype Mono', monospace;
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  text-decoration: none !important;
  letter-spacing: 0.05em;
  border: 2px solid #2c2c2c;
  transition: background 0.2s, color 0.2s;
}

.plan-cta:hover {
  background: #4ECDC4;
  color: #2c2c2c !important;
}

.save-my-race-note {
  text-align: center;
  padding: 16px;
  background: #F5F5DC;
  border: 2px solid #2c2c2c;
  font-family: 'Sometype Mono', monospace;
  font-size: 13px;
  color: #59473C;
  margin-top: 24px;
}

/* Responsive */
@media (max-width: 900px) {
  .plans-grid {
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 20px;
  }
}

@media (max-width: 600px) {
  .plans-grid {
    grid-template-columns: 1fr;
  }
  
  .section-title {
    font-size: 28px;
  }
}
</style>"""


def generate_simplified_plans_html(data: Dict) -> str:
    """
    Generate simplified Training Plans section from race data dict.
    
    Args:
        data: Race data dictionary with 'race' key
    
    Returns:
        Complete HTML string for the Training Plans section
    """
    race = data['race']
    race_name = race.get('display_name', race.get('name', 'This Race'))
    race_slug = race.get('slug', 'race')
    
    return generate_simplified_plans_section(
        race_name=race_name,
        race_slug=race_slug
    )


# Test
if __name__ == "__main__":
    html = generate_simplified_plans_section(
        race_name="SBT GRVL",
        race_slug="sbt-grvl"
    )
    print("Generated HTML length:", len(html))
    print("\nFirst 800 chars:")
    print(html[:800])
    print("\n✓ Module working correctly")

