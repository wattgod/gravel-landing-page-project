# GITHUB PUSH INSTRUCTIONS
# All 60 Unbound 200 Marketplace Descriptions

## REPOSITORY STRUCTURE

Add these files to your existing `gravel-landing-page-project` repository.

**Recommended location:**
```
gravel-landing-page-project/
├── marketplace_descriptions/
│   └── unbound_200/
│       ├── ayahuasca/          (15 files)
│       ├── finisher/           (15 files)
│       ├── compete/            (15 files)
│       ├── podium/             (15 files)
│       └── DESCRIPTION_MAPPING.md
└── (existing files)
```

---

## STEP-BY-STEP PUSH

### 1. Create directory structure in your repo

```bash
cd /path/to/gravel-landing-page-project
mkdir -p marketplace_descriptions/unbound_200
```

### 2. Copy all generated files

```bash
# Copy all 60 description files
cp -r /Users/mattirowe/Downloads/unbound_200/* marketplace_descriptions/unbound_200/

# Copy the mapping document
cp /Users/mattirowe/Downloads/TRAININGPEAKS_DESCRIPTION_MAPPING.md marketplace_descriptions/unbound_200/DESCRIPTION_MAPPING.md
```

### 3. Commit and push

```bash
git add marketplace_descriptions/
git commit -m "Add tier-specific marketplace descriptions for Unbound 200 (60 variations)"
git push origin main
```

---

## WHAT YOU'RE PUSHING

**Total:** 61 files
- 60 description files (.txt)
- 1 mapping document (.md)

**Breakdown:**
- `ayahuasca/` - 15 variations
- `finisher/` - 15 variations  
- `compete/` - 15 variations
- `podium/` - 15 variations

**Why push all 60?**
- Future A/B testing
- Swapping underperforming descriptions
- Reference library for other races
- Version control for copy changes

---

## FUTURE RACES

When you generate descriptions for Belgian Waffle Ride, Mid South, etc:

```bash
# Same structure
marketplace_descriptions/
├── unbound_200/
├── belgian_waffle_ride/
├── mid_south/
└── sbt_grvl/
```

Each race gets its own folder with 60 variations.

---

## ACCESSING FROM GITHUB

Once pushed, you can:
- Browse descriptions on GitHub web interface
- Clone repo on any computer to access files
- Share specific description URLs with collaborators
- Track which descriptions perform best via commit history

---

## UPDATING DESCRIPTIONS

If you want to refine copy later:

1. Edit the `.txt` file in your local repo
2. Commit the change with descriptive message
3. Push to GitHub
4. Copy updated description to TrainingPeaks

**Example:**
```bash
# Edit a description
nano marketplace_descriptions/unbound_200/finisher/finisher_advanced.txt

# Commit with context
git commit -am "Finisher Advanced: Strengthen race-execution copy"

# Push
git push origin main
```

---

## .GITIGNORE NOTES

Make sure these are NOT in your .gitignore:
- `*.txt` files (your descriptions)
- `marketplace_descriptions/` directory

If you have blanket ignores, add exceptions:
```gitignore
# Allow marketplace descriptions
!marketplace_descriptions/**/*.txt
!marketplace_descriptions/**/*.md
```

---

## VERIFYING THE PUSH

After pushing, check GitHub:
1. Navigate to your repo on github.com
2. Browse to `marketplace_descriptions/unbound_200/`
3. Confirm you see 4 folders + 1 markdown file
4. Open a few `.txt` files to verify content

---

## QUICK COMMANDS (Copy-Paste Ready)

```bash
# Navigate to your repo
cd /path/to/gravel-landing-page-project

# Create structure
mkdir -p marketplace_descriptions/unbound_200

# Copy all files from Downloads
cp -r ~/Downloads/unbound_200/* marketplace_descriptions/unbound_200/
cp ~/Downloads/TRAININGPEAKS_DESCRIPTION_MAPPING.md marketplace_descriptions/unbound_200/

# Add, commit, push
git add marketplace_descriptions/
git commit -m "Add tier-specific marketplace descriptions for Unbound 200"
git push origin main

# Verify
open https://github.com/YOUR_USERNAME/gravel-landing-page-project/tree/main/marketplace_descriptions
```

---

## DONE

All 60 descriptions preserved in version control.
Your 15 primary descriptions mapped.
Ready to update TrainingPeaks marketplace.
