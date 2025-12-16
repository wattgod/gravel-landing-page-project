# Gravel God Landing Page Generator

Automated system for generating Elementor JSON landing pages from race data.

## Quick Start

### Single Race Generation

```bash
# 1. Validate race data
python3 scripts/validate_race_data.py data/unbound-200-data.json

# 2. Generate landing page
python3 scripts/generate_landing_page.py \
  data/unbound-200-data.json \
  templates/elementor-base-template.json \
  output/elementor-unbound-200.json

# 3. Validate output
python3 scripts/validate_output.py output/elementor-unbound-200.json
```

### Batch Generation

```bash
# Generate all races in data/ directory
bash scripts/batch_generate.sh
```

## File Structure

```
/
├── data/
│   └── unbound-200-data.json          # Race data schema
├── templates/
│   └── elementor-base-template.json   # Base Elementor template
├── scripts/
│   ├── generate_landing_page.py      # Main generator
│   ├── validate_race_data.py         # Pre-generation validation
│   ├── validate_output.py            # Post-generation validation
│   └── batch_generate.sh             # Batch processing
└── output/
    └── elementor-*.json               # Generated files
```

## Race Data Schema

Each race data file must follow the schema defined in `docs/skills/ELEMENTOR_LANDING_PAGE_AUTOMATION.md`.

**Required fields:**
- `race.name`, `race.slug`, `race.display_name`, `race.tagline`
- `race.vitals` (distance, elevation, location, etc.)
- `race.gravel_god_rating` (scores and ratings)
- `race.ratings_breakdown` (7 categories with explanations)
- `race.training_plans` (all 15 plans with TP URLs)
- `race.black_pill` (reality check content)

## Validation

### Pre-Generation Checks

Validates race data completeness:
- All required fields present
- TrainingPeaks plan count matches actual plans
- All plans have TP IDs and slugs
- All 7 rating categories present

```bash
python3 scripts/validate_race_data.py data/unbound-200-data.json
```

### Post-Generation Checks

Validates generated Elementor JSON:
- No unreplaced template placeholders (`{{VARIABLE}}`)
- JSON is valid and parseable
- Expected section IDs present
- TrainingPeaks URLs are well-formed

```bash
python3 scripts/validate_output.py output/elementor-unbound-200.json
```

## Importing to WordPress

1. **Export generated JSON:**
   ```bash
   cp output/elementor-unbound-200.json ~/Downloads/
   ```

2. **Import to Elementor:**
   - WordPress → Elementor → Tools → Import Template
   - Upload the JSON file
   - Publish page with slug `/races/unbound-200`

3. **Spot-check:**
   - Mobile responsive working?
   - All TP links working?
   - Images loading?
   - Navigation anchors working?

## Troubleshooting

### "Widget not found" warnings

The generator searches for widgets by:
1. Element ID (`_element_id` in settings)
2. Content pattern (e.g., `gg-hero-inner`)

If a widget isn't found, check:
- Base template has the expected HTML structure
- Element IDs match between template and generator

### Validation failures

**Missing fields:**
- Check race data JSON matches schema exactly
- Use `validate_race_data.py` to identify missing fields

**Unreplaced placeholders:**
- Check HTML generation functions are using correct data paths
- Verify all template variables are being substituted

**Malformed TP URLs:**
- Check `category` field in plan data (should be `gran-fondo-century` or `road-cycling`)
- Verify `tp_id` and `tp_slug` are correct

## Adding New Races

1. **Create race data file:**
   ```bash
   cp data/unbound-200-data.json data/new-race-data.json
   # Edit with new race information
   ```

2. **Validate:**
   ```bash
   python3 scripts/validate_race_data.py data/new-race-data.json
   ```

3. **Generate:**
   ```bash
   python3 scripts/generate_landing_page.py \
     data/new-race-data.json \
     templates/elementor-base-template.json \
     output/elementor-new-race.json
   ```

4. **Validate output:**
   ```bash
   python3 scripts/validate_output.py output/elementor-new-race.json
   ```

## Time Savings

- **Manual:** 7-8 hours per page
- **Automated:** 40 minutes per page
- **10 races:** 70 hours → 7 hours (10x compression)
- **20 races:** 140 hours → 13 hours (10.8x compression)

## Success Criteria

✅ **Phase 1 Complete:**
- Generator runs without errors
- Output JSON is valid and imports to Elementor
- Regenerated page looks identical to original
- All 15 TrainingPeaks links work

✅ **Phase 2 Complete:**
- Validation scripts catch missing fields
- Validation scripts catch un-replaced placeholders
- Both validators return clear error messages

✅ **Phase 3 Complete:**
- Batch script generates multiple races successfully
- All outputs pass validation
- README is clear enough for non-technical user

## Notes

- Use UTF-8 encoding for all file operations
- JSON output is pretty-printed (indent=2) for debugging
- Generator includes helpful print statements showing progress
- Missing data is handled gracefully (doesn't crash on None values)


