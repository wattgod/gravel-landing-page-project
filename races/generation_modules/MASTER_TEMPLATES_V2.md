# GRAVEL GOD STRENGTH — MASTER TEMPLATES V2
## 16 Final Descriptions + Zero-Equipment + Video URLs (Tiered)
## Production-Ready: December 11, 2025

---

# PART 1: TEMPLATE KEY REFERENCE

| Key | Weeks | Pathway | Session | Phase |
|-----|-------|---------|---------|-------|
| `RED_A_PHASE1` | 1-2 | Red | A | Bodyweight |
| `RED_A_PHASE2` | 3-4 | Red | A | Light Load |
| `RED_A_PHASE3` | 5-6 | Red | A | Progression |
| `RED_B_PHASE1` | 1-2 | Red | B | Bodyweight |
| `RED_B_PHASE2` | 3-4 | Red | B | Light Load |
| `RED_B_PHASE3` | 5-6 | Red | B | Progression |
| `YELLOW_A_HYPER` | 7-9 | Yellow | A | Hypertrophy |
| `YELLOW_A_MAX` | 10-12 | Yellow | A | Max Strength |
| `YELLOW_B_HYPER` | 7-9 | Yellow | B | Hypertrophy |
| `YELLOW_B_MAX` | 10-12 | Yellow | B | Max Strength |
| `GREEN_A_POWER` | 13-16 | Green | A | Power |
| `GREEN_A_CONV` | 17-18 | Green | A | Conversion |
| `GREEN_A_MAINT` | 19-20 | Green | A | Maintenance |
| `GREEN_B_POWER` | 13-16 | Green | B | Power |
| `GREEN_B_CONV` | 17-18 | Green | B | Conversion |
| `GREEN_B_MAINT` | 19-20 | Green | B | Maintenance |

---

# PART 2: JSON STRUCTURE FOR PLAN GENERATOR

```json
{
  "strength_config": {
    "sessions_per_week": 2,
    "session_days": ["Monday", "Thursday"],
    "placement_rules": {
      "avoid_before": ["VO2max", "Race Sim", "Threshold"],
      "minimum_hours_before_intensity": 48
    }
  },
  
  "strength_schedule": [
    {"week": 1, "sessions": [{"day": "Mon", "key": "RED_A_PHASE1"}, {"day": "Thu", "key": "RED_B_PHASE1"}]},
    {"week": 2, "sessions": [{"day": "Mon", "key": "RED_A_PHASE1"}, {"day": "Thu", "key": "RED_B_PHASE1"}]},
    {"week": 3, "sessions": [{"day": "Mon", "key": "RED_A_PHASE2"}, {"day": "Thu", "key": "RED_B_PHASE2"}]},
    {"week": 4, "sessions": [{"day": "Mon", "key": "RED_A_PHASE2"}, {"day": "Thu", "key": "RED_B_PHASE2"}]},
    {"week": 5, "sessions": [{"day": "Mon", "key": "RED_A_PHASE3"}, {"day": "Thu", "key": "RED_B_PHASE3"}]},
    {"week": 6, "sessions": [{"day": "Mon", "key": "RED_A_PHASE3"}, {"day": "Thu", "key": "RED_B_PHASE3"}]},
    {"week": 7, "sessions": [{"day": "Mon", "key": "YELLOW_A_HYPER"}, {"day": "Thu", "key": "YELLOW_B_HYPER"}]},
    {"week": 8, "sessions": [{"day": "Mon", "key": "YELLOW_A_HYPER"}, {"day": "Thu", "key": "YELLOW_B_HYPER"}]},
    {"week": 9, "sessions": [{"day": "Mon", "key": "YELLOW_A_HYPER"}, {"day": "Thu", "key": "YELLOW_B_HYPER"}]},
    {"week": 10, "sessions": [{"day": "Mon", "key": "YELLOW_A_MAX"}, {"day": "Thu", "key": "YELLOW_B_MAX"}]},
    {"week": 11, "sessions": [{"day": "Mon", "key": "YELLOW_A_MAX"}, {"day": "Thu", "key": "YELLOW_B_MAX"}]},
    {"week": 12, "sessions": [{"day": "Mon", "key": "YELLOW_A_MAX"}, {"day": "Thu", "key": "YELLOW_B_MAX"}]},
    {"week": 13, "sessions": [{"day": "Mon", "key": "GREEN_A_POWER"}, {"day": "Thu", "key": "GREEN_B_POWER"}]},
    {"week": 14, "sessions": [{"day": "Mon", "key": "GREEN_A_POWER"}, {"day": "Thu", "key": "GREEN_B_POWER"}]},
    {"week": 15, "sessions": [{"day": "Mon", "key": "GREEN_A_POWER"}, {"day": "Thu", "key": "GREEN_B_POWER"}]},
    {"week": 16, "sessions": [{"day": "Mon", "key": "GREEN_A_POWER"}, {"day": "Thu", "key": "GREEN_B_POWER"}]},
    {"week": 17, "sessions": [{"day": "Mon", "key": "GREEN_A_CONV"}, {"day": "Thu", "key": "GREEN_B_CONV"}]},
    {"week": 18, "sessions": [{"day": "Mon", "key": "GREEN_A_CONV"}, {"day": "Thu", "key": "GREEN_B_CONV"}]},
    {"week": 19, "sessions": [{"day": "Mon", "key": "GREEN_A_MAINT"}]},
    {"week": 20, "sessions": [{"day": "Mon", "key": "GREEN_B_MAINT"}]}
  ],

  "title_format": "W{week:02d} STR: {pathway_name} ({session})",
  
  "pathway_names": {
    "RED": "Rebuild Frame",
    "YELLOW": "Fortify Engine", 
    "GREEN": "Sharpen Sword",
    "GREEN_MAINT": "Race Ready"
  },

  "workout_xml": "<FreeRide Duration=\"60\" Power=\"0.0\"/>"
}
```

---

# PART 3: VIDEO URL LIBRARY (JSON for Generator)

```json
{
  "exercise_videos": {
    "Split Squat (bodyweight)": "https://www.youtube.com/watch?v=aclHkVaku9U",
    "Goblet Split Squat": "https://www.youtube.com/watch?v=De0O70I0dH0",
    "Goblet Squat": "https://www.youtube.com/watch?v=MeIiIdhvXT4",
    "Bulgarian Split Squat": "https://www.youtube.com/watch?v=2C-uNgKwPLE",
    "Front Squat": "https://www.youtube.com/watch?v=tlfahNdNPPI",
    "Jump Squat": "https://www.youtube.com/watch?v=1u7S018Nt1M",
    "Split Squat Jump": "https://www.youtube.com/watch?v=VQ5IrLpPG-Y",
    "Single-Leg Squat to Box": "https://www.youtube.com/watch?v=nu8kI1u_0q8",
    "Hip Hinge w/ Dowel": "https://www.youtube.com/watch?v=R2Z4W8q9Zek",
    "KB/DB RDL": "https://www.youtube.com/watch?v=0u5RZ8i5p4o",
    "Single-Leg RDL": "https://www.youtube.com/watch?v=Zfr6wizR8rs",
    "Trap Bar Deadlift": "https://www.youtube.com/watch?v=_T7S5pEXVYI",
    "KB/DB Deadlift": "https://www.youtube.com/watch?v=UGv0YjxPNBg",
    "Good Morning": "https://www.youtube.com/watch?v=1i5KDf3k8Yg",
    "Single-Leg DL to Hop": "https://www.youtube.com/watch?v=sP5pKUZgMoo",
    "Glute Bridge": "https://www.youtube.com/watch?v=m2Gghe-wq0Y",
    "Single-Leg Glute Bridge": "https://www.youtube.com/watch?v=xaZPp8vlDXY",
    "Incline Push-Up": "https://www.youtube.com/watch?v=bm4WZyH5p2I",
    "Push-Up": "https://www.youtube.com/watch?v=_l3ySVKYVJ8",
    "Push-Up + Shoulder Tap": "https://www.youtube.com/watch?v=3UWi44yN-wM",
    "Plyo Push-Up": "https://www.youtube.com/watch?v=Qin7o84f0RQ",
    "DB Bench Press": "https://www.youtube.com/watch?v=vthMCtgVtFw",
    "DB Floor Press": "https://www.youtube.com/watch?v=mKxS2JpUd_g",
    "Incline DB Press": "https://www.youtube.com/watch?v=8iPEnn-ltC8",
    "Med Ball Chest Pass": "https://www.youtube.com/watch?v=sfGJz7dDq4M",
    "Inverted Row": "https://www.youtube.com/watch?v=GdyhjXlxE-U",
    "Band Row": "https://www.youtube.com/watch?v=7aK6Wf2Z_4A",
    "Bent-Over DB Row": "https://www.youtube.com/watch?v=pYcpY20QaE8",
    "Single-Arm DB Row": "https://www.youtube.com/watch?v=pYcpY20QaE8&t=33",
    "TRX Row": "https://www.youtube.com/watch?v=GydJz8wjVRA",
    "Pull-Up": "https://www.youtube.com/watch?v=eGo4IYlbE5g",
    "Band Pull-Apart": "https://www.youtube.com/watch?v=-8fKkXCoKxY",
    "KB Swing": "https://www.youtube.com/watch?v=sSESeQAir2M",
    "Dead Bug": "https://www.youtube.com/watch?v=ZSYRZKYOf28",
    "Weighted Dead Bug": "https://www.youtube.com/watch?v=xmQ9zF3DoW8",
    "Hollow Body Hold": "https://www.youtube.com/watch?v=YaXPRqUwItQ",
    "Hollow Body Rock": "https://www.youtube.com/watch?v=mqnf9n0SPU0",
    "Plank": "https://www.youtube.com/watch?v=pSHjTRCQxIw",
    "Ab Wheel Rollout": "https://www.youtube.com/watch?v=rGevQLZ5aOw",
    "Bird Dog": "https://www.youtube.com/watch?v=wiFNA3sqjCA",
    "Side Plank": "https://www.youtube.com/watch?v=K2VljzCC16g",
    "Side Plank w/ Hip Dip": "https://www.youtube.com/watch?v=mtjKFpQi7GE",
    "Pallof Press": "https://www.youtube.com/watch?v=Te5VAYXy0wQ",
    "Band Chop": "https://www.youtube.com/watch?v=4BOTvaRaDjI",
    "Med Ball Rotational Throw": "https://www.youtube.com/watch?v=YRiUvhz2lag",
    "Russian Twist": "https://www.youtube.com/watch?v=wkD8rjkodUI",
    "Farmer Carry": "https://www.youtube.com/watch?v=YlIuF7JbP0s",
    "Suitcase Carry": "https://www.youtube.com/watch?v=PbO81QHSyKk",
    "Suitcase Deadlift": "https://www.youtube.com/watch?v=PdEy1pNcbdA",
    "Box Jump": "https://www.youtube.com/watch?v=hxldG9FX4j4",
    "Broad Jump": "https://www.youtube.com/watch?v=7s8iH3mJzhk",
    "Med Ball Slam": "https://www.youtube.com/watch?v=3r70rXMHt4k"
  }
}
```

---

# PART 4: ALL 16 DESCRIPTION TEMPLATES
## Main lifts = inline URLs | Warmup/Mobility = library reference

---

## RED_A_PHASE1
```
★ STRENGTH: Red Pathway │ Session A │ Weeks 1-2
  Phase: Anatomical Adaptation │ RPE Target: 5-6
  Equipment: Bodyweight, bands, light DB/KB optional
  Duration: ~40 min

★ WARMUP (10 min) → All demos: gravelgod.com/demos
  • Downward Dog Lunge + Rotation ─ 5/side
  • Tripod Bridge ─ 5/side
  • Curtsy Lunges (assisted OK) ─ 10/side
  • Lateral Lunges ─ 10/side

★ PREP (5 min) │ 2 rounds │ 60s rest
  • Hip Rails ─ 10/side
  • MiniBand Marches ─ 10/side
  • Glute Activation (Clamshells) ─ 15/side

★ MAIN 1: Squat Pattern │ 3 sets │ 90s rest │ RPE 5-6
  A1 Split Squat (bodyweight) ─ 10/side
     → https://www.youtube.com/watch?v=aclHkVaku9U
  A2 Incline Push-Up (hands elevated) ─ 10 reps
     → https://www.youtube.com/watch?v=bm4WZyH5p2I

★ MAIN 2: Core + Carry │ 3 sets │ 90s rest │ RPE 5-6
  B1 Dead Bug ─ 10/side (slow, controlled)
     → https://www.youtube.com/watch?v=ZSYRZKYOf28
  B2 Farmer Carry (light-moderate) ─ 30m
     → https://www.youtube.com/watch?v=YlIuF7JbP0s

★ COOLDOWN (5 min) → All demos: gravelgod.com/demos
  • Deep Squat Sit ─ 45 sec
  • Hip Flexor Stretch ─ 45 sec/side
  • Cat-Cow ─ 10 reps

★ ZERO EQUIPMENT (Hotel/Travel)
  • Split Squat → Same (wall for balance)
  • Incline Push-Up → Hands on bed/chair
  • Dead Bug → Same
  • Farmer Carry → High-Knee March 30 sec

★ NOTES
  This is "Rebuild the Frame" ─ master the movement first.
  Quality > load. Every rep clean.
  If form breaks → reduce reps or rest longer.
```

---

## RED_A_PHASE2
```
★ STRENGTH: Red Pathway │ Session A │ Weeks 3-4
  Phase: Anatomical Adaptation │ RPE Target: 5-6
  Equipment: Light DB/KB, bands
  Duration: ~40 min

★ WARMUP (10 min) → All demos: gravelgod.com/demos
  • Downward Dog Lunge + Rotation ─ 5/side
  • Tripod Bridge ─ 5/side
  • Curtsy Lunges ─ 10/side
  • Lateral Lunges ─ 10/side

★ PREP (5 min) │ 2 rounds │ 60s rest
  • Hip Rails ─ 10/side
  • MiniBand Marches ─ 10/side
  • Glute Activation (Clamshells) ─ 15/side

★ MAIN 1: Squat Pattern │ 3 sets │ 90s rest │ RPE 5-6
  A1 Goblet Split Squat (light DB/KB) ─ 10/side
     → https://www.youtube.com/watch?v=De0O70I0dH0
  A2 Push-Up (floor) ─ 10 reps
     → https://www.youtube.com/watch?v=_l3ySVKYVJ8

★ MAIN 2: Core + Carry │ 3 sets │ 90s rest │ RPE 5-6
  B1 Dead Bug ─ 12/side
     → https://www.youtube.com/watch?v=ZSYRZKYOf28
  B2 Farmer Carry (heavier than W1-2) ─ 30m
     → https://www.youtube.com/watch?v=YlIuF7JbP0s

★ COOLDOWN (5 min) → All demos: gravelgod.com/demos
  • Deep Squat Sit ─ 45 sec
  • Hip Flexor Stretch ─ 45 sec/side
  • Cat-Cow ─ 10 reps

★ ZERO EQUIPMENT (Hotel/Travel)
  • Goblet Split Squat → BW Split Squat
  • Push-Up → Same or Knee Push-Up
  • Dead Bug → Same
  • Farmer Carry → High-Knee March 30 sec

★ NOTES
  Light load introduced. Same movement quality standard.
  The weight should feel like "assistance" not "challenge."
```

---

## RED_A_PHASE3
```
★ STRENGTH: Red Pathway │ Session A │ Weeks 5-6
  Phase: Anatomical Adaptation │ RPE Target: 6
  Equipment: DB/KB (moderate), bands
  Duration: ~40 min

★ WARMUP (10 min) → All demos: gravelgod.com/demos
  • Downward Dog Lunge + Rotation ─ 5/side
  • Tripod Bridge ─ 5/side
  • Curtsy Lunges ─ 10/side
  • Lateral Lunges ─ 10/side

★ PREP (5 min) │ 2 rounds │ 60s rest
  • Hip Rails ─ 10/side
  • MiniBand Marches ─ 10/side
  • Monster Walk ─ 10/direction

★ MAIN 1: Squat Pattern │ 3 sets │ 90s rest │ RPE 6
  A1 Goblet Squat OR Bulgarian Split Squat ─ 10 reps or 10/side
     → Goblet: https://www.youtube.com/watch?v=MeIiIdhvXT4
     → BSS: https://www.youtube.com/watch?v=2C-uNgKwPLE
  A2 Push-Up + Shoulder Tap ─ 8/side
     → https://www.youtube.com/watch?v=3UWi44yN-wM

★ MAIN 2: Core + Carry │ 3 sets │ 90s rest │ RPE 6
  B1 Dead Bug (add light weight) ─ 10/side
     → https://www.youtube.com/watch?v=ZSYRZKYOf28
  B2 Suitcase Carry (single side) ─ 30m/side
     → https://www.youtube.com/watch?v=PbO81QHSyKk

★ COOLDOWN (5 min) → All demos: gravelgod.com/demos
  • Deep Squat Sit ─ 60 sec
  • Hip Flexor Stretch ─ 45 sec/side
  • Pigeon Pose ─ 45 sec/side

★ ZERO EQUIPMENT (Hotel/Travel)
  • Goblet Squat/BSS → Air Squat or BW Split Squat
  • Push-Up + Tap → Same
  • Dead Bug → Same
  • Suitcase Carry → High-Knee March 30 sec/side

★ NOTES
  Final Red phase. Testing readiness for Yellow.
  If goblet squat + push-up feel solid → you're ready.
```

---

## RED_B_PHASE1
```
★ STRENGTH: Red Pathway │ Session B │ Weeks 1-2
  Phase: Anatomical Adaptation │ RPE Target: 5-6
  Equipment: Bodyweight, bands, dowel
  Duration: ~40 min

★ WARMUP (10 min) → All demos: gravelgod.com/demos
  • Cat-Cow ─ 10 reps
  • World's Greatest Stretch ─ 5/side
  • Lying Windshield Wipers ─ 10/side
  • Bird Dog (hold 3 sec) ─ 5/side

★ PREP (5 min) │ 2 rounds │ 60s rest
  • Glute Bridge (double leg) ─ 15 reps
     → https://www.youtube.com/watch?v=m2Gghe-wq0Y
  • Band Pull-Apart ─ 15 reps
     → https://www.youtube.com/watch?v=-8fKkXCoKxY
  • Hip Circles (quadruped) ─ 10/side

★ MAIN 1: Hinge Pattern │ 3 sets │ 90s rest │ RPE 5-6
  A1 Hip Hinge w/ Dowel ─ 12 reps
     → https://www.youtube.com/watch?v=R2Z4W8q9Zek
  A2 Band Row (bent-over) ─ 12 reps
     → https://www.youtube.com/watch?v=7aK6Wf2Z_4A

★ MAIN 2: Glute + Pull │ 3 sets │ 90s rest │ RPE 5-6
  B1 Single-Leg Glute Bridge ─ 10/side
     → https://www.youtube.com/watch?v=xaZPp8vlDXY
  B2 Incline Row (hands on chair/table) ─ 10 reps

★ CORE (8 min) │ 2 rounds │ 60s rest
  C1 Side Plank (knees bent OK) ─ 20 sec/side
     → https://www.youtube.com/watch?v=K2VljzCC16g
  C2 Bird Dog ─ 8/side
     → https://www.youtube.com/watch?v=wiFNA3sqjCA
  C3 Pallof Press (light band) ─ 10/side
     → https://www.youtube.com/watch?v=Te5VAYXy0wQ

★ COOLDOWN (5 min) → All demos: gravelgod.com/demos
  • 90-90 Hip Stretch ─ 45 sec/side
  • Supine Spinal Twist ─ 45 sec/side
  • Child's Pose ─ 60 sec

★ ZERO EQUIPMENT (Hotel/Travel)
  • Hip Hinge → Good Morning (hands behind head)
  • Band Row → Towel Row (door handle)
  • Single-Leg Glute Bridge → Same
  • Side Plank, Bird Dog, Pallof → All BW (Pallof = isometric brace)

★ NOTES
  Learn the hinge. Dowel maintains 3 points of contact.
  Row from whatever angle lets you keep shoulders packed.
```

---

## RED_B_PHASE2
```
★ STRENGTH: Red Pathway │ Session B │ Weeks 3-4
  Phase: Anatomical Adaptation │ RPE Target: 5-6
  Equipment: Light KB/DB, bands, TRX optional
  Duration: ~40 min

★ WARMUP (10 min) → All demos: gravelgod.com/demos
  • Cat-Cow ─ 10 reps
  • World's Greatest Stretch ─ 5/side
  • Lying Windshield Wipers ─ 10/side
  • Bird Dog (hold 3 sec) ─ 5/side

★ PREP (5 min) │ 2 rounds │ 60s rest
  • Glute Bridge (double leg) ─ 15 reps
     → https://www.youtube.com/watch?v=m2Gghe-wq0Y
  • Band Pull-Apart ─ 15 reps
     → https://www.youtube.com/watch?v=-8fKkXCoKxY
  • Hip Circles (quadruped) ─ 10/side

★ MAIN 1: Hinge Pattern │ 3 sets │ 90s rest │ RPE 5-6
  A1 KB/DB RDL (light) ─ 10 reps
     → https://www.youtube.com/watch?v=0u5RZ8i5p4o
  A2 Inverted Row (body at 45°) ─ 10 reps
     → https://www.youtube.com/watch?v=GdyhjXlxE-U

★ MAIN 2: Glute + Pull │ 3 sets │ 90s rest │ RPE 5-6
  B1 Single-Leg Glute Bridge (foot elevated) ─ 10/side
     → https://www.youtube.com/watch?v=xaZPp8vlDXY
  B2 TRX Row or Band Row (steeper angle) ─ 10 reps
     → https://www.youtube.com/watch?v=GydJz8wjVRA

★ CORE (8 min) │ 2 rounds │ 60s rest
  C1 Side Plank (straight legs) ─ 25 sec/side
     → https://www.youtube.com/watch?v=K2VljzCC16g
  C2 Bird Dog ─ 10/side
     → https://www.youtube.com/watch?v=wiFNA3sqjCA
  C3 Pallof Press ─ 12/side
     → https://www.youtube.com/watch?v=Te5VAYXy0wQ

★ COOLDOWN (5 min) → All demos: gravelgod.com/demos
  • 90-90 Hip Stretch ─ 45 sec/side
  • Supine Spinal Twist ─ 45 sec/side
  • Child's Pose ─ 60 sec

★ ZERO EQUIPMENT (Hotel/Travel)
  • KB/DB RDL → Good Morning (BW)
  • Inverted Row → Towel Row or under table
  • Single-Leg Glute Bridge → Same
  • TRX Row → Towel Row

★ NOTES
  Load the hinge. Keep spine neutral throughout.
  Inverted row > band row when possible.
```

---

## RED_B_PHASE3
```
★ STRENGTH: Red Pathway │ Session B │ Weeks 5-6
  Phase: Anatomical Adaptation │ RPE Target: 6
  Equipment: KB/DB (moderate), bands
  Duration: ~40 min

★ WARMUP (10 min) → All demos: gravelgod.com/demos
  • Cat-Cow ─ 10 reps
  • World's Greatest Stretch ─ 5/side
  • Lying Windshield Wipers ─ 10/side
  • Bird Dog (hold 3 sec) ─ 5/side

★ PREP (5 min) │ 2 rounds │ 60s rest
  • Glute Bridge (banded) ─ 15 reps
     → https://www.youtube.com/watch?v=m2Gghe-wq0Y
  • Band Pull-Apart ─ 15 reps
     → https://www.youtube.com/watch?v=-8fKkXCoKxY
  • Good Morning (light) ─ 10 reps
     → https://www.youtube.com/watch?v=1i5KDf3k8Yg

★ MAIN 1: Hinge Pattern │ 3 sets │ 90s rest │ RPE 6
  A1 KB/DB RDL (moderate load) ─ 10 reps
     → https://www.youtube.com/watch?v=0u5RZ8i5p4o
  A2 Single-Arm DB Row ─ 10/side
     → https://www.youtube.com/watch?v=pYcpY20QaE8

★ MAIN 2: Glute + Anti-Rotation │ 3 sets │ 90s rest │ RPE 6
  B1 Single-Leg Glute Bridge (banded) ─ 12/side
     → https://www.youtube.com/watch?v=xaZPp8vlDXY
  B2 Pallof Press (walk-out) ─ 8/side
     → https://www.youtube.com/watch?v=Te5VAYXy0wQ

★ CORE (8 min) │ 2 rounds │ 60s rest
  C1 Side Plank w/ Hip Dip ─ 8/side
     → https://www.youtube.com/watch?v=mtjKFpQi7GE
  C2 Bird Dog (opposite reach) ─ 10/side
     → https://www.youtube.com/watch?v=wiFNA3sqjCA
  C3 Dead Bug ─ 10/side
     → https://www.youtube.com/watch?v=ZSYRZKYOf28

★ COOLDOWN (5 min) → All demos: gravelgod.com/demos
  • 90-90 Hip Stretch ─ 45 sec/side
  • Supine Hamstring Stretch ─ 45 sec/side
  • Thread the Needle ─ 5/side

★ ZERO EQUIPMENT (Hotel/Travel)
  • KB/DB RDL → Good Morning (BW)
  • Single-Arm DB Row → Superman Pull
  • Single-Leg Glute Bridge → Same
  • Pallof Press → Isometric brace

★ NOTES
  Ready for Yellow. RDL form should be locked in.
  If hinge feels solid under moderate load → progress.
```

---

## YELLOW_A_HYPER
```
★ STRENGTH: Yellow Pathway │ Session A │ Weeks 7-9
  Phase: Hypertrophy │ RPE Target: 7-8
  Equipment: KB/DB (moderate-heavy), bands
  Duration: ~45 min

★ WARMUP (8 min) → All demos: gravelgod.com/demos
  • Downward Dog Lunge + Rotation ─ 5/side
  • Goblet Squat Hold (light) ─ 30 sec
  • Lateral Lunges ─ 8/side
  • Arm Circles + Shoulder CARs ─ 10/side

★ PREP (5 min) │ 2 rounds │ 45s rest
  • MiniBand Lateral Walks ─ 10/side
  • Monster Walk ─ 10 steps/direction
  • Push-Up (slow, controlled) ─ 5 reps

★ MAIN 1: Squat Pattern │ 4 sets │ 90s rest │ RPE 7-8
  A1 Goblet Squat ─ 10 reps
     → https://www.youtube.com/watch?v=MeIiIdhvXT4
  A2 Push-Up + Shoulder Tap ─ 8/side
     → https://www.youtube.com/watch?v=3UWi44yN-wM

★ MAIN 2: Single-Leg Strength │ 4 sets │ 90s rest │ RPE 7-8
  B1 Bulgarian Split Squat (or Goblet Squat) ─ 8/side
     → https://www.youtube.com/watch?v=2C-uNgKwPLE
  B2 Floor Press or Incline DB Press ─ 10 reps
     → Floor: https://www.youtube.com/watch?v=mKxS2JpUd_g
     → Incline: https://www.youtube.com/watch?v=8iPEnn-ltC8

★ CORE/CARRY (10 min) │ 3 rounds │ 60s rest
  C1 Dead Bug (weighted) ─ 10/side
     → https://www.youtube.com/watch?v=xmQ9zF3DoW8
  C2 Suitcase Carry ─ 30m/side
     → https://www.youtube.com/watch?v=PbO81QHSyKk
  C3 Hollow Body Hold ─ 20 sec
     → https://www.youtube.com/watch?v=YaXPRqUwItQ

★ COOLDOWN (5 min) → All demos: gravelgod.com/demos
  • Deep Squat Sit ─ 60 sec
  • Hip Flexor Stretch ─ 45 sec/side
  • Pigeon Pose ─ 45 sec/side

★ ZERO EQUIPMENT (Hotel/Travel)
  • Goblet Squat → Air Squat (add jump for challenge)
  • Push-Up + Tap → Same
  • BSS → Reverse Lunge (BW, alternate)
  • Floor/Incline Press → Decline Push-Up (feet elevated)
  • Carries → High-Knee March 40 sec/side

★ NOTES
  Hypertrophy zone: 8-12 reps, last 2 should be hard.
  → BSS hurting your knee? Swap to Goblet Squat, same reps.
  → KB jump too big? Add reps or 2-sec pause before adding weight.
  → Unilateral failing? Go bilateral. Strength > wobble.
```

---

## YELLOW_A_MAX
```
★ STRENGTH: Yellow Pathway │ Session A │ Weeks 10-12
  Phase: Max Strength │ RPE Target: 8-9
  Equipment: KB/DB/Barbell (heavy), rack optional
  Duration: ~50 min

★ WARMUP (8 min) → All demos: gravelgod.com/demos
  • Downward Dog Lunge + Rotation ─ 5/side
  • Goblet Squat (light, 3 sec hold) ─ 5 reps
  • Lateral Lunges ─ 8/side
  • Band Pull-Aparts ─ 15 reps

★ PREP (5 min) │ 2 rounds │ 60s rest
  • MiniBand Lateral Walks ─ 10/side
  • Box Jump (low, stick landing) ─ 5 reps
     → https://www.youtube.com/watch?v=hxldG9FX4j4
  • Push-Up (controlled) ─ 5 reps

★ MAIN 1: Squat Pattern │ 4 sets │ 2-3 min rest │ RPE 8-9
  A1 Goblet Squat (heavy) OR Front Squat ─ 5 reps
     → Goblet: https://www.youtube.com/watch?v=MeIiIdhvXT4
     → Front: https://www.youtube.com/watch?v=tlfahNdNPPI
  A2 DB Bench Press ─ 6 reps
     → https://www.youtube.com/watch?v=vthMCtgVtFw

★ MAIN 2: Single-Leg Strength │ 4 sets │ 2-3 min rest │ RPE 8-9
  B1 Bulgarian Split Squat (heavy) or Goblet Squat ─ 5/side
     → https://www.youtube.com/watch?v=2C-uNgKwPLE
  B2 DB Floor Press (heavy) ─ 6 reps
     → https://www.youtube.com/watch?v=mKxS2JpUd_g

★ CORE/CARRY (8 min) │ 2 rounds │ 90s rest
  C1 Weighted Dead Bug ─ 8/side
     → https://www.youtube.com/watch?v=xmQ9zF3DoW8
  C2 Heavy Farmer Carry ─ 40m
     → https://www.youtube.com/watch?v=YlIuF7JbP0s
  C3 Plank (brace hard) ─ 45 sec
     → https://www.youtube.com/watch?v=pSHjTRCQxIw

★ COOLDOWN (5 min) → All demos: gravelgod.com/demos
  • Deep Squat Sit ─ 60 sec
  • Hip Flexor Stretch ─ 45 sec/side
  • Couch Stretch ─ 60 sec/side

★ ZERO EQUIPMENT (Hotel/Travel)
  • Goblet/Front Squat → Air Squat (add jump for power)
  • DB Bench → Standard Push-Up or Decline Push-Up
  • BSS → Reverse Lunge (BW)
  • DB Floor Press → Push-Up (slow 3-sec eccentric)
  • Farmer Carry → High-Knee March 40 sec

★ NOTES
  Max Strength: heavy loads, full recovery, quality reps only.
  If form breaks → rack it. No grinding.
  → Unilateral failing? Go bilateral. Strength > wobble.
  → KB jump too big? Add reps or pause before adding weight.
  → Week 12: Test day OR deload (cut volume 30%).
```

---

## YELLOW_B_HYPER
```
★ STRENGTH: Yellow Pathway │ Session B │ Weeks 7-9
  Phase: Hypertrophy │ RPE Target: 7-8
  Equipment: KB/DB (moderate-heavy), bands, pull-up bar optional
  Duration: ~45 min

★ WARMUP (8 min) → All demos: gravelgod.com/demos
  • Cat-Cow ─ 10 reps
  • World's Greatest Stretch ─ 5/side
  • Hip Circles (standing) ─ 10/side
  • Band Pull-Aparts ─ 15 reps

★ PREP (5 min) │ 2 rounds │ 45s rest
  • Glute Bridge (banded) ─ 15 reps
  • Dead Hang or Lat Stretch ─ 20 sec
  • Good Morning (bodyweight) ─ 10 reps

★ MAIN 1: Hinge Pattern │ 4 sets │ 90s rest │ RPE 7-8
  A1 Single-Leg RDL (or Conventional RDL) ─ 8/side
     → https://www.youtube.com/watch?v=Zfr6wizR8rs
  A2 Bent-Over DB Row ─ 10 reps
     → https://www.youtube.com/watch?v=pYcpY20QaE8

★ MAIN 2: Pull + Hinge │ 4 sets │ 90s rest │ RPE 7-8
  B1 KB/DB Deadlift ─ 10 reps
     → https://www.youtube.com/watch?v=UGv0YjxPNBg
  B2 Inverted Row or Pull-Up ─ 6-10 reps
     → Inverted: https://www.youtube.com/watch?v=GdyhjXlxE-U
     → Pull-Up: https://www.youtube.com/watch?v=eGo4IYlbE5g
     → Default: Inverted Row. Pull-Up only if you own 5+ strict reps.

★ CORE (10 min) │ 3 rounds │ 60s rest
  C1 Pallof Press (hold 5 sec) ─ 8/side
     → https://www.youtube.com/watch?v=Te5VAYXy0wQ
  C2 Side Plank ─ 30 sec/side
     → https://www.youtube.com/watch?v=K2VljzCC16g
  C3 Band Chop ─ 10/side
     → https://www.youtube.com/watch?v=4BOTvaRaDjI

★ COOLDOWN (5 min) → All demos: gravelgod.com/demos
  • 90-90 Hip Stretch ─ 45 sec/side
  • Supine Hamstring Stretch ─ 45 sec/side
  • Thread the Needle ─ 5/side

★ ZERO EQUIPMENT (Hotel/Travel)
  • Single-Leg RDL → Same (BW, reach to floor)
  • Bent-Over DB Row → Superman Pull (face-down, lift arms/chest)
  • KB/DB Deadlift → Good Morning (BW)
  • Inverted Row/Pull-Up → Towel Row or under table
  • Band Chop → Russian Twist (fast)

★ NOTES
  Hypertrophy zone: 8-12 reps builds muscle that serves the bike.
  → SL RDL wobbling? Switch to Conventional RDL.
  → No pull-up bar? Inverted row IS the exercise.
  → KB jump too big? Add reps or pause before adding weight.
```

---

## YELLOW_B_MAX
```
★ STRENGTH: Yellow Pathway │ Session B │ Weeks 10-12
  Phase: Max Strength │ RPE Target: 8-9
  Equipment: KB/DB/Barbell (heavy), pull-up bar optional
  Duration: ~50 min

★ WARMUP (8 min) → All demos: gravelgod.com/demos
  • Cat-Cow ─ 10 reps
  • World's Greatest Stretch ─ 5/side
  • Hip Circles (standing) ─ 10/side
  • Band Pull-Aparts ─ 15 reps

★ PREP (5 min) │ 2 rounds │ 60s rest
  • Glute Bridge (banded) ─ 15 reps
  • Dead Hang ─ 30 sec
  • KB Swing (light, groove pattern) ─ 10 reps
     → https://www.youtube.com/watch?v=sSESeQAir2M

★ MAIN 1: Hinge Pattern │ 4 sets │ 2-3 min rest │ RPE 8-9
  A1 Trap Bar DL or Heavy KB Deadlift ─ 5 reps
     → Trap Bar: https://www.youtube.com/watch?v=_T7S5pEXVYI
     → KB DL: https://www.youtube.com/watch?v=UGv0YjxPNBg
  A2 Inverted Row (steep) or Weighted Pull-Up ─ 5-6 reps
     → Inverted: https://www.youtube.com/watch?v=GdyhjXlxE-U
     → Pull-Up: https://www.youtube.com/watch?v=eGo4IYlbE5g
     → Default: Steep Inverted Row or Row + 3 sec hold.
     → Weighted Pull-Up only if 8+ BW reps.

★ MAIN 2: Single-Leg + Row │ 4 sets │ 2-3 min rest │ RPE 8-9
  B1 Single-Leg RDL (heavy) or Conventional RDL ─ 5/side
     → https://www.youtube.com/watch?v=Zfr6wizR8rs
  B2 Heavy DB Row (3-point) ─ 6/side
     → https://www.youtube.com/watch?v=pYcpY20QaE8

★ CORE (8 min) │ 2 rounds │ 90s rest
  C1 Pallof Press (heavy band) ─ 8/side
     → https://www.youtube.com/watch?v=Te5VAYXy0wQ
  C2 Side Plank ─ 45 sec/side
     → https://www.youtube.com/watch?v=K2VljzCC16g
  C3 Suitcase Deadlift ─ 6/side
     → https://www.youtube.com/watch?v=PdEy1pNcbdA

★ COOLDOWN (5 min) → All demos: gravelgod.com/demos
  • 90-90 Hip Stretch ─ 45 sec/side
  • Supine Hamstring Stretch ─ 45 sec/side
  • Thread the Needle ─ 5/side

★ ZERO EQUIPMENT (Hotel/Travel)
  • Trap Bar/KB DL → Good Morning (BW)
  • Inverted Row/Pull-Up → Towel Row or under table
  • Single-Leg RDL → Same (BW)
  • DB Row → Superman Pull
  • Suitcase DL → Side Plank (hold)

★ NOTES
  Max Strength: heavy hinge = power on the pedals.
  Full rest between sets. Quality reps only.
  → Unilateral failing? Go bilateral. Strength > wobble.
  → No pull-up bar? Steep inverted row with pause at top.
  → KB jump too big? Add reps or pause before adding weight.
  → Week 12: Test day OR deload (cut volume 30%).
```

---

## GREEN_A_POWER
```
★ STRENGTH: Green Pathway │ Session A │ Weeks 13-16
  Phase: Power │ RPE Target: 7-8 (explosive intent)
  Equipment: KB/DB, med ball optional, box
  Duration: ~40 min

★ WARMUP (8 min) → All demos: gravelgod.com/demos
  • Jump Rope or Jumping Jacks ─ 60 sec
  • Leg Swings (front/back + lateral) ─ 10/direction
  • Goblet Squat (light, fast) ─ 5 reps
  • Arm Circles + Clapping Push-Ups ─ 10 reps

★ POWER PREP (5 min) │ 2 rounds │ 60s rest
  • Box Jump (stick landing) ─ 5 reps
     → https://www.youtube.com/watch?v=hxldG9FX4j4
  • Med Ball Slam or Squat Jump ─ 6 reps
     → Slam: https://www.youtube.com/watch?v=3r70rXMHt4k
     → Squat Jump: https://www.youtube.com/watch?v=1u7S018Nt1M
  • Broad Jump (step back) ─ 5 reps
     → https://www.youtube.com/watch?v=7s8iH3mJzhk

★ MAIN 1: Explosive Squat │ 4 sets │ 2 min rest │ Max Intent
  A1 Jump Squat (bodyweight) ─ 6 reps
     → https://www.youtube.com/watch?v=1u7S018Nt1M
  A2 Plyo Push-Up (hands leave ground) ─ 6 reps
     → https://www.youtube.com/watch?v=Qin7o84f0RQ

★ MAIN 2: Loaded Power │ 4 sets │ 2 min rest │ RPE 7
  B1 Goblet Squat (moderate, FAST up) ─ 6 reps
     → https://www.youtube.com/watch?v=MeIiIdhvXT4
  B2 Med Ball Chest Pass or Explosive Push-Up ─ 8 reps
     → https://www.youtube.com/watch?v=sfGJz7dDq4M

★ CORE (8 min) │ 2 rounds │ 60s rest
  C1 Med Ball Rotational Throw or Russian Twist ─ 6/side
     → Throw: https://www.youtube.com/watch?v=YRiUvhz2lag
     → Twist: https://www.youtube.com/watch?v=wkD8rjkodUI
  C2 Plank + Shoulder Tap (fast) ─ 10/side
  C3 Hollow Body Rock ─ 15 sec
     → https://www.youtube.com/watch?v=mqnf9n0SPU0

★ COOLDOWN (5 min) → All demos: gravelgod.com/demos
  • Deep Squat Sit ─ 60 sec
  • Quad Stretch (standing) ─ 30 sec/side
  • Hip Flexor Stretch ─ 45 sec/side

★ ZERO EQUIPMENT (Hotel/Travel)
  • Jump Squat → Same (BW)
  • Plyo Push-Up → Same (or from knees)
  • Goblet Squat → Air Squat Jump
  • Med Ball Chest Pass → Explosive Push-Up or Shadow Box
  • Med Ball Throw → Russian Twist (fast)

★ NOTES
  Power phase: Intent > load. Move fast, land soft.
  Full rest = full power. Don't rush sets.
  → Can't do plyo push-up? Fast regular push-up works.
  → KB jump too big? Add reps or pause before adding weight.
  → If tired, skip a set. Quality only.
```

---

## GREEN_A_CONV
```
★ STRENGTH: Green Pathway │ Session A │ Weeks 17-18
  Phase: Conversion │ RPE Target: 6-7
  Equipment: Light KB/DB, bands
  Duration: ~35 min

★ WARMUP (8 min) → All demos: gravelgod.com/demos
  • Jump Rope ─ 60 sec
  • Leg Swings ─ 10/direction
  • Air Squat (fast) ─ 10 reps
  • Arm Circles ─ 10/direction

★ POWER PREP (5 min) │ 2 rounds │ 60s rest
  • Squat Jump (low box) ─ 5 reps
     → https://www.youtube.com/watch?v=1u7S018Nt1M
  • Push-Up (explosive, not plyometric) ─ 5 reps

★ MAIN 1: Sport-Specific │ 3 sets │ 2 min rest │ Quality Focus
  A1 Single-Leg Squat to Box (or Goblet Squat) ─ 5/side
     → https://www.youtube.com/watch?v=nu8kI1u_0q8
  A2 Clapping Push-Up or Fast Push-Up ─ 5 reps
     → https://www.youtube.com/watch?v=Qin7o84f0RQ

★ MAIN 2: Reduced Volume │ 3 sets │ 2 min rest │ RPE 6-7
  B1 Split Squat Jump (or Jump Squat) ─ 5/side
     → https://www.youtube.com/watch?v=VQ5IrLpPG-Y
  B2 Med Ball Push or Explosive Push-Up ─ 6 reps
     → https://www.youtube.com/watch?v=sfGJz7dDq4M

★ CORE (5 min) │ 2 rounds │ 45s rest
  C1 Dead Bug (fast) ─ 10/side
     → https://www.youtube.com/watch?v=ZSYRZKYOf28
  C2 Mountain Climbers ─ 20 total

★ COOLDOWN (5 min) → All demos: gravelgod.com/demos
  • Foam Roll Quads ─ 60 sec
  • Hip Flexor Stretch ─ 45 sec/side
  • Pigeon Pose ─ 45 sec/side

★ ZERO EQUIPMENT (Hotel/Travel)
  • Single-Leg Squat to Box → Pistol (chair assist)
  • Clapping Push-Up → Same (or fast standard)
  • Split Squat Jump → Same or Tuck Jump
  • Med Ball Push → Explosive Push-Up

★ NOTES
  Conversion: Volume drops, intensity stays.
  You're transferring strength → pedal power.
  Feel athletic after this, not destroyed.
  → Unilateral failing? Go bilateral. Strength > wobble.
```

---

## GREEN_A_MAINT
```
★ STRENGTH: Green Pathway │ Session A │ Weeks 19-20
  Phase: Maintenance │ RPE Target: 5-6
  Equipment: Bodyweight, light KB/DB optional
  Duration: ~25 min

★ WARMUP (5 min) → All demos: gravelgod.com/demos
  • Light Jog in Place ─ 60 sec
  • Leg Swings ─ 8/direction
  • Air Squat ─ 8 reps
  • Arm Circles ─ 8/direction

★ ACTIVATION (5 min) │ 1 round
  • Box Jump or Squat Jump (light) ─ 3 reps
     → https://www.youtube.com/watch?v=hxldG9FX4j4
  • Push-Up ─ 5 reps
  • Lateral Lunge ─ 5/side

★ MAIN (10 min) │ 2 sets │ 2 min rest │ Stay Sharp
  A1 Goblet Squat (light) ─ 6 reps
     → https://www.youtube.com/watch?v=MeIiIdhvXT4
  A2 Push-Up ─ 8 reps
     → https://www.youtube.com/watch?v=_l3ySVKYVJ8
  A3 Jump Squat ─ 4 reps
     → https://www.youtube.com/watch?v=1u7S018Nt1M

★ CORE (5 min) │ 1-2 rounds
  C1 Plank ─ 30 sec
     → https://www.youtube.com/watch?v=pSHjTRCQxIw
  C2 Dead Bug ─ 8/side
     → https://www.youtube.com/watch?v=ZSYRZKYOf28
  C3 Ab Wheel or Weighted Dead Bug ─ 6 reps
     → Ab Wheel: https://www.youtube.com/watch?v=rGevQLZ5aOw
     → Weighted DB: https://www.youtube.com/watch?v=xmQ9zF3DoW8

★ COOLDOWN (5 min) → All demos: gravelgod.com/demos
  • Stretch what's tight
  • Focus on hip flexors + quads

★ ZERO EQUIPMENT (Hotel/Travel)
  • Goblet Squat → Air Squat
  • Push-Up → Same
  • Jump Squat → Same
  • Ab Wheel → Plank Knee-to-Elbow

★ NOTES
  Minimal effective dose. Don't dig a hole.
  Race week? Consider skipping or 1 set only.
  You're sharp. Stay sharp. Trust the work.
```

---

## GREEN_B_POWER
```
★ STRENGTH: Green Pathway │ Session B │ Weeks 13-16
  Phase: Power │ RPE Target: 7-8 (explosive intent)
  Equipment: KB (required), bands, pull-up bar optional
  Duration: ~40 min

★ WARMUP (8 min) → All demos: gravelgod.com/demos
  • Jump Rope ─ 60 sec
  • Hip Circles (standing) ─ 10/side
  • Hinge + Reach (no weight) ─ 10 reps
  • Band Pull-Aparts ─ 15 reps

★ POWER PREP (5 min) │ 2 rounds │ 60s rest
  • KB Swing (light, focus on snap) ─ 10 reps
     → https://www.youtube.com/watch?v=sSESeQAir2M
  • Broad Jump (step back) ─ 5 reps
     → https://www.youtube.com/watch?v=7s8iH3mJzhk
  • Explosive Row or Jump Pull-Up ─ 3 reps

★ MAIN 1: Ballistic Hinge │ 4 sets │ 2 min rest │ Max Intent
  A1 KB Swing (2-hand) ─ 12 reps
     → https://www.youtube.com/watch?v=sSESeQAir2M
  A2 Explosive Inverted Row or Band Pull ─ 8 reps
     → https://www.youtube.com/watch?v=GdyhjXlxE-U
     → Default: Fast inverted row, chest to bar
     → No bar? Explosive band row

★ MAIN 2: Power Hinge │ 4 sets │ 2 min rest │ RPE 7
  B1 KB Swing to Goblet Catch (or heavy swing) ─ 8 reps
     → https://www.youtube.com/watch?v=sSESeQAir2M
  B2 Explosive Pull-Up or Steep Inverted Row ─ 5-6 reps
     → Pull-Up: https://www.youtube.com/watch?v=eGo4IYlbE5g
     → Inverted: https://www.youtube.com/watch?v=GdyhjXlxE-U
     → Pull-Up only if 5+ strict reps

★ CORE (8 min) │ 2 rounds │ 60s rest
  C1 Med Ball Rotational Throw or Russian Twist ─ 6/side
     → Throw: https://www.youtube.com/watch?v=YRiUvhz2lag
     → Twist: https://www.youtube.com/watch?v=wkD8rjkodUI
  C2 Side Plank w/ Hip Drop ─ 8/side
     → https://www.youtube.com/watch?v=mtjKFpQi7GE
  C3 Pallof Press ─ 8/side
     → https://www.youtube.com/watch?v=Te5VAYXy0wQ

★ COOLDOWN (5 min) → All demos: gravelgod.com/demos
  • 90-90 Hip Stretch ─ 45 sec/side
  • Pigeon Pose ─ 45 sec/side
  • Hamstring Stretch ─ 30 sec/side

★ ZERO EQUIPMENT (Hotel/Travel)
  • KB Swing → Broad Jump or Frog Jump (hip snap)
  • Explosive Inverted Row → Explosive Towel Row or Superman Pull
  • Explosive Pull-Up → Same substitute
  • Med Ball Throw → Russian Twist (fast)

★ NOTES
  KB Swing = cycling power transfer. Snap the hips.
  → No pull-up bar? Inverted row IS the exercise.
  → KB jump too big? Add reps or pause before adding weight.
  → If form breaks → lighter weight or more rest.
```

---

## GREEN_B_CONV
```
★ STRENGTH: Green Pathway │ Session B │ Weeks 17-18
  Phase: Conversion │ RPE Target: 6-7
  Equipment: KB (moderate), bands
  Duration: ~35 min

★ WARMUP (8 min) → All demos: gravelgod.com/demos
  • Jump Rope ─ 60 sec
  • Hip Circles ─ 10/side
  • Good Morning (bodyweight) ─ 10 reps
  • Band Pull-Aparts ─ 15 reps

★ POWER PREP (5 min) │ 2 rounds │ 60s rest
  • KB Swing (light) ─ 10 reps
     → https://www.youtube.com/watch?v=sSESeQAir2M
  • Explosive Row (band) ─ 8 reps

★ MAIN 1: Cycling-Specific │ 3 sets │ 2 min rest │ Quality Focus
  A1 Single-Leg DL to Hop (or Broad Jump) ─ 5/side
     → https://www.youtube.com/watch?v=sP5pKUZgMoo
  A2 Band Pull-Apart (explosive) ─ 12 reps
     → https://www.youtube.com/watch?v=-8fKkXCoKxY

★ MAIN 2: Reduced Volume │ 3 sets │ 2 min rest │ RPE 6-7
  B1 KB Swing (moderate) ─ 10 reps
     → https://www.youtube.com/watch?v=sSESeQAir2M
  B2 Inverted Row or Pull-Up (controlled) ─ 5 reps
     → Inverted: https://www.youtube.com/watch?v=GdyhjXlxE-U
     → Pull-Up: https://www.youtube.com/watch?v=eGo4IYlbE5g

★ CORE (5 min) │ 2 rounds │ 45s rest
  C1 Bird Dog (hold 3 sec) ─ 6/side
     → https://www.youtube.com/watch?v=wiFNA3sqjCA
  C2 Side Plank ─ 30 sec/side
     → https://www.youtube.com/watch?v=K2VljzCC16g

★ COOLDOWN (5 min) → All demos: gravelgod.com/demos
  • 90-90 Hip Stretch ─ 45 sec/side
  • Hamstring Stretch ─ 45 sec/side
  • Cat-Cow ─ 10 reps

★ ZERO EQUIPMENT (Hotel/Travel)
  • Single-Leg DL to Hop → Single-Leg Hop (BW)
  • KB Swing → Broad Jump
  • Band Pull-Apart → Shoulder Blade Squeeze (isometric)
  • Inverted Row/Pull-Up → Towel Row

★ NOTES
  Transfer to the pedals. Volume down, quality up.
  Feel athletic, not fatigued.
  → SL DL to Hop not clicking? Broad jump works.
  → No pull-up bar? Inverted row IS the exercise.
```

---

## GREEN_B_MAINT
```
★ STRENGTH: Green Pathway │ Session B │ Weeks 19-20
  Phase: Maintenance │ RPE Target: 5-6
  Equipment: Light KB, bands
  Duration: ~25 min

★ WARMUP (5 min) → All demos: gravelgod.com/demos
  • Light Jog in Place ─ 60 sec
  • Hip Circles ─ 8/side
  • Hinge Pattern (bodyweight) ─ 8 reps
  • Band Pull-Aparts ─ 10 reps

★ ACTIVATION (5 min) │ 1 round
  • KB Swing (light) ─ 10 reps
     → https://www.youtube.com/watch?v=sSESeQAir2M
  • Band Row (explosive) ─ 10 reps
  • Broad Jump ─ 3 reps
     → https://www.youtube.com/watch?v=7s8iH3mJzhk

★ MAIN (10 min) │ 2 sets │ 2 min rest │ Stay Sharp
  A1 KB Swing ─ 8 reps
     → https://www.youtube.com/watch?v=sSESeQAir2M
  A2 Inverted Row or Pull-Up ─ 5 reps
     → Inverted: https://www.youtube.com/watch?v=GdyhjXlxE-U
     → Pull-Up: https://www.youtube.com/watch?v=eGo4IYlbE5g
  A3 Single-Leg RDL (light) ─ 5/side
     → https://www.youtube.com/watch?v=Zfr6wizR8rs

★ CORE (5 min) │ 1-2 rounds
  C1 Side Plank ─ 20 sec/side
     → https://www.youtube.com/watch?v=K2VljzCC16g
  C2 Bird Dog ─ 6/side
     → https://www.youtube.com/watch?v=wiFNA3sqjCA
  C3 Ab Wheel or Weighted Dead Bug ─ 6 reps
     → Ab Wheel: https://www.youtube.com/watch?v=rGevQLZ5aOw
     → Weighted DB: https://www.youtube.com/watch?v=xmQ9zF3DoW8

★ COOLDOWN (5 min) → All demos: gravelgod.com/demos
  • Stretch what's tight
  • Focus on hips + hamstrings

★ ZERO EQUIPMENT (Hotel/Travel)
  • KB Swing → Broad Jump
  • Inverted Row/Pull-Up → Towel Row
  • Single-Leg RDL → Same (BW)
  • Ab Wheel → Plank Knee-to-Elbow

★ NOTES
  Minimal dose. Maximum freshness.
  Race week? Consider skipping or 1 set only.
  Trust the work you've done.
```

---

# PART 5: USAGE INSTRUCTIONS

## To Generate a Strength ZWO:

1. Look up the week number in the JSON schedule
2. Get the template key (e.g., `YELLOW_A_HYPER`)
3. Copy the description from Part 4
4. Generate title: `W{week:02d} STR: {pathway_name} ({session})`
5. Use XML block: `<FreeRide Duration="60" Power="0.0"/>`

## Example Output:

**Week 8, Session A:**
- Title: `W08 STR: Fortify Engine (A)`
- Description: [copy YELLOW_A_HYPER]
- XML: `<FreeRide Duration="60" Power="0.0"/>`

---

# PART 6: EXTENSION RULES

## For 12-Week Plans (No Red):
Start at Week 7 (Yellow). Skip Red entirely.

## For 24-30 Week Plans:
After Week 20, alternate:
- Odd weeks: GREEN_A_CONV + GREEN_B_CONV
- Even weeks: GREEN_A_MAINT + GREEN_B_MAINT

## For Athletes Starting Yellow (Passed Assessment):
- Map Week 1 → YELLOW_A_HYPER (not RED)
- Compress to: W1-3 Yellow Hyper, W4-6 Yellow Max, W7+ Green

---

# PART 7: RESTART FLOWCHART

```
★ MISSED TRAINING? — WHERE TO JUMP BACK IN

  Missed 3-6 days?
  → Repeat your last completed week. No drama.

  Missed 1-2 weeks?
  → Drop back ONE pathway:
    • Was in Green → restart Yellow W10-12 (Max Strength)
    • Was in Yellow → restart Red W5-6
    • Was in Red → restart Red W3-4

  Missed 3+ weeks or feel like garbage?
  → Redo the 3-question assessment. Start wherever it tells you.

  Progress is never truly lost. You just need 1-2 weeks to wake the patterns back up.
```

---

# PART 8: SELF-ASSESSMENT (3 Questions)

Before starting, answer honestly:

1. Can you hold a deep squat (heels down) for 30 seconds?
2. Can you do 15 single-leg glute bridges per side with hips level?
3. Have you been lifting 2x/week for 6+ months?

**Scoring:**
- Any "No" → Start RED (Week 1)
- All "Yes" → Start YELLOW (Week 7)

No shame in starting Red. It builds the foundation that makes Yellow and Green actually work.
