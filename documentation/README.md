# Gravel Landing Page Project

This folder contains all training plans, generation scripts, and documentation for the Gravel Landing Page project.

## 📝 Voice and Tone Guidelines

**Essential reading for all content generation:**

- **`VOICE_AND_TONE_GUIDELINES.md`** - Core voice principles (dry, matter-of-fact, no theatrical language)
- **`VOICE_EDGE_CASES.md`** - Extended guidelines for specific content types and situations:
  - Content-type calibration (marketplace descriptions, training guides, workout text, race previews)
  - Tier voice handling (Ayahuasca, Finisher, Compete, Podium)
  - Warmth register (dry/amused, warmer gear, coldest gear)
  - Brand terminology integration (G Spot, tier names)
  - Length targets by content type
  - Quick reference decision tree

**All generation scripts should reference both files when creating content.**

## 🎨 Color Palette Rules

**CRITICAL for brand consistency:**

- **`COLOR_PALETTE_RULES.md`** - Earth-tone neobrutalist color system:
  - Muted earth tones for backgrounds (cream, sand, muted cream)
  - Bright yellow (#F4D03F, #FFFF00) ONLY for text shadows and small accents
  - **NEVER use bright yellow for table rows, card backgrounds, or large blocks**
  - Decision tree for choosing correct colors

**One wrong color value destroys brand consistency. Always verify large backgrounds use muted earth tones.**

## 🚀 JSON Template System (NEW)

**Faster plan generation using structured JSON templates!**

- **`JSON_TEMPLATE_SYSTEM.md`** - Complete guide to the JSON system
- **`nutrition_hydration_guidelines.json`** - Nutrition/fueling guidelines for all plans
- **`altitude_guidelines.json`** - Altitude considerations (placeholder)
- **`technical_guidelines.json`** - Technical/equipment guidelines (placeholder)

Each plan folder now includes:
- **`template.json`** - Structured plan data (weeks, workouts, blocks)
- **`JSON_USAGE.md`** - Quick start guide for Cursor AI

**Benefits:**
- 60-70% faster plan generation
- Consistent structure across all races
- Easy to add new races
- Automatic nutrition/hydration integration

## Folder Structure

Each plan type has its own folder following this structure:

```
[Plan Number]. [Plan Name] ([Duration])/
  ├── README.md (generalized template instructions)
  ├── GENERATE_[PLAN]_[TYPE].py (base generation script)
  ├── ALL_WORKOUTS_DATA_[PLAN]_[TYPE].py (workout definitions)
  └── [Plan Number]. [Race Name] - [Plan Name] ([Duration])/
      ├── README.md (race-specific quick start)
      ├── GENERATE_[PLAN]_[TYPE]_[RACE].py (race-specific generation script)
      ├── COMPETE_[PLAN]_[TYPE]_[RACE]_MODIFICATIONS.md (modifications document)
      └── generated_workouts_[plan]_[type]_[race]/ (ZWO files)
```

## Plans Included

### 5. Finisher Beginner (12 weeks)
- **Location:** `current/plans/5. Finisher Beginner (12 weeks)/`
- **Template:** Complete JSON template (12 weeks, 84 workouts)
- **Status:** ✅ Complete and ready for race-specific generation

### 6. Finisher Intermediate (12 weeks)
- **Location:** `current/plans/6. Finisher Intermediate (12 weeks)/`
- **Template:** Complete JSON template (12 weeks, 84 workouts)
- **Philosophy:** Polarized (80/20)
- **Status:** ✅ Complete and ready for race-specific generation

### 7. Finisher Advanced (12 weeks)
- **Location:** `current/plans/7. Finisher Advanced (12 weeks)/`
- **Template:** Complete JSON template (12 weeks, 84 workouts)
- **Philosophy:** GOAT Method (Gravel Optimized Adaptive Training)
- **Status:** ✅ Complete and ready for race-specific generation

### 8. Finisher Masters (12 weeks)
- **Location:** `current/plans/8. Finisher Masters (12 weeks)/`
- **Template:** Complete JSON template (12 weeks, 84 workouts)
- **Philosophy:** Autoregulated (HRV-Based) + Polarized
- **Status:** ✅ Complete and ready for race-specific generation

### 9. Finisher Save My Race (6 weeks)
- **Location:** `current/plans/9. Finisher Save My Race (6 weeks)/`
- **Template:** Complete JSON template (6 weeks, 21 base workouts + 3 tracks × 21 workouts)
- **Philosophy:** G-Spot/Threshold (Emergency Sharpening)
- **Status:** ✅ Complete and ready for race-specific generation

### 10. Compete Intermediate (12 weeks)
- **Location:** `current/plans/10. Compete Intermediate (12 weeks)/`
- **Template:** Complete JSON template (12 weeks, 84 workouts)
- **Philosophy:** Polarized (80/20)
- **Status:** ✅ Complete and ready for race-specific generation

### 11. Compete Advanced (12 weeks)
- **Location:** `current/plans/11. Compete Advanced (12 weeks)/`
- **Template:** Partial JSON template (Week 1 + Week 2 for all 4 blocks complete, Weeks 3-12 need population)
- **Philosophy:** Block Periodization
- **Status:** ⚠️ Structure complete, needs population (35/168 workouts)

### 12. Compete Masters (12 weeks)
- **Location:** `current/plans/12. Compete Masters (12 weeks)/`
- **Template:** Complete JSON template (12 weeks, 84 workouts)
- **Philosophy:** Autoregulated (HRV-Based) + Polarized
- **Status:** ✅ Complete and ready for race-specific generation

### 14. Podium Advanced (12 weeks)
- **Location:** `current/plans/14. Podium Advanced (12 weeks)/`
- **Template:** Complete JSON template (12 weeks, 84 workouts)
- **Philosophy:** HVLI/LSD-Centric (High Volume, Low Intensity)
- **Status:** ✅ Complete and ready for race-specific generation

### 15. Podium Advanced GOAT (12 weeks)
- **Location:** `current/plans/15. Podium Advanced GOAT (12 weeks)/`
- **Template:** Complete JSON template (12 weeks, 112 workouts including block options)
- **Philosophy:** GOAT (Gravel Optimized Adaptive Training)
- **Status:** ✅ Complete and ready for race-specific generation

### 1. Ayahuasca Beginner (12 weeks)
- **Location:** `current/plans/1. Ayahuasca Beginner (12 weeks)/`
- **Template:** Complete JSON template (12 weeks, 84 workouts)
- **Philosophy:** HIIT-Focused (Survival Mode)
- **Status:** ✅ Complete and ready for race-specific generation

### 2. Ayahuasca Intermediate (12 weeks)
- **Location:** `current/plans/2. Ayahuasca Intermediate (12 weeks)/`
- **Template:** Complete JSON template (12 weeks, 84 workouts)
- **Philosophy:** G-Spot/Threshold (Time-Crunched)
- **Status:** ✅ Complete and ready for race-specific generation

### 3. Ayahuasca Masters (12 weeks)
- **Location:** `current/plans/3. Ayahuasca Masters (12 weeks)/`
- **Template:** Complete JSON template (12 weeks, 84 workouts)
- **Philosophy:** Autoregulated (HRV-Based)
- **Status:** ✅ Complete and ready for race-specific generation

### 4. Ayahuasca Save My Race (6 weeks)
- **Location:** `current/plans/4. Ayahuasca Save My Race (6 weeks)/`
- **Template:** Complete JSON template (6 weeks, 42 workouts)
- **Philosophy:** G-Spot/Threshold (Emergency Sharpening)
- **Status:** ✅ Complete and ready for race-specific generation

### 13. Compete Save My Race (6 weeks)
- **Location:** `current/plans/13. Compete Save My Race (6 weeks)/`
- **Template:** Complete JSON template (6 weeks, 42 base workouts + 3 block options)
- **Races:**
  - Unbound 200

## How to Use with Cursor AI

1. Navigate to the plan type folder (e.g., "13. Compete Save My Race (6 weeks)")
2. Read the README.md for template instructions
3. Provide Cursor with:
   - The template files (generation script + workout data)
   - Race-specific considerations
   - Request for modifications
4. Cursor will generate:
   - Modified generation script
   - Generated ZWO files
   - Modifications document

## Adding New Races

To add a new race-specific version:

1. Copy the template generation script
2. Modify it with race-specific considerations
3. Generate the ZWO files
4. Create a modifications document
5. Place all files in: `[Plan Number]. [Race Name] - [Plan Name] ([Duration])/`

## File Types

- **`.py`** - Python generation scripts
- **`.zwo`** - TrainingPeaks workout files
- **`.md`** - Documentation (README, modifications)
- **`generated_workouts_*/`** - Folders containing ZWO files ready for TrainingPeaks upload

