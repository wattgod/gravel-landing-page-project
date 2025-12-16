#!/usr/bin/env python3
"""
Convert markdown descriptions to Sultanic V3 HTML format
"""

import re
from pathlib import Path

def markdown_to_sultanic_html(markdown_text):
    """Convert markdown to HTML with Sultanic V3 styling"""
    
    # Start with Sultanic wrapper
    html_parts = ['<div style="font-family:\'Courier New\',monospace;color:#111;max-width:800px;margin:0 auto;line-height:1.5;font-size:16px">']
    
    lines = markdown_text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # H1 - Main title (convert to Sultanic hook style)
        if line.startswith('# ') and i == 0:
            title = line[2:].strip()
            html_parts.append(f'<div style="border-bottom:2px solid #000;padding-bottom:10px;margin-bottom:14px">')
            html_parts.append(f'<p style="margin:0;font-size:30px;font-weight:900;text-transform:uppercase;letter-spacing:-1px;line-height:1.1">{title}</p>')
            html_parts.append('</div>')
            i += 1
            continue
        
        # H2 - Section headers
        if line.startswith('## '):
            title = line[3:].strip()
            html_parts.append(f'<h2 style="font-size:18px;font-weight:700;text-transform:uppercase;margin:20px 0 10px;border-bottom:1px solid #000;padding-bottom:5px">{title}</h2>')
            i += 1
            continue
        
        # H3 - Subsection headers
        if line.startswith('### '):
            title = line[4:].strip()
            html_parts.append(f'<h3 style="font-size:14px;font-weight:700;text-transform:uppercase;margin:16px 0 8px;color:#555">{title}</h3>')
            i += 1
            continue
        
        # Bullet lists
        if line.startswith('- '):
            list_items = []
            while i < len(lines) and lines[i].strip().startswith('- '):
                item_text = lines[i].strip()[2:].strip()
                # Convert bold within list items
                item_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item_text)
                list_items.append(f'<li style="margin:4px 0;line-height:1.4">{item_text}</li>')
                i += 1
            
            html_parts.append('<ul style="margin:10px 0;padding-left:20px;line-height:1.6">')
            html_parts.extend(list_items)
            html_parts.append('</ul>')
            continue
        
        # Horizontal rule
        if line.startswith('---'):
            html_parts.append('<div style="border-top:2px solid #000;margin:20px 0;padding-top:10px"></div>')
            i += 1
            continue
        
        # Regular paragraphs
        if line:
            # Convert bold
            para_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            html_parts.append(f'<p style="margin:10px 0;line-height:1.6">{para_text}</p>')
        
        i += 1
    
    # Close wrapper
    html_parts.append('</div>')
    
    return '\n'.join(html_parts)

# Plan mapping
plan_mapping = {
    "1. Ayahuasca Beginner (12 weeks)": "ayahuasca/ayahuasca_beginner.txt",
    "2. Ayahuasca Intermediate (12 weeks)": "ayahuasca/ayahuasca_intermediate.txt",
    "3. Ayahuasca Masters (12 weeks)": "ayahuasca/ayahuasca_beginner_masters.txt",
    "4. Ayahuasca Save My Race (6 weeks)": "ayahuasca/ayahuasca_save_my_race.txt",
    "5. Finisher Beginner (12 weeks)": "finisher/finisher_beginner.txt",
    "6. Finisher Intermediate (12 weeks)": "finisher/finisher_intermediate.txt",
    "7. Finisher Advanced (12 weeks)": "finisher/finisher_advanced.txt",
    "8. Finisher Masters (12 weeks)": "finisher/finisher_intermediate_masters.txt",
    "9. Finisher Save My Race (6 weeks)": "finisher/finisher_save_my_race.txt",
    "10. Compete Intermediate (12 weeks)": "compete/compete_intermediate.txt",
    "11. Compete Advanced (12 weeks)": "compete/compete_advanced.txt",
    "12. Compete Masters (12 weeks)": "compete/compete_intermediate_masters.txt",
    "13. Compete Save My Race (6 weeks)": "compete/compete_save_my_race.txt",
    "14. Podium Advanced (12 weeks)": "podium/podium_advanced.txt",
    "15. Podium Advanced GOAT (12 weeks)": "podium/podium_elite.txt",
}

base_path = Path("races/Unbound Gravel 200")
desc_path = Path("marketplace_descriptions/unbound_200")

converted = 0
for plan_name, desc_file in plan_mapping.items():
    plan_folder = base_path / plan_name
    desc_source = desc_path / desc_file
    dest_file = plan_folder / "marketplace_description.html"
    
    if desc_source.exists() and plan_folder.exists():
        # Read markdown description
        markdown_content = desc_source.read_text()
        
        # Convert to HTML
        html_content = markdown_to_sultanic_html(markdown_content)
        
        # Write HTML file
        dest_file.write_text(html_content)
        
        # Check character count
        char_count = len(html_content)
        status = "✓" if char_count <= 4000 else "⚠️"
        print(f"{status} {plan_name}: {char_count} chars")
        converted += 1
    else:
        print(f"✗ Missing: {plan_name} or {desc_file}")

print(f"\n✅ Converted {converted} descriptions to Sultanic HTML format")


