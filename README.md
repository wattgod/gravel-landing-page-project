# Gravel God Landing Page & Training Plan System

Comprehensive system for generating race landing pages and race-specific training plans.

## 🗄️ Gravel Race Database

**Source of Truth:** [`data/gravel_race_database.json`](data/gravel_race_database.json)

- **246 races** cataloged globally
- **88% UCI World Series coverage** (29 of 33 events)
- **89% have ZERO competition** - massive SEO opportunity
- Complete regional series: Ironbear 1000, Michigan, Oregon, Pennsylvania, Canadian Gravel Cup

See [`data/README.md`](data/README.md) for complete database documentation, usage examples, and query patterns.

## Quick Start

### Landing Page Generation
1. Ensure race data exists in `data/[race-name]-data.json`
2. Run: `python3 scripts/generate_landing_page.py [race-slug]`
3. Output: Elementor JSON files in `landing-pages/[race-name]/`

### Training Plan Generation
1. Create a race JSON file (see `races/race_schema_template.json`)
2. Run: `python3 races/generate_race_plans.py races/[race_name].json`
3. Output: `races/[Race Name]/[15 Plan Folders]/` with workouts, marketplace descriptions, and guides

## Documentation

- **Database:** [`data/README.md`](data/README.md) - Complete database documentation
- **Workflow:** [WORKFLOW_DOCUMENTATION.md](WORKFLOW_DOCUMENTATION.md) - Training plan system docs

## Features

- **1,211 ZWO workout files** per race (varies by plan complexity)
- **15 marketplace HTML descriptions** with randomized copy variations
- **15 training plan guides** (placeholder for Google Docs integration)
- **Race-specific modifications:** Heat training, aggressive fueling, dress rehearsal, taper, mental prep
- **Position alternation guidance** for endurance/long rides
- **Copy variations** prevent duplicate marketplace descriptions

## Structure

```
current/
├── races/
│   ├── generation_modules/     # Core generation logic
│   ├── generate_race_plans.py  # Main orchestrator
│   └── [race_name].json        # Race data files
├── plans/                       # 15 plan templates
└── WORKFLOW_DOCUMENTATION.md    # Complete system docs
```

## Requirements

- Python 3.7+
- Standard library only (no external dependencies)

## License

Private - Gravel God Cycling

