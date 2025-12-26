"""
Coaching Section

Standalone section for "Get Coaching" option.
Positioned after the Custom Training Plan section.

Usage:
    from automation.coaching_section import generate_coaching_section
    
    html = generate_coaching_section()
"""

from typing import Dict, Optional


def generate_coaching_section(
    coaching_email: str = "gravelgodcoaching@gmail.com",
    coaching_url: Optional[str] = None
) -> str:
    """
    Generate Coaching section.
    
    Args:
        coaching_email: Email address for coaching inquiries
        coaching_url: Optional URL to coaching page or contact form
    
    Returns:
        Complete HTML string for the Coaching section
    """
    
    cta_link = coaching_url or f"mailto:{coaching_email}?subject=Coaching Inquiry"
    cta_text = "Get Started →" if coaching_url else "Contact Me →"
    
    html = f"""<section class="coaching-section" id="coaching">
{get_coaching_css()}
  <div class="section-header">
    <div class="section-badge">◆ Coaching</div>
    <h2 class="section-title">Want More Support?</h2>
    <p class="section-subtitle">Get personalized coaching with weekly check-ins, race strategy, and unlimited questions.</p>
  </div>
  
  <div class="coaching-content">
    <div class="coaching-left">
      <div class="coaching-cta-block">
        <h3>Get Coaching</h3>
        <p class="cta-subtitle">Weekly adjustments, strategy calls, and race-day support</p>
        <a href="{cta_link}" class="coaching-cta-button">
          {cta_text}
        </a>
        <div class="coaching-contact">
          <div class="contact-item">
            <span class="contact-label">Email:</span>
            <a href="mailto:{coaching_email}" class="contact-value">{coaching_email}</a>
          </div>
        </div>
      </div>
    </div>
    
    <div class="coaching-right">
      <h3>What's Included</h3>
      <ul class="coaching-features">
        <li>
          <div class="feature-icon">✓</div>
          <div class="feature-text">
            <strong>Weekly plan adjustments</strong>
            <span>Your plan evolves based on progress, fatigue, and life changes</span>
          </div>
        </li>
        <li>
          <div class="feature-icon">✓</div>
          <div class="feature-text">
            <strong>Pre-race strategy call</strong>
            <span>30-60 minute call to dial in pacing, fueling, and race execution</span>
          </div>
        </li>
        <li>
          <div class="feature-icon">✓</div>
          <div class="feature-text">
            <strong>Unlimited questions</strong>
            <span>Email or messaging support for training, nutrition, and strategy</span>
          </div>
        </li>
        <li>
          <div class="feature-icon">✓</div>
          <div class="feature-text">
            <strong>TrainingPeaks integration</strong>
            <span>Plans synced to your TrainingPeaks calendar with automatic updates</span>
          </div>
        </li>
        <li>
          <div class="feature-icon">✓</div>
          <div class="feature-text">
            <strong>Race-day support</strong>
            <span>Pre-race check-in and post-race analysis</span>
          </div>
        </li>
      </ul>
    </div>
  </div>
</section>"""
    
    return html.strip()


def get_coaching_css() -> str:
    """Return the CSS for the Coaching section."""
    return """<style>
/* Coaching Section */
.coaching-section {
  max-width: 1100px;
  margin: 0 auto;
  padding: 48px 24px;
}

.section-header {
  text-align: center;
  margin-bottom: 40px;
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
  max-width: 650px;
  margin: 0 auto;
  line-height: 1.6;
}

.coaching-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: start;
}

.coaching-cta-block {
  background: #2c2c2c;
  padding: 32px;
  border: 4px solid #2c2c2c;
  box-shadow: 8px 8px 0 #59473C;
  text-align: center;
}

.coaching-cta-block h3 {
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

.coaching-cta-button {
  display: inline-block;
  background: #F4D03F;
  color: #2c2c2c !important;
  padding: 18px 40px;
  font-family: 'Sometype Mono', monospace;
  font-size: 16px;
  font-weight: 700;
  text-transform: uppercase;
  text-decoration: none !important;
  letter-spacing: 0.05em;
  border: 3px solid #F5F5DC;
  box-shadow: 6px 6px 0 #4ECDC4;
  transition: transform 0.1s, box-shadow 0.1s;
  margin-bottom: 24px;
}

.coaching-cta-button:hover {
  transform: translate(3px, 3px);
  box-shadow: 3px 3px 0 #4ECDC4;
  color: #2c2c2c !important;
}

.coaching-contact {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #59473C;
}

.contact-item {
  font-family: 'Sometype Mono', monospace;
  font-size: 13px;
  color: #F5F5DC;
}

.contact-label {
  color: #A89074;
  margin-right: 8px;
}

.contact-value {
  color: #4ECDC4;
  text-decoration: none;
}

.contact-value:hover {
  text-decoration: underline;
}

.coaching-right h3 {
  font-family: 'Sometype Mono', monospace;
  font-size: 20px;
  font-weight: 700;
  text-transform: uppercase;
  color: #2c2c2c;
  margin-bottom: 24px;
}

.coaching-features {
  list-style: none;
  padding: 0;
  margin: 0;
}

.coaching-features li {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  align-items: flex-start;
}

.feature-icon {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  background: #F4D03F;
  border: 2px solid #2c2c2c;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: #2c2c2c;
  font-weight: 700;
}

.feature-text {
  flex: 1;
  font-family: 'Sometype Mono', monospace;
  font-size: 14px;
}

.feature-text strong {
  display: block;
  color: #2c2c2c;
  font-weight: 700;
  margin-bottom: 4px;
}

.feature-text span {
  color: #59473C;
  font-size: 13px;
  line-height: 1.5;
}

/* Responsive */
@media (max-width: 900px) {
  .coaching-content {
    grid-template-columns: 1fr;
    gap: 32px;
  }
  
  .coaching-left {
    order: 1;
  }
  
  .coaching-right {
    order: 2;
  }
}

@media (max-width: 600px) {
  .section-title {
    font-size: 28px;
  }
  
  .coaching-cta-block {
    padding: 24px;
  }
}
</style>"""


def generate_coaching_html(data: Dict) -> str:
    """
    Generate Coaching section from race data dict.
    
    Args:
        data: Race data dictionary (coaching section is race-agnostic)
    
    Returns:
        Complete HTML string for the Coaching section
    """
    return generate_coaching_section()


# Test
if __name__ == "__main__":
    html = generate_coaching_section()
    print("Generated HTML length:", len(html))
    print("\nFirst 600 chars:")
    print(html[:600])
    print("\n✓ Module working correctly")

