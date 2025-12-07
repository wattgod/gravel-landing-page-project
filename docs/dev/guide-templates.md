# Guide Templates Documentation

## Purpose

The `templates/guide-template.md` file defines the standard structure for all training plan guides. It ensures consistency across all race × tier × level combinations.

## Creating a New Guide

### Step 1: Copy the Template

Copy `templates/guide-template.md` to your target location:

```
docs/guides/<race-slug>/<tier>-<level>.html
```

Example:
```
docs/guides/unbound-gravel-200/compete-advanced.html
```

### Step 2: Replace Placeholders

Replace all `{{PLACEHOLDER}}` values with actual content:

- `{{RACE_NAME}}` → "Unbound Gravel 200"
- `{{RACE_DISTANCE}}` → "200"
- `{{RACE_ELEVATION}}` → "11,000 feet of elevation gain"
- `{{PLAN_TIER}}` → "COMPETE", "FINISHER", "AYAHUASCA", or "PODIUM"
- `{{ATHLETE_LEVEL}}` → "Beginner", "Intermediate", or "Advanced"
- `{{HOURS_PER_WEEK}}` → "12-18"
- `{{PLAN_WEEKS}}` → "12" or "6" (for emergency plans)
- And all other placeholders as documented in the template

### Step 3: Ensure Proper Structure

Make sure your guide follows this structure:

```html
<body>
<main class="gg-guide-page">
  <div class="gg-guide-container">
    <!-- Breadcrumb -->
    <p class="gg-guide-breadcrumb">...</p>
    
    <!-- Title block -->
    <h1>{{RACE_NAME}}</h1>
    <h2>{{PLAN_TIER}} • {{ATHLETE_LEVEL}} Training Plan</h2>
    <p class="gg-plan-meta">{{HOURS_PER_WEEK}} hours/week • {{PLAN_WEEKS}} weeks</p>
    
    <!-- TOC -->
    <nav class="gg-guide-toc">...</nav>
    
    <!-- Sections 1-14 -->
    <h2 id="section-1-training-plan-brief">1: Training Plan Brief</h2>
    <!-- ... -->
  </div>
</main>
</body>
```

### Step 4: Verify Heading Hierarchy

- **h1** - Race name (only one per page)
- **h2** - Plan tier/level subtitle
- **h2** - All 14 main sections
- **h3** - Subsections within sections
- **h4** - Sub-subsections (only where nested under h3)

### Step 5: Use Callout Sections

Wrap special content (rating tables, quick-reference lists) in:

```html
<section class="gg-guide-callout gg-guide-callout--ratings">
  <h3>Title</h3>
  <!-- content -->
</section>
```

## Styling

**All styling is done via `assets/css/guides.css`.**

Do not add inline styles or race-specific CSS. The shared stylesheet provides:

- Layout containers (`.gg-guide-page`, `.gg-guide-container`)
- Typography (headings, paragraphs, lists)
- TOC styling (`.gg-guide-toc`)
- Callout sections (`.gg-guide-callout`)
- Tables and other components

## Section IDs

All sections use normalized IDs for consistent linking:

- `section-1-training-plan-brief`
- `section-2-before-you-start`
- `section-3-training-fundamentals`
- `section-4-your-12-week-arc` (or `your-{{PLAN_WEEKS}}-week-arc`)
- `section-5-training-zones`
- `section-6-workout-execution`
- `section-7-technical-skills`
- `section-8-fueling-hydration`
- `section-9-mental-training`
- `section-10-race-tactics`
- `section-11-race-specific-preparation`
- `section-12-race-week-protocol`
- `section-13-quick-reference`
- `section-14-glossary`

## Golden Master

The file `docs/guides/unbound-gravel-200/compete-advanced.html` serves as the "golden master" reference. All other guides should match its structure and styling patterns.

