# Training Plan Survey - Post-Completion

A survey system for collecting feedback from athletes **after completing** their Gravel God training plans.

## Overview

The survey is designed to:
- Collect post-completion feedback on training plan effectiveness
- Identify what worked and what didn't work in each specific plan
- Gather data on race performance vs expectations
- Provide actionable, plan-specific insights for improvements
- Track plan adherence and outcomes

## Files

- `docs/survey.html` - Main survey form (styled to match guides)
- `scripts/collect_survey_data.py` - Script for processing survey responses
- `data/survey_responses/` - Directory where responses are stored

## Embedding in Workouts

**Important:** This survey is for **after** completing the training plan, not during. Add it to the final week or post-race.

### Option 1: Link in Final Week ZWO Description

Add a link to the survey in the final week's rest day or post-race workout:

```xml
<description>
• Rest day. Life day. Do what you need to do.

• TRAINING PLAN SURVEY (POST-COMPLETION):
You've completed your training plan! Share your experience to help us improve: 
https://wattgod.github.io/gravel-landing-page-project/survey.html?race=Mid%20South&plan=Ayahuasca%20Beginner
</description>
```

### Option 2: Post-Race Follow-up

Send the survey link after race completion via email or TrainingPeaks message.

### Option 3: Final Week Workout

Add to the last workout of the plan (Week 12 or Week 6 for SMR plans).

## Survey Questions (Post-Completion)

1. **Race completion status** (Yes/DNF/DNS/Haven't raced yet)
2. **Plan effectiveness** (1-5 rating)
3. **Plan adherence** (Exactly/Mostly/Partially/Reference only)
4. **Average training hours per week** (number)
5. **What worked best** (checkboxes: intensity, volume, structure, recovery, specificity, guide, other)
6. **What didn't work** (checkboxes: intensity, volume, structure, recovery, specificity, guide, nothing major)
7. **Race performance vs expectations** (Exceeded/Met/Below/Significantly below) - *shown only if race completed*
8. **Plan difficulty rating** (1-5 rating)
9. **Would recommend** (Yes/Probably/Maybe/No)
10. **Specific improvements needed** (required open-ended - most important for actionable feedback)
11. **Additional feedback** (optional open-ended)

## Data Collection

### Method 1: GitHub Issues (Recommended)

The survey attempts to create a GitHub Issue automatically. If authentication is not available, it falls back to showing formatted data that can be manually submitted.

### Method 2: Local JSON Files

Survey responses can be saved as JSON files in `data/survey_responses/` and committed to the repository.

### Method 3: Manual GitHub Issue Creation

Users can copy the formatted survey data and create a GitHub Issue manually at:
https://github.com/wattgod/gravel-landing-page-project/issues/new

## URL Parameters

The survey accepts these URL parameters (both required for plan-specific feedback):
- `race` - Race name (e.g., "Mid South")
- `plan` - Plan name (e.g., "Ayahuasca Beginner")

Example:
```
https://wattgod.github.io/gravel-landing-page-project/survey.html?race=Mid%20South&plan=Ayahuasca%20Beginner
```

**Note:** The `week` parameter is no longer used since this is a post-completion survey.

## Styling

The survey matches the guide styling:
- Font: Sometype Mono (monospace)
- Colors: Gravel God brand colors
- Layout: Clean, minimal, readable
- Responsive: Works on mobile and desktop

## Best Practices

The survey follows survey design best practices:
- ✅ Starts with easy questions (satisfaction rating)
- ✅ Mixes question types (rating, multiple choice, open-ended)
- ✅ Keeps it short (10 questions, 2-3 minutes)
- ✅ Asks about behavior/experience, not just opinions
- ✅ Includes optional open-ended questions for rich feedback
- ✅ Clear, specific language
- ✅ Logical question flow

## Future Enhancements

- [ ] GitHub API authentication for automatic issue creation
- [ ] Analytics dashboard for survey responses
- [ ] Automated response aggregation and reporting
- [ ] Integration with TrainingPeaks API
- [ ] Email notifications for new responses
