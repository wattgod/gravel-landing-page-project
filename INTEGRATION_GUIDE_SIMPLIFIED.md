# Integration Guide: Simplified Landing Page Structure

## Overview

This guide shows how to integrate the new simplified landing page structure:
- **5 core training plans** (instead of 15)
- **Build My Custom Training Plan** section
- **Get Coaching** section

## New Components Created

### 1. `simplified_training_plans_section.py`
Generates the 5 core plan cards:
- Finisher
- Finisher Plus
- Compete
- Compete Masters
- Podium

### 2. `custom_training_plan_section.py`
Generates the "Build My Custom Training Plan" section with questionnaire CTA.

### 3. `coaching_section.py`
Generates the "Get Coaching" section with contact information.

## Integration Steps

### Step 1: Update `generate_landing_page.py`

Add imports for new sections:

```python
# Add these imports
from automation.simplified_training_plans_section import generate_simplified_plans_html
from automation.custom_training_plan_section import generate_custom_plan_html
from automation.coaching_section import generate_coaching_html
```

### Step 2: Replace Training Plans Section Generation

In the `build_elementor_json()` function, replace:

```python
# OLD:
training_html = generate_training_plans_html(data)

# NEW:
simplified_plans_html = generate_simplified_plans_html(data)
custom_plan_html = generate_custom_plan_html(data)
coaching_html = generate_coaching_html(data)
```

### Step 3: Update Widget Replacement

Replace the single training plans widget with three widgets:

```python
# OLD: Single widget
replace_widget_html(elementor_json, "Training Plans", training_html)

# NEW: Three widgets
replace_widget_html(elementor_json, "Training Plans", simplified_plans_html, element_id="training-plans")
replace_widget_html(elementor_json, "Custom Plan", custom_plan_html, element_id="custom-plan")
replace_widget_html(elementor_json, "Coaching", coaching_html, element_id="coaching")
```

Or combine into one section if preferred:

```python
combined_training_html = f"""
{simplified_plans_html}
{custom_plan_html}
{coaching_html}
"""
replace_widget_html(elementor_json, "Training Plans", combined_training_html)
```

## New Landing Page Flow

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
   └─ [Coaching CTA / Email]
   ↓
6. Additional Sections (Course Map, Ratings, etc.)
```

## Plan Consolidation

### Current 15 Plans → New 5 Plans

| New Plan | Replaces | Target Hours | Goal |
|----------|----------|--------------|------|
| **Finisher** | Ayahuasca Beginner, Finisher Beginner | 0-5 hrs/week | Finish the race |
| **Finisher Plus** | Ayahuasca Intermediate, Finisher Intermediate | 5-8 hrs/week | Finish strong |
| **Compete** | Compete Intermediate, Compete Advanced | 8-12 hrs/week | Competitive finish |
| **Compete Masters** | Compete Masters, Ayahuasca Masters, Finisher Masters | 8-12 hrs/week | Age-group competitive |
| **Podium** | Podium Advanced, Podium Advanced GOAT | 12+ hrs/week | Race to win |

**Save My Race** (6 weeks) remains as optional add-on for any plan.

## Testing

Test the new components:

```bash
# Test simplified plans
python3 automation/simplified_training_plans_section.py

# Test custom plan section
python3 automation/custom_training_plan_section.py

# Test coaching section
python3 automation/coaching_section.py
```

## Example Output

See `automation/example_simplified_landing_page.html` for a visual example of how all three sections work together.

## Benefits

1. **Simpler UX**: 5 clear choices vs 15 confusing options
2. **Natural Upsell Path**: Plans → Custom → Coaching
3. **Better Conversion**: Less decision paralysis
4. **Easier Maintenance**: Fewer plans to update
5. **Clear Positioning**: Each plan has distinct target athlete

## Migration Notes

- Existing plan files can be archived, not deleted
- Plan metadata can be updated to reflect new structure
- Questionnaire flow remains the same
- Custom plan generation logic unchanged

