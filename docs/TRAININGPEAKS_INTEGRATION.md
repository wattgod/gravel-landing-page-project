# TrainingPeaks Integration Guide

## Quick Copy-Paste Templates

### For Plan Description:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📘 YOUR COMPLETE TRAINING GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Access your comprehensive training guide here:
[GUIDE_URL]

This guide covers:
✓ Race-specific preparation protocols
✓ Heat adaptation (if applicable)
✓ Fueling strategy for [DISTANCE] miles
✓ Workout execution tips
✓ Recovery and race-week protocol
✓ Mental training techniques
✓ Equipment recommendations

Read this BEFORE starting Week 1.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### For Workout Notes:

Add to key workout descriptions:

```
📖 See your training guide for detailed execution tips:
[GUIDE_URL]
```

## Getting Guide URLs

### Method 1: Quick Script
```bash
bash docs/GET_GUIDE_URL.sh "Race Name" "tier" "level"
```

### Method 2: URL Mapping
```bash
cat docs/URL_MAPPING.md
```

### Method 3: Manual Format
```
https://wattgod.github.io/gravel-landing-page-project/guides/{race-slug}/{tier}-{level}.html
```

## URL Format Rules

- Race names: Converted to lowercase, spaces/hyphens normalized
  - "Unbound Gravel 200" → `unbound-gravel-200`
  - "SBT GRVL" → `sbt-grvl`

- Tiers: Lowercase
  - "COMPETE" → `compete`
  - "FINISHER" → `finisher`

- Levels: Lowercase, spaces become hyphens
  - "Save My Race" → `save-my-race`
  - "Advanced GOAT" → `advanced-goat`

## Examples

- Unbound Gravel 200, Compete Advanced:
  `https://wattgod.github.io/gravel-landing-page-project/guides/unbound-gravel-200/compete-advanced.html`

- Unbound Gravel 200, Finisher Save My Race:
  `https://wattgod.github.io/gravel-landing-page-project/guides/unbound-gravel-200/finisher-save-my-race.html`

## Best Practices

1. **Add URL to Plan Description** - Athletes see it immediately
2. **Mention in Week 1 workout notes** - Remind them to read it
3. **Include in welcome email** - If you send one
4. **Test the URL** - Click it yourself before sharing

## Troubleshooting

**URL doesn't work?**
- Check deployment status: https://github.com/wattgod/gravel-landing-page-project/deployments
- Verify file exists: `ls docs/guides/{race-slug}/{tier}-{level}.html`
- Wait 2-3 minutes after pushing changes

**Wrong guide shows?**
- Verify race name spelling matches exactly
- Check tier/level capitalization doesn't matter (URLs are lowercase)
- Use the GET_GUIDE_URL.sh script for exact URL

