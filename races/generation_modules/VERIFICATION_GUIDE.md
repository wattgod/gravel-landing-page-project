# Guide Verification System

This directory contains automated verification tools to ensure training guides are correctly structured before committing.

## Quick Start

### Verify All Guides

```bash
# Verify all guides in a directory
python3 races/generation_modules/verify_guide_structure.py docs/guides/unbound-gravel-200/ --skip-index

# Verify a single guide
python3 races/generation_modules/verify_guide_structure.py docs/guides/unbound-gravel-200/ayahuasca-beginner.html
```

### Automatic Verification

The verification script runs automatically after generating guides:

```bash
python3 races/generate_race_plans.py races/unbound_gravel_200.json
```

You'll see verification results at the end of the generation process.

## What Gets Checked

### 1. TOC Links Match Section IDs ✅
- Every TOC link (`href="#section-X"`) must have a matching section ID (`id="section-X"`)
- Prevents broken navigation

### 2. Required Sections Present ✅
- All 14 required sections must be present
- Conditional sections (Masters) are checked appropriately
- Non-Masters plans should NOT have Masters section

### 3. No Duplicate IDs ✅
- Allows 2 occurrences per section (normal: `<section id="...">` and `<h2 id="...">`)
- Flags if more than 2 occurrences found

### 4. Women-Specific Content ✅
- Verifies Women-Specific section exists
- Checks for key content markers:
  - "Women aren't small men"
  - "Menstrual Cycle and Training"
  - "Iron: The Critical Difference"

## Required Sections

See `REQUIRED_SECTIONS_CHECKLIST.md` for the complete list of required sections.

### Standard Plans (Non-Masters)
- Sections 1-12: Standard content
- Section 13: Women-Specific Considerations
- Section 14: FAQ

### Masters Plans
- Sections 1-12: Standard content
- Section 13: Masters-Specific Considerations
- Section 14: Women-Specific Considerations
- Section 15: FAQ

## Common Issues & Fixes

### Issue: TOC Links Don't Match Section IDs

**Symptom:**
```
TOC Mismatches:
  - TOC links to 'section-3-training-fundamentals' but no matching section ID found
```

**Fix:**
- Update TOC links in `guide_template_full.html` to match actual section IDs
- Sections 3-7, 9-11 use short IDs: `section-3`, `section-4`, etc.
- Sections 1, 2, 8, 12, 13, 14, 15 use full IDs: `section-1-training-plan-brief`, etc.

### Issue: Missing Women-Specific Section

**Symptom:**
```
Missing Sections:
  - Missing required section: section-13-women-specific-considerations
```

**Fix:**
- Ensure Women-Specific section is in `guide_template_full.html`
- Check generator renumbering logic handles it correctly

### Issue: Duplicate IDs (More Than 2)

**Symptom:**
```
Duplicate IDs:
  - Duplicate section ID 'section-1-training-plan-brief' found 3 times
```

**Fix:**
- Check template for accidental duplicate sections
- Normal: 2 occurrences (section tag + h2 tag)
- Problem: 3+ occurrences

## Integration with Git Workflow

### Pre-Commit Hook (Optional)

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Verify guides before committing
python3 races/generation_modules/verify_guide_structure.py docs/guides/unbound-gravel-200/ --skip-index
if [ $? -ne 0 ]; then
    echo "❌ Guide verification failed. Fix issues before committing."
    exit 1
fi
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

## Exit Codes

- `0`: All guides passed verification ✅
- `1`: Some guides failed verification ❌

Use in CI/CD pipelines:
```bash
python3 verify_guide_structure.py docs/guides/ && echo "✅ Verification passed" || exit 1
```


