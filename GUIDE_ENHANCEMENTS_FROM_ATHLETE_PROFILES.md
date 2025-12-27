# Guide Enhancements from Athlete Profiles

## Overview

The athlete profiles repo has excellent guide generation with visual/infographic elements that we should incorporate into race plan guides.

---

## Key Enhancements Found

### 1. Philosophy Diagrams ✅

**What it is:**
- Visual bar chart showing intensity distribution
- Easy vs Hard percentage visualization
- Plan-specific philosophy display

**Code:**
```html
<div class="philosophy-diagram">
    <div class="philosophy-bar bar-easy" style="width: 240px;">EASY 80%</div>
    <div class="philosophy-bar bar-hard" style="width: 60px;">HARD 20%</div>
</div>
```

**CSS:**
```css
.philosophy-diagram {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin: 20px 0;
}

.philosophy-bar {
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    border: 2px solid #000;
}

.bar-easy {
    background: #e0e0e0;
}

.bar-hard {
    background: #000;
    color: #fff;
}
```

**How to use:**
- Show 80/20 split for Polarized plans
- Show 60/40 for Pyramidal plans
- Show 90/10 for HVLI plans

---

### 2. Quick Stats Grid ✅

**What it is:**
- Grid layout with key plan metrics
- Large numbers for visual impact
- Clean stat boxes

**Code:**
```html
<div class="quick-stats">
    <div class="stat-box">
        <span class="stat-value">12</span>
        <span class="stat-label">Weeks</span>
    </div>
    <div class="stat-box">
        <span class="stat-value">8-12</span>
        <span class="stat-label">Hours/Week</span>
    </div>
    <div class="stat-box">
        <span class="stat-value">84</span>
        <span class="stat-label">Workouts</span>
    </div>
</div>
```

**CSS:**
```css
.quick-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 12px;
    margin: 20px 0;
}

.stat-box {
    border: 2px solid var(--gg-border);
    padding: 16px;
    text-align: center;
}

.stat-value {
    font-size: 24px;
    font-weight: 700;
    display: block;
    margin-bottom: 4px;
}

.stat-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--gg-muted);
}
```

**How to use:**
- Plan duration
- Target hours per week
- Total workouts
- FTP test frequency

---

### 3. Phase Cards ✅

**What it is:**
- Border-styled cards for each training phase
- Header with phase name
- Body with phase details

**Code:**
```html
<div class="phase-card">
    <div class="phase-card-header">Phase 1: Base Building</div>
    <div class="phase-card-body">
        <p><strong>Weeks:</strong> 1-4</p>
        <p><strong>Focus:</strong> Aerobic base development</p>
        <ul>
            <li>Build volume gradually</li>
            <li>Focus on Z2 endurance</li>
        </ul>
    </div>
</div>
```

**CSS:**
```css
.phase-card {
    border: 2px solid var(--gg-border);
    margin: 16px 0;
    background: #fff;
}

.phase-card-header {
    background: #000;
    color: #fff;
    padding: 12px 16px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-size: 13px;
}

.phase-card-body {
    padding: 16px;
}
```

**How to use:**
- Base building phase
- Build phase
- Peak phase
- Taper phase
- FTP test weeks

---

### 4. Weekly Structure Tables ✅

**What it is:**
- Day-by-day workout breakdown
- Key session indicators (🔑)
- Priority order

**Code:**
```html
<table>
    <thead>
        <tr>
            <th>Day</th>
            <th>Workout</th>
            <th>Notes</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Monday 🔑</td>
            <td>Intervals</td>
            <td><strong>Key session</strong></td>
        </tr>
        <tr>
            <td>Tuesday</td>
            <td>Easy Ride</td>
            <td>Recovery</td>
        </tr>
    </tbody>
</table>
```

**How to use:**
- Show weekly structure
- Highlight key sessions
- Show priority order when life gets in the way

---

### 5. Neo-Brutalist Styling ✅

**What it is:**
- Bold borders, uppercase text
- Monospace font (Sometype Mono)
- High contrast, clean layout

**Key Elements:**
- `font-family: "Sometype Mono", ui-monospace`
- `text-transform: uppercase`
- `letter-spacing: 0.1em`
- `border: 2px solid #000`
- High contrast colors

**How to use:**
- Apply to all guide sections
- Maintains GG brand consistency
- Professional, clean appearance

---

## Implementation Plan

### Step 1: Update Guide Template
- Add philosophy diagram section
- Add quick stats grid
- Add phase cards
- Update styling to neo-brutalist

### Step 2: Generate Content
- Calculate intensity distribution (80/20, etc.)
- Generate phase breakdowns by duration
- Create weekly structure tables
- Add FTP test schedule visualization

### Step 3: Duration-Specific Content
- **12 weeks**: 3-4 phases
- **16 weeks**: 4-5 phases (extended build)
- **20 weeks**: 5-6 phases (with FTP test schedule)

---

## Example Guide Structure

```
1. Header (Title, Subtitle, Meta)
2. Quick Stats Grid
3. Table of Contents
4. Training Philosophy (with diagram)
5. Phase-by-Phase Guide (phase cards)
6. Weekly Structure (table)
7. FTP Test Schedule (if 20-week)
8. Race-Specific Adaptations
9. Equipment & Logistics
10. Mental Preparation
```

---

*Analysis Date: December 26, 2025*  
*Source: athlete-profiles/athletes/scripts/generate_html_guide.py*

