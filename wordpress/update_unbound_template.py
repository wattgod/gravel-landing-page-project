#!/usr/bin/env python3
"""
Update the Unbound 200 template with race-specific content from research brief.
Uses simple string replacement - no escaping needed for JSON (apostrophes are fine in JSON).
"""
import re

TEMPLATE_PATH = 'templates/template-unbound-200.json'

# Read template
with open(TEMPLATE_PATH, 'r') as f:
    content = f.read()

# === SCORE UPDATES ===
# Hero section scores: 85 -> 88, 21/50 -> 22/35
content = content.replace('85<span>/100</span>', '88<span>/100</span>')
content = content.replace('TIER 1 · Iconic · High Consequence', 'TIER 1 · Icon · The Super Bowl of Gravel')
content = content.replace('width: 42%;', 'width: 63%;')  # Course profile bar (22/35)
content = content.replace('21 / 50', '22 / 35')
content = content.replace('width: 64%;', 'width: 100%;')  # Prestige bar (5/5)
content = content.replace('32 / 50', '5 / 5')
content = content.replace('Biased Opinion', 'Prestige')
content = content.replace('85 / 100', '88 / 100')

# Course Profile section: update raw score
content = content.replace('21 / 35', '22 / 35')

# Overall score card
content = content.replace('>85<', '>88<')

# Course metric rows - update bar widths and scores
# Length: 4/5 -> 5/5
content = re.sub(
    r'(Length.*?width: )80(%.*?">)4(/5<)',
    r'\g<1>100\g<2>5\3',
    content
)

# Technicality: 2/5 -> 3/5
content = re.sub(
    r'(Technicality.*?width: )40(%.*?">)2(/5<)',
    r'\g<1>60\g<2>3\3',
    content
)

# Elevation: 2/5 -> 3/5
content = re.sub(
    r'(Elevation.*?width: )40(%.*?">)2(/5<)',
    r'\g<1>60\g<2>3\3',
    content
)

# Climate: 5/5 -> 4/5
content = re.sub(
    r'(Climate.*?width: )100(%.*?">)5(/5<)',
    r'\g<1>80\g<2>4\3',
    content
)

# Logistics: 3/5 -> 2/5
content = re.sub(
    r'(Logistics.*?width: )60(%.*?">)3(/5<)',
    r'\g<1>40\g<2>2\3',
    content
)

# Update JavaScript radar config
content = content.replace('{ label: \\"Length\\",       value: 4 }', '{ label: \\"Length\\",       value: 5 }')
content = content.replace('{ label: \\"Technicality\\",       value: 2 }', '{ label: \\"Technicality\\",       value: 3 }')
content = content.replace('{ label: \\"Elevation\\",       value: 2 }', '{ label: \\"Elevation\\",       value: 3 }')
content = content.replace('{ label: \\"Climate\\",       value: 5 }', '{ label: \\"Climate\\",       value: 4 }')
content = content.replace('{ label: \\"Logistics\\",       value: 3 }', '{ label: \\"Logistics\\",       value: 2 }')

# === PULL QUOTE ===
content = content.replace(
    'The early-season gravel race with the biggest heart and the most unpredictable conditions.',
    'The fastest tire at Unbound is the one with air in it.'
)

# === SUFFERING ZONES ===
content = content.replace('Mile 30', 'Mile 28')
content = content.replace('First Reality Check', 'First Selection')
content = content.replace('Aid station one. Decide if you', 'Rough double track. Front pack of 1,100 drops to <50. Position matters. Decide if you')

content = content.replace('Mile 60', 'Mile 40')
content = content.replace('The Grind Begins', 'Divide Road')
content = content.replace('Aid station two. 40 miles left. Mental game starts here.', 'Minimally maintained, rutted, muddy. Where winning moves happen. Where mechanicals end races.')

content = content.replace('Mile 85', 'Mile 104')
content = content.replace('The Final Push', 'Little Egypt')
content = content.replace('Last 15 miles. You can see the finish but your legs disagree.', 'Rugged terrain, sharp rocks, high-speed danger. Last chance for elite separation.')

# === STAT BOXES ===
content = content.replace('121</div><div class=\\"gg-stat-lbl\\">Year One Riders', '34</div><div class=\\"gg-stat-lbl\\">Year One (2006)')
content = content.replace("2,500+</div><div class=\\\"gg-stat-lbl\\\">Today's Field", '5,000</div><div class=\\"gg-stat-lbl\\">All Distances')
content = content.replace('$100K</div><div class=\\"gg-stat-lbl\\">Prize Purse', '23%</div><div class=\\"gg-stat-lbl\\">2023 DNF Rate')

# === LOGISTICS LINK ===
content = content.replace('https://www.midsouthgravel.com', 'https://unboundgravel.com')

# Write template
with open(TEMPLATE_PATH, 'w') as f:
    f.write(content)

# Verify JSON is valid
import json
try:
    with open(TEMPLATE_PATH, 'r') as f:
        json.load(f)
    print("Template updated successfully - JSON is valid")
    print("Scores: 88/100 overall, 22/35 course profile, 5/5 prestige")
    print("Radar: Length 5, Tech 3, Elev 3, Climate 4, Alt 1, Adv 4, Log 2")
except json.JSONDecodeError as e:
    print(f"ERROR: Invalid JSON - {e}")
