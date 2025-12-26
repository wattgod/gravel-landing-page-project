# Simplified Landing Page Structure - Summary

## What You Asked For

✅ **Simplify 15 training plans to 5**  
✅ **Add "Build my custom training plan" section**  
✅ **Add "Get coaching" section**

## What Was Created

### 1. Documentation
- **LANDING_PAGE_REDESIGN.md** - Complete redesign proposal with plan consolidation mapping
- **INTEGRATION_GUIDE_SIMPLIFIED.md** - Step-by-step integration instructions
- **SIMPLIFIED_STRUCTURE_SUMMARY.md** - This summary document

### 2. New Components

#### `automation/simplified_training_plans_section.py`
- Generates 5 core plan cards in a clean grid layout
- Each plan shows: number, name, duration, target hours, goal, philosophy
- Responsive design matching your existing style
- Plan cards link to custom plan section

#### `automation/custom_training_plan_section.py`
- Standalone "Build My Custom Training Plan" section
- Two-column layout: benefits on left, CTA on right
- Links to existing questionnaire
- Emphasizes personalization and same-day delivery

#### `automation/coaching_section.py`
- Standalone "Get Coaching" section
- Two-column layout: CTA on left, features on right
- Email contact: gravelgodcoaching@gmail.com
- Lists coaching benefits (weekly adjustments, strategy calls, etc.)

### 3. Visual Example
- **automation/example_simplified_landing_page.html** - Complete visual example showing all three sections

## The 5 Core Plans

| Plan | Target Hours | Goal | Replaces |
|------|-------------|------|----------|
| **1. Finisher** | 0-5 hrs/week | Finish the race | Ayahuasca Beginner, Finisher Beginner |
| **2. Finisher Plus** | 5-8 hrs/week | Finish strong | Ayahuasca Intermediate, Finisher Intermediate |
| **3. Compete** | 8-12 hrs/week | Competitive finish | Compete Intermediate, Compete Advanced |
| **4. Compete Masters** | 8-12 hrs/week | Age-group competitive | Compete Masters, Ayahuasca Masters, Finisher Masters |
| **5. Podium** | 12+ hrs/week | Race to win | Podium Advanced, Podium Advanced GOAT |

**Save My Race** (6 weeks) - Optional add-on for any plan

## New Landing Page Flow

```
Hero Section
    ↓
Race Overview
    ↓
5 Core Training Plans ← NEW: Simplified from 15
    ↓
Build My Custom Training Plan ← NEW: Standalone section
    ↓
Get Coaching ← NEW: Standalone section
    ↓
Other Sections (Course Map, Ratings, etc.)
```

## Design Features

### Training Plans Section
- Clean 5-card grid (responsive)
- Numbered badges (1-5)
- Clear target athlete and goal for each
- Consistent styling with existing design system
- "Save My Race" note at bottom

### Custom Plan Section
- Beige background (#F5F5DC) to differentiate
- Two-column: benefits list + CTA block
- Links to questionnaire
- Emphasizes personalization

### Coaching Section
- Matches existing design system
- Two-column: CTA block + features list
- Email contact prominently displayed
- Yellow accent color for CTA button

## Next Steps

1. **Review the components** - Test them with `python3 automation/[component].py`
2. **Check the visual example** - Open `automation/example_simplified_landing_page.html` in browser
3. **Integrate into generator** - Follow `INTEGRATION_GUIDE_SIMPLIFIED.md`
4. **Test on sample race** - Generate a landing page with new structure
5. **Deploy** - Update production landing pages

## Files Ready to Use

All components are tested and working:
- ✅ `simplified_training_plans_section.py` - Generates 5-plan grid
- ✅ `custom_training_plan_section.py` - Generates custom plan section
- ✅ `coaching_section.py` - Generates coaching section
- ✅ All components match your existing design system
- ✅ All components are responsive
- ✅ All components follow your color scheme and typography

## Questions?

- See `LANDING_PAGE_REDESIGN.md` for detailed plan consolidation rationale
- See `INTEGRATION_GUIDE_SIMPLIFIED.md` for technical integration steps
- See `automation/example_simplified_landing_page.html` for visual reference

