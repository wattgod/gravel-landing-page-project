# Gravel Race Database

**The most comprehensive gravel race database available.**

This database serves as the **source of truth** for all gravel race information used in landing page generation, SEO optimization, and race analysis.

---

## 📊 Database Overview

- **Total Races:** 246
- **Last Updated:** December 19, 2024
- **Format:** JSON and CSV
- **Coverage:** Global (21+ countries)

### Files

- `gravel_race_database.json` - Full database in JSON format
- `gravel_race_database.csv` - Full database in CSV format
- `gravel_race_database_summary.md` - Technical summary

---

## 🎯 Database Structure

Each race entry contains:

- **Race Name** - Official race name
- **Location** - City/State or City/Country
- **Country** - Primary country
- **Region** - Regional classification (USA regions, European countries, etc.)
- **Date/Month** - Typical race timing
- **Distance (mi)** - Race distances available
- **Elevation (ft)** - Elevation gain
- **Field Size** - Typical participant numbers
- **Entry Cost** - Registration fee range
- **Tier** - Race tier (1 = Premier, 2 = Major, 3 = Regional)
- **Competition** - Competition level (HIGH, MEDIUM, LOW, NONE)
- **Protocol Fit** - Training protocol category (Heat, Altitude, Climbing, etc.)
- **Priority Score** - Business priority (1-10)
- **Notes** - Additional context and details

---

## 📈 Coverage Statistics

### By Country
- **USA:** 164 races (67%)
- **Europe:** 40 races (16%)
- **Australia:** 14 races (6%)
- **South America:** 8 races (3%)
- **Canada:** 6 races (2%)
- **Africa:** 6 races (2%)
- **Asia:** 4 races (2%)

### By Tier
- **Tier 1 (Premier):** 62 races
- **Tier 2 (Major):** 126 races
- **Tier 3 (Regional):** 56 races

### By Competition Level
- **NONE:** 220 races (89%) - **Massive opportunity**
- **LOW:** 10 races (4%)
- **MEDIUM:** 12 races (5%)
- **HIGH:** 4 races (2%)

### UCI Gravel World Series
- **Coverage:** 29 of 33 events (88%)
- **Status:** Near-complete coverage

---

## 🏆 Key Race Series Included

### Complete Regional Series
- ✅ **Ironbear 1000 Gravel Series** (12 races) - Wisconsin
- ✅ **Michigan Gravel Race Series** (5 races)
- ✅ **Oregon Triple Crown Series** (7 races)
- ✅ **Pennsylvania Gravel Series** (5 races)
- ✅ **Canadian Gravel Cup** (3 races)

### Major Events
- ✅ **USA Cycling Gravel National Championships** (La Crescent, MN)
- ✅ **Highlands Gravel Classic** (Arkansas) - UCI qualifier
- ✅ **Gran Fondo Strade Bianche** (Italy)
- ✅ **Nordic Chase Gravel Edition** (800km ultra)
- ✅ **Collegiate Gravel Nationals** (Texas)

---

## 🎯 Priority Races

### Tier 1, Priority Score 10
- **Mid South** (Stillwater, OK)
- **Big Sugar** (Bentonville, AR)
- **Crusher in the Tushar** (Beaver, UT)
- **Rebecca's Private Idaho** (Ketchum, ID)
- **The Traka 360** (Girona, Spain)
- **Highlands Gravel Classic** (Fayetteville-Goshen, AR)
- **USA Cycling Gravel National Championships** (La Crescent, MN)

### User's Personal Favorites
- **Red Granite Grinder** (Athens, WI) - Priority Score 9

---

## 🔍 Using the Database

### JSON Format
```python
import json

with open('gravel_race_database.json') as f:
    data = json.load(f)
    
races = data['All Races']['rows']
for race in races:
    print(race['Race Name'], race['Location'])
```

### CSV Format
```python
import pandas as pd

df = pd.read_csv('gravel_race_database.csv')
# Filter by tier
tier1_races = df[df['Tier'] == 1]
# Filter by competition
no_competition = df[df['Competition'] == 'NONE']
```

### Common Queries

**Find all races with zero competition:**
```python
no_comp = [r for r in races if r.get('Competition') == 'NONE']
```

**Find all UCI World Series events:**
```python
uci_races = [r for r in races if 'UCI' in r.get('Race Name', '') or 'uci' in r.get('Notes', '').lower()]
```

**Find races by region:**
```python
midwest_races = [r for r in races if r.get('Region') == 'Midwest']
```

**Find races by protocol fit:**
```python
altitude_races = [r for r in races if 'Altitude' in r.get('Protocol Fit', '')]
```

---

## 📝 Maintenance

### Adding New Races
1. Update `gravel_race_database.json` with new race entry
2. Follow existing schema structure
3. Update this README if adding new series
4. Commit with descriptive message

### Data Quality Standards
- All races must have: Name, Location, Country, Region, Date/Month
- Tier should be assigned (1-3)
- Competition level should be assessed (HIGH/MEDIUM/LOW/NONE)
- Priority Score should reflect business value (1-10)
- Notes should include relevant context

### Validation
Run regression tests to ensure data quality:
```bash
python automation/test_race_data_quality.py
```

---

## 🚀 Integration

This database is used by:
- Landing page generation scripts (`scripts/generate_landing_page.py`)
- Race data JSON files (`data/*-data.json`)
- SEO optimization workflows
- Market analysis and opportunity identification

---

## 📚 Related Documentation

- `../automation/test_race_data_quality.py` - Data quality tests
- `../automation/fix_race_data_quality.py` - Automated data fixes
- `../MISSING_RACES_ANALYSIS.md` - Analysis of missing races
- `../DATABASE_EXPANSION_COMPLETE.md` - Expansion summary

---

## 🔗 External References

- [UCI Gravel World Series](https://ucigravelworldseries.com/)
- [USA Cycling Gravel](https://usacycling.org/)
- [Gravel Earth Series](https://gravel-earth.com/)

---

## 📊 Database History

- **December 19, 2024:** Massive expansion - Added 72+ races
  - Complete Ironbear 1000 series
  - 15 missing UCI World Series events
  - Complete regional series (Michigan, Oregon, Pennsylvania)
  - Nordic races, state championships, major international events
  - UCI coverage improved from 42% to 88%

- **December 19, 2024:** Initial database conversion from Excel
  - Converted `GRAVEL_RACE_DATABASE_MASTER.xlsx` to JSON/CSV
  - 222 races initially cataloged

---

## 💡 Market Insights

### Opportunity Analysis
- **89% of races have ZERO competition** - Massive first-mover advantage
- **Only 4 races have HIGH competition** - Market is wide open
- **Tier 1 races:** 62 total, many still need landing pages
- **Regional series:** Complete coverage of major series

### Strategic Priorities
1. **Tier 1, Priority 10 races** - Highest value, low competition
2. **UCI World Series events** - Prestige and international reach
3. **National Championships** - Official recognition
4. **Regional favorites** - Local market penetration
5. **Zero competition races** - Easy SEO wins

---

**Last Updated:** December 19, 2024  
**Maintained By:** Gravel God Cycling  
**License:** Internal use only
