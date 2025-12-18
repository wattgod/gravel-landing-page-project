"""
Gravel God CTA Sections Generator

Generates both CTA sections:
- Coaching CTA
- Gravel Races CTA

Usage:
    from automation.ctas import generate_coaching_cta_html, generate_gravel_races_cta_html
    
    coaching_html = generate_coaching_cta_html()
    races_html = generate_gravel_races_cta_html()
"""


def generate_coaching_cta_html() -> str:
    """Generate coaching CTA section HTML."""
    return """<section class="gg-coaching-cta-section">
  <div class="gg-coaching-cta-card">
    <div class="gg-coaching-cta-content">
      <h3 class="gg-coaching-cta-title">Really Want to Train Right?</h3>
      <p class="gg-coaching-cta-text">
        Plans are templates. Coaching is personal. If you want someone who adapts your training to your life, not the other way around, let's talk.
      </p>
      <a href="https://gravelgodcycling.com/coaching/" class="gg-coaching-cta-button">
        Apply for Coaching →
      </a>
    </div>
  </div>
</section>

<style>
/* ============================================================================
   COACHING CTA BLOCK - NEOBRUTALIST
   ============================================================================ */
.gg-coaching-cta-section {
  margin: 3rem 0 4rem;
  padding: 0;
}

.gg-coaching-cta-card {
  border: 4px solid #000000;
  background: #4ECDC4;  /* Turquoise - matches tier badges */
  padding: 2.5rem 2rem;
  box-shadow: 10px 10px 0px 0px #000000;
  position: relative;
  max-width: 600px;
  margin: 0 auto;
}

.gg-coaching-cta-content {
  text-align: center;
}

.gg-coaching-cta-title {
  font-family: 'Sometype Mono', monospace;
  font-size: 24px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #000000;
  margin: 0 0 1rem 0;
  line-height: 1.2;
}

.gg-coaching-cta-text {
  font-family: 'Sometype Mono', monospace;
  font-size: 16px;
  line-height: 1.6;
  color: #000000;
  margin: 0 0 1.5rem 0;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.gg-coaching-cta-button {
  display: inline-block;
  padding: 14px 32px;
  background: #4ECDC4; /* Turquoise - matches card background */
  color: #000000 !important;
  border: 4px solid #000000;
  text-decoration: none !important;
  font-family: 'Sometype Mono', monospace;
  font-size: 15px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  box-shadow: 6px 6px 0 #59473C;
  transition: all 0.15s ease;
  cursor: pointer;
}

.gg-coaching-cta-button:hover {
  background: #F4D03F; /* Brand yellow - use judiciously */
  color: #000000 !important;
  transform: translate(3px, 3px);
  box-shadow: 3px 3px 0 #59473C;
}

.gg-coaching-cta-button:active {
  transform: translate(6px, 6px);
  box-shadow: 0 0 0 #59473C;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .gg-coaching-cta-card {
    padding: 2rem 1.5rem;
    box-shadow: 6px 6px 0px 0px #000000;
  }
  
  .gg-coaching-cta-title {
    font-size: 20px;
  }
  
  .gg-coaching-cta-text {
    font-size: 14px;
  }
  
  .gg-coaching-cta-button {
    padding: 12px 24px;
    font-size: 13px;
  }
}
</style>"""


def generate_gravel_races_cta_html() -> str:
    """Generate 'more gravel races' CTA section HTML."""
    return """<div class="gravel-races-cta">
  <h2>Ready to explore more suffering?</h2>
  <a href="https://gravelgodcycling.com/gravel-races/" class="gravel-races-cta-button">← ALL GRAVEL RACES</a>
</div>

<style>
@import url('https://fonts.googleapis.com/css2?family=Sometype+Mono:wght@400;700&display=swap');

.gravel-races-cta {
  background: #F5E5D3;
  padding: 60px 20px;
  border-top: 4px solid #000000;
  text-align: center;
  font-family: 'Sometype Mono', monospace;
}

.gravel-races-cta h2 {
  font-size: 28px;
  font-weight: 700;
  color: #59473C;
  margin: 0 0 30px 0;
  line-height: 1.3;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

/* Multiple selectors for maximum specificity */
.gravel-races-cta-button,
.gravel-races-cta a.gravel-races-cta-button,
a.gravel-races-cta-button:link,
a.gravel-races-cta-button:visited {
  display: inline-block !important;
  background: #4ECDC4 !important;
  color: #000000 !important;
  font-family: 'Sometype Mono', monospace !important;
  font-size: 16px !important;
  font-weight: 800 !important;
  text-decoration: none !important;
  padding: 16px 36px !important;
  border: 4px solid #000000 !important;
  box-shadow: 8px 8px 0 #000000 !important;
  transition: all 0.15s ease !important;
  text-transform: uppercase !important;
  letter-spacing: 0.12em !important;
}

.gravel-races-cta-button:hover,
.gravel-races-cta a.gravel-races-cta-button:hover {
  transform: translate(4px, 4px) !important;
  box-shadow: 4px 4px 0 #000000 !important;
  background: #F4D03F !important; /* Brand yellow - use judiciously */
  color: #000000 !important;
}

.gravel-races-cta-button:active,
.gravel-races-cta a.gravel-races-cta-button:active {
  transform: translate(8px, 8px) !important;
  box-shadow: 0 0 0 #000000 !important;
  color: #000000 !important;
}

@media (max-width: 768px) {
  .gravel-races-cta h2 {
    font-size: 22px;
  }
  
  .gravel-races-cta-button,
  .gravel-races-cta a.gravel-races-cta-button {
    font-size: 14px !important;
    padding: 14px 28px !important;
  }
}
</style>"""
