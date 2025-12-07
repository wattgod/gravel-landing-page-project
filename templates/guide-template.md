# Training Guide Template

This template defines the structure for all training plan guides. Replace placeholders with race- and plan-specific values.

## Placeholders

- `{{RACE_NAME}}` - Full race name (e.g., "Unbound Gravel 200")
- `{{RACE_DISTANCE}}` - Distance in miles (e.g., "200")
- `{{RACE_ELEVATION}}` - Elevation gain with units (e.g., "11,000 feet of elevation gain")
- `{{RACE_ELEVATION_FEET}}` - Elevation in feet, number only (e.g., "11000")
- `{{RACE_DURATION}}` - Expected completion time (e.g., "10-15 hours")
- `{{RACE_TERRAIN}}` - Brief terrain description (e.g., "Flint Hills gravel roads")
- `{{RACE_DESCRIPTION}}` - 1-2 sentence race overview
- `{{RACE_CHALLENGES}}` - Comma-separated list of main challenges
- `{{RACE_URL}}` - Official race website URL
- `{{PLAN_TIER}}` - AYAHUASCA, FINISHER, COMPETE, or PODIUM
- `{{ATHLETE_LEVEL}}` - Beginner, Intermediate, or Advanced
- `{{HOURS_PER_WEEK}}` - Time commitment range (e.g., "12-18")
- `{{PLAN_WEEKS}}` - Number of weeks in plan (e.g., "12")
- `{{WEEKLY_STRUCTURE}}` - Weekly session breakdown description
- `{{TIRE_WIDTH}}` - Recommended tire width (e.g., "38-42mm")
- `{{WEATHER_STRATEGY}}` - Weather preparation advice (HTML formatted)
- `{{AID_STATION_STRATEGY}}` - Aid station tactics (HTML formatted)
- `{{ALTITUDE_EFFECTS}}` - Altitude effects or "Minimal" if low elevation
- `{{EQUIPMENT_CHECKLIST}}` - Race-specific gear list (HTML formatted)
- `{{TECHNICAL_SKILLS}}` - Technical skills needed (HTML formatted)
- `{{RACE_TACTICS}}` - Race strategy notes (HTML formatted)

## HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{RACE_NAME}} - {{PLAN_TIER}} {{ATHLETE_LEVEL}} Training Plan</title>
    <link rel="stylesheet" href="/gravel-landing-page-project/assets/css/guides.css">
</head>
<body>
<main class="gg-guide-page">
  <div class="gg-guide-container">
    <p class="gg-guide-breadcrumb">
      ← <a href="/gravel-landing-page-project/{{RACE_SLUG}}/">Back to {{RACE_NAME}} plans</a>
    </p>

    <h1>{{RACE_NAME}}</h1>
    <h2>{{PLAN_TIER}} • {{ATHLETE_LEVEL}} Training Plan</h2>
    <p class="gg-plan-meta">{{HOURS_PER_WEEK}} hours/week • {{PLAN_WEEKS}} weeks</p>

    <nav class="gg-guide-toc">
      <h2>Contents</h2>
      <p class="gg-guide-toc-intro">Navigate your training guide</p>
      <ol>
        <li><a href="#section-1-training-plan-brief">01. Training Plan Brief</a></li>
        <li><a href="#section-2-before-you-start">02. BEFORE YOU START</a></li>
        <li><a href="#section-3-training-fundamentals">03. TRAINING FUNDAMENTALS</a></li>
        <li><a href="#section-4-your-12-week-arc">04. YOUR {{PLAN_WEEKS}}-WEEK ARC</a></li>
        <li><a href="#section-5-training-zones">05. TRAINING ZONES</a></li>
        <li><a href="#section-6-workout-execution">06. WORKOUT EXECUTION</a></li>
        <li><a href="#section-7-technical-skills">07. Technical Skills for {{RACE_NAME}}</a></li>
        <li><a href="#section-8-fueling-hydration">08. FUELING & HYDRATION</a></li>
        <li><a href="#section-9-mental-training">09. MENTAL TRAINING</a></li>
        <li><a href="#section-10-race-tactics">10. Race Tactics for {{RACE_NAME}}</a></li>
        <li><a href="#section-11-race-specific-preparation">11. Race-Specific Preparation for {{RACE_NAME}}</a></li>
        <li><a href="#section-12-race-week-protocol">12. RACE WEEK PROTOCOL</a></li>
        <li><a href="#section-13-quick-reference">13. QUICK REFERENCE</a></li>
        <li><a href="#section-14-glossary">14. GLOSSARY</a></li>
      </ol>
    </nav>

    <h2 id="section-1-training-plan-brief">1: Training Plan Brief</h2>
    
    <p>Welcome to <strong>{{RACE_NAME}}</strong> Training</p>
    
    <p>This plan isn't generic. It's built for <strong>{{RACE_NAME}}</strong>—its <strong>{{RACE_DISTANCE}} miles</strong>, <strong>{{RACE_TERRAIN}}</strong>, <strong>{{RACE_ELEVATION}}</strong>, and what it'll take to be out there for <strong>{{RACE_DURATION}}</strong>.</p>
    
    <h2>{{RACE_DESCRIPTION}}</h2>
    
    <p>By the time you roll to the start, you'll know you're ready.</p>
    
    <h2>What Makes This Plan Different</h2>
    
    <h3>Built for your ability level.</h3>
    
    <p>You're on the <strong>{{ATHLETE_LEVEL}}</strong> version (Beginner / Intermediate / Advanced). The load and intensity match where you are right now.</p>
    
    <h3>Built for your schedule.</h3>
    
    <p>This is the <strong>{{PLAN_TIER}}</strong> tier, designed around <strong>{{HOURS_PER_WEEK}}</strong> hours. The week fits into your life so you can actually complete it.</p>
    
    <h3>Built for this race.</h3>
    
    <p>The sessions, long rides, and progressions target the key demands of <strong>{{RACE_NAME}}</strong>: <strong>{{RACE_CHALLENGES}}</strong>.</p>
    
    <h2>How This Plan Is Structured</h2>
    
    <h3>{{PLAN_WEEKS}} Weeks, 4 Phases</h3>
    
    <ul>
    <li><strong>Weeks 1-3: Base Phase</strong> — Building aerobic foundation and endurance</li>
    <li><strong>Weeks 4-7: Build Phase</strong> — Adding intensity, developing race-specific fitness</li>
    <li><strong>Weeks 8-10: Peak Phase</strong> — Maximum training load and sharpening</li>
    <li><strong>Weeks 11-12: Taper Phase</strong> — Reducing volume while maintaining intensity, arriving fresh</li>
    </ul>
    
    <h3>Weekly Structure</h3>
    
    <p>{{WEEKLY_STRUCTURE}}</p>
    
    <h3>Recovery Weeks</h3>
    
    <p>Every third or fourth week is a recovery week with 30-40% reduced volume. Recovery makes you fast. Don't skip these.</p>
    
    <h2>What You Need to Succeed</h2>
    
    <h3>Non-negotiables:</h3>
    
    <ol>
    <li>A power meter</li>
    <li>A heart rate monitor</li>
    <li>A bike set up correctly for gravel racing</li>
    <li>Commitment to the full {{PLAN_WEEKS}} weeks</li>
    <li>Willingness to follow the plan as written</li>
    <li>TrainingPeaks Premium (so your workouts sync to your device)</li>
    <li>Smart trainer for indoor workouts</li>
    </ol>
    
    <h3>A Note on Compliance vs. Perfection</h3>
    
    <p>You won't execute this plan perfectly. No one does.</p>
    
    <p>Life happens. Work intrudes. Illness strikes. Weather doesn't cooperate. Kids need attention. That's reality.</p>
    
    <h3>Built for your ability level.</h3>
    
    <p>You're on the <strong>{{ATHLETE_LEVEL}}</strong> version (Beginner / Intermediate / Advanced). The load and intensity match where you are right now.</p>
    
    <h3>Built for your schedule.</h3>
    
    <p>This is the <strong>{{PLAN_TIER}}</strong> tier, designed around <strong>{{HOURS_PER_WEEK}}</strong> hours. The week fits into your life so you can actually complete it.</p>
    
    <h3>Built for this race.</h3>
    
    <p>The sessions, long rides, and progressions target the key demands of <strong>{{RACE_NAME}}</strong>: <strong>{{RACE_CHALLENGES}}</strong>.</p>
    
    <h2>How This Plan Is Structured</h2>
    
    <h3>{{PLAN_WEEKS}} Weeks, 4 Phases</h3>
    
    <!-- Phase descriptions will vary by plan -->
    
    <h3>Weekly Structure</h3>
    
    <p>{{WEEKLY_STRUCTURE}}</p>
    
    <!-- Additional sections follow the same pattern with h2 for main sections, h3 for subsections -->
    
    <!-- Section 2: BEFORE YOU START -->
    <h2 id="section-2-before-you-start">2: BEFORE YOU START</h2>
    
    <!-- Section 3: TRAINING FUNDAMENTALS -->
    <h2 id="section-3-training-fundamentals">3: TRAINING FUNDAMENTALS</h2>
    
    <!-- Continue with all 14 sections -->
    
  </div>
</main>
</body>
</html>
```

## Section IDs

All section headings use normalized IDs:
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

## Heading Hierarchy

- `h1` - Race name (page title)
- `h2` - Plan tier/level subtitle
- `h2` - Section headings (1-14)
- `h3` - Subsections within sections
- `h4` - Sub-subsections (only where clearly nested under h3)

## Callout Sections

Wrap rating tables, quick-reference lists, and other special content in:

```html
<section class="gg-guide-callout gg-guide-callout--ratings">
  <h3>Title</h3>
  <!-- content -->
</section>
```

