"""
Custom Training Plan Section

Standalone section for "Build My Custom Training Plan" option.
Positioned after the 5 core plans.

Usage:
    from automation.custom_training_plan_section import generate_custom_plan_section
    
    html = generate_custom_plan_section(
        race_name="SBT GRVL",
        race_slug="sbt-grvl"
    )
"""

from typing import Dict


def generate_custom_plan_section(
    race_name: str,
    race_slug: str
) -> str:
    """
    Generate Custom Training Plan section.
    
    Args:
        race_name: Display name of the race (e.g., "SBT GRVL")
        race_slug: URL-safe race identifier (e.g., "sbt-grvl")
    
    Returns:
        Complete HTML string for the Custom Training Plan section
    """
    
    questionnaire_url = f"https://wattgod.github.io/training-plans-component/training-plan-questionnaire.html?race={race_slug}"
    
    html = f"""<section class="custom-plan-section" id="custom-plan">
{get_custom_plan_css()}
  <div class="section-header">
    <div class="section-badge">◆ Custom Plans</div>
    <h2 class="section-title">Need Something Different?</h2>
    <p class="section-subtitle">Build a custom plan tailored to <strong>YOUR</strong> life, schedule, and goals.</p>
  </div>
  
  <div class="custom-plan-content">
    <div class="custom-plan-left">
      <h3>Why Custom?</h3>
      <ul class="custom-benefits">
        <li>
          <div class="benefit-icon">✓</div>
          <div class="benefit-text">
            <strong>Personalized to your schedule</strong>
            <span>Works around your work, family, and life commitments</span>
          </div>
        </li>
        <li>
          <div class="benefit-icon">✓</div>
          <div class="benefit-text">
            <strong>Race-specific adaptations</strong>
            <span>Calibrated to {race_name}'s unique demands and terrain</span>
          </div>
        </li>
        <li>
          <div class="benefit-icon">✓</div>
          <div class="benefit-text">
            <strong>Workouts for any device</strong>
            <span>Garmin · Wahoo · Hammerhead · Zwift · TrainerRoad · TrainingPeaks</span>
          </div>
        </li>
        <li>
          <div class="benefit-icon">✓</div>
          <div class="benefit-text">
            <strong>Delivered same day</strong>
            <span>Complete plan with strategy guide, fueling, and pacing playbooks</span>
          </div>
        </li>
      </ul>
    </div>
    
    <div class="custom-plan-right">
      <div class="custom-cta-block">
        <h3>Build My Custom Training Plan</h3>
        <p class="cta-subtitle">Takes 5 minutes. Get your plan today.</p>
        <a href="{questionnaire_url}" class="custom-cta-button" target="_blank">
          Start Questionnaire →
        </a>
        <div class="cta-includes">
          <div class="include-item">✓ 35,000+ word gravel manual</div>
          <div class="include-item">✓ Heat, fueling, pacing playbooks</div>
          <div class="include-item">✓ Race-specific strategy</div>
          <div class="include-item">✓ Workouts ready to upload</div>
        </div>
      </div>
    </div>
  </div>
</section>"""
    
    return html.strip()


def get_custom_plan_css() -> str:
    """Return the CSS for the Custom Training Plan section."""
    return """<style>
/* Custom Training Plan Section */
.custom-plan-section {
  max-width: 1100px;
  margin: 0 auto;
  padding: 48px 24px;
  background: #F5F5DC;
}

.section-header {
  text-align: center;
  margin-bottom: 40px;
}

.section-badge {
  display: inline-block;
  background: #4ECDC4;
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
  color: #59473C;
  max-width: 650px;
  margin: 0 auto;
  line-height: 1.6;
}

.section-subtitle strong {
  color: #2c2c2c;
}

.custom-plan-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: start;
}

.custom-plan-left h3 {
  font-family: 'Sometype Mono', monospace;
  font-size: 20px;
  font-weight: 700;
  text-transform: uppercase;
  color: #2c2c2c;
  margin-bottom: 24px;
}

.custom-benefits {
  list-style: none;
  padding: 0;
  margin: 0;
}

.custom-benefits li {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  align-items: flex-start;
}

.benefit-icon {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  background: #4ECDC4;
  border: 2px solid #2c2c2c;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: #2c2c2c;
  font-weight: 700;
}

.benefit-text {
  flex: 1;
  font-family: 'Sometype Mono', monospace;
  font-size: 14px;
}

.benefit-text strong {
  display: block;
  color: #2c2c2c;
  font-weight: 700;
  margin-bottom: 4px;
}

.benefit-text span {
  color: #59473C;
  font-size: 13px;
  line-height: 1.5;
}

.custom-cta-block {
  background: #2c2c2c;
  padding: 32px;
  border: 4px solid #2c2c2c;
  box-shadow: 8px 8px 0 #59473C;
  text-align: center;
}

.custom-cta-block h3 {
  font-family: 'Sometype Mono', monospace;
  color: #F5F5DC;
  font-size: 22px;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.cta-subtitle {
  font-family: 'Sometype Mono', monospace;
  color: #A89074;
  font-size: 13px;
  margin-bottom: 24px;
}

.custom-cta-button {
  display: inline-block;
  background: #4ECDC4;
  color: #2c2c2c !important;
  padding: 18px 40px;
  font-family: 'Sometype Mono', monospace;
  font-size: 16px;
  font-weight: 700;
  text-transform: uppercase;
  text-decoration: none !important;
  letter-spacing: 0.05em;
  border: 3px solid #F5F5DC;
  box-shadow: 6px 6px 0 #F4D03F;
  transition: transform 0.1s, box-shadow 0.1s;
  margin-bottom: 24px;
}

.custom-cta-button:hover {
  transform: translate(3px, 3px);
  box-shadow: 3px 3px 0 #F4D03F;
  color: #2c2c2c !important;
}

.cta-includes {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 24px;
}

.include-item {
  font-family: 'Sometype Mono', monospace;
  color: #F5F5DC;
  font-size: 13px;
  text-align: left;
}

/* Responsive */
@media (max-width: 900px) {
  .custom-plan-content {
    grid-template-columns: 1fr;
    gap: 32px;
  }
  
  .custom-plan-left {
    order: 2;
  }
  
  .custom-plan-right {
    order: 1;
  }
}

@media (max-width: 600px) {
  .section-title {
    font-size: 28px;
  }
  
  .custom-cta-block {
    padding: 24px;
  }
}
</style>"""


def generate_custom_plan_html(data: Dict) -> str:
    """
    Generate Custom Training Plan section from race data dict.
    
    Args:
        data: Race data dictionary with 'race' key
    
    Returns:
        Complete HTML string for the Custom Training Plan section
    """
    race = data['race']
    race_name = race.get('display_name', race.get('name', 'This Race'))
    race_slug = race.get('slug', 'race')
    
    return generate_custom_plan_section(
        race_name=race_name,
        race_slug=race_slug
    )


# Test
if __name__ == "__main__":
    html = generate_custom_plan_section(
        race_name="SBT GRVL",
        race_slug="sbt-grvl"
    )
    print("Generated HTML length:", len(html))
    print("\nFirst 600 chars:")
    print(html[:600])
    print("\n✓ Module working correctly")

