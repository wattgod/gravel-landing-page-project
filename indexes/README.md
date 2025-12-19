# Landing Page Index Files

Structured JSON index files for each race landing page, enabling searchable database creation.

## What Are These?

Each landing page generates a companion `{race-slug}-index.json` file containing all searchable/filterable data extracted from the race data. These indexes enable building a searchable race database without re-parsing HTML.

## File Structure

```
output/
├── belgian-waffle-ride-landing-page.json    (Elementor JSON)
└── belgian-waffle-ride-index.json           (Searchable index)

indexes/                                      (Optional: centralized location)
└── belgian-waffle-ride-index.json
```

## Index File Structure

Each index contains:

### Core Data
- `race_id`, `race_name`, `race_slug`
- `tier`, `tier_label`
- `tagline`, `race_date`

### Course Characteristics
- Distance, elevation, terrain type
- Signature challenge, character description
- Key features, suffering zones
- Climate information

### Ratings
- Overall score, tier
- Length, technicality, elevation scores
- Climate, altitude, adventure, logistics scores

### Biased Opinion
- Course quality, organization, value, atmosphere
- Overall biased opinion score

### TLDR
- Best for / Not for
- Key considerations

### Logistics
- Location (city, state, county)
- Venue, parking, lodging
- Registration info, start time, field size

### Final Verdict
- Overall score
- Recommendation
- Best for riders
- Key strengths, considerations

### Search & Filter
- `searchable_text`: All text concatenated for full-text search
- `filter_tags`: Pre-computed tags for quick filtering UI

## Use Cases

### 1. Full-Text Search
```javascript
// Search across all races
const searchTerm = "sand technical singletrack";
const results = indexes.filter(index => 
  index.searchable_text.toLowerCase().includes(searchTerm.toLowerCase())
);
```

### 2. Filter by Tags
```javascript
// Filter by multiple criteria
const results = indexes.filter(index => 
  index.filter_tags.includes('tier-1') &&
  index.filter_tags.includes('distance-long') &&
  index.filter_tags.includes('terrain-sand')
);
```

### 3. Range Filters
```javascript
// Filter by distance range
const results = indexes.filter(index => 
  index.course.distance_miles >= 100 &&
  index.course.distance_miles <= 150
);

// Filter by elevation
const results = indexes.filter(index => 
  index.course.elevation_gain_feet >= 10000
);
```

### 4. Location-Based Search
```javascript
// Find races in a state
const results = indexes.filter(index => 
  index.logistics.state === 'California'
);

// Find races in a region
const results = indexes.filter(index => 
  index.logistics.county.includes('San Diego')
);
```

### 5. Rating-Based Sorting
```javascript
// Sort by overall score
const sorted = indexes.sort((a, b) => 
  (b.ratings.overall_score || 0) - (a.ratings.overall_score || 0)
);

// Find highest-rated races
const topRaces = indexes
  .filter(index => index.ratings.overall_score >= 85)
  .sort((a, b) => b.ratings.overall_score - a.ratings.overall_score);
```

## Building a Searchable Database

### Option 1: Static JSON Database
1. Collect all index files into `indexes/` directory
2. Create `indexes/all-races.json` with array of all indexes
3. Load in frontend and filter client-side

### Option 2: Server-Side API
1. Load all indexes into memory or database
2. Create API endpoints:
   - `GET /api/races?tier=1&distance=long`
   - `GET /api/races/search?q=sand+technical`
   - `GET /api/races?state=California`

### Option 3: Static Site Generator
1. Use indexes to generate static HTML pages
2. Create filter pages: `/races/tier-1/`, `/races/distance-long/`
3. Generate search index for client-side search

## Filter Tags Reference

### Distance
- `distance-short` (< 50 miles)
- `distance-medium` (50-100 miles)
- `distance-long` (100-150 miles)
- `distance-ultra` (150+ miles)

### Elevation
- `elevation-moderate` (< 5,000 ft)
- `elevation-high` (5,000-10,000 ft)
- `elevation-extreme` (10,000+ ft)

### Terrain
- `terrain-gravel`
- `terrain-pavement`
- `terrain-singletrack`
- `terrain-sand`
- `terrain-water-crossings`

### Technical
- `technical-easy` (rating ≤ 2)
- `technical-moderate` (rating 3-4)
- `technical-hard` (rating 5+)

### Score
- `score-excellent` (90+)
- `score-very-good` (80-89)
- `score-good` (70-79)
- `score-fair` (< 70)

### Tier
- `tier-1`, `tier-2`, `tier-3`

## Generating All Indexes

```bash
# Generate index for single race
python3 scripts/generate_landing_page.py data/belgian-waffle-ride-data.json templates/elementor-base-template.json output/belgian-waffle-ride-landing-page.json

# Generate all indexes
python3 automation/generate_landing_page_index.py
```

## Example: Building a Filter UI

```javascript
// Load all indexes
const allRaces = await fetch('/indexes/all-races.json').then(r => r.json());

// Filter UI state
const filters = {
  tier: null,
  distance: null,
  elevation: null,
  terrain: [],
  state: null
};

// Apply filters
function filterRaces(races, filters) {
  return races.filter(race => {
    // Tier filter
    if (filters.tier && race.tier !== filters.tier) return false;
    
    // Distance filter
    if (filters.distance) {
      const tag = `distance-${filters.distance}`;
      if (!race.filter_tags.includes(tag)) return false;
    }
    
    // Terrain filters (multiple)
    if (filters.terrain.length > 0) {
      const hasAllTerrain = filters.terrain.every(t => 
        race.filter_tags.includes(`terrain-${t}`)
      );
      if (!hasAllTerrain) return false;
    }
    
    // State filter
    if (filters.state && race.logistics.state !== filters.state) return false;
    
    return true;
  });
}

// Search
function searchRaces(races, query) {
  const terms = query.toLowerCase().split(' ');
  return races.filter(race => {
    const text = race.searchable_text.toLowerCase();
    return terms.every(term => text.includes(term));
  });
}
```

## Next Steps

1. **Generate indexes for all races**: Run index generation for existing races
2. **Create aggregation script**: Combine all indexes into single file
3. **Build search UI**: Use indexes to power search/filter interface
4. **Add to website**: Integrate searchable database into Gravel God site
