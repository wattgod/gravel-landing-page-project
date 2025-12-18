"""
Gravel God TLDR/Decision Section Generator

Generates the TLDR decision grid with "Should Race" / "Skip If" cards.

Usage:
    from automation.tldr import generate_tldr_html
    
    html = generate_tldr_html(race_data)
"""

from typing import Dict


def generate_tldr_html(data: Dict) -> str:
    """Generate TLDR/Decision section HTML - brief and scannable (2-3 sentences max, ~40-60 words)."""
    race = data['race']
    
    # Use tldr fields if available (preferred - already condensed)
    if 'tldr' in race:
        tldr = race['tldr']
        should_race_condensed = tldr.get('should_race_if', 'You value community and authentic hospitality over predictable conditions.')
        skip_if_text = tldr.get('skip_if', 'You need to know exactly what you\'re getting into before you commit.')
    else:
        # Fallback: extract from final_verdict and condense
        verdict = race.get('final_verdict', {})
        should_race_full = verdict.get('should_you_race', 'You like hurting yourself, surprises (not the good kind), and you\'re prepared to commit a month of salary and (hopefully) a shit load of training getting ready for one truly insane day.')
        
        # Condense to core message - extract key points
        should_race_condensed = should_race_full
        
        # If it's too long, extract the core message
        if len(should_race_full.split()) > 60:
            sentences = should_race_full.split('. ')
            if len(sentences) >= 2:
                should_race_condensed = '. '.join(sentences[:2]) + '.'
                if len(should_race_condensed.split()) > 60:
                    should_race_condensed = sentences[0] + '.'
            else:
                if 'value' in should_race_full.lower():
                    parts = should_race_full.split('—')
                    if len(parts) > 0:
                        should_race_condensed = parts[0].strip() + '.'
        
        # Get skip_if
        skip_if_text = 'You\'re not ready to find out what\'s actually inside you.'
        if 'reconsider' in should_race_full.lower():
            parts = should_race_full.split('—')
            if len(parts) > 1:
                skip_part = parts[1].strip()
                skip_sentences = skip_part.split('. ')
                if len(skip_sentences) >= 2:
                    skip_if_text = '. '.join(skip_sentences[:2]) + '.'
                else:
                    skip_if_text = skip_part
                if len(skip_if_text.split()) > 60:
                    skip_if_text = skip_sentences[0] + '.' if skip_sentences else skip_if_text
    
    template = f"""<div class="gg-decision-grid">
  <div class="gg-decision-card gg-decision-card--yes">
    <h3>You Should Race This If:</h3>
    <p>{should_race_condensed}</p>
    <a href="#training" class="gg-decision-cta">Get a Training Plan →</a>
  </div>

  <div class="gg-decision-card gg-decision-card--no">
    <h3>Skip This If:</h3>
    <p>{skip_if_text}</p>
    
  </div>
</div>"""
    
    return template
