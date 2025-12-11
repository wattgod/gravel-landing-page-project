# MARKETPLACE DESCRIPTION QC SYSTEM

## **STOP. READ THIS FIRST.**

**Before showing Matti ANYTHING, run:**
```bash
make qc
```

If it fails, **FIX IT**. Do not show Matti broken output.

---

## WHY THIS EXISTS

Matti is sick of back-and-forth iteration catching obvious issues.

This QC system catches:
- Missing required elements (guide intrigue line, etc.)
- Character count violations
- Old template artifacts
- Masters plans missing Masters content
- Repetitive patterns
- Placeholder text
- Forbidden patterns

**Run QC BEFORE every review. No exceptions.**

---

## COMMANDS (USE THESE IN CURSOR)

### 1. Full QC (use this 99% of the time)
```bash
make qc
```
Validates variation pools + generated descriptions.
**This is what you run before showing Matti.**

### 2. Quick checks
```bash
make validate-pools    # Check variation pools only
make validate-output   # Check generated HTML only
```

### 3. Generate + validate
```bash
make generate
```
Generates all 15 descriptions, then runs QC automatically.

### 4. Clean slate
```bash
make clean
```
Removes generated files for fresh start.

---

## WHAT GETS VALIDATED

### VARIATION POOLS (`validate_variation_pools.py`)
✓ All tiers have correct number of variations
✓ No duplicate content
✓ No placeholder text ([TODO], [REPLACE], etc.)
✓ No forbidden old template content
✓ Masters content exists in Finisher/Compete tiers
✓ Reasonable content length

### GENERATED DESCRIPTIONS (`validate_descriptions.py`)
✓ Character count under 3700 (warning) and 4000 (hard limit)
✓ Required elements present:
  - Opening (24px bold)
  - Story paragraph
  - Plan name header
  - Guide header + intrigue line + topics
  - Alternative? header + behavioral mirror
  - Value prop box + philosophy + props
  - Closing (one-two punch)
  - Footer with URL + branding
✓ No old template artifacts:
  - No bullets in main sections
  - No "Pain/Problem" boxes
  - No "You Should Buy This If"
  - No race header at top
  - No "This isn't generic" opening
✓ Masters plans have Masters-specific content
✓ No repetitive closing patterns
✓ Proper em dash usage (—, not -)

---

## TYPICAL WORKFLOW IN CURSOR

### Scenario 1: Making changes to variation pools
```bash
# 1. Edit variation pool file (e.g., TIER_SPECIFIC_SOLUTION_STATE_V3.py)
# 2. Validate pools
make validate-pools

# 3. If passed, regenerate + validate
make generate

# 4. If passed, show Matti
```

### Scenario 2: Tweaking generator
```bash
# 1. Edit generate_html_marketplace_descriptions.py
# 2. Generate + validate
make generate

# 3. If passed, show Matti
```

### Scenario 3: Before showing Matti ANYTHING
```bash
make qc
```
**If it fails, DO NOT show Matti. Fix first.**

---

## ERROR CODES

Scripts return:
- `0` = All checks passed (safe to show Matti)
- `1` = Validation failed (DO NOT show Matti)

---

## ADDING NEW VALIDATION RULES

Edit `validate_descriptions.py` or `validate_variation_pools.py`:

```python
# Add to REQUIRED_ELEMENTS
'new_element': r'regex pattern here',

# Add to FORBIDDEN_PATTERNS
'new_forbidden': r'regex pattern here',

# Add to MASTERS_KEYWORDS
'newkeyword',
```

Then test:
```bash
make qc
```

---

## WHAT TO DO WHEN QC FAILS

### Error: "Missing required element: guide_intrigue"
→ Guide intrigue line not in template
→ Check HTML_TEMPLATE has: `{guide_intrigue}`
→ Check generator selects: `guide_intrigue = random.choice(GUIDE_INTRIGUE_LINES)`

### Error: "Masters plan missing Masters-specific content"
→ Masters variation pools don't have Masters keywords
→ Add 2-3 variations per tier with: recovery, age, 40+, masters
→ Or: generator not using Masters-specific pools

### Error: "Character count exceeded"
→ Reduce variation text length
→ Or: use fewer features/topics (currently 3 each)

### Error: "Found forbidden pattern: generic_closing_start"
→ Old closing template still in use
→ Update CLOSING_STATEMENTS to remove "This isn't generic" openings

### Warning: "Guide intrigue line very short"
→ Acceptable if under 20 chars
→ Review GUIDE_INTRIGUE_LINES for quality

---

## INTEGRATION WITH CURSOR

### Run QC automatically before commit:
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
make qc || exit 1
```

### Run QC in Cursor terminal:
Just type: `make qc`

### Run QC before showing anything:
**ALWAYS RUN `make qc` BEFORE SHOWING MATTI**

---

## FILES IN QC SYSTEM

```
validate_variation_pools.py  - Checks variation pool structure/content
validate_descriptions.py     - Checks generated HTML files
run_all_qc.py               - Master script (runs all validations)
Makefile                    - Easy commands for Cursor
QC_README.md                - This file
```

---

## GOLDEN RULE

**If `make qc` fails, DO NOT show Matti until fixed.**

Period.

End of discussion.

No exceptions.

---

## QUESTIONS?

Read the script comments. They explain what each check does.

If you add new validation rules, document them above.

**Now go run `make qc`.**
