# Course Breakdown Research Guide

## Overview

When researching a race for the landing page generator, identify 3-5 **KEY SUFFERING ZONES** where the course gets spicy. These should be specific, sourced, and actionable—not generic milestones.

Also included: **Random Facts Quality Standards** for ensuring facts are memorable and substantive, not just boring stats.

## What to Research

### Key Elements to Find:

1. **Named climbs or sections** (e.g., "Shellback Hill," "The Roller Coaster")
2. **Creek crossings, river fords, technical descents**
3. **Specific mileage points where the race changes character**
4. **Weather-dependent sections** (mud pits, exposed ridges)
5. **Aid station locations** and what condition riders are in when they arrive

## Research Sources

### Primary Sources (in order of reliability):

1. **Race Reports** - Search: `"[race name] race report mile 60"`
   - Blog posts from past finishers
   - Forum discussions (Reddit r/gravelcycling, BikeForums)
   - Personal race reports on Medium, personal blogs

2. **Strava Segments** - Search course on Strava
   - Named segments along the route
   - Segment comments from riders
   - Segment leaderboards (shows where people struggle)

3. **RideWithGPS** - Course route page
   - Elevation profile + comments
   - Route notes from organizers
   - User comments on the route

4. **YouTube Race Videos** - Search: `"[race name] race video"`
   - Timestamped sections showing difficult terrain
   - Rider commentary during race
   - Post-race interviews

5. **Event Organizer Descriptions** - Official race website
   - Course previews
   - Pre-race briefings
   - Course notes/guides

6. **Past Finisher Interviews** - Podcasts, articles
   - Post-race interviews
   - Training plan testimonials
   - Race recap articles

## Writing Rules

### ✅ GOOD Example:

```
Mile 60: The Grind Begins at aid station two. This marks the start of the Roller Coaster section - 8 miles of 12-15% punches. Race reports consistently cite this as the point where undertrained riders start walking. Weather note: Fast and tactical when dry, unrideable mud when wet.
Citation: Race report, 2024 Mid South
```

### ❌ BAD Example:

```
Mile 60: The Grind Begins. Aid station two. 40 miles left. Mental game starts here.
```

**Why it's bad:** Generic milestone with no specific terrain details, no named sections, no actionable information.

## Data Structure

### Enhanced Suffering Zone Format:

```json
{
  "mile": 60,
  "label": "The Grind Begins",
  "desc": "Aid station two. 40 miles left. Mental game starts here.",
  "terrain_detail": "Course turns north into prevailing winds. Exposed red clay sections.",
  "named_section": "The Roller Coaster",
  "weather_note": "Fast and tactical when dry, unrideable mud when wet.",
  "citation": "Race report, 2024 Mid South"
}
```

### Required Fields:
- `mile`: Mile marker (integer)
- `label`: Section name/title
- `desc`: Base description

### Optional Fields (use when available):
- `terrain_detail`: Specific terrain description (climbs, descents, surface type)
- `named_section`: Named climb/section if applicable
- `weather_note`: Weather-dependent behavior
- `citation`: Source for specific claims

### If No Specific Details Available:

- **Don't write generic milestone copy**
- **Skip that section entirely**, OR
- **Write:** `"Details about course character at this point not available in public sources"`

## Citation Standards

### When to Cite:

- ✅ **Cite:** Specific terrain claims ("12-15% punches", "exposed clay sections")
- ✅ **Cite:** Named sections from race reports
- ✅ **Cite:** Weather-dependent behavior from specific sources
- ✅ **Cite:** Statistics or data from race reports

### When NOT to Cite:

- ❌ General race character descriptions
- ❌ Common knowledge about the race
- ❌ Your own analysis/interpretation

### Citation Format:

- `"Race report, 2024 Mid South"`
- `"Strava segment: The Roller Coaster"`
- `"Organizer course description"`
- `"Race report, [blog name], 2024"`

## Example Research Process

### Query 1: "Mid South mile 60 course terrain difficult"

**Find:** Race report mentioning "Mile 60 is where the course turns north into the wind and the exposed clay sections begin"

**Write:**
```json
{
  "mile": 60,
  "label": "The Grind Begins",
  "desc": "Aid station two marks the start of exposed terrain.",
  "terrain_detail": "Course turns north into prevailing winds. Exposed red clay sections begin here.",
  "weather_note": "Fast and tactical when dry, unrideable mud when wet.",
  "citation": "Race report, 2024 Mid South"
}
```

### Query 2: "Unbound 200 mile 85 course"

**Find:** Strava segment "Final Flint Hills Push" starting at mile 85

**Write:**
```json
{
  "mile": 85,
  "label": "The Final Push",
  "desc": "Last 15 miles through signature terrain.",
  "named_section": "Final Flint Hills Push",
  "terrain_detail": "Signature Flint Hills rollers. This section breaks more people than the entire first 100 miles.",
  "citation": "Strava segment: Final Flint Hills Push"
}
```

## Quality Checklist

Before adding a suffering zone, verify:

- [ ] Has specific terrain details (not just "it gets hard")
- [ ] Includes mileage point and context
- [ ] Mentions named sections if applicable
- [ ] Notes weather-dependent behavior if relevant
- [ ] Cites sources for specific claims
- [ ] Provides actionable information for riders

## Integration with Generator

The generator (`generate_course_map_html()`) automatically:

1. Displays enhanced details when available
2. Formats citations below zone descriptions
3. Handles missing optional fields gracefully
4. Adds research note explaining data sources

## Future Enhancements

- Add support for multiple citations per zone
- Add support for elevation profiles at specific zones
- Add support for photos/images at suffering zones
- Add support for Strava segment embeds

