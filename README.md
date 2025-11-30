# Gravel God Training Plan Generation System

Automated system for generating race-specific training plans with 15 plan variants per race.

## Quick Start

1. Create a race JSON file (see `races/race_schema_template.json`)
2. Run: `python3 races/generate_race_plans.py races/[race_name].json`
3. Output: `races/[Race Name]/[15 Plan Folders]/` with workouts, marketplace descriptions, and guides

## Documentation

See [WORKFLOW_DOCUMENTATION.md](WORKFLOW_DOCUMENTATION.md) for complete system documentation.

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

