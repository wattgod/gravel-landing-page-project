# GitHub Push Instructions

## Current Status

✅ Git repository initialized
✅ All core files committed (134 files, 23,514+ lines)
✅ Documentation added

## Files Committed

- **Core System:**
  - `races/generate_race_plans.py` - Main orchestrator
  - `races/generation_modules/` - All generation logic
  - `races/race_schema_template.json` - Race JSON schema
  - `races/unbound_gravel_200.json` - Example race data

- **Plan Templates:**
  - All 15 plan templates in `plans/` directory
  - Each with `template.json` containing full workout structure

- **Documentation:**
  - `WORKFLOW_DOCUMENTATION.md` - Complete system documentation
  - `README.md` - Quick start guide
  - `races/INTEGRATION_SUMMARY.md` - Copy variations integration notes

## What's NOT Committed (by design)

- Generated race outputs (`races/[Race Name]/workouts/`) - These are generated, not source
- Test files and temporary outputs
- Google API credentials (if added later)

## Push to GitHub

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `gravel-god-training-plans` (or your preferred name)
3. Description: "Automated race-specific training plan generation system"
4. **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

### Step 2: Push to GitHub

Run these commands in the project directory:

```bash
cd ~/Documents/"Gravel Landing Page Project/current"

# Add remote (replace YOUR_USERNAME and YOUR_REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Or use SSH (if you have SSH keys set up):
# git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 3: Verify

Check your GitHub repository - you should see:
- All plan templates
- Generation modules
- Documentation files
- Example race data (Unbound Gravel 200)

## Repository Structure on GitHub

```
gravel-god-training-plans/
├── README.md
├── WORKFLOW_DOCUMENTATION.md
├── GITHUB_PUSH_INSTRUCTIONS.md
├── .gitignore
├── races/
│   ├── generate_race_plans.py
│   ├── generation_modules/
│   │   ├── zwo_generator.py
│   │   ├── marketplace_generator.py
│   │   ├── guide_generator.py
│   │   └── gravel_god_copy_variations.py
│   ├── race_schema_template.json
│   ├── unbound_gravel_200.json
│   └── README.md
└── plans/
    ├── 1. Ayahuasca Beginner (12 weeks)/
    ├── 2. Ayahuasca Intermediate (12 weeks)/
    └── ... (15 total plan templates)
```

## Future Updates

To push future changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

## Notes

- The `.gitignore` excludes generated outputs (workouts, marketplace HTML, guides)
- Only source files and templates are committed
- Generated files are created locally when you run the generator
- This keeps the repository clean and focused on the generation system

