# Training Plan Survey

A survey system for collecting feedback from athletes using Gravel God training plans.

## Overview

The survey is designed to:
- Collect feedback on training plan effectiveness
- Identify common challenges athletes face
- Gather data on plan adherence and confidence levels
- Provide actionable insights for plan improvements

## Files

- `docs/survey.html` - Main survey form (styled to match guides)
- `scripts/collect_survey_data.py` - Script for processing survey responses
- `data/survey_responses/` - Directory where responses are stored

## Embedding in Workouts

### Option 1: Link in ZWO Description

Add a link to the survey in rest day workout descriptions:

```xml
<description>
• Rest day. Life day. Do what you need to do.

• TRAINING PLAN SURVEY:
Take 2-3 minutes to share your feedback: https://wattgod.github.io/gravel-landing-page-project/survey.html?race=Mid%20South&plan=Ayahuasca%20Beginner&week=4
</description>
```

### Option 2: Direct Link in TrainingPeaks

Add the survey link directly in TrainingPeaks workout notes for rest days or specific weeks.

## Survey Questions

1. **Overall satisfaction** (1-5 rating)
2. **Biggest challenge** (multiple choice)
3. **Confidence level** (1-5 rating)
4. **Training hours per week** (number)
5. **Following plan** (yes/mostly/partially/no)
6. **What's working well** (open-ended, optional)
7. **Biggest concern** (multiple choice)
8. **Plan difficulty** (1-5 rating)
9. **What to change** (open-ended, optional)
10. **Additional feedback** (open-ended, optional)

## Data Collection

### Method 1: GitHub Issues (Recommended)

The survey attempts to create a GitHub Issue automatically. If authentication is not available, it falls back to showing formatted data that can be manually submitted.

### Method 2: Local JSON Files

Survey responses can be saved as JSON files in `data/survey_responses/` and committed to the repository.

### Method 3: Manual GitHub Issue Creation

Users can copy the formatted survey data and create a GitHub Issue manually at:
https://github.com/wattgod/gravel-landing-page-project/issues/new

## URL Parameters

The survey accepts these URL parameters:
- `race` - Race name (e.g., "Mid South")
- `plan` - Plan name (e.g., "Ayahuasca Beginner")
- `week` - Current week number (e.g., "4")

Example:
```
https://wattgod.github.io/gravel-landing-page-project/survey.html?race=Mid%20South&plan=Ayahuasca%20Beginner&week=4
```

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
