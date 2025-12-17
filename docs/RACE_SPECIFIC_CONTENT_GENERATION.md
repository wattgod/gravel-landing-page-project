# Race-Specific Content Pool Generation

## Overview

The marketplace description generator now **automatically extracts race-specific content** from race JSON files and research documents to create unique content pools for each race. This ensures every marketplace description includes race-specific references without manual configuration.

## How It Works

### Automatic Content Extraction

When generating marketplace descriptions, the system:

1. **Reads the race JSON file** (`races/{race_name}.json`)
2. **Extracts content from:**
   - `race_metadata` (name, location, distance)
   - `race_characteristics` (terrain, weather, climate)
   - `race_hooks` (punchy, detail hooks)
   - `non_negotiables` (requirements and explanations)
3. **Optionally reads research documents** (`docs/COURSE_BREAKDOWN_RESEARCH.md`)
4. **Generates content pools** for 5 categories:
   - **Terrain**: Race-specific terrain references
   - **Weather**: Climate and weather conditions
   - **Location**: Geographic references
   - **Character**: Race personality/culture
   - **Challenges**: Specific race challenges

### Content Pool Categories

#### Terrain References
Extracted from:
- `race_characteristics.terrain` (e.g., "red_clay", "flint_hills")
- `race_metadata.location` + terrain type
- `non_negotiables` mentioning terrain (e.g., "red clay", "flint")

**Examples:**
- Mid South: "Oklahoma red clay", "red clay terrain", "red clay that becomes unrideable mud when wet"
- Unbound: "Flint Hills", "Flint-specific cornering"

#### Weather References
Extracted from:
- `race_characteristics.climate` (e.g., "unpredictable", "hot")
- `race_characteristics.typical_weather` (e.g., "40-75°F swings", "85-95°F")
- `non_negotiables` mentioning weather

**Examples:**
- Mid South: "weather lottery", "unpredictable weather", "40-75°F temperature swings"
- Unbound: "June heat", "85-95°F conditions", "heat that breaks people"

#### Location References
Extracted from:
- `race_metadata.location` (e.g., "Stillwater, Oklahoma")
- `race_metadata.distance_miles` + location

**Examples:**
- Mid South: "Stillwater, Oklahoma", "100 miles of Stillwater"
- Unbound: "Emporia, Kansas", "200 miles of Emporia"

#### Character References
Extracted from:
- `race_hooks.punchy` (e.g., "Bobby Wintle hugs every finisher")
- `race_hooks.detail` (e.g., "unreasonable hospitality")
- `non_negotiables` mentioning race character

**Examples:**
- Mid South: "Bobby Wintle hugs every finisher", "tactical pack racing"
- Unbound: (extracted from hooks if available)

#### Challenge References
Extracted from:
- `non_negotiables[].why` explanations
- Specific challenges mentioned in requirements

**Examples:**
- Mid South: "red clay becomes unrideable peanut butter mud when wet", "weather turns mid-race"
- Unbound: "heat that breaks people", "Flint-specific cornering and line selection"

## Integration into Marketplace Descriptions

Race-specific references are automatically inserted into:

1. **Training Approach Section** (paragraph 2):
   - Format: "The [Plan] builds systems for [Race]'s [terrain/weather reference] that work/function..."
   - Each plan gets unique references based on tier+level seed

2. **Plan Features Section**:
   - Adds race-specific challenges (e.g., "red clay becomes unrideable mud when wet")

3. **Guide Content Summary**:
   - Adds "Mid South-specific: [reference]" in Race-Specific Preparation section

## Uniqueness Guarantee

- Uses `tier_key + level_key + category` as seed for consistent but varied references
- Each plan gets different race-specific references
- Tracks used references to avoid duplicates within a description
- All regression tests pass (no duplicate content violations)

## Adding a New Race

**No manual configuration needed!** Just:

1. Create `races/{race_name}.json` with:
   - `race_metadata` (name, location, distance)
   - `race_characteristics` (terrain, weather, climate)
   - `race_hooks` (punchy, detail)
   - `non_negotiables` (requirements with "why" explanations)

2. Optionally add race-specific content to `docs/COURSE_BREAKDOWN_RESEARCH.md`

3. Run `python3 races/generate_race_plans.py races/{race_name}.json`

The system will automatically:
- Extract race-specific content from the JSON
- Build content pools for all 5 categories
- Integrate unique references into marketplace descriptions
- Ensure no duplicate content across plans

## Example: Mid South

**Input (from `mid_south.json`):**
```json
{
  "race_metadata": {
    "name": "Mid South",
    "location": "Stillwater, Oklahoma",
    "distance_miles": 100
  },
  "race_characteristics": {
    "terrain": "red_clay",
    "climate": "unpredictable",
    "typical_weather": "Weather lottery: 40-75°F swings..."
  },
  "race_hooks": {
    "punchy": "100 miles of Oklahoma red clay. Weather lottery that decides your race. Bobby Wintle hugs every finisher."
  },
  "non_negotiables": [
    {
      "why": "Oklahoma red clay becomes unrideable peanut butter mud when wet."
    }
  ]
}
```

**Output (automatic content pools):**
- Terrain: 5 references (Oklahoma red clay, red clay terrain, etc.)
- Weather: 6 references (weather lottery, unpredictable weather, etc.)
- Location: 3 references (Stillwater, Oklahoma, etc.)
- Character: 5 references (Bobby Wintle, tactical pack racing, etc.)
- Challenges: 4 references (mud conditions, weather turns, etc.)

**Result:** Each marketplace description includes 1-3 unique Mid South references, making it clear the plan is race-specific.

## Testing

Run regression tests to verify:
```bash
python3 test_regression_marketplace.py
```

Tests verify:
- No duplicate content across plans
- No duplicate content within tiers
- Character limits
- All required sections present
