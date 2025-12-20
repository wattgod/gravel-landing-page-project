# HANDOFF: Sub-200 Participant Gravel Race Research

## CONTEXT

We built a Global Gravel Race Database with 222 races. Current database skews toward larger events (500+ riders). To reach comprehensive coverage (387+ races), we need to capture smaller regional/local events.

**Why sub-200 matters:**
- Often ZERO training plan competition (untapped markets)
- Loyal local communities = word-of-mouth potential
- Lower TAM but higher conversion rates (serious participants)
- Pipeline races that feed into larger events
- Some are hidden gems with cult followings

---

## WHAT EXISTS

**File:** `data/gravel_race_database.json` (in project)
- 247 races currently (after enhancements)
- Columns: Race Name, Location, Country, Region, Date/Month, Distance, Elevation, Field Size, Entry Cost, Tier, Competition, Protocol Fit, Priority Score, Notes, _data_quality, _sources, _last_verified

**Current Coverage Gaps (sub-200 events):**
- US Southeast: Many small events missing
- US Midwest: Regional series events missing
- Mountain West: Local CO/UT/AZ events missing
- International: Smaller European events, all of Asia basically

---

## TASK FOR NEXT CHAT

Research and compile gravel races with field sizes under 200 participants.

**Target:** 100-150 additional races

**Priority Regions:**
1. **US Southeast** - Fastest growing gravel region, underserved
2. **US Upper Midwest** - Minnesota, Wisconsin, Iowa small events
3. **US Mountain West** - Local Colorado, Utah, Arizona events
4. **UK Regional** - Beyond Dirty Reiver/Gralloch
5. **European Regional** - Germany, France, Benelux small events
6. **Australia Regional** - State-level events

**Data to collect per race:**
```
- Race Name
- Location (City, State/Country)
- Country
- Region
- Date/Month
- Distance (primary option in miles)
- Elevation (ft)
- Field Size (estimate if needed)
- Entry Cost ($)
- Tier (likely 3 or 4 for sub-200)
- Competition (likely NONE)
- Protocol Fit (Standard/Altitude/Heat/Technical/etc)
- Priority Score (1-10, likely 4-6 range)
- Notes (unique characteristics, growth potential)
- Data Quality (Verified/Estimated/Unknown)
- Sources (where data came from)
```

---

## RESEARCH SOURCES TO CHECK

**US Events:**
- BikeReg.com (filter by gravel, sort by date)
- USACycling.org event calendar
- State cycling association calendars
- Regional gravel Facebook groups
- Local bike shop event listings
- Strava local clubs

**Series to Enumerate:**
- Ironbear 1000 Gravel Series (12 races, Wisconsin) - ✅ Already in database
- Michigan Gravel Race Series (5 races) - ✅ Already in database
- Oregon Triple Crown Series (7 races) - ✅ Already in database
- Pennsylvania Gravel Series (5 races) - ✅ Already in database
- Canadian Gravel Cup (3 races) - ✅ Already in database
- State championship events

**International:**
- UCI Gravel World Series qualifiers list
- National federation calendars (British Cycling, Cycling Australia, etc.)
- European gravel race aggregators
- Komoot/Strava popular gravel routes with associated events

---

## RACES ALREADY FLAGGED AS MISSING

Add these first (identified in review):
1. **Highlands Gravel Classic** (Arkansas) - UCI Qualifier, should be Tier 1 - ✅ Already in database
2. **USA Cycling Gravel National Championships** (La Crescent, MN) - ✅ Already in database
3. **Red Granite Grinder** (Wisconsin) - ✅ Already in database
4. **Nordic Chase Gravel Edition** (800km ultra) - ✅ Already in database
5. **Collegiate Gravel Nationals** (2026 debut) - ✅ Already in database

**Note:** All flagged races are already in our database. Focus on finding NEW sub-200 events.

---

## OUTPUT FORMAT

Add directly to `data/gravel_race_database.json` using the same structure:

```json
{
  "Race Name": "Example Local Gravel",
  "Location": "Somewhere NC",
  "Country": "USA",
  "Region": "Southeast",
  "Date/Month": "April",
  "Distance (mi)": "50",
  "Elevation (ft)": "3500",
  "Field Size": "150",
  "Entry Cost": "$50-75",
  "Tier": 3,
  "Competition": "NONE",
  "Protocol Fit": "Standard",
  "Priority Score": 5,
  "Notes": "Growing local event",
  "_data_quality": {
    "field_size": "Estimated",
    "competition": "Estimated",
    "elevation": "Estimated"
  },
  "_sources": ["BikeReg", "Web research"],
  "_last_verified": "2024-12-19"
}
```

---

## PRIORITY SCORING FOR SUB-200 EVENTS

Use this simplified rubric:

| Factor | Weight | Scoring |
|--------|--------|---------|
| Growth Potential | 3x | High=3, Med=2, Low=1 |
| Competition Gap | 3x | NONE=3, LOW=2, MED=1 |
| Protocol Fit | 2x | Unique=2, Standard=1 |
| Community Strength | 2x | Strong=2, Unknown=1 |

**Score = (Growth×3) + (Competition×3) + (Protocol×2) + (Community×2) / 2**

Range: 4-10 for sub-200 events (most will be 4-6)

**Or use the existing formula from `enhance_global_db.py`:**
```
Score = (Field_Size_Tier × 3) + (Competition_Gap × 4) + (Protocol_Fit × 2) + (Prestige × 1)
Normalized to 1-10 scale
```

---

## START PROMPT FOR NEXT CHAT

```
Continue Gravel God race database project.

CONTEXT:
- Built master database with 247 races (data/gravel_race_database.json)
- Need to add sub-200 participant events to reach comprehensive coverage
- Target: 100-150 additional smaller races

HANDOFF DOC: HANDOFF_SUB200_RACE_RESEARCH.md

TASK:
1. Research gravel races with field sizes under 200 participants
2. Prioritize: US Southeast, Upper Midwest, Mountain West, UK/Europe regional
3. Include series events (check if already in database first)
4. Add missing high-priority races (check database first - most are already there)
5. Add directly to gravel_race_database.json
6. Include Data Quality flags, sources, and timestamps

START WITH:
- Verify the 5 flagged missing races are in database (they should be)
- Then systematically search BikeReg, USAC calendar, state associations
- Group by region for efficient research
- Use web_search tool extensively
- Add races in batches as you find them

Ready to start?
```

---

## SUCCESS CRITERIA

- [ ] 100+ new races added
- [ ] All flagged missing races verified (likely already in database)
- [ ] Regional series fully enumerated (check database first - many already there)
- [ ] Data Quality column populated for all new races
- [ ] Sources and timestamps added
- [ ] No duplicate entries with existing 247 races
- [ ] Database updated and committed to GitHub

---

## NOTES

- Don't worry about perfect data - "Estimated" quality is fine
- Prioritize breadth over depth for this pass
- Can always verify/enhance individual races later
- Sub-200 events likely all have NONE competition on TrainingPeaks
- Many will be Tier 3-4, Priority 4-6, and that's fine
- **Check existing database first** - many races may already be there
- Use the enhancement script's priority score formula for consistency

**Goal is comprehensive market map, not just high-TAM events.**

---

## DATABASE ENHANCEMENTS TO USE

**Priority Score Formula (from `automation/enhance_global_db.py`):**
```python
Score = (Field_Size_Tier × 3) + (Competition_Gap × 4) + (Protocol_Fit × 2) + (Prestige × 1)
Normalized to 1-10 scale
```

**Data Quality Flags:**
- Verified: Confirmed from official source
- Estimated: Reasonable estimate, needs verification
- Unknown: No data available

**Required Fields for New Races:**
- All standard fields (Race Name, Location, etc.)
- `_data_quality` object with field statuses
- `_sources` array
- `_last_verified` timestamp
- `_added_date` timestamp

---

## CURRENT DATABASE STATUS

- **Total Races:** 247
- **Enhanced Database:** `data/gravel_race_database_enhanced.json`
- **Priority Scores:** All calculated using formula
- **Data Quality:** All races flagged
- **Source Tracking:** Complete

**Target After Sub-200 Research:** 347-397 races total
