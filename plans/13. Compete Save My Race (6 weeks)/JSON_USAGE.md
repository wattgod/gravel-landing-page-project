# Using JSON Template for COMPETE SAVE MY RACE

## Quick Start for Cursor AI

### To Generate a New Race-Specific Plan:

1. **Load the template:**
   ```
   Load: template.json from this folder
   Load: ../nutrition_hydration_guidelines.json
   ```

2. **Provide race-specific considerations:**
   ```
   Race: [RACE NAME]
   
   Race-Specific Considerations:
   1. Heat training needed (Weeks 2-5)
   2. Aggressive fueling: 60-90g carbs/hour (up to 100g on dress rehearsal)
   3. Dress rehearsal: 9-hour ride Week 3 Saturday (~3 weeks before race)
   4. Robust taper: Week 6 volume reduced
   5. Gravel Grit: Week 6 race day
   ```

3. **Cursor will:**
   - Load template.json
   - Load nutrition_hydration_guidelines.json
   - Apply race-specific modifications
   - Generate: `GENERATE_COMPETE_SAVEMYRACE_[RACE].py`
   - Generate: 70 ZWO files
   - Create: `COMPETE_SAVEMYRACE_[RACE]_MODIFICATIONS.md`

## Template Structure

The `template.json` contains:
- **6 weeks** of structured workout data
- **3 block options** for Weeks 2-3 (VO2max, Threshold, Durability)
- **Default modifications** (cadence work, rhythm/loaded intervals, G-Spot terminology)

## Nutrition Integration

Nutrition guidelines are automatically applied based on workout duration:
- **<60 min**: Water only
- **60-90 min**: 20-40g carbs/hr if needed
- **90-180 min**: 40-70g carbs/hr
- **3-6+ hours**: 70-90g carbs/hr (up to 100g for well-trained)

## Example: Unbound 200

See: `13. Unbound 200 - Compete Save My Race (6 weeks)/` for a complete example of:
- Modified generation script
- Generated ZWO files
- Modifications document

