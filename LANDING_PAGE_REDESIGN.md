# Landing Page Redesign Proposal

## Current State
- **15 training plans** organized by:
  - Ayahuasca (4 plans: Beginner, Intermediate, Masters, Save My Race)
  - Finisher (5 plans: Beginner, Intermediate, Advanced, Masters, Save My Race)
  - Compete (4 plans: Intermediate, Advanced, Masters, Save My Race)
  - Podium (2 plans: Advanced, Advanced GOAT)

## Proposed New Structure

### 1. Simplified Training Plans (5 Plans)

Instead of 15 plans, consolidate to **5 core plans** that cover the spectrum:

#### **Plan 1: Finisher** (12 weeks)
- **Target**: Complete beginners, time-limited (0-5 hrs/week)
- **Goal**: Finish the race
- **Philosophy**: HIIT-focused survival mode
- **Replaces**: Ayahuasca Beginner, Finisher Beginner

#### **Plan 2: Finisher Plus** (12 weeks)
- **Target**: Intermediate riders, moderate time (5-8 hrs/week)
- **Goal**: Finish strong and comfortable
- **Philosophy**: Balanced HIIT + endurance
- **Replaces**: Ayahuasca Intermediate, Finisher Intermediate

#### **Plan 3: Compete** (12 weeks)
- **Target**: Advanced riders, committed training (8-12 hrs/week)
- **Goal**: Competitive finish, race for position
- **Philosophy**: Structured periodization
- **Replaces**: Compete Intermediate, Compete Advanced

#### **Plan 4: Compete Masters** (12 weeks)
- **Target**: Masters athletes (40+), experienced (8-12 hrs/week)
- **Goal**: Age-group competitive
- **Philosophy**: Masters-optimized recovery and intensity
- **Replaces**: Compete Masters, Ayahuasca Masters, Finisher Masters

#### **Plan 5: Podium** (12 weeks)
- **Target**: Elite/experienced athletes (12+ hrs/week)
- **Goal**: Race to win, podium finish
- **Philosophy**: High-volume, race-specific preparation
- **Replaces**: Podium Advanced, Podium Advanced GOAT

#### **Save My Race** (6 weeks) - Optional Quick Fix
- Available as add-on for any plan
- Emergency 6-week prep for late starters

---

### 2. New Section: "Build My Custom Training Plan"

**Position**: After the 5 core plans

**Structure**:
```
┌─────────────────────────────────────────┐
│  Build My Custom Training Plan          │
├─────────────────────────────────────────┤
│  [Questionnaire CTA Button]             │
│                                         │
│  ✓ Personalized to your schedule        │
│  ✓ Race-specific adaptations            │
│  ✓ Workouts for any device              │
│  ✓ Delivered same day                   │
└─────────────────────────────────────────┘
```

**Content**:
- **Headline**: "Need Something Different?"
- **Subhead**: "Build a custom plan tailored to YOUR life, schedule, and goals"
- **CTA**: "Build My Custom Training Plan →"
- **Features**:
  - Personalized to your available hours
  - Adapts to your race date
  - Considers injury history and constraints
  - Race-specific strategy included

**Implementation**: 
- Link to existing questionnaire: `training-plan-questionnaire.html?race={race_slug}`
- Can reuse existing `training_plans_section.py` component

---

### 3. New Section: "Get Coaching"

**Position**: After "Build My Custom Training Plan"

**Structure**:
```
┌─────────────────────────────────────────┐
│  Get Coaching                           │
├─────────────────────────────────────────┤
│  [Coaching CTA Button]                  │
│                                         │
│  ✓ Weekly plan adjustments              │
│  ✓ Race strategy calls                  │
│  ✓ Unlimited questions                  │
│  ✓ TrainingPeaks integration            │
└─────────────────────────────────────────┘
```

**Content**:
- **Headline**: "Want More Support?"
- **Subhead**: "Get personalized coaching with weekly check-ins and race strategy"
- **CTA**: "Learn About Coaching →"
- **Features**:
  - Weekly plan adjustments based on progress
  - Pre-race strategy call
  - Unlimited questions via email/messaging
  - TrainingPeaks integration
  - Race-day support

**Pricing/Info**:
- Link to coaching page or contact form
- Email: gravelgodcoaching@gmail.com
- Or embed contact form

---

## Proposed Landing Page Flow

```
1. Hero Section
   ↓
2. Race Overview / Course Description
   ↓
3. Training Plans (5 Core Plans)
   ├─ Plan 1: Finisher
   ├─ Plan 2: Finisher Plus
   ├─ Plan 3: Compete
   ├─ Plan 4: Compete Masters
   └─ Plan 5: Podium
   ↓
4. Build My Custom Training Plan
   └─ [Questionnaire CTA]
   ↓
5. Get Coaching
   └─ [Coaching CTA]
   ↓
6. Additional Sections (Nutrition, Gear, etc.)
```

---

## Implementation Plan

### Phase 1: Simplify Plans
1. **Consolidate plan files**:
   - Keep 5 core plan directories
   - Archive or merge the other 10 plans
   - Update plan metadata to reflect new structure

2. **Update plan selection UI**:
   - Replace 15-card grid with 5-card grid
   - Update plan descriptions
   - Add "Save My Race" as optional add-on

### Phase 2: Add Custom Plan Section
1. **Create component**: `custom_training_plan_section.py`
   - Similar structure to existing `training_plans_section.py`
   - Points to questionnaire
   - Emphasizes personalization

2. **Update landing page generator**:
   - Add custom plan section after core plans
   - Maintain existing questionnaire flow

### Phase 3: Add Coaching Section
1. **Create component**: `coaching_section.py`
   - Coaching benefits and features
   - CTA to contact/coaching page
   - Email or form integration

2. **Update landing page generator**:
   - Add coaching section after custom plan section

---

## Plan Consolidation Mapping

### Finisher (New Plan 1)
**Merges**:
- Ayahuasca Beginner (12 weeks)
- Finisher Beginner (12 weeks)

**Key Elements**:
- 0-5 hrs/week target
- HIIT-focused
- Survival mode philosophy
- Maximum time efficiency

### Finisher Plus (New Plan 2)
**Merges**:
- Ayahuasca Intermediate (12 weeks)
- Finisher Intermediate (12 weeks)

**Key Elements**:
- 5-8 hrs/week target
- Balanced approach
- More endurance work than Finisher
- Still time-efficient

### Compete (New Plan 3)
**Merges**:
- Compete Intermediate (12 weeks)
- Compete Advanced (12 weeks)

**Key Elements**:
- 8-12 hrs/week target
- Full periodization
- Race-specific work
- Competitive focus

### Compete Masters (New Plan 4)
**Merges**:
- Compete Masters (12 weeks)
- Ayahuasca Masters (12 weeks)
- Finisher Masters (12 weeks)

**Key Elements**:
- 8-12 hrs/week target
- Masters-optimized recovery
- Age-group competitive
- Experience-based pacing

### Podium (New Plan 5)
**Merges**:
- Podium Advanced (12 weeks)
- Podium Advanced GOAT (12 weeks)

**Key Elements**:
- 12+ hrs/week target
- High-volume training
- Elite preparation
- Race-to-win mentality

---

## Benefits of New Structure

1. **Simpler Decision Making**: 5 clear options vs 15 confusing choices
2. **Better User Experience**: Less analysis paralysis
3. **Clearer Positioning**: Each plan has distinct target athlete
4. **Upsell Path**: Plans → Custom → Coaching (natural progression)
5. **Maintainability**: Fewer plans to maintain and update

---

## Next Steps

1. Review and approve plan consolidation mapping
2. Create new plan components for 5 core plans
3. Build "Build My Custom Training Plan" section
4. Build "Get Coaching" section
5. Update landing page generator
6. Test on sample race landing page
7. Deploy to production

