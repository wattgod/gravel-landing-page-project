# Guide Production Process - Complete Workflow

**Last Updated:** December 5, 2024

## 📋 Overview

This document describes the complete process for generating training guides, from race data to live GitHub Pages URLs.

---

## 🔄 Complete Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    GUIDE PRODUCTION PIPELINE                 │
└─────────────────────────────────────────────────────────────┘

INPUT FILES
    │
    ├─→ Race JSON (e.g., unbound_gravel_200.json)
    │   └─→ Contains: race metadata, characteristics, hooks, guide_variables
    │
    ├─→ Plan JSON Templates (15 files)
    │   └─→ Location: plans/[Plan Name]/plan.json
    │   └─→ Contains: week-by-week structure, workouts, TSS, etc.
    │
    └─→ Guide Template (HTML)
        └─→ Location: generation_modules/guide_template_full.html
        └─→ Contains: {{PLACEHOLDERS}} to be replaced

    ▼

GENERATION SCRIPT
    │
    └─→ python3 generate_race_plans.py [race].json
        │
        ├─→ For each of 15 plans:
        │   │
        │   ├─→ 1. ZWO Generator
        │   │      └─→ Creates 84 .zwo workout files
        │   │      └─→ Output: [race]/[plan]/workouts/*.zwo
        │   │
        │   ├─→ 2. Marketplace Generator
        │   │      └─→ Creates marketplace description HTML
        │   │      └─→ Output: [race]/[plan]/marketplace.html
        │   │
        │   └─→ 3. Guide Generator (subprocess)
        │          ├─→ Loads guide_template_full.html
        │          ├─→ Replaces {{PLACEHOLDERS}} with race data
        │          ├─→ Removes altitude section if elevation < 5000ft
        │          └─→ Output: [race]/guides/[race]_[tier]_[level]_guide.html
        │
        └─→ Result: 15 plan folders, each with:
            • 84 ZWO files
            • 1 marketplace description
            • 1 training guide (in central guides/ folder)

    ▼

DEPLOYMENT TO GITHUB PAGES
    │
    └─→ bash deploy_to_github_pages.sh
        │
        ├─→ Scans races/[Race Name]/guides/*.html
        ├─→ Normalizes race/plan names to URL slugs
        ├─→ Copies to docs/guides/[race-slug]/[tier]-[level].html
        └─→ Generates docs/URL_MAPPING.md

    ▼

COMMIT & PUSH
    │
    └─→ git add docs/ && git commit && git push
        │
        └─→ GitHub Pages auto-deploys (2-3 minutes)

    ▼

LIVE URLS
    │
    └─→ https://wattgod.github.io/gravel-landing-page-project/guides/
        [race-slug]/[tier]-[level].html
```

---

## 📥 INPUT FILES

### 1. Race JSON File
**Location:** `races/[race_name].json`

**Structure:**
```json
{
  "race_metadata": {
    "name": "Unbound Gravel 200",
    "distance_miles": 200,
    "elevation_feet": 11000,
    ...
  },
  "race_characteristics": {
    "climate": "hot",
    "terrain": "flint_hills",
    ...
  },
  "guide_variables": {
    "race_terrain": "Flint Hills gravel roads",
    "race_elevation": "11,000 feet",
    ...
  }
}
```

### 2. Plan JSON Templates
**Location:** `plans/[Plan Name]/plan.json`

**15 Plans:**
1. Ayahuasca Beginner (12 weeks)
2. Ayahuasca Intermediate (12 weeks)
3. Ayahuasca Masters (12 weeks)
4. Ayahuasca Save My Race (6 weeks)
5. Finisher Beginner (12 weeks)
6. Finisher Intermediate (12 weeks)
7. Finisher Advanced (12 weeks)
8. Finisher Masters (12 weeks)
9. Finisher Save My Race (6 weeks)
10. Compete Intermediate (12 weeks)
11. Compete Advanced (12 weeks)
12. Compete Masters (12 weeks)
13. Compete Save My Race (6 weeks)
14. Podium Advanced (12 weeks)
15. Podium Advanced GOAT (12 weeks)

### 3. Guide Template
**Location:** `generation_modules/guide_template_full.html`

**Contains:**
- Full HTML structure (3,910 lines)
- CSS styling (neo-brutalist design)
- JavaScript for checklists/downloads
- {{PLACEHOLDERS}} for race-specific data

---

## ⚙️ GENERATION PROCESS

### Step 1: Run Main Generator

```bash
cd races
python3 generate_race_plans.py unbound_gravel_200.json
```

**What it does:**
1. Loads race JSON
2. Creates folder structure: `races/[Race Name]/[15 plan folders]/`
3. For each plan:
   - Loads plan template JSON
   - Generates ZWO files (84 workouts)
   - Generates marketplace description
   - Generates training guide (calls `guide_generator.py`)

### Step 2: Guide Generator Details

**Called via subprocess:**
```python
python guide_generator.py \
  --race unbound_gravel_200.json \
  --plan [plan]_temp.json \
  --output-dir races/[Race]/guides/
```

**Process:**
1. Loads `guide_template_full.html`
2. Extracts race data from JSON:
   - Elevation gain: `guide_variables.race_elevation` or `metadata.elevation_feet`
   - Distance: `metadata.distance_miles`
   - Terrain: `guide_variables.race_terrain`
   - Duration: Calculated from distance
   - Weather: Built from `race_characteristics.typical_weather`
3. Replaces all `{{PLACEHOLDERS}}`:
   - `{{RACE_NAME}}` → "Unbound Gravel 200"
   - `{{DISTANCE}}` → "200 miles"
   - `{{ELEVATION_GAIN}}` → "11,000 feet of elevation gain"
   - `{{TERRAIN_DESCRIPTION}}` → "Flint Hills gravel roads"
   - `{{DURATION_ESTIMATE}}` → "10-15 hours"
   - ... (50+ more placeholders)
4. Conditionally removes altitude section if elevation < 5000ft
5. Saves to: `[race]/guides/[race]_[tier]_[level]_guide.html`

---

## 📤 OUTPUT STRUCTURE

```
races/
└── Unbound Gravel 200/
    ├── guides/                          ← Central guides folder
    │   ├── unbound_gravel_200_ayahuasca_beginner_guide.html
    │   ├── unbound_gravel_200_compete_advanced_guide.html
    │   └── ... (15 total guides)
    │
    ├── 1. Ayahuasca Beginner (12 weeks)/
    │   ├── workouts/
    │   │   ├── Week_01_Day_01.zwo
    │   │   ├── Week_01_Day_02.zwo
    │   │   └── ... (84 total)
    │   └── marketplace_description.html
    │
    ├── 2. Ayahuasca Intermediate (12 weeks)/
    │   └── ... (same structure)
    │
    └── ... (15 plan folders total)
```

---

## 🌐 DEPLOYMENT PROCESS

### Step 1: Deploy to GitHub Pages

```bash
bash deploy_to_github_pages.sh
```

**What it does:**
1. Scans `races/[Race Name]/guides/*.html`
2. Normalizes names to URL slugs:
   - "Unbound Gravel 200" → `unbound-gravel-200`
   - "COMPETE Advanced" → `compete-advanced`
3. Copies to `docs/guides/[race-slug]/[tier]-[level].html`
4. Generates `docs/URL_MAPPING.md` with all URLs

### Step 2: Commit and Push

```bash
git add docs/
git commit -m "Deploy guides to GitHub Pages"
git push
```

### Step 3: Auto-Deployment

- GitHub Pages automatically builds from `/docs` folder
- Takes 2-3 minutes
- Site goes live at: `https://wattgod.github.io/gravel-landing-page-project/guides/`

---

## 🔍 KEY FILES & LOCATIONS

### Generation Scripts
- **Main:** `races/generate_race_plans.py`
- **ZWO:** `races/generation_modules/zwo_generator.py`
- **Marketplace:** `races/generation_modules/marketplace_generator.py`
- **Guide:** `races/generation_modules/guide_generator.py`

### Templates
- **Guide Template:** `races/generation_modules/guide_template_full.html` (3,910 lines)
- **Plan Templates:** `plans/[Plan Name]/plan.json` (15 files)

### Deployment
- **Deploy Script:** `deploy_to_github_pages.sh`
- **URL Helper:** `docs/GET_GUIDE_URL.sh`
- **URL Mapping:** `docs/URL_MAPPING.md`

### Output Locations
- **Local:** `races/[Race Name]/guides/*.html`
- **GitHub Pages:** `docs/guides/[race-slug]/[tier]-[level].html`
- **Live URLs:** `https://wattgod.github.io/gravel-landing-page-project/guides/...`

---

## 📊 EXAMPLE: Unbound Gravel 200

### Input
- `races/unbound_gravel_200.json`
- 15 plan templates from `plans/`
- `generation_modules/guide_template_full.html`

### Processing
```bash
python3 generate_race_plans.py unbound_gravel_200.json
```

### Output (per plan)
- 84 ZWO files → `races/Unbound Gravel 200/[Plan]/workouts/`
- 1 marketplace → `races/Unbound Gravel 200/[Plan]/marketplace.html`
- 1 guide → `races/Unbound Gravel 200/guides/unbound_gravel_200_[tier]_[level]_guide.html`

### Deployment
```bash
bash deploy_to_github_pages.sh
git add docs/ && git commit -m "Deploy" && git push
```

### Live URLs
- `https://wattgod.github.io/gravel-landing-page-project/guides/unbound-gravel-200/compete-advanced.html`
- `https://wattgod.github.io/gravel-landing-page-project/guides/unbound-gravel-200/finisher-intermediate.html`
- ... (15 total URLs)

---

## ⏱️ TIME ESTIMATES

- **Generate 1 race (15 plans):** ~5-10 minutes
- **Deploy to GitHub Pages:** ~30 seconds
- **GitHub Pages build:** 2-3 minutes
- **Total per race:** ~8-14 minutes

---

## 🔧 TROUBLESHOOTING

### Placeholders Not Replaced?
- Check: `guide_generator.py` substitution logic
- Verify: Race JSON has correct field names
- Test: Generate one guide and check for "XXX"

### Guides Not Deploying?
- Check: `docs/guides/` folder exists
- Verify: Files copied correctly
- Confirm: GitHub Pages enabled (Settings → Pages)

### URLs Not Working?
- Wait: 2-3 minutes after push
- Check: GitHub Pages deployment status
- Verify: File exists at `docs/guides/[race-slug]/[tier]-[level].html`

---

## 📝 QUICK REFERENCE

### Generate Guides
```bash
cd races
python3 generate_race_plans.py [race].json
```

### Deploy to GitHub Pages
```bash
bash deploy_to_github_pages.sh
git add docs/ && git commit -m "Deploy guides" && git push
```

### Get Guide URL
```bash
bash docs/GET_GUIDE_URL.sh "Race Name" "tier" "level"
```

### View All URLs
```bash
cat docs/URL_MAPPING.md
```

---

**This is your complete guide production process!**

