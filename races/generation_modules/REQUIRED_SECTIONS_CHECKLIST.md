# Training Guide Section Checklist

This document lists all required sections that must be present in every training guide, and conditional sections that appear only in specific plan types.

## Required Sections (All Plans)

1. **Section 1: Training Plan Brief** (`section-1-training-plan-brief`)
   - Race introduction
   - Course description
   - What it takes to finish
   - Plan preparation summary

2. **Section 2: Before You Start** (`section-2-before-you-start`)
   - Health & safety check
   - Non-negotiables
   - Equipment requirements

3. **Section 3: Training Fundamentals** (`section-3`)
   - How training works
   - Stress and adaptation
   - Consistency principles

4. **Section 4: Your Training Arc** (`section-4`)
   - 12-week arc (for 12-week plans)
   - 6-week arc (for 6-week "Save My Race" plans)

5. **Section 5: Training Zones** (`section-5`)
   - Zone definitions
   - Power and heart rate zones
   - Zone usage guidelines

6. **Section 6: Workout Execution** (`section-6`)
   - How to execute workouts
   - Warm-up and cool-down
   - Recovery between intervals

7. **Section 7: Technical Skills** (`section-7`)
   - Race-specific technical skills
   - Cornering, descending, handling

8. **Section 8: Fueling & Hydration** (`section-8-fueling-hydration`)
   - Daily nutrition
   - Workout fueling
   - Race-day nutrition
   - Hydration protocols
   - Cramping management
   - Weight management

9. **Section 9: Mental Training** (`section-9`)
   - Breathing techniques (6-2-7)
   - Reframing strategies
   - Suffering management

10. **Section 10: Race Tactics** (`section-10`)
    - Three-act structure
    - Tactical decision trees
    - Mental landmarks

11. **Section 11: Race-Specific Preparation** (`section-11`)
    - Weather strategy
    - Heat acclimatization protocol
    - Altitude considerations (if applicable)

12. **Section 12: Race Week Protocol** (`section-12-race-week-protocol`)
    - Race morning timeline
    - Comprehensive gear checklist
    - The night before

13. **Women-Specific Considerations**
    - **Non-Masters plans:** `section-13-women-specific-considerations`
    - **Masters plans:** `section-14-women-specific-considerations`
    - Must include: "Women aren't small men" content
    - Menstrual cycle and training
    - Iron management
    - Fueling differences
    - Heat/hydration considerations
    - Recovery differences
    - Pregnancy/postpartum guidance

14. **Frequently Asked Questions**
    - **Non-Masters plans:** `section-14-faq`
    - **Masters plans:** `section-15-faq`
    - Must be Q&A format (not glossary)
    - 14 questions with answers

## Conditional Sections

### Masters Plans Only

- **Section 13: Masters-Specific Considerations** (`section-13-masters-specific-considerations`)
  - Physiology of aging
  - Polarized training for masters
  - Recovery protocols
  - Periodization adjustments
  - Strength training
  - Race-day execution differences

## Section Numbering Rules

### Non-Masters Plans
- Sections 1-12: Standard numbering
- Section 13: Women-Specific Considerations
- Section 14: FAQ

### Masters Plans
- Sections 1-12: Standard numbering
- Section 13: Masters-Specific Considerations
- Section 14: Women-Specific Considerations
- Section 15: FAQ

## Verification

Run the verification script before committing:

```bash
python3 races/generation_modules/verify_guide_structure.py docs/guides/unbound-gravel-200/
```

This will check:
1. ✅ All TOC links match section IDs
2. ✅ All required sections are present
3. ✅ No duplicate section IDs
4. ✅ Women-Specific section has actual content
5. ✅ Conditional sections are correctly included/excluded

## Common Issues to Watch For

1. **TOC Links Don't Match Section IDs**
   - TOC uses `#section-3-training-fundamentals` but section has `id="section-3"`
   - Fix: Update TOC links to match actual section IDs

2. **Missing Women-Specific Section**
   - Section completely missing or has placeholder content
   - Fix: Ensure Women-Specific section is in template and generator includes it

3. **Incorrect Section Numbering**
   - FAQ labeled as section 14 in Masters plan (should be 15)
   - Fix: Update generator renumbering logic

4. **QUICK REFERENCE Section**
   - Old section that should not exist
   - Fix: Remove from template

5. **Glossary Instead of FAQ**
   - Section 14/15 has glossary terms instead of Q&A
   - Fix: Use FAQ format with questions and answers


