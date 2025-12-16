# GG Voice and Tone Guidelines

## Overview

All content for Gravel God landing pages, race data files, and training plan descriptions must adhere to the **Matti voice**—a dry, understated, matter-of-fact tone that avoids theatrical language, motivational-speech energy, or dramatic buildup.

## Core Principles

### ✅ DO: Matti Voice Characteristics

- **Dry and matter-of-fact**: State facts directly without embellishment
- **Understated**: Let the content speak for itself without hype
- **Observational**: Report what is, not what feels impressive
- **Direct statements**: Minimal flourish, maximum clarity
- **Confidence without volume**: Know what you're saying without shouting
- **Understated humor**: Subtle, not performative

### ❌ DON'T: Voice Violations

- **Dramatic buildup**: Avoid phrases like "terminal climb," "existential questions," "transformation disguised as punishment"
- **Heavy-handed metaphors**: Don't force poetic language where facts suffice
- **Epic tone**: Don't try to sound impressive or epic
- **Motivational-speech energy**: Avoid rallying-cry language
- **Theatrical suffering**: Treat difficulty matter-of-factly, not dramatically
- **Overly impressed tone**: Be observational, not awestruck

## Examples

### ❌ WRONG: Theatrical/Dramatic

> "The terminal climb arrives at mile 130, where riders face existential questions about their training choices. This transformation disguised as punishment will expose every weakness."

### ✅ RIGHT: Matter-of-Fact

> "Double Peak arrives at mile 116-130. You've ridden six hours. Your legs are empty. Now climb 1,800 feet over 4.5 miles with grades reaching 23%. The gradient doesn't care about your training plan."

### ❌ WRONG: Motivational

> "This is where champions are made! Push through the pain and discover what you're truly capable of!"

### ✅ RIGHT: Observational

> "Black Canyon is where the race stops being fun. The washboard fire road vibrates your body while steep sand sections force power outputs you can't sustain."

### ❌ WRONG: Overly Impressed

> "The legendary Belgian Waffle Ride stands as a monument to human endurance and cycling excellence!"

### ✅ RIGHT: Direct

> "BWR California is one of gravel's original monuments and the only event successfully claiming 'un-road' identity."

## Application Areas

### Race Data Files (`data/*.json`)

All content in race JSON files must follow Matti voice:
- `ratings_breakdown.explanation` fields
- `history.origin_story` and `history.reputation`
- `course_description.character` and `suffering_zones.desc`
- `biased_opinion.summary`
- `black_pill.reality`
- `final_verdict.should_you_race` and `alternatives`
- `tldr` sections

### Landing Page Content

- Course profile descriptions
- Biased opinion sections
- Editorial content (History, Course Description, Experience)
- Quotes (Course Profile, Biased Opinion, Black Pill)
- Final Verdict sections

### Training Plan Descriptions

- Marketplace descriptions
- Guide content
- Plan philosophy explanations

## Specific Language Guidelines

### Suffering/Difficulty

**Avoid:**
- "Suffering," "agony," "torment" (unless quoting someone else)
- "Transformative journey"
- "Character-building experience"
- "Ultimate test"

**Use:**
- "Hard," "difficult," "challenging"
- "The race stops being fun"
- "Your legs are empty"
- "The course doesn't care"

### Achievements/Accomplishments

**Avoid:**
- "Legendary," "epic," "monumental" (unless factual, like "one of gravel's original monuments")
- "Incredible," "amazing," "unbelievable"
- "Life-changing transformation"

**Use:**
- "Significant," "notable," "important"
- "One of gravel's original monuments" (factual)
- "Credible," "respected"

### Technical Descriptions

**Avoid:**
- "Brutal," "savage," "merciless"
- "Soul-crushing," "spirit-breaking"

**Use:**
- "Steep," "technical," "demanding"
- "The field shatters here"
- "Equipment casualties"

## Altitude vs. Elevation

**Critical distinction:**
- **Altitude** = elevation above sea level (e.g., "Stillwater sits at ~900 feet")
- **Elevation** = total climbing/elevation gain (e.g., "10,000 feet of climbing")

**Rating altitude:**
- If race is at sea level or under 5,000 feet: Score 5/5, explain that altitude is irrelevant
- If race is at altitude (5,000+ feet): Score appropriately based on altitude impact
- **DO NOT** confuse elevation gain with altitude

**Example (BWR):**
- ✅ "Sea level start rising to approximately 2,500 feet maximum. Zero altitude concerns. Your lungs aren't the problem here."
- ❌ "High altitude challenge" (BWR is NOT at altitude)

## Testing and Validation

All content must pass voice/tone regression tests (see `test_regression_voice_tone.py`).

### Automated Checks

Tests verify:
1. No theatrical language patterns
2. No motivational-speech patterns
3. No dramatic buildup phrases
4. Altitude vs. elevation usage is correct
5. Matter-of-fact tone throughout

### Manual Review Checklist

Before finalizing any content:
- [ ] No "terminal," "existential," "transformation disguised as" language
- [ ] No motivational rallying-cry phrases
- [ ] Suffering described matter-of-factly, not theatrically
- [ ] Altitude rating matches actual altitude (not elevation gain)
- [ ] Direct statements, minimal hype
- [ ] Understated humor where appropriate
- [ ] Observational rather than impressed tone

## References

- Original voice guidelines: `Desktop/GGBD/GG Voice:Tone.pdf`
- Example of correct voice: Mid South data file
- Example of violations (now corrected): Previous BWR content

