#!/usr/bin/env python3
"""
Convert markdown descriptions to Sultanic V3 HTML structure
Keeps the HTML template structure but uses new markdown content
Removes Section X references
"""

import re
from pathlib import Path

def remove_section_refs(text):
    """Remove all Section X references"""
    text = re.sub(r'\(Section \d+\)', '', text)
    text = re.sub(r'Section \d+', '', text)
    text = re.sub(r'\s+', ' ', text)  # Clean up extra spaces
    return text.strip()

def parse_markdown_description(markdown_text):
    """Parse markdown and extract content for Sultanic template"""
    
    lines = markdown_text.split('\n')
    content = {
        'title': '',
        'intro': '',
        'features': [],
        'guide_topics': [],
        'race_specific': [],
        'pattern_for': [],
        'pattern_not_for': '',
        'functionally_free': '',
    }
    
    i = 0
    
    # Get title (H1)
    if lines[0].startswith('# '):
        content['title'] = lines[0][2:].strip()
        i = 1
    
    # Get intro (first paragraph after title, skip empty lines)
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].strip():
        content['intro'] = lines[i].strip()
        i += 1
    
    # Parse sections
    current_section = None
    while i < len(lines):
        line = lines[i].strip()
        
        # H2 sections
        if line.startswith('## '):
            section_name = line[3:].strip()
            if 'What You Get' in section_name:
                current_section = 'what_you_get'
            elif 'This Plan Includes' in section_name:
                current_section = 'features'
            elif 'Training Guide' in section_name or 'Guide Covers' in section_name:
                current_section = 'guide_topics'
            elif 'Alternative' in section_name:
                current_section = 'alternative'
            elif 'What This Isn' in section_name:
                current_section = 'what_isnt'
            else:
                current_section = None
            i += 1
            continue
        
        # Bullet lists
        if line.startswith('- '):
            items = []
            while i < len(lines) and lines[i].strip().startswith('- '):
                item = lines[i].strip()[2:].strip()
                # Remove bold markers but keep text
                item = re.sub(r'\*\*(.+?)\*\*', r'\1', item)
                # Remove section references
                item = remove_section_refs(item)
                if item:
                    items.append(item)
                i += 1
            
            if current_section == 'features':
                content['features'].extend(items)
            elif current_section == 'guide_topics':
                content['guide_topics'].extend(items)
            continue
        
        # Regular paragraphs
        if line:
            cleaned = remove_section_refs(line)
            if current_section == 'alternative' and cleaned:
                content['functionally_free'] = cleaned
            elif current_section == 'what_isnt' and cleaned and not content['pattern_not_for']:
                # Use "What This Isn't" as pattern_not_for
                content['pattern_not_for'] = cleaned[:80] + "..." if len(cleaned) > 80 else cleaned
        
        i += 1
    
    return content

def create_sultanic_html(content, plan_config):
    """Create Sultanic HTML from parsed content"""
    
    # Extract comparison hook from title (first part before —)
    if '—' in content['title']:
        comparison_hook = content['title'].split('—')[0].strip()
    else:
        # Extract key phrase
        comparison_hook = content['title'].replace('Unbound Gravel 200', '').strip()
        if not comparison_hook:
            comparison_hook = "First 200 miles: no plan — or a plan built for you"
    
    # Create pain/problem from intro
    pain_stat = "200 miles. 11,000 feet. 95°F June heat. 40% don't finish."
    if content['intro']:
        solution_state = content['intro'][:120] + "..." if len(content['intro']) > 120 else content['intro']
    else:
        solution_state = "You prepared for distance but not heat. 95°F broke you at mile 100"
    
    # Get features (first 4, remove section refs)
    features = [remove_section_refs(f) for f in content['features'][:4]]
    while len(features) < 4:
        features.append("Structured training that respects your reality")
    
    # Get guide topics (first 4, remove section refs)
    guide_topics = [remove_section_refs(g) for g in content['guide_topics'][:4]]
    while len(guide_topics) < 4:
        guide_topics.append("Complete training guide covering all aspects")
    
    # Race-specific (use features if available, otherwise generic)
    if content['features']:
        race_specific = [remove_section_refs(f) for f in content['features'][:3]]
    else:
        race_specific = ["Race-specific preparation", "Endurance training", "Technical skills"]
    
    # Pattern matching (generic, can be customized per tier)
    pattern_for = [
        "You want structured training, not guesswork",
        "You're ready to commit to the process",
        "You value preparation over hope",
        "You want a plan built for your reality"
    ]
    
    pattern_not_for = content['pattern_not_for'] or "Riders looking for shortcuts or magic bullets"
    if len(pattern_not_for) > 100:
        pattern_not_for = pattern_not_for[:97] + "..."
    
    # Functionally free
    functionally_free = content['functionally_free'] or "You're investing time and money either way. Plan or hope?"
    if len(functionally_free) > 120:
        functionally_free = functionally_free[:117] + "..."
    
    # Story justification (from intro)
    if content['intro']:
        story_justification = content['intro'][:100] + "..." if len(content['intro']) > 100 else content['intro']
    else:
        story_justification = "200 miles doesn't care about your intentions. It cares about your preparation"
    
    # Plan details
    weeks = plan_config.get('weeks', 12)
    workouts = 84 if weeks == 12 else 42
    
    # Build HTML (compressed)
    html = f'''<div style="font-family:'Courier New',monospace;color:#111;max-width:800px;margin:0 auto;line-height:1.5;font-size:16px"><div style="border-bottom:2px solid #000;padding-bottom:10px;margin-bottom:14px"><p style="margin:0;font-size:30px;font-weight:900;text-transform:uppercase;letter-spacing:-1px;line-height:1.1">{comparison_hook}</p></div><div style="background:#f5f5f5;border:1px solid #ccc;border-left:5px solid #000;padding:12px;margin-bottom:14px"><h3 style="font-size:13px;text-transform:uppercase;margin:0 0 8px;color:#555">Pain / Problem</h3><p style="margin:0 0 8px;font-weight:700">{pain_stat}</p><p style="margin:0;font-size:16px">{solution_state}</p></div><div style="margin-bottom:14px"><h3 style="font-size:14px;text-transform:uppercase;border-bottom:1px solid #000;padding-bottom:5px;margin-bottom:8px">What This Plan Builds</h3><ul style="margin:0;padding-left:15px;font-size:14px;line-height:1.4"><li>{features[0]}</li><li>{features[1]}</li><li>{features[2]}</li><li>{features[3]}</li></ul></div><div style="background:#f5f5f5;border:1px solid #ccc;border-left:5px solid #777;padding:12px;margin-bottom:14px"><h3 style="font-size:13px;text-transform:uppercase;margin:0 0 8px;color:#555">Included Guide</h3><p style="margin:0 0 6px;font-size:14px"><strong>35-Page Tactical Manual</strong></p><ul style="margin:0;padding-left:15px;font-size:14px;line-height:1.4"><li>{guide_topics[0]}</li><li>{guide_topics[1]}</li><li>{guide_topics[2]}</li><li>{guide_topics[3]}</li></ul></div><div style="margin-bottom:14px"><h3 style="font-size:14px;text-transform:uppercase;border-bottom:1px solid #000;padding-bottom:5px;margin-bottom:8px">Built For Unbound Gravel 200</h3><p style="margin:0 0 8px;font-size:16px">{story_justification}</p><ul style="margin:0;padding-left:15px;font-size:14px;line-height:1.4"><li>✓ {race_specific[0]}</li><li>✓ {race_specific[1]}</li><li>✓ {race_specific[2]}</li></ul><p style="margin:8px 0 0;font-size:14px">{weeks} weeks. {workouts} workouts. TP sync.</p></div><div style="background:#f5f5f5;border:1px solid #ccc;padding:12px;margin-bottom:14px"><h3 style="font-size:13px;text-transform:uppercase;margin:0 0 8px;color:#555">You Should Buy This If...</h3><ul style="margin:0;padding-left:15px;font-size:14px;line-height:1.4"><li>{pattern_for[0]}</li><li>{pattern_for[1]}</li><li>{pattern_for[2]}</li><li>{pattern_for[3]}</li></ul><p style="margin:8px 0 0;font-size:14px"><strong>Not For:</strong> {pattern_not_for}</p></div><div style="border-top:2px solid #000;padding-top:10px;margin-top:14px"><p style="margin:0 0 8px;font-size:14px">{functionally_free}</p><p style="margin:0;font-size:14px">Browse all 15 Unbound Gravel 200 plans:<br><a href="https://gravelgodcycling.com/unbound-200" style="color:#111;text-decoration:underline">gravelgodcycling.com/unbound-200</a></p><p style="margin:8px 0 0;font-size:13px;color:#777">GRAVEL GOD CYCLING | Become what you are.<br>gravelgodcoaching@gmail.com</p></div></div>'''
    
    # Compress whitespace
    html = re.sub(r'>\s+<', '><', html)
    html = re.sub(r' +', ' ', html)
    
    # If still over 4000, trim content more aggressively
    while len(html) > 4000:
        # Shorten features/guide topics
        for i in range(4):
            if len(features[i]) > 70:
                features[i] = features[i][:67] + "..."
            if len(guide_topics[i]) > 70:
                guide_topics[i] = guide_topics[i][:67] + "..."
        
        # Shorten other fields
        solution_state = solution_state[:90] + "..." if len(solution_state) > 90 else solution_state
        story_justification = story_justification[:70] + "..." if len(story_justification) > 70 else story_justification
        for i in range(3):
            if len(race_specific[i]) > 50:
                race_specific[i] = race_specific[i][:47] + "..."
        pattern_not_for = pattern_not_for[:70] + "..." if len(pattern_not_for) > 70 else pattern_not_for
        functionally_free = functionally_free[:90] + "..." if len(functionally_free) > 90 else functionally_free
        
        # Rebuild with shortened content
        html = f'''<div style="font-family:'Courier New',monospace;color:#111;max-width:800px;margin:0 auto;line-height:1.5;font-size:16px"><div style="border-bottom:2px solid #000;padding-bottom:10px;margin-bottom:14px"><p style="margin:0;font-size:30px;font-weight:900;text-transform:uppercase;letter-spacing:-1px;line-height:1.1">{comparison_hook}</p></div><div style="background:#f5f5f5;border:1px solid #ccc;border-left:5px solid #000;padding:12px;margin-bottom:14px"><h3 style="font-size:13px;text-transform:uppercase;margin:0 0 8px;color:#555">Pain / Problem</h3><p style="margin:0 0 8px;font-weight:700">{pain_stat}</p><p style="margin:0;font-size:16px">{solution_state}</p></div><div style="margin-bottom:14px"><h3 style="font-size:14px;text-transform:uppercase;border-bottom:1px solid #000;padding-bottom:5px;margin-bottom:8px">What This Plan Builds</h3><ul style="margin:0;padding-left:15px;font-size:14px;line-height:1.4"><li>{features[0]}</li><li>{features[1]}</li><li>{features[2]}</li><li>{features[3]}</li></ul></div><div style="background:#f5f5f5;border:1px solid #ccc;border-left:5px solid #777;padding:12px;margin-bottom:14px"><h3 style="font-size:13px;text-transform:uppercase;margin:0 0 8px;color:#555">Included Guide</h3><p style="margin:0 0 6px;font-size:14px"><strong>35-Page Tactical Manual</strong></p><ul style="margin:0;padding-left:15px;font-size:14px;line-height:1.4"><li>{guide_topics[0]}</li><li>{guide_topics[1]}</li><li>{guide_topics[2]}</li><li>{guide_topics[3]}</li></ul></div><div style="margin-bottom:14px"><h3 style="font-size:14px;text-transform:uppercase;border-bottom:1px solid #000;padding-bottom:5px;margin-bottom:8px">Built For Unbound Gravel 200</h3><p style="margin:0 0 8px;font-size:16px">{story_justification}</p><ul style="margin:0;padding-left:15px;font-size:14px;line-height:1.4"><li>✓ {race_specific[0]}</li><li>✓ {race_specific[1]}</li><li>✓ {race_specific[2]}</li></ul><p style="margin:8px 0 0;font-size:14px">{weeks} weeks. {workouts} workouts. TP sync.</p></div><div style="background:#f5f5f5;border:1px solid #ccc;padding:12px;margin-bottom:14px"><h3 style="font-size:13px;text-transform:uppercase;margin:0 0 8px;color:#555">You Should Buy This If...</h3><ul style="margin:0;padding-left:15px;font-size:14px;line-height:1.4"><li>{pattern_for[0]}</li><li>{pattern_for[1]}</li><li>{pattern_for[2]}</li><li>{pattern_for[3]}</li></ul><p style="margin:8px 0 0;font-size:14px"><strong>Not For:</strong> {pattern_not_for}</p></div><div style="border-top:2px solid #000;padding-top:10px;margin-top:14px"><p style="margin:0 0 8px;font-size:14px">{functionally_free}</p><p style="margin:0;font-size:14px">Browse all 15 Unbound Gravel 200 plans:<br><a href="https://gravelgodcycling.com/unbound-200" style="color:#111;text-decoration:underline">gravelgodcycling.com/unbound-200</a></p><p style="margin:8px 0 0;font-size:13px;color:#777">GRAVEL GOD CYCLING | Become what you are.<br>gravelgodcoaching@gmail.com</p></div></div>'''
        html = re.sub(r'>\s+<', '><', html)
        html = re.sub(r' +', ' ', html)
        
        # Safety break to avoid infinite loop
        if len(html) > 4100:
            break
    
    return html

# Plan mapping
plan_mapping = {
    "1. Ayahuasca Beginner (12 weeks)": {"file": "ayahuasca/ayahuasca_beginner.txt", "config": {"weeks": 12}},
    "2. Ayahuasca Intermediate (12 weeks)": {"file": "ayahuasca/ayahuasca_intermediate.txt", "config": {"weeks": 12}},
    "3. Ayahuasca Masters (12 weeks)": {"file": "ayahuasca/ayahuasca_beginner_masters.txt", "config": {"weeks": 12}},
    "4. Ayahuasca Save My Race (6 weeks)": {"file": "ayahuasca/ayahuasca_save_my_race.txt", "config": {"weeks": 6}},
    "5. Finisher Beginner (12 weeks)": {"file": "finisher/finisher_beginner.txt", "config": {"weeks": 12}},
    "6. Finisher Intermediate (12 weeks)": {"file": "finisher/finisher_intermediate.txt", "config": {"weeks": 12}},
    "7. Finisher Advanced (12 weeks)": {"file": "finisher/finisher_advanced.txt", "config": {"weeks": 12}},
    "8. Finisher Masters (12 weeks)": {"file": "finisher/finisher_intermediate_masters.txt", "config": {"weeks": 12}},
    "9. Finisher Save My Race (6 weeks)": {"file": "finisher/finisher_save_my_race.txt", "config": {"weeks": 6}},
    "10. Compete Intermediate (12 weeks)": {"file": "compete/compete_intermediate.txt", "config": {"weeks": 12}},
    "11. Compete Advanced (12 weeks)": {"file": "compete/compete_advanced.txt", "config": {"weeks": 12}},
    "12. Compete Masters (12 weeks)": {"file": "compete/compete_intermediate_masters.txt", "config": {"weeks": 12}},
    "13. Compete Save My Race (6 weeks)": {"file": "compete/compete_save_my_race.txt", "config": {"weeks": 6}},
    "14. Podium Advanced (12 weeks)": {"file": "podium/podium_advanced.txt", "config": {"weeks": 12}},
    "15. Podium Advanced GOAT (12 weeks)": {"file": "podium/podium_elite.txt", "config": {"weeks": 12}},
}

base_path = Path("races/Unbound Gravel 200")
desc_path = Path("marketplace_descriptions/unbound_200")

for plan_name, mapping in plan_mapping.items():
    plan_folder = base_path / plan_name
    dest_file = plan_folder / "marketplace_description.html"
    source_file = desc_path / mapping["file"]
    
    if source_file.exists():
        # Read markdown
        markdown = source_file.read_text()
        
        # Parse content
        content = parse_markdown_description(markdown)
        
        # Create Sultanic HTML
        html = create_sultanic_html(content, mapping["config"])
        
        # Write
        dest_file.write_text(html)
        
        char_count = len(html)
        status = "✓" if char_count <= 4000 else "⚠️"
        print(f"{status} {plan_name}: {char_count} chars")

