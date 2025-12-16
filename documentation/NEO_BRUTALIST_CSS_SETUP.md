# Neo-Brutalist CSS Setup Guide

## Issue: CSS Not Applying After Import

When importing an Elementor JSON file, the `page_settings.custom_css` may not automatically be applied. Elementor requires manual activation of custom CSS.

## Solution: Manual CSS Activation

After importing the Elementor JSON file:

1. **Go to the page in Elementor editor**
2. **Click the page settings icon** (gear icon in bottom left)
3. **Navigate to "Advanced" tab**
4. **Scroll to "Custom CSS" section**
5. **Copy the CSS from `assets/css/landing-page.css`**
6. **Paste into the Custom CSS field**
7. **Save and update the page**

## Alternative: Verify CSS is in JSON

The CSS should already be in `page_settings.custom_css` in the JSON file. To verify:

```python
import json
with open('output/elementor-belgian-waffle-ride.json', 'r') as f:
    data = json.load(f)
css = data.get('page_settings', {}).get('custom_css', '')
print(f'CSS length: {len(css)} chars')
print(f'Has neo-brutalist styles: {".gg-zone-card" in css}')
```

## Required CSS Classes

The neo-brutalist styling requires these CSS classes:

- `.gg-zone-card` - Suffering zone cards
- `.gg-vitals-table` - Race vitals table
- `.gg-timeline-section` - Timeline section
- `.gg-timeline-event` - Timeline events
- `.gg-timeline-year` - Year boxes
- `.gg-course-breakdown-note` - Course breakdown note

All styles are in `assets/css/landing-page.css` and should be automatically included in the generated JSON file's `page_settings.custom_css`.

