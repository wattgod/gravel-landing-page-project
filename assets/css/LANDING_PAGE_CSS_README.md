# Landing Page CSS - Neo Brutalist Styling

## Overview
This CSS file (`landing-page.css`) provides neo brutalist styling for:
- **Course Breakdown** (suffering zones) sections
- **Facts** sections

## Neo Brutalist Design Principles Applied
- **Bold, thick borders** (4px solid black)
- **High contrast** (black/white/yellow)
- **Raw, unpolished aesthetic** (no rounded corners, minimal shadows)
- **Strong typography** (uppercase, bold, letter-spacing)
- **Geometric shapes** (box shadows for depth)
- **Bright accent colors** (yellow highlights)

## How to Include

### Option 1: Elementor Custom CSS
1. In Elementor, go to **Page Settings** → **Custom CSS**
2. Copy the contents of `landing-page.css`
3. Paste into the custom CSS field

### Option 2: Theme Functions.php
Add to your theme's `functions.php`:
```php
function enqueue_landing_page_styles() {
    wp_enqueue_style(
        'landing-page-neo-brutalist',
        get_template_directory_uri() . '/assets/css/landing-page.css',
        array(),
        '1.0.0'
    );
}
add_action('wp_enqueue_scripts', 'enqueue_landing_page_styles');
```

### Option 3: Direct Link in HTML
Add to the `<head>` section:
```html
<link rel="stylesheet" href="/assets/css/landing-page.css">
```

## Classes Used

### Course Breakdown
- `.gg-suffering-zones` - Container for all zone cards
- `.gg-zone-card` - Individual suffering zone card
- `.gg-zone-mile` - Mile marker badge (top-left)
- `.gg-zone-label` - Zone name/title
- `.gg-zone-desc` - Zone description
- `.gg-zone-citation` - Source citation (optional)
- `.gg-course-breakdown-note` - Research note box

### Facts Section
- `.gg-facts-header` - Dynamic facts section title
- `.gg-facts-grid` - Grid container for fact cards
- `.gg-fact-card` - Individual fact card
- `.gg-fact-number` - Number badge (top-left)
- `.gg-fact-text` - Fact content

## Dynamic Facts Header
The generator now creates dynamic facts headers instead of always using "Random Facts". Variations include:
- "{Race} Facts"
- "Things You Should Know"
- "What Makes {Race} Different"
- "The Details That Matter"
- "{Race} Reality Check"

The variation is selected deterministically based on the race slug, so each race gets a consistent but unique header.

## Responsive Design
- Mobile: Single column layout, reduced shadows
- Tablet: 2-column grid where space allows
- Desktop: 3-column grid for optimal use of space

## Browser Support
- Modern browsers (Chrome, Firefox, Safari, Edge)
- CSS Grid support required
- Fallbacks for older browsers not included (intentional - neo brutalist is modern)

