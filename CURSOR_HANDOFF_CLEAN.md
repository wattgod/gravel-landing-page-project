# CURSOR HANDOFF: Strength ZWO Generation Integration

**Date:** December 11, 2025  
**Status:** Ready for Implementation  
**Priority:** High

---

## 📋 HANDOFF FILES

| File | Purpose | Location |
|------|---------|----------|
| `CURSOR_HANDOFF_STRENGTH.md` | **Instructions** — What to build, how it works | `/strengt3/` |
| `MASTER_TEMPLATES_V2.md` | **Data Source** — All 16 templates, JSON schedule, video URLs | `/strengt3/` |

**Read both files before starting implementation.**

---

## 🎯 TASK

Wire strength training sessions into the existing plan generator. Each week should get 2 strength ZWO files (Monday + Thursday) following the schedule mapping in `MASTER_TEMPLATES_V2.md`.

**Output:** ZWO files that import to TrainingPeaks with clickable URLs and proper formatting.

---

## 🚀 IMPLEMENTATION PROMPT FOR CURSOR

```
Read CURSOR_HANDOFF_STRENGTH.md for instructions. Use MASTER_TEMPLATES_V2.md as the data source. 

Wire strength sessions into the plan generator so each week gets 2 strength ZWO files (Mon + Thu) following the schedule mapping.

Key requirements:
- Use workaround: sportType="bike" + <FreeRide Duration="60" Power="0.0"/>
- Title format: W{week:02d} STR: {pathway_name} ({session})
- Description from templates in MASTER_TEMPLATES_V2.md
- Follow JSON schedule mapping (week → template key)
- Respect placement rules (avoid before VO2max/Threshold)
- Include video URLs from library
- Output format: W01_STR_Rebuild_Frame_A.zwo
```

---

## ✅ FIRST TEST REQUEST

**Before generating full batch, test with:**

```
Generate W01_STR_Rebuild_Frame_A.zwo and show me the output before doing the full batch.
```

**Expected output:**
- File: `W01_STR_Rebuild_Frame_A.zwo`
- Title: `W01 STR: Rebuild Frame (A)`
- Template: `RED_A_PHASE1` from MASTER_TEMPLATES_V2.md
- Description: Full formatted strength session with Unicode symbols (★ • →)
- URLs: Clickable links to exercise videos
- XML: `<FreeRide Duration="60" Power="0.0"/>`

**Validation:**
1. Import to TrainingPeaks
2. Verify description renders correctly
3. Verify URLs are clickable
4. Verify Unicode symbols display properly

---

## 📊 QUICK REFERENCE

### Schedule Mapping (from MASTER_TEMPLATES_V2.md)
- **Weeks 1-2:** RED_A_PHASE1 / RED_B_PHASE1
- **Weeks 3-4:** RED_A_PHASE2 / RED_B_PHASE2
- **Weeks 5-6:** RED_A_PHASE3 / RED_B_PHASE3
- **Weeks 7-9:** YELLOW_A_HYPER / YELLOW_B_HYPER
- **Weeks 10-12:** YELLOW_A_MAX / YELLOW_B_MAX
- **Weeks 13-16:** GREEN_A_POWER / GREEN_B_POWER
- **Weeks 17-18:** GREEN_A_CONV / GREEN_B_CONV
- **Week 19:** GREEN_A_MAINT (Mon only)
- **Week 20:** GREEN_B_MAINT (Mon only)

### Title Format
```
W{week:02d} STR: {pathway_name} ({session})
```

### Pathway Names
- `RED` → "Rebuild Frame"
- `YELLOW` → "Fortify Engine"
- `GREEN` → "Sharpen Sword"
- `GREEN_MAINT` → "Race Ready"

### ZWO Structure
```xml
<?xml version="1.0" encoding="UTF-8"?>
<workout_file>
    <author>Gravel God</author>
    <name>W01 STR: Rebuild Frame (A)</name>
    <description><![CDATA[
[PASTE TEMPLATE FROM MASTER_TEMPLATES_V2.md HERE]
]]></description>
    <sportType>bike</sportType>
    <tags/>
    <workout>
        <FreeRide Duration="60" Power="0.0"/>
    </workout>
</workout_file>
```

---

## 🔧 INTEGRATION POINTS

### Option A: Separate Strength Generator (Recommended)
Create `generate_strength_zwo()` function:
1. Takes week number + day (Mon/Thu)
2. Looks up template key from schedule
3. Looks up description from templates
4. Generates title using pathway mapping
5. Outputs ZWO file

### Option B: Integrated into Plan Generator
Add strength generation to existing plan flow:
1. After cycling workouts generated
2. Add strength sessions on Mon/Thu
3. Respect placement rules

---

## ⚠️ EDGE CASES

### 12-Week Plans (No Red)
- Skip weeks 1-6
- Start at `YELLOW_A_HYPER` (Week 7)

### 24-30 Week Plans
- After week 20, loop:
  - Odd weeks: `GREEN_A_CONV` + `GREEN_B_CONV`
  - Even weeks: `GREEN_A_MAINT` + `GREEN_B_MAINT`

### Athletes Who Pass Assessment
- Week 1 → `YELLOW_A_HYPER` (not RED)
- Compress: W1-3 Hyper, W4-6 Max, W7+ Green

---

## ✅ SUCCESS CRITERIA

- [ ] 40 ZWO files generated (20 weeks × 2 sessions, minus week 19-20 which have 1 each)
- [ ] Titles follow format exactly: `W## STR: [Pathway] ([Session])`
- [ ] Descriptions copy cleanly from templates (no encoding issues)
- [ ] URLs are clickable in TrainingPeaks
- [ ] Unicode symbols (★ • → │ ─) render correctly
- [ ] Files import without errors
- [ ] Placement rules respected (not before VO2max/Threshold)

---

## 📝 FILES TO REFERENCE

1. **CURSOR_HANDOFF_STRENGTH.md** — Detailed instructions, integration points, edge cases
2. **MASTER_TEMPLATES_V2.md** — All 16 templates, JSON schedule, video URLs, zero-equipment alternatives
3. **Existing plan generator code** — For integration pattern
4. **Existing ZWO generation code** — For XML structure (see `zwo_generator.py`)

---

## 🎬 NEXT STEPS AFTER IMPLEMENTATION

1. **Test single file:** Generate `W01_STR_Rebuild_Frame_A.zwo` and verify
2. **Test full batch:** Generate all 40 files
3. **Import test:** Import sample files to TrainingPeaks
4. **Validation:** Check URLs, formatting, Unicode symbols
5. **Integration:** Wire into full plan generation pipeline

---

## 📌 NOTES

- **Video URLs:** All URLs are in `MASTER_TEMPLATES_V2.md` Part 3
- **Zero-equipment:** Alternatives baked into templates
- **Placement rules:** Strength should NOT be scheduled day before key cycling sessions
- **File naming:** Use underscores: `W01_STR_Rebuild_Frame_A.zwo`

---

**That's it. Strength system is out of your hands.**

**One thing you still own:** Setting up `gravelgod.com/demos` (or a YouTube playlist) for the warmup/mobility video references. Low priority but worth having before launch.

