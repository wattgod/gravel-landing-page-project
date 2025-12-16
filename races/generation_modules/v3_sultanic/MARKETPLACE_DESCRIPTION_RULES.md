# Marketplace Description Rules & Alignment

## Voice & Tone Guidelines

**All marketplace descriptions must follow:**
- `documentation/VOICE_AND_TONE_GUIDELINES.md` - Core voice principles
- `documentation/VOICE_EDGE_CASES.md` - Section 7.1 (Marketplace Descriptions) for content-type calibration, Section 11.1 for length targets (300-450 words total)

**Key principles for marketplace descriptions:**
- Lead with the problem the athlete already knows they have
- State what the plan does—no inflation
- Confidence reads as competence; hype reads as desperation
- One philosophical line max; the rest is practical value
- End on outcome, not enthusiasm

---

## CRITICAL RULE: Marketplace Descriptions MUST Match Guides & Plans

**All promises made in marketplace descriptions must be verifiable in:**
1. The training guide (actual sections and content)
2. The training plan workouts (what's actually programmed)
3. Race-specific preparation requirements

**If it's not in the guide or plan, it cannot be in the marketplace description.**

---

## Guide Sections (What's Actually Covered)

All guides include these 14 sections:

1. **Training Plan Brief** - Race intro, plan overview, expectations
2. **Before You Start** - FTP testing, equipment needs, setup
3. **Training Fundamentals** - Philosophy, periodization, zones
4. **Your 12-Week Arc** - Phase breakdown (Base, Build, Peak, Taper)
5. **Training Zones** - Power, HR, RPE zones and how to set them
6. **Workout Execution** - How to execute different workout types
7. **Technical Skills** - Race-specific skills (cornering, descending, eating while riding, group riding, emergency repairs)
8. **Fueling & Hydration** - Gut training, race-day nutrition, hydration protocols
9. **Mental Training** - 6-2-7 breathing, reframing, performance statements, anchoring
10. **Race Tactics** - Three-act structure, pacing decisions, tactical moments
11. **Race-Specific Preparation** - Race hazards, weather strategy, equipment checklist
12. **Race Week Protocol** - Taper guidelines, race morning timeline, gear checklist
13. **Women-Specific Considerations** - Menstrual cycle, iron, fueling differences, heat/hydration, recovery
14. **FAQ** - 14 common questions with short answers

---

## What Marketplace Descriptions CAN Promise

### ✅ Race-Specific Features (Section 11)
- **Flint Hills technical skills** - Cornering, descending, eating while riding (Section 7)
- **Dress rehearsal in week 9** - Tests nutrition, pacing, mental prep (Section 11 table)
- **Power pacing for 200-mile endurance** - Hold watts, not speed (Section 6, 10)

### ✅ Guide Topics (What's Actually Covered)
- **Fueling: Gut training protocol** - Section 8 covers gut training, race-day nutrition
- **Technical Skills: Flint Hills cornering and descending** - Section 7 covers 5 key skills
- **Race Tactics: Three-act structure** - Section 10 covers three-act structure with tactical decisions
- **Mental: 6-2-7 breathing and performance statements** - Section 9 covers mental training framework

### ✅ Tier-Specific Pain Points

**Finisher (8-12 hrs/week):**
- Most common mistake: Training too hard on easy days (Section 6)
- Polarized training (80% easy, 20% hard) - Section 3
- Two quality sessions per week - Section 4
- Long rides building to 4-5 hours - Section 4

**Ayahuasca (0-5 hrs/week):**
- Time constraints - maximize fitness from minimal time
- HIIT that works - not base-building that breaks you
- 3-5 quality hours vs 8 junk hours

**Compete (12-18 hrs/week):**
- Race fitness that competes - not just finishes
- Block periodization - Section 4
- Threshold power that holds for hours
- Repeatability - surge and recover

**Podium (18+ hrs/week):**
- Elite-level preparation
- Massive aerobic volume
- GOAT Method or HVLI - Section 4
- Multi-signal autoregulation

---

## What Marketplace Descriptions CANNOT Promise

### ❌ Specific Protocols Not in Guides
- **"Heat protocol weeks 6-10"** - Guide mentions heat adaptation but NO specific protocol exists
- **"Week 6 protocol so 95° feels manageable"** - No week 6 protocol detailed in guide
- Any specific week-by-week protocol not documented in Section 11

### ❌ Features Not in Plans
- Strength training (plans don't program strength)
- Multiple block options (plans have single block)
- Features not mentioned in guide sections

---

## Alignment Checklist

Before generating marketplace descriptions:

1. **Verify race-specific features** match Section 11 (Race-Specific Preparation)
2. **Verify guide topics** match actual guide sections (7, 8, 9, 10, 11)
3. **Verify choice features** match tier-specific pain points and plan structure
4. **Verify expectations** match tier performance expectations from Section 1
5. **Remove any claims** about protocols/features not in guides or plans

---

## Updating Process

When guides or plans change:

1. Update race variables (`race_variables/[race].py`) to match new guide content
2. Update tier variables (`tier_variables/[tier].py`) to match new plan structure
3. Regenerate all marketplace descriptions
4. Verify character counts (must be ≤ 4000 including HTML)
5. Commit with note about what changed and why

---

## Example: Unbound 200 Finisher Intermediate

**What's ACTUALLY in the guide:**
- Section 7: Technical Skills (5 skills including Flint Hills cornering, descending, eating while riding)
- Section 8: Fueling & Hydration (gut training protocol, race-day nutrition)
- Section 9: Mental Training (6-2-7 breathing, performance statements)
- Section 10: Race Tactics (three-act structure)
- Section 11: Race-Specific (mentions heat adaptation but no protocol, Flint Hills skills, dress rehearsal)

**What marketplace CAN say:**
- "Flint Hills technical skills — cornering, descending, eating while riding"
- "Fueling: Gut training protocol so you can eat at mile 60 when nothing sounds good"
- "Race Tactics: Three-act structure — what to do when everyone's redlining in the first 30"
- "Mental: 6-2-7 breathing and performance statements for when brain says 'stop'"

**What marketplace CANNOT say:**
- "Heat protocol weeks 6-10 so 95° feels manageable" (no protocol exists)
- "Week 6 protocol so 95° feels manageable by race day" (no week 6 protocol)

---

**Last Updated:** December 10, 2024  
**Maintained By:** Guide Generator System


